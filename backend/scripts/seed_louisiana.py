"""Seed Louisiana Motion Picture Production Program rules."""
import sys, os, uuid, json, logging
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.db.session import SessionLocal
from app.models.jurisdiction import Jurisdiction
from app.models.program import Program

logger = logging.getLogger(__name__)


LOUISIANA_RULES = {
    "program_name": "Louisiana Motion Picture Production Program",
    "jurisdiction": "Louisiana",
    "version": "2026.01",
    "base_credit_rate": 0.25,
    "bonus_conditions": [
        {
            "id": "promotional_logo",
            "name": "Louisiana Promotional Logo",
            "rate": 0.05,
            "condition": "logo_included == True",
            "description": "Additional 5% for including Louisiana promotional logo in credits"
        }
    ],
    "qualified_expenditure_categories": [
        "above_the_line", "below_the_line", "post_production",
        "visual_effects", "music_production", "transportation", "lodging"
    ],
    "minimum_requirements": [
        {
            "id": "min_spend",
            "rule": "qualified_spend >= 500000",
            "message": "Minimum qualified spend of $500,000 required",
            "severity": "blocking"
        },
        {
            "id": "georgia_filming",
            "rule": "filming_location contains 'Louisiana'",
            "message": "At least 50% of principal photography must occur in Louisiana",
            "severity": "blocking"
        }
    ],
    "exclusions": [
        {
            "category": "music_licensing",
            "condition": "licensor_resident_louisiana == False",
            "message": "Music licensing payments to non-Louisiana residents are excluded"
        }
    ],
    "local_hire_bonus": {
        "rate": 0.05,
        "threshold": 0.20,
        "description": "Additional 5% when Louisiana resident crew exceeds 20% of total crew",
        "condition": "local_hire_percentage >= 0.20"
    },
    "diversity_bonus": {
        "rate": 0.02,
        "threshold": 0.20,
        "description": "Additional 2% for diversity in key creative roles",
        "condition": "diversity_score >= 0.20"
    },
    "application_deadlines": {
        "initial_application": {
            "timing": "within 90 days of principal photography commencement",
            "message": "Initial application must be filed within 90 days"
        },
        "final_claim": {
            "timing": "within 3 years of completion",
            "message": "Final claim must be submitted within 3 years"
        }
    },
    "checklist": [
        {"item": "Register with Louisiana Entertainment Office", "required": True},
        {"item": "Submit initial certification application", "required": True},
        {"item": "Provide affidavit of Louisiana spend", "required": True},
        {"item": "Confirm promotional logo inclusion", "required": False, "condition": "logo_included == True"}
    ],
    "transferability": {
        "allowed": True,
        "fee_market_range": "0.87 - 0.93 per dollar",
        "notes": "Credits are transferable; market pricing varies by demand and transaction costs"
    },
    "sunset_date": "2029-12-31"
}


def seed_louisiana():
    db = SessionLocal()
    try:
        louisiana = db.query(Jurisdiction).filter(Jurisdiction.name == "Louisiana").first()
        if not louisiana:
            logger.error("Louisiana jurisdiction not found. Run add_louisiana first.")
            return None

        existing = db.query(Program).filter(
            Program.name == "Louisiana Motion Picture Production Program",
            Program.jurisdiction_id == louisiana.id
        ).first()

        if existing:
            existing.rules = json.dumps(LOUISIANA_RULES)
            existing.description = "Louisiana production incentive with transferable credit and workforce/diversity bonuses."
            existing.active = True
            existing.updated_at = datetime.utcnow()
            logger.info(f"Updated existing program: {existing.id}")
            db.commit()
            return existing.id

        program = Program(
            id=str(uuid.uuid4()),
            jurisdiction_id=louisiana.id,
            name="Louisiana Motion Picture Production Program",
            description="Louisiana production incentive with transferable credit and workforce/diversity bonuses.",
            rules=json.dumps(LOUISIANA_RULES),
            active=True
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
    seed_louisiana()
