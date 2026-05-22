"""
Vector search endpoints.
"""

from fastapi import APIRouter, HTTPException
from db import get_db
from services.vector_search import search_knowledge_base, search_historical_records

router = APIRouter(prefix="/api/search", tags=["search"])


@router.post("/{scenario}")
def run_vector_search(scenario: str, body: dict):
    """
    Run Atlas Vector Search for the given demo record scenario.

    Accepts optional MQL filters: category, subcategory (for knowledge_base)
    and category, outcome (for historical_records). Combines semantic
    relevance with hard filters.
    """
    db = get_db()
    record = db.records.find_one({"scenario": scenario, "demo_record": True})
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"Demo record for scenario {scenario} not found.",
        )

    embedding = record.get("record_embedding")
    if not embedding or isinstance(embedding, str):
        raise HTTPException(
            status_code=400,
            detail="Record has no embedding yet. Run /embed first.",
        )

    filters = body.get("filters", {})
    category = filters.get("category")
    subcategory = filters.get("subcategory")
    outcome = filters.get("outcome")

    n_kb = filters.get("n_knowledge_base", 3)
    n_hist = filters.get("n_historical_records", 3)

    # Reuse the stored embedding as query vector — no extra Voyage API call.
    query_vector = embedding

    kb_results = search_knowledge_base(
        db.knowledge_base,
        query_vector,
        limit=n_kb,
        category=category,
        subcategory=subcategory,
    )

    hist_results = search_historical_records(
        db.historical_records,
        query_vector,
        limit=n_hist,
        category=category,
        outcome=outcome,
    )

    return {
        "query_filters_applied": {
            "category": category,
            "subcategory": subcategory,
            "outcome": outcome,
        },
        "knowledge_base": kb_results,
        "historical_records": hist_results,
        "meta": {
            "knowledge_base_count": len(kb_results),
            "historical_records_count": len(hist_results),
            "embedding_model": "voyage-3",
            "search_index_knowledge_base": "kb_vector_index",
            "search_index_historical_records": "historical_vector_index",
        },
    }
