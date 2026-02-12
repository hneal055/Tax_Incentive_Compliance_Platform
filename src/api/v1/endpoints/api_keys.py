"""
API Key Management Endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
import secrets
from datetime import datetime, timezone

from src.models.api_key import (
    ApiKeyCreate,
    ApiKeyUpdate,
    ApiKeyResponse,
    ApiKeyCreatedResponse,
    ApiKeyWithPrefix,
    get_key_prefix
)
from src.core.auth import hash_api_key, get_current_organization_from_jwt
from src.utils.database import prisma

router = APIRouter(prefix="/api-keys", tags=["API Keys"])


def generate_api_key() -> str:
    """
    Generate a secure random API key
    
    Returns:
        str: Random API key (64 characters)
    """
    return secrets.token_urlsafe(48)  # generates ~64 chars


@router.post("/", response_model=ApiKeyCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    request: ApiKeyCreate,
    organization = Depends(get_current_organization_from_jwt)
):
    """
    Create a new API key for the current user's organization.
    
    **IMPORTANT**: The plaintext key is only shown once - store it securely!
    """
    # Generate plaintext key
    plaintext_key = generate_api_key()
    hashed_key = hash_api_key(plaintext_key)
    prefix = get_key_prefix(plaintext_key)
    
    # Create API key record
    api_key = await prisma.apikey.create(
        data={
            "name": request.name,
            "key": hashed_key,
            "prefix": prefix,
            "organizationId": organization.id,
            "expiresAt": request.expiresAt,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc),
        }
    )
    
    # Return with plaintext key (only time it's shown!)
    return ApiKeyCreatedResponse(
        id=api_key.id,
        name=api_key.name,
        organizationId=api_key.organizationId,
        prefix=api_key.prefix,
        lastUsedAt=api_key.lastUsedAt,
        expiresAt=api_key.expiresAt,
        createdAt=api_key.createdAt,
        updatedAt=api_key.updatedAt,
        plaintextKey=plaintext_key
    )


@router.get("/", response_model=List[ApiKeyWithPrefix])
async def list_api_keys(
    organization = Depends(get_current_organization_from_jwt)
):
    """
    List all API keys for the current user's organization.
    
    Shows key prefix for identification but not the full key.
    """
    api_keys = await prisma.apikey.find_many(
        where={"organizationId": organization.id},
        order={"createdAt": "desc"}
    )
    
    return [
        ApiKeyWithPrefix(
            id=key.id,
            name=key.name,
            organizationId=key.organizationId,
            prefix=key.prefix,
            lastUsedAt=key.lastUsedAt,
            expiresAt=key.expiresAt,
            createdAt=key.createdAt,
            updatedAt=key.updatedAt
        )
        for key in api_keys
    ]


@router.get("/{key_id}", response_model=ApiKeyWithPrefix)
async def get_api_key(
    key_id: str,
    organization = Depends(get_current_organization_from_jwt)
):
    """
    Get details of a specific API key.
    
    Shows key prefix but not the full key.
    """
    api_key = await prisma.apikey.find_first(
        where={
            "id": key_id,
            "organizationId": organization.id
        }
    )
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    return ApiKeyWithPrefix(
        id=api_key.id,
        name=api_key.name,
        organizationId=api_key.organizationId,
        prefix=api_key.prefix,
        lastUsedAt=api_key.lastUsedAt,
        expiresAt=api_key.expiresAt,
        createdAt=api_key.createdAt,
        updatedAt=api_key.updatedAt
    )


@router.patch("/{key_id}", response_model=ApiKeyWithPrefix)
async def update_api_key(
    key_id: str,
    request: ApiKeyUpdate,
    organization = Depends(get_current_organization_from_jwt)
):
    """
    Update API key metadata (name).
    
    The actual key value cannot be changed - delete and create a new one instead.
    """
    # Verify key exists and belongs to user's organization
    api_key = await prisma.apikey.find_first(
        where={
            "id": key_id,
            "organizationId": organization.id
        }
    )
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    # Update name if provided
    update_data = {}
    if request.name is not None:
        update_data["name"] = request.name
    update_data["updatedAt"] = datetime.now(timezone.utc)
    
    updated_key = await prisma.apikey.update(
        where={"id": key_id},
        data=update_data
    )
    
    return ApiKeyWithPrefix(
        id=updated_key.id,
        name=updated_key.name,
        organizationId=updated_key.organizationId,
        prefix=updated_key.prefix,
        lastUsedAt=updated_key.lastUsedAt,
        expiresAt=updated_key.expiresAt,
        createdAt=updated_key.createdAt,
        updatedAt=updated_key.updatedAt
    )


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    key_id: str,
    organization = Depends(get_current_organization_from_jwt)
):
    """
    Delete (revoke) an API key.
    
    This is permanent and cannot be undone.
    """
    # Verify key exists and belongs to user's organization
    api_key = await prisma.apikey.find_first(
        where={
            "id": key_id,
            "organizationId": organization.id
        }
    )
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    # Delete the key
    await prisma.apikey.delete(where={"id": key_id})
    
    return None
