"""
Test API key creation and authentication
"""
import pytest
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from jose import jwt
from src.utils.config import settings
from src.core.auth import hash_api_key
import secrets


class MockUser:
    """Mock user object for testing"""
    def __init__(self, id="test-user-id", email="test@example.com", name="Test User"):
        self.id = id
        self.email = email
        self.name = name


class MockOrg:
    """Mock organization object for testing"""
    def __init__(self, id="test-org-id", name="Test Organization", slug="test-org"):
        self.id = id
        self.name = name
        self.slug = slug


class MockMembership:
    """Mock membership object for testing"""
    def __init__(self, user_id, org_id, organization):
        self.userId = user_id
        self.organizationId = org_id
        self.organization = organization


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


@pytest.fixture
def test_user():
    """Test user fixture"""
    return MockUser()


@pytest.fixture
def test_org():
    """Test organization fixture"""
    return MockOrg()


@pytest.fixture
async def client():
    """HTTP client for testing"""
    from src.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_api_key(client, test_org, test_user):
    """Test creating an API key via POST /api/v1/api-keys/"""
    from src.main import app
    from src.core.auth import get_current_organization_from_jwt
    
    # Track what prefix was used when creating the API key
    created_prefix = None
    original_create = None
    
    async def mock_create(data):
        """Mock prisma.apikey.create and capture the prefix"""
        nonlocal created_prefix
        created_prefix = data.get('prefix')
        
        mock_api_key = MagicMock()
        mock_api_key.id = "test-api-key-id"
        mock_api_key.name = data['name']
        mock_api_key.organizationId = data['organizationId']
        mock_api_key.permissions = data['permissions']
        mock_api_key.prefix = created_prefix
        mock_api_key.lastUsedAt = None
        mock_api_key.expiresAt = None
        mock_api_key.createdAt = data['createdAt']
        mock_api_key.updatedAt = data['updatedAt']
        return mock_api_key
    
    # Override the authentication dependency
    async def mock_get_org():
        return test_org
    
    app.dependency_overrides[get_current_organization_from_jwt] = mock_get_org
    
    try:
        # Patch the database and service functions
        with patch('src.api.v1.endpoints.api_keys.prisma.apikey.create', mock_create), \
             patch('src.api.v1.endpoints.api_keys.audit_log_service.log_action', AsyncMock()), \
             patch('src.api.v1.endpoints.api_keys.webhook_service.notify_key_created', AsyncMock()):
            
            # Authenticate
            token = create_test_jwt(test_user)
            
            response = await client.post(
                "/api/v1/api-keys/",
                headers={"Authorization": f"Bearer {token}"},
                json={"name": "Test Key"}
            )
            
            assert response.status_code == 201
            data = response.json()
            assert "plaintext_key" in data  # Only time we see this!
            assert data["name"] == "Test Key"
            assert data["prefix"] == data["plaintext_key"][:8]
            assert len(data["plaintext_key"]) > 8  # Make sure we got a real key
    finally:
        # Clean up the override
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_api_key_authentication(client, test_org, monkeypatch):
    """Test using an API key to authenticate to /api/v1/productions"""
    
    # Generate a test API key
    plaintext_key = secrets.token_urlsafe(48)
    hashed_key = hash_api_key(plaintext_key)
    
    # Mock API key record
    mock_api_key_record = MagicMock()
    mock_api_key_record.id = "test-api-key-id"
    mock_api_key_record.key = hashed_key
    mock_api_key_record.organizationId = test_org.id
    mock_api_key_record.organization = test_org
    mock_api_key_record.permissions = ["read", "write"]
    mock_api_key_record.expiresAt = None
    
    # Patch database lookups
    with patch('src.core.api_key_middleware.prisma.apikey.find_first', AsyncMock(return_value=mock_api_key_record)), \
         patch('src.utils.database.prisma.apikey.update', AsyncMock(return_value=mock_api_key_record)), \
         patch('src.utils.database.prisma.production.find_many', AsyncMock(return_value=[])):
        
        # Use key to authenticate
        response = await client.get(
            "/api/v1/productions/",
            headers={"X-API-Key": plaintext_key}
        )
        assert response.status_code == 200

