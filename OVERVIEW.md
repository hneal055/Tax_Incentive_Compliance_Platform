# PilotForge - Project Overview

## Executive Summary

**PilotForge** is a comprehensive tax incentive intelligence platform designed specifically for the global film and television production industry. The platform empowers production companies to maximize tax savings by providing instant access to tax incentive calculations, compliance checks, and comparative analysis across 32+ global jurisdictions.

### The Problem We Solve

Film and television productions face complex challenges when selecting filming locations:
- **Tax incentive programs vary dramatically** across jurisdictions (16.5% to 40% credits)
- **Compliance requirements are complex** and constantly changing
- **Manual research is time-consuming** and expensive
- **Missing deadlines or requirements** can cost millions in lost incentives
- **Comparing multiple jurisdictions** requires specialized expertise

### Our Solution

PilotForge automates tax incentive analysis, providing production companies with:
- **Instant calculations** across 32 global jurisdictions
- **Compliance validation** against program requirements
- **Professional reports** for stakeholders and investors
- **Real-time monitoring** of legislative changes
- **Production tracking** with budget and location management

---

## Platform Capabilities

### 🌍 Global Jurisdiction Coverage

**32 Active Jurisdictions** spanning:
- **United States**: California, New York, Georgia, Louisiana, New Mexico, Texas, Massachusetts, Illinois, Pennsylvania, Connecticut, Maryland, North Carolina, Oregon, Rhode Island, Utah
- **Canada**: British Columbia, Ontario, Quebec
- **Europe**: United Kingdom, France, Germany, Italy, Czech Republic, Hungary, Ireland, Spain
- **Asia-Pacific**: Australia, New Zealand, Singapore, South Korea

**33 Tax Incentive Programs** including:
- State film tax credits (20-40%)
- Federal tax incentives (16.5-25%)
- Production rebates and grants
- Post-production incentives
- Visual effects incentives

### 📊 Core Features

#### 1. Tax Incentive Calculator
- Select production and jurisdiction from live database
- Instant credit estimates with qualified expense breakdown
- Multi-jurisdiction comparison
- Professional downloadable reports (PDF/Excel)
- Compliance requirement validation

#### 2. Production Management
- Create and track multiple productions
- Budget tracking and management
- Filming location association
- Production status workflows (Development → Pre-Production → Filming → Post-Production → Complete)
- Document management

#### 3. Dashboard & Analytics
- Real-time production metrics
- Jurisdiction performance comparison
- Recent activity feed
- System health monitoring
- Customizable zoom controls (50%-150%)

#### 4. Real-Time Monitoring System ✨
- **Legislative change tracking** via NewsAPI integration
- **WebSocket live updates** for instant alerts
- **AI-powered summaries** using GPT-4o-mini
- **Email/Slack notifications** for critical changes
- **RSS feed monitoring** from film commissions

#### 5. Professional Reporting
- PDF reports with ReportLab
- Excel exports with openpyxl
- Financial breakdown and budget utilization
- Compliance disclaimers
- Stakeholder-ready formatting

---

## Technology Architecture

### Backend Stack
```
Language:     Python 3.12
Framework:    FastAPI 0.115 (async)
Database:     PostgreSQL 16
ORM:          Prisma (type-safe queries)
API Docs:     OpenAPI 3.1 (Swagger/ReDoc)
Testing:      Pytest (127/127 tests passing)
Background:   APScheduler (monitoring tasks)
WebSocket:    Native FastAPI WebSocket support
```

### Frontend Stack
```
Framework:    React 19 (concurrent rendering)
Language:     TypeScript 5.9 (strict mode)
Build Tool:   Vite 7 (lightning-fast HMR)
Styling:      TailwindCSS 4 (utility-first)
State:        Zustand (lightweight)
Routing:      React Router v7
HTTP Client:  Axios (typed)
Testing:      Vitest (51/51 tests passing)
```

### Developer Portal
```
Framework:    Next.js (App Router)
Docs:         Swagger UI + ReDoc
API Spec:     OpenAPI 3.1
```

