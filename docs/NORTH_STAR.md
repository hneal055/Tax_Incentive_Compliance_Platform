# Tax-Incentive Compliance API — North Star

## Mission
Build a **Jurisdictional Rule Engine** that helps **production companies, accountants, and studios**:
- **maximize eligible tax incentives** (credits, rebates, grants),
- **ensure compliance** with jurisdiction-specific requirements,
- and produce **auditable calculation outputs** that can be defended.

## The North Star Product
A FastAPI-based platform that:
1) **Stores** multi-jurisdiction incentive programs and rules  
2) **Evaluates** eligibility and computes incentive outcomes  
3) **Explains** *why* a result happened (traceable reasoning)  
4) **Audits** who/what/when for compliance and reproducibility

## Who It Serves
- Production companies (film/TV)
- Accountants / tax incentive specialists
- Studios and finance teams

## Core Problem
Tax incentive rules vary widely across **states/provinces/countries**, with complex constraints:
- eligible expense categories
- labor residency rules
- caps, thresholds, and minimum spends
- effective dates, sunsets, and program changes
- documentation/compliance requirements

## Core Principles (Non-Negotiables)
### 1) Auditability by design
Every calculation must store:
- input snapshot (production + expenses + assumptions)
- rule version used (jurisdiction + effective date window)
- outputs (numbers) and **explanation trace**
- timestamps and user identity (where applicable)

### 2) Configuration-driven rules (portable + maintainable)
Rules must be definable in **JSON/YAML** (and/or DB-backed equivalents) so new jurisdictions
can be added without rewriting core engine logic.

### 3) Correctness over cleverness
We prioritize:
- deterministic results
- strict validation
- clear error messages
- safe defaults

### 4) Stable, repeatable environment
To avoid drift:
- use the project venv consistently
- pin dependencies
- keep “known-good” baselines (tags/releases)

## Current Technical Stack
- **API:** FastAPI
- **Database:** PostgreSQL
- **ORM/Client:** Prisma (prisma-client-py)
- **Dev tools:** Python + PowerShell + VS Code
- **Docs:** Markdown in /docs

## Data Model (Core Entities)
- **Jurisdictions** — states/provinces/countries
- **Incentive Rules** — credits/rebates/grants; effective dates; eligibility constraints
- **Productions** — project tracking and metadata
- **Expenses** — categorized spend (labor, in-state, qualified, etc.)
- **Calculations** — computed incentive outputs + trace/explanations
- **Users** — auth/roles (as needed)
- **Audit Logs** — immutable event trail

## What “Done” Looks Like (MVP Definition)
A user can:
1) pick a jurisdiction and a production
2) enter/import expenses (categorized)
3) run a calculation
4) receive:
   - computed incentive amount
   - compliance/eligibility flags
   - an explanation trace (what rules applied and why)
5) export results for accounting workflows (JSON/CSV later)

## Guardrails (Prevent Scope Creep)
We do NOT build advanced UI/analytics before:
- rule format is defined
- evaluator is implemented
- results are auditable and reproducible
- test coverage exists for core rules

## Daily Workflow Pattern (Target)
1) update DB schema / rules as needed
2) seed / validate reference data
3) run tests
4) run API and verify /docs + endpoints
5) commit small, verifiable changes to GitHub
