# PilotForge
> Tax Incentive Intelligence for Film & TV
> Tax Incentive Intelligence for Film & TV
Jurisdictional rule engine for managing tax incentives for the film & television industry.

## Quick Start

### Backend
```powershell
cd C:\Projects\PilotForge
> Tax Incentive Intelligence for Film & TV
> Tax Incentive Intelligence for Film & TV
.\scripts\setup\setup.ps1
.\venv\Scripts\Activate.ps1
python -m uvicorn src.main:app --reload
```

Visit: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Visit: http://localhost:3000

## Features

- Multi-jurisdictional tax incentive rules
- Production expense tracking
- Automated incentive calculations
- Compliance verification
- Audit trail
- **Modern React UI** with Dashboard, Productions, Jurisdictions, and Calculator

## Technology

### Backend
- Python 3.11+ (FastAPI)
- PostgreSQL 16
- Prisma ORM
- Pytest

### Frontend
- React 19 + TypeScript
- Vite 7
- TailwindCSS 4
- Zustand (State Management)
- React Router v7

## Documentation

See `docs/QUICK_START.md` for detailed setup instructions.
See `frontend/FRONTEND_README.md` for frontend-specific documentation.
