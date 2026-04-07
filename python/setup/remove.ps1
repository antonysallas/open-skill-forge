# ─── open-skill-forge removal (Windows) ───

param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

function Write-Info  { param($msg) Write-Host "▶ $msg" -ForegroundColor Cyan }
function Write-Ok    { param($msg) Write-Host "✔ $msg" -ForegroundColor Green }
function Write-Warn  { param($msg) Write-Host "⚠ $msg" -ForegroundColor Yellow }

Write-Host ""
Write-Host "═══════════════════════════════════════════"
Write-Host "  open-skill-forge – Environment Removal"
Write-Host "═══════════════════════════════════════════"
Write-Host ""
$RepoDir = "$env:USERPROFILE\projects\open-skill-forge"

Write-Host "This will remove the virtual environment, cloned repository,"
Write-Host "uv-managed Python, and uv."
Write-Host ""

if (-not $Force) {
    $confirm = Read-Host "Continue? (y/N)"
    if ($confirm -notin @("y", "Y")) {
        Write-Host "Aborted."
        exit 0
    }
}
Write-Host ""

# ── 1. Remove cloned repository (includes venv) ──
if (Test-Path $RepoDir) {
    Write-Info "Removing $RepoDir..."
    Remove-Item $RepoDir -Recurse -Force
    Write-Ok "Repository and virtual environment removed"
} else {
    Write-Warn "Repository not found at $RepoDir"
}

# ── 2. Remove uv-managed Python installations ──
$uvCmd = Get-Command uv -ErrorAction SilentlyContinue
if ($uvCmd) {
    Write-Info "Removing uv-managed Python installations..."
    try {
        uv python uninstall --all 2>$null
        Write-Ok "Python installations removed"
    } catch {
        Write-Warn "No Python installations found"
    }
}

# ── 3. Remove uv ──
Write-Info "Removing uv..."

# Remove data/cache dirs first
$uvDataDirs = @(
    "$env:USERPROFILE\.local\share\uv",
    "$env:LOCALAPPDATA\uv"
)

foreach ($d in $uvDataDirs) {
    if (Test-Path $d) { Remove-Item $d -Recurse -Force }
}

# Remove binaries (uv, uvx, and any tool shims like jupyter-lab)
$localBin = "$env:USERPROFILE\.local\bin"
if (Test-Path $localBin) {
    Remove-Item $localBin -Recurse -Force
}

if ($env:CARGO_HOME) {
    $cargoPaths = @(
        "$env:CARGO_HOME\bin\uv.exe",
        "$env:CARGO_HOME\bin\uvx.exe"
    )
    foreach ($p in $cargoPaths) {
        if (Test-Path $p) { Remove-Item $p -Force }
    }
}

Write-Ok "uv removed"

Write-Host ""
Write-Host "═══════════════════════════════════════════"
Write-Host "  Removal complete"
Write-Host "═══════════════════════════════════════════"
Write-Host ""
Write-Ok "All open-skill-forge components have been removed."
Write-Host ""
