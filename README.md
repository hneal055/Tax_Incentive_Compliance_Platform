# PilotForge
> Tax Incentive Intelligence for Film & TV

Jurisdictional rule engine for managing tax incentives for the film & television industry.

## Quick Start
```powershell
cd C:\Projects\Tax_Incentive_Compliance_Platform
.\scripts\setup\setup.ps1
.\venv\Scripts\Activate.ps1
python -m uvicorn src.main:app --reload
```

Visit: http://localhost:8000/docs

## Features

- Multi-jurisdictional tax incentive rules
- Production expense tracking
- Automated incentive calculations
- Compliance verification
- Audit trail
- **Comprehensive test suite (37 tests)**

## Testing

Run the comprehensive test suite:
```bash
# All tests (37 total)
pytest tests/ -v

# By endpoint category
pytest tests/test_jurisdiction_create.py     # 7 tests
pytest tests/test_incentive_rule_create.py   # 9 tests  
pytest tests/test_production_create.py       # 6 tests
pytest tests/test_calculator.py              # 7 tests
pytest tests/test_reports.py                 # 8 tests
```

**Test Coverage:**
- ✅ 100% endpoint coverage
- ✅ Creation workflows
- ✅ Validation scenarios
- ✅ Error handling (201, 404, 422, 400)
- ✅ Relationship integrity
- ✅ Business logic validation

## Technology

- Python 3.12+ (FastAPI)
- PostgreSQL 16
- Prisma ORM
- pytest + pytest-asyncio
- asgi-lifespan

## Documentation

See `docs/QUICK_START.md` for detailed setup instructions.
