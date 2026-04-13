import psycopg2, os, uuid, json
from datetime import datetime, timezone

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()
NOW = datetime.now(timezone.utc)
EFF = datetime(2024, 1, 1, tzinfo=timezone.utc)

SA_PR_ID = '23d66b25-cb7f-47c1-bf2e-31ecad3380c6'
SA_ID    = 'bc370e4d-25a5-45e0-bc36-158bcdd91dfd'

# 1. Approve SA pending record
cur.execute("""
    UPDATE pending_rules SET status = 'approved', "reviewedAt" = %s,
    "reviewNotes" = 'Rule 0 (14%% local incentive) verified on filmsanantonio.com, seeded as TX-SA-LOCAL-INCENTIVE. Rule 1 (45%% combined total) rejected — unverifiable marketing figure. Rule 2 (permit) added to jurisdiction_requirements.'
    WHERE id = %s
""", (NOW, SA_PR_ID))
print(f'[ok] TX-SANANTONIO pending record approved ({cur.rowcount} row)')

# 2. Insert TX-SA-LOCAL-INCENTIVE (14% opt-in local grant)
sa_req = json.dumps({
    "optIn": True,
    "description": (
        "City of San Antonio local production incentive — up to 14%. "
        "Verified on filmsanantonio.com. Stacks with TX state grant (max 22.5%) "
        "for a combined 36.5% on fully qualified spend. "
        "Note: filmsanantonio.com claims 'up to 45% combined' — verified math is 14% + 22.5% = 36.5%. "
        "Source: https://www.filmsanantonio.com/local-incentives/"
    )
})
cur.execute('SELECT id FROM incentive_rules WHERE "ruleCode" = %s', ('TX-SA-LOCAL-INCENTIVE',))
if cur.fetchone():
    cur.execute("""UPDATE incentive_rules SET percentage=14.0, requirements=%s, "updatedAt"=%s
        WHERE "ruleCode"='TX-SA-LOCAL-INCENTIVE'""", (sa_req, NOW))
    print('[ok] TX-SA-LOCAL-INCENTIVE updated')
else:
    cur.execute("""
        INSERT INTO incentive_rules
            (id, "jurisdictionId", "ruleName", "ruleCode", "incentiveType",
             "creditType", percentage, "eligibleExpenses", "excludedExpenses",
             "effectiveDate", requirements, active, "createdAt", "updatedAt")
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,true,%s,%s)
    """, (
        str(uuid.uuid4()), SA_ID,
        'San Antonio Local Production Incentive', 'TX-SA-LOCAL-INCENTIVE', 'rebate',
        'grant', 14.0, '{}', '{}', EFF, sa_req, NOW, NOW
    ))
    print('[ok] TX-SA-LOCAL-INCENTIVE inserted (14%, opt-in)')

# 3. Insert SA permit requirement
cur.execute("""
    INSERT INTO jurisdiction_requirements
        (id, "jurisdictionId", name, category, "requirementType",
         description, "applicableTo", "sourceUrl", "extractedBy",
         active, "createdAt", "updatedAt")
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'monitor',true,%s,%s)
    ON CONFLICT DO NOTHING
""", (
    str(uuid.uuid4()), SA_ID,
    'City Film Permit — San Antonio City Properties', 'permit', 'requirement',
    'Film productions shooting on any of 250+ City of San Antonio-owned properties must obtain a film permit through the San Antonio Film Commission.',
    ['film', 'tv', 'commercial', 'music_video'],
    'https://www.filmsanantonio.com/permits/',
    NOW, NOW
))
print('[ok] TX-SANANTONIO requirement inserted: City Film Permit')

conn.commit()
conn.close()
print('\nDone.')
