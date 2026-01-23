# Comprehensive Test Suite Runner for PilotForge
# Tax Incentive Intelligence for Film & TV

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "🎬 PilotForge - Comprehensive Test Suite" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Use current directory as repo root
$RepoRoot = Get-Location
Write-Host "📁 Repository:  $RepoRoot" -ForegroundColor Green
Write-Host ""

# Check for virtual environment
$VenvPath = Join-Path $RepoRoot ".venv"
$PythonExe = Join-Path $VenvPath "Scripts\python.exe"

if (-not (Test-Path $PythonExe)) {
    Write-Host "⚠️  Virtual environment not found at . venv" -ForegroundColor Yellow
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
}

# Install/upgrade dependencies
Write-Host ""
Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan

& $PythonExe -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to upgrade pip" -ForegroundColor Red
    exit 1
}

# Install from requirements. core. txt if available, otherwise requirements.txt
$ReqCore = Join-Path $RepoRoot "requirements.core.txt"
$ReqMain = Join-Path $RepoRoot "requirements.txt"

if (Test-Path $ReqCore) {
    Write-Host "Installing from requirements.core.txt..." -ForegroundColor Yellow
    & $PythonExe -m pip install -r $ReqCore --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Some packages failed to install, continuing..." -ForegroundColor Yellow
    }
} elseif (Test-Path $ReqMain) {
    Write-Host "Installing from requirements.txt..." -ForegroundColor Yellow
    & $PythonExe -m pip install -r $ReqMain --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Some packages failed to install, continuing..." -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  No requirements file found" -ForegroundColor Yellow
}

Write-Host "✅ Dependencies processed" -ForegroundColor Green
Write-Host ""

# Display test configuration
Write-Host "🔧 Test Configuration:" -ForegroundColor Cyan
Write-Host "  - Test Framework: pytest" -ForegroundColor White
Write-Host "  - Test Path: tests/" -ForegroundColor White
Write-Host "  - Coverage Target: src/" -ForegroundColor White
Write-Host ""

# Check if tests directory exists
if (-not (Test-Path "tests")) {
    Write-Host "❌ Tests directory not found!" -ForegroundColor Red
    exit 1
}

# Run tests with different levels of verbosity
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🧪 Running Test Suite" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

$TestResults = @{}

# Test 1: Quick smoke test
if (Test-Path "tests/test_smoke_api.py") {
    Write-Host "1️⃣  SMOKE TESTS (Quick validation)" -ForegroundColor Yellow
    Write-Host "-" * 70
    & $PythonExe -m pytest tests/test_smoke_api.py -v --tb=short
    $TestResults['Smoke Tests'] = $LASTEXITCODE
    Write-Host ""
} else {
    Write-Host "1️⃣  SMOKE TESTS - SKIPPED (file not found)" -ForegroundColor Gray
    Write-Host ""
}

# Test 2: API endpoint tests
if (Test-Path "tests/test_api_endpoints. py") {
    Write-Host "2️⃣  API ENDPOINT TESTS" -ForegroundColor Yellow
    Write-Host "-" * 70
    & $PythonExe -m pytest tests/test_api_endpoints.py -v --tb=short
    $TestResults['API Endpoints'] = $LASTEXITCODE
    Write-Host ""
} else {
    Write-Host "2️⃣  API ENDPOINT TESTS - SKIPPED (file not found)" -ForegroundColor Gray
    Write-Host ""
}

# Test 3: Calculator logic tests
if (Test-Path "tests/test_calculator_logic.py") {
    Write-Host "3️⃣  CALCULATOR LOGIC TESTS" -ForegroundColor Yellow
    Write-Host "-" * 70
    & $PythonExe -m pytest tests/test_calculator_logic.py -v --tb=short
    $TestResults['Calculator Logic'] = $LASTEXITCODE
    Write-Host ""
} else {
    Write-Host "3️⃣  CALCULATOR LOGIC TESTS - SKIPPED (file not found)" -ForegroundColor Gray
    Write-Host ""
}

# Test 4: Report generation tests
if (Test-Path "tests/test_report_generation.py") {
    Write-Host "4️⃣  REPORT GENERATION TESTS" -ForegroundColor Yellow
    Write-Host "-" * 70
    & $PythonExe -m pytest tests/test_report_generation.py -v --tb=short
    $TestResults['Report Generation'] = $LASTEXITCODE
    Write-Host ""
} else {
    Write-Host "4️⃣  REPORT GENERATION TESTS - SKIPPED (file not found)" -ForegroundColor Gray
    Write-Host ""
}

# Test 5: Rule engine tests
if (Test-Path "tests/test_engine_entrypoint.py") {
    Write-Host "5️⃣  RULE ENGINE TESTS" -ForegroundColor Yellow
    Write-Host "-" * 70
    & $PythonExe -m pytest tests/test_engine_entrypoint. py -v --tb=short
    $TestResults['Rule Engine'] = $LASTEXITCODE
    Write-Host ""
} else {
    Write-Host "5️⃣  RULE ENGINE TESTS - SKIPPED (file not found)" -ForegroundColor Gray
    Write-Host ""
}

# Test 6: Full test suite with coverage
Write-Host "6️⃣  FULL TEST SUITE WITH COVERAGE" -ForegroundColor Yellow
Write-Host "-" * 70
& $PythonExe -m pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html --tb=short
$TestResults['Full Suite'] = $LASTEXITCODE
Write-Host ""

# Summary Report
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "📊 TEST SUMMARY REPORT" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

$AllPassed = $true
foreach ($TestName in $TestResults. Keys) {
    $Result = $TestResults[$TestName]
    if ($Result -eq 0) {
        Write-Host "✅ $TestName :  PASSED" -ForegroundColor Green
    } else {
        Write-Host "❌ $TestName : FAILED (Exit Code: $Result)" -ForegroundColor Red
        $AllPassed = $false
    }
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan

# Coverage Report Location
$CoverageReport = Join-Path $RepoRoot "htmlcov\index.html"
if (Test-Path $CoverageReport) {
    Write-Host "📈 Coverage Report Generated:" -ForegroundColor Green
    Write-Host "   $CoverageReport" -ForegroundColor White
    Write-Host ""
    Write-Host "   Open with:  start htmlcov\index.html" -ForegroundColor Yellow
    Write-Host ""
}

# Final Status
if ($AllPassed) {
    Write-Host "🎉 ALL TESTS PASSED!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your platform is:" -ForegroundColor Cyan
    Write-Host "  ✅ Bulletproof" -ForegroundColor Green
    Write-Host "  ✅ Production-ready" -ForegroundColor Green
    Write-Host "  ✅ Professional quality" -ForegroundColor Green
    Write-Host ""
    exit 0
} else {
    Write-Host "⚠️  SOME TESTS FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Review failed test output above" -ForegroundColor White
    Write-Host "  2. Check test logs for details" -ForegroundColor White
    Write-Host "  3. Fix issues and re-run tests" -ForegroundColor White
    Write-Host ""
    exit 1
}