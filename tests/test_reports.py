"""
Test report generation endpoints for PilotForge
> Tax Incentive Intelligence for Film & TV
"""
import pytest
import uuid
from datetime import datetime
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from src.main import app


@pytest.mark.asyncio
class TestReportEndpoints:
    """Test report generation endpoints"""
    
    async def test_generate_comparison_report_success(self):
        """Test generating a comparison PDF report"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Create 2 jurisdictions with rules
                jurisdiction_ids = []
                
                for i in range(2):
                    jurisdiction_code = f"RPT-{i}-{str(uuid.uuid4())[:6]}"
                    jurisdiction_data = {
                        "name": f"Report Jurisdiction {i+1}",
                        "code": jurisdiction_code,
                        "country": "USA",
                        "type": "state"
                    }
                    juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                    jurisdiction_id = juris_response.json()["id"]
                    jurisdiction_ids.append(jurisdiction_id)
                    
                    # Create rule
                    rule_code = f"RPT-RULE-{i}-{str(uuid.uuid4())[:6]}"
                    rule_data = {
                        "jurisdictionId": jurisdiction_id,
                        "ruleName": f"{(i+1)*20}% Credit",
                        "ruleCode": rule_code,
                        "incentiveType": "tax_credit",
                        "percentage": (i + 1) * 20.0,
                        "effectiveDate": datetime.now().isoformat()
                    }
                    await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                
                # Generate comparison report
                report_request = {
                    "productionTitle": "Test Feature Film",
                    "budget": 5000000,
                    "jurisdictionIds": jurisdiction_ids
                }
                
                response = await client.post("/api/0.1.0/reports/comparison", json=report_request)
                
                assert response.status_code == 200
                assert response.headers["content-type"] == "application/pdf"
                assert "Content-Disposition" in response.headers
                assert "comparison_report" in response.headers["Content-Disposition"]
                # Verify PDF content exists
                assert len(response.content) > 0
    
    async def test_generate_comparison_report_missing_jurisdictions(self):
        """Test that comparison report requires valid jurisdictions"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Use non-existent jurisdiction IDs
                report_request = {
                    "productionTitle": "Test Film",
                    "budget": 5000000,
                    "jurisdictionIds": ["fake-id-1", "fake-id-2"]
                }
                
                response = await client.post("/api/0.1.0/reports/comparison", json=report_request)
                
                assert response.status_code == 404
    
    async def test_generate_compliance_report_success(self):
        """Test generating a compliance PDF report"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Create jurisdiction and rule
                jurisdiction_code = f"COMP-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Compliance Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                jurisdiction_id = juris_response.json()["id"]
                
                # Create rule with requirements
                rule_code = f"COMP-RULE-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "Compliance Test Rule",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "percentage": 25.0,
                    "minSpend": 1000000,
                    "effectiveDate": datetime.now().isoformat(),
                    "requirements": {
                        "minShootDays": 10,
                        "localHirePercentage": 75
                    }
                }
                rule_response = await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                rule_id = rule_response.json()["id"]
                
                # Generate compliance report
                compliance_request = {
                    "productionTitle": "Compliance Test Film",
                    "ruleId": rule_id,
                    "productionBudget": 5000000,
                    "shootDays": 15,
                    "localHirePercentage": 80,
                    "hasPromoLogo": True,
                    "hasCulturalTest": False
                }
                
                response = await client.post("/api/0.1.0/reports/compliance", json=compliance_request)
                
                assert response.status_code == 200
                assert response.headers["content-type"] == "application/pdf"
                assert "Content-Disposition" in response.headers
                assert "compliance_report" in response.headers["Content-Disposition"]
                assert len(response.content) > 0
    
    async def test_generate_compliance_report_invalid_rule(self):
        """Test that compliance report requires valid rule"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Use non-existent rule ID
                compliance_request = {
                    "productionTitle": "Test Film",
                    "ruleId": "fake-rule-id",
                    "productionBudget": 5000000
                }
                
                response = await client.post("/api/0.1.0/reports/compliance", json=compliance_request)
                
                assert response.status_code == 404
    
    async def test_generate_scenario_report_success(self):
        """Test generating a scenario analysis PDF report"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Create jurisdiction and rule
                jurisdiction_code = f"SCEN-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Scenario Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                jurisdiction_id = juris_response.json()["id"]
                
                # Create rule
                rule_code = f"SCEN-RULE-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "Scenario Test Rule",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "percentage": 25.0,
                    "effectiveDate": datetime.now().isoformat()
                }
                await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                
                # Generate scenario report
                scenario_request = {
                    "productionTitle": "Scenario Test Film",
                    "jurisdictionId": jurisdiction_id,
                    "baseProductionBudget": 5000000,
                    "scenarios": [
                        {"name": "Conservative", "budget": 4000000},
                        {"name": "Base", "budget": 5000000},
                        {"name": "Aggressive", "budget": 7000000}
                    ]
                }
                
                response = await client.post("/api/0.1.0/reports/scenario", json=scenario_request)
                
                assert response.status_code == 200
                assert response.headers["content-type"] == "application/pdf"
                assert "Content-Disposition" in response.headers
                assert "scenario_report" in response.headers["Content-Disposition"]
                assert len(response.content) > 0
    
    async def test_generate_scenario_report_invalid_jurisdiction(self):
        """Test that scenario report requires valid jurisdiction"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Use non-existent jurisdiction ID
                scenario_request = {
                    "productionTitle": "Test Film",
                    "jurisdictionId": "fake-jurisdiction-id",
                    "baseProductionBudget": 5000000,
                    "scenarios": [
                        {"name": "Test", "budget": 5000000}
                    ]
                }
                
                response = await client.post("/api/0.1.0/reports/scenario", json=scenario_request)
                
                assert response.status_code == 404
    
    async def test_generate_report_with_multiple_scenarios(self):
        """Test scenario report with multiple budget variations"""
        async with LifespanManager(app):
            async with AsyncClient(app=app, base_url="http://test") as client:
                # Create jurisdiction and rule
                jurisdiction_code = f"MULTI-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Multi Scenario Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                jurisdiction_id = juris_response.json()["id"]
                
                # Create rule with tiered benefits
                rule_code = f"MULTI-RULE-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "Tiered Credit",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "percentage": 30.0,
                    "minSpend": 2000000,
                    "maxCredit": 5000000,
                    "effectiveDate": datetime.now().isoformat()
                }
                await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                
                # Generate report with 5 scenarios
                scenario_request = {
                    "productionTitle": "Multi-Scenario Analysis",
                    "jurisdictionId": jurisdiction_id,
                    "baseProductionBudget": 10000000,
                    "scenarios": [
                        {"name": "Micro", "budget": 1000000},
                        {"name": "Small", "budget": 3000000},
                        {"name": "Medium", "budget": 10000000},
                        {"name": "Large", "budget": 20000000},
                        {"name": "Mega", "budget": 50000000}
                    ]
                }
                
                response = await client.post("/api/0.1.0/reports/scenario", json=scenario_request)
                
                assert response.status_code == 200
                assert response.headers["content-type"] == "application/pdf"
                assert len(response.content) > 0
