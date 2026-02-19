"""
Integration tests for Budget Management API endpoints.

These tests validate the budget management REST API for MMB Connector integration.
They use a mocked database to avoid requiring a live PostgreSQL connection.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timezone

from src.main import app

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_TOKEN_PAYLOAD = {"sub": "api_client", "api_key": "test-key"}


def _make_budget_db_record(**kwargs):
    """Return a mock Prisma Budget record."""
    defaults = {
        "id": "budget-123",
        "projectTitle": "Test Film",
        "productionType": "feature_film",
        "totalBudget": 5000000.0,
        "startDate": datetime(2026, 3, 1, tzinfo=timezone.utc),
        "endDate": datetime(2026, 8, 31, tzinfo=timezone.utc),
        "productionCompany": "Test Productions",
        "primaryJurisdiction": "CA",
        "jurisdictions": ["CA", "GA"],
        "status": "processing",
        "createdAt": datetime(2026, 2, 19, tzinfo=timezone.utc),
        "updatedAt": datetime(2026, 2, 19, tzinfo=timezone.utc),
        "accounts": [],
    }
    defaults.update(kwargs)
    record = MagicMock()
    for k, v in defaults.items():
        setattr(record, k, v)
    return record


SAMPLE_BUDGET_PAYLOAD = {
    "project": {
        "title": "Test Feature Film",
        "production_type": "feature_film",
        "total_budget": 5000000,
        "start_date": "2026-03-01T00:00:00Z",
        "end_date": "2026-08-31T00:00:00Z",
        "production_company": "Test Productions Inc",
        "primary_jurisdiction": "CA",
    },
    "accounts": [
        {
            "account_number": "1100",
            "category": "Above-the-Line",
            "subcategory": "Writers",
            "description": "Screenplay",
            "amount": 250000,
            "eligible_for_incentives": True,
        }
    ],
    "jurisdictions": ["CA", "GA"],
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestAuthEndpoint:
    """Test /api/0.1.0/v1/auth/token endpoint"""

    async def test_get_token_success(self):
        """Test getting a token with a valid API key (no keys configured = allow any)."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/0.1.0/v1/auth/token",
                json={"api_key": "any-key"},
            )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_get_token_empty_key_fails(self):
        """Test that an empty API key is rejected."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/0.1.0/v1/auth/token",
                json={"api_key": ""},
            )
        assert response.status_code == 401


@pytest.mark.asyncio
class TestBudgetEndpoints:
    """Test /api/0.1.0/v1/budgets endpoints"""

    async def _get_token(self, client: AsyncClient) -> str:
        response = await client.post(
            "/api/0.1.0/v1/auth/token",
            json={"api_key": "test-key"},
        )
        return response.json()["access_token"]

    async def test_create_budget_requires_auth(self):
        """Test that creating a budget requires authentication (returns 401)."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/0.1.0/v1/budgets/",
                json=SAMPLE_BUDGET_PAYLOAD,
            )
        assert response.status_code == 401

    @patch("src.services.budget_service.prisma")
    async def test_create_budget_success(self, mock_prisma):
        """Test successful budget creation."""
        mock_budget = _make_budget_db_record()
        mock_prisma.budget.create = AsyncMock(return_value=mock_budget)
        mock_prisma.budgetaccount.create = AsyncMock(return_value=MagicMock())

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            token = await self._get_token(client)
            response = await client.post(
                "/api/0.1.0/v1/budgets/",
                json=SAMPLE_BUDGET_PAYLOAD,
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 201
        data = response.json()
        assert "budget_id" in data
        assert data["status"] == "processing"
        assert data["message"] == "Budget uploaded successfully"

    @patch("src.services.budget_service.prisma")
    async def test_get_budget_not_found(self, mock_prisma):
        """Test that a missing budget returns 404."""
        mock_prisma.budget.find_unique = AsyncMock(return_value=None)

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            token = await self._get_token(client)
            response = await client.get(
                "/api/0.1.0/v1/budgets/nonexistent-id",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 404

    @patch("src.services.budget_service.prisma")
    async def test_get_budget_success(self, mock_prisma):
        """Test successful budget retrieval."""
        mock_budget = _make_budget_db_record()
        mock_prisma.budget.find_unique = AsyncMock(return_value=mock_budget)

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            token = await self._get_token(client)
            response = await client.get(
                "/api/0.1.0/v1/budgets/budget-123",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert data["budget_id"] == "budget-123"
        assert data["project"]["title"] == "Test Film"

    @patch("src.services.budget_service.prisma")
    async def test_list_budgets(self, mock_prisma):
        """Test budget listing with pagination."""
        mock_budget = _make_budget_db_record()
        mock_prisma.budget.find_many = AsyncMock(return_value=[mock_budget])
        mock_prisma.budget.count = AsyncMock(return_value=1)

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            token = await self._get_token(client)
            response = await client.get(
                "/api/0.1.0/v1/budgets/?page=1&limit=20",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["page"] == 1
        assert len(data["budgets"]) == 1

    @patch("src.services.budget_service.prisma")
    async def test_delete_budget_success(self, mock_prisma):
        """Test soft-delete of a budget."""
        mock_budget = _make_budget_db_record()
        mock_prisma.budget.find_unique = AsyncMock(return_value=mock_budget)
        mock_prisma.budget.update = AsyncMock(return_value=mock_budget)

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            token = await self._get_token(client)
            response = await client.delete(
                "/api/0.1.0/v1/budgets/budget-123",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert "deleted" in data["message"].lower()

    async def test_create_budget_invalid_data(self):
        """Test that invalid budget data returns 422."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            token = await self._get_token(client)
            response = await client.post(
                "/api/0.1.0/v1/budgets/",
                json={"project": {"title": ""}},  # Missing required fields
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 422


@pytest.mark.asyncio
class TestIncentiveEndpoints:
    """Test incentive analysis endpoints"""

    async def _get_token(self, client: AsyncClient) -> str:
        response = await client.post(
            "/api/0.1.0/v1/auth/token",
            json={"api_key": "test-key"},
        )
        return response.json()["access_token"]

    @patch("src.services.incentive_service.prisma")
    async def test_analyze_budget(self, mock_prisma):
        """Test triggering incentive analysis."""
        mock_budget = MagicMock()
        mock_budget.id = "budget-123"
        mock_budget.jurisdictions = ["CA"]
        mock_prisma.budget.find_unique = AsyncMock(return_value=mock_budget)
        mock_prisma.budgetaccount.find_many = AsyncMock(return_value=[])
        mock_analysis = MagicMock()
        mock_analysis.id = "analysis-123"
        mock_prisma.incentiveanalysis.create = AsyncMock(return_value=mock_analysis)
        mock_prisma.incentiveprogram.create = AsyncMock(return_value=MagicMock())

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            token = await self._get_token(client)
            response = await client.post(
                "/api/0.1.0/v1/budgets/budget-123/analyze",
                json={"jurisdictions": ["CA"]},
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert "analysis_id" in data
        assert data["budget_id"] == "budget-123"
        assert data["status"] == "completed"


@pytest.mark.asyncio
class TestComplianceEndpoints:
    """Test compliance monitoring endpoints"""

    async def _get_token(self, client: AsyncClient) -> str:
        response = await client.post(
            "/api/0.1.0/v1/auth/token",
            json={"api_key": "test-key"},
        )
        return response.json()["access_token"]

    @patch("src.services.compliance_service.prisma")
    async def test_get_compliance_status(self, mock_prisma):
        """Test getting compliance status for a budget."""
        mock_budget = MagicMock()
        mock_budget.id = "budget-123"
        mock_budget.jurisdictions = ["CA"]
        mock_budget.endDate = datetime(2026, 8, 31, tzinfo=timezone.utc)
        mock_prisma.budget.find_unique = AsyncMock(return_value=mock_budget)
        mock_prisma.compliancecheck.create = AsyncMock(return_value=MagicMock())

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            token = await self._get_token(client)
            response = await client.get(
                "/api/0.1.0/v1/budgets/budget-123/compliance",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert data["budget_id"] == "budget-123"
        assert "overall_status" in data
        assert "jurisdictions" in data

    @patch("src.services.compliance_service.prisma")
    async def test_budget_not_found_compliance(self, mock_prisma):
        """Test compliance check returns 404 for unknown budget."""
        mock_prisma.budget.find_unique = AsyncMock(return_value=None)

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            token = await self._get_token(client)
            response = await client.get(
                "/api/0.1.0/v1/budgets/nonexistent/compliance",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 404


@pytest.mark.asyncio
class TestHealthEndpoint:
    """Test health check endpoint"""

    async def test_api_health(self):
        """Test the health endpoint accessible via the API router."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/0.1.0/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
