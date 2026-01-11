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
