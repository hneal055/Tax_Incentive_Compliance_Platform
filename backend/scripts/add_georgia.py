"""Add Georgia jurisdiction to the database."""
import sys, os, uuid, logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.db.session import SessionLocal
from app.models.jurisdiction import Jurisdiction
logger = logging.getLogger(__name__)

def add_georgia():
    db = SessionLocal()
    try:
        existing = db.query(Jurisdiction).filter(Jurisdiction.name == "Georgia").first()
        if existing:
            logger.info(f"Georgia already exists: {existing.id}")
            return existing.id
        georgia = Jurisdiction(
            id=str(uuid.uuid4()),
            name="Georgia",
            type="state"
        )
        db.add(georgia)
        db.commit()
        logger.info(f"✅ Created Georgia: {georgia.id}")
        return georgia.id
    except Exception as e:
        logger.error(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_georgia()
