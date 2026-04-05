"""
Seed the remaining US states that have active film/TV incentive programs
but are not yet in the database.

Active programs as of 2025 — 16 additional states:
AL, CT, KY, MD, MA, MN, NV, NC, OH, OK, PA, RI, SC, TN, UT, WV
"""
import asyncio, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.database import prisma


# ---------------------------------------------------------------------------
# Jurisdictions to add
# ---------------------------------------------------------------------------

NEW_JURISDICTIONS = [
    {"code": "AL", "name": "Alabama",        "country": "USA", "type": "state",
     "description": "Alabama Film Office — 25% refundable tax credit",
     "website": "https://www.alabamafilm.org"},
    {"code": "CT", "name": "Connecticut",    "country": "USA", "type": "state",
     "description": "Connecticut Film & TV — 30% transferable tax credit",
     "website": "https://portal.ct.gov/DECD/Content/Arts-Culture-Film/Film/Film-Tax-Credit"},
    {"code": "KY", "name": "Kentucky",       "country": "USA", "type": "state",
     "description": "Kentucky Film Office — 35% refundable tax credit",
     "website": "https://kyfilmoffice.com"},
    {"code": "MD", "name": "Maryland",       "country": "USA", "type": "state",
     "description": "Maryland Film Office — 27% tax credit",
     "website": "https://marylandfilm.org"},
    {"code": "MA", "name": "Massachusetts",  "country": "USA", "type": "state",
     "description": "Massachusetts Film Office — 25% transferable tax credit",
     "website": "https://www.mass.gov/film-office"},
    {"code": "MN", "name": "Minnesota",      "country": "USA", "type": "state",
     "description": "Minnesota Film & TV — 25% refundable credit",
     "website": "https://mn.gov/deed/business/financing-business/tax-credits/film/"},
    {"code": "NV", "name": "Nevada",         "country": "USA", "type": "state",
     "description": "Nevada Film Office — up to 20% transferable tax credit",
     "website": "https://nevadafilm.com"},
    {"code": "NC", "name": "North Carolina", "country": "USA", "type": "state",
     "description": "NC Film Office — 25% refundable grant (NCRRF)",
     "website": "https://www.ncfilm.com"},
    {"code": "OH", "name": "Ohio",           "country": "USA", "type": "state",
     "description": "Ohio Film Office — 30% non-refundable tax credit",
     "website": "https://development.ohio.gov/wps/portal/gov/development/community/film-office"},
    {"code": "OK", "name": "Oklahoma",       "country": "USA", "type": "state",
     "description": "Oklahoma Film & Music Office — 20% cash rebate",
     "website": "https://www.okcommerce.gov/industries/film-music/"},
    {"code": "PA", "name": "Pennsylvania",   "country": "USA", "type": "state",
     "description": "Pennsylvania Film Office — 30% transferable tax credit",
     "website": "https://www.film.pa.gov"},
    {"code": "RI", "name": "Rhode Island",   "country": "USA", "type": "state",
     "description": "Rhode Island Film & TV Office — 30% tax credit",
     "website": "https://film.ri.gov"},
    {"code": "SC", "name": "South Carolina", "country": "USA", "type": "state",
     "description": "SC Film Commission — 20% base + 5% labor bonus",
     "website": "https://filmsc.com"},
    {"code": "TN", "name": "Tennessee",      "country": "USA", "type": "state",
     "description": "Tennessee Entertainment Commission — 25% tax credit",
     "website": "https://www.tn.gov/ecd/film-entertainment.html"},
    {"code": "UT", "name": "Utah",           "country": "USA", "type": "state",
     "description": "Utah Film Commission — up to 25% tax credit",
     "website": "https://film.utah.gov"},
    {"code": "WV", "name": "West Virginia",  "country": "USA", "type": "state",
     "description": "West Virginia Film Office — 27% tax credit",
     "website": "https://wvfilm.com"},
]


# ---------------------------------------------------------------------------
# Incentive rules per state
# ---------------------------------------------------------------------------

