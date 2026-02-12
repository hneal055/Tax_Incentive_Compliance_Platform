"""
Test API key creation and authentication
"""
import pytest
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timezone, timedelta
from jose import jwt
from src.utils.config import settings
from src.core.auth import hash_api_key
from src.utils.database import prisma
from src.main import app
import secrets


def create_test_jwt(test_user):
    """
    Create a test JWT token for a user
    
    Args:
        test_user: User object with id attribute
        
    Returns:
        str: JWT token
    """
    payload = {
        "sub": test_user.id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


async def create_test_api_key(org_id: str) -> str:
    """
    Create a test API key for an organization
    
    Args:
        org_id: Organization ID
        
    Returns:
        str: Plaintext API key
    """
    # Generate plaintext key
    plaintext_key = secrets.token_urlsafe(48)
    hashed_key = hash_api_key(plaintext_key)
    prefix = plaintext_key[:8]
    
    # Create API key in database
    await prisma.apikey.create(
        data={
            "name": "Test API Key",
            "key": hashed_key,
            "prefix": prefix,
            "organizationId": org_id,
            "permissions": ["read", "write"],
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc),
        }
    )
    
    return plaintext_key


@pytest.fixture
async def client():
    """HTTP client for testing"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_org():
    """Create a test organization"""
    org = await prisma.organization.create(
        data={
            "name": "Test Organization",
            "slug": "test-org",
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc),
        }
    )
    yield org
    # Cleanup
    await prisma.organization.delete(where={"id": org.id})


@pytest.fixture
async def test_user(test_org):
    """Create a test user and membership"""
    user = await prisma.user.create(
        data={
            "email": "test@example.com",
            "name": "Test User",
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc),
        }
    )
    
    # Create membership
    await prisma.membership.create(
        data={
            "userId": user.id,
            "organizationId": test_org.id,
            "role": "ADMIN",
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": datetime.now(timezone.utc),
        }
    )
    
    yield user
    # Cleanup
    await prisma.user.delete(where={"id": user.id})


@pytest.mark.asyncio
async def test_create_api_key(client, test_org, test_user):
    # Authenticate
    token = create_test_jwt(test_user)
    
    response = await client.post(
        "/api/v1/api-keys",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Test Key"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "plaintext_key" in data  # Only time we see this!
    assert data["name"] == "Test Key"
    assert data["prefix"] == data["plaintext_key"][:8]


@pytest.mark.asyncio
async def test_api_key_authentication(client, test_org):
    # Create key first
    plaintext_key = await create_test_api_key(test_org.id)
    
    # Use key to authenticate
    response = await client.get(
        "/api/v1/productions",
        headers={"X-API-Key": plaintext_key}
    )
    assert response.status_code == 200