### Infrastructure
```
Database:     PostgreSQL 16 (managed)
Deployment:   Render.com / Docker
CI/CD:        GitHub Actions ready
Monitoring:   Health checks + WebSocket status
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  React UI    │  │  Developer   │  │  Monitoring  │          │
│  │  (Port 5200) │  │  Portal      │  │  Dashboard   │          │
│  │              │  │  (Port 3000) │  │  (WebSocket) │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────┬────────────────┬────────────────┬──────────────────┘
             │                │                │
             │ REST API       │ OpenAPI Spec   │ WebSocket
             │                │                │
┌────────────┴────────────────┴────────────────┴──────────────────┐
│                      Backend Layer (FastAPI)                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  API Routes     │  │  Rule Engine    │  │  Monitoring     │ │
│  │  • Productions  │  │  • Compliance   │  │  • NewsAPI      │ │
│  │  • Jurisdictions│  │  • Calculations │  │  • RSS Feeds    │ │
│  │  • Calculator   │  │  • Validation   │  │  • LLM Summary  │ │
│  │  • Reports      │  │  • Rules JSON   │  │  • WebSocket    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└────────────┬────────────────┬────────────────┬──────────────────┘
             │                │                │
             │ Prisma ORM     │ Direct Access  │ APScheduler
             │                │                │
┌────────────┴────────────────┴────────────────┴──────────────────┐
│                      Data Layer                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              PostgreSQL 16 Database                      │    │
│  │  • Productions  • Jurisdictions  • IncentivePrograms    │    │
│  │  • Expenses     • MonitoringEvents  • MonitoringSources │    │
│  └─────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                      External Services                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  NewsAPI     │  │  OpenAI      │  │  SMTP/Slack  │          │
│  │  (Monitoring)│  │  (LLM)       │  │  (Alerts)    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└──────────────────────────────────────────────────────────────────┘
```

---

## Project Metrics

### Code Statistics
```
Backend Code:       5,000+ lines of Python
Frontend Code:      4,000+ lines of TypeScript/React
Test Code:          2,850+ lines of test coverage
Documentation:      25+ markdown files
Total Files:        200+ tracked files
```

### Test Coverage
```
Backend Tests:      127/127 passing (100%)
Frontend Tests:     51/51 passing (100%)
Total Tests:        178 comprehensive tests
Coverage:           80%+ across all modules
```

### API Endpoints
```
REST Endpoints:     30+ endpoints across 8 routers
  • Jurisdictions:  6 endpoints
  • Productions:    8 endpoints
  • Calculator:     4 endpoints
  • Reports:        5 endpoints
  • Monitoring:     7+ endpoints
  • Excel:          4 endpoints
  • Expenses:       3 endpoints
  • Health:         1 endpoint
WebSocket:          1 live monitoring connection
```

### Data Coverage
```
Jurisdictions:      32 global locations
Programs:           33 tax incentive programs
Credit Ranges:      16.5% - 40% tax credits
Budget Range:       $1M - $500M+ productions
```

---

## Development Status

### ✅ Completed Features

**Core Platform (v1.0)**
- [x] Full-stack application architecture
- [x] 32 jurisdiction database with 33 programs
- [x] Production management CRUD
- [x] Tax incentive calculator with rule engine
- [x] PDF and Excel report generation
- [x] Comprehensive test suite (178 tests)
- [x] Developer portal with API documentation
- [x] Health monitoring and status checks

**Real-Time Monitoring System (v1.1)**
- [x] WebSocket live updates
- [x] NewsAPI integration (4-hour intervals)
- [x] RSS feed monitoring (5-minute checks)
- [x] LLM-powered summaries (GPT-4o-mini)
- [x] Email and Slack notifications
- [x] Monitoring dashboard UI
- [x] Event severity classification
- [x] Read/unread status tracking

### 🚧 In Progress

- [ ] Enhanced multi-jurisdiction comparison reports
- [ ] Advanced filtering and search
- [ ] User authentication and role-based access
- [ ] Production budget forecasting
- [ ] Historical data analytics

### 📋 Planned Features

