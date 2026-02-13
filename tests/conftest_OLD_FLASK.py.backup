"""
Pytest Configuration and Shared Fixtures
Tax Incentive Compliance Platform
"""
import pytest
import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime, timedelta
import jwt

# Adjust these imports based on your actual app structure
# from app import create_app, db
# from app.models import User, Production, Jurisdiction, IncentiveProgram


# ============================================================================
# CONFIGURATION FIXTURES
# ============================================================================

@pytest.fixture(scope='session')
def test_database_url():
    """Test database URL - uses separate test database"""
    return os.environ.get(
        'TEST_DATABASE_URL',
        'postgresql://postgres:password@localhost:5433/pilotforge_test'
    )


@pytest.fixture(scope='session')
def app(test_database_url):
    """Create Flask application for testing"""
    # Adjust based on your app factory pattern
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': test_database_url,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-secret-key-do-not-use-in-production',
        'JWT_SECRET_KEY': 'test-jwt-secret-key',
        'WTF_CSRF_ENABLED': False,  # Disable CSRF for testing
    })
    
    # Initialize extensions with app
    # db.init_app(app)
    
    with app.app_context():
        # Create all tables
        # db.create_all()
        
        yield app
        
        # Cleanup
        # db.session.remove()
        # db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Flask test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Flask CLI test runner"""
    return app.test_cli_runner()


# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture(scope='function')
def db_session(app):
    """Database session for testing - rolls back after each test"""
    # Adjust based on your db setup
    # connection = db.engine.connect()
    # transaction = connection.begin()
    
    # session = scoped_session(
    #     sessionmaker(bind=connection)
    # )
    # db.session = session
    
    yield None  # Replace with: yield session
    
    # Rollback transaction
    # session.close()
    # transaction.rollback()
    # connection.close()


@pytest.fixture(scope='function')
def clean_db(db_session):
    """Provides a clean database for each test"""
    # Clear all tables
    # meta = db.metadata
    # for table in reversed(meta.sorted_tables):
    #     db.session.execute(table.delete())
    # db.session.commit()
    yield


# ============================================================================
# USER & AUTHENTICATION FIXTURES
# ============================================================================

@pytest.fixture
def test_admin_user(db_session):
    """Create a test admin user"""
    user_data = {
        'email': 'admin@test.com',
        'username': 'admin_test',
        'password_hash': 'hashed_password_here',
        'role': 'admin',
        'is_active': True,
        'created_at': datetime.utcnow()
    }
    # user = User(**user_data)
    # db.session.add(user)
    # db.session.commit()
    # return user
    return user_data


@pytest.fixture
def test_producer_user(db_session):
    """Create a test producer user"""
    user_data = {
        'email': 'producer@test.com',
        'username': 'producer_test',
        'password_hash': 'hashed_password_here',
        'role': 'producer',
        'is_active': True,
        'created_at': datetime.utcnow()
    }
    # user = User(**user_data)
    # db.session.add(user)
    # db.session.commit()
    # return user
    return user_data


@pytest.fixture
def test_accountant_user(db_session):
    """Create a test accountant user"""
    user_data = {
        'email': 'accountant@test.com',
        'username': 'accountant_test',
        'password_hash': 'hashed_password_here',
        'role': 'accountant',
        'is_active': True,
        'created_at': datetime.utcnow()
    }
    return user_data


