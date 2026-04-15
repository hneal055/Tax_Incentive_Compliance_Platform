"""Add New Jersey jurisdiction to the database."""
import sys
import os
import uuid
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.db.session import SessionLocal
from app.models.jurisdiction import Jurisdiction

logger = logging.getLogger(__name__)


def add_new_jersey():
    db = SessionLocal()
    try:
        existing = db.query(Jurisdiction).filter(Jurisdiction.name == "New Jersey").first()
        if existing:
            logger.info(f"New Jersey already exists: {existing.id}")
            return existing.id

        new_jersey = Jurisdiction(
            id=str(uuid.uuid4()),
            name="New Jersey",
            type="state",
        )
        db.add(new_jersey)
        db.commit()
        logger.info(f"Created New Jersey: {new_jersey.id}")
        return new_jersey.id
    except Exception as e:
        logger.error(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_new_jersey()