"""
API Key Management Endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, status, Request
from typing import List, Optional
import secrets
import json
from datetime import datetime, timezone, timedelta

from src.models.api_key import (
    ApiKeyCreate,
    ApiKeyUpdate,
    ApiKeyResponse,
    ApiKeyCreatedResponse,
    ApiKeyWithPrefix,
    get_key_prefix
)
from src.models.webhook_config import WebhookConfigCreate, WebhookConfigUpdate, WebhookConfigResponse
from src.models.audit_log import AuditLogResponse
from src.models.usage_analytics import UsageAnalytics
from src.core.auth import hash_api_key, get_current_organization_from_jwt
from src.utils.database import prisma
from src.services.audit_log_service import audit_log_service
from src.services.webhook_service import webhook_service
from src.services.usage_analytics_service import usage_analytics_service

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
    req: Request,
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
    
    # Validate permissions
    valid_permissions = {"read", "write", "admin"}
    if not all(p in valid_permissions for p in request.permissions):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid permissions. Valid values: {valid_permissions}"
        )
    
    # Create API key record
    api_key = await prisma.apikey.create(
        data={
            "name": request.name,
            "key": hashed_key,
            "prefix": prefix,
            "organizationId": organization.id,
            "permissions": request.permissions,
            "expiresAt": request.expiresAt,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc),
        }
    )
    
    # Log audit event
    await audit_log_service.log_action(
        organization_id=organization.id,
        action="create",
        api_key_id=api_key.id,
        metadata=json.dumps({"name": request.name, "permissions": request.permissions}),
        ip_address=req.client.host if req.client else None,
        user_agent=req.headers.get("user-agent")
    )
    
    # Send webhook notification
    await webhook_service.notify_key_created(
        organization_id=organization.id,
        api_key_id=api_key.id,
        api_key_name=api_key.name
    )
    
    # Return with plaintext key (only time it's shown!)
    return ApiKeyCreatedResponse(
        id=api_key.id,
        name=api_key.name,
        organizationId=api_key.organizationId,
        permissions=api_key.permissions,
        prefix=api_key.prefix,
        lastUsedAt=api_key.lastUsedAt,
        expiresAt=api_key.expiresAt,
        createdAt=api_key.createdAt,
        updatedAt=api_key.updatedAt,
        plaintext_key=plaintext_key
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
            permissions=key.permissions,
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
        permissions=api_key.permissions,
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
    req: Request,
    organization = Depends(get_current_organization_from_jwt)
):
    """
    Update API key metadata (name and permissions).
    
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
    
    # Validate permissions if provided
    if request.permissions:
        valid_permissions = {"read", "write", "admin"}
        if not all(p in valid_permissions for p in request.permissions):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid permissions. Valid values: {valid_permissions}"
            )
    
    # Update fields if provided
    update_data = {}
    if request.name is not None:
        update_data["name"] = request.name
    if request.permissions is not None:
        update_data["permissions"] = request.permissions
    update_data["updatedAt"] = datetime.now(timezone.utc)
    
    updated_key = await prisma.apikey.update(
        where={"id": key_id},
        data=update_data
    )
    
    # Log audit event
    await audit_log_service.log_action(
        organization_id=organization.id,
        action="update",
        api_key_id=key_id,
        metadata=json.dumps(update_data),
        ip_address=req.client.host if req.client else None,
        user_agent=req.headers.get("user-agent")
    )
    
    return ApiKeyWithPrefix(
        id=updated_key.id,
        name=updated_key.name,
        organizationId=updated_key.organizationId,
        permissions=updated_key.permissions,
        prefix=updated_key.prefix,
        lastUsedAt=updated_key.lastUsedAt,
        expiresAt=updated_key.expiresAt,
        createdAt=updated_key.createdAt,
        updatedAt=updated_key.updatedAt
    )


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    key_id: str,
    req: Request,
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
    
    # Log audit event before deletion
    await audit_log_service.log_action(
        organization_id=organization.id,
        action="delete",
        api_key_id=key_id,
        metadata=json.dumps({"name": api_key.name}),
        ip_address=req.client.host if req.client else None,
        user_agent=req.headers.get("user-agent")
    )
    
    # Send webhook notification
    await webhook_service.notify_key_revoked(
        organization_id=organization.id,
        api_key_id=api_key.id,
        api_key_name=api_key.name
    )
    
    # Delete the key
    await prisma.apikey.delete(where={"id": key_id})
    
    return None


