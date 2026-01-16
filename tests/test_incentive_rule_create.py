"""
Test incentive rule creation endpoints for PilotForge
> Tax Incentive Intelligence for Film & TV
"""
import pytest
import uuid
from datetime import datetime, timedelta
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from src.main import app
from src.utils.database import prisma


@pytest.mark.asyncio
class TestIncentiveRuleCreate:
    """Test incentive rule creation endpoint"""
    
    async def test_create_incentive_rule_success(self):
        """Test creating an incentive rule successfully"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # First, create a jurisdiction to use
                jurisdiction_code = f"JUR-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Test Jurisdiction for Rules",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                assert juris_response.status_code == 201
                jurisdiction_id = juris_response.json()["id"]
                
                # Now create an incentive rule
                rule_code = f"RULE-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "Test Film Tax Credit",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "percentage": 25.0,
                    "minSpend": 1000000,
                    "maxCredit": 10000000,
                    "eligibleExpenses": ["labor", "equipment", "locations"],
                    "excludedExpenses": ["marketing", "distribution"],
                    "effectiveDate": datetime.now().isoformat(),
                    "expirationDate": (datetime.now() + timedelta(days=365)).isoformat(),
                    "requirements": {
                        "minShootDays": 10,
                        "localHirePercentage": 75
                    },
                    "active": True
                }
                
                response = await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                
                assert response.status_code == 201
                data = response.json()
                assert data["ruleCode"] == rule_code
                assert data["ruleName"] == "Test Film Tax Credit"
                assert data["incentiveType"] == "tax_credit"
                assert data["percentage"] == 25.0
                assert data["jurisdictionId"] == jurisdiction_id
                assert "id" in data
    
    async def test_create_incentive_rule_minimal_fields(self):
        """Test creating incentive rule with only required fields"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Create a jurisdiction first
                jurisdiction_code = f"JUR-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Minimal Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                assert juris_response.status_code == 201
                jurisdiction_id = juris_response.json()["id"]
                
                # Create rule with minimal fields
                rule_code = f"MIN-{str(uuid.uuid4())[:8]}"
                minimal_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "Minimal Rule",
                    "ruleCode": rule_code,
                    "incentiveType": "rebate",
                    "effectiveDate": datetime.now().isoformat()
                }
                
                response = await client.post("/api/0.1.0/incentive-rules/", json=minimal_data)
                
                assert response.status_code == 201
                data = response.json()
                assert data["ruleCode"] == rule_code
                assert data["ruleName"] == "Minimal Rule"
                assert data["active"] is True  # Should default to True
    
    async def test_create_incentive_rule_missing_required_fields(self):
        """Test that missing required fields returns 422 validation error"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Missing 'ruleCode' field
                invalid_data = {
                    "jurisdictionId": "some-id",
                    "ruleName": "Invalid Rule",
                    "incentiveType": "tax_credit",
                    "effectiveDate": datetime.now().isoformat()
                }
                
                response = await client.post("/api/0.1.0/incentive-rules/", json=invalid_data)
                
                assert response.status_code == 422
    
    async def test_create_incentive_rule_invalid_jurisdiction(self):
        """Test that invalid jurisdiction ID returns 404 error"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Use a non-existent jurisdiction ID
                rule_code = f"INVALID-{str(uuid.uuid4())[:8]}"
                invalid_data = {
                    "jurisdictionId": "non-existent-jurisdiction-id",
                    "ruleName": "Invalid Jurisdiction Rule",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "effectiveDate": datetime.now().isoformat()
                }
                
                response = await client.post("/api/0.1.0/incentive-rules/", json=invalid_data)
                
                # Should return 404 for non-existent jurisdiction
                assert response.status_code == 404
    
    async def test_create_incentive_rule_duplicate_code(self):
        """Test that duplicate rule code returns error"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Create a jurisdiction first
                jurisdiction_code = f"JUR-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Duplicate Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                assert juris_response.status_code == 201
                jurisdiction_id = juris_response.json()["id"]
                
                # Create first rule
                rule_code = f"DUP-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "First Rule",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "effectiveDate": datetime.now().isoformat()
                }
                
                response1 = await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                assert response1.status_code == 201
                
                # Try to create second rule with same code
                duplicate_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "Duplicate Rule",
                    "ruleCode": rule_code,  # Same code
                    "incentiveType": "rebate",
                    "effectiveDate": datetime.now().isoformat()
                }
                
                response2 = await client.post("/api/0.1.0/incentive-rules/", json=duplicate_data)
                # Should return 400 for duplicate
                assert response2.status_code == 400
                assert "already exists" in response2.json()["detail"]
    
    async def test_create_incentive_rule_with_percentage(self):
        """Test creating rule with percentage-based incentive"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Create a jurisdiction first
                jurisdiction_code = f"JUR-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Percentage Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                assert juris_response.status_code == 201
                jurisdiction_id = juris_response.json()["id"]
                
                # Create rule with percentage
                rule_code = f"PCT-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "30% Tax Credit",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "percentage": 30.0,
                    "minSpend": 500000,
                    "maxCredit": 5000000,
                    "effectiveDate": datetime.now().isoformat()
                }
                
                response = await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                
                assert response.status_code == 201
                data = response.json()
                assert data["percentage"] == 30.0
                assert data["minSpend"] == 500000
                assert data["maxCredit"] == 5000000
    
    async def test_create_incentive_rule_with_fixed_amount(self):
        """Test creating rule with fixed amount incentive"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Create a jurisdiction first
                jurisdiction_code = f"JUR-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Fixed Amount Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                assert juris_response.status_code == 201
                jurisdiction_id = juris_response.json()["id"]
                
                # Create rule with fixed amount
                rule_code = f"FIX-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "Fixed Grant",
                    "ruleCode": rule_code,
                    "incentiveType": "grant",
                    "fixedAmount": 100000,
                    "effectiveDate": datetime.now().isoformat()
                }
                
                response = await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                
                assert response.status_code == 201
                data = response.json()
                assert data["fixedAmount"] == 100000
                assert data["incentiveType"] == "grant"
