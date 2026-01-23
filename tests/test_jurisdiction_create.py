"""
Tests for Jurisdiction Create endpoint
"""
import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app


@pytest.mark.asyncio
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
            
            response = await client.post("/api/0.1.0/jurisdictions/", json=new_jurisdiction)
            
            # Should return 201 Created
            assert response.status_code == 201
            
            data = response.json()
            
            # Verify returned data
            assert data["name"] == "Washington"
            assert data["code"] == "WA"
            assert data["country"] == "USA"
            assert data["type"] == "state"
            assert data["active"] is True
            
            # Verify generated fields
            assert "id" in data
            assert data["id"] is not None
            assert "createdAt" in data
            assert "updatedAt" in data
