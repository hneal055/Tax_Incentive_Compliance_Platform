"""
seed_new_mexico.py — New Mexico incentive rules correction + sub-jurisdiction update
=====================================================================================
Changes:
  1. Fix NM-FILM-TV-UPLIFT  — set optIn=true, correct conditions (6-ep minimum, etc.)
  2. Delete NM-VETERAN-BONUS — not a real NM program
  3. Insert NM-QPF-UPLIFT    — +5% Qualified Production Facility uplift (opt-in)
  4. Insert NM-RURAL-UPLIFT  — +10% Filming Uplift Zone (60+ miles outside SF/ABQ)
  5. Fix NM-ALBUQUERQUE feedUrl — cabq.gov/film/rss was 404; correct to cabq.gov/film
  6. Insert NM-SANTAFE sub-jurisdiction — santafe.org/film (verified 200)

Source: https://www.nmfilm.com/incentives
Max stacked rate: 25% base + 5% TV + 5% QPF + 10% Rural = 45%
nmfilm.com advertises "up to 40%" — QPF and Rural are unlikely to stack simultaneously.
Credits are REFUNDABLE (not transferable).
"""

import os, uuid, sys, json
from datetime import datetime, timezone

import psycopg2

DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    sys.exit("DATABASE_URL not set")

conn = psycopg2.connect(DB_URL)
conn.autocommit = False
cur = conn.cursor()
NOW = datetime.now(timezone.utc)
EFF = datetime(2024, 1, 1, tzinfo=timezone.utc)

# ── Locate NM state jurisdiction ──────────────────────────────────────────────
cur.execute("SELECT id FROM jurisdictions WHERE code = 'NM'")
row = cur.fetchone()
if not row:
    sys.exit("ERROR: NM jurisdiction not found")
NM_ID = row[0]
print(f"[ok] NM jurisdiction id = {NM_ID}")

# ── 1. Fix NM-FILM-TV-UPLIFT → optIn=true, correct conditions ────────────────
tv_req = json.dumps({
    "optIn": True,
    "conditions": [
        "Series TV: commercial distribution, 6+ episode order, $50K+ NM budget per episode",
        "Standalone pilot: intended for series production in New Mexico"
    ],
    "description": (
        "Additional 5% for TV series or qualifying standalone pilots. "
        "Series must have a 6-episode minimum order and $50K+ NM budget per episode. "
        "Pilot must be intended for series production in NM. "
        "Cite: nmfilm.com/incentives"
    )
})
cur.execute("""
    UPDATE incentive_rules
    SET requirements = %s, "updatedAt" = %s
    WHERE "ruleCode" = 'NM-FILM-TV-UPLIFT'
""", (tv_req, NOW))
print(f"[ok] NM-FILM-TV-UPLIFT updated — optIn=true, conditions corrected ({cur.rowcount} row)")

# ── 2. Delete NM-VETERAN-BONUS — not a real NM program ───────────────────────
cur.execute("DELETE FROM incentive_rules WHERE \"ruleCode\" = 'NM-VETERAN-BONUS'")
print(f"[ok] NM-VETERAN-BONUS deleted ({cur.rowcount} row)")

# ── 3. Insert NM-QPF-UPLIFT (+5% Qualified Production Facility) ──────────────
qpf_req = json.dumps({
    "optIn": True,
    "requiresQPF": True,
    "description": (
        "Additional 5% on qualifying spend at a New Mexico Qualified Production Facility "
        "(soundstage or standing set). Uplift applies only to time spent in production "
        "at the QPF — does not apply to attached offices. "
        "Cite: nmfilm.com/incentives"
    )
})
cur.execute("SELECT id FROM incentive_rules WHERE \"ruleCode\" = 'NM-QPF-UPLIFT'")
if cur.fetchone():
    cur.execute("""
        UPDATE incentive_rules
        SET percentage = 5.0, requirements = %s, "updatedAt" = %s
        WHERE "ruleCode" = 'NM-QPF-UPLIFT'
    """, (qpf_req, NOW))
    print(f"[ok] NM-QPF-UPLIFT updated")
else:
    cur.execute("""
        INSERT INTO incentive_rules (
            id, "jurisdictionId", "ruleName", "ruleCode", "incentiveType",
            "creditType", percentage, "eligibleExpenses", "excludedExpenses",
            "effectiveDate", requirements, active, "createdAt", "updatedAt"
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,true,%s,%s)
    """, (
        str(uuid.uuid4()), NM_ID,
        'New Mexico QPF Uplift', 'NM-QPF-UPLIFT', 'tax_credit',
        'refundable', 5.0, '{}', '{}',
        EFF, qpf_req, NOW, NOW
    ))
    print(f"[ok] NM-QPF-UPLIFT inserted (+5%, opt-in, QPF required)")

