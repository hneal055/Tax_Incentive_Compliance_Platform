"""
Pydantic models for Monitoring System
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# MonitoringSource models
class MonitoringSourceBase(BaseModel):
    """Base monitoring source fields"""
    jurisdictionId: str = Field(..., description="ID of the jurisdiction being monitored")
    sourceType: str = Field(..., description="Type of source: rss, api, webpage")
    url: str = Field(..., description="URL of the monitoring source")
    checkInterval: int = Field(3600, description="Check interval in seconds (default: 3600)")
    active: bool = Field(True, description="Whether source is active")


class MonitoringSourceCreate(MonitoringSourceBase):
    """Model for creating a monitoring source"""
    pass


class MonitoringSourceUpdate(BaseModel):
    """Model for updating a monitoring source (all fields optional)"""
    jurisdictionId: Optional[str] = None
    sourceType: Optional[str] = None
    url: Optional[str] = None
    checkInterval: Optional[int] = None
    lastCheckedAt: Optional[datetime] = None
    lastHash: Optional[str] = None
    active: Optional[bool] = None


class MonitoringSourceResponse(MonitoringSourceBase):
    """Model for monitoring source responses"""
    id: str = Field(..., description="Unique identifier")
    lastCheckedAt: Optional[datetime] = Field(None, description="Last check timestamp")
    lastHash: Optional[str] = Field(None, description="Last content hash for change detection")
    createdAt: datetime = Field(..., description="Creation timestamp")
    updatedAt: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True


class MonitoringSourceList(BaseModel):
    """Model for list of monitoring sources"""
    total: int
    sources: list[MonitoringSourceResponse]


# MonitoringEvent models
class MonitoringEventBase(BaseModel):
    """Base monitoring event fields"""
    jurisdictionId: str = Field(..., description="ID of the jurisdiction")
    eventType: str = Field(..., description="Type: incentive_change, new_program, expiration, news")
    severity: str = Field(..., description="Severity: info, warning, critical")
    title: str = Field(..., description="Event title")
    summary: str = Field(..., description="Event summary/description")


class MonitoringEventCreate(MonitoringEventBase):
    """Model for creating a monitoring event"""
    sourceId: Optional[str] = Field(None, description="ID of the monitoring source")
    sourceUrl: Optional[str] = Field(None, description="URL of the original source")
    metadata: Optional[str] = Field(None, description="Additional metadata as JSON string")


class MonitoringEventUpdate(BaseModel):
    """Model for updating a monitoring event (all fields optional)"""
    readAt: Optional[datetime] = None
    metadata: Optional[str] = None


class MonitoringEventResponse(MonitoringEventBase):
    """Model for monitoring event responses"""
    id: str = Field(..., description="Unique identifier")
    sourceId: Optional[str] = Field(None, description="ID of the monitoring source")
    sourceUrl: Optional[str] = Field(None, description="URL of the original source")
    detectedAt: datetime = Field(..., description="When the event was detected")
    readAt: Optional[datetime] = Field(None, description="When the event was read")
    metadata: Optional[str] = Field(None, description="Additional metadata as JSON string")
    createdAt: datetime = Field(..., description="Creation timestamp")
    updatedAt: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True


class MonitoringEventList(BaseModel):
    """Model for list of monitoring events"""
    total: int
    events: list[MonitoringEventResponse]


class UnreadCountResponse(BaseModel):
    """Model for unread event count"""
    unreadCount: int = Field(..., description="Number of unread events")
