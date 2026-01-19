"""
Pytest configuration and fixtures for PilotForge
Tax Incentive Intelligence for Film & TV

This module provides test fixtures and configuration for the test suite,
including database connection management and async support.
"""
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.utils.database import prisma


# ============================================================================
# Event Loop Configuration
# ============================================================================

@pytest.fixture(scope="function")  # Changed from "session" to "function"
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

@pytest.fixture(scope="function", autouse=False)  # Changed scope and autouse
async def setup_database() -> AsyncGenerator[None, None]: 
    """
    Connect to the database before a test runs.
    Disconnect after the test completes.
    
    Add this fixture as a parameter to tests that need database access: 
        async def test_something(setup_database):
            # Your test code
    """
    # Check if already connected
    if not prisma.is_connected():
        await prisma.connect()
    
    yield
    
    # Note: We don't disconnect here because other tests might need it
    # The connection will be cleaned up when the test session ends


@pytest.fixture(scope="session", autouse=True)
def setup_database_session():
    """
    Ensure database connection for the entire test session.
    This runs once at the start and cleanup happens at the end.
    """
    # Connection happens in individual tests via setup_database
    yield
    
    # Cleanup:  disconnect from database after all tests
    # This uses sync code because session fixtures can't be async
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        if prisma.is_connected():
            loop.run_until_complete(prisma.disconnect())
    finally:
        loop.close()


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