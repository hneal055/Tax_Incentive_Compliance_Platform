"""
Pydantic models for Productions
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime, date


class ProductionBase(BaseModel):
    """Base production fields"""
    title: str = Field(..., description="Production title")
    productionType: str = Field(..., description="Type: feature, tv_series, commercial, documentary")
    jurisdictionId: str = Field(..., description="Jurisdiction ID where production is based")
    budgetTotal: float = Field(..., description="Total production budget in USD")
    budgetQualifying: Optional[float] = Field(None, description="Qualifying budget for incentives")
    startDate: date = Field(..., description="Production start date")
    endDate: Optional[date] = Field(None, description="Production end date")
    wrapDate: Optional[date] = Field(None, description="Production wrap date")
    productionCompany: str = Field(..., description="Production company name")
    accountant: Optional[str] = Field(None, description="Production accountant name")
    contact: Optional[Dict[str, Any]] = Field(None, description="Contact information")
    status: str = Field(..., description="Status: planning, pre_production, production, post_production, completed")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ProductionCreate(ProductionBase):
    """Model for creating a production"""
    pass


class ProductionUpdate(BaseModel):
    """Model for updating a production"""
    title: Optional[str] = None
    productionType: Optional[str] = None
    jurisdictionId: Optional[str] = None
    budgetTotal: Optional[float] = None
    budgetQualifying: Optional[float] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    wrapDate: Optional[date] = None
    productionCompany: Optional[str] = None
    accountant: Optional[str] = None
    contact: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ProductionResponse(ProductionBase):
    """Model for production responses"""
    id: str
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True


class ProductionList(BaseModel):
    """Model for list of productions"""
    total: int
    productions: List[ProductionResponse]
