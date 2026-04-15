"""Run all baseline jurisdiction + program seeders in one entry point."""
import sys
import os
import logging

# Ensure backend root is on sys.path when executed as a script from backend/scripts.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.add_georgia import add_georgia
from scripts.seed_georgia import seed_georgia
from scripts.add_louisiana import add_louisiana
from scripts.seed_louisiana import seed_louisiana
from scripts.add_new_jersey import add_new_jersey
from scripts.seed_new_jersey import seed_new_jersey

logger = logging.getLogger(__name__)


def seed_baseline():
    """Seed all baseline jurisdictions and programs.

    Add future jurisdictions/programs here so startup and manual runs stay centralized.
    """
    # Jurisdictions first
    add_georgia()
    add_louisiana()
    add_new_jersey()

    # Programs second
    seed_georgia()
    seed_louisiana()
    seed_new_jersey()

    logger.info("Baseline seeding complete")


if __name__ == "__main__":
    seed_baseline()