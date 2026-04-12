import psycopg2, os, json

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()
cur.execute("""
    SELECT pr.id, j.code, j.name, pr."sourceUrl", pr.confidence, pr.status,
           pr."extractedData"::text
    FROM pending_rules pr
    JOIN jurisdictions j ON j.id = pr."jurisdictionId"
    WHERE j.code LIKE 'GA-%'
    ORDER BY pr."createdAt" DESC
    LIMIT 10
""")
for row in cur.fetchall():
    print(f'{row[1]} ({row[2]}): conf={row[4]}, status={row[5]}')
    raw = row[6]
    data = json.loads(raw) if isinstance(raw, str) else raw
    # extractedData may be a JSON string of a dict, or a double-encoded string
    if isinstance(data, str):
        data = json.loads(data)
    rules = data.get('rules', [])
    for r in rules:
        print(f'  rule: {r.get("name")} | type={r.get("rule_type")} | amt={r.get("amount")} | pct={r.get("percentage")}')
    if not rules:
        print(f'  (no rules extracted) summary={data.get("summary","?")}')
conn.close()
