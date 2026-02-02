# End-to-End Testing Process
**PilotForge - Tax Incentive Intelligence for Film & TV**

**Version:** 1.0  
**Last Updated:** January 13, 2026  
**Status:** Active

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Testing Objectives and Scope](#testing-objectives-and-scope)
3. [Critical Workflows](#critical-workflows)
4. [Test Case Design](#test-case-design)
5. [Testing Tools and Environment](#testing-tools-and-environment)
6. [Test Execution Process](#test-execution-process)
7. [Defect Management](#defect-management)
8. [Roles and Responsibilities](#roles-and-responsibilities)
9. [Metrics and Reporting](#metrics-and-reporting)
10. [Appendix](#appendix)

---

## 🎯 Overview

### Purpose

This document establishes the formal end-to-end (E2E) testing process for the PilotForge Tax Incentive Compliance Platform. It provides a comprehensive framework for validating that all components work together correctly to deliver business value.

### Goals

- Ensure platform reliability and correctness across all user workflows
- Validate integration between API, database, and business logic layers
- Verify compliance calculations meet jurisdictional requirements
- Maintain quality standards throughout the development lifecycle
- Provide clear testing guidelines for all team members

### Scope

**In Scope:**
- API endpoint testing (all CRUD operations)
- Tax incentive calculation engine
- Multi-jurisdiction comparison workflows
- Report generation (PDF, Excel)
- Database operations and data integrity
- Business rule validation
- Compliance verification workflows

**Out of Scope:**
- Infrastructure/deployment testing (covered separately)
- Performance/load testing (separate test suite)
- Security penetration testing (separate process)
- UI/Frontend testing (when implemented)

---

## 🎯 Testing Objectives and Scope

### Primary Objectives

1. **Functional Correctness**
   - All API endpoints return expected responses
   - Tax credit calculations are mathematically accurate
   - Business rules are correctly applied

2. **Data Integrity**
   - Database transactions complete successfully
   - Data relationships are maintained
   - No data corruption during CRUD operations

3. **Integration Validation**
   - All system components work together seamlessly
   - External dependencies function correctly
   - API contracts are honored

4. **Compliance Verification**
   - Jurisdictional rules are correctly implemented
   - Regulatory requirements are met
   - Audit trails are complete

5. **User Workflow Validation**
   - End-to-end business processes complete successfully
   - Error handling works as expected
   - Edge cases are handled gracefully

### Test Coverage Goals

- **Unit Tests:** 80% minimum code coverage
- **Integration Tests:** All critical API endpoints
- **E2E Tests:** All major user workflows
- **Regression Tests:** All previously fixed bugs

---

## 🔄 Critical Workflows

### Business Workflows

#### 1. Jurisdiction Discovery
**Purpose:** Users find available filming jurisdictions for their production

**Steps:**
1. List all available jurisdictions
2. Filter by country (e.g., USA, Canada)
3. Filter by type (state, province, country)
4. View jurisdiction details
5. Access jurisdiction website and contact info

**Success Criteria:**
- All jurisdictions are displayed correctly
- Filters work as expected
- Jurisdiction data is accurate and complete

**Test Priority:** HIGH

---

#### 2. Incentive Rule Comparison
**Purpose:** Compare tax incentives across multiple jurisdictions

**Steps:**
1. Select production parameters (budget, type)
2. Choose 2-10 jurisdictions to compare
3. System calculates incentives for each jurisdiction
4. View side-by-side comparison
5. Identify best incentive opportunity

**Success Criteria:**
- Calculations are accurate for all jurisdictions
- Comparison includes all relevant data points
- Results are ranked correctly

**Test Priority:** HIGH

---

#### 3. Tax Credit Calculation
**Purpose:** Calculate potential tax credit for a specific production

**Steps:**
1. Select jurisdiction
2. Enter production budget
3. Select applicable incentive rule
4. Enter production details (shoot days, local hire %, etc.)
5. System calculates base credit
6. System applies bonuses/uplifts if applicable
7. System applies caps/limits
8. Review detailed calculation breakdown

**Success Criteria:**
- Base calculation is mathematically correct
- All bonuses are correctly applied
- Caps and minimums are enforced
- Calculation matches jurisdictional rules

**Test Priority:** CRITICAL

---

#### 4. Compliance Verification
**Purpose:** Verify production meets incentive requirements

**Steps:**
1. Select incentive rule
2. Enter production details
3. System checks all requirements
4. System identifies compliance gaps
5. System provides recommendations
6. Generate compliance report

**Success Criteria:**
- All requirements are checked
- Pass/fail status is accurate
- Recommendations are actionable
- Report is comprehensive

**Test Priority:** HIGH

---

#### 5. Report Generation
**Purpose:** Generate professional reports for stakeholders

**Steps:**
1. Complete calculation or comparison
2. Select report type (PDF or Excel)
3. System generates formatted report
4. Download report
5. Verify report contents

**Success Criteria:**
- Report is generated without errors
- All data is accurate
- Formatting is professional
- Report is downloadable

**Test Priority:** MEDIUM

---

#### 6. Production Management
**Purpose:** Create and manage production records

**Steps:**
1. Create new production
2. Add production details
3. Link to jurisdiction
4. Track expenses
5. Update production status
6. Archive completed production

**Success Criteria:**
- Production is created successfully
- All fields are saved correctly
- Updates work properly
- Production can be retrieved

**Test Priority:** MEDIUM

---

### Technical Workflows

#### 1. Database Connection Management
**Steps:**
- Application startup
- Prisma connection established
- Database migrations applied
- Connection pooling active
- Graceful shutdown

**Test Priority:** HIGH

---

#### 2. API Request/Response Cycle
**Steps:**
- Client sends HTTP request
- FastAPI routes request to handler
- Handler processes business logic
- Database queries executed
- Response formatted and returned
- CORS headers applied

**Test Priority:** HIGH

---

#### 3. Rule Engine Evaluation
**Steps:**
- Load jurisdiction rules
- Parse rule conditions
- Evaluate production against rules
- Calculate incentive amounts
- Apply bonuses and caps
- Return calculation result

**Test Priority:** CRITICAL

---

#### 4. Multi-Jurisdiction Processing
**Steps:**
- Receive comparison request
- Load rules for all jurisdictions
- Execute calculations in parallel
- Aggregate results
- Rank jurisdictions
- Return comparison data

**Test Priority:** HIGH

---

#### 5. PDF/Excel Generation
**Steps:**
- Receive report request
- Format data for report
- Apply branding/styling
- Generate document
- Stream to client
- Clean up temporary files

**Test Priority:** MEDIUM

---

## 🧪 Test Case Design

### Test Case Structure

Each test case should include:

```
Test Case ID: TC-[Category]-[Number]
Title: [Descriptive name]
Priority: [Critical/High/Medium/Low]
Category: [API/Calculator/Reports/Integration]
Preconditions: [What must be true before test]
Test Steps: [Numbered steps]
Expected Results: [What should happen]
Test Data: [Specific inputs]
Status: [Pass/Fail/Blocked]
```

---

### Test Categories

#### 1. API Endpoint Tests (TC-API-XXX)

##### TC-API-001: List All Jurisdictions
**Priority:** HIGH  
**Preconditions:** Database contains jurisdiction data  
**Steps:**
1. Send GET request to `/api/v1/jurisdictions/`
2. Verify response status is 200
3. Verify response contains `total` field
4. Verify response contains `jurisdictions` array
5. Verify array contains jurisdiction objects

**Expected Results:**
- Status code: 200
- Response time: < 500ms
- Valid JSON structure
- All active jurisdictions returned

**Test Data:** None required

---

##### TC-API-002: Get Jurisdiction by ID
**Priority:** HIGH  
**Preconditions:** At least one jurisdiction exists  
**Steps:**
1. Get valid jurisdiction ID from list endpoint
2. Send GET request to `/api/v1/jurisdictions/{id}`
3. Verify response status is 200
4. Verify returned ID matches request
5. Verify all jurisdiction fields are present

**Expected Results:**
- Status code: 200
- Correct jurisdiction data
- All required fields populated

**Test Data:** Valid jurisdiction UUID

---

##### TC-API-003: Get Invalid Jurisdiction
**Priority:** MEDIUM  
**Preconditions:** None  
**Steps:**
1. Send GET request with non-existent ID
2. Verify response status is 404
3. Verify error message is clear

**Expected Results:**
- Status code: 404
- Error message: "Jurisdiction not found"

**Test Data:** Invalid UUID (e.g., "00000000-0000-0000-0000-000000000000")

---

##### TC-API-004: List Incentive Rules
**Priority:** HIGH  
**Preconditions:** Database contains rule data  
**Steps:**
1. Send GET request to `/api/v1/incentive-rules/`
2. Verify response status is 200
3. Verify response structure
4. Count returned rules

**Expected Results:**
- Status code: 200
- Rules array populated
- Total count accurate

---

##### TC-API-005: Filter Rules by Jurisdiction
**Priority:** HIGH  
**Preconditions:** Multiple jurisdictions with rules exist  
**Steps:**
1. Get valid jurisdiction ID
2. Send GET with `jurisdiction_id` parameter
3. Verify all returned rules match jurisdiction
4. Verify no rules from other jurisdictions

**Expected Results:**
- Only matching rules returned
- Filter works correctly

**Test Data:** Valid jurisdiction ID

---

#### 2. Calculator Tests (TC-CALC-XXX)

##### TC-CALC-001: Basic Percentage Credit
**Priority:** CRITICAL  
**Test Data:**
- Budget: $5,000,000
- Percentage: 25%
- No caps or minimums

**Steps:**
1. Submit calculation request
2. Verify credit = $1,250,000
3. Verify calculation breakdown

**Expected Results:**
- Correct mathematical calculation
- Detailed breakdown provided

---

##### TC-CALC-002: Credit with Maximum Cap
**Priority:** CRITICAL  
**Test Data:**
- Budget: $100,000,000
- Percentage: 25%
- Maximum credit: $10,000,000

**Steps:**
1. Submit calculation request
2. Verify credit = $10,000,000 (capped)
3. Verify cap is noted in response

**Expected Results:**
- Cap is applied correctly
- Uncapped amount shown
- Cap explanation provided

---

##### TC-CALC-003: Below Minimum Spend
**Priority:** HIGH  
**Test Data:**
- Budget: $500,000
- Percentage: 25%
- Minimum spend: $1,000,000

**Steps:**
1. Submit calculation request
2. Verify credit = $0
3. Verify ineligibility reason provided

**Expected Results:**
- No credit awarded
- Clear explanation of minimum requirement

---

##### TC-CALC-004: Stackable Credits
**Priority:** HIGH  
**Test Data:**
- Budget: $5,000,000
- Base percentage: 25%
- Bonus percentage: 10%

**Steps:**
1. Submit calculation request
2. Verify base credit = $1,250,000
3. Verify bonus credit = $500,000
4. Verify total = $1,750,000

**Expected Results:**
- Both credits calculated
- Total is sum of both
- Breakdown shows each component

---

##### TC-CALC-005: Negative Budget Validation
**Priority:** HIGH  
**Test Data:**
- Budget: -$1,000

**Steps:**
1. Submit calculation with negative budget
2. Verify validation error
3. Verify status code 422

**Expected Results:**
- Request rejected
- Clear error message

---

#### 3. Comparison Tests (TC-COMP-XXX)

##### TC-COMP-001: Compare Two Jurisdictions
**Priority:** HIGH  
**Test Data:**
- Budget: $5,000,000
- Jurisdictions: California, Georgia

**Steps:**
1. Submit comparison request
2. Verify calculations for both
3. Verify ranking is correct
4. Verify all data points included

**Expected Results:**
- Both jurisdictions calculated
- Results ranked by incentive amount
- Complete comparison data

---

##### TC-COMP-002: Too Few Jurisdictions
**Priority:** MEDIUM  
**Test Data:**
- Jurisdictions: Only one ID

**Steps:**
1. Submit comparison with 1 jurisdiction
2. Verify validation error
3. Verify status code 422

**Expected Results:**
- Request rejected
- Error: "At least 2 jurisdictions required"

---

##### TC-COMP-003: Too Many Jurisdictions
**Priority:** MEDIUM  
**Test Data:**
- Jurisdictions: 11 jurisdiction IDs

**Steps:**
1. Submit comparison with 11 jurisdictions
2. Verify validation error

**Expected Results:**
- Request rejected
- Error: "Maximum 10 jurisdictions allowed"

---

#### 4. Report Tests (TC-RPT-XXX)

##### TC-RPT-001: Generate PDF Comparison Report
**Priority:** MEDIUM  
**Test Data:**
- Production title: "Test Feature Film"
- Budget: $5,000,000
- Jurisdictions: 3 valid IDs

**Steps:**
1. Submit PDF report request
2. Verify response is PDF file
3. Verify Content-Type header
4. Verify file downloads
5. Verify PDF opens correctly

**Expected Results:**
- PDF generated successfully
- Content-Type: application/pdf
- File is valid PDF format

---

##### TC-RPT-002: Generate Excel Comparison Report
**Priority:** MEDIUM  
**Test Data:**
- Same as TC-RPT-001

**Steps:**
1. Submit Excel report request
2. Verify response is Excel file
3. Verify Content-Type header
4. Verify file downloads
5. Open and verify data

**Expected Results:**
- Excel generated successfully
- Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
- File is valid Excel format
- Data is accurate

---

##### TC-RPT-003: Invalid Report Request
**Priority:** LOW  
**Test Data:**
- Budget: $0

**Steps:**
1. Submit report with invalid data
2. Verify validation error

**Expected Results:**
- Request rejected
- Status code: 422

---

#### 5. Production Management Tests (TC-PROD-XXX)

##### TC-PROD-001: Create Production
**Priority:** MEDIUM  
**Test Data:**
```json
{
  "title": "Test Feature Film",
  "productionType": "feature",
  "jurisdictionId": "{valid-id}",
  "budgetTotal": 5000000,
  "budgetQualifying": 4500000,
  "startDate": "2026-03-01",
  "endDate": "2026-06-30",
  "productionCompany": "Test Productions LLC",
  "status": "pre_production"
}
```

**Steps:**
1. Send POST request to create production
2. Verify status code 201
3. Verify ID is generated
4. Verify all fields saved correctly

**Expected Results:**
- Production created
- Unique ID assigned
- All data persisted

---

##### TC-PROD-002: List Productions
**Priority:** MEDIUM  
**Steps:**
1. Create test production
2. List all productions
3. Verify new production in list

**Expected Results:**
- All productions returned
- New production included

---

##### TC-PROD-003: Update Production
**Priority:** MEDIUM  
**Steps:**
1. Create production
2. Update production status
3. Verify update succeeded
4. Retrieve and verify changes

**Expected Results:**
- Update successful
- Changes persisted

---

#### 6. Integration Tests (TC-INT-XXX)

##### TC-INT-001: Complete User Workflow
**Priority:** CRITICAL  
**Description:** End-to-end test of typical user journey

**Steps:**
1. List jurisdictions
2. Select 3 jurisdictions
3. Compare incentives for $5M production
4. Select best jurisdiction
5. Calculate detailed incentive
6. Check compliance requirements
7. Generate PDF report
8. Create production record

**Expected Results:**
- All steps complete successfully
- Data flows correctly between steps
- No errors encountered

---

##### TC-INT-002: Database Transaction Integrity
**Priority:** HIGH  
**Steps:**
1. Create production with expenses
2. Update production details
3. Add more expenses
4. Verify all data relationships maintained
5. Delete production
6. Verify cascade delete works

**Expected Results:**
- All operations succeed
- Referential integrity maintained
- Cascade deletes work correctly

---

### Edge Cases and Error Scenarios

#### Edge Case Tests

**EC-001: Zero Budget**
- Input: Budget = $0
- Expected: Validation error

**EC-002: Extremely Large Budget**
- Input: Budget = $999,999,999,999
- Expected: Calculate correctly or cap appropriately

**EC-003: Missing Required Fields**
- Input: Request without required fields
- Expected: Validation error with field names

**EC-004: Invalid Date Ranges**
- Input: End date before start date
- Expected: Validation error

**EC-005: Expired Incentive Rule**
- Input: Rule with expiration date in past
- Expected: Rule excluded from calculations or flagged

**EC-006: Concurrent Updates**
- Input: Two simultaneous updates to same production
- Expected: Both succeed or proper locking

**EC-007: Special Characters in Strings**
- Input: Production title with special characters
- Expected: Characters properly escaped/handled

**EC-008: Unicode in Text Fields**
- Input: Non-English characters
- Expected: Proper UTF-8 handling

---

### Happy Path Test Suite

**HP-001: New User First Experience**
1. Access API documentation
2. List jurisdictions
3. Calculate simple incentive
4. Success!

**HP-002: Production Accountant Workflow**
1. Create production
2. Add expenses
3. Calculate incentives
4. Generate compliance report
5. Download Excel for accounting

**HP-003: Location Scout Workflow**
1. Compare 5 jurisdictions
2. Review incentive details
3. Generate comparison PDF
4. Present to producers

---

## 🛠️ Testing Tools and Environment

### Testing Stack

#### Core Testing Framework
- **pytest**: Primary test framework
- **pytest-asyncio**: Async test support
- **pytest-cov**: Code coverage reporting
- **httpx**: Async HTTP client for API testing

#### Current Configuration
```ini
[pytest]
minversion = 8.0
testpaths = tests
addopts = -q --disable-warnings --maxfail=1 --cov=src --cov-report=term-missing
```

#### Additional Tools
- **Pydantic**: Request/response validation
- **FastAPI TestClient**: API endpoint testing
- **Prisma Client**: Database operations

---

### Test Environments

#### 1. Local Development
**Purpose:** Developer unit/integration testing  
**Database:** SQLite or local PostgreSQL  
**API:** Local uvicorn server  
**Usage:** During development

**Setup:**
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Install test dependencies
pip install -r requirements-dev.txt

# Run database migrations
prisma db push

# Start test server
python -m uvicorn src.main:app --reload
```

---

#### 2. CI/CD Testing
**Purpose:** Automated test execution  
**Database:** Test database (isolated)  
**API:** Test instance  
**Usage:** On each commit/PR

**Environment Variables:**
```bash
DATABASE_URL=postgresql://test:test@localhost:5432/test_db
TESTING=true
LOG_LEVEL=DEBUG
```

---

#### 3. Staging/QA
**Purpose:** Pre-production validation  
**Database:** Staging database (production-like data)  
**API:** Staging server  
**Usage:** Before release

**Characteristics:**
- Production-like data volume
- Real jurisdictional rules
- Full report generation
- Performance monitoring

---

### Test Data Management

#### Fixtures
Test fixtures are defined in `tests/conftest.py`:
- `sample_jurisdiction`: Test jurisdiction data
- `sample_incentive_rule`: Test incentive rule
- `sample_production`: Test production data
- `sample_expenses`: Test expense records
- `calculator_test_cases`: Calculator validation data

#### Test Database Seeding
```python
# Create test jurisdictions
jurisdictions = [
    {"name": "California", "code": "CA", "country": "USA"},
    {"name": "Georgia", "code": "GA", "country": "USA"},
    {"name": "New York", "code": "NY", "country": "USA"}
]

# Create test incentive rules
rules = [
    {
        "jurisdiction": "California",
        "percentage": 25.0,
        "minSpend": 1000000,
        "maxCredit": 10000000
    }
]
```

---

### Running Tests

#### Run All Tests
```bash
pytest
```

#### Run Specific Test File
```bash
pytest tests/test_api_endpoints.py
```

#### Run Specific Test Class
```bash
pytest tests/test_api_endpoints.py::TestCalculatorEndpoints
```

#### Run Specific Test
```bash
pytest tests/test_api_endpoints.py::TestCalculatorEndpoints::test_simple_calculate_validation
```

#### Run with Coverage Report
```bash
pytest --cov=src --cov-report=html
```

#### Run in Verbose Mode
```bash
pytest -v
```

#### Run Only Failed Tests
```bash
pytest --lf
```

---

## 🚀 Test Execution Process

### Pre-Execution Checklist

Before running tests, ensure:

- [ ] Virtual environment is activated
- [ ] All dependencies are installed (`pip install -r requirements-dev.txt`)
- [ ] Database is accessible and migrations are applied
- [ ] Test database is seeded with required data
- [ ] Environment variables are set correctly
- [ ] No conflicting processes on test ports

---

### Test Execution Stages

#### Stage 1: Unit Tests
**Duration:** 2-5 minutes  
**Scope:** Individual functions and classes  
**When:** On each code change

```bash
pytest tests/unit/ -v
```

**Pass Criteria:** All tests pass, coverage > 80%

---

#### Stage 2: Integration Tests
**Duration:** 5-10 minutes  
**Scope:** API endpoints, database operations  
**When:** Before committing code

```bash
pytest tests/test_api_endpoints.py tests/test_calculator_logic.py -v
```

**Pass Criteria:** All endpoints return expected responses

---

#### Stage 3: End-to-End Tests
**Duration:** 10-15 minutes  
**Scope:** Complete user workflows  
**When:** Before merging to main

```bash
pytest tests/ -v --cov=src
```

**Pass Criteria:** All workflows complete successfully

---

#### Stage 4: Regression Tests
**Duration:** 5-10 minutes  
**Scope:** Previously fixed bugs  
**When:** Before each release

```bash
pytest -m regression -v
```

**Pass Criteria:** No regressions detected

---

### Continuous Integration

#### GitHub Actions Workflow
```yaml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: pytest --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

---

### Test Execution Schedule

| Test Type | Frequency | Trigger | Duration |
|-----------|-----------|---------|----------|
| Unit | On each save | Developer | < 5 min |
| Integration | On commit | Git commit | < 10 min |
| E2E | On PR | Pull request | < 15 min |
| Regression | Pre-release | Manual | < 10 min |
| Smoke | Post-deploy | Deployment | < 5 min |

---

## 🐛 Defect Management

### Defect Lifecycle

```
New → Assigned → In Progress → Fixed → Testing → Verified → Closed
                                  ↓
                              Reopened (if verification fails)
```

---

### Defect Severity Levels

#### Critical (P0)
**Definition:** System is completely unusable or data corruption occurs  
**Examples:**
- Database connection fails
- All API endpoints return 500 errors
- Calculation returns incorrect results

**SLA:** Fix within 24 hours  
**Notification:** Immediate team notification

---

#### High (P1)
**Definition:** Major feature is broken, significant user impact  
**Examples:**
- Report generation fails
- Comparison endpoint not working
- Compliance check gives wrong results

**SLA:** Fix within 3 business days  
**Notification:** Daily standup

---

#### Medium (P2)
**Definition:** Feature works but with limitations or workarounds  
**Examples:**
- Slow API response times
- Missing validation on edge case
- Minor UI formatting issue

**SLA:** Fix within 1 week  
**Notification:** Weekly review

---

#### Low (P3)
**Definition:** Minor inconvenience, cosmetic issue  
**Examples:**
- Typo in documentation
- Inconsistent error message
- Optional field validation

**SLA:** Fix in next release  
**Notification:** Backlog grooming

---

### Defect Logging Process

#### Required Information

Every defect report must include:

1. **Summary:** One-line description
2. **Description:** Detailed explanation
3. **Steps to Reproduce:**
   ```
   1. Navigate to...
   2. Enter data...
   3. Click...
   4. Observe...
   ```
4. **Expected Result:** What should happen
5. **Actual Result:** What actually happens
6. **Environment:** OS, browser, API version
7. **Test Data:** Input values used
8. **Screenshots/Logs:** If applicable
9. **Severity:** P0/P1/P2/P3
10. **Priority:** Critical/High/Medium/Low

---

### Defect Tracking Template

```markdown
## Defect Report

**ID:** BUG-001  
**Date:** 2026-01-13  
**Reporter:** QA Team  
**Severity:** High (P1)  

### Summary
Tax credit calculation incorrect for California incentive

### Description
When calculating tax credits for California Film & TV Tax Credit, 
the system does not apply the additional 5% uplift for independent films.

### Steps to Reproduce
1. POST /api/v1/calculate/simple
2. Use jurisdictionId: {california-id}
3. Use ruleId: {ca-ftc-rule-id}
4. Set budget: $5,000,000
5. Set productionType: "independent"
6. Review calculation result

### Expected Result
- Base credit: $1,250,000 (25%)
- Independent uplift: $250,000 (5%)
- Total credit: $1,500,000

### Actual Result
- Base credit: $1,250,000 (25%)
- Total credit: $1,250,000
- Uplift not applied

### Environment
- API Version: v1
- Database: PostgreSQL 16
- Test Environment: Local

### Test Data
```json
{
  "budget": 5000000,
  "jurisdictionId": "bfae464b-9551-4aad-b5e7-2abcf687134e",
  "ruleId": "ca-ftc-001",
  "productionType": "independent"
}
```

### Impact
All independent film producers receive incorrect calculations

### Suggested Fix
Check rule_engine/calculator.py line 145 - uplift logic

### Status
Assigned to: @dev-team  
Target Fix: 2026-01-15
```

---

### Defect Resolution Process

#### 1. Triage (QA Lead)
- Review defect report
- Assign severity
- Assign to developer
- Set target fix date

#### 2. Investigation (Developer)
- Reproduce the issue
- Identify root cause
- Estimate fix effort
- Update status

#### 3. Fix (Developer)
- Implement fix
- Write regression test
- Update documentation
- Submit for code review

#### 4. Verification (QA)
- Test the fix
- Run regression suite
- Verify no side effects
- Update defect status

#### 5. Closure
- Confirm fix in production
- Update test cases
- Close defect
- Update metrics

---

### Root Cause Categories

Track defects by root cause:

- **Logic Error:** Incorrect algorithm or business rule
- **Data Issue:** Invalid or missing test data
- **Integration:** Component interaction failure
- **Validation:** Missing or incorrect input validation
- **Performance:** Timeout or slow response
- **Configuration:** Environment or settings issue
- **Documentation:** Unclear specifications
- **Third-Party:** External dependency issue

---

## 👥 Roles and Responsibilities

### QA Lead
**Responsibilities:**
- Own the testing process
- Create and maintain test plans
- Triage defects
- Report test metrics
- Coordinate test execution
- Train team on testing practices

**Activities:**
- Daily: Review new defects
- Weekly: Test metrics review
- Sprint: Test plan updates
- Release: Sign-off on quality

---

### QA Engineers
**Responsibilities:**
- Execute test cases
- Report defects
- Verify fixes
- Maintain test automation
- Update test documentation

**Activities:**
- Write test cases
- Execute manual tests
- Run automated tests
- Log defects with complete information
- Verify defect fixes

---

### Developers
**Responsibilities:**
- Write unit tests
- Fix defects
- Support QA in issue reproduction
- Maintain test coverage

**Activities:**
- Unit test coverage for all new code
- Fix assigned defects within SLA
- Write regression tests for fixes
- Code review for test quality

---

### Product Owner
**Responsibilities:**
- Define acceptance criteria
- Prioritize defects
- Approve test scope
- Sign off on releases

**Activities:**
- Review test plans
- Prioritize defect backlog
- Approve production releases
- Validate business requirements

---

### DevOps Engineer
**Responsibilities:**
- Maintain test environments
- Configure CI/CD pipelines
- Monitor test execution
- Manage test data

**Activities:**
- Keep test environments running
- Update CI/CD configurations
- Provision test databases
- Monitor test infrastructure

---

## 📊 Metrics and Reporting

### Key Metrics

#### 1. Test Coverage
**Definition:** Percentage of code covered by tests  
**Target:** ≥ 80%  
**Measurement:** pytest-cov report

```bash
pytest --cov=src --cov-report=term-missing
```

**Tracking:**
- Overall coverage percentage
- Coverage by module
- Uncovered lines

---

#### 2. Test Pass Rate
**Definition:** Percentage of tests passing  
**Target:** 100% on main branch  
**Calculation:** (Passed Tests / Total Tests) × 100

**Tracking:**
- Daily: CI/CD dashboard
- Weekly: Trend analysis
- Release: Must be 100%

---

#### 3. Defect Density
**Definition:** Defects per 1000 lines of code  
**Target:** < 1.0  
**Calculation:** (Total Defects / KLOC)

**Tracking:**
- By module
- By severity
- Trend over time

---

#### 4. Defect Resolution Time
**Definition:** Average time to fix defects  
**Target:**
- P0: < 24 hours
- P1: < 3 days
- P2: < 7 days
- P3: < 14 days

**Tracking:**
- Mean time to resolution (MTTR)
- By severity level
- By root cause

---

#### 5. Test Execution Time
**Definition:** Time to run test suite  
**Target:** < 15 minutes  
**Tracking:**
- Unit tests: < 5 min
- Integration tests: < 10 min
- Full suite: < 15 min

**Optimization:** Parallelize slow tests

---

#### 6. Regression Defect Rate
**Definition:** Percentage of defects that are regressions  
**Target:** < 5%  
**Calculation:** (Regression Defects / Total Defects) × 100

**Action:** If > 5%, increase regression test coverage

---

### Reporting Cadence

#### Daily Standup Report
**Audience:** Development team  
**Content:**
- Tests run yesterday
- Pass/fail status
- Blocking issues
- Today's plan

**Format:** Verbal update

---

#### Weekly Test Summary
**Audience:** Team + management  
**Content:**
- Total tests executed
- Pass rate
- New defects found
- Defects fixed
- Coverage metrics
- Blockers/risks

**Format:** Email/Slack + Dashboard

**Template:**
```
📊 Weekly Test Summary (Week of Jan 13, 2026)

✅ Tests Executed: 156
✅ Pass Rate: 98.7% (154 passed, 2 failed)
🐛 New Defects: 3 (1 High, 2 Medium)
🔧 Defects Fixed: 5
📈 Code Coverage: 82.4% (+1.2% from last week)
🚨 Blockers: None

Top Issues:
1. PDF report generation timing out for large datasets
2. Missing validation on expense date ranges

Next Week Focus:
- Fix remaining 2 test failures
- Increase coverage to 85%
- Complete comparison workflow tests
```

---

#### Sprint Test Report
**Audience:** Full team + stakeholders  
**Content:**
- Sprint testing summary
- Quality metrics
- Defect trends
- Test coverage changes
- Risks for next sprint

**Format:** Presentation + Document

---

#### Release Quality Report
**Audience:** Management + stakeholders  
**Content:**
- All test results
- Defect summary
- Coverage achieved
- Known issues
- Quality sign-off

**Format:** Formal document

**Template:**
```
🚀 Release Quality Report - v0.2.0

Release Date: January 20, 2026
Test Period: January 6-19, 2026
Sign-off: [QA Lead Name]

📊 Summary
- Total Test Cases: 187
- Tests Executed: 187 (100%)
- Tests Passed: 186 (99.5%)
- Tests Failed: 1 (0.5% - documented below)
- Code Coverage: 83.7%

✅ Test Execution
- Unit Tests: 95 (all passed)
- Integration Tests: 67 (all passed)
- E2E Tests: 25 (24 passed, 1 known issue)

🐛 Defects
- Total Found: 12
- Fixed: 11
- Deferred to v0.2.1: 1 (low priority)
- Open: 0 critical, 0 high

📈 Quality Metrics
- Defect Density: 0.8 per KLOC ✅
- Test Coverage: 83.7% ✅
- Pass Rate: 99.5% ✅

⚠️ Known Issues
1. Excel export occasionally slow for 10+ jurisdictions
   - Severity: Low (P3)
   - Workaround: Available
   - Fix planned: v0.2.1

✅ Quality Sign-Off
All acceptance criteria met. Approved for release.

Signed: [QA Lead]
Date: January 19, 2026
```

---

### Dashboards

#### Real-Time Test Dashboard
**Tool:** GitHub Actions / Jenkins  
**Metrics:**
- Current build status
- Latest test run results
- Coverage trends
- Failed test details

**Access:** Team dashboard (updated on each commit)

---

#### Quality Metrics Dashboard
**Tool:** Custom dashboard or reporting tool  
**Metrics:**
- Coverage over time
- Defect trends
- Test execution trends
- Velocity metrics

**Access:** Team + management  
**Update:** Daily

---

## 📚 Appendix

### A. Test Case Repository

All test cases are stored in:
```
tests/
├── test_api_endpoints.py       # API endpoint tests
├── test_calculator_logic.py    # Calculator tests
├── test_report_generation.py   # Report tests
├── test_engine_entrypoint.py   # Rule engine tests
├── test_registry.py            # Registry tests
├── conftest.py                 # Test fixtures
└── unit/                       # Unit tests
```

---

### B. Common Test Scenarios

#### Scenario 1: New Jurisdiction Added
**Testing Checklist:**
- [ ] Jurisdiction appears in list endpoint
- [ ] Can retrieve by ID
- [ ] Can filter rules by new jurisdiction
- [ ] Calculations work correctly
- [ ] Comparison includes new jurisdiction
- [ ] Reports generate successfully

---

#### Scenario 2: Incentive Rule Updated
**Testing Checklist:**
- [ ] Old calculations remain unchanged (historical)
- [ ] New calculations use updated rule
- [ ] Effective dates are honored
- [ ] Expiration dates work correctly
- [ ] Database migration successful
- [ ] No impact on other jurisdictions

---

#### Scenario 3: API Endpoint Modified
**Testing Checklist:**
- [ ] Request validation still works
- [ ] Response format unchanged (backward compatible)
- [ ] Error handling intact
- [ ] Performance not degraded
- [ ] Documentation updated
- [ ] Integration tests pass

---

### C. Testing Best Practices

1. **Arrange-Act-Assert Pattern**
   ```python
   def test_calculate_credit():
       # Arrange
       budget = 5000000
       percentage = 25.0
       
       # Act
       result = calculate_credit(budget, percentage)
       
       # Assert
       assert result == 1250000
   ```

2. **One Assertion Per Test** (when possible)
   - Easier to debug failures
   - Clear test purpose
   - Better failure messages

3. **Descriptive Test Names**
   ```python
   # Good
   def test_calculation_applies_maximum_cap_when_exceeded()
   
   # Bad
   def test_calc_1()
   ```

4. **Use Fixtures for Test Data**
   ```python
   @pytest.fixture
   def california_rule():
       return {
           "percentage": 25.0,
           "minSpend": 1000000,
           "maxCredit": 10000000
       }
   ```

5. **Test Independence**
   - Tests should not depend on other tests
   - Each test should clean up after itself
   - Use database transactions or cleanup fixtures

6. **Meaningful Assertions**
   ```python
   # Good
   assert response.status_code == 200, "Expected successful response"
   assert len(jurisdictions) > 0, "Expected at least one jurisdiction"
   
   # Basic
   assert response.status_code == 200
   ```

---

### D. Troubleshooting Guide

#### Test Failures

**Problem:** Tests pass locally but fail in CI  
**Solutions:**
- Check environment variables
- Verify database state/seeding
- Check for timezone issues
- Review CI logs carefully

**Problem:** Intermittent test failures  
**Solutions:**
- Look for race conditions
- Check for shared state between tests
- Add explicit waits for async operations
- Use test isolation techniques

**Problem:** Slow test execution  
**Solutions:**
- Parallelize tests with pytest-xdist
- Use database transactions instead of cleanup
- Mock external dependencies
- Profile test execution

---

### E. Testing Resources

#### Documentation
- [pytest documentation](https://docs.pytest.org/)
- [FastAPI testing guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [Prisma testing](https://www.prisma.io/docs/guides/testing)

#### Training Materials
- Internal testing workshop (quarterly)
- Pytest best practices guide
- API testing patterns

#### Tools
- pytest: Test framework
- pytest-cov: Coverage reporting
- pytest-asyncio: Async test support
- httpx: HTTP client for testing

---

### F. Glossary

**E2E Testing:** End-to-End testing validates complete workflows from start to finish

**Integration Testing:** Testing interactions between system components

**Unit Testing:** Testing individual functions or classes in isolation

**Regression Testing:** Re-testing previously working features to ensure no new bugs

**Smoke Testing:** Quick validation that critical features work

**Test Coverage:** Percentage of code executed by tests

**Test Fixture:** Reusable test data or setup code

**Mock:** Simulated object that mimics real object behavior

**Assertion:** Statement that verifies expected behavior

**Test Suite:** Collection of related test cases

---

### G. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-13 | QA Team | Initial document creation |

---

### H. Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| QA Lead | [Name] | _________ | ______ |
| Development Lead | [Name] | _________ | ______ |
| Product Owner | [Name] | _________ | ______ |

---

## 📞 Contact

**Questions about this process?**

- QA Lead: qa@pilotforge.com
- Development Team: dev@pilotforge.com
- Documentation: docs@pilotforge.com

---

*This document is maintained by the QA team and reviewed quarterly.*

**Next Review Date:** April 13, 2026
