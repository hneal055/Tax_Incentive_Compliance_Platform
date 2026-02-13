# PilotForge Test Suite

## Overview

This directory contains comprehensive tests for the PilotForge Tax Incentive Compliance Platform, including unit tests, integration tests, and end-to-end tests.

## Test Organization

### Test Types

- **Unit Tests** (`@pytest.mark.unit`): Test individual components in isolation
- **Integration Tests** (`@pytest.mark.integration`): Test interactions between components
- **End-to-End Tests** (`@pytest.mark.e2e`): Test complete user workflows from start to finish
- **API Tests** (`@pytest.mark.api`): Test API endpoints
- **Slow Tests** (`@pytest.mark.slow`): Tests that take longer to run

### Test Files

- `test_end_to_end.py` - **NEW**: Comprehensive end-to-end workflow tests
- `test_smoke_api.py` - Quick smoke tests for critical endpoints
- `test_*_api.py` - API endpoint tests for various features
- `test_*_create.py` - Creation workflow tests
- `test_*.py` - Various unit and integration tests

### Key End-to-End Tests

The new `test_end_to_end.py` file includes:

1. **Complete Production Workflow**
   - Create jurisdiction
   - Create incentive rule
   - Create production
   - Add expenses
   - Calculate incentives
   - Generate reports

2. **Multi-Jurisdiction Comparison**
   - Create multiple jurisdictions
   - Create incentive rules with different rates
   - Compare incentives across jurisdictions

3. **Rule Engine Evaluation**
   - Load jurisdiction rules
   - Evaluate expenses against rules
   - Calculate incentive amounts

4. **Jurisdiction Discovery**
   - List all jurisdictions
   - Filter by country and type
   - Get jurisdiction details

5. **Health and Status Checks**
   - Test system health endpoints

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Types
```bash
# End-to-end tests only
pytest -m e2e

# Integration tests only
pytest -m integration

# Unit tests only
pytest -m unit

# Fast tests (exclude slow tests)
pytest -m "not slow"
```

### Run Specific Test Files
```bash
# End-to-end tests
pytest tests/test_end_to_end.py -v

# Smoke tests
pytest tests/test_smoke_api.py -v

# Specific test class
pytest tests/test_end_to_end.py::TestCompleteProductionWorkflow -v

# Specific test method
pytest tests/test_end_to_end.py::TestHealthAndStatus::test_health_check -v
```

### Run with Coverage
```bash
pytest --cov=src --cov-report=html --cov-report=term-missing
```

## Test Infrastructure

### Fixtures

The `conftest.py` file provides shared fixtures:

- `mock_prisma_db` (autouse): Automatically mocks the Prisma database for all tests
- `async_client`: Provides an AsyncClient for testing HTTP endpoints
- `calculator_test_cases`: Sample test data for calculator tests
- `sample_expenses`: Sample expense data

### Mock Database

Tests use an in-memory mock database (`MockStore`) that:
- Simulates Prisma database operations
- Enforces foreign key and unique constraints
- Provides smart data generation for missing IDs
- Returns proper validation errors (422 for Pydantic, 404 for not found)

No actual database connection is required for most tests.

## Configuration

### pytest.ini
- Test discovery patterns
- Markers registration
- Coverage configuration

### pyproject.toml
- pytest configuration options
- Coverage settings
- AsyncIO settings

## Test Results

### Current Status (as of latest run)

- **End-to-End Tests**: 5 tests created
  - Health check: ✅ PASSING
  - Rule engine: ✅ PASSING
  - Complete workflow: ⚠️ In progress
  - Multi-jurisdiction: ⚠️ In progress
  - Jurisdiction discovery: ⚠️ In progress

- **Smoke Tests**: ✅ All passing (2/2)
- **Coverage**: ~30% (increasing as more tests are added)

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Run: `pip install -r requirements.txt`
   - Or: `pip install -r requirements-test.txt`

2. **"Marker not found" errors**
   - Ensure pytest.ini is in the project root
   - Check that pyproject.toml has markers defined

3. **Database connection errors**
   - Most tests use mocks and don't need a database
   - Check that conftest.py mock_prisma_db fixture is loaded
   - For real database tests, ensure DATABASE_URL is set

4. **Import errors**
   - Run from project root directory
   - Ensure src/ is in PYTHONPATH

## Adding New Tests

### Template for End-to-End Test
```python
@pytest.mark.e2e
@pytest.mark.asyncio
class TestMyWorkflow:
    """Test description"""
    
    async def test_my_workflow(self, async_client):
        """Test a complete workflow"""
        # Step 1: Setup
        response = await async_client.post("/api/endpoint", json=data)
        assert response.status_code == 201
        
        # Step 2: Action
        result = await async_client.get("/api/endpoint/123")
        assert result.status_code == 200
        
        # Step 3: Verify
        data = result.json()
        assert data["field"] == "expected_value"
```

### Best Practices

1. **Use descriptive test names** that explain what is being tested
2. **Group related tests** in test classes
3. **Use appropriate markers** (@pytest.mark.e2e, @pytest.mark.integration, etc.)
4. **Assert meaningful results**, not just status codes
5. **Clean up resources** after tests (fixtures handle this automatically)
6. **Document complex test logic** with comments

## CI/CD Integration

Tests run automatically on:
- Push to main/develop branches
- Pull requests
- Via GitHub Actions workflow (.github/workflows/ci-cd.yml)

## Further Documentation

- See `TESTING.md` in project root for overall testing strategy
- See `TEST_COVERAGE_MATRIX.md` for detailed coverage mapping
- See `END_TO_END_TESTING_PROCESS.md` in docs/ for detailed E2E process
