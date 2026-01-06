"""
scripts/seed_jurisdictions.py

Robust jurisdiction seeder (UPSERT by `code`) for Prisma Client Python.

Key features:
- Upsert by `code`: create if missing, update changed fields if exists
- Validation: required fields, normalized codes, URL sanity checks
- Duplicate detection within jurisdictions_data (normalized)
- Dry-run mode: preview adds/updates without writing to DB
- Strict mode: prevent updates to identity fields (optional)
- Selective update: control which fields may be updated once a row exists
- Clear summary + non-zero exit codes for CI usage

Run:
  python scripts/seed_jurisdictions.py
  python scripts/seed_jurisdictions.py --dry-run
  python scripts/seed_jurisdictions.py --strict
  python scripts/seed_jurisdictions.py --only-update description website active

Assumptions:
- Prisma model: jurisdiction
- `code` is unique (recommended) in your Prisma schema
"""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urlparse

# Add project root to sys.path so `src.*` imports work when run from /scripts
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.database import prisma  # noqa: E402


# ---------------------------------------------------------------------------
# CONFIG: What fields exist + default update policy
# ---------------------------------------------------------------------------

# Canonical set of fields we write to Jurisdiction.
ALL_FIELDS: Tuple[str, ...] = (
    "name",
    "code",
    "country",
    "type",
    "description",
    "website",
    "active",
)

# "Identity" fields: often you want to treat these as stable once created.
# In --strict mode, changes to these fields are rejected.
IDENTITY_FIELDS: Tuple[str, ...] = ("code", "name", "country", "type")

# Default update policy: update everything EXCEPT code (code is the key).
# You can override with CLI: --only-update ...
DEFAULT_UPDATE_FIELDS: Tuple[str, ...] = (
    "name",
    "country",
    "type",
    "description",
    "website",
    "active",
)

CODE_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9_-]{0,15}$")  # flexible, but bounded


# ---------------------------------------------------------------------------
# DATA: Your jurisdiction list
# ---------------------------------------------------------------------------

jurisdictions_data: List[Dict[str, Any]] = [
    # US States
    {
        "name": "Louisiana",
        "code": "LA",
        "country": "USA",
        "type": "state",
        "description": "Louisiana Entertainment Tax Credit - up to 40% tax credit",
        "website": "https://www.opportunitylouisiana.gov/business-incentives/entertainment",
        "active": True,
    },
    {
        "name": "New Mexico",
        "code": "NM",
        "country": "USA",
        "type": "state",
        "description": "Film Production Tax Credit - 25-35% refundable tax credit",
        "website": "https://nmfilm.com/incentives/",
        "active": True,
    },
    {
        "name": "Massachusetts",
        "code": "MA",
        "country": "USA",
        "type": "state",
        "description": "Film Tax Incentive - 25% payroll credit plus 25% production expense credit",
        "website": "https://www.mass.gov/film-tax-incentive",
        "active": True,
    },
    {
        "name": "Connecticut",
        "code": "CT",
        "country": "USA",
        "type": "state",
        "description": "Film and Digital Media Tax Credit - up to 30%",
        "website": "https://portal.ct.gov/DECD/Content/Industry/Film-Tax-Credit",
        "active": True,
    },
    {
        "name": "Illinois",
        "code": "IL",
        "country": "USA",
        "type": "state",
        "description": "Film Production Tax Credit - 30% credit",
        "website": "https://www2.illinois.gov/dceo/AboutDCEO/GrantsIncentives/Pages/FilmTaxCredit.aspx",
        "active": True,
    },
    {
        "name": "Pennsylvania",
        "code": "PA",
        "country": "USA",
        "type": "state",
        "description": "Film Tax Credit - 25-30% credit",
        "website": "https://www.filminpa.com/tax-credit/",
        "active": True,
    },
    {
        "name": "North Carolina",
        "code": "NC",
        "country": "USA",
        "type": "state",
        "description": "Film and Entertainment Grant - rebate program",
        "website": "https://www.ncfilm.com/incentives/",
        "active": True,
    },
    {
        "name": "Florida",
        "code": "FL",
        "country": "USA",
        "type": "state",
        "description": "Entertainment Industry Financial Incentive Program",
        "website": "https://www.filminflorida.com/incentives/",
        "active": True,
    },
    # Canadian Provinces
    {
        "name": "Ontario",
        "code": "ON",
        "country": "Canada",
        "type": "province",
        "description": "Ontario Film and Television Tax Credits - various programs",
        "website": "https://www.ontario.ca/page/ontario-film-and-television-tax-credits",
        "active": True,
    },
    {
        "name": "Quebec",
        "code": "QC",
        "country": "Canada",
        "type": "province",
        "description": "Film Production Tax Credits - up to 40%",
        "website": "https://www.revenuquebec.ca/en/businesses/income-tax-credits/film-production/",
        "active": True,
    },
    {
        "name": "Alberta",
        "code": "AB",
        "country": "Canada",
        "type": "province",
        "description": "Alberta Film and Television Tax Credit",
        "website": "https://www.alberta.ca/film-industry-incentive-programs.aspx",
        "active": True,
    },
    # UK
    {
        "name": "United Kingdom",
        "code": "UK",
        "country": "United Kingdom",
        "type": "country",
        "description": "Film Tax Relief and High-End TV Tax Relief - up to 25%",
        "website": "https://www.bfi.org.uk/film-industry/film-tax-relief",
        "active": True,
    },
    # Australia
    {
        "name": "New South Wales",
        "code": "NSW",
        "country": "Australia",
        "type": "state",
        "description": "Made in NSW Fund - production incentives",
        "website": "https://www.screen.nsw.gov.au/funding/made-in-nsw",
        "active": True,
    },
    {
        "name": "Victoria",
        "code": "VIC",
        "country": "Australia",
        "type": "state",
        "description": "Victorian Screen Incentive - production attraction",
        "website": "https://www.vic.gov.au/victorian-screen-incentive",
        "active": True,
    },
    {
        "name": "Queensland",
        "code": "QLD",
        "country": "Australia",
        "type": "state",
        "description": "Production Attraction Strategy",
        "website": "https://www.screenqld.com.au/incentives/",
        "active": True,
    },
]


