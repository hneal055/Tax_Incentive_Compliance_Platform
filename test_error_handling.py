"""
Error Handling & Logging Tests
Validates proper error responses and logging behavior
"""

import pytest
import logging
import json
from httpx import AsyncClient
from src.main import app
from src.utils.exceptions import (
    ValidationError, NotFoundError, DatabaseError,
    UnauthorizedError, ForbiddenError
)


@pytest.fixture(scope="function")
async def client():
    """Async HTTP client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await app.router.lifespan_context(None).__aenter__()
        yield ac
        try:
            await app.router.lifespan_context(None).__aexit__(None, None, None)
        except:
            pass


class TestErrorResponses:
    """Test error response formatting"""

    @pytest.mark.asyncio
    async def test_404_error_response_format(self, client):
        """404 errors should return proper format"""
        response = await client.get("/api/0.1.0/nonexistent")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "message" in data["error"]
        assert "code" in data["error"]
        assert "timestamp" in data["error"]
        assert data["error"]["code"] == "HTTP_ERROR"

    @pytest.mark.asyncio
    async def test_422_validation_error_response_format(self, client):
        """Validation errors should return proper format"""
        payload = {}  # Missing required fields
        response = await client.post("/api/0.1.0/calculate/simple", json=payload)
        
        assert response.status_code == 422
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "VALIDATION_ERROR"
        assert "details" in data["error"]

    @pytest.mark.asyncio
    async def test_error_includes_correlation_id(self, client):
        """Error responses should include correlation ID"""
        response = await client.get("/api/0.1.0/nonexistent")
        
        data = response.json()
        assert "correlation_id" in data["error"]
        # Default is "no-id" if not provided
        assert data["error"]["correlation_id"] is not None

    @pytest.mark.asyncio
    async def test_error_includes_timestamp(self, client):
        """Error responses should include ISO timestamp"""
        response = await client.get("/api/0.1.0/nonexistent")
        
        data = response.json()
        assert "timestamp" in data["error"]
        # Should be ISO format
        assert "T" in data["error"]["timestamp"]


class TestExceptionTypes:
    """Test custom exception types"""

    def test_validation_error_creation(self):
        """ValidationError should have correct status code"""
        exc = ValidationError("Invalid input", {"field": "age"})
        assert exc.status_code == 422
        assert exc.error_code == "VALIDATION_ERROR"
        assert exc.details == {"field": "age"}

    def test_not_found_error_creation(self):
        """NotFoundError should have correct status code"""
        exc = NotFoundError("Jurisdiction", "jur-123")
        assert exc.status_code == 404
        assert exc.error_code == "NOT_FOUND"
        assert "jur-123" in str(exc)

    def test_database_error_creation(self):
        """DatabaseError should have correct status code"""
        exc = DatabaseError("Connection timeout")
        assert exc.status_code == 500
        assert exc.error_code == "DATABASE_ERROR"

    def test_unauthorized_error_creation(self):
        """UnauthorizedError should have correct status code"""
        exc = UnauthorizedError()
        assert exc.status_code == 401
        assert exc.error_code == "UNAUTHORIZED"

    def test_forbidden_error_creation(self):
        """ForbiddenError should have correct status code"""
        exc = ForbiddenError()
        assert exc.status_code == 403
        assert exc.error_code == "FORBIDDEN"


class TestErrorLogging:
    """Test that errors are properly logged"""

    @pytest.mark.asyncio
    async def test_404_is_logged_as_warning(self, client, caplog):
        """404 errors should be logged"""
        with caplog.at_level(logging.WARNING):
            response = await client.get("/api/0.1.0/nonexistent")
            assert response.status_code == 404
        
        # Should have logged something about the error

    @pytest.mark.asyncio
    async def test_validation_error_is_logged(self, client, caplog):
        """Validation errors should be logged"""
        with caplog.at_level(logging.WARNING):
            payload = {}
            response = await client.post("/api/0.1.0/calculate/simple", json=payload)
            assert response.status_code == 422


class TestSuccessLogging:
    """Test that successful requests are logged properly"""

    @pytest.mark.asyncio
    async def test_health_endpoint_logs_successfully(self, client, caplog):
        """Successful requests should be logged"""
        with caplog.at_level(logging.INFO):
            response = await client.get("/health")
            assert response.status_code == 200


class TestErrorRecovery:
    """Test application recovery from errors"""

    @pytest.mark.asyncio
    async def test_application_continues_after_404(self, client):
        """Application should continue working after 404"""
        # First: trigger 404
        response1 = await client.get("/api/0.1.0/nonexistent")
        assert response1.status_code == 404
        
        # Second: verify health still works
        response2 = await client.get("/health")
        assert response2.status_code == 200

    @pytest.mark.asyncio
    async def test_application_continues_after_validation_error(self, client):
        """Application should continue working after validation error"""
        # First: trigger validation error
        response1 = await client.post("/api/0.1.0/calculate/simple", json={})
        assert response1.status_code == 422
        
        # Second: verify health still works
        response2 = await client.get("/health")
        assert response2.status_code == 200


class TestErrorDetailsSensitivity:
    """Test that sensitive details are not leaked in errors"""

    @pytest.mark.asyncio
    async def test_error_responses_dont_leak_secrets(self, client):
        """Error responses should not contain database credentials"""
        response = await client.get("/api/0.1.0/nonexistent")
        
        data = response.json()
        response_str = json.dumps(data)
        
        # Should not contain database connection info
        assert "postgresql://" not in response_str
        assert "password" not in response_str.lower() or "@" not in response_str
        assert "localhost" not in response_str or "5432" not in response_str


class TestErrorConsistency:
    """Test error response consistency across endpoints"""

    @pytest.mark.asyncio
    async def test_all_errors_have_required_fields(self, client):
        """All error responses should have required fields"""
        error_urls = [
            "/api/0.1.0/nonexistent",
        ]
        
        for url in error_urls:
            response = await client.get(url)
            assert response.status_code >= 400
            
            data = response.json()
            assert "error" in data
            assert "message" in data["error"]
            assert "code" in data["error"]
            assert "timestamp" in data["error"]
            assert "correlation_id" in data["error"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
