# Demo Script — Legal Contract Review

> This script is accessible from the **Docs** menu inside the running app.
> Keep it open in a second tab or window while presenting.

---

## The one-sentence pitch

> "MongoDB Atlas handles every step of this workflow — storage, vector indexing,
> semantic search, and AI output — in a single platform, with the results written
> back to the same operational record that triggered the process."

---

## Opening (1–2 min)

Set up the problem before touching the UI:

> "Most AI demos show you a chatbot or a search box. What I want to show you
> today is what happens when AI is embedded directly into an operational
> workflow — where the records, the embeddings, the retrieved context, and the
> AI output all live in the same database.
>
> We're going to process a contract clause through four steps: embed it,
> search for relevant context, and generate an AI-assisted legal assessment.
> Every one of those steps writes its result back to the same MongoDB document.
> No separate vector store. No separate AI pipeline. One platform."

---

## Step 1 — Load Record (~1 min)

**Click:** Select a scenario from the top picker.

**Say:**
> "Here's the clause record as it exists in MongoDB right now. It has structured
> fields — clause_type, contract_type, risk_level, jurisdiction — and a
> `record_text` field that holds the full unstructured clause description.
> Notice `record_embedding` is null and `processing_status` is PENDING.
> This is the pre-AI state."

**Key point to land:** This is a real operational document, not a
pre-processed AI input. The embedding and AI output fields don't exist yet
— we're about to add them in place.

---

## Step 2 — Embed (~1 min)

**Click:** "Generate Embedding" button on the Embed tab.

**Say:**
> "We're sending `record_text` to Voyage AI's voyage-3 model. It returns a
> 1024-dimensional vector. Watch what happens — that vector gets written
> directly back into this same MongoDB document. There's no separate vector
> database. The embedding lives next to the operational data, in the same
> document, queryable with the same driver."

**If they ask why store it in the document:**
> "Because the embedding is deterministic — same text always produces the same
> vector. Storing it means we call Voyage exactly once per clause record. Every
> subsequent search reuses it. No per-search API calls, no rate-limit risk."

---

## Step 3 — Vector Search (~2 min)

**Click:** "Run Vector Search" on the Vector Search tab.

**Say:**
> "Atlas Vector Search takes that stored embedding as the query vector and
> finds semantically similar documents across two collections simultaneously —
> contract standards and legal guidelines and comparable past contract clause
> reviews.
>
> This isn't keyword search. It's cosine similarity over 1024-dimensional
> space — so it surfaces content that means the same thing, not just content
> that uses the same words."

**Point at the filter pills:**
> "The filters here are hard constraints, not hints. When you set a category
> filter, Atlas eliminates non-matching documents before the vector scoring
> runs — so you get semantic relevance within the relevant subset, not across
> everything."

**Key technical point:** The `$vectorSearch` stage runs inside a MongoDB
aggregation pipeline. No round trip to a separate service. The query vector
is the one we stored in Step 2 — no second Voyage API call.

---

## Step 4 — Retrieved Context (~1 min)

**Click:** The "Retrieved Context" tab to see results.

**Say:**
> "These are the top matches, ranked by cosine similarity score. The contract
> standards items on the left are the relevant reference material — the
> market-standard guidelines and legal criteria that apply to this clause.
> The prior contract reviews on the right are the closest analogues from past
> cases."

**Point at the similarity scores:**
> "A score of 0.85+ means these documents are very close semantically to the
> clause text. That's not a coincidence — the embedding captures what the
> clause is actually about, and these are the most relevant items in the
> collection."

---

## Step 5 — Generate Output + Write-back (~2 min)

**Click:** "Generate Output" on the AI Output tab.

**Say:**
> "Now we assemble the legal assessment from the retrieved context and write
> it back to the original clause record. Watch the record in Tab 1 —
> `processing_status` changes, the AI output fields appear, and the supporting
> reference IDs are stored alongside the determination."

**After the write-back, switch to Tab 1:**
> "Same document. The operational fields, the embedding, and now the legal
> assessment — all in one MongoDB document. If a compliance team or a downstream
> system queries this record, they get everything: the raw clause text, what
> standards were retrieved, what the AI concluded, and when."

**Key point to land:**
> "This is the pattern: every step in the AI workflow writes its artifact back
> to the same operational record. You don't need a separate audit log or a
> separate results table. MongoDB is the system of record for the entire
> process."

---

## Closing (~1 min)

> "What you just saw — embedding, vector search, AI output, write-back — ran
> against a real MongoDB Atlas cluster. No external vector database. No
> separate AI results store. The aggregation pipeline handled search, the
> same update_one call that you'd use for any other field write handled
> persistence.
>
> The reason that matters is operability. When this goes to production, your
> ops team doesn't manage a new database tier. Your application code doesn't
> change its data model. And your compliance team can query the clause record
> and see exactly what the AI saw and what it recommended — because it's all
> in the same document."

---

## Handling common questions

**"Why not just use pgvector / Pinecone / Weaviate?"**
> "You can. The question is whether you want to manage a second database,
> keep it in sync with your operational data, and build joins across two
> systems at query time. Our argument is that co-locating the embedding with
> the document eliminates that entire class of problem."

**"Is the AI output accurate?"**
> "This demo uses a template engine by default — no LLM, fully deterministic.
> The template is grounded in the retrieved context: the contract standards and
> prior contract reviews you just saw. Option B in llm.py swaps in a Claude API
> call if you want a real language model. The storage and retrieval pattern
> is identical either way."

**"What does this cost at scale?"**
> "Atlas Vector Search runs on the same cluster as your operational data —
> no separate pricing tier. Voyage AI charges per token on embedding calls,
> but because you store the embedding in the document, you call it once per
> clause record, not once per query."

---

## Scenario variations

| Scenario | What it shows |
|----------|---------------|
| Limitation of Liability (Mutual Cap) | Clean acceptable path — mutual terms match market standard, comparable approved clauses surface directly. Shows how structured fields (clause_type, risk_level) confirm an acceptable outcome with supporting precedent. |
| Indemnification (One-Sided) | High-risk one-sided provision — demonstrates how the system flags against market-standard mutual indemnification and surfaces comparable revision cases. Illustrates the FLAG_FOR_REVISION path with actionable redline guidance. |
| IP Assignment (No Carve-Outs) | Critical risk, overbroad assignment — illustrates the escalation path and how prior counsel-escalated cases are retrieved. Shows how risk_level drives the determination directly to ESCALATE_TO_COUNSEL without ambiguity. |

---

## Reset between runs

Click **Reset Demo** in the header. This clears AI output and restores
`processing_status` to PENDING while preserving embeddings — so Step 2
returns instantly from cache and you skip the Voyage API call.
