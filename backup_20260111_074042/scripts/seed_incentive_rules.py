"""
Seed script to populate incentive rules with real tax credit data
"""
import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.database import prisma

# Real tax incentive data from major jurisdictions
incentive_rules_data = [
    # USA - California
    {
        "jurisdictionCode": "CA",
        "ruleName": "California Film & TV Tax Credit 2.0",
        "ruleCode": "CA-FILM-2.0",
        "incentiveType": "tax_credit",
        "percentage": 20.0,
        "minSpend": 1000000,
        "maxCredit": 10000000,
        "eligibleExpenses": ["labor", "equipment", "locations", "post_production"],
        "excludedExpenses": ["above_the_line", "marketing", "financing_costs"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "minShootDays": 10,
            "californiaResidents": 75,
            "relocatingProject": False
        },
        "active": True
    },
    {
        "jurisdictionCode": "CA",
        "ruleName": "California Relocating TV Series Credit",
        "ruleCode": "CA-TV-RELOCATE",
        "incentiveType": "tax_credit",
        "percentage": 25.0,
        "minSpend": 1000000,
        "maxCredit": 12000000,
        "eligibleExpenses": ["labor", "equipment", "locations", "post_production"],
        "excludedExpenses": ["above_the_line", "marketing"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "relocatingProject": True,
            "tvSeries": True,
            "californiaResidents": 75
        },
        "active": True
    },
    # USA - Georgia
    {
        "jurisdictionCode": "GA",
        "ruleName": "Georgia Film Tax Credit",
        "ruleCode": "GA-FILM-BASE",
        "incentiveType": "tax_credit",
        "percentage": 20.0,
        "minSpend": 500000,
        "eligibleExpenses": ["labor", "equipment", "locations", "post_production", "talent"],
        "excludedExpenses": ["marketing", "distribution"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "georgiaSpend": 500000,
            "promotionalRequirements": True
        },
        "active": True
    },
    {
        "jurisdictionCode": "GA",
        "ruleName": "Georgia Film Tax Credit + Promotional Bonus",
        "ruleCode": "GA-FILM-PROMO",
        "incentiveType": "tax_credit",
        "percentage": 30.0,
        "minSpend": 500000,
        "eligibleExpenses": ["labor", "equipment", "locations", "post_production", "talent"],
        "excludedExpenses": ["marketing", "distribution"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "georgiaSpend": 500000,
            "georgiaPromo": True,
            "logoInCredits": True
        },
        "active": True
    },
    # USA - New York
    {
        "jurisdictionCode": "NY",
        "ruleName": "NY Film Production Tax Credit",
        "ruleCode": "NY-FILM-BASE",
        "incentiveType": "tax_credit",
        "percentage": 30.0,
        "minSpend": 250000,
        "maxCredit": 7000000,
        "eligibleExpenses": ["labor", "equipment", "locations", "post_production"],
        "excludedExpenses": ["above_the_line_over_cap", "marketing"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "nySpend": 75,
            "shootingDays": 75
        },
        "active": True
    },
    {
        "jurisdictionCode": "NY",
        "ruleName": "NY Post-Production Credit",
        "ruleCode": "NY-POST-PROD",
        "incentiveType": "tax_credit",
        "percentage": 30.0,
        "minSpend": 250000,
        "maxCredit": 7000000,
        "eligibleExpenses": ["post_production", "vfx", "editing", "sound"],
        "excludedExpenses": ["marketing"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "nyFacilities": True
        },
        "active": True
    },
    # USA - Louisiana
    {
        "jurisdictionCode": "LA",
        "ruleName": "Louisiana Film Tax Credit",
        "ruleCode": "LA-FILM-BASE",
        "incentiveType": "tax_credit",
        "percentage": 25.0,
        "minSpend": 300000,
        "eligibleExpenses": ["labor", "equipment", "locations", "post_production"],
        "excludedExpenses": ["marketing", "above_the_line_over_1m"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "louisianaResident": 60,
            "louisianaSpend": 300000
        },
        "active": True
    },
    {
        "jurisdictionCode": "LA",
        "ruleName": "Louisiana Additional Payroll Credit",
        "ruleCode": "LA-PAYROLL-BONUS",
        "incentiveType": "tax_credit",
        "percentage": 10.0,
        "eligibleExpenses": ["louisiana_resident_labor"],
        "excludedExpenses": [],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "louisianaResident": 100,
            "stackableWithBase": True
        },
        "active": True
    },
    # USA - New Mexico
    {
        "jurisdictionCode": "NM",
        "ruleName": "New Mexico Film Production Tax Credit",
        "ruleCode": "NM-FILM-BASE",
        "incentiveType": "tax_credit",
        "percentage": 25.0,
        "minSpend": 50000,
        "eligibleExpenses": ["labor", "equipment", "locations", "post_production"],
        "excludedExpenses": ["marketing", "indirect_costs"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "newMexicoSpend": 60
        },
        "active": True
    },
    {
        "jurisdictionCode": "NM",
        "ruleName": "New Mexico Veteran Crew Bonus",
        "ruleCode": "NM-VETERAN-BONUS",
        "incentiveType": "tax_credit",
        "percentage": 5.0,
        "eligibleExpenses": ["veteran_labor"],
        "excludedExpenses": [],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "veteranCrew": True,
            "stackableWithBase": True
        },
        "active": True
    },
    # Canada - British Columbia
    {
        "jurisdictionCode": "BC",
        "ruleName": "BC Film Incentive - Basic",
        "ruleCode": "BC-FILM-BASIC",
        "incentiveType": "tax_credit",
        "percentage": 35.0,
        "eligibleExpenses": ["bc_labor"],
        "excludedExpenses": ["non_bc_labor", "marketing"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "bcResident": True,
            "canadianContent": True
        },
        "active": True
    },
    {
        "jurisdictionCode": "BC",
        "ruleName": "BC Production Services Tax Credit",
        "ruleCode": "BC-PSTC",
        "incentiveType": "tax_credit",
        "percentage": 28.0,
        "eligibleExpenses": ["bc_labor", "bc_goods_services"],
        "excludedExpenses": ["marketing", "financing"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "foreignProduction": True,
            "bcSpend": 1000000
        },
        "active": True
    },
    # Canada - Ontario
    {
        "jurisdictionCode": "ON",
        "ruleName": "Ontario Film & Television Tax Credit",
        "ruleCode": "ON-FILM-BASE",
        "incentiveType": "tax_credit",
        "percentage": 35.0,
        "eligibleExpenses": ["ontario_labor"],
        "excludedExpenses": ["marketing", "financing"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "ontarioResident": True,
            "canadianContent": True
        },
        "active": True
    },
    {
        "jurisdictionCode": "ON",
        "ruleName": "Ontario Production Services Tax Credit",
        "ruleCode": "ON-PSTC",
        "incentiveType": "tax_credit",
        "percentage": 21.5,
        "eligibleExpenses": ["ontario_labor"],
        "excludedExpenses": ["marketing"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "foreignProduction": True
        },
        "active": True
    },
    # Canada - Quebec
    {
        "jurisdictionCode": "QC",
        "ruleName": "Quebec Film Production Tax Credit",
        "ruleCode": "QC-FILM-BASE",
        "incentiveType": "tax_credit",
        "percentage": 40.0,
        "eligibleExpenses": ["quebec_labor"],
        "excludedExpenses": ["marketing", "above_the_line"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "quebecResident": True,
            "frenchLanguage": 75
        },
        "active": True
    },
    # UK
    {
        "jurisdictionCode": "UK",
        "ruleName": "UK Film Tax Relief",
        "ruleCode": "UK-FILM-BASE",
        "incentiveType": "tax_credit",
        "percentage": 25.0,
        "minSpend": 1000000,
        "eligibleExpenses": ["uk_core_expenditure"],
        "excludedExpenses": ["marketing", "distribution"],
        "effectiveDate": datetime(2024, 1, 1),
        "requirements": {
            "ukSpend": 10,
            "culturalTest": True,
            "ukProduction": True
        },
        "active": True
    },
]


