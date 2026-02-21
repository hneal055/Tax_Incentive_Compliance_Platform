"""
Pydantic models for Audit Log
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AuditLogCreate(BaseModel):
    """Create an audit log entry"""
    apiKeyId: Optional[str] = None
    organizationId: str
    action: str = Field(..., description="Action performed: create, delete, rotate, revoke, update")
    actorId: Optional[str] = None
    metadata: Optional[str] = None
    ipAddress: Optional[str] = None
    userAgent: Optional[str] = None


class AuditLogResponse(BaseModel):
    """Audit log response"""
    id: str
    apiKeyId: Optional[str]
    organizationId: str
    action: str
    actorId: Optional[str]
    metadata: Optional[str]
    ipAddress: Optional[str]
    userAgent: Optional[str]
    timestamp: datetime

    model_config = {"from_attributes": True}
