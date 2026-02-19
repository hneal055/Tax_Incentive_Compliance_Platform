"""
Tax Incentive Analysis API endpoints
"""
from fastapi import APIRouter, Depends

from src.models.incentive import (
    AnalyzeRequest,
    AnalyzeResponse,
    IncentiveAnalysisResponse,
    JurisdictionIncentiveResponse,
)
from src.api.middleware.auth import verify_token
from src.services.incentive_service import incentive_service

router = APIRouter(tags=["Incentives"])


@router.post(
    "/budgets/{budget_id}/analyze",
    response_model=AnalyzeResponse,
    summary="Trigger tax incentive analysis",
)
async def analyze_budget(
    budget_id: str,
    request: AnalyzeRequest = AnalyzeRequest(),
    _token: dict = Depends(verify_token),
):
    """
    Trigger a tax incentive analysis for a budget.
    Optionally specify jurisdictions and optimization mode.
    """
    return await incentive_service.analyze_budget(
        budget_id, request.jurisdictions
    )


@router.get(
    "/budgets/{budget_id}/incentives",
    response_model=IncentiveAnalysisResponse,
    summary="Get incentive analysis results",
)
async def get_incentives(
    budget_id: str,
    _token: dict = Depends(verify_token),
):
    """
    Retrieve the latest tax incentive analysis results for a budget.
    """
    return await incentive_service.get_analysis(budget_id)


@router.get(
    "/budgets/{budget_id}/incentives/{jurisdiction}",
    response_model=JurisdictionIncentiveResponse,
    summary="Get incentive details for a specific jurisdiction",
)
async def get_jurisdiction_incentive(
    budget_id: str,
    jurisdiction: str,
    _token: dict = Depends(verify_token),
):
    """
    Get detailed incentive information for a specific jurisdiction.
    """
    return await incentive_service.get_jurisdiction_incentive(budget_id, jurisdiction)
