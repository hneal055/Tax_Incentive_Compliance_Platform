# Expenses API Documentation

## Overview
The Expenses API provides endpoints for managing production expenses and calculating tax incentives based on actual expense data.

## Endpoints

### 1. List All Expenses
**GET** `/api/v1/expenses/`

Query all production expenses with optional filtering.

**Query Parameters:**
- `production_id` (optional): Filter by production ID
- `category` (optional): Filter by expense category
- `is_qualifying` (optional): Filter by qualifying status (true/false)

**Response:**
```json
{
  "total": 10,
  "totalAmount": 150000.00,
  "qualifyingAmount": 120000.00,
  "nonQualifyingAmount": 30000.00,
  "expenses": [...]
}
```

### 2. Get Expense by ID
**GET** `/api/v1/expenses/{expense_id}`

Retrieve a specific expense by its ID.

**Response:**
```json
{
  "id": "uuid",
  "productionId": "uuid",
  "category": "labor",
  "description": "Crew wages",
  "amount": 50000.00,
  "expenseDate": "2025-01-15",
  "isQualifying": true,
  "createdAt": "2025-01-15T10:00:00Z",
  "updatedAt": "2025-01-15T10:00:00Z"
}
```

### 3. Create Expense
**POST** `/api/v1/expenses/`

Create a new production expense.

**Request Body:**
```json
{
  "productionId": "uuid",
  "category": "labor",
  "subcategory": "crew",
  "description": "Crew wages - Week 1",
  "amount": 50000.00,
  "expenseDate": "2025-01-15",
  "paymentDate": "2025-01-20",
  "isQualifying": true,
  "qualifyingNote": "Meets local hire requirements",
  "vendorName": "Payroll Services Inc",
  "vendorLocation": "Los Angeles, CA",
  "receiptNumber": "RCP-001",
  "invoiceNumber": "INV-001"
}
```

**Validation Rules:**
- `amount` must be greater than 0
- `productionId` must reference an existing production
- `expenseDate` is required
- All other fields are optional

**Response:** Returns the created expense with `id`, `createdAt`, and `updatedAt` fields.

### 4. Update Expense
**PUT** `/api/v1/expenses/{expense_id}`

Update an existing expense. All fields are optional.

**Request Body:**
```json
{
  "amount": 55000.00,
  "description": "Updated description",
  "isQualifying": false
}
```

**Response:** Returns the updated expense.

### 5. Delete Expense
**DELETE** `/api/v1/expenses/{expense_id}`

Delete an expense.

**Response:** 204 No Content on success.

### 6. Calculate Tax Credit from Expenses
**GET** `/api/v1/expenses/production/{production_id}/calculate`

Calculate tax credit based on actual production expenses.

**Response:**
```json
{
  "productionId": "uuid",
  "productionTitle": "Feature Film Title",
  "jurisdictionName": "California",
  "totalExpenses": 5000000.00,
  "qualifyingExpenses": 4500000.00,
  "nonQualifyingExpenses": 500000.00,
  "qualifyingPercentage": 90.0,
  "bestRuleName": "California Film & TV Tax Credit",
  "bestRuleCode": "CA-FTC-2025",
  "ruleId": "uuid",
  "appliedRate": 25.0,
  "estimatedCredit": 1125000.00,
  "meetsMinimum": true,
  "minimumRequired": 1000000.00,
  "underMaximum": true,
  "maximumCap": 10000000.00,
  "expensesByCategory": [
    {
      "category": "labor",
      "totalAmount": 3000000.00,
      "qualifyingAmount": 3000000.00,
      "nonQualifyingAmount": 0,
      "count": 25
    }
  ],
  "totalExpensesCount": 50,
  "notes": [
    "💰 50 expenses totaling $5,000,000",
    "✅ Qualifying: $4,500,000 (90.0%)",
    "📊 Rate: 25.0%",
    "💵 Estimated credit: $1,125,000"
  ],
  "recommendations": [
    "Continue tracking expenses - currently at $1,125,000 credit"
  ]
}
```

## Expense Categories

Common expense categories include:
- `labor` - Cast and crew wages
- `equipment` - Camera, lighting, sound equipment rentals
- `locations` - Location fees and permits
- `post_production` - Editing, VFX, sound post
- `production_services` - Production support services
- `travel` - Travel and accommodation
- `catering` - Food and catering services
- `marketing` - Marketing and advertising (often non-qualifying)
- `distribution` - Distribution costs (often non-qualifying)

## Error Responses

### 400 Bad Request
Production has no expenses.

### 404 Not Found
Expense, production, or jurisdiction not found.

### 422 Validation Error
Invalid data provided (e.g., negative amount, zero amount).

### 500 Internal Server Error
Could not determine applicable rule or database error.

## Testing

Run the test suite:
```bash
pytest tests/test_expenses_api.py -v
```

All 8 model validation tests should pass.
