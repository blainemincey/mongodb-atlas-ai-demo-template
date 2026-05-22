# Demo Runbook — Operator Reference

---

## Pre-demo checklist

- [ ] Domain pack applied (`python scripts/init_domain.py <domain>`) or custom
      data files in place under `backend/data/`
- [ ] `.env` present at repo root with real (non-placeholder) `MONGODB_URI`,
      `VOYAGE_API_KEY`, and `DEMO_NAME`
- [ ] `./setup.sh` completed successfully — all indexes READY
- [ ] `./start.sh` running — backend on :8000, frontend on :5173
- [ ] http://localhost:5173 loads without errors in browser
- [ ] All three scenarios (A, B, C) load records without 404 errors
- [ ] Verify scenario titles in the UI match the domain you applied

---

## Setup

```bash
# 1. Apply a domain pack
python scripts/init_domain.py --list          # see available domains
python scripts/init_domain.py <domain-name>   # e.g. it-support, mortgage
# Claude Code alternative: /init-domain (interactive) or /init-domain <domain>

# 2. Install dependencies, configure .env, and seed the database
./setup.sh
# This script:
#   - Checks Python 3.11+ and Node 18+
#   - Creates backend/.venv and installs pip dependencies
#   - Runs npm install in frontend/
#   - Copies .env.example → .env (if missing) and prompts for credentials
#   - Runs scripts/setup.py to seed data and create Atlas Vector Search indexes
#
# Claude Code alternative: /setup
#
# If you prefer to do steps manually:
#   cp .env.example .env            # then fill in MONGODB_URI and VOYAGE_API_KEY
#   python3 -m venv backend/.venv && backend/.venv/bin/pip install -r backend/requirements.txt
#   cd frontend && npm install && cd ..
#   backend/.venv/bin/python scripts/setup.py
#   Note: python-dotenv and other deps live in the venv — running
#   `python scripts/setup.py` directly (system Python) will fail with
#   ModuleNotFoundError. Use backend/.venv/bin/python or just run ./setup.sh.

# 3. Start services
./start.sh
```

---

## Reset between runs

**Soft reset (recommended)** — clears AI output, preserves embeddings:
```bash
python scripts/reset_demo.py
```
Or use the **Reset Demo** button in the UI header.

**Hard reset** — clears everything including embeddings (slower; re-calls Voyage AI):
```bash
python scripts/reset_demo.py --hard
```

**Reset then restart in one command:**
```bash
./start.sh --reset       # soft
./start.sh --reset-hard  # hard
```

---

## Switching domains between sessions

Each domain uses its own database. To switch:

```bash
python scripts/init_domain.py <new-domain>   # patches data files + .env
# Claude Code alternative: /init-domain <new-domain>
./setup.sh                                   # seeds the new database
# Claude Code alternative: /setup
./start.sh
```

The previous domain's database is untouched in Atlas — point `DB_NAME`
back to it in `.env` to restore.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| 404 on scenario load | `setup.py` not run or collection empty | `./setup.sh` or `/setup` |
| Scenario titles show `[TODO]` | Domain pack not applied | `python scripts/init_domain.py <domain>` |
| "no embedding yet" error on search | Step 2 skipped | Click Embed on the record first |
| Vector search returns 0 results | Index not READY | Wait for index build; check Atlas UI |
| Vector search returns wrong category | Category options in UI don't match KB data | Re-run `init_domain.py` to patch `SearchStep.tsx` |
| `VOYAGE_API_KEY` error | Missing or placeholder env var | Run `./setup.sh` to set credentials |
| CORS error in browser | Backend not running or wrong port | Check `backend.log`; verify `BACKEND_PORT` in `.env` |
| `ModuleNotFoundError` on startup | Python deps not installed | `./setup.sh --deps-only` |
| Backend didn't start within 30s | uvicorn error at launch | `tail -f backend.log` for details |

---

## Key URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |
| Health check | http://localhost:8000/api/health |
| Atlas UI | https://cloud.mongodb.com |
| Voyage AI dashboard | https://dash.voyageai.com |

---

## Configuration reference (scripts/setup.py)

The config block at the top of `scripts/setup.py` controls collection names,
index names, filter fields, and embedding field names. Edit it if you add new
filterable fields to your data.

Key variables:
- `KB_FILTER_FIELDS` — fields added as filter paths to `kb_vector_index`
- `HIST_FILTER_FIELDS` — fields added as filter paths to `historical_vector_index`

Filter fields in the index definition must match exactly what you pass to
`$vectorSearch filter` in the search router.

---

## Docker path (no Python venv required)

If Docker is available, the full stack can be run without installing Python
or Node locally:

```bash
python scripts/init_domain.py <domain>  # still needs Python for init
cp .env.example .env                    # fill in credentials
docker compose up --build
```

Open http://localhost:5173. The frontend waits for the backend health check
before starting, so there's no race on first boot.
