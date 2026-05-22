# Template Implementation Prompt

Paste this prompt into Claude Code when you open this repo to execute the
template transformation. It captures all decisions made during the planning
session so you can proceed without re-explaining context.

---

## Prompt to paste

This repo is a copy of a working healthcare claims demo built on MongoDB Atlas
+ Voyage AI + Atlas Vector Search. The goal is to transform it into a clean,
domain-agnostic scaffold that can be used to build new demo apps for different
domains and datasets, while keeping the full architectural pattern intact.

The architecture to preserve:

- FastAPI backend + React/Vite/TypeScript frontend + Docker Compose
- 4-step demo workflow: Load Record → Embed (Voyage AI) → Vector Search (Atlas) → Generate Output
- Two supporting collections searched in parallel: knowledge_base + historical_records
- Scenario A/B/C structure for showing multiple use cases
- Voyage AI (voyage-3, 1024-dim) for embeddings stored directly in MongoDB documents
- Atlas Vector Search with optional MQL pre-filters
- Markdown docs viewer in header (keep as-is)
- setup.py + reset_demo.py scripts pattern
- Docker Compose for local dev and deployment

Decisions already made:
- Embedding field name: `record_embedding` (was `clinical_embedding`)
- Collection names: `records`, `knowledge_base`, `historical_records` (were `claims`, `policies`, `prior_claims`)
- Endpoint prefix: `/api/records` (was `/api/claims`)
- Generic field name for the text that gets embedded: `record_text` (was `clinical_notes`)

### Work to do — execute each section in order

---

#### 1. backend/config.py

- Add `DEMO_NAME: str = "Atlas AI Demo"` setting
- Change `db_name` default from `"healthcare_demo"` to `"demo_db"`
- No other changes

---

#### 2. backend/data/ — replace all three files with domain-agnostic stubs

Replace `demo_claims.py` with `demo_records.py`:
- Same dict structure pattern
- Generic field names: `record_id`, `scenario`, `demo_record: True`, `record_text` (this is the field that gets embedded), `record_embedding` (starts as None/absent)
- Include Scenario A, B, C stubs with clear TODO comments indicating what domain-specific fields to add
- Keep `record_id` naming like `REC-001-A`, `REC-001-B`, `REC-001-C`
- Add a prominent docstring explaining what fields are required vs optional

Replace `policies.py` with `knowledge_base.py`:
- Generic fields: `kb_id`, `title`, `category`, `subcategory`, `content_text` (the field that gets embedded), `kb_embedding`
- Include 3-5 stub records with TODO comments
- Docstring explaining this is the reference/policy/rules collection

Replace `prior_claims.py` with `historical_records.py`:
- Generic fields: `record_id`, `category`, `outcome`, `outcome_rationale`, `source_text` (the field that gets embedded), `source_embedding`
- Include 3-5 stub records with TODO comments
- Docstring explaining this is the historical examples collection

Delete `backend/data/__init__.py` content (keep file, clear imports to match new filenames).

---

#### 3. backend/services/vector_search.py

Replace the two healthcare-specific search functions with generic equivalents:

- Rename `search_policies` → `search_knowledge_base`
- Rename `search_prior_claims` → `search_historical_records`
- Replace hardcoded index names `POLICIES_INDEX` / `PRIOR_CLAIMS_INDEX` with `KB_INDEX = "kb_vector_index"` and `HIST_INDEX = "historical_vector_index"`
- Replace hardcoded embedding path `"clinical_embedding"` with `"record_embedding"` in both functions
- Replace healthcare-specific `$project` fields with generic ones matching the new data shapes from step 2
- Keep the pre-filter pattern (filter_clauses dict + optional MQL filter in the vectorSearch stage) — just make the filter field names generic (`category` instead of `clinical_area`, `outcome` instead of `adjudication_outcome`)
- Keep `NUM_CANDIDATES = 80` and the cosine similarity approach

---

#### 4. backend/services/llm.py

Replace the entire file with a clean stub that supports two modes — template
engine or LLM call. The new file should:

