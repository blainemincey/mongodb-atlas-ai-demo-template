"""
Legal Contract Review — historical records.

Past reviewed contract clauses used as analogues during vector search. Outcomes:
  ACCEPTABLE           — clause meets market-standard terms, approved for execution
  FLAG_FOR_REVISION    — clause returned to counterparty with redline comments
  ESCALATE_TO_COUNSEL  — routed to senior counsel for review before any action
"""

HISTORICAL_RECORDS = [
    {
        "record_id": "HIST-001",
        "category": "liability",
        "outcome": "ACCEPTABLE",
        "outcome_rationale": (
            "Mutual limitation of liability with 12-month fee cap and standard carve-outs "
            "was approved as consistent with market-standard enterprise SaaS terms."
        ),
        "source_text": (
            "SaaS MSA clause provided mutual cap on aggregate liability at 12 months of "
            "fees paid in the prior year. Consequential damages exclusion included standard "
            "carve-outs for gross negligence, willful misconduct, and IP indemnification. "
            "Cap applied equally to both parties with no asymmetric provisions. Legal review "
            "confirmed clause as market-standard and approved for execution."
        ),
    },
    {
        "record_id": "HIST-002",
        "category": "liability",
        "outcome": "FLAG_FOR_REVISION",
        "outcome_rationale": (
            "Liability cap was unlimited for the company but capped at $50,000 for the "
            "vendor — flagged as one-sided and returned for revision to mutual market-standard terms."
        ),
        "source_text": (
            "Vendor services agreement proposed a $50,000 aggregate liability cap for the "
            "vendor with no corresponding cap for the company's liability to the vendor. "
            "Contract value was $180,000 annual, making the vendor's cap below one-third "
            "of annual contract value and non-reciprocal. Legal team returned the clause "
            "with redline requesting mutual cap at 12 months of fees paid."
        ),
    },
    {
        "record_id": "HIST-003",
        "category": "IP",
        "outcome": "ACCEPTABLE",
        "outcome_rationale": (
            "IP assignment was properly limited to deliverables under the contract with a "
            "documented pre-existing IP schedule and work-for-hire basis — approved as "
            "market-standard."
        ),
        "source_text": (
            "Consulting agreement IP clause assigned to the company all work product "
            "specifically created for and delivered under the statement of work. Pre-existing "
            "IP schedule was attached as Exhibit A at contract execution documenting "
            "consultant's frameworks and tools. Independent development carve-out was "
            "explicit and tied to absence of company resources. Legal review confirmed "
            "clause as market-standard and approved for execution."
        ),
    },
    {
        "record_id": "HIST-004",
        "category": "IP",
        "outcome": "ESCALATE_TO_COUNSEL",
        "outcome_rationale": (
            "All IP including pre-existing tools and methodologies was assigned without "
            "carve-outs under California law — escalated to senior counsel given "
            "enforceability concerns and litigation risk."
        ),
        "source_text": (
            "Consulting agreement proposed assignment of all IP created or conceived during "
            "the engagement term with no pre-existing IP carve-out and no independent "
            "development exclusion. Agreement was governed by California law. Engagement "
            "was for software development; consultant's core framework would have been "
            "captured by the overbroad assignment. Senior counsel review was required "
            "before any further negotiation or execution."
        ),
    },
    {
        "record_id": "HIST-005",
        "category": "termination",
        "outcome": "ACCEPTABLE",
        "outcome_rationale": (
            "Thirty-day notice for termination for convenience, 30-day cure period for "
            "material breach, and explicit wind-down obligations were approved as "
            "market-standard termination provisions."
        ),
        "source_text": (
            "SaaS services agreement termination clause provided 30-day written notice for "
            "termination for convenience. Termination for material breach required written "
            "notice and 30-day cure period, with immediate termination right for "
            "confidentiality breaches. Wind-down obligations including data export and "
            "transition assistance were specified in an attached schedule. Legal review "
            "confirmed provisions as market-standard and approved."
        ),
    },
    {
        "record_id": "HIST-006",
        "category": "termination",
        "outcome": "FLAG_FOR_REVISION",
        "outcome_rationale": (
            "Five-day termination for convenience notice with no transition assistance "
            "obligations was flagged as insufficient notice and returned for revision to "
            "30-day standard."
        ),
        "source_text": (
            "Vendor agreement proposed 5-day written notice for termination for convenience "
            "on a $150,000 annual managed services contract with no transition assistance "
            "or wind-down obligations. Legal team flagged notice period as well below "
            "30-day market standard and insufficient to allow orderly transition. Clause "
            "was returned with redline requesting 30-day notice and explicit transition "
            "assistance obligations."
        ),
    },
    {
        "record_id": "HIST-007",
        "category": "liability",
        "outcome": "ACCEPTABLE",
        "outcome_rationale": (
            "Mutual indemnification with IP infringement carve-outs in both directions and "
            "a liability cap linked to insurance coverage was approved as market-standard."
        ),
        "source_text": (
            "Professional services agreement included mutual indemnification obligations "
            "covering IP infringement by each party's own deliverables, breach of "
            "representations, and gross negligence. Indemnification cap was linked to "
            "vendor's professional liability insurance coverage minimum of $2,000,000. "
            "Consequential damages exclusion applied to indemnification with standard "
            "carve-outs. Legal review approved as market-standard enterprise terms."
        ),
    },
    {
        "record_id": "HIST-008",
        "category": "IP",
        "outcome": "FLAG_FOR_REVISION",
        "outcome_rationale": (
            "Broad IP assignment clause with only a narrow pre-existing IP carve-out "
            "requiring a documented inventory was returned for revision with guidance on "
            "standard carve-out language."
        ),
        "source_text": (
            "Consulting agreement IP clause assigned all work product created during the "
            "term with a pre-existing IP carve-out limited to IP listed in a schedule "
            "signed at engagement start — but no carve-out for independently developed "
            "IP during the term or open-source components. Legal team returned the clause "
            "with redline adding independent development carve-out language and an "
            "open-source license exception. Revised clause was subsequently approved."
        ),
    },
]
