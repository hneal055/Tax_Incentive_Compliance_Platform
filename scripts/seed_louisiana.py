"""
seed_louisiana.py — Louisiana incentive rules cleanup + music/VFX bonus
=======================================================================
1. Delete duplicate LA-PAYROLL-BONUS (superseded by LA-FILM-PAYROLL-BONUS)
2. Upsert LA-MUSIC-BONUS (5% opt-in for Louisiana music or VFX work)

Jurisdiction already exists as code='LA'. Does NOT touch LA-FILM-BASE or
LA-FILM-PAYROLL-BONUS — those are correct.
"""

import os, json, uuid, sys
from datetime import datetime, timezone

import psycopg2

DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    sys.exit("DATABASE_URL not set")

conn = psycopg2.connect(DB_URL)
conn.autocommit = False
cur = conn.cursor()

NOW = datetime.now(timezone.utc)

# ── 1. Locate LA jurisdiction ─────────────────────────────────────────────────
cur.execute("SELECT id FROM jurisdictions WHERE code = 'LA'")
row = cur.fetchone()
if not row:
    sys.exit("ERROR: LA jurisdiction not found — run seed_jurisdictions.py first")
LA_ID = row[0]
print(f"[ok] LA jurisdiction id = {LA_ID}")

# ── 2. Remove duplicate payroll rule ─────────────────────────────────────────
cur.execute("DELETE FROM incentive_rules WHERE \"ruleCode\" = 'LA-PAYROLL-BONUS'")
if cur.rowcount:
    print("[ok] Deleted duplicate LA-PAYROLL-BONUS (superseded by LA-FILM-PAYROLL-BONUS)")
else:
    print("[--] LA-PAYROLL-BONUS not found (already removed)")

# ── 3. Upsert LA-MUSIC-BONUS (5% opt-in) ─────────────────────────────────────
music_req = json.dumps({
    "optIn": True,
    "requiresLAMusicOrVFX": True,
    "description": (
        "5% bonus on qualifying expenditures for productions that use "
        "Louisiana-based music or VFX services. Stacks with base 25% and "
        "labor 10% for a maximum effective rate of 40%. "
        "Cite: LA R.S. 47:6007"
    )
})

cur.execute("SELECT id FROM incentive_rules WHERE \"ruleCode\" = 'LA-MUSIC-BONUS'")
if cur.fetchone():
    cur.execute("""
        UPDATE incentive_rules
        SET percentage = 5.0,
            "ruleName" = 'Louisiana Music or VFX Bonus',
            requirements = %s,
            "updatedAt" = %s
        WHERE "ruleCode" = 'LA-MUSIC-BONUS' AND "jurisdictionId" = %s
    """, (music_req, NOW, LA_ID))
    print("[ok] LA-MUSIC-BONUS updated (5%, optIn=true)")
else:
    cur.execute("""
        INSERT INTO incentive_rules (
            id, "jurisdictionId", "ruleName", "ruleCode", "incentiveType",
            "creditType", percentage, "eligibleExpenses", "excludedExpenses",
            "effectiveDate", requirements, active, "createdAt", "updatedAt"
        ) VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, true, %s, %s
        )
    """, (
        str(uuid.uuid4()), LA_ID,
        'Louisiana Music or VFX Bonus', 'LA-MUSIC-BONUS', 'tax_credit',
        'transferable', 5.0, '{}', '{}',
        datetime(2024, 1, 1, tzinfo=timezone.utc), music_req, NOW, NOW
    ))
    print("[ok] LA-MUSIC-BONUS inserted (5%, optIn=true)")

conn.commit()
conn.close()

print("\nDone. Louisiana incentive rules summary:")
print("  LA-FILM-BASE         25%  base transferable credit ($300K min LA spend)")
print("  LA-FILM-PAYROLL-BONUS 10%  opt-in — resident labor only (stacks to 35%)")
print("  LA-MUSIC-BONUS        5%  opt-in — LA music or VFX (stacks to 40%)")
