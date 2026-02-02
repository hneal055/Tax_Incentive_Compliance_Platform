# 📖 Tax-Incentive Compliance Platform - User Manual

> Complete API documentation and usage guide

---

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Frontend UI Guide](#frontend-ui-guide)
3. [Authentication](#authentication)
4. [Calculator API](#calculator-api)
5. [Reports API](#reports-api)
6. [Excel Export API](#excel-export-api)
7. [Data Management APIs](#data-management-apis)
8. [Response Formats](#response-formats)
9. [Error Handling](#error-handling)
10. [Rate Limits](#rate-limits)
11. [Best Practices](#best-practices)

---

## 🚀 Getting Started

### **Base URL**
```
http://localhost:8000/api/v1
```

### **Interactive Documentation**
```
http://localhost:8000/docs       # Swagger UI
http://localhost:8000/redoc      # ReDoc
```

### **API Root**
```http
GET /api/v1/
```

**Response:**
```json
{
  "message": "Tax-Incentive Compliance Platform API",
  "version": "v1",
  "endpoints": {
    "jurisdictions": "/api/v1/jurisdictions",
    "incentive_rules": "/api/v1/incentive-rules",
    "productions": "/api/v1/productions",
    "calculator": "/api/v1/calculate",
    "reports": "/api/v1/reports",
    "excel": "/api/v1/excel"
  }
}
```

---

## 🎨 Frontend UI Guide

The PilotForge platform features a modern React frontend providing an intuitive interface for managing productions and calculating tax incentives.

### **Accessing the UI**

**Development:**
```
http://localhost:3000
```

**Production:**
```
https://pilotforge.onrender.com
```

### **Dashboard**

The main dashboard provides an overview of your productions and available jurisdictions.

**Features:**
- **Production Count**: Total number of productions in the system
- **Jurisdiction Overview**: Grid display of all 32+ jurisdictions
- **Quick Actions**: 
  - "Create Production" - Navigate to production creation
  - "View Jurisdictions" - Browse all available jurisdictions
- **Jurisdiction Grid**: Visual cards showing each jurisdiction with:
  - Jurisdiction name
  - Country
  - Type (State, Country, Province)

**Navigation:**
1. Access dashboard at `/` (root path)
2. Click "Create Production" to add a new production
3. Click "View Jurisdictions" to explore jurisdictions
4. Use navbar to navigate to other sections

### **Productions Management**

Manage all your film and TV productions in one place.

**Accessing Productions:**
- Click "Productions" in the navbar
- Or navigate to `/productions`

**Viewing Productions:**
- See list of all productions
- Each production shows:
  - Title
  - Budget
  - Status (Active, Pre-Production, Post-Production)
  - Jurisdiction
  - Created date
- Click on a production to view details

**Creating a New Production:**
1. Click "Create New Production" button
2. Fill in the form:
   - **Title** (required): Production name
   - **Production Type**: Feature, Series, Commercial, etc.
   - **Budget**: Total production budget
   - **Jurisdiction**: Select from dropdown
   - **Status**: Current production status
   - **Start Date**: Filming start date
   - **Production Company**: Company name
3. Click "Create Production"
4. Production appears in the list

**Editing a Production:**
1. Click "Edit" button on a production
2. Update any fields
3. Click "Save Changes"
4. Changes reflect immediately

**Deleting a Production:**
1. Click "Delete" button
2. Confirm deletion in the dialog
3. Production is removed from the system

**Tips:**
- Use filters to find specific productions
- Sort by date, budget, or status
- Productions can be edited multiple times

### **Jurisdictions Browser**

Explore all available tax incentive jurisdictions worldwide.

**Accessing Jurisdictions:**
- Click "Jurisdictions" in the navbar
- Or navigate to `/jurisdictions`

**Viewing Jurisdictions:**
- See all 32+ jurisdictions in a grid layout
- Each jurisdiction card shows:
  - Name (e.g., "California", "British Columbia")
  - Country (e.g., "USA", "Canada")
  - Type (State, Country, Province)
  - Code (e.g., "CA", "BC")

**Filtering Jurisdictions:**
1. Use the type filter dropdown
2. Select "All", "State", "Country", or "Province"
3. Grid updates to show matching jurisdictions

**Viewing Jurisdiction Details:**
1. Click on a jurisdiction card
2. See detailed information:
   - Full name and code
   - Country and type
   - Available incentive programs
   - Minimum budget requirements
   - Tax credit percentages
   - Eligibility requirements

**Search and Sort:**
- Search by jurisdiction name
- Filter by country
- Sort alphabetically
- Filter by incentive type

### **Tax Incentive Calculator**

Calculate potential tax incentives for your productions.

**Accessing Calculator:**
- Click "Calculator" in the navbar
- Or navigate to `/calculator`

**Calculating Tax Incentives:**

1. **Select Production**
   - Choose from dropdown of your productions
   - Or create a new production first

2. **Select Jurisdiction**
   - Choose jurisdiction from dropdown
   - See all 32+ available jurisdictions
   - Filter by country or type

3. **Calculate**
   - Click "Calculate Incentive" button
   - Results appear instantly

4. **View Results**
   - Total tax credit amount
   - Effective percentage
   - Breakdown by category
   - Eligibility status
   - Requirements checklist

**Understanding Results:**

**Tax Credit Breakdown:**
- **Base Credit**: Primary incentive percentage
- **Bonus Credits**: Additional stackable credits
- **Total Credit**: Combined incentive amount
- **Effective Rate**: Total percentage of budget

**Eligibility Requirements:**
- ✅ Green checkmark: Requirement met
- ❌ Red X: Requirement not met
- View detailed requirements list
- See what's needed to qualify

**Comparing Jurisdictions:**
1. Calculate for multiple jurisdictions
2. View side-by-side comparison
3. See savings differences
4. Choose best option

**Tips:**
- Calculate early in pre-production
- Compare multiple jurisdictions
- Consider stackable bonuses
- Review all requirements carefully
- Save calculations for reference

### **Navigation**

**Navbar:**
- **PilotForge Logo**: Return to dashboard
- **Dashboard**: Main overview page
- **Productions**: Manage productions
- **Jurisdictions**: Browse jurisdictions
- **Calculator**: Calculate incentives

**Keyboard Shortcuts** (Coming Soon):
- `Alt + D`: Go to Dashboard
- `Alt + P`: Go to Productions
- `Alt + J`: Go to Jurisdictions
- `Alt + C`: Go to Calculator

### **Common Workflows**

#### **New Production Analysis:**
1. Create production in Productions page
2. Navigate to Calculator
3. Select your production
4. Calculate for multiple jurisdictions
5. Compare results
6. Choose best jurisdiction

#### **Jurisdiction Research:**
1. Browse Jurisdictions page
2. Filter by type or country
3. View jurisdiction details
4. Check incentive programs
5. Note minimum requirements

#### **Production Management:**
1. View all productions
2. Edit production details
3. Update status as filming progresses
4. Track budget changes
5. Re-calculate incentives if needed

### **Troubleshooting**

**Issue: Productions not loading**
- Check that backend API is running
- Verify network connection
- Refresh the page (Ctrl+R / Cmd+R)

**Issue: Calculator not working**
- Ensure production is selected
- Ensure jurisdiction is selected
- Check console for errors (F12)

**Issue: Data not updating**
- Try refreshing the page
- Clear browser cache
- Check API connection

**Issue: Cannot create production**
- Fill in all required fields
- Check budget is a valid number
- Verify jurisdiction is selected

---

## 🔐 Authentication

**Current Version:** No authentication required  
**Future Versions:** Will support API keys and OAuth2

---

## 🧮 Calculator API

### **Simple Calculator**

Calculate tax credit for a single production in one jurisdiction.

**Endpoint:** `POST /api/v1/calculate/simple`

**Request Body:**
```json
{
  "budget": 5000000,
  "jurisdictionId": "bfae464b-9551-4aad-b5e7-2abcf687134e",
  "ruleId": "california-film-credit-2025"
}
```

**Response:**
```json
{
  "jurisdiction": "California",
  "ruleName": "CA Film & TV Tax Credit 3.0",
  "ruleCode": "CA-FTC-2025",
  "incentiveType": "tax_credit",
  "percentage": 20.0,
  "estimatedCredit": 1000000,
  "meetsMinimum": true,
  "minimumRequired": 1000000,
  "underMaximum": true,
  "maximumCap": 25000000,
  "requirements": {
    "minSpend": "Minimum $1,000,000 qualified spend",
    "californiaResidents": "75% of principal photography days in CA",
    "applicationRequired": "Must apply before principal photography"
  }
}
```

---

### **Multi-Jurisdiction Comparison**

Compare tax incentives across multiple jurisdictions.

**Endpoint:** `POST /api/v1/calculate/compare`

**Request Body:**
```json
{
  "budget": 5000000,
  "jurisdictionIds": [
    "california-id",
    "georgia-id",
    "louisiana-id",
    "new-york-id"
  ]
}
```

**Response:**
```json
{
  "comparisons": [
    {
      "rank": 1,
      "jurisdiction": "Louisiana",
      "jurisdictionId": "louisiana-id",
      "ruleName": "Louisiana Motion Picture Tax Credit",
      "ruleCode": "LA-MPTC-2025",
      "incentiveType": "tax_credit",
      "percentage": 25.0,
      "estimatedCredit": 1250000
    },
    {
      "rank": 2,
      "jurisdiction": "Georgia",
      "jurisdictionId": "georgia-id",
      "ruleName": "Georgia Film Tax Credit",
      "ruleCode": "GA-FTC-2025",
      "incentiveType": "tax_credit",
      "percentage": 30.0,
      "estimatedCredit": 1500000
    }
  ],
  "bestOption": {
    "jurisdiction": "Georgia",
    "estimatedCredit": 1500000,
    "percentage": 30.0
  },
  "worstOption": {
    "jurisdiction": "California",
    "estimatedCredit": 1000000
  },
  "savings": 500000,
  "recommendation": "Film in Georgia to save $500,000 vs lowest option"
}
```

---

### **Compliance Verification**

Verify if a production meets all requirements for a specific incentive program.

**Endpoint:** `POST /api/v1/calculate/compliance`

**Request Body:**
```json
{
  "productionBudget": 5000000,
  "ruleId": "california-film-credit-2025",
  "shootDays": 45,
  "localHirePercentage": 80,
  "hasPromoLogo": true,
  "hasCulturalTest": false,
  "productionType": "feature"
}
```

**Response:**
```json
{
  "overallStatus": "compliant",
  "estimatedCredit": 1000000,
  "requirementsMet": 4,
  "requirementsNotMet": 0,
  "requirements": [
    {
      "requirement": "minimum_spend",
      "status": "met",
      "description": "Minimum spend of $1,000,000",
      "value": 5000000,
      "required": 1000000
    },
    {
      "requirement": "shoot_days",
      "status": "met",
      "description": "Minimum 10 shoot days in jurisdiction",
      "value": 45,
      "required": 10
    },
    {
      "requirement": "local_hiring",
      "status": "met",
      "description": "75% California residents",
      "value": 80,
      "required": 75
    },
    {
      "requirement": "promotional_logo",
      "status": "met",
      "description": "Include CA logo in credits",
      "value": true
    }
  ],
  "nextSteps": [
    "Submit application to California Film Commission",
    "Provide proof of California residency for crew",
    "Include promotional materials in deliverables"
  ]
}
```

---

### **Stackable Credits Calculator**

Calculate base credit plus all applicable bonus programs.

**Endpoint:** `POST /api/v1/calculate/stackable`

**Request Body:**
```json
{
  "budget": 5000000,
  "ruleId": "louisiana-stackable-2025",
  "qualifyingPayroll": 2000000,
  "additionalQualifications": {
    "payrollBonus": true,
    "visualEffects": false
  }
}
```

**Response:**
```json
{
  "totalCredit": 1750000,
  "effectiveRate": 35.0,
  "breakdown": [
    {
      "component": "base",
      "name": "Louisiana Base Credit",
      "percentage": 25.0,
      "amount": 1250000
    },
    {
      "component": "bonus",
      "name": "Louisiana Payroll Credit",
      "percentage": 10.0,
      "qualifyingAmount": 2000000,
      "amount": 500000
    }
  ],
  "stackingDetails": {
    "baseCredit": 1250000,
    "bonusCredits": 500000,
    "totalCredits": 1750000
  },
  "recommendations": [
    "Maximize Louisiana payroll to qualify for full bonus",
    "Consider VFX credit by adding $100K in VFX spend"
  ]
}
```

---

### **Date-Based Rule Selection**

Check which incentive programs are active on a specific production date.

**Endpoint:** `POST /api/v1/calculate/date-based`

**Request Body:**
```json
{
  "jurisdictionId": "california-id",
  "productionDate": "2026-06-01"
}
```

**Response:**
```json
{
  "jurisdiction": "California",
  "queryDate": "2026-06-01",
  "activeRules": [
    {
      "ruleName": "CA Film & TV Tax Credit 3.0",
      "ruleCode": "CA-FTC-2025",
      "percentage": 20.0,
      "effectiveDate": "2025-01-01",
      "expirationDate": "2030-12-31",
      "status": "active"
    },
    {
      "ruleName": "CA Independent Film Credit",
      "ruleCode": "CA-IFC-2025",
      "percentage": 25.0,
      "effectiveDate": "2025-07-01",
      "expirationDate": null,
      "status": "active"
    }
  ],
  "expiredRules": [],
  "upcomingRules": []
}
```

---

### **Scenario Modeling**

Model multiple "what if" budget scenarios to find optimal approach.

**Endpoint:** `POST /api/v1/calculate/scenario`

**Request Body:**
```json
{
  "baseProductionBudget": 5000000,
  "jurisdictionId": "california-id",
  "scenarios": [
    {
      "name": "Conservative Budget",
      "budget": 4000000,
      "shootDays": 30
    },
    {
      "name": "Base Budget",
      "budget": 5000000,
      "shootDays": 45
    },
    {
      "name": "Premium Budget",
      "budget": 7500000,
      "shootDays": 60
    }
  ]
}
```

**Response:**
```json
{
  "scenarios": [
    {
      "scenarioName": "Premium Budget",
      "scenarioParams": {
        "budget": 7500000,
        "shootDays": 60
      },
      "bestRuleName": "CA Film & TV Tax Credit 3.0",
      "estimatedCredit": 1875000,
      "effectiveRate": 25.0,
      "rank": 1
    },
    {
      "scenarioName": "Base Budget",
      "scenarioParams": {
        "budget": 5000000,
        "shootDays": 45
      },
      "bestRuleName": "CA Film & TV Tax Credit 3.0",
      "estimatedCredit": 1250000,
      "effectiveRate": 25.0,
      "rank": 2
    },
    {
      "scenarioName": "Conservative Budget",
      "scenarioParams": {
        "budget": 4000000,
        "shootDays": 30
      },
      "bestRuleName": "CA Film & TV Tax Credit 3.0",
      "estimatedCredit": 1000000,
      "effectiveRate": 25.0,
      "rank": 3
    }
  ],
  "bestScenario": {
    "name": "Premium Budget",
    "credit": 1875000
  },
  "optimizationPotential": 875000,
  "recommendation": "Premium Budget yields $875K more than Conservative"
}
```

---

## 📄 Reports API

Generate professional PDF reports.

### **Comparison Report**

**Endpoint:** `POST /api/v1/reports/comparison`

**Request Body:**
```json
{
  "productionTitle": "Awesome Feature Film",
  "budget": 5000000,
  "jurisdictionIds": [
    "california-id",
    "georgia-id"
  ]
}
```

**Response:** Downloads PDF file
```
comparison_report_20260110_143052.pdf
```

**Report Contents:**
- Executive summary with best option
- Detailed comparison table
- Savings analysis
- Recommendations

---

### **Compliance Report**

**Endpoint:** `POST /api/v1/reports/compliance`

**Request Body:**
```json
{
  "productionTitle": "Awesome Feature Film",
  "ruleId": "california-film-credit-2025",
  "productionBudget": 5000000,
  "shootDays": 45,
  "localHirePercentage": 80,
  "hasPromoLogo": true
}
```

**Response:** Downloads PDF file
```
compliance_report_20260110_143052.pdf
```

**Report Contents:**
- Compliance status (Pass/Fail)
- Requirements checklist
- Estimated credit if compliant
- Action items

---

### **Scenario Analysis Report**

**Endpoint:** `POST /api/v1/reports/scenario`

**Request Body:**
```json
{
  "productionTitle": "Awesome Feature Film",
  "jurisdictionId": "california-id",
  "baseProductionBudget": 5000000,
  "scenarios": [
    {"name": "Conservative", "budget": 4000000},
    {"name": "Base", "budget": 5000000},
    {"name": "Premium", "budget": 7500000}
  ]
}
```

**Response:** Downloads PDF file
```
scenario_report_20260110_143052.pdf
```

**Report Contents:**
- Scenario comparison table
- ROI analysis
- Optimization recommendations
- Best scenario highlighted

---

## 📊 Excel Export API

Generate professional Excel workbooks with multiple sheets.

### **Comparison Workbook**

**Endpoint:** `POST /api/v1/excel/comparison`

**Request Body:** Same as comparison report

**Response:** Downloads Excel file
```
comparison_20260110_143052.xlsx
```

**Workbook Contents:**
- **Summary Sheet**: Production info, best recommendation
- **Jurisdictions Sheet**: Detailed comparison table
- **Savings Analysis Sheet**: ROI calculations

---

### **Compliance Workbook**

**Endpoint:** `POST /api/v1/excel/compliance`

**Request Body:** Same as compliance report

**Response:** Downloads Excel file
```
compliance_20260110_143052.xlsx
```

**Workbook Contents:**
- Compliance status
- Requirements checklist with color coding
- Estimated credit calculation

---

### **Scenario Workbook**

**Endpoint:** `POST /api/v1/excel/scenario`

**Request Body:** Same as scenario report

**Response:** Downloads Excel file
```
scenario_20260110_143052.xlsx
```

**Workbook Contents:**
- **Scenario Analysis Sheet**: Comparison table
- **ROI Analysis Sheet**: Optimization calculations

---

## 🗄️ Data Management APIs

### **Jurisdictions**

#### List All Jurisdictions
```http
GET /api/v1/jurisdictions/
```

**Query Parameters:**
- `country` (optional): Filter by country
- `active` (optional): Filter by active status

**Response:**
```json
{
  "total": 32,
  "jurisdictions": [
    {
      "id": "california-id",
      "name": "California",
      "code": "CA",
      "country": "USA",
      "type": "state",
      "active": true
    }
  ]
}
```

#### Get Single Jurisdiction
```http
GET /api/v1/jurisdictions/{id}
```

#### Create Jurisdiction
```http
POST /api/v1/jurisdictions/
```

#### Update Jurisdiction
```http
PUT /api/v1/jurisdictions/{id}
```

#### Delete Jurisdiction
```http
DELETE /api/v1/jurisdictions/{id}
```

---

### **Incentive Rules**

#### List All Rules
```http
GET /api/v1/incentive-rules/
```

**Query Parameters:**
- `jurisdiction_id` (optional): Filter by jurisdiction
- `active` (optional): Filter by active status
- `incentive_type` (optional): Filter by type

**Response:**
```json
{
  "total": 33,
  "rules": [
    {
      "id": "rule-id",
      "jurisdictionId": "california-id",
      "ruleName": "CA Film & TV Tax Credit 3.0",
      "ruleCode": "CA-FTC-2025",
      "incentiveType": "tax_credit",
      "percentage": 20.0,
      "minSpend": 1000000,
      "maxCredit": 25000000,
      "active": true
    }
  ]
}
```

#### Get Single Rule
```http
GET /api/v1/incentive-rules/{id}
```

#### Create Rule
```http
POST /api/v1/incentive-rules/
```

#### Update Rule
```http
PUT /api/v1/incentive-rules/{id}
```

#### Delete Rule
```http
DELETE /api/v1/incentive-rules/{id}
```

---

### **Productions**

#### List All Productions
```http
GET /api/v1/productions/
```

**Query Parameters:**
- `status` (optional): Filter by status
- `jurisdiction_id` (optional): Filter by jurisdiction

**Response:**
```json
{
  "total": 5,
  "productions": [
    {
      "id": "production-id",
      "title": "Awesome Feature Film",
      "productionType": "feature",
      "jurisdictionId": "california-id",
      "budgetTotal": 5000000,
      "status": "production",
      "startDate": "2026-06-01"
    }
  ]
}
```

#### Get Single Production
```http
GET /api/v1/productions/{id}
```

#### Create Production
```http
POST /api/v1/productions/
```

#### Update Production
```http
PUT /api/v1/productions/{id}
```

#### Delete Production
```http
DELETE /api/v1/productions/{id}
```

---

## 📋 Response Formats

### **Success Response**
```json
{
  "status": "success",
  "data": { ... }
}
```

### **Error Response**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "budget"],
      "msg": "Budget must be greater than 0",
      "input": -1000
    }
  ]
}
```

---

## ⚠️ Error Handling

### **HTTP Status Codes**

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 204 | No Content | Delete successful |
| 400 | Bad Request | Invalid input |
| 404 | Not Found | Resource not found |
| 422 | Validation Error | Input validation failed |
| 500 | Server Error | Internal server error |

### **Common Errors**

**Budget must be positive:**
```json
{
  "detail": "Budget must be greater than 0"
}
```

**Jurisdiction not found:**
```json
{
  "detail": "Jurisdiction with ID xyz not found"
}
```

**Insufficient jurisdictions for comparison:**
```json
{
  "detail": "Comparison requires at least 2 jurisdictions"
}
```

---

## 🚦 Rate Limits

**Current Version:** No rate limiting  
**Production:** 100 requests per minute per IP

---

## ✅ Best Practices

### **1. Always Validate Input**
```javascript
// Good
if (budget > 0 && jurisdictionIds.length >= 2) {
  await callAPI();
}

// Bad
await callAPI();  // No validation
```

### **2. Handle Errors Gracefully**
```javascript
try {
  const response = await fetch(url, options);
  const data = await response.json();
} catch (error) {
  console.error('API Error:', error);
  // Show user-friendly message
}
```

### **3. Use Appropriate Endpoints**
- Use `/calculate/simple` for single calculations
- Use `/calculate/compare` when comparing 2+ locations
- Use `/reports/*` for professional documents
- Use `/excel/*` for data analysis

### **4. Cache Results**
```javascript
// Cache jurisdiction list
const jurisdictions = await getJurisdictions();
localStorage.setItem('jurisdictions', JSON.stringify(jurisdictions));
```

### **5. Request Only What You Need**
```javascript
// Good: Filter server-side
GET /api/v1/jurisdictions/?country=USA

// Bad: Filter client-side
GET /api/v1/jurisdictions/  // Returns all 32
```

---

## 🎨 Frontend UI Guide

### **Overview**

The PilotForge React frontend provides an intuitive interface for managing productions, browsing jurisdictions, and calculating tax incentives.

**Access:** http://localhost:3000 (development) or your deployed URL

---

### **Dashboard Page**

**Route:** `/`

**Features:**
- **Production Metrics**: View total productions and recent activity
- **Jurisdiction Count**: See number of available jurisdictions
- **Quick Actions**: Create new production or calculate incentives
- **Jurisdiction Grid**: Browse top jurisdictions at a glance

**What You'll See:**
```
┌─────────────────────────────────────────┐
│  Dashboard                               │
├─────────────────────────────────────────┤
│  📊 Productions: 12    🌍 Jurisdictions: 32 │
│                                          │
│  [New Production]  [Calculate Incentive] │
│                                          │
│  Recent Jurisdictions:                   │
│  ┌──────┐ ┌──────┐ ┌──────┐             │
│  │ CA   │ │ GA   │ │ LA   │             │
│  │ USA  │ │ USA  │ │ USA  │             │
│  └──────┘ └──────┘ └──────┘             │
└─────────────────────────────────────────┘
```

**Usage:**
1. View production and jurisdiction counts at the top
2. Click **"New Production"** to create a production
3. Click **"Calculate Incentive"** to go to the calculator
4. Browse jurisdiction cards to see available locations

---

### **Productions Page**

**Route:** `/productions`

**Features:**
- **Production List**: View all productions in a grid
- **Create Production**: Form with validation
- **Production Details**: Title, type, budget, dates, jurisdiction
- **Status Tracking**: Pre-production, production, post-production, completed

**Creating a Production:**

1. Click **"Create New Production"** button
2. Fill out the form:
   - **Title**: Production name (e.g., "My Feature Film")
   - **Type**: Feature, TV Series, Documentary, Commercial
   - **Budget**: Total production budget
   - **Jurisdiction**: Select from dropdown
   - **Start Date**: Production start date
   - **End Date**: Production end date (optional)
   - **Status**: Current production phase

3. Click **"Save Production"**
4. Production appears in the list

**Form Validation:**
- Title is required
- Budget must be a positive number
- Start date must be a valid date
- Jurisdiction must be selected

**Example Form:**
```
┌──────────────────────────────────────┐
│  Create New Production                │
├──────────────────────────────────────┤
│  Title: ___________________________  │
│                                       │
│  Type: [Feature ▼]                   │
│                                       │
│  Budget: $________                   │
│                                       │
│  Jurisdiction: [California ▼]        │
│                                       │
│  Start Date: [2026-06-01]            │
│                                       │
│  End Date: [2026-09-30]              │
│                                       │
│  Status: [Production ▼]              │
│                                       │
│  [Cancel]  [Save Production]         │
└──────────────────────────────────────┘
```

**Viewing Productions:**

Productions are displayed as cards showing:
- Title in bold
- Production type badge
- Budget amount
- Start date
- Jurisdiction name

---

### **Jurisdictions Page**

**Route:** `/jurisdictions`

**Features:**
- **Jurisdiction Grid**: All 32 jurisdictions displayed as cards
- **Type Badges**: Visual indicators for state/province/country/territory
- **Country Grouping**: Jurisdictions organized by country
- **Quick Reference**: See key information at a glance

**What You'll See:**

```
┌─────────────────────────────────────────┐
│  Jurisdictions (32)                      │
├─────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐│
│  │California│ │ Georgia  │ │Louisiana ││
│  │   CA     │ │    GA    │ │   LA     ││
│  │  [State] │ │  [State] │ │ [State]  ││
│  │   USA    │ │   USA    │ │   USA    ││
│  └──────────┘ └──────────┘ └──────────┘│
│                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐│
│  │  Ontario │ │  B.C.    │ │ Quebec   ││
│  │   ON     │ │    BC    │ │   QC     ││
│  │[Province]│ │[Province]│ │[Province]││
│  │  Canada  │ │  Canada  │ │  Canada  ││
│  └──────────┘ └──────────┘ └──────────┘│
└─────────────────────────────────────────┘
```

**Badge Colors:**
- **Blue**: State
- **Green**: Province
- **Purple**: Country
- **Yellow**: Territory

**Usage:**
1. Browse all available jurisdictions
2. See jurisdiction code (e.g., CA, GA, ON)
3. Identify jurisdiction type (state, province, etc.)
4. Note country for international jurisdictions

---

### **Calculator Page**

**Route:** `/calculator`

**Features:**
- **Production Selection**: Choose from your productions
- **Jurisdiction Selection**: Select location for calculation
- **Instant Calculation**: Click to calculate tax incentive
- **Results Display**: View estimated credits and details

**Step-by-Step Usage:**

**Step 1: Select Production**
```
Production: [My Feature Film ▼]
```
Choose from your saved productions or the dropdown will show "No productions available" if none exist.

**Step 2: Select Jurisdiction**
```
Jurisdiction: [California ▼]
```
Choose the location where you want to film.

**Step 3: Calculate**
```
[Calculate Tax Incentive]
```
Click the button to run the calculation.

**Step 4: View Results**
```
┌──────────────────────────────────────┐
│  Calculation Results                  │
├──────────────────────────────────────┤
│  🎬 Production: My Feature Film       │
│  📍 Jurisdiction: California          │
│  💰 Budget: $5,000,000               │
│                                       │
│  ✅ Estimated Tax Credit:            │
│     $1,000,000                       │
│                                       │
│  📊 Rate: 20%                        │
│  📋 Program: CA Film & TV Credit 3.0 │
│                                       │
│  Requirements:                        │
│  ✓ Minimum spend met                 │
│  ✓ Under maximum cap                 │
└──────────────────────────────────────┘
```

**What the Results Show:**
- Production name and budget
- Jurisdiction and program name
- **Estimated Tax Credit** (most important!)
- Effective rate (percentage)
- Compliance status (requirements met/not met)

---

### **Navigation**

**Navbar:**

The top navigation bar provides access to all pages:

```
┌────────────────────────────────────────┐
│ 🎬 PilotForge  [Dashboard] [Productions]│
│               [Jurisdictions] [Calculator]│
└────────────────────────────────────────┘
```

**Active Route Highlighting:**
- Current page is highlighted with blue text and bold font
- Other pages are gray
- Hover effect shows interactivity

**Keyboard Navigation:**
- Tab through navigation links
- Enter to activate
- Accessible for screen readers

---

### **Loading States**

When data is being fetched, you'll see:

```
┌──────────────────────────────────────┐
│           ⚪ Loading...               │
└──────────────────────────────────────┘
```

**Spinner appears when:**
- Loading productions on Dashboard/Productions page
- Loading jurisdictions on Jurisdictions page
- Performing calculations on Calculator page

---

### **Error Handling**

**No Data Available:**
```
No productions found. Create your first production!
```

**API Connection Error:**
```
Failed to load data. Please check your connection.
```

**Form Validation Errors:**
```
⚠️ Title is required
⚠️ Budget must be greater than 0
```

---

### **Mobile Responsive Design**

The UI adapts to different screen sizes:

**Desktop (1200px+):**
- 3-column grid for jurisdictions
- Side-by-side layout for forms
- Full navigation bar

**Tablet (768px - 1199px):**
- 2-column grid
- Stacked form fields
- Compact navigation

**Mobile (< 768px):**
- Single column layout
- Full-width cards
- Hamburger menu (if implemented)

---

### **Tips for Best Experience**

1. **Start with Dashboard**: Get an overview before diving into specific pages
2. **Create Productions First**: Calculator requires existing productions
3. **Use Calculator for Quick Estimates**: Fast way to compare locations
4. **Check All Jurisdictions**: Don't miss better incentive opportunities
5. **Note Compliance Requirements**: Some jurisdictions have specific rules

---

## 📞 Support

- **Documentation Issues**: Open GitHub issue
- **API Questions**: Check [API_EXAMPLES.md](./API_EXAMPLES.md)
- **Bug Reports**: Include request/response details
- **Testing & QA**: See [END_TO_END_TESTING_PROCESS.md](./END_TO_END_TESTING_PROCESS.md)

---

## 🔄 Changelog

### **v1.0.0 (Current)**
- Initial release
- 32 jurisdictions
- 33 incentive programs
- 6 calculator endpoints
- PDF & Excel reports
- Full CRUD operations

---

**Last Updated:** January 10, 2026