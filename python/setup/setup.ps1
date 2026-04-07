# ─── open-skill-forge setup (Windows) ───

$ErrorActionPreference = "Stop"
$PythonVersion = "3.12"
$RepoUrl = "https://github.com/antonysallas/open-skill-forge.git"
$RepoDir = "$env:USERPROFILE\projects\open-skill-forge"

function Write-Info  { param($msg) Write-Host "▶ $msg" -ForegroundColor Cyan }
function Write-Ok    { param($msg) Write-Host "✔ $msg" -ForegroundColor Green }
function Write-Fail  { param($msg) Write-Host "✖ $msg" -ForegroundColor Red; exit 1 }

Write-Host ""
Write-Host "═══════════════════════════════════════════"
Write-Host "  open-skill-forge – Environment Setup"
Write-Host "═══════════════════════════════════════════"
Write-Host ""

# ── 1. Install uv ──
$uvCmd = Get-Command uv -ErrorAction SilentlyContinue
if ($uvCmd) {
    Write-Ok "uv already installed ($(uv --version))"
} else {
    Write-Info "Installing uv..."
    irm https://astral.sh/uv/install.ps1 | iex
    # Refresh PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "User") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    $uvCmd = Get-Command uv -ErrorAction SilentlyContinue
    if (-not $uvCmd) { Write-Fail "uv installation failed" }
    Write-Ok "uv installed ($(uv --version))"
}

# ── 2. Install Python ──
Write-Info "Installing Python $PythonVersion via uv..."
uv python install $PythonVersion
Write-Ok "Python $PythonVersion installed"

# ── 3. Install JupyterLab ──
Write-Info "Installing JupyterLab via uv..."
uv tool install --force jupyterlab
Write-Ok "JupyterLab installed"

# ── 4. Clone repository ──
if (Test-Path "$RepoDir\.git") {
    Write-Ok "Repository already cloned at $RepoDir"
} else {
    New-Item -ItemType Directory -Path (Split-Path $RepoDir) -Force | Out-Null
    Write-Info "Cloning repository to $RepoDir..."
    git clone $RepoUrl $RepoDir
    Write-Ok "Repository cloned"
}

# ── 5. Verify ──
Write-Host ""
Write-Host "═══════════════════════════════════════════"
Write-Host "  Verification"
Write-Host "═══════════════════════════════════════════"
Write-Host ""
Write-Host "  uv:         $(uv --version)"
Write-Host "  Python:     $(uv run --python $PythonVersion python --version)"
try {
    $jlVersion = jupyter-lab --version 2>$null
    Write-Host "  JupyterLab: $jlVersion"
} catch {
    Write-Host "  JupyterLab: run 'jupyter lab' to start"
}
Write-Host ""

# ── 6. Done ──
Write-Ok "Setup complete!"
Write-Host ""
Write-Host "Open a new terminal, then run:"
Write-Host ""
Write-Host "  cd $RepoDir\python\notebooks; jupyter lab"
Write-Host ""