**Phase 2 - Advanced Analytics**
- Multi-year trend analysis
- ROI forecasting tools
- Budget optimization recommendations
- Comparative scenario modeling

**Phase 3 - Collaboration**
- Team collaboration features
- Shared production workspaces
- Comment and annotation system
- Approval workflows

**Phase 4 - Enterprise Features**
- Multi-organization support
- Custom branding
- Advanced reporting templates
- API rate limiting and quotas
- Audit logging and compliance

---

## Quick Links to Documentation

### Getting Started
- **[README.md](./README.md)** - Complete setup and usage guide
- **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - Quick command reference
- **[UI_SETUP.md](./UI_SETUP.md)** - Frontend setup guide

### Development
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Contribution guidelines
- **[docs/README.md](./docs/README.md)** - Backend architecture
- **[docs/FRONTEND_SETUP.md](./docs/FRONTEND_SETUP.md)** - Frontend development guide
- **[docs/API_EXAMPLES.md](./docs/API_EXAMPLES.md)** - API code samples

### Testing
- **[TESTING.md](./TESTING.md)** - Testing overview
- **[COMPREHENSIVE_TEST_REPORT.md](./COMPREHENSIVE_TEST_REPORT.md)** - Detailed test results
- **[docs/END_TO_END_TESTING_PROCESS.md](./docs/END_TO_END_TESTING_PROCESS.md)** - E2E testing guide

### Operations
- **[DEPLOYMENT_NOTES.md](./DEPLOYMENT_NOTES.md)** - Deployment checklist
- **[docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)** - Full deployment guide
- **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - Common issues and fixes

### Features
- **[MONITORING_COMPLETE.md](./MONITORING_COMPLETE.md)** - Monitoring system details
- **[docs/MONITORING_SYSTEM.md](./docs/MONITORING_SYSTEM.md)** - Monitoring architecture
- **[docs/WEBSOCKET_API.md](./docs/WEBSOCKET_API.md)** - WebSocket documentation
- **[FRONTEND_IMPLEMENTATION.md](./FRONTEND_IMPLEMENTATION.md)** - Frontend features

### Project Management
- **[PROJECT_PROGRESS.md](./PROJECT_PROGRESS.md)** - Development progress
- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - Brief summary
- **[docs/ROADMAP.md](./docs/ROADMAP.md)** - Future development plans

---

## Running the Platform

### Full Stack (Recommended)

**Windows:**
```powershell
.\start-fullstack.ps1
```

**Linux/Mac:**
```bash
./start-fullstack.sh
```

**Access Points:**
- Frontend UI: http://localhost:5200
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- API Docs (ReDoc): http://localhost:8000/redoc
- Developer Portal: http://localhost:3000

### Individual Components

**Backend Only:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m prisma generate
python -m prisma migrate deploy
python -m uvicorn src.main:app --reload
```

**Frontend Only:**
```bash
cd frontend
npm install
npm run dev -- --port 5200
```

**Developer Portal:**
```bash
cd developer-portal
npm install
npm run dev
```

---

## Business Value Proposition

### For Production Companies

**Time Savings:**
- Reduce research time from days to minutes
- Automate compliance checking
- Instant multi-jurisdiction comparison

**Cost Savings:**
- Maximize tax credit capture (16.5% - 40%)
- Identify optimal filming locations
- Avoid missed deadlines and requirements

**Risk Reduction:**
- Stay current with legislative changes
- Validate compliance before commitment
- Professional documentation for audits

### ROI Example

**Sample Production: $50M Budget**
```
Scenario 1: Manual Research (Without PilotForge)
  • Research Cost:        $15,000 (consultant fees)
  • Time:                 2-3 weeks
  • Missed Opportunity:   $500,000 (better jurisdiction)
  • Total Cost:           $515,000

Scenario 2: Using PilotForge
  • Platform Cost:        $0 (self-service)
  • Time:                 15 minutes
  • Optimal Selection:    $2.5M tax credit (50% vs 45%)
  • Monitoring Alerts:    Early warning on changes
  • Net Benefit:          $515,000+ saved