NEW_RULES = [
    # Alabama
    {"jur": "AL", "code": "AL-FILM-BASE", "name": "Alabama Film Incentive (25%)",
     "type": "tax_credit", "pct": 25.0, "min": 500_000, "max": None,
     "eligible": ["labor","equipment","locations","post_production","travel","catering"],
     "reqs": ["Min $500K total production spend","20% must be spent with Alabama vendors",
              "Application to Alabama Film Office before principal photography",
              "Refundable credit — excess refunded in cash"],
     "effective": "2009-01-01"},

    # Connecticut
    {"jur": "CT", "code": "CT-FILM-BASE", "name": "Connecticut Film & TV Tax Credit (30%)",
     "type": "tax_credit", "pct": 30.0, "min": 100_000, "max": None,
     "eligible": ["labor","equipment","locations","post_production","travel","catering","visual_effects"],
     "reqs": ["Min $100K Connecticut expenditure","Transferable — can be sold to Connecticut taxpayers",
              "50% of budget must be spent in Connecticut for full credit",
              "Register with CT DECD before start of production"],
     "effective": "2006-01-01"},

    # Kentucky
    {"jur": "KY", "code": "KY-FILM-BASE", "name": "Kentucky Film Tax Credit (35%)",
     "type": "tax_credit", "pct": 35.0, "min": 250_000, "max": 10_000_000,
     "eligible": ["labor","equipment","locations","post_production","travel","catering"],
     "reqs": ["Min $250K Kentucky production expenditure","Max $10M credit per project",
              "Refundable credit","Kentucky Film Office approval required",
              "25% of principal cast/crew must be Kentucky residents for max rate"],
     "effective": "2021-01-01"},

    # Maryland
    {"jur": "MD", "code": "MD-FILM-BASE", "name": "Maryland Film Production Activity Tax Credit (27%)",
     "type": "tax_credit", "pct": 27.0, "min": 500_000, "max": None,
     "eligible": ["labor","equipment","locations","post_production","travel","catering"],
     "reqs": ["Min $500K direct costs for feature / $100K for TV episode",
              "Application to Maryland Film Office required",
              "Credit is transferable","Must hire minimum percentage of Maryland residents"],
     "effective": "2012-01-01"},

    # Massachusetts
    {"jur": "MA", "code": "MA-FILM-BASE", "name": "Massachusetts Film Tax Credit (25%)",
     "type": "tax_credit", "pct": 25.0, "min": 50_000, "max": None,
     "eligible": ["labor","equipment","locations","post_production","travel","catering","visual_effects"],
     "reqs": ["Min $50K Massachusetts expenditure","Transferable or saleable to MA taxpayers",
              "50% of principal photography in Massachusetts, OR 50% of budget spent in MA",
              "No per-project cap"],
     "effective": "2006-01-01"},

    # Minnesota
    {"jur": "MN", "code": "MN-FILM-BASE", "name": "Minnesota Film & TV Tax Credit (25%)",
     "type": "tax_credit", "pct": 25.0, "min": 1_000_000, "max": 5_000_000,
     "eligible": ["labor","equipment","locations","post_production","travel","catering"],
     "reqs": ["Min $1M Minnesota expenditure","Max $5M credit per project",
              "Refundable credit","At least 60% of principal photography days in Minnesota",
              "Application to DEED before production start"],
     "effective": "2013-01-01"},

    # Nevada
    {"jur": "NV", "code": "NV-FILM-BASE", "name": "Nevada Film Tax Credit (up to 20%)",
     "type": "tax_credit", "pct": 20.0, "min": 500_000, "max": 6_000_000,
     "eligible": ["labor","equipment","locations","post_production","travel","catering"],
     "reqs": ["Min $500K Nevada expenditure","Base rate 15%, +5% for Nevada-resident wages",
              "Max $6M credit per project","Transferable","Nevada Film Office approval required",
              "Begin principal photography within 12 months of approval"],
     "effective": "2013-01-01"},
    {"jur": "NV", "code": "NV-LABOR-BONUS", "name": "Nevada Resident Labor Bonus (+5%)",
     "type": "tax_credit", "pct": 5.0, "min": None, "max": None,
     "eligible": ["labor"],
     "reqs": ["Wages paid to Nevada residents","Stackable with NV-FILM-BASE"],
     "effective": "2013-01-01"},

    # North Carolina
    {"jur": "NC", "code": "NC-REEL-REBATE", "name": "NC Reel Rebate / NCRRF Grant (25%)",
     "type": "grant", "pct": 25.0, "min": 250_000, "max": 15_000_000,
     "eligible": ["labor","equipment","locations","post_production","travel","catering"],
     "reqs": ["Min $250K NC expenditure","Max rebate $15M per project",
              "Grant — not a tax credit; paid after audit","At least 15% of principal photography in NC",
              "NC Film Office application required"],
     "effective": "2015-01-01"},

    # Ohio
    {"jur": "OH", "code": "OH-FILM-BASE", "name": "Ohio Film Tax Credit (30%)",
     "type": "tax_credit", "pct": 30.0, "min": 300_000, "max": 40_000_000,
     "eligible": ["labor","equipment","locations","post_production","travel","catering"],
     "reqs": ["Min $300K Ohio expenditure","Max $40M credit per project — non-refundable, transferable",
              "Ohio Development application required","35% of cast/crew must be Ohio residents"],
     "effective": "2009-01-01"},

    # Oklahoma
    {"jur": "OK", "code": "OK-FILM-REBATE", "name": "Filmed in Oklahoma Act — Cash Rebate (20%)",
     "type": "rebate", "pct": 20.0, "min": 50_000, "max": 8_000_000,
     "eligible": ["labor","equipment","locations","post_production","travel","catering"],
     "reqs": ["Min $50K Oklahoma expenditure (feature) / $25K (TV)",
              "Cash rebate — not a tax credit","Max $8M per project",
              "Oklahoma Film + Music Office approval required",
              "+2% bonus for hiring Oklahoma crew"],
     "effective": "2010-01-01"},

    # Pennsylvania
    {"jur": "PA", "code": "PA-FILM-BASE", "name": "Pennsylvania Film Production Tax Credit (30%)",
     "type": "tax_credit", "pct": 30.0, "min": 100_000, "max": None,
     "eligible": ["labor","equipment","locations","post_production","travel","catering","visual_effects"],
     "reqs": ["Min $100K PA expenditure","60% of total production budget must be spent in PA",
              "Transferable credit — can be sold","No per-project cap",
              "Application to PA Film Office before start"],
     "effective": "2004-01-01"},

    # Rhode Island
    {"jur": "RI", "code": "RI-FILM-BASE", "name": "Rhode Island Motion Picture Production Tax Credit (30%)",
     "type": "tax_credit", "pct": 30.0, "min": 100_000, "max": 7_000_000,
     "eligible": ["labor","equipment","locations","post_production","travel","catering"],
     "reqs": ["Min $100K RI expenditure","Max $7M credit per project",
              "Transferable","RI Commerce application required",
              "No residency requirement for base credit"],
     "effective": "2005-01-01"},

    # South Carolina
    {"jur": "SC", "code": "SC-FILM-BASE", "name": "South Carolina Film & TV Tax Credit (20%)",
     "type": "tax_credit", "pct": 20.0, "min": 1_000_000, "max": None,
     "eligible": ["labor","equipment","locations","post_production","travel","catering"],
     "reqs": ["Min $1M SC expenditure","SC Film Commission approval required",
              "Refundable","Payroll must be processed through a South Carolina payroll company"],
     "effective": "2005-01-01"},
    {"jur": "SC", "code": "SC-SC-LABOR-BONUS", "name": "South Carolina Resident Labor Bonus (+5%)",
     "type": "tax_credit", "pct": 5.0, "min": None, "max": None,
     "eligible": ["labor"],
     "reqs": ["Additional 5% on wages paid to SC residents","Stackable with SC-FILM-BASE"],
     "effective": "2005-01-01"},

    # Tennessee
    {"jur": "TN", "code": "TN-FILM-BASE", "name": "Tennessee Entertainment Industry Tax Credit (25%)",
     "type": "tax_credit", "pct": 25.0, "min": 200_000, "max": None,
     "eligible": ["labor","equipment","locations","post_production","travel","catering"],
     "reqs": ["Min $200K Tennessee expenditure","Refundable","Tennessee ECD approval required",
              "At least 15% of principal photography days in Tennessee"],
     "effective": "2018-01-01"},

    # Utah
    {"jur": "UT", "code": "UT-MIIIP", "name": "Utah Motion Picture Incentive Program (up to 25%)",
     "type": "tax_credit", "pct": 25.0, "min": 1_000_000, "max": 8_000_000,
     "eligible": ["labor","equipment","locations","post_production","travel","catering"],
     "reqs": ["Min $1M Utah production expenditure","Max $8M credit per project",
              "Base 20% + 5% bonus for rural locations or Utah resident wages",
              "Utah Film Commission application required","Transferable"],
     "effective": "2015-01-01"},

    # West Virginia
    {"jur": "WV", "code": "WV-FILM-BASE", "name": "West Virginia Film Industry Investment Act (27%)",
     "type": "tax_credit", "pct": 27.0, "min": 25_000, "max": None,
     "eligible": ["labor","equipment","locations","post_production","travel","catering"],
     "reqs": ["Min $25K West Virginia expenditure","Refundable",
              "West Virginia Film Office registration required",
              "10% bonus for productions spending $1M+ with WV vendors"],
     "effective": "2009-01-01"},
]


