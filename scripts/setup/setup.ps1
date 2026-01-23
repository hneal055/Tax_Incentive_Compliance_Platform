# Tax-Incentive Compliance Platform - Setup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Tax-Incentive Compliance Platform - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python 3.12
Write-Host "Checking Python 3.12..." -ForegroundColor Yellow
try {
    $python312 = Get-Command py -ErrorAction Stop
    $pythonVersion = py -3.12 --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python 3.12 not found"
    }
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python 3.12 not found" -ForegroundColor Red
    Write-Host "Please install Python 3.12 from https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found" -ForegroundColor Red
    exit 1
}

# Check PostgreSQL
Write-Host "Checking PostgreSQL..." -ForegroundColor Yellow
try {
    $psqlVersion = psql --version 2>&1
    Write-Host "✓ $psqlVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠ PostgreSQL not found (optional if using Docker)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Creating virtual environment with Python 3.12..." -ForegroundColor Yellow
py -3.12 -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
pip install -r requirements-dev.txt

Write-Host "Installing Node dependencies..." -ForegroundColor Yellow
npm install

Write-Host ""
if (-Not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "✓ Created .env file" -ForegroundColor Green
    Write-Host "Edit with: notepad .env" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Database setup - Create database? (Y/N)" -ForegroundColor Cyan
$createDb = Read-Host

if ($createDb -eq "Y") {
    Write-Host "PostgreSQL password:" -ForegroundColor Cyan
    $pgPassword = Read-Host -AsSecureString
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($pgPassword)
    $plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    
    $env:PGPASSWORD = $plainPassword
    psql -U postgres -c "CREATE DATABASE tax_incentive_db;"
    Remove-Item Env:\PGPASSWORD
    
    npx prisma generate
    npx prisma migrate dev --name init
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next: python -m uvicorn src.main:app --reload" -ForegroundColor White