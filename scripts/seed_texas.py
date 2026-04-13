"""
seed_texas.py — Texas TMIIIP grant rules correction + sub-jurisdiction cleanup
===============================================================================
Changes:
  1. Fix TX-FILM-GRANT-BASE     — correct rate 5% → 15%, min spend $250K → $200K
  2. Delete TX-FILM-GRANT-ENHANCED — monolithic catch-all; replaced by stacked uplifts
  3. Insert TX-MUSIC-UPLIFT     — +2.5% opt-in, Texas-based music composer
  4. Insert TX-VETERAN-UPLIFT   — +2.5% opt-in, min 3 Texas military veterans hired
  5. Insert TX-POST-UPLIFT      — +2.5% opt-in, post-production work done in Texas
  6. Fix TX state feedUrl       — gov.texas.gov/film/rss was 404 → gov.texas.gov/film/page/tmiiip
  7. TX-AUSTIN / TX-HOUSTON     — no verified permit office URLs found, feedUrl stays NULL

Program: Texas Moving Image Industry Incentive Program (TMIIIP)
Type: GRANT (cash rebate after production — NOT a tax credit)
Max stacked: 15% + 2.5% + 2.5% + 2.5% = 22.5%
Min spend: $200K general / $100K commercials
No annual cap (subject to legislative appropriation)
Source: https://gov.texas.gov/film/page/tmiiip
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
EFF = datetime(2024, 1, 1, tzinfo=timezone.utc)

# ── Locate TX jurisdiction ────────────────────────────────────────────────────
cur.execute("SELECT id FROM jurisdictions WHERE code = 'TX'")
row = cur.fetchone()
if not row:
    sys.exit("ERROR: TX jurisdiction not found")
TX_ID = row[0]
print(f"[ok] TX jurisdiction id = {TX_ID}")

# ── 1. Fix TX-FILM-GRANT-BASE: 5% → 15%, min spend $250K → $200K ─────────────
base_req = json.dumps({
    "programType": "grant",
    "minTXSpend": 200000,
    "minSpendCommercial": 100000,
    "noCap": True,
    "scoringFactors": ["economic_impact", "job_creation", "diversity"],
    "description": (
        "15% cash grant on qualifying Texas spend. "
        "Grant is paid after production — NOT a tax credit. "
        "Minimum $200K Texas spend ($100K for commercials). "
        "No annual program cap, but subject to legislative appropriation. "
        "Applications scored on economic impact, job creation, and diversity. "
        "Cite: gov.texas.gov/film/page/tmiiip"
    )
})
cur.execute("""
    UPDATE incentive_rules
    SET percentage = 15.0,
        "ruleName" = 'Texas TMIIIP Grant — Base',
        "creditType" = 'grant',
        requirements = %s,
        "updatedAt" = %s
    WHERE "ruleCode" = 'TX-FILM-GRANT-BASE'
""", (base_req, NOW))
print(f"[ok] TX-FILM-GRANT-BASE updated — 15%, creditType=grant, minSpend=$200K ({cur.rowcount} row)")

# ── 2. Delete TX-FILM-GRANT-ENHANCED ─────────────────────────────────────────
cur.execute("DELETE FROM incentive_rules WHERE \"ruleCode\" = 'TX-FILM-GRANT-ENHANCED'")
print(f"[ok] TX-FILM-GRANT-ENHANCED deleted ({cur.rowcount} row)")

# ── 3–5. Uplift rules ─────────────────────────────────────────────────────────
uplifts = [
    {
        "ruleCode":    "TX-MUSIC-UPLIFT",
        "ruleName":    "Texas TMIIIP Grant — Music Uplift",
        "percentage":  2.5,
        "requirements": json.dumps({
            "optIn": True,
            "requiresTexasComposer": True,
            "description": (
                "Additional 2.5% grant for productions using a Texas-based music composer. "
                "Stacks with base 15% for 17.5% effective rate. "
                "Cite: gov.texas.gov/film/page/tmiiip"
            )
        }),
    },
    {
        "ruleCode":    "TX-VETERAN-UPLIFT",
        "ruleName":    "Texas TMIIIP Grant — Veteran Uplift",
        "percentage":  2.5,
        "requirements": json.dumps({
            "optIn": True,
            "minTexasVeterans": 3,
            "description": (
                "Additional 2.5% grant for productions hiring a minimum of 3 Texas military "
                "veterans. Stacks with base 15% for 17.5% effective rate. "
                "Cite: gov.texas.gov/film/page/tmiiip"
            )
        }),
    },
    {
        "ruleCode":    "TX-POST-UPLIFT",
        "ruleName":    "Texas TMIIIP Grant — Post-Production Uplift",
        "percentage":  2.5,
        "requirements": json.dumps({
            "optIn": True,
            "requiresTexasPostProduction": True,
            "description": (
                "Additional 2.5% grant for productions completing post-production work in Texas. "
                "Stacks with base 15% for 17.5% effective rate. "
                "All three uplifts may stack: max 22.5% total. "
                "Cite: gov.texas.gov/film/page/tmiiip"
            )
        }),
    },
]

for uplift in uplifts:
    cur.execute("SELECT id FROM incentive_rules WHERE \"ruleCode\" = %s", (uplift["ruleCode"],))
    if cur.fetchone():
        cur.execute("""
            UPDATE incentive_rules
            SET percentage = %s, requirements = %s, "updatedAt" = %s
            WHERE "ruleCode" = %s
        """, (uplift["percentage"], uplift["requirements"], NOW, uplift["ruleCode"]))
        print(f"[ok] {uplift['ruleCode']} updated")
    else:
        cur.execute("""
            INSERT INTO incentive_rules (
                id, "jurisdictionId", "ruleName", "ruleCode", "incentiveType",
                "creditType", percentage, "eligibleExpenses", "excludedExpenses",
                "effectiveDate", requirements, active, "createdAt", "updatedAt"
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,true,%s,%s)
        """, (
            str(uuid.uuid4()), TX_ID,
            uplift["ruleName"], uplift["ruleCode"], "rebate",
            "grant", uplift["percentage"], "{}", "{}",
            EFF, uplift["requirements"], NOW, NOW
        ))
        print(f"[ok] {uplift['ruleCode']} inserted (+{uplift['percentage']}%, opt-in)")

# ── 6. Fix TX state feedUrl ───────────────────────────────────────────────────
cur.execute("""
    UPDATE jurisdictions
    SET "feedUrl" = 'https://gov.texas.gov/film/page/tmiiip',
        "updatedAt" = %s
    WHERE code = 'TX'
""", (NOW,))
print(f"[ok] TX feedUrl updated → gov.texas.gov/film/page/tmiiip ({cur.rowcount} row)")

conn.commit()
conn.close()

print("\nDone. Texas TMIIIP grant summary:")
print("  TX-FILM-GRANT-BASE  15%   cash grant, all qualified TX spend ($200K min)")
print("  TX-MUSIC-UPLIFT    +2.5%  opt-in — Texas-based music composer")
print("  TX-VETERAN-UPLIFT  +2.5%  opt-in — min 3 Texas military veterans")
print("  TX-POST-UPLIFT     +2.5%  opt-in — post-production done in Texas")
print("  Max stacked:       22.5%  all uplifts elected")
print("  TX-AUSTIN / TX-HOUSTON — feedUrl NULL (no verified permit office URLs)")
