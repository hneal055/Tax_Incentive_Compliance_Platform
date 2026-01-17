# PilotForge
> Tax Incentive Intelligence for Film & TV
> Tax Incentive Intelligence for Film & TV
Jurisdictional rule engine for managing tax incentives for the film & television industry.

## Quick Start

### 🚀 Full Stack (Recommended)

Start both backend and frontend together:

**Linux/Mac:**
```bash
./start-fullstack.sh
```

**Windows:**
```powershell
.\start-fullstack.ps1
```

This starts:
- Backend API: http://localhost:8000
- Frontend UI: http://localhost:3000

### 🔧 Backend Only

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn src.main:app --reload
```

**Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn src.main:app --reload
```

Visit: http://localhost:8000/docs

### 🎨 Frontend Only

**Linux/Mac:**
```bash
cd frontend
./start-ui.sh
```

**Windows:**
```powershell
cd frontend
.\start-ui.ps1
```

**Or manually:**
```bash
cd frontend
npm install
npm run dev
```

Visit: http://localhost:3000

> 📖 **Detailed Setup Guide**: See [UI_SETUP.md](./UI_SETUP.md) for comprehensive UI setup instructions

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

- **[UI_SETUP.md](./UI_SETUP.md)** - Comprehensive frontend setup and troubleshooting guide
- **[frontend/FRONTEND_README.md](./frontend/FRONTEND_README.md)** - Frontend technology stack details
- **[docs/USER_MANUAL.md](./docs/USER_MANUAL.md)** - User guide for the application
- **[docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)** - Production deployment instructions
