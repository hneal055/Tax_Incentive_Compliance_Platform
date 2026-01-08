Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Step([string]$Msg) {
  Write-Host ""
  Write-Host "==> $Msg"
}

function Run([Parameter(Mandatory=$true)][string]$File, [string[]]$Arguments = @()) {
  $joined = ($Arguments | ForEach-Object { if ($_ -match '\s') { "`"$_`"" } else { $_ } }) -join " "
  if ($joined) { Write-Host ">> $File $joined" } else { Write-Host ">> $File" }

  & $File @Arguments
  if ($LASTEXITCODE -ne 0) { throw "Command failed (exit $LASTEXITCODE): $File $joined" }
}

# Repo root = parent of /scripts
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RepoRoot

$VenvDir = Join-Path $RepoRoot ".venv"
$Py = Join-Path $VenvDir "Scripts\python.exe"

Write-Step "Ensuring venv"
if (-not (Test-Path $Py)) {
  Run "python" @("-m","venv",$VenvDir)
}

Write-Step "Upgrading pip"
Run $Py @("-m","pip","install","-U","pip")

# Prefer Phase-1 stable deps; fallback to requirements.txt only if core doesn't exist
$ReqCore = Join-Path $RepoRoot "requirements.core.txt"
$ReqMain = Join-Path $RepoRoot "requirements.txt"

Write-Step "Installing dependencies"
if (Test-Path $ReqCore) {
  Run $Py @("-m","pip","install","-r",$ReqCore)
} elseif (Test-Path $ReqMain) {
  Run $Py @("-m","pip","install","-r",$ReqMain)
} else {
  throw "No requirements file found. Expected requirements.core.txt (preferred) or requirements.txt at repo root."
}

Write-Step "Running tests"
Run $Py @("-m","pytest","-q")

Write-Step "All tests passed ✅"
exit 0
