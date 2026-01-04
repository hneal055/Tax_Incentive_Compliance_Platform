"""Main API router"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def api_root():
    return {
        "message": "Tax-Incentive Compliance Platform API",
        "endpoints": {
            "jurisdictions": "/api/v1/jurisdictions",
            "incentive_rules": "/api/v1/incentive-rules",
            "productions": "/api/v1/productions",
            "expenses": "/api/v1/expenses",
            "calculations": "/api/v1/calculations"
        }
    }
