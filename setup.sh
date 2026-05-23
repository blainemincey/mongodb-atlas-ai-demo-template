#!/usr/bin/env bash
# =============================================================================
# Atlas AI Demo — First-Run Setup
# =============================================================================
# Idempotent: safe to re-run. Already-installed deps and seeded data are
# skipped automatically.
#
# Usage:
#   ./setup.sh              — install deps + configure .env + seed database
#   ./setup.sh --deps-only  — install deps and configure .env only (skip
#                             setup.py — useful when credentials aren't
#                             ready yet)
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DEPS_ONLY=0
for arg in "$@"; do
  case "$arg" in
    --deps-only) DEPS_ONLY=1 ;;
    *) echo "Usage: $0 [--deps-only]"; exit 1 ;;
  esac
done

# ── Helpers ───────────────────────────────────────────────────────────────────
step() {
  echo ""
  echo "────────────────────────────────────────────────────────────"
  echo "  $1"
  echo "────────────────────────────────────────────────────────────"
}
log() { echo "  $1"; }
ok()  { echo "  [OK] $1"; }
err() { echo "" ; echo "  ERROR: $1" >&2; exit 1; }

# Read a single value from .env (strips surrounding quotes)
_read_env() {
  grep "^$1=" .env 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'"
}

# Returns 0 (true) if the value looks like a placeholder
_is_placeholder() {
  [[ -z "$1" ]] || \
  [[ "$1" == *"USERNAME:PASSWORD"* ]] || \
  [[ "$1" == *"YOUR-CLUSTER"* ]] || \
  [[ "$1" == *"xxxxxxxx"* ]]
}

# Patch a KEY=value line in .env (safe for URIs with @/:)
_patch_env() {
  local field="$1"
  local value="$2"
  python3 - "$field" "$value" <<'PYEOF'
import re, sys
field, value = sys.argv[1], sys.argv[2]
with open('.env') as f:
    c = f.read()
c = re.sub(r'^' + re.escape(field) + r'=.*$', field + '=' + value, c, flags=re.MULTILINE)
with open('.env', 'w') as f:
    f.write(c)
PYEOF
}

echo ""
echo "============================================================"
echo "  Atlas AI Demo — Setup"
echo "============================================================"

# ── Step 1: Prerequisites ─────────────────────────────────────────────────────
step "Step 1: Checking prerequisites"

if ! command -v python3 &>/dev/null; then
  err "python3 not found. Install Python 3.11 or later."
fi
PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 11 ]; }; then
  err "Python 3.11+ required. Found: Python $PY_VER"
fi
if [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -ge 14 ]; then
  err "Python $PY_VER is not yet supported. Several dependencies (pydantic-core,
  voyageai) require native extensions built with PyO3, which does not yet have
  pre-built wheels for Python 3.14. Use Python 3.11, 3.12, or 3.13.
  Tip: pyenv install 3.13 && pyenv local 3.13"
fi
ok "Python $PY_VER"

if ! command -v node &>/dev/null; then
  err "node not found. Install Node.js 18 or later (https://nodejs.org)."
fi
NODE_VER=$(node --version | sed 's/v//')
NODE_MAJOR=$(echo "$NODE_VER" | cut -d. -f1)
if [ "$NODE_MAJOR" -lt 18 ]; then
  err "Node.js 18+ required. Found: $NODE_VER"
fi
ok "Node $NODE_VER"

if ! command -v npm &>/dev/null; then
  err "npm not found. Install Node.js 18 or later (https://nodejs.org)."
fi
ok "npm $(npm --version)"

# ── Step 2: Python venv + dependencies ───────────────────────────────────────
step "Step 2: Python environment"

if [ ! -d "backend/.venv" ]; then
  log "Creating virtual environment..."
  python3 -m venv backend/.venv
  ok "Created backend/.venv"
else
  ok "Virtual environment already exists"
fi

log "Installing Python dependencies..."
backend/.venv/bin/pip install --quiet --upgrade pip
backend/.venv/bin/pip install --quiet -r backend/requirements.txt
ok "Requirements installed"

