"""
Pydantic models for Organization management
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


# ---------- Enums ----------
class RoleEnum(str, Enum):
    """User roles within an organization"""
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


# ---------- Request Schemas ----------
class OrganizationUpdate(BaseModel):
    """Update organization metadata."""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Organization name")
    slug: Optional[str] = Field(None, min_length=1, max_length=50, description="Organization slug (URL-safe)")


class MemberCreate(BaseModel):
    """Add a member to an organization."""
    userId: str = Field(..., description="User ID to add as member")
    role: RoleEnum = Field(default=RoleEnum.MEMBER, description="Role for the new member")


class MemberUpdate(BaseModel):
    """Update member role."""
    role: RoleEnum = Field(..., description="New role for the member")


# ---------- Response Schemas ----------
class OrganizationResponse(BaseModel):
    """Organization details response."""
    id: str
    name: str
    slug: str
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


class MemberResponse(BaseModel):
    """Member details with user info."""
    id: str
    role: str
    userId: str
    organizationId: str
    createdAt: datetime
    updatedAt: datetime
    user: Optional[dict] = None  # Will include user details (id, email, name)

    model_config = {"from_attributes": True}
