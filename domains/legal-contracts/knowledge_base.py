"""
Legal Contract Review — knowledge base.

Contract standards and legal guidelines across liability, IP, and termination
categories. Each item's content_text is embedded by Voyage AI so that relevant
standards surface when an incoming clause is searched.
"""

KNOWLEDGE_BASE = [
    {
        "kb_id": "KB-001",
        "title": "Limitation of Liability — Market-Standard Cap Provisions",
        "category": "liability",
        "subcategory": "liability-cap",
        "content_text": (
            "Standard SaaS and professional services agreements cap aggregate liability at "
            "12 months of fees paid in the preceding 12-month period. Mutual caps — applying "
            "equally to both parties — are the market norm for enterprise agreements. "
            "Exceptions to the cap are required for death and personal injury, fraud, gross "
            "negligence, and willful misconduct. A consequential damages exclusion with "
            "standard carve-outs for IP indemnification obligations and confidentiality "
            "breaches is acceptable market practice. Caps below 3 months of fees or caps "
            "applying only to one party are non-standard and require further negotiation."
        ),
    },
    {
        "kb_id": "KB-002",
        "title": "Indemnification — Mutual vs. One-Sided Obligations",
        "category": "liability",
        "subcategory": "indemnification",
        "content_text": (
            "Market standard for enterprise and vendor agreements requires mutual "
            "indemnification: each party indemnifies the other for its own IP infringement "
            "claims, breach of representations and warranties, and gross negligence. "
            "One-sided indemnification — where the company indemnifies the vendor without "
            "reciprocal protection — creates unreasonable and non-market risk exposure. "
            "Company-favorable minimum terms require the vendor to indemnify the company "
            "for IP infringement claims related to the vendor's deliverables or pre-existing "
            "IP. Any proposal that removes the vendor's IP indemnification obligation should "
            "be returned for revision."
        ),
    },
    {
        "kb_id": "KB-003",
        "title": "Indemnification — Scope and Carve-Out Requirements",
        "category": "liability",
        "subcategory": "indemnification",
        "content_text": (
            "Indemnification triggered by \"all claims arising from use or business "
            "activities\" is overbroad and should be revised to specifically enumerated "
            "triggers: breach of contract, IP infringement, gross negligence, and willful "
            "misconduct. Open-ended scope language exposes the company to indemnification "
            "obligations for the vendor's own errors or third-party claims unrelated to the "
            "company's actions. A cap on indemnification obligations — typically linked to "
            "the liability cap or the vendor's insurance coverage — is standard market "
            "practice and should be included. Indemnification obligations that are uncapped "
            "create material financial exposure and should always be flagged for revision."
        ),
    },
    {
        "kb_id": "KB-004",
        "title": "IP Assignment — Work Made for Hire and Scope Limitations",
        "category": "IP",
        "subcategory": "assignment",
        "content_text": (
            "IP assignment in consulting agreements should be limited to work product "
            "specifically created for and under the engagement. Assignment language that "
            "covers all IP \"created, developed, or conceived\" during the term — without "
            "tying it to the scope of work — is a recognized overreach that creates "
            "litigation risk and may deter future consultants. Pre-existing IP, "
            "independently developed tools, and general methodologies that the consultant "
            "brought to the engagement must be explicitly carved out to ensure the "
            "consultant can continue to use their own tools in subsequent engagements. "
            "Clauses without these limitations may be challenged as unenforceable "
            "restraints of trade, particularly in New York and California."
        ),
    },
    {
        "kb_id": "KB-005",
        "title": "IP Assignment — Standard Carve-Out Provisions",
        "category": "IP",
        "subcategory": "assignment",
        "content_text": (
            "Standard carve-outs required in any IP assignment clause: (1) consultant's "
            "pre-existing IP documented in a schedule at engagement start; (2) IP developed "
            "independently without use of company resources, facilities, or confidential "
            "information; (3) open-source components subject to their own licenses. "
            "Failure to include pre-existing IP carve-outs may prevent the consultant from "
            "using their own foundational tools and frameworks in future work, making the "
            "clause practically unenforceable and legally questionable. A moral rights waiver "
            "that applies across all jurisdictions without corresponding compensation is "
            "non-standard and creates enforceability questions in jurisdictions where moral "
            "rights are inalienable."
        ),
    },
    {
        "kb_id": "KB-006",
        "title": "Termination for Convenience — Notice Period Standards",
        "category": "termination",
        "subcategory": "convenience",
        "content_text": (
            "Standard notice periods for termination for convenience: 30 days for contracts "
            "with annual value under $250,000; 60 days for contracts at or above $250,000. "
            "Wind-down obligations — including data export, transition assistance, and "
            "handoff documentation — should be specified explicitly in the termination "
            "clause rather than left to negotiation at termination time. Early termination "
            "fees are acceptable only when the formula is clearly defined and tied to "
            "actual unrecovered costs or a reasonable estimate. Notice periods below 15 "
            "days for any contract value are non-standard and should be returned for revision."
        ),
    },
    {
        "kb_id": "KB-007",
        "title": "Termination for Cause — Cure Period and Trigger Criteria",
        "category": "termination",
        "subcategory": "cause",
        "content_text": (
            "Termination for material breach requires a 30-day written cure period after "
            "delivery of notice, except for payment default (10-day cure) and "
            "confidentiality or IP breaches (immediate termination right). The definition "
            "of 'material breach' should be specific and enumerated rather than open-ended "
            "to reduce dispute risk at the point of termination. Termination for cause "
            "without a cure period — except for the carve-outs above — is non-standard "
            "and creates termination-for-convenience risk. Both parties should have "
            "equivalent termination-for-cause rights; asymmetric termination rights "
            "favoring one party should be flagged for revision."
        ),
    },
    {
        "kb_id": "KB-008",
        "title": "Governing Law and Dispute Resolution — Standard Provisions",
        "category": "liability",
        "subcategory": "governing-law",
        "content_text": (
            "Preferred governing law jurisdictions for enterprise agreements are Delaware "
            "and New York, which provide predictable and commercially sophisticated legal "
            "frameworks. California governing law in consulting and vendor agreements "
            "creates employee-favorable interpretations for contractor relationships and "
            "may affect IP assignment enforceability, restrictive covenants, and "
            "indemnification analysis. Arbitration clauses are acceptable when governed "
            "by JAMS or AAA rules with a specified seat of arbitration. Class action "
            "waivers should be mutual; one-sided class action waivers are increasingly "
            "subject to challenge. Venue selection clauses should be consistent with "
            "governing law jurisdiction."
        ),
    },
]
