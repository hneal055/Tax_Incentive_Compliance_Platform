# PilotForge
> Tax Incentive Intelligence for Film & TV

## User Manual v2.0

**Platform Version:** 0.2.0
**API Version:** 0.1.0
**Last Updated:** April 11, 2026
**Documentation Standard:** OAS 3.1

---

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Platform Features](#platform-features)
4. [API Reference](#api-reference)
5. [Deployment Guide](#deployment-guide)
6. [Data Reference](#data-reference)
7. [Troubleshooting](#troubleshooting)
8. [Technical Specifications](#technical-specifications)

---

## Overview

### What is PilotForge?

PilotForge is a **film and television production tax incentive compliance platform** that helps production companies discover, compare, calculate, and stack tax incentives across US states, counties, and international jurisdictions.

### Who Should Use This Platform?

- **Production Companies** — Find the best locations for tax incentives
- **Production Accountants** — Calculate and track incentive claims
- **Line Producers** — Budget productions with accurate incentive estimates
- **Location Scouts** — Identify financially advantageous filming locations
- **Studios** — Strategic planning for multi-project slates

### Key Capabilities

- **35+ incentive programs** across 23 state/country jurisdictions
- **11 sub-jurisdictions** (counties and cities) with stacked local incentives
- **Scenario Calculator** — compare 2–6 jurisdictions side-by-side, finds best stack
- **AI Advisor** — natural language queries powered by Claude
- **Automated Feed Monitoring** — daily checks of government pages for rule changes
- **Pending Rules Review** — AI-extracted rules from county/city sites awaiting approval
- **MMB Connector** — CSV upload tool for Motion Picture Association data
- **JWT Authentication** — secure login with role-based access

---

## Getting Started

### Production URL

```
https://taxincentivecomplianceplatform-production.up.railway.app
```

### Local Development URL

```
http://localhost:3000
```

### Login Credentials

| Field | Value |
|-------|-------|
| Email | `admin@pilotforge.com` |
| Password | `pilotforge2024` |

> **Note:** Change the admin password in production via the Admin panel.

### API Base URL

```
/api/0.1.0
```

**Interactive docs:** `{base_url}/docs` (Swagger UI)

### Authentication

All API endpoints (except `/auth/login`) require a JWT Bearer token.

**Login:**
```bash
POST /api/0.1.0/auth/login
Content-Type: application/json

{
  "email": "admin@pilotforge.com",
  "password": "pilotforge2024"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

**Use the token:**
```bash
curl -H "Authorization: Bearer eyJ..." https://{host}/api/0.1.0/jurisdictions/
```

---

## Platform Features

### Dashboard

The Dashboard provides a real-time overview of:
- Total productions, budget, and qualifying spend
- Active jurisdictions count
- Incentive rules count
- Budget vs. actual spend bar chart across all productions

---

### Productions

Manage film and TV production records.

**Create a production** via the modal — fields:
- Title, Production Type, Jurisdiction
- Budget Total, Budget Qualifying
- Start Date, End Date
- Production Company, Status, Contact

**Production status values:** `planning` | `pre_production` | `production` | `post_production` | `completed`

---

### Incentive Calculator

Run a quick calculation for a single production against a jurisdiction:
1. Select a production
2. Select a jurisdiction
3. Click **Calculate** to see incentive amount, effective rate, and expense breakdown

---

### Jurisdictions

Browse all 23 state/country jurisdictions. Click any jurisdiction to view:
- Incentive programs with rates, min spend, and max credit caps
- Active local rules (county/city level)
- Sub-jurisdictions (counties/cities within the state)

---

### AI Advisor

Natural language interface to the platform's data powered by Claude (Anthropic).

**Example queries:**
- "Which state has the highest rebate for a $10M feature?"
- "What are Georgia's minimum spend requirements?"
- "Compare New York and Illinois incentives for a $5M TV series"

> Requires `ANTHROPIC_API_KEY` environment variable to be set.

---

### Georgia

Dedicated Georgia incentive workspace — pre-loaded with Georgia-specific rules, compliance checklist, and budget tools.

---

### MMB Connector

Upload a CSV file from the Motion Picture Association / MMB system. The connector:
1. Parses each row with field-level validation
2. Auto-populates production fields
3. Flags validation errors per row before import

**CSV format:** Standard MMB export format. See column headers in the upload modal.

---

### Local Rules

View approved county and city incentive rules. These are rules extracted from government websites by the feed monitor and approved through the Rule Review workflow.

**Filters:** Category (tax_credit, rebate, fee_waiver, grant), search by name/jurisdiction.

**Stats bar:** Total rules | AI-extracted | Manually entered

---

### Rule Review

Approve or reject AI-extracted incentive rules before they go live.

**Workflow:**
1. `monitor.py` fetches government pages daily and queues Claude-extracted rules as `pending`
2. Reviewer opens **Rule Review**, expands a pending rule to see extracted fields
3. Click **Approve** (with optional notes) → rule is promoted to `local_rules` table
4. Click **Reject** → rule is archived with notes

**Confidence scores** are color-coded: green (≥0.8), amber (0.5–0.8), red (<0.5).

---

### Scenario Calculator

Compare state + local incentive stacks across 2–6 jurisdictions simultaneously.

**Inputs per scenario:**
- Jurisdiction (state or county/city)
- Qualified Spend ($)
- Local Hire % (optional — triggers local hire warnings)
- Shooting Days (optional)
- Production Start date (optional — used for date-validity checks)

**Output:**
- Incentive stack breakdown (state layers + local layers)
- Total incentive value and effective rate
- Warnings (min spend not met, expired rules, local hire thresholds)
- Best jurisdiction highlighted with "Best Stack" badge

**How stacking works:**
- County/city jurisdictions inherit parent state rules via **additive** inheritance policy
- State `IncentiveRules` are stacked first, then `LocalRules`
- Min spend gates, date ranges, and max credit caps are all enforced

---

### Admin

Admin-only panel (visible to users with `role: admin`):
- User management
- System configuration
- Data seeding controls

---

### Notifications

Configure email alerts for jurisdiction rule changes. Set:
- Which jurisdictions to watch
- Email address for alerts
- Toggle notifications on/off

---

## API Reference

### Base URL
```
/api/0.1.0
```

---

### Authentication

#### POST /auth/login
Login and receive JWT token.

```json
Request:  { "email": "string", "password": "string" }
Response: { "access_token": "string", "token_type": "bearer" }
```

---

### Jurisdictions

| Method | Path | Description |
|--------|------|-------------|
| GET | `/jurisdictions/` | List all jurisdictions |
| GET | `/jurisdictions/{id}` | Get jurisdiction details + incentive rules |
| POST | `/jurisdictions/` | Create jurisdiction (admin) |
| PUT | `/jurisdictions/{id}` | Update jurisdiction (admin) |
| DELETE | `/jurisdictions/{id}` | Delete jurisdiction (admin) |

**Query params for GET /jurisdictions/:**
- `country` — filter by country code
- `type` — `state` | `province` | `country` | `county` | `city`
- `active` — `true` | `false`

---

### Incentive Rules

| Method | Path | Description |
|--------|------|-------------|
| GET | `/incentive-rules/` | List rules (filter by jurisdiction_id, type, active) |
| GET | `/incentive-rules/{id}` | Get rule details |
| POST | `/incentive-rules/` | Create rule (admin) |
| PUT | `/incentive-rules/{id}` | Update rule (admin) |
| DELETE | `/incentive-rules/{id}` | Delete rule (admin) |

---

### Productions

| Method | Path | Description |
|--------|------|-------------|
| GET | `/productions/` | List productions |
| GET | `/productions/{id}` | Get production details |
| POST | `/productions/` | Create production |
| PUT | `/productions/{id}` | Update production |
| DELETE | `/productions/{id}` | Delete production |

---

### Calculator

| Method | Path | Description |
|--------|------|-------------|
| POST | `/calculate/simple` | Simple incentive calculation |
| POST | `/calculate/compare` | Compare multiple jurisdictions |

---

### Stacking Engine

| Method | Path | Description |
|--------|------|-------------|
| POST | `/stacking-engine/calculate` | Full stack for a single scenario |
| POST | `/stacking-engine/compare` | Compare 2–6 scenarios side-by-side |
| GET | `/stacking-engine/jurisdictions-with-local-rules` | List jurisdictions with active local rules |

**POST /stacking-engine/compare — Request:**
```json
{
  "scenarios": [
    {
      "jurisdiction_code": "CA-LA",
      "qualified_spend": 5000000,
      "local_hire_percent": 80,
      "shooting_days": 45,
      "production_start": "2026-06-01"
    },
    {
      "jurisdiction_code": "IL-COOK",
      "qualified_spend": 5000000
    }
  ]
}
```

**Response:**
```json
{
  "scenarios": [
    {
      "jurisdiction_code": "CA-LA",
      "jurisdiction_name": "Los Angeles County",
      "qualified_spend": 5000000,
      "layers": [
        { "source": "state_incentive_rule", "name": "CA Film Credit", "incentive_value": 1500000, "rate": 30 },
        { "source": "local_rule", "name": "LA County Bonus", "incentive_value": 250000, "rate": 5 }
      ],
      "total_incentive": 1750000,
      "effective_rate": 0.35,
      "warnings": []
    }
  ],
  "best_jurisdiction": "CA-LA",
  "best_total_incentive": 1750000
}
```

---

### Local Rules

| Method | Path | Description |
|--------|------|-------------|
| GET | `/local-rules/` | List approved local rules |
| GET | `/local-rules/jurisdiction/{code}` | Rules for a specific jurisdiction |
| GET | `/local-rules/stats/summary` | Count by source and category |
| POST | `/local-rules/` | Create rule manually |
| PUT | `/local-rules/{id}` | Update rule |
| DELETE | `/local-rules/{id}` | Soft-delete (sets active=false) |

---

### Pending Rules

| Method | Path | Description |
|--------|------|-------------|
| GET | `/pending-rules/` | List pending rules (filter by status) |
| GET | `/pending-rules/{id}` | Get pending rule details |
| PATCH | `/pending-rules/{id}/approve` | Approve → promotes to local_rules |
| PATCH | `/pending-rules/{id}/reject` | Reject with notes |

---

### System

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check (unauthenticated) |
| GET | `/` | API root with endpoint listing |

---

## Deployment Guide

### Railway (Production)

#### Required Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (use `${{Postgres.DATABASE_URL}}` to auto-link) |
| `JWT_SECRET` | 256-bit hex secret for JWT signing |
| `SECRET_KEY` | 256-bit hex secret for session encryption |
| `APP_ENV` | Set to `production` |
| `ANTHROPIC_API_KEY` | Anthropic API key (required for AI Advisor) |

#### Build & Start (railway.toml)

```toml
[build]
builder = "NIXPACKS"
buildCommand = "pip install -r requirements.txt && python -m prisma generate"

[build.environment]
PYTHON_VERSION = "3.12"

[deploy]
startCommand = "prisma migrate deploy && uvicorn src.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
```

#### Post-Deploy: Seed Sub-Jurisdictions

After first successful deploy, run via Railway shell:
```bash
python scripts/seed_sub_jurisdictions.py
python scripts/seed_more_sub_jurisdictions.py
```

This seeds 11 county/city sub-jurisdictions with additive inheritance policies.

---

### Local Development (Docker)

#### Services

| Service | Container | Port |
|---------|-----------|------|
| FastAPI backend | `pilotforge-api` | 8001 |
| React frontend | `pilotforge-ui` | 3000 |
| nginx proxy | `pilotforge-nginx` | 80 |
| PostgreSQL | `tax-incentive-db` | 5432 |

#### Start
```bash
docker compose up -d
```

#### Access
- Frontend: http://localhost:3000
- API (direct): http://localhost:8001/api/0.1.0/
- API (nginx): http://localhost/api/0.1.0/

#### Deploy code changes (without rebuilding image)
```bash
# Backend
docker cp src/api/your_file.py pilotforge-api:/app/src/api/your_file.py
docker restart pilotforge-api

# Frontend
npm run build --prefix frontend
docker cp frontend/dist/. pilotforge-ui:/usr/share/nginx/html/
docker exec pilotforge-ui nginx -s reload
```

#### Rebuild image (after schema.prisma changes)
```bash
docker compose build backend
docker compose up -d backend
```

---

### Feed Monitor (Windows Task Scheduler)

`monitor.py` checks government pages for rule changes and queues Claude-extracted rules for review.

**Run manually:**
```bash
# Single jurisdiction
python monitor.py --code NY-ERIE --dry-run

# All jurisdictions
python monitor.py
```

**Schedule:** Daily at 6 AM via Windows Task Scheduler (`scripts/schedule_monitor.ps1`).

**Mock mode (no API billing):**
```
MOCK_CLAUDE=true
```
Set in `.env` to test the pipeline without Anthropic API calls.

---

## Data Reference

### State Jurisdictions (23)

**United States:** CA, GA, NY, LA, NM, IL, MI, NJ, VA, CO, HI, OR, MT, MS

**Canada:** BC, ON, QC

**International:** UK, AU, IE, FR, ES, NZ

### Sub-Jurisdictions (11)

| Code | Name | Parent |
|------|------|--------|
| CA-LA | Los Angeles County | CA |
| IL-COOK | Cook County (Chicago) | IL |
| NY-NYC | New York City | NY |
| NY-BROOKLYN | Brooklyn | NY |
| NY-QUEENS | Queens | NY |
| NY-MANHATTAN | Manhattan | NY |
| NY-BRONX | Bronx | NY |
| NY-STATEN-ISLAND | Staten Island | NY |
| NY-ERIE | Erie County | NY |
| NY-NASSAU | Nassau County | NY |
| NY-WESTCHESTER | Westchester County | NY |

### Incentive Types

| Type | Description |
|------|-------------|
| `tax_credit` | Credit against production company taxes |
| `rebate` | Cash rebate paid directly to production |
| `grant` | Government grant (no tax liability required) |
| `fee_waiver` | Permit or location fee waiver |
| `in_kind` | Non-cash support (crew, equipment, facilities) |

### Production Types

`feature` | `tv_series` | `tv_movie` | `commercial` | `documentary` | `web_series` | `pilot`

### Production Status

`planning` | `pre_production` | `production` | `post_production` | `completed`

---

## Troubleshooting

### "Failed to load resource: 404" on production (Railway)

**Cause:** Railway deployment hasn't completed yet, or migrations haven't run.

**Solutions:**
1. Check Railway dashboard → Deployments → wait for green status
2. Check deploy logs for prisma generate/migrate errors
3. Verify `DATABASE_URL` is linked to the Postgres service

---

### "Database connection failed" locally

```bash
docker ps                          # verify tax-incentive-db is running
docker compose up -d postgres      # restart postgres if needed
docker exec tax-incentive-db pg_isready -U postgres
```

---

### "401 Unauthorized" on API calls

Token has expired (8-hour TTL). Log out and log back in — the frontend handles this automatically via the 401 interceptor.

---

### Empty jurisdictions list after Railway deploy

Sub-jurisdictions aren't auto-seeded. Run:
```bash
python scripts/seed_sub_jurisdictions.py
python scripts/seed_more_sub_jurisdictions.py
```

---

### Chart "width(-1) height(-1)" console warning

Cosmetic Recharts initialization warning. Does not affect functionality. Fixed in v0.2.0.

---

### Prisma FieldNotFoundError after schema change

The container's Prisma client is stale.
```bash
docker exec pilotforge-api python -m prisma generate
docker restart pilotforge-api
```
If that fails (broken generated files), rebuild:
```bash
docker compose build backend && docker compose up -d backend
```

---

## Technical Specifications

### Technology Stack

**Frontend:**
- React 19 + TypeScript
- Vite 7
- Tailwind CSS v4
- Recharts (data visualization)
- Lucide React (icons)
- Zustand (auth state)
- Axios (API client)

**Backend:**
- FastAPI (Python 3.12)
- Prisma Client Python 0.15.0
- PostgreSQL 16
- Uvicorn (ASGI server)
- APScheduler (background jobs)
- JWT (python-jose + bcrypt)

**Infrastructure:**
- Docker + Docker Compose (local)
- Railway (production hosting)
- nginx (reverse proxy)
- GitHub (version control + CI/CD trigger)

**AI Integration:**
- Anthropic Claude (claude-sonnet-4-6) — AI Advisor + rule extraction

### Database Schema — Key Models

| Table | Purpose |
|-------|---------|
| `jurisdictions` | State, country, county, city jurisdictions |
| `incentive_rules` | State-level tax incentive programs |
| `local_rules` | Approved county/city rules |
| `pending_rules` | AI-extracted rules awaiting review |
| `inheritance_policies` | Parent→child stacking rules (additive/exclusive) |
| `productions` | Production records |
| `expenses` | Production expense line items |
| `users` | Platform users (JWT auth) |
| `sub_jurisdictions` | Phase 0: detailed county incentive records |
| `production_scenarios` | What-if scenario inputs |
| `scenario_optimization_results` | Cached stacking engine output |

### API Security

- JWT HS256 tokens, 8-hour TTL
- bcrypt password hashing
- 401 interceptor clears stale tokens
- CORS configured per environment

---

## Legal

### Disclaimer

This platform provides information about film tax incentive programs for planning purposes. While we strive for accuracy:

- **Not Legal Advice** — Consult with tax professionals and attorneys before making production location decisions
- **Not Financial Advice** — Verify all calculations with qualified accountants
- **Subject to Change** — Incentive programs change frequently; verify current program status with film commissions
- **No Guarantee** — We do not guarantee eligibility or approval for any incentive program

### Data Sources

Incentive rule data sourced from official film commission websites, government tax authority publications, and county/city government pages monitored by the automated feed system.

---

**End of User Manual**

Repository: https://github.com/hneal055/Tax_Incentive_Compliance_Platform
