#!/usr/bin/env python3
"""
Seed script to load Georgia Film Tax Credit program rules into the database.
Run: python -m scripts.seed_georgia
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.jurisdiction import Jurisdiction
from app.models.program import Program
from uuid import uuid4
from datetime import datetime

# The complete Georgia rules JSON (from our design)
GEORGIA_RULES = {
    "program_name": "Georgia Film Tax Credit",
    "jurisdiction": "Georgia",
    "version": "2025.01",
    "base_credit_rate": 0.20,
    "bonus_conditions": [
        {
            "id": "promotional_logo",
            "name": "Georgia Promotional Logo",
            "rate": 0.10,
            "condition": "logo_included == true",
            "description": "Additional 10% for including the Georgia state logo in credits",
        }
    ],
    "qualified_expenditure_categories": [
        "above_the_line",
        "below_the_line",
        "post_production",
        "visual_effects",
        "music_production",
        "transportation",
        "lodging",
    ],
    "minimum_requirements": [
        {
            "id": "min_spend",
            "rule": "qualified_spend >= 500000",
            "message": "Minimum qualified spend of $500,000 required",
            "severity": "blocking",
        },
        {
            "id": "georgia_filming",
            "rule": "filming_location contains 'Georgia'",
            "message": "At least 50% of principal photography must occur in Georgia",
            "severity": "blocking",
        },
    ],
    "exclusions": [
        {
            "category": "music_licensing",
            "condition": "licensor_resident_georgia == false",
            "message": "Music licensing payments to non-Georgia residents are excluded",
        },
        {
            "category": "travel_outside_georgia",
            "condition": "travel_destination != 'Georgia'",
            "message": "Travel expenses outside Georgia are excluded",
        },
    ],
    "local_hire_bonus": {
        "rate": 0.05,
        "threshold": 0.15,
        "description": "Additional 5% when Georgia resident crew exceeds 15% of total crew",
        "condition": "local_hire_percentage >= 0.15",
    },
    "diversity_bonus": {
        "rate": 0.02,
        "threshold": 0.20,
        "description": "Additional 2% for diversity in key creative roles",
        "condition": "diversity_score >= 0.20",
    },
    "application_deadlines": {
        "initial_application": {
            "timing": "within 90 days of principal photography commencement",
            "grace_period_days": 30,
            "message": "Initial application must be filed within 90 days of start of principal photography",
        },
        "final_claim": {
            "timing": "within 3 years of completion of principal photography",
            "message": "Final claim must be submitted within 3 years of production completion",
        },
        "interim_reports": {
            "frequency": "annual",
            "message": "Annual progress reports required until final claim",
        },
    },
    "checklist": [
        {
            "item": "Register with Georgia Film Office",
            "url": "https://www.georgiafilm.org/registration",
            "required": True,
        },
        {
            "item": "Submit Georgia Entertainment Industry Promotion Act (GEIPA) form",
            "required": True,
        },
        {"item": "Provide affidavit of Georgia spend", "required": True},
        {
            "item": "Confirm promotional logo inclusion (if claiming bonus)",
            "required": False,
            "condition": "logo_included == true",
        },
    ],
    "transferability": {
        "allowed": True,
        "fee_market_range": "0.88 - 0.94 per dollar",
        "notes": "Credits are transferable; typically sold at 88-94% of face value",
    },
    "sunset_date": "2028-12-31",
}


def seed_georgia():
    db = SessionLocal()

    try:
        # Check if Georgia jurisdiction exists
        georgia = db.query(Jurisdiction).filter(Jurisdiction.name == "Georgia").first()

        if not georgia:
            print("❌ Georgia jurisdiction not found. Please create it first.")
            print(
                "   Run: INSERT INTO jurisdictions (id, name, type) VALUES (uuid_generate_v4(), 'Georgia', 'state');"
            )
            return

        # Check if program already exists
        existing = (
            db.query(Program)
            .filter(
                Program.name == "Georgia Film Tax Credit",
                Program.jurisdiction_id == georgia.id,
            )
            .first()
        )

        if existing:
            print(f"⚠️  Program already exists. Updating rules for: {existing.id}")
            existing.rules = GEORGIA_RULES
            existing.updated_at = datetime.utcnow()
        else:
            # Create new program
            program = Program(
                id=uuid4(),
                jurisdiction_id=georgia.id,
                name="Georgia Film Tax Credit",
                description="Georgia's film tax credit program offers 20% base credit with up to 10% additional for promotional logo and bonuses for local hire and diversity.",
                rules=GEORGIA_RULES,
                active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(program)
            print(f"✅ Created new program with ID: {program.id}")

        db.commit()
        print("✅ Georgia rules seeded successfully!")

        # Show preview
        program = (
            db.query(Program)
            .filter(
                Program.name == "Georgia Film Tax Credit",
                Program.jurisdiction_id == georgia.id,
            )
            .first()
        )
        print(f"\n📋 Program: {program.name}")
        print(f"   Base Rate: {program.rules['base_credit_rate'] * 100}%")
        print(
            f"   Qualified Categories: {len(program.rules['qualified_expenditure_categories'])}"
        )
        print(f"   Bonus Conditions: {len(program.rules['bonus_conditions'])}")
        print(f"   Checklist Items: {len(program.rules['checklist'])}")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_georgia()
