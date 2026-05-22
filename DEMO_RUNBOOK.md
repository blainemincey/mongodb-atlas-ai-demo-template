# Demo Runbook — Operator Reference

---

## Pre-demo checklist

- [ ] Domain pack applied (`python scripts/init_domain.py <domain>`) or custom
      data files in place under `backend/data/`
- [ ] `.env` file present at repo root with `MONGODB_URI`, `VOYAGE_API_KEY`, `DEMO_NAME`
- [ ] `python scripts/setup.py` completed successfully (all indexes READY)
- [ ] `./start.sh` running — backend on :8000, frontend on :5173
- [ ] http://localhost:5173 loads without errors in browser
- [ ] All three scenarios (A, B, C) load records without 404 errors
- [ ] Verify scenario titles in the UI match the domain you applied

---

## Setup

```bash
# 1. Apply a domain pack (skip if you've already customized manually)
python scripts/init_domain.py --list          # see available domains
python scripts/init_domain.py <domain-name>   # e.g. it-support, mortgage
# Claude Code alternative: /init-domain (interactive) or /init-domain <domain-name>

# 2. Install dependencies
cd backend && pip install -r requirements.txt && cd ..
cd frontend && npm install && cd ..

# 3. Configure environment
cp .env.example .env
# Edit .env: fill in MONGODB_URI and VOYAGE_API_KEY
# (init_domain.py sets DEMO_NAME and DB_NAME automatically)

# 4. Seed database and create indexes
python scripts/setup.py

# 5. Start services
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

---

## Switching domains between sessions

Each domain uses its own database. To switch:

```bash
python scripts/init_domain.py <new-domain>   # patches data files + .env
# Claude Code alternative: /init-domain <new-domain>
python scripts/setup.py                      # seeds the new database
./start.sh
```

The previous domain's database is untouched in Atlas — just point `DB_NAME`
back to it in `.env` to restore.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| 404 on scenario load | `setup.py` not run or collection empty | Run `python scripts/setup.py` |
| Scenario titles show `[TODO]` | Domain pack not applied | Run `python scripts/init_domain.py <domain>` |
| "no embedding yet" error on search | Step 2 skipped | Click Embed on the record first |
| Vector search returns 0 results | Index not READY | Wait for index build; check Atlas UI |
| Vector search returns wrong category | Category options in UI don't match KB data | Re-run `init_domain.py` to patch `SearchStep.tsx` |
| `VOYAGE_API_KEY` error | Missing env var | Check `.env` file |
| CORS error in browser | Backend not running | Check `./start.sh` output |
| `ModuleNotFoundError: voyageai` | Python deps not installed | `cd backend && pip install -r requirements.txt` |

---

## Key URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |
| Atlas UI | https://cloud.mongodb.com |
| Voyage AI dashboard | https://dash.voyageai.com |

---

## Configuration reference (scripts/setup.py)

The config block at the top of `scripts/setup.py` controls collection names,
index names, filter fields, and embedding field names. Edit it if you add new
filterable fields to your data.

Key variables:
- `KB_FILTER_FIELDS` — fields added as filter paths to the `kb_vector_index`
- `HIST_FILTER_FIELDS` — fields added as filter paths to `historical_vector_index`

Filter fields in the index definition must match exactly what you pass to
`$vectorSearch filter` in the search router.
