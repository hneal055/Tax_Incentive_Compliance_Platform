"""
Organization Admin Endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, status, Request
from typing import List
import json
from datetime import datetime, timezone

from src.models.organization import (
    OrganizationResponse,
    OrganizationUpdate,
    MemberResponse,
    MemberCreate,
    MemberUpdate,
    RoleEnum
)
from src.core.auth import require_admin_role, get_current_user
from src.utils.database import prisma
from src.services.audit_log_service import audit_log_service
from prisma.models import User, Organization

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: str,
    admin_context: tuple[User, Organization] = Depends(require_admin_role)
):
    """
    Get organization details (Admin only).
    
    Requires ADMIN role in the organization.
    """
    user, user_org = admin_context
    
    # Ensure user can only access their own organization
    if user_org.id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other organizations"
        )
    
    organization = await prisma.organization.find_unique(
        where={"id": organization_id}
    )
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    return OrganizationResponse.model_validate(organization)


@router.put("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: str,
    request: OrganizationUpdate,
    req: Request,
    admin_context: tuple[User, Organization] = Depends(require_admin_role)
):
    """
    Update organization details (Admin only).
    
    Requires ADMIN role in the organization.
    """
    user, user_org = admin_context
    
    # Ensure user can only update their own organization
    if user_org.id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update other organizations"
        )
    
    # Build update data
    update_data = {}
    if request.name is not None:
        update_data["name"] = request.name
    if request.slug is not None:
        # Check if slug is already taken by another organization
        existing = await prisma.organization.find_first(
            where={
                "slug": request.slug,
                "id": {"not": organization_id}
            }
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Organization slug already in use"
            )
        update_data["slug"] = request.slug
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update fields provided"
        )
    
    update_data["updatedAt"] = datetime.now(timezone.utc)
    
    organization = await prisma.organization.update(
        where={"id": organization_id},
        data=update_data
    )
    
    # Log audit event (exclude datetime from metadata)
    metadata_for_log = {k: v for k, v in update_data.items() if k != "updatedAt"}
    if request.name is not None:
        metadata_for_log["name"] = request.name
    if request.slug is not None:
        metadata_for_log["slug"] = request.slug
    
    await audit_log_service.log_action(
        organization_id=organization_id,
        action="update_organization",
        actor_id=user.id,
        metadata=json.dumps(metadata_for_log),
        ip_address=req.client.host if req.client else None,
        user_agent=req.headers.get("user-agent")
    )
    
    return OrganizationResponse.model_validate(organization)


@router.get("/{organization_id}/members", response_model=List[MemberResponse])
async def list_organization_members(
    organization_id: str,
    admin_context: tuple[User, Organization] = Depends(require_admin_role)
):
    """
    List all members of an organization (Admin only).
    
    Requires ADMIN role in the organization.
    """
    user, user_org = admin_context
    
    # Ensure user can only access their own organization
    if user_org.id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other organizations"
        )
    
    memberships = await prisma.membership.find_many(
        where={"organizationId": organization_id},
        include={"user": True},
        order={"createdAt": "desc"}
    )
    
    # Convert to response format
    members = []
    for membership in memberships:
        member_data = {
            "id": membership.id,
            "role": membership.role,
            "userId": membership.userId,
            "organizationId": membership.organizationId,
            "createdAt": membership.createdAt,
            "updatedAt": membership.updatedAt,
            "user": {
                "id": membership.user.id,
                "email": membership.user.email,
                "name": membership.user.name
            } if membership.user else None
        }
        members.append(MemberResponse.model_validate(member_data))
    
    return members


@router.post("/{organization_id}/members", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def add_organization_member(
    organization_id: str,
    request: MemberCreate,
    req: Request,
    admin_context: tuple[User, Organization] = Depends(require_admin_role)
):
    """
    Add a member to the organization (Admin only).
    
    Requires ADMIN role in the organization.
    """
    user, user_org = admin_context
    
    # Ensure user can only modify their own organization
    if user_org.id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify other organizations"
        )
    
    # Check if user exists
    target_user = await prisma.user.find_unique(
        where={"id": request.userId}
    )
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is already a member
    existing_membership = await prisma.membership.find_first(
        where={
            "userId": request.userId,
            "organizationId": organization_id
        }
    )
    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a member of this organization"
        )
    
    # Create membership
    membership = await prisma.membership.create(
        data={
            "userId": request.userId,
            "organizationId": organization_id,
            "role": request.role.value,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc)
        },
        include={"user": True}
    )
    
    # Log audit event
    await audit_log_service.log_action(
        organization_id=organization_id,
        action="add_member",
        actor_id=user.id,
        metadata=json.dumps({
            "userId": request.userId,
            "role": request.role.value,
            "email": target_user.email
        }),
        ip_address=req.client.host if req.client else None,
        user_agent=req.headers.get("user-agent")
    )
    
    # Convert to response format
    member_data = {
        "id": membership.id,
        "role": membership.role,
        "userId": membership.userId,
        "organizationId": membership.organizationId,
        "createdAt": membership.createdAt,
        "updatedAt": membership.updatedAt,
        "user": {
            "id": membership.user.id,
            "email": membership.user.email,
            "name": membership.user.name
        } if membership.user else None
    }
    
    return MemberResponse.model_validate(member_data)


@router.put("/{organization_id}/members/{user_id}", response_model=MemberResponse)
async def update_member_role(
    organization_id: str,
    user_id: str,
    request: MemberUpdate,
    req: Request,
    admin_context: tuple[User, Organization] = Depends(require_admin_role)
):
    """
    Update a member's role in the organization (Admin only).
    
    Requires ADMIN role in the organization.
    """
    admin_user, user_org = admin_context
    
    # Ensure user can only modify their own organization
    if user_org.id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify other organizations"
        )
    
    # Find the membership
    membership = await prisma.membership.find_first(
        where={
            "userId": user_id,
            "organizationId": organization_id
        },
        include={"user": True}
    )
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found in this organization"
        )
    
    # Prevent self-demotion (admin removing their own admin role)
    if admin_user.id == user_id and request.role == RoleEnum.MEMBER:
        # Check if there are other admins
        admin_count = await prisma.membership.count(
            where={
                "organizationId": organization_id,
                "role": "ADMIN"
            }
        )
        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove your own admin role - organization must have at least one admin"
            )
    
    # Update role
    updated_membership = await prisma.membership.update(
        where={"id": membership.id},
        data={
            "role": request.role.value,
            "updatedAt": datetime.now(timezone.utc)
        },
        include={"user": True}
    )
    
    # Log audit event
    await audit_log_service.log_action(
        organization_id=organization_id,
        action="update_member_role",
        actor_id=admin_user.id,
        metadata=json.dumps({
            "userId": user_id,
            "oldRole": membership.role,
            "newRole": request.role.value,
            "email": membership.user.email if membership.user else None
        }),
        ip_address=req.client.host if req.client else None,
        user_agent=req.headers.get("user-agent")
    )
    
    # Convert to response format
    member_data = {
        "id": updated_membership.id,
        "role": updated_membership.role,
        "userId": updated_membership.userId,
        "organizationId": updated_membership.organizationId,
        "createdAt": updated_membership.createdAt,
        "updatedAt": updated_membership.updatedAt,
        "user": {
            "id": updated_membership.user.id,
            "email": updated_membership.user.email,
            "name": updated_membership.user.name
        } if updated_membership.user else None
    }
    
    return MemberResponse.model_validate(member_data)


@router.delete("/{organization_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_organization_member(
    organization_id: str,
    user_id: str,
    req: Request,
    admin_context: tuple[User, Organization] = Depends(require_admin_role)
):
    """
    Remove a member from the organization (Admin only).
    
    Requires ADMIN role in the organization.
    """
    admin_user, user_org = admin_context
    
    # Ensure user can only modify their own organization
    if user_org.id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify other organizations"
        )
    
    # Find the membership
    membership = await prisma.membership.find_first(
        where={
            "userId": user_id,
            "organizationId": organization_id
        },
        include={"user": True}
    )
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found in this organization"
        )
    
    # Prevent self-removal if last admin
    if admin_user.id == user_id:
        admin_count = await prisma.membership.count(
            where={
                "organizationId": organization_id,
                "role": "ADMIN"
            }
        )
        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove yourself - organization must have at least one admin"
            )
    
    # Store user email for audit log before deletion
    user_email = membership.user.email if membership.user else None
    
    # Delete membership
    await prisma.membership.delete(
        where={"id": membership.id}
    )
    
    # Log audit event
    await audit_log_service.log_action(
        organization_id=organization_id,
        action="remove_member",
        actor_id=admin_user.id,
        metadata=json.dumps({
            "userId": user_id,
            "role": membership.role,
            "email": user_email
        }),
        ip_address=req.client.host if req.client else None,
        user_agent=req.headers.get("user-agent")
    )
    
    return None
