# PilotForge — Tax Incentive Compliance Platform
## User Manual v2.1

---

## Table of Contents

1. [Platform Overview](#1-platform-overview)
2. [Getting Started](#2-getting-started)
3. [Dashboard](#3-dashboard)
4. [Productions](#4-productions)
5. [Calculator & Scenario Tools](#5-calculator--scenario-tools)
6. [Jurisdictions](#6-jurisdictions)
7. [Local Rules & Rule Review](#7-local-rules--rule-review)
8. [AI Advisor](#8-ai-advisor)
9. [Reports & Exports](#9-reports--exports)
10. [Monitoring System](#10-monitoring-system)
11. [Incentive Maximizer](#11-incentive-maximizer)
12. [Admin & User Management](#12-admin--user-management)
13. [Notifications & Preferences](#13-notifications--preferences)
14. [Command-Line Tools](#14-command-line-tools)
15. [API Reference](#15-api-reference)
16. [Database Models](#16-database-models)
17. [Deployment & Operations](#17-deployment--operations)
18. [Environment Variables](#18-environment-variables)
19. [Troubleshooting](#19-troubleshooting)

---

## 1. Platform Overview

PilotForge is a tax incentive compliance platform built for film and TV production professionals. It centralizes jurisdiction research, incentive calculation, compliance tracking, rule monitoring, and AI-powered advisory in one system.

### Core Capabilities

| Capability | Description |
|---|---|
| **Productions** | Track all productions with budget, expenses, status, and jurisdiction |
| **Calculator** | Estimate and compare tax credits across jurisdictions |
| **Scenario Analysis** | Model what-if spending scenarios per production |
| **Compliance Tracking** | Manage checklist items with due dates and status |
| **Jurisdiction Database** | 50+ jurisdictions with incentive rules and live feed monitoring |
| **Compliance Checklist** | Per-jurisdiction permit, insurance, and registration requirements |
| **Local Rules** | Sub-jurisdiction and county/city rules extracted from government feeds |
| **Rule Review** | Human-in-the-loop approval of AI-extracted rules |
| **AI Advisor** | Claude-powered chat for incentive questions |
| **Maximizer** | Stack-optimize incentives across jurisdiction layers by location |
| **Monitoring** | Automated change detection on government feeds |
| **Exports** | PDF and Excel reports for all major views |

### Tech Stack

- **Frontend:** React 19 + TypeScript + Vite + Tailwind CSS v4
- **Backend:** FastAPI + Python 3.12 + Prisma ORM
- **Database:** PostgreSQL
- **AI:** Anthropic Claude (Sonnet 4.6) for rule extraction and advisory
- **Background Jobs:** APScheduler (feed ingestion every 4 hours)

---

## 2. Getting Started

### Default Credentials

| Field | Value |
|---|---|
| Email | `admin@pilotforge.com` |
| Password | `pilotforge2024` |

> Change these immediately after first login via Settings → Account.

### Local URLs

| Service | URL | Notes |
|---|---|---|
| Platform UI | `http://localhost` | Use this — nginx reverse proxy on port 80 |
| API (via proxy) | `http://localhost/api/0.1.0/` | All frontend API calls route here |
| API (direct) | `http://localhost:8001/api/0.1.0/` | Direct to backend, bypasses proxy |
| API Docs | `http://localhost/docs` | Swagger UI — requires JWT to test protected routes |
| API Redoc | `http://localhost/redoc` | Alternative docs UI |

> **Do not use port 3000** for API calls. The frontend container's nginx on port 3000 does not proxy `/api/` — all API calls will return 405. Always use `http://localhost` (port 80).

### Docker Services

| Service Name | Container | Role |
|---|---|---|
| `backend` | `pilotforge-api` | FastAPI + Prisma backend |
| `frontend` | `pilotforge-ui` | React frontend (built static files) |
| `nginx` | `pilotforge-nginx` | Reverse proxy (port 80) |
| `postgres` | `tax-incentive-db` | PostgreSQL database |

### Starting the Platform

```bash
docker compose up -d
```

### Stopping

```bash
docker compose down
```

### Fresh Database Recovery Order

If the database is empty or reset:

```bash
# 1. Run migrations
docker exec pilotforge-api python -m prisma migrate deploy

# 2. Seed jurisdictions
docker cp scripts/seed_jurisdictions.py pilotforge-api:/app/scripts/seed_jurisdictions.py
docker exec pilotforge-api python scripts/seed_jurisdictions.py

# 3. Seed incentive rules
docker cp scripts/seed_incentive_rules.py pilotforge-api:/app/scripts/seed_incentive_rules.py
docker exec pilotforge-api python scripts/seed_incentive_rules.py

# 4. Seed sub-jurisdictions and more rules
docker exec pilotforge-api python scripts/seed_more_jurisdictions.py
docker exec pilotforge-api python scripts/seed_more_rules.py

# 5. Seed maximizer test data (optional)
python scripts/seed_maximizer_test.py
```

---

## 3. Dashboard

**Navigation:** Click the PilotForge logo or "Dashboard" in the sidebar.

The dashboard provides an executive overview of all productions and incentive performance.

### Metric Cards

| Card | What It Shows |
|---|---|
| **Total Budget Volume** | Sum of all production budgets across the portfolio |
| **Estimated Tax Credits** | Projected incentive value across all productions |
| **Active Projects** | Productions in planning, pre-production, or production status |
| **Alerts** | Compliance items overdue or jurisdictions with feed changes |

### Top Productions Chart

A horizontal bar chart showing the top 5 productions by budget, comparing **budgeted** vs. **actual** qualified spend. Use this to spot productions that are under- or over-spending their qualifying budget.

### Reading the Dashboard

- **Green values** — on track or ahead of targets
- **Amber values** — attention needed (compliance approaching due date, minor budget variance)
- **Red values** — action required (overdue compliance, significant budget shortfall)

---

## 4. Productions

**Navigation:** Sidebar → Productions

### Production List

The list shows all productions with:
- Title and production company
- Status badge (planning / pre-production / production / post-production / completed)
- Production type (feature, TV series, commercial, documentary)
- Home jurisdiction
- Total budget and qualifying spend

### Filtering & Search

| Filter | How |
|---|---|
| Search | Type in the search bar — matches title or production company |
| Status | Click a status badge in the filter bar |
| Production type | Dropdown in the filter bar |

### Creating a Production

1. Click **+ New Production**
2. Fill in the required fields:

| Field | Description |
|---|---|
| **Title** | Production working title |
| **Production Type** | Feature / TV Series / Commercial / Documentary |
| **Production Company** | Legal entity name |
| **Jurisdiction** | Primary filming jurisdiction (state/country) |
| **Total Budget** | Full production budget in USD |
| **Qualifying Budget** | Portion eligible for incentives |
| **Start Date** | Principal photography start |
| **End Date** | Wrap date (optional) |
| **Status** | Current phase |
| **Contact** | Production contact name/email |

3. Click **Create Production**

### Production Detail

Click any production to open the detail view with these tabs:

#### Overview Tab
Full metadata for the production. Click any field to edit inline.

#### Expenses Tab
Track individual expense line items.

**Adding an expense:**
1. Click **+ Add Expense**
2. Fill in category, description, amount, date, vendor
3. Toggle **Is Qualifying** to mark whether the expense counts toward incentives
4. Click **Save**

**Expense categories:** Labor, Equipment, Location, Post-Production, Travel, Legal, Marketing, Other

**Auto-generate sample expenses:** Click **Generate Sample Expenses** to populate test data for a new production.

#### Compliance Tab
Checklist of compliance requirements for this production's jurisdiction.

**Status values:**

| Status | Meaning |
|---|---|
| `pending` | Not yet done |
| `complete` | Verified and done |
| `waived` | Exempted from this requirement |
| `na` | Not applicable to this production |

**Auto-generate checklist:** Click **Generate Checklist** — creates standard compliance items for the selected jurisdiction.

#### Scenarios Tab
See [Section 5](#5-calculator--scenario-tools) for full scenario documentation.

### Editing a Production

All fields in the Overview tab are inline-editable. Click the field, make the change, and click **Save** or press Enter.

### Deleting a Production

Click the **trash icon** on the production list row or the **Delete** button in the production detail. A confirmation dialog will appear — this action is permanent.

---

## 5. Calculator & Scenario Tools

**Navigation:** Sidebar → Calculator

The Calculator has six calculation modes accessible via tabs.

---

### Mode 1: Quick Calculate

**Use for:** Fast estimate of the incentive for a production in a specific jurisdiction.

**Inputs:**
- Select production
- Select jurisdiction

**Output:**
- Estimated credit amount
- Effective rate
- Rule that was applied
- Minimum spend requirement check

---

### Mode 2: Simple Calculate

**Use for:** Apply a single known incentive rule to a qualified spend amount.

**Inputs:**
- Production
- Jurisdiction
- Qualified spend amount

**Output:**
- Credit amount (percentage × spend)
- Credit type (refundable / transferable / non-refundable)
- Eligibility requirements

---

### Mode 3: Compare

**Use for:** Side-by-side comparison of the same production across multiple jurisdictions.

**Inputs:**
- Production
- Select 2–6 jurisdictions to compare

**Output:**
- Table showing incentive value, effective rate, and credit type for each jurisdiction
- Ranked from highest to lowest incentive value
- Download as PDF or Excel

---

### Mode 4: Compliance Check

**Use for:** Verify whether a production's expense breakdown meets a jurisdiction's eligibility rules.

**Inputs:**
- Production
- Jurisdiction
- Expense breakdown by category

**Output:**
- Per-category eligibility (qualified / excluded / partially qualified)
- Total qualified spend
- Estimated credit based on qualified amounts
- Warning flags for categories at or near caps

---

### Mode 5: Scenario Analysis

**Use for:** Model multiple budget scenarios for a single production.

**Inputs:**
- Production
- 1–6 spending scenarios (vary total budget, qualifying %, category breakdowns)

**Output:**
- Incentive value for each scenario
- Chart showing scenario comparison
- Best-case and worst-case projections

---

### Mode 6: Date-Based Rules

**Use for:** Check which incentive rules apply on a specific date (useful for productions that span rule change dates).

**Inputs:**
- Jurisdiction
- Date

**Output:**
- All active rules on that date
- Rules that expired before or became effective after that date
- Credit rates and eligibility as of that date

---

### Scenario Calculator (Stacking Engine)

**Navigation:** Sidebar → Scenario Calculator

A dedicated multi-jurisdiction scenario tool powered by the stacking engine.

**How to use:**
1. Click **+ Add Scenario** — up to 6 scenarios
2. For each scenario, select:
   - Jurisdiction
   - Qualified Spend
   - Local Hire % (optional — unlocks local hire bonuses)
   - Shooting Days (optional — some jurisdictions have per-day thresholds)
   - Production Start Date (optional — for date-sensitive rule matching)
3. Click **Compare Stacks**

**Results show:**
- **Best Stack** badge on the highest-value jurisdiction
- Layer breakdown (state incentive + local incentive + any bonuses)
- Effective rate and total incentive per jurisdiction
- Warnings (e.g., annual cap exhaustion, minimum spend not met)
- Stacking conflicts (where rules cannot stack)

---

## 6. Jurisdictions

**Navigation:** Sidebar → Jurisdictions

Browse and manage the full jurisdiction database.

### Jurisdiction List

| Column | Description |
|---|---|
| Name | Full jurisdiction name |
| Code | Short identifier (e.g., `NY`, `CA`, `NY-ERIE`) |
| Type | state / county / city / country / province |
| Country | ISO country code |
| Rules | Count of active incentive rules |
| Feed Status | Last checked timestamp + change indicator |

### Filtering

- **Search:** Name or code
- **Type filter:** state, county, city, country, province
- **Active only:** Toggle to hide inactive jurisdictions

### Jurisdiction Detail

Click any row to open the detail modal:

| Tab | Content |
|---|---|
| **Overview** | Description, website, currency, treaty partners |
| **Incentive Rules** | All active rules with rates, caps, and eligibility |
| **Sub-Jurisdictions** | Counties and cities under this jurisdiction |
| **Monitoring** | Feed URL, last checked, last hash, manual refresh |

### Monitoring Feed Controls

In the **Monitoring** tab of a jurisdiction detail:
- **Feed URL** — the government page being watched
- **Last Checked** — timestamp of most recent fetch
- **Refresh Now** — trigger an immediate feed fetch (runs Claude extraction if content changed)

> Changes detected by the monitor create **Pending Rules** — see [Section 7](#7-local-rules--rule-review).

---

## 7. Local Rules & Rule Review

### Local Rules

**Navigation:** Sidebar → Local Rules

Local rules are jurisdiction-specific rules stored at the county, city, or sub-jurisdiction level. They supplement the main state-level IncentiveRules.

#### Local Rules List

Each row shows:
- Rule name and code
- Jurisdiction
- Category (film_incentive, local_incentive, permit_fee, etc.)
- Rule type (tax_credit, rebate, fee, restriction)
- Amount (USD) or Percentage
- Effective and expiration dates
- Status (active / inactive)

#### Stats Bar

At the top of the page:
- **Total Rules** — All local rules in the system
- **Active** — Currently in effect
- **Credits** — Rules that provide incentive value
- **Fees** — Rules that add cost (permit fees, etc.)

#### Filtering

| Filter | Options |
|---|---|
| Search | Rule name or code |
| Jurisdiction | Dropdown of all jurisdictions |
| Rule Type | credit / rebate / fee / restriction / all |
| Status | Active only / All |

#### Creating a Local Rule Manually

1. Click **+ Add Rule**
2. Fill in:

| Field | Description |
|---|---|
| **Jurisdiction** | Select from dropdown |
| **Name** | Display name for the rule |
| **Code** | Unique identifier (e.g., `NY-ERIE-FILM-FEE`) |
| **Category** | film_incentive / local_incentive / permit_fee / other |
| **Rule Type** | tax_credit / rebate / fee / restriction / exemption |
| **Amount** | Fixed USD value (use for flat fees) |
| **Percentage** | Rate (use for percentage-based credits) |
| **Description** | Full description |
| **Requirements** | Eligibility conditions |
| **Effective Date** | When rule becomes active |
| **Expiration Date** | When rule expires (leave blank for indefinite) |
| **Source URL** | Link to government source |

3. Click **Save Rule**

> Either Amount or Percentage should be filled — not both.

#### Editing and Deactivating

Click a rule row to open the edit form. Toggle the **Active** switch to deactivate without deleting.

---

### Rule Review (Pending Rules)

**Navigation:** Sidebar → Rule Review

When the monitor detects a feed change and Claude extracts rules from the government page, those rules land here as **Pending Rules** for human review before being promoted to Local Rules.

#### Pending Rules List

Each row shows:
- Jurisdiction the rule was extracted from
- Source URL fetched
- Extraction confidence score (0.0 – 1.0)
- Number of rules extracted
- Status: `pending` / `approved` / `rejected`
- Date created

#### Reviewing a Pending Rule

1. Click a pending rule row to open the review modal
2. Review tabs:

| Tab | Content |
|---|---|
| **Extracted Rules** | JSON array of rules Claude found (name, category, type, amount, percentage, description) |
| **Raw Content** | First 5,000 chars of the government page content fetched |
| **Metadata** | Source URL, confidence score, extraction timestamp |

3. Take action:

| Button | Effect |
|---|---|
| **Approve** | Promotes quantified rules (credits, rebates, fees with dollar/percent values) to the `incentive_rules` table; promotes non-quantified process rules (permits, insurance mandates, portal links) to `jurisdiction_requirements` |
| **Reject** | Marks as rejected — no rule is created |
| **Add Notes** | Save review notes before approving or rejecting |

#### Confidence Scores

| Score | Meaning |
|---|---|
| 0.8 – 1.0 | High confidence — rule found in clear, structured government text |
| 0.5 – 0.8 | Medium confidence — rule inferred from context, verify before approving |
| 0.0 – 0.5 | Low confidence — likely no relevant rules or ambiguous content |

> Always verify rules with the source URL before approving, especially for fee amounts and eligibility dates.

---

## 8. AI Advisor

**Navigation:** Sidebar → AI Advisor

The AI Advisor is a Claude-powered chat interface for tax incentive questions.

### Using the Advisor

1. **Optional:** Select a production from the sidebar dropdown — gives Claude context about your specific budget, jurisdiction, and dates
2. Type your question in the input field
3. Press Enter or click **Send**
4. Responses stream in real time with markdown formatting

### Suggested Prompts

Click any suggested prompt to pre-fill the input:

- "What expenses qualify for the New York film tax credit?"
- "Compare Georgia vs. New Mexico incentives for a $5M feature"
- "What are the local hire requirements in Illinois?"
- "Explain the stacking rules for California productions"
- "What documentation is required for a refundable credit?"

### Production Context

When a production is selected in the sidebar:
- Claude knows the jurisdiction, budget, and dates
- Questions like "What credits apply to my project?" will use your production's data
- Responses include jurisdiction-specific details

### Limitations

- The Advisor answers based on its training data and the rules in your database — always verify against official government sources before filing
- If `ANTHROPIC_API_KEY` is not configured, the Advisor returns scripted fallback responses for common questions
- Chat history is session-only — it is not saved between page reloads

---

## 9. Reports & Exports

Reports can be generated from the Calculator page or the API directly.

### PDF Reports

| Report Type | What It Contains | Endpoint |
|---|---|---|
| **Comparison Report** | Multi-jurisdiction comparison table, rates, caps, eligibility | `POST /reports/comparison/` |
| **Compliance Report** | Checklist status, completion rate, outstanding items | `POST /reports/compliance/` |
| **Scenario Report** | Scenario inputs, projected credits, chart | `POST /reports/scenario/` |

### Excel Reports

| Report Type | Worksheets | Endpoint |
|---|---|---|
| **Comparison Workbook** | Summary, per-jurisdiction details, rule breakdown | `POST /excel/comparison/` |
| **Compliance Workbook** | Checklist, categories, due dates | `POST /excel/compliance/` |
| **Scenario Workbook** | Scenarios, projections, sensitivity table | `POST /excel/scenario/` |

### Generating a Report from the UI

1. Navigate to **Calculator** → run any calculation
2. Click **Download PDF** or **Download Excel** on the result card
3. The file downloads immediately

### Generating via API

```bash
# PDF comparison report
curl -X POST http://localhost/api/0.1.0/reports/comparison/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"production_id": "uuid", "jurisdiction_ids": ["uuid1", "uuid2"]}' \
  --output report.pdf

# Excel compliance workbook
curl -X POST http://localhost/api/0.1.0/excel/compliance/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"production_id": "uuid"}' \
  --output compliance.xlsx
```

---

## 10. Monitoring System

The monitoring system automatically tracks government web pages for rule changes and uses Claude to extract new rules.

### How It Works

```
Government Website  →  fetch_url()  →  SHA-256 hash comparison
                                              ↓ (changed)
                                       Claude extraction
                                              ↓
                                       PendingRule created
                                              ↓
                                       Human review → approve → LocalRule
```

### Feed Sources

Each jurisdiction can have a `feedUrl` pointing to a government web page, RSS feed, or PDF URL. The monitor fetches these and detects changes by comparing SHA-256 hashes.

**Currently monitored jurisdictions:**

| Code | Jurisdiction | Feed URL |
| ---- | ------------ | -------- |
| NY-ERIE | Erie County, NY | `filmbuffaloniagara.com/permits-guidelines/` |
| NY-NASSAU | Nassau County, NY | `nassaucountyny.gov/film` |
| NY-WESTCHESTER | Westchester County, NY | `visitwestchesterny.com/film/permits/` |
| NY-NYC | New York City | `nyc.gov/site/mome/industries/tv-film.page` |
| CA-LA | Los Angeles County | `filmla.com/permits/` |
| IL-COOK | Cook County / Chicago | `chicago.gov/…/chicago_film_office_tax.html` |
| GA-SAVANNAH | Savannah, GA | `filmsavannah.org/permits/` |
| GA-FULTON | Fulton County, GA | `fultoncountyga.gov/fultonfilms` |
| GA-DEKALB | DeKalb County, GA | `dekalbcountyga.gov/planning-and-sustainability/other-permitting-services-1` |
| GA-ATLANTA | Atlanta, GA | *(WAF-protected — manual monitoring; URL: `atlantaga.gov/…/office-of-film-entertainment-nightlife`)* |

### Automated Schedule

The scheduler runs feed ingestion **every 4 hours** automatically when the backend is running. No manual action is required.

### Monitoring Events

The monitoring events feed is accessible via:
- `GET /api/0.1.0/monitoring/events/` — all events
- `GET /api/0.1.0/monitoring/events/unread-count/` — badge count
- `PATCH /api/0.1.0/monitoring/events/{id}/read/` — mark read

Events include: title, summary, severity (info/warning/alert), and publish date.

### Adding a New Monitoring Source

```bash
curl -X POST http://localhost/api/0.1.0/monitoring/sources/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Mexico Film Office",
    "url": "https://nmfilm.com/incentives/",
    "sourceType": "rss",
    "jurisdiction": "NM"
  }'
```

### Manual Ingest

```bash
curl -X POST http://localhost/api/0.1.0/monitoring/ingest/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 11. Incentive Maximizer

The Maximizer resolves jurisdiction layers from a lat/lng coordinate and calculates the maximum incentive stack from all applicable rules in `incentive_rules`.

### How It Differs from the Calculator

| | Calculator | Maximizer |
|---|---|---|
| Input | Select jurisdiction from dropdown | Lat/lng coordinates or codes |
| Data source | `incentive_rules` (single jurisdiction) | `incentive_rules` (state + all sub-jurisdictions) |
| Stacking | Single jurisdiction | Additive stacking across all layers |
| Spatial | Manual selection | Automatic bounding-box lookup |
| Mutual exclusions | N/A | Automatically resolves conflicting rules (keeps higher value) |

### Via the UI

The **Maximizer** tab (⚡ icon, sidebar) provides a point-and-click interface to the stacking engine.

**Input controls:**

| Control | Description |
| ------- | ----------- |
| **Input Mode** | Toggle between *Codes* (comma/space-separated jurisdiction codes) and *Lat / Lng* (decimal coordinates) |
| **Jurisdiction Codes** | e.g. `NY, NY-NYC` — stack parent + sub-jurisdiction rules together |
| **Project Type** | Feature Film, TV Series, Commercial, Documentary, or All / Unknown — filters out TV-only rules for film projects |
| **Qualified Spend** | Dollar amount (USD) — converts percentage rules to real dollar values; live display shows formatted amount |
| **Split spend by location** | Appears when ≥ 2 codes are entered. Toggle to enter per-jurisdiction spend — sub-jurisdiction bonuses (e.g. IL-CHICAGO-BONUS) use their location's spend; other rules use the total. |

**Quick Presets** (one-click fill):

| Preset | Codes | Result (film, $5M) |
| ------ | ----- | ------------------- |
| NYC — $5M Film | `NY, NY-NYC` | $2.00M at 40% |
| Chicago — $5M Film | `IL, IL-COOK` | $2.50M at 50% |
| Los Angeles — $5M Film | `CA, CA-LA` | $1.50M at 30% |
| Erie County — $5M Film | `NY, NY-ERIE` | $1.50M at 30% |

**Results panel:**

- **Hero card** — total incentive value, effective rate, jurisdiction count, spend (shows *split* badge when location splits are active)
- **Applied Rules** — table of every rule applied, with rule type badge, dollar value, and underlying % rate
- **Breakdown by Category** — horizontal bar chart showing credit / rebate / permit-fee totals
- **Opt-in Upside** (amber) — rules that require an election and were excluded from the base total; shown as additive upside
- **Notes / Warnings** (slate) — mutual exclusions resolved, permit fees netted, and other advisory messages

### Via the API

**POST /api/0.1.0/maximize**

```json
{
  "jurisdiction_codes": ["IL", "IL-COOK"],
  "qualified_spend": 5000000,
  "project_type": "film",
  "spend_by_location": {
    "IL": 5000000,
    "IL-COOK": 2000000
  }
}
```

`spend_by_location` is optional. Omit it and every rule uses `qualified_spend`. Include it to scope sub-jurisdiction bonuses to their actual local spend. Keys are jurisdiction codes; values are USD. Jurisdictions not present fall back to `qualified_spend`.

Lat/lng mode:

```json
{
  "lat": 42.8864,
  "lng": -78.8784,
  "qualified_spend": 5000000,
  "project_type": "film"
}
```

**Response:**

```json
{
  "resolved_state": "NY",
  "jurisdictions_evaluated": 10,
  "qualified_spend": 5000000,
  "total_incentive_usd": 1500000.00,
  "effective_rate": 0.30,
  "breakdown": {
    "credit": 1500000.0,
    "rebate": 0.0,
    "tax_abatement": 0.0,
    "permit_fee": 0.0,
    "other": 0.0
  },
  "applied_rules": [
    {
      "rule_key": "NY-FILM-BASE",
      "rule_type": "tax_credit",
      "raw_value": 30.0,
      "value_unit": "percent",
      "computed_value": 1500000.0
    }
  ],
  "overridden_rules": [],
  "warnings": [
    "NY-FILM-BASE and NY-POST-PROD are mutually exclusive — kept NY-FILM-BASE ($1,500,000)"
  ],
  "recommendations": ["Incentive stack is clean — no conflicts detected"]
}
```

**GET /api/0.1.0/maximize/lookup?lat=42.8864&lng=-78.8784**

Returns the list of jurisdictions that contain the point — useful for populating frontend dropdowns.

### Via Command Line

```bash
# Basic — lat/lng, no spend (returns raw percentages)
python maximizer.py 42.8864 -78.8784

# With qualified spend — returns real dollar values
python maximizer.py 42.8864 -78.8784 --spend 5000000

# Explicit jurisdiction codes
python maximizer.py --codes NY NY-ERIE NY-NYC --spend 5000000

# Filter by project type
python maximizer.py 34.0522 -118.2437 --spend 10000000 --type film

# Split spend by location (Chicago: $5M total, $2M in Chicago)
python maximizer.py --codes IL IL-COOK --spend 5000000 --type film \
    --location-spend IL:5000000 IL-COOK:2000000
```

### Project-Type Filtering

Pass `project_type` to exclude rules that are inapplicable to your production category:

| Value | Rules excluded |
|---|---|
| `film` | Rules with `"tvSeries": true` in their requirements (e.g. `CA-TV-RELOCATE`) |
| `all` (default) | No filtering — all active rules included |

Additional project-type logic can be added to the `fetch_rules` SQL filter in `maximizer.py`.

### Opt-In Bonuses

Some rules require a production-specific election before they apply — a formal Green Sustainability Plan filing, a Relocation Series designation, etc. These rules have `"optIn": true` in their `requirements` JSON.

The Maximizer **excludes opt-in rules from the base total** and surfaces them as warnings instead:

```text
[!] IL-FILM-GREEN-BONUS (5% = $250,000) requires opt-in election — not included in base total
[!] IL-FILM-RELOCATION-BONUS (5% = $250,000) requires opt-in election — not included in base total
```

This prevents the engine from overstating incentives while still informing productions of potential upside if they take the qualifying action.

### Three-Market Benchmark ($5M Film)

Validated results from the engine as of April 2026:

| Market | Jurisdiction Codes | Base Incentive | Rate | Opt-In Upside |
| ------ | ------------------ | -------------- | ---- | ------------- |
| NYC | `NY` + `NY-NYC` | $2,000,000 | 40% | — |
| Chicago | `IL` + `IL-COOK` | $2,500,000 | 50% | +$500K (Green + Relocation bonuses) |
| Los Angeles | `CA` + `CA-LA` | $1,500,000 | 30% | — |
| Georgia | `GA` | $1,000,000 | 20% | +$500K (logo in credits) |

> Chicago's 50% rate: IL base (35%) + Chicago location bonus (15%). IL-CHICAGO-BONUS is scoped to IL-COOK spend — use the *Split spend by location* toggle to enter only the Chicago-local portion. Example: `spend_by_location={"IL": 5000000, "IL-COOK": 2000000}` → $2.05M at 41% instead of $2.5M at 50%.
>
> Georgia's 10% logo uplift (`GA-FILM-LOGO`) is opt-in: productions that include the Georgia promotional logo in their end credits qualify for the additional credit. It appears as opt-in upside in the Maximizer results, not in the base total.

### Spatial Resolution

Without PostGIS, the Maximizer uses bounding-box matching to identify the US state. It then loads the state + all direct child sub-jurisdictions (counties and cities with `parentId` = state id).

**Supported regions:** All 50 US states. International jurisdictions require explicit `jurisdiction_codes`.

### Breakdown Categories

| Category | What It Includes |
|---|---|
| `credit` | Tax credits (`tax_credit` rule type) |
| `tax_abatement` | Property tax abatements, tax breaks |
| `rebate` | Cash rebates on qualifying spend |
| `permit_fee` | Filming permit fees (shown as negative — reduces total) |
| `other` | Anything not mapped to the above |

### Mutual Exclusions

Some rules are mutually exclusive and cannot be stacked. When both are present, the Maximizer keeps the higher-value rule and adds a warning to the response. Currently defined:

| Rule A         | Rule B         | Reason                                                                                                                |
|----------------|----------------|-----------------------------------------------------------------------------------------------------------------------|
| `NY-FILM-BASE` | `NY-POST-PROD` | Post-production credit is for productions that did **not** shoot in NY — mutually exclusive with the production credit |

Additional exclusions are defined in the `MUTUAL_EXCLUSIONS` list in `maximizer.py`.

### Inheritance Logic

When multiple rules share the same `rule_key` across jurisdictions, the Maximizer applies **additive stacking** — values from all layers are summed. Override and strict modes are configurable via the `inheritance_policies` table.

---

## 12. Admin & User Management

**Navigation:** Sidebar → Settings → Admin (visible to admin role only)

### User Roles

| Role | Access |
|---|---|
| `admin` | Full access — all pages, user management, rule approval |
| `viewer` | Read-only — can view productions, run calculator, use advisor |

### Creating a User

1. Go to **Admin** page
2. Click **+ Invite User**
3. Enter email, temporary password, and assign role
4. Click **Create User**
5. Share credentials securely — users should change password on first login

### Updating a User

1. Click the user row in the admin table
2. Options:
   - **Change role** (admin ↔ viewer)
   - **Reset password** — set a new temporary password
   - **Deactivate** — blocks login without deleting the user
   - **Reactivate** — restores access
   - **Delete** — permanent

### Changing Your Own Password

1. Go to **Settings** → **Account**
2. Enter current password and new password
3. Click **Save**

---

## 13. Notifications & Preferences

**Navigation:** Settings → Notifications

### Setting Up Notifications

1. Enter your **email address** for notifications
2. Select **jurisdictions** to watch (you will be notified when their rules change)
3. Toggle **Active** to enable/disable all notifications
4. Click **Save**

### Notification Triggers

- A monitored jurisdiction's feed changes and a new PendingRule is created
- A compliance item on one of your productions is overdue
- A rule you follow is about to expire

### Managing via API

```bash
# Get preferences
GET /api/0.1.0/notifications/preferences/

# Create or update
POST /api/0.1.0/notifications/preferences/
{
  "jurisdictions": ["NY", "CA", "IL"],
  "emailAddress": "you@studio.com",
  "active": true
}

# Remove
DELETE /api/0.1.0/notifications/preferences/
```

---

## 14. Command-Line Tools

### monitor.py

Fetches government web pages, detects content changes, and extracts rules via Claude.

```bash
# Full scan — all sub-jurisdictions with feedUrl
python monitor.py

# Single jurisdiction
python monitor.py --code NY-ERIE

# Dry run — fetch and hash only, no DB writes or Claude calls
python monitor.py --dry-run

# Run with real Claude API (override MOCK_CLAUDE setting)
MOCK_CLAUDE=false python monitor.py --code NY-WESTCHESTER
```

**What it logs:**

```
[NY-ERIE] Change detected — sending to Claude
[NY-ERIE] 3 rule(s) extracted, confidence=0.82
[NY-NASSAU] No change
Complete — changed: 1  unchanged: 1  errors: 0  pending rules queued: 3
```

**Cron example (run nightly at 2 AM):**
```
0 2 * * * cd /app && python monitor.py >> /var/log/monitor.log 2>&1
```

---

### maximizer.py

Command-line interface to the incentive stacking engine.

```bash
python maximizer.py <lat> <lng> [--spend AMOUNT] [--type TYPE] [--codes CODE1 CODE2...]

# Examples
python maximizer.py 42.8864 -78.8784 --spend 5000000
python maximizer.py 34.0522 -118.2437 --spend 8000000 --type film
python maximizer.py --codes CA CA-LA --spend 8000000
```

**Output:**
```
PILOTFORGE MAXIMIZER RESULT
Resolved state:     CA
Jurisdictions:      2
Qualified spend:    $8,000,000
Total incentive:    $2,400,000.00
Effective rate:     30.0%

Breakdown:
  credit                  $2,400,000.00

Applied rules:   2
Overridden rules: 0
```

---

### Seed Scripts (scripts/)

| Script | Purpose | When to Run |
|---|---|---|
| `seed_jurisdictions.py` | Base US states + international | Fresh install only |
| `seed_incentive_rules.py` | State-level incentive rules | After jurisdictions |
| `seed_more_jurisdictions.py` | County/city sub-jurisdictions | After base jurisdictions |
| `seed_more_rules.py` | Additional rules and variants | After sub-jurisdictions |
| `seed_remaining_us_states.py` | Full 50-state coverage | Optional |
| `seed_global_expansion.py` | Canada, UK, Australia, Ireland, etc. | Optional |
| `seed_maximizer_test.py` | LocalRules for NY/CA/IL/GA (test data) | For Maximizer testing |
| `resolve_migrations.py` | Mark failed migrations as resolved | Migration fix only |
| `update_rules_2026.py` | Refresh rule rates and expiration dates | Annual update |

**Running a seed script:**
```bash
# Locally (with .env loaded)
python scripts/seed_jurisdictions.py

# Inside Docker container
docker cp scripts/seed_jurisdictions.py pilotforge-api:/app/scripts/seed_jurisdictions.py
docker exec pilotforge-api python scripts/seed_jurisdictions.py
```

> Scripts use `INSERT ... ON CONFLICT DO NOTHING` — safe to re-run.

---

## 15. API Reference

All endpoints require a JWT Bearer token except `POST /auth/login` and `POST /auth/token`.

### Authentication

```bash
# Get token
POST /api/0.1.0/auth/login
Body: { "email": "admin@pilotforge.com", "password": "pilotforge2024" }
Returns: { "access_token": "eyJ...", "token_type": "bearer" }

# Use token
curl -H "Authorization: Bearer eyJ..." http://localhost/api/0.1.0/productions/
```

Tokens expire after **8 hours** (configurable via `JWT_EXPIRE_HOURS`). A 401 response automatically clears the stored token and redirects to the login page.

---

### Productions

| Method | Path | Description |
|---|---|---|
| GET | `/productions/` | List all productions |
| POST | `/productions/` | Create production |
| GET | `/productions/{id}` | Get production detail |
| PUT | `/productions/{id}` | Update production |
| DELETE | `/productions/{id}` | Delete production |
| GET | `/productions/{id}/expenses/` | List expenses |
| POST | `/productions/{id}/expenses/` | Add expense |
| DELETE | `/productions/{id}/expenses/{eid}` | Delete expense |
| POST | `/productions/{id}/expenses/generate/` | Auto-generate expenses |
| GET | `/productions/{id}/compliance/` | List compliance items |
| POST | `/productions/{id}/compliance/generate/` | Auto-generate checklist |
| POST | `/productions/{id}/compliance/` | Add compliance item |
| PATCH | `/compliance/{item_id}` | Update compliance item |
| DELETE | `/compliance/{item_id}` | Delete compliance item |

### Calculator

| Method | Path | Description |
|---|---|---|
| POST | `/calculate/` | Quick calculate |
| POST | `/calculate/simple/` | Single rule calculation |
| POST | `/calculate/compare/` | Multi-jurisdiction compare |
| GET | `/calculate/jurisdiction/{id}` | Rules for jurisdiction |
| POST | `/calculate/compliance/` | Compliance check |
| POST | `/calculate/date-based/` | Date-specific rules |
| POST | `/calculate/scenario/` | Scenario modeling |

### Jurisdictions & Rules

| Method | Path | Description |
|---|---|---|
| GET | `/jurisdictions/` | List jurisdictions |
| GET | `/jurisdictions/{id}` | Jurisdiction detail |
| POST | `/jurisdictions/` | Create jurisdiction |
| PUT | `/jurisdictions/{id}` | Update jurisdiction |
| DELETE | `/jurisdictions/{id}` | Delete jurisdiction |
| GET | `/incentive-rules/` | List all incentive rules |
| GET | `/incentive-rules/{id}` | Rule detail |
| GET | `/local-rules/` | List local rules |
| GET | `/local-rules/by-jurisdiction/{code}/` | Rules for jurisdiction |
| POST | `/local-rules/` | Create local rule |
| PATCH | `/local-rules/{id}/` | Update local rule |
| DELETE | `/local-rules/{id}/` | Deactivate local rule |
| GET | `/local-rules/stats/summary/` | Local rules statistics |

### Pending Rules

| Method | Path                           | Description         |
|--------|--------------------------------|---------------------|
| GET    | `/pending-rules/`              | List pending rules  |
| GET    | `/pending-rules/{id}/`         | Pending rule detail |
| PATCH  | `/pending-rules/{id}/approve/` | Approve rule        |
| PATCH  | `/pending-rules/{id}/reject/`  | Reject rule         |

### Compliance Requirements (Checklist)

Non-quantified process requirements per jurisdiction (permits, insurance mandates, portal links, designations).

| Method | Path | Description |
| --- | --- | --- |
| GET | `/jurisdictions/{code}/requirements` | Compliance checklist. Query params: `project_type`, `include_parent` (default `true`), `active_only` (default `true`) |
| POST | `/jurisdictions/{code}/requirements` | Manually add a requirement |
| PATCH | `/requirements/{requirement_id}` | Update a requirement |
| DELETE | `/requirements/{requirement_id}` | Delete a requirement |

**GET example:**

```bash
# All requirements for Erie County, film projects only, including NY state requirements
GET /api/0.1.0/jurisdictions/NY-ERIE/requirements?project_type=film&include_parent=true
```

**Response shape:**

```json
{
  "jurisdictionCode": "NY-ERIE",
  "jurisdictionName": "Erie County",
  "projectType": "film",
  "total": 7,
  "byCategory": { "permit": 2, "insurance": 1, "portal": 1, "other": 3 },
  "requirements": [
    {
      "id": "uuid",
      "name": "Film Permit Required Before Filming",
      "category": "permit",
      "requirementType": "mandatory",
      "description": "...",
      "applicableTo": [],
      "fromParent": false
    }
  ]
}
```

### Stacking Engine & Maximizer

| Method | Path | Description |
|---|---|---|
| POST | `/stacking-engine/calculate/` | Stack for a scenario |
| POST | `/stacking-engine/compare/` | Compare across jurisdictions |
| GET | `/stacking-engine/jurisdictions-with-local-rules/` | Which jurisdictions have local rules |
| POST | `/maximize` | Full maximize (lat/lng or codes) |
| GET | `/maximize/lookup` | Resolve jurisdictions for a point |

### Monitoring & Reports

| Method | Path | Description |
|---|---|---|
| GET | `/monitoring/events/` | List events |
| GET | `/monitoring/events/unread-count/` | Unread count |
| PATCH | `/monitoring/events/{id}/read/` | Mark read |
| POST | `/monitoring/events/mark-all-read/` | Mark all read |
| GET | `/monitoring/sources/` | List sources |
| POST | `/monitoring/sources/` | Add source |
| POST | `/monitoring/ingest/` | Trigger ingest |
| POST | `/reports/comparison/` | PDF comparison report |
| POST | `/reports/compliance/` | PDF compliance report |
| POST | `/reports/scenario/` | PDF scenario report |
| POST | `/excel/comparison/` | Excel comparison workbook |
| POST | `/excel/compliance/` | Excel compliance workbook |
| POST | `/excel/scenario/` | Excel scenario workbook |

### AI & Admin

| Method | Path | Description |
|---|---|---|
| POST | `/advisor/chat/` | Streaming AI chat (SSE) |
| GET | `/admin/users/` | List users |
| POST | `/admin/users/` | Create user |
| PATCH | `/admin/users/{id}/` | Update user |
| DELETE | `/admin/users/{id}/` | Delete user |
| GET | `/notifications/preferences/` | Get preferences |
| POST | `/notifications/preferences/` | Set preferences |
| DELETE | `/notifications/preferences/` | Remove preferences |
| GET | `/health` | Health check |

---

## 16. Database Models

### Core Models

**User** — Platform accounts
- `email` (unique), `passwordHash`, `role` (admin/viewer), `isActive`

**Jurisdiction** — States, counties, cities, countries
- `code` (unique — e.g., `NY`, `NY-ERIE`), `name`, `type`, `country`, `currency`
- `parentId` — links counties/cities to their parent state
- `feedUrl`, `feedLastChecked`, `feedLastHash` — monitoring fields
- `treatyPartners[]` — array of co-treaty jurisdiction codes

**IncentiveRule** — Primary state-level tax incentive rules
- `ruleCode` (unique), `ruleName`, `incentiveType`, `percentage`, `fixedAmount`
- `minSpend`, `maxCredit`, `eligibleExpenses[]`, `excludedExpenses[]`, `creditType`
- `effectiveDate`, `expirationDate`
- `requirements` (JSON) — machine-readable eligibility flags read by the Maximizer:
  - `"tvSeries": true` — rule is excluded when `project_type=film`
  - `"optIn": true` — rule requires production election; excluded from base total, surfaced as warning
  - `"relocatingProject": true` — rule only applies to productions relocating to the jurisdiction

**LocalRule** — County/city/sub-jurisdiction rules
- `code` (unique), `name`, `category`, `ruleType`, `amount`, `percentage`
- `effectiveDate`, `expirationDate`, `sourceUrl`, `extractedBy` (manual/monitor), `active`

**JurisdictionRequirement** — Non-quantified compliance requirements (no dollar/percent value)

- `name`, `category` — `permit | insurance | registration | designation | infrastructure | portal | contact | other`
- `requirementType` — `mandatory | recommended | informational`
- `description`, `applicableTo[]` — project types this applies to; empty = all types
- `contactInfo`, `portalUrl`, `sourceUrl`
- `extractedBy` (monitor/manual), `active`
- Linked to `Jurisdiction` via `jurisdictionId`; inherits parent requirements via `include_parent` query param

**Production** — Film/TV productions
- `title`, `productionType`, `budgetTotal`, `budgetQualifying`
- `status` — `planning | pre_production | production | post_production | completed`
- `jurisdictionId`, `startDate`, `endDate`, `productionCompany`

**Expense** — Production expense line items
- `category`, `description`, `amount`, `expenseDate`
- `isQualifying` — whether this expense counts toward incentive calculation
- `vendorName`, `vendorLocation`, `receiptNumber`, `invoiceNumber`

**ComplianceItem** — Checklist items per production
- `label`, `category`, `status` (pending/complete/waived/na)
- `dueDate`, `completedAt`, `notes`

**PendingRule** — Extracted rules awaiting review
- `sourceUrl`, `rawContent`, `extractedData` (JSON), `confidence`
- `status` — `pending | approved | rejected`
- `reviewNotes`, `reviewedBy`, `reviewedAt`

**MonitoringSource** — Feed sources to watch
- `name`, `url`, `feedUrl`, `sourceType` (rss/atom/page)
- `jurisdiction`, `active`, `lastFetched`

**MonitoringEvent** — Change detections
- `title`, `summary`, `url`, `contentHash`
- `severity` (info/warning/alert), `isRead`, `publishedAt`

**NotificationPreference** — Per-user notification settings
- `jurisdictions[]`, `emailAddress`, `active`

**InheritancePolicy** — How rules cascade between parent/child jurisdictions
- `childJurisdictionId`, `parentJurisdictionId`
- `policyType` — additive / override / strict
- `ruleCategory`, `priority`

### Phase 0: Stacking & Scenarios

**SubJurisdiction** — County/city incentive layers (stacking engine)
- `type` (county/city/region/special_district)
- `incentiveType` (credit/rebate/fee_waiver/in_kind)
- `ratePercent`, `fixedAmount`, `capPerProduction`, `annualCap`, `minSpendRequired`
- `stackingRules` (JSON), `eligibleExpenditureCategories` (JSON)
- `localHirePercentageRequired`

**ProductionScenario** — What-if scenarios per production
- `name`, `totalBudget`, `qualifiedSpend`, `spendByCategory` (JSON)
- `shootingDays`, `daysByJurisdiction` (JSON), `localHirePercent`

**ScenarioOptimizationResult** — Cached stacking engine output
- `recommendedStack` (JSON), `totalIncentiveValue`, `effectiveRate`
- `cashFlowEstimate`, `warnings` (JSON), `expiresAt`

---

## 17. Deployment & Operations

### Docker Compose (Local Development)

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f backend
docker compose logs -f frontend

# Rebuild after code changes
docker compose build backend
docker compose up -d backend

# Rebuild frontend (after UI changes)
docker compose build frontend
docker compose up -d frontend

# Restart a service
docker compose restart backend
```

### Copying Files Into Containers

The backend `src/` directory is volume-mounted, so changes to `src/` are live. Files at the project root (like `maximizer.py`) are **not** volume-mounted and must be copied:

```bash
docker cp maximizer.py pilotforge-api:/app/maximizer.py
docker cp scripts/my_script.py pilotforge-api:/app/scripts/my_script.py
```

### Railway Deployment

The platform deploys to Railway using Railpack (backend) and a Dockerfile (frontend).

**Backend service:** `Tax_Incentive_Compliance_Platform`
**Frontend service:** `nurturing-flow`
**Database service:** `Postgres`

**`railway.toml` (backend):**
```toml
[build]
builder = "RAILPACK"
buildCommand = "pip install -r requirements.txt && python -m prisma generate"

[build.environment]
PYTHON_VERSION = "3.12"

[deploy]
startCommand = "uvicorn src.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
```

**Required Railway environment variables:**
```
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret-here
ANTHROPIC_API_KEY=sk-ant-...
```

### Health Check

```bash
curl https://your-backend-domain.railway.app/health
# Returns: {"status": "ok", "database": "connected"}
```

### API Documentation (Live)

```
https://your-backend-domain.railway.app/docs
https://your-backend-domain.railway.app/redoc
```

---

## 18. Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `JWT_SECRET` | Yes | — | Secret key for JWT signing (32+ chars) |
| `ANTHROPIC_API_KEY` | No | — | Claude API key (AI Advisor + monitor.py rule extraction) |
| `MOCK_CLAUDE` | No | `false` | Set `true` to use simulated Claude responses |
| `JWT_ALGORITHM` | No | `HS256` | JWT signing algorithm |
| `JWT_EXPIRE_HOURS` | No | `8` | Token lifetime in hours |
| `APP_HOST` | No | `0.0.0.0` | Server bind address |
| `APP_PORT` | No | `8000` | Server port |
| `LOG_LEVEL` | No | `info` | Logging verbosity |
| `API_VERSION` | No | `0.1.0` | API path version segment |

**Example `.env`:**
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5435/tax_incentive_db
JWT_SECRET=my-super-secret-32-char-key-here
ANTHROPIC_API_KEY=sk-ant-api03-...
MOCK_CLAUDE=false
JWT_EXPIRE_HOURS=8
```

---

## 19. Troubleshooting

### Login fails — "Invalid credentials"
- Confirm you are using `admin@pilotforge.com` / `pilotforge2024`
- Confirm the backend is running: `curl http://localhost/health`
- Check backend logs: `docker compose logs backend`

### All pages show blank / white screen
- Rebuild: `docker compose build backend && docker compose up -d backend`
- Check browser console for JS errors
- Confirm you are using `http://localhost` (port 80), **not** `http://localhost:3000`

### API calls return 405 Method Not Allowed
- You are hitting port 3000 directly — that nginx has no `/api/` proxy
- Always use `http://localhost` (port 80)

### "Failed to load pending rules" or "Failed to load local rules"
- Check that migrations ran: `docker exec pilotforge-api python -m prisma migrate status`
- Re-run if needed: `docker exec pilotforge-api python -m prisma migrate deploy`

### monitor.py returns "invalid x-api-key" (401)
- `ANTHROPIC_API_KEY` in `.env` is missing or invalid
- Use mock mode for local testing: `MOCK_CLAUDE=true python monitor.py`

### maximizer.py returns "No jurisdictions found"
- The `jurisdictions` table is empty — run `seed_jurisdictions.py`
- Coordinates must fall within a US state's bounding box
- Use `--codes` to specify explicitly: `python maximizer.py --codes NY --spend 1000000`

### Prisma P3009 migration error on Railway
- A migration was recorded as failed in `_prisma_migrations`
- Run: `python scripts/resolve_migrations.py`

### Database connection refused
- Check `DATABASE_URL` is set correctly
- Verify postgres container is healthy: `docker compose ps`
- Test: `docker exec pilotforge-api python -c "import psycopg2, os; psycopg2.connect(os.environ['DATABASE_URL']); print('OK')"`

### Frontend shows stale data / old UI
- Hard refresh: Ctrl+Shift+R (Windows) / Cmd+Shift+R (Mac)
- Rebuild frontend: `docker compose build frontend && docker compose up -d frontend`
- Clear `localStorage` in browser devtools if auth token is stale

### AI Advisor shows no response / stops streaming
- Check `ANTHROPIC_API_KEY` is set: `docker exec pilotforge-api printenv ANTHROPIC_API_KEY`
- Set `MOCK_CLAUDE=true` for scripted fallback responses
- Check backend logs for SSE errors: `docker compose logs -f backend`

---

*PilotForge v2.1 — Tax Incentive Compliance Platform*
*For support, file an issue at the project repository.*