# ---------------------------------------------------------------------------
# SUPPORT: Validation + diff + reporting
# ---------------------------------------------------------------------------

@dataclass
class PlanItem:
    code: str
    name: str
    action: str  # "create" | "update" | "unchanged" | "error" | "blocked"
    changes: Dict[str, Any]
    message: Optional[str] = None


def normalize_code(code: Any) -> str:
    c = str(code).strip().upper()
    if not c:
        raise ValueError("code is blank")
    if any(ch.isspace() for ch in c):
        raise ValueError(f"code contains whitespace: {c!r}")
    if not CODE_PATTERN.match(c):
        raise ValueError(
            f"code {c!r} fails pattern {CODE_PATTERN.pattern}. "
            "Use A-Z, 0-9, underscore, hyphen; max length 16."
        )
    return c


def normalize_text(value: Any, field: str, required: bool = True, max_len: int = 255) -> str:
    if value is None:
        if required:
            raise ValueError(f"{field} is required")
        return ""
    s = str(value).strip()
    if required and not s:
        raise ValueError(f"{field} is blank")
    if len(s) > max_len:
        raise ValueError(f"{field} too long ({len(s)} > {max_len})")
    return s


def normalize_url(url: Any) -> Optional[str]:
    if url is None:
        return None
    s = str(url).strip()
    if not s:
        return None
    parsed = urlparse(s)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"website must start with http:// or https:// (got {s!r})")
    if not parsed.netloc:
        raise ValueError(f"website URL missing host (got {s!r})")
    return s


def normalize_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    payload = {
        "name": normalize_text(raw.get("name"), "name", required=True, max_len=200),
        "code": normalize_code(raw.get("code")),
        "country": normalize_text(raw.get("country"), "country", required=True, max_len=80),
        "type": normalize_text(raw.get("type"), "type", required=True, max_len=40),
        "description": normalize_text(raw.get("description", ""), "description", required=False, max_len=5000) or None,
        "website": normalize_url(raw.get("website")),
        "active": bool(raw.get("active", True)),
    }
    return payload


def find_duplicate_codes(items: Iterable[Dict[str, Any]]) -> List[Tuple[str, List[str]]]:
    seen: Dict[str, List[str]] = {}
    bad: List[Tuple[str, List[str]]] = []

    for j in items:
        raw_code = j.get("code", "")
        raw_name = j.get("name", "")
        try:
            code = normalize_code(raw_code)
        except Exception:
            code = str(raw_code).strip().upper()
        name = str(raw_name).strip() or "<unnamed>"
        seen.setdefault(code, []).append(name)

    for code, names in seen.items():
        if not code:
            bad.append(("<BLANK CODE>", names))
        elif len(names) > 1:
            bad.append((code, names))

    return bad


def compute_changes(existing_obj: Any, desired: Dict[str, Any], allowed_update_fields: Sequence[str]) -> Dict[str, Any]:
    changes: Dict[str, Any] = {}
    for field in allowed_update_fields:
        desired_value = desired.get(field)
        current_value = getattr(existing_obj, field, None)
        if current_value != desired_value:
            changes[field] = desired_value
    return changes


def blocked_identity_changes(existing_obj: Any, desired: Dict[str, Any]) -> Dict[str, Tuple[Any, Any]]:
    blocked: Dict[str, Tuple[Any, Any]] = {}
    for field in IDENTITY_FIELDS:
        if field == "code":
            continue
        cur = getattr(existing_obj, field, None)
        des = desired.get(field)
        if cur != des:
            blocked[field] = (cur, des)
    return blocked


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed jurisdictions (upsert by code).")
    parser.add_argument("--dry-run", action="store_true", help="Plan changes but do not write to the database.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Block updates to identity fields (name/country/type). Useful to prevent accidental drift.",
    )
    parser.add_argument(
        "--only-update",
        nargs="*",
        default=None,
        help=(
            "Limit updates to these fields only (e.g., --only-update description website active). "
            f"Default: {', '.join(DEFAULT_UPDATE_FIELDS)}"
        ),
    )
    parser.add_argument(
        "--quiet-unchanged",
        action="store_true",
        help="Do not print per-row lines for unchanged records.",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# MAIN: Plan + apply
# ---------------------------------------------------------------------------

async def seed_jurisdictions() -> None:
    args = parse_args()

    dups = find_duplicate_codes(jurisdictions_data)
    if dups:
        print("\nERROR: Duplicate (or invalid/blank) jurisdiction codes in jurisdictions_data:\n")
        for code, names in dups:
            print(f"  - {code}: {names}")
        print("\nFix duplicates and rerun.")
        raise SystemExit(2)

    allowed_update_fields = tuple(args.only_update) if args.only_update is not None else DEFAULT_UPDATE_FIELDS
    allowed_update_fields = tuple([f for f in allowed_update_fields if f != "code"])

    unknown = [f for f in allowed_update_fields if f not in ALL_FIELDS]
    if unknown:
        print(f"ERROR: Unknown field(s) in --only-update: {unknown}. Allowed: {list(ALL_FIELDS)}")
        raise SystemExit(2)

    print("Starting jurisdiction seeding (upsert by code)...")
    if args.dry_run:
        print("DRY-RUN: no database writes will occur.")
    if args.strict:
        print("STRICT: identity fields (name/country/type) updates are blocked.")
    print(f"Update fields: {', '.join(allowed_update_fields)}")
    print("-" * 60)

    plan: List[PlanItem] = []
    added = updated = unchanged = blocked = errors = 0

    try:
        await prisma.connect()

        existing = await prisma.jurisdiction.find_many()
        existing_by_code = {j.code: j for j in existing}

        for raw in jurisdictions_data:
            try:
                desired = normalize_payload(raw)
                code = desired["code"]
                name = desired["name"]
            except Exception as e:
                plan.append(
                    PlanItem(
                        code="<unknown>",
                        name=str(raw.get("name", "<unknown>")),
                        action="error",
                        changes={},
                        message=str(e),
                    )
                )
                errors += 1
                continue

            existing_row = existing_by_code.get(code)

            if not existing_row:
                plan.append(PlanItem(code=code, name=name, action="create", changes=desired))
                added += 1
                continue

            if args.strict:
                identity_drift = blocked_identity_changes(existing_row, desired)
                if identity_drift:
                    msg = "Identity field change blocked: " + ", ".join(
                        [f"{k}: {v[0]!r} -> {v[1]!r}" for k, v in identity_drift.items()]
                    )
                    plan.append(PlanItem(code=code, name=name, action="blocked", changes={}, message=msg))
                    blocked += 1
                    continue

            changes = compute_changes(existing_row, desired, allowed_update_fields)
            if changes:
                plan.append(PlanItem(code=code, name=name, action="update", changes=changes))
                updated += 1
            else:
                plan.append(PlanItem(code=code, name=name, action="unchanged", changes={}))
                unchanged += 1

        for item in plan:
            if item.action == "unchanged" and args.quiet_unchanged:
                continue
            if item.action in ("create", "update"):
                keys = ", ".join(item.changes.keys())
                print(f"{item.action.upper():8} {item.code:6} {item.name}  [{keys}]")
            elif item.action == "unchanged":
                print(f"UNCHANGED {item.code:6} {item.name}")
            else:
                extra = f" - {item.message}" if item.message else ""
                print(f"{item.action.upper():8} {item.code:6} {item.name}{extra}")

        print("-" * 60)

        if args.dry_run:
            print("DRY-RUN complete. No changes written.")
        else:
            for item in plan:
                if item.action == "create":
                    created = await prisma.jurisdiction.create(data=item.changes)
                    existing_by_code[item.code] = created
                elif item.action == "update":
                    updated_row = await prisma.jurisdiction.update(where={"code": item.code}, data=item.changes)
                    existing_by_code[item.code] = updated_row

            print("Applied changes to database.")

        print("\n" + "=" * 60)
        print("Jurisdiction seed summary")
        print(f"Added:     {added}")
        print(f"Updated:   {updated}")
        print(f"Unchanged: {unchanged}")
        print(f"Blocked:   {blocked}")
        print(f"Errors:    {errors}")
        print("=" * 60)

        if errors:
            raise SystemExit(1)

    finally:
        try:
            await prisma.disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(seed_jurisdictions())
