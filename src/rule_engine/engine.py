from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import date, datetime
import json
from pathlib import Path


@dataclass
class EvalResult:
    eligible: bool
    benefit_amount: float
    qualified_spend_total: float
    compliance_flags: List[str]
    trace: List[Dict[str, Any]]


def _parse_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    return datetime.fromisoformat(s).date()


def load_rule_from_file(path: str | Path) -> Dict[str, Any]:
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8"))


def evaluate_rule(
    *,
    rule: Dict[str, Any],
    jurisdiction_code: str,
    production_start_date: Optional[str],
    expenses: List[Dict[str, Any]],
) -> EvalResult:
    """
    MVP evaluator:
    - Computes qualified spend total using simple flags + category rules.
    - Applies eligibility thresholds.
    - Calculates benefit = rate * base_total, then applies caps (if any).
    - Produces compliance flags + trace steps.
    """
    trace: List[Dict[str, Any]] = []
    flags: List[str] = []

    # Basic rule checks
    if not rule.get("active", False):
        return EvalResult(False, 0.0, 0.0, ["RULE_INACTIVE"], [{"step": "rule_inactive"}])

    if jurisdiction_code.strip().upper() != str(rule.get("jurisdiction_code", "")).strip().upper():
        return EvalResult(False, 0.0, 0.0, ["JURISDICTION_MISMATCH"], [{"step": "jurisdiction_mismatch"}])

    eff_from = _parse_date(rule.get("effective_from"))
    eff_to = _parse_date(rule.get("effective_to"))
    prod_date = _parse_date(production_start_date) if production_start_date else None

    if prod_date and eff_from and prod_date < eff_from:
        return EvalResult(False, 0.0, 0.0, ["OUTSIDE_EFFECTIVE_DATES"], [{"step": "prod_before_effective_from"}])
    if prod_date and eff_to and prod_date > eff_to:
        return EvalResult(False, 0.0, 0.0, ["OUTSIDE_EFFECTIVE_DATES"], [{"step": "prod_after_effective_to"}])

    eligibility = rule.get("eligibility", {}) or {}
    calc = rule.get("calculation", {}) or {}

    qualified_categories = {str(x).strip().lower() for x in (eligibility.get("qualified_categories", []) or [])}
    exclude_categories = {str(x).strip().lower() for x in (eligibility.get("exclude_categories", []) or [])}
    in_state_required = bool(eligibility.get("in_state_required", False))
    labor_residency_required = bool(eligibility.get("labor_residency_required", False))
    min_qualified_spend = float(eligibility.get("min_qualified_spend", 0) or 0)

    # Compute qualified spend total
    qualified_total = 0.0
    counted = 0
    skipped = 0

    for e in expenses:
        amount = float(e.get("amount", 0) or 0)
        category = str(e.get("category", "") or "").strip().lower()

        is_qualified = bool(e.get("qualified", True))  # default True if not provided
        in_state = bool(e.get("in_state", True))       # default True if not provided
        is_labor = bool(e.get("labor", False))
        is_resident = bool(e.get("resident", True))

        # Category rules
        if qualified_categories and category not in qualified_categories:
            skipped += 1
            continue
        if exclude_categories and category in exclude_categories:
            skipped += 1
            continue

        # Qualification flags
        if not is_qualified:
            skipped += 1
            continue
        if in_state_required and not in_state:
            skipped += 1
            continue
        if labor_residency_required and is_labor and not is_resident:
            skipped += 1
            continue

        qualified_total += amount
        counted += 1

    trace.append(
        {
            "step": "compute_qualified_total",
            "qualified_total": qualified_total,
            "counted": counted,
            "skipped": skipped,
            "in_state_required": in_state_required,
            "labor_residency_required": labor_residency_required,
        }
    )

    # Eligibility threshold
    if min_qualified_spend and qualified_total < min_qualified_spend:
        flags.append("BELOW_MIN_QUALIFIED_SPEND")
        trace.append({"step": "min_spend_failed", "min_required": min_qualified_spend, "actual": qualified_total})
        return EvalResult(False, 0.0, qualified_total, flags, trace)

    # Calculation
    rate = float(calc.get("rate", 0) or 0)
    base = str(calc.get("base", "qualified_spend_total"))

    base_total = qualified_total
    if base != "qualified_spend_total":
        flags.append("BASE_FALLBACK_TO_QUALIFIED_SPEND_TOTAL")
        trace.append({"step": "base_fallback", "requested_base": base, "used_base": "qualified_spend_total"})

    benefit = base_total * rate
    trace.append({"step": "apply_rate", "rate": rate, "base_total": base_total, "benefit_pre_cap": benefit})

    # Caps
    caps = calc.get("caps", {}) or {}
    max_benefit = caps.get("max_benefit", None)
    if max_benefit is not None:
        max_benefit_f = float(max_benefit)
        if benefit > max_benefit_f:
            benefit = max_benefit_f
            flags.append("CAPPED_MAX_BENEFIT")
            trace.append({"step": "cap_applied", "max_benefit": max_benefit_f, "benefit_post_cap": benefit})

    return EvalResult(True, float(benefit), float(qualified_total), flags, trace)
