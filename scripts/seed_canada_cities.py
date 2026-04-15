"""
seed_canada_cities.py — Vancouver, Toronto, Montreal as sub-jurisdictions
==========================================================================
Canadian financial incentives are at the province level (BC, ON, QC).
City sub-jurisdictions represent local film commissions providing permits
and production support. The parent-state banner correctly directs users
to provincial programs.

Feed URLs verified 2026-04-14.
"""
import os, sys, uuid
from datetime import datetime, timezone
import psycopg2

DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    sys.exit("DATABASE_URL not set")

conn = psycopg2.connect(DB_URL)
conn.autocommit = False
cur = conn.cursor()
NOW = datetime.now(timezone.utc)

PARENTS = {
    'BC': '2e0fc441-5fb6-4588-b946-e8d871338e45',
    'ON': 'f937a3f8-db51-44b2-ba88-240296f11441',
    'QC': 'de3bb997-d922-4dd0-99e0-dc28c6e315eb',
}

SUB_JURISDICTIONS = [
    # ── British Columbia ──────────────────────────────────────────────────────
    {
        'parent': 'BC', 'name': 'Vancouver', 'code': 'BC-VANCOUVER', 'type': 'city',
        'currency': 'CAD',
        'feedUrl': 'https://www.vancouverfilm.ca',
        'description': (
            'Vancouver Film Commission — one of the largest film production hubs in North America. '
            'Manages permits, location scouting, and crew resources for the Greater Vancouver area. '
            'BC province incentives apply: 35% basic tax credit + 28% PSTC for foreign productions. '
            'Additional 6% distant location bonus may not apply within Vancouver metro.'
        ),
    },
    {
        'parent': 'BC', 'name': 'Victoria', 'code': 'BC-VICTORIA', 'type': 'city',
        'currency': 'CAD',
        'feedUrl': None,
        'description': (
            'Victoria / Capital Regional District — BC provincial film permits via Creative BC. '
            'Scenic coastal and heritage locations. BC provincial incentives apply.'
        ),
    },

    # ── Ontario ───────────────────────────────────────────────────────────────
    {
        'parent': 'ON', 'name': 'Toronto', 'code': 'ON-TORONTO', 'type': 'city',
        'currency': 'CAD',
        'feedUrl': 'https://www.toronto.ca/film',
        'description': (
            'Toronto Film, Television and Digital Media Office — Canada\'s largest production hub. '
            'Manages city filming permits, location database, and production assistance. '
            'Ontario incentives apply: OFTTC 35% (domestic) or OPSTC 21.5% (foreign production services). '
            'Toronto is one of the top 5 film production markets in North America.'
        ),
    },
    {
        'parent': 'ON', 'name': 'Ottawa', 'code': 'ON-OTTAWA', 'type': 'city',
        'currency': 'CAD',
        'feedUrl': None,
        'description': (
            'Ottawa Film Office — national capital permits and government location access. '
            'Ontario provincial incentives apply.'
        ),
    },

    # ── Quebec ────────────────────────────────────────────────────────────────
    {
        'parent': 'QC', 'name': 'Montreal', 'code': 'QC-MONTREAL', 'type': 'city',
        'currency': 'CAD',
        'feedUrl': 'https://www.montrealfilm.com',
        'description': (
            'Bureau du cinéma et de la télévision du Québec (BCTQ) / Montreal Film & TV Bureau. '
            'Manages city filming permits and production support for the Greater Montreal area. '
            'Quebec incentives apply: QPSP 40% credit on all eligible Quebec spend; '
            '32% on Quebec resident labor (stackable). '
            'Major studio infrastructure: Mel\'s Studios, Studio Grandé Allée.'
        ),
    },
    {
        'parent': 'QC', 'name': 'Quebec City', 'code': 'QC-QUEBECCITY', 'type': 'city',
        'currency': 'CAD',
        'feedUrl': None,
        'description': (
            'Quebec City film permits — UNESCO heritage old city district, '
            'European-style architecture popular for period and European-set productions. '
            'Quebec provincial incentives apply.'
        ),
    },
]

inserted = 0
updated = 0

for j in SUB_JURISDICTIONS:
    parent_id = PARENTS[j['parent']]
    cur.execute("SELECT id FROM jurisdictions WHERE code = %s", (j['code'],))
    existing = cur.fetchone()
    if existing:
        cur.execute("""
            UPDATE jurisdictions
            SET "feedUrl"=%s, description=%s, "updatedAt"=%s
            WHERE code=%s
        """, (j['feedUrl'], j['description'], NOW, j['code']))
        print(f"[--] {j['code']} updated")
        updated += 1
    else:
        cur.execute("""
            INSERT INTO jurisdictions (
                id, name, code, country, type, "parentId",
                active, currency, "treatyPartners",
                description, "feedUrl", "createdAt", "updatedAt"
            ) VALUES (%s,%s,%s,%s,%s,%s,true,%s,'{}', %s,%s,%s,%s)
        """, (
            str(uuid.uuid4()), j['name'], j['code'], 'CA',
            j['type'], parent_id, j['currency'],
            j['description'], j['feedUrl'], NOW, NOW
        ))
        print(f"[ok] {j['code']} inserted — {j['name']}")
        inserted += 1

conn.commit()
conn.close()
print(f"\nDone. {inserted} inserted, {updated} updated.")
print("Cities added: Vancouver, Victoria (BC) · Toronto, Ottawa (ON) · Montreal, Quebec City (QC)")
