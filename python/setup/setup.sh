#!/usr/bin/env bash
set -euo pipefail

# ─── open-skill-forge setup (macOS / Linux) ───

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

PYTHON_VERSION="3.12"
REPO_URL="https://github.com/antonysallas/open-skill-forge.git"
REPO_DIR="$HOME/projects/open-skill-forge"
VENV_DIR="$REPO_DIR/.venv"

info()  { echo -e "${BLUE}▶${NC} $1"; }
ok()    { echo -e "${GREEN}✔${NC} $1"; }
fail()  { echo -e "${RED}✖${NC} $1"; exit 1; }

echo ""
echo "═══════════════════════════════════════════"
echo "  open-skill-forge – Environment Setup"
echo "═══════════════════════════════════════════"
echo ""

# Ensure ~/.local/bin is in PATH (uv installs here)
export PATH="$HOME/.local/bin:$PATH"

# ── 1. Install uv ──
if command -v uv &>/dev/null; then
  ok "uv already installed ($(uv --version))"
else
  info "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  command -v uv &>/dev/null || fail "uv installation failed"
  ok "uv installed ($(uv --version))"
fi

# ── 2. Install Python ──
info "Installing Python ${PYTHON_VERSION} via uv..."
uv python install "$PYTHON_VERSION"
ok "Python ${PYTHON_VERSION} installed"

# ── 3. Clone repository ──
if [ -d "$REPO_DIR/.git" ]; then
  ok "Repository already cloned at $REPO_DIR"
else
  mkdir -p "$(dirname "$REPO_DIR")"
  info "Cloning repository to $REPO_DIR..."
  git clone "$REPO_URL" "$REPO_DIR" </dev/null
  ok "Repository cloned"
fi

# ── 4. Create virtual environment ──
if [ -d "$VENV_DIR" ]; then
  ok "Virtual environment already exists at $VENV_DIR"
else
  info "Creating virtual environment..."
  uv venv --python "$PYTHON_VERSION" "$VENV_DIR"
  ok "Virtual environment created"
fi

# ── 5. Install JupyterLab in venv ──
info "Installing JupyterLab in virtual environment..."
uv pip install --python "$VENV_DIR/bin/python" jupyterlab
ok "JupyterLab installed"

# ── 6. Verify ──
echo ""
echo "═══════════════════════════════════════════"
echo "  Verification"
echo "═══════════════════════════════════════════"
echo ""
echo "  uv:         $(uv --version)"
VENV_PYTHON="$VENV_DIR/bin/python"
echo "  Python:     $($VENV_PYTHON --version)"
echo "  JupyterLab: $($VENV_PYTHON -m jupyterlab --version 2>/dev/null || echo 'installed')"
echo ""

# ── 7. Done ──
ok "Setup complete!"
echo ""
echo "To start JupyterLab, run:"
echo ""
echo "  cd $REPO_DIR/python/notebooks"
echo "  source $VENV_DIR/bin/activate"
echo "  jupyter lab"
echo ""
