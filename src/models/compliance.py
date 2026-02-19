"""
Pydantic models for Compliance Monitoring
"""
from pydantic import BaseModel
from typing import List
from datetime import datetime


class ComplianceRequirement(BaseModel):
    requirement: str
    due_date: datetime
    status: str


class JurisdictionCompliance(BaseModel):
    jurisdiction: str
    status: str
    requirements_met: int
    requirements_total: int
    pending_requirements: List[ComplianceRequirement]
    alerts: List[str]


class ComplianceStatusResponse(BaseModel):
    budget_id: str
    overall_status: str
    last_checked: datetime
    jurisdictions: List[JurisdictionCompliance]


class ComplianceAlert(BaseModel):
    budget_id: str
    jurisdiction: str
    alert_type: str
    message: str
    due_date: datetime
    severity: str


class ComplianceAlertsResponse(BaseModel):
    budget_id: str
    alerts: List[ComplianceAlert]
    total: int
