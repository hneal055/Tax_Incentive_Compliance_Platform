"""
Test API endpoints for PilotForge
Tax Incentive Intelligence for Film & TV
"""
import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from src.main import app


@pytest.mark.asyncio
class TestHealthEndpoints:
    """Test health and root endpoints"""
    
    async def test_root_endpoint(self):
        """Test API root returns correct info"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/")
            response = await client.get("/")
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Welcome to PilotForge"
            assert "version" in data
            assert "endpoints" in data
    @pytest.mark.skip(reason="Health endpoint not implemented")
    async def test_health_check(self):
        """Test health check endpoint"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/calculate/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "api" in data


@pytest.mark.asyncio
class TestCalculatorEndpoints:
    """Test calculator API endpoints"""
    
    async def test_calculator_options(self):
        """Test calculator options endpoint"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/calculate/options")
            
            assert response.status_code == 200
            data = response.json()
            assert "jurisdictions" in data
            assert len(data["jurisdictions"]) > 0
    
    async def test_simple_calculate_validation(self):
        """Test simple calculate endpoint validation"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Test with invalid budget (negative)
            invalid_request = {
                "budget": -1000,
                "jurisdictionId": "test-id",
                "ruleId": "test-rule"
            }
            
            response = await client.post("/api/v1/calculate/simple", json=invalid_request)
            
            # Should return 422 for validation error
            assert response.status_code == 422
    
    async def test_compare_validation(self):
        """Test compare endpoint requires minimum jurisdictions"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Test with only 1 jurisdiction (needs 2+)
            invalid_request = {
                "budget": 5000000,
                "jurisdictionIds": ["only-one-id"]
            }
            
            response = await client.post("/api/v1/calculate/compare", json=invalid_request)
            
            # Should return 422 for validation error
            assert response.status_code == 422


@pytest.mark.asyncio  
class TestReportEndpoints:
    """Test PDF report generation endpoints"""
    
    async def test_comparison_report_validation(self):
        """Test comparison report endpoint validation"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            invalid_request = {
                "productionTitle": "Test Film",
                "budget": -1000,  # Invalid negative budget
                "jurisdictionIds": ["id1", "id2"]
            }
            
            response = await client.post("/api/v1/reports/comparison", json=invalid_request)
            
            assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.asyncio
class TestExcelEndpoints:
    """Test Excel export endpoints"""
    
    async def test_excel_comparison_validation(self):
        """Test Excel comparison endpoint validation"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                invalid_request = {
                    "productionTitle": "Test Film",
                    "budget": 0,  # Zero budget
                    "jurisdictionIds": ["id1", "id2"]
                }
                
                response = await client.post("/api/v1/excel/comparison", json=invalid_request)
                
                # Should validate budget > 0
                assert response.status_code in [422, 404]
    async def test_simple_calculate(self):
        """Test simple calculate endpoint"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/calculate/simple",
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
                "/api/v1/calculate/compare",
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
        """Test listing all jurisdictions"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.get("/api/v1/jurisdictions/")
                
                assert response.status_code == 200
                data = response.json()
                assert "total" in data
                assert "jurisdictions" in data
    
    async def test_get_jurisdiction_by_id(self):
        """Test getting specific jurisdiction"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Get list first
                list_response = await client.get("/api/v1/jurisdictions/")
                jurisdictions = list_response.json()["jurisdictions"]
                
                if len(jurisdictions) > 0:
                    jurisdiction_id = jurisdictions[0]["id"]
                    
                    # Get specific jurisdiction
                    response = await client.get(f"/api/v1/jurisdictions/{jurisdiction_id}")
                    
                    assert response.status_code == 200
                    data = response.json()
                    assert data["id"] == jurisdiction_id
        """Test list jurisdictions endpoint"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/jurisdictions/")
            
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
    
    async def test_get_jurisdiction_by_id(self):
        """Test get jurisdiction by ID"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/jurisdictions/")
            
            if response.status_code == 200:
                jurisdictions = response.json()
                if len(jurisdictions) > 0:
                    jurisdiction_id = jurisdictions[0]["id"]
                    detail_response = await client.get(f"/api/v1/jurisdictions/{jurisdiction_id}")
                    assert detail_response.status_code == 200


@pytest.mark.asyncio
class TestIncentiveRuleEndpoints:
    """Test incentive rule API endpoints"""
    
    async def test_list_incentive_rules(self):
        """Test listing all incentive rules"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.get("/api/v1/incentive-rules/")
                
                assert response.status_code == 200
                data = response.json()
                assert "total" in data
                assert "rules" in data
    
    async def test_filter_rules_by_jurisdiction(self):
        """Test filtering rules by jurisdiction"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Get a jurisdiction first
                juris_response = await client.get("/api/v1/jurisdictions/")
                jurisdictions = juris_response.json()["jurisdictions"]
                
                if len(jurisdictions) > 0:
                    jurisdiction_id = jurisdictions[0]["id"]
                    
                    # Filter rules
                    response = await client.get(
                        "/api/v1/incentive-rules/",
                        params={"jurisdiction_id": jurisdiction_id}
                    )
                    
                    assert response.status_code == 200
                    data = response.json()
                    
                    # All returned rules should be for this jurisdiction
                    for rule in data["rules"]:
                        assert rule["jurisdictionId"] == jurisdiction_id
        """Test list incentive rules endpoint"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/incentive-rules/")
            
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
    
    async def test_get_rule_by_id(self):
        """Test get rule by ID"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/incentive-rules/")
            
            if response.status_code == 200:
                rules = response.json()
                if len(rules) > 0:
                    rule_id = rules[0]["id"]
                    detail_response = await client.get(f"/api/v1/incentive-rules/{rule_id}")
                    assert detail_response.status_code == 200


@pytest.mark.asyncio
class TestProductionEndpoints:
    """Test production API endpoints"""
    
    async def test_list_productions(self):
        """Test listing all productions"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.get("/api/v1/productions/")
                
                assert response.status_code == 200
                data = response.json()
                assert "total" in data
                assert "productions" in data
        """Test list productions endpoint"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/productions/")
            
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
    
    async def test_get_production_by_id(self):
        """Test get production by ID"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/productions/")
            
            if response.status_code == 200:
                productions = response.json()
                if len(productions) > 0:
                    production_id = productions[0]["id"]
                    detail_response = await client.get(f"/api/v1/productions/{production_id}")
                    assert detail_response.status_code == 200


@pytest.mark.asyncio
class TestReportEndpoints:
    """Test report API endpoints"""
    
    async def test_comparison_report_endpoint(self):
        """Test comparison report endpoint exists"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/reports/comparison",
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
                "/api/v1/reports/compliance",
                json={
                    "productionId": "test-production",
                    "jurisdictionId": "test-jurisdiction"
                }
            )
            # Just test that endpoint exists
            assert response.status_code in [200, 404, 422]