- Have a single entry point: `generate_output(record: dict, knowledge_items: list[dict], historical_records: list[dict], timestamp: str) -> str`
- Include two clearly labeled implementation blocks inside the function body:
  - **OPTION A — Template engine** (uncommented/active by default): builds a plain-text structured output using f-strings from the retrieved context, no external API calls. Should reference `record.get("record_id")`, `knowledge_items[0].get("title")`, etc. using the generic field names.
  - **OPTION B — LLM call** (commented out): shows how to call Claude via the Anthropic SDK (`anthropic.Anthropic().messages.create()`), constructing a prompt that includes the record and retrieved context as the user message. Use `claude-sonnet-4-6` as the model. Include `import anthropic` at the top of the option B block (commented). Add a note that `ANTHROPIC_API_KEY` must be added to `.env` and `config.py` if Option B is used.
- Remove all healthcare-specific logic (`_determine_recommendation`, pend codes, etc.)

---

#### 5. backend/routers/claims.py → backend/routers/records.py

Rename the file. Update all internals:

- Router prefix: `/api/records`
- `GET /{scenario}/record` — fetch the demo record; use `demo_record: True` flag and generic field names
- `POST /{scenario}/embed` — embed `record_text` field, store as `record_embedding`; response messages should use generic language
- `POST /{scenario}/output` (was `/rationale`) — calls `generate_output()` from the new llm.py; write result back to the record as `ai_output` field; update `processing_status` to `"READY_FOR_REVIEW"` (was `adjudication_status`)
- `POST /reset-all` — clear `ai_output`, `ai_determination`, `ai_output_generated_at`, `ai_supporting_kb_ids`, `ai_comparable_record_ids`; preserve `record_embedding`
- Import from `data.demo_records` instead of `data.demo_claims`
- Update `_serialize` to handle generic field names

---

#### 6. backend/routers/search.py

- Remove hardcoded clinical area inference (the CPT/HCPCS J/S code logic)
- Remove hardcoded scenario validation string `"scenario must be A, B, or C"` — make it a config or just allow any scenario string and 404 if not found
- Import from `services.vector_search` using the new function names
- Collection refs: `db.knowledge_base` and `db.historical_records`
- Response shape: replace `"policies"` key with `"knowledge_base"` and `"prior_claims"` with `"historical_records"`
- Update meta block index names to match new index names from step 3
- Keep the optional filter passthrough pattern

---

#### 7. backend/main.py

- Update `title` to use `settings.DEMO_NAME`
- Update `description` to generic: `"MongoDB Atlas + Voyage AI + Atlas Vector Search — operational record, embeddings, retrieval, and AI output in one platform."`
- Import `records_router` instead of `claims_router`; update `include_router` call

---

#### 8. scripts/setup.py

Restructure so all domain-specific config lives in a clearly marked block at
the very top of the file (after imports):

```python
# =============================================================================
# DEMO CONFIGURATION — edit this block for each new demo
# =============================================================================
DEMO_DB_NAME         = "demo_db"
RECORDS_COLLECTION   = "records"
KB_COLLECTION        = "knowledge_base"
HIST_COLLECTION      = "historical_records"
EMBED_FIELD          = "record_embedding"
KB_INDEX_NAME        = "kb_vector_index"
HIST_INDEX_NAME      = "historical_vector_index"
KB_EMBED_FIELD       = "record_embedding"        # field name in kb docs
HIST_EMBED_FIELD     = "record_embedding"        # field name in hist docs
KB_FILTER_FIELDS     = ["category", "subcategory"]
HIST_FILTER_FIELDS   = ["category", "outcome"]
# =============================================================================
```

Use these variables throughout instead of hardcoded strings. Import from
`data.demo_records`, `data.knowledge_base`, `data.historical_records`.

Update the index definitions to use the config vars above. Keep the same
setup flow: create collections → seed knowledge_base with embeddings → seed
historical_records with embeddings → insert demo records with embeddings →
wait for indexes → smoke test.

---

#### 9. scripts/reset_demo.py

Update collection names and field names to match the new generic naming.
No structural changes needed.

---

#### 10. frontend/src/types.ts

Replace all healthcare types with generic equivalents:

