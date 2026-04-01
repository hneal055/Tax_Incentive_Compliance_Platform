"""Seed Georgia Film Tax Credit program."""
import sys, os, uuid, json, logging
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.db.session import SessionLocal
from app.models.jurisdiction import Jurisdiction
from app.models.program import Program
logger = logging.getLogger(__name__)

GEORGIA_RULES = {"program_name":"Georgia Film Tax Credit","base_credit_rate":0.20,"bonus_conditions":[{"id":"promotional_logo","name":"Georgia Promotional Logo","rate":0.10,"condition":"logo_included == true"}],"qualified_expenditure_categories":["above_the_line","below_the_line","post_production","visual_effects","music_production","transportation","lodging"],"minimum_requirements":[{"id":"min_spend","rule":"qualified_spend >= 500000","message":"Minimum qualified spend of $500,000 required"},{"id":"georgia_filming","rule":"filming_location contains 'Georgia'","message":"Filming must occur in Georgia"}],"local_hire_bonus":{"rate":0.05,"threshold":0.15},"diversity_bonus":{"rate":0.02,"threshold":0.20},"checklist":[{"item":"Register with Georgia Film Office","required":true},{"item":"Submit GEIPA form","required":true},{"item":"Provide affidavit of Georgia spend","required":true}],"sunset_date":"2028-12-31"}

def seed_georgia():
    db = SessionLocal()
    try:
        georgia = db.query(Jurisdiction).filter(Jurisdiction.name == "Georgia").first()
        if not georgia:
            logger.error("Georgia not found")
            return None
        existing = db.query(Program).filter(Program.name == "Georgia Film Tax Credit").first()
        if existing:
            existing.rules = json.dumps(GEORGIA_RULES)
            existing.updated_at = datetime.utcnow()
            logger.info(f"Updated program: {existing.id}")
            return existing.id
        program = Program(id=str(uuid.uuid4()), jurisdiction_id=georgia.id, name="Georgia Film Tax Credit", rules=json.dumps(GEORGIA_RULES), active=True)
        db.add(program)
        db.commit()
        logger.info(f"Created program: {program.id}")
        return program.id
    except Exception as e:
        logger.error(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_georgia()
