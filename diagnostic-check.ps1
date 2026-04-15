# ========================================
# System Diagnostic Check
# Tests all key components of SceneIQ
# ========================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "SceneIQ System Diagnostic" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

$results = @{
    Passed = @()
    Failed = @()
    Warnings = @()
}

# ========================================
# 1. PYTHON VERSION CHECK
# ========================================
Write-Host "[1/10] Python Version..." -NoNewline

try {
    $pythonVersion = & python --version 2>&1
    if ($pythonVersion -match "Python 3\.12\.\d+") {
        Write-Host " ✅ $pythonVersion" -ForegroundColor Green
        $results.Passed += "Python 3.12 installed"
    } else {
        Write-Host " ⚠️  $pythonVersion (Expected 3.12)" -ForegroundColor Yellow
        $results.Warnings += "Python version is $pythonVersion, expected 3.12.x"
    }
} catch {
    Write-Host " ❌ Python not found" -ForegroundColor Red
    $results.Failed += "Python not found in PATH"
}

# ========================================
# 2. VIRTUAL ENVIRONMENT
# ========================================
Write-Host "[2/10] Virtual Environment..." -NoNewline

$venvPath = ".venv\Scripts\python.exe"
if (Test-Path $venvPath) {
    $venvPython = & $venvPath --version 2>&1
    Write-Host " ✅ $venvPython" -ForegroundColor Green
    $results.Passed += "Virtual environment exists"
} else {
    Write-Host " ❌ Not found" -ForegroundColor Red
    $results.Failed += "Virtual environment not created (.venv/)"
}

# ========================================
# 3. REQUIRED DEPENDENCIES
# ========================================
Write-Host "[3/10] Python Dependencies..." -NoNewline

if (Test-Path $venvPath) {
    $pipList = & $venvPath -m pip list 2>&1
    $requiredPackages = @("fastapi", "prisma", "uvicorn", "pydantic")
    $missingPackages = @()
    
    foreach ($pkg in $requiredPackages) {
        if ($pipList -notmatch $pkg) {
            $missingPackages += $pkg
        }
    }
    
    if ($missingPackages.Count -eq 0) {
        Write-Host " ✅ All core packages installed" -ForegroundColor Green
        $results.Passed += "All required Python packages present"
    } else {
        Write-Host " ⚠️  Missing: $($missingPackages -join ', ')" -ForegroundColor Yellow
        $results.Warnings += "Missing packages: $($missingPackages -join ', ')"
    }
} else {
    Write-Host " ⏭️  Skipped (no venv)" -ForegroundColor Gray
}

# ========================================
# 4. DOCKER
# ========================================
Write-Host "[4/10] Docker..." -NoNewline

try {
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅ $dockerVersion" -ForegroundColor Green
        $results.Passed += "Docker installed"
    } else {
        throw "Docker not accessible"
    }
} catch {
    Write-Host " ❌ Not running" -ForegroundColor Red
    $results.Failed += "Docker not running or not installed"
}

# ========================================
# 5. DOCKER CONTAINER
# ========================================
Write-Host "[5/10] PostgreSQL Container..." -NoNewline

try {
    $container = docker ps --format "{{.Names}}" | Select-String "tax-incentive-db"
    if ($container) {
        Write-Host " ✅ Running" -ForegroundColor Green
        $results.Passed += "PostgreSQL container running"
    } else {
        $containerExists = docker ps -a --format "{{.Names}}" | Select-String "tax-incentive-db"
        if ($containerExists) {
            Write-Host " ⚠️  Stopped" -ForegroundColor Yellow
            $results.Warnings += "PostgreSQL container exists but not running"
        } else {
            Write-Host " ⚠️  Not created" -ForegroundColor Yellow
            $results.Warnings += "PostgreSQL container not created yet"
        }
    }
} catch {
    Write-Host " ⏭️  Skipped (Docker issue)" -ForegroundColor Gray
}

# ========================================
# 6. DATABASE CONNECTION
# ========================================
Write-Host "[6/10] Database Connection..." -NoNewline

try {
    $dbCheck = docker exec tax-incentive-db pg_isready -U postgres 2>&1
    if ($dbCheck -match "accepting connections") {
        Write-Host " ✅ Connected" -ForegroundColor Green
        $results.Passed += "Database accepting connections"
    } else {
        Write-Host " ❌ Not ready" -ForegroundColor Red
        $results.Failed += "Database not accepting connections"
    }
} catch {
    Write-Host " ⏭️  Skipped" -ForegroundColor Gray
}

# ========================================
# 7. PRISMA SCHEMA
# ========================================
Write-Host "[7/10] Prisma Schema..." -NoNewline

$schemaPath = "prisma\schema.prisma"
if (Test-Path $schemaPath) {
    $schemaContent = Get-Content $schemaPath -Raw
    $models = ([regex]::Matches($schemaContent, "model \w+")).Count
    Write-Host " ✅ Found ($models models)" -ForegroundColor Green
    $results.Passed += "Prisma schema exists with $models models"
} else {
    Write-Host " ❌ Not found" -ForegroundColor Red
    $results.Failed += "Prisma schema file missing"
}

# ========================================
# 8. ENVIRONMENT FILE
# ========================================
Write-Host "[8/10] Environment Config..." -NoNewline

if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "DATABASE_URL") {
        Write-Host " ✅ Configured" -ForegroundColor Green
        $results.Passed += ".env file exists with DATABASE_URL"
    } else {
        Write-Host " ⚠️  Missing DATABASE_URL" -ForegroundColor Yellow
        $results.Warnings += ".env exists but missing DATABASE_URL"
    }
} else {
    Write-Host " ⚠️  Not found" -ForegroundColor Yellow
    $results.Warnings += ".env file not found (will use defaults)"
}

