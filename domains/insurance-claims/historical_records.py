"""
Insurance Claims P&C — historical records.

Past claim decisions used as analogues during vector search. Outcomes:
  APPROVED             — claim approved and payment processed
  DENIED               — claim denied with policy language citation
  NEEDS_INVESTIGATION  — claim escalated for additional review
"""

HISTORICAL_RECORDS = [
    {
        "record_id": "HIST-001",
        "category": "auto",
        "outcome": "APPROVED",
        "outcome_rationale": (
            "Rear-end collision with police report confirming fault and repair estimate "
            "within policy limits. Claim approved within 3 business days; payment processed "
            "for repair amount less deductible, with rental car authorized for repair period."
        ),
        "source_text": (
            "Claimant's vehicle was rear-ended at a stop sign; police report filed and "
            "at-fault driver's insurer confirmed liability. Two certified shop estimates "
            "were consistent; preferred shop estimate of $6,950 was approved. No injuries "
            "reported. Rental coverage authorized for 5 days. Claim closed with standard "
            "payment within 3 business days of documentation receipt."
        ),
    },
    {
        "record_id": "HIST-002",
        "category": "auto",
        "outcome": "NEEDS_INVESTIGATION",
        "outcome_rationale": (
            "Collision involved disputed fault with no police report and two conflicting "
            "accounts of the incident. Claim sent to field adjuster for independent "
            "liability investigation before a coverage determination could be issued."
        ),
        "source_text": (
            "Two-vehicle collision at an uncontrolled intersection with no witnesses and "
            "no police report. Each driver claimed the other failed to yield. Dashcam "
            "footage was unavailable from either vehicle. Insurer could not establish "
            "fault from available documentation. Claim escalated to field adjuster for "
            "scene reconstruction and independent liability assessment."
        ),
    },
    {
        "record_id": "HIST-003",
        "category": "property",
        "outcome": "APPROVED",
        "outcome_rationale": (
            "Burst pipe caused water damage confined to a 48-hour window confirmed by "
            "adjuster inspection. No prior staining or mold present; damage was sudden "
            "and accidental. Claim approved under standard homeowners coverage."
        ),
        "source_text": (
            "Claimant reported a burst supply pipe in the basement that flooded the "
            "laundry room and adjacent hallway. Adjuster inspection found no pre-existing "
            "staining, no mold, and damage consistent with a single acute water event. "
            "Contractor timeline estimate was consistent with a 24–48 hour water exposure "
            "window. Claim approved; payment issued for extraction, drying, and flooring "
            "replacement less deductible."
        ),
    },
    {
        "record_id": "HIST-004",
        "category": "property",
        "outcome": "DENIED",
        "outcome_rationale": (
            "Water damage inspection confirmed gradual leakage over 4-plus weeks based on "
            "mold growth, cabinet staining, and mineral deposits on the supply fitting. "
            "Gradual damage exclusion applied; denial issued with policy language citation."
        ),
        "source_text": (
            "Claimant reported kitchen water damage attributed to a leaking dishwasher "
            "supply line. Adjuster found mold covering approximately 40% of the cabinet "
            "base, staining consistent with 4 to 6 weeks of moisture exposure, and "
            "significant mineral scale on the fitting. Contractor confirmed deteriorated "
            "hose clamp not consistent with sudden failure. Gradual damage exclusion "
            "applied; denial issued with claimant advised of appeal rights."
        ),
    },
    {
        "record_id": "HIST-005",
        "category": "auto",
        "outcome": "APPROVED",
        "outcome_rationale": (
            "Total loss declared by adjuster; claimant accepted insurer's ACV determination "
            "without dispute. Standard settlement issued with salvage transferred to insurer "
            "and net payment processed after deductible."
        ),
        "source_text": (
            "Claimant's 2019 Honda CR-V was declared a total loss following a front-end "
            "collision. Adjuster's ACV of $22,400 was based on five comparable local "
            "market vehicles. Claimant reviewed the comparables and accepted the valuation. "
            "Salvage transferred to insurer's auction vendor. Settlement payment of $21,900 "
            "issued (ACV less $500 deductible) within 5 business days."
        ),
    },
    {
        "record_id": "HIST-006",
        "category": "auto",
        "outcome": "NEEDS_INVESTIGATION",
        "outcome_rationale": (
            "Claimant disputed ACV by $3,200, providing three comparable listings citing "
            "aftermarket upgrades. Dispute exceeded the $2,000 materiality threshold, "
            "triggering the independent appraisal option under policy language."
        ),
        "source_text": (
            "Total loss claim on a 2020 Chevrolet Silverado; insurer's ACV was $34,100. "
            "Claimant disputed, citing aftermarket lift kit, custom wheels, and upgraded "
            "exhaust valued at the time of installation at $4,800. Claimant provided three "
            "comparable listings averaging $37,300. Dispute of $3,200 exceeded the $2,000 "
            "threshold; independent appraisal process initiated per policy. Appraisers "
            "agreed on a final ACV of $35,600."
        ),
    },
    {
        "record_id": "HIST-007",
        "category": "property",
        "outcome": "NEEDS_INVESTIGATION",
        "outcome_rationale": (
            "Water damage claim produced conflicting cause-of-loss assessments from the "
            "claimant's contractor and the insurer's adjuster. Claim escalated to senior "
            "adjuster for additional inspection before a coverage determination."
        ),
        "source_text": (
            "Claimant reported bathroom water damage from an overhead pipe. Claimant's "
            "contractor assessed the damage as resulting from sudden pipe failure. The "
            "insurer's adjuster found staining patterns suggesting 2 to 3 weeks of prior "
            "moisture exposure. The two assessments directly conflicted on cause of loss. "
            "Claim escalated to a senior adjuster who ordered an independent inspection; "
            "final determination deferred pending second inspection report."
        ),
    },
    {
        "record_id": "HIST-008",
        "category": "liability",
        "outcome": "APPROVED",
        "outcome_rationale": (
            "Slip and fall on commercial property with clear surveillance footage confirming "
            "liability. Medical damages and general damages approved; liability confirmed "
            "without dispute from the insured commercial property owner."
        ),
        "source_text": (
            "Claimant slipped on a wet floor in an insured retail property. Surveillance "
            "footage showed a spill left unattended for 22 minutes before the incident "
            "with no wet floor signage present. Insured's property manager confirmed no "
            "corrective action had been taken. Liability was not contested. Medical "
            "expenses of $4,200 and general damages of $8,000 were approved; settlement "
            "executed within 30 days."
        ),
    },
]
