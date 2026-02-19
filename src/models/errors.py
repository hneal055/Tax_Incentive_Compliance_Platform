"""
Error models for consistent API error responses
"""
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[dict] = None


class BudgetNotFoundError(HTTPException):
    def __init__(self, budget_id: str):
        super().__init__(
            status_code=404,
            detail=f"Budget with id {budget_id} not found"
        )


class InvalidBudgetDataError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=400,
            detail=f"Invalid budget data: {message}"
        )


class AnalysisNotFoundError(HTTPException):
    def __init__(self, budget_id: str):
        super().__init__(
            status_code=404,
            detail=f"No incentive analysis found for budget {budget_id}"
        )


class UnauthorizedError(HTTPException):
    def __init__(self, detail: str = "Invalid authentication credentials"):
        super().__init__(
            status_code=401,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )
