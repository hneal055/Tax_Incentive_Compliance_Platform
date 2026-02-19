"""
Pydantic models for Tax Incentive Analysis
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class OptimizationMode(str, Enum):
    MAXIMUM_BENEFIT = "maximum_benefit"
    FASTEST_PROCESSING = "fastest_processing"
    MOST_FLEXIBLE = "most_flexible"


class AnalyzeRequest(BaseModel):
    jurisdictions: Optional[List[str]] = None
    optimization_mode: OptimizationMode = OptimizationMode.MAXIMUM_BENEFIT


class AnalyzeResponse(BaseModel):
    analysis_id: str
    budget_id: str
    status: str
    estimated_completion: datetime


class IncentiveDeadline(BaseModel):
    type: str
    date: datetime
    description: str


class IncentiveProgram(BaseModel):
    jurisdiction: str
    program_name: str
    eligible_spend: float
    credit_rate: float
    estimated_benefit: float
    eligibility_status: str
    requirements: List[str]
    deadlines: List[IncentiveDeadline]


class IncentiveRecommendation(BaseModel):
    type: str
    description: str
    potential_additional_benefit: float


class IncentiveAnalysisResponse(BaseModel):
    budget_id: str
    analysis_date: datetime
    total_estimated_benefit: float
    incentives: List[IncentiveProgram]
    recommendations: List[IncentiveRecommendation]


class JurisdictionIncentiveResponse(BaseModel):
    budget_id: str
    jurisdiction: str
    analysis_date: datetime
    incentive: Optional[IncentiveProgram] = None
    message: Optional[str] = None
