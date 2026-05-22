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
python scripts/setup.py                     # seed data + create indexes
./start.sh                                  # start the app
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

`init_domain.py` copies the domain's data files into place, patches the
frontend scenario config, updates `.env`, and prints the next steps.

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

## Quick start

```bash
# 1. Apply a domain pack
#    Shell:       python scripts/init_domain.py it-support
#    Claude Code: /init-domain it-support
python scripts/init_domain.py it-support

# 2. Configure credentials
cp .env.example .env
# Edit .env: fill in MONGODB_URI and VOYAGE_API_KEY

# 3. Seed the database and create Atlas Vector Search indexes
python scripts/setup.py

# 4. Start the app
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
