# Tax Incentive Compliance Platform — API Reference

> **Base URL:** `http://127.0.0.1:8080`
> **OpenAPI Version:** 3.1.0
> **API Version:** 1.0.0
> **Interactive Docs:** [Swagger UI](/docs) | [ReDoc](/redoc)

---

## Table of Contents

1. [Meta & Health](#1-meta--health) (3 endpoints)
2. [Jurisdictions](#2-jurisdictions) (5 endpoints)
3. [Incentive Rules](#3-incentive-rules) (3 endpoints)
4. [Productions](#4-productions) (5 endpoints)
5. [Expenses](#5-expenses) (6 endpoints)
6. [Calculator](#6-calculator) (7 endpoints)
7. [Reports (PDF)](#7-reports-pdf) (3 endpoints)
8. [Excel Exports](#8-excel-exports) (3 endpoints)
9. [Rule Engine](#9-rule-engine) (1 endpoint)
10. [Monitoring](#10-monitoring) (5 endpoints)
11. [AI Strategic Advisor](#11-ai-strategic-advisor) (1 endpoint)
12. [Schemas Reference](#12-schemas-reference)
13. [Error Handling](#13-error-handling)

---

## 1. Meta & Health

### 1.1 Root

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/` |
| **Description** | Application root endpoint |

**Response `200`**
```json
{
  "message": "Tax Incentive Compliance Platform API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### 1.2 API Root

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/` |
| **Tags** | `Meta` |
| **Description** | API root endpoint (under /api/v1/) |

**Response `200`**
```json
{
  "message": "Tax Incentive Compliance Platform API v1",
  "endpoints": { ... }
}
```

---

### 1.3 Health Check

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/health` |
| **Description** | Returns service health status including database connectivity |

**Response `200`**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-02-08T12:00:00Z"
}
```

---

## 2. Jurisdictions

Manage geographic jurisdictions (states, provinces, countries) that offer film/TV production tax incentives.

### 2.1 Get All Jurisdictions

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/jurisdictions/` |
| **Tags** | `Jurisdictions` |
| **Description** | Retrieve all jurisdictions with optional filtering |

**Query Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country` | `string` | No | Filter by country (e.g., USA, Canada). Case-insensitive. |
| `type` | `string` | No | Filter by type: `state`, `province`, `country`. Case-insensitive. |
| `active` | `boolean` | No | Filter by active status |

**Response `200`** — [JurisdictionList](#jurisdictionlist)
```json
{
  "total": 5,
  "jurisdictions": [
    {
      "id": "uuid",
      "name": "California",
      "code": "CA",
      "country": "USA",
      "type": "state",
      "description": "California Film & TV Tax Credit Program",
      "website": "https://film.ca.gov",
      "active": true,
      "createdAt": "2026-01-15T10:00:00Z",
      "updatedAt": "2026-01-15T10:00:00Z"
    }
  ]
}
```

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 2.2 Create Jurisdiction

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/jurisdictions/` |
| **Tags** | `Jurisdictions` |
| **Description** | Create a new jurisdiction. Code must be unique. |

**Request Body** — [JurisdictionCreate](#jurisdictioncreate) *(required)*
```json
{
  "name": "California",
  "code": "CA",
  "country": "USA",
  "type": "state",
  "description": "California Film & TV Tax Credit Program",
  "website": "https://film.ca.gov",
  "active": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | **Yes** | Full name of the jurisdiction |
| `code` | `string` | **Yes** | Short code (e.g., CA, NY, BC). Must be unique. |
| `country` | `string` | **Yes** | Country name (e.g., USA, Canada) |
| `type` | `string` | **Yes** | Type: `state`, `province`, or `country` |
| `description` | `string \| null` | No | Description of jurisdiction |
| `website` | `string \| null` | No | Official website URL |
| `active` | `boolean` | No | Whether jurisdiction is active (default: `true`) |

**Response `201`** — [JurisdictionResponse](#jurisdictionresponse)

**Response `400`** — Jurisdiction with given code already exists

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 2.3 Get Jurisdiction by ID

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/jurisdictions/{jurisdiction_id}` |
| **Tags** | `Jurisdictions` |
| **Description** | Retrieve a specific jurisdiction by ID |

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jurisdiction_id` | `string` | **Yes** | UUID of the jurisdiction |

**Response `200`** — [JurisdictionResponse](#jurisdictionresponse)

**Response `404`** — Jurisdiction not found

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 2.4 Update Jurisdiction

| | |
|---|---|
| **Method** | `PUT` |
| **Path** | `/api/v1/jurisdictions/{jurisdiction_id}` |
| **Tags** | `Jurisdictions` |
| **Description** | Update an existing jurisdiction. Only provided fields will be updated. |

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jurisdiction_id` | `string` | **Yes** | UUID of the jurisdiction |

**Request Body** — [JurisdictionUpdate](#jurisdictionupdate) *(required)*
```json
{
  "name": "California",
  "description": "Updated description",
  "website": "https://film.ca.gov/tax-credit"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string \| null` | No | Jurisdiction name |
| `code` | `string \| null` | No | Jurisdiction code |
| `country` | `string \| null` | No | Country |
| `type` | `string \| null` | No | Type |
| `description` | `string \| null` | No | Description |
| `website` | `string \| null` | No | Website URL |
| `active` | `boolean \| null` | No | Active status |

**Response `200`** — [JurisdictionResponse](#jurisdictionresponse)

**Response `404`** — Jurisdiction not found

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 2.5 Delete Jurisdiction

| | |
|---|---|
| **Method** | `DELETE` |
| **Path** | `/api/v1/jurisdictions/{jurisdiction_id}` |
| **Tags** | `Jurisdictions` |
| **Description** | Delete a jurisdiction |

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jurisdiction_id` | `string` | **Yes** | UUID of the jurisdiction |

**Response `204`** — Successfully deleted (no content)

**Response `404`** — Jurisdiction not found

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

## 3. Incentive Rules

Manage tax incentive rules associated with jurisdictions, including percentage rates, spend thresholds, and eligibility criteria.

### 3.1 Get All Incentive Rules

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/incentive-rules/` |
| **Tags** | `Incentive Rules` |
| **Description** | Retrieve all incentive rules with optional filtering and pagination |

**Query Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `jurisdiction_id` | `string` | No | — | Filter by jurisdiction UUID |
| `incentive_type` | `string` | No | — | Filter by type: `tax_credit`, `rebate`, `grant`, `exemption` |
| `active` | `boolean` | No | — | Filter by active status |
| `page` | `integer` | No | `1` | Page number (min: 1) |
| `page_size` | `integer` | No | `50` | Items per page (min: 1, max: 100) |

**Response `200`** — [IncentiveRuleList](#incentiverulelist)
```json
{
  "total": 12,
  "page": 1,
  "pageSize": 50,
  "totalPages": 1,
  "rules": [
    {
      "id": "uuid",
      "jurisdictionId": "uuid",
      "ruleName": "California Film Tax Credit 4.0",
      "ruleCode": "CA-FTC-4.0",
      "incentiveType": "tax_credit",
      "percentage": 25.0,
      "fixedAmount": null,
      "minSpend": 1000000,
      "maxCredit": null,
      "eligibleExpenses": ["labor", "equipment", "locations"],
      "excludedExpenses": ["insurance", "financing"],
      "effectiveDate": "2025-07-01T00:00:00Z",
      "expirationDate": null,
      "requirements": { "minShootDays": 5, "localHirePercent": 50 },
      "active": true,
      "createdAt": "2026-01-15T10:00:00Z",
      "updatedAt": "2026-01-15T10:00:00Z"
    }
  ]
}
```

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 3.2 Create Incentive Rule

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/incentive-rules/` |
| **Tags** | `Incentive Rules` |
| **Description** | Create a new incentive rule |

**Request Body** — [IncentiveRuleCreate](#incentiverulecreate) *(required)*
```json
{
  "jurisdictionId": "uuid",
  "ruleName": "California Film Tax Credit 4.0",
  "ruleCode": "CA-FTC-4.0",
  "incentiveType": "tax_credit",
  "percentage": 25.0,
  "fixedAmount": null,
  "minSpend": 1000000,
  "maxCredit": null,
  "eligibleExpenses": ["labor", "equipment", "locations"],
  "excludedExpenses": ["insurance"],
  "effectiveDate": "2025-07-01T00:00:00Z",
  "expirationDate": null,
  "requirements": { "minShootDays": 5 },
  "active": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `jurisdictionId` | `string` | **Yes** | Jurisdiction UUID this rule belongs to |
| `ruleName` | `string` | **Yes** | Name of the incentive rule |
| `ruleCode` | `string` | **Yes** | Internal reference code (unique) |
| `incentiveType` | `string` | **Yes** | Type: `tax_credit`, `rebate`, `grant`, `exemption` |
| `percentage` | `number \| null` | No | Percentage rate (e.g., 25.0 for 25%) |
| `fixedAmount` | `number \| null` | No | Fixed amount incentive |
| `minSpend` | `number \| null` | No | Minimum spend required |
| `maxCredit` | `number \| null` | No | Maximum credit cap |
| `eligibleExpenses` | `string[]` | No | Eligible expense categories |
| `excludedExpenses` | `string[]` | No | Excluded expense categories |
| `effectiveDate` | `datetime` | **Yes** | When rule becomes effective |
| `expirationDate` | `datetime \| null` | No | When rule expires |
| `requirements` | `object` | No | Additional requirements (JSON) |
| `active` | `boolean` | No | Whether rule is active (default: `true`) |

**Response `201`** — [IncentiveRuleResponse](#incentiveruleresponse)

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 3.3 Get Incentive Rule by ID

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/incentive-rules/{rule_id}` |
| **Tags** | `Incentive Rules` |
| **Description** | Retrieve a specific incentive rule by ID |

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `rule_id` | `string` | **Yes** | UUID of the incentive rule |

**Response `200`** — [IncentiveRuleResponse](#incentiveruleresponse)

**Response `404`** — Rule not found

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

## 4. Productions

Manage film and TV productions, including budget tracking, status management, and jurisdiction assignment.

### 4.1 Get All Productions

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/productions/` |
| **Tags** | `Productions` |
| **Description** | Retrieve all productions with optional filtering |

**Query Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `production_type` | `string` | No | Filter by type: `feature`, `tv_series`, `commercial`, `documentary` |
| `active` | `boolean` | No | Filter by active status |

**Response `200`** — [ProductionList](#productionlist)
```json
{
  "total": 3,
  "productions": [
    {
      "id": "uuid",
      "title": "Sunset Boulevard Redux",
      "productionType": "feature",
      "jurisdictionId": "uuid",
      "budgetTotal": 5000000,
      "budgetQualifying": 3500000,
      "startDate": "2026-03-01T00:00:00Z",
      "endDate": "2026-08-15T00:00:00Z",
      "productionCompany": "Silver Screen Studios",
      "status": "pre_production",
      "createdAt": "2026-01-20T10:00:00Z",
      "updatedAt": "2026-01-20T10:00:00Z"
    }
  ]
}
```

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 4.2 Create Production

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/productions/` |
| **Tags** | `Productions` |
| **Description** | Create a new production with all required fields |

**Request Body** — [ProductionCreate](#productioncreate) *(required)*
```json
{
  "title": "Sunset Boulevard Redux",
  "productionType": "feature",
  "jurisdictionId": "uuid",
  "budgetTotal": 5000000,
  "budgetQualifying": 3500000,
  "startDate": "2026-03-01",
  "endDate": "2026-08-15",
  "productionCompany": "Silver Screen Studios",
  "status": "planning"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | **Yes** | Production title |
| `productionType` | `string` | **Yes** | Type: `feature`, `tv_series`, `commercial`, `documentary` |
| `jurisdictionId` | `string` | **Yes** | Jurisdiction UUID |
| `budgetTotal` | `number` | **Yes** | Total production budget in USD |
| `budgetQualifying` | `number \| null` | No | Qualifying budget for incentives |
| `startDate` | `date` | **Yes** | Production start date (YYYY-MM-DD) |
| `endDate` | `date \| null` | No | Production end date |
| `productionCompany` | `string` | **Yes** | Production company name |
| `status` | `string` | **Yes** | Status: `planning`, `pre_production`, `production`, `post_production`, `completed` |

**Response `201`** — [ProductionResponse](#productionresponse)

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 4.3 Quick Create Production

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/productions/quick` |
| **Tags** | `Productions` |
| **Description** | Quick create a production with minimal required fields. Auto-fills defaults. |

**Request Body** — [ProductionQuickCreate](#productionquickcreate) *(required)*
```json
{
  "title": "Quick Test Production",
  "budget": 2000000
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `title` | `string` | **Yes** | — | Production title |
| `budget` | `number` | **Yes** | — | Total budget in USD |
| `jurisdictionId` | `string \| null` | No | First available | Jurisdiction UUID |
| `productionType` | `string \| null` | No | `"feature"` | Production type |
| `productionCompany` | `string \| null` | No | `"TBD"` | Company name |
| `startDate` | `date \| null` | No | Today | Start date |
| `status` | `string \| null` | No | `"planning"` | Status |

**Response `201`** — [ProductionResponse](#productionresponse)

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 4.4 Get Production by ID

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/productions/{production_id}` |
| **Tags** | `Productions` |
| **Description** | Retrieve a specific production by ID |

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `production_id` | `string` | **Yes** | UUID of the production |

**Response `200`** — [ProductionResponse](#productionresponse)

**Response `404`** — Production not found

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 4.5 Update Production

| | |
|---|---|
| **Method** | `PUT` |
| **Path** | `/api/v1/productions/{production_id}` |
| **Tags** | `Productions` |
| **Description** | Update an existing production. Only provided fields will be updated. |

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `production_id` | `string` | **Yes** | UUID of the production |

**Request Body** — [ProductionUpdate](#productionupdate) *(required)*
```json
{
  "status": "production",
  "budgetTotal": 5500000
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string \| null` | No | Production title |
| `productionType` | `string \| null` | No | Production type |
| `jurisdictionId` | `string \| null` | No | Jurisdiction UUID |
| `budgetTotal` | `number \| null` | No | Total budget |
| `budgetQualifying` | `number \| null` | No | Qualifying budget |
| `startDate` | `date \| null` | No | Start date |
| `endDate` | `date \| null` | No | End date |
| `productionCompany` | `string \| null` | No | Company name |
| `status` | `string \| null` | No | Status |

**Response `200`** — [ProductionResponse](#productionresponse)

**Response `404`** — Production not found

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 4.6 Delete Production

| | |
|---|---|
| **Method** | `DELETE` |
| **Path** | `/api/v1/productions/{production_id}` |
| **Tags** | `Productions` |
| **Description** | Delete a production |

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `production_id` | `string` | **Yes** | UUID of the production |

**Response `204`** — Successfully deleted (no content)

**Response `404`** — Production not found

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

## 5. Expenses

Track and manage production expenses, categorize qualifying vs. non-qualifying spend, and calculate real-time tax credits from actual expense data.

### 5.1 Get All Expenses

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/expenses/` |
| **Tags** | `Expenses` |
| **Description** | Retrieve all expenses with optional filtering |

**Query Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `production_id` | `string` | No | Filter by production UUID |
| `category` | `string` | No | Filter by category (e.g., `labor`, `equipment`, `locations`) |
| `is_qualifying` | `boolean` | No | Filter by qualifying status |

**Response `200`** — [ExpenseList](#expenselist)
```json
{
  "total": 25,
  "totalAmount": 1250000,
  "qualifyingAmount": 1050000,
  "nonQualifyingAmount": 200000,
  "expenses": [
    {
      "id": "uuid",
      "productionId": "uuid",
      "category": "labor",
      "subcategory": "crew",
      "description": "Principal photography crew wages",
      "amount": 85000,
      "expenseDate": "2026-04-15",
      "paymentDate": "2026-04-30",
      "isQualifying": true,
      "qualifyingNote": null,
      "vendorName": "Local Crew Inc.",
      "vendorLocation": "Los Angeles, CA",
      "receiptNumber": "REC-2026-001",
      "invoiceNumber": "INV-4521",
      "createdAt": "2026-04-16T10:00:00Z",
      "updatedAt": "2026-04-16T10:00:00Z"
    }
  ]
}
```

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 5.2 Create Expense

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/expenses/` |
| **Tags** | `Expenses` |
| **Description** | Create a new production expense |

**Request Body** — [ExpenseCreate](#expensecreate) *(required)*
```json
{
  "productionId": "uuid",
  "category": "labor",
  "subcategory": "crew",
  "description": "Principal photography crew wages",
  "amount": 85000,
  "expenseDate": "2026-04-15",
  "paymentDate": "2026-04-30",
  "isQualifying": true,
  "vendorName": "Local Crew Inc.",
  "vendorLocation": "Los Angeles, CA",
  "receiptNumber": "REC-2026-001",
  "invoiceNumber": "INV-4521"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `productionId` | `string` | **Yes** | Production UUID |
| `category` | `string` | **Yes** | Category: `labor`, `equipment`, `locations`, `post_production`, etc. |
| `subcategory` | `string \| null` | No | Subcategory |
| `description` | `string` | **Yes** | Expense description |
| `amount` | `number` | **Yes** | Amount in USD (must be > 0) |
| `expenseDate` | `date` | **Yes** | Date expense incurred (YYYY-MM-DD) |
| `paymentDate` | `date \| null` | No | Date payment made |
| `isQualifying` | `boolean` | No | Whether expense qualifies for incentive (default: `true`) |
| `qualifyingNote` | `string \| null` | No | Note about qualifying status |
| `vendorName` | `string \| null` | No | Vendor/payee name |
| `vendorLocation` | `string \| null` | No | Vendor location |
| `receiptNumber` | `string \| null` | No | Receipt number |
| `invoiceNumber` | `string \| null` | No | Invoice number |

**Response `201`** — [ExpenseResponse](#expenseresponse)

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 5.3 Get Expense by ID

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/expenses/{expense_id}` |
| **Tags** | `Expenses` |
| **Description** | Retrieve a specific expense by ID |

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `expense_id` | `string` | **Yes** | UUID of the expense |

**Response `200`** — [ExpenseResponse](#expenseresponse)

**Response `404`** — Expense not found

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 5.4 Update Expense

| | |
|---|---|
| **Method** | `PUT` |
| **Path** | `/api/v1/expenses/{expense_id}` |
| **Tags** | `Expenses` |
| **Description** | Update an existing expense. Only provided fields will be updated. |

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `expense_id` | `string` | **Yes** | UUID of the expense |

**Request Body** — [ExpenseUpdate](#expenseupdate) *(required)*
```json
{
  "amount": 90000,
  "isQualifying": false,
  "qualifyingNote": "Vendor not in qualifying zone"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `category` | `string \| null` | No | Category |
| `subcategory` | `string \| null` | No | Subcategory |
| `description` | `string \| null` | No | Description |
| `amount` | `number \| null` | No | Amount (must be > 0) |
| `expenseDate` | `date \| null` | No | Expense date |
| `paymentDate` | `date \| null` | No | Payment date |
| `isQualifying` | `boolean \| null` | No | Qualifying status |
| `qualifyingNote` | `string \| null` | No | Qualifying note |
| `vendorName` | `string \| null` | No | Vendor name |
| `vendorLocation` | `string \| null` | No | Vendor location |
| `receiptNumber` | `string \| null` | No | Receipt number |
| `invoiceNumber` | `string \| null` | No | Invoice number |

**Response `200`** — [ExpenseResponse](#expenseresponse)

**Response `404`** — Expense not found

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 5.5 Delete Expense

| | |
|---|---|
| **Method** | `DELETE` |
| **Path** | `/api/v1/expenses/{expense_id}` |
| **Tags** | `Expenses` |
| **Description** | Delete an expense |

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `expense_id` | `string` | **Yes** | UUID of the expense |

**Response `204`** — Successfully deleted (no content)

**Response `404`** — Expense not found

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 5.6 Calculate Credit from Actual Expenses

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/expenses/production/{production_id}/calculate` |
| **Tags** | `Expenses` |
| **Description** | Calculate tax credit based on actual production expenses. This is the real-time calculator that updates as expenses are added. |

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `production_id` | `string` | **Yes** | UUID of the production |

**Response `200`** — [ProductionExpenseCalculation](#productionexpensecalculation)
```json
{
  "productionId": "uuid",
  "productionTitle": "Sunset Boulevard Redux",
  "jurisdictionName": "California",
  "totalExpenses": 1250000,
  "qualifyingExpenses": 1050000,
  "nonQualifyingExpenses": 200000,
  "qualifyingPercentage": 84.0,
  "bestRuleName": "California Film Tax Credit 4.0",
  "bestRuleCode": "CA-FTC-4.0",
  "ruleId": "uuid",
  "appliedRate": 25.0,
  "estimatedCredit": 262500,
  "meetsMinimum": true,
  "minimumRequired": 1000000,
  "underMaximum": true,
  "maximumCap": null,
  "expensesByCategory": [
    {
      "category": "labor",
      "totalAmount": 800000,
      "qualifyingAmount": 750000,
      "nonQualifyingAmount": 50000,
      "count": 15
    }
  ],
  "totalExpensesCount": 25,
  "notes": ["Qualifying expenses meet minimum spend requirement"],
  "recommendations": ["Consider adding more local crew hires to maximize credit"]
}
```

**Response `404`** — Production not found

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

## 6. Calculator

Estimate tax credits, compare jurisdictions, check compliance, model scenarios, and analyze date-based rule availability.

### 6.1 Simple Tax Credit Calculation

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/calculate/simple` |
| **Tags** | `Calculator` |
| **Description** | Calculate estimated tax credit for a production using a specific incentive rule |

**Request Body** — [SimpleCalculateRequest](#simplecalculaterequest) *(required)*
```json
{
  "productionBudget": 5000000,
  "jurisdictionId": "uuid",
  "ruleId": "uuid",
  "qualifyingBudget": 3500000
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `productionBudget` | `number` | **Yes** | Total production budget in USD (must be > 0) |
| `jurisdictionId` | `string` | **Yes** | Jurisdiction UUID |
| `ruleId` | `string` | **Yes** | Incentive rule UUID to apply |
| `qualifyingBudget` | `number \| null` | No | Override qualifying budget |

**Response `200`** — [SimpleCalculateResponse](#simplecalculateresponse)
```json
{
  "jurisdiction": "California",
  "ruleName": "California Film Tax Credit 4.0",
  "ruleCode": "CA-FTC-4.0",
  "incentiveType": "tax_credit",
  "totalBudget": 5000000,
  "qualifyingBudget": 3500000,
  "percentage": 25.0,
  "estimatedCredit": 875000,
  "meetsMinimumSpend": true,
  "minimumSpendRequired": 1000000,
  "underMaximumCap": true,
  "maximumCapAmount": null,
  "requirements": { "minShootDays": 5 },
  "notes": ["Credit calculated at 25% of qualifying budget"]
}
```

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 6.2 Compare Tax Credits Across Jurisdictions

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/calculate/compare` |
| **Tags** | `Calculator` |
| **Description** | Compare estimated tax credits across multiple jurisdictions. Returns ranked comparison with best recommendation. |

**Request Body** — [CompareCalculateRequest](#comparecalculaterequest) *(required)*
```json
{
  "productionBudget": 5000000,
  "jurisdictionIds": ["uuid-1", "uuid-2", "uuid-3"],
  "qualifyingBudget": 3500000
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `productionBudget` | `number` | **Yes** | Total budget (must be > 0) |
| `jurisdictionIds` | `string[]` | **Yes** | List of 2–10 jurisdiction UUIDs to compare |
| `qualifyingBudget` | `number \| null` | No | Override qualifying budget |

**Response `200`** — [CompareCalculateResponse](#comparecalculateresponse)
```json
{
  "totalBudget": 5000000,
  "comparisons": [
    {
      "jurisdiction": "Illinois",
      "jurisdictionId": "uuid",
      "ruleName": "Illinois Film Tax Credit",
      "ruleCode": "IL-FTC",
      "incentiveType": "tax_credit",
      "percentage": 30.0,
      "estimatedCredit": 1050000,
      "meetsRequirements": true,
      "rank": 1,
      "savings": 175000
    }
  ],
  "bestOption": { ... },
  "savingsVsWorst": 350000,
  "notes": ["Illinois offers the highest credit at 30%"]
}
```

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 6.3 Get Jurisdiction Rules with Budget Estimate

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/calculate/jurisdiction/{jurisdiction_id}` |
| **Tags** | `Calculator` |
| **Description** | Get all available incentive rules for a jurisdiction with estimated credits for a given budget |

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jurisdiction_id` | `string` | **Yes** | UUID of the jurisdiction |

**Query Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `budget` | `number` | **Yes** | Production budget for estimates |

**Response `200`** — JSON object with jurisdiction details and rule estimates

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 6.4 Check Compliance

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/calculate/compliance` |
| **Tags** | `Calculator` |
| **Description** | Verify if a production meets all requirements for a specific incentive rule. Checks minimum spend, shoot days, local hiring percentages, and special requirements. |

**Request Body** — [ComplianceCheckRequest](#compliancecheckrequest) *(required)*
```json
{
  "productionId": "uuid",
  "ruleId": "uuid",
  "productionBudget": 5000000,
  "qualifyingBudget": 3500000,
  "shootDays": 30,
  "crewSize": 50,
  "localHirePercentage": 65.0,
  "hasPromoLogo": true,
  "hasCulturalTest": false,
  "isRelocating": false,
  "additionalInfo": {}
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `productionId` | `string \| null` | No | Production UUID (if checking existing) |
| `ruleId` | `string` | **Yes** | Incentive rule UUID |
| `productionBudget` | `number \| null` | No | Total budget (must be > 0) |
| `qualifyingBudget` | `number \| null` | No | Qualifying budget |
| `shootDays` | `integer \| null` | No | Number of shoot days |
| `crewSize` | `integer \| null` | No | Total crew size |
| `localHirePercentage` | `number \| null` | No | Percentage of local hires |
| `hasPromoLogo` | `boolean \| null` | No | Has promotional logo in credits |
| `hasCulturalTest` | `boolean \| null` | No | Passed cultural test |
| `isRelocating` | `boolean \| null` | No | Is relocating production |
| `additionalInfo` | `object \| null` | No | Additional compliance info |

**Response `200`** — [ComplianceCheckResponse](#compliancecheckresponse)
```json
{
  "overallCompliance": "partial",
  "jurisdiction": "California",
  "ruleName": "California Film Tax Credit 4.0",
  "ruleCode": "CA-FTC-4.0",
  "totalRequirements": 5,
  "requirementsMet": 3,
  "requirementsNotMet": 1,
  "requirementsUnknown": 1,
  "requirements": [
    {
      "requirement": "Minimum Spend",
      "description": "Minimum $1,000,000 in qualifying spend",
      "status": "met",
      "required": true,
      "userValue": 3500000,
      "requiredValue": 1000000,
      "notes": null
    }
  ],
  "estimatedCredit": 875000,
  "actionItems": ["Increase local hire percentage to 70%"],
  "warnings": ["Cultural test requirement not verified"],
  "nextSteps": ["Submit application with documentation"]
}
```

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 6.5 Get Date-Based Rules

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/calculate/date-based` |
| **Tags** | `Calculator` |
| **Description** | Get all incentive rules available for a specific production date. Useful for planning productions in advance and checking rule changes. |

**Request Body** — [DateBasedRulesRequest](#datebasedrulesrequest) *(required)*
```json
{
  "jurisdictionId": "uuid",
  "productionDate": "2026-06-15",
  "includeExpired": false
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `jurisdictionId` | `string` | **Yes** | — | Jurisdiction UUID |
| `productionDate` | `date` | **Yes** | — | Date to check (YYYY-MM-DD) |
| `includeExpired` | `boolean` | No | `false` | Include expired rules |

**Response `200`** — [DateBasedRulesResponse](#datebasedrulesresponse)
```json
{
  "jurisdiction": "California",
  "queryDate": "2026-06-15",
  "activeRules": [ { ... } ],
  "upcomingRules": [ { ... } ],
  "expiredRules": [],
  "totalActive": 2,
  "totalUpcoming": 1,
  "totalExpired": 0,
  "notes": ["New rule effective July 2026"]
}
```

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 6.6 Model Multiple Scenarios

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/calculate/scenario` |
| **Tags** | `Calculator` |
| **Description** | Model multiple "what if" scenarios for production planning. Compare different budgets, dates, hiring percentages, and more. |

**Request Body** — [ScenarioCalculateRequest](#scenariocalculaterequest) *(required)*
```json
{
  "productionBudget": 5000000,
  "jurisdictionId": "uuid",
  "productionStartDate": "2026-06-01",
  "productionEndDate": "2026-12-01",
  "scenarios": [
    { "name": "Base Budget", "budget": 5000000 },
    { "name": "Increased Budget", "budget": 7000000 },
    { "name": "Reduced Budget", "budget": 3000000 }
  ],
  "qualifyingBudget": null,
  "includeExpiredRules": false
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `productionBudget` | `number` | **Yes** | — | Total budget (must be > 0) |
| `jurisdictionId` | `string` | **Yes** | — | Jurisdiction UUID |
| `productionStartDate` | `date \| null` | No | — | Start date |
| `productionEndDate` | `date \| null` | No | — | End date |
| `scenarios` | `object[]` | No | — | Scenario parameters to model |
| `qualifyingBudget` | `number \| null` | No | — | Qualifying budget |
| `includeExpiredRules` | `boolean` | No | `false` | Include expired rules |

**Response `200`** — [ScenarioCalculateResponse](#scenariocalculateresponse)
```json
{
  "jurisdiction": "California",
  "baseProductionBudget": 5000000,
  "productionDate": "2026-06-01",
  "scenarios": [
    {
      "scenarioName": "Base Budget",
      "scenarioParams": { "budget": 5000000 },
      "bestRuleName": "California Film Tax Credit 4.0",
      "bestRuleCode": "CA-FTC-4.0",
      "ruleId": "uuid",
      "estimatedCredit": 1250000,
      "effectiveRate": 25.0,
      "meetsRequirements": true,
      "isActive": true,
      "isExpired": false,
      "effectiveDate": "2025-07-01",
      "expirationDate": null,
      "notes": []
    }
  ],
  "bestScenario": { ... },
  "worstScenario": { ... },
  "savingsDifference": 500000,
  "recommendations": ["Increasing budget to $7M yields proportionally higher credit"],
  "availableRules": 2,
  "expiredRules": 0
}
```

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 6.7 Get Calculator Options

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/calculate/options` |
| **Tags** | `Calculator` |
| **Description** | Get available options for calculator scenarios. Returns lists of available types and statuses formatted for dropdowns. |

**Response `200`**
```json
{
  "productionTypes": ["feature", "tv_series", "commercial", "documentary"],
  "statuses": ["planning", "pre_production", "production", "post_production", "completed"],
  "incentiveTypes": ["tax_credit", "rebate", "grant", "exemption"]
}
```

---

## 7. Reports (PDF)

Generate professional PDF reports for jurisdiction comparisons, compliance verification, and scenario analysis.

### 7.1 Generate Comparison PDF Report

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/reports/comparison` |
| **Tags** | `Reports` |
| **Description** | Generate a professional 4-page PDF comparing tax incentives across jurisdictions |
| **Response Type** | `application/pdf` (file download) |

**Request Body** — [GenerateComparisonReportRequest](#generatecomparisonreportrequest) *(required)*
```json
{
  "productionTitle": "Sunset Boulevard Redux",
  "budget": 5000000,
  "jurisdictionIds": ["uuid-1", "uuid-2", "uuid-3"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `productionTitle` | `string` | **Yes** | Production title for the report |
| `budget` | `number` | **Yes** | Production budget (must be > 0) |
| `jurisdictionIds` | `string[]` | **Yes** | 2–10 jurisdiction UUIDs to compare |

**PDF Contents:**
- Page 1: Executive summary and recommended location
- Page 2: Detailed jurisdiction analysis with program specifics
- Page 3: Requirements & eligibility criteria for each location
- Page 4: Recommendations, action plan, and next steps

**Response `200`** — PDF file download

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 7.2 Generate Compliance PDF Report

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/reports/compliance` |
| **Tags** | `Reports` |
| **Description** | Generate a PDF report verifying production compliance with incentive requirements |
| **Response Type** | `application/pdf` (file download) |

**Request Body** — [GenerateComplianceReportRequest](#generatecompliancereportrequest) *(required)*
```json
{
  "productionTitle": "Sunset Boulevard Redux",
  "ruleId": "uuid",
  "productionBudget": 5000000,
  "shootDays": 30,
  "localHirePercentage": 65.0,
  "hasPromoLogo": true,
  "hasCulturalTest": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `productionTitle` | `string` | **Yes** | Production title |
| `ruleId` | `string` | **Yes** | Incentive rule UUID |
| `productionBudget` | `number` | **Yes** | Budget (must be > 0) |
| `shootDays` | `integer \| null` | No | Shoot days |
| `localHirePercentage` | `number \| null` | No | Local hire % |
| `hasPromoLogo` | `boolean \| null` | No | Has promo logo |
| `hasCulturalTest` | `boolean \| null` | No | Cultural test passed |

**Response `200`** — PDF file download

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 7.3 Generate Scenario PDF Report

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/reports/scenario` |
| **Tags** | `Reports` |
| **Description** | Generate a PDF report analyzing multiple production scenarios |
| **Response Type** | `application/pdf` (file download) |

**Request Body** — [GenerateScenarioReportRequest](#generatescenarioreportrequest) *(required)*
```json
{
  "productionTitle": "Sunset Boulevard Redux",
  "jurisdictionId": "uuid",
  "baseProductionBudget": 5000000,
  "scenarios": [
    { "name": "Low", "budget": 3000000 },
    { "name": "Base", "budget": 5000000 },
    { "name": "High", "budget": 7000000 }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `productionTitle` | `string` | **Yes** | Production title |
| `jurisdictionId` | `string` | **Yes** | Jurisdiction UUID |
| `baseProductionBudget` | `number` | **Yes** | Base budget (must be > 0) |
| `scenarios` | `object[]` | **Yes** | 2+ scenarios to analyze |

**Response `200`** — PDF file download

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

## 8. Excel Exports

Export analysis results to professionally formatted Excel workbooks.

### 8.1 Export Comparison to Excel

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/excel/comparison` |
| **Tags** | `Excel Exports` |
| **Description** | Export jurisdiction comparison to formatted Excel spreadsheet |
| **Response Type** | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |

**Request Body** — [GenerateComparisonReportRequest](#generatecomparisonreportrequest) *(required)*

Same request body as [7.1 Generate Comparison PDF Report](#71-generate-comparison-pdf-report).

**Excel Contents:**
- Summary sheet with best recommendation
- Detailed comparison table
- Savings analysis
- Professional formatting

**Response `200`** — Excel file download

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 8.2 Export Compliance to Excel

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/excel/compliance` |
| **Tags** | `Excel Exports` |
| **Description** | Export compliance verification to formatted Excel spreadsheet |
| **Response Type** | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |

**Request Body** — [GenerateComplianceReportRequest](#generatecompliancereportrequest) *(required)*

Same request body as [7.2 Generate Compliance PDF Report](#72-generate-compliance-pdf-report).

**Excel Contents:**
- Compliance status summary
- Requirements checklist with pass/fail indicators
- Professional formatting

**Response `200`** — Excel file download

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 8.3 Export Scenario to Excel

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/excel/scenario` |
| **Tags** | `Excel Exports` |
| **Description** | Export scenario analysis to formatted Excel spreadsheet |
| **Response Type** | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |

**Request Body** — [GenerateScenarioReportRequest](#generatescenarioreportrequest) *(required)*

Same request body as [7.3 Generate Scenario PDF Report](#73-generate-scenario-pdf-report).

**Excel Contents:**
- Scenario comparison table
- ROI analysis
- Best scenario recommendation
- Professional formatting

**Response `200`** — Excel file download

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

## 9. Rule Engine

Evaluate jurisdiction-specific incentive rules against production data and expenses using the built-in rule engine.

### 9.1 Evaluate Rule Engine

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/rule-engine/evaluate` |
| **Tags** | `rule-engine` |
| **Description** | Evaluate incentive rules for a jurisdiction with optional production context and expense data |

**Query Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `debug` | `boolean` | No | `false` | Include debug trace/meta in response |

**Request Body** — [EvaluateRequest](#evaluaterequest) *(required)*
```json
{
  "jurisdiction_code": "CA",
  "production": {
    "title": "Sunset Boulevard Redux",
    "budget": 5000000
  },
  "expenses": [
    {
      "category": "labor",
      "amount": 250000,
      "description": "Crew wages",
      "is_payroll": true,
      "is_resident": true
    },
    {
      "category": "equipment",
      "amount": 100000,
      "description": "Camera rental",
      "is_payroll": false,
      "is_resident": null
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `jurisdiction_code` | `string` | **Yes** | Jurisdiction code (1–10 chars, e.g., "CA") |
| `production` | `ProductionContext \| null` | No | Production context |
| `production.title` | `string \| null` | No | Title (max 120 chars) |
| `production.budget` | `number \| null` | No | Budget (must be > 0) |
| `expenses` | `ExpenseItem[]` | No | List of expenses to evaluate |
| `expenses[].category` | `string` | **Yes** | Category (1–64 chars) |
| `expenses[].amount` | `number` | **Yes** | Amount (must be > 0) |
| `expenses[].description` | `string \| null` | No | Description (max 240 chars) |
| `expenses[].is_payroll` | `boolean \| null` | No | Whether this is a payroll expense |
| `expenses[].is_resident` | `boolean \| null` | No | Whether vendor/employee is a resident |

**Response `200`** — Rule evaluation results (JSON)

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

## 10. Monitoring

Track changes to tax incentive programs across jurisdictions through configurable monitoring sources and event notifications.

### 10.1 Get Monitoring Events

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/monitoring/events` |
| **Tags** | `Monitoring` |
| **Description** | Retrieve monitoring events with optional filtering and pagination |

**Query Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `jurisdiction_id` | `string` | No | — | Filter by jurisdiction UUID |
| `event_type` | `string` | No | — | Filter: `incentive_change`, `new_program`, `expiration`, `news` |
| `severity` | `string` | No | — | Filter: `info`, `warning`, `critical` |
| `unread_only` | `boolean` | No | `false` | Show only unread events |
| `page` | `integer` | No | `1` | Page number (min: 1) |
| `page_size` | `integer` | No | `10` | Items per page (min: 1, max: 100) |

**Response `200`** — [MonitoringEventList](#monitoringeventlist)
```json
{
  "total": 15,
  "events": [
    {
      "id": "uuid",
      "jurisdictionId": "uuid",
      "eventType": "incentive_change",
      "severity": "warning",
      "title": "California Tax Credit Rate Increase",
      "summary": "CA Film Tax Credit rate increased from 20% to 25% effective July 2026",
      "sourceId": "uuid",
      "sourceUrl": "https://film.ca.gov/updates",
      "detectedAt": "2026-02-01T08:30:00Z",
      "readAt": null,
      "metadata": null,
      "createdAt": "2026-02-01T08:30:00Z",
      "updatedAt": "2026-02-01T08:30:00Z"
    }
  ]
}
```

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 10.2 Get Unread Event Count

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/monitoring/events/unread` |
| **Tags** | `Monitoring` |
| **Description** | Get count of unread monitoring events |

**Query Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jurisdiction_id` | `string` | No | Filter by jurisdiction UUID |

**Response `200`** — [UnreadCountResponse](#unreadcountresponse)
```json
{
  "unreadCount": 3
}
```

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 10.3 Mark Event as Read

| | |
|---|---|
| **Method** | `PATCH` |
| **Path** | `/api/v1/monitoring/events/{event_id}/read` |
| **Tags** | `Monitoring` |
| **Description** | Mark a monitoring event as read |

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `event_id` | `string` | **Yes** | UUID of the event |

**Response `200`** — [MonitoringEventResponse](#monitoringeventresponse)

**Response `404`** — Event not found

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 10.4 Get Monitoring Sources

| | |
|---|---|
| **Method** | `GET` |
| **Path** | `/api/v1/monitoring/sources` |
| **Tags** | `Monitoring` |
| **Description** | Retrieve monitoring sources with optional filtering |

**Query Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jurisdiction_id` | `string` | No | Filter by jurisdiction UUID |
| `source_type` | `string` | No | Filter: `rss`, `api`, `webpage` |
| `active` | `boolean` | No | Filter by active status |

**Response `200`** — [MonitoringSourceList](#monitoringsourcelist)
```json
{
  "total": 8,
  "sources": [
    {
      "id": "uuid",
      "jurisdictionId": "uuid",
      "sourceType": "rss",
      "url": "https://film.ca.gov/feed",
      "checkInterval": 3600,
      "active": true,
      "lastCheckedAt": "2026-02-08T10:00:00Z",
      "lastHash": "abc123...",
      "createdAt": "2026-01-15T10:00:00Z",
      "updatedAt": "2026-02-08T10:00:00Z"
    }
  ]
}
```

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

### 10.5 Create Monitoring Source

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/monitoring/sources` |
| **Tags** | `Monitoring` |
| **Description** | Create a new monitoring source |

**Request Body** — [MonitoringSourceCreate](#monitoringsourcecreate) *(required)*
```json
{
  "jurisdictionId": "uuid",
  "sourceType": "rss",
  "url": "https://film.ca.gov/feed",
  "checkInterval": 3600,
  "active": true
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `jurisdictionId` | `string` | **Yes** | — | Jurisdiction UUID to monitor |
| `sourceType` | `string` | **Yes** | — | Type: `rss`, `api`, `webpage` |
| `url` | `string` | **Yes** | — | URL of the monitoring source |
| `checkInterval` | `integer` | No | `3600` | Check interval in seconds |
| `active` | `boolean` | No | `true` | Whether source is active |

**Response `201`** — [MonitoringSourceResponse](#monitoringsourceresponse)

**Response `422`** — [HTTPValidationError](#httpvalidationerror)

---

## 11. AI Strategic Advisor

### 11.1 Request Recommendation

| | |
|---|---|
| **Method** | `POST` |
| **Path** | `/api/v1/advisor/recommend` |
| **Tags** | `Advisor` |
| **Description** | Generate AI-powered production strategy recommendations. The Anthropic API key is held server-side — it is never exposed to the browser. |

**Request Body** (`application/json`)

```json
{
  "budget": 5000000,
  "production_type": "feature_film",
  "preferred_jurisdictions": ["CA", "GA", "NM"],
  "notes": "Prefer refundable credits"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `budget` | `number` | Yes | Total production budget in USD |
| `production_type` | `string` | No | e.g. `feature_film`, `series`, `commercial` |
| `preferred_jurisdictions` | `string[]` | No | ISO or jurisdiction codes to prioritize |
| `notes` | `string` | No | Free-text context passed to the AI |

**Response `200`**
```json
{
  "recommendations": [
    "Georgia offers a 30% transferable credit with no cap — ideal for this budget.",
    "New Mexico provides a 25–35% refundable credit contingent on 60% in-state spend."
  ]
}
```

**Response `500`** — `ANTHROPIC_API_KEY` not configured or upstream API error

**Response `422`** — Validation error

---

## 12. Schemas Reference

### JurisdictionResponse

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | UUID — Unique identifier |
| `name` | `string` | Jurisdiction name |
| `code` | `string` | Short code (unique) |
| `country` | `string` | Country |
| `type` | `string` | `state` \| `province` \| `country` |
| `description` | `string \| null` | Description |
| `website` | `string \| null` | Official website URL |
| `active` | `boolean` | Active status |
| `createdAt` | `datetime` | Creation timestamp |
| `updatedAt` | `datetime` | Last update timestamp |

### IncentiveRuleResponse

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | UUID |
| `jurisdictionId` | `string` | Parent jurisdiction UUID |
| `ruleName` | `string` | Rule name |
| `ruleCode` | `string` | Unique rule code |
| `incentiveType` | `string` | `tax_credit` \| `rebate` \| `grant` \| `exemption` |
| `percentage` | `number \| null` | Percentage rate |
| `fixedAmount` | `number \| null` | Fixed amount |
| `minSpend` | `number \| null` | Minimum spend required |
| `maxCredit` | `number \| null` | Maximum credit cap |
| `eligibleExpenses` | `string[]` | Eligible expense categories |
| `excludedExpenses` | `string[]` | Excluded expense categories |
| `effectiveDate` | `datetime` | Effective date |
| `expirationDate` | `datetime \| null` | Expiration date |
| `requirements` | `object` | Additional requirements (JSON) |
| `active` | `boolean` | Active status |
| `createdAt` | `datetime` | Creation timestamp |
| `updatedAt` | `datetime` | Last update timestamp |

### ProductionResponse

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | UUID |
| `title` | `string` | Production title |
| `productionType` | `string` | `feature` \| `tv_series` \| `commercial` \| `documentary` |
| `jurisdictionId` | `string` | Jurisdiction UUID |
| `budgetTotal` | `number` | Total budget (USD) |
| `budgetQualifying` | `number \| null` | Qualifying budget |
| `startDate` | `datetime` | Start date |
| `endDate` | `datetime \| null` | End date |
| `productionCompany` | `string` | Company name |
| `status` | `string` | `planning` \| `pre_production` \| `production` \| `post_production` \| `completed` |
| `createdAt` | `datetime` | Creation timestamp |
| `updatedAt` | `datetime` | Last update timestamp |

### ExpenseResponse

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | UUID |
| `productionId` | `string` | Production UUID |
| `category` | `string` | Expense category |
| `subcategory` | `string \| null` | Subcategory |
| `description` | `string` | Description |
| `amount` | `number` | Amount in USD |
| `expenseDate` | `date` | Date incurred |
| `paymentDate` | `date \| null` | Date paid |
| `isQualifying` | `boolean` | Qualifying status |
| `qualifyingNote` | `string \| null` | Qualifying note |
| `vendorName` | `string \| null` | Vendor name |
| `vendorLocation` | `string \| null` | Vendor location |
| `receiptNumber` | `string \| null` | Receipt number |
| `invoiceNumber` | `string \| null` | Invoice number |
| `createdAt` | `datetime` | Creation timestamp |
| `updatedAt` | `datetime` | Last update timestamp |

### MonitoringEventResponse

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | UUID |
| `jurisdictionId` | `string` | Jurisdiction UUID |
| `eventType` | `string` | `incentive_change` \| `new_program` \| `expiration` \| `news` |
| `severity` | `string` | `info` \| `warning` \| `critical` |
| `title` | `string` | Event title |
| `summary` | `string` | Event summary |
| `sourceId` | `string \| null` | Monitoring source UUID |
| `sourceUrl` | `string \| null` | Original source URL |
| `detectedAt` | `datetime` | Detection timestamp |
| `readAt` | `datetime \| null` | Read timestamp |
| `metadata` | `string \| null` | Additional metadata (JSON string) |
| `createdAt` | `datetime` | Creation timestamp |
| `updatedAt` | `datetime` | Last update timestamp |

### MonitoringSourceResponse

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | UUID |
| `jurisdictionId` | `string` | Jurisdiction UUID |
| `sourceType` | `string` | `rss` \| `api` \| `webpage` |
| `url` | `string` | Source URL |
| `checkInterval` | `integer` | Check interval (seconds) |
| `active` | `boolean` | Active status |
| `lastCheckedAt` | `datetime \| null` | Last check timestamp |
| `lastHash` | `string \| null` | Content hash for change detection |
| `createdAt` | `datetime` | Creation timestamp |
| `updatedAt` | `datetime` | Last update timestamp |

### List Wrappers

| Schema | Fields |
|--------|--------|
| **JurisdictionList** | `total: int`, `jurisdictions: JurisdictionResponse[]` |
| **IncentiveRuleList** | `total: int`, `page: int`, `pageSize: int`, `totalPages: int`, `rules: IncentiveRuleResponse[]` |
| **ProductionList** | `total: int`, `productions: ProductionResponse[]` |
| **ExpenseList** | `total: int`, `totalAmount: number`, `qualifyingAmount: number`, `nonQualifyingAmount: number`, `expenses: ExpenseResponse[]` |
| **MonitoringEventList** | `total: int`, `events: MonitoringEventResponse[]` |
| **MonitoringSourceList** | `total: int`, `sources: MonitoringSourceResponse[]` |
| **UnreadCountResponse** | `unreadCount: int` |

---

## 13. Error Handling

### Validation Error (422)

Returned when request parameters or body fail validation.

```json
{
  "detail": [
    {
      "loc": ["body", "productionBudget"],
      "msg": "Input should be greater than 0",
      "type": "greater_than"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `detail` | `ValidationError[]` | List of validation errors |
| `detail[].loc` | `(string \| int)[]` | Location of the error (e.g., `["body", "fieldName"]`) |
| `detail[].msg` | `string` | Human-readable error message |
| `detail[].type` | `string` | Error type identifier |

### Not Found (404)

```json
{
  "detail": "Jurisdiction with ID abc-123 not found"
}
```

### Bad Request (400)

```json
{
  "detail": "Jurisdiction with code 'CA' already exists"
}
```

### Common HTTP Status Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `201` | Created |
| `204` | No Content (successful delete) |
| `400` | Bad Request (business logic error) |
| `404` | Not Found |
| `422` | Validation Error |
| `500` | Internal Server Error |

---

## Endpoint Summary

| # | Method | Path | Tag | Description |
|---|--------|------|-----|-------------|
| 1 | `GET` | `/` | — | Root |
| 2 | `GET` | `/api/v1/` | Meta | API root |
| 3 | `GET` | `/api/v1/health` | — | Health check |
| 4 | `GET` | `/api/v1/jurisdictions/` | Jurisdictions | List all jurisdictions |
| 5 | `POST` | `/api/v1/jurisdictions/` | Jurisdictions | Create jurisdiction |
| 6 | `GET` | `/api/v1/jurisdictions/{id}` | Jurisdictions | Get jurisdiction |
| 7 | `PUT` | `/api/v1/jurisdictions/{id}` | Jurisdictions | Update jurisdiction |
| 8 | `DELETE` | `/api/v1/jurisdictions/{id}` | Jurisdictions | Delete jurisdiction |
| 9 | `GET` | `/api/v1/incentive-rules/` | Incentive Rules | List all rules |
| 10 | `POST` | `/api/v1/incentive-rules/` | Incentive Rules | Create rule |
| 11 | `GET` | `/api/v1/incentive-rules/{id}` | Incentive Rules | Get rule |
| 12 | `GET` | `/api/v1/productions/` | Productions | List all productions |
| 13 | `POST` | `/api/v1/productions/` | Productions | Create production |
| 14 | `POST` | `/api/v1/productions/quick` | Productions | Quick create production |
| 15 | `GET` | `/api/v1/productions/{id}` | Productions | Get production |
| 16 | `PUT` | `/api/v1/productions/{id}` | Productions | Update production |
| 17 | `DELETE` | `/api/v1/productions/{id}` | Productions | Delete production |
| 18 | `GET` | `/api/v1/expenses/` | Expenses | List all expenses |
| 19 | `POST` | `/api/v1/expenses/` | Expenses | Create expense |
| 20 | `GET` | `/api/v1/expenses/{id}` | Expenses | Get expense |
| 21 | `PUT` | `/api/v1/expenses/{id}` | Expenses | Update expense |
| 22 | `DELETE` | `/api/v1/expenses/{id}` | Expenses | Delete expense |
| 23 | `GET` | `/api/v1/expenses/production/{id}/calculate` | Expenses | Calculate from expenses |
| 24 | `POST` | `/api/v1/calculate/simple` | Calculator | Simple calculation |
| 25 | `POST` | `/api/v1/calculate/compare` | Calculator | Compare jurisdictions |
| 26 | `GET` | `/api/v1/calculate/jurisdiction/{id}` | Calculator | Jurisdiction options |
| 27 | `POST` | `/api/v1/calculate/compliance` | Calculator | Compliance check |
| 28 | `POST` | `/api/v1/calculate/date-based` | Calculator | Date-based rules |
| 29 | `POST` | `/api/v1/calculate/scenario` | Calculator | Scenario modeling |
| 30 | `GET` | `/api/v1/calculate/options` | Calculator | Calculator options |
| 31 | `POST` | `/api/v1/reports/comparison` | Reports | Comparison PDF |
| 32 | `POST` | `/api/v1/reports/compliance` | Reports | Compliance PDF |
| 33 | `POST` | `/api/v1/reports/scenario` | Reports | Scenario PDF |
| 34 | `POST` | `/api/v1/excel/comparison` | Excel Exports | Comparison Excel |
| 35 | `POST` | `/api/v1/excel/compliance` | Excel Exports | Compliance Excel |
| 36 | `POST` | `/api/v1/excel/scenario` | Excel Exports | Scenario Excel |
| 37 | `POST` | `/api/v1/rule-engine/evaluate` | Rule Engine | Evaluate rules |
| 38 | `GET` | `/api/v1/monitoring/events` | Monitoring | List events |
| 39 | `GET` | `/api/v1/monitoring/events/unread` | Monitoring | Unread count |
| 40 | `PATCH` | `/api/v1/monitoring/events/{id}/read` | Monitoring | Mark event read |
| 41 | `GET` | `/api/v1/monitoring/sources` | Monitoring | List sources |
| 42 | `POST` | `/api/v1/monitoring/sources` | Monitoring | Create source |

---

*Generated from OpenAPI spec v3.1.0 — Tax Incentive Compliance Platform API v1.0.0*
