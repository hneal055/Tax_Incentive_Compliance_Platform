"""
Tests for API Key enhancements including permissions, audit logging, webhooks, and analytics
"""
import pytest
from datetime import datetime, timezone, timedelta
from src.models.api_key import ApiKeyCreate, ApiKeyUpdate
from src.models.audit_log import AuditLogCreate, AuditLogResponse
from src.models.webhook_config import WebhookConfigCreate, WebhookConfigUpdate
from src.models.usage_analytics import ApiKeyUsageCreate, UsageAnalytics


class TestApiKeyPermissions:
    """Tests for API key permissions field"""
    
    def test_create_with_default_permissions(self):
        """Test creating API key with default permissions"""
        data = {"name": "Test Key"}
        key_create = ApiKeyCreate(**data)
        assert key_create.permissions == ["read", "write"]
    
    def test_create_with_custom_permissions(self):
        """Test creating API key with custom permissions"""
        data = {"name": "Test Key", "permissions": ["read"]}
        key_create = ApiKeyCreate(**data)
        assert key_create.permissions == ["read"]
    
    def test_create_with_admin_permission(self):
        """Test creating API key with admin permission"""
        data = {"name": "Admin Key", "permissions": ["read", "write", "admin"]}
        key_create = ApiKeyCreate(**data)
        assert "admin" in key_create.permissions
    
    def test_update_permissions(self):
        """Test updating API key permissions"""
        data = {"permissions": ["read"]}
        key_update = ApiKeyUpdate(**data)
        assert key_update.permissions == ["read"]


class TestAuditLog:
    """Tests for audit log models"""
    
    def test_create_audit_log(self):
        """Test creating an audit log entry"""
        data = {
            "organizationId": "org-123",
            "action": "create",
            "apiKeyId": "key-123",
            "actorId": "user-123",
            "metadata": '{"name": "Test Key"}',
            "ipAddress": "127.0.0.1",
            "userAgent": "Test Agent"
        }
        audit_log = AuditLogCreate(**data)
        assert audit_log.action == "create"
        assert audit_log.organizationId == "org-123"
    
    def test_audit_log_response(self):
        """Test audit log response model"""
        now = datetime.now(timezone.utc)
        data = {
            "id": "log-123",
            "organizationId": "org-123",
            "action": "delete",
            "apiKeyId": "key-123",
            "actorId": "user-123",
            "metadata": '{"reason": "expired"}',
            "ipAddress": "127.0.0.1",
            "userAgent": "Test Agent",
            "timestamp": now
        }
        audit_log = AuditLogResponse(**data)
        assert audit_log.action == "delete"
        assert audit_log.timestamp == now


class TestWebhookConfig:
    """Tests for webhook configuration models"""
    
    def test_create_webhook_config(self):
        """Test creating a webhook configuration"""
        data = {
            "url": "https://example.com/webhook",
            "events": ["api_key_created", "api_key_expired"],
            "secret": "my-secret"
        }
        webhook = WebhookConfigCreate(**data)
        assert webhook.url == "https://example.com/webhook"
        assert "api_key_created" in webhook.events
    
    def test_update_webhook_config(self):
        """Test updating a webhook configuration"""
        data = {
            "active": False,
            "events": ["api_key_revoked"]
        }
        webhook = WebhookConfigUpdate(**data)
        assert webhook.active is False
        assert webhook.events == ["api_key_revoked"]


class TestUsageAnalytics:
    """Tests for usage analytics models"""
    
    def test_create_usage_record(self):
        """Test creating a usage record"""
        data = {
            "apiKeyId": "key-123",
            "endpoint": "/api/v1/productions",
            "method": "GET",
            "statusCode": 200,
            "responseTime": 150
        }
        usage = ApiKeyUsageCreate(**data)
        assert usage.endpoint == "/api/v1/productions"
        assert usage.statusCode == 200
    
    def test_usage_analytics(self):
        """Test usage analytics aggregation model"""
        data = {
            "totalRequests": 100,
            "successfulRequests": 95,
            "failedRequests": 5,
            "averageResponseTime": 125.5,
            "requestsByEndpoint": {"/api/v1/productions": 50, "/api/v1/expenses": 50},
            "requestsByMethod": {"GET": 80, "POST": 20},
            "recentActivity": []
        }
        analytics = UsageAnalytics(**data)
        assert analytics.totalRequests == 100
        assert analytics.successfulRequests == 95
        assert analytics.averageResponseTime == 125.5
