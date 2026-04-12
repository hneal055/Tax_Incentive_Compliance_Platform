import psycopg2, os

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()
cur.execute("""
    SELECT ir.id, ir."ruleCode", ir."ruleName", ir.percentage, ir.requirements, ir.active
    FROM incentive_rules ir
    JOIN jurisdictions j ON j.id = ir."jurisdictionId"
    WHERE j.code = 'GA'
    ORDER BY ir."ruleCode"
""")
for r in cur.fetchall():
    print(r)
conn.close()