# ============================================================================
# BULK OPERATIONS
# ============================================================================

@router.post("/bulk/revoke-expired", status_code=status.HTTP_200_OK)
async def bulk_revoke_expired_keys(
    req: Request,
    organization = Depends(get_current_organization_from_jwt)
):
    """
    Bulk revoke all expired API keys for the organization.
    
    Returns the number of keys revoked.
    """
    # Find all expired keys
    now = datetime.now(timezone.utc)
    expired_keys = await prisma.apikey.find_many(
        where={
            "organizationId": organization.id,
            "expiresAt": {
                "lte": now
            }
        }
    )
    
    revoked_count = len(expired_keys)
    
    if revoked_count == 0:
        return {
            "message": "No expired API keys found",
            "count": 0
        }
    
    # Collect key IDs for bulk delete
    key_ids = [key.id for key in expired_keys]
    key_info = [{" name": key.name} for key in expired_keys]
    
    # Bulk delete expired keys
    await prisma.apikey.delete_many(
        where={
            "id": {"in": key_ids}
        }
    )
    
    # Batch audit logging
    await audit_log_service.log_action(
        organization_id=organization.id,
        action="bulk_revoke",
        metadata=json.dumps({"count": revoked_count, "keys": key_info}),
        ip_address=req.client.host if req.client else None,
        user_agent=req.headers.get("user-agent")
    )
    
    # Send webhook notifications for each key (async, non-blocking)
    for key in expired_keys:
        await webhook_service.notify_key_expired(
            organization_id=organization.id,
            api_key_id=key.id,
            api_key_name=key.name
        )
    
    return {
        "message": f"Successfully revoked {revoked_count} expired API key(s)",
        "count": revoked_count
    }


# ============================================================================
# AUDIT LOGS
# ============================================================================

@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    organization = Depends(get_current_organization_from_jwt),
    action: Optional[str] = None,
    limit: int = 100
):
    """
    Get audit logs for the organization's API keys.
    
    Optionally filter by action type.
    """
    logs = await audit_log_service.get_logs(
        organization_id=organization.id,
        action=action,
        limit=limit
    )
    
    return [
        AuditLogResponse(
            id=log.id,
            apiKeyId=log.apiKeyId,
            organizationId=log.organizationId,
            action=log.action,
            actorId=log.actorId,
            metadata=log.metadata,
            ipAddress=log.ipAddress,
            userAgent=log.userAgent,
            timestamp=log.timestamp
        )
        for log in logs
    ]


