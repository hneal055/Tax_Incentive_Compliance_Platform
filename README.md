# PilotForge

> **Tax Incentive Intelligence for Film & TV Productions**
> Tax Incentive Intelligence for Film & TV

## 🎬 Overview

PilotForge is a comprehensive tax incentive calculation and compliance platform for the global film and television industry. Manage productions, calculate tax incentives across 32+ jurisdictions, and maximize your tax savings with our modern full-stack application.

## ✨ Features

- **Multi-jurisdictional tax incentive rules** across 32 jurisdictions and 33 programs
- **Production expense tracking** with categorization and validation
- **Automated incentive calculations** with stackable credits
- **Compliance verification** against jurisdiction requirements
- **Audit trail** for defensible reporting
- **Modern React UI** with Dashboard, Productions, Jurisdictions, and Calculator pages
- **RESTful API** with comprehensive OpenAPI documentation
- **PDF & Excel reports** for professional documentation

## 🚀 Quick Start

Jurisdictional rule engine for managing tax incentives for the film & television industry.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6.svg)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

---

## 🎯 Features

- 🌍 **32 Global Jurisdictions** - Compare incentives across USA, Canada, UK, and more
- 💰 **Tax Incentive Calculator** - Instant credit estimates with compliance checks
- 🎬 **Production Management** - Track productions, budgets, and locations
- 📊 **Dashboard UI** - Modern React interface for easy navigation
- 📄 **PDF & Excel Reports** - Professional documentation for stakeholders
- 🔒 **Type-Safe** - Full TypeScript coverage for reliability

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- **Node.js 20+** and **npm 10+**
- **PostgreSQL 16**

### Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Generate Prisma client
python -m prisma generate

# Run migrations
python -m prisma migrate deploy

# Start development server
### Backend

```powershell
cd C:\Projects\Tax_Incentive_Compliance_Platform
# Windows PowerShell
cd C:\Projects\PilotForge
.\scripts\setup\setup.ps1
.\venv\Scripts\Activate.ps1
python -m uvicorn src.main:app --reload
```

```bash
# macOS/Linux
cd /path/to/PilotForge
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m prisma generate
python -m uvicorn src.main:app --reload
```

**Backend API**: http://localhost:8000/docs

### Frontend

Visit: **http://localhost:8000/docs** (Swagger UI)

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend UI**: http://localhost:3000

## 🏗️ Technology Stack

### Backend
- **Python 3.12+** - Modern Python with type hints
- **FastAPI 0.115** - High-performance async web framework
- **PostgreSQL 16** - Robust relational database
- **Prisma ORM** - Type-safe database access
- **Pytest** - Comprehensive testing (31/31 passing)
- **ReportLab & openpyxl** - PDF and Excel generation

### Frontend
- **React 19** - Latest React with concurrent rendering
- **TypeScript 5.9** - Type-safe development
- **Vite 7** - Lightning-fast build tool with HMR
- **TailwindCSS 4** - Utility-first styling framework
- **Zustand** - Lightweight state management
- **React Router v7** - Client-side routing
- **Axios** - Typed HTTP client for API calls

## 📁 Project Structure

```
PilotForge/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── api/             # Typed API client and services
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components (Dashboard, Productions, etc.)
│   │   ├── store/           # Zustand state management
│   │   └── types/           # TypeScript interfaces
│   ├── package.json         # Frontend dependencies
│   └── vite.config.ts       # Vite configuration
├── src/                     # Backend Python application
│   ├── main.py             # FastAPI application entry
│   ├── routes.py           # API route definitions
│   └── utils/              # Utility functions
├── prisma/                 # Database schema and migrations
├── rules/                  # Jurisdiction tax rule definitions (JSON)
├── tests/                  # Backend test suite
├── docs/                   # Documentation
│   ├── README.md           # Architecture overview
│   ├── FRONTEND_SETUP.md   # Frontend setup guide
│   ├── DEPLOYMENT.md       # Deployment instructions
│   ├── USER_MANUAL.md      # API and UI usage guide
│   └── API_EXAMPLES.md     # Code examples
└── requirements.txt        # Backend Python dependencies
```

## 🎨 Frontend Features

