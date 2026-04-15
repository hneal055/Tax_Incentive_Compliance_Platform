"""
seed_australia.py — Australian Screen Production Incentive rules
================================================================
Sources verified 2026-04-14:
  - screen.gov.au/funding-and-support/australian-screen-production-incentive
  - Producer Offset: 40% feature film / 20% TV & SVOD (Australian content)
  - Location Offset: 16.5% on qualifying Australian production expenditure (QAPE)
    for large-budget foreign productions (min AUD $15M total budget)
  - PDV Offset: 30% on qualifying Australian PDV expenditure (min AUD $500K)
All three offsets are refundable tax rebates administered by Screen Australia / ATO.
"""

import os, uuid, sys
from datetime import datetime, timezone
import psycopg2

DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    sys.exit("DATABASE_URL not set")

conn = psycopg2.connect(DB_URL)
conn.autocommit = False
cur = conn.cursor()
NOW = datetime.now(timezone.utc)
EFF = datetime(2024, 1, 1, tzinfo=timezone.utc)

# ── Locate AU jurisdiction ─────────────────────────────────────────────────────
cur.execute("SELECT id FROM jurisdictions WHERE code = 'AU'")
row = cur.fetchone()
if not row:
    sys.exit("ERROR: AU jurisdiction not found")
AU_ID = row[0]
print(f"[ok] AU jurisdiction id = {AU_ID}")

# ── Update feedUrl ─────────────────────────────────────────────────────────────
cur.execute("""
    UPDATE jurisdictions
    SET "feedUrl" = 'https://www.screen.gov.au/funding-and-support/australian-screen-production-incentive',
        "updatedAt" = %s
    WHERE code = 'AU'
""", (NOW,))
print(f"[ok] AU feedUrl updated ({cur.rowcount} row)")

# ── Rules ──────────────────────────────────────────────────────────────────────
RULES = [
    {
        "ruleName":      "Producer Offset — Feature Film",
        "ruleCode":      "AU-PRODUCER-OFFSET-FILM",
        "incentiveType": "rebate",
        "creditType":    "refundable",
        "percentage":    40.0,
        "fixedAmount":   None,
        "eligibleExpenses": ["below_the_line_labor", "equipment", "locations",
                             "post_production", "set_construction", "vfx"],
        "excludedExpenses":  ["marketing", "distribution"],
        "requirements": {
            "minSpend": None,
            "description": (
                "40% refundable tax offset for Australian feature films with significant "
                "Australian content. Production must be a 'qualifying Australian film' — "
                "passes the Australian content test (points-based). "
                "Administered by Screen Australia and the ATO. "
                "Source: screen.gov.au/funding-and-support/australian-screen-production-incentive"
            )
        },
    },
    {
        "ruleName":      "Producer Offset — TV & SVOD",
        "ruleCode":      "AU-PRODUCER-OFFSET-TV",
        "incentiveType": "rebate",
        "creditType":    "refundable",
        "percentage":    20.0,
        "fixedAmount":   None,
        "eligibleExpenses": ["below_the_line_labor", "equipment", "locations",
                             "post_production", "set_construction"],
        "excludedExpenses":  ["marketing", "distribution"],
        "requirements": {
            "minSpend": None,
            "description": (
                "20% refundable tax offset for Australian TV series and SVOD content "
                "with significant Australian content. Same points-based Australian content "
                "test as the feature film offset. "
                "Administered by Screen Australia and the ATO. "
                "Source: screen.gov.au/funding-and-support/australian-screen-production-incentive"
            )
        },
    },
    {
        "ruleName":      "Location Offset",
        "ruleCode":      "AU-LOCATION-OFFSET",
        "incentiveType": "rebate",
        "creditType":    "refundable",
        "percentage":    16.5,
        "fixedAmount":   None,
        "eligibleExpenses": ["below_the_line_labor", "equipment", "locations",
                             "post_production", "set_construction"],
        "excludedExpenses":  ["marketing", "distribution"],
        "requirements": {
            "minSpend": 15_000_000,
            "minSpendCurrency": "AUD",
            "description": (
                "16.5% refundable tax offset on qualifying Australian production expenditure (QAPE) "
                "for large-budget foreign productions. Minimum total production budget AUD $15M. "
                "No Australian content test required — designed to attract foreign productions. "
                "Can be stacked with state-level incentives (NSW, VIC, QLD). "
                "Administered by the ATO. "
                "Source: screen.gov.au/funding-and-support/australian-screen-production-incentive"
            )
        },
    },
    {
        "ruleName":      "PDV Offset (Post, Digital & Visual Effects)",
        "ruleCode":      "AU-PDV-OFFSET",
        "incentiveType": "rebate",
        "creditType":    "refundable",
        "percentage":    30.0,
        "fixedAmount":   None,
        "eligibleExpenses": ["post_production", "vfx", "digital_production"],
        "excludedExpenses":  ["principal_photography", "marketing"],
        "requirements": {
            "minSpend": 500_000,
            "minSpendCurrency": "AUD",
            "description": (
                "30% refundable tax offset on qualifying Australian PDV expenditure. "
                "Minimum AUD $500K in Australian PDV spend. "
                "Available to both Australian and foreign productions for post, digital, "
                "and VFX work performed in Australia. No Australian content test required. "
                "Administered by the ATO. "
                "Source: screen.gov.au/funding-and-support/australian-screen-production-incentive"
            )
        },
    },
]

import json

for r in RULES:
    cur.execute('SELECT id FROM incentive_rules WHERE "ruleCode" = %s', (r["ruleCode"],))
    existing = cur.fetchone()
    req_json = json.dumps(r["requirements"])

    if existing:
        cur.execute("""
            UPDATE incentive_rules
            SET "ruleName"=%s, percentage=%s, requirements=%s,
                "eligibleExpenses"=%s, "excludedExpenses"=%s, "updatedAt"=%s
            WHERE "ruleCode"=%s
        """, (r["ruleName"], r["percentage"], req_json,
              r["eligibleExpenses"], r["excludedExpenses"], NOW, r["ruleCode"]))
        print(f"[ok] {r['ruleCode']} updated")
    else:
        cur.execute("""
            INSERT INTO incentive_rules
                (id, "jurisdictionId", "ruleName", "ruleCode", "incentiveType",
                 "creditType", percentage, "fixedAmount", "eligibleExpenses",
                 "excludedExpenses", "effectiveDate", requirements,
                 active, "createdAt", "updatedAt")
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,true,%s,%s)
        """, (
            str(uuid.uuid4()), AU_ID,
            r["ruleName"], r["ruleCode"], r["incentiveType"],
            r["creditType"], r["percentage"], r["fixedAmount"],
            r["eligibleExpenses"], r["excludedExpenses"], EFF, req_json, NOW, NOW
        ))
        print(f"[ok] {r['ruleCode']} inserted ({r['percentage']}%)")

conn.commit()
conn.close()
print("\nDone. Australia incentive rules seeded:")
print("  AU-PRODUCER-OFFSET-FILM  40%  refundable  feature film")
print("  AU-PRODUCER-OFFSET-TV    20%  refundable  TV & SVOD")
print("  AU-LOCATION-OFFSET       16.5% refundable  foreign productions (min AUD $15M)")
print("  AU-PDV-OFFSET            30%  refundable  post/VFX (min AUD $500K)")