# ---------------------------------------------------------------------------
# Monitoring sources
# ---------------------------------------------------------------------------

NEW_SOURCES = [
    {"name": "Alabama Film Office", "url": "https://www.alabamafilm.org", "type": "web", "jur": "AL"},
    {"name": "Connecticut Film & TV Office", "url": "https://portal.ct.gov/DECD/Content/Arts-Culture-Film/Film/Film-Tax-Credit", "type": "web", "jur": "CT"},
    {"name": "Kentucky Film Office", "url": "https://kyfilmoffice.com", "type": "web", "jur": "KY"},
    {"name": "Maryland Film Office", "url": "https://marylandfilm.org", "type": "web", "jur": "MD"},
    {"name": "Massachusetts Film Office", "url": "https://www.mass.gov/film-office", "type": "web", "jur": "MA"},
    {"name": "Minnesota Film & TV Board", "url": "https://mn.gov/deed/business/financing-business/tax-credits/film/", "type": "web", "jur": "MN"},
    {"name": "Nevada Film Office", "url": "https://nevadafilm.com", "type": "web", "jur": "NV"},
    {"name": "North Carolina Film Office", "url": "https://www.ncfilm.com", "type": "web", "jur": "NC"},
    {"name": "Ohio Film Office", "url": "https://development.ohio.gov/wps/portal/gov/development/community/film-office", "type": "web", "jur": "OH"},
    {"name": "Oklahoma Film & Music Office", "url": "https://www.okcommerce.gov/industries/film-music/", "type": "web", "jur": "OK"},
    {"name": "Pennsylvania Film Office", "url": "https://www.film.pa.gov", "type": "web", "jur": "PA"},
    {"name": "Rhode Island Film & TV Office", "url": "https://film.ri.gov", "type": "web", "jur": "RI"},
    {"name": "South Carolina Film Commission", "url": "https://filmsc.com", "type": "web", "jur": "SC"},
    {"name": "Tennessee Entertainment Commission", "url": "https://www.tn.gov/ecd/film-entertainment.html", "type": "web", "jur": "TN"},
    {"name": "Utah Film Commission", "url": "https://film.utah.gov", "type": "web", "jur": "UT"},
    {"name": "West Virginia Film Office", "url": "https://wvfilm.com", "type": "web", "jur": "WV"},
]


