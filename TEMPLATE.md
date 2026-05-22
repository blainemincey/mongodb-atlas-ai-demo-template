# Atlas AI Demo Template — Manual Customization Reference

> **Faster option:** `python scripts/init_domain.py <domain>` applies a
> pre-built domain pack automatically, then `./setup.sh` handles dependencies
> and database seeding in one command. This checklist is for manual
> customization or for building a new domain pack from scratch.

A reusable scaffold for building MongoDB Atlas AI demos. Preserves a proven
4-step demo workflow while keeping all domain-specific content in clearly
marked `TODO` blocks that you replace for each new demo.

---

## What this is

This template demonstrates how MongoDB Atlas, Voyage AI embeddings, and Atlas
Vector Search work together as a single operational platform. Incoming records
are embedded by Voyage AI and stored alongside the original document in
MongoDB. Vector Search retrieves semantically relevant knowledge base items
and historical examples. An AI output step synthesizes the retrieved context
and writes the result back to the same record — operational data, embeddings,
retrieval, and AI output all in one document, one database.

---

## Architecture

```
                          MongoDB Atlas
                    ┌─────────────────────────┐
                    │                         │
 Domain Record ──── │ records collection      │
 (record_text)      │  └─ record_embedding ◄──┼── Voyage AI embed step
                    │  └─ ai_output           │
                    │  └─ processing_status   │
                    │                         │
                    │ knowledge_base           │
                    │  └─ record_embedding ◄──┼── embedded at setup
                    │  └─ content_text        │◄─┐
                    │                         │  │ Atlas Vector Search
                    │ historical_records       │  │ ($vectorSearch stage)
                    │  └─ record_embedding ◄──┼──┘
                    │  └─ source_text         │
                    └─────────────────────────┘
                               │
                      Retrieved context
                               │
                    Generate Output (llm.py)
                               │
                    Write ai_output back to
                    the same record document
```

---

## Checklist: what to replace for each new demo

- [ ] **`backend/data/demo_records.py`** — Replace stub `record_text` values and
      add domain-specific fields (e.g., `customer_id`, `category`, `amount`).

- [ ] **`backend/data/knowledge_base.py`** — Replace with real reference content
      (rules, policies, documentation, guidelines) for your domain.

- [ ] **`backend/data/historical_records.py`** — Replace with real historical
      examples. Include "anchor" records that will surface for your demo scenarios.

- [ ] **`backend/services/llm.py`** — Customize Option A template output sections,
      or switch to Option B for a real LLM call.

- [ ] **`scripts/setup.py`** — Update `KB_FILTER_FIELDS` and `HIST_FILTER_FIELDS`
      in the config block if you add new filterable fields.

- [ ] **`frontend/src/App.tsx`** — Update `SCENARIO_CONFIG` labels and descriptions
      between the `BEGIN_DOMAIN:scenario_config` / `END_DOMAIN:scenario_config`
      marker comments near the top of the file.

- [ ] **`frontend/src/components/SearchStep.tsx`** — Update filter dropdown options
      between the `BEGIN_DOMAIN:category_options` / `END_DOMAIN:category_options`
      marker comments to match your domain's category values.

- [ ] **`DEMO_SCRIPT.md`** and **`DEMO_RUNBOOK.md`** — Replace `[TODO]` placeholders
      with domain-specific talking points.

---

## Environment variables

| Variable           | Required | Description                                      |
|--------------------|----------|--------------------------------------------------|
| `MONGODB_URI`      | Yes      | Atlas connection string                          |
| `DB_NAME`          | Yes      | Database name (default: `demo_db`)               |
| `DEMO_NAME`        | No       | Display name shown in API docs (default: `Atlas AI Demo`) |
| `VOYAGE_API_KEY`   | Yes      | Voyage AI key for embeddings                     |
| `ANTHROPIC_API_KEY`| No       | Only needed if using Option B in `llm.py`        |
| `BACKEND_HOST`     | No       | Host for uvicorn (default: `0.0.0.0`)            |
| `BACKEND_PORT`     | No       | Port for uvicorn (default: `8000`)               |
| `CORS_ORIGIN`      | No       | Allowed CORS origin (default: `http://localhost:5173`) |

---

## Atlas Vector Search index setup

Indexes are created automatically by `scripts/setup.py`. Two indexes are
required for the demo to function:

- **`kb_vector_index`** — on the `knowledge_base` collection, vector path
  `record_embedding`, filter fields: `category`, `subcategory`
- **`historical_vector_index`** — on the `historical_records` collection,
  vector path `record_embedding`, filter fields: `category`, `outcome`

If you add new filter fields to your data (e.g., `region`, `status`), add
them to `KB_FILTER_FIELDS` or `HIST_FILTER_FIELDS` in the setup.py config
block. The index definition is built from those lists — the filter fields in
the index definition must match the fields you pass to `$vectorSearch filter`.

---

## Option A vs Option B in llm.py

**Option A** (default): Template-driven output. Assembles a structured text
response from the retrieved context using f-strings. No extra API key required
beyond Voyage AI and MongoDB. Good for demos where the output format is fixed.

**Option B** (commented out): LLM call via the Anthropic SDK. Sends the record
text and retrieved context as a user message to `claude-sonnet-4-6`. Requires
`ANTHROPIC_API_KEY` in `.env` and `anthropic_api_key: str` added to
`backend/config.py`. Good for demos where open-ended natural language output
adds value.

To switch: uncomment the Option B block in `backend/services/llm.py` and
comment out the Option A block.
