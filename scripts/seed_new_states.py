"""
seed_new_states.py — Seed TX, NM, LA, PA jurisdictions + incentive rules
=========================================================================
Idempotent: safe to re-run. Uses ON CONFLICT DO NOTHING for jurisdictions
and upsert logic for incentive rules.

State programs as of 2025:
  NM  New Mexico Film Production Tax Credit — 25% base + 5% TV/NM-resident uplift
  LA  Louisiana Film Production Tax Credit — 25% base + 10% on LA resident payroll
  PA  Pennsylvania Film Production Tax Credit — 25%, capped $100M/yr, transferable
  TX  Texas Moving Image Industry Incentive Program — 5–22.5% grant (active 2024 session)

Sub-jurisdictions:
  NM-ALBUQUERQUE  (Bernalillo County — film office waivers)
  LA-NEW-ORLEANS  (NOLA Film Office — local fee waivers + permit support)
  PA-PHILADELPHIA (10% local bonus on qualified Philly spend)
  TX-AUSTIN       (Austin Film Commission incentive fund)
  TX-HOUSTON      (Houston Film Commission — local incentives)
"""

import json, os, sys, uuid
from datetime import datetime, timezone

import psycopg2

DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    sys.exit("DATABASE_URL not set — run inside the pilotforge-api container")

conn = psycopg2.connect(DB_URL)
conn.autocommit = False
cur = conn.cursor()
NOW = datetime.now(timezone.utc)


# ── helpers ───────────────────────────────────────────────────────────────────

def upsert_jurisdiction(code, name, country, jtype, description, website, currency="USD", feed_url=None):
    cur.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    row = cur.fetchone()
    if row:
        jid = row[0]
        cur.execute(
            """UPDATE jurisdictions SET name=%s, description=%s, website=%s, "feedUrl"=%s, "updatedAt"=%s
               WHERE id=%s""",
            (name, description, website, feed_url, NOW, jid),
        )
        print(f"[upd] {code} jurisdiction")
    else:
        jid = str(uuid.uuid4())
        cur.execute(
            """INSERT INTO jurisdictions
               (id, name, code, country, type, description, website, currency,
                "treatyPartners", active, "feedUrl", "createdAt", "updatedAt")
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'{}',true,%s,%s,%s)""",
            (jid, name, code, country, jtype, description, website, currency, feed_url, NOW, NOW),
        )
        print(f"[ins] {code} jurisdiction")
    return jid


def upsert_sub_jurisdiction(code, name, parent_id, jtype="city", description="", website=None, feed_url=None):
    cur.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    row = cur.fetchone()
    if row:
        sid = row[0]
        cur.execute(
            """UPDATE jurisdictions SET name=%s, description=%s, website=%s, "feedUrl"=%s,
               "parentId"=%s, "updatedAt"=%s WHERE id=%s""",
            (name, description, website, feed_url, parent_id, NOW, sid),
        )
        print(f"  [upd] {code} sub-jurisdiction")
    else:
        sid = str(uuid.uuid4())
        cur.execute(
            """INSERT INTO jurisdictions
               (id, name, code, country, type, description, website, currency,
                "treatyPartners", active, "parentId", "feedUrl", "createdAt", "updatedAt")
               VALUES (%s,%s,%s,'US',%s,%s,%s,'USD','{}',true,%s,%s,%s,%s)""",
            (sid, name, code, jtype, description, website, parent_id, feed_url, NOW, NOW),
        )
        print(f"  [ins] {code} sub-jurisdiction")
    return sid


def upsert_rule(jid, rule_code, rule_name, incentive_type, credit_type,
                percentage=None, fixed_amount=None, min_spend=None, max_credit=None,
                requirements=None, effective_date=None, expiration_date=None):
    req_json = json.dumps(requirements or {})
    eff = effective_date or datetime(2024, 1, 1, tzinfo=timezone.utc)
    cur.execute("SELECT id FROM incentive_rules WHERE \"ruleCode\" = %s", (rule_code,))
    if cur.fetchone():
        cur.execute(
            """UPDATE incentive_rules
               SET percentage=%s, "fixedAmount"=%s, "minSpend"=%s, "maxCredit"=%s,
                   requirements=%s, "expirationDate"=%s, "updatedAt"=%s
               WHERE "ruleCode"=%s""",
            (percentage, fixed_amount, min_spend, max_credit, req_json, expiration_date, NOW, rule_code),
        )
        print(f"  [upd] rule {rule_code}")
    else:
        cur.execute(
            """INSERT INTO incentive_rules
               (id, "jurisdictionId", "ruleName", "ruleCode", "incentiveType", "creditType",
                percentage, "fixedAmount", "minSpend", "maxCredit",
                "eligibleExpenses", "excludedExpenses",
                "effectiveDate", "expirationDate", requirements, active, "createdAt", "updatedAt")
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'{}','{}', %s,%s,%s,true,%s,%s)""",
            (str(uuid.uuid4()), jid, rule_name, rule_code, incentive_type, credit_type,
             percentage, fixed_amount, min_spend, max_credit,
             eff, expiration_date, req_json, NOW, NOW),
        )
        print(f"  [ins] rule {rule_code}")


