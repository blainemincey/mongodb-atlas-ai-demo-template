"""
Mortgage Underwriting — demo records.

Three scenarios covering the main underwriting paths:
  A — Strong conventional purchase (clean APPROVE path)
  B — Borderline FHA purchase with compensating factors
  C — Jumbo refinance via asset depletion income (REFER path)
"""

DEMO_RECORDS = {
    "A": {
        "record_id": "MTG-001-A",
        "scenario": "A",
        "demo_record": True,
        "processing_status": "PENDING",
        "loan_type": "conventional",
        "loan_amount": 425000,
        "fico_score": 742,
        "dti_ratio": 0.28,
        "ltv_ratio": 0.80,
        "property_type": "single_family",
        "record_text": (
            "Applicant is a 38-year-old software engineer employed 6 years at the same firm, "
            "base salary $142,000, year-end bonus averaging $18,000. W-2 income verified; no "
            "employment gaps. FICO 742, two minor derogatories both over 48 months old, no "
            "collections. Back-end DTI 28%. Purchase price $531,250, 20% down from seasoned "
            "savings, 60-day statements provided. Single-family primary residence, appraised "
            "value matches purchase price. Loan amount $425,000 within conforming limit. "
            "Conventional 30-year fixed rate requested."
        ),
    },
    "B": {
        "record_id": "MTG-001-B",
        "scenario": "B",
        "demo_record": True,
        "processing_status": "PENDING",
        "loan_type": "FHA",
        "loan_amount": 287000,
        "fico_score": 638,
        "dti_ratio": 0.43,
        "ltv_ratio": 0.965,
        "property_type": "single_family",
        "record_text": (
            "Applicant is a 31-year-old registered nurse, employed 2.5 years at a regional "
            "hospital, base salary $68,000 plus $9,200 documented overtime. FICO 638 following "
            "a $2,100 medical collection from 2021 now paid-in-full; no foreclosures or "
            "bankruptcies. Back-end DTI 43% including the new payment. Down payment 3.5% from "
            "savings with full gift fund documentation. Compensating factors: 14 months PITI "
            "reserves and zero late payments on all installment accounts in the past 24 months. "
            "FHA 30-year fixed rate requested on a single-family primary residence."
        ),
    },
    "C": {
        "record_id": "MTG-001-C",
        "scenario": "C",
        "demo_record": True,
        "processing_status": "PENDING",
        "loan_type": "jumbo",
        "loan_amount": 1100000,
        "fico_score": 798,
        "dti_ratio": 0.38,
        "ltv_ratio": 0.73,
        "property_type": "single_family",
        "record_text": (
            "Retired applicant age 67, FICO 798. Qualifying via asset depletion on $4.2 million "
            "in verified liquid assets; monthly income calculated as $9,722 using $2.1 million "
            "eligible assets amortized over 216 months per investor guidelines. Back-end DTI "
            "38%. Cash-out refinance $1.1 million on a property appraised at $1.505 million "
            "(LTV 73%). Cash-out purpose: business investment in a family LLC. Loan amount "
            "exceeds conforming limit and requires jumbo non-agency investor approval. "
            "Applicant has no employment income; all qualifying income is asset-depletion "
            "derived. 15-year fixed rate requested."
        ),
    },
}