# ========================================
# 9. FRONTEND
# ========================================
Write-Host "[9/10] Frontend..." -NoNewline

$frontendPath = "frontend"
if (Test-Path $frontendPath) {
    $packageJsonPath = Join-Path $frontendPath "package.json"
    if (Test-Path $packageJsonPath) {
        $nodeModulesPath = Join-Path $frontendPath "node_modules"
        if (Test-Path $nodeModulesPath) {
            Write-Host " ✅ Ready (dependencies installed)" -ForegroundColor Green
            $results.Passed += "Frontend exists with dependencies"
        } else {
            Write-Host " ⚠️  Dependencies not installed" -ForegroundColor Yellow
            $results.Warnings += "Frontend exists but needs 'npm install'"
        }
    } else {
        Write-Host " ⚠️  package.json missing" -ForegroundColor Yellow
        $results.Warnings += "Frontend folder exists but package.json missing"
    }
} else {
    Write-Host " ⚠️  Not found" -ForegroundColor Yellow
    $results.Warnings += "Frontend folder not found"
}

# ========================================
# 10. REPOSITORY STRUCTURE
# ========================================
Write-Host "[10/10] Repository Structure..." -NoNewline

$nestedFolder = "Tax_Incentive_Compliance_Platform\Tax_Incentive_Compliance_Platform"
if (Test-Path $nestedFolder) {
    Write-Host " ⚠️  Nested folders detected" -ForegroundColor Yellow
    $results.Warnings += "Nested folder structure found - needs cleanup"
} else {
    Write-Host " ✅ Clean" -ForegroundColor Green
    $results.Passed += "Repository structure is clean"
}

# ========================================
# SUMMARY
# ========================================
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "DIAGNOSTIC SUMMARY" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

$totalPassed = $results.Passed.Count
$totalWarnings = $results.Warnings.Count
$totalFailed = $results.Failed.Count
$totalChecks = $totalPassed + $totalWarnings + $totalFailed

Write-Host "Checks Performed: $totalChecks`n" -ForegroundColor White

if ($totalPassed -gt 0) {
    Write-Host "✅ PASSED ($totalPassed):" -ForegroundColor Green
    foreach ($item in $results.Passed) {
        Write-Host "   • $item" -ForegroundColor Gray
    }
    Write-Host ""
}

if ($totalWarnings -gt 0) {
    Write-Host "⚠️  WARNINGS ($totalWarnings):" -ForegroundColor Yellow
    foreach ($item in $results.Warnings) {
        Write-Host "   • $item" -ForegroundColor Gray
    }
    Write-Host ""
}

if ($totalFailed -gt 0) {
    Write-Host "❌ FAILED ($totalFailed):" -ForegroundColor Red
    foreach ($item in $results.Failed) {
        Write-Host "   • $item" -ForegroundColor Gray
    }
    Write-Host ""
}

# Overall health score
$healthScore = [math]::Round(($totalPassed / $totalChecks) * 100, 0)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Overall Health: $healthScore%" -NoNewline

if ($healthScore -ge 80) {
    Write-Host " 🎉 Excellent" -ForegroundColor Green
    Write-Host "System is ready for development!" -ForegroundColor Green
} elseif ($healthScore -ge 60) {
    Write-Host " 👍 Good" -ForegroundColor Yellow
    Write-Host "Some minor issues to address." -ForegroundColor Yellow
} elseif ($healthScore -ge 40) {
    Write-Host " ⚠️  Fair" -ForegroundColor Yellow
    Write-Host "Several issues need attention." -ForegroundColor Yellow
} else {
    Write-Host " 🚨 Poor" -ForegroundColor Red
    Write-Host "Significant issues require resolution." -ForegroundColor Red
}

Write-Host "========================================`n" -ForegroundColor Cyan

# Recommendations
if ($totalFailed -gt 0 -or $totalWarnings -gt 0) {
    Write-Host "📋 RECOMMENDATIONS:`n" -ForegroundColor Cyan
    
    if ($results.Failed -match "Python not found") {
        Write-Host "   1. Install Python 3.12 from python.org" -ForegroundColor White
    }
    
    if ($results.Failed -match "Virtual environment") {
        Write-Host "   2. Create virtual environment: python -m venv .venv" -ForegroundColor White
    }
    
    if ($results.Warnings -match "Missing packages") {
        Write-Host "   3. Install dependencies: pip install -r requirements.txt" -ForegroundColor White
    }
    
    if ($results.Failed -match "Docker") {
        Write-Host "   4. Install and start Docker Desktop" -ForegroundColor White
    }
    
    if ($results.Warnings -match "container.*not running") {
        Write-Host "   5. Start database: docker-compose up -d" -ForegroundColor White
    }
    
    if ($results.Warnings -match "Nested folder") {
        Write-Host "   6. Run cleanup: .\cleanup-repo.ps1 -DryRun" -ForegroundColor White
    }
    
    if ($results.Warnings -match "Frontend.*npm install") {
        Write-Host "   7. Install frontend: cd frontend && npm install" -ForegroundColor White
    }
    
    Write-Host "`n   Or run automated setup: .\start.ps1`n" -ForegroundColor Cyan
}

Write-Host "For detailed stability report, see: STABILITY_REVIEW.md`n" -ForegroundColor Gray
