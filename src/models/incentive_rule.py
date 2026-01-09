"""
Pydantic models for Incentive Rules
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class IncentiveRuleBase(BaseModel):
    """Base incentive rule fields"""
    jurisdictionId: str = Field(..., description="Jurisdiction ID this rule belongs to")
    ruleName: str = Field(..., description="Name of the incentive rule")
    ruleCode: str = Field(..., description="Internal reference code")
    incentiveType: str = Field(..., description="Type: tax_credit, rebate, grant, exemption")
    percentage: Optional[float] = Field(None, description="Percentage rate (e.g., 25.0 for 25%)")
    minSpend: Optional[float] = Field(None, description="Minimum spend required")
    maxCredit: Optional[float] = Field(None, description="Maximum credit cap")
    eligibleExpenses: List[str] = Field(default_factory=list, description="Eligible expense categories")
    excludedExpenses: List[str] = Field(default_factory=list, description="Excluded expense categories")
    effectiveDate: datetime = Field(..., description="When rule becomes effective")
    expirationDate: Optional[datetime] = Field(None, description="When rule expires")
    requirements: Dict[str, Any] = Field(default_factory=dict, description="Additional requirements")
    active: bool = Field(default=True, description="Whether rule is active")


class IncentiveRuleCreate(IncentiveRuleBase):
    """Model for creating an incentive rule"""
    pass


class IncentiveRuleUpdate(BaseModel):
    """Model for updating an incentive rule"""
    jurisdictionId: Optional[str] = None
    ruleName: Optional[str] = None
    ruleCode: Optional[str] = None
    incentiveType: Optional[str] = None
    percentage: Optional[float] = None
    minSpend: Optional[float] = None
    maxCredit: Optional[float] = None
    eligibleExpenses: Optional[List[str]] = None
    excludedExpenses: Optional[List[str]] = None
    effectiveDate: Optional[datetime] = None
    expirationDate: Optional[datetime] = None
    requirements: Optional[Dict[str, Any]] = None
    active: Optional[bool] = None


class IncentiveRuleResponse(IncentiveRuleBase):
    """Model for incentive rule responses"""
    id: str
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True


class IncentiveRuleList(BaseModel):
    """Model for list of incentive rules"""
    total: int
    rules: List[IncentiveRuleResponse]
