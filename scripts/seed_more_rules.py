"""
Enhanced seed script - adds more incentive rules for new jurisdictions
"""
import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.database import prisma

# Additional incentive rules for new jurisdictions
additional_rules = [
    # USA - Michigan
    {
        "jurisdictionCode": "MI",
        "ruleName": "Michigan Film Production Incentive",
        "ruleCode": "MI-FILM-BASE",
        "incentiveType": "rebate",
        "percentage": 30.0,
        "minSpend": 50000,
        "eligibleExpenses": ["labor", "goods", "services", "michigan_spend"],
        "excludedExpenses": ["marketing", "distribution"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "michiganSpend": 50000,
            "completionWithin12Months": True
        },
        "active": True
    },
    # USA - New Jersey
    {
        "jurisdictionCode": "NJ",
        "ruleName": "NJ Film Tax Credit",
        "ruleCode": "NJ-FILM-BASE",
        "incentiveType": "tax_credit",
        "percentage": 30.0,
        "minSpend": 1000000,
        "eligibleExpenses": ["labor", "services", "goods"],
        "excludedExpenses": ["above_the_line_over_500k", "marketing"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "njSpend": 60,
            "diversity": True
        },
        "active": True
    },
    {
        "jurisdictionCode": "NJ",
        "ruleName": "NJ Film Tax Credit - Diversity Bonus",
        "ruleCode": "NJ-DIVERSITY",
        "incentiveType": "tax_credit",
        "percentage": 5.0,
        "eligibleExpenses": ["qualified_diverse_spend"],
        "excludedExpenses": [],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "diversityPlan": True,
            "stackableWithBase": True
        },
        "active": True
    },
    # USA - Virginia
    {
        "jurisdictionCode": "VA",
        "ruleName": "Virginia Film Tax Credit",
        "ruleCode": "VA-FILM-BASE",
        "incentiveType": "tax_credit",
        "percentage": 20.0,
        "minSpend": 250000,
        "maxCredit": 6500000,
        "eligibleExpenses": ["virginia_labor", "goods", "services"],
        "excludedExpenses": ["marketing"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "virginiaSpend": 250000
        },
        "active": True
    },
    {
        "jurisdictionCode": "VA",
        "ruleName": "Virginia Enhanced Credit - Rural",
        "ruleCode": "VA-RURAL",
        "incentiveType": "tax_credit",
        "percentage": 10.0,
        "eligibleExpenses": ["rural_spend"],
        "excludedExpenses": [],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "ruralLocation": True,
            "stackableWithBase": True
        },
        "active": True
    },
    # USA - Colorado
    {
        "jurisdictionCode": "CO",
        "ruleName": "Colorado Film Incentive",
        "ruleCode": "CO-FILM-BASE",
        "incentiveType": "rebate",
        "percentage": 20.0,
        "minSpend": 100000,
        "eligibleExpenses": ["colorado_labor", "colorado_goods"],
        "excludedExpenses": ["marketing", "distribution"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "coloradoSpend": 100000
        },
        "active": True
    },
    # USA - Hawaii
    {
        "jurisdictionCode": "HI",
        "ruleName": "Hawaii Film Production Tax Credit",
        "ruleCode": "HI-FILM-BASE",
        "incentiveType": "tax_credit",
        "percentage": 20.0,
        "minSpend": 200000,
        "eligibleExpenses": ["hawaii_labor", "goods", "services"],
        "excludedExpenses": ["marketing"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "hawaiiResident": 50,
            "hawaiiSpend": 200000
        },
        "active": True
    },
    {
        "jurisdictionCode": "HI",
        "ruleName": "Hawaii Additional Credit - Neighbor Islands",
        "ruleCode": "HI-NEIGHBOR",
        "incentiveType": "tax_credit",
        "percentage": 5.0,
        "eligibleExpenses": ["neighbor_island_spend"],
        "excludedExpenses": [],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "neighborIsland": True,
            "stackableWithBase": True
        },
        "active": True
    },
    # USA - Oregon
    {
        "jurisdictionCode": "OR",
        "ruleName": "Oregon Production Investment Fund",
        "ruleCode": "OR-OPIF",
        "incentiveType": "rebate",
        "percentage": 20.0,
        "minSpend": 750000,
        "maxCredit": 10000000,
        "eligibleExpenses": ["oregon_labor", "oregon_goods"],
        "excludedExpenses": ["marketing"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "oregonLabor": 50,
            "oregonSpend": 750000
        },
        "active": True
    },
    # USA - Montana
    {
        "jurisdictionCode": "MT",
        "ruleName": "Montana Media Production Tax Credit",
        "ruleCode": "MT-FILM-BASE",
        "incentiveType": "tax_credit",
        "percentage": 35.0,
        "minSpend": 50000,
        "eligibleExpenses": ["montana_labor", "montana_goods"],
        "excludedExpenses": ["marketing", "distribution"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "montanaSpend": 50000
        },
        "active": True
    },
    # USA - Mississippi
    {
        "jurisdictionCode": "MS",
        "ruleName": "Mississippi Film Incentive - Base",
        "ruleCode": "MS-FILM-BASE",
        "incentiveType": "rebate",
        "percentage": 25.0,
        "minSpend": 50000,
        "eligibleExpenses": ["mississippi_labor", "goods", "services"],
        "excludedExpenses": ["marketing"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "mississippiSpend": 50000
        },
        "active": True
    },
    {
        "jurisdictionCode": "MS",
        "ruleName": "Mississippi Payroll Bonus",
        "ruleCode": "MS-PAYROLL",
        "incentiveType": "rebate",
        "percentage": 10.0,
        "eligibleExpenses": ["mississippi_resident_labor"],
        "excludedExpenses": [],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "mississippiResident": 100,
            "stackableWithBase": True
        },
        "active": True
    },
    # International - Ireland
    {
        "jurisdictionCode": "IE",
        "ruleName": "Section 481 Film Tax Credit",
        "ruleCode": "IE-S481",
        "incentiveType": "tax_credit",
        "percentage": 32.0,
        "eligibleExpenses": ["irish_labor", "irish_goods"],
        "excludedExpenses": ["marketing", "distribution"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "irishSpend": 250000,
            "culturalTest": True
        },
        "active": True
    },
    # International - France
    {
        "jurisdictionCode": "FR",
        "ruleName": "Tax Rebate for International Production (TRIP)",
        "ruleCode": "FR-TRIP",
        "incentiveType": "rebate",
        "percentage": 30.0,
        "minSpend": 1000000,
        "maxCredit": 30000000,
        "eligibleExpenses": ["french_eligible_spend"],
        "excludedExpenses": ["development", "marketing"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "minFrenchSpend": 1000000,
            "culturalTest": True
        },
        "active": True
    },
    # International - Spain
    {
        "jurisdictionCode": "ES",
        "ruleName": "Spanish Film Production Incentive",
        "ruleCode": "ES-FILM",
        "incentiveType": "rebate",
        "percentage": 30.0,
        "minSpend": 1000000,
        "eligibleExpenses": ["spanish_eligible_spend"],
        "excludedExpenses": ["marketing", "distribution"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "spanishSpend": 1000000,
            "culturalTest": True
        },
        "active": True
    },
    # International - New Zealand
    {
        "jurisdictionCode": "NZ",
        "ruleName": "NZ Screen Production Grant",
        "ruleCode": "NZ-NZSPG",
        "incentiveType": "grant",
        "percentage": 40.0,
        "minSpend": 15000000,
        "eligibleExpenses": ["nz_labor", "nz_goods_services"],
        "excludedExpenses": ["marketing", "distribution"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "nzSpend": 15000000,
            "significantNZContent": True
        },
        "active": True
    },
    {
        "jurisdictionCode": "NZ",
        "ruleName": "NZ Post-Digital-Visual Effects Grant",
        "ruleCode": "NZ-PDV",
        "incentiveType": "grant",
        "percentage": 20.0,
        "minSpend": 500000,
        "eligibleExpenses": ["nz_vfx", "nz_post_production"],
        "excludedExpenses": [],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "nzPDVSpend": 500000
        },
        "active": True
    },
]


