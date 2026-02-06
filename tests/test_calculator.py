"""
Test calculator endpoints for PilotForge
> Tax Incentive Intelligence for Film & TV
"""
import pytest
import uuid
from datetime import datetime, timedelta, date
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from src.main import app


@pytest.mark.asyncio
class TestCalculatorEndpoints:
    """Test calculator calculation endpoints"""
    
    async def test_calculate_simple_success(self):
        """Test simple tax credit calculation"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Create jurisdiction and rule first
                jurisdiction_code = f"CALC-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Calculator Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                assert juris_response.status_code == 201
                jurisdiction_id = juris_response.json()["id"]
                
                # Create an incentive rule
                rule_code = f"CALC-RULE-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "25% Tax Credit",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "percentage": 25.0,
                    "minSpend": 1000000,
                    "maxCredit": 10000000,
                    "effectiveDate": datetime.now().isoformat()
                }
                rule_response = await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                assert rule_response.status_code == 201
                rule_id = rule_response.json()["id"]
                
                # Now calculate
                calc_request = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleId": rule_id,
                    "productionBudget": 5000000
                }
                
                response = await client.post("/api/0.1.0/calculate/simple", json=calc_request)
                
                assert response.status_code == 200
                data = response.json()
                assert "estimatedCredit" in data
                assert data["estimatedCredit"] == 1250000  # 25% of 5M
                assert data["meetsMinimumSpend"] is True
    
    async def test_calculate_simple_below_minimum(self):
        """Test calculation when budget is below minimum spend"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Create jurisdiction and rule
                jurisdiction_code = f"MIN-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Minimum Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                jurisdiction_id = juris_response.json()["id"]
                
                rule_code = f"MIN-RULE-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "High Minimum Rule",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "percentage": 30.0,
                    "minSpend": 5000000,
                    "effectiveDate": datetime.now().isoformat()
                }
                rule_response = await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                rule_id = rule_response.json()["id"]
                
                # Calculate with budget below minimum
                calc_request = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleId": rule_id,
                    "productionBudget": 2000000  # Below 5M minimum
                }
                
                response = await client.post("/api/0.1.0/calculate/simple", json=calc_request)
                
                assert response.status_code == 200
                data = response.json()
                assert data["estimatedCredit"] == 0  # Should be 0 due to minimum
                assert data["meetsMinimumSpend"] is False
    
    async def test_calculate_compare_success(self):
        """Test comparing tax credits across jurisdictions"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Create 2 jurisdictions with different rates
                jurisdiction_ids = []
                
                for i, percentage in enumerate([20.0, 30.0]):
                    jurisdiction_code = f"COMP-{i}-{str(uuid.uuid4())[:6]}"
                    jurisdiction_data = {
                        "name": f"Compare Jurisdiction {i+1}",
                        "code": jurisdiction_code,
                        "country": "USA",
                        "type": "state"
                    }
                    juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                    jurisdiction_id = juris_response.json()["id"]
                    jurisdiction_ids.append(jurisdiction_id)
                    
                    # Create rule for this jurisdiction
                    rule_code = f"COMP-RULE-{i}-{str(uuid.uuid4())[:6]}"
                    rule_data = {
                        "jurisdictionId": jurisdiction_id,
                        "ruleName": f"{percentage}% Credit",
                        "ruleCode": rule_code,
                        "incentiveType": "tax_credit",
                        "percentage": percentage,
                        "effectiveDate": datetime.now().isoformat()
                    }
                    await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                
                # Compare jurisdictions
                compare_request = {
                    "productionBudget": 10000000,
                    "jurisdictionIds": jurisdiction_ids
                }
                
                response = await client.post("/api/0.1.0/calculate/compare", json=compare_request)
                
                assert response.status_code == 200
                data = response.json()
                assert "comparisons" in data
                assert len(data["comparisons"]) == 2
                assert "bestOption" in data
                # Best option should be the 30% rule
                assert data["bestOption"]["percentage"] == 30.0
    
    async def test_calculate_compare_invalid_jurisdiction_count(self):
        """Test that compare requires 2-10 jurisdictions"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Test with only 1 jurisdiction (should fail)
                jurisdiction_code = f"ONE-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Single Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                jurisdiction_id = juris_response.json()["id"]
                
                compare_request = {
                    "productionBudget": 5000000,
                    "jurisdictionIds": [jurisdiction_id]  # Only 1
                }
                
                response = await client.post("/api/0.1.0/calculate/compare", json=compare_request)
                
                assert response.status_code == 422
                assert "at least 2" in str(response.json()["detail"])
    
    async def test_calculate_jurisdiction_options(self):
        """Test getting all rules for a jurisdiction with estimates"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Create jurisdiction
                jurisdiction_code = f"OPT-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Options Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                jurisdiction_id = juris_response.json()["id"]
                
                # Create 2 rules
                for i, percentage in enumerate([25.0, 30.0]):
                    rule_code = f"OPT-RULE-{i}-{str(uuid.uuid4())[:6]}"
                    rule_data = {
                        "jurisdictionId": jurisdiction_id,
                        "ruleName": f"{percentage}% Option {i+1}",
                        "ruleCode": rule_code,
                        "incentiveType": "tax_credit",
                        "percentage": percentage,
                        "effectiveDate": datetime.now().isoformat()
                    }
                    await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                
                # Get options
                response = await client.get(
                    f"/api/0.1.0/calculate/jurisdiction/{jurisdiction_id}",
                    params={"budget": 5000000}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert "options" in data
                assert len(data["options"]) == 2
                assert "bestOption" in data
    
    async def test_calculate_with_qualifying_budget_override(self):
        """Test calculation with qualifying budget override"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Create jurisdiction and rule
                jurisdiction_code = f"QUAL-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Qualifying Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                jurisdiction_id = juris_response.json()["id"]
                
                rule_code = f"QUAL-RULE-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "Qualifying Budget Test",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "percentage": 25.0,
                    "effectiveDate": datetime.now().isoformat()
                }
                rule_response = await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                rule_id = rule_response.json()["id"]
                
                # Calculate with qualifying budget override
                calc_request = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleId": rule_id,
                    "productionBudget": 10000000,
                    "qualifyingBudget": 8000000  # 80% qualifies
                }
                
                response = await client.post("/api/0.1.0/calculate/simple", json=calc_request)
                
                assert response.status_code == 200
                data = response.json()
                assert data["qualifyingBudget"] == 8000000
                assert data["estimatedCredit"] == 2000000  # 25% of 8M
