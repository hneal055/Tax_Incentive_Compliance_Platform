"""Database connection"""
from prisma import Prisma

prisma = Prisma()

async def get_db():
    return prisma
