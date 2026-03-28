"""
Enhanced seed script - adds more jurisdictions
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.database import prisma

# Additional jurisdictions to add
additional_jurisdictions = [
    # USA States
    {
        "name": "Michigan",
        "code": "MI",
        "country": "USA",
        "type": "state",
        "description": "Michigan Film Production Incentive",
        "website": "https://www.michiganbusiness.org/industries/film/",
        "active": True
    },
    {
        "name": "New Jersey",
        "code": "NJ",
        "country": "USA",
        "type": "state",
        "description": "NJ Film Tax Credit Program",
        "website": "https://www.njeda.gov/film/",
        "active": True
    },
    {
        "name": "Virginia",
        "code": "VA",
        "country": "USA",
        "type": "state",
        "description": "Virginia Film Tax Credit",
        "website": "https://www.film.virginia.gov/incentives/",
        "active": True
    },
    {
        "name": "Colorado",
        "code": "CO",
        "country": "USA",
        "type": "state",
        "description": "Colorado Film Incentive Program",
        "website": "https://coloradofilm.org/incentives/",
        "active": True
    },
    {
        "name": "Hawaii",
        "code": "HI",
        "country": "USA",
        "type": "state",
        "description": "Hawaii Film Production Tax Credit",
        "website": "https://filmoffice.hawaii.gov/tax-incentive/",
        "active": True
    },
    {
        "name": "Oregon",
        "code": "OR",
        "country": "USA",
        "type": "state",
        "description": "Oregon Production Investment Fund",
        "website": "https://www.oregon4biz.com/Film/",
        "active": True
    },
    {
        "name": "Montana",
        "code": "MT",
        "country": "USA",
        "type": "state",
        "description": "Montana Media Production Tax Credit",
        "website": "https://montanafilm.com/incentive-program/",
        "active": True
    },
    {
        "name": "Mississippi",
        "code": "MS",
        "country": "USA",
        "type": "state",
        "description": "Mississippi Film Incentive Program",
        "website": "https://www.filmmississippi.org/incentives",
        "active": True
    },
    # International
    {
        "name": "Ireland",
        "code": "IE",
        "country": "Ireland",
        "type": "country",
        "description": "Section 481 Film Tax Credit - 32% credit",
        "website": "https://www.revenue.ie/en/companies-and-charities/reliefs-and-exemptions/film-relief/index.aspx",
        "active": True
    },
    {
        "name": "France",
        "code": "FR",
        "country": "France",
        "type": "country",
        "description": "French Tax Rebate for International Production (TRIP) - 30%",
        "website": "https://www.cnc.fr/professionnels/aides-et-financements/",
        "active": True
    },
    {
        "name": "Spain",
        "code": "ES",
        "country": "Spain",
        "type": "country",
        "description": "Spanish Film Production Incentives - 30% rebate",
        "website": "https://www.icex.es/",
        "active": True
    },
    {
        "name": "New Zealand",
        "code": "NZ",
        "country": "New Zealand",
        "type": "country",
        "description": "NZ Screen Production Grant - 40% rebate",
        "website": "https://www.nzfilm.co.nz/funding/nzspg",
        "active": True
    },
]


async def seed_additional_jurisdictions():
    """Add more jurisdictions to the database"""
    print("Adding more jurisdictions...")
    
    try:
        await prisma.connect()
        print("✓ Connected to database")
        
        # Check existing
        existing = await prisma.jurisdiction.find_many()
        existing_codes = {j.code for j in existing}
        print(f"✓ Found {len(existing)} existing jurisdictions")
        
        # Add new ones
        added = 0
        skipped = 0
        
        for jurisdiction in additional_jurisdictions:
            if jurisdiction["code"] in existing_codes:
                print(f"⏭️  Skipping {jurisdiction['name']} - already exists")
                skipped += 1
                continue
            
            try:
                await prisma.jurisdiction.create(data=jurisdiction)
                print(f"✅ Added: {jurisdiction['name']} ({jurisdiction['code']})")
                added += 1
            except Exception as e:
                print(f"❌ Error adding {jurisdiction['name']}: {e}")
        
        await prisma.disconnect()
        
        # Summary
        print("\n" + "="*60)
        print("✅ Jurisdiction expansion complete!")
        print(f"Added: {added} jurisdictions")
        print(f"Skipped: {skipped} (already existed)")
        print(f"Total in database: {len(existing) + added}")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        await prisma.disconnect()


if __name__ == "__main__":
    asyncio.run(seed_additional_jurisdictions())