```typescript
export interface DemoRecord {
  record_id: string;
  scenario: string;
  record_text: string;
  record_embedding?: string; // serialized as "<vector:N dims>" from backend
  processing_status: string;
  ai_output?: string;
  ai_determination?: string;
  [key: string]: unknown; // domain-specific fields pass through
}

export interface KnowledgeItem {
  kb_id: string;
  title: string;
  category: string;
  subcategory?: string;
  content_text: string;
  vector_score?: number;
  [key: string]: unknown;
}

export interface HistoricalRecord {
  record_id: string;
  category: string;
  outcome: string;
  outcome_rationale?: string;
  vector_score?: number;
  [key: string]: unknown;
}

export interface SearchResults {
  knowledge_base: KnowledgeItem[];
  historical_records: HistoricalRecord[];
  query_filters_applied: Record<string, string | null>;
  meta: Record<string, string | number>;
}
```

---

#### 11. frontend/src/api.ts

Update all endpoint paths from `/api/claims` to `/api/records` and from
`/api/search` (keep search prefix). Update response destructuring to match
new field names (`knowledge_base`, `historical_records` instead of `policies`,
`prior_claims`).

---

#### 12. frontend/src/components/ — strip domain language, keep structure

For each component, keep the layout, styling, and interactivity exactly as-is.
Only change:
- Display labels: "Claim" → "Record", "Policy" → "Knowledge Base Item",
  "Prior Claim" → "Historical Record", "Clinical Notes" → "Record Text",
  "Adjudication Status" → "Processing Status", "Rationale" → "AI Output"
- Field references in props/rendering: use the new generic field names from types.ts
- Component filenames: rename
  - `ClaimRecord.tsx` → `RecordCard.tsx`
  - `ClaimSummaryBar.tsx` → `RecordSummaryBar.tsx`
  - `RationalePanel.tsx` → `OutputPanel.tsx`
  - Keep all others as-is (EmbeddingStep, SearchStep, ContextPanel, ScenarioSelector, StepIndicator, DocsModal, Header)
- In `SearchStep.tsx` / `ContextPanel.tsx`: replace `policies` prop with `knowledgeBase` and `priorClaims` with `historicalRecords`

---

#### 13. frontend/src/App.tsx

- Update scenario config object at the top — replace healthcare scenario labels
  with generic placeholders: `"Scenario A"`, `"Scenario B"`, `"Scenario C"`
  with description `"[TODO: describe this scenario]"`
- Update all state variable names that reference `claim` → `record`,
  `policies` → `knowledgeBase`, `priorClaims` → `historicalRecords`,
  `rationale` → `aiOutput`
- Update API call sites to match new function signatures from api.ts
- Update component imports to use renamed component files

---

#### 14. backend/.env.example and .env.example (root)

Add `DEMO_NAME=My Atlas AI Demo` to both. Add a commented line for
`# ANTHROPIC_API_KEY=` with a note that it's only needed if using LLM output
(Option B in llm.py).

---

#### 15. Template documentation

Create `TEMPLATE.md` at the repo root with:

**Sections:**
1. What this is — one paragraph on the pattern
2. Architecture diagram (ASCII) showing: Domain Records → [Embed] → MongoDB (record_embedding stored inline) → [Vector Search] → Knowledge Base + Historical Records → [Generate Output] → AI Output written back to record
3. Checklist: What to replace for each new demo (data files, collection names, filter fields, scenario labels, output generation logic, frontend labels)
4. `.env` vars table
5. Atlas Vector Search index setup notes (the indexes are created by setup.py, but note the filter fields must match what's in the index definition)
6. Brief note on Option A vs Option B in llm.py

Update `README.md` to describe the template purpose rather than the healthcare demo. Remove all healthcare-specific content.

Rewrite `DEMO_SCRIPT.md` and `DEMO_RUNBOOK.md` as skeletal templates with
`[TODO: domain-specific]` placeholders throughout.

---

#### 16. Final check

After all changes:
- Run `cd backend && python -c "from config import settings; from data.demo_records import DEMO_RECORDS; print('imports ok')"` to verify backend imports resolve
- Run `cd frontend && npm run build` to verify frontend compiles
- Confirm no references to `clinical_`, `claim_`, `policy_`, `prior_claim_`, `healthcare` remain in any Python or TypeScript source file (grep to verify)

---

That's the full plan. Execute each section in order, mark tasks complete as you go.
