import psycopg2, os

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()
cur.execute("""
    SELECT ir.id, ir."ruleCode", ir.percentage, ir."fixedAmount", ir.active,
           j.name as jname, j.code as jcode
    FROM incentive_rules ir
    JOIN jurisdictions j ON j.id = ir."jurisdictionId"
    WHERE ir."ruleCode" = 'IL-FILM-BASE'
""")
for r in cur.fetchall():
    print(r)
conn.close()
