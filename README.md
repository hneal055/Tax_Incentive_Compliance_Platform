# PilotForge

> **Tax Incentive Intelligence for Film & TV Productions**

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6.svg)](https://www.typescriptlang.org/)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](./LICENSE)
[![Status: Private](https://img.shields.io/badge/Status-Private-important.svg)]

---

## Overview

PilotForge is a comprehensive tax incentive calculation and compliance platform for the global film and television industry. Manage productions, calculate tax incentives across 32+ jurisdictions, and maximize your tax savings with a modern full-stack application.

## Features

- **32 Global Jurisdictions** — Compare incentives across USA, Canada, UK, and more
- **Tax Incentive Calculator** — Instant credit estimates with compliance checks and downloadable reports
- **Production Management** — Track productions, budgets, and locations
- **Dashboard** — Modern React interface with real-time metrics and zoom controls
- **PDF & Excel Reports** — Professional documentation for stakeholders
- **Type-Safe** — Full TypeScript coverage for reliability
- **Comprehensive Testing** — 51 frontend tests + 127 backend tests passing

---

## Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 20+** and **npm 10+**
- **PostgreSQL 16**
- **Visual Studio Code** (recommended) - See [VS Code Setup Guide](./VSCODE_SETUP.md)

### Getting Started with VS Code

For the best development experience, we recommend using Visual Studio Code:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hneal055/Tax_Incentive_Compliance_Platform.git
   cd Tax_Incentive_Compliance_Platform
   ```

2. **Open in VS Code**:
   ```bash
   code PilotForge.code-workspace
   ```

3. **Install recommended extensions** when prompted

4. **Follow the setup wizard** in the [VS Code Setup Guide](./VSCODE_SETUP.md)

The workspace includes pre-configured:
- ✅ Python debugging and testing
- ✅ TypeScript/React IntelliSense
- ✅ Integrated tasks for build, test, and run
- ✅ Code formatting and linting
- ✅ Database management with Prisma

**OR** use **Docker** (recommended for quick setup):
- **Docker** version 20.10+
- **Docker Compose** version 2.0+

### 🐳 Docker (Easiest - Recommended)

```bash
# Build and start all services (database, backend, frontend)
docker compose up --build -d

# Or use the test script
./docker-test.sh
```

This starts:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

See [README-DOCKER.md](./README-DOCKER.md) for detailed Docker documentation.

### Full Stack (Recommended)

**Windows:**
```powershell
.\start-fullstack.ps1
```

**Linux/Mac:**
```bash
./start-fullstack.sh
```

This starts:
- Backend API: http://localhost:8000
- Frontend UI: http://localhost:5200

### Backend Only

```bash
python -m venv .venv
source .venv/bin/activate          # Linux/Mac
# .\.venv\Scripts\Activate.ps1    # Windows

pip install -r requirements.txt
python -m prisma generate
python -m prisma migrate deploy
python -m uvicorn src.main:app --reload
```

API Docs: http://localhost:8000/docs

### Frontend Only

```bash
cd frontend
npm install
npm run dev -- --port 5200
```

Frontend UI: http://localhost:5200

### Developer Portal

```bash
cd developer-portal
npm install
npm run dev
```

Developer Portal: http://localhost:3000

The Developer Portal provides comprehensive API documentation with interactive Swagger UI and ReDoc interfaces.

---

## Technology Stack

### Backend
- **Python 3.12** — Modern Python with type hints
- **FastAPI 0.115** — High-performance async web framework
- **PostgreSQL 16** — Robust relational database
- **Prisma ORM** — Type-safe database access
- **Pytest** — Comprehensive testing (127/127 passing)
- **ReportLab & openpyxl** — PDF and Excel generation

### Frontend
- **React 19** — Latest React with concurrent rendering
- **TypeScript 5.9** — Type-safe development
- **Vite 7** — Lightning-fast build tool with HMR
- **TailwindCSS 4** — Utility-first styling framework
- **Zustand** — Lightweight state management
- **Vitest** — Unit and integration testing (51/51 passing)
- **React Router v7** — Client-side routing
- **Axios** — Typed HTTP client for API calls

---

## Project Structure

```
Tax_Incentive_Compliance_Platform/
├── src/                     # Backend Python application
│   ├── main.py             # FastAPI app entry (async lifespan, CORS, health check)
│   ├── api/                # API route handlers
│   │   ├── routes.py       # Router registry (8 sub-routers)
│   │   ├── jurisdictions.py
│   │   ├── productions.py
│   │   ├── calculator.py
│   │   ├── expenses.py
│   │   ├── incentive_rules.py
│   │   ├── reports.py
│   │   ├── excel.py
│   │   └── rule_engine.py
│   ├── models/             # Pydantic request/response models
│   ├── rule_engine/        # Jurisdiction rule evaluation engine
│   └── utils/              # Config, DB, PDF/Excel generators
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── api/           # Axios API client and service layer
│   │   ├── components/    # Reusable UI (Card, Button, Modal, Navbar, etc.)
│   │   ├── pages/         # Route pages (Dashboard, Productions, Jurisdictions, Calculator)
│   │   ├── store/         # Zustand state management
│   │   ├── types/         # TypeScript interfaces
│   │   ├── utils/         # Report generation utilities
│   │   └── test/          # Vitest test suite
│   └── vitest.config.ts
├── developer-portal/       # Next.js API documentation portal
│   ├── app/               # Next.js App Router pages
│   │   ├── page.tsx       # Homepage with API overview
│   │   ├── docs/          # Swagger UI documentation
│   │   └── redoc/         # ReDoc documentation
│   └── public/
│       └── openapi.json   # OpenAPI 3.1 specification
├── prisma/                 # Database schema and migrations
├── rules/                  # Jurisdiction tax rule definitions (JSON)
├── tests/                  # Backend test suite
├── docs/                   # Documentation
└── requirements.txt        # Python dependencies
```

---

## Frontend Pages

### Dashboard
- Production count overview with trend indicators
- Jurisdiction metrics across 15+ active jurisdictions
- Quick overview list with clickable production rows
- Recent activity feed with status indicators
- System compliance card with report navigation
- Zoom controls (50%–150%) with localStorage persistence
- System health monitoring (live backend ping)

### Productions Management
- Create, view, edit, delete productions
- Track budget, status, and filming details
- Associate with jurisdictions
- Side-panel detail view

### Jurisdictions Browser
- Browse all available jurisdictions (15 seeded)
- Filter by type (State, Country, Province)
- View incentive program descriptions and websites
- Search and sort options

### Tax Incentive Calculator
- Select production and jurisdiction from live data
- Calculate tax incentives with qualified expense breakdown
- **Generate Report** — Preview in new window or download as HTML
- Professional report includes financial breakdown, budget utilization bar, and disclaimers

---

## Testing

### Backend Tests
```bash
pytest                     # Run all tests
pytest -v                  # Verbose output
pytest --cov=src           # With coverage
```
**Coverage:** 127/127 tests passing

### Frontend Tests
```bash
cd frontend
npx vitest run             # Run all tests
npx vitest --watch         # Watch mode
```
**Coverage:** 51/51 tests across 8 test files (Dashboard, Button, Card, Input, Modal, Navbar, MetricCard, CreateProductionModal)

---

## Deployment

### Build Frontend
```bash
cd frontend
npm install
npm run build
```

### Deploy (Render.com)
```yaml
buildCommand: cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt && python -m prisma generate
startCommand: python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

**Production**: https://pilotforge.onrender.com

See [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed instructions.

---

## Real-Time Monitoring System ✨ **NEW**

### Overview

PilotForge now includes a **real-time legislative monitoring system** that watches external sources for changes to tax incentive programs and pushes instant alerts to your dashboard.

### Features

- **WebSocket Live Updates** — Real-time event notifications via WebSocket connections
- **NewsAPI Integration** — Automated monitoring of news sources for tax incentive changes
- **LLM Summarization** — AI-powered summaries using OpenAI GPT-4o-mini
- **Email/Slack Notifications** — Critical alerts sent via email and Slack
- **Jurisdiction Tracking Dashboard** — Dedicated UI for monitoring all jurisdictions

### Architecture

```
┌─────────────────────┐     ┌──────────────────────┐     ┌────────────────────┐
│   Data Collection    │     │   Event Pipeline      │     │   Live Frontend    │
│                      │     │                       │     │                    │
│  • News API feeds    │────▶│  • FastAPI async      │────▶│  • WebSocket conn  │
│  • RSS/Atom feeds    │     │  • PostgreSQL events   │     │  • Zustand events  │
│  • Gov open data     │     │  • Change detection    │     │  • Notification UI │
│  • Web scraping      │     │  • APScheduler cron    │     │  • Alert feed      │
│  • LLM summarization │     │  • WebSocket push      │     │  • Toast alerts    │
└─────────────────────┘     └──────────────────────┘     └────────────────────┘
```

### Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   ```bash
   # NewsAPI (free tier: 100 requests/day)
   NEWS_API_KEY=your-newsapi-key-here
   MONITOR_INTERVAL_HOURS=4
   
   # OpenAI for LLM Summarization
   OPENAI_API_KEY=your-openai-api-key-here
   OPENAI_MODEL=gpt-4o-mini
   
   # Email Notifications (SMTP)
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@example.com
   SMTP_PASSWORD=your-app-password
   NOTIFICATION_FROM_EMAIL=noreply@pilotforge.com
   NOTIFICATION_TO_EMAILS=admin@example.com,alerts@example.com
   
   # Slack Notifications
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   SLACK_CHANNEL=#pilotforge-alerts
   ```

3. **Seed Monitoring Sources**:
   ```bash
   python seed_monitoring_sources.py
   ```

4. **Access Monitoring Dashboard**:
   - Navigate to http://localhost:5200/monitoring
   - View real-time events, unread count, and WebSocket connection status
   - Click events to mark as read and view source links

### API Endpoints

- `GET /api/v1/monitoring/events` — List monitoring events with filters
- `GET /api/v1/monitoring/events/unread` — Get unread event count
- `PATCH /api/v1/monitoring/events/:id/read` — Mark event as read
- `GET /api/v1/monitoring/sources` — List monitoring sources
- `POST /api/v1/monitoring/sources` — Add new monitoring source
- `WS /api/v1/monitoring/ws` — WebSocket endpoint for real-time updates

### How It Works

1. **Scheduled Monitoring**: APScheduler runs background tasks every 5 minutes (RSS/web) and 4 hours (NewsAPI)
2. **Change Detection**: Each source is monitored via SHA-256 content hashing
3. **Event Creation**: When changes are detected, events are created with AI-generated summaries
4. **Real-Time Push**: Events are broadcast via WebSocket to connected frontend clients
5. **Notifications**: Critical severity events trigger email/Slack notifications
6. **User Actions**: Users can view, filter, and mark events as read in the dashboard

### Event Types

- **incentive_change** — Changes to existing tax credit programs
- **new_program** — Launch of new incentive programs
- **expiration** — Upcoming or past deadline alerts
- **news** — General news articles about tax incentives

### Severity Levels

- **🚨 Critical** — Urgent deadlines, major changes requiring immediate action
- **⚠️ Warning** — Important updates that may impact productions
- **ℹ️ Info** — General news and minor updates

### Cost Estimate

| Service | Monthly Cost | Notes |
|---------|--------------|-------|
| NewsAPI (free tier) | $0 | 100 requests/day, sufficient for 4-hour intervals |
| NewsAPI (paid) | $49 | 1,000 requests/day for higher frequency |
| OpenAI GPT-4o-mini | $10–50 | ~100 summaries/day at current pricing |
| Email (SMTP) | $0 | Use existing email provider |
| Slack | $0 | Free webhook integration |
| **Total** | **$10–100/mo** | Depends on volume and API tier |

---

## Next Phase: Real-Time Jurisdiction Monitoring

### Vision

A real-time monitoring system that watches external sources — state film commission websites, legislative trackers, news feeds — for changes to tax incentive programs, rebates, and grants, then pushes alerts to the PilotForge dashboard as they happen.

### Why This Matters

Tax incentive programs change frequently. States modify credit percentages, cap amounts shift, new programs launch, and existing ones expire — often with limited notice. Currently, production companies rely on manual research or expensive consultants to stay current. PilotForge monitoring would provide an automated early warning system that keeps users ahead of changes that directly impact their bottom line.

### Architecture

```
┌─────────────────────┐     ┌──────────────────────┐     ┌────────────────────┐
│   Data Collection    │     │   Event Pipeline      │     │   Live Frontend    │
│                      │     │                       │     │                    │
│  • News API feeds    │────▶│  • FastAPI async      │────▶│  • WebSocket conn  │
│  • RSS/Atom feeds    │     │  • PostgreSQL events   │     │  • Zustand events  │
│  • Gov open data     │     │  • Change detection    │     │  • Notification UI │
│  • Web scraping      │     │  • APScheduler cron    │     │  • Alert feed      │
│  • LLM summarization │     │  • WebSocket push      │     │  • Toast alerts    │
└─────────────────────┘     └──────────────────────┘     └────────────────────┘
```

### Implementation Plan

#### Phase 1 — Data Models & REST API (Week 1, Days 1–3)

**Objective:** Establish the database foundation and basic CRUD for monitoring events.

- [ ] Add `MonitoringSource` model to Prisma schema
  - Fields: `jurisdictionId`, `sourceType` (rss/api/webpage), `url`, `checkInterval`, `lastCheckedAt`, `lastHash`, `active`
- [ ] Add `MonitoringEvent` model to Prisma schema
  - Fields: `jurisdictionId`, `sourceId`, `eventType` (incentive_change/new_program/expiration/news), `severity` (info/warning/critical), `title`, `summary`, `sourceUrl`, `detectedAt`, `readAt`, `metadata`
- [ ] Create `src/api/monitoring.py` with REST endpoints:
  - `GET /api/v1/monitoring/events` — paginated event feed with filters
  - `GET /api/v1/monitoring/events/unread` — unread count
  - `PATCH /api/v1/monitoring/events/:id/read` — mark as read
  - `GET /api/v1/monitoring/sources` — list configured sources
  - `POST /api/v1/monitoring/sources` — add new source
- [ ] Register router in `src/api/routes.py`
- [ ] Write Pytest tests for all new endpoints

#### Phase 2 — WebSocket & Frontend Real-Time UI (Week 1–2, Days 3–6)

**Objective:** Push events to the browser in real-time and display them.

- [ ] Add WebSocket endpoint `ws://localhost:8000/ws/events` in FastAPI
  - Broadcast new events to all connected clients
  - Support connection heartbeat/ping-pong
- [ ] Create frontend WebSocket connection manager (`src/utils/wsClient.ts`)
  - Auto-reconnect with exponential backoff
  - Parse incoming event payloads
- [ ] Extend Zustand store with `monitoringEvents` slice
  - `events: MonitoringEvent[]`, `unreadCount: number`
  - Actions: `addEvent()`, `markRead()`, `fetchEvents()`
- [ ] Add notification bell/badge to Navbar showing unread count
- [ ] Add event feed panel to Dashboard (replace or augment "Recent Activity" card)
- [ ] Add toast notifications for critical severity alerts
- [ ] Write Vitest tests for new components

#### Phase 3 — News API Integration (Week 2, Days 7–9)

**Objective:** Automated keyword monitoring across news sources.

- [ ] Integrate NewsAPI (free tier: 100 requests/day) or GNews API
  - Keywords: `"film tax credit"`, `"production incentive"`, `"film rebate"`, `"entertainment tax"`, per-jurisdiction terms
- [ ] Create `src/services/news_monitor.py`
  - Async news fetcher with httpx
  - Deduplication via article URL hashing
  - Map articles to relevant jurisdictions by keyword matching
- [ ] Create `MonitoringEvent` records from matched articles
- [ ] Add APScheduler background task (runs every 4 hours)
- [ ] Configure via environment variables (`NEWS_API_KEY`, `MONITOR_INTERVAL_HOURS`)

#### Phase 4 — RSS Feed Monitoring (Week 2–3, Days 9–12)

**Objective:** Watch film commission and government RSS feeds for program updates.

- [ ] Add `feedparser` dependency
- [ ] Create `src/services/rss_monitor.py`
  - Parse RSS/Atom feeds from film commissions
  - Content-hash-based change detection (`lastHash` field)
  - Extract title, summary, publication date
- [ ] Seed initial `MonitoringSource` records for key jurisdictions:
  - California Film Commission, New York Governor's Office, Georgia Film Office, etc.
- [ ] Schedule feed checks via APScheduler (configurable per-source interval)
- [ ] Write deduplication logic (avoid repeat alerts for the same story)

#### Phase 5 — Web Scraping for Commission Pages (Week 3–4, Days 12–16)

**Objective:** Monitor specific film commission pages that don't offer RSS.

- [ ] Create `src/services/page_monitor.py`
  - Fetch page HTML via httpx
  - Compute content hash; compare against stored `lastHash`
  - On change: extract text diff, create MonitoringEvent
- [ ] Add configurable CSS selectors per source (target specific page sections)
- [ ] Implement retry logic and error handling (sites go down, layouts change)
- [ ] Add admin endpoint to manually trigger a source check
- [ ] Note: This layer is inherently fragile — design for graceful degradation

#### Phase 6 — LLM-Assisted Summarization (Week 4, Days 16–18)

**Objective:** Use AI to summarize detected changes into actionable alerts.

- [ ] Integrate OpenAI API (or equivalent) for text summarization
- [ ] When a change is detected, send the diff/article text to LLM with prompt:
  - "Summarize this tax incentive change for a film production company. Include: what changed, effective date, impact on qualifying productions."
- [ ] Store LLM summary in `MonitoringEvent.summary`
- [ ] Add cost controls: cache results, rate-limit API calls, token budgets
- [ ] Configure via `OPENAI_API_KEY` environment variable

### New Dependencies Required

**Backend (requirements.txt):**
```
apscheduler>=3.10         # Background task scheduling
feedparser>=6.0           # RSS/Atom feed parsing
```

**Frontend:** None — native `WebSocket` API + existing Zustand is sufficient.

### Cost Estimate

| Component | Cost | Notes |
|---|---|---|
| NewsAPI (free tier) | $0 | 100 requests/day, sufficient for hourly checks |
| NewsAPI (paid) | $49/mo | 1,000 requests/day, historical search |
| OpenAI summarization | $10–50/mo | ~100 summaries/day at GPT-4o-mini pricing |
| Infrastructure | $0 | Runs on existing FastAPI server |
| RSS feeds | $0 | Public feeds, no API key needed |

### Success Metrics

- **Alert latency:** < 4 hours from source publication to user notification
- **False positive rate:** < 15% of alerts are irrelevant
- **Jurisdiction coverage:** 10+ jurisdictions monitored at launch
- **User engagement:** > 60% of alerts are read within 24 hours

---

## Documentation

- **[VS Code Setup Guide](./VSCODE_SETUP.md)** — Getting started with Visual Studio Code (recommended)
- **[Frontend Setup Guide](./docs/FRONTEND_SETUP.md)** — Complete frontend development guide
- **[Backend Architecture](./docs/README.md)** — Backend setup and architecture
- **[Deployment Guide](./docs/DEPLOYMENT.md)** — Production deployment instructions
- **[User Manual](./docs/USER_MANUAL.md)** — API reference and UI guide
- **[API Examples](./docs/API_EXAMPLES.md)** — Code samples in Python, JavaScript, TypeScript
- **[Roadmap](./docs/ROADMAP.md)** — Development phases and future plans
- **[UI Setup](./UI_SETUP.md)** — Comprehensive UI setup and troubleshooting

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest` for backend, `npx vitest run` for frontend)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## License

**Proprietary and Confidential**

Copyright (c) 2026 PilotForge - Tax Incentive Compliance Platform. All Rights Reserved.

This software is proprietary and confidential. Unauthorized copying, distribution, modification, or use is strictly prohibited. See [LICENSE](./LICENSE) for full terms and restrictions.

## Support

- **Documentation**: Check the [docs/](./docs/) directory
- **Issues**: Open a [GitHub Issue](https://github.com/hneal055/Tax_Incentive_Compliance_Platform/issues)
- **API Questions**: See [API_EXAMPLES.md](./docs/API_EXAMPLES.md)
- **Frontend Setup**: See [FRONTEND_SETUP.md](./docs/FRONTEND_SETUP.md)

---

**Built with care for the film and television industry**
