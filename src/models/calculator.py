"""
Pydantic models for Tax Credit Calculator
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import date


class SimpleCalculateRequest(BaseModel):
    """Request for simple tax credit calculation"""
    productionBudget: float = Field(..., description="Total production budget in USD", gt=0)
    jurisdictionId: str = Field(..., description="Jurisdiction ID")
    ruleId: str = Field(..., description="Incentive rule ID to apply")
    qualifyingBudget: Optional[float] = Field(None, description="Override qualifying budget (if different from total)")


class SimpleCalculateResponse(BaseModel):
    """Response for simple calculation"""
    jurisdiction: str = Field(..., description="Jurisdiction name")
    ruleName: str = Field(..., description="Incentive rule name")
    ruleCode: str = Field(..., description="Rule code")
    incentiveType: str = Field(..., description="Type of incentive")
    
    # Budget info
    totalBudget: float = Field(..., description="Total production budget")
    qualifyingBudget: float = Field(..., description="Budget that qualifies for incentive")
    
    # Rate info
    percentage: Optional[float] = Field(None, description="Incentive percentage rate")
    
    # Calculated amounts
    estimatedCredit: float = Field(..., description="Estimated tax credit/rebate amount")
    
    # Requirements check
    meetsMinimumSpend: bool = Field(..., description="Whether production meets minimum spend requirement")
    minimumSpendRequired: Optional[float] = Field(None, description="Minimum spend requirement")
    underMaximumCap: bool = Field(..., description="Whether credit is under maximum cap")
    maximumCapAmount: Optional[float] = Field(None, description="Maximum cap amount")
    
    # Additional info
    requirements: Dict[str, Any] = Field(default_factory=dict, description="Additional requirements")
    notes: List[str] = Field(default_factory=list, description="Calculation notes and warnings")


class CompareCalculateRequest(BaseModel):
    """Request for comparing multiple jurisdictions"""
    productionBudget: float = Field(..., description="Total production budget in USD", gt=0)
    jurisdictionIds: List[str] = Field(..., description="List of jurisdiction IDs to compare", min_items=2, max_items=10)
    qualifyingBudget: Optional[float] = Field(None, description="Override qualifying budget")


class ComparisonResult(BaseModel):
    """Single jurisdiction comparison result"""
    jurisdiction: str
    jurisdictionId: str
    ruleName: str
    ruleCode: str
    incentiveType: str
    percentage: Optional[float]
    estimatedCredit: float
    meetsRequirements: bool
    rank: int
    savings: float


class CompareCalculateResponse(BaseModel):
    """Response for comparison calculation"""
    totalBudget: float
    comparisons: List[ComparisonResult]
    bestOption: ComparisonResult
    savingsVsWorst: float
    notes: List[str] = Field(default_factory=list)
