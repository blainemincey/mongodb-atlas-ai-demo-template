"""
Mortgage Underwriting — historical records.

Past loan decisions used as analogues during vector search. Outcomes:
  APPROVED                    — loan approved for commitment
  DENIED                      — loan denied with adverse action
  REFER_TO_SENIOR_UNDERWRITER — routed to senior underwriter queue
"""

HISTORICAL_RECORDS = [
    {
        "record_id": "HIST-001",
        "category": "conventional",
        "outcome": "APPROVED",
        "outcome_rationale": (
            "Strong W-2 borrower profile: FICO 755, DTI 31%, 20% down from seasoned funds. "
            "Loan within conforming limits. Standard approval with no conditions."
        ),
        "source_text": (
            "Purchase of single-family primary residence, conventional 30-year fixed, "
            "$412,000 loan. Borrower employed 8 years as a project manager, income $138,000 "
            "W-2. FICO 755, clean credit history, DTI 31%, LTV 80%. Down payment from "
            "seasoned savings. Appraisal at purchase price. AUS approval, no conditions."
        ),
    },
    {
        "record_id": "HIST-002",
        "category": "conventional",
        "outcome": "DENIED",
        "outcome_rationale": (
            "Back-end DTI of 52% exceeded the 45% maximum for conventional conforming loans "
            "and could not be supported by compensating factors. Adverse action issued citing "
            "debt-to-income ratio."
        ),
        "source_text": (
            "Purchase of townhome, conventional 30-year fixed, $385,000 loan. Borrower had "
            "FICO 698 but back-end DTI of 52% due to high student loan and auto loan balances. "
            "No significant reserves; AUS referral required manual underwrite. DTI exceeded "
            "all available manual underwriting overlays. Adverse action issued."
        ),
    },
    {
        "record_id": "HIST-003",
        "category": "FHA",
        "outcome": "APPROVED",
        "outcome_rationale": (
            "FHA purchase approved with elevated DTI of 43% supported by two compensating "
            "factors: 14 months PITI reserves and zero late payments on installment accounts "
            "for 24 months. FICO 635, paid medical collection, no foreclosures."
        ),
        "source_text": (
            "First-time homebuyer, FHA 30-year fixed, $272,000 loan. Borrower FICO 635 after "
            "a paid medical collection; no foreclosures or bankruptcies. DTI 43%, down "
            "payment 3.5%. Compensating factors: 14 months reserves and clean 24-month "
            "installment payment history. Manual underwrite; approved with standard FHA "
            "conditions."
        ),
    },
    {
        "record_id": "HIST-004",
        "category": "FHA",
        "outcome": "DENIED",
        "outcome_rationale": (
            "FICO 572 fell below the FHA minimum of 580 required for 3.5% down payment. "
            "Borrower was advised to rebuild credit for 6–12 months before reapplying; "
            "adverse action issued citing insufficient credit score."
        ),
        "source_text": (
            "FHA purchase application, $198,000 loan. Borrower FICO 572 due to recent "
            "charged-off credit card and 30-day late on auto loan 8 months prior. DTI 38%, "
            "adequate down payment. FICO below FHA minimum of 580 for maximum LTV financing. "
            "Borrower declined to increase down payment to 10% for FICO 500–579 tier. "
            "Adverse action issued."
        ),
    },
    {
        "record_id": "HIST-005",
        "category": "jumbo",
        "outcome": "REFER_TO_SENIOR_UNDERWRITER",
        "outcome_rationale": (
            "Retired borrower qualifying via asset depletion income on jumbo cash-out "
            "refinance. Non-standard income method and business-purpose cash-out above $1M "
            "required senior underwriter review per investor guidelines."
        ),
        "source_text": (
            "Cash-out refinance, jumbo 15-year fixed, $975,000 loan. Retired borrower age 65 "
            "qualifying on asset depletion from $3.8M liquid assets; no employment income. "
            "DTI 35%, FICO 805, LTV 68%. Cash-out purpose: capital contribution to family "
            "partnership. Senior underwriter review required for asset depletion method and "
            "business-purpose cash-out on jumbo product."
        ),
    },
    {
        "record_id": "HIST-006",
        "category": "jumbo",
        "outcome": "APPROVED",
        "outcome_rationale": (
            "Jumbo purchase approved: FICO 811, DTI 28%, LTV 72%, 18 months PITI reserves. "
            "Conventional employment income with 10-year history. Strong profile met all "
            "non-agency investor overlays."
        ),
        "source_text": (
            "Jumbo purchase, 30-year fixed, $1.25M loan. Executive borrower FICO 811, "
            "W-2 income $385,000, employed 10 years. DTI 28%, LTV 72%, 18 months PITI "
            "reserves. No collections or derogatories. Full appraisal at purchase price. "
            "Investor approved; no conditions beyond standard documentation."
        ),
    },
    {
        "record_id": "HIST-007",
        "category": "conventional",
        "outcome": "REFER_TO_SENIOR_UNDERWRITER",
        "outcome_rationale": (
            "Self-employed borrower with 18 months business history — 6 months short of the "
            "24-month minimum for conventional conforming. DTI 39%, FICO 724. Referred for "
            "senior review of self-employment income documentation."
        ),
        "source_text": (
            "Purchase, conventional 30-year fixed, $395,000 loan. Self-employed business "
            "owner 18 months, FICO 724, DTI 39%, LTV 80%. Income documented via tax returns "
            "and CPA letter, but self-employment history below 24-month guideline. AUS "
            "returned refer; senior underwriter review required for income duration exception."
        ),
    },
    {
        "record_id": "HIST-008",
        "category": "FHA",
        "outcome": "APPROVED",
        "outcome_rationale": (
            "FHA purchase approved at 43% DTI with post-medical-collection FICO 641. "
            "Compensating factor: zero late payments on all accounts in 36 months. "
            "Paid collection excluded per FHA medical collection guidelines."
        ),
        "source_text": (
            "FHA purchase, 30-year fixed, $241,000 loan. Borrower FICO 641 following a "
            "paid $3,400 medical collection; 36 months clean payment history since. "
            "DTI 43%, 3.5% down, no foreclosures. Medical collection excluded from DTI "
            "per FHA guidelines. Single compensating factor: zero lates in 36 months. "
            "Manual underwrite approved."
        ),
    },
]
