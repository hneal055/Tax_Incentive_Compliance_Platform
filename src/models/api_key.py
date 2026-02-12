"""
Pydantic models for API Key management
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ---------- Request Schemas ----------
class ApiKeyCreate(BaseModel):
    """Create a new API key - only name is required."""
    name: str = Field(..., min_length=1, max_length=100, description="Human-readable key name")
    expiresAt: Optional[datetime] = Field(None, description="Optional expiration date")
    permissions: list[str] = Field(default=["read", "write"], description="API key permissions (read, write, admin)")


class ApiKeyUpdate(BaseModel):
    """Update API key metadata (currently just name)."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    permissions: Optional[list[str]] = Field(None, description="Update permissions")


class ApiKeyExpire(BaseModel):
    """Set or update expiration."""
    expiresAt: Optional[datetime] = None  # None = never expires


# ---------- Response Schemas ----------
class ApiKeyResponse(BaseModel):
    """Full API key details (safe to return - no key value)."""
    id: str
    name: str
    organizationId: str
    permissions: list[str]
    lastUsedAt: Optional[datetime]
    expiresAt: Optional[datetime]
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}


class ApiKeyWithPrefix(ApiKeyResponse):
    """Adds the first 8 chars of the key for UI identification."""
    prefix: str  # First 8 chars of the original key


class ApiKeyCreatedResponse(ApiKeyWithPrefix):
    """Response when creating a new key - INCLUDES the plaintext key."""
    plaintextKey: str = Field(..., description="Store this immediately - it won't be shown again!")


# ---------- Internal Helper ----------
def get_key_prefix(plaintext_key: str) -> str:
    """
    Extract first 8 chars from a plaintext key (for display only).
    
    Args:
        plaintext_key: The original plaintext API key
        
    Returns:
        str: First 8 characters of the key for UI display
        
    Note:
        This should be called before hashing the key and the prefix
        should be stored separately in the database for later display.
    """
    if not plaintext_key:
        return ""
    return plaintext_key[:8]
