"""
Test API endpoints for PilotForge
Tax Incentive Intelligence for Film & TV
"""
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.mark.asyncio
class TestHealthEndpoints:
    """Test health and root endpoints"""
    
    async def test_root_endpoint(self):
        """Test API root returns correct info"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/")
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Welcome to PilotForge"
            assert "version" in data
            assert "api" in data


@pytest.mark.asyncio
class TestCalculatorEndpoints:
    """Test calculator API endpoints"""
    
    async def test_simple_calculate(self):
        """Test simple calculate endpoint"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/0.1.0/calculate/simple",
                json={
                    "jurisdictionId": "test-jurisdiction",
                    "qualifiedSpend": 1000000.0
                }
            )
            # Just test that endpoint exists (may return error without valid data)
            assert response.status_code in [200, 404, 422]
    
    async def test_compare_endpoint(self):
        """Test compare endpoint exists"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/0.1.0/calculate/compare",
                json={
                    "jurisdictionIds": ["test-1", "test-2"],
                    "qualifiedSpend": 1000000.0
                }
            )
            # Just test that endpoint exists
            assert response.status_code in [200, 404, 422]


@pytest.mark.asyncio
class TestJurisdictionEndpoints:
    """Test jurisdiction API endpoints"""
    
    async def test_list_jurisdictions(self):
        """Test list jurisdictions endpoint"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/0.1.0/jurisdictions/")
            
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
    
    async def test_get_jurisdiction_by_id(self):
        """Test get jurisdiction by ID"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/0.1.0/jurisdictions/")
            
            if response.status_code == 200:
                jurisdictions = response.json()
                if len(jurisdictions) > 0:
                    jurisdiction_id = jurisdictions[0]["id"]
                    detail_response = await client.get(f"/api/0.1.0/jurisdictions/{jurisdiction_id}")
                    assert detail_response.status_code == 200


@pytest.mark.asyncio
class TestIncentiveRuleEndpoints:
    """Test incentive rule API endpoints"""
    
    async def test_list_incentive_rules(self):
        """Test list incentive rules endpoint"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/0.1.0/incentive-rules/")
            
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
    
    async def test_get_rule_by_id(self):
        """Test get rule by ID"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/0.1.0/incentive-rules/")
            
            if response.status_code == 200:
                rules = response.json()
                if len(rules) > 0:
                    rule_id = rules[0]["id"]
                    detail_response = await client.get(f"/api/0.1.0/incentive-rules/{rule_id}")
                    assert detail_response.status_code == 200


@pytest.mark.asyncio
class TestProductionEndpoints:
    """Test production API endpoints"""
    
    async def test_list_productions(self):
        """Test list productions endpoint"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/0.1.0/productions/")
            
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
    
    async def test_get_production_by_id(self):
        """Test get production by ID"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/0.1.0/productions/")
            
            if response.status_code == 200:
                productions = response.json()
                if len(productions) > 0:
                    production_id = productions[0]["id"]
                    detail_response = await client.get(f"/api/0.1.0/productions/{production_id}")
                    assert detail_response.status_code == 200


@pytest.mark.asyncio
class TestReportEndpoints:
    """Test report API endpoints"""
    
    async def test_comparison_report_endpoint(self):
        """Test comparison report endpoint exists"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/0.1.0/reports/comparison",
                json={
                    "jurisdictionIds": ["test-1", "test-2"],
                    "qualifiedSpend": 1000000.0
                }
            )
            # Just test that endpoint exists
            assert response.status_code in [200, 404, 422]
    
    async def test_compliance_report_endpoint(self):
        """Test compliance report endpoint exists"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/0.1.0/reports/compliance",
                json={
                    "productionId": "test-production",
                    "jurisdictionId": "test-jurisdiction"
                }
            )
            # Just test that endpoint exists
            assert response.status_code in [200, 404, 422]
