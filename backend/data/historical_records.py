"""
Historical records seed data for the Atlas AI Demo scaffold.

This collection holds past examples — adjudicated cases, resolved tickets,
prior decisions, or any historical data that provides analogues for the
current record being processed.

REQUIRED fields:
  - record_id      : str  — unique ID, e.g. "HIST-001"
  - source_text    : str  — the text that gets embedded by Voyage AI
  - source_embedding: absent on insert; written back by setup.py

OPTIONAL fields (recommended for filter-based search):
  - category       : str  — top-level grouping (usable as a vector search filter)
  - outcome        : str  — result of this historical case, e.g. "APPROVED", "DENIED"
  - outcome_rationale: str — brief explanation of why this outcome was reached

TODO: Replace stub entries with real historical examples before running setup.py.
Anchor records (ones that should surface for the specific demo scenarios) are
the most important — add those first, then pad with a broader corpus.
"""

HISTORICAL_RECORDS = [
    {
        "record_id": "HIST-001",
        "category": "general",
        "outcome": "APPROVED",
        "outcome_rationale": "[TODO: Explain why this historical record was approved.]",
        # ----------------------------------------------------------------
        # TODO: Replace with real historical case text for your domain.
        # This text is embedded — include terminology that will match
        # Scenario A demo records so this surfaces as an analogue.
        # ----------------------------------------------------------------
        "source_text": (
            "HIST-001 — [TODO: Replace with historical record text relevant to "
            "Scenario A. Include outcome context so the AI output step can "
            "reference this case as a comparable example.]"
        ),
    },
    {
        "record_id": "HIST-002",
        "category": "general",
        "outcome": "DENIED",
        "outcome_rationale": "[TODO: Explain why this historical record was denied.]",
        "source_text": (
            "HIST-002 — [TODO: Replace with historical record text. Including "
            "denied-outcome examples creates contrast in the demo.]"
        ),
    },
    {
        "record_id": "HIST-003",
        "category": "general",
        "outcome": "APPROVED",
        "outcome_rationale": "[TODO: Explain why this historical record was approved.]",
        "source_text": (
            "HIST-003 — [TODO: Replace with historical record text relevant to "
            "Scenario B.]"
        ),
    },
    {
        "record_id": "HIST-004",
        "category": "general",
        "outcome": "APPROVED",
        "outcome_rationale": "[TODO: Explain why this historical record was approved.]",
        "source_text": (
            "HIST-004 — [TODO: Replace with historical record text relevant to "
            "Scenario C.]"
        ),
    },
    {
        "record_id": "HIST-005",
        "category": "general",
        "outcome": "DENIED",
        "outcome_rationale": "[TODO: Explain why this historical record was denied.]",
        "source_text": (
            "HIST-005 — [TODO: Add additional historical records as needed. "
            "More examples improve search recall and make the demo more convincing.]"
        ),
    },
]
