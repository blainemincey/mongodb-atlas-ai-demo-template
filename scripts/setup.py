#!/usr/bin/env python3
"""
Atlas AI Demo — Setup Script
==============================
Idempotent: safe to run multiple times.

What this does (in order):
  1. Connect to Atlas and create the database / collections.
  2. Drop and recreate demo records (so re-runs start clean).
  3. Create Atlas Vector Search indexes via the MongoDB driver.
  4. Seed knowledge_base with Voyage AI embeddings.
  5. Seed historical_records with Voyage AI embeddings.
  6. Insert demo records (A, B, C) with Voyage AI embeddings.
  7. Wait for all Vector Search indexes to reach READY state.
  8. Run a quick smoke-test search against each index.

Usage:
  cd /path/to/demo
  python scripts/setup.py

Prerequisites:
  .env file with MONGODB_URI and VOYAGE_API_KEY
"""

import sys
import os
import time

# Allow importing from backend/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
from config import settings
from services.embedding import embed_batch, embed_document, embed_query
from data.demo_records import DEMO_RECORDS
from data.knowledge_base import KNOWLEDGE_BASE
from data.historical_records import HISTORICAL_RECORDS


# =============================================================================
# DEMO CONFIGURATION — edit this block for each new demo
# =============================================================================
DEMO_DB_NAME         = settings.db_name           # overridden by .env DB_NAME
RECORDS_COLLECTION   = "records"
KB_COLLECTION        = "knowledge_base"
HIST_COLLECTION      = "historical_records"
EMBED_FIELD          = "record_embedding"          # embedding field on demo records
KB_INDEX_NAME        = "kb_vector_index"
HIST_INDEX_NAME      = "historical_vector_index"
KB_EMBED_FIELD       = "record_embedding"          # embedding field in kb docs
HIST_EMBED_FIELD     = "record_embedding"          # embedding field in hist docs
KB_TEXT_FIELD        = "content_text"              # text field embedded in kb docs
HIST_TEXT_FIELD      = "source_text"               # text field embedded in hist docs
RECORD_TEXT_FIELD    = "record_text"               # text field embedded in demo records
KB_FILTER_FIELDS     = ["category", "subcategory"]
HIST_FILTER_FIELDS   = ["category", "outcome"]
# =============================================================================


# ─────────────────────────────────────────────────────────────────────────────
# Index definitions
# ─────────────────────────────────────────────────────────────────────────────

KB_INDEX = SearchIndexModel(
    name=KB_INDEX_NAME,
    type="vectorSearch",
    definition={
        "fields": [
            {
                "type": "vector",
                "path": KB_EMBED_FIELD,
                "numDimensions": 1024,
                "similarity": "cosine",
            },
            *[{"type": "filter", "path": f} for f in KB_FILTER_FIELDS],
        ]
    },
)

HIST_INDEX = SearchIndexModel(
    name=HIST_INDEX_NAME,
    type="vectorSearch",
    definition={
        "fields": [
            {
                "type": "vector",
                "path": HIST_EMBED_FIELD,
                "numDimensions": 1024,
                "similarity": "cosine",
            },
            *[{"type": "filter", "path": f} for f in HIST_FILTER_FIELDS],
        ]
    },
)

RECORDS_INDEX = SearchIndexModel(
    name="records_vector_index",
    type="vectorSearch",
    definition={
        "fields": [
            {
                "type": "vector",
                "path": EMBED_FIELD,
                "numDimensions": 1024,
                "similarity": "cosine",
            },
            {"type": "filter", "path": "scenario"},
        ]
    },
)


def log(msg: str) -> None:
    print(f"  {msg}")


