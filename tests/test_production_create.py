"""
Test production creation endpoints for PilotForge
> Tax Incentive Intelligence for Film & TV
"""
import pytest
import uuid
from datetime import datetime, timedelta, date
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from src.main import app


@pytest.mark.asyncio
class TestProductionCreate:
    """Test production creation endpoint"""
    
    async def test_create_production_success(self):
        """Test creating a production successfully"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # First, create a jurisdiction
                jurisdiction_code = f"PROD-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Production Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                assert juris_response.status_code == 201
                jurisdiction_id = juris_response.json()["id"]
                
                # Now create a production
                production_data = {
                    "title": "Test Feature Film",
                    "productionType": "feature",
                    "jurisdictionId": jurisdiction_id,
                    "budgetTotal": 5000000,
                    "budgetQualifying": 4500000,
                    "startDate": date.today().isoformat(),
                    "endDate": (date.today() + timedelta(days=90)).isoformat(),
                    "productionCompany": "Test Productions LLC",
                    "status": "pre_production",
                    "contact": {"email": "producer@testproductions.com", "phone": "555-1234"}
                }
                
                response = await client.post("/api/0.1.0/productions/", json=production_data)
                
                assert response.status_code == 201
                data = response.json()
                assert data["title"] == "Test Feature Film"
                assert data["productionType"] == "feature"
                assert data["jurisdictionId"] == jurisdiction_id
                assert data["budgetTotal"] == 5000000
                assert "id" in data
    
    async def test_create_production_minimal_fields(self):
        """Test creating production with only required fields"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Create jurisdiction first
                jurisdiction_code = f"MIN-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Minimal Production Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                assert juris_response.status_code == 201
                jurisdiction_id = juris_response.json()["id"]
                
                # Create production with minimal fields
                minimal_data = {
                    "title": "Minimal Production",
                    "productionType": "tv_series",
                    "jurisdictionId": jurisdiction_id,
                    "budgetTotal": 1000000,
                    "startDate": date.today().isoformat(),
                    "productionCompany": "Minimal Productions",
                    "status": "development"
                }
                
                response = await client.post("/api/0.1.0/productions/", json=minimal_data)
                
                assert response.status_code == 201
                data = response.json()
                assert data["title"] == "Minimal Production"
                assert data["productionType"] == "tv_series"
    
    async def test_create_production_missing_required_fields(self):
        """Test that missing required fields returns 422 validation error"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Missing 'title' field
                invalid_data = {
                    "productionType": "feature",
                    "jurisdictionId": "some-id",
                    "budgetTotal": 1000000,
                    "startDate": date.today().isoformat(),
                    "productionCompany": "Test Productions",
                    "status": "development"
                }
                
                response = await client.post("/api/0.1.0/productions/", json=invalid_data)
                
                assert response.status_code == 422
    
    async def test_create_production_invalid_jurisdiction(self):
        """Test that invalid jurisdiction ID returns 404 error"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Use non-existent jurisdiction ID
                invalid_data = {
                    "title": "Invalid Production",
                    "productionType": "feature",
                    "jurisdictionId": "non-existent-jurisdiction-id",
                    "budgetTotal": 1000000,
                    "startDate": date.today().isoformat(),
                    "productionCompany": "Test Productions",
                    "status": "development"
                }
                
                response = await client.post("/api/0.1.0/productions/", json=invalid_data)
                
                # Should return 404 for non-existent jurisdiction
                assert response.status_code == 404
    
    async def test_create_production_various_types(self):
        """Test creating productions of different types"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Create jurisdiction first
                jurisdiction_code = f"TYPE-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Type Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                assert juris_response.status_code == 201
                jurisdiction_id = juris_response.json()["id"]
                
                # Test different production types
                production_types = ["feature", "tv_series", "documentary", "commercial"]
                
                for prod_type in production_types:
                    production_data = {
                        "title": f"Test {prod_type.title()}",
                        "productionType": prod_type,
                        "jurisdictionId": jurisdiction_id,
                        "budgetTotal": 2000000,
                        "startDate": date.today().isoformat(),
                        "productionCompany": "Test Productions",
                        "status": "development"
                    }
                    
                    response = await client.post("/api/0.1.0/productions/", json=production_data)
                    
                    assert response.status_code == 201
                    data = response.json()
                    assert data["productionType"] == prod_type
    
    async def test_create_production_with_budget_breakdown(self):
        """Test creating production with budget breakdown"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Create jurisdiction first
                jurisdiction_code = f"BUD-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Budget Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                assert juris_response.status_code == 201
                jurisdiction_id = juris_response.json()["id"]
                
                # Create production with budget breakdown
                production_data = {
                    "title": "Budget Breakdown Film",
                    "productionType": "feature",
                    "jurisdictionId": jurisdiction_id,
                    "budgetTotal": 10000000,
                    "budgetQualifying": 8500000,
                    "startDate": date.today().isoformat(),
                    "endDate": (date.today() + timedelta(days=120)).isoformat(),
                    "productionCompany": "Big Budget Productions",
                    "status": "production"
                }
                
                response = await client.post("/api/0.1.0/productions/", json=production_data)
                
                assert response.status_code == 201
                data = response.json()
                assert data["budgetTotal"] == 10000000
                assert data["budgetQualifying"] == 8500000
