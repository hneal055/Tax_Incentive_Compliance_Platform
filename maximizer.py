"""
SceneIQ Maximizer Engine
Optimizes tax incentive stacking across jurisdiction layers.

Usage:
    python maximizer.py 42.8864 -78.8784 --spend 5000000 --type all
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# ── US state bounding boxes (min_lat, max_lat, min_lng, max_lng) ──────────────
# Used for lat/lng → jurisdiction resolution without PostGIS.
_US_STATE_BOUNDS: Dict[str, Tuple[float, float, float, float]] = {
    "AL": (30.1, 35.0, -88.5, -84.9),
    "AK": (51.2, 71.4, -180.0, -130.0),
    "AZ": (31.3, 37.0, -114.8, -109.0),
    "AR": (33.0, 36.5, -94.6, -89.6),
    "CA": (32.5, 42.0, -124.5, -114.1),
    "CO": (37.0, 41.0, -109.1, -102.0),
    "CT": (40.9, 42.1, -73.7, -71.8),
    "DE": (38.4, 39.8, -75.8, -75.0),
    "FL": (24.5, 31.0, -87.6, -80.0),
    "GA": (30.4, 35.0, -85.6, -81.0),
    "HI": (18.9, 22.2, -160.2, -154.8),
    "ID": (42.0, 49.0, -117.2, -111.0),
    "IL": (36.9, 42.5, -91.5, -87.0),
    "IN": (37.8, 41.8, -88.1, -84.8),
    "IA": (40.4, 43.5, -96.6, -90.1),
    "KS": (37.0, 40.0, -102.1, -94.6),
    "KY": (36.5, 39.1, -89.6, -81.9),
    "LA": (28.9, 33.0, -94.1, -89.0),
    "ME": (43.1, 47.5, -71.1, -66.9),
    "MD": (37.9, 39.7, -79.5, -75.0),
    "MA": (41.2, 42.9, -73.5, -70.0),
    "MI": (41.7, 48.3, -90.4, -82.4),
    "MN": (43.5, 49.4, -97.2, -89.5),
    "MS": (30.2, 35.0, -91.7, -88.1),
    "MO": (36.0, 40.6, -95.8, -89.1),
    "MT": (44.4, 49.0, -116.0, -104.0),
    "NE": (40.0, 43.0, -104.1, -95.3),
    "NV": (35.0, 42.0, -120.0, -114.0),
    "NH": (42.7, 45.3, -72.6, -70.6),
    "NJ": (38.9, 41.4, -75.6, -73.9),
    "NM": (31.3, 37.0, -109.1, -103.0),
    "NY": (40.5, 45.0, -79.8, -71.9),
    "NC": (33.8, 36.6, -84.3, -75.5),
    "ND": (45.9, 49.0, -104.1, -96.6),
    "OH": (38.4, 42.3, -84.8, -80.5),
    "OK": (33.6, 37.0, -103.0, -94.4),
    "OR": (42.0, 46.3, -124.6, -116.5),
    "PA": (39.7, 42.3, -80.5, -74.7),
    "RI": (41.1, 42.0, -71.9, -71.1),
    "SC": (32.0, 35.2, -83.4, -78.5),
    "SD": (42.5, 45.9, -104.1, -96.5),
    "TN": (34.9, 36.7, -90.3, -81.7),
    "TX": (25.8, 36.5, -106.6, -93.5),
    "UT": (37.0, 42.0, -114.1, -109.0),
    "VT": (42.7, 45.0, -73.4, -71.5),
    "VA": (36.5, 39.5, -83.7, -75.2),
    "WA": (45.5, 49.0, -124.8, -116.9),
    "WV": (37.2, 40.6, -82.6, -77.7),
    "WI": (42.5, 47.1, -92.9, -86.8),
    "WY": (41.0, 45.0, -111.1, -104.1),
}


def _state_code_for_point(lat: float, lng: float) -> Optional[str]:
    """Return the best-matching US state code for a lat/lng point using bounding boxes."""
    matches = [
        code for code, (min_lat, max_lat, min_lng, max_lng) in _US_STATE_BOUNDS.items()
        if min_lat <= lat <= max_lat and min_lng <= lng <= max_lng
    ]
    if not matches:
        return None
    # If multiple states match (border areas), prefer smallest bounding box
    return min(
        matches,
        key=lambda c: (
            (_US_STATE_BOUNDS[c][1] - _US_STATE_BOUNDS[c][0]) *
            (_US_STATE_BOUNDS[c][3] - _US_STATE_BOUNDS[c][2])
        ),
    )


# ── Data classes ──────────────────────────────────────────────────────────────

@dataclass
class ApplicableRule:
    jurisdiction_id: str
    jurisdiction_name: str
    jurisdiction_type: str
    rule_key: str
    rule_type: str
    raw_value: float           # raw number from DB (percentage OR USD amount)
    value_unit: str            # 'percent' | 'USD'
    computed_value: float      # actual dollar value after applying qualified_spend
    inheritance_mode: str
    conflict_priority: int
    source_citation: str
    effective_date: datetime


@dataclass
class MaximizedResult:
    total_incentive_usd: float
    qualified_spend: Optional[float]
    effective_rate: Optional[float]         # total_incentive / qualified_spend
    breakdown: Dict[str, float]
    applied_rules: List[ApplicableRule]
    overridden_rules: List[ApplicableRule]
    conflicts_resolved: List[str]
    warnings: List[str]
    recommendations: List[str]
    jurisdictions_evaluated: int
    resolved_state: Optional[str] = None   # state code matched from lat/lng


# ── Engine ────────────────────────────────────────────────────────────────────

class SceneIQMaximizer:
    RULE_TYPE_MAP = {
        "tax_credit":    "credit",
        "tax_abatement": "tax_abatement",
        "rebate":        "rebate",
        "green_bonus":   "green_bonus",
        "permit_fee":    "permit_fee",
        "fee":           "permit_fee",
        "credit":        "credit",
    }

    HIERARCHY = {
        "federal": 0, "country": 0,
        "state": 1, "province": 1,
        "county": 2,
        "city": 3, "town": 3, "borough": 3,
        "village": 4, "district": 4, "special": 4,
    }

    def __init__(self, db_url: str = None):
        self.db_url = db_url or os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("DATABASE_URL not set")

    def _connect(self):
        return psycopg2.connect(self.db_url)

    # ── Spatial resolution ─────────────────────────────────────────────────────

    def resolve_jurisdictions_by_location(
        self,
        lat: float,
        lng: float,
    ) -> Tuple[List[Dict], Optional[str]]:
        """
        Return (jurisdictions, state_code) for a lat/lng using bounding-box
        matching.  Includes the matched state + all its direct sub-jurisdictions
        (counties/cities with parentId = state.id).
        """
        state_code = _state_code_for_point(lat, lng)
        if not state_code:
            return [], None

        conn = self._connect()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            # Get the state row
            cur.execute(
                "SELECT id, name, type, code FROM jurisdictions WHERE code = %s AND active = true",
                (state_code,),
            )
            state_row = cur.fetchone()
            if not state_row:
                return [], state_code

            # Get all sub-jurisdictions of that state
            cur.execute(
                """SELECT id, name, type, code FROM jurisdictions
                   WHERE "parentId" = %s AND active = true""",
                (state_row["id"],),
            )
            subs = cur.fetchall()
            return [dict(state_row)] + [dict(r) for r in subs], state_code
        finally:
            cur.close()
            conn.close()

    def resolve_jurisdictions_by_codes(
        self,
        codes: List[str],
    ) -> List[Dict]:
        """Return jurisdiction rows for explicit code list."""
        if not codes:
            return []
        conn = self._connect()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                "SELECT id, name, type, code FROM jurisdictions WHERE code = ANY(%s) AND active = true",
                (codes,),
            )
            return [dict(r) for r in cur.fetchall()]
        finally:
            cur.close()
            conn.close()

    # ── Rule fetching ──────────────────────────────────────────────────────────

    def fetch_rules(
        self,
        jurisdiction_ids: List[str],
        qualified_spend: Optional[float],
        project_type: str = "all",
        spend_by_location: Optional[Dict[str, float]] = None,
    ) -> Tuple[List[ApplicableRule], List[str]]:
        """
        Fetch applicable incentive rules for the given jurisdiction IDs.

        spend_by_location maps jurisdiction CODE → qualifying spend for that
        location (e.g. {"IL-COOK": 2_000_000}).  Rules whose jurisdiction has
        an explicit entry use that spend instead of qualified_spend, so bonuses
        tied to within-city spend (like IL-CHICAGO-BONUS) compute correctly for
        split-location shoots.  Jurisdictions not in spend_by_location fall back
        to qualified_spend.
        """
        if not jurisdiction_ids:
            return [], []

        # Exclude rules whose requirements JSON explicitly marks them as
        # inapplicable to the requested project type.
        # Currently enforced: tvSeries=true rules are skipped for film projects.
        tv_only_filter = ""
        if project_type.lower() == "film":
            tv_only_filter = (
                "AND (ir.requirements IS NULL "
                "     OR (ir.requirements::jsonb->>'tvSeries') IS NULL "
                "     OR (ir.requirements::jsonb->>'tvSeries') <> 'true')"
            )

        conn = self._connect()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            placeholders = ",".join(["%s"] * len(jurisdiction_ids))
            cur.execute(
                f"""
                SELECT
                    ir."jurisdictionId"                              AS jurisdiction_id,
                    j.name                                           AS jurisdiction_name,
                    j.type                                           AS jurisdiction_type,
                    j.code                                           AS jurisdiction_code,
                    ir."ruleCode"                                    AS rule_key,
                    ir."incentiveType"                               AS rule_type,
                    COALESCE(ir.percentage, ir."fixedAmount")        AS raw_value,
                    CASE WHEN ir.percentage IS NOT NULL THEN 'percent'
                         ELSE 'USD' END                              AS value_unit,
                    NULL                                             AS source_citation,
                    ir."effectiveDate"                               AS effective_date,
                    ir.requirements                                  AS requirements_json
                FROM incentive_rules ir
                JOIN jurisdictions j ON ir."jurisdictionId" = j.id
                WHERE ir."jurisdictionId" IN ({placeholders})
                    AND (ir."expirationDate" IS NULL OR ir."expirationDate" > NOW())
                    AND ir."effectiveDate" <= NOW()
                    AND ir.active = true
                    AND (ir.percentage IS NOT NULL OR ir."fixedAmount" IS NOT NULL)
                    {tv_only_filter}
                ORDER BY j.type, ir."ruleCode"
                """,
                jurisdiction_ids,
            )
            rows = cur.fetchall()
        finally:
            cur.close()
            conn.close()

        import json as _json
        rules = []
        opt_in_warnings: list[str] = []
        for r in rows:
            raw = float(r["raw_value"] or 0.0)

            # Determine the spend basis for this rule's jurisdiction.
            # If the caller provided per-location splits, use that jurisdiction's
            # specific spend; otherwise fall back to the overall qualified_spend.
            j_code = r.get("jurisdiction_code", "")
            if spend_by_location and j_code in spend_by_location:
                effective_spend = spend_by_location[j_code]
            else:
                effective_spend = qualified_spend

            if r["value_unit"] == "percent" and effective_spend is not None:
                computed = (raw / 100.0) * effective_spend
            else:
                computed = raw   # USD amount or raw % when no spend provided

            # Skip opt-in bonuses — they require production-specific elections
            # (e.g. Green Sustainability Plan, Relocation Series designation).
            # Surface them as informational warnings instead.
            req = r.get("requirements_json")
            if req:
                try:
                    req_data = _json.loads(req) if isinstance(req, str) else req
                    if req_data.get("optIn"):
                        dollar_str = (
                            f"${computed:,.0f}" if effective_spend else f"{raw:.0f}%"
                        )
                        opt_in_warnings.append(
                            f"{r['rule_key']} ({raw:.0f}% = {dollar_str}) requires "
                            f"opt-in election — not included in base total"
                        )
                        continue
                except (ValueError, TypeError):
                    pass

            rules.append(
                ApplicableRule(
                    jurisdiction_id=r["jurisdiction_id"],
                    jurisdiction_name=r["jurisdiction_name"],
                    jurisdiction_type=r["jurisdiction_type"],
                    rule_key=r["rule_key"],
                    rule_type=r["rule_type"],
                    raw_value=raw,
                    value_unit=r["value_unit"],
                    computed_value=computed,
                    inheritance_mode="additive",
                    conflict_priority=self.HIERARCHY.get(
                        (r["jurisdiction_type"] or "").lower(), 5
                    ),
                    source_citation=r["source_citation"] or "",
                    effective_date=r["effective_date"] or datetime.now(),
                )
            )
        return rules, opt_in_warnings

    # ── Inheritance logic ──────────────────────────────────────────────────────

    def apply_inheritance(
        self,
        rules: List[ApplicableRule],
    ) -> Tuple[List[ApplicableRule], List[ApplicableRule]]:
        """
        Group by rule_key.  Within each group:
        - additive: sum computed_value across all layers
        - override: higher-priority (lower level number) wins
        - strict: lower jurisdictions blocked
        """
        by_key: Dict[str, List[ApplicableRule]] = {}
        for r in rules:
            by_key.setdefault(r.rule_key, []).append(r)

        applied: List[ApplicableRule] = []
        overridden: List[ApplicableRule] = []

        for rule_key, group in by_key.items():
            group.sort(key=lambda x: (x.conflict_priority, x.rule_key))

            # All additive by default — sum same-unit values, keep highest otherwise
            usd_total = sum(r.computed_value for r in group if r.value_unit == "USD")
            pct_total = sum(r.computed_value for r in group if r.value_unit == "percent")

            # Combine into a synthetic rule using the first entry as template
            base = group[0]
            if len(group) == 1:
                applied.append(base)
            else:
                # Build a merged rule
                import copy
                merged = copy.copy(base)
                merged.computed_value = usd_total + pct_total
                merged.value_unit = "mixed" if (usd_total and pct_total) else base.value_unit
                merged.jurisdiction_name = (
                    f"{base.jurisdiction_name} + {len(group)-1} more"
                )
                applied.append(merged)
                overridden.extend(group[1:])

        return applied, overridden

    # ── Net value ──────────────────────────────────────────────────────────────

    def calculate_breakdown(
        self,
        applied_rules: List[ApplicableRule],
    ) -> Dict[str, float]:
        breakdown: Dict[str, float] = {
            "credit": 0.0,
            "tax_abatement": 0.0,
            "rebate": 0.0,
            "green_bonus": 0.0,
            "permit_fee": 0.0,
            "other": 0.0,
        }
        for rule in applied_rules:
            cat = self.RULE_TYPE_MAP.get(rule.rule_type.lower(), "other")
            value = rule.computed_value
            if cat == "permit_fee":
                value = -abs(value)
            breakdown[cat] += value
        return breakdown

    # ── Main entry point ───────────────────────────────────────────────────────

    def maximize(
        self,
        *,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        jurisdiction_codes: Optional[List[str]] = None,
        project_type: str = "all",
        qualified_spend: Optional[float] = None,
        spend_by_location: Optional[Dict[str, float]] = None,
    ) -> MaximizedResult:
        """
        Maximize incentives for a location or explicit jurisdiction list.

        Provide either (lat, lng) for automatic state resolution, or
        jurisdiction_codes for explicit lookup — or both.

        spend_by_location (optional) maps jurisdiction CODE → qualifying spend
        for that location.  Useful for split-location shoots where a sub-
        jurisdiction bonus (e.g. IL-CHICAGO-BONUS) should only apply to the
        fraction of spend that occurred within that city/county.

        Example:
            spend_by_location={"IL": 5_000_000, "IL-COOK": 2_000_000}
            → IL-FILM-BASE uses $5M, IL-CHICAGO-BONUS uses $2M
        """
        resolved_state: Optional[str] = None

        # --- Resolve jurisdictions ---
        if jurisdiction_codes:
            jurisdictions = self.resolve_jurisdictions_by_codes(jurisdiction_codes)
        elif lat is not None and lng is not None:
            jurisdictions, resolved_state = self.resolve_jurisdictions_by_location(lat, lng)
        else:
            return MaximizedResult(
                total_incentive_usd=0.0, qualified_spend=qualified_spend,
                effective_rate=None, breakdown={}, applied_rules=[],
                overridden_rules=[], conflicts_resolved=[],
                warnings=["Provide lat/lng or jurisdiction_codes"],
                recommendations=[], jurisdictions_evaluated=0,
            )

        if not jurisdictions:
            return MaximizedResult(
                total_incentive_usd=0.0, qualified_spend=qualified_spend,
                effective_rate=None, breakdown={}, applied_rules=[],
                overridden_rules=[], conflicts_resolved=[],
                warnings=["No matching jurisdictions found"],
                recommendations=["Check that jurisdictions table is seeded"],
                jurisdictions_evaluated=0, resolved_state=resolved_state,
            )

        jurisdiction_ids = [j["id"] for j in jurisdictions]

        # --- Fetch and apply rules ---
        all_rules, opt_in_warnings = self.fetch_rules(
            jurisdiction_ids, qualified_spend, project_type, spend_by_location
        )

        if not all_rules:
            return MaximizedResult(
                total_incentive_usd=0.0, qualified_spend=qualified_spend,
                effective_rate=None, breakdown={}, applied_rules=[],
                overridden_rules=[], conflicts_resolved=[],
                warnings=["No active incentive_rules in database for these jurisdictions"],
                recommendations=["Run scripts/seed_incentive_rules.py or monitor.py"],
                jurisdictions_evaluated=len(jurisdictions),
                resolved_state=resolved_state,
            )

        # ── Mutual exclusions ─────────────────────────────────────────────────
        # NY-FILM-BASE and NY-POST-PROD are mutually exclusive: the post-prod
        # credit is for productions that did NOT shoot in NY.  Keep the higher
        # value and warn when both appear.
        MUTUAL_EXCLUSIONS = [
            {"NY-FILM-BASE", "NY-POST-PROD"},
        ]
        exclusion_warnings: list[str] = []
        for excl_set in MUTUAL_EXCLUSIONS:
            hits = [r for r in all_rules if r.rule_key in excl_set]
            if len(hits) >= 2:
                hits.sort(key=lambda r: r.computed_value, reverse=True)
                kept, dropped = hits[0], hits[1:]
                for d in dropped:
                    all_rules.remove(d)
                    exclusion_warnings.append(
                        f"{kept.rule_key} and {d.rule_key} are mutually exclusive "
                        f"— kept {kept.rule_key} (${kept.computed_value:,.0f})"
                    )

        applied, overridden = self.apply_inheritance(all_rules)
        breakdown = self.calculate_breakdown(applied)
        total = sum(breakdown.values())

        effective_rate = (total / qualified_spend) if qualified_spend else None

        warnings = exclusion_warnings + opt_in_warnings
        if breakdown.get("permit_fee", 0) < 0:
            warnings.append(
                f"Net permit fees of ${-breakdown['permit_fee']:,.2f} reduce total value"
            )
        if qualified_spend is None:
            warnings.append(
                "No qualified_spend provided — percentage rules shown as raw % values, not dollars"
            )

        recommendations = [
            f"{r.jurisdiction_name} {r.rule_key} overridden by higher-priority rule"
            for r in overridden
        ] or ["Incentive stack is clean — no conflicts detected"]

        return MaximizedResult(
            total_incentive_usd=total,
            qualified_spend=qualified_spend,
            effective_rate=effective_rate,
            breakdown=breakdown,
            applied_rules=applied,
            overridden_rules=overridden,
            conflicts_resolved=[
                f"{r.jurisdiction_name} {r.rule_key}" for r in overridden
            ],
            warnings=warnings,
            recommendations=recommendations,
            jurisdictions_evaluated=len(jurisdictions),
            resolved_state=resolved_state,
        )


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    import argparse
    import json

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="SceneIQ Maximizer")
    parser.add_argument("lat", type=float, nargs="?", help="Latitude")
    parser.add_argument("lng", type=float, nargs="?", help="Longitude")
    parser.add_argument("--codes", nargs="+", help="Explicit jurisdiction codes")
    parser.add_argument("--spend", type=float, help="Qualified spend in USD")
    parser.add_argument("--type", default="all", dest="project_type")
    parser.add_argument(
        "--location-spend", nargs="+", metavar="CODE:AMOUNT",
        help="Per-location spend splits, e.g. --location-spend IL:5000000 IL-COOK:2000000"
    )
    args = parser.parse_args()

    spend_by_location: Optional[Dict[str, float]] = None
    if args.location_spend:
        spend_by_location = {}
        for item in args.location_spend:
            code, _, amount_str = item.partition(":")
            if not code or not amount_str:
                parser.error(f"Invalid --location-spend value '{item}' — use CODE:AMOUNT")
            spend_by_location[code.upper()] = float(amount_str)

    maximizer = SceneIQMaximizer()
    result = maximizer.maximize(
        lat=args.lat,
        lng=args.lng,
        jurisdiction_codes=args.codes,
        project_type=args.project_type,
        qualified_spend=args.spend,
        spend_by_location=spend_by_location,
    )

    print("\n" + "=" * 60)
    print("PILOTFORGE MAXIMIZER RESULT")
    print("=" * 60)
    if result.resolved_state:
        print(f"Resolved state:     {result.resolved_state}")
    print(f"Jurisdictions:      {result.jurisdictions_evaluated}")
    if result.qualified_spend:
        print(f"Qualified spend:    ${result.qualified_spend:,.0f}")
    print(f"Total incentive:    ${result.total_incentive_usd:,.2f}")
    if result.effective_rate is not None:
        print(f"Effective rate:     {result.effective_rate * 100:.1f}%")

    if any(v for v in result.breakdown.values()):
        print("\nBreakdown:")
        for cat, val in result.breakdown.items():
            if val:
                print(f"  {cat:20s}  ${val:>12,.2f}")

    if result.warnings:
        print("\nWarnings:")
        for w in result.warnings:
            print(f"  [!] {w}")

    if result.recommendations != ["Incentive stack is clean — no conflicts detected"]:
        print("\nRecommendations:")
        for r in result.recommendations:
            print(f"  --> {r}")

    print(f"\nApplied rules:   {len(result.applied_rules)}")
    print(f"Overridden rules: {len(result.overridden_rules)}")


if __name__ == "__main__":
    main()
