# PilotForge

> **Tax Incentive Intelligence for Film & TV Productions**

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6.svg)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

---

## Overview

PilotForge is a comprehensive tax incentive calculation and compliance platform for the global film and television industry. Manage productions, calculate tax incentives across 32+ jurisdictions, and maximize your tax savings with a modern full-stack application.

## Features

- **32 Global Jurisdictions** — Compare incentives across USA, Canada, UK, and more
- **Tax Incentive Calculator** — Instant credit estimates with compliance checks and downloadable reports
- **Production Management** — Track productions, budgets, and locations
- **Dashboard** — Modern React interface with real-time metrics and zoom controls
- **Live Regulatory Feed** — Real-time monitoring events pulled from the `/monitoring/events` API
- **AI Strategic Advisor** — Server-side Anthropic Claude proxy for budget and jurisdiction recommendations
- **Mock Data Mode** — Toggle between live API and built-in mock data for offline UI development
- **Settings Panel** — In-app settings with developer tools (mock mode, API config, currency, notifications)
- **PDF & Excel Reports** — Professional documentation for stakeholders
- **Type-Safe** — Full TypeScript coverage for reliability
- **Comprehensive Testing** — 51 frontend tests + 127 backend tests passing

---

## Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 20+** and **npm 10+**
- **PostgreSQL 16**

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
│   ├── main.py             # FastAPI app entry (async lifespan, CORS, SPA fallback via 404 handler)
│   ├── api/                # API route handlers
│   │   ├── routes.py       # Router registry (9 sub-routers)
│   │   ├── advisor.py      # AI Strategic Advisor — Anthropic proxy endpoint
│   │   ├── monitoring.py   # Regulatory monitoring events & sources
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
│   │   ├── api/
│   │   │   ├── client.ts  # Axios API client configuration
│   │   │   ├── index.ts   # API service layer (Proxy-wrapped for mock support)
│   │   │   └── mock.ts    # Built-in mock data + isMockMode() toggle helper
│   │   ├── components/    # Reusable UI (Card, Button, Modal, Navbar, etc.)
│   │   ├── hooks/
│   │   │   └── useSettings.ts  # UserSettings hook with localStorage persistence
│   │   ├── pages/         # Route pages (Dashboard, Productions, Jurisdictions, Calculator, Settings)
│   │   ├── store/         # Zustand state management
│   │   ├── types/         # TypeScript interfaces
│   │   ├── utils/         # Report generation utilities
│   │   ├── App.tsx        # Monolithic UI (active) with all views including Settings & AI Advisor
│   │   └── test/          # Vitest test suite
│   └── vitest.config.ts
├── prisma/                 # Database schema and migrations
│   └── migrations/        # All applied migrations (including monitoring tables)
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
- Live **Regulatory Feed** — recent monitoring events per jurisdiction
- Search and sort options

### Tax Incentive Calculator
- Select production and jurisdiction from live data
- Calculate tax incentives with qualified expense breakdown
- **Generate Report** — Preview in new window or download as HTML
- Professional report includes financial breakdown, budget utilization bar, and disclaimers

### AI Strategic Advisor
- Natural language recommendations for budget allocation and jurisdiction selection
- Server-side Anthropic Claude proxy — API key never exposed to browser
- Endpoint: `POST /api/v1/advisor/recommend`

### Settings
- Currency, default jurisdiction, notification preferences
- Dark mode and compact view toggles
- **Mock Data Mode** — one-click toggle for offline UI development with built-in fixture data
- API Configuration panel showing current data source, base URL, and version

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

## Monitoring & AI: Implementation Status

### Real-Time Jurisdiction Monitoring

A monitoring system that watches external sources — state film commission websites, legislative trackers, news feeds — for changes to tax incentive programs, rebates, and grants, then surfaces alerts in the PilotForge dashboard.

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

#### Phase 1 — Data Models & REST API ✅ COMPLETE

- [x] Added `MonitoringSource` model to Prisma schema (migration `20260306173718`)
- [x] Added `MonitoringEvent` model to Prisma schema
- [x] Created `src/api/monitoring.py` with REST endpoints:
  - `GET /api/v1/monitoring/events/` — paginated event feed with filters
  - `GET /api/v1/monitoring/events/unread/` — unread count
  - `PATCH /api/v1/monitoring/events/:id/read` — mark as read
  - `GET /api/v1/monitoring/sources/` — list configured sources
  - `POST /api/v1/monitoring/sources/` — add new source
- [x] Registered router in `src/api/routes.py`
- [x] Frontend `JurisdictionsView` fetches and renders live regulatory feed
- [x] AI Strategic Advisor (`src/api/advisor.py`) — Anthropic server-side proxy

#### Phase 2 — WebSocket & Frontend Real-Time UI (Next)

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

MIT License — Copyright (c) 2025-2026 Howard Neal - PilotForge

See [LICENSE](./docs/LICENSE) for full details.

## Support

- **Documentation**: Check the [docs/](./docs/) directory
- **Issues**: Open a [GitHub Issue](https://github.com/hneal055/Tax_Incentive_Compliance_Platform/issues)
- **API Questions**: See [API_EXAMPLES.md](./docs/API_EXAMPLES.md)
- **Frontend Setup**: See [FRONTEND_SETUP.md](./docs/FRONTEND_SETUP.md)

---

**Built with care for the film and television industry**