```

---

## Technical Highlights

### Performance
- **API Response Time**: < 100ms (average)
- **Calculator Processing**: < 500ms for complex scenarios
- **WebSocket Latency**: < 50ms for live updates
- **Database Queries**: Optimized with Prisma indexing

### Scalability
- **Async Architecture**: FastAPI async/await throughout
- **Connection Pooling**: PostgreSQL connection management
- **Stateless Design**: Horizontal scaling ready
- **Caching Strategy**: Ready for Redis integration

### Security
- **Input Validation**: Pydantic models with strict typing
- **SQL Injection Protection**: Prisma parameterized queries
- **CORS Configuration**: Controlled cross-origin access
- **Environment Secrets**: .env file management
- **HTTPS Ready**: TLS/SSL certificate support

### Code Quality
- **Type Safety**: 100% TypeScript frontend, Python type hints
- **Linting**: ESLint + Prettier (frontend), Ruff (backend)
- **Testing**: 178 comprehensive tests, 80%+ coverage
- **Documentation**: OpenAPI 3.1 specification
- **Version Control**: Git with semantic commits

---

## Team & Collaboration

### Development Philosophy
- **Test-Driven Development**: Write tests first
- **Minimal Changes**: Surgical, focused updates
- **Documentation-First**: Comprehensive docs for all features
- **Code Review**: All changes reviewed before merge
- **Continuous Integration**: Automated testing on commits

### Project Structure
```
Tax_Incentive_Compliance_Platform/
├── src/                    # Backend Python application
│   ├── main.py            # FastAPI app entry
│   ├── api/               # API route handlers
│   ├── models/            # Pydantic models
│   ├── rule_engine/       # Compliance logic
│   └── utils/             # Utilities
├── frontend/              # React TypeScript UI
│   ├── src/
│   │   ├── api/          # API client
│   │   ├── components/   # React components
│   │   ├── pages/        # Route pages
│   │   ├── store/        # Zustand state
│   │   └── test/         # Vitest tests
│   └── vitest.config.ts
├── developer-portal/      # Next.js docs portal
├── prisma/               # Database schema
├── rules/                # Jurisdiction rules (JSON)
├── tests/                # Backend tests
├── docs/                 # Documentation
└── requirements.txt      # Python dependencies
```

---

## License & Legal

**Proprietary and Confidential**

Copyright (c) 2026 PilotForge - Tax Incentive Compliance Platform. All Rights Reserved.

This software is proprietary and confidential. Unauthorized copying, distribution, modification, or use is strictly prohibited. See [LICENSE](./LICENSE) for full terms.

---

## Support & Contact

**Documentation:** [docs/](./docs/) directory  
**Issues:** [GitHub Issues](https://github.com/hneal055/Tax_Incentive_Compliance_Platform/issues)  
**API Reference:** [API_EXAMPLES.md](./docs/API_EXAMPLES.md)  
**User Manual:** [USER_MANUAL.md](./USER_MANUAL.md)

---

## Next Steps

### For New Users
1. Read the [README.md](./README.md) for setup instructions
2. Follow the [Quick Start Guide](./QUICK_REFERENCE.md)
3. Explore the [User Manual](./USER_MANUAL.md)
4. Try the [API Examples](./docs/API_EXAMPLES.md)

### For Developers
1. Review [CONTRIBUTING.md](./CONTRIBUTING.md)
2. Set up your development environment ([docs/FRONTEND_SETUP.md](./docs/FRONTEND_SETUP.md))
3. Run the test suite ([TESTING.md](./TESTING.md))
4. Check the [Roadmap](./docs/ROADMAP.md) for planned features

### For Stakeholders
1. Review this overview document
2. Examine [PROJECT_PROGRESS.md](./PROJECT_PROGRESS.md)
3. Check the [Comprehensive Test Report](./COMPREHENSIVE_TEST_REPORT.md)
4. See the [Deployment Guide](./docs/DEPLOYMENT.md)

---

**PilotForge** - Tax Incentive Intelligence for the Modern Film Industry

*Built with care for production companies worldwide* 🎬
