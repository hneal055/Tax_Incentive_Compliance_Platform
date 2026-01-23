# setup-env.ps1
Write-Host "Setting up PilotForge environment..." -ForegroundColor Cyan

# Remove old venv if it exists
if (Test-Path .venv) {
    Write-Host "Removing old venv..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .venv
}

# Create venv with Python 3.12 (adjust path to your Python 3.12 installation)
py -3.12 -m venv .venv

# Activate and install requirements
.\.venv\Scripts\Activate.ps1
Write-Host "Installing requirements..." -ForegroundColor Green
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Environment ready! ✓" -ForegroundColor Green