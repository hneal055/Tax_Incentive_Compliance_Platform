# Largo + PilotForge Integration

This document covers setup, usage, and API reference for the Largo.ai ↔ PilotForge tax incentive integration.

---

## Overview

PilotForge exposes a REST API that Largo.ai (or any production platform) can call to receive real-time tax incentive recommendations. Given a project's budget, filming locations, and optional bonus parameters, the API evaluates every active incentive program and returns estimated credits, eligibility status, bonus breakdowns, and pre-application checklists.

---

## Architecture

```
Largo.ai  ──POST──▶  /api/v1/integrations/largo/project  ──▶  SQLite DB (active programs)
                              │
                              ▼
                    IncentiveRecommendation[]
                    (sorted by estimated credit, eligible first)
```

The integration lives in the **`backend/`** app — a standalone FastAPI + SQLAlchemy + SQLite service, separate from the main PilotForge Prisma/PostgreSQL app in `src/`.

---

## Local Setup

### Prerequisites

- Python 3.11+
- Dependencies installed (`fastapi`, `uvicorn`, `sqlalchemy`)

```bash
# From the project root
pip install fastapi uvicorn sqlalchemy aiosqlite
```

### Start the backend server

```bash
cd backend
uvicorn app.main:app --reload --port 8002
```

Server starts at `http://127.0.0.1:8002`.

### Initialize the database (first run only)

```bash
cd backend
python init_db.py
```

This creates `tax_incentive.db` and seeds jurisdictions + active incentive programs.

---

## URLs

| Resource | URL |
|---|---|
| Interactive demo | `http://localhost:8002/static/integration_demo.html` |
| Swagger UI | `http://localhost:8002/docs` |
| ReDoc | `http://localhost:8002/redoc` |
| Rules viewer | `http://localhost:8002/static/rules_viewer.html` |
| Health check | `http://localhost:8002/health` |

---

## API Reference

### POST `/api/v1/integrations/largo/project`

Evaluate incentive programs for a Largo project submission.

**Request body**

```json
{
  "project_name": "The Last Frontier",
  "genre": "Drama",
  "budget": 2500000,
  "locations": ["Georgia", "Atlanta"],
  "audience_score": 78.5,
  "include_logo": true,
  "local_hire_pct": 0.20,
  "diversity_score": 0.25
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `project_name` | string | Yes | Project title |
| `genre` | string | Yes | e.g. Drama, Comedy, Documentary |
| `budget` | float | Yes | Total production budget in USD |
| `locations` | string[] | Yes | Filming locations (state or country names) |
| `audience_score` | float | No | Largo audience score 0–100 |
| `include_logo` | bool | No | Include promotional logo for bonus eligibility |
| `local_hire_pct` | float | No | Fraction of crew that are local residents (0.0–1.0) |
| `diversity_score` | float | No | Diversity score for key creative roles (0.0–1.0) |

**Response**

```json
{
  "project_name": "The Last Frontier",
  "genre": "Drama",
  "budget": 2500000,
  "locations": ["Georgia", "Atlanta"],
  "audience_score": 78.5,
  "recommendations": [
    {
      "jurisdiction": "Georgia",
      "program_name": "Georgia Entertainment Industry Investment Act",
      "program_id": "1",
      "estimated_credit": 520000,
      "credit_rate": 0.26,
      "qualified_spend": 2000000,
      "qualified_categories": ["production", "post-production", "crew"],
      "bonuses_applied": [
        { "name": "Promotional Logo", "rate": 0.10, "amount": 200000 }
      ],
      "pre_application_checklist": [...],
      "audit_readiness_score": 85,
      "eligible": true,
      "ineligibility_reason": null,
      "transferable": true,
      "sunset_date": null
    }
  ],
  "total_estimated_credits": 520000,
  "generated_at": "2026-03-31T15:00:00Z"
}
```

---

### GET `/api/v1/integrations/largo/demo-payload`

Returns a ready-to-use sample request payload for testing.

```bash
curl http://localhost:8002/api/v1/integrations/largo/demo-payload
```

---

## Incentive Calculation Logic

| Step | Rule |
|---|---|
| Qualified spend | 80% of total budget |
| Minimum spend check | Must be ≥ $500,000 qualified spend |
| Location check | Project must list the jurisdiction's state/country |
| Base credit | `qualified_spend × base_credit_rate` |
| Promotional logo bonus | +10% rate if `include_logo = true` |
| Local hire bonus | +5% rate if `local_hire_pct ≥ 15%` |
| Diversity bonus | +2% rate if `diversity_score ≥ 20%` |
| Ineligible projects | `estimated_credit = 0`, reason returned in response |

Bonus rates and thresholds are stored per-program in the `rules` JSON column and can be updated without code changes.

---

## Interactive Demo

Open `http://localhost:8002/static/integration_demo.html` for a full UI demo:

- **Left panel** — Largo project form (budget, locations, genre, bonus toggles)
- **Right panel** — PilotForge results (estimated credits, audit readiness score, expandable checklists)
- Loads the demo payload automatically via **Load Demo** button
- Displays a total credit bar across all eligible jurisdictions

---

## File Structure

```
backend/
├── app/
│   ├── main.py                          # FastAPI app + static file mount
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py              # Router registration
│   │       └── endpoints/
│   │           └── integrations.py      # Largo endpoints + evaluation logic
│   ├── models/
│   │   ├── jurisdiction.py
│   │   ├── program.py
│   │   └── largo_project.py             # Submission storage model
│   └── db/
│       └── session.py                   # SQLAlchemy session + Base
├── static/
│   ├── integration_demo.html            # Interactive demo UI
│   └── rules_viewer.html                # Program rules viewer
├── init_db.py                           # DB init + seed script
└── tax_incentive.db                     # SQLite database
```

---

## Example cURL

```bash
curl -X POST http://localhost:8002/api/v1/integrations/largo/project \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Peach State Chronicles",
    "genre": "Drama",
    "budget": 2500000,
    "locations": ["Georgia", "Atlanta", "Savannah"],
    "audience_score": 78.5,
    "include_logo": true,
    "local_hire_pct": 0.20,
    "diversity_score": 0.25
  }'
```

---

## Extending the Integration

**Add a new jurisdiction/program** — seed a new row into the `programs` table with a `rules` JSON blob following the schema used by existing programs. No code changes required.

**Save submissions to the database** — `LargoProject` model (`backend/app/models/largo_project.py`) is ready. Add a `db.add(LargoProject(...))` call in the `evaluate_largo_project` endpoint to persist every inbound request.

**Authentication** — the integration endpoints are currently open. Add an `api_key` header check or OAuth dependency in `integrations.py` before exposing to production.
