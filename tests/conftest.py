import pytest
from unittest.mock import MagicMock, AsyncMock

@pytest.fixture(autouse=True)
def mock_prisma_db(monkeypatch):
    """
    Mock the Prisma database client for all tests to avoid requiring a running DB.
    """
    mock_client = MagicMock()
    mock_client.connect = AsyncMock()
    mock_client.disconnect = AsyncMock()
    mock_client.is_connected = MagicMock(return_value=True)

    # Common mock object that behaves like a generic DB record
    class MockObj:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__

    # Sample Data
    mock_jurisdiction = MockObj(
        id="test-j-id", 
        name="Illinois", 
        code="IL", 
        active=True
    )
    mock_rule = MockObj(
        id="test-r-id", 
        name="IL Film Credit", 
        ruleCode="IL-FILM", 
        jurisdictionId="test-j-id", 
        active=True,
        percentage=30,
        minSpend=0,
        maxCredit=None,
        fixedAmount=None,
        incentiveType="tax_credit",
        requirements="{}"
    )

    # Async methods
    async def find_many(*args, **kwargs):
        return [mock_jurisdiction, mock_rule]

    async def find_unique(*args, **kwargs):
        return mock_jurisdiction

    async def count(*args, **kwargs):
        return 1

    # Apply to all models
    for model in ['jurisdiction', 'incentiverule', 'production', 'expense']: 
        mock_model = MagicMock()
        mock_model.find_many = AsyncMock(side_effect=find_many)
        mock_model.find_unique = AsyncMock(side_effect=find_unique)
        mock_model.count = AsyncMock(side_effect=count)
        setattr(mock_client, model, mock_model)

    # Specific override for rule to return rule object
    mock_client.incentiverule.find_unique = AsyncMock(return_value=mock_rule)
    mock_client.incentiverule.find_many = AsyncMock(return_value=[mock_rule])
    
    # Specific override for jurisdiction
    mock_client.jurisdiction.find_unique = AsyncMock(return_value=mock_jurisdiction)
    mock_client.jurisdiction.find_many = AsyncMock(return_value=[mock_jurisdiction])

    # Patch the singleton in src.utils.database
    from src.utils import database
    monkeypatch.setattr(database, "prisma", mock_client)
    
    # Patch module-level imports in API
    # Must use try-except to avoid ImportErrors if modules changed
    for module in [
        "src.api.jurisdictions.prisma",
        "src.api.incentive_rules.prisma",
        "src.api.productions.prisma",
        "src.api.calculator.prisma",
        "src.api.reports.prisma",
        "src.api.excel.prisma",
        "src.main.prisma"
    ]:
        try:
            monkeypatch.setattr(module, mock_client)
        except (ImportError, AttributeError):
            pass

    return mock_client