### **Dashboard**
- Production count overview
- Jurisdiction grid with 32+ jurisdictions
- Quick actions for common tasks
- Responsive design with PilotForge branding

### **Productions Management**
- Create, view, edit, delete productions
- Track budget, status, and filming details
- Associate with jurisdictions
- Filter and search capabilities

### **Jurisdictions Browser**
- Browse all available jurisdictions
- Filter by type (State, Country, Province)
- View incentive program details
- Search and sort options

### **Tax Incentive Calculator**
- Select production and jurisdiction
- Calculate tax incentives in real-time
- View detailed credit breakdown
- Compare multiple jurisdictions

## 📚 Documentation

### Getting Started
- **[Frontend Setup Guide](./docs/FRONTEND_SETUP.md)** - Complete frontend installation and development guide
- **[Backend Setup](./docs/README.md#backend-architecture)** - Backend setup and architecture
- **[Deployment Guide](./docs/DEPLOYMENT.md)** - Production deployment with frontend build steps

### Usage
- **[User Manual](./docs/USER_MANUAL.md)** - API reference and Frontend UI guide
- **[API Examples](./docs/API_EXAMPLES.md)** - Code samples including React frontend examples
- **[Frontend Examples](./docs/API_EXAMPLES.md#frontend-react-examples)** - React hooks, Zustand, and API integration

### Development
- **[Roadmap](./docs/ROADMAP.md)** - Project phases and future features
- **[Rule Format](./docs/RULE_FORMAT.md)** - Jurisdiction rule schema
- **[North Star](./docs/NORTH_STAR.md)** - Project vision and principles

## 🌐 Live Demo

**Production Application**: https://pilotforge.onrender.com
- Full React frontend with interactive UI
- RESTful API with Swagger documentation
- Real-time tax incentive calculations

**API Documentation**: https://pilotforge.onrender.com/docs

## 💻 Development

### Backend Development
```bash
# Run with auto-reload
python -m uvicorn src.main:app --reload

# Run tests
pytest

# Generate Prisma client after schema changes
python -m prisma generate
python -m prisma migrate dev
```

### Frontend Development
```bash
cd frontend

# Start dev server (http://localhost:3000)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

### Full Stack Development
```bash
# Terminal 1: Backend
python -m uvicorn src.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🚀 Deployment

### Build Frontend
```bash
cd frontend
npm install
npm run build
```

### Deploy Full Stack (Render.com)
The backend serves the built frontend from `frontend/dist/`:

```yaml
# render.yaml
buildCommand: cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt && python -m prisma generate
startCommand: python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed instructions.

## 🧪 Testing

### Backend Tests
```bash
pytest                    # Run all tests
pytest -v                # Verbose output
pytest tests/test_api.py # Specific test file
```

**Test Coverage**: 31/31 tests passing

### Frontend Tests (Coming Soon)
- Unit tests with Vitest
- Component tests with React Testing Library
- E2E tests with Playwright

## 📦 Production Bundle

**Frontend:**
- JavaScript: 283KB (92KB gzipped)
- CSS: 3.6KB
- Optimized with Vite code splitting and tree shaking

- Multi-jurisdictional tax incentive rules
- Production expense tracking
- Automated incentive calculations
- Compliance verification
- Audit trail
- **Comprehensive test suite (46 tests)**

## Testing

Run the comprehensive test suite:
```bash
# All tests (46 total)
pytest tests/ -v

# By endpoint category
pytest tests/test_jurisdiction_create.py     # 7 tests
pytest tests/test_incentive_rule_create.py   # 9 tests  
pytest tests/test_production_create.py       # 6 tests
pytest tests/test_calculator.py              # 7 tests
pytest tests/test_reports.py                 # 8 tests
pytest tests/test_excel_exports.py           # 9 tests
```

**Test Coverage:**
- ✅ 100% endpoint coverage
- ✅ Creation workflows
- ✅ Validation scenarios
- ✅ Error handling (201, 404, 422, 400)
- ✅ Relationship integrity
- ✅ Business logic validation
**Backend:**
- Python 3.12+ with FastAPI
- PostgreSQL database
- Serves frontend static files
Visit: **http://localhost:3000**

---

- Python 3.12+ (FastAPI)
## 🛠️ Technology Stack

### Backend
- **Python 3.12** - Modern Python with FastAPI
- **FastAPI** - High-performance async web framework
- **PostgreSQL 16** - Robust relational database
- **Prisma ORM** - Type-safe database client
- **Pytest** - Comprehensive testing suite
- **Python 3.12** (FastAPI)
- PostgreSQL 16
- Prisma ORM
- pytest + pytest-asyncio
- asgi-lifespan

### Frontend
- **React 19** - Latest React with concurrent features
- **TypeScript 5.9** - Type safety and better DX
- **Vite 7** - Lightning-fast build tool and HMR
- **TailwindCSS 4** - Utility-first CSS framework
- **Zustand** - Lightweight state management (<1KB)
- **React Router v7** - Client-side routing
- **Axios** - Promise-based HTTP client

---

## 📚 Documentation

- **[Frontend Setup Guide](./docs/FRONTEND_SETUP.md)** - Complete frontend development guide
- **[Deployment Guide](./docs/DEPLOYMENT.md)** - Deploy to production (Render, Vercel, AWS)
- **[User Manual](./docs/USER_MANUAL.md)** - API reference and UI guide
- **[API Examples](./docs/API_EXAMPLES.md)** - Code examples in Python, JavaScript, TypeScript
- **[Roadmap](./docs/ROADMAP.md)** - Development phases and future plans
- **[Full Documentation](./docs/README.md)** - Architecture overview

---

## 💡 Example Usage

### Calculate Tax Incentive (API)

```python
import httpx

response = httpx.post('http://localhost:8000/api/v1/calculate/simple', json={
    'budget': 5000000,
    'jurisdictionId': 'california-id',
    'ruleId': 'ca-film-credit-2025'
})

result = response.json()
print(f"Estimated Credit: ${result['estimatedCredit']:,}")
# Output: Estimated Credit: $1,000,000
```

### Using Frontend (React/TypeScript)

```typescript
import { calculatorService } from './api'

const result = await calculatorService.calculate(
  productionId,
  jurisdictionId
)

console.log(`Estimated Credit: $${result.estimatedCredit.toLocaleString()}`)
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_calculator_logic.py

# Run with coverage
pytest --cov=src
```

**Test Coverage:** 31/31 tests passing ✅

---

## 📦 Project Structure

```
Tax_Incentive_Compliance_Platform/
├── src/                    # Backend source code
│   ├── main.py            # FastAPI application
│   ├── routes.py          # API endpoints
│   └── ...
├── frontend/              # React frontend
│   ├── src/
│   │   ├── api/          # API client
│   │   ├── components/   # UI components
│   │   ├── pages/        # Route pages
│   │   ├── store/        # Zustand store
│   │   └── types/        # TypeScript types
│   └── package.json
├── docs/                  # Documentation
├── tests/                 # Backend tests
├── rules/                 # Jurisdiction rule files
└── requirements.txt       # Python dependencies
```

---

## 🌐 Deployment

Deploy the backend to **Render.com**, **Railway**, **Fly.io**, or **AWS**.

Deploy the frontend to **Vercel**, **Netlify**, or **Render Static Site**.

See **[docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)** for detailed instructions.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest` for backend, `npm run lint` for frontend)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License

Copyright (c) 2025-2026 Howard Neal - PilotForge

See [LICENSE](./docs/LICENSE) for full details.

## 📞 Support

- **Documentation**: Check the [docs/](./docs/) directory
- **Issues**: Open a [GitHub Issue](https://github.com/hneal055/Tax_Incentive_Compliance_Platform/issues)
- **API Questions**: See [API_EXAMPLES.md](./docs/API_EXAMPLES.md)
- **Frontend Setup**: See [FRONTEND_SETUP.md](./docs/FRONTEND_SETUP.md)

---

**Built with ❤️ for the film and television industry**
See [LICENSE](./docs/LICENSE) for details.

---

## 📞 Support

- **Documentation Issues**: Open a GitHub issue
- **Questions**: Check [docs/USER_MANUAL.md](./docs/USER_MANUAL.md)
- **Bug Reports**: Include reproduction steps and error messages

---

**Built with ❤️ for the film & TV industry**
See `docs/QUICK_START.md` for detailed setup instructions.
See `frontend/FRONTEND_README.md` for frontend-specific documentation.
