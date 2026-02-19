# Contributing to PilotForge

Welcome! We're excited you want to contribute to the Tax Incentive Compliance Platform. This guide will help you get started.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Requirements](#testing-requirements)
6. [Security Guidelines](#security-guidelines)
7. [Documentation](#documentation)
8. [Commit Messages](#commit-messages)
9. [Pull Requests](#pull-requests)
10. [Deployment](#deployment)

---

## Code of Conduct

Be respectful, inclusive, and professional. We don't tolerate harassment or discrimination.

---

## Getting Started

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git
- GitHub account

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/hneal055/Tax_Incentive_Compliance_Platform.git
cd Tax_Incentive_Compliance_Platform

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Start development environment
docker compose up --build

# 4. Verify everything works
docker compose exec backend pytest -v
docker compose exec backend curl http://localhost:8001/health

# 5. Make your changes
# ... edit files ...

# 6. Run tests again
docker compose exec backend pytest -v

# 7. Commit and push
git add .
git commit -m "feat: describe your changes"
git push origin feature/your-feature-name
```

---

## Development Workflow

### 1. Create Feature Branch
```bash
# Branch naming convention:
# - feature/xyz - new features
# - fix/xyz - bug fixes
# - perf/xyz - performance improvements
# - docs/xyz - documentation changes
# - refactor/xyz - code refactoring
# - test/xyz - test additions

git checkout -b feature/redis-caching
```

### 2. Make Changes
```bash
# Edit files in src/ directory
# Add/update tests in tests/ directory
```

### 3. Test Locally
```bash
# Run all tests
docker compose exec backend pytest -v

# Run specific test file
docker compose exec backend pytest tests/test_api_endpoints.py -v

# Run with coverage
docker compose exec backend pytest --cov=src --cov-report=html

# Run performance tests
docker compose exec backend pytest tests/test_performance.py -v

# Check security
docker compose exec backend pytest tests/test_security.py -v
```

### 4. Format Code
```bash
# Format with Black
docker compose exec backend black src/ tests/

# Check with pylint
docker compose exec backend pylint src/
```

### 5. Commit Changes
```bash
git add src/utils/cache.py tests/test_cache.py
git commit -m "feat(cache): add redis support with TTL configuration"
```

### 6. Push and Create PR
```bash
git push origin feature/redis-caching

# Then create PR on GitHub.com
# Fill out the PR template completely
# Wait for CI checks to pass
# Request code review
```

---

## Coding Standards

### Style Guide
- **Python**: PEP 8 with Black formatting (line length: 88)
- **Imports**: Use `isort` to organize imports
- **Docstrings**: Use Google-style docstrings

### Python Style Example

```python
"""Module docstring explaining purpose."""

from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


def calculate_incentive(
    jurisdiction: str,
    production_spend: float,
    eligible_expenses: List[dict],
) -> Optional[float]:
    """Calculate tax incentive for a production.
    
    Args:
        jurisdiction: State/province code (e.g., 'IL')
        production_spend: Total production spending in USD
        eligible_expenses: List of eligible expense items
        
    Returns:
        Calculated incentive amount or None if not eligible
        
    Raises:
        ValueError: If jurisdiction not found
        ValidationError: If expenses invalid
    """
    try:
        # Implementation
        return incentive_amount
    except Exception as e:
        logger.error(f"Failed to calculate: {e}")
        raise
```

### File Organization

```
src/
├─ main.py              # Entry point
├─ api/
│  └─ routes.py        # All API endpoints
├─ models/
│  ├─ jurisdiction.py
│  ├─ production.py
│  └─ expense.py
├─ utils/
│  ├─ config.py        # Configuration
│  ├─ database.py      # Database client
│  ├─ security.py      # Security utilities
│  ├─ exceptions.py    # Custom exceptions
│  └─ logging_config.py
└─ rule_engine/
   ├─ engine.py        # Rule evaluation
   └─ registry.py      # Rule registry
```

---

## Testing Requirements

### Minimum Test Coverage
- **Endpoints**: 100% (every API route)
- **Utilities**: 95%+ (security, validation, logging)
- **Business Logic**: 100%

### Test Organization

```
tests/
├─ conftest.py                 # Fixtures & setup
├─ test_api_endpoints.py       # API tests (14+ tests)
├─ test_config_validation.py   # Config tests (23+ tests)
├─ test_security.py            # Security tests (28+ tests)
├─ test_error_handling.py      # Error tests (16+ tests)
└─ test_performance.py         # Performance tests (15+ tests)
```

### Test Example

```python
"""Test incentive calculation endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


@pytest.fixture
def valid_calculation_request():
    """Fixture for valid calculation request."""
    return {
        "jurisdiction": "IL",
        "production_spend": 1000000,
        "eligible_expenses": [
            {"category": "labor", "amount": 500000},
            {"category": "equipment", "amount": 300000},
        ]
    }


class TestIncentiveCalculation:
    """Tests for incentive calculation endpoint."""
    
    def test_calculate_incentive_success(self, valid_calculation_request):
        """Test successful incentive calculation."""
        response = client.post(
            "/api/incentives/calculate",
            json=valid_calculation_request
        )
        assert response.status_code == 200
        data = response.json()
        assert data["incentive_amount"] > 0
        assert "jurisdiction" in data
    
    def test_calculate_invalid_jurisdiction(self):
        """Test calculation with invalid jurisdiction."""
        response = client.post(
            "/api/incentives/calculate",
            json={
                "jurisdiction": "XX",
                "production_spend": 1000000,
                "eligible_expenses": []
            }
        )
        assert response.status_code == 404
    
    def test_calculate_negative_spend(self):
        """Test calculation with negative spend."""
        response = client.post(
            "/api/incentives/calculate",
            json={
                "jurisdiction": "IL",
                "production_spend": -1000,
                "eligible_expenses": []
            }
        )
        assert response.status_code == 422  # Validation error
```

### Running Tests

```bash
# All tests
docker compose exec backend pytest -v

# With coverage report
docker compose exec backend pytest --cov=src --cov-report=html

# Only security tests
docker compose exec backend pytest tests/test_security.py -v -k "sql_injection or xss"

# Performance tests
docker compose exec backend pytest tests/test_performance.py -v

# Single test
docker compose exec backend pytest tests/test_api_endpoints.py::test_health_check -v

# Watch mode (requires pytest-watch)
docker compose exec backend ptw
```

---

## Security Guidelines

### Before Every Commit

- [ ] No hardcoded secrets (passwords, API keys, tokens)
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Input validation on all user inputs
- [ ] Rate limiting on public endpoints
- [ ] Error messages don't expose sensitive info

### Security Testing

```bash
# Run security tests
docker compose exec backend pytest tests/test_security.py -v

# Scan dependencies
docker compose exec backend pip install safety
docker compose exec backend safety check

# Scan code
docker compose exec backend pip install bandit
docker compose exec backend bandit -r src/
```

### Common Security Issues to Avoid

❌ **Don't do this:**
```python
# SQL injection
query = f"SELECT * FROM users WHERE id = {user_id}"

# Hardcoded secrets
DATABASE_URL = "postgresql://user:password@localhost/db"

# Exposing internal errors
except Exception as e:
    return {"error": str(e)}  # Too detailed!

# No input validation
def process_data(data):
    return data.upper()  # What if data is None?
```

✅ **Do this instead:**
```python
# Parameterized queries
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))

# Use environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Generic error messages
except Exception as e:
    logger.error(f"Internal error: {e}")
    return {"error": "Processing failed. Please contact support."}

# Validate inputs
from pydantic import BaseModel, validator

class DataRequest(BaseModel):
    data: str
    
    @validator('data')
    def validate_data(cls, v):
        if not v:
            raise ValueError('Data cannot be empty')
        return v.upper()
```

---

## Documentation

### Update These Files
- `README.md` - If adding features or changing setup
- `DEPLOYMENT_GUIDE.md` - If deployment changes
- Docstrings - For all functions/classes
- Comments - For complex logic

### Documentation Standards

```python
def calculate_tax_credit(
    production_spend: float,
    jurisdiction: str,
) -> float:
    """Calculate tax credit for production spending.
    
    This function evaluates the production spending against
    jurisdiction-specific rules to determine the eligible
    tax credit amount.
    
    Args:
        production_spend: Total production spending in USD
        jurisdiction: State/province code (e.g., 'IL', 'CA')
        
    Returns:
        Calculated tax credit amount in USD
        
    Raises:
        ValueError: If jurisdiction not found
        TypeError: If production_spend is not a number
        
    Example:
        >>> credit = calculate_tax_credit(1000000, 'IL')
        >>> credit
        250000.0
    """
```

---

## Commit Messages

Use conventional commits for clarity:

```
<type>(<scope>): <subject>

<body (optional)>

<footer (optional)>
```

### Types
- `feat` - New feature
- `fix` - Bug fix
- `perf` - Performance improvement
- `refactor` - Code restructuring
- `test` - Test additions/changes
- `docs` - Documentation
- `ci` - CI/CD changes
- `chore` - Maintenance

### Examples

Good commit messages:
```
feat(api): add redis caching for rule lookups
fix(security): prevent sql injection in production query
perf(database): add index to jurisdiction lookups
test(security): add xss prevention tests
docs(deployment): update kubernetes guide
ci(github): add automated security scanning
```

Bad commit messages:
```
Updated code
Fixed stuff
Changed things
Work in progress
```

---

## Pull Requests

### Before Creating PR

- [ ] All tests pass: `docker compose exec backend pytest -v`
- [ ] Code formatted: `docker compose exec backend black src/ tests/`
- [ ] No hardcoded secrets
- [ ] Branch is up to date: `git pull origin main`
- [ ] Meaningful commit messages

### PR Checklist

Use the PR template:
1. Describe changes clearly
2. Link related issues
3. List testing done
4. Confirm security review
5. Update documentation
6. Note any breaking changes

### PR Review Process

1. **Automated Checks**
   - Tests must pass
   - Security scans must pass
   - Build must succeed

2. **Code Review**
   - At least 1 approval required
   - Maintainer reviews for:
     - Code quality
     - Security
     - Performance
     - Testing coverage

3. **Merge**
   - Resolve all conversations
   - Update from main if needed
   - Merge via GitHub UI

---

## Deployment

### Local Development
```bash
docker compose up --build
```

### Staging Deployment
```bash
docker compose -f docker-compose.prod.yml up -d
# See DEPLOYMENT_GUIDE.md for detailed steps
```

### Production Deployment
```bash
# Create release tag
git tag v1.1.0
git push origin v1.1.0

# Deploy via Kubernetes
kubectl apply -f k8s-deployment.yaml

# Verify deployment
kubectl rollout status deployment/pilotforge
kubectl get pods
```

---

## Questions?

- **Git/GitHub Help**: See `GIT_WORKFLOW.md`
- **GitHub Configuration**: See `GITHUB_SETUP.md`
- **Deployment**: See `DEPLOYMENT_GUIDE.md`
- **API Documentation**: See `README.md`

---

## Recognition

Contributors will be recognized in:
- GitHub commits (automatic)
- Release notes
- Contributors page

Thank you for contributing to PilotForge! 🚀
