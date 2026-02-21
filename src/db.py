"""
Database dependency for FastAPI
"""
from prisma import Prisma
from src.utils.database import prisma


async def get_db() -> Prisma:
    """
    FastAPI dependency to get database connection
    """
    return prisma
