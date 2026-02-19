# Quick Test Runner
# Usage: .\run-tests.ps1

Write-Host "🧪 Tax Incentive Compliance Platform - Test Runner" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
    . \.venv\Scripts\Activate.ps1
}

Write-Host "✅ Virtual environment active" -ForegroundColor Green
Write-Host ""

# Show menu
Write-Host "Select test mode:" -ForegroundColor Cyan
Write-Host "1. Quick test (no coverage)" -ForegroundColor White
Write-Host "2. Verbose test" -ForegroundColor White
Write-Host "3. Test with coverage report" -ForegroundColor White
Write-Host "4. Test with HTML coverage report" -ForegroundColor White
Write-Host "5. Test specific file" -ForegroundColor White
Write-Host "6. Run all (verbose + coverage)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-6)"

switch ($choice) {
    "1" {
        Write-Host "🧪 Running quick tests..." -ForegroundColor Cyan
        pytest
    }
    "2" {
        Write-Host "🧪 Running verbose tests..." -ForegroundColor Cyan
        pytest -v
    }
    "3" {
        Write-Host "🧪 Running tests with coverage..." -ForegroundColor Cyan
        pytest --cov=src --cov-report=term-missing
    }
    "4" {
        Write-Host "🧪 Running tests with HTML coverage..." -ForegroundColor Cyan
        pytest --cov=src --cov-report=html
        Write-Host ""
        Write-Host "✅ Opening coverage report..." -ForegroundColor Green
        start htmlcov\index.html
    }
    "5" {
        Write-Host ""
        Write-Host "Available test files:" -ForegroundColor Cyan
        Get-ChildItem tests\test_*.py | ForEach-Object { Write-Host "  - $($_.Name)" }
        Write-Host ""
        $testFile = Read-Host "Enter test file name (e.g., test_registry.py)"
        Write-Host "🧪 Running $testFile..." -ForegroundColor Cyan
        pytest "tests\$testFile" -v
    }
    "6" {
        Write-Host "🧪 Running comprehensive tests..." -ForegroundColor Cyan
        pytest -v --cov=src --cov-report=term-missing --cov-report=html
        Write-Host ""
        Write-Host "✅ Opening coverage report..." -ForegroundColor Green
        start htmlcov\index.html
    }
    default {
        Write-Host "❌ Invalid choice" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Tests completed successfully!" -ForegroundColor Green
}
else {
    Write-Host "❌ Some tests failed" -ForegroundColor Red
}