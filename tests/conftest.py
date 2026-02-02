"""
Pytest configuration and fixtures for PilotForge
Tax Incentive Intelligence for Film & TV

This module provides test fixtures and configuration for the test suite,
including database connection management and async support.
"""
import pytest
import pytest_asyncio
import asyncio
import os
from typing import Generator, AsyncGenerator
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch

# Set test environment variable before importing app
os.environ.setdefault("TESTING", "true")

from src.main import app
from src.utils.database import prisma


# ============================================================================
# Event Loop Configuration
# ============================================================================

@pytest.fixture(scope="function")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Create an event loop for each test function.
    
    This ensures each async test has its own event loop,
    which is the recommended approach for pytest-asyncio.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


# ============================================================================
# Database Connection Management
# ============================================================================

# Connect to database before each test function using the test's event loop
@pytest.fixture(scope="function", autouse=True)
def setup_database_for_test(event_loop):
    """
    Setup database for each test using the test's event loop.
    Ensures the Prisma client can work with the test's async context.
    """
    # Force disconnect if connected to clear old event loop binding
    if prisma.is_connected():
        try:
            # Try to disconnect in a new loop
            import asyncio
            old_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(old_loop)
            old_loop.run_until_complete(prisma.disconnect())
            old_loop.close()
        except:
            pass
    
    # Connect in the test's event loop
    event_loop.run_until_complete(prisma.connect())
    
    yield
    
    # Clean disconnect after test
    try:
        event_loop.run_until_complete(prisma.disconnect())
    except:
        pass


@pytest.fixture(scope="session", autouse=True)
def cleanup_database():
    """
    Final cleanup of database at end of test session.
    """
    yield
    
    # Final cleanup
    import asyncio
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        if prisma.is_connected():
            loop.run_until_complete(prisma.disconnect())
        loop.close()
    except:
        pass



# ============================================================================
# HTTP Client Fixtures
# ============================================================================

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
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Provide an async HTTP client for testing API endpoints.
    
    Usage:
        async def test_endpoint(async_client):
            response = await async_client.get("/api/v1/jurisdictions/")
            assert response.status_code == 200
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


# ============================================================================
# Test Data Cleanup (Optional)
# ============================================================================

@pytest.fixture(autouse=False)
async def clean_test_data():
    """
    Optional fixture to clean up test data between tests.
    
    To use this fixture, add it as a parameter to your test function:
        async def test_something(clean_test_data):
            # Test code here
    
    Note: Set autouse=True if you want this to run for every test.
    """
    yield
    
    # Add cleanup logic here if needed
    # Example: Delete test records created during the test
    # await prisma.production.delete_many(where={"title": {"contains":  "TEST"}})


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """
    Configure pytest with custom markers and settings.
    """
    config.addinivalue_line(
        "markers", "integration:  mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "slow:  mark test as slow running"
    )
