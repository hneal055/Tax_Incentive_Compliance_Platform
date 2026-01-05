"""
Main API router - aggregates all route modules
"""
from fastapi import APIRouter
from src.api.jurisdictions import router as jurisdictions_router
from src.api.incentive_rules import router as incentive_rules_router

router = APIRouter()

# Include routers
router.include_router(jurisdictions_router)
router.include_router(incentive_rules_router)


@router.get("/")
async def api_root():
    """API root endpoint"""
    return {
        "message": "Tax-Incentive Compliance Platform API",
        "version": "v1",
        "endpoints": {
            "jurisdictions": "/api/v1/jurisdictions",
            "incentive_rules": "/api/v1/incentive-rules",
            "productions": "/api/v1/productions (coming soon)",
            "expenses": "/api/v1/expenses (coming soon)",
            "calculations": "/api/v1/calculations (coming soon)"
        }
    }