# ── 4. Insert NM-RURAL-UPLIFT (+10% Filming Uplift Zone) ─────────────────────
rural_req = json.dumps({
    "optIn": True,
    "ruralZone": True,
    "description": (
        "Additional 10% on qualifying expenditures for productions filming in New Mexico "
        "areas at least 60 miles outside the Santa Fe and Albuquerque City Halls. "
        "Known as the Filming Uplift Zone. "
        "Cite: nmfilm.com/incentives"
    )
})
cur.execute("SELECT id FROM incentive_rules WHERE \"ruleCode\" = 'NM-RURAL-UPLIFT'")
if cur.fetchone():
    cur.execute("""
        UPDATE incentive_rules
        SET percentage = 10.0, requirements = %s, "updatedAt" = %s
        WHERE "ruleCode" = 'NM-RURAL-UPLIFT'
    """, (rural_req, NOW))
    print(f"[ok] NM-RURAL-UPLIFT updated")
else:
    cur.execute("""
        INSERT INTO incentive_rules (
            id, "jurisdictionId", "ruleName", "ruleCode", "incentiveType",
            "creditType", percentage, "eligibleExpenses", "excludedExpenses",
            "effectiveDate", requirements, active, "createdAt", "updatedAt"
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,true,%s,%s)
    """, (
        str(uuid.uuid4()), NM_ID,
        'New Mexico Filming Uplift Zone — Rural Bonus', 'NM-RURAL-UPLIFT', 'tax_credit',
        'refundable', 10.0, '{}', '{}',
        EFF, rural_req, NOW, NOW
    ))
    print(f"[ok] NM-RURAL-UPLIFT inserted (+10%, opt-in, 60+ miles from SF/ABQ)")

# ── 5. Fix NM-ALBUQUERQUE feedUrl ─────────────────────────────────────────────
cur.execute("""
    UPDATE jurisdictions
    SET "feedUrl" = 'https://www.cabq.gov/film',
        "updatedAt" = %s
    WHERE code = 'NM-ALBUQUERQUE'
""", (NOW,))
print(f"[ok] NM-ALBUQUERQUE feedUrl fixed → cabq.gov/film ({cur.rowcount} row)")

# ── 6. Insert NM-SANTAFE sub-jurisdiction ────────────────────────────────────
cur.execute("SELECT id FROM jurisdictions WHERE code = 'NM-SANTAFE'")
if cur.fetchone():
    cur.execute("""
        UPDATE jurisdictions
        SET "feedUrl" = 'https://www.santafe.org/film', "updatedAt" = %s
        WHERE code = 'NM-SANTAFE'
    """, (NOW,))
    print(f"[ok] NM-SANTAFE updated")
else:
    cur.execute("""
        INSERT INTO jurisdictions (
            id, name, code, country, type, "parentId",
            active, currency, "treatyPartners",
            description, "feedUrl", "createdAt", "updatedAt"
        ) VALUES (%s,%s,%s,%s,%s,%s,true,'USD','{}', %s,%s,%s,%s)
    """, (
        str(uuid.uuid4()), 'Santa Fe', 'NM-SANTAFE', 'US', 'city', NM_ID,
        'Santa Fe Film Office — location services, permits, and production support.',
        'https://www.santafe.org/film',
        NOW, NOW
    ))
    print(f"[ok] NM-SANTAFE inserted — feedUrl: santafe.org/film")

conn.commit()
conn.close()

print("\nDone. New Mexico incentive rule summary:")
print("  NM-FILM-BASE    25%  refundable base credit ($500K min NM spend, no cap)")
print("  NM-FILM-TV-UPLIFT 5%  opt-in — TV series 6+ ep order / qualifying pilot")
print("  NM-QPF-UPLIFT    5%  opt-in — QPF soundstage/standing set spend only")
print("  NM-RURAL-UPLIFT 10%  opt-in — 60+ miles outside Santa Fe & Albuquerque")
print("  Max stacked:    45%  (base + all uplifts; QPF+Rural unlikely to co-apply)")
print("\nSub-jurisdictions:")
print("  NM-ALBUQUERQUE  feedUrl: cabq.gov/film (corrected)")
print("  NM-SANTAFE      feedUrl: santafe.org/film (new)")
