"""
Integration tests for API key management endpoints
"""
import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
import json


@pytest.mark.asyncio
class TestApiKeyEndpoints:
    """Integration tests for API key endpoints with new features"""
    
    async def test_create_api_key_with_permissions(self):
        """Test creating an API key with custom permissions"""
        # This would require a full app setup with database
        # For now, we'll test the model validation
        from src.models.api_key import ApiKeyCreate
        
        data = {
            "name": "Test Key",
            "permissions": ["read", "write"]
        }
        key_create = ApiKeyCreate(**data)
        assert key_create.permissions == ["read", "write"]
    
    async def test_bulk_revoke_expired_keys(self):
        """Test bulk revoking expired API keys"""
        # Mock test - would need database setup
        pass


@pytest.mark.asyncio
class TestRateLimiting:
    """Tests for rate limiting service"""
    
    async def test_rate_limit_check_no_redis(self):
        """Test rate limiting when Redis is not available"""
        from src.services.rate_limit_service import RateLimitService
        
        service = RateLimitService()
        # Without Redis initialization, should allow all requests
        allowed, remaining, reset = await service.check_rate_limit("test-key-id")
        assert allowed is True
        assert remaining > 0
    
    async def test_rate_limit_usage_tracking(self):
        """Test that rate limit usage is tracked"""
        from src.services.rate_limit_service import RateLimitService
        
        service = RateLimitService()
        usage = await service.get_current_usage("test-key-id")
        assert "current" in usage
        assert "limit" in usage
        assert "remaining" in usage


@pytest.mark.asyncio
class TestAuditLogging:
    """Tests for audit logging service"""
    
    @patch('src.services.audit_log_service.prisma')
    async def test_log_api_key_creation(self, mock_prisma):
        """Test logging API key creation"""
        from src.services.audit_log_service import audit_log_service
        
        mock_prisma.auditlog.create = AsyncMock()
        
        await audit_log_service.log_action(
            organization_id="org-123",
            action="create",
            api_key_id="key-123",
            metadata='{"name": "Test Key"}'
        )
        
        mock_prisma.auditlog.create.assert_called_once()
        call_args = mock_prisma.auditlog.create.call_args
        assert call_args[1]["data"]["action"] == "create"
        assert call_args[1]["data"]["organizationId"] == "org-123"
    
    @patch('src.services.audit_log_service.prisma')
    async def test_log_api_key_deletion(self, mock_prisma):
        """Test logging API key deletion"""
        from src.services.audit_log_service import audit_log_service
        
        mock_prisma.auditlog.create = AsyncMock()
        
        await audit_log_service.log_action(
            organization_id="org-123",
            action="delete",
            api_key_id="key-123"
        )
        
        mock_prisma.auditlog.create.assert_called_once()
        call_args = mock_prisma.auditlog.create.call_args
        assert call_args[1]["data"]["action"] == "delete"
    
    @patch('src.services.audit_log_service.prisma')
    async def test_get_audit_logs(self, mock_prisma):
        """Test retrieving audit logs"""
        from src.services.audit_log_service import audit_log_service
        
        mock_log = MagicMock()
        mock_log.id = "log-123"
        mock_log.action = "create"
        mock_prisma.auditlog.find_many = AsyncMock(return_value=[mock_log])
        
        logs = await audit_log_service.get_logs(
            organization_id="org-123",
            limit=10
        )
        
        assert len(logs) == 1
        assert logs[0].action == "create"


@pytest.mark.asyncio
class TestWebhooks:
    """Tests for webhook service"""
    
    @patch('src.services.webhook_service.prisma')
    @patch('src.services.webhook_service.httpx.AsyncClient')
    async def test_send_webhook_notification(self, mock_client, mock_prisma):
        """Test sending webhook notification"""
        from src.services.webhook_service import webhook_service
        
        # Mock webhook config
        mock_webhook = MagicMock()
        mock_webhook.url = "https://example.com/webhook"
        mock_webhook.events = ["api_key_created"]
        mock_webhook.secret = "test-secret"
        mock_prisma.webhookconfig.find_many = AsyncMock(return_value=[mock_webhook])
        
        # Mock HTTP client
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        # Mock the get_client method instead
        webhook_service._client = AsyncMock()
        webhook_service._client.post = AsyncMock(return_value=mock_response)
        
        await webhook_service.send_webhook(
            organization_id="org-123",
            event="api_key_created",
            payload={"api_key_id": "key-123"}
        )
        
        mock_prisma.webhookconfig.find_many.assert_called_once()
    
    @patch('src.services.webhook_service.prisma')
    async def test_notify_key_created(self, mock_prisma):
        """Test key creation notification"""
        from src.services.webhook_service import webhook_service
        
        # Mock empty webhook configs
        mock_prisma.webhookconfig.find_many = AsyncMock(return_value=[])
        
        await webhook_service.notify_key_created(
            organization_id="org-123",
            api_key_id="key-123",
            api_key_name="Test Key"
        )
        
        # Verify the call was made
        mock_prisma.webhookconfig.find_many.assert_called_once()


