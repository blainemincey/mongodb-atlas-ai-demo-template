# Demo Runbook — Operator Reference

[TODO: Fill in domain-specific setup details before presenting.]

---

## Pre-demo checklist

- [ ] `.env` file present at repo root with `MONGODB_URI`, `VOYAGE_API_KEY`, `DEMO_NAME`
- [ ] `python scripts/setup.py` completed successfully (all indexes READY)
- [ ] `./start.sh` running — backend on :8000, frontend on :5173
- [ ] http://localhost:5173 loads without errors in browser
- [ ] All three scenarios (A, B, C) load records without 404 errors
- [ ] [TODO: Add domain-specific pre-checks here]

---

## Setup

```bash
# 1. Install dependencies
cd backend && pip install -r requirements.txt && cd ..
cd frontend && npm install && cd ..

# 2. Configure environment
cp .env.example .env
# Edit .env: fill in MONGODB_URI and VOYAGE_API_KEY

# 3. Seed database and create indexes
python scripts/setup.py

# 4. Start services
./start.sh
```

---

## Reset between runs

**Soft reset (recommended)** — clears AI output, preserves embeddings:
```bash
python scripts/reset_demo.py
```
Or use the Reset button in the UI header.

**Hard reset** — clears everything including embeddings (slower, re-calls Voyage AI):
```bash
python scripts/reset_demo.py --hard
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| 404 on scenario load | setup.py not run or collection empty | Run `python scripts/setup.py` |
| "no embedding yet" error on search | Step 2 skipped | Click Embed on the record first |
| Vector search returns 0 results | Index not READY | Wait for index build; check Atlas UI |
| `VOYAGE_API_KEY` error | Missing env var | Check `.env` file |
| CORS error in browser | Backend not running | Check `./start.sh` output |
| [TODO: domain-specific issue] | [TODO: cause] | [TODO: fix] |

---

## Key URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |
| Atlas UI | https://cloud.mongodb.com |

---

## Configuration block (scripts/setup.py)

Edit the block at the top of `scripts/setup.py` to change collection names,
index names, filter fields, or embedding field names without modifying the rest
of the script.

---

## Notes

[TODO: Add domain-specific operational notes, edge cases, or presenter tips here.]
