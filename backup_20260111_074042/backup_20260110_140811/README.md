# Tax-Incentive Compliance Platform

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

## Technology

- Python 3.11+ (FastAPI)
- PostgreSQL 16
- Prisma ORM
- Pytest

## Documentation

See `docs/QUICK_START.md` for detailed setup instructions.
