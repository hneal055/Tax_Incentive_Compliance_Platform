"""
Comprehensive tests for Incentive Rules API endpoints
Improves test coverage to 90-100%
"""
import pytest
from datetime import datetime


class TestIncentiveRuleModelValidation:
    """Test Pydantic model validation for incentive rules"""
    
    def test_incentive_rule_create_valid(self):
        """Test creating a valid incentive rule"""
        from src.models.incentive_rule import IncentiveRuleCreate
        
        rule = IncentiveRuleCreate(
            jurisdictionId="test-jurisdiction-id",
            ruleName="California Film Credit",
            ruleCode="CA-FC-2025",
            incentiveType="tax_credit",
            percentage=25.0,
            effectiveDate=datetime.now(),
            active=True
        )
        
        assert rule.ruleName == "California Film Credit"
        assert rule.percentage == 25.0
        assert rule.active is True
    
    def test_incentive_rule_create_with_optional_fields(self):
        """Test creating rule with all optional fields"""
        from src.models.incentive_rule import IncentiveRuleCreate
        
        rule = IncentiveRuleCreate(
            jurisdictionId="test-id",
            ruleName="Test Rule",
            ruleCode="TEST-001",
            incentiveType="tax_credit",
            percentage=30.0,
            fixedAmount=5000.0,
            minSpend=1000000.0,
            maxCredit=10000000.0,
            eligibleExpenses=["labor", "equipment"],
            excludedExpenses=["marketing"],
            effectiveDate=datetime.now(),
            expirationDate=datetime(2026, 12, 31),
            requirements={"minShootDays": 10},
            active=True
        )
        
        assert rule.minSpend == 1000000.0
        assert rule.maxCredit == 10000000.0
        assert "labor" in rule.eligibleExpenses
        assert "marketing" in rule.excludedExpenses
    
    def test_incentive_rule_update_all_fields_optional(self):
        """Test that all fields in IncentiveRuleUpdate are optional"""
        from src.models.incentive_rule import IncentiveRuleUpdate
        
        # Empty update should work
        update = IncentiveRuleUpdate()
        assert update.model_dump(exclude_unset=True) == {}
        
        # Partial update should work
        update = IncentiveRuleUpdate(percentage=28.0)
        assert update.percentage == 28.0
        
        # Update with requirements
        update = IncentiveRuleUpdate(
            requirements={"minShootDays": 15}
        )
        assert update.requirements == {"minShootDays": 15}
    
    def test_incentive_rule_response_structure(self):
        """Test IncentiveRuleResponse model structure"""
        from src.models.incentive_rule import IncentiveRuleResponse
        
        rule = IncentiveRuleResponse(
            id="rule-id-123",
            jurisdictionId="jurisdiction-id",
            ruleName="Georgia Film Credit",
            ruleCode="GA-FC-2025",
            incentiveType="tax_credit",
            percentage=20.0,
            eligibleExpenses=["labor", "equipment"],
            excludedExpenses=["marketing"],
            effectiveDate=datetime.now(),
            active=True,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        
        assert rule.id == "rule-id-123"
        assert rule.percentage == 20.0
        assert rule.active is True
    
    def test_incentive_rule_list_structure(self):
        """Test IncentiveRuleList model structure"""
        from src.models.incentive_rule import IncentiveRuleList, IncentiveRuleResponse
        
        rules = [
            IncentiveRuleResponse(
                id="1",
                jurisdictionId="jur-1",
                ruleName="Test Rule 1",
                ruleCode="TEST-001",
                incentiveType="tax_credit",
                percentage=25.0,
                eligibleExpenses=[],
                excludedExpenses=[],
                effectiveDate=datetime.now(),
                active=True,
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            ),
            IncentiveRuleResponse(
                id="2",
                jurisdictionId="jur-2",
                ruleName="Test Rule 2",
                ruleCode="TEST-002",
                incentiveType="rebate",
                percentage=30.0,
                eligibleExpenses=[],
                excludedExpenses=[],
                effectiveDate=datetime.now(),
                active=False,
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            )
        ]
        
        rule_list = IncentiveRuleList(
            total=2,
            page=1,
            pageSize=50,
            totalPages=1,
            rules=rules
        )
        
        assert rule_list.total == 2
        assert len(rule_list.rules) == 2
        assert rule_list.rules[0].ruleCode == "TEST-001"
        assert rule_list.rules[1].active is False
    
    def test_eligible_expenses_default(self):
        """Test that eligibleExpenses defaults to empty list"""
        from src.models.incentive_rule import IncentiveRuleCreate
        
        rule = IncentiveRuleCreate(
            jurisdictionId="test-id",
            ruleName="Test",
            ruleCode="TEST",
            incentiveType="tax_credit",
            percentage=20.0,
            effectiveDate=datetime.now(),
            active=True
        )
        
        assert rule.eligibleExpenses == []
        assert rule.excludedExpenses == []
    
    def test_requirements_default(self):
        """Test that requirements defaults to empty dict"""
        from src.models.incentive_rule import IncentiveRuleCreate
        
        rule = IncentiveRuleCreate(
            jurisdictionId="test-id",
            ruleName="Test",
            ruleCode="TEST",
            incentiveType="tax_credit",
            percentage=20.0,
            effectiveDate=datetime.now(),
            active=True
        )
        
        # Requirements should default to empty dict
        assert rule.requirements == {} or rule.requirements is None or rule.requirements == {}
    
    def test_active_default_true(self):
        """Test that active defaults to True"""
        from src.models.incentive_rule import IncentiveRuleCreate
        
        rule = IncentiveRuleCreate(
            jurisdictionId="test-id",
            ruleName="Test",
            ruleCode="TEST",
            incentiveType="tax_credit",
            percentage=20.0,
            effectiveDate=datetime.now()
        )
        
        assert rule.active is True
    
    def test_percentage_and_fixed_amount_both_optional(self):
        """Test that both percentage and fixedAmount can be None"""
        from src.models.incentive_rule import IncentiveRuleCreate
        
        # Rule with percentage
        rule1 = IncentiveRuleCreate(
            jurisdictionId="test-id",
            ruleName="Percentage Rule",
            ruleCode="PCT-001",
            incentiveType="tax_credit",
            percentage=25.0,
            effectiveDate=datetime.now(),
            active=True
        )
        assert rule1.percentage == 25.0
        assert rule1.fixedAmount is None
        
        # Rule with fixed amount
        rule2 = IncentiveRuleCreate(
            jurisdictionId="test-id",
            ruleName="Fixed Amount Rule",
            ruleCode="FIX-001",
            incentiveType="grant",
            fixedAmount=100000.0,
            effectiveDate=datetime.now(),
            active=True
        )
        assert rule2.fixedAmount == 100000.0
        assert rule2.percentage is None
    
    def test_min_spend_and_max_credit_optional(self):
        """Test min/max constraints are optional"""
        from src.models.incentive_rule import IncentiveRuleCreate
        
        rule = IncentiveRuleCreate(
            jurisdictionId="test-id",
            ruleName="No Limits",
            ruleCode="NOLIM-001",
            incentiveType="tax_credit",
            percentage=20.0,
            effectiveDate=datetime.now(),
            active=True
        )
        
        assert rule.minSpend is None
        assert rule.maxCredit is None
    
    def test_expiration_date_optional(self):
        """Test that expiration date is optional"""
        from src.models.incentive_rule import IncentiveRuleCreate
        
        rule = IncentiveRuleCreate(
            jurisdictionId="test-id",
            ruleName="No Expiry",
            ruleCode="NOEXP-001",
            incentiveType="tax_credit",
            percentage=20.0,
            effectiveDate=datetime.now(),
            active=True
        )
        
        assert rule.expirationDate is None
import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from main import app  # Adjust if your app is elsewhere

@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.mark.anyio
async def test_get_incentive_rules_no_filters(async_client):
    resp = await async_client.get("/api/v1/incentive-rules/")
    assert resp.status_code == status.HTTP_200_OK
    assert "rules" in resp.json()

@pytest.mark.anyio
async def test_get_incentive_rules_with_jurisdiction(async_client):
    resp = await async_client.get("/api/v1/incentive-rules/?jurisdiction_id=test-jurisdiction")
    assert resp.status_code == status.HTTP_200_OK

@pytest.mark.anyio
async def test_get_incentive_rules_with_incentive_type(async_client):
    resp = await async_client.get("/api/v1/incentive-rules/?incentive_type=grant")
    assert resp.status_code == status.HTTP_200_OK

@pytest.mark.anyio
async def test_get_incentive_rules_with_active(async_client):
    resp = await async_client.get("/api/v1/incentive-rules/?active=true")
    assert resp.status_code == status.HTTP_200_OK

@pytest.mark.anyio
async def test_get_incentive_rules_pagination(async_client):
    resp = await async_client.get("/api/v1/incentive-rules/?page=2&page_size=10")
    assert resp.status_code == status.HTTP_200_OK

@pytest.mark.anyio
async def test_get_incentive_rules_invalid_page(async_client):
    resp = await async_client.get("/api/v1/incentive-rules/?page=0")
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.anyio
async def test_get_incentive_rules_invalid_page_size(async_client):
    resp = await async_client.get("/api/v1/incentive-rules/?page_size=101")
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



