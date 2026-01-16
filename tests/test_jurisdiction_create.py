"""
Test jurisdiction creation endpoints for PilotForge
> Tax Incentive Intelligence for Film & TV
"""
import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.mark.asyncio
class TestJurisdictionCreate:
    """Test jurisdiction creation endpoint"""
    
    async def test_create_jurisdiction_success(self):
        """Test creating a jurisdiction successfully"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Use UUID to ensure unique code
            unique_code = f"TST-{str(uuid.uuid4())[:8]}"
            
            jurisdiction_data = {
                "name": "Test Jurisdiction",
                "code": unique_code,
                "country": "USA",
                "type": "state",
                "description": "Test jurisdiction for automated testing",
                "website": "https://test.example.gov",
                "active": True
            }
            
            response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
            
            assert response.status_code == 201
            data = response.json()
            assert data["code"] == unique_code
            assert data["name"] == "Test Jurisdiction"
            assert data["country"] == "USA"
            assert data["type"] == "state"
            assert "id" in data
    
    async def test_create_jurisdiction_minimal_fields(self):
        """Test creating jurisdiction with only required fields"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Use UUID to ensure unique code
            unique_code = f"MIN-{str(uuid.uuid4())[:8]}"
            
            minimal_data = {
                "name": "Minimal Test Jurisdiction",
                "code": unique_code,
                "country": "USA",
                "type": "state"
            }
            
            response = await client.post("/api/0.1.0/jurisdictions/", json=minimal_data)
            
            assert response.status_code == 201
            data = response.json()
            assert data["code"] == unique_code
            assert data["name"] == "Minimal Test Jurisdiction"
            assert data["active"] is True  # Should default to True
    
    async def test_create_jurisdiction_missing_required_fields(self):
        """Test that missing required fields returns 422 validation error"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Missing 'code' field
            invalid_data = {
                "name": "Invalid Jurisdiction",
                "country": "USA",
                "type": "state"
            }
            
            response = await client.post("/api/0.1.0/jurisdictions/", json=invalid_data)
            
            assert response.status_code == 422
    
    async def test_create_jurisdiction_missing_name(self):
        """Test that missing name field returns 422 validation error"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Missing 'name' field
            unique_code = f"ERR-{str(uuid.uuid4())[:8]}"
            
            invalid_data = {
                "code": unique_code,
                "country": "USA",
                "type": "state"
            }
            
            response = await client.post("/api/0.1.0/jurisdictions/", json=invalid_data)
            
            assert response.status_code == 422
    
    async def test_create_jurisdiction_duplicate_code(self):
        """Test that duplicate jurisdiction code returns error"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Use UUID to ensure unique code
            unique_code = f"DUP-{str(uuid.uuid4())[:8]}"
            
            jurisdiction_data = {
                "name": "First Jurisdiction",
                "code": unique_code,
                "country": "USA",
                "type": "state"
            }
            
            # First creation should succeed
            response1 = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
            assert response1.status_code == 201
            
            # Second creation with same code should fail
            duplicate_data = {
                "name": "Duplicate Jurisdiction",
                "code": unique_code,  # Same code
                "country": "Canada",
                "type": "province"
            }
            
            response2 = await client.post("/api/0.1.0/jurisdictions/", json=duplicate_data)
            # Should return 400 or 409 for duplicate
            assert response2.status_code in [400, 409, 422]
