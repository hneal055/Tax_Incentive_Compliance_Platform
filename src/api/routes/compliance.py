"""
Compliance Monitoring API endpoints
"""
from fastapi import APIRouter, Depends

from src.models.compliance import (
    ComplianceStatusResponse,
    ComplianceAlertsResponse,
)
from src.api.middleware.auth import verify_token
from src.services.compliance_service import compliance_service

router = APIRouter(tags=["Compliance"])


@router.get(
    "/budgets/{budget_id}/compliance",
    response_model=ComplianceStatusResponse,
    summary="Get compliance status for all jurisdictions",
)
async def get_compliance(
    budget_id: str,
    _token: dict = Depends(verify_token),
):
    """
    Check compliance status for all applicable jurisdictions.
    """
    return await compliance_service.check_compliance(budget_id)


@router.post(
    "/budgets/{budget_id}/compliance/check",
    response_model=ComplianceStatusResponse,
    summary="Trigger immediate compliance check",
)
async def trigger_compliance_check(
    budget_id: str,
    _token: dict = Depends(verify_token),
):
    """
    Trigger an immediate compliance check and return updated status.
    """
    return await compliance_service.check_compliance(budget_id)


@router.get(
    "/budgets/{budget_id}/compliance/alerts",
    response_model=ComplianceAlertsResponse,
    summary="Get active compliance alerts",
)
async def get_compliance_alerts(
    budget_id: str,
    _token: dict = Depends(verify_token),
):
    """
    Get active compliance alerts and time-sensitive items.
    """
    return await compliance_service.get_compliance_alerts(budget_id)
