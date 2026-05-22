#!/usr/bin/env bash
# =============================================================================
# Atlas AI Demo — Start/Stop Script
#
# Usage:
#   ./start.sh               — start backend + frontend
#   ./start.sh --reset       — soft reset (keep embeddings), then start
#   ./start.sh --reset-hard  — full reset (clear embeddings too), then start
#   ./start.sh --stop        — stop running services
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PID_FILE="$SCRIPT_DIR/.demo.pids"

# ── Parse flags ───────────────────────────────────────────────────────────────
RESET=0
RESET_HARD=0
STOP=0
for arg in "$@"; do
  case "$arg" in
    --reset|-r)   RESET=1 ;;
    --reset-hard) RESET=1; RESET_HARD=1 ;;
    --stop|-s)    STOP=1 ;;
    *) echo "Usage: $0 [--reset | --reset-hard | --stop]"; exit 1 ;;
  esac
done

# ── Read config from .env ─────────────────────────────────────────────────────
_read_env() {
  grep "^$1=" .env 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'"
}

BACKEND_PORT=8000
FRONTEND_PORT=5173
DEMO_NAME="Atlas AI Demo"

if [ -f ".env" ]; then
  _p=$(_read_env BACKEND_PORT);  [ -n "$_p" ] && BACKEND_PORT=$_p
  _p=$(_read_env FRONTEND_PORT); [ -n "$_p" ] && FRONTEND_PORT=$_p
  _p=$(_read_env DEMO_NAME);     [ -n "$_p" ] && DEMO_NAME=$_p
fi

# ── Helpers ───────────────────────────────────────────────────────────────────
_is_placeholder() {
  [[ -z "$1" ]] || \
  [[ "$1" == *"USERNAME:PASSWORD"* ]] || \
  [[ "$1" == *"YOUR-CLUSTER"* ]] || \
  [[ "$1" == *"xxxxxxxx"* ]]
}

# ── Stop ──────────────────────────────────────────────────────────────────────
stop_services() {
  if [ -f "$PID_FILE" ]; then
    # shellcheck disable=SC1090
    source "$PID_FILE"
    echo "  Stopping backend  (pid $BACKEND_PID)..."
    kill -- "-$(ps -o pgid= -p "$BACKEND_PID"  2>/dev/null | tr -d ' ')" 2>/dev/null \
      || kill "$BACKEND_PID"  2>/dev/null || true
    echo "  Stopping frontend (pid $FRONTEND_PID)..."
    kill -- "-$(ps -o pgid= -p "$FRONTEND_PID" 2>/dev/null | tr -d ' ')" 2>/dev/null \
      || kill "$FRONTEND_PID" 2>/dev/null || true
    sleep 1
    rm -f "$PID_FILE"
  else
    echo "  No PID file found — stopping by port..."
    fuser -k "${BACKEND_PORT}/tcp"  2>/dev/null || true
    fuser -k "${FRONTEND_PORT}/tcp" 2>/dev/null || true
    sleep 1
  fi
  echo "  Done."
}

if [ "$STOP" -eq 1 ]; then
  echo ""
  echo "============================================================"
  echo "  $DEMO_NAME — Stopping"
  echo "============================================================"
  echo ""
  stop_services
  echo ""
  exit 0
fi

# ── Preflight checks ──────────────────────────────────────────────────────────
if [ ! -f ".env" ]; then
  echo ""
  echo "  ERROR: .env not found."
  echo "  Run ./setup.sh to configure the project, or:"
  echo "    cp .env.example .env  and fill in your credentials."
  exit 1
fi

if [ ! -d "backend/.venv" ]; then
  echo ""
  echo "  ERROR: Python virtual environment not found (backend/.venv)."
  echo "  Run ./setup.sh to install dependencies."
  exit 1
fi

if [ ! -d "frontend/node_modules" ]; then
  echo ""
  echo "  ERROR: Frontend dependencies not installed (frontend/node_modules)."
  echo "  Run ./setup.sh to install dependencies."
  exit 1
fi

MONGODB_URI=$(_read_env MONGODB_URI)
VOYAGE_KEY=$(_read_env VOYAGE_API_KEY)
if _is_placeholder "$MONGODB_URI" || _is_placeholder "$VOYAGE_KEY"; then
  echo ""
  echo "  ERROR: .env has placeholder credentials."
  echo "  Run ./setup.sh to configure MONGODB_URI and VOYAGE_API_KEY."
  exit 1
fi

# ── Stop any already-running instance ─────────────────────────────────────────
if [ -f "$PID_FILE" ]; then
  echo "  Stopping previous instance..."
  stop_services
  sleep 1
fi

echo ""
echo "============================================================"
echo "  $DEMO_NAME — Starting"
echo "============================================================"
echo ""

# ── Optional reset ────────────────────────────────────────────────────────────
if [ "$RESET" -eq 1 ]; then
  cd backend
  if [ -d ".venv/bin" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
  fi
  if [ "$RESET_HARD" -eq 1 ]; then
    echo "  Resetting demo records (hard — embedding + output cleared)..."
    python ../scripts/reset_demo.py --hard
  else
    echo "  Resetting demo records (soft — output cleared, embeddings kept)..."
    python ../scripts/reset_demo.py
  fi
  cd "$SCRIPT_DIR"
  echo ""
fi

# ── Backend ───────────────────────────────────────────────────────────────────
echo "  [1/2] Starting FastAPI backend on http://localhost:${BACKEND_PORT} ..."
cd backend
if [ -d ".venv/bin" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
uvicorn main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload \
  >> "$SCRIPT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
cd "$SCRIPT_DIR"

# Poll /api/health instead of a fixed sleep
MAX_WAIT=30
COUNT=0
printf "  Waiting for backend"
until curl -sf "http://localhost:${BACKEND_PORT}/api/health" > /dev/null 2>&1; do
  COUNT=$((COUNT + 1))
  if [ "$COUNT" -ge "$MAX_WAIT" ]; then
    echo ""
    echo ""
    echo "  ERROR: backend did not start within ${MAX_WAIT}s."
    echo "  Check backend.log for details:  tail -f backend.log"
    kill "$BACKEND_PID" 2>/dev/null || true
    exit 1
  fi
  printf "."
  sleep 1
done
echo " ready."

# ── Frontend ──────────────────────────────────────────────────────────────────
echo "  [2/2] Starting Vite frontend on http://localhost:${FRONTEND_PORT} ..."
cd frontend
npm run dev -- --host \
  >> "$SCRIPT_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
cd "$SCRIPT_DIR"

# Save PIDs for --stop
echo "BACKEND_PID=$BACKEND_PID"   > "$PID_FILE"
echo "FRONTEND_PID=$FRONTEND_PID" >> "$PID_FILE"

echo ""
echo "============================================================"
echo "  Demo running:"
echo "    Frontend: http://localhost:${FRONTEND_PORT}"
echo "    Backend:  http://localhost:${BACKEND_PORT}"
echo "    API docs: http://localhost:${BACKEND_PORT}/docs"
echo ""
echo "  Logs:     tail -f backend.log  |  tail -f frontend.log"
echo "  Reset:    ./start.sh --reset"
echo "  Stop:     ./start.sh --stop   (or Ctrl+C)"
echo "============================================================"
echo ""

# ── Cleanup on exit ───────────────────────────────────────────────────────────
cleanup() {
  echo ""
  echo "  Stopping demo..."
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
  wait "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
  rm -f "$PID_FILE"
  echo "  Done."
}
trap cleanup INT TERM

wait "$BACKEND_PID" "$FRONTEND_PID"