@pytest.mark.asyncio
class TestUsageAnalytics:
    """Tests for usage analytics service"""
    
    @patch('src.services.usage_analytics_service.prisma')
    async def test_record_usage(self, mock_prisma):
        """Test recording API usage"""
        from src.services.usage_analytics_service import usage_analytics_service
        
        mock_prisma.apikeyusage.create = AsyncMock()
        
        await usage_analytics_service.record_usage(
            api_key_id="key-123",
            endpoint="/api/v1/productions",
            method="GET",
            status_code=200,
            response_time=150
        )
        
        mock_prisma.apikeyusage.create.assert_called_once()
        call_args = mock_prisma.apikeyusage.create.call_args
        assert call_args[1]["data"]["endpoint"] == "/api/v1/productions"
        assert call_args[1]["data"]["statusCode"] == 200
    
    @patch('src.services.usage_analytics_service.prisma')
    async def test_get_analytics(self, mock_prisma):
        """Test getting usage analytics"""
        from src.services.usage_analytics_service import usage_analytics_service
        
        # Mock usage records
        mock_record = MagicMock()
        mock_record.statusCode = 200
        mock_record.responseTime = 100
        mock_record.endpoint = "/api/v1/productions"
        mock_record.method = "GET"
        mock_record.id = "usage-123"
        mock_record.apiKeyId = "key-123"
        mock_record.timestamp = datetime.now(timezone.utc)
        
        mock_prisma.apikeyusage.find_many = AsyncMock(return_value=[mock_record, mock_record])
        
        analytics = await usage_analytics_service.get_analytics(
            api_key_id="key-123"
        )
        
        assert analytics["totalRequests"] == 2
        assert analytics["successfulRequests"] == 2
        assert analytics["failedRequests"] == 0
        assert "/api/v1/productions" in analytics["requestsByEndpoint"]


@pytest.mark.asyncio
class TestPermissionMiddleware:
    """Tests for permission checking in middleware"""
    
    async def test_read_permission_allows_get(self):
        """Test that read permission allows GET requests"""
        from src.core.api_key_middleware import ApiKeyMiddleware
        
        middleware = ApiKeyMiddleware(app=None)
        
        # Mock request
        request = MagicMock()
        request.method = "GET"
        request.url.path = "/api/v1/productions"
        
        # Mock API key with read permission
        api_key_record = MagicMock()
        api_key_record.permissions = ["read"]
        
        has_permission = await middleware._check_permissions(request, api_key_record)
        assert has_permission is True
    
    async def test_read_permission_denies_post(self):
        """Test that read-only permission denies POST requests"""
        from src.core.api_key_middleware import ApiKeyMiddleware
        
        middleware = ApiKeyMiddleware(app=None)
        
        # Mock request
        request = MagicMock()
        request.method = "POST"
        request.url.path = "/api/v1/productions"
        
        # Mock API key with read permission only
        api_key_record = MagicMock()
        api_key_record.permissions = ["read"]
        
        has_permission = await middleware._check_permissions(request, api_key_record)
        assert has_permission is False
    
    async def test_write_permission_allows_post(self):
        """Test that write permission allows POST requests"""
        from src.core.api_key_middleware import ApiKeyMiddleware
        
        middleware = ApiKeyMiddleware(app=None)
        
        # Mock request
        request = MagicMock()
        request.method = "POST"
        request.url.path = "/api/v1/productions"
        
        # Mock API key with write permission
        api_key_record = MagicMock()
        api_key_record.permissions = ["read", "write"]
        
        has_permission = await middleware._check_permissions(request, api_key_record)
        assert has_permission is True
    
    async def test_admin_permission_allows_admin_endpoints(self):
        """Test that admin permission allows admin endpoints"""
        from src.core.api_key_middleware import ApiKeyMiddleware
        
        middleware = ApiKeyMiddleware(app=None)
        
        # Mock request to admin endpoint
        request = MagicMock()
        request.method = "GET"
        request.url.path = "/api/v1/api-keys/audit-logs"
        
        # Mock API key with admin permission
        api_key_record = MagicMock()
        api_key_record.permissions = ["read", "write", "admin"]
        
        has_permission = await middleware._check_permissions(request, api_key_record)
        assert has_permission is True
    
    async def test_non_admin_denied_admin_endpoints(self):
        """Test that non-admin is denied access to admin endpoints"""
        from src.core.api_key_middleware import ApiKeyMiddleware
        
        middleware = ApiKeyMiddleware(app=None)
        
        # Mock request to admin endpoint
        request = MagicMock()
        request.method = "GET"
        request.url.path = "/api/v1/api-keys/audit-logs"
        
        # Mock API key without admin permission
        api_key_record = MagicMock()
        api_key_record.permissions = ["read", "write"]
        
        has_permission = await middleware._check_permissions(request, api_key_record)
        assert has_permission is False
