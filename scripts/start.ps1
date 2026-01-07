Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Step([string]$msg) {
  Write-Host ""
  Write-Host "==> $msg"
}

function Run-Cmd([string]$Label, [string]$Exe, [string[]]$ArgList) {
  $pretty = ($ArgList | ForEach-Object { if ($_ -match "\s") { "`"$_`"" } else { $_ } }) -join " "
  Write-Host ">> $Label"
  Write-Host "   $Exe $pretty"
  & $Exe @ArgList
  if ($LASTEXITCODE -ne 0) { throw "Command failed: $Label" }
}

# Repo root = parent of /scripts
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

$VenvDir = Join-Path $RepoRoot ".venv"
$Py = Join-Path $VenvDir "Scripts\python.exe"

# Env overrides (optional)
$HostAddr = if ($env:HOST) { $env:HOST } else { "127.0.0.1" }
$Port = if ($env:PORT) { $env:PORT } else { "8000" }
$AppImport = if ($env:APP) { $env:APP } else { "src.main:app" }

Write-Step "Ensuring venv"
if (-not (Test-Path $Py)) {
  Write-Host ">> python -m venv `"$VenvDir`""
  python -m venv "$VenvDir"
  if ($LASTEXITCODE -ne 0) { throw "Command failed: python -m venv" }
}

# Non-interactive version check (works everywhere)
Run-Cmd "Python version" $Py @("-c","import sys; print(sys.version.split()[0])")

Write-Step "Upgrading pip"
Run-Cmd "pip upgrade" $Py @("-m","pip","install","-U","pip")

# Prefer Phase-1 core deps (no heavy/DB extras)
$ReqCore = Join-Path $RepoRoot "requirements.core.txt"
$ReqMain = Join-Path $RepoRoot "requirements.txt"

Write-Step "Installing dependencies"
if (Test-Path $ReqCore) {
  Run-Cmd "pip install core" $Py @("-m","pip","install","-r",$ReqCore)
} elseif (Test-Path $ReqMain) {
  Run-Cmd "pip install main" $Py @("-m","pip","install","-r",$ReqMain)
} else {
  throw "No requirements file found. Expected requirements.core.txt (preferred) or requirements.txt at repo root."
}

# Load .env if present (simple KEY=VALUE lines; ignores comments/blank lines)
$EnvPath = Join-Path $RepoRoot ".env"
if (Test-Path $EnvPath) {
  Write-Step "Loading .env"
  Get-Content $EnvPath | ForEach-Object {
    $line = $_.Trim()
    if (-not $line) { return }
    if ($line.StartsWith("#")) { return }
    $idx = $line.IndexOf("=")
    if ($idx -lt 1) { return }
    $k = $line.Substring(0, $idx).Trim()
    $v = $line.Substring($idx + 1).Trim()
    if (($v.StartsWith('"') -and $v.EndsWith('"')) -or ($v.StartsWith("'") -and $v.EndsWith("'"))) {
      $v = $v.Substring(1, $v.Length - 2)
    }
    [Environment]::SetEnvironmentVariable($k, $v, "Process")
  }
}

Write-Step "Starting API"
Write-Host "App:  $AppImport"
Write-Host "Bind: http://$HostAddr`:$Port"
Write-Host "Docs: http://$HostAddr`:$Port/docs"
Write-Host "API:  http://$HostAddr`:$Port/api/v1/"

# Reload default ON for dev; set RELOAD=0 to disable
$ReloadArgs = @()
if (-not ($env:RELOAD -and $env:RELOAD -eq "0")) { $ReloadArgs = @("--reload") }

Run-Cmd "uvicorn" $Py (@("-m","uvicorn",$AppImport,"--host",$HostAddr,"--port",$Port) + $ReloadArgs)
