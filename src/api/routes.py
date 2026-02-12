"""
Main API router - aggregates all route modules
"""
from fastapi import APIRouter
from src.api.v1 import router as v1_router

router = APIRouter()

# Include v1 API router
router.include_router(v1_router)

