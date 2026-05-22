"""
Record-level endpoints.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from db import get_db
from services.embedding import embed_document
from data.demo_records import DEMO_RECORDS

router = APIRouter(prefix="/api/records", tags=["records"])


def _serialize(doc: dict) -> dict:
    """Convert ObjectId and embedding vectors to JSON-safe values."""
    out = {}
    for k, v in doc.items():
        if k == "_id":
            out["_id"] = str(v)
        elif isinstance(v, list) and v and isinstance(v[0], float):
            out[k] = f"<vector:{len(v)} dims>"
        else:
            out[k] = v
    return out


def _serialize_full(doc: dict) -> dict:
    """Serialize record including full embedding vector."""
    out = {}
    for k, v in doc.items():
        if k == "_id":
            out["_id"] = str(v)
        else:
            out[k] = v
    return out


@router.get("/{scenario}/record")
def get_record(scenario: str):
    """Return the demo record for the given scenario."""
    db = get_db()
    record = db.records.find_one({"scenario": scenario, "demo_record": True})
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"Demo record for scenario {scenario} not found. Run setup.py first.",
        )
    return _serialize(record)


@router.post("/{scenario}/embed")
def generate_embedding(scenario: str):
    """
    Generate a Voyage AI embedding for the record's record_text and
    write it back into the same MongoDB document.
    """
    db = get_db()
    record = db.records.find_one({"scenario": scenario, "demo_record": True})
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"Demo record for scenario {scenario} not found.",
        )

    record_text = record.get("record_text", "")
    if not record_text:
        raise HTTPException(status_code=400, detail="Record has no record_text to embed.")

    existing_embedding = record.get("record_embedding")
    if existing_embedding and isinstance(existing_embedding, list):
        return {
            "status": "ok",
            "record_id": record["record_id"],
            "embedding_model": record.get("embedding_model", "voyage-3"),
            "embedding_dimensions": len(existing_embedding),
            "embedding_preview": existing_embedding[:8],
            "generated_at": record.get("embedding_generated_at", ""),
            "message": (
                f"Voyage AI voyage-3 embedding ({len(existing_embedding)} dims) already stored "
                "in this MongoDB document — returned from cache, no API call made."
            ),
        }

    embedding = embed_document(record_text)
    now = datetime.now(timezone.utc).isoformat()

    db.records.update_one(
        {"scenario": scenario, "demo_record": True},
        {
            "$set": {
                "record_embedding": embedding,
                "embedding_model": "voyage-3",
                "embedding_generated_at": now,
                "updated_at": now,
            }
        },
    )

    return {
        "status": "ok",
        "record_id": record["record_id"],
        "embedding_model": "voyage-3",
        "embedding_dimensions": len(embedding),
        "embedding_preview": embedding[:8],
        "generated_at": now,
        "message": (
            f"Voyage AI voyage-3 embedding ({len(embedding)} dims) written to the "
            "same MongoDB document as the record text. No separate vector store."
        ),
    }


@router.post("/{scenario}/output")
def generate_and_writeback_output(scenario: str, body: dict):
    """
    Generate AI output from retrieved context and write it back into the
    original record document, updating processing_status to READY_FOR_REVIEW.
    """
    db = get_db()
    record = db.records.find_one({"scenario": scenario, "demo_record": True})
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"Demo record for scenario {scenario} not found.",
        )

    knowledge_items = body.get("knowledge_items", [])
    historical_records = body.get("historical_records", [])

    if not knowledge_items and not historical_records:
        raise HTTPException(
            status_code=400,
            detail="Must supply retrieved knowledge_items and/or historical_records.",
        )

    from services.llm import generate_output

    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S UTC")

    output_text = generate_output(record, knowledge_items, historical_records, timestamp)

    supporting_kb_ids = [k.get("kb_id") for k in knowledge_items if k.get("kb_id")]
    comparable_record_ids = [h.get("record_id") for h in historical_records if h.get("record_id")]

    now_iso = now.isoformat()

    db.records.update_one(
        {"scenario": scenario, "demo_record": True},
        {
            "$set": {
                "ai_output": output_text,
                "ai_determination": _extract_determination(output_text),
                "ai_output_generated_at": now_iso,
                "ai_supporting_kb_ids": supporting_kb_ids,
                "ai_comparable_record_ids": comparable_record_ids,
                "processing_status": "READY_FOR_REVIEW",
                "updated_at": now_iso,
            }
        },
    )

    updated_record = db.records.find_one({"scenario": scenario, "demo_record": True})
    return {
        "output": output_text,
        "determination": _extract_determination(output_text),
        "supporting_kb_ids": supporting_kb_ids,
        "comparable_record_ids": comparable_record_ids,
        "updated_record": _serialize(updated_record),
    }


@router.post("/reset-all")
def soft_reset_all_records():
    """
    Soft-reset all demo records: clear AI output and revert processing_status
    to PENDING. Preserves record_embedding so Step 2 returns from cache on the
    next run without calling Voyage AI.
    """
    db = get_db()
    now = datetime.now(timezone.utc).isoformat()

    reset_fields = {
        "processing_status": "PENDING",
        "ai_output": None,
        "ai_determination": None,
        "ai_output_generated_at": None,
        "ai_supporting_kb_ids": [],
        "ai_comparable_record_ids": [],
        "updated_at": now,
    }

    db.records.update_many({"demo_record": True}, {"$set": reset_fields})

    results = []
    for scenario in ("A", "B", "C"):
        doc = db.records.find_one({"scenario": scenario, "demo_record": True})
        if doc:
            results.append({
                "record_id": doc["record_id"],
                "scenario": scenario,
                "embedding_preserved": bool(
                    doc.get("record_embedding") and isinstance(doc["record_embedding"], list)
                ),
            })

    return {
        "status": "ok",
        "records_reset": results,
        "message": "Demo records reset to PENDING. AI output cleared. Embeddings preserved where present.",
    }


def _extract_determination(output_text: str) -> str:
    """Pull the DETERMINATION section header line from the output."""
    lines = output_text.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "DETERMINATION":
            # Return the next non-empty line as the determination value
            for next_line in lines[i + 1:]:
                next_stripped = next_line.strip()
                if next_stripped and not next_stripped.startswith("[TODO"):
                    return next_stripped
    return "PENDING"
