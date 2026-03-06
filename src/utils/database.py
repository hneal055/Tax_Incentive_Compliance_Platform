"""
Database connection module for PilotForge
"""
import json
import logging
from typing import Any, Dict

from prisma import Prisma

logger = logging.getLogger(__name__)


def parse_json_field(field: Any) -> Dict:
    """Parse a JSON field that may be a string, dict, or None.
    Returns a dictionary; returns empty dict on failure or if field is falsy.
    """
    if isinstance(field, str):
        try:
            return json.loads(field)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON field: {e}. Field content (first 100 chars): {field[:100]}")
            return {}
    if isinstance(field, dict):
        return field
    return {}

# Create global prisma client instance
prisma = Prisma()


async def connect_db():
    """Connect to database"""
    await prisma.connect()


async def disconnect_db():
    """Disconnect from database"""
    await prisma.disconnect()
