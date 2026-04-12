"""
Move IL-CHICAGO-BONUS from the IL state jurisdiction to the IL-COOK
sub-jurisdiction so spend_by_location correctly scopes it to Chicago spend.

The bonus is a state-administered credit but applies only to Cook County /
Chicago production activity — it belongs under IL-COOK for computation.
"""
import psycopg2, os
from datetime import datetime, timezone

conn = psycopg2.connect(os.environ['DATABASE_URL'])
conn.autocommit = True
cur = conn.cursor()

NOW = datetime.now(timezone.utc)

# Get IL-COOK jurisdiction id
cur.execute("SELECT id, name FROM jurisdictions WHERE code = 'IL-COOK'")
row = cur.fetchone()
if not row:
    print("ERROR: IL-COOK jurisdiction not found")
    conn.close()
    raise SystemExit(1)
il_cook_id, il_cook_name = row
print(f"[ok] IL-COOK id = {il_cook_id} ({il_cook_name})")

# Move IL-CHICAGO-BONUS to IL-COOK
cur.execute("""
    UPDATE incentive_rules
    SET "jurisdictionId" = %s, "updatedAt" = %s
    WHERE "ruleCode" = 'IL-CHICAGO-BONUS'
""", (il_cook_id, NOW))

if cur.rowcount:
    print(f"[ok] IL-CHICAGO-BONUS moved to IL-COOK ({cur.rowcount} row)")
else:
    print("WARNING: IL-CHICAGO-BONUS not found")

# Verify
cur.execute("""
    SELECT ir."ruleCode", j.code, j.name, ir.percentage
    FROM incentive_rules ir
    JOIN jurisdictions j ON j.id = ir."jurisdictionId"
    WHERE ir."ruleCode" IN ('IL-FILM-BASE', 'IL-CHICAGO-BONUS', 'IL-FILM-GREEN-BONUS', 'IL-FILM-RELOCATION-BONUS')
    ORDER BY j.code, ir."ruleCode"
""")
print("\nIL rules after update:")
for r in cur.fetchall():
    print(f"  {r[0]:35s} | {r[1]:15s} | {r[3]}%")

conn.close()
