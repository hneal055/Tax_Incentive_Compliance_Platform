"""
Seed script for monitoring sources - adds initial RSS/webpage sources for key jurisdictions
"""
import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.database import prisma


async def seed_monitoring_sources():
    """Seed initial monitoring sources for key jurisdictions"""
    
    print("🌱 Seeding monitoring sources...")
    
    # Connect to database
    await prisma.connect()
    
    try:
        # Define monitoring sources for key jurisdictions
        sources_data = [
            # California Film Commission
            {
                'jurisdiction_code': 'CA',
                'source_type': 'rss',
                'url': 'https://film.ca.gov/news/feed/',
                'check_interval': 3600,  # 1 hour
            },
            # New York Governor's Office
            {
                'jurisdiction_code': 'NY',
                'source_type': 'webpage',
                'url': 'https://esd.ny.gov/film-production-credit',
                'check_interval': 7200,  # 2 hours
            },
            # Georgia Department of Economic Development
            {
                'jurisdiction_code': 'GA',
                'source_type': 'webpage',
                'url': 'https://www.georgia.org/industries/film-entertainment',
                'check_interval': 7200,  # 2 hours
            },
            # Louisiana Entertainment
            {
                'jurisdiction_code': 'LA',
                'source_type': 'webpage',
                'url': 'https://louisianaentertainment.gov/film-tv-industry/incentives/',
                'check_interval': 7200,  # 2 hours
            },
            # New Mexico Film Office
            {
                'jurisdiction_code': 'NM',
                'source_type': 'webpage',
                'url': 'https://nmfilm.com/incentives/',
                'check_interval': 7200,  # 2 hours
            },
            # Illinois Film Office
            {
                'jurisdiction_code': 'IL',
                'source_type': 'webpage',
                'url': 'https://www.illinois.gov/dceo/whyillinois/keyindustries/film.html',
                'check_interval': 7200,  # 2 hours
            },
        ]
        
        sources_created = 0
        
        for source_data in sources_data:
            # Find jurisdiction by code
            jurisdiction = await prisma.jurisdiction.find_first(
                where={'code': source_data['jurisdiction_code']}
            )
            
            if not jurisdiction:
                print(f"⚠️  Jurisdiction {source_data['jurisdiction_code']} not found, skipping...")
                continue
            
            # Check if source already exists
            existing = await prisma.monitoringsource.find_first(
                where={
                    'jurisdictionId': jurisdiction.id,
                    'url': source_data['url']
                }
            )
            
            if existing:
                print(f"⏭️  Source already exists for {jurisdiction.name}")
                continue
            
            # Create monitoring source
            await prisma.monitoringsource.create(
                data={
                    'jurisdictionId': jurisdiction.id,
                    'sourceType': source_data['source_type'],
                    'url': source_data['url'],
                    'checkInterval': source_data['check_interval'],
                    'active': True
                }
            )
            
            sources_created += 1
            print(f"✅ Created {source_data['source_type']} source for {jurisdiction.name}")
        
        print(f"\n✨ Seeding complete! Created {sources_created} monitoring sources")
        
    except Exception as e:
        print(f"❌ Error seeding monitoring sources: {e}")
        raise
    finally:
        await prisma.disconnect()


if __name__ == "__main__":
    asyncio.run(seed_monitoring_sources())
