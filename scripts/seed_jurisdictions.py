"""
Seed script for core jurisdictions (CA, GA, NY, LA, NM, BC, ON, QC, UK, AU)
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.database import prisma

core_jurisdictions = [
    {
        "name": "California",
        "code": "CA",
        "country": "USA",
        "type": "state",
        "description": "California Film & TV Tax Credit Program",
        "website": "https://film.ca.gov/tax-credit/",
        "active": True,
    },
    {
        "name": "Georgia",
        "code": "GA",
        "country": "USA",
        "type": "state",
        "description": "Georgia Film Tax Credit Program",
        "website": "https://www.georgia.org/film",
        "active": True,
    },
    {
        "name": "New York",
        "code": "NY",
        "country": "USA",
        "type": "state",
        "description": "New York Film Production Tax Credit",
        "website": "https://esd.ny.gov/nyc-film-tv-commercials-production-credit",
        "active": True,
    },
    {
        "name": "Louisiana",
        "code": "LA",
        "country": "USA",
        "type": "state",
        "description": "Louisiana Motion Picture Production Tax Credit",
        "website": "https://www.louisianaentertainment.gov/film/",
        "active": True,
    },
    {
        "name": "New Mexico",
        "code": "NM",
        "country": "USA",
        "type": "state",
        "description": "New Mexico Film Production Tax Credit",
        "website": "https://www.nmfilm.com/incentives/",
        "active": True,
    },
    {
        "name": "British Columbia",
        "code": "BC",
        "country": "Canada",
        "type": "province",
        "description": "BC Film Incentive & Production Services Tax Credit",
        "website": "https://creativebc.com/programs-funding/production-incentives/",
        "active": True,
    },
    {
        "name": "Ontario",
        "code": "ON",
        "country": "Canada",
        "type": "province",
        "description": "Ontario Film & Television Tax Credit",
        "website": "https://ontariocreates.ca/tax-incentives/",
        "active": True,
    },
    {
        "name": "Quebec",
        "code": "QC",
        "country": "Canada",
        "type": "province",
        "description": "Quebec Film Production Tax Credit",
        "website": "https://www.sodec.gouv.qc.ca/en/programs/",
        "active": True,
    },
    {
        "name": "United Kingdom",
        "code": "UK",
        "country": "United Kingdom",
        "type": "country",
        "description": "UK Film Tax Relief & High-End TV Tax Relief",
        "website": "https://www.bfi.org.uk/certification-funding/british-certification-tax-relief",
        "active": True,
    },
    {
        "name": "Australia",
        "code": "AU",
        "country": "Australia",
        "type": "country",
        "description": "Australian Screen Production Incentive",
        "website": "https://www.screenaustralia.gov.au/funding-and-support/producer-offset",
        "active": True,
    },
]


async def seed_jurisdictions():
    print("Starting jurisdiction seeding...")
    await prisma.connect()
    print("Connected to database")

    existing = await prisma.jurisdiction.find_many()
    existing_codes = {j.code for j in existing}
    print(f"Found {len(existing)} existing jurisdictions")

    added = 0
    skipped = 0

    for jur in core_jurisdictions:
        if jur["code"] in existing_codes:
            print(f"  Skipping {jur['name']} - already exists")
            skipped += 1
            continue
        await prisma.jurisdiction.create(data=jur)
        print(f"  Added: {jur['name']} ({jur['code']})")
        added += 1

    await prisma.disconnect()

    print("\n" + "=" * 60)
    print("Jurisdiction seeding complete!")
    print(f"Added: {added} | Skipped: {skipped} | Total: {len(existing) + added}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(seed_jurisdictions())
