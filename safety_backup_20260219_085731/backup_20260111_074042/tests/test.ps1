# scripts/test.ps1
# Phase 1 "bulletproof" test runner:
# - No dot-sourcing Activate.ps1 (avoids execution-policy / scope weirdness)
# - Uses .venv\Scripts\python.exe directly
# - Installs requirements.core.txt by default (fallbacks to requirements.txt)
# - Runs pytest in one command with a hard fail on errors

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Step([string]$Message) {
    Write-Host ""
    Write-Host "==> $Message"
}

function Run([string]$Command) {
    Write-Host ">> $Command"
    & powershell -NoProfile -Command $Command
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed (exit $LASTEXITCODE): $Command"
    }
}

# Repo root = parent of this scripts folder
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RepoRoot

$VenvDir = Join-Path $RepoRoot ".venv"
$Py = Join-Path $VenvDir "Scripts\python.exe"

Write-Step "Ensuring virtual environment (.venv)"
if (-not (Test-Path $Py)) {
    Run "python -m venv `"$VenvDir`""
}

Write-Step "Upgrading pip"
Run "`"$Py`" -m pip install -U pip"

# Prefer Phase-1 stable deps; fallback to requirements.txt only if core doesn't exist
$ReqCore = Join-Path $RepoRoot "requirements.core.txt"
$ReqMain = Join-Path $RepoRoot "requirements.txt"

if (Test-Path $ReqCore) {
    Write-Step "Installing dependencies from requirements.core.txt"
    Run "`"$Py`" -m pip install -r `"$ReqCore`""
}
elseif (Test-Path $ReqMain) {
    Write-Step "Installing dependencies from requirements.txt"
    Run "`"$Py`" -m pip install -r `"$ReqMain`""
}
else {
    throw "No requirements file found. Expected requirements.core.txt (preferred) or requirements.txt at repo root."
}

Write-Step "Running tests"
Run "`"$Py`" -m pytest -q"

Write-Step "All tests passed"
exit 0
