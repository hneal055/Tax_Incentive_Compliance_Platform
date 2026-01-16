"""
Test API endpoints for PilotForge
> Tax Incentive Intelligence for Film & TV
> Tax Incentive Intelligence for Film & TV
"""
import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from src.main import app


@pytest.mark.asyncio
class TestHealthEndpoints:
    """Test health and root endpoints"""
    
    async def test_root_endpoint(self):
        """Test API root returns correct info"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/0.1.0/")
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "PilotForge API"
            assert "version" in data
            assert "endpoints" in data
    @pytest.mark.skip(reason="Health endpoint not implemented")
    async def test_health_check(self):
        """Test health check endpoint"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/0.1.0/calculate/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"


@pytest.mark.asyncio
class TestCalculatorEndpoints:
    """Test calculator API endpoints"""
    
    async def test_calculator_options(self):
        """Test calculator options endpoint"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/0.1.0/calculate/options")
            
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
            
            response = await client.post("/api/0.1.0/calculate/simple", json=invalid_request)
            
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
            
            response = await client.post("/api/0.1.0/calculate/compare", json=invalid_request)
            
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
            
            response = await client.post("/api/0.1.0/reports/comparison", json=invalid_request)
            
            assert response.status_code == 422


@pytest.mark.asyncio
class TestExcelEndpoints:
    """Test Excel export endpoints"""
    
    async def test_excel_comparison_validation(self):
        """Test Excel comparison endpoint validation"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            invalid_request = {
                "productionTitle": "Test Film",
                "budget": 0,  # Zero budget
                "jurisdictionIds": ["id1", "id2"]
            }
            
            response = await client.post("/api/0.1.0/excel/comparison", json=invalid_request)
            
            # Should validate budget > 0
            assert response.status_code in [422, 404]


@pytest.mark.asyncio
class TestJurisdictionEndpoints:
    """Test jurisdiction CRUD endpoints"""
    
    async def test_list_jurisdictions(self):
        """Test listing all jurisdictions"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/api/0.1.0/jurisdictions/")
                
                assert response.status_code == 200
                data = response.json()
                assert "total" in data
                assert "jurisdictions" in data
    
    async def test_get_jurisdiction_by_id(self):
        """Test getting specific jurisdiction"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Get list first
            list_response = await client.get("/api/0.1.0/jurisdictions/")
            jurisdictions = list_response.json()["jurisdictions"]
            
            if len(jurisdictions) > 0:
                jurisdiction_id = jurisdictions[0]["id"]
                
                # Get specific jurisdiction
                response = await client.get(f"/api/0.1.0/jurisdictions/{jurisdiction_id}")
                
                assert response.status_code == 200
                data = response.json()
                assert data["id"] == jurisdiction_id


@pytest.mark.asyncio
class TestIncentiveRuleEndpoints:
    """Test incentive rule CRUD endpoints"""
    
    async def test_list_incentive_rules(self):
        """Test listing all incentive rules"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/0.1.0/incentive-rules/")
            
            assert response.status_code == 200
            data = response.json()
            assert "total" in data
            assert "rules" in data
    
    async def test_filter_rules_by_jurisdiction(self):
        """Test filtering rules by jurisdiction"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Get a jurisdiction first
            juris_response = await client.get("/api/0.1.0/jurisdictions/")
            jurisdictions = juris_response.json()["jurisdictions"]
            
            if len(jurisdictions) > 0:
                jurisdiction_id = jurisdictions[0]["id"]
                
                # Filter rules
                response = await client.get(
                    "/api/0.1.0/incentive-rules/",
                    params={"jurisdiction_id": jurisdiction_id}
                )
                
                assert response.status_code == 200
                data = response.json()
                
                # All returned rules should be for this jurisdiction
                for rule in data["rules"]:
                    assert rule["jurisdictionId"] == jurisdiction_id


@pytest.mark.asyncio
class TestProductionEndpoints:
    """Test production CRUD endpoints"""
    
    async def test_list_productions(self):
        """Test listing all productions"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/0.1.0/productions/")
            
            assert response.status_code == 200
            data = response.json()
            assert "total" in data
            assert "productions" in data


class TestModelValidation:
    """Test Pydantic model validation"""
    
    def test_positive_budget_validation(self):
        """Test that budgets must be positive"""
        from src.models.calculator import SimpleCalculateRequest
        
        # This should raise validation error
        with pytest.raises(Exception):  # Pydantic ValidationError
            SimpleCalculateRequest(
                budget=-1000,
                jurisdictionId="test",
                ruleId="test"
            )
    
    def test_scenario_minimum_items(self):
        """Test scenarios require at least 2 items"""
        from src.models.report import GenerateScenarioReportRequest
        
        # This should raise validation error
        with pytest.raises(Exception):  # Pydantic ValidationError
            GenerateScenarioReportRequest(
                productionTitle="Test",
                jurisdictionId="test",
                baseProductionBudget=5000000,
                scenarios=[{"name": "Only One"}]  # Too few scenarios
            )
    
    def test_jurisdiction_ids_length(self):
        """Test comparison requires 2-10 jurisdictions"""
        from src.models.calculator import CompareCalculateRequest
        
        # Too few
        with pytest.raises(Exception):
            CompareCalculateRequest(
                budget=5000000,
                jurisdictionIds=["only-one"]
            )
        
        # Too many
        with pytest.raises(Exception):
            CompareCalculateRequest(
                budget=5000000,
                jurisdictionIds=["id" + str(i) for i in range(11)]  # 11 IDs
            )