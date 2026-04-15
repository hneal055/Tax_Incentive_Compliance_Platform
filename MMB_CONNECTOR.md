# SceneIQ MMB Connector

Integration guide for connecting Movie Magic Budgeting (MMB) to the SceneIQ Tax Incentive Intelligence platform.

GitHub repo: [hneal055/SceneIQ-MMB-Connector](https://github.com/hneal055/SceneIQ-MMB-Connector)

---

## What It Does

The MMB Connector is a standalone Python library that:

1. **Parses** `.mmbx`, `.mdb`, CSV, and Excel exports from Movie Magic Budgeting
2. **Transforms** the budget data into SceneIQ's standardized schema
3. **Evaluates** the budget against active incentive programs via the SceneIQ API
4. **Returns** ranked incentive recommendations with estimated credits, bonuses, and audit checklists

---

## Architecture

```
Movie Magic Budgeting (.mmbx / .mdb / CSV)
        │
        ▼
MMBParser  (src/parsers/mmb_parser.py)
  - MMBX: unzips archive, parses project.xml + workbook.xml
  - MDB:  pyodbc (Windows) or mdbtools (Linux/macOS)
  - CSV/Excel: pandas with flexible column detection
        │
        ▼
BudgetTransformer  (src/transformers/budget_transformer.py)
  - Maps account numbers to incentive categories (ATL / BTL / post / equipment)
  - Normalises field names, currency, and dates
  - Computes incentive-eligible subtotals
        │
        ▼
SceneIQClient  (src/connectors/pilotforge_api.py)
  - evaluate_budget()  →  POST /api/v1/integrations/largo/project
  - get_incentive_programs()  →  GET /api/v1/programs/
  - list_productions()  →  GET /api/0.1.0/productions/  (main app)
  - calculate_incentive()  →  POST /api/0.1.0/calculate  (main app)
        │
        ▼
SceneIQ Backend (this repo)
  backend/  — FastAPI + SQLite  (Largo integration, incentive programs)
  src/      — FastAPI + Prisma/PostgreSQL  (productions, calculator, jurisdictions)
```

---

## Quick Start

### 1. Clone and install the connector

```bash
git clone https://github.com/hneal055/SceneIQ-MMB-Connector.git
cd SceneIQ-MMB-Connector
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the SceneIQ backend

```bash
# From Tax_Incentive_Compliance_Platform/backend/
uvicorn app.main:app --reload --port 8002
```

### 3. Parse and evaluate an MMB budget

```python
from src.parsers.mmb_parser import MMBParser
from src.transformers.budget_transformer import BudgetTransformer
from src.connectors.pilotforge_api import SceneIQClient

# Parse
parser = MMBParser()
raw = parser.parse_file("path/to/budget.mmbx")

# Transform
transformer = BudgetTransformer()
pf_data = transformer.transform_to_pilotforge(raw)

# Evaluate
client = SceneIQClient(environment="local_backend")
result = client.evaluate_budget(
    pf_data,
    include_logo=True,
    local_hire_pct=0.20,
    diversity_score=0.25,
    audience_score=78.5,
)

print(f"Total estimated credits: ${result['total_estimated_credits']:,.0f}")
for rec in result["recommendations"]:
    if rec["eligible"]:
        print(f"  {rec['jurisdiction']}: ${rec['estimated_credit']:,.0f} ({rec['credit_rate']*100:.0f}% rate)")
```

---

## Environments

The connector supports four target environments configured via the `environment` parameter:

| Environment | URL | Used for |
|---|---|---|
| `local_backend` | `http://localhost:8002/api/v1` | `backend/` SQLite app — Largo integration |
| `local_main` | `http://localhost:8001/api/0.1.0` | `src/` Prisma app — productions, calculator |
| `production` | `https://taxincentivecomplianceplatform-production.up.railway.app/api/0.1.0` | Railway deployment |
| `staging` | Override via `PILOTFORGE_STAGING_URL` env var | Pre-prod testing |

Override credentials with environment variables:

```bash
export PILOTFORGE_EMAIL=admin@pilotforge.com
export PILOTFORGE_PASSWORD=pilotforge2024
```

---

## API Endpoints Used

### `backend/` app (local port 8002)

| Method | Endpoint | Connector method |
|---|---|---|
| `POST` | `/api/v1/integrations/largo/project` | `client.evaluate_budget()` |
| `GET` | `/api/v1/integrations/largo/demo-payload` | `client.get_demo_payload()` |
| `GET` | `/api/v1/programs/` | `client.get_incentive_programs()` |

### `src/` app (local port 8001 / Railway)

| Method | Endpoint | Connector method |
|---|---|---|
| `POST` | `/api/0.1.0/auth/login` | `client.authenticate()` |
| `GET` | `/api/0.1.0/productions/` | `client.list_productions()` |
| `POST` | `/api/0.1.0/productions/` | `client.create_production()` |
| `GET` | `/api/0.1.0/jurisdictions/` | `client.get_jurisdictions()` |
| `POST` | `/api/0.1.0/calculate` | `client.calculate_incentive()` |

---

## Incentive Evaluation Logic

The `evaluate_budget()` method sends the transformed budget to `POST /api/v1/integrations/largo/project`. The backend:

1. Computes **qualified spend** = 80% of total budget
2. Checks **minimum spend** ≥ $500,000
3. Matches **filming locations** against active program jurisdictions
4. Calculates **base credit** = qualified spend × base rate
5. Applies **bonus rates** (stacked):
   - Promotional Logo: +10% if `include_logo=True`
   - Local Hire: +5% if `local_hire_pct ≥ 15%`
   - Diversity: +2% if `diversity_score ≥ 20%`
6. Returns sorted recommendations (eligible first, by estimated credit descending)

---

## Supported MMB File Formats

| Format | Extension | MMB Version | Notes |
|---|---|---|---|
| MMBX | `.mmbx` | 7.0 – 10.0+ | ZIP archive with XML files |
| Access DB | `.mdb` | 6.x and earlier | Requires pyodbc or mdbtools |
| CSV Export | `.csv` | All | Any MMB version via File > Export |
| Excel Export | `.xlsx` / `.xls` | All | Requires `pip install openpyxl` |

### Installing MDB support

**Windows:**
```bash
pip install pyodbc
# Also requires Microsoft Access Database Engine:
# https://www.microsoft.com/en-us/download/details.aspx?id=54920
```

**macOS:**
```bash
brew install mdbtools
```

**Linux:**
```bash
sudo apt install mdbtools
```

---

## SceneIQ Budget Schema

The transformer outputs this standardized schema before sending to SceneIQ:

```python
{
    "project": {
        "name": str,               # Production title
        "production_company": str,
        "genre": str,              # Drama, Comedy, etc.
        "total_budget": float,     # USD
        "filming_locations": list, # ["Georgia", "Atlanta"]
        "start_date": str | None,
        "end_date": str | None,
        "source": "mmb",
    },
    "accounts": [
        {
            "code": str,                  # e.g. "2100"
            "description": str,
            "budgeted_amount": Decimal,
            "account_type": "group" | "detail",
            "incentive_category": str,    # above_the_line | below_the_line_labor | equipment | post_production
            "incentive_eligible": bool,
        }
    ],
    "metadata": {
        "transformer_version": str,
        "source_format": str,   # mmbx | mdb | csv | excel
        "mmb_version": str,
    }
}
```

### Account category → incentive eligibility

| Account range | Category | Eligible |
|---|---|---|
| 1000–1999 | Above-the-line | No (typically excluded from labor incentives) |
| 2000–3999 | Below-the-line labor | Yes (`qualified_wages`, `labor_credit`) |
| 4000–4999 | Equipment & materials | Yes (`qualified_spend`) |
| 6000–6999 | Post-production | Yes (`qualified_spend`, `post_credit`) |

---

## Running the Demo

```bash
# Start SceneIQ backend
cd Tax_Incentive_Compliance_Platform/backend
uvicorn app.main:app --reload --port 8002

# In a second terminal — run the connector example
cd SceneIQ-MMB-Connector
python examples/test_integration_example.py

# Or view the interactive demo UI
open http://localhost:8002/static/integration_demo.html
```

---

## Connector File Map

```
SceneIQ-MMB-Connector/
├── src/
│   ├── parsers/
│   │   └── mmb_parser.py          # MMBX, MDB, CSV/Excel parsing
│   ├── transformers/
│   │   └── budget_transformer.py  # MMB → SceneIQ schema mapping
│   ├── connectors/
│   │   ├── pilotforge_api.py      # SceneIQ REST client (wired to this repo)
│   │   └── mmb_api.py             # MMB API stub (future)
│   └── intelligence/
│       └── tax_optimizer.py       # TaxOptimizer, IncentiveProgram dataclasses
├── tests/
│   ├── test_parsers.py
│   ├── test_transformers.py
│   ├── test_api_client.py
│   └── test_integration_tax_platform.py
├── examples/
│   └── test_integration_example.py
└── docs/
    ├── ARCHITECTURE.md
    ├── MMB_FILE_FORMATS.md
    ├── INTEGRATION_POINTS.md
    └── ROADMAP.md
```

---

## Related Docs in This Repo

- [LARGO_INTEGRATION.md](LARGO_INTEGRATION.md) — Largo.ai integration (the API the connector calls)
- `backend/app/api/v1/endpoints/integrations.py` — The live incentive evaluation endpoint
- `backend/static/integration_demo.html` — Interactive demo UI
