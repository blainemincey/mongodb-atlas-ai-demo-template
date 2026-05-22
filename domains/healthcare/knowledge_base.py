"""
Healthcare Prior Authorization — knowledge base.

Clinical coverage policies and medical necessity criteria across medical,
pharmacy, and behavioral health categories. Each item's content_text is
embedded by Voyage AI so that relevant policies surface when an incoming
prior authorization request is searched.
"""

KNOWLEDGE_BASE = [
    {
        "kb_id": "KB-001",
        "title": "MRI Medical Necessity Criteria — Orthopedic Indications",
        "category": "medical",
        "subcategory": "musculoskeletal",
        "content_text": (
            "MRI of the extremities or joints is medically necessary when the member has "
            "completed at least six weeks of conservative treatment — including physical "
            "therapy and anti-inflammatory medication — with documented insufficient "
            "improvement in pain or function. Authorization requires progression from "
            "prior diagnostic imaging such as X-ray and a clinical rationale explaining "
            "why MRI findings will change clinical management. MRI is appropriate for "
            "surgical planning when weight-bearing imaging demonstrates structural changes "
            "consistent with moderate or severe joint disease. Studies requested solely "
            "for symptom monitoring without a treatment decision point do not meet medical "
            "necessity criteria."
        ),
    },
    {
        "kb_id": "KB-002",
        "title": "Imaging Authorization — Documentation Requirements",
        "category": "medical",
        "subcategory": "documentation",
        "content_text": (
            "All imaging prior authorization requests must include current physician "
            "clinical notes dated within 90 days, records documenting prior conservative "
            "treatment with dates and response, supporting diagnostic imaging such as "
            "X-ray with radiology interpretation, the ICD-10 diagnosis code, the CPT or "
            "procedure code for the requested study, and a clinical rationale statement "
            "explaining how findings will guide treatment. Submissions lacking prior "
            "treatment documentation or without a clear clinical decision point may be "
            "pended for additional information. Incomplete submissions should be returned "
            "to the requesting provider with a specific documentation checklist."
        ),
    },
    {
        "kb_id": "KB-003",
        "title": "Specialty Pharmacy — Biologic DMARD Step Therapy Requirements",
        "category": "pharmacy",
        "subcategory": "biologics",
        "content_text": (
            "The plan requires trial and documented failure of at least two conventional "
            "disease-modifying antirheumatic drugs (DMARDs) before a biologic agent will "
            "be authorized for inflammatory arthritis indications. Qualifying conventional "
            "DMARDs include methotrexate, sulfasalazine, hydroxychloroquine, and "
            "leflunomide. Failure is defined as an adequate trial of at least three months "
            "at a therapeutic dose with inadequate clinical response, or discontinuation "
            "due to a documented adverse effect or contraindication requiring cessation "
            "before three months. Prescriber attestation with supporting clinical "
            "documentation is required for each failed agent."
        ),
    },
    {
        "kb_id": "KB-004",
        "title": "Specialty Pharmacy — Step Therapy Exception Criteria",
        "category": "pharmacy",
        "subcategory": "exceptions",
        "content_text": (
            "Step therapy exceptions for biologic agents may be approved when the member "
            "has a documented intolerance, adverse reaction, or medical contraindication "
            "to required conventional DMARD agents, or when failure of two required agents "
            "is fully documented. Exception requests must include laboratory results "
            "supporting adverse effects, DAS28 or equivalent disease activity scores, "
            "prescriber attestation, and clinical notes describing the course of each "
            "prior DMARD trial. Exceptions are not granted based on prescriber preference "
            "alone or anticipated efficacy without documented prior treatment history."
        ),
    },
    {
        "kb_id": "KB-005",
        "title": "Behavioral Health Residential Treatment — Level of Care Criteria",
        "category": "behavioral_health",
        "subcategory": "level-of-care",
        "content_text": (
            "Residential level of care is clinically indicated when outpatient treatment "
            "is insufficient to maintain member safety or psychiatric stability, the member "
            "has failed or is unable to benefit from a lower level of care, and 24-hour "
            "therapeutic structure is medically necessary. Clinical criteria include PHQ-9 "
            "or GAF score documentation reflecting severe symptom burden, current or recent "
            "safety risk assessment, prior level of care history, and a treatment plan "
            "demonstrating goals achievable only in a residential setting. Residential "
            "authorization should be the least restrictive level that can safely meet the "
            "member's clinical needs."
        ),
    },
    {
        "kb_id": "KB-006",
        "title": "Behavioral Health — Prior Inpatient History and Step-Down Authorization",
        "category": "behavioral_health",
        "subcategory": "authorization",
        "content_text": (
            "Members with two or more acute inpatient psychiatric admissions within an "
            "18-month period who have not maintained clinical stability at an outpatient "
            "level of care meet the clinical threshold for residential treatment "
            "consideration under this policy. Authorization requires documentation of each "
            "prior inpatient admission including dates, length of stay, and discharge "
            "diagnosis, as well as records of outpatient treatment attempts following each "
            "discharge and the clinical basis for the current request. Failure to maintain "
            "stability at outpatient or intensive outpatient level of care after two "
            "inpatient episodes is a strong clinical indicator supporting residential "
            "authorization."
        ),
    },
    {
        "kb_id": "KB-007",
        "title": "Pharmacy Coverage — Rheumatoid Arthritis Biologic Policy",
        "category": "pharmacy",
        "subcategory": "RA",
        "content_text": (
            "Biologic DMARDs for rheumatoid arthritis — including TNF inhibitors such as "
            "adalimumab, etanercept, and certolizumab, and IL-6 inhibitors such as "
            "tocilizumab — are covered under the specialty pharmacy tier and require prior "
            "authorization. Clinical criteria for approval include active moderate-to-severe "
            "RA as documented by DAS28 score greater than 3.2, completion of the required "
            "DMARD step therapy protocol, absence of contraindications to the requested "
            "biologic, and a current prescription from a board-certified rheumatologist "
            "or treating physician. Renewal authorization requires documentation of "
            "clinical response and continued medical necessity."
        ),
    },
    {
        "kb_id": "KB-008",
        "title": "Clinical Documentation — Prior Authorization Submission Standards",
        "category": "medical",
        "subcategory": "compliance",
        "content_text": (
            "All prior authorization submissions must include current clinical notes dated "
            "within 90 days of the request, an ICD-10 diagnosis code matching the clinical "
            "indication, the CPT or HCPCS procedure code or drug name and NDC for pharmacy "
            "requests, a clinical rationale statement, and documented prior treatment "
            "history relevant to the request. Submissions that are missing required "
            "elements may be assigned a PEND status and returned to the requesting provider "
            "with a request for additional documentation within the applicable turnaround "
            "time. Persistently incomplete submissions after two documentation requests "
            "may result in a denial for failure to provide information."
        ),
    },
]
