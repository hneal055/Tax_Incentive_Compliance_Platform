import psycopg2, os

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()
cur.execute("SELECT \"ruleCode\", percentage, requirements FROM incentive_rules WHERE \"ruleCode\" LIKE 'IL-%'")
for r in cur.fetchall():
    print(r)
conn.close()
