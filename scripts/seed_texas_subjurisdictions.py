"""
seed_texas_subjurisdictions.py — Texas local jurisdiction setup
===============================================================
TX-AUSTIN and TX-HOUSTON already exist (seeded previously).
Adds: TX-DALLAS, TX-FORTWORTH, TX-SANANTONIO
Updates: TX-HOUSTON feedUrl with verified URL

Feed URL verification (all checked 2026-04-13):
  TX-AUSTIN     — no verified city film commission URL found; stays NULL
  TX-DALLAS     — filmdallas.com (200) homepage only, no permit path verified
  TX-FORTWORTH  — fortworthtexas.gov/departments/communications/media-relations (200)
  TX-HOUSTON    — www.houstonfilmcommission.com (200) confirmed
  TX-SANANTONIO — www.filmsanantonio.com/permits/ (200) confirmed
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

# ── Locate TX jurisdiction ────────────────────────────────────────────────────
cur.execute("SELECT id FROM jurisdictions WHERE code = 'TX'")
row = cur.fetchone()
if not row:
    sys.exit("ERROR: TX jurisdiction not found")
TX_ID = row[0]
print(f"[ok] TX jurisdiction id = {TX_ID}")

# ── Update TX-HOUSTON feedUrl ─────────────────────────────────────────────────
cur.execute("""
    UPDATE jurisdictions
    SET "feedUrl" = 'https://www.houstonfilmcommission.com',
        "updatedAt" = %s
    WHERE code = 'TX-HOUSTON'
""", (NOW,))
print(f"[ok] TX-HOUSTON feedUrl updated → houstonfilmcommission.com ({cur.rowcount} row)")

# ── New sub-jurisdictions ─────────────────────────────────────────────────────
SUB_JURISDICTIONS = [
    {
        "name": "Dallas",
        "code": "TX-DALLAS",
        "type": "city",
        "feedUrl": "https://filmdallas.com/",
        "description": (
            "Film Dallas — local film permits and production services. "
            "Homepage verified live; no dedicated permit path found."
        ),
    },
    {
        "name": "Fort Worth",
        "code": "TX-FORTWORTH",
        "type": "city",
        "feedUrl": "https://www.fortworthtexas.gov/departments/communications/media-relations",
        "description": (
            "City of Fort Worth — Media Relations / Film Office. "
            "Handles film permit inquiries and production coordination."
        ),
    },
    {
        "name": "San Antonio",
        "code": "TX-SANANTONIO",
        "type": "city",
        "feedUrl": "https://www.filmsanantonio.com/permits/",
        "description": (
            "Film San Antonio — local film permits, location services, and production support."
        ),
    },
]

for j in SUB_JURISDICTIONS:
    cur.execute("SELECT id FROM jurisdictions WHERE code = %s", (j["code"],))
    if cur.fetchone():
        cur.execute("""
            UPDATE jurisdictions
            SET "feedUrl" = %s,
                description = %s,
                "updatedAt" = %s
            WHERE code = %s
        """, (j["feedUrl"], j["description"], NOW, j["code"]))
        print(f"[ok] {j['code']} updated")
    else:
        cur.execute("""
            INSERT INTO jurisdictions (
                id, name, code, country, type, "parentId",
                active, currency, "treatyPartners",
                description, "feedUrl", "createdAt", "updatedAt"
            ) VALUES (%s,%s,%s,%s,%s,%s,true,'USD','{}', %s,%s,%s,%s)
        """, (
            str(uuid.uuid4()), j["name"], j["code"], "US", j["type"], TX_ID,
            j["description"], j["feedUrl"], NOW, NOW
        ))
        print(f"[ok] {j['code']} inserted — feedUrl: {j['feedUrl']}")

conn.commit()
conn.close()

print("\nDone. Texas sub-jurisdiction summary:")
print("  TX-AUSTIN      feedUrl: NULL (no verified city film office URL)")
print("  TX-DALLAS      feedUrl: filmdallas.com/")
print("  TX-FORTWORTH   feedUrl: fortworthtexas.gov/departments/communications/media-relations")
print("  TX-HOUSTON     feedUrl: houstonfilmcommission.com")
print("  TX-SANANTONIO  feedUrl: filmsanantonio.com/permits/")
