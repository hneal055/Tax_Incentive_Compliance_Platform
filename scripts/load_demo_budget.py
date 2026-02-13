#!/usr/bin/env python3
"""
Load the Atlanta Heist demo budget into PilotForge for testing/demo.
"""

import asyncio
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from src.utils.database import prisma


async def load_demo_budget():
    """Load the sample MMB file into the database."""
    
    # Load XML file
    file_path = Path(__file__).parent.parent / "tests" / "fixtures" / "mmb_files" / "atlanta_heist.mmbx"
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Connect to database if not already connected
    if not prisma.is_connected():
        await prisma.connect()
    
    # Get or create a jurisdiction (Georgia)
    jurisdiction = await prisma.jurisdiction.find_first(
        where={"code": "GA"}
    )
    
    if not jurisdiction:
        # Create a basic Georgia jurisdiction if it doesn't exist
        jurisdiction = await prisma.jurisdiction.create({
            "name": "Georgia",
            "code": "GA",
            "country": "USA",
            "jurisdictionType": "state",
            "baseIncentiveRate": 0.30,
            "currency": "USD",
            "isActive": True
        })
        print(f"✅ Created jurisdiction: {jurisdiction.name}")
    
    # Create production record
    header = root.find("Header")
    summary = root.find("Summary")
    shoot_dates = header.find("ShootDates")
    
    production = await prisma.production.create({
        "title": header.find("Title").text,
        "productionType": "feature",
        "jurisdictionId": jurisdiction.id,
        "budgetTotal": float(summary.find("Total").text),
        "budgetQualifying": float(summary.find("BelowLine").text) + float(summary.find("Post").text),
        "startDate": datetime.fromisoformat(shoot_dates.find("Start").text),
        "endDate": datetime.fromisoformat(shoot_dates.find("End").text),
        "productionCompany": header.find("Producer").text,
        "status": "pre_production"
    })
    
    print(f"✅ Created production: {production.title}")
    
    # Extract and create expenses
    expenses = []
    for category in root.findall(".//Category"):
        category_name = category.get("name")
        
        for account in category.findall("Account"):
            account_name = account.get("name")
            account_amount = float(account.get("amount", 0))
            
            # Create expense for account total
            expense = await prisma.expense.create({
                "productionId": production.id,
                "category": category_name,
                "subcategory": account_name,
                "description": f"{account_name} - Total",
                "amount": account_amount,
                "expenseDate": datetime.fromisoformat("2024-06-01"),
                "isQualifying": _is_qualifying(category_name, account_name)
            })
            expenses.append(expense)
            
            # Create expenses for subaccounts
            for sub in account.findall("SubAccount"):
                sub_name = sub.get("name")
                sub_amount = float(sub.get("amount", 0))
                
                expense = await prisma.expense.create({
                    "productionId": production.id,
                    "category": category_name,
                    "subcategory": account_name,
                    "description": sub_name,
                    "amount": sub_amount,
                    "expenseDate": datetime.fromisoformat("2024-06-01"),
                    "isQualifying": _is_qualifying(category_name, account_name, sub_name)
                })
                expenses.append(expense)
    
    print(f"✅ Created {len(expenses)} expense records")
    print(f"\n🎬 Demo budget loaded successfully!")
    print(f"Production ID: {production.id}")
    print(f"Total Budget: ${production.budgetTotal:,.0f}")
    
    return production


def _is_qualifying(category, account, subaccount=None):
    """Determine if an expense is qualifying for Georgia incentives."""
    
    # Georgia qualifying rules
    qualifying_categories = [
        "Below-the-Line",
        "Post-Production"
    ]
    
    # Non-qualifying categories
    non_qualifying = [
        "Above-the-Line",
        "Contingency",
        "Fringes"  # Some fringes qualify, but not all
    ]
    
    if category in qualifying_categories:
        return True
    
    # Special cases
    if category == "Fringes" and "Payroll" in account:
        return True  # Payroll taxes often qualify
        
    if "Music" in str(account) and "Scoring" in str(subaccount):
        return True  # Scoring sessions qualify
        
    return False


if __name__ == "__main__":
    asyncio.run(load_demo_budget())
