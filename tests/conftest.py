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

# Connect to database before each test function
@pytest.fixture(scope="function", autouse=True)
def setup_database_for_test(event_loop):
    """
    Setup database for each test using the test's event loop.
    Connects before test and disconnects after.
    """
    # Connect to database in the test's event loop
    if not prisma.is_connected():
        event_loop.run_until_complete(prisma.connect())
    
    yield
    
    # Disconnect after test
    if prisma.is_connected():
        event_loop.run_until_complete(prisma.disconnect())


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