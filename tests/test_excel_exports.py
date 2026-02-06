"""
Test Excel export endpoints for PilotForge
> Tax Incentive Intelligence for Film & TV
"""
import pytest
import uuid
from datetime import datetime
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from src.main import app


@pytest.mark.asyncio
class TestExcelExports:
    """Test Excel export endpoints"""
    
    async def test_export_comparison_excel_success(self):
        """Test generating comparison Excel workbook"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Create 2 jurisdictions with rules
                jurisdiction_ids = []
                
                for i, percentage in enumerate([20.0, 30.0]):
                    jurisdiction_code = f"XLS-{i}-{str(uuid.uuid4())[:6]}"
                    jurisdiction_data = {
                        "name": f"Excel Jurisdiction {i+1}",
                        "code": jurisdiction_code,
                        "country": "USA",
                        "type": "state"
                    }
                    juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                    assert juris_response.status_code == 201
                    jurisdiction_id = juris_response.json()["id"]
                    jurisdiction_ids.append(jurisdiction_id)
                    
                    # Create rule
                    rule_code = f"XLS-RULE-{i}-{str(uuid.uuid4())[:6]}"
                    rule_data = {
                        "jurisdictionId": jurisdiction_id,
                        "ruleName": f"{percentage}% Excel Credit",
                        "ruleCode": rule_code,
                        "incentiveType": "tax_credit",
                        "percentage": percentage,
                        "effectiveDate": datetime.now().isoformat()
                    }
                    await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                
                # Export comparison to Excel
                export_request = {
                    "productionTitle": "Excel Test Film",
                    "budget": 5000000,
                    "jurisdictionIds": jurisdiction_ids
                }
                
                response = await client.post("/api/0.1.0/excel/comparison", json=export_request)
                
                assert response.status_code == 200
                assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                assert "Content-Disposition" in response.headers
                assert "comparison_" in response.headers["Content-Disposition"]
                assert ".xlsx" in response.headers["Content-Disposition"]
                # Verify Excel content exists
                assert len(response.content) > 0
    
    async def test_export_comparison_excel_missing_jurisdictions(self):
        """Test that comparison Excel requires valid jurisdictions"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Use non-existent jurisdiction IDs
                export_request = {
                    "productionTitle": "Test Film",
                    "budget": 5000000,
                    "jurisdictionIds": ["fake-id-1", "fake-id-2"]
                }
                
                response = await client.post("/api/0.1.0/excel/comparison", json=export_request)
                
                assert response.status_code == 404
    
    async def test_export_compliance_excel_success(self):
        """Test generating compliance Excel workbook"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Create jurisdiction and rule
                jurisdiction_code = f"XLS-COMP-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Excel Compliance Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                assert juris_response.status_code == 201
                jurisdiction_id = juris_response.json()["id"]
                
                # Create rule with requirements
                rule_code = f"XLS-COMP-RULE-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "Excel Compliance Test Rule",
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
                assert rule_response.status_code == 201
                rule_id = rule_response.json()["id"]
                
                # Export compliance to Excel
                compliance_request = {
                    "productionTitle": "Excel Compliance Film",
                    "ruleId": rule_id,
                    "productionBudget": 5000000,
                    "shootDays": 15,
                    "localHirePercentage": 80,
                    "hasPromoLogo": True,
                    "hasCulturalTest": False
                }
                
                response = await client.post("/api/0.1.0/excel/compliance", json=compliance_request)
                
                assert response.status_code == 200
                assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                assert "Content-Disposition" in response.headers
                assert "compliance_" in response.headers["Content-Disposition"]
                assert ".xlsx" in response.headers["Content-Disposition"]
                assert len(response.content) > 0
    
    async def test_export_compliance_excel_invalid_rule(self):
        """Test that compliance Excel requires valid rule"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Use non-existent rule ID
                compliance_request = {
                    "productionTitle": "Test Film",
                    "ruleId": "fake-rule-id",
                    "productionBudget": 5000000
                }
                
                response = await client.post("/api/0.1.0/excel/compliance", json=compliance_request)
                
                assert response.status_code == 404
    
    async def test_export_scenario_excel_success(self):
        """Test generating scenario analysis Excel workbook"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Create jurisdiction and rule
                jurisdiction_code = f"XLS-SCEN-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Excel Scenario Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                assert juris_response.status_code == 201
                jurisdiction_id = juris_response.json()["id"]
                
                # Create rule
                rule_code = f"XLS-SCEN-RULE-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "Excel Scenario Test Rule",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "percentage": 25.0,
                    "effectiveDate": datetime.now().isoformat()
                }
                await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                
                # Export scenario analysis to Excel
                scenario_request = {
                    "productionTitle": "Excel Scenario Film",
                    "jurisdictionId": jurisdiction_id,
                    "baseProductionBudget": 5000000,
                    "scenarios": [
                        {"name": "Conservative", "budget": 4000000},
                        {"name": "Base", "budget": 5000000},
                        {"name": "Aggressive", "budget": 7000000}
                    ]
                }
                
                response = await client.post("/api/0.1.0/excel/scenario", json=scenario_request)
                
                assert response.status_code == 200
                assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                assert "Content-Disposition" in response.headers
                assert "scenario_" in response.headers["Content-Disposition"]
                assert ".xlsx" in response.headers["Content-Disposition"]
                assert len(response.content) > 0
    
    async def test_export_scenario_excel_invalid_jurisdiction(self):
        """Test that scenario Excel requires valid jurisdiction"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Use non-existent jurisdiction ID
                scenario_request = {
                    "productionTitle": "Test Film",
                    "jurisdictionId": "fake-jurisdiction-id",
                    "baseProductionBudget": 5000000,
                    "scenarios": [
                        {"name": "Test", "budget": 5000000}
                    ]
                }
                
                response = await client.post("/api/0.1.0/excel/scenario", json=scenario_request)
                
                assert response.status_code == 422
    
    async def test_export_comparison_excel_with_multiple_jurisdictions(self):
        """Test Excel export with multiple jurisdictions"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Create 3 jurisdictions with different rates
                jurisdiction_ids = []
                percentages = [15.0, 25.0, 35.0]
                
                for i, percentage in enumerate(percentages):
                    jurisdiction_code = f"XLS-MULTI-{i}-{str(uuid.uuid4())[:6]}"
                    jurisdiction_data = {
                        "name": f"Multi Excel Jurisdiction {i+1}",
                        "code": jurisdiction_code,
                        "country": "USA",
                        "type": "state"
                    }
                    juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                    jurisdiction_id = juris_response.json()["id"]
                    jurisdiction_ids.append(jurisdiction_id)
                    
                    # Create rule
                    rule_code = f"XLS-MULTI-RULE-{i}-{str(uuid.uuid4())[:6]}"
                    rule_data = {
                        "jurisdictionId": jurisdiction_id,
                        "ruleName": f"{percentage}% Multi Credit",
                        "ruleCode": rule_code,
                        "incentiveType": "tax_credit",
                        "percentage": percentage,
                        "effectiveDate": datetime.now().isoformat()
                    }
                    await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                
                # Export comparison
                export_request = {
                    "productionTitle": "Multi Jurisdiction Excel Test",
                    "budget": 10000000,
                    "jurisdictionIds": jurisdiction_ids
                }
                
                response = await client.post("/api/0.1.0/excel/comparison", json=export_request)
                
                assert response.status_code == 200
                assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                assert len(response.content) > 0
    
    async def test_export_scenario_excel_with_multiple_scenarios(self):
        """Test scenario Excel with multiple budget variations"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Create jurisdiction and rule
                jurisdiction_code = f"XLS-MULTI-SCEN-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Multi Scenario Excel Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                jurisdiction_id = juris_response.json()["id"]
                
                # Create rule with tiered benefits
                rule_code = f"XLS-MULTI-SCEN-RULE-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "Tiered Excel Credit",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "percentage": 30.0,
                    "minSpend": 2000000,
                    "maxCredit": 5000000,
                    "effectiveDate": datetime.now().isoformat()
                }
                await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                
                # Export with 5 scenarios
                scenario_request = {
                    "productionTitle": "Multi-Scenario Excel Analysis",
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
                
                response = await client.post("/api/0.1.0/excel/scenario", json=scenario_request)
                
                assert response.status_code == 200
                assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                assert len(response.content) > 0
    
    async def test_export_compliance_excel_with_requirements(self):
        """Test compliance Excel with complex requirements"""
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                # Create jurisdiction and rule
                jurisdiction_code = f"XLS-REQ-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Requirements Excel Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state"
                }
                juris_response = await client.post("/api/0.1.0/jurisdictions/", json=jurisdiction_data)
                jurisdiction_id = juris_response.json()["id"]
                
                # Create rule with multiple requirements
                rule_code = f"XLS-REQ-RULE-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "Complex Requirements Excel Rule",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "percentage": 30.0,
                    "minSpend": 1000000,
                    "maxCredit": 10000000,
                    "effectiveDate": datetime.now().isoformat(),
                    "requirements": {
                        "minShootDays": 15,
                        "localHirePercentage": 80,
                        "georgiaPromo": True,
                        "culturalTest": True
                    }
                }
                rule_response = await client.post("/api/0.1.0/incentive-rules/", json=rule_data)
                rule_id = rule_response.json()["id"]
                
                # Export compliance
                compliance_request = {
                    "productionTitle": "Complex Requirements Excel Film",
                    "ruleId": rule_id,
                    "productionBudget": 5000000,
                    "shootDays": 20,
                    "localHirePercentage": 85,
                    "hasPromoLogo": True,
                    "hasCulturalTest": True
                }
                
                response = await client.post("/api/0.1.0/excel/compliance", json=compliance_request)
                
                assert response.status_code == 200
                assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                assert len(response.content) > 0
