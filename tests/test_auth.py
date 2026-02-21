"""
Tests for authentication module
Tests JWT and API Key authentication
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from src.core.auth import (
    get_current_user,
    get_current_organization_from_jwt,
    get_organization_from_api_key,
    get_current_organization,
    hash_api_key,
)
from src.utils.config import settings


# Mock models
class MockUser:
    def __init__(self, id, email, name):
        self.id = id
        self.email = email
        self.name = name


class MockOrganization:
    def __init__(self, id, name, slug):
        self.id = id
        self.name = name
        self.slug = slug


class MockMembership:
    def __init__(self, id, userId, organizationId, organization):
        self.id = id
        self.userId = userId
        self.organizationId = organizationId
        self.organization = organization


class MockApiKey:
    def __init__(self, id, key, organizationId, organization, lastUsedAt=None):
        self.id = id
        self.key = key
        self.organizationId = organizationId
        self.organization = organization
        self.lastUsedAt = lastUsedAt


# Helper to create JWT token
def create_test_token(user_id: str) -> str:
    """Create a test JWT token"""
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@pytest.mark.asyncio
async def test_get_current_user_success():
    """Test successful JWT authentication"""
    # Create test user and token
    user_id = "test-user-123"
    test_user = MockUser(id=user_id, email="test@example.com", name="Test User")
    token = create_test_token(user_id)
    
    # Mock database
    mock_db = MagicMock()
    mock_db.user.find_unique = AsyncMock(return_value=test_user)
    
    # Create credentials
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    
    # Test
    result = await get_current_user(credentials, mock_db)
    
    assert result == test_user
    mock_db.user.find_unique.assert_called_once_with(where={"id": user_id})


@pytest.mark.asyncio
async def test_get_current_user_missing_credentials():
    """Test JWT authentication with missing credentials"""
    mock_db = MagicMock()
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(None, mock_db)
    
    assert exc_info.value.status_code == 401
    assert "Missing authentication credentials" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    """Test JWT authentication with invalid token"""
    mock_db = MagicMock()
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid-token")
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(credentials, mock_db)
    
    assert exc_info.value.status_code == 401
    assert "Invalid token" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_user_user_not_found():
    """Test JWT authentication with valid token but user not found"""
    user_id = "nonexistent-user"
    token = create_test_token(user_id)
    
    mock_db = MagicMock()
    mock_db.user.find_unique = AsyncMock(return_value=None)
    
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(credentials, mock_db)
    
    assert exc_info.value.status_code == 401
    assert "User not found" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_organization_from_jwt_success():
    """Test getting organization from JWT authenticated user"""
    user_id = "test-user-123"
    org_id = "test-org-456"
    
    test_user = MockUser(id=user_id, email="test@example.com", name="Test User")
    test_org = MockOrganization(id=org_id, name="Test Org", slug="test-org")
    test_membership = MockMembership(
        id="membership-123",
        userId=user_id,
        organizationId=org_id,
        organization=test_org
    )
    
    mock_db = MagicMock()
    mock_db.membership.find_first = AsyncMock(return_value=test_membership)
    
    result = await get_current_organization_from_jwt(test_user, mock_db)
    
    assert result == test_org
    mock_db.membership.find_first.assert_called_once()


@pytest.mark.asyncio
async def test_get_current_organization_from_jwt_no_membership():
    """Test getting organization when user has no membership"""
    test_user = MockUser(id="test-user-123", email="test@example.com", name="Test User")
    
    mock_db = MagicMock()
    mock_db.membership.find_first = AsyncMock(return_value=None)
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_organization_from_jwt(test_user, mock_db)
    
    assert exc_info.value.status_code == 403
    assert "User not in any organization" in exc_info.value.detail


def test_hash_api_key():
    """Test API key hashing"""
    plain_key = "test-api-key-123"
    hashed = hash_api_key(plain_key)
    
    # Should be consistent
    assert hash_api_key(plain_key) == hashed
    
    # Different keys should have different hashes
    assert hash_api_key("different-key") != hashed
    
    # Should be 64 characters (SHA256 hex)
    assert len(hashed) == 64


@pytest.mark.asyncio
async def test_get_organization_from_api_key_success():
    """Test successful API key authentication"""
    plain_key = "test-api-key-123"
    hashed_key = hash_api_key(plain_key)
    
    test_org = MockOrganization(id="org-123", name="Test Org", slug="test-org")
    test_api_key = MockApiKey(
        id="key-123",
        key=hashed_key,
        organizationId="org-123",
        organization=test_org
    )
    
    mock_db = MagicMock()
    mock_db.apikey.find_first = AsyncMock(return_value=test_api_key)
    mock_db.apikey.update = AsyncMock()
    
    result = await get_organization_from_api_key(plain_key, mock_db)
    
    assert result == test_org
    mock_db.apikey.find_first.assert_called_once()
    mock_db.apikey.update.assert_called_once()


@pytest.mark.asyncio
async def test_get_organization_from_api_key_missing():
    """Test API key authentication with missing key"""
    mock_db = MagicMock()
    
    with pytest.raises(HTTPException) as exc_info:
        await get_organization_from_api_key(None, mock_db)
    
    assert exc_info.value.status_code == 401
    assert "Missing API Key" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_organization_from_api_key_invalid():
    """Test API key authentication with invalid key"""
    mock_db = MagicMock()
    mock_db.apikey.find_first = AsyncMock(return_value=None)
    
    with pytest.raises(HTTPException) as exc_info:
        await get_organization_from_api_key("invalid-key", mock_db)
    
    assert exc_info.value.status_code == 401
    assert "Invalid API Key" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_organization_with_jwt():
    """Test unified auth with JWT token"""
    user_id = "test-user-123"
    org_id = "test-org-456"
    token = create_test_token(user_id)
    
    test_user = MockUser(id=user_id, email="test@example.com", name="Test User")
    test_org = MockOrganization(id=org_id, name="Test Org", slug="test-org")
    test_membership = MockMembership(
        id="membership-123",
        userId=user_id,
        organizationId=org_id,
        organization=test_org
    )
    
    mock_db = MagicMock()
    mock_db.user.find_unique = AsyncMock(return_value=test_user)
    mock_db.membership.find_first = AsyncMock(return_value=test_membership)
    
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    
    result = await get_current_organization(credentials, None, mock_db)
    
    assert result == test_org


@pytest.mark.asyncio
async def test_get_current_organization_with_api_key():
    """Test unified auth with API key"""
    plain_key = "test-api-key-123"
    hashed_key = hash_api_key(plain_key)
    
    test_org = MockOrganization(id="org-123", name="Test Org", slug="test-org")
    test_api_key = MockApiKey(
        id="key-123",
        key=hashed_key,
        organizationId="org-123",
        organization=test_org
    )
    
    mock_db = MagicMock()
    mock_db.apikey.find_first = AsyncMock(return_value=test_api_key)
    mock_db.apikey.update = AsyncMock()
    
    result = await get_current_organization(None, plain_key, mock_db)
    
    assert result == test_org


@pytest.mark.asyncio
async def test_get_current_organization_jwt_fallback_to_api_key():
    """Test unified auth falls back to API key when JWT fails"""
    plain_key = "test-api-key-123"
    hashed_key = hash_api_key(plain_key)
    
    test_org = MockOrganization(id="org-123", name="Test Org", slug="test-org")
    test_api_key = MockApiKey(
        id="key-123",
        key=hashed_key,
        organizationId="org-123",
        organization=test_org
    )
    
    # Invalid JWT token
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid-token")
    
    mock_db = MagicMock()
    # JWT will fail, so API key should be used
    mock_db.apikey.find_first = AsyncMock(return_value=test_api_key)
    mock_db.apikey.update = AsyncMock()
    
    result = await get_current_organization(credentials, plain_key, mock_db)
    
    assert result == test_org


@pytest.mark.asyncio
async def test_get_current_organization_no_auth():
    """Test unified auth with neither JWT nor API key"""
    mock_db = MagicMock()
    
    with pytest.raises(HTTPException) as exc_info:
        await get_current_organization(None, None, mock_db)
    
    assert exc_info.value.status_code == 401
    assert "Authentication required" in exc_info.value.detail
