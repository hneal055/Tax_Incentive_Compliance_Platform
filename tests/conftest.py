"""
Test fixtures for PilotForge
> Tax Incentive Intelligence for Film & TV
> Tax Incentive Intelligence for Film & TV
Provides sample data for testing
"""
import pytest
from datetime import datetime, timedelta
from typing import Dict, Any


@pytest.fixture
def sample_jurisdiction() -> Dict[str, Any]:
    """Sample jurisdiction for testing"""
    return {
        "id": "test-jurisdiction-001",
        "name": "Test State",
        "code": "TS",
        "country": "USA",
        "type": "state",
        "description": "Test jurisdiction for unit tests",
        "website": "https://test.gov",
        "active": True
    }


@pytest.fixture
def sample_california_jurisdiction() -> Dict[str, Any]:
    """California jurisdiction"""
    return {
        "id": "bfae464b-9551-4aad-b5e7-2abcf687134e",
        "name": "California",
        "code": "CA",
        "country": "USA",
        "type": "state",
        "active": True
    }


@pytest.fixture
def sample_incentive_rule() -> Dict[str, Any]:
    """Sample incentive rule for testing"""
    return {
        "id": "test-rule-001",
        "jurisdictionId": "test-jurisdiction-001",
        "ruleName": "Test Film Tax Credit",
        "ruleCode": "TEST-FTC-2025",
        "incentiveType": "tax_credit",
        "percentage": 25.0,
        "fixedAmount": None,
        "minSpend": 1000000,
        "maxCredit": 10000000,
        "eligibleExpenses": ["labor", "equipment", "locations"],
        "excludedExpenses": ["marketing", "distribution"],
        "effectiveDate": datetime(2025, 1, 1),
        "expirationDate": datetime(2026, 12, 31),
        "requirements": {
            "minShootDays": 10,
            "localHirePercentage": 75,
            "logoInCredits": True
        },
        "active": True
    }


@pytest.fixture
def sample_stackable_rule() -> Dict[str, Any]:
    """Sample stackable rule with bonuses"""
    return {
        "id": "test-rule-stackable",
        "jurisdictionId": "test-jurisdiction-001",
        "ruleName": "Test Stackable Credit",
        "ruleCode": "TEST-STACK-2025",
        "incentiveType": "stackable_credit",
        "percentage": 25.0,
        "fixedAmount": None,
        "minSpend": 1000000,
        "maxCredit": None,
        "eligibleExpenses": ["labor", "equipment"],
        "excludedExpenses": [],
        "effectiveDate": datetime(2025, 1, 1),
        "expirationDate": None,
        "requirements": {
            "additionalCredits": [
                {"name": "payroll", "percentage": 10.0, "description": "Additional payroll credit"}
            ]
        },
        "active": True
    }


@pytest.fixture
def sample_production() -> Dict[str, Any]:
    """Sample production for testing"""
    return {
        "id": "test-production-001",
        "title": "Test Feature Film",
        "productionType": "feature",
        "jurisdictionId": "test-jurisdiction-001",
        "budgetTotal": 5000000,
        "budgetQualifying": 4500000,
        "startDate": datetime.now(),
        "endDate": datetime.now() + timedelta(days=90),
        "productionCompany": "Test Productions LLC",
        "status": "production",
        "contact": "test@testproductions.com"
    }


@pytest.fixture
def sample_expenses() -> list[Dict[str, Any]]:
    """Sample expenses for testing"""
    return [
        {
            "id": "expense-001",
            "productionId": "test-production-001",
            "category": "labor",
            "description": "Crew wages - Week 1",
            "amount": 500000,
            "expenseDate": datetime.now(),
            "isQualifying": True,
            "vendorName": "Payroll Services"
        },
        {
            "id": "expense-002",
            "productionId": "test-production-001",
            "category": "equipment",
            "description": "Camera rental",
            "amount": 150000,
            "expenseDate": datetime.now(),
            "isQualifying": True,
            "vendorName": "Panavision"
        },
        {
            "id": "expense-003",
            "productionId": "test-production-001",
            "category": "marketing",
            "description": "Advertising",
            "amount": 200000,
            "expenseDate": datetime.now(),
            "isQualifying": False,
            "vendorName": "Marketing Co"
        }
    ]


@pytest.fixture
def sample_comparison_request() -> Dict[str, Any]:
    """Sample comparison request"""
    return {
        "productionTitle": "Test Feature Film",
        "budget": 5000000,
        "jurisdictionIds": ["test-jurisdiction-001", "test-jurisdiction-002"]
    }


@pytest.fixture
def sample_compliance_request() -> Dict[str, Any]:
    """Sample compliance check request"""
    return {
        "productionTitle": "Test Feature Film",
        "ruleId": "test-rule-001",
        "productionBudget": 5000000,
        "shootDays": 45,
        "localHirePercentage": 80,
        "hasPromoLogo": True,
        "hasCulturalTest": False
    }


@pytest.fixture
def sample_scenario_request() -> Dict[str, Any]:
    """Sample scenario analysis request"""
    return {
        "productionTitle": "Test Feature Film",
        "jurisdictionId": "test-jurisdiction-001",
        "baseProductionBudget": 5000000,
        "scenarios": [
            {"name": "Conservative", "budget": 4000000},
            {"name": "Base", "budget": 5000000},
            {"name": "Premium", "budget": 7500000}
        ]
    }


# Calculator test data
@pytest.fixture
def calculator_test_cases() -> list[Dict[str, Any]]:
    """Test cases for calculator logic"""
    return [
        {
            "name": "Basic 25% credit",
            "budget": 5000000,
            "percentage": 25.0,
            "expected_credit": 1250000
        },
        {
            "name": "Credit with max cap",
            "budget": 100000000,
            "percentage": 25.0,
            "max_credit": 10000000,
            "expected_credit": 10000000
        },
        {
            "name": "Below minimum spend",
            "budget": 500000,
            "percentage": 25.0,
            "min_spend": 1000000,
            "expected_credit": 0
        },
        {
            "name": "Fixed amount credit",
            "budget": 5000000,
            "fixed_amount": 500000,
            "expected_credit": 500000
        },
        {
            "name": "Stackable credits",
            "budget": 5000000,
            "base_percentage": 25.0,
            "bonus_percentage": 10.0,
            "expected_credit": 1750000
        }
    ]


# Async test fixtures for database and event loop
import asyncio
from typing import Generator


@pytest.fixture(scope="function")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for each test function."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    """
    Set up database connection for tests.
    This fixture runs before each test function that needs database access.
    """
    from src.utils.database import prisma
    
    # Connect to database
    if not prisma.is_connected():
        await prisma.connect()
    
    yield
    
    # Cleanup is handled by the app lifespan, but we can disconnect if needed
    # Note: We don't disconnect here to allow connection pooling across tests
