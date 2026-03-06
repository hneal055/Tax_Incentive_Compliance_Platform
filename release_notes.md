
## What's New

---

### v1.2.0 — March 6, 2026

**AI Strategic Advisor**
- New `POST /api/v1/advisor/recommend` endpoint proxies requests to Anthropic Claude (claude-sonnet-4-6) server-side — API key never exposed to the browser
- `AdvisorView` in the dashboard calls the backend proxy instead of the Anthropic API directly
- Requires `ANTHROPIC_API_KEY` in `.env`; dependency added to `requirements.docker.txt`

**Live Regulatory Feed**
- `JurisdictionsView` now fetches monitoring events from `GET /api/v1/monitoring/events/` on load
- Events rendered with relative timestamps and severity badges (info / warning / critical)
- Replaced static hard-coded array with live API data

**Regulatory Monitoring REST API (Phase 1 complete)**
- New `src/api/monitoring.py` registered in `src/api/routes.py`
- Endpoints: `GET /events/`, `GET /events/unread/`, `PATCH /events/:id/read`, `GET /sources/`, `POST /sources/`
- Prisma migration `20260306173718_add_monitoring_tables` adds `MonitoringEvent` and `MonitoringSource` tables

**Mock Data Mode**
- New `frontend/src/api/mock.ts` — 8 jurisdictions, 8 incentive rules, 4 productions, 5 monitoring events
- `isMockMode()` reads `localStorage` at call-time; no build change required to toggle
- `api/index.ts` wrapped in a Proxy that redirects API calls to mock implementations when active
- `apiFetch()` in `App.tsx` path-matches against `MOCK_FETCH_RESPONSES` when mock mode is on

**Settings Page**
- Settings now accessible from the main sidebar nav (gear icon + "Settings" label)
- `SettingsView` component in `App.tsx` (monolithic UI) reads/writes `pilotforge_settings` localStorage directly
- Developer Tools panel: Mock Data Mode toggle with amber styling and ACTIVE badge, stat counters, API Configuration info card
- `pages/Settings.tsx` (modular UI) also updated with Developer Tools card using `useSettings` hook

**Backend Routing Fix**
- Removed `/{full_path:path}` catch-all route that was shadowing API path normalization
- SPA serving moved to `@app.exception_handler(404)` — non-API 404s serve `index.html`
- Eliminated trailing-slash middleware that caused redirect loops on monitoring endpoints

---

### v1.1.0 — January 11, 2026

- Stackable credits endpoint combining multiple incentive rules
- Batch rule fetching in compare endpoint (eliminates N+1 queries)
- Compliance checker refactored to `ComplianceChecker` class
- Improved handling of missing/zero qualifying budgets with user notes
- All pytest collection and runtime failures resolved (127/127 passing)

---

### v1.0.0 — January 10, 2026

- Initial release: FastAPI backend with Prisma/PostgreSQL
- React 19 + TypeScript + Vite 7 frontend
- 32 jurisdictions, 33 incentive programs seeded
- Tax incentive calculator with compliance checking
- PDF and Excel report generation
- 51 frontend tests + 127 backend tests
