"""
Seed incentive rules into database
"""
import asyncio
from prisma import Prisma
from datetime import datetime
import json

async def seed_rules():
    db = Prisma()
    await db.connect()
    
    print("🎬 Adding Incentive Rules...\n")
    
    # 1. Georgia
    try:
        ga_rule = await db.incentiverule.create(
            data={
                "jurisdictionId": "d258f302-dfb5-4449-8bce-eb723a11429b",
                "ruleName": "Georgia Film Tax Credit",
                "ruleCode": "GA-FTC-2025",
                "incentiveType": "tax_credit",
                "percentage": 20.0,
                "fixedAmount": 0.0,
                "minSpend": 500000.0,
                "maxCredit": 0.0,
                "eligibleExpenses": ["cast_salaries", "crew_salaries", "equipment_rental", "location_fees", "set_construction", "post_production"],
                "excludedExpenses": ["marketing", "distribution", "financing_costs"],
                "effectiveDate": datetime(2025, 1, 1),
                "requirements": json.dumps({
                    "georgia_logo": "Must include Georgia promotional logo in credits",
                    "minimum_spend": "$500,000 minimum qualified expenditure",
                    "promotional_uplift": "Additional 10% for Georgia promotional logo (total 30%)"
                }),
                "active": True
            }
        )
        print(f"✅ 1. {ga_rule.ruleName}")
    except Exception as e:
        print(f"❌ Georgia: {e}")
    
    # 2. California
    try:
        ca_rule = await db.incentiverule.create(
            data={
                "jurisdictionId": "0cfcc411-59d8-4056-944d-fc5ea288479a",
                "ruleName": "California Film & TV Tax Credit 3.0",
                "ruleCode": "CA-FTC-2025",
                "incentiveType": "tax_credit",
                "percentage": 20.0,
                "fixedAmount": 0.0,
                "minSpend": 1000000.0,
                "maxCredit": 25000000.0,
                "eligibleExpenses": ["qualified_wages", "qualified_expenditures", "below_the_line_salaries"],
                "excludedExpenses": ["above_the_line_talent", "marketing", "distribution"],
                "effectiveDate": datetime(2025, 1, 1),
                "expirationDate": datetime(2030, 6, 30),
                "requirements": json.dumps({
                    "allocation_required": "Must receive tax credit allocation from CFC",
                    "minimum_spend": "$1M for features, $500K for relocating TV",
                    "jobs_ratio": "Minimum 75% of principal photography days in California"
                }),
                "active": True
            }
        )
        print(f"✅ 2. {ca_rule.ruleName}")
    except Exception as e:
        print(f"❌ California: {e}")
    
    # 3. New York
    try:
        ny_rule = await db.incentiverule.create(
            data={
                "jurisdictionId": "d8984f4a-caf3-4447-9402-6e4ecf3ab7f9",
                "ruleName": "New York State Film Tax Credit",
                "ruleCode": "NY-FTC-2025",
                "incentiveType": "tax_credit",
                "percentage": 25.0,
                "fixedAmount": 0.0,
                "minSpend": 1000000.0,
                "maxCredit": 0.0,
                "eligibleExpenses": ["production_costs", "post_production_costs", "qualified_labor"],
                "excludedExpenses": ["marketing", "distribution", "financing_costs"],
                "effectiveDate": datetime(2025, 1, 1),
                "requirements": json.dumps({
                    "minimum_spend": "$1M in qualified production costs",
                    "upstate_bonus": "Additional 10% for production in certain upstate counties"
                }),
                "active": True
            }
        )
        print(f"✅ 3. {ny_rule.ruleName}")
    except Exception as e:
        print(f"❌ New York: {e}")
    
    # 4. Louisiana
    try:
        la_rule = await db.incentiverule.create(
            data={
                "jurisdictionId": "ded634c1-216f-4f52-88cb-1a66c945c4f9",
                "ruleName": "Louisiana Motion Picture Production Tax Credit",
                "ruleCode": "LA-MPPTC-2025",
                "incentiveType": "tax_credit",
                "percentage": 18.0,
                "fixedAmount": 0.0,
                "minSpend": 300000.0,
                "maxCredit": 0.0,
                "eligibleExpenses": ["production_expenditures", "resident_labor", "non_resident_labor"],
                "excludedExpenses": ["marketing", "distribution"],
                "effectiveDate": datetime(2025, 1, 1),
                "requirements": json.dumps({
                    "base_credit": "18% base transferable credit",
                    "resident_payroll_bonus": "Additional 7% for resident labor (total 25%)",
                    "transferable": "Credits are transferable"
                }),
                "active": True
            }
        )
        print(f"✅ 4. {la_rule.ruleName}")
    except Exception as e:
        print(f"❌ Louisiana: {e}")
    
    # 5. New Mexico
    try:
        nm_rule = await db.incentiverule.create(
            data={
                "jurisdictionId": "048ae514-1d28-4cac-a918-38f2e56d6e49",
                "ruleName": "New Mexico Film Production Tax Credit",
                "ruleCode": "NM-FPTC-2025",
                "incentiveType": "tax_credit",
                "percentage": 25.0,
                "fixedAmount": 0.0,
                "minSpend": 50000.0,
                "maxCredit": 110000000.0,
                "eligibleExpenses": ["direct_production_costs", "resident_labor", "non_resident_labor"],
                "excludedExpenses": ["marketing", "distribution", "financing"],
                "effectiveDate": datetime(2025, 1, 1),
                "requirements": json.dumps({
                    "base_credit": "25% refundable base credit",
                    "series_bonus": "Additional 5% for TV series (total 30%)",
                    "combined_max": "Up to 35% total credit"
                }),
                "active": True
            }
        )
        print(f"✅ 5. {nm_rule.ruleName}")
    except Exception as e:
        print(f"❌ New Mexico: {e}")
    
    # 6. Texas
    try:
        tx_rule = await db.incentiverule.create(
            data={
                "jurisdictionId": "6254dcbe-c4da-4a01-b4d7-141e1b53ee1a",
                "ruleName": "Texas Moving Image Industry Incentive Program",
                "ruleCode": "TX-MIIIP-2025",
                "incentiveType": "grant",
                "percentage": 15.0,
                "fixedAmount": 0.0,
                "minSpend": 100000.0,
                "maxCredit": 0.0,
                "eligibleExpenses": ["texas_wages", "texas_goods_services"],
                "excludedExpenses": ["marketing", "distribution", "out_of_state_expenses"],
                "effectiveDate": datetime(2025, 1, 1),
                "requirements": json.dumps({
                    "base_grant": "15% cash grant on Texas spending",
                    "underused_areas_bonus": "Additional 7.5% for filming in underused areas (total 22.5%)",
                    "grant_type": "Cash grant, not tax credit"
                }),
                "active": True
            }
        )
        print(f"✅ 6. {tx_rule.ruleName}")
    except Exception as e:
        print(f"❌ Texas: {e}")
    
    # Count rules
    total = await db.incentiverule.count()
    print(f"\n🎉 Total Incentive Rules: {total}")
    
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(seed_rules())