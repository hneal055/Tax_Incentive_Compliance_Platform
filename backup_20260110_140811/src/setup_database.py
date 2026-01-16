"""
PilotForge Database Setup Script
Creates database, runs migrations, and seeds initial data
"""
import asyncio
from datetime import datetime
from prisma import Prisma

# Jurisdiction and Rule data
JURISDICTIONS = [
    # United States
    {"name": "California", "code": "CA", "country": "United States", "type": "state"},
    {"name": "Georgia", "code": "GA", "country": "United States", "type": "state"},
    {"name": "Louisiana", "code": "LA", "country": "United States", "type": "state"},
    {"name": "New Mexico", "code": "NM", "country": "United States", "type": "state"},
    {"name": "New York", "code": "NY", "country": "United States", "type": "state"},
    {"name": "Texas", "code": "TX", "country": "United States", "type": "state"},
    {"name": "Florida", "code": "FL", "country": "United States", "type": "state"},
    {"name": "British Columbia", "code": "BC", "country": "Canada", "type": "province"},
    {"name": "Ontario", "code": "ON", "country": "Canada", "type": "province"},
    {"name": "Quebec", "code": "QC", "country": "Canada", "type": "province"},
    {"name": "United Kingdom", "code": "UK", "country": "United Kingdom", "type": "country"},
]

INCENTIVE_RULES = [
    {
        "jurisdiction_code": "BC",
        "ruleName": "BC Film Incentive - Basic Tax Credit",
        "ruleCode": "BC-FI-BASIC",
        "incentiveType": "tax_credit",
        "percentage": 35.0,
        "minSpend": 100000.0,
        "eligibleExpenses": ["labour", "production"],
        "excludedExpenses": ["financing", "marketing"],
    },
    {
        "jurisdiction_code": "BC",
        "ruleName": "BC Production Services Tax Credit",
        "ruleCode": "BC-PSTC",
        "incentiveType": "tax_credit",
        "percentage": 28.0,
        "minSpend": 100000.0,
        "eligibleExpenses": ["labour"],
        "excludedExpenses": ["above_line_talent"],
    },
    {
        "jurisdiction_code": "CA",
        "ruleName": "California Film & TV Tax Credit",
        "ruleCode": "CA-FTTC",
        "incentiveType": "tax_credit",
        "percentage": 20.0,
        "minSpend": 1000000.0,
        "maxCredit": 20000000.0,
        "eligibleExpenses": ["qualified_wages", "qualified_expenditures"],
        "excludedExpenses": ["marketing", "distribution"],
    },
    {
        "jurisdiction_code": "CA",
        "ruleName": "California Film & TV Tax Credit - Uplift",
        "ruleCode": "CA-FTTC-UPLIFT",
        "incentiveType": "tax_credit",
        "percentage": 25.0,
        "minSpend": 1000000.0,
        "maxCredit": 25000000.0,
        "eligibleExpenses": ["qualified_wages", "qualified_expenditures"],
        "excludedExpenses": ["marketing", "distribution"],
    },
    {
        "jurisdiction_code": "GA",
        "ruleName": "Georgia Film Tax Credit",
        "ruleCode": "GA-FTC",
        "incentiveType": "tax_credit",
        "percentage": 20.0,
        "minSpend": 500000.0,
        "eligibleExpenses": ["all_production"],
        "excludedExpenses": [],
    },
    {
        "jurisdiction_code": "GA",
        "ruleName": "Georgia Film Tax Credit - Logo Uplift",
        "ruleCode": "GA-FTC-LOGO",
        "incentiveType": "tax_credit",
        "percentage": 30.0,
        "minSpend": 500000.0,
        "eligibleExpenses": ["all_production"],
        "excludedExpenses": [],
    },
    {
        "jurisdiction_code": "LA",
        "ruleName": "Louisiana Motion Picture Tax Credit",
        "ruleCode": "LA-MPTC",
        "incentiveType": "tax_credit",
        "percentage": 25.0,
        "minSpend": 300000.0,
        "eligibleExpenses": ["in_state_expenditures"],
        "excludedExpenses": ["marketing"],
    },
    {
        "jurisdiction_code": "LA",
        "ruleName": "Louisiana Motion Picture Tax Credit - Uplift",
        "ruleCode": "LA-MPTC-UPLIFT",
        "incentiveType": "tax_credit",
        "percentage": 40.0,
        "minSpend": 300000.0,
        "eligibleExpenses": ["in_state_expenditures"],
        "excludedExpenses": ["marketing"],
    },
    {
        "jurisdiction_code": "NM",
        "ruleName": "New Mexico Film Tax Credit",
        "ruleCode": "NM-FTC",
        "incentiveType": "tax_credit",
        "percentage": 25.0,
        "minSpend": 1000000.0,
        "eligibleExpenses": ["direct_production_expenditures"],
        "excludedExpenses": ["financing", "marketing"],
    },
    {
        "jurisdiction_code": "NY",
        "ruleName": "New York Film Production Tax Credit",
        "ruleCode": "NY-FPTC",
        "incentiveType": "tax_credit",
        "percentage": 30.0,
        "minSpend": 250000.0,
        "eligibleExpenses": ["qualified_production_costs"],
        "excludedExpenses": ["marketing"],
    },
    {
        "jurisdiction_code": "ON",
        "ruleName": "Ontario Film & TV Tax Credit",
        "ruleCode": "ON-OFTTC",
        "incentiveType": "tax_credit",
        "percentage": 35.0,
        "minSpend": 0.0,
        "eligibleExpenses": ["labour"],
        "excludedExpenses": [],
    },
    {
        "jurisdiction_code": "QC",
        "ruleName": "Quebec Film & TV Tax Credit",
        "ruleCode": "QC-FTTC",
        "incentiveType": "tax_credit",
        "percentage": 32.0,
        "minSpend": 0.0,
        "eligibleExpenses": ["labour"],
        "excludedExpenses": [],
    },
    {
        "jurisdiction_code": "UK",
        "ruleName": "UK Film Tax Relief",
        "ruleCode": "UK-FTR",
        "incentiveType": "tax_relief",
        "percentage": 25.0,
        "minSpend": 1000000.0,
        "eligibleExpenses": ["qualifying_expenditure"],
        "excludedExpenses": [],
    },
]


