"""
seed_uk_subjurisdictions.py — UK nations + London as sub-jurisdictions
=======================================================================
Each UK nation has its own screen agency and additional financial programs
that stack on top of the UK AVEC (34% film/HETV, 39% animation).

UK-LONDON:       Film London — Production Growth Fund, studio support
UK-SCOTLAND:     Screen Scotland — Production Growth Fund (up to £1M)
UK-WALES:        Creative Wales — Wales Screen Fund (up to £2M)
UK-NORTHERN-IRELAND: NI Screen — various production funds

Feed URLs verified 2026-04-14.
"""
import os, sys, uuid
from datetime import datetime, timezone
import psycopg2
import json

DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    sys.exit("DATABASE_URL not set")

conn = psycopg2.connect(DB_URL)
conn.autocommit = False
cur = conn.cursor()
NOW = datetime.now(timezone.utc)
EFF = datetime(2024, 1, 1, tzinfo=timezone.utc)

UK_ID = '7318020c-02e1-4d51-9886-ace13b852ef5'

# ── Sub-jurisdictions ─────────────────────────────────────────────────────────
SUB_JURS = [
    {
        'name':    'London',
        'code':    'UK-LONDON',
        'type':    'city',
        'currency': 'GBP',
        'feedUrl': 'https://filmlondon.org.uk',
        'description': (
            'Film London — official film office for Greater London. '
            'Manages permits for filming on public land, Location Register, '
            'and the Film London Production Growth Fund (discretionary grants up to £250K). '
            'UK AVEC (34%) applies to all qualifying London expenditure.'
        ),
    },
    {
        'name':    'Scotland',
        'code':    'UK-SCOTLAND',
        'type':    'region',
        'currency': 'GBP',
        'feedUrl': 'https://www.screen.scot',
        'description': (
            'Screen Scotland (Creative Scotland) — the national screen agency for Scotland. '
            'Administers the Screen Scotland Production Growth Fund (up to £1M discretionary grant) '
            'which can stack with UK AVEC. Also manages the Screen Scotland Development Fund. '
            'Locations: Edinburgh, Glasgow, Highlands, Islands.'
        ),
    },
    {
        'name':    'Wales',
        'code':    'UK-WALES',
        'type':    'region',
        'currency': 'GBP',
        'feedUrl': 'https://creativewales.wales',
        'description': (
            'Creative Wales — the Welsh Government\'s screen agency. '
            'Administers the Wales Screen Fund providing up to £2M per project (discretionary). '
            'Locations: Cardiff, Swansea, Snowdonia, Pembrokeshire. '
            'UK AVEC (34%) applies to qualifying Welsh expenditure.'
        ),
    },
    {
        'name':    'Northern Ireland',
        'code':    'UK-NORTHERN-IRELAND',
        'type':    'region',
        'currency': 'GBP',
        'feedUrl': 'https://northernirelandscreen.co.uk',
        'description': (
            'Northern Ireland Screen — the national screen agency for Northern Ireland. '
            'Administers production funding, the Ulster-Scots Broadcast Fund, and '
            'the Irish Language Broadcast Fund. '
            'Home of major studio infrastructure (Belfast Harbour Studios, Paint Hall). '
            'UK AVEC (34%) applies to qualifying NI expenditure.'
        ),
    },
]

