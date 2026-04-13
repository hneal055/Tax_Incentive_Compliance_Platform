"""
seed_california_subjurisdictions.py — California local jurisdiction setup
=========================================================================
Adds San Francisco, San Diego, Sacramento, and Oakland as sub-jurisdictions of CA.
Los Angeles County (CA-LA) already exists — skipped.

All feed URLs verified live (200) as of 2026-04-13.
Proposed URLs were dead — replaced with confirmed film office URLs.
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

# ── Locate CA state jurisdiction ──────────────────────────────────────────────
cur.execute("SELECT id FROM jurisdictions WHERE code = 'CA'")
row = cur.fetchone()
if not row:
    sys.exit("ERROR: CA jurisdiction not found — run seed_jurisdictions.py first")
CA_ID = row[0]
print(f"[ok] CA jurisdiction id = {CA_ID}")

# ── Sub-jurisdictions ─────────────────────────────────────────────────────────
SUB_JURISDICTIONS = [
    {
        "name": "San Francisco",
        "code": "CA-SANFRANCISCO",
        "type": "city",
        "feedUrl": "https://oewd.org/film-san-francisco",
        "description": (
            "San Francisco Film Commission (OEWD). "
            "Local film permits, location scouting, and production support."
        ),
    },
    {
        "name": "San Diego",
        "code": "CA-SANDIEGO",
        "type": "city",
        "feedUrl": "https://www.sandiego.gov/specialevents-filming/filming",
        "description": (
            "City of San Diego Special Events & Filming Office. "
            "Film permit applications and location resources."
        ),
    },
    {
        "name": "Sacramento",
        "code": "CA-SACRAMENTO",
        "type": "city",
        "feedUrl": "https://filmsac.com/permitting/",
        "description": (
            "Sacramento Film Commission (filmsac.com). "
            "Local permits, crew resources, and location services."
        ),
    },
    {
        "name": "Oakland",
        "code": "CA-OAKLAND",
        "type": "city",
        "feedUrl": "https://www.oaklandca.gov/Business/Oakland-Economic-Development/Film-Office",
        "description": (
            "Oakland Film Office — Economic Development. "
            "Film permit applications and production support."
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
        print(f"[ok] {j['code']} updated")
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
            str(uuid.uuid4()), j["name"], j["code"], "US", j["type"], CA_ID,
            j.get("description"), j["feedUrl"], NOW, NOW
        ))
        print(f"[ok] {j['code']} inserted — feedUrl: {j['feedUrl']}")

conn.commit()
conn.close()

print("\nDone. California sub-jurisdiction summary:")
print("  CA-LA            (pre-existing) feedUrl: filmla.com")
print("  CA-SANFRANCISCO  feedUrl: oewd.org/film-san-francisco")
print("  CA-SANDIEGO      feedUrl: sandiego.gov/specialevents-filming/filming")
print("  CA-SACRAMENTO    feedUrl: filmsac.com/permitting/")
print("  CA-OAKLAND       feedUrl: oaklandca.gov/Business/Oakland-Economic-Development/Film-Office")