async def seed_more_incentive_rules():
    """Add more incentive rules to the database"""
    print("Adding more incentive rules...")
    
    try:
        await prisma.connect()
        print("✓ Connected to database")
        
        # Get jurisdictions map
        jurisdictions = await prisma.jurisdiction.find_many()
        jurisdiction_map = {j.code: j.id for j in jurisdictions}
        print(f"✓ Found {len(jurisdictions)} jurisdictions")
        
        # Check existing rules
        existing_rules = await prisma.incentiverule.find_many()
        existing_codes = {r.ruleCode for r in existing_rules}
        print(f"✓ Found {len(existing_rules)} existing rules")
        
        # Add new rules
        added = 0
        skipped = 0
        errors = 0
        
        for rule_data in additional_rules:
            jurisdiction_code = rule_data.pop("jurisdictionCode")
            
            # Check jurisdiction exists
            if jurisdiction_code not in jurisdiction_map:
                print(f"⚠️  Jurisdiction {jurisdiction_code} not found, skipping {rule_data['ruleName']}")
                errors += 1
                continue
            
            # Check if rule exists
            if rule_data["ruleCode"] in existing_codes:
                print(f"⏭️  Skipping {rule_data['ruleName']} - already exists")
                skipped += 1
                continue
            
            try:
                # Get jurisdiction ID
                jurisdiction_id = jurisdiction_map[jurisdiction_code]
                
                # Convert requirements to JSON string
                if "requirements" in rule_data:
                    rule_data["requirements"] = json.dumps(rule_data["requirements"])
                
                # Create with proper relationship
                await prisma.incentiverule.create(
                    data={
                        **rule_data,
                        "jurisdiction": {
                            "connect": {"id": jurisdiction_id}
                        }
                    }
                )
                print(f"✅ Added: {rule_data['ruleName']} ({rule_data['ruleCode']})")
                added += 1
            except Exception as e:
                print(f"❌ Error adding {rule_data['ruleName']}: {e}")
                errors += 1
        
        await prisma.disconnect()
        
        # Summary
        print("\n" + "="*60)
        print("✅ Incentive rules expansion complete!")
        print(f"Added: {added} rules")
        print(f"Skipped: {skipped} (already existed)")
        print(f"Errors: {errors}")
        print(f"Total rules in database: {len(existing_rules) + added}")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        await prisma.disconnect()


if __name__ == "__main__":
    asyncio.run(seed_more_incentive_rules())
