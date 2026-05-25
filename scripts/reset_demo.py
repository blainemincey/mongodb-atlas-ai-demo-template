#!/usr/bin/env python3
"""
Reset all demo records between demo runs.

Default (soft) reset — keeps the Voyage AI embedding, clears only the
AI output and processing_status fields. The Step 2 embed button will detect
the existing embedding and skip the Voyage API call, eliminating rate-limit
risk on repeat runs while the UI experience remains identical.

Hard reset (--hard) — clears everything including the embedding. Use this
when you want a true first-run experience or to force a fresh Voyage API call.

Usage:
  python scripts/reset_demo.py           # soft reset (default)
  python scripts/reset_demo.py --hard    # full reset including embedding
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from db import get_db

# Record IDs to reset — update if you change demo_records.py
RECORDS = ["TKT-001-A", "TKT-001-B", "TKT-001-C"]

# Always cleared — AI output and processing state
SOFT_RESET_FIELDS = {
    "processing_status": "PENDING",
    "ai_output": None,
    "ai_determination": None,
    "ai_output_generated_at": None,
    "ai_supporting_kb_ids": [],
    "ai_comparable_record_ids": [],
}

# Additionally cleared on --hard
HARD_ONLY_FIELDS = {
    "record_embedding": None,
    "embedding_model": None,
    "embedding_generated_at": None,
}


def main():
    hard = "--hard" in sys.argv

    reset_fields = dict(SOFT_RESET_FIELDS)
    if hard:
        reset_fields.update(HARD_ONLY_FIELDS)

    mode = "hard (embedding cleared)" if hard else "soft (embedding preserved)"
    print(f"Resetting demo records [{mode}]...")

    db = get_db()
    for rid in RECORDS:
        result = db.records.update_one({"record_id": rid}, {"$set": reset_fields})
        status = "reset" if result.modified_count else "already clean"
        print(f"  {rid}: {status}")

    if hard:
        print("Done — all records are PENDING with no embedding or AI output.")
    else:
        print("Done — all records are PENDING. Embeddings preserved; AI output cleared.")


if __name__ == "__main__":
    main()
