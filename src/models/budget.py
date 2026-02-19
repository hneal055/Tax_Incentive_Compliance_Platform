"""
Pydantic models for Budget Management
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from enum import Enum


class ProductionType(str, Enum):
    FEATURE_FILM = "feature_film"
    TV_SERIES = "tv_series"
    COMMERCIAL = "commercial"
    DOCUMENTARY = "documentary"


class ProjectInfo(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    production_type: ProductionType
    total_budget: float = Field(..., gt=0)
    start_date: datetime
    end_date: datetime
    production_company: str
    primary_jurisdiction: str = Field(..., min_length=2, max_length=2)

    @field_validator("end_date")
    @classmethod
    def end_date_after_start(cls, v, info):
        if "start_date" in info.data and v <= info.data["start_date"]:
            raise ValueError("end_date must be after start_date")
        return v


class BudgetAccount(BaseModel):
    account_number: str
    category: str
    subcategory: Optional[str] = None
    description: str
    amount: float = Field(..., ge=0)
    eligible_for_incentives: bool = True
    notes: Optional[str] = None


class BudgetUploadRequest(BaseModel):
    project: ProjectInfo
    accounts: List[BudgetAccount] = Field(..., min_length=1)
    jurisdictions: List[str] = Field(..., min_length=1)


class BudgetResponse(BaseModel):
    budget_id: str
    status: str
    created_at: datetime
    message: str


class BudgetAccountResponse(BudgetAccount):
    id: str
    budget_id: str

    class Config:
        from_attributes = True


class BudgetDetail(BaseModel):
    budget_id: str
    project: ProjectInfo
    accounts: List[BudgetAccountResponse]
    jurisdictions: List[str]
    status: str
    created_at: datetime
    updated_at: datetime


class BudgetUpdateRequest(BaseModel):
    project: Optional[ProjectInfo] = None
    accounts: Optional[List[BudgetAccount]] = None
    jurisdictions: Optional[List[str]] = None


class BudgetListItem(BaseModel):
    budget_id: str
    title: str
    production_type: str
    total_budget: float
    primary_jurisdiction: str
    status: str
    created_at: datetime


class BudgetListResponse(BaseModel):
    total: int
    page: int
    limit: int
    budgets: List[BudgetListItem]
