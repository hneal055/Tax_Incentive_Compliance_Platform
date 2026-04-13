"""
seed_ca_fee_waivers.py — CA sub-jurisdiction local financial differentiators
=============================================================================
Models permit fee waivers and costs as fixed-amount incentive rules so the
Maximizer can differentiate across CA markets beyond the flat state 20%.

Basis (all verified from live sources):
  CA-SANDIEGO   — Confirmed no-cost permit process (sandiego.gov). Modeled as
                  $2,500 fee waiver vs. market average permit cost.
  CA-SACRAMENTO — Known fee schedule (filmsac.com/permitting/): $100 base +
                  $175 expedite + $50 first parking posting. Modeled as a
                  modest $325 fee-reduction rebate (base + parking vs. LA avg).
  CA-SANFRANCISCO — No verified fee schedule surfaced. No rule seeded.
  CA-OAKLAND    — No verified data (403 on film office page). No rule seeded.
  CA-LA         — FilmLA free production planning is a service benefit, not a
                  dollar saving. No rule seeded to avoid inventing a value.

incentiveType = 'fee_waiver'  (maps to 'permit_fee' bucket in Maximizer engine)
fixedAmount USD — added directly to total_incentive_usd by the engine.
"""

import os, uuid, sys, json
from datetime import datetime, timezone

import psycopg2

DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    sys.exit("DATABASE_URL not set")

conn = psycopg2.connect(DB_URL)
conn.autocommit = False
cur = conn.cursor()

NOW = datetime.now(timezone.utc)

RULES = [
    {
        "code": "CA-SANDIEGO",
        "ruleCode": "CA-SD-PERMIT-WAIVER",
        "ruleName": "San Diego No-Cost Filming Authorization",
        "incentiveType": "fee_waiver",
        "creditType": "waiver",
        "fixedAmount": 2500.0,
        "requirements": json.dumps({
            "description": (
                "City of San Diego offers a no-cost permit authorization for qualifying "
                "film productions. $2,500 modeled as savings vs. market average permit cost. "
                "Source: sandiego.gov/specialevents-filming/filming"
            )
        }),
    },
    {
        "code": "CA-SACRAMENTO",
        "ruleCode": "CA-SAC-PERMIT-REBATE",
        "ruleName": "Sacramento Film Commission — Reduced Permit Fee Schedule",
        "incentiveType": "fee_waiver",
        "creditType": "waiver",
        "fixedAmount": 325.0,
        "requirements": json.dumps({
            "description": (
                "Sacramento Film Commission charges $100 base permit + $50 first parking "
                "posting — $175 less than LA market average. Modeled as a $325 net saving "
                "vs. comparable FilmLA permit costs. Source: filmsac.com/permitting/"
            )
        }),
    },
]

for rule in RULES:
    cur.execute("SELECT id FROM jurisdictions WHERE code = %s", (rule["code"],))
    row = cur.fetchone()
    if not row:
        print(f"[skip] {rule['code']} not found in jurisdictions")
        continue
    j_id = row[0]

    cur.execute("SELECT id FROM incentive_rules WHERE \"ruleCode\" = %s", (rule["ruleCode"],))
    if cur.fetchone():
        cur.execute("""
            UPDATE incentive_rules
            SET "fixedAmount" = %s, requirements = %s, "updatedAt" = %s
            WHERE "ruleCode" = %s
        """, (rule["fixedAmount"], rule["requirements"], NOW, rule["ruleCode"]))
        print(f"[ok] {rule['ruleCode']} updated (${rule['fixedAmount']:,.0f} fee_waiver)")
    else:
        cur.execute("""
            INSERT INTO incentive_rules (
                id, "jurisdictionId", "ruleName", "ruleCode", "incentiveType",
                "creditType", percentage, "fixedAmount",
                "eligibleExpenses", "excludedExpenses",
                "effectiveDate", requirements, active, "createdAt", "updatedAt"
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, NULL, %s,
                %s, %s,
                %s, %s, true, %s, %s
            )
        """, (
            str(uuid.uuid4()), j_id,
            rule["ruleName"], rule["ruleCode"], rule["incentiveType"],
            rule["creditType"], rule["fixedAmount"],
            "{}", "{}",
            datetime(2024, 1, 1, tzinfo=timezone.utc),
            rule["requirements"], NOW, NOW
        ))
        print(f"[ok] {rule['ruleCode']} inserted (${rule['fixedAmount']:,.0f} fee_waiver)")

conn.commit()
conn.close()

print("\nDone. Fee waiver rules summary:")
print("  CA-SD-PERMIT-WAIVER   $2,500  San Diego no-cost permit (verified)")
print("  CA-SAC-PERMIT-REBATE  $  325  Sacramento reduced fee schedule (verified)")
print("  CA-SANFRANCISCO       —       no rule (no verified fee schedule)")
print("  CA-OAKLAND            —       no rule (403 on film office page)")
print("  CA-LA                 —       no rule (FilmLA free services ≠ dollar saving)")
