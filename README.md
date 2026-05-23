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

## Pre-built domain packs

Six domains are included and ready to run. Apply one in seconds:

```bash
python scripts/init_domain.py --list        # see all domains
python scripts/init_domain.py it-support    # apply a domain
```

If you're working in Claude Code, the `/init-domain` slash command wraps the
same script interactively:

```
/init-domain              # list domains and pick one
/init-domain it-support   # apply directly
```

| Domain | Scenarios | Outcomes |
|--------|-----------|---------|
| `healthcare` | Medical imaging · Specialty pharmacy · Behavioral health | APPROVED / DENIED / PEND_FOR_REVIEW |
| `insurance-claims` | Auto collision · Property water damage · Total loss | APPROVED / DENIED / NEEDS_INVESTIGATION |
| `it-support` | Hardware failure · ERP crash · VPN outage | RESOLVED / ESCALATED / CLOSED_NO_ACTION |
| `legal-contracts` | Liability cap · Indemnification · IP assignment | ACCEPTABLE / FLAG_FOR_REVISION / ESCALATE_TO_COUNSEL |
| `mortgage` | Strong conventional · Borderline FHA · Jumbo asset depletion | APPROVED / DENIED / REFER_TO_SENIOR_UNDERWRITER |
| `retail-support` | Electronics return · Apparel defect · Appliance refund | APPROVE / DENY / ESCALATE |

---

## Quick start (local)

```bash
# 1. Apply a domain pack
python scripts/init_domain.py it-support

# 2. Install dependencies + configure credentials
./setup.sh
#    Creates backend/.venv, installs pip + npm deps, copies .env.example → .env,
#    and prompts for your MongoDB URI and Voyage AI API key.
#    Run ./setup.sh --deps-only to install without seeding the database.

# 3. Start the app
./start.sh
```

Open http://localhost:5173

If you're using Claude Code, `/init-domain` and `/setup` slash commands drive
both steps interactively without leaving your editor.

The **Docs** menu in the header gives presenters in-app access to the README,
Demo Script, and Runbook without leaving the browser.

---

## Quick start (Docker)

No Python venv or `npm install` required — Docker handles the build.

```bash
# 1. Apply a domain pack (still needs Python for the init script)
python scripts/init_domain.py it-support

# 2. Configure credentials
cp .env.example .env
# Edit .env: fill in MONGODB_URI and VOYAGE_API_KEY

# 3. Build and start
docker compose up --build
```

Open http://localhost:5173

The frontend container waits for the backend health check to pass before
starting, so there's no race condition on first boot.

---

## Custom domain

To build a demo for a domain not in the list above, open this repo in
Claude Code and run:

```
@CUSTOMIZE_PROMPT.md
```

Claude will offer the domain pack list first, then — if none fit — interview
you (6 questions, one message), generate all sample data, fill in every
placeholder, handle your `.env` credentials, and verify the build. The output
includes a domain-specific demo script accessible from the **Docs** menu
inside the running app.

See [TEMPLATE.md](./TEMPLATE.md) for the manual checklist if you prefer to
customize by hand.

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
        ├── /api/health                      — health check
        └── /api/docs/{readme|script|runbook} — serve markdown docs to UI
```

## Requirements

- MongoDB Atlas cluster (free tier M0 works)
- Voyage AI API key (free tier sufficient for demos)
- **Local path:** Python 3.11–3.14, Node 18+
  (Python 3.14: `voyageai` metadata caps at `<3.14` but is pure Python — `setup.sh` handles it automatically)
- **Docker path:** Docker with Compose plugin
