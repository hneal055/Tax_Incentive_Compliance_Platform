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
        self.user_id = user_id
        self.organization_id = org_id
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


@pytest.mark.asyncio
async def test_rotate_api_key(client, test_org, test_user):
    """Test rotating an API key via POST /api/v1/api-keys/{key_id}/rotate"""
    from src.main import app
    from src.core.auth import get_current_organization_from_jwt
    
    key_id = "test-api-key-id"
    old_prefix = "oldprefi"  # 8-character prefix matching standard format
    
    # Mock existing API key
    mock_old_key = MagicMock()
    mock_old_key.id = key_id
    mock_old_key.name = "Test Key"
    mock_old_key.organizationId = test_org.id
    mock_old_key.permissions = ["read", "write"]
    mock_old_key.prefix = old_prefix
    mock_old_key.lastUsedAt = datetime.now(timezone.utc)
    mock_old_key.expiresAt = None
    mock_old_key.createdAt = datetime.now(timezone.utc)
    mock_old_key.updatedAt = datetime.now(timezone.utc)
    
    # Track what new data was used when updating
    updated_data = {}
    
    async def mock_find_first(where):
        """Mock finding the existing key"""
        return mock_old_key
    
    async def mock_update(where, data):
        """Mock updating the key with new values"""
        nonlocal updated_data
        updated_data = data
        
        # Create updated key with new values
        mock_new_key = MagicMock()
        mock_new_key.id = key_id
        mock_new_key.name = mock_old_key.name
        mock_new_key.organizationId = mock_old_key.organizationId
        mock_new_key.permissions = mock_old_key.permissions
        mock_new_key.prefix = data.get('prefix', old_prefix)
        mock_new_key.lastUsedAt = data.get('lastUsedAt')
        mock_new_key.expiresAt = mock_old_key.expiresAt
        mock_new_key.createdAt = mock_old_key.createdAt
        mock_new_key.updatedAt = data.get('updatedAt', datetime.now(timezone.utc))
        return mock_new_key
    
    # Override authentication dependency
    async def mock_get_org():
        return test_org
    
    app.dependency_overrides[get_current_organization_from_jwt] = mock_get_org
    
    try:
        # Patch database and service functions
        with patch('src.api.v1.endpoints.api_keys.prisma.apikey.find_first', mock_find_first), \
             patch('src.api.v1.endpoints.api_keys.prisma.apikey.update', mock_update), \
             patch('src.api.v1.endpoints.api_keys.audit_log_service.log_action', AsyncMock()), \
             patch('src.api.v1.endpoints.api_keys.webhook_service.notify_key_rotated', AsyncMock()):
            
            # Authenticate
            token = create_test_jwt(test_user)
            
            # Rotate the key
            response = await client.post(
                f"/api/v1/api-keys/{key_id}/rotate",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # Verify we got a new plaintext key
            assert "plaintext_key" in data
            assert len(data["plaintext_key"]) > 8
            
            # Verify the prefix changed
            assert data["prefix"] != old_prefix
            assert data["prefix"] == data["plaintext_key"][:8]
            
            # Verify metadata stayed the same
            assert data["name"] == "Test Key"
            assert data["permissions"] == ["read", "write"]
            assert data["id"] == key_id
            
            # Verify lastUsedAt was reset to None
            assert data["lastUsedAt"] is None
            
            # Verify the update included new key hash and prefix
            assert 'key' in updated_data
            assert 'prefix' in updated_data
            assert 'updatedAt' in updated_data
            assert 'lastUsedAt' in updated_data
    finally:
        # Clean up
        app.dependency_overrides.clear()

