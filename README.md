# MongoDB Atlas AI Demo Template

A domain-agnostic scaffold for building MongoDB Atlas AI demos. Built on a
FastAPI + React/Vite/TypeScript + Docker Compose stack with Voyage AI
embeddings and Atlas Vector Search.

## What this demonstrates

- **Records embedded in place** — Voyage AI generates a 1024-dim vector from
  each record's `record_text` and writes it directly into the same MongoDB
  document. No separate vector store.
- **Atlas Vector Search with pre-filters** — The `$vectorSearch` aggregation
  stage retrieves semantically relevant knowledge base items and historical
  records, with optional hard MQL filters on metadata fields.
- **AI output written back** — An output generation step synthesizes the
  retrieved context and writes the result back to the same record document,
  updating `processing_status` to `READY_FOR_REVIEW`.

---

## Customizing for a new domain

Open this repo in Claude Code and run:

```
@CUSTOMIZE_PROMPT.md
```

Claude will interview you (6 questions, one message), generate all sample
data, fill in every placeholder, handle your `.env` credentials, and verify
the build — in a single session. The generated content includes a domain-specific
demo script accessible from the **Docs** menu inside the running app.

See [TEMPLATE.md](./TEMPLATE.md) for the manual checklist if you prefer to
customize by hand.

---

## Quick start (after customizing)

```bash
# 1. Ensure .env is filled in (MONGODB_URI + VOYAGE_API_KEY)
cp .env.example .env   # if not already done by the interview

# 2. Seed the database and create Atlas Vector Search indexes
python scripts/setup.py

# 3. Start the app
./start.sh
```

Open http://localhost:5173

The **Docs** menu in the header gives presenters in-app access to the README,
Demo Script, and Runbook without leaving the browser.

---

## Architecture

```
FastAPI (backend/)  +  React/Vite/TS (frontend/)  +  Docker Compose
        |
        ├── /api/records/{scenario}/record   — fetch demo record
        ├── /api/records/{scenario}/embed    — Voyage AI embed + write-back
        ├── /api/search/{scenario}           — Atlas Vector Search
        ├── /api/records/{scenario}/output   — generate output + write-back
        ├── /api/records/reset-all           — soft reset
        └── /api/docs/{readme|script|runbook} — serve markdown docs to UI
```

## Requirements

- MongoDB Atlas cluster (free tier M0 works)
- Voyage AI API key (free tier sufficient for demos)
- Python 3.11+, Node 18+, Docker (optional)
