"""
Authentication and authorization for PilotForge
Supports both JWT and API Key authentication
"""
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from jose import jwt, JWTError
from prisma import Prisma
from prisma.models import Organization, User, ApiKey
from src.utils.config import settings
from src.db import get_db
import hashlib
from datetime import datetime
from typing import Optional

security = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# ---------- JWT Auth ----------
async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Prisma = Depends(get_db),
) -> User:
    """
    Get current user from JWT token
    
    Args:
        credentials: HTTP Bearer token credentials
        db: Database connection
        
    Returns:
        User: Authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing authentication credentials")
        
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await db.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


async def get_current_organization_from_jwt(
    user: User = Depends(get_current_user),
    db: Prisma = Depends(get_db),
) -> Organization:
    """
    Get organization from JWT authenticated user
    
    Args:
        user: Authenticated user from JWT
        db: Database connection
        
    Returns:
        Organization: User's organization
        
    Raises:
        HTTPException: If user is not in any organization
    """
    membership = await db.membership.find_first(
        where={"userId": user.id},
        include={"organization": True}
    )
    if not membership:
        raise HTTPException(status_code=403, detail="User not in any organization")
    return membership.organization


# ---------- API Key Auth ----------
def hash_api_key(plain_key: str) -> str:
    """
    Hash an API key for secure storage
    
    Args:
        plain_key: Plain text API key
        
    Returns:
        str: Hashed API key
    """
    return hashlib.sha256(plain_key.encode()).hexdigest()


async def get_organization_from_api_key(
    api_key: Optional[str] = Security(api_key_header),
    db: Prisma = Depends(get_db),
) -> Organization:
    """
    Get organization from API key
    
    Args:
        api_key: API key from header
        db: Database connection
        
    Returns:
        Organization: Organization associated with API key
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API Key")
    
    hashed = hash_api_key(api_key)
    key_record = await db.apikey.find_first(
        where={"key": hashed},
        include={"organization": True}
    )
    
    if not key_record:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    # Update last used timestamp
    await db.apikey.update(
        where={"id": key_record.id},
        data={"lastUsedAt": datetime.utcnow()}
    )
    
    return key_record.organization


# ---------- Unified: try JWT first, fallback to API Key ----------
async def get_current_organization(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    api_key: Optional[str] = Security(api_key_header),
    db: Prisma = Depends(get_db),
) -> Organization:
    """
    Get organization from either JWT or API key
    Tries JWT first, then falls back to API key if JWT is not provided
    
    Args:
        credentials: HTTP Bearer token credentials (optional)
        api_key: API key from header (optional)
        db: Database connection
        
    Returns:
        Organization: Authenticated organization
        
    Raises:
        HTTPException: If neither JWT nor API key is valid
    """
    # Try JWT authentication first
    if credentials:
        try:
            user = await get_current_user(credentials, db)
            membership = await db.membership.find_first(
                where={"userId": user.id},
                include={"organization": True}
            )
            if membership:
                return membership.organization
        except HTTPException:
            # JWT failed, continue to try API key
            pass
    
    # Try API key authentication
    if api_key:
        hashed = hash_api_key(api_key)
        key_record = await db.apikey.find_first(
            where={"key": hashed},
            include={"organization": True}
        )
        
        if key_record:
            # Update last used timestamp
            await db.apikey.update(
                where={"id": key_record.id},
                data={"lastUsedAt": datetime.utcnow()}
            )
            return key_record.organization
    
    # Neither authentication method succeeded
    raise HTTPException(
        status_code=401, 
        detail="Authentication required. Provide either a valid JWT token or API key."
    )
