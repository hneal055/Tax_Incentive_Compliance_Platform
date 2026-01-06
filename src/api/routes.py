from fastapi import APIRouter

from src.api.jurisdictions import router as jurisdictions_router
from src.api.incentive_rules import router as incentive_rules_router
from src.api.calculations import router as calculations_router

router = APIRouter()

router.include_router(jurisdictions_router)
router.include_router(incentive_rules_router)
router.include_router(calculations_router)

@router.get("/")
async def api_root():
    return {
        "message": "Tax-Incentive Compliance API",
        "endpoints": {
            "jurisdictions": "/api/v1/jurisdictions",
            "incentive_rules": "/api/v1/incentive-rules",
            "calculations": "/api/v1/calculations",
            "docs": "/docs"
        }
    }
