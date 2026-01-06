# Roadmap (Short)

## Where We Are Now (Completed Foundation)
- PostgreSQL connectivity stabilized (local dev)
- Prisma client generation + schema sync (`db push`) working
- Core DB tables present (jurisdictions, incentive_rules, productions, expenses, calculations, users, audit_logs)
- Seeded **15 jurisdictions** and verified in SQL
- FastAPI app running with `/docs` and `/openapi.json`
- `/api/v1/jurisdictions` supports:
  - paging (limit/offset)
  - sorting (order_by/order_dir)
  - filtering/search
  - tight payload by default
  - optional `include_relations=true`

## Next: Phase 1 — Rule Engine MVP (Highest Priority)
### 1) Define rule format (JSON/YAML)
- effective dates (from/to)
- program type (credit/rebate/grant)
- rates and caps
- eligible expense categories
- thresholds/minimum spend
- exclusions and documentation flags
- versioning strategy

### 2) Implement evaluator (core engine)
Input:
- production + jurisdiction + expenses (+ optional assumptions)
Output:
- computed incentive values
- compliance flags
- explanation trace (rule application log)

### 3) API endpoints for rules + calculations
- CRUD incentive rules
- run calculation endpoint (store results)
- retrieve calculations history

### 4) Tests (must-have)
- unit tests for evaluator
- validation tests for rule format
- regression tests for “known-good” scenarios

## Phase 2 — Operational Hardening
- Docker Compose dev stack (API + Postgres)
- CI pipeline (GitHub Actions):
  - lint, type-check, tests
  - security scanning (basic)
  - build artifacts
- release tagging for “known good” baselines

## Phase 3 — Exports & Integration
- standard exports (JSON/CSV; Excel later)
- import helpers for expenses
- API usage examples + integration cookbook

## Phase 4 — UI (Only after MVP engine is stable)
- minimal admin UI for jurisdictions/rules
- calculation runner + results view
- audit review screens
