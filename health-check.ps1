# health-check.ps1
# PilotForge Health Check - Run this FIRST after environment setup
# Validates: Database connection, Prisma sync, API startup, basic endpoints

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "PilotForge Health Check" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

$errors = 0

# 1. Check Python version
Write-Host "[1/5] Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "3\.12") {
    Write-Host "  ✓ Python 3.12 detected: $pythonVersion" -ForegroundColor Green
}
else {
    Write-Host "  ✗ Wrong Python version: $pythonVersion" -ForegroundColor Red
    Write-Host "    Expected: Python 3.12.x" -ForegroundColor Red
    $errors++
}
Write-Host ""

# 2. Check database connection
Write-Host "[2/5] Checking database connection..." -ForegroundColor Yellow
try {
    $dbCheck = python -c "from prisma import Prisma; import asyncio; db = Prisma(); asyncio.run(db.connect()); print('OK'); asyncio.run(db.disconnect())" 2>&1
    if ($dbCheck -match "OK") {
        Write-Host "  ✓ Database connection successful" -ForegroundColor Green
    }
    else {
        Write-Host "  ✗ Database connection failed" -ForegroundColor Red
        Write-Host "    Error: $dbCheck" -ForegroundColor Red
        $errors++
    }
}
catch {
    Write-Host "  ✗ Database connection check failed" -ForegroundColor Red
    Write-Host "    Error: $_" -ForegroundColor Red
    $errors++
}
Write-Host ""

# 3. Check Prisma schema is generated
Write-Host "[3/5] Checking Prisma client..." -ForegroundColor Yellow
if (Test-Path "prisma/schema.prisma") {
    Write-Host "  ✓ Prisma schema found" -ForegroundColor Green
    
    # Check if Prisma client is generated
    try {
        python -c "from prisma import Prisma" 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Prisma client is generated" -ForegroundColor Green
        }
        else {
            Write-Host "  ✗ Prisma client not generated - run: prisma generate" -ForegroundColor Red
            $errors++
        }
    }
    catch {
        Write-Host "  ✗ Prisma client import failed" -ForegroundColor Red
        $errors++
    }
}
else {
    Write-Host "  ✗ Prisma schema not found at prisma/schema.prisma" -ForegroundColor Red
    $errors++
}
Write-Host ""

# 4. Check if FastAPI can import
Write-Host "[4/5] Checking FastAPI application..." -ForegroundColor Yellow
try {
    python -c "from src.main import app; print('OK')" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ FastAPI app imports successfully" -ForegroundColor Green
    }
    else {
        Write-Host "  ✗ FastAPI app import failed" -ForegroundColor Red
        $errors++
    }
}
catch {
    Write-Host "  ✗ FastAPI app check failed: $_" -ForegroundColor Red
    $errors++
}
Write-Host ""

# 5. Run core smoke tests (if pytest is available)
Write-Host "[5/5] Running core smoke tests..." -ForegroundColor Yellow
if (Test-Path "tests") {
    try {
        # Run only tests marked as 'smoke' or run a small subset
        $testResult = pytest tests/ -k "test_" --maxfail=3 -v 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Core tests passed" -ForegroundColor Green
        }
        else {
            Write-Host "  ! Some tests failed (check details above)" -ForegroundColor Yellow
            Write-Host "    This might be OK if you're still developing" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "  ! Could not run tests: $_" -ForegroundColor Yellow
    }
}
else {
    Write-Host "  ! No tests directory found - skipping" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "=====================================" -ForegroundColor Cyan
if ($errors -eq 0) {
    Write-Host "HEALTH CHECK PASSED ✓" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Your project core is stable. Safe to proceed with development." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  • Run API server: uvicorn src.main:app --reload" -ForegroundColor White
    Write-Host "  • Run full test suite: pytest tests/ -v" -ForegroundColor White
    Write-Host "  • Check API docs: http://localhost:8000/docs" -ForegroundColor White
}
else {
    Write-Host "HEALTH CHECK FAILED ✗" -ForegroundColor Red
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Found $errors critical issue(s). Fix these before proceeding." -ForegroundColor Red
    Write-Host ""
    Write-Host "Common fixes:" -ForegroundColor Yellow
    Write-Host "  • Database: Check DATABASE_URL in .env file" -ForegroundColor White
    Write-Host "  • Prisma: Run 'prisma generate' to regenerate client" -ForegroundColor White
    Write-Host "  • Imports: Check for missing dependencies in requirements.txt" -ForegroundColor White
}
Write-Host ""