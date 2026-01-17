# PilotForge
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

### Backend

```powershell
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

```bash
cd frontend
npm install
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

**Backend:**
- Python 3.12+ with FastAPI
- PostgreSQL database
- Serves frontend static files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest` for backend, `npm run lint` for frontend)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

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