async def main():
    await prisma.connect()

    # ── Add jurisdictions ─────────────────────────────────────────────────────
    print("Adding jurisdictions...")
    jur_map = {}
    for j in NEW_JURISDICTIONS:
        existing = await prisma.jurisdiction.find_first(where={"code": j["code"]})
        if existing:
            print(f"  skip {j['code']} (exists)")
            jur_map[j["code"]] = existing.id
            continue
        rec = await prisma.jurisdiction.create(data={
            "code":        j["code"],
            "name":        j["name"],
            "country":     j["country"],
            "type":        j["type"],
            "description": j.get("description"),
            "website":     j.get("website"),
            "active":      True,
        })
        jur_map[j["code"]] = rec.id
        print(f"  + {rec.code}  {rec.name}")

    # ── Add incentive rules ───────────────────────────────────────────────────
    print("\nAdding incentive rules...")
    for r in NEW_RULES:
        existing = await prisma.incentiverule.find_first(where={"ruleCode": r["code"]})
        if existing:
            print(f"  skip {r['code']} (exists)")
            continue

        jur_id = jur_map.get(r["jur"])
        if not jur_id:
            print(f"  WARN: no jurisdiction for {r['jur']}")
            continue

        data = {
            "jurisdictionId":  jur_id,
            "ruleCode":        r["code"],
            "ruleName":        r["name"],
            "incentiveType":   r["type"],
            "percentage":      r.get("pct"),
            "minSpend":        r.get("min"),
            "maxCredit":       r.get("max"),
            "eligibleExpenses": r.get("eligible", []),
            "excludedExpenses": [],
            "requirements":    "\n".join(r.get("reqs", [])),
            "effectiveDate":   r["effective"] + "T00:00:00Z",
            "active":          True,
        }
        data = {k: v for k, v in data.items() if v is not None}
        rec = await prisma.incentiverule.create(data=data)
        print(f"  + {rec.ruleCode}  {rec.percentage}%  {r['jur']}")

    # ── Add monitoring sources ────────────────────────────────────────────────
    print("\nAdding monitoring sources...")
    for s in NEW_SOURCES:
        existing = await prisma.monitoringsource.find_first(where={"url": s["url"]})
        if existing:
            print(f"  skip {s['name']} (exists)")
            continue
        rec = await prisma.monitoringsource.create(data={
            "name":         s["name"],
            "url":          s["url"],
            "sourceType":   s["type"],
            "jurisdiction": s["jur"],
            "active":       True,
        })
        print(f"  + {rec.name}")

    await prisma.disconnect()
    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())
