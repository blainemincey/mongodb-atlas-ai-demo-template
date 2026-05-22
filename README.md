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

## Quick start

```bash
cp .env.example .env
# Edit .env — fill in MONGODB_URI and VOYAGE_API_KEY

python scripts/setup.py   # creates collections, indexes, seeds data
./start.sh                # starts backend + frontend
```

Open http://localhost:5173

## Adapting this template

See [TEMPLATE.md](./TEMPLATE.md) for the full checklist of what to replace
when building a new domain-specific demo.

## Architecture

```
FastAPI (backend/)  +  React/Vite/TS (frontend/)  +  Docker Compose
        |
        ├── /api/records/{scenario}/record   — fetch demo record
        ├── /api/records/{scenario}/embed    — Voyage AI embed + write-back
        ├── /api/search/{scenario}           — Atlas Vector Search
        ├── /api/records/{scenario}/output   — generate output + write-back
        └── /api/records/reset-all           — soft reset
```

## Requirements

- MongoDB Atlas cluster (free tier M0 works)
- Voyage AI API key (free tier sufficient for demos)
- Python 3.11+, Node 18+, Docker (optional)
