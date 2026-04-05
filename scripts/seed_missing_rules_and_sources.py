"""
Seed missing incentive rules (Australia) and monitoring sources
for all jurisdictions not currently being watched.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DATABASE_URL", os.getenv("DATABASE_URL", ""))

from src.utils.database import prisma


# ---------------------------------------------------------------------------
# Incentive rules to add
# ---------------------------------------------------------------------------

NEW_RULES = [
    # ── Australia ────────────────────────────────────────────────────────────
    {
        "jurisdictionCode": "AU",
        "ruleCode":  "AU-PRODUCER-OFFSET-FEATURE",
        "ruleName":  "Producer Offset — Feature Film (40%)",
        "ruleType":  "tax_credit",
        "percentage": 40.0,
        "minSpend":  1_000_000,
        "maxCredit": None,
        "description": (
            "Refundable tax offset of 40% of Qualifying Australian Production "
            "Expenditure (QAPE) for feature films with at least $1M QAPE. "
            "Administered by Screen Australia."
        ),
        "eligibleExpenses": ["labor", "equipment", "locations", "post_production",
                             "travel", "catering", "visual_effects"],
        "requirements": [
            "Minimum $1M QAPE",
            "Significant Australian content test OR qualifying co-production",
            "Australian production company must be the producer",
            "Certificate of Australian Content required",
            "Lodge claim with Australian Taxation Office (ATO)",
        ],
        "effectiveDate": "2024-01-01",
        "expirationDate": None,
        "active": True,
    },
    {
        "jurisdictionCode": "AU",
        "ruleCode":  "AU-PRODUCER-OFFSET-TV",
        "ruleName":  "Producer Offset — TV & Other Content (20%)",
        "ruleType":  "tax_credit",
        "percentage": 20.0,
        "minSpend":  500_000,
        "maxCredit": None,
        "description": (
            "Refundable tax offset of 20% of QAPE for television series, "
            "documentaries, and other eligible formats with at least $500K QAPE."
        ),
        "eligibleExpenses": ["labor", "equipment", "locations", "post_production",
                             "travel", "catering"],
        "requirements": [
            "Minimum $500K QAPE",
            "Significant Australian content test",
            "Australian production company must be the producer",
            "Certificate of Australian Content required",
        ],
        "effectiveDate": "2024-01-01",
        "expirationDate": None,
        "active": True,
    },
    {
        "jurisdictionCode": "AU",
        "ruleCode":  "AU-LOCATION-OFFSET",
        "ruleName":  "Location Offset — Large Budget Foreign (16.5%)",
        "ruleType":  "tax_credit",
        "percentage": 16.5,
        "minSpend":  15_000_000,
        "maxCredit": None,
        "description": (
            "Refundable tax offset of 16.5% of QAPE for large-budget foreign "
            "productions spending at least $15M in Australia. Does not require "
            "Australian content test."
        ),
        "eligibleExpenses": ["labor", "equipment", "locations", "travel",
                             "catering", "post_production"],
        "requirements": [
            "Minimum $15M QAPE spent in Australia",
            "Production must be a foreign film or TV series",
            "No Australian content test required",
            "Application to Screen Australia before principal photography",
        ],
        "effectiveDate": "2024-01-01",
        "expirationDate": None,
        "active": True,
    },
    {
        "jurisdictionCode": "AU",
        "ruleCode":  "AU-PDV-OFFSET",
        "ruleName":  "PDV Offset — Post, Digital & Visual Effects (30%)",
        "ruleType":  "tax_credit",
        "percentage": 30.0,
        "minSpend":  500_000,
        "maxCredit": None,
        "description": (
            "Refundable tax offset of 30% of Qualifying Australian PDV "
            "Expenditure (QAPDE) for post-production, digital, and visual "
            "effects work performed in Australia."
        ),
        "eligibleExpenses": ["post_production", "visual_effects"],
        "requirements": [
            "Minimum $500K qualifying Australian PDV expenditure",
            "PDV work must be performed in Australia",
            "No Australian content test required",
            "Claim lodged with ATO after financial year end",
        ],
        "effectiveDate": "2024-01-01",
        "expirationDate": None,
        "active": True,
    },
]


# ---------------------------------------------------------------------------
# Monitoring sources to add (jurisdictions not yet covered)
# ---------------------------------------------------------------------------

NEW_SOURCES = [
    # Australia
    {"name": "Screen Australia — News",
     "url": "https://www.screenaustralia.gov.au/sa/media-centre/news",
     "sourceType": "web", "jurisdictionCode": "AU"},
    {"name": "Australian Taxation Office — PDV & Location Offset",
     "url": "https://www.ato.gov.au/businesses-and-organisations/income-deductions-offsets-and-records/offsets-and-rebates/film-offsets",
     "sourceType": "web", "jurisdictionCode": "AU"},

    # Louisiana
    {"name": "Louisiana Entertainment — Film Office",
     "url": "https://louisianaentertainment.gov/film",
     "sourceType": "web", "jurisdictionCode": "LA"},

    # New York
    {"name": "Empire State Development — Film Tax Credit",
     "url": "https://esd.ny.gov/nyc-film-tv-commercial-production-tax-credit",
     "sourceType": "web", "jurisdictionCode": "NY"},

    # New Mexico
    {"name": "New Mexico Film Office",
     "url": "https://nmfilm.com",
     "sourceType": "web", "jurisdictionCode": "NM"},

    # Illinois
    {"name": "Illinois Film Office",
     "url": "https://www.illinois.gov/business/licenses-permits-and-appeals/Film.html",
     "sourceType": "web", "jurisdictionCode": "IL"},

    # Michigan
    {"name": "Michigan Film & Digital Media Office",
     "url": "https://www.michiganbusiness.org/industry/creative-sector/film-digital-media/",
     "sourceType": "web", "jurisdictionCode": "MI"},

    # Ireland
    {"name": "Screen Ireland — Section 481 Tax Relief",
     "url": "https://www.screenireland.ie/funding/section-481-tax-credit",
     "sourceType": "web", "jurisdictionCode": "IE"},

    # France
    {"name": "Centre national du cinéma (CNC) — Tax Rebate",
     "url": "https://www.cnc.fr/professionnels/aides-et-financements/international/credit-dimpot-international",
     "sourceType": "web", "jurisdictionCode": "FR"},

    # Spain
    {"name": "Spain Film Commission — Tax Incentives",
     "url": "https://www.shootinginspain.info/en/incentives",
     "sourceType": "web", "jurisdictionCode": "ES"},

    # New Zealand
    {"name": "New Zealand Film Commission — NZSPG",
     "url": "https://www.nzfilm.co.nz/incentives",
     "sourceType": "web", "jurisdictionCode": "NZ"},

    # British Columbia
    {"name": "Creative BC — Film Incentives",
     "url": "https://www.creativebc.com/programs/film-incentive-bc/",
     "sourceType": "web", "jurisdictionCode": "BC"},

    # Ontario
    {"name": "Ontario Creates — Film & TV Tax Credits",
     "url": "https://ontariocreates.ca/tax-credits/OFTTC",
     "sourceType": "web", "jurisdictionCode": "ON"},

    # Quebec
    {"name": "SODEC — Film Production Tax Credit",
     "url": "https://www.sodec.gouv.qc.ca/en/programme/credit-impot-production-cinematographique",
     "sourceType": "web", "jurisdictionCode": "QC"},

    # Colorado
    {"name": "Colorado Office of Film, TV & Media",
     "url": "https://choosecolorado.com/doing-business/incentives-financing/film-tv-media/",
     "sourceType": "web", "jurisdictionCode": "CO"},

    # Oregon
    {"name": "Oregon Film — Production Incentive",
     "url": "https://oregonfilm.org/incentives/",
     "sourceType": "web", "jurisdictionCode": "OR"},

    # Hawaii
    {"name": "Hawaii Film Office — Tax Credit",
     "url": "https://filmoffice.hawaii.gov/incentives/",
     "sourceType": "web", "jurisdictionCode": "HI"},

    # Virginia
    {"name": "Virginia Film Office — Tax Incentives",
     "url": "https://www.film.virginia.org/incentives/",
     "sourceType": "web", "jurisdictionCode": "VA"},

    # Mississippi
    {"name": "Mississippi Film Office",
     "url": "https://www.mississippifilm.org",
     "sourceType": "web", "jurisdictionCode": "MS"},

    # Montana
    {"name": "Montana Film Office",
     "url": "https://film.mt.gov/incentives",
     "sourceType": "web", "jurisdictionCode": "MT"},

    # New Jersey
    {"name": "New Jersey Motion Picture & TV Commission",
     "url": "https://www.njfilmtv.com/programs/incentives/",
     "sourceType": "web", "jurisdictionCode": "NJ"},

    # Industry-wide RSS
    {"name": "Variety — Tax Incentives & Runaway Production",
     "url": "https://variety.com/t/tax-incentives/feed/",
     "sourceType": "rss", "jurisdictionCode": None},
    {"name": "ProductionWeekly — Incentives News",
     "url": "https://productionweekly.com/feed/",
     "sourceType": "rss", "jurisdictionCode": None},
]


async def main():
    await prisma.connect()

    # ── Seed incentive rules ──────────────────────────────────────────────────
    print("\n📋 Seeding incentive rules...")
    for rule_def in NEW_RULES:
        jur_code = rule_def.pop("jurisdictionCode")
        jur = await prisma.jurisdiction.find_first(where={"code": jur_code})
        if not jur:
            print(f"  ⚠️  Jurisdiction not found: {jur_code}")
            continue

        existing = await prisma.incentiverule.find_first(
            where={"ruleCode": rule_def["ruleCode"]}
        )
        if existing:
            print(f"  ⏭️  Already exists: {rule_def['ruleCode']}")
            continue

        create_data = {
            "jurisdictionId":  jur.id,
            "ruleCode":        rule_def["ruleCode"],
            "ruleName":        rule_def["ruleName"],
            "incentiveType":   rule_def.get("ruleType", "tax_credit"),
            "percentage":      rule_def.get("percentage"),
            "fixedAmount":     rule_def.get("fixedAmount"),
            "minSpend":        rule_def.get("minSpend"),
            "maxCredit":       rule_def.get("maxCredit"),
            "eligibleExpenses": rule_def.get("eligibleExpenses", []),
            "excludedExpenses": [],
            "requirements":    "\n".join(rule_def.get("requirements", [])),
            "effectiveDate":   rule_def["effectiveDate"] + "T00:00:00Z",
            "expirationDate":  rule_def["expirationDate"] + "T00:00:00Z" if rule_def.get("expirationDate") else None,
            "active":          rule_def.get("active", True),
        }
        # Remove None values
        create_data = {k: v for k, v in create_data.items() if v is not None}

        r = await prisma.incentiverule.create(data=create_data)
        print(f"  ✅  Created: {r.ruleCode} — {r.ruleName}")

    # ── Seed monitoring sources ───────────────────────────────────────────────
    print("\n🔭 Seeding monitoring sources...")
    for src in NEW_SOURCES:
        jur_code = src.pop("jurisdictionCode", None)
        jur_id = None
        if jur_code:
            jur = await prisma.jurisdiction.find_first(where={"code": jur_code})
            jur_id = jur.id if jur else None

        existing = await prisma.monitoringsource.find_first(
            where={"url": src["url"]}
        )
        if existing:
            print(f"  ⏭️  Already exists: {src['name']}")
            continue

        create_data = {
            "name":       src["name"],
            "url":        src["url"],
            "sourceType": src["sourceType"],
            "active":     True,
        }
        if jur_code:
            create_data["jurisdiction"] = jur_code

        s = await prisma.monitoringsource.create(data=create_data)
        print(f"  ✅  Added: {s.name}")

    await prisma.disconnect()
    print("\n✅ Done.")


if __name__ == "__main__":
    asyncio.run(main())
