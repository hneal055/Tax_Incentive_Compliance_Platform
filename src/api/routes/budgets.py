"""
Budget management API endpoints
"""
from fastapi import APIRouter, Depends, status
from typing import Optional

from src.models.budget import (
    BudgetUploadRequest,
    BudgetResponse,
    BudgetDetail,
    BudgetListResponse,
    BudgetUpdateRequest,
)
from src.api.middleware.auth import verify_token
from src.services.budget_service import budget_service

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.post(
    "/",
    response_model=BudgetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload budget data from MMB Connector",
)
async def create_budget(
    budget_data: BudgetUploadRequest,
    _token: dict = Depends(verify_token),
):
    """
    Accept transformed budget data from the MMB Connector.
    Creates budget with project info and line-item accounts.
    """
    return await budget_service.create_budget(budget_data)


@router.get(
    "/",
    response_model=BudgetListResponse,
    summary="List all budgets with pagination",
)
async def list_budgets(
    page: int = 1,
    limit: int = 20,
    production_type: Optional[str] = None,
    jurisdiction: Optional[str] = None,
    _token: dict = Depends(verify_token),
):
    """
    List budgets with optional filtering by production type and jurisdiction.
    """
    return await budget_service.list_budgets(
        page=page,
        limit=limit,
        production_type=production_type,
        jurisdiction=jurisdiction,
    )


@router.get(
    "/{budget_id}",
    response_model=BudgetDetail,
    summary="Get budget details",
)
async def get_budget(
    budget_id: str,
    _token: dict = Depends(verify_token),
):
    """
    Retrieve detailed budget information including all accounts and metadata.
    """
    return await budget_service.get_budget(budget_id)


@router.put(
    "/{budget_id}",
    response_model=BudgetDetail,
    summary="Update budget (bidirectional sync)",
)
async def update_budget(
    budget_id: str,
    updates: BudgetUpdateRequest,
    _token: dict = Depends(verify_token),
):
    """
    Update an existing budget. Used for bidirectional sync with MMB Connector.
    All fields are optional.
    """
    return await budget_service.update_budget(budget_id, updates)


@router.delete(
    "/{budget_id}",
    status_code=status.HTTP_200_OK,
    summary="Soft-delete a budget",
)
async def delete_budget(
    budget_id: str,
    _token: dict = Depends(verify_token),
):
    """
    Soft-delete a budget by setting its status to 'deleted'.
    """
    await budget_service.delete_budget(budget_id)
    return {"message": f"Budget {budget_id} deleted successfully"}