@router.get("/{key_id}/audit-logs", response_model=List[AuditLogResponse])
async def get_api_key_audit_logs(
    key_id: str,
    organization = Depends(get_current_organization_from_jwt),
    limit: int = 100
):
    """
    Get audit logs for a specific API key.
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
    
    logs = await audit_log_service.get_logs(
        organization_id=organization.id,
        api_key_id=key_id,
        limit=limit
    )
    
    return [
        AuditLogResponse(
            id=log.id,
            apiKeyId=log.apiKeyId,
            organizationId=log.organizationId,
            action=log.action,
            actorId=log.actorId,
            metadata=log.metadata,
            ipAddress=log.ipAddress,
            userAgent=log.userAgent,
            timestamp=log.timestamp
        )
        for log in logs
    ]


# ============================================================================
# USAGE ANALYTICS
# ============================================================================

@router.get("/{key_id}/analytics", response_model=UsageAnalytics)
async def get_api_key_analytics(
    key_id: str,
    organization = Depends(get_current_organization_from_jwt),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Get usage analytics for a specific API key.
    
    Optionally filter by date range (defaults to last 30 days).
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
    
    analytics = await usage_analytics_service.get_analytics(
        api_key_id=key_id,
        start_date=start_date,
        end_date=end_date
    )
    
    return UsageAnalytics(**analytics)


# ============================================================================
# WEBHOOK CONFIGURATION
# ============================================================================

@router.post("/webhooks", response_model=WebhookConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_webhook_config(
    request: WebhookConfigCreate,
    organization = Depends(get_current_organization_from_jwt)
):
    """
    Create a webhook configuration for API key events.
    
    Events: api_key_expiring, api_key_expired, api_key_created, api_key_revoked
    """
    valid_events = {"api_key_expiring", "api_key_expired", "api_key_created", "api_key_revoked"}
    if not all(e in valid_events for e in request.events):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid events. Valid values: {valid_events}"
        )
    
    webhook = await prisma.webhookconfig.create(
        data={
            "organizationId": organization.id,
            "url": request.url,
            "events": request.events,
            "secret": request.secret,
            "active": True,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc)
        }
    )
    
    return WebhookConfigResponse(
        id=webhook.id,
        organizationId=webhook.organizationId,
        url=webhook.url,
        events=webhook.events,
        active=webhook.active,
        createdAt=webhook.createdAt,
        updatedAt=webhook.updatedAt
    )


@router.get("/webhooks", response_model=List[WebhookConfigResponse])
async def list_webhook_configs(
    organization = Depends(get_current_organization_from_jwt)
):
    """
    List all webhook configurations for the organization.
    """
    webhooks = await prisma.webhookconfig.find_many(
        where={"organizationId": organization.id},
        order={"createdAt": "desc"}
    )
    
    return [
        WebhookConfigResponse(
            id=w.id,
            organizationId=w.organizationId,
            url=w.url,
            events=w.events,
            active=w.active,
            createdAt=w.createdAt,
            updatedAt=w.updatedAt
        )
        for w in webhooks
    ]


@router.patch("/webhooks/{webhook_id}", response_model=WebhookConfigResponse)
async def update_webhook_config(
    webhook_id: str,
    request: WebhookConfigUpdate,
    organization = Depends(get_current_organization_from_jwt)
):
    """
    Update a webhook configuration.
    """
    # Verify webhook exists and belongs to organization
    webhook = await prisma.webhookconfig.find_first(
        where={
            "id": webhook_id,
            "organizationId": organization.id
        }
    )
    
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook configuration not found"
        )
    
    # Validate events if provided
    if request.events:
        valid_events = {"api_key_expiring", "api_key_expired", "api_key_created", "api_key_revoked"}
        if not all(e in valid_events for e in request.events):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid events. Valid values: {valid_events}"
            )
    
    # Update fields
    update_data = {}
    if request.url is not None:
        update_data["url"] = request.url
    if request.events is not None:
        update_data["events"] = request.events
    if request.secret is not None:
        update_data["secret"] = request.secret
    if request.active is not None:
        update_data["active"] = request.active
    update_data["updatedAt"] = datetime.now(timezone.utc)
    
    updated_webhook = await prisma.webhookconfig.update(
        where={"id": webhook_id},
        data=update_data
    )
    
    return WebhookConfigResponse(
        id=updated_webhook.id,
        organizationId=updated_webhook.organizationId,
        url=updated_webhook.url,
        events=updated_webhook.events,
        active=updated_webhook.active,
        createdAt=updated_webhook.createdAt,
        updatedAt=updated_webhook.updatedAt
    )


@router.delete("/webhooks/{webhook_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_webhook_config(
    webhook_id: str,
    organization = Depends(get_current_organization_from_jwt)
):
    """
    Delete a webhook configuration.
    """
    # Verify webhook exists and belongs to organization
    webhook = await prisma.webhookconfig.find_first(
        where={
            "id": webhook_id,
            "organizationId": organization.id
        }
    )
    
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook configuration not found"
        )
    
    await prisma.webhookconfig.delete(where={"id": webhook_id})
    
    return None
