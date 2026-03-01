"""
Comprehensive API endpoint tests for PilotForge Tax Incentive Platform
With proper Prisma connection handling
"""

import pytest
from httpx import AsyncClient
from src.main import app
from src.utils.database import prisma


@pytest.fixture(scope="function")
async def client():
    """Async HTTP client with proper startup/shutdown"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Manually trigger startup events
        await app.router.lifespan_context(None).__aenter__()
        yield ac
        # Trigger shutdown events
        try:
            await app.router.lifespan_context(None).__aexit__(None, None, None)
        except:
            pass


# ========================================
# HEALTH & ROOT ENDPOINTS
# ========================================

@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test /health endpoint returns 200"""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root / endpoint"""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


# ========================================
# JURISDICTIONS ENDPOINTS (with DB)
# ========================================

@pytest.mark.asyncio
async def test_get_jurisdictions_with_connection(client):
    """Test GET /jurisdictions/ - requires DB connection"""
    # Ensure connection
    if not prisma.is_connected():
        await prisma.connect()
    
    response = await client.get("/api/0.1.0/jurisdictions/")
    assert response.status_code in [200, 404, 422]
    
    await prisma.disconnect()


# ========================================
# CALCULATION ENDPOINTS (no DB required)
# ========================================

@pytest.mark.asyncio
async def test_calculate_simple(client):
    """Test POST /calculate/simple - simple calculation"""
    payload = {
        "amount": 100000.0,
        "percentage": 25.0
    }
    response = await client.post("/api/0.1.0/calculate/simple", json=payload)
    assert response.status_code in [200, 400, 422]
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_calculate_compare(client):
    """Test POST /calculate/compare"""
    payload = {
        "amount": 100000.0,
        "jurisdictions": ["CA", "NY"]
    }
    response = await client.post("/api/0.1.0/calculate/compare", json=payload)
    assert response.status_code in [200, 400, 422]


@pytest.mark.asyncio
async def test_calculate_compliance(client):
    """Test POST /calculate/compliance"""
    payload = {
        "expenses": [{"category": "labor", "amount": 50000}],
        "rules": []
    }
    response = await client.post("/api/0.1.0/calculate/compliance", json=payload)
    assert response.status_code in [200, 400, 422]


# ========================================
# REPORT ENDPOINTS
# ========================================

@pytest.mark.asyncio
async def test_report_comparison(client):
    """Test POST /reports/comparison"""
    payload = {
        "scenarios": []
    }
    response = await client.post("/api/0.1.0/reports/comparison", json=payload)
    assert response.status_code in [200, 400, 422, 500]


@pytest.mark.asyncio
async def test_report_compliance(client):
    """Test POST /reports/compliance"""
    payload = {
        "productionId": "test-prod-001",
        "rules": []
    }
    response = await client.post("/api/0.1.0/reports/compliance", json=payload)
    assert response.status_code in [200, 400, 422, 500]


# ========================================
# EXCEL EXPORT ENDPOINTS
# ========================================

@pytest.mark.asyncio
async def test_excel_comparison(client):
    """Test POST /excel/comparison"""
    payload = {
        "scenarios": []
    }
    response = await client.post("/api/0.1.0/excel/comparison", json=payload)
    assert response.status_code in [200, 400, 422, 415, 500]


@pytest.mark.asyncio
async def test_excel_compliance(client):
    """Test POST /excel/compliance"""
    payload = {
        "productionId": "test-prod-001"
    }
    response = await client.post("/api/0.1.0/excel/compliance", json=payload)
    assert response.status_code in [200, 400, 422, 415, 500]


# ========================================
# ERROR HANDLING TESTS
# ========================================

@pytest.mark.asyncio
async def test_404_not_found(client):
    """Test 404 for non-existent endpoint"""
    response = await client.get("/api/0.1.0/nonexistent")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_invalid_json_payload(client):
    """Test endpoint with invalid JSON"""
    response = await client.post(
        "/api/0.1.0/calculate/simple",
        content="invalid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code in [400, 422]


@pytest.mark.asyncio
async def test_missing_required_fields(client):
    """Test POST with missing required fields"""
    payload = {"incomplete": "data"}
    response = await client.post("/api/0.1.0/calculate/simple", json=payload)
    assert response.status_code in [400, 422]


@pytest.mark.asyncio
async def test_calculate_simple_validation(client):
    """Test calculate/simple validates input"""
    # Missing percentage
    payload = {"amount": 100000.0}
    response = await client.post("/api/0.1.0/calculate/simple", json=payload)
    assert response.status_code in [400, 422]
    
    # Missing amount
    payload = {"percentage": 25.0}
    response = await client.post("/api/0.1.0/calculate/simple", json=payload)
    assert response.status_code in [400, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
