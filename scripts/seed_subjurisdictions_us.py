"""
seed_subjurisdictions_us.py — Sub-jurisdictions for CO, HI, MI, MS, MT, NJ, OR, VA
=====================================================================================
Adds local film office sub-jurisdictions for 8 US states that currently have none.
All are permit/production-support offices; financial incentives are at state level.
Feed URLs verified against known film commission websites (2026-04-14).
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

# ── State parent IDs (hardcoded from DB) ──────────────────────────────────────
PARENTS = {
    'CO': 'f1fc791c-c076-4eb5-ba24-5680a74347f1',
    'HI': '77635413-8c7c-4473-9a24-e8688fa8acfa',
    'MI': 'ee06c2a0-539b-4eb7-b91d-6e2de9c54c57',
    'MS': '1ca7c3cd-a78f-450a-8bf6-ec499f189a68',
    'MT': '639ec950-5a57-40ec-9a7c-e82e4689381e',
    'NJ': 'd473d63a-ee54-4749-9e94-854a8e5e69e9',
    'OR': 'e3cd0091-c491-40c3-b26a-77663369f17a',
    'VA': '4a5b6d14-ed91-4dc6-91c4-17fa9f831457',
}

SUB_JURISDICTIONS = [
    # ── Colorado ──────────────────────────────────────────────────────────────
    {
        'parent': 'CO', 'name': 'Denver', 'code': 'CO-DENVER', 'type': 'city',
        'feedUrl': 'https://www.denvergov.org/film',
        'description': (
            'Denver Film Commission — local film permits, location scouting, '
            'and production support for Denver metro area. Colorado state incentives apply.'
        ),
    },
    {
        'parent': 'CO', 'name': 'Boulder', 'code': 'CO-BOULDER', 'type': 'city',
        'feedUrl': 'https://bouldercolorado.gov/film',
        'description': (
            'City of Boulder film permits and location services. '
            'Colorado state incentives apply to productions shooting in Boulder.'
        ),
    },
    {
        'parent': 'CO', 'name': 'Colorado Springs', 'code': 'CO-COLORADOSPRINGS', 'type': 'city',
        'feedUrl': None,
        'description': (
            'Colorado Springs Film Commission — permits and production support for the Pikes Peak region. '
            'Colorado state incentives apply.'
        ),
    },

    # ── Hawaii ────────────────────────────────────────────────────────────────
    {
        'parent': 'HI', 'name': 'Honolulu', 'code': 'HI-HONOLULU', 'type': 'city',
        'feedUrl': 'https://filmoffice.hawaii.gov',
        'description': (
            'Hawaii Film Office — Oahu/Honolulu permits and production support. '
            'Hawaii state 20% base credit + 5% Oahu uplift applies (Oahu is not a "neighbor island").'
        ),
    },
    {
        'parent': 'HI', 'name': 'Maui County', 'code': 'HI-MAUI', 'type': 'county',
        'feedUrl': 'https://www.filmmaui.com',
        'description': (
            'Maui Film Commission — permits and location services for Maui, Molokai, and Lanai. '
            'Hawaii state 20% base credit + 5% neighbor island uplift applies (25% combined).'
        ),
    },
    {
        'parent': 'HI', 'name': "Hawaii Island (Big Island)", 'code': 'HI-BIGISLAND', 'type': 'county',
        'feedUrl': None,
        'description': (
            'Hawaii County film permits for the Big Island. '
            'Hawaii state 20% base credit + 5% neighbor island uplift applies (25% combined).'
        ),
    },
    {
        'parent': 'HI', 'name': 'Kauai', 'code': 'HI-KAUAI', 'type': 'county',
        'feedUrl': None,
        'description': (
            'County of Kauai film permits and production support. '
            'Hawaii state 20% base credit + 5% neighbor island uplift applies (25% combined).'
        ),
    },

    # ── Michigan ─────────────────────────────────────────────────────────────
    {
        'parent': 'MI', 'name': 'Detroit', 'code': 'MI-DETROIT', 'type': 'city',
        'feedUrl': 'https://www.detroitmi.gov/film',
        'description': (
            'Detroit Film Office — location permits, scout assistance, and production support. '
            'Michigan state 30% rebate applies to qualified Michigan expenditures.'
        ),
    },
    {
        'parent': 'MI', 'name': 'Grand Rapids', 'code': 'MI-GRANDRAPIDS', 'type': 'city',
        'feedUrl': 'https://www.filmgr.com',
        'description': (
            'Film GR (Grand Rapids) — West Michigan film permits and location services. '
            'Michigan state 30% rebate applies.'
        ),
    },

    # ── Mississippi ───────────────────────────────────────────────────────────
    {
        'parent': 'MS', 'name': 'Jackson', 'code': 'MS-JACKSON', 'type': 'city',
        'feedUrl': 'https://www.filmmississippi.org',
        'description': (
            'Film Mississippi — statewide film office headquartered in Jackson. '
            'Mississippi state 25% + 10% resident payroll incentive applies statewide.'
        ),
    },
    {
        'parent': 'MS', 'name': 'Natchez', 'code': 'MS-NATCHEZ', 'type': 'city',
        'feedUrl': None,
        'description': (
            'Natchez, MS — historic location popular for period productions. '
            'Mississippi state incentives apply. Contact Film Mississippi for permits.'
        ),
    },
    {
        'parent': 'MS', 'name': 'Gulf Coast', 'code': 'MS-GULFCOAST', 'type': 'region',
        'feedUrl': None,
        'description': (
            'Mississippi Gulf Coast (Biloxi, Gulfport, Hattiesburg region). '
            'Mississippi state 25% + 10% resident payroll incentive applies. '
            'Local tourism boards offer additional location support.'
        ),
    },

    # ── Montana ───────────────────────────────────────────────────────────────
    {
        'parent': 'MT', 'name': 'Billings', 'code': 'MT-BILLINGS', 'type': 'city',
        'feedUrl': 'https://www.montanafilm.com',
        'description': (
            'Billings area film permits — Montana Film Office handles statewide permitting. '
            'Montana state 35% labor-based tax credit applies.'
        ),
    },
    {
        'parent': 'MT', 'name': 'Missoula', 'code': 'MT-MISSOULA', 'type': 'city',
        'feedUrl': None,
        'description': (
            'Missoula film production support — scenic mountains and Glacier-adjacent locations. '
            'Montana state 35% labor-based tax credit applies.'
        ),
    },
    {
        'parent': 'MT', 'name': 'Bozeman', 'code': 'MT-BOZEMAN', 'type': 'city',
        'feedUrl': None,
        'description': (
            'Bozeman / Big Sky area — popular for outdoor and adventure productions. '
            'Montana state 35% labor-based tax credit applies.'
        ),
    },

    # ── New Jersey ────────────────────────────────────────────────────────────
    {
        'parent': 'NJ', 'name': 'Jersey City', 'code': 'NJ-JERSEYCITY', 'type': 'city',
        'feedUrl': 'https://www.jerseycitynj.gov/film',
        'description': (
            'Jersey City Film Commission — NYC skyline backdrop, diverse locations, '
            'studio access. NJ state 30% + 5% diversity bonus tax credit applies.'
        ),
    },
    {
        'parent': 'NJ', 'name': 'Newark', 'code': 'NJ-NEWARK', 'type': 'city',
        'feedUrl': None,
        'description': (
            'City of Newark film permits and location services. '
            'NJ state 30% + 5% diversity bonus tax credit applies.'
        ),
    },
    {
        'parent': 'NJ', 'name': 'Atlantic City', 'code': 'NJ-ATLANTICCITY', 'type': 'city',
        'feedUrl': None,
        'description': (
            'Atlantic City film permits — casino, boardwalk, and coastal locations. '
            'NJ state 30% + 5% diversity bonus tax credit applies.'
        ),
    },

    # ── Oregon ────────────────────────────────────────────────────────────────
    {
        'parent': 'OR', 'name': 'Portland', 'code': 'OR-PORTLAND', 'type': 'city',
        'feedUrl': 'https://www.portland.gov/film',
        'description': (
            'Portland Film Office — permits, location scouting, and crew resources '
            'for the Portland metro area. Oregon OPIF 20% rebate applies.'
        ),
    },
    {
        'parent': 'OR', 'name': 'Eugene', 'code': 'OR-EUGENE', 'type': 'city',
        'feedUrl': None,
        'description': (
            'Eugene / Lane County film permits and location support. '
            'Oregon OPIF 20% rebate applies to qualified Oregon expenditures.'
        ),
    },

    # ── Virginia ──────────────────────────────────────────────────────────────
    {
        'parent': 'VA', 'name': 'Richmond', 'code': 'VA-RICHMOND', 'type': 'city',
        'feedUrl': 'https://www.visitrichmondva.com/film',
        'description': (
            'Richmond Film Commission — historic architecture, diverse neighborhoods, '
            'and proximity to Northern Virginia studios. VA state 20% + 10% rural credit applies.'
        ),
    },
    {
        'parent': 'VA', 'name': 'Virginia Beach', 'code': 'VA-VIRGINIABEACH', 'type': 'city',
        'feedUrl': 'https://www.visitvirginiabeach.com/film',
        'description': (
            'Virginia Beach Film Commission — oceanfront, military installations, and suburban locations. '
            'Virginia state 20% + 10% rural credit applies.'
        ),
    },
    {
        'parent': 'VA', 'name': 'Northern Virginia', 'code': 'VA-NOVA', 'type': 'region',
        'feedUrl': None,
        'description': (
            'Northern Virginia (Arlington, Fairfax, Alexandria) — DC metro area proximity, '
            'government locations, diverse urban environments. '
            'Virginia state 20% tax credit applies. Productions may access both VA and DC incentives.'
        ),
    },
    {
        'parent': 'VA', 'name': 'Shenandoah Valley', 'code': 'VA-SHENANDOAH', 'type': 'region',
        'feedUrl': None,
        'description': (
            'Shenandoah Valley and Blue Ridge — scenic mountain landscapes popular for outdoor productions. '
            'Virginia state 20% + 10% rural enhanced credit applies to this region.'
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
            SET "feedUrl" = %s, description = %s, "updatedAt" = %s
            WHERE code = %s
        """, (j['feedUrl'], j['description'], NOW, j['code']))
        print(f"[--] {j['code']} already exists, updated")
        updated += 1
    else:
        cur.execute("""
            INSERT INTO jurisdictions (
                id, name, code, country, type, "parentId",
                active, currency, "treatyPartners",
                description, "feedUrl", "createdAt", "updatedAt"
            ) VALUES (%s,%s,%s,%s,%s,%s,true,'USD','{}', %s,%s,%s,%s)
        """, (
            str(uuid.uuid4()), j['name'], j['code'], 'US', j['type'], parent_id,
            j['description'], j['feedUrl'], NOW, NOW
        ))
        print(f"[ok] {j['code']} inserted — {j['name']}")
        inserted += 1

conn.commit()
conn.close()
print(f"\nDone. {inserted} inserted, {updated} updated.")
print("Sub-jurisdictions added for: CO (3), HI (4), MI (2), MS (3), MT (3), NJ (3), OR (2), VA (4)")
