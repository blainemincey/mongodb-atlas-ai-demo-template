"""
Healthcare Prior Authorization — demo records.

Three scenarios covering common prior authorization request types:
  A — Medical imaging, MRI knee (clean approval path)
  B — Specialty pharmacy biologic, adalimumab (step therapy exception)
  C — Behavioral health residential treatment (complex PEND path)
"""

DEMO_RECORDS = {
    "A": {
        "record_id": "PA-001-A",
        "scenario": "A",
        "demo_record": True,
        "processing_status": "PENDING",
        "service_type": "medical_imaging",
        "procedure_code": "71550",
        "diagnosis_code": "M17.11",
        "plan_type": "PPO",
        "member_id": "MBR-44821",
        "record_text": (
            "Prior authorization request for MRI of the left knee for member Sarah Chen, "
            "submitted by requesting physician Dr. James Ortega, orthopedic surgeon. "
            "Member has completed six weeks of conservative treatment including eight "
            "sessions of physical therapy and a full course of NSAIDs with insufficient "
            "improvement in function or pain level. Current pain is rated 7 out of 10 at "
            "rest with significant limitation of daily activities. Weight-bearing X-ray "
            "demonstrates moderate joint space narrowing consistent with diagnosis of left "
            "knee osteoarthritis (ICD-10 M17.11). MRI is requested to evaluate soft tissue "
            "structures, assess meniscal and ligamentous integrity, and guide surgical "
            "decision-making. No MRI of this joint has been performed in the past 24 months."
        ),
    },
    "B": {
        "record_id": "PA-001-B",
        "scenario": "B",
        "demo_record": True,
        "processing_status": "PENDING",
        "service_type": "specialty_pharmacy",
        "drug_name": "adalimumab",
        "brand": "Humira",
        "diagnosis_code": "M05.79",
        "plan_type": "HMO",
        "member_id": "MBR-58932",
        "record_text": (
            "Prior authorization request for adalimumab (Humira) for member Marcus Webb, "
            "diagnosed with seropositive rheumatoid arthritis (ICD-10 M05.79) fourteen "
            "months ago, submitted by treating rheumatologist Dr. Patricia Sullivan. "
            "Member has failed two conventional DMARDs: methotrexate trialed for six months "
            "at therapeutic dose, discontinued due to hepatotoxicity confirmed by LFT "
            "elevation, and leflunomide trialed for three months with inadequate response "
            "per DAS28 score of 5.2 at discontinuation. Current DAS28 score is 4.8, "
            "indicating moderate-to-high disease activity. Plan formulary requires step "
            "therapy through conventional DMARDs prior to biologic approval. Prescriber "
            "requests exception based on documented failure of two required DMARD agents "
            "with supporting laboratory and clinical documentation enclosed."
        ),
    },
    "C": {
        "record_id": "PA-001-C",
        "scenario": "C",
        "demo_record": True,
        "processing_status": "PENDING",
        "service_type": "behavioral_health",
        "procedure_code": "H0019",
        "diagnosis_code": "F32.2",
        "plan_type": "PPO",
        "member_id": "MBR-67441",
        "record_text": (
            "Prior authorization request for 28-day residential treatment (HCPCS H0019) "
            "for member David Park, diagnosed with major depressive disorder, severe "
            "(ICD-10 F32.2), submitted by treating psychiatrist Dr. Elena Rodriguez. "
            "Member has two prior acute inpatient admissions within the past 18 months — "
            "seven days and five days respectively — both followed by step-down to "
            "outpatient care that proved insufficient to maintain clinical stability. "
            "Current PHQ-9 score is 21, indicating severe depression, with passive "
            "suicidal ideation without a specific plan documented at most recent assessment. "
            "Member is experiencing multiple acute psychosocial stressors including recent "
            "job loss and housing instability. Outpatient treatment has been unable to "
            "maintain symptom stabilization. Residential level of care is requested as the "
            "least restrictive setting capable of providing the necessary therapeutic "
            "structure and 24-hour clinical support."
        ),
    },
}
