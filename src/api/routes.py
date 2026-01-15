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

router = APIRouter()

# Include routers
router.include_router(jurisdictions_router)
router.include_router(incentive_rules_router)
router.include_router(productions_router)
router.include_router(calculator_router)
router.include_router(reports_router)
router.include_router(excel_router)


@router.get("/")
async def api_root():
    """API root endpoint"""
    return {
        "message": "PilotForge API",
        "version": "v1",
        "endpoints": {
            "jurisdictions": "/api/0.1.0/jurisdictions",
"incentive_rules": "/api/0.1.0/incentive-rules",
"productions": "/api/0.1.0/productions",
"calculator": "/api/0.1.0/calculate",
"reports": "/api/0.1.0/reports",
"excel": "/api/0.1.0/excel",

        }
    }
