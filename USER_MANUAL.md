# PilotForge
> Tax Incentive Intelligence for Film & TV
> Tax Incentive Intelligence for Film & TV
## User Manual v1.0

**Platform Version:** 0.1.0  
**API Version:** v1  
**Last Updated:** January 9, 2026  
**Documentation Standard:** OAS 3.1

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Platform Capabilities](#platform-capabilities)
4. [API Endpoints Reference](#api-endpoints-reference)
5. [Use Cases & Examples](#use-cases--examples)
6. [Data Reference](#data-reference)
7. [Troubleshooting](#troubleshooting)
8. [Technical Specifications](#technical-specifications)

---

## 🎯 Overview

### What is the PilotForge?

The PilotForge is a **jurisdictional rule engine** designed to help film and television production companies:

- **Discover** available tax incentives across global jurisdictions
- **Compare** incentive programs side-by-side
- **Calculate** potential tax savings for productions
- **Ensure compliance** with jurisdiction-specific requirements
- **Optimize** production location decisions

### Who Should Use This Platform?

- **Production Companies** - Find the best locations for tax incentives
- **Production Accountants** - Calculate and track incentive claims
- **Line Producers** - Budget productions with accurate incentive estimates
- **Location Scouts** - Identify financially advantageous filming locations
- **Film Commissions** - Manage and publish incentive program information
- **Studios** - Strategic planning for multi-project slates

### Key Benefits

✅ **Comprehensive Data** - 32 jurisdictions, 33+ incentive programs  
✅ **Real-Time Access** - RESTful API with instant responses  
✅ **Accurate Calculations** - Rule-based engine ensures compliance  
✅ **Easy Integration** - Standard REST API, works with any system  
✅ **Up-to-Date Information** - Regular updates to incentive rules  

---

## 🚀 Getting Started

### Accessing the Platform

**Base URL:** `http://localhost:8000`

**Interactive Documentation:**
- **Swagger UI:** http://localhost:8000/docs (Try it live!)
- **ReDoc:** http://localhost:8000/redoc (Beautiful documentation)
- **OpenAPI Spec:** http://localhost:8000/openapi.json

### Authentication

**Current Version:** No authentication required (development mode)  
**Production:** Will require API keys (coming soon)

### Making Your First Request

#### Example 1: Get All Jurisdictions
```bash
curl http://localhost:8000/api/v1/jurisdictions/
```

#### Example 2: Find Georgia's Incentive Rules
```bash
# First, get Georgia's ID
curl http://localhost:8000/api/v1/jurisdictions/ | grep -A 5 "Georgia"

# Then get its rules (replace {id} with actual ID)
curl http://localhost:8000/api/v1/incentive-rules/?jurisdiction_id={id}
```

---

## 💡 Platform Capabilities

### Current Features (Phase 2 Complete)

#### ✅ Jurisdiction Management
- View all available filming jurisdictions
- Filter by country, type (state/province/country), active status
- Access jurisdiction details (website, contact info, description)

#### ✅ Incentive Rules Database
- Access 33+ real tax incentive programs
- Filter by jurisdiction, incentive type, status
- View detailed requirements and qualifications
- See eligible and excluded expenses

#### ✅ Production Tracking
- Create production records
- Track budgets and timelines
- Associate with target jurisdictions

### Coming Soon (Phase 3+)

#### 🔜 Tax Credit Calculator
- Calculate exact savings for your production
- Compare multiple jurisdictions automatically
- Get recommendations: "Film in X, save $Y more"

#### 🔜 Compliance Checker
- Verify your production meets requirements
- Get alerts for missing documentation
- Track compliance status

#### 🔜 Expense Tracking
- Categorize production expenses
- Auto-categorize as qualifying or non-qualifying
- Generate expense reports

---

## 📡 API Endpoints Reference

### Base URL
```
http://localhost:8000/api/v1
```

---

### **Jurisdictions API**

#### GET /jurisdictions/
**Purpose:** List all available filming jurisdictions

**Query Parameters:**
- `country` (string, optional) - Filter by country (e.g., "USA", "Canada")
- `type` (string, optional) - Filter by type ("state", "province", "country")
- `active` (boolean, optional) - Filter by active status

**Response:**
```json
{
  "total": 32,
  "jurisdictions": [
    {
      "id": "uuid",
      "name": "California",
      "code": "CA",
      "country": "USA",
      "type": "state",
      "active": true,
      "description": "California Film & Television Tax Credit Program",
      "website": "https://film.ca.gov",
      "createdAt": "2026-01-08T...",
      "updatedAt": "2026-01-08T..."
    }
  ]
}
```

**Example Use Cases:**
- Find all US states: `GET /jurisdictions/?country=USA`
- Find all provinces: `GET /jurisdictions/?type=province`
- Find active jurisdictions: `GET /jurisdictions/?active=true`

---

#### GET /jurisdictions/{id}
**Purpose:** Get details for a specific jurisdiction

**Path Parameters:**
- `id` (string, required) - Jurisdiction UUID

**Response:** Single jurisdiction object

**Example:**
```bash
GET /jurisdictions/bfae464b-9551-4aad-b5e7-2abcf687134e
```

---

#### POST /jurisdictions/
**Purpose:** Create a new jurisdiction (Admin only)

**Request Body:**
```json
{
  "name": "Washington",
  "code": "WA",
  "country": "USA",
  "type": "state",
  "description": "Washington State Film Incentive",
  "website": "https://www.filmseattle.com",
  "active": true
}
```

**Response:** Created jurisdiction with ID (201 Created)

---

#### PUT /jurisdictions/{id}
**Purpose:** Update a jurisdiction (Admin only)

**Path Parameters:**
- `id` (string, required)

**Request Body:** Any jurisdiction fields to update

---

#### DELETE /jurisdictions/{id}
**Purpose:** Delete a jurisdiction (Admin only)

**Path Parameters:**
- `id` (string, required)

**Response:** 204 No Content

---

### **Incentive Rules API**

#### GET /incentive-rules/
**Purpose:** List all tax incentive programs

**Query Parameters:**
- `jurisdiction_id` (string, optional) - Filter by jurisdiction
- `incentive_type` (string, optional) - Filter by type ("tax_credit", "rebate", "grant", "exemption")
- `active` (boolean, optional) - Filter by active status

**Response:**
```json
{
  "total": 33,
  "rules": [
    {
      "id": "uuid",
      "jurisdictionId": "uuid",
      "ruleName": "California Film & TV Tax Credit 2.0",
      "ruleCode": "CA-FILM-2.0",
      "incentiveType": "tax_credit",
      "percentage": 20.0,
      "minSpend": 1000000,
      "maxCredit": 10000000,
      "eligibleExpenses": ["labor", "equipment", "locations", "post_production"],
      "excludedExpenses": ["above_the_line", "marketing"],
      "effectiveDate": "2024-01-01T00:00:00Z",
      "requirements": {
        "minShootDays": 10,
        "californiaResidents": 75
      },
      "active": true,
      "createdAt": "2026-01-08T...",
      "updatedAt": "2026-01-08T..."
    }
  ]
}
```

**Example Use Cases:**
- Find all tax credits: `GET /incentive-rules/?incentive_type=tax_credit`
- Find Georgia's programs: `GET /incentive-rules/?jurisdiction_id={ga-id}`
- Find active programs: `GET /incentive-rules/?active=true`

---

#### GET /incentive-rules/{id}
**Purpose:** Get details for a specific incentive rule

**Path Parameters:**
- `id` (string, required) - Rule UUID

**Response:** Single rule object with full details

---

#### POST /incentive-rules/
**Purpose:** Create a new incentive rule (Admin only)

**Request Body:**
```json
{
  "jurisdictionId": "uuid",
  "ruleName": "Program Name",
  "ruleCode": "CODE-001",
  "incentiveType": "tax_credit",
  "percentage": 25.0,
  "minSpend": 500000,
  "maxCredit": 5000000,
  "eligibleExpenses": ["labor", "equipment"],
  "excludedExpenses": ["marketing"],
  "effectiveDate": "2024-01-01T00:00:00Z",
  "requirements": {},
  "active": true
}
```

**Response:** Created rule with ID (201 Created)

---

#### PUT /incentive-rules/{id}
**Purpose:** Update an incentive rule (Admin only)

---

#### DELETE /incentive-rules/{id}
**Purpose:** Delete an incentive rule (Admin only)

---

### **Productions API**

#### GET /productions/
**Purpose:** List all productions

**Query Parameters:**
- `production_type` (string, optional) - Filter by type
- `active` (boolean, optional) - Filter by active status

**Response:**
```json
{
  "total": 5,
  "productions": [
    {
      "id": "uuid",
      "title": "Untitled Action Film",
      "productionType": "feature",
      "jurisdictionId": "uuid",
      "budgetTotal": 5000000,
      "budgetQualifying": 4500000,
      "startDate": "2026-06-01",
      "endDate": "2026-08-15",
      "productionCompany": "Acme Productions",
      "status": "planning",
      "createdAt": "2026-01-09T...",
      "updatedAt": "2026-01-09T..."
    }
  ]
}
```

---

#### GET /productions/{id}
**Purpose:** Get production details

---

#### POST /productions/
**Purpose:** Create a new production

**Request Body:**
```json
{
  "title": "My Film Project",
  "productionType": "feature",
  "jurisdictionId": "uuid",
  "budgetTotal": 5000000,
  "startDate": "2026-06-01",
  "productionCompany": "Your Company",
  "status": "planning"
}
```

---

#### PUT /productions/{id}
**Purpose:** Update production details

---

#### DELETE /productions/{id}
**Purpose:** Delete a production

---

### **System Endpoints**

#### GET /health
**Purpose:** Check system health

**Response:**
```json
{
  "status": "healthy",
  "database": "healthy",
  "api_version": "v1"
}
```

---

## 🎬 Use Cases & Examples

### Use Case 1: Find Best Location for $5M Feature Film

**Goal:** Determine which jurisdiction offers the best tax incentive for a $5M feature film.

**Steps:**

1. **Get all active jurisdictions:**
```bash
GET /jurisdictions/?active=true
```

2. **For each jurisdiction, get incentive rules:**
```bash
GET /incentive-rules/?jurisdiction_id={id}
```

3. **Compare rates:**
   - Georgia: 30% (with promo)
   - New York: 30%
   - Louisiana: 25% + 10% payroll = 35%
   - California: 20-25%
   - New Zealand: 40% (highest!)

4. **Check requirements:**
   - Minimum spend thresholds
   - Local hiring percentages
   - Qualifying expenses

**Result:** For $5M budget, New Zealand offers best rate (40% = $2M credit), but has $15M minimum spend. Louisiana offers 35% stackable ($1.75M) with lower minimum.

---

### Use Case 2: Budget a TV Series in Multiple States

**Goal:** Production wants to film in 3 states. Calculate total incentives.

**Steps:**

1. **Create production record:**
```bash
POST /productions/
{
  "title": "Mystery Series Season 1",
  "productionType": "tv_series",
  "jurisdictionId": "ny-id",
  "budgetTotal": 15000000,
  "startDate": "2026-09-01",
  "productionCompany": "StreamCo Productions",
  "status": "planning"
}
```

2. **Get incentive rules for all target states:**
   - New York: 30%
   - New Jersey: 30% + 5% diversity = 35%
   - Pennsylvania: 25-30%

3. **Calculate per-state:**
   - NY (5 episodes): $5M spend × 30% = $1.5M
   - NJ (3 episodes): $3M spend × 35% = $1.05M
   - PA (2 episodes): $2M spend × 27.5% = $550K
   - **Total incentives: $3.1M**

---

### Use Case 3: Check Compliance Requirements

**Goal:** Verify production meets Georgia's requirements for 30% credit.

**Steps:**

1. **Get Georgia's rules:**
```bash
GET /incentive-rules/?jurisdiction_id={ga-id}
```

2. **Check requirements:**
```json
{
  "georgiaSpend": 500000,
  "georgiaPromo": true,
  "logoInCredits": true
}
```

3. **Compliance Checklist:**
   - ✅ $500K minimum spend in Georgia
   - ✅ Include Georgia logo in credits
   - ✅ Promotional requirements met
   - **Result: Qualifies for 30% rate**

---

### Use Case 4: Compare International Options

**Goal:** Major studio wants to compare US vs international incentives.

**Comparison Table:**

| Jurisdiction | Rate | Min Spend | Max Credit | Notes |
|-------------|------|-----------|------------|-------|
| Georgia (US) | 30% | $500K | None | Best US rate |
| California (US) | 20-25% | $1M | $10M | Competitive allocation |
| Louisiana (US) | 35% | $300K | None | Stackable credits |
| UK | 25% | £1M | None | Strong infrastructure |
| Ireland | 32% | €250K | None | Cultural test required |
| France | 30% | €1M | €30M | TRIP program |
| New Zealand | 40% | NZ$15M | None | Highest rate! |
| Canada BC | 35% | None | None | Strong for Canadian content |

**Analysis:**
- **Highest rate:** New Zealand (40%)
- **Best for mid-budget:** Louisiana (35%, low minimum)
- **Best for mega-budget:** New Zealand or UK
- **Best for Canadian content:** British Columbia (35%)

---

## 📊 Data Reference

### Supported Jurisdictions (32 Total)

#### United States (20)
- California (CA)
- Georgia (GA)
- New York (NY)
- Texas (TX)
- Louisiana (LA)
- New Mexico (NM)
- Massachusetts (MA)
- Connecticut (CT)
- Illinois (IL)
- Pennsylvania (PA)
- North Carolina (NC)
- Florida (FL)
- Michigan (MI)
- New Jersey (NJ)
- Virginia (VA)
- Colorado (CO)
- Hawaii (HI)
- Oregon (OR)
- Montana (MT)
- Mississippi (MS)

#### Canada (4)
- British Columbia (BC)
- Ontario (ON)
- Quebec (QC)
- Alberta (AB)

#### Australia (3)
- New South Wales (NSW)
- Victoria (VIC)
- Queensland (QLD)

#### Europe (3)
- United Kingdom (UK)
- Ireland (IE)
- France (FR)
- Spain (ES)

#### Oceania (1)
- New Zealand (NZ)

---

### Incentive Types

**tax_credit** - Tax credit against production company taxes  
**rebate** - Cash rebate paid directly to production  
**grant** - Government grant (does not require tax liability)  
**exemption** - Sales tax or other tax exemptions  

---

### Expense Categories

**Eligible Expenses (commonly):**
- labor (crew wages)
- equipment (rentals, purchases)
- locations (location fees)
- post_production (editing, vfx, sound)
- lodging (cast/crew accommodation)
- transportation (production-related)

**Excluded Expenses (commonly):**
- above_the_line (producers, directors, lead actors over cap)
- marketing (advertising, promotion)
- distribution (delivery, duplication)
- financing (interest, fees)
- development (pre-greenlight costs)

---

### Production Types

- **feature** - Feature film (theatrical release)
- **tv_series** - Television series
- **tv_movie** - Television movie
- **commercial** - Commercial/advertising
- **documentary** - Documentary film
- **web_series** - Web/streaming series
- **pilot** - Television pilot

---

### Production Status

- **planning** - In development/planning phase
- **pre_production** - Pre-production (casting, location scouting)
- **production** - Principal photography in progress
- **post_production** - Editing, vfx, finishing
- **completed** - Production wrapped and delivered
- **on_hold** - Temporarily paused
- **cancelled** - Project cancelled

---

## 🔧 Troubleshooting

### Common Issues

#### Issue: "Cannot connect to API"

**Symptoms:** Browser shows "Cannot reach this page"

**Solutions:**
1. Check server is running: Look for "Application startup complete"
2. Verify URL: http://localhost:8000
3. Check Docker: `docker ps` should show `tax-incentive-db`
4. Restart server: `python -m uvicorn src.main:app --reload`

---

#### Issue: "Database connection failed"

**Symptoms:** "Client is not connected to the query engine"

**Solutions:**
1. Check PostgreSQL: `docker ps` (should show tax-incentive-db)
2. Start database: `docker-compose up -d`
3. Test connection: `docker exec tax-incentive-db pg_isready -U postgres`
4. Check .env file has: `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tax_incentive_db?schema=public`

---

#### Issue: "404 Not Found" on endpoint

**Symptoms:** Endpoint returns 404 error

**Solutions:**
1. Check endpoint path (case-sensitive)
2. Verify API version prefix: `/api/v1/`
3. Check available endpoints: `GET /api/v1/`
4. Refresh Swagger docs: http://localhost:8000/docs

---

#### Issue: "422 Validation Error"

**Symptoms:** Request rejected with validation errors

**Solutions:**
1. Check required fields are included
2. Verify data types (strings, numbers, dates)
3. Check date format: "YYYY-MM-DD" or "YYYY-MM-DDTHH:MM:SSZ"
4. Review error details in response body
5. Use Swagger UI to see field requirements

---

#### Issue: No data returned (empty arrays)

**Symptoms:** `{"total": 0, "jurisdictions": []}`

**Solutions:**
1. Run seed scripts:
   - `python scripts/seed_jurisdictions.py`
   - `python scripts/seed_incentive_rules.py`
2. Check database: `docker exec tax-incentive-db psql -U postgres -d tax_incentive_db -c "SELECT COUNT(*) FROM jurisdictions;"`
3. Verify migrations: `python -m prisma migrate status`

---

### Error Code Reference

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Delete successful |
| 400 | Bad Request | Invalid request data |
| 404 | Not Found | Resource doesn't exist |
| 422 | Validation Error | Request data doesn't meet requirements |
| 500 | Internal Server Error | Server-side error (check logs) |

---

## ⚙️ Technical Specifications

### System Requirements

**Development Environment:**
- Python 3.12+
- Docker Desktop
- PostgreSQL 16 (via Docker)
- 4GB RAM minimum
- 10GB disk space

**Production Environment:**
- Python 3.12+
- PostgreSQL 16+
- 8GB RAM recommended
- Load balancer (for high traffic)
- SSL certificate

---

### Technology Stack

**Backend:**
- **Framework:** FastAPI 0.109.0
- **Database:** PostgreSQL 16
- **ORM:** Prisma Client Python 0.15.0
- **Server:** Uvicorn (ASGI)
- **Language:** Python 3.12

**API:**
- **Standard:** OpenAPI 3.1 / OAS 3.1
- **Documentation:** Swagger UI, ReDoc
- **Format:** JSON
- **Authentication:** API Keys (coming soon)

**Database:**
- **Engine:** PostgreSQL 16-alpine
- **Container:** Docker
- **Migrations:** Prisma Migrate
- **Backup:** Automated daily (production)

---

### Performance

**Response Times:**
- Simple GET: <50ms
- Filtered queries: <100ms
- Complex calculations: <500ms

**Capacity:**
- Jurisdictions: 1000+
- Incentive Rules: 10,000+
- Productions: Unlimited
- Concurrent users: 100+ (can scale)

---

### Security

**Current (Development):**
- No authentication required
- CORS enabled for localhost
- SQL injection protection (Prisma ORM)

**Production (Coming):**
- API key authentication
- Rate limiting (60 requests/minute)
- HTTPS only
- Input validation
- Audit logging

---

### API Versioning

**Current:** v1  
**Stability:** Beta  
**Breaking Changes:** Will be communicated 30 days in advance  
**Deprecation Policy:** Endpoints supported for 6 months after deprecation  

---

### Rate Limits

**Development:** No limits  
**Production (Free Tier):** 60 requests/minute  
**Production (Pro Tier):** 600 requests/minute  
**Production (Enterprise):** Custom limits  

---

### Data Retention

**Productions:** Indefinite  
**Calculations:** 2 years  
**Audit Logs:** 1 year  
**Deleted Records:** 30-day recovery period  

---

## 📞 Support

### Getting Help

**Documentation:**
- User Manual: This document
- API Reference: http://localhost:8000/docs
- Technical Specs: WORKING_STATE.md

**GitHub:**
- Repository: https://github.com/hneal055/PilotForge
> Tax Incentive Intelligence for Film & TV
> Tax Incentive Intelligence for Film & TV
- Issues: Report bugs and request features
- Discussions: Ask questions, share ideas

**Contact:**
- Developer: Howard Neal
- Project: PilotForge
> Tax Incentive Intelligence for Film & TV
> Tax Incentive Intelligence for Film & TV
- Version: 0.1.0 (Beta)

---

### Contributing

Interested in contributing data or features?
1. Fork the repository
2. Create feature branch
3. Submit pull request
4. Include tests and documentation

---

### Roadmap

**Phase 3 (Q1 2026):**
- Calculator Engine
- Rule Validator
- Comparison Tool

**Phase 4 (Q2 2026):**
- Expenses API
- Calculations API
- Report Generation

**Phase 5 (Q3 2026):**
- Testing Suite
- Performance Optimization
- Security Audit

**Phase 6 (Q4 2026):**
- Web Interface
- User Authentication
- Admin Dashboard

**Phase 7 (2027):**
- Production Deployment
- Mobile App
- Advanced Analytics

---

## 📄 Legal

### Disclaimer

This platform provides information about film tax incentive programs. While we strive for accuracy:

- **Not Legal Advice:** Consult with tax professionals and attorneys
- **Not Financial Advice:** Verify all calculations with accountants
- **Subject to Change:** Incentive programs change; verify current status
- **No Guarantee:** We don't guarantee eligibility or approval

### Data Sources

Incentive rule data sourced from:
- Official film commission websites
- Government tax authority publications
- Industry publications
- Direct communication with film offices

### License

**All Rights Reserved - Proprietary and Confidential**

This software and all associated materials (code, data, and documentation) are proprietary and confidential. Unauthorized copying, distribution, modification, or use is strictly prohibited. See [LICENSE](./LICENSE) for full terms and restrictions.  

---

### Updates

**Last Updated:** January 9, 2026  
**Version:** 1.0  
**Next Review:** March 2026  

---

**End of User Manual**

For the latest version of this manual, visit: https://github.com/hneal055/PilotForge/blob/main/USER_MANUAL.md
