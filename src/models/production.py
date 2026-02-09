"""
Pydantic models for Productions
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import date, datetime


class ProductionBase(BaseModel):
    """Base production fields"""
    title: str = Field(..., description="Production title")
    productionType: str = Field(..., description="Type: feature, tv_series, commercial, documentary")
    jurisdictionId: str = Field(..., description="Jurisdiction ID where production is based")
    preferredRuleId: Optional[str] = Field(None, description="Preferred incentive rule ID for this production")
    budgetTotal: float = Field(..., description="Total production budget in USD")
    budgetQualifying: Optional[float] = Field(None, description="Qualifying budget for incentives")
    startDate: datetime = Field(..., description="Production start date")
    endDate: Optional[datetime] = Field(None, description="Production end date")
    productionCompany: str = Field(..., description="Production company name")
    status: str = Field(..., description="Status: planning, pre_production, production, post_production, completed")


class ProductionCreate(BaseModel):
    """Model for creating a production with all fields"""
    title: str = Field(..., description="Production title")
    productionType: str = Field(..., description="Type: feature, tv_series, commercial, documentary")
    jurisdictionId: str = Field(..., description="Jurisdiction ID where production is based")
    budgetTotal: float = Field(..., description="Total production budget in USD")
    budgetQualifying: Optional[float] = Field(None, description="Qualifying budget for incentives")
    startDate: date = Field(..., description="Production start date")
    endDate: Optional[date] = Field(None, description="Production end date")
    productionCompany: str = Field(..., description="Production company name")
    status: str = Field(..., description="Status: planning, pre_production, production, post_production, completed")


class ProductionQuickCreate(BaseModel):
    """Model for quick creating a production with minimal required fields"""
    title: str = Field(..., description="Production title")
    budget: float = Field(..., description="Total production budget in USD")
    jurisdictionId: Optional[str] = Field(None, description="Jurisdiction ID (auto-selects first if not provided)")
    preferredRuleId: Optional[str] = Field(None, description="Preferred incentive rule ID")
    productionType: Optional[str] = Field(None, description="Type: feature, tv_series, commercial, documentary")
    productionCompany: Optional[str] = Field(None, description="Production company name")
    startDate: Optional[date] = Field(None, description="Production start date (defaults to today)")
    status: Optional[str] = Field(None, description="Status (defaults to planning)")


class ProductionUpdate(BaseModel):
    """Model for updating a production"""
    title: Optional[str] = None
    productionType: Optional[str] = None
    jurisdictionId: Optional[str] = None
    preferredRuleId: Optional[str] = None
    budgetTotal: Optional[float] = None
    budgetQualifying: Optional[float] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    productionCompany: Optional[str] = None
    status: Optional[str] = None


class ProductionResponse(ProductionBase):
    """Model for production responses"""
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class ProductionList(BaseModel):
    """Model for list of productions response"""
    total: int
    productions: list[ProductionResponse]