async def seed_incentive_rules():
    """Seed the database with real incentive rules"""
    print("Starting incentive rules seeding...")
    
    try:
        # Connect to database
        await prisma.connect()
        print("Connected to database")
        
        # Get all jurisdictions to map codes to IDs
        jurisdictions = await prisma.jurisdiction.find_many()
        jurisdiction_map = {j.code: j.id for j in jurisdictions}
        print(f"Found {len(jurisdictions)} jurisdictions")
        
        # Check existing rules
        existing_rules = await prisma.incentiverule.find_many()
        existing_codes = {r.ruleCode for r in existing_rules}
        print(f"Found {len(existing_rules)} existing rules")
        
        # Add new rules
        added = 0
        skipped = 0
        errors = 0
        
        for rule_data in incentive_rules_data:
            jurisdiction_code = rule_data.pop("jurisdictionCode")
            
            # Check if jurisdiction exists
            if jurisdiction_code not in jurisdiction_map:
                print(f"WARNING: Jurisdiction {jurisdiction_code} not found, skipping rule {rule_data['ruleName']}")
                errors += 1
                continue
            
            # Check if rule already exists
            if rule_data["ruleCode"] in existing_codes:
                print(f"Skipping {rule_data['ruleName']} - already exists")
                skipped += 1
                continue
            
            try:
                # Get jurisdiction ID
                jurisdiction_id = jurisdiction_map[jurisdiction_code]
                
                # Convert requirements to JSON string
                if "requirements" in rule_data:
                    rule_data["requirements"] = json.dumps(rule_data["requirements"])
                
                # Create rule with proper Prisma relationship
                await prisma.incentiverule.create(
                    data={
                        **rule_data,
                        "jurisdiction": {
                            "connect": {"id": jurisdiction_id}
                        }
                    }
                )
                print(f"Added: {rule_data['ruleName']} ({rule_data['ruleCode']})")
                added += 1
            except Exception as e:
                print(f"ERROR adding {rule_data['ruleName']}: {e}")
                errors += 1
        
        # Disconnect
        await prisma.disconnect()
        
        # Summary
        print("\n" + "="*60)
        print("Incentive Rules Seeding Complete!")
        print(f"Added: {added} rules")
        print(f"Skipped: {skipped} (already existed)")
        print(f"Errors: {errors}")
        print(f"Total rules in database: {len(existing_rules) + added}")
        print("="*60)
        
    except Exception as e:
        print(f"ERROR during seeding: {e}")
        await prisma.disconnect()


if __name__ == "__main__":
    asyncio.run(seed_incentive_rules())
