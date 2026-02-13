"""
V1 API Module
"""
from fastapi import APIRouter
from src.api.v1.endpoints import (
    api_keys,
    productions,
    calculator,
    monitoring,
    expenses,
    reports,
    jurisdictions,
    incentive_rules,
    excel,
    rule_engine,
    organizations,
    mmb
)

API_PREFIX = "/api/v1"

router = APIRouter()

# Include all v1 endpoint routers
router.include_router(api_keys.router)
router.include_router(productions.router)
router.include_router(calculator.router)
router.include_router(monitoring.router)
router.include_router(expenses.router)
router.include_router(reports.router)
router.include_router(jurisdictions.router)
router.include_router(incentive_rules.router)
router.include_router(excel.router)
router.include_router(rule_engine.router)
router.include_router(organizations.router)
router.include_router(mmb.router)


@router.get("/", tags=["Meta"])
async def api_v1_root():
    """API v1 root endpoint"""
    return {
        "message": "Welcome to PilotForge API v1",
        "version": "1.0.0",
        "endpoints": {
            "api_keys": f"{API_PREFIX}/api-keys/",
            "organizations": f"{API_PREFIX}/organizations/",
            "jurisdictions": f"{API_PREFIX}/jurisdictions/",
            "incentive_rules": f"{API_PREFIX}/incentive-rules/",
            "productions": f"{API_PREFIX}/productions/",
            "expenses": f"{API_PREFIX}/expenses/",
            "calculator_simple": f"{API_PREFIX}/calculate/simple",
            "calculator_compare": f"{API_PREFIX}/calculate/compare",
            "reports": f"{API_PREFIX}/reports",
            "excel": f"{API_PREFIX}/excel",
            "monitoring_events": f"{API_PREFIX}/monitoring/events",
            "monitoring_sources": f"{API_PREFIX}/monitoring/sources",
            "mmb_upload": f"{API_PREFIX}/mmb/upload",
            "health": "/health",
        },
    }
