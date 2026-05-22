"""
Demo records for the Atlas AI Demo scaffold.

REQUIRED fields (the scaffold depends on these):
  - record_id       : str  — unique ID, e.g. "REC-001-A"
  - scenario        : str  — "A", "B", or "C"
  - demo_record     : bool — must be True; used to find demo docs in MongoDB
  - record_text     : str  — the unstructured text that gets embedded by Voyage AI
  - record_embedding: absent on insert; written back by the /embed endpoint

OPTIONAL fields (domain-specific — add whatever your demo needs):
  Any additional fields you include will pass through to the frontend via the
  [key: string]: unknown index on DemoRecord in types.ts.

TODO: Replace the stub record_text values and add domain-specific fields for
your target use case before running setup.py.
"""

DEMO_RECORDS = {
    "A": {
        "record_id": "REC-001-A",
        "scenario": "A",
        "demo_record": True,
        "processing_status": "PENDING",
        # ----------------------------------------------------------------
        # TODO: Replace with Scenario A domain-specific text and fields.
        # record_text is the field embedded by Voyage AI — make it rich
        # enough to produce meaningful vector search results.
        # ----------------------------------------------------------------
        "record_text": (
            "Scenario A — [TODO: replace with domain-specific unstructured text "
            "that describes this record. This is the field Voyage AI will embed, "
            "so include the relevant terminology, categories, and context that "
            "should match items in your knowledge_base and historical_records.]"
        ),
        # TODO: Add domain-specific structured fields here, e.g.:
        # "category": "...",
        # "subcategory": "...",
        # "requestor_id": "...",
    },
    "B": {
        "record_id": "REC-001-B",
        "scenario": "B",
        "demo_record": True,
        "processing_status": "PENDING",
        # ----------------------------------------------------------------
        # TODO: Replace with Scenario B domain-specific text and fields.
        # ----------------------------------------------------------------
        "record_text": (
            "Scenario B — [TODO: replace with domain-specific unstructured text "
            "for the second use case. Should produce different vector search "
            "results than Scenario A to illustrate multiple use cases.]"
        ),
        # TODO: Add domain-specific structured fields here.
    },
    "C": {
        "record_id": "REC-001-C",
        "scenario": "C",
        "demo_record": True,
        "processing_status": "PENDING",
        # ----------------------------------------------------------------
        # TODO: Replace with Scenario C domain-specific text and fields.
        # ----------------------------------------------------------------
        "record_text": (
            "Scenario C — [TODO: replace with domain-specific unstructured text "
            "for the third use case.]"
        ),
        # TODO: Add domain-specific structured fields here.
    },
}