def step(msg: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {msg}")
    print(f"{'─' * 60}")


def ensure_index(collection, index_model: SearchIndexModel) -> None:
    """Create index if it doesn't already exist."""
    existing = {idx["name"]: idx for idx in collection.list_search_indexes()}
    name = index_model.document["name"]
    if name in existing:
        log(f"Index '{name}' already exists — skipping creation.")
    else:
        collection.create_search_index(index_model)
        log(f"Index '{name}' creation submitted.")


def wait_for_indexes(collection, index_names: list[str], timeout: int = 300) -> None:
    """Poll until all named indexes reach READY status."""
    log(f"Waiting for indexes to become READY (timeout {timeout}s)...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        statuses = {
            idx["name"]: idx.get("status", "UNKNOWN")
            for idx in collection.list_search_indexes()
        }
        pending = [n for n in index_names if statuses.get(n) != "READY"]
        if not pending:
            log("All indexes READY.")
            return
        log(f"  Pending: {pending} — sleeping 10s...")
        time.sleep(10)
    raise TimeoutError(f"Indexes not READY after {timeout}s: {pending}")


def embed_records(records: list[dict], text_field: str, embed_field: str, batch_size: int = 64) -> list[dict]:
    """
    Add Voyage AI embeddings to a list of records.

    Processes in batches with a 1-second pause between batches to stay
    within Voyage AI free-tier rate limits (requests/minute).
    """
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    all_embeddings: list = []

    for i in range(0, len(records), batch_size):
        batch = records[i : i + batch_size]
        texts = [r[text_field] for r in batch]
        log(f"  Embedding batch {i // batch_size + 1} ({len(texts)} docs)...")
        embeddings = embed_batch(texts, input_type="document")
        all_embeddings.extend(embeddings)
        if i + batch_size < len(records):
            time.sleep(1)

    for rec, emb in zip(records, all_embeddings):
        rec[embed_field] = emb
        rec["embedding_generated_at"] = now
    return records


def main() -> None:
    print("\n" + "=" * 60)
    print(f"  {settings.demo_name} — Atlas Setup")
    print("=" * 60)

    # ── Connect ──────────────────────────────────────────────────
    step("Step 1: Connecting to MongoDB Atlas")
    client = MongoClient(settings.mongodb_uri)
    db = client[DEMO_DB_NAME]
    log(f"Connected. Database: {DEMO_DB_NAME}")
    db.command("ping")
    log("Ping OK.")

    # ── Collections ──────────────────────────────────────────────
    step("Step 2: Ensuring collections exist")
    for cname in (RECORDS_COLLECTION, KB_COLLECTION, HIST_COLLECTION):
        if cname not in db.list_collection_names():
            db.create_collection(cname)
            log(f"Created collection: {cname}")
        else:
            log(f"Collection '{cname}' already exists.")

    # ── Vector Search Indexes ─────────────────────────────────────
    step("Step 3: Creating Atlas Vector Search indexes")
    ensure_index(db[KB_COLLECTION], KB_INDEX)
    ensure_index(db[HIST_COLLECTION], HIST_INDEX)
    ensure_index(db[RECORDS_COLLECTION], RECORDS_INDEX)

    # ── Seed Knowledge Base ───────────────────────────────────────
    step("Step 4: Seeding knowledge base with Voyage AI embeddings")
    existing_kb_ids = {
        d["kb_id"] for d in db[KB_COLLECTION].find({}, {"kb_id": 1})
    }
    new_kb = [k for k in KNOWLEDGE_BASE if k["kb_id"] not in existing_kb_ids]

    if new_kb:
        log(f"Embedding {len(new_kb)} new knowledge base items via Voyage AI...")
        new_kb = embed_records(new_kb, KB_TEXT_FIELD, KB_EMBED_FIELD)
        db[KB_COLLECTION].insert_many(new_kb)
        log(f"Inserted {len(new_kb)} knowledge base items.")
    else:
        log(f"All {len(KNOWLEDGE_BASE)} knowledge base items already present — skipping.")

    total_kb = db[KB_COLLECTION].count_documents({})
    log(f"Total knowledge base items in collection: {total_kb}")

    # ── Seed Historical Records ───────────────────────────────────
    step("Step 5: Seeding historical records with Voyage AI embeddings")
    existing_hist_ids = {
        d["record_id"] for d in db[HIST_COLLECTION].find({}, {"record_id": 1})
    }
    new_hist = [h for h in HISTORICAL_RECORDS if h["record_id"] not in existing_hist_ids]

    if new_hist:
        log(f"Embedding {len(new_hist)} new historical records via Voyage AI...")
        new_hist = embed_records(new_hist, HIST_TEXT_FIELD, HIST_EMBED_FIELD)
        db[HIST_COLLECTION].insert_many(new_hist)
        log(f"Inserted {len(new_hist)} historical records.")
    else:
        log(f"All {len(HISTORICAL_RECORDS)} historical records already present — skipping.")

    total_hist = db[HIST_COLLECTION].count_documents({})
    log(f"Total historical records in collection: {total_hist}")

    # ── Insert/Refresh Demo Records ───────────────────────────────
    step("Step 6: Inserting demo records (A, B, C) with Voyage AI embeddings")
    for scenario_key, record in DEMO_RECORDS.items():
        db[RECORDS_COLLECTION].delete_one({"scenario": scenario_key, "demo_record": True})
        record_copy = dict(record)
        log(f"Embedding Scenario {scenario_key} demo record...")
        embedding = embed_document(record_copy[RECORD_TEXT_FIELD])
        import datetime
        record_copy[EMBED_FIELD] = embedding
        record_copy["embedding_generated_at"] = datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()
        db[RECORDS_COLLECTION].insert_one(record_copy)
        log(
            f"  Scenario {scenario_key}: {record_copy['record_id']} inserted "
            f"({len(embedding)}-dim embedding)."
        )

    # ── Wait for Indexes ──────────────────────────────────────────
    step("Step 7: Waiting for Atlas Vector Search indexes to be READY")
    wait_for_indexes(db[KB_COLLECTION], [KB_INDEX_NAME])
    wait_for_indexes(db[HIST_COLLECTION], [HIST_INDEX_NAME])
    log("Records index may still be building — that's OK; demo uses kb and historical indexes.")

    # ── Smoke Test ────────────────────────────────────────────────
    step("Step 8: Smoke-testing vector search")

    test_query = "TODO replace with domain-specific test query for your knowledge base"
    log(f"Query: '{test_query[:60]}'")
    test_vector = embed_query(test_query)

    kb_results = list(
        db[KB_COLLECTION].aggregate([
            {
                "$vectorSearch": {
                    "index": KB_INDEX_NAME,
                    "path": KB_EMBED_FIELD,
                    "queryVector": test_vector,
                    "numCandidates": 20,
                    "limit": 3,
                }
            },
            {"$project": {"kb_id": 1, "title": 1, "_id": 0,
                          "score": {"$meta": "vectorSearchScore"}}},
        ])
    )
    log("Top knowledge base matches:")
    for k in kb_results:
        log(f"  {k.get('kb_id')} | {str(k.get('title', ''))[:50]} | score={k.get('score', 0):.4f}")

    hist_results = list(
        db[HIST_COLLECTION].aggregate([
            {
                "$vectorSearch": {
                    "index": HIST_INDEX_NAME,
                    "path": HIST_EMBED_FIELD,
                    "queryVector": test_vector,
                    "numCandidates": 20,
                    "limit": 3,
                }
            },
            {"$project": {"record_id": 1, "outcome": 1, "_id": 0,
                          "score": {"$meta": "vectorSearchScore"}}},
        ])
    )
    log("Top historical record matches:")
    for h in hist_results:
        log(f"  {h.get('record_id')} | {h.get('outcome')} | score={h.get('score', 0):.4f}")

    # ── Done ──────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  Setup complete. Demo is ready to run.")
    print("=" * 60)
    print()
    print("  To start the demo:")
    print("    ./start.sh")
    print()


if __name__ == "__main__":
    main()
