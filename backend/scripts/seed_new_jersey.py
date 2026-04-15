"""Seed New Jersey Film and Digital Media Tax Credit Program rules."""
import sys
import os
import uuid
import json
import logging
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.db.session import SessionLocal
from app.models.jurisdiction import Jurisdiction
from app.models.program import Program

logger = logging.getLogger(__name__)


NEW_JERSEY_RULES = {
    "program_name": "New Jersey Film and Digital Media Tax Credit Program",
    "jurisdiction": "New Jersey",
    "version": "2026.01",
    "source_urls": [
        "https://nj.gov/njfilm/index.shtml",
        "https://nj.gov/njfilm/incentives-credit.shtml",
        "https://nj.gov/njfilm/incentives-studio-partners-film-lease-partners-designation.shtml",
        "https://nj.gov/njfilm/incentives-sales.shtml",
        "https://www.njeda.gov/film/",
    ],
    "base_credit_rate": 0.30,
    "bonus_conditions": [
        {
            "id": "designated_subjurisdiction",
            "name": "Designated New Jersey Sub-Jurisdiction Bonus",
            "rate": 0.05,
            "applies_to": "sub_jurisdiction",
            "locations": [
                "Atlantic City",
                "Camden",
                "East Orange",
                "Elizabeth",
                "Jersey City",
                "New Brunswick",
                "Newark",
                "Paterson",
                "Trenton",
            ],
            "description": "Projects in designated municipalities can receive up to 35% total credit."
        },
        {
            "id": "film_lease_partner_bonus",
            "name": "Film-Lease Partner Facility Bonus",
            "rate": 0.10,
            "applies_to": "film_lease_partner",
            "description": "Film-lease production company projects at designated facilities can qualify for increased base credit up to 40%."
        }
    ],
    "qualified_expenditure_categories": [
        "above_the_line",
        "below_the_line",
        "post_production",
        "visual_effects",
        "digital_media_labor",
        "production_services",
        "transportation",
        "lodging"
    ],
    "minimum_requirements": [
        {
            "id": "min_spend",
            "rule": "qualified_spend >= 500000",
            "message": "Minimum qualified spend of $500,000 required",
            "severity": "blocking"
        },
        {
            "id": "new_jersey_filming",
            "rule": "filming_location contains 'New Jersey'",
            "rule_type": "location",
            "message": "Project must include filming in New Jersey",
            "severity": "blocking"
        }
    ],
    "exclusions": [
        {
            "category": "non_qualified_expenses",
            "condition": "expense_not_eligible_under_njeda_rules",
            "message": "Only qualified expenses are eligible under the NJ Film and Digital Media Tax Credit Program"
        }
    ],
    "local_hire_bonus": {
        "rate": 0.0,
        "threshold": 1.0,
        "description": "No generalized local-hire bonus configured in this integration for New Jersey."
    },
    "diversity_bonus": {
        "rate": 0.02,
        "threshold": 0.20,
        "description": "Additional 2% for diversity in key creative roles where applicable.",
        "condition": "diversity_score >= 0.20"
    },
    "application_deadlines": {
        "initial_application": {
            "timing": "See NJEDA application portal",
            "message": "Apply through NJEDA Film and Digital Media Tax Credit portal"
        },
        "final_claim": {
            "timing": "See NJEDA guidance",
            "message": "Final claim timing follows NJEDA program guidance"
        }
    },
    "checklist": [
        {"item": "Register business to do business in New Jersey", "required": True},
        {"item": "Submit application through NJEDA Film Tax Credit portal", "required": True},
        {"item": "Document all qualified New Jersey expenditures", "required": True},
        {"item": "Confirm designated municipality eligibility for 35% tier", "required": False},
        {"item": "Confirm film-lease partner facility qualification for up to 40% tier", "required": False},
    ],
    "transferability": {
        "allowed": True,
        "notes": "Transferable credit against corporation business tax and gross income tax."
    },
    "sub_jurisdictions": {
        "designated_35_percent_municipalities": [
            "Atlantic City",
            "Camden",
            "East Orange",
            "Elizabeth",
            "Jersey City",
            "New Brunswick",
            "Newark",
            "Paterson",
            "Trenton"
        ],
        "commission_offices": ["Newark", "North Brunswick", "Trenton"]
    },
    "sales_tax_exemption": {
        "rate": 0.06625,
        "description": "Certain tangible property used directly and primarily in production may be exempt from New Jersey sales tax; long-term hotel rentals over 90 days may also qualify."
    },
    "sunset_date": None
}


def seed_new_jersey():
    db = SessionLocal()
    try:
        new_jersey = db.query(Jurisdiction).filter(Jurisdiction.name == "New Jersey").first()
        if not new_jersey:
            logger.error("New Jersey jurisdiction not found. Run add_new_jersey first.")
            return None

        existing = db.query(Program).filter(
            Program.name == "New Jersey Film and Digital Media Tax Credit Program",
            Program.jurisdiction_id == new_jersey.id,
        ).first()

        if existing:
            existing.rules = json.dumps(NEW_JERSEY_RULES)
            existing.description = "New Jersey incentive with 30% base, designated sub-jurisdiction 35% tier, and qualified film-lease partner projects up to 40%."
            existing.active = True
            existing.updated_at = datetime.utcnow()
            logger.info(f"Updated existing program: {existing.id}")
            db.commit()
            return existing.id

        program = Program(
            id=str(uuid.uuid4()),
            jurisdiction_id=new_jersey.id,
            name="New Jersey Film and Digital Media Tax Credit Program",
            description="New Jersey incentive with 30% base, designated sub-jurisdiction 35% tier, and qualified film-lease partner projects up to 40%.",
            rules=json.dumps(NEW_JERSEY_RULES),
            active=True,
        )
        db.add(program)
        db.commit()
        logger.info(f"Created new program: {program.id}")
        return program.id

    except Exception as e:
        logger.error(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_new_jersey()