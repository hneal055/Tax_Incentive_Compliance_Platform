"""
Example usage of authentication in FastAPI routes

This file demonstrates how to use the authentication system
with both JWT and API Key authentication.
"""
from fastapi import APIRouter, Depends
from prisma.models import Organization, User
from src.core.auth import (
    get_current_user,
    get_current_organization_from_jwt,
    get_organization_from_api_key,
    get_current_organization,
)

router = APIRouter(prefix="/example", tags=["Example Auth"])


@router.get("/jwt-protected")
async def jwt_protected_route(user: User = Depends(get_current_user)):
    """
    Example of a route protected by JWT authentication only
    """
    return {
        "message": "JWT authentication successful",
        "user_id": user.id,
        "user_email": user.email,
    }


@router.get("/jwt-org-protected")
async def jwt_org_protected_route(
    org: Organization = Depends(get_current_organization_from_jwt)
):
    """
    Example of a route that requires JWT auth and returns organization
    """
    return {
        "message": "JWT organization authentication successful",
        "organization_id": org.id,
        "organization_name": org.name,
    }


@router.get("/api-key-protected")
async def api_key_protected_route(
    org: Organization = Depends(get_organization_from_api_key)
):
    """
    Example of a route protected by API Key authentication only
    """
    return {
        "message": "API Key authentication successful",
        "organization_id": org.id,
        "organization_name": org.name,
    }


@router.get("/unified-protected")
async def unified_protected_route(
    org: Organization = Depends(get_current_organization)
):
    """
    Example of a route that accepts either JWT or API Key authentication
    JWT is tried first, then falls back to API Key
    """
    return {
        "message": "Unified authentication successful",
        "organization_id": org.id,
        "organization_name": org.name,
    }
