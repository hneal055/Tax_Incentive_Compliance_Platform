param(
  [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

Write-Host "=== Tax Incentive API: Daily Startup ===" -ForegroundColor Cyan

# 1) Ensure we're at repo root
Set-Location (Split-Path $PSScriptRoot -Parent)

# 2) Ensure venv exists + activate
if (!(Test-Path ".\.venv\Scripts\Activate.ps1")) {
  Write-Host "Creating .venv..." -ForegroundColor Yellow
  python -m venv .venv
}

Write-Host "Activating .venv..." -ForegroundColor Green
. .\.venv\Scripts\Activate.ps1

# 3) Install/refresh deps (safe, quick if already satisfied)
Write-Host "Installing requirements..." -ForegroundColor Green
python -m pip install -U pip
if (Test-Path ".\requirements.txt") {
  python -m pip install -r .\requirements.txt
}

# 4) Quick sanity checks
Write-Host "Sanity checks..." -ForegroundColor Green
python -c "import fastapi, uvicorn; print('FastAPI/uvicorn OK')"
python -m pytest -q

# 5) Start API
Write-Host "Starting API on port $Port..." -ForegroundColor Cyan
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port $Port