# ── Step 3: Frontend dependencies ────────────────────────────────────────────
step "Step 3: Frontend dependencies"

if [ ! -d "frontend/node_modules" ]; then
  log "Running npm install (this may take a minute)..."
  (cd frontend && npm install --silent)
  ok "npm install complete"
else
  ok "node_modules already installed"
fi

# ── Step 4: Environment configuration ────────────────────────────────────────
step "Step 4: Environment configuration"

if [ ! -f ".env" ]; then
  cp .env.example .env
  log "Created .env from .env.example"
else
  ok ".env exists"
fi

MONGODB_URI=$(_read_env MONGODB_URI)
VOYAGE_KEY=$(_read_env VOYAGE_API_KEY)

NEEDS_CREDS=0
if _is_placeholder "$MONGODB_URI"; then NEEDS_CREDS=1; fi
if _is_placeholder "$VOYAGE_KEY";  then NEEDS_CREDS=1; fi

if [ "$NEEDS_CREDS" -eq 1 ]; then
  echo ""
  echo "  Your .env needs credentials before the demo can run."
  echo ""

  if _is_placeholder "$MONGODB_URI"; then
    echo "  MongoDB Atlas connection string"
    echo "  Where to get it: Atlas UI → your cluster → Connect → Drivers"
    echo "  It looks like: mongodb+srv://user:pass@cluster.mongodb.net/..."
    echo ""
    read -r -p "  Paste MONGODB_URI (Enter to skip for now): " NEW_URI
    if [ -n "$NEW_URI" ]; then
      _patch_env MONGODB_URI "$NEW_URI"
      ok "MONGODB_URI saved to .env"
    else
      log "Skipped — add MONGODB_URI to .env before running setup.py"
    fi
    echo ""
  fi

  if _is_placeholder "$VOYAGE_KEY"; then
    echo "  Voyage AI API key"
    echo "  Where to get it: https://dash.voyageai.com/api-keys (free tier is enough)"
    echo ""
    read -r -p "  Paste VOYAGE_API_KEY (Enter to skip for now): " NEW_KEY
    if [ -n "$NEW_KEY" ]; then
      _patch_env VOYAGE_API_KEY "$NEW_KEY"
      ok "VOYAGE_API_KEY saved to .env"
    else
      log "Skipped — add VOYAGE_API_KEY to .env before running setup.py"
    fi
  fi
else
  ok "Credentials configured"
fi

# Re-read after possible updates
MONGODB_URI=$(_read_env MONGODB_URI)
VOYAGE_KEY=$(_read_env VOYAGE_API_KEY)

READY=1
if _is_placeholder "$MONGODB_URI"; then READY=0; fi
if _is_placeholder "$VOYAGE_KEY";  then READY=0; fi

# ── Early exit if --deps-only ─────────────────────────────────────────────────
if [ "$DEPS_ONLY" -eq 1 ]; then
  echo ""
  echo "============================================================"
  echo "  Dependencies installed."
  echo "============================================================"
  if [ "$READY" -eq 0 ]; then
    echo ""
    echo "  Still needed: fill in MONGODB_URI and/or VOYAGE_API_KEY in .env"
  fi
  echo ""
  echo "  When credentials are ready:"
  echo "    python scripts/setup.py   — seed data + create vector search indexes"
  echo "    ./start.sh                — start the demo"
  echo ""
  exit 0
fi

# ── Step 5: Seed database ─────────────────────────────────────────────────────
if [ "$READY" -eq 0 ]; then
  echo ""
  echo "============================================================"
  echo "  Setup paused — credentials not fully configured."
  echo "============================================================"
  echo ""
  echo "  Edit .env and fill in the missing values, then run:"
  echo "    python scripts/setup.py   — seed data + create vector search indexes"
  echo "    ./start.sh                — start the demo"
  echo ""
  exit 0
fi

step "Step 5: Seeding database and creating vector search indexes"
backend/.venv/bin/python scripts/setup.py

echo ""
echo "============================================================"
echo "  Setup complete."
echo "============================================================"
echo ""
echo "  Start the demo:  ./start.sh"
echo "  Open:            http://localhost:5173"
echo ""
