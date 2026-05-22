# Demo Script — Atlas AI Demo

[TODO: Replace this file with domain-specific talking points before presenting.]

---

## Opening (1–2 min)

[TODO: Describe the domain problem this demo addresses. What kind of records
are being processed? What is the business question being answered?]

Example framing:
> "Today I'll show how MongoDB Atlas handles [domain] records end-to-end —
> from ingestion through AI-assisted output — without stitching together
> separate vector stores, caches, or AI pipelines."

---

## Step 1 — Load Record (~1 min)

**What to say:**
> "Here's a [domain] record stored in MongoDB. It has [domain-specific fields]
> and an unstructured text field — `record_text` — that captures the key context.
> The embedding field is currently null."

[TODO: Point out specific fields in the record that make this scenario interesting.]

**Talking points:**
- This is a real operational document, not a separate AI input file
- All domain-specific fields live alongside the fields we're about to add

---

## Step 2 — Embed (~1 min)

**What to say:**
> "We send `record_text` to Voyage AI. The resulting 1024-dimensional vector
> is written back into the same document. No separate vector database — the
> embedding lives next to the operational data."

**Talking points:**
- Show the `record_embedding: <vector: 1024 dims>` field appear in the record
- Emphasize: one document, one collection, everything co-located

---

## Step 3 — Vector Search (~2 min)

**What to say:**
> "Atlas Vector Search uses the stored embedding as a query vector. We get
> semantically relevant [knowledge base items] and [historical records] back —
> ranked by cosine similarity."

[TODO: Explain what the filters mean in your domain context.]

**Talking points:**
- The `$vectorSearch` stage runs inside the aggregation pipeline — no round trip
  to a separate service
- Optional hard filters (category, outcome) narrow the result set before ranking
- The query vector is the stored embedding — no second Voyage API call

---

## Step 4 — Retrieved Context (~1 min)

**What to say:**
> "These are the top matches. Notice the similarity scores — [explain what high/
> low scores mean for your domain]."

[TODO: Point out the most interesting retrieved items for each scenario and
explain why they're relevant.]

---

## Step 5 — Generate Output + Write-back (~2 min)

**What to say:**
> "The output is assembled from the retrieved context and written back to the
> original record. Watch `processing_status` change and the AI output fields
> appear — all in the same document."

**Talking points:**
- Operational data, embeddings, retrieval results, and AI output: one platform
- The write-back is a standard MongoDB `update_one` — no external storage

---

## Closing (~1 min)

[TODO: Summarize the business value for your specific audience.]

> "MongoDB Atlas handled every step: storage, vector indexing, semantic search,
> and AI output persistence. [Domain-specific value statement.]"

---

## Scenario variations

| Scenario | [TODO: Name] | [TODO: What it demonstrates] |
|----------|-------------|-------------------------------|
| A        | [TODO]      | [TODO]                        |
| B        | [TODO]      | [TODO]                        |
| C        | [TODO]      | [TODO]                        |
