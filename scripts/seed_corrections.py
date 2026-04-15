"""
seed_corrections.py — Fix misassigned rules + add feed URLs to all US states
=============================================================================
Errors found:
  CO-FILM-REBATE-DOMESTIC / CO-FILM-REBATE-FOREIGN → Colombia (ProColombia), not Colorado
  MT-FILM-REBATE → Malta Film Commission, not Montana
  CO-FILM-BASE → description says "Colombia" not "Colorado" — update ruleName/description
Actions:
  1. Delete CO Colombia rules
  2. Delete MT Malta rule
  3. Fix CO-FILM-BASE ruleName
  4. Add verified feed URLs to all US states missing them
"""
import os, sys
from datetime import datetime, timezone
import psycopg2

DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    sys.exit("DATABASE_URL not set")

conn = psycopg2.connect(DB_URL)
conn.autocommit = False
cur = conn.cursor()
NOW = datetime.now(timezone.utc)

# ── 1. Delete misassigned rules ───────────────────────────────────────────────
bad_rules = [
    'CO-FILM-REBATE-DOMESTIC',
    'CO-FILM-REBATE-FOREIGN',
    'MT-FILM-REBATE',
]
for code in bad_rules:
    cur.execute('DELETE FROM incentive_rules WHERE "ruleCode" = %s', (code,))
    print(f"[ok] Deleted {code} ({cur.rowcount} row)")

# ── 2. Fix CO-FILM-BASE ruleName (was labeled Colombia) ───────────────────────
cur.execute("""
    UPDATE incentive_rules
    SET "ruleName" = 'Colorado Film Incentive Program',
        "updatedAt" = %s
    WHERE "ruleCode" = 'CO-FILM-BASE'
""", (NOW,))
print(f"[ok] CO-FILM-BASE ruleName fixed ({cur.rowcount} row)")

# ── 3. Add feed URLs to US states missing them ────────────────────────────────
FEED_URLS = {
    'CA':  'https://film.ca.gov',
    'CO':  'https://coloradofilm.org',
    'GA':  'https://georgia.org/film',
    'HI':  'https://filmoffice.hawaii.gov',
    'IL':  'https://film.illinois.gov',
    'MI':  'https://www.michiganfilmoffice.org',
    'MS':  'https://www.filmmississippi.org',
    'MT':  'https://montanafilm.com',
    'NJ':  'https://www.njfilmoffice.com',
    'NY':  'https://www.nyc.gov/film',
    'OR':  'https://oregonfilm.org',
    'PA':  'https://www.filmpa.com',
    'VA':  'https://film.virginia.org',
    # Canada
    'BC':  'https://www.creativebc.com',
    'ON':  'https://ontariocreates.ca',
    'QC':  'https://sodec.gouv.qc.ca',
    # International
    'UK':  'https://www.bfi.org.uk/certification',
    'IE':  'https://screenireland.ie',
    'NZ':  'https://www.screennz.govt.nz',
    'FR':  'https://www.cnc.fr',
    'ES':  'https://www.icaa.gob.es',
}

for code, url in FEED_URLS.items():
    cur.execute("""
        UPDATE jurisdictions SET "feedUrl" = %s, "updatedAt" = %s
        WHERE code = %s AND ("feedUrl" IS NULL OR "feedUrl" != %s)
    """, (url, NOW, code, url))
    if cur.rowcount:
        print(f"[ok] {code} feedUrl → {url}")
    else:
        print(f"[--] {code} feedUrl already set, skipped")

conn.commit()
conn.close()
print("\nDone.")
