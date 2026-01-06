# Tax-Incentive Compliance API — North Star

## Mission
Build a **Jurisdictional Rule Engine** that helps production companies, accountants, and studios **maximize eligible incentives** while **ensuring audit-ready compliance** across multiple jurisdictions.

## Purpose
- Normalize incentive programs (credits, rebates, grants) into a consistent rules model
- Evaluate productions + expenses against jurisdiction rules
- Produce transparent calculations and defensible audit trails

## Primary Users
- Production accounting teams
- Studios / finance teams
- Incentive compliance accountants / auditors
- Producers who need planning estimates (pre-production)

## Core Capabilities
1) **Jurisdictions**
   - Store jurisdictions (state/province/country)
   - Search/filter/sort, active flags, metadata

2) **Incentive Rules**
   - Model programs (effective dates, thresholds, categories, caps)
   - Rule versioning + activation/deactivation

3) **Productions + Expenses**
   - Track productions (dates, jurisdiction, status)
   - Track expenses (category, amount, eligibility attributes)

4) **Calculation Engine**
   - Compute qualified spend
   - Apply rates, caps, and thresholds
   - Emit compliance flags (why something was excluded)
   - Output a calculation “trace” (audit trail)

5) **Compliance & Auditability**
   - Audit log of rule changes + calculations
   - Reproducible results (same inputs → same outputs)

## Non-Goals (for MVP)
- Full UI / dashboard
- Complex multi-jurisdiction stacking logic
- Automated document ingestion/receipt OCR
- Real-time integrations with third-party accounting systems

## Engineering Principles
- **Deterministic**: same inputs produce same outputs
- **Explainable**: trace every decision (included/excluded)
- **Extensible**: add new jurisdictions/rules without code rewrites
- **Tested**: unit tests for engine; API contract tests later
- **Secure by default**: env-based config, least privilege DB users

## Architecture (Current Direction)
- FastAPI (Python) API layer
- PostgreSQL as source of truth
- Prisma Client Python for DB access
- Rule engine as a pure-Python module (testable independently)
- Docker/Docker Compose for dev + prod stacks (later)

## Definition of Done (MVP)
- List jurisdictions reliably from DB
- Create/read incentive rules
- Run a calculation: inputs → eligibility + benefit + trace
- Seed scripts are idempotent (upsert)
- Tests pass in a clean local environment
