"""
Pytest Configuration for FastAPI + Prisma
Tax Incentive Compliance Platform - PilotForge
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.utils.database import prisma
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

@pytest.fixture(scope='session')
def test_database_url():
    '''Test database URL'''
    return os.environ.get(
        'TEST_DATABASE_URL',
        'postgresql://postgres:password@localhost:5433/pilotforge_test'
    )

# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest_asyncio.fixture(scope='session')
async def db():
    '''Database connection for tests'''
    await prisma.connect()
    yield prisma
    await prisma.disconnect()

@pytest_asyncio.fixture(scope='function')
async def clean_db(db):
    '''Clean database before each test'''
    # Delete all data in reverse order of dependencies
    await prisma.production.delete_many()
    await prisma.incentiverule.delete_many()
    await prisma.jurisdiction.delete_many()
    yield
    # Cleanup after test
    await prisma.production.delete_many()
    await prisma.incentiverule.delete_many()
    await prisma.jurisdiction.delete_many()

# ============================================================================
# CLIENT FIXTURES
# ============================================================================

@pytest_asyncio.fixture
async def client():
    '''Async HTTP client for testing'''
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac

# ============================================================================
# SAMPLE DATA FIXTURES
# ============================================================================

@pytest_asyncio.fixture
async def sample_jurisdiction(db, clean_db):
    '''Create sample jurisdiction'''
    jurisdiction = await prisma.jurisdiction.create(
        data={
            'name': 'California',
            'code': 'CA',
            'country': 'USA',
            'type': 'state',
            'description': 'California Film & TV Tax Credit',
            'active': True
        }
    )
    return jurisdiction

@pytest_asyncio.fixture
async def sample_incentive_rule(db, sample_jurisdiction):
    '''Create sample incentive rule'''
    from datetime import datetime, timedelta
    rule = await prisma.incentiverule.create(
        data={
            'jurisdictionId': sample_jurisdiction.id,
            'ruleName': 'California Film Tax Credit 3.0',
            'ruleCode': 'CA_FILM_30',
            'incentiveType': 'tax_credit',
            'percentage': 0.25,
            'minSpend': 1000000.0,
            'eligibleExpenses': ['labor', 'equipment', 'locations'],
            'excludedExpenses': ['marketing', 'distribution'],
            'effectiveDate': datetime.now(),
            'active': True
        }
    )
    return rule

@pytest_asyncio.fixture
async def sample_production(db, sample_jurisdiction):
    '''Create sample production'''
    production = await prisma.production.create(
        data={
            'title': 'Test Feature Film',
            'projectType': 'feature',
            'budget': 5000000.0,
            'jurisdictionId': sample_jurisdiction.id,
            'status': 'active'
        }
    )
    return production

@pytest_asyncio.fixture
async def multiple_jurisdictions(db, clean_db):
    '''Create multiple test jurisdictions'''
    jurisdictions = []
    
    # California
    ca = await prisma.jurisdiction.create(
        data={
            'name': 'California',
            'code': 'CA',
            'country': 'USA',
            'type': 'state',
            'active': True
        }
    )
    jurisdictions.append(ca)
    
    # New York
    ny = await prisma.jurisdiction.create(
        data={
            'name': 'New York',
            'code': 'NY',
            'country': 'USA',
            'type': 'state',
            'active': True
        }
    )
    jurisdictions.append(ny)
    
    # British Columbia
    bc = await prisma.jurisdiction.create(
        data={
            'name': 'British Columbia',
            'code': 'BC',
            'country': 'Canada',
            'type': 'province',
            'active': True
        }
    )
    jurisdictions.append(bc)
    
    return jurisdictions