@pytest.fixture
def admin_token(app, test_admin_user):
    """Generate JWT token for admin user"""
    payload = {
        'user_id': 1,  # test_admin_user.id,
        'role': 'admin',
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token


@pytest.fixture
def producer_token(app, test_producer_user):
    """Generate JWT token for producer user"""
    payload = {
        'user_id': 2,
        'role': 'producer',
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token


@pytest.fixture
def auth_headers_admin(admin_token):
    """Authorization headers for admin user"""
    return {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def auth_headers_producer(producer_token):
    """Authorization headers for producer user"""
    return {
        'Authorization': f'Bearer {producer_token}',
        'Content-Type': 'application/json'
    }


# ============================================================================
# JURISDICTION & INCENTIVE FIXTURES
# ============================================================================

@pytest.fixture
def sample_jurisdictions():
    """Sample jurisdiction data for testing"""
    return [
        {
            'code': 'CA',
            'name': 'California',
            'country': 'USA',
            'type': 'state',
            'is_active': True
        },
        {
            'code': 'NY',
            'name': 'New York',
            'country': 'USA',
            'type': 'state',
            'is_active': True
        },
        {
            'code': 'BC',
            'name': 'British Columbia',
            'country': 'Canada',
            'type': 'province',
            'is_active': True
        },
        {
            'code': 'UK',
            'name': 'United Kingdom',
            'country': 'UK',
            'type': 'country',
            'is_active': True
        }
    ]


@pytest.fixture
def sample_incentive_programs():
    """Sample incentive program data for testing"""
    return [
        {
            'jurisdiction_code': 'CA',
            'program_name': 'California Film & TV Tax Credit 3.0',
            'program_type': 'tax_credit',
            'credit_rate': 0.25,
            'min_spend': 1000000,
            'max_credit': 0,  # No cap
            'labor_requirements': {'ca_labor_percentage': 0.75},
            'is_active': True
        },
        {
            'jurisdiction_code': 'NY',
            'program_name': 'New York Film Tax Credit',
            'program_type': 'tax_credit',
            'credit_rate': 0.30,
            'min_spend': 250000,
            'max_credit': 0,
            'labor_requirements': {'ny_labor_percentage': 0.75},
            'is_active': True
        },
        {
            'jurisdiction_code': 'BC',
            'program_name': 'BC Production Services Tax Credit',
            'program_type': 'tax_credit',
            'credit_rate': 0.35,
            'min_spend': 1000000,
            'max_credit': 0,
            'labor_requirements': {'bc_labor_days': 50},
            'is_active': True
        }
    ]


@pytest.fixture
def create_jurisdictions(db_session, sample_jurisdictions):
    """Create test jurisdictions in database"""
    jurisdictions = []
    for jdata in sample_jurisdictions:
        # jurisdiction = Jurisdiction(**jdata)
        # db.session.add(jurisdiction)
        jurisdictions.append(jdata)
    # db.session.commit()
    return jurisdictions


@pytest.fixture
def create_incentive_programs(db_session, create_jurisdictions, sample_incentive_programs):
    """Create test incentive programs in database"""
    programs = []
    for pdata in sample_incentive_programs:
        # program = IncentiveProgram(**pdata)
        # db.session.add(program)
        programs.append(pdata)
    # db.session.commit()
    return programs


# ============================================================================
# PRODUCTION DATA FIXTURES
# ============================================================================

@pytest.fixture
def sample_production_data():
    """Sample production data for testing compliance"""
    return {
        'title': 'Test Feature Film',
        'production_type': 'feature',
        'budget': 5000000,
        'jurisdiction_code': 'CA',
        'shoot_dates': {
            'start': '2024-03-01',
            'end': '2024-05-15'
        },
        'qualified_spend': {
            'total': 4000000,
            'labor': 3000000,
            'non_labor': 1000000
        },
        'labor_breakdown': {
            'ca_labor': 2250000,
            'non_ca_labor': 750000,
            'ca_labor_percentage': 0.75
        },
        'shoot_days': {
            'ca_days': 45,
            'non_ca_days': 5,
            'total_days': 50
        }
    }


@pytest.fixture
def create_test_production(db_session, test_producer_user, sample_production_data):
    """Create a test production in database"""
    # production = Production(**sample_production_data, user_id=test_producer_user.id)
    # db.session.add(production)
    # db.session.commit()
    # return production
    return sample_production_data


@pytest.fixture
def multi_jurisdiction_production():
    """Production that shoots in multiple jurisdictions"""
    return {
        'title': 'Multi-Location Feature',
        'production_type': 'feature',
        'budget': 15000000,
        'jurisdictions': ['CA', 'NY', 'BC'],
        'qualified_spend_by_jurisdiction': {
            'CA': {'total': 5000000, 'labor': 4000000},
            'NY': {'total': 6000000, 'labor': 4500000},
            'BC': {'total': 3000000, 'labor': 2000000}
        }
    }


# ============================================================================
# COMPLIANCE CALCULATION FIXTURES
# ============================================================================

@pytest.fixture
def compliance_calculator():
    """Mock compliance calculator for testing"""
    class ComplianceCalculator:
        def calculate_incentive(self, production_data, program_data):
            """Calculate incentive based on production and program data"""
            qualified_spend = production_data.get('qualified_spend', {}).get('total', 0)
            credit_rate = program_data.get('credit_rate', 0)
            return qualified_spend * credit_rate
        
        def check_compliance(self, production_data, program_data):
            """Check if production meets program requirements"""
            results = {
                'meets_minimum_spend': False,
                'meets_labor_requirements': False,
                'is_compliant': False,
                'issues': []
            }
            
            # Check minimum spend
            qualified_spend = production_data.get('qualified_spend', {}).get('total', 0)
            min_spend = program_data.get('min_spend', 0)
            results['meets_minimum_spend'] = qualified_spend >= min_spend
            
            # Check labor requirements
            labor_reqs = program_data.get('labor_requirements', {})
            if labor_reqs:
                labor_breakdown = production_data.get('labor_breakdown', {})
                for req_key, req_value in labor_reqs.items():
                    actual_value = labor_breakdown.get(req_key, 0)
                    if actual_value < req_value:
                        results['issues'].append(f"Does not meet {req_key} requirement")
                        results['meets_labor_requirements'] = False
                    else:
                        results['meets_labor_requirements'] = True
            
            results['is_compliant'] = (
                results['meets_minimum_spend'] and 
                results['meets_labor_requirements']
            )
            
            return results
    
    return ComplianceCalculator()


# ============================================================================
# UTILITY FIXTURES
# ============================================================================

@pytest.fixture
def api_version():
    """Current API version"""
    return 'v1'


@pytest.fixture
def base_api_url(api_version):
    """Base API URL for testing"""
    return f'/api/{api_version}'


@pytest.fixture
def mock_audit_logger():
    """Mock audit logger for testing"""
    class AuditLogger:
        def __init__(self):
            self.logs = []
        
        def log(self, user_id, action, resource, details=None):
            self.logs.append({
                'user_id': user_id,
                'action': action,
                'resource': resource,
                'details': details,
                'timestamp': datetime.utcnow()
            })
        
        def get_logs(self):
            return self.logs
        
        def clear(self):
            self.logs = []
    
    return AuditLogger()