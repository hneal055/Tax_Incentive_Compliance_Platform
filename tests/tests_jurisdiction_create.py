"""
Tests for Jurisdiction Create endpoint
"""
import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app


@pytest. mark.asyncio
class TestJurisdictionCreate: 
    """Test jurisdiction creation endpoint"""
    
    async def test_create_jurisdiction_success(self):
        """Test successfully creating a new jurisdiction"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            new_jurisdiction = {
                "name": "Washington",
                "code": "WA",
                "country": "USA",
                "type": "state",
                "description": "Washington State Film Incentive Program",
                "website": "https://www.filmseattle.com",
                "active": True
            }
            
            response = await client.post("/api/v1/jurisdictions/", json=new_jurisdiction)
            
            # Should return 201 Created
            assert response.status_code == 201
            
            data = response.json()
            
            # Verify returned data
            assert data["name"] == "Washington"
            assert data["code"] == "WA"
            assert data["country"] == "USA"
            assert data["type"] == "state"
            assert data["description"] == "Washington State Film Incentive Program"
            assert data["website"] == "https://www.filmseattle.com"
            assert data["active"] is True
            
            # Verify generated fields
            assert "id" in data
            assert data["id"] is not None
            assert "createdAt" in data
            assert "updatedAt" in data
    
    async def test_create_jurisdiction_minimal_fields(self):
        """Test creating jurisdiction with only required fields"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            new_jurisdiction = {
                "name": "Oregon",
                "code": "OR",
                "country": "USA",
                "type": "state"
            }
            
            response = await client.post("/api/v1/jurisdictions/", json=new_jurisdiction)
            
            assert response.status_code == 201
            
            data = response.json()
            assert data["name"] == "Oregon"
            assert data["code"] == "OR"
            assert data["description"] is None  # Optional field should be null
            assert data["website"] is None
            assert data["active"] is True  # Default value
    
    async def test_create_jurisdiction_duplicate_code(self):
        """Test creating jurisdiction with duplicate code fails"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Create first jurisdiction
            first_jurisdiction = {
                "name": "Texas",
                "code": "TX",
                "country": "USA",
                "type": "state"
            }
            
            response1 = await client.post("/api/v1/jurisdictions/", json=first_jurisdiction)
            assert response1.status_code == 201
            
            # Try to create duplicate
            duplicate_jurisdiction = {
                "name": "Texas Again",
                "code": "TX",  # Same code
                "country": "USA",
                "type": "state"
            }
            
            response2 = await client.post("/api/v1/jurisdictions/", json=duplicate_jurisdiction)
            
            # Should return 400 Bad Request
            assert response2.status_code == 400
            
            data = response2.json()
            assert "detail" in data
            assert "already exists" in data["detail"]. lower()
    
    async def test_create_jurisdiction_missing_required_fields(self):
        """Test creating jurisdiction without required fields fails"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            incomplete_jurisdiction = {
                "name": "Florida",
                # Missing required fields:  code, country, type
            }
            
            response = await client.post("/api/v1/jurisdictions/", json=incomplete_jurisdiction)
            
            # Should return 422 Validation Error
            assert response.status_code == 422
            
            data = response.json()
            assert "detail" in data
    
    async def test_create_jurisdiction_invalid_field_types(self):
        """Test creating jurisdiction with invalid field types fails"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            invalid_jurisdiction = {
                "name": "Nevada",
                "code": "NV",
                "country": "USA",
                "type": "state",
                "active": "yes"  # Should be boolean
            }
            
            response = await client.post("/api/v1/jurisdictions/", json=invalid_jurisdiction)
            
            # Should return 422 Validation Error
            assert response.status_code == 422
    
    async def test_create_jurisdiction_case_insensitive_code_check(self):
        """Test that duplicate code check is case-insensitive"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Create jurisdiction with lowercase code
            first_jurisdiction = {
                "name": "Arizona",
                "code": "az",
                "country": "USA",
                "type": "state"
            }
            
            response1 = await client.post("/api/v1/jurisdictions/", json=first_jurisdiction)
            assert response1.status_code == 201
            
            # Try to create with uppercase code
            duplicate_jurisdiction = {
                "name": "Arizona Again",
                "code": "AZ",  # Different case, same code
                "country": "USA",
                "type": "state"
            }
            
            response2 = await client.post("/api/v1/jurisdictions/", json=duplicate_jurisdiction)
            
            # Should fail due to case-insensitive duplicate check
            assert response2.status_code == 400
    
    async def test_create_jurisdiction_with_all_optional_fields(self):
        """Test creating jurisdiction with all optional fields populated"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            complete_jurisdiction = {
                "name": "British Columbia",
                "code": "BC",
                "country": "Canada",
                "type": "province",
                "description": "BC Film Incentive - One of Canada's premier filming locations",
                "website": "https://www.creativebc.com",
                "active": True
            }
            
            response = await client.post("/api/v1/jurisdictions/", json=complete_jurisdiction)
            
            assert response.status_code == 201
            
            data = response.json()
            assert data["name"] == "British Columbia"
            assert data["code"] == "BC"
            assert data["country"] == "Canada"
            assert data["type"] == "province"
            assert data["description"] == "BC Film Incentive - One of Canada's premier filming locations"
            assert data["website"] == "https://www.creativebc.com"
            assert data["active"] is True
    
    async def test_create_jurisdiction_inactive(self):
        """Test creating an inactive jurisdiction"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            inactive_jurisdiction = {
                "name": "Old Program",
                "code": "OLD",
                "country": "USA",
                "type": "state",
                "active": False
            }
            
            response = await client.post("/api/v1/jurisdictions/", json=inactive_jurisdiction)
            
            assert response.status_code == 201
            
            data = response. json()
            assert data["active"] is False
    
    async def test_create_jurisdiction_and_verify_in_list(self):
        """Test that created jurisdiction appears in list"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Create jurisdiction
            new_jurisdiction = {
                "name": "Colorado",
                "code": "CO",
                "country": "USA",
                "type": "state"
            }
            
            create_response = await client.post("/api/v1/jurisdictions/", json=new_jurisdiction)
            assert create_response.status_code == 201
            
            created_id = create_response.json()["id"]
            
            # Verify it appears in the list
            list_response = await client.get("/api/v1/jurisdictions/")
            assert list_response.status_code == 200
            
            jurisdictions = list_response.json()["jurisdictions"]
            jurisdiction_ids = [j["id"] for j in jurisdictions]
            
            assert created_id in jurisdiction_ids
    
    async def test_create_jurisdiction_and_retrieve_by_id(self):
        """Test creating and then retrieving jurisdiction by ID"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Create jurisdiction
            new_jurisdiction = {
                "name": "New Mexico",
                "code": "NM",
                "country": "USA",
                "type": "state",
                "description": "New Mexico Film Office Incentive"
            }
            
            create_response = await client.post("/api/v1/jurisdictions/", json=new_jurisdiction)
            assert create_response.status_code == 201
            
            created_data = create_response.json()
            created_id = created_data["id"]
            
            # Retrieve by ID
            get_response = await client.get(f"/api/v1/jurisdictions/{created_id}")
            assert get_response.status_code == 200
            
            retrieved_data = get_response.json()
            
            # Verify data matches
            assert retrieved_data["id"] == created_id
            assert retrieved_data["name"] == "New Mexico"
            assert retrieved_data["code"] == "NM"
            assert retrieved_data["description"] == "New Mexico Film Office Incentive"