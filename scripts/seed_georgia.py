"""
seed_georgia.py — Georgia incentive rules + local jurisdiction setup
====================================================================
1. Restructure GA-FILM-PROMO → GA-FILM-LOGO (10% opt-in uplift)
2. Insert GA sub-jurisdictions: Atlanta, Savannah, Fulton County, DeKalb County
3. Set feed URLs on all four sub-jurisdictions
"""

import os, json, uuid, sys
from datetime import datetime, timezone

import psycopg2

# Use the container's DATABASE_URL env var directly (do not load .env,
# which has localhost:5435 — the container uses postgres:5432)
DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    sys.exit("DATABASE_URL not set")

conn = psycopg2.connect(DB_URL)
conn.autocommit = False
cur = conn.cursor()

NOW = datetime.now(timezone.utc)

# ── 1. Locate GA state jurisdiction ──────────────────────────────────────────
cur.execute("SELECT id FROM jurisdictions WHERE code = 'GA'")
row = cur.fetchone()
if not row:
    sys.exit("ERROR: GA jurisdiction not found — run seed_jurisdictions.py first")
GA_ID = row[0]
print(f"[ok] GA jurisdiction id = {GA_ID}")

# ── 2. Ensure GA-FILM-LOGO (10% opt-in) and remove legacy GA-FILM-PROMO ──────
# GA-FILM-PROMO (30%) was the combined base+logo credit — misleading for
# stacking. We use two separate rules instead:
#   GA-FILM-BASE  20%  (base total, no opt-in)
#   GA-FILM-LOGO  10%  (opt-in upside — requires Georgia logo in credits)

new_req = json.dumps({
    "georgiaSpend": 500000,
    "optIn": True,
    "logoInCredits": True,
    "description": "Must include Georgia promotional logo in end credits"
})

# Remove the legacy combined-rate rule if still present
cur.execute("DELETE FROM incentive_rules WHERE \"ruleCode\" = 'GA-FILM-PROMO'")
if cur.rowcount:
    print("[ok] Deleted legacy GA-FILM-PROMO (combined 30%) rule")

# Upsert GA-FILM-LOGO
cur.execute("SELECT id FROM incentive_rules WHERE \"ruleCode\" = 'GA-FILM-LOGO'")
if cur.fetchone():
    cur.execute("""
        UPDATE incentive_rules
        SET percentage = 10.0, requirements = %s, "updatedAt" = %s
        WHERE "ruleCode" = 'GA-FILM-LOGO' AND "jurisdictionId" = %s
    """, (new_req, NOW, GA_ID))
    print("[ok] GA-FILM-LOGO updated (10%, optIn=true)")
else:
    cur.execute("""
        INSERT INTO incentive_rules (
            id, "jurisdictionId", "ruleName", "ruleCode", "incentiveType",
            "creditType", percentage, "eligibleExpenses", "excludedExpenses",
            "effectiveDate", requirements, active, "createdAt", "updatedAt"
        ) VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, true, %s, %s
        )
    """, (
        str(uuid.uuid4()), GA_ID,
        'Georgia Film Tax Credit — Logo Uplift', 'GA-FILM-LOGO', 'tax_credit',
        'refundable', 10.0, '{}', '{}',
        datetime(2024, 1, 1, tzinfo=timezone.utc), new_req, NOW, NOW
    ))
    print("[ok] GA-FILM-LOGO inserted (10%, optIn=true)")

# ── 3. Sub-jurisdictions ──────────────────────────────────────────────────────
SUB_JURISDICTIONS = [
    {
        "name": "Atlanta",
        "code": "GA-ATLANTA",
        "type": "city",
        # atlantaga.gov returns 403 for automated requests (WAF protection).
        # feedUrl left None — manual monitoring required.
        "feedUrl": None,
        "description": (
            "City of Atlanta Office of Film, Entertainment & Nightlife. "
            "Permits page: https://www.atlantaga.gov/government/mayor-s-office/"
            "executive-offices/office-of-film-entertainment-nightlife "
            "(WAF-protected — manual monitoring required)"
        ),
    },
    {
        "name": "Savannah",
        "code": "GA-SAVANNAH",
        "type": "city",
        "feedUrl": "https://www.filmsavannah.org/permits/",
    },
    {
        "name": "Fulton County",
        "code": "GA-FULTON",
        "type": "county",
        "feedUrl": "https://fultoncountyga.gov/fultonfilms",
    },
    {
        "name": "DeKalb County",
        "code": "GA-DEKALB",
        "type": "county",
        "feedUrl": "https://www.dekalbcountyga.gov/planning-and-sustainability/other-permitting-services-1",
    },
]

for j in SUB_JURISDICTIONS:
    cur.execute("SELECT id FROM jurisdictions WHERE code = %s", (j["code"],))
    existing = cur.fetchone()
    if existing:
        cur.execute("""
            UPDATE jurisdictions
            SET "feedUrl" = %s, "feedLastHash" = NULL,
                description = COALESCE(%s, description),
                "updatedAt" = %s
            WHERE code = %s
        """, (j["feedUrl"], j.get("description"), NOW, j["code"]))
        print(f"[ok] {j['code']} updated (feedUrl={'set' if j['feedUrl'] else 'cleared — WAF-blocked'})")
    else:
        cur.execute("""
            INSERT INTO jurisdictions (
                id, name, code, country, type, "parentId",
                active, currency, "treatyPartners",
                description, "feedUrl", "createdAt", "updatedAt"
            ) VALUES (
                %s, %s, %s, %s, %s, %s,
                true, 'USD', '{}',
                %s, %s, %s, %s
            )
        """, (
            str(uuid.uuid4()), j["name"], j["code"], "US", j["type"], GA_ID,
            j.get("description"), j["feedUrl"], NOW, NOW
        ))
        print(f"[ok] {j['code']} inserted")

conn.commit()
conn.close()

print("\nDone. Summary:")
print("  GA-FILM-BASE  20%  base credit (applies to all GA-qualifying films)")
print("  GA-FILM-LOGO  10%  opt-in uplift (requires Georgia logo in credits)")
print("  Sub-jurisdictions: GA-ATLANTA, GA-SAVANNAH, GA-FULTON, GA-DEKALB")
print("  Feed URLs set — monitor.py will fetch on next run")
