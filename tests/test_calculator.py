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

    # ---------- Existing Tests ----------
    async def test_calculate_simple_success(self):
        """Test simple tax credit calculation"""
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Create jurisdiction and rule first
                jurisdiction_code = f"CALC-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Calculator Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state",
                }
                juris_response = await client.post(
                    "/api/0.1.0/jurisdictions/", json=jurisdiction_data
                )
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
                    "effectiveDate": datetime.now().isoformat(),
                }
                rule_response = await client.post(
                    "/api/0.1.0/incentive-rules/", json=rule_data
                )
                assert rule_response.status_code == 201
                rule_id = rule_response.json()["id"]

                # Now calculate
                calc_request = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleId": rule_id,
                    "productionBudget": 5000000,
                }

                response = await client.post(
                    "/api/0.1.0/calculate/simple", json=calc_request
                )

                assert response.status_code == 200
                data = response.json()
                assert "estimatedCredit" in data
                assert data["estimatedCredit"] == 1250000  # 25% of 5M
                assert data["meetsMinimumSpend"] is True

    async def test_calculate_simple_below_minimum(self):
        """Test calculation when budget is below minimum spend"""
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Create jurisdiction and rule
                jurisdiction_code = f"MIN-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Minimum Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state",
                }
                juris_response = await client.post(
                    "/api/0.1.0/jurisdictions/", json=jurisdiction_data
                )
                jurisdiction_id = juris_response.json()["id"]

                rule_code = f"MIN-RULE-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "High Minimum Rule",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "percentage": 30.0,
                    "minSpend": 5000000,
                    "effectiveDate": datetime.now().isoformat(),
                }
                rule_response = await client.post(
                    "/api/0.1.0/incentive-rules/", json=rule_data
                )
                rule_id = rule_response.json()["id"]

                # Calculate with budget below minimum
                calc_request = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleId": rule_id,
                    "productionBudget": 2000000,  # Below 5M minimum
                }

                response = await client.post(
                    "/api/0.1.0/calculate/simple", json=calc_request
                )

                assert response.status_code == 200
                data = response.json()
                assert data["estimatedCredit"] == 0  # Should be 0 due to minimum
                assert data["meetsMinimumSpend"] is False

    async def test_calculate_compare_success(self):
        """Test comparing tax credits across jurisdictions"""
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Create 2 jurisdictions with different rates
                jurisdiction_ids = []

                for i, percentage in enumerate([20.0, 30.0]):
                    jurisdiction_code = f"COMP-{i}-{str(uuid.uuid4())[:6]}"
                    jurisdiction_data = {
                        "name": f"Compare Jurisdiction {i+1}",
                        "code": jurisdiction_code,
                        "country": "USA",
                        "type": "state",
                    }
                    juris_response = await client.post(
                        "/api/0.1.0/jurisdictions/", json=jurisdiction_data
                    )
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
                        "effectiveDate": datetime.now().isoformat(),
                    }
                    await client.post("/api/0.1.0/incentive-rules/", json=rule_data)

                # Compare jurisdictions
                compare_request = {
                    "productionBudget": 10000000,
                    "jurisdictionIds": jurisdiction_ids,
                }

                response = await client.post(
                    "/api/0.1.0/calculate/compare", json=compare_request
                )

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
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Test with only 1 jurisdiction (should fail)
                jurisdiction_code = f"ONE-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Single Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state",
                }
                juris_response = await client.post(
                    "/api/0.1.0/jurisdictions/", json=jurisdiction_data
                )
                jurisdiction_id = juris_response.json()["id"]

                compare_request = {
                    "productionBudget": 5000000,
                    "jurisdictionIds": [jurisdiction_id],  # Only 1
                }

                response = await client.post(
                    "/api/0.1.0/calculate/compare", json=compare_request
                )

                assert response.status_code == 422
                assert "at least 2" in str(response.json()["detail"])

    async def test_calculate_jurisdiction_options(self):
        """Test getting all rules for a jurisdiction with estimates"""
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Create jurisdiction
                jurisdiction_code = f"OPT-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Options Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state",
                }
                juris_response = await client.post(
                    "/api/0.1.0/jurisdictions/", json=jurisdiction_data
                )
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
                        "effectiveDate": datetime.now().isoformat(),
                    }
                    await client.post("/api/0.1.0/incentive-rules/", json=rule_data)

                # Get options
                response = await client.get(
                    f"/api/0.1.0/calculate/jurisdiction/{jurisdiction_id}",
                    params={"budget": 5000000},
                )

                assert response.status_code == 200
                data = response.json()
                assert "options" in data
                assert len(data["options"]) == 2
                assert "bestOption" in data

    async def test_calculate_with_qualifying_budget_override(self):
        """Test calculation with qualifying budget override"""
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Create jurisdiction and rule
                jurisdiction_code = f"QUAL-{str(uuid.uuid4())[:8]}"
                jurisdiction_data = {
                    "name": "Qualifying Test Jurisdiction",
                    "code": jurisdiction_code,
                    "country": "USA",
                    "type": "state",
                }
                juris_response = await client.post(
                    "/api/0.1.0/jurisdictions/", json=jurisdiction_data
                )
                jurisdiction_id = juris_response.json()["id"]

                rule_code = f"QUAL-RULE-{str(uuid.uuid4())[:8]}"
                rule_data = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleName": "Qualifying Budget Test",
                    "ruleCode": rule_code,
                    "incentiveType": "tax_credit",
                    "percentage": 25.0,
                    "effectiveDate": datetime.now().isoformat(),
                }
                rule_response = await client.post(
                    "/api/0.1.0/incentive-rules/", json=rule_data
                )
                rule_id = rule_response.json()["id"]

                # Calculate with qualifying budget override
                calc_request = {
                    "jurisdictionId": jurisdiction_id,
                    "ruleId": rule_id,
                    "productionBudget": 10000000,
                    "qualifyingBudget": 8000000,  # 80% qualifies
                }

                response = await client.post(
                    "/api/0.1.0/calculate/simple", json=calc_request
                )

                assert response.status_code == 200
                data = response.json()
                assert data["qualifyingBudget"] == 8000000
                assert data["estimatedCredit"] == 2000000  # 25% of 8M

    # ---------- New Stackable Credits Tests ----------

    async def test_stackable_success(self):
        """Test successful stackable calculation with multiple rules"""
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Create jurisdiction
                juris_data = {
                    "name": "Stackable Test",
                    "code": f"STACK-{str(uuid.uuid4())[:8]}",
                    "country": "USA",
                    "type": "state",
                }
                juris_resp = await client.post(
                    "/api/0.1.0/jurisdictions/", json=juris_data
                )
                assert (
                    juris_resp.status_code == 201
                ), f"Jurisdiction creation failed: {juris_resp.text}"
                juris_id = juris_resp.json()["id"]

                # Create two rules
                rule1_data = {
                    "jurisdictionId": juris_id,
                    "ruleName": "Base Credit",
                    "ruleCode": f"BASE-{str(uuid.uuid4())[:8]}",
                    "incentiveType": "tax_credit",  # Changed from "base"
                    "percentage": 20.0,
                    "active": True,
                    "effectiveDate": datetime.now().isoformat(),  # Added
                }
                rule1_resp = await client.post(
                    "/api/0.1.0/incentive-rules/", json=rule1_data
                )
                assert (
                    rule1_resp.status_code == 201
                ), f"Rule1 creation failed: {rule1_resp.text}"
                rule1_id = rule1_resp.json()["id"]

                rule2_data = {
                    "jurisdictionId": juris_id,
                    "ruleName": "Bonus Credit",
                    "ruleCode": f"BONUS-{str(uuid.uuid4())[:8]}",
                    "incentiveType": "tax_credit",  # Changed from "bonus"
                    "percentage": 5.0,
                    "active": True,
                    "effectiveDate": datetime.now().isoformat(),  # Added
                }
                rule2_resp = await client.post(
                    "/api/0.1.0/incentive-rules/", json=rule2_data
                )
                assert (
                    rule2_resp.status_code == 201
                ), f"Rule2 creation failed: {rule2_resp.text}"
                rule2_id = rule2_resp.json()["id"]

                payload = {
                    "productionBudget": 1_000_000,
                    "jurisdictionId": juris_id,
                    "ruleIds": [rule1_id, rule2_id],
                    "qualifyingBudget": 800_000,
                }

                response = await client.post(
                    "/api/0.1.0/calculate/stackable", json=payload
                )
                if response.status_code != 200:
                    print(
                        f"Stackable endpoint response: {response.status_code} - {response.text}"
                    )
                assert response.status_code == 200
                data = response.json()

                assert data["jurisdiction"] == "Stackable Test"
                assert data["jurisdictionId"] == juris_id
                assert data["totalBudget"] == 1_000_000
                assert data["qualifyingBudget"] == 800_000
                assert len(data["components"]) == 2
                # 20% + 5% = 25% of 800k = 200k
                assert data["totalEstimatedCredit"] == 200_000
                assert "notes" in data

                # Check first component
                comp1 = data["components"][0]
                assert comp1["ruleId"] == rule1_id
                assert comp1["ruleName"] == "Base Credit"
                assert comp1["percentage"] == 20.0
                assert comp1["estimatedCredit"] == 160_000
                assert comp1["meetsMinimum"] is True

                # Check second component
                comp2 = data["components"][1]
                assert comp2["ruleId"] == rule2_id
                assert comp2["ruleName"] == "Bonus Credit"
                assert comp2["percentage"] == 5.0
                assert comp2["estimatedCredit"] == 40_000
                assert comp2["meetsMinimum"] is True

    async def test_stackable_single_rule(self):
        """Test stackable with a single rule (should still work)"""
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Create jurisdiction
                juris_data = {
                    "name": "Single Rule Test",
                    "code": f"SINGLE-{str(uuid.uuid4())[:8]}",
                    "country": "USA",
                    "type": "state",
                }
                juris_resp = await client.post(
                    "/api/0.1.0/jurisdictions/", json=juris_data
                )
                assert juris_resp.status_code == 201
                juris_id = juris_resp.json()["id"]

                # Create rule
                rule_data = {
                    "jurisdictionId": juris_id,
                    "ruleName": "Only Credit",
                    "ruleCode": f"ONLY-{str(uuid.uuid4())[:8]}",
                    "incentiveType": "tax_credit",
                    "percentage": 15.0,
                    "active": True,
                    "effectiveDate": datetime.now().isoformat(),
                }
                rule_resp = await client.post(
                    "/api/0.1.0/incentive-rules/", json=rule_data
                )
                assert rule_resp.status_code == 201
                rule_id = rule_resp.json()["id"]

                payload = {
                    "productionBudget": 500_000,
                    "jurisdictionId": juris_id,
                    "ruleIds": [rule_id],
                }

                response = await client.post(
                    "/api/0.1.0/calculate/stackable", json=payload
                )
                assert response.status_code == 200
                data = response.json()
                assert len(data["components"]) == 1
                assert data["totalEstimatedCredit"] == 75_000  # 15% of 500k
                assert data["components"][0]["estimatedCredit"] == 75_000

    async def test_stackable_with_min_spend_not_met(self):
        """Test rules with minimum spend requirement not met"""
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Create jurisdiction
                juris_data = {
                    "name": "Min Spend Test",
                    "code": f"MIN-{str(uuid.uuid4())[:8]}",
                    "country": "USA",
                    "type": "state",
                }
                juris_resp = await client.post(
                    "/api/0.1.0/jurisdictions/", json=juris_data
                )
                juris_id = juris_resp.json()["id"]

                # Create rule with high minimum spend
                rule_data = {
                    "jurisdictionId": juris_id,
                    "ruleName": "High Min Credit",
                    "ruleCode": f"HIGH-{str(uuid.uuid4())[:8]}",
                    "incentiveType": "tax_credit",
                    "percentage": 25.0,
                    "minSpend": 1_000_000,
                    "active": True,
                    "effectiveDate": datetime.now().isoformat(),
                }
                rule_resp = await client.post(
                    "/api/0.1.0/incentive-rules/", json=rule_data
                )
                assert rule_resp.status_code == 201
                rule_id = rule_resp.json()["id"]

                payload = {
                    "productionBudget": 500_000,  # below minimum
                    "jurisdictionId": juris_id,
                    "ruleIds": [rule_id],
                }

                response = await client.post(
                    "/api/0.1.0/calculate/stackable", json=payload
                )
                assert response.status_code == 200
                data = response.json()
                comp = data["components"][0]
                assert comp["estimatedCredit"] == 0
                assert comp["meetsMinimum"] is False
                assert any(
                    "does not meet minimum" in note.lower() for note in comp["notes"]
                )

    async def test_stackable_with_cap(self):
        """Test rule with maximum cap"""
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Create jurisdiction
                juris_data = {
                    "name": "Cap Test",
                    "code": f"CAP-{str(uuid.uuid4())[:8]}",
                    "country": "USA",
                    "type": "state",
                }
                juris_resp = await client.post(
                    "/api/0.1.0/jurisdictions/", json=juris_data
                )
                juris_id = juris_resp.json()["id"]

                # Create rule with cap
                rule_data = {
                    "jurisdictionId": juris_id,
                    "ruleName": "Capped Credit",
                    "ruleCode": f"CAP-{str(uuid.uuid4())[:8]}",
                    "incentiveType": "tax_credit",
                    "percentage": 30.0,
                    "maxCredit": 100_000,
                    "active": True,
                    "effectiveDate": datetime.now().isoformat(),
                }
                rule_resp = await client.post(
                    "/api/0.1.0/incentive-rules/", json=rule_data
                )
                assert rule_resp.status_code == 201
                rule_id = rule_resp.json()["id"]

                payload = {
                    "productionBudget": 1_000_000,
                    "jurisdictionId": juris_id,
                    "ruleIds": [rule_id],
                }

                response = await client.post(
                    "/api/0.1.0/calculate/stackable", json=payload
                )
                assert response.status_code == 200
                data = response.json()
                comp = data["components"][0]
                # 30% of 1M = 300k, capped at 100k
                assert comp["estimatedCredit"] == 100_000
                assert any("Capped at" in note for note in comp["notes"])

    async def test_stackable_missing_rule(self):
        """Test requesting a rule that doesn't exist"""
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Create jurisdiction
                juris_data = {
                    "name": "Missing Rule Test",
                    "code": f"MISS-{str(uuid.uuid4())[:8]}",
                    "country": "USA",
                    "type": "state",
                }
                juris_resp = await client.post(
                    "/api/0.1.0/jurisdictions/", json=juris_data
                )
                juris_id = juris_resp.json()["id"]

                payload = {
                    "productionBudget": 500_000,
                    "jurisdictionId": juris_id,
                    "ruleIds": ["non-existent-id"],
                }

                response = await client.post(
                    "/api/0.1.0/calculate/stackable", json=payload
                )
                # Our endpoint returns 400 when rules are missing
                assert (
                    response.status_code == 400
                ), f"Expected 400, got {response.status_code}: {response.text}"
                data = response.json()
                assert "detail" in data
                assert (
                    "not found" in data["detail"].lower()
                    or "inactive" in data["detail"].lower()
                )

    async def test_stackable_inactive_rule(self):
        """Test including an inactive rule"""
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Create jurisdiction
                juris_data = {
                    "name": "Inactive Rule Test",
                    "code": f"INACT-{str(uuid.uuid4())[:8]}",
                    "country": "USA",
                    "type": "state",
                }
                juris_resp = await client.post(
                    "/api/0.1.0/jurisdictions/", json=juris_data
                )
                juris_id = juris_resp.json()["id"]

                # Create inactive rule
                rule_data = {
                    "jurisdictionId": juris_id,
                    "ruleName": "Inactive Credit",
                    "ruleCode": f"INACT-{str(uuid.uuid4())[:8]}",
                    "incentiveType": "tax_credit",
                    "percentage": 10.0,
                    "active": False,
                    "effectiveDate": datetime.now().isoformat(),
                }
                rule_resp = await client.post(
                    "/api/0.1.0/incentive-rules/", json=rule_data
                )
                assert rule_resp.status_code == 201
                rule_id = rule_resp.json()["id"]

                payload = {
                    "productionBudget": 500_000,
                    "jurisdictionId": juris_id,
                    "ruleIds": [rule_id],
                }

                response = await client.post(
                    "/api/0.1.0/calculate/stackable", json=payload
                )
                assert (
                    response.status_code == 400
                ), f"Expected 400, got {response.status_code}: {response.text}"
                data = response.json()
                assert "detail" in data
                assert "inactive" in data["detail"].lower()

    async def test_stackable_wrong_jurisdiction(self):
        """Test rule from a different jurisdiction"""
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Create two jurisdictions
                juris1_data = {
                    "name": "Jur A",
                    "code": f"A-{str(uuid.uuid4())[:8]}",
                    "country": "USA",
                    "type": "state",
                }
                juris1_resp = await client.post(
                    "/api/0.1.0/jurisdictions/", json=juris1_data
                )
                juris1_id = juris1_resp.json()["id"]

                juris2_data = {
                    "name": "Jur B",
                    "code": f"B-{str(uuid.uuid4())[:8]}",
                    "country": "USA",
                    "type": "state",
                }
                juris2_resp = await client.post(
                    "/api/0.1.0/jurisdictions/", json=juris2_data
                )
                juris2_id = juris2_resp.json()["id"]

                # Create rule in first jurisdiction
                rule_data = {
                    "jurisdictionId": juris1_id,
                    "ruleName": "Rule A",
                    "ruleCode": f"RULE-{str(uuid.uuid4())[:8]}",
                    "incentiveType": "tax_credit",
                    "percentage": 10.0,
                    "active": True,
                    "effectiveDate": datetime.now().isoformat(),
                }
                rule_resp = await client.post(
                    "/api/0.1.0/incentive-rules/", json=rule_data
                )
                assert rule_resp.status_code == 201
                rule_id = rule_resp.json()["id"]

                # Request with second jurisdiction
                payload = {
                    "productionBudget": 500_000,
                    "jurisdictionId": juris2_id,
                    "ruleIds": [rule_id],
                }

                response = await client.post(
                    "/api/0.1.0/calculate/stackable", json=payload
                )
                assert (
                    response.status_code == 400
                ), f"Expected 400, got {response.status_code}: {response.text}"
                data = response.json()
                assert "detail" in data
                assert (
                    "not found" in data["detail"].lower()
                    or "inactive" in data["detail"].lower()
                )

    async def test_stackable_too_many_rules(self):
        """Test exceeding max rules (should be limited by request model)"""
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Create jurisdiction
                juris_data = {
                    "name": "Many Rules Test",
                    "code": f"MANY-{str(uuid.uuid4())[:8]}",
                    "country": "USA",
                    "type": "state",
                }
                juris_resp = await client.post(
                    "/api/0.1.0/jurisdictions/", json=juris_data
                )
                juris_id = juris_resp.json()["id"]

                # Create 11 rule IDs (they don't need to exist for validation)
                rule_ids = [f"rule-{i}" for i in range(11)]

                payload = {
                    "productionBudget": 500_000,
                    "jurisdictionId": juris_id,
                    "ruleIds": rule_ids,
                }

                response = await client.post(
                    "/api/0.1.0/calculate/stackable", json=payload
                )
                # Should be 422 validation error from Pydantic (max_items=10)
                assert (
                    response.status_code == 422
                ), f"Expected 422, got {response.status_code}: {response.text}"
                data = response.json()
                assert "ruleIds" in str(data)

    async def test_stackable_zero_qualifying_budget(self):
        """Test with zero qualifying budget"""
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                # Create jurisdiction
                juris_data = {
                    "name": "Zero Budget Test",
                    "code": f"ZERO-{str(uuid.uuid4())[:8]}",
                    "country": "USA",
                    "type": "state",
                }
                juris_resp = await client.post(
                    "/api/0.1.0/jurisdictions/", json=juris_data
                )
                juris_id = juris_resp.json()["id"]

                # Create rule
                rule_data = {
                    "jurisdictionId": juris_id,
                    "ruleName": "Zero Credit",
                    "ruleCode": f"ZERO-{str(uuid.uuid4())[:8]}",
                    "incentiveType": "tax_credit",
                    "percentage": 20.0,
                    "active": True,
                    "effectiveDate": datetime.now().isoformat(),
                }
                rule_resp = await client.post(
                    "/api/0.1.0/incentive-rules/", json=rule_data
                )
                assert rule_resp.status_code == 201
                rule_id = rule_resp.json()["id"]

                payload = {
                    "productionBudget": 0,
                    "jurisdictionId": juris_id,
                    "ruleIds": [rule_id],
                }

                response = await client.post(
                    "/api/0.1.0/calculate/stackable", json=payload
                )
                assert response.status_code == 200
                data = response.json()
                assert data["totalEstimatedCredit"] == 0
                # There should be a note about zero budget
                assert any("zero" in note.lower() for note in data["notes"])
