"""
Pydantic models for API Key Usage Analytics
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ApiKeyUsageCreate(BaseModel):
    """Create a usage record"""
    apiKeyId: str
    endpoint: str
    method: str
    statusCode: int
    responseTime: int  # milliseconds


class ApiKeyUsageResponse(BaseModel):
    """Usage record response"""
    id: str
    apiKeyId: str
    endpoint: str
    method: str
    statusCode: int
    responseTime: int
    timestamp: datetime

    model_config = {"from_attributes": True}


class UsageAnalytics(BaseModel):
    """Aggregated usage analytics"""
    totalRequests: int
    successfulRequests: int
    failedRequests: int
    averageResponseTime: float
    requestsByEndpoint: dict[str, int]
    requestsByMethod: dict[str, int]
    recentActivity: list[ApiKeyUsageResponse]
