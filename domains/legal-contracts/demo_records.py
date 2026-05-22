"""
Legal Contract Review — demo records.

Three scenarios covering common contract clause review types:
  A — Limitation of liability clause, mutual and capped (clean acceptable path)
  B — One-sided broad indemnification clause (needs revision)
  C — Overly broad IP assignment clause, no carve-outs (escalate to counsel)
"""

DEMO_RECORDS = {
    "A": {
        "record_id": "CTR-001-A",
        "scenario": "A",
        "demo_record": True,
        "processing_status": "PENDING",
        "clause_type": "limitation_of_liability",
        "contract_type": "software_services",
        "risk_level": "low",
        "jurisdiction": "Delaware",
        "counterparty_type": "enterprise_customer",
        "record_text": (
            "Limitation of liability clause submitted for review from a SaaS Master Service "
            "Agreement. Clause provides mutual cap on liability at 12 months of fees paid in "
            "the preceding 12 months. Both parties excluded from liability for indirect, "
            "incidental, or consequential damages with standard carve-outs for gross negligence, "
            "willful misconduct, indemnification obligations, and IP infringement. Cap applies "
            "equally to both parties. Contract value: $240,000 annual. Counterparty is a "
            "Fortune 500 enterprise customer represented by in-house counsel. No unusual "
            "deviations from standard market terms detected by legal intake team. Prior reviewed "
            "contracts in this category from same customer type have been consistently acceptable."
        ),
    },
    "B": {
        "record_id": "CTR-001-B",
        "scenario": "B",
        "demo_record": True,
        "processing_status": "PENDING",
        "clause_type": "indemnification",
        "contract_type": "vendor_agreement",
        "risk_level": "high",
        "jurisdiction": "California",
        "counterparty_type": "vendor",
        "record_text": (
            "Indemnification clause submitted for review from a vendor services agreement. "
            "Vendor's proposed clause requires the company to indemnify, defend, and hold "
            "harmless the vendor against all claims arising from the company's \"use, operation, "
            "or business activities\" without limitation on scope. No reciprocal indemnification "
            "from vendor to company. No cap on indemnification obligations. Carve-outs are "
            "limited to vendor gross negligence only — no exclusion for vendor's breach of "
            "contract or IP infringement claims. Contract value: $85,000 annual for managed IT "
            "services. Legal intake flagged the one-sided indemnification and lack of IP "
            "infringement carve-out as requiring revision before signing."
        ),
    },
    "C": {
        "record_id": "CTR-001-C",
        "scenario": "C",
        "demo_record": True,
        "processing_status": "PENDING",
        "clause_type": "ip_assignment",
        "contract_type": "consulting_agreement",
        "risk_level": "critical",
        "jurisdiction": "New York",
        "counterparty_type": "consultant",
        "record_text": (
            "IP assignment clause submitted for review from a consulting services agreement. "
            "Consultant's proposed clause assigns to the company all intellectual property "
            "\"created, developed, or conceived\" by the consultant \"at any time during the "
            "term of this agreement\" without limiting the assignment to work performed under "
            "the contract. No carve-out for consultant's pre-existing IP, tools, methodologies, "
            "or works created outside the scope of engagement. No carve-out for consultant's "
            "independently developed IP unrelated to company's business. Assignment extends to "
            "moral rights waiver in all jurisdictions. Consulting engagement is for software "
            "architecture design, 6-month term. Legal intake flagged the clause as critically "
            "overbroad — assignment with no carve-outs creates litigation risk and may be "
            "unenforceable in New York, requiring full counsel review before proceeding."
        ),
    },
}
