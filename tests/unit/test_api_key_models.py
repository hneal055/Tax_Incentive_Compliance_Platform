"""
Tests for API Key Pydantic models
"""
import pytest
from datetime import datetime, timezone, timedelta
from pydantic import ValidationError

from src.models.api_key import (
    ApiKeyCreate,
    ApiKeyUpdate,
    ApiKeyExpire,
    ApiKeyResponse,
    ApiKeyWithPrefix,
    ApiKeyCreatedResponse,
    get_key_prefix,
)


class TestApiKeyCreate:
    """Tests for ApiKeyCreate schema"""
    
    def test_create_with_name_only(self):
        """Test creating API key with only name"""
        data = {"name": "Production API Key"}
        key_create = ApiKeyCreate(**data)
        assert key_create.name == "Production API Key"
        assert key_create.expiresAt is None
    
    def test_create_with_expiration(self):
        """Test creating API key with expiration date"""
        expires = datetime.now(timezone.utc) + timedelta(days=30)
        data = {"name": "Temporary Key", "expiresAt": expires}
        key_create = ApiKeyCreate(**data)
        assert key_create.name == "Temporary Key"
        assert key_create.expiresAt == expires
    
    def test_create_name_too_short(self):
        """Test validation error for empty name"""
        with pytest.raises(ValidationError) as exc_info:
            ApiKeyCreate(name="")
        assert "String should have at least 1 character" in str(exc_info.value)
    
    def test_create_name_too_long(self):
        """Test validation error for name too long"""
        long_name = "x" * 101
        with pytest.raises(ValidationError) as exc_info:
            ApiKeyCreate(name=long_name)
        assert "String should have at most 100 characters" in str(exc_info.value)
    
    def test_create_missing_name(self):
        """Test validation error for missing name"""
        with pytest.raises(ValidationError) as exc_info:
            ApiKeyCreate()
        assert "Field required" in str(exc_info.value)


class TestApiKeyUpdate:
    """Tests for ApiKeyUpdate schema"""
    
    def test_update_name(self):
        """Test updating API key name"""
        data = {"name": "Updated Key Name"}
        key_update = ApiKeyUpdate(**data)
        assert key_update.name == "Updated Key Name"
    
    def test_update_empty(self):
        """Test update with no fields"""
        key_update = ApiKeyUpdate()
        assert key_update.name is None
    
    def test_update_name_validation(self):
        """Test name validation on update"""
        with pytest.raises(ValidationError):
            ApiKeyUpdate(name="")


class TestApiKeyExpire:
    """Tests for ApiKeyExpire schema"""
    
    def test_set_expiration(self):
        """Test setting expiration date"""
        expires = datetime.now(timezone.utc) + timedelta(days=60)
        key_expire = ApiKeyExpire(expiresAt=expires)
        assert key_expire.expiresAt == expires
    
    def test_clear_expiration(self):
        """Test clearing expiration (set to never expire)"""
        key_expire = ApiKeyExpire(expiresAt=None)
        assert key_expire.expiresAt is None
    
    def test_default_expiration(self):
        """Test default expiration is None"""
        key_expire = ApiKeyExpire()
        assert key_expire.expiresAt is None


class TestApiKeyResponse:
    """Tests for ApiKeyResponse schema"""
    
    def test_response_from_dict(self):
        """Test creating response from dictionary"""
        now = datetime.now(timezone.utc)
        data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Test Key",
            "organizationId": "org-123",
            "lastUsedAt": now,
            "expiresAt": now + timedelta(days=30),
            "createdAt": now,
            "updatedAt": now,
        }
        response = ApiKeyResponse(**data)
        assert response.id == "123e4567-e89b-12d3-a456-426614174000"
        assert response.name == "Test Key"
        assert response.organizationId == "org-123"
        assert response.lastUsedAt == now
        assert response.expiresAt == now + timedelta(days=30)
    
    def test_response_optional_fields(self):
        """Test response with optional fields as None"""
        now = datetime.now(timezone.utc)
        data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Test Key",
            "organizationId": "org-123",
            "lastUsedAt": None,
            "expiresAt": None,
            "createdAt": now,
            "updatedAt": now,
        }
        response = ApiKeyResponse(**data)
        assert response.lastUsedAt is None
        assert response.expiresAt is None


class TestApiKeyWithPrefix:
    """Tests for ApiKeyWithPrefix schema"""
    
    def test_with_prefix(self):
        """Test response includes prefix"""
        now = datetime.now(timezone.utc)
        data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Test Key",
            "organizationId": "org-123",
            "prefix": "abcd1234",
            "lastUsedAt": None,
            "expiresAt": None,
            "createdAt": now,
            "updatedAt": now,
        }
        response = ApiKeyWithPrefix(**data)
        assert response.prefix == "abcd1234"
        assert response.name == "Test Key"


class TestApiKeyCreatedResponse:
    """Tests for ApiKeyCreatedResponse schema"""
    
    def test_created_with_plaintext(self):
        """Test created response includes plaintext key"""
        now = datetime.now(timezone.utc)
        data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Test Key",
            "organizationId": "org-123",
            "prefix": "abcd1234",
            "plaintextKey": "abcd1234-5678-90ef-ghij-klmnopqrstuv",
            "lastUsedAt": None,
            "expiresAt": None,
            "createdAt": now,
            "updatedAt": now,
        }
        response = ApiKeyCreatedResponse(**data)
        assert response.plaintextKey == "abcd1234-5678-90ef-ghij-klmnopqrstuv"
        assert response.prefix == "abcd1234"
        assert response.name == "Test Key"


class TestGetKeyPrefix:
    """Tests for get_key_prefix helper function"""
    
    def test_get_prefix_full_key(self):
        """Test extracting prefix from a full key"""
        key = "abcd1234-5678-90ef-ghij-klmnopqrstuv"
        prefix = get_key_prefix(key)
        assert prefix == "abcd1234"
        assert len(prefix) == 8
    
    def test_get_prefix_short_key(self):
        """Test extracting prefix from a short key"""
        key = "short"
        prefix = get_key_prefix(key)
        assert prefix == "short"
        assert len(prefix) == 5
    
    def test_get_prefix_empty_key(self):
        """Test extracting prefix from empty key"""
        prefix = get_key_prefix("")
        assert prefix == ""
    
    def test_get_prefix_none_key(self):
        """Test extracting prefix from None"""
        prefix = get_key_prefix(None)
        assert prefix == ""
    
    def test_get_prefix_exact_8_chars(self):
        """Test extracting prefix from exactly 8 character key"""
        key = "12345678"
        prefix = get_key_prefix(key)
        assert prefix == "12345678"
        assert len(prefix) == 8
    
    def test_get_prefix_unicode(self):
        """Test extracting prefix with unicode characters"""
        key = "🔑🔐🔒🔓🗝️123456789"
        prefix = get_key_prefix(key)
        assert len(prefix) == 8
        assert prefix == key[:8]
