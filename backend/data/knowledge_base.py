"""
Knowledge base seed data for the Atlas AI Demo scaffold.

This collection holds reference material — rules, policies, guidelines,
documentation, or any domain knowledge that should be retrieved by vector
search to inform AI output generation.

REQUIRED fields:
  - kb_id        : str  — unique ID, e.g. "KB-001"
  - content_text : str  — the text that gets embedded by Voyage AI
  - kb_embedding : absent on insert; written back by setup.py

OPTIONAL fields (but recommended for meaningful filter-based search):
  - title        : str  — human-readable title
  - category     : str  — top-level category (used as a vector search filter)
  - subcategory  : str  — finer grouping (also usable as a filter)

TODO: Replace stub entries with real domain knowledge before running setup.py.
Add as many records as needed — setup.py will batch-embed them all.
"""

KNOWLEDGE_BASE = [
    {
        "kb_id": "KB-001",
        "title": "[TODO: Knowledge base item title]",
        "category": "general",
        "subcategory": "example",
        # ----------------------------------------------------------------
        # TODO: Replace with real reference text for your domain.
        # The richer and more specific this text, the better vector search
        # results you will get when matching against demo record_text.
        # ----------------------------------------------------------------
        "content_text": (
            "KB-001 — [TODO: Replace with real reference content. "
            "Include domain-specific terminology, rules, criteria, or "
            "guidelines relevant to Scenario A records.]"
        ),
    },
    {
        "kb_id": "KB-002",
        "title": "[TODO: Knowledge base item title]",
        "category": "general",
        "subcategory": "example",
        "content_text": (
            "KB-002 — [TODO: Replace with real reference content relevant "
            "to Scenario B records.]"
        ),
    },
    {
        "kb_id": "KB-003",
        "title": "[TODO: Knowledge base item title]",
        "category": "general",
        "subcategory": "example",
        "content_text": (
            "KB-003 — [TODO: Replace with real reference content relevant "
            "to Scenario C records.]"
        ),
    },
    {
        "kb_id": "KB-004",
        "title": "[TODO: Knowledge base item title]",
        "category": "general",
        "subcategory": "example",
        "content_text": (
            "KB-004 — [TODO: Add additional knowledge base entries as needed. "
            "More entries improve search recall and make the demo richer.]"
        ),
    },
    {
        "kb_id": "KB-005",
        "title": "[TODO: Knowledge base item title]",
        "category": "general",
        "subcategory": "example",
        "content_text": (
            "KB-005 — [TODO: Add additional knowledge base entries as needed.]"
        ),
    },
]