async def setup():
    """Main setup function"""
    print("🎬 PilotForge Database Setup")
    print("=" * 50)
    
    prisma = Prisma()
    await prisma.connect()
    
    try:
        # Create jurisdictions
        print("\n📍 Creating jurisdictions...")
        jurisdiction_map = {}
        
        for jur_data in JURISDICTIONS:
            jur = await prisma.jurisdiction.create(
                data={
                    "name": jur_data["name"],
                    "code": jur_data["code"],
                    "country": jur_data["country"],
                    "type": jur_data["type"],
                    "active": True,
                }
            )
            jurisdiction_map[jur.code] = jur.id
            print(f"  ✓ {jur.name} ({jur.code})")
        
        print(f"✅ Created {len(JURISDICTIONS)} jurisdictions\n")
        
        # Create incentive rules
        print("📋 Creating incentive rules...")
        
        for rule_data in INCENTIVE_RULES:
            jurisdiction_id = jurisdiction_map.get(rule_data["jurisdiction_code"])
            if not jurisdiction_id:
                print(f"  ⚠️  Skipping rule for unknown jurisdiction: {rule_data['jurisdiction_code']}")
                continue
            
            await prisma.incentiverule.create(
                data={
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": rule_data["ruleName"],
                    "ruleCode": rule_data["ruleCode"],
                    "incentiveType": rule_data["incentiveType"],
                    "percentage": rule_data.get("percentage"),
                    "minSpend": rule_data.get("minSpend"),
                    "maxCredit": rule_data.get("maxCredit"),
                    "eligibleExpenses": rule_data["eligibleExpenses"],
                    "excludedExpenses": rule_data["excludedExpenses"],
                    "effectiveDate": datetime.now(),
                    "active": True,
                }
            )
            print(f"  ✓ {rule_data['ruleName']}")
        
        print(f"✅ Created {len(INCENTIVE_RULES)} incentive rules\n")
        print("=" * 50)
        print("✅ Setup complete! PilotForge is ready!")
        print("\nNext steps:")
        print("  1. Run: python -m uvicorn src.main:app --reload")
        print("  2. Open: http://localhost:8000/docs")
        print("  3. Try the API endpoints!")
        
    finally:
        await prisma.disconnect()


if __name__ == "__main__":
    asyncio.run(setup())