# ── New Mexico ────────────────────────────────────────────────────────────────

NM_ID = upsert_jurisdiction(
    code="NM", name="New Mexico", country="US", jtype="state",
    description="New Mexico Film Production Tax Credit — 25% refundable on qualifying NM spend. "
                "One of the most competitive programs in the US with no annual cap.",
    website="https://nmfilm.com",
    feed_url="https://nmfilm.com/feed/",
)

upsert_rule(
    NM_ID, "NM-FILM-BASE", "New Mexico Film Production Tax Credit — Base",
    incentive_type="tax_credit", credit_type="refundable",
    percentage=25.0,
    min_spend=500_000.0,
    requirements={
        "minNMSpend": 500000,
        "noCap": True,
        "description": "25% refundable tax credit on qualifying New Mexico spend. "
                       "Minimum $500K NM spend. No annual program cap.",
    },
)

upsert_rule(
    NM_ID, "NM-FILM-TV-UPLIFT",
    "New Mexico Film Tax Credit — TV Series / NM Resident Uplift",
    incentive_type="tax_credit", credit_type="refundable",
    percentage=5.0,
    requirements={
        "optIn": False,
        "conditions": ["tv_series OR 60%+ NM resident crew"],
        "description": "Additional 5% on qualifying spend for TV series or productions "
                       "where at least 60% of below-the-line crew are NM residents.",
    },
)

NM_ABQ_ID = upsert_sub_jurisdiction(
    code="NM-ALBUQUERQUE", name="Albuquerque / Bernalillo County", parent_id=NM_ID,
    jtype="city",
    description="Albuquerque Film Office — location fee waivers, permit assistance, "
                "crew database. No direct cash incentive beyond state credit.",
    website="https://www.cabq.gov/film",
    feed_url="https://www.cabq.gov/film/rss",
)

# ── Louisiana ─────────────────────────────────────────────────────────────────

LA_ID = upsert_jurisdiction(
    code="LA", name="Louisiana", country="US", jtype="state",
    description="Louisiana Film Production Tax Credit — 25% base on qualifying LA spend, "
                "plus 10% additional on Louisiana resident payroll (35% effective on qualifying labor). "
                "Transferable, no per-project cap.",
    website="https://louisianaentertainment.gov",
    feed_url="https://louisianaentertainment.gov/feed",
)

upsert_rule(
    LA_ID, "LA-FILM-BASE", "Louisiana Film Production Tax Credit — Base",
    incentive_type="tax_credit", credit_type="transferable",
    percentage=25.0,
    min_spend=300_000.0,
    requirements={
        "minLASpend": 300000,
        "transferable": True,
        "description": "25% transferable tax credit on qualifying Louisiana production spend. "
                       "Minimum $300K in-state spend. No per-project cap.",
    },
)

upsert_rule(
    LA_ID, "LA-FILM-PAYROLL-BONUS",
    "Louisiana Film Tax Credit — Resident Payroll Bonus",
    incentive_type="tax_credit", credit_type="transferable",
    percentage=10.0,
    requirements={
        "appliesTo": "LA_resident_payroll_only",
        "description": "Additional 10% on wages paid to Louisiana residents. "
                       "Stacks on the 25% base for an effective 35% on qualifying resident labor.",
    },
)

LA_NO_ID = upsert_sub_jurisdiction(
    code="LA-NEW-ORLEANS", name="New Orleans / Orleans Parish", parent_id=LA_ID,
    jtype="city",
    description="NOLA Film Office — local film permit processing, location coordination, "
                "and expedited fee waivers for productions spending $1M+ locally.",
    website="https://www.nolafilm.com",
    feed_url="https://www.nolafilm.com/feed",
)

# ── Pennsylvania ──────────────────────────────────────────────────────────────

