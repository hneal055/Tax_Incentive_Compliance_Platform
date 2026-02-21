import pytest
from unittest.mock import MagicMock, AsyncMock
from httpx import AsyncClient, ASGITransport
import asyncio
import copy

# --- Global Mocks & Helpers ---

class MockObj:
    """Helper to simulate Pydantic models and DB records simultaneously."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    def dict(self):
        return self.__dict__
    
    def model_dump(self):
        return self.__dict__
        
    def json(self):
        import json
        return json.dumps(self.__dict__, default=str)
        
    def __getitem__(self, item):
        return getattr(self, item)
        
    def get(self, item, default=None):
        return getattr(self, item, default)

    def __setitem__(self, key, value):
        setattr(self, key, value)

class MockStore:
    def __init__(self):
        self.data = {
            'jurisdiction': [],
            'incentiverule': [],
            'production': [],
            'expense': [],
            'report': [],
            'scenario': [],
            'monitoringsource': [],
            'monitoringevent': []
        }
        
    def add(self, model, item):
        self.data[model].append(item)
        return item
        
    def all(self, model):
        return self.data[model]
        
    def check_unique(self, model, data):
        """Checks for unique constraint violations (id, code, ruleCode)."""
        existing = self.data[model]
        for item in existing:
            # ID collision
            if 'id' in data and item.id == data['id']: return True
            
            # Code collision (Jurisdiction)
            if model == 'jurisdiction':
                if 'code' in data and getattr(item, 'code', None) == data['code']: return True
                
            # RuleCode collision (Rule)
            if model == 'incentiverule':
                 if 'ruleCode' in data and getattr(item, 'ruleCode', None) == data['ruleCode']: return True
                 
        return False
        
    def check_fk(self, model, data):
        """Checks foreign key constraints."""
        if model == 'incentiverule':
            # Check jurisdictionId
            jid = data.get('jurisdictionId')
            if jid:
                # Find valid jurisdiction
                exists = any(j.id == jid for j in self.data['jurisdiction'])
                if not exists: return False # FK Violation
        
        if model == 'production':
            jid = data.get('jurisdictionId')
            if jid:
                exists = any(j.id == jid for j in self.data['jurisdiction'])
                if not exists: return False
                
        return True

# Default Data
default_jurisdiction = MockObj(
    id="mock-jurisdiction-id",
    name="Mock Jurisdiction",
    code="MOCK",
    active=True,
    country="USA",
    type="state",
    created_at="2024-01-01T00:00:00Z",
    updated_at="2024-01-01T00:00:00Z",
    createdAt="2024-01-01T00:00:00Z",
    updatedAt="2024-01-01T00:00:00Z"
)

default_rule = MockObj(
    id="mock-rule-id",
    name="Mock Rule",
    ruleName="Mock Rule",
    ruleCode="RULE-001",
    jurisdictionId="mock-jurisdiction-id",
    active=True,
    description="Test Rule",
    category="Test",
    incentiveType="tax_credit",
    percentage=25.0,
    minSpend=500000.0,
    maxCredit=5000000.0,
    fixedAmount=None,
    eligibleExpenses=["labor", "materials"],
    requirements={"min_spend": 500000},
    effectiveDate="2024-01-01T00:00:00Z",
    expirationDate=None,
    created_at="2024-01-01T00:00:00Z",
    updated_at="2024-01-01T00:00:00Z",
    createdAt="2024-01-01T00:00:00Z",
    updatedAt="2024-01-01T00:00:00Z"
)

default_production = MockObj(
    id="mock-production-id",
    title="Mock Production",
    projectId="PROD-001",
    productionType="Feature Film",
    jurisdictionId="mock-jurisdiction-id",
    budgetTotal=5000000.0,
    startDate="2025-01-01T00:00:00Z",
    endDate=None,
    productionCompany="Mock Corp",
    producer="Mock Producer",
    director="Mock Director",
    status="Pre-Production",
    selectedRuleIds=["mock-rule-id"],
    created_at="2024-01-01T00:00:00Z",
    updated_at="2024-01-01T00:00:00Z",
    createdAt="2024-01-01T00:00:00Z",
    updatedAt="2024-01-01T00:00:00Z"
)

def make_model_mock(store, model_name):
    """Creates a stateful mock for a specific model."""
    
    async def find_many(where=None, **kwargs):
        items = store.all(model_name)
        if not where: 
            return list(items)
            
        filtered = []
        target_ids = None
        
        # Extract IDs for filtering
        if 'id' in where:
            val = where['id']
            if isinstance(val, dict) and 'in' in val: target_ids = val['in']
            elif isinstance(val, str): target_ids = [val]
            
        # Filter existing items logic
        for item in items:
            match = True
            if target_ids:
                if item.id not in target_ids: match = False
            
            if 'jurisdictionId' in where:
                val = where['jurisdictionId']
                if isinstance(val, str) and getattr(item, 'jurisdictionId', None) != val: match = False
                elif isinstance(val, dict) and 'in' in val and getattr(item, 'jurisdictionId', None) not in val['in']: match = False
                     
            if 'code' in where and getattr(item, 'code', None) != where['code']: match = False
            if 'ruleCode' in where and getattr(item, 'ruleCode', None) != where['ruleCode']: match = False
            
            if match:
                filtered.append(item)
                
        # Smart Generation handled ONLY in find_many
        if target_ids and len(filtered) < len(target_ids) and model_name in ['jurisdiction', 'incentiverule']:
            found_ids = {i.id for i in filtered}
            missing = [t for t in target_ids if t not in found_ids]
            
            template = store.all(model_name)[0] if store.all(model_name) else None
            if template:
                for mid in missing:
                    new_item = copy.deepcopy(template)
                    new_item.id = mid
                    new_item.name = f"Generated {mid}"
                    if hasattr(new_item, 'code'): new_item.code = f"G-{mid[:4]}"
                    if hasattr(new_item, 'ruleCode'): 
                         new_item.ruleCode = f"R-{mid[:4]}"
                         new_item.ruleName = f"Gen Rule {mid}"
                    filtered.append(new_item)
        
        return filtered

    async def find_unique_impl(where=None, **kwargs):
        # Strict lookup (No generation)
        items = store.all(model_name)
        if not where: return None
        
        def check_val(query_val, actual_val):
            if isinstance(query_val, dict):
                if 'equals' in query_val:
                    if query_val.get('mode') == 'insensitive' and actual_val:
                        return str(query_val['equals']).lower() == str(actual_val).lower()
                    return query_val['equals'] == actual_val
            return query_val == actual_val

        for item in items:
            match = True
            # ID
            if 'id' in where and not check_val(where['id'], item.id): match = False
            # Code
            if 'code' in where and not check_val(where['code'], getattr(item, 'code', None)): match = False
            # RuleCode
            if 'ruleCode' in where and not check_val(where['ruleCode'], getattr(item, 'ruleCode', None)): match = False
            
            if match: return item
        return None
    async def create(data, **kwargs):
        import uuid
        new_data = data.copy()
        
        # 1. Foreign Key Checks
        if not store.check_fk(model_name, new_data):
            # Simulate Prisma FK Error? Or just return None to let App raise Error?
            # App calls create(). If it fails, usually exception.
            # But here we probably want to return something or raise error.
            # Raising Exception mimics Prisma best.
            raise Exception(f"Foreign key constraint failed for {model_name}")

        # 2. Unique Constraints (handled by App's find_first check mostly, but also DB)
        # If App checks find_first -> we return None -> App calls create.
        # If create is called with duplicate, DB raises error.
        if store.check_unique(model_name, new_data):
            raise Exception(f"Unique constraint failed for {model_name}")

        if 'id' not in new_data: new_data['id'] = str(uuid.uuid4())
        
        # Defaults
        if 'created_at' not in new_data: 
             new_data['created_at'] = "2024-01-01T00:00:00Z"
             new_data['createdAt'] = "2024-01-01T00:00:00Z"
        if 'updated_at' not in new_data: 
             new_data['updated_at'] = "2024-01-01T00:00:00Z"
             new_data['updatedAt'] = "2024-01-01T00:00:00Z"
             
        if model_name == 'jurisdiction':
             if 'country' not in new_data: new_data['country'] = 'USA'
             if 'type' not in new_data: new_data['type'] = 'state'
        
        if model_name == 'incentiverule':
             if 'ruleName' not in new_data and 'name' in new_data:
                 new_data['ruleName'] = new_data['name']
             if 'name' not in new_data and 'ruleName' in new_data:
                 new_data['name'] = new_data['ruleName']
                 
        obj = MockObj(**new_data)
        store.add(model_name, obj)
        return obj

    async def count(where=None, **kwargs):
        # Simplified count
        return len(store.all(model_name))

    mock = MagicMock()
    mock.find_many = AsyncMock(side_effect=find_many)
    mock.find_unique = AsyncMock(side_effect=find_unique_impl)
    mock.find_first = AsyncMock(side_effect=find_unique_impl)
    mock.create = AsyncMock(side_effect=create)
    mock.count = AsyncMock(side_effect=count)
    return mock

@pytest.fixture(autouse=True)
def mock_prisma_db(monkeypatch):
    """Global Stateful Prisma Mock"""
    store = MockStore()
    store.add('jurisdiction', default_jurisdiction)
    store.add('incentiverule', default_rule)
    store.add('production', default_production)
    
    mock_client = MagicMock()
    mock_client.connect = AsyncMock()
    mock_client.disconnect = AsyncMock()
    mock_client.is_connected = MagicMock(return_value=True)

    mock_client.jurisdiction = make_model_mock(store, 'jurisdiction')
    mock_client.incentiverule = make_model_mock(store, 'incentiverule')
    mock_client.production = make_model_mock(store, 'production')
    mock_client.expense = make_model_mock(store, 'expense')
    mock_client.report = make_model_mock(store, 'report')
    mock_client.scenario = make_model_mock(store, 'scenario')
    mock_client.monitoringsource = make_model_mock(store, 'monitoringsource')
    mock_client.monitoringevent = make_model_mock(store, 'monitoringevent')

    from src.utils import database
    monkeypatch.setattr(database, "prisma", mock_client)
    
    modules_to_patch = [
        "src.api.jurisdictions.prisma", "src.api.incentive_rules.prisma",
        "src.api.productions.prisma", "src.api.calculator.prisma",
        "src.api.reports.prisma", "src.api.excel.prisma", "src.api.monitoring.prisma",
        "src.api.v1.endpoints.jurisdictions.prisma", "src.api.v1.endpoints.incentive_rules.prisma",
        "src.api.v1.endpoints.productions.prisma", "src.api.v1.endpoints.reports.prisma",
        "src.api.v1.endpoints.api_keys.prisma", "src.api.v1.endpoints.expenses.prisma",
        "src.api.v1.endpoints.monitoring.prisma", "src.api.v1.endpoints.organizations.prisma",
        "src.main.prisma"
    ]
    for module in modules_to_patch:
        try: monkeypatch.setattr(module, mock_client)
        except: pass
            
    return mock_client

@pytest.fixture
async def async_client():
    from src.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

# --- Missing Fixtures ---

@pytest.fixture
def calculator_test_cases():
    return [
        {"name": "Scenario 1", "budget": 5000000, "percentage": 25.0, "min_spend": 1000000, "max_credit": 10000000},
        {"name": "Scenario 2", "budget": 100000, "percentage": 25.0, "min_spend": 1000000, "max_credit": 10000000},
        {"name": "Scenario 3", "budget": 100000000, "percentage": 25.0, "min_spend": 1000000, "max_credit": 5000000},
    ]

@pytest.fixture
def sample_expenses():
    return [
        {"id": "1", "amount": 100000, "isQualifying": True, "category": "Labor"},
        {"id": "2", "amount": 200000, "isQualifying": True, "category": "Materials"},
        {"id": "3", "amount": 350000, "isQualifying": True, "category": "Rentals"},
        {"id": "4", "amount": 200000, "isQualifying": False, "category": "Travel"},
    ]
