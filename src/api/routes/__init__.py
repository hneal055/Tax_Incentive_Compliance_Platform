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
from src.api.rule_engine import router as rule_engine_router

# New v1 routers for MMB Connector integration
from src.api.routes.budgets import router as budgets_router
from src.api.routes.incentives import router as incentives_router
from src.api.routes.compliance import router as compliance_router
from src.api.routes.sync import router as sync_router
from src.api.routes.auth import router as auth_router

API_PREFIX = "/api/0.1.0"

router = APIRouter()

# Include existing routers
router.include_router(jurisdictions_router)
router.include_router(incentive_rules_router)
router.include_router(productions_router)
router.include_router(calculator_router)
router.include_router(reports_router)
router.include_router(excel_router)
router.include_router(rule_engine_router)

# Include new MMB Connector integration routers (under /v1 prefix)
router.include_router(auth_router, prefix="/v1")
router.include_router(budgets_router, prefix="/v1")
router.include_router(incentives_router, prefix="/v1")
router.include_router(compliance_router, prefix="/v1")
router.include_router(sync_router, prefix="/v1")


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
            "calculator_simple": f"{API_PREFIX}/calculate/simple",
            "calculator_compare": f"{API_PREFIX}/calculate/compare",
            "reports": f"{API_PREFIX}/reports",
            "excel": f"{API_PREFIX}/excel",
            "health": "/health",
            "budgets": f"{API_PREFIX}/v1/budgets",
            "auth": f"{API_PREFIX}/v1/auth/token",
            "webhooks": f"{API_PREFIX}/v1/webhooks/register",
        },
    }


@router.get("/health", tags=["Health"])
async def api_health():
    """Health check endpoint accessible at /api/{version}/health"""
    return {"status": "healthy", "version": "1.0.0"}
