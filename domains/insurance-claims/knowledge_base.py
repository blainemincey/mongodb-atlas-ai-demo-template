"""
Insurance Claims P&C — knowledge base.

Coverage guidelines and claims handling procedures across auto, property,
and liability categories. Each item's content_text is embedded by Voyage AI
so that relevant guidelines surface when an incoming claim is searched.
"""

KNOWLEDGE_BASE = [
    {
        "kb_id": "KB-001",
        "title": "Auto Collision — Liability Determination and Fault Assessment",
        "category": "auto",
        "subcategory": "liability",
        "content_text": (
            "A police report is the primary evidence for fault determination in an auto "
            "collision claim. Admission of fault at the scene, documented by the responding "
            "officer, constitutes strong liability confirmation and supports standard claim "
            "approval. Third-party witness statements and dashcam footage are secondary "
            "evidence used when no police report is available. When clear liability is "
            "established through police confirmation, the claim proceeds through the standard "
            "approval workflow without field adjuster review. Disputed fault with conflicting "
            "accounts and no police report requires assignment to a field adjuster for "
            "independent liability investigation before a coverage determination is made."
        ),
    },
    {
        "kb_id": "KB-002",
        "title": "Auto Repair — Estimate Process and Shop Authorization",
        "category": "auto",
        "subcategory": "repair",
        "content_text": (
            "Claims exceeding $5,000 require a minimum of three independent repair estimates "
            "before approval. Estimates from preferred network shops take precedence; OEM "
            "parts are required for vehicles under 3 years old and optional for older vehicles "
            "where aftermarket parts meet quality standards. The highest estimate from a "
            "certified network shop is the approved payment ceiling when no appraisal dispute "
            "is raised. Rental car coverage is included for the documented repair duration, "
            "up to 30 days, when the insured vehicle is not drivable due to covered damage. "
            "Supplements for hidden damage discovered during repair are approved with shop "
            "documentation submitted to the claim file."
        ),
    },
    {
        "kb_id": "KB-003",
        "title": "Auto Total Loss — Actual Cash Value Calculation",
        "category": "auto",
        "subcategory": "total-loss",
        "content_text": (
            "Actual cash value for a total loss vehicle is determined using comparable "
            "vehicles in the local market reflecting the same year, make, model, trim level, "
            "mileage, and condition. Aftermarket upgrades — including audio systems, wheels, "
            "and performance modifications — are considered at their depreciated market value, "
            "not installation cost. When the claimant disputes the ACV determination and "
            "provides comparable market evidence, the difference is evaluated against a "
            "$2,000 materiality threshold. Disputes exceeding this threshold trigger the "
            "independent appraisal option under standard policy language. Both parties select "
            "an appraiser; if appraisers disagree, an umpire is appointed to resolve the "
            "difference. The agreed appraisal value is binding on both parties."
        ),
    },
    {
        "kb_id": "KB-004",
        "title": "Auto Total Loss — Salvage Retention Policy",
        "category": "auto",
        "subcategory": "total-loss",
        "content_text": (
            "A claimant may elect to retain the salvage vehicle following a total loss "
            "settlement. When salvage retention is elected, the assessed salvage value is "
            "deducted from the settlement payment per standard policy language. The assessed "
            "salvage value is determined by the insurer's salvage vendor at the time of loss "
            "and is not subject to negotiation separate from the ACV dispute process. "
            "Proceeds from the claimant's independent sale of salvage above the assessed "
            "value remain with the claimant. The insurer retains the right to verify salvage "
            "disposition and title transfer to confirm the vehicle is not returned to road "
            "use without disclosure."
        ),
    },
    {
        "kb_id": "KB-005",
        "title": "Homeowners — Sudden vs. Gradual Water Damage Coverage",
        "category": "property",
        "subcategory": "water",
        "content_text": (
            "Homeowners policies cover sudden and accidental discharge or overflow of water "
            "from plumbing systems, including burst pipes and abrupt appliance supply line "
            "failures. Coverage is excluded for gradual seepage, continuous or repeated "
            "leakage, and damage resulting from deterioration over time that the insured "
            "knew or should have known about. The distinction between sudden and gradual "
            "is determined by physical inspection: sudden damage shows no pre-existing "
            "staining, no mold or microbial growth consistent with extended moisture, and "
            "damage confined to the period of absence or non-use. Gradual damage indicators "
            "include staining older than 72 hours, mineral deposits on plumbing fittings, "
            "structural softening of wood substrates, and mold growth requiring more than "
            "48–72 hours to develop."
        ),
    },
    {
        "kb_id": "KB-006",
        "title": "Property Claim — Inspection Requirements and Documentation",
        "category": "property",
        "subcategory": "documentation",
        "content_text": (
            "An on-site property inspection by an insurer-assigned adjuster is required for "
            "all property claims exceeding $10,000. The inspection must be completed before "
            "a coverage determination is issued. Contractor documentation submitted with the "
            "claim must include a cause-of-loss assessment, itemized repair scope, and "
            "estimated timeline. When the contractor's cause-of-loss assessment conflicts "
            "with the adjuster's inspection findings, a second independent inspection is "
            "required before the claim is resolved. Photographs documenting damage extent, "
            "staining patterns, and material condition must be retained in the claim file "
            "for any property claim over $5,000."
        ),
    },
    {
        "kb_id": "KB-007",
        "title": "Property Claim — Gradual Damage Exclusion Application",
        "category": "property",
        "subcategory": "exclusions",
        "content_text": (
            "The gradual damage exclusion applies when inspection evidence demonstrates "
            "that damage occurred over an extended period rather than as a discrete sudden "
            "event. Key indicators that support application of the exclusion include: "
            "staining patterns consistent with moisture exposure older than 72 hours, "
            "presence of mold or microbial growth requiring extended moisture conditions, "
            "mineral deposits or scale buildup on plumbing fittings indicating long-term "
            "leakage, and structural softening or deterioration of wood substrates. "
            "The burden of proof rests with the insurer to demonstrate gradual onset "
            "through physical evidence documented by the adjuster. When evidence is "
            "ambiguous, the claim is escalated to a senior adjuster for a final coverage "
            "determination before denial is issued."
        ),
    },
    {
        "kb_id": "KB-008",
        "title": "Claims Investigation — Escalation Criteria for Disputed Claims",
        "category": "liability",
        "subcategory": "investigation",
        "content_text": (
            "Claims involving disputed liability with conflicting accounts and no police "
            "report, or disputes exceeding $10,000, require field adjuster review before "
            "a determination is issued. ACV disputes where the claimant's evidence exceeds "
            "the insurer's valuation by more than $2,000 trigger the independent appraisal "
            "option under policy language. Coverage disputes involving interpretation of "
            "policy exclusions — including the sudden vs. gradual water damage distinction "
            "— require supervisor or senior adjuster review before a denial is issued. "
            "All escalated claims must have a written escalation rationale in the claim "
            "file and a claimant notification issued within 5 business days of escalation."
        ),
    },
]
