# Tax-Incentive Compliance API — Roadmap

## Phase 1 — Rule Engine MVP
- Stabilize jurisdictions endpoint (tight payload, paging, filters)
- Incentive rules CRUD (MVP fields)
- Rule evaluator (qualified spend, thresholds, caps, trace)
- Seed scripts are idempotent (upsert)
- Unit tests for evaluator + basic API smoke tests

## Phase 2 — Production + Expense Tracking
- Productions CRUD
- Expenses CRUD with eligibility attributes (in-state, labor/resident, categories)
- Calculation records persisted (inputs, outputs, trace)

## Phase 3 — Compliance & Audit
- Audit logs on rule changes + calculations
- Role-based access (basic)
- Exportable reports (JSON/CSV)

## Phase 4 — Hardening & Deploy
- Docker Compose dev stack + production deploy path
- CI (lint/test) + CD (staging/prod)
- Performance + pagination tuning
- Documentation polish (LOCAL_SETUP, TROUBLESHOOTING, API examples)

## Phase 5 — Advanced Incentive Logic
- Multi-tier rates, bonuses, exclusions
- Jurisdiction-specific special cases
- Rule versioning + effective-date selection