PA_ID = upsert_jurisdiction(
    code="PA", name="Pennsylvania", country="US", jtype="state",
    description="Pennsylvania Film Production Tax Credit — 25% non-refundable, transferable. "
                "Annual program cap of $100M; early application recommended. "
                "Philadelphia productions may qualify for an additional local bonus.",
    website="https://dced.pa.gov/programs/film-tax-credit",
    feed_url=None,  # No public RSS
)

upsert_rule(
    PA_ID, "PA-FILM-BASE", "Pennsylvania Film Production Tax Credit",
    incentive_type="tax_credit", credit_type="transferable",
    percentage=25.0,
    min_spend=1_000_000.0,
    max_credit=None,  # per-project no cap; program has $100M annual aggregate
    requirements={
        "minPASpend": 1000000,
        "annualProgramCap": 100_000_000,
        "transferable": True,
        "applyEarly": True,
        "description": "25% transferable tax credit on qualifying Pennsylvania spend. "
                       "Minimum $1M in-state spend. Program has $100M annual aggregate cap — "
                       "apply early in the calendar year.",
    },
)

PA_PHL_ID = upsert_sub_jurisdiction(
    code="PA-PHILADELPHIA", name="Philadelphia", parent_id=PA_ID,
    jtype="city",
    description="Philadelphia Film Office — local 10% bonus credit on qualifying Philadelphia "
                "spend for productions spending $5M+ in the city.",
    website="https://www.filmphiladelphia.org",
    feed_url="https://www.filmphiladelphia.org/feed",
)

upsert_rule(
    PA_PHL_ID, "PA-PHILLY-BONUS", "Philadelphia Film Production Bonus Credit",
    incentive_type="tax_credit", credit_type="transferable",
    percentage=10.0,
    min_spend=5_000_000.0,
    requirements={
        "minPhillySpend": 5000000,
        "description": "Additional 10% credit on qualifying Philadelphia spend for "
                       "productions spending $5M+ within city limits. Stacks on PA state credit.",
    },
)

# ── Texas ─────────────────────────────────────────────────────────────────────

TX_ID = upsert_jurisdiction(
    code="TX", name="Texas", country="US", jtype="state",
    description="Texas Moving Image Industry Incentive Program (MIIP) — 5–22.5% grant "
                "on qualifying Texas spend. Grant size depends on in-state spend level and "
                "percentage of Texas resident crew. Program funded through 2025 legislative session.",
    website="https://gov.texas.gov/film",
    feed_url="https://gov.texas.gov/film/rss",
)

upsert_rule(
    TX_ID, "TX-FILM-GRANT-BASE", "Texas MIIP Grant — Base (5%)",
    incentive_type="rebate", credit_type="non_refundable",
    percentage=5.0,
    min_spend=250_000.0,
    requirements={
        "minTXSpend": 250000,
        "programType": "grant",
        "description": "Base 5% grant on qualifying Texas spend. Minimum $250K. "
                       "Grant percentage increases with Texas resident crew percentage and total spend.",
    },
)

upsert_rule(
    TX_ID, "TX-FILM-GRANT-ENHANCED", "Texas MIIP Grant — Enhanced (up to 22.5%)",
    incentive_type="rebate", credit_type="non_refundable",
    percentage=22.5,
    min_spend=1_000_000.0,
    requirements={
        "minTXSpend": 1000000,
        "minTXResidentCrew": 0.70,
        "programType": "grant",
        "description": "Up to 22.5% grant for productions with $1M+ Texas spend AND "
                       "70%+ of below-the-line crew are Texas residents. "
                       "Effective rate is negotiated with Texas Film Commission.",
    },
)

TX_AUS_ID = upsert_sub_jurisdiction(
    code="TX-AUSTIN", name="Austin", parent_id=TX_ID,
    jtype="city",
    description="Austin Film Commission — local incentive fund, location scouting, "
                "permit assistance. City-level cash incentive available for productions "
                "spending $500K+ in Austin.",
    website="https://austintexas.gov/film",
    feed_url=None,
)

TX_HOU_ID = upsert_sub_jurisdiction(
    code="TX-HOUSTON", name="Houston", parent_id=TX_ID,
    jtype="city",
    description="Houston Film Commission — local production incentives, permit coordination. "
                "Incentive negotiations handled directly with the film office.",
    website="https://www.houstontx.gov/filmcommission",
    feed_url=None,
)

# ── Commit ────────────────────────────────────────────────────────────────────

conn.commit()
cur.close()
conn.close()
print("\n✅ TX, NM, LA, PA seeded successfully.")
