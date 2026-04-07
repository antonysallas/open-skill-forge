# ─── open-skill-forge removal (Windows) ───

$ErrorActionPreference = "Stop"

function Write-Info  { param($msg) Write-Host "▶ $msg" -ForegroundColor Cyan }
function Write-Ok    { param($msg) Write-Host "✔ $msg" -ForegroundColor Green }
function Write-Warn  { param($msg) Write-Host "⚠ $msg" -ForegroundColor Yellow }

Write-Host ""
Write-Host "═══════════════════════════════════════════"
Write-Host "  open-skill-forge – Environment Removal"
Write-Host "═══════════════════════════════════════════"
Write-Host ""
Write-Host "This will remove JupyterLab, uv-managed Python, and uv."
Write-Host ""

$confirm = Read-Host "Continue? (y/N)"
if ($confirm -notin @("y", "Y")) {
    Write-Host "Aborted."
    exit 0
}
Write-Host ""

# ── 1. Remove JupyterLab ──
$uvCmd = Get-Command uv -ErrorAction SilentlyContinue
if ($uvCmd) {
    Write-Info "Removing JupyterLab..."
    try {
        uv tool uninstall jupyterlab 2>$null
        Write-Ok "JupyterLab removed"
    } catch {
        Write-Warn "JupyterLab was not installed"
    }
} else {
    Write-Warn "uv not found — skipping JupyterLab removal"
}

# ── 2. Remove uv-managed Python installations ──
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

$uvPaths = @(
    "$env:USERPROFILE\.local\bin\uv.exe",
    "$env:USERPROFILE\.local\bin\uvx.exe"
)
if ($env:CARGO_HOME) {
    $uvPaths += "$env:CARGO_HOME\bin\uv.exe"
    $uvPaths += "$env:CARGO_HOME\bin\uvx.exe"
}

foreach ($p in $uvPaths) {
    if ($p -and (Test-Path $p)) { Remove-Item $p -Force }
}

$uvDataDirs = @(
    "$env:USERPROFILE\.local\share\uv",
    "$env:LOCALAPPDATA\uv"
)

foreach ($d in $uvDataDirs) {
    if (Test-Path $d) { Remove-Item $d -Recurse -Force }
}

Write-Ok "uv removed"

Write-Host ""
Write-Host "═══════════════════════════════════════════"
Write-Host "  Removal complete"
Write-Host "═══════════════════════════════════════════"
Write-Host ""
Write-Ok "All open-skill-forge components have been removed."
Write-Host ""
