"""Add Louisiana jurisdiction to the database."""
import sys, os, uuid, logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.db.session import SessionLocal
from app.models.jurisdiction import Jurisdiction

logger = logging.getLogger(__name__)


def add_louisiana():
    db = SessionLocal()
    try:
        existing = db.query(Jurisdiction).filter(Jurisdiction.name == "Louisiana").first()
        if existing:
            logger.info(f"Louisiana already exists: {existing.id}")
            return existing.id

        louisiana = Jurisdiction(
            id=str(uuid.uuid4()),
            name="Louisiana",
            type="state"
        )
        db.add(louisiana)
        db.commit()
        logger.info(f"Created Louisiana: {louisiana.id}")
        return louisiana.id
    except Exception as e:
        logger.error(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_louisiana()
