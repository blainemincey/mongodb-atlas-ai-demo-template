"""
Healthcare Prior Authorization — historical records.

Past prior authorization decisions used as analogues during vector search.
Outcomes:
  APPROVED         — authorization granted based on criteria met
  DENIED           — authorization denied, criteria not met
  PEND_FOR_REVIEW  — pended pending additional clinical documentation
"""

HISTORICAL_RECORDS = [
    {
        "record_id": "HIST-001",
        "category": "medical",
        "outcome": "APPROVED",
        "outcome_rationale": (
            "MRI knee authorized after member demonstrated six weeks of conservative "
            "treatment with physical therapy and NSAIDs, X-ray confirming osteoarthritis, "
            "and clinical rationale for surgical planning. All medical necessity criteria met."
        ),
        "source_text": (
            "Member presented with left knee pain and functional limitation. Treating "
            "orthopedic surgeon documented six weeks of physical therapy (eight sessions) "
            "and NSAID trial without sufficient improvement. X-ray showed moderate joint "
            "space narrowing consistent with osteoarthritis. MRI requested for surgical "
            "planning and soft tissue evaluation. Prior authorization approved — all "
            "imaging medical necessity criteria met and documentation complete."
        ),
    },
    {
        "record_id": "HIST-002",
        "category": "medical",
        "outcome": "DENIED",
        "outcome_rationale": (
            "MRI knee denied because the submission contained no documentation of prior "
            "conservative treatment. Criteria require at least six weeks of physical "
            "therapy or equivalent conservative management before imaging is authorized."
        ),
        "source_text": (
            "Member reported knee pain of two weeks duration. Requesting physician "
            "submitted MRI prior authorization without documentation of any prior "
            "conservative treatment, physical therapy, or diagnostic imaging. No X-ray "
            "or clinical notes supporting disease severity were included. Authorization "
            "denied — medical necessity criteria for imaging require documented failure "
            "of conservative treatment prior to advanced imaging. Member advised to "
            "complete required conservative treatment course."
        ),
    },
    {
        "record_id": "HIST-003",
        "category": "pharmacy",
        "outcome": "APPROVED",
        "outcome_rationale": (
            "Adalimumab step therapy exception approved after member documented failure "
            "of two conventional DMARDs — methotrexate (adverse effect) and sulfasalazine "
            "(inadequate response at six months) — with supporting laboratory and DAS28 "
            "score documentation."
        ),
        "source_text": (
            "Rheumatologist submitted adalimumab prior authorization for member with "
            "seropositive RA. Documentation included methotrexate trial with LFT "
            "elevation requiring discontinuation and a six-month sulfasalazine trial "
            "with DAS28 4.6 at discontinuation indicating inadequate response. Current "
            "DAS28 was 5.1. Step therapy exception criteria met with two fully documented "
            "DMARD failures. Prior authorization approved for adalimumab 40 mg biweekly."
        ),
    },
    {
        "record_id": "HIST-004",
        "category": "pharmacy",
        "outcome": "DENIED",
        "outcome_rationale": (
            "Biologic authorization denied because the member had completed only three "
            "weeks of DMARD trial — well short of the required minimum three-month "
            "therapeutic trial. Step therapy requirements were not met."
        ),
        "source_text": (
            "Prescriber submitted request for etanercept for member with newly diagnosed "
            "RA. Clinical notes showed methotrexate was initiated three weeks prior with "
            "no documented adverse effects. No second DMARD had been trialed. Member had "
            "not met the plan's step therapy requirement of documented failure of two "
            "conventional DMARDs at therapeutic doses for at least three months each. "
            "Request denied — inadequate step therapy documentation. Prescriber directed "
            "to continue DMARD trial and resubmit with complete documentation."
        ),
    },
    {
        "record_id": "HIST-005",
        "category": "behavioral_health",
        "outcome": "PEND_FOR_REVIEW",
        "outcome_rationale": (
            "Residential treatment request pended for additional documentation because "
            "this was the member's first depressive episode with no prior inpatient "
            "history. Clinical reviewer requested outpatient treatment records and a "
            "current safety assessment before determination."
        ),
        "source_text": (
            "Member with first episode major depressive disorder, moderate severity, "
            "was referred directly to residential treatment without prior inpatient "
            "admission or documented intensive outpatient or partial hospitalization "
            "program trial. PHQ-9 score 16. No active suicidal ideation documented. "
            "Residential authorization pended — clinical reviewer requested outpatient "
            "treatment records for prior six months, documentation of any lower level "
            "of care attempts, and a current safety plan prior to determination."
        ),
    },
    {
        "record_id": "HIST-006",
        "category": "behavioral_health",
        "outcome": "APPROVED",
        "outcome_rationale": (
            "Residential treatment approved based on two prior acute inpatient admissions "
            "within 12 months, PHQ-9 of 22, documented failure of multiple outpatient "
            "treatment courses, and active safety risk requiring structured clinical "
            "support."
        ),
        "source_text": (
            "Member with recurrent major depressive disorder presented with two acute "
            "inpatient admissions in the preceding 12 months, each followed by outpatient "
            "treatment that failed to maintain stability. Current PHQ-9 score was 22. "
            "Treating psychiatrist documented passive suicidal ideation and inability to "
            "maintain safety contract in outpatient setting. Multiple psychosocial "
            "stressors present. Residential prior authorization approved — criteria for "
            "level of care met based on recurrent inpatient history, severe symptom "
            "burden, and failure at lower levels of care."
        ),
    },
    {
        "record_id": "HIST-007",
        "category": "medical",
        "outcome": "APPROVED",
        "outcome_rationale": (
            "MRI shoulder authorized after member completed eight weeks of physical therapy "
            "for rotator cuff symptoms without adequate improvement, with surgical planning "
            "as the documented clinical decision point."
        ),
        "source_text": (
            "Member reported right shoulder pain with range-of-motion limitation. "
            "Orthopedic surgeon documented eight weeks of physical therapy and a course "
            "of NSAIDs with persistent pain and functional deficit. X-ray showed no "
            "acute fracture but soft tissue pathology was suspected. MRI requested for "
            "rotator cuff evaluation and surgical planning. All medical necessity criteria "
            "met — conservative treatment documented, clinical decision point stated, "
            "prior imaging reviewed. Authorization approved."
        ),
    },
    {
        "record_id": "HIST-008",
        "category": "pharmacy",
        "outcome": "PEND_FOR_REVIEW",
        "outcome_rationale": (
            "Biologic authorization pended because only one DMARD failure was documented "
            "at submission. Prescriber was requested to provide evidence of a second "
            "DMARD trial or documented contraindication before determination."
        ),
        "source_text": (
            "Rheumatologist submitted prior authorization for certolizumab for member "
            "with seropositive RA. Clinical notes documented methotrexate failure due "
            "to hepatotoxicity after four months of therapy with supporting LFT results. "
            "No second DMARD trial was documented and no contraindication to second-line "
            "DMARDs was stated. Plan step therapy policy requires two documented DMARD "
            "failures or documented contraindications. Authorization pended — prescriber "
            "requested to submit evidence of second DMARD trial or formal contraindication "
            "documentation within 14 days."
        ),
    },
]
