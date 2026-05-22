"""
Atlas Vector Search queries.

Uses the $vectorSearch aggregation stage with optional MQL pre-filters.
Filters enforce hard operational constraints on top of semantic similarity.
"""

from typing import Optional, List
from pymongo.collection import Collection


KB_INDEX = "kb_vector_index"
HIST_INDEX = "historical_vector_index"

# Number of candidates Atlas Vector Search will consider before returning limit
NUM_CANDIDATES = 80


def search_knowledge_base(
    collection: Collection,
    query_vector: List[float],
    limit: int = 3,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
) -> List[dict]:
    """
    Search the knowledge_base collection by semantic similarity.
    Optional pre-filters on category / subcategory.
    """
    vector_search_stage: dict = {
        "index": KB_INDEX,
        "path": "record_embedding",
        "queryVector": query_vector,
        "numCandidates": NUM_CANDIDATES,
        "limit": limit,
    }

    filter_clauses = {}
    if category:
        filter_clauses["category"] = {"$eq": category}
    if subcategory:
        filter_clauses["subcategory"] = {"$eq": subcategory}

    if filter_clauses:
        vector_search_stage["filter"] = filter_clauses

    pipeline = [
        {"$vectorSearch": vector_search_stage},
        {
            "$project": {
                "_id": 0,
                "kb_id": 1,
                "title": 1,
                "category": 1,
                "subcategory": 1,
                "content_text": 1,
                "vector_score": {"$meta": "vectorSearchScore"},
            }
        },
    ]

    return list(collection.aggregate(pipeline))


def search_historical_records(
    collection: Collection,
    query_vector: List[float],
    limit: int = 3,
    category: Optional[str] = None,
    outcome: Optional[str] = None,
) -> List[dict]:
    """
    Search the historical_records collection by semantic similarity.
    Optional pre-filters on category / outcome.
    """
    vector_search_stage: dict = {
        "index": HIST_INDEX,
        "path": "record_embedding",
        "queryVector": query_vector,
        "numCandidates": NUM_CANDIDATES,
        "limit": limit,
    }

    filter_clauses = {}
    if category:
        filter_clauses["category"] = {"$eq": category}
    if outcome:
        filter_clauses["outcome"] = {"$eq": outcome}

    if filter_clauses:
        vector_search_stage["filter"] = filter_clauses

    pipeline = [
        {"$vectorSearch": vector_search_stage},
        {
            "$project": {
                "_id": 0,
                "record_id": 1,
                "category": 1,
                "outcome": 1,
                "outcome_rationale": 1,
                "source_text": 1,
                "vector_score": {"$meta": "vectorSearchScore"},
            }
        },
    ]

    return list(collection.aggregate(pipeline))
