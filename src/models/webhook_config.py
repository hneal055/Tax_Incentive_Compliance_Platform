"""
Pydantic models for Webhook Configuration
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class WebhookConfigCreate(BaseModel):
    """Create a webhook configuration"""
    url: str = Field(..., description="Webhook endpoint URL")
    events: list[str] = Field(..., description="Events to trigger: api_key_expiring, api_key_expired, api_key_created, api_key_revoked")
    secret: Optional[str] = Field(None, description="Secret for webhook signature verification")


class WebhookConfigUpdate(BaseModel):
    """Update webhook configuration"""
    url: Optional[str] = None
    events: Optional[list[str]] = None
    secret: Optional[str] = None
    active: Optional[bool] = None


class WebhookConfigResponse(BaseModel):
    """Webhook configuration response"""
    id: str
    organizationId: str
    url: str
    events: list[str]
    active: bool
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}
