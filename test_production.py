import asyncio
import sys
from datetime import date

sys.path.insert(0, ".")

from src.utils.database import prisma
from src.models.production import ProductionCreate

async def test_create():
    try:
        print("Connecting to database...")
        await prisma.connect()
        print("✓ Connected")
        
        # Get a jurisdiction
        print("\nFetching jurisdictions...")
        jurisdictions = await prisma.jurisdiction.find_many()
        print(f"✓ Found {len(jurisdictions)} jurisdictions")
        
        if not jurisdictions:
            print("ERROR: No jurisdictions found!")
            return
        
        jurisdiction_id = jurisdictions[0].id
        print(f"✓ Using jurisdiction: {jurisdictions[0].name} ({jurisdiction_id})")
        
        # Create production object
        print("\nCreating ProductionCreate object...")
        production = ProductionCreate(
            title="Test Film",
            productionType="feature",
            jurisdictionId=jurisdiction_id,
            budgetTotal=5000000.0,
            startDate=date(2026, 6, 1),
            productionCompany="Acme Productions",
            status="planning"
        )
        print(f"✓ Production object created: {production.title}")
        
        # Convert to dict
        print("\nConverting to dict...")
        data = production.model_dump()
        print(f"✓ Data: {data}")
        
        # Create in database
        print("\nCreating in database...")
        result = await prisma.production.create(data=data)
        print(f"✓ SUCCESS! Created production: {result.id}")
        print(f"  Title: {result.title}")
        print(f"  Type: {result.productionType}")
        print(f"  Budget: ${result.budgetTotal:,.0f}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await prisma.disconnect()
        print("\n✓ Disconnected")

if __name__ == "__main__":
    asyncio.run(test_create())
