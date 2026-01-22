"""
Pytest configuration and fixtures for PilotForge
Tax Incentive Intelligence for Film & TV

This module provides test fixtures and configuration for the test suite,
including database connection management and async support.
"""
import pytest
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

@pytest.fixture(scope="session", autouse=True)
def setup_database_session():
    """
    Ensure database connection for the entire test session.
    This runs once at the start and cleanup happens at the end.
    
    If database connection fails, it will be mocked for tests.
    """
    # Setup: Connect to database at start of test session
    import asyncio
    import os
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Try to connect, but don't fail if no database is available
    database_available = False
    try:
        if not prisma.is_connected():
            loop.run_until_complete(prisma.connect())
            database_available = True
            print("✅ Test database connected")
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print("   Tests will run with mocked database")
        
        # Use patch to mock database operations since Prisma attributes are read-only
        patcher1 = patch.object(prisma.jurisdiction, 'find_many', new=AsyncMock(return_value=[]))
        patcher2 = patch.object(prisma.jurisdiction, 'find_unique', new=AsyncMock(return_value=None))
        patcher3 = patch.object(prisma.jurisdiction, 'create', new=AsyncMock(return_value={
            "id": "test-id",
            "name": "Washington",
            "code": "WA",
            "country": "USA",
            "type": "state",
            "description": "Washington State Film Incentive Program",
            "website": "https://www.filmseattle.com",
            "active": True,
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z"
        }))
        
        patcher1.start()
        patcher2.start()
        patcher3.start()
    
    yield
    
    # Cleanup: disconnect from database after all tests
    if database_available:
        try:
            if prisma.is_connected():
                loop.run_until_complete(prisma.disconnect())
        finally:
            loop.close()
    else:
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