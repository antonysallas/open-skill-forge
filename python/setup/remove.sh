#!/usr/bin/env bash
set -euo pipefail

# ─── open-skill-forge removal (macOS / Linux) ───

FORCE=false
[[ "${1:-}" == "--force" ]] && FORCE=true

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m'

info()  { echo -e "${BLUE}▶${NC} $1"; }
ok()    { echo -e "${GREEN}✔${NC} $1"; }
warn()  { echo -e "${YELLOW}⚠${NC} $1"; }

echo ""
echo "═══════════════════════════════════════════"
echo "  open-skill-forge – Environment Removal"
echo "═══════════════════════════════════════════"
echo ""
REPO_DIR="$HOME/projects/open-skill-forge"

echo "This will remove the virtual environment, cloned repository,"
echo "uv-managed Python, and uv."
echo ""
if [[ "$FORCE" != true ]]; then
  read -rp "Continue? (y/N) " confirm
  [[ "$confirm" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }
fi
echo ""

# ── 1. Remove cloned repository (includes venv) ──
if [ -d "$REPO_DIR" ]; then
  info "Removing $REPO_DIR..."
  rm -rf "$REPO_DIR"
  ok "Repository and virtual environment removed"
else
  warn "Repository not found at $REPO_DIR"
fi

# ── 2. Remove uv-managed Python installations ──
if command -v uv &>/dev/null; then
  info "Removing uv-managed Python installations..."
  uv python uninstall --all 2>/dev/null && ok "Python installations removed" || warn "No Python installations found"
fi

# ── 3. Remove uv ──
info "Removing uv..."
rm -f "$HOME/.local/bin/uv" "$HOME/.local/bin/uvx"
rm -rf "$HOME/.local/share/uv"
rm -rf "$HOME/.cache/uv"
ok "uv removed"

echo ""
echo "═══════════════════════════════════════════"
echo "  Removal complete"
echo "═══════════════════════════════════════════"
echo ""
ok "All open-skill-forge components have been removed."
echo ""