# ── Incentive rules for each nation ──────────────────────────────────────────
NATION_RULES = {
    'UK-LONDON': [
        {
            'ruleName':      'Film London Production Growth Fund',
            'ruleCode':      'UK-LONDON-PRODUCTION-GROWTH-FUND',
            'incentiveType': 'grant',
            'creditType':    'grant',
            'percentage':    None,
            'fixedAmount':   250_000,
            'requirements':  json.dumps({
                'optIn': True,
                'description': (
                    'Film London discretionary grant up to £250,000 for qualifying productions. '
                    'Competitive — productions must demonstrate significant London spend and creative benefit. '
                    'Stacks with UK AVEC. Apply via filmlondon.org.uk/production-growth-fund. '
                    'Source: filmlondon.org.uk'
                )
            }),
        },
    ],
    'UK-SCOTLAND': [
        {
            'ruleName':      'Screen Scotland Production Growth Fund',
            'ruleCode':      'UK-SCOTLAND-PRODUCTION-GROWTH-FUND',
            'incentiveType': 'grant',
            'creditType':    'grant',
            'percentage':    None,
            'fixedAmount':   1_000_000,
            'requirements':  json.dumps({
                'optIn': True,
                'description': (
                    'Screen Scotland discretionary production grant up to £1,000,000. '
                    'Must demonstrate significant Scottish creative and economic benefit. '
                    'Stacks with UK AVEC (34%). Competitive application. '
                    'Source: screen.scot/funding-and-support/production-growth-fund'
                )
            }),
        },
    ],
    'UK-WALES': [
        {
            'ruleName':      'Wales Screen Fund',
            'ruleCode':      'UK-WALES-SCREEN-FUND',
            'incentiveType': 'grant',
            'creditType':    'grant',
            'percentage':    None,
            'fixedAmount':   2_000_000,
            'requirements':  json.dumps({
                'optIn': True,
                'description': (
                    'Creative Wales Screen Fund — discretionary production investment up to £2,000,000. '
                    'Must demonstrate Welsh cultural relevance and economic impact. '
                    'Stacks with UK AVEC (34%). Competitive application. '
                    'Source: creativewales.wales'
                )
            }),
        },
    ],
    'UK-NORTHERN-IRELAND': [
        {
            'ruleName':      'Northern Ireland Screen Production Fund',
            'ruleCode':      'UK-NI-PRODUCTION-FUND',
            'incentiveType': 'grant',
            'creditType':    'grant',
            'percentage':    None,
            'fixedAmount':   500_000,
            'requirements':  json.dumps({
                'optIn': True,
                'description': (
                    'Northern Ireland Screen discretionary production fund. '
                    'Must shoot primarily in Northern Ireland with NI crew/cast engagement. '
                    'Stacks with UK AVEC (34%). '
                    'Source: northernirelandscreen.co.uk/funding'
                )
            }),
        },
    ],
}

inserted_jurs = 0
inserted_rules = 0

for j in SUB_JURS:
    cur.execute("SELECT id FROM jurisdictions WHERE code = %s", (j['code'],))
    existing = cur.fetchone()
    if existing:
        jur_id = existing[0]
        cur.execute("""
            UPDATE jurisdictions SET "feedUrl"=%s, description=%s, "updatedAt"=%s
            WHERE code=%s
        """, (j['feedUrl'], j['description'], NOW, j['code']))
        print(f"[--] {j['code']} updated")
    else:
        jur_id = str(uuid.uuid4())
        cur.execute("""
            INSERT INTO jurisdictions (
                id, name, code, country, type, "parentId",
                active, currency, "treatyPartners",
                description, "feedUrl", "createdAt", "updatedAt"
            ) VALUES (%s,%s,%s,%s,%s,%s,true,%s,'{}', %s,%s,%s,%s)
        """, (
            jur_id, j['name'], j['code'], 'UK', j['type'], UK_ID,
            j['currency'], j['description'], j['feedUrl'], NOW, NOW
        ))
        print(f"[ok] {j['code']} inserted — {j['name']}")
        inserted_jurs += 1

    for r in NATION_RULES.get(j['code'], []):
        cur.execute('SELECT id FROM incentive_rules WHERE "ruleCode" = %s', (r['ruleCode'],))
        if cur.fetchone():
            print(f"[--] {r['ruleCode']} already exists")
            continue
        cur.execute("""
            INSERT INTO incentive_rules (
                id, "jurisdictionId", "ruleName", "ruleCode",
                "incentiveType", "creditType", percentage, "fixedAmount",
                "eligibleExpenses", "excludedExpenses",
                "effectiveDate", requirements,
                active, "createdAt", "updatedAt"
            ) VALUES (%s,
                (SELECT id FROM jurisdictions WHERE code=%s),
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,true,%s,%s)
        """, (
            str(uuid.uuid4()), j['code'],
            r['ruleName'], r['ruleCode'],
            r['incentiveType'], r['creditType'], r['percentage'], r['fixedAmount'],
            '{}', '{}',
            EFF, r['requirements'],
            NOW, NOW
        ))
        print(f"[ok] {r['ruleCode']} inserted")
        inserted_rules += 1

conn.commit()
conn.close()
print(f"\nDone. {inserted_jurs} UK sub-jurisdictions inserted, {inserted_rules} rules seeded.")
