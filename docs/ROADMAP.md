# ROADMAP — Phase Plan (Aligned to NORTH STAR)

This roadmap is intentionally **Rule-Engine-first**. Everything else builds on that foundation.

---

## Phase 1 — Rule Engine MVP (Canonical + Tested)
**Goal:** A stable jurisdictional rule engine that evaluates eligibility + incentive amount with a tight response contract.

### Deliverables
- Canonical rules registry:
  - `<repo_root>/rules/<CODE>.json`
  - Missing rule → 404 at API layer
- Rule evaluator:
  - Computes eligible spend
  - Applies rate/caps
  - Returns contract-stable payload
- Rule Engine API:
  - `POST /api/v1/rule-engine/evaluate`
  - Optional `?debug=true` for trace/meta
- Tests:
  - Happy path (e.g., IL)
  - Unknown jurisdiction / missing rule file behavior

### Phase 1 Endpoints (Canonical)
- `GET  /api/v1/` (index)
- `GET  /api/v1/jurisdictions`
- `GET  /api/v1/jurisdictions/{code}`
- `GET  /api/v1/incentive-rules`
- `GET  /api/v1/incentive-rules/{id-or-code}`
- `POST /api/v1/rule-engine/evaluate`  ✅ Contract-stable

### Exit Criteria
- Contract fields ALWAYS present:
  - `jurisdiction_code`, `total_eligible_spend`, `total_incentive_amount`, `breakdown[]`
- Tight payload by default
- All tests pass consistently

---

## Phase 2 — Production Inputs + Saved Evaluations
**Goal:** Feed the engine with real production context and persist results for downstream workflows.

### Deliverables
- Minimal domain APIs:
  - Productions
  - Expenses
  - Calculations (saved evaluation runs)
- Persisted evaluation:
  - Save request + response snapshot for audits & reports
- Validation rules:
  - Expense normalization (categories, currency, payroll flags, residency)

### Phase 2 Endpoints (Target)
- `POST /api/v1/productions`
- `GET  /api/v1/productions`
- `GET  /api/v1/productions/{id}`
- `POST /api/v1/expenses`
- `GET  /api/v1/expenses?production_id=...`
- `POST /api/v1/calculations` (save an evaluation)
- `GET  /api/v1/calculations?production_id=...`
- `GET  /api/v1/calculations/{id}`

### Exit Criteria
- Production + expenses flow cleanly into evaluation
- Saved calculations retrievable and consistent

---

## Phase 3 — Compliance, Audit Trail, Reporting
**Goal:** Make results defensible, exportable, and executive-friendly.

### Deliverables
- Audit logging + evidence chain
- Documentation package generation (JSON/CSV bundles, summary reports)
- Comparisons:
  - Compare multiple jurisdictions for “best incentive vs risk”
- Reporting surfaces (API-first; UI later)

### Phase 3 Endpoints (Target)
- `GET  /api/v1/audit-logs`
- `GET  /api/v1/audit-logs/{id}`
- `GET  /api/v1/reports/dashboard`
- `POST /api/v1/reports/incentives`
- `POST /api/v1/reports/comparison`

---

## Notes on the “20 Endpoints” Concept
We can absolutely end up with ~20+ endpoints, but they must be introduced in this order:
1) Engine + contract stability
2) Inputs + persistence
3) Compliance + reporting
4) UI/dashboard (optional) as a consumer of the API — not the driver of architecture

---

## Phase 4 — Frontend Development ✅
**Goal:** Build a modern, production-ready React UI to consume the API and provide an intuitive user experience.

### Status: **COMPLETED** 🎉

### Deliverables
- ✅ Modern React 19 + TypeScript frontend
- ✅ Vite 7 build system with HMR
- ✅ TailwindCSS 4 styling system
- ✅ Zustand state management
- ✅ React Router v7 navigation
- ✅ Typed Axios API client

### Implemented Pages
- ✅ **Dashboard**: Production metrics, jurisdiction overview, quick actions
- ✅ **Productions**: Full CRUD interface with form validation
- ✅ **Jurisdictions**: Browse and filter 32 jurisdictions
- ✅ **Calculator**: Tax incentive calculation with production/jurisdiction selection

### Technical Implementation
**Component Library:**
- ✅ Button, Card, Input, Spinner components
- ✅ Navbar with active route highlighting
- ✅ Layout wrapper with responsive design

**State Management:**
- ✅ Productions store with CRUD operations
- ✅ Jurisdictions store with filtering
- ✅ Loading states and error handling

**API Integration:**
- ✅ Typed service methods for all endpoints
- ✅ Axios client with baseURL configuration
- ✅ TypeScript interfaces for API contracts

### Future Enhancements (Planned)
- [ ] Authentication & Authorization UI
  - Login/logout flows
  - User profile management
  - Role-based access control
- [ ] Advanced Filtering & Search
  - Multi-criteria jurisdiction filtering
  - Production search by title/date/status
  - Saved search preferences
- [ ] Enhanced Calculator Features
  - Multi-jurisdiction comparison view
  - Scenario modeling interface
  - Compliance verification workflow
- [ ] Mobile Responsive Improvements
  - Touch-optimized interactions
  - Mobile-first dashboard layout
  - Progressive Web App (PWA) capabilities
- [ ] Data Visualization
  - Charts for savings comparisons
  - Interactive jurisdiction maps
  - Production timeline views
- [ ] Export & Sharing
  - PDF report generation from UI
  - Excel export functionality
  - Shareable calculation links
- [ ] Offline Support
  - Service worker implementation
  - Cached jurisdiction data
  - Offline calculation mode
- [ ] Performance Optimizations
  - Code splitting per route
  - Lazy loading components
  - Image optimization

### Exit Criteria
- ✅ All core pages implemented and functional
- ✅ Type-safe API integration
- ✅ Responsive design across devices
- ✅ Production build optimized
- ✅ Documentation complete
