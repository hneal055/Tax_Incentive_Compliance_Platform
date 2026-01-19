"""
Main API router - aggregates all route modules
"""
from fastapi import APIRouter

from src.api.jurisdictions import router as jurisdictions_router
from src.api.incentive_rules import router as incentive_rules_router
from src.api.productions import router as productions_router
from src.api.calculator import router as calculator_router
from src.api.reports import router as reports_router
from src.api.excel import router as excel_router
from src.api.expenses import router as expenses_router

API_PREFIX = "/api/0.1.0"

router = APIRouter()

# Include routers
router.include_router(jurisdictions_router)
router.include_router(incentive_rules_router)
router.include_router(productions_router)
router.include_router(calculator_router)
router.include_router(reports_router)
router.include_router(excel_router)
router.include_router(expenses_router)


@router.get("/", tags=["Meta"])
async def api_root():
    """API root endpoint (under /api/0.1.0/)"""
    return {
        "message": "Tax Incentive Compliance Platform API",
        "version": "1.0.0",
        "endpoints": {
            "jurisdictions": f"{API_PREFIX}/jurisdictions/",
            "incentive_rules": f"{API_PREFIX}/incentive-rules/",
            "productions": f"{API_PREFIX}/productions/",
            "expenses": f"{API_PREFIX}/expenses/",
            "calculator_simple": f"{API_PREFIX}/calculate/simple",
            "calculator_compare": f"{API_PREFIX}/calculate/compare",
            "reports": f"{API_PREFIX}/reports",
            "excel": f"{API_PREFIX}/excel",
            "health": "/health",
        },
    }
