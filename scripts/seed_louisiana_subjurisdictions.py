"""
seed_louisiana_subjurisdictions.py — Louisiana local jurisdiction setup
=======================================================================
Adds Baton Rouge, Shreveport, and Jefferson Parish as sub-jurisdictions of LA.
New Orleans (LA-NEW-ORLEANS) already exists — skipped.

Feed URL policy:
  - Baton Rouge:      batonrougefilm.com/permits/ (verified 200)
  - Shreveport:       None — no verified film office URL found; manual monitoring
  - Jefferson Parish: None — no verified film office URL found; manual monitoring
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

# ── Locate LA state jurisdiction ──────────────────────────────────────────────
cur.execute("SELECT id FROM jurisdictions WHERE code = 'LA'")
row = cur.fetchone()
if not row:
    sys.exit("ERROR: LA jurisdiction not found — run seed_jurisdictions.py first")
LA_ID = row[0]
print(f"[ok] LA jurisdiction id = {LA_ID}")

# ── Sub-jurisdictions ─────────────────────────────────────────────────────────
SUB_JURISDICTIONS = [
    {
        "name": "Baton Rouge",
        "code": "LA-BATONROUGE",
        "type": "city",
        "feedUrl": "https://batonrougefilm.com/permits/",
        "description": "Baton Rouge Film Commission — local permits and production services.",
    },
    {
        "name": "Shreveport",
        "code": "LA-SHREVEPORT",
        "type": "city",
        "feedUrl": None,
        "description": (
            "Shreveport-Bossier Film Office. "
            "No verified automated feed URL found — manual monitoring required. "
            "City gov: https://www.shreveportla.gov (blocks automated fetching)"
        ),
    },
    {
        "name": "Jefferson Parish",
        "code": "LA-JEFFERSON",
        "type": "parish",
        "feedUrl": None,
        "description": (
            "Jefferson Parish film permits. "
            "No verified automated feed URL found — manual monitoring required. "
            "Parish gov: https://www.jeffparish.net"
        ),
    },
]

for j in SUB_JURISDICTIONS:
    cur.execute("SELECT id FROM jurisdictions WHERE code = %s", (j["code"],))
    existing = cur.fetchone()
    if existing:
        cur.execute("""
            UPDATE jurisdictions
            SET "feedUrl" = %s,
                description = COALESCE(%s, description),
                "updatedAt" = %s
            WHERE code = %s
        """, (j["feedUrl"], j.get("description"), NOW, j["code"]))
        print(f"[ok] {j['code']} updated (feedUrl={'set' if j['feedUrl'] else 'cleared — no verified URL'})")
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
            str(uuid.uuid4()), j["name"], j["code"], "US", j["type"], LA_ID,
            j.get("description"), j["feedUrl"], NOW, NOW
        ))
        print(f"[ok] {j['code']} inserted (feedUrl={'set' if j['feedUrl'] else 'None — manual monitoring'})")

conn.commit()
conn.close()

print("\nDone. Louisiana sub-jurisdiction summary:")
print("  LA-NEW-ORLEANS  (pre-existing) feedUrl: nolafilm.com/feed")
print("  LA-BATONROUGE   feedUrl: batonrougefilm.com/permits/")
print("  LA-SHREVEPORT   feedUrl: None (manual monitoring)")
print("  LA-JEFFERSON    feedUrl: None (manual monitoring)")
