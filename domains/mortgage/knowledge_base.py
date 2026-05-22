"""
Mortgage Underwriting — knowledge base.

Lending guidelines and underwriting criteria across conventional, FHA, and
jumbo categories. Each item's content_text is embedded by Voyage AI so that
relevant guidelines surface when an incoming loan application is searched.
"""

KNOWLEDGE_BASE = [
    {
        "kb_id": "KB-001",
        "title": "Conventional Conforming Loan — Income and Employment Requirements",
        "category": "conventional",
        "subcategory": "income",
        "content_text": (
            "Conventional conforming loans require a minimum of 24 months continuous employment "
            "history; job changes within the same field are acceptable with no gap. W-2 income "
            "is documented with the two most recent pay stubs and federal tax returns. Bonus and "
            "overtime income may be used if received for at least 24 months and likely to "
            "continue, verified by employer letter. Self-employment income requires 24 months "
            "of tax returns and a CPA letter confirming business stability. Income used for "
            "qualifying must be stable, predictable, and likely to continue for at least three "
            "years."
        ),
    },
    {
        "kb_id": "KB-002",
        "title": "Conventional Loan — FICO and DTI Eligibility Thresholds",
        "category": "conventional",
        "subcategory": "credit",
        "content_text": (
            "Standard conventional conforming loans require a minimum FICO score of 620, with "
            "best pricing tiers at 740 and above. Maximum back-end DTI is 45% with DU/LP "
            "approval, or 43% for manually underwritten loans. LTV up to 97% with PMI for "
            "primary residence purchase; 80% LTV eliminates PMI requirement. Minor derogatories "
            "older than 36 months with no pattern of delinquency are generally acceptable. "
            "No outstanding collections or judgments are permitted; charge-offs must be paid "
            "or addressed in writing."
        ),
    },
    {
        "kb_id": "KB-003",
        "title": "FHA Loan — Minimum Credit Score and DTI Limits",
        "category": "FHA",
        "subcategory": "credit",
        "content_text": (
            "FHA loans require a minimum FICO of 580 for maximum financing (3.5% down payment). "
            "Borrowers with FICO 500–579 are eligible with 10% down payment; below 500 is "
            "ineligible. Maximum back-end DTI is 43% for manually underwritten loans; "
            "automated approval (TOTAL Scorecard) may approve up to 57% DTI with strong "
            "compensating factors. Medical collections under $2,000 are excluded from DTI "
            "calculation if documented as paid or payment plan established. FHA requires "
            "upfront MIP of 1.75% and annual MIP for the loan life if LTV exceeds 90% at "
            "origination."
        ),
    },
    {
        "kb_id": "KB-004",
        "title": "FHA Loan — Compensating Factors for Elevated DTI",
        "category": "FHA",
        "subcategory": "compensating-factors",
        "content_text": (
            "When FHA back-end DTI exceeds 43%, at least one significant compensating factor "
            "is required for manual underwriting approval. Acceptable compensating factors "
            "include: verified cash reserves of at least 3 months PITI after closing; no "
            "late payments on any installment accounts in the previous 24 months; residual "
            "income exceeding the VA residual income table by 20%; or minimal increase in "
            "housing expense (new payment does not exceed prior housing cost by more than "
            "$100 or 5%). Two compensating factors are required when DTI exceeds 50%."
        ),
    },
    {
        "kb_id": "KB-005",
        "title": "Jumbo Loan — Non-Agency Underwriting Standards",
        "category": "jumbo",
        "subcategory": "eligibility",
        "content_text": (
            "Jumbo loans (above the conforming loan limit) are non-agency products and require "
            "investor-specific approval. Standard jumbo guidelines require a minimum FICO of "
            "700, maximum DTI of 43%, and LTV no greater than 80% for loan amounts above "
            "$1 million. Loan purpose restrictions vary by investor: cash-out refinances above "
            "$750,000 typically require additional reserves (12 months PITI). All jumbo loans "
            "require full appraisal with no waiver. A second appraisal may be required for "
            "loan amounts above $1.5 million."
        ),
    },
    {
        "kb_id": "KB-006",
        "title": "Asset Depletion Income — Calculation and Eligibility",
        "category": "jumbo",
        "subcategory": "income",
        "content_text": (
            "Asset depletion is an alternative income qualification method for borrowers with "
            "substantial liquid assets and limited employment income, typically retirees. "
            "Eligible assets include checking, savings, money market, CDs, and 70% of vested "
            "retirement accounts. Calculation: divide eligible assets by the remaining loan "
            "term in months; the result is the monthly qualifying income. Assets used for down "
            "payment and closing costs must be excluded before calculation. Assets must be "
            "verified with 60-day statements. This method is available on jumbo non-agency "
            "products only; conventional conforming and FHA do not permit asset depletion "
            "qualifying."
        ),
    },
    {
        "kb_id": "KB-007",
        "title": "LTV Requirements by Loan Type — Purchase and Refinance",
        "category": "conventional",
        "subcategory": "ltv",
        "content_text": (
            "Maximum LTV varies by loan type, occupancy, and purpose. Conventional purchase: "
            "up to 97% LTV for primary residence with PMI; 85% for second home; 75% for "
            "investment property. FHA purchase: maximum 96.5% LTV with 580+ FICO. "
            "Conventional rate-term refinance: up to 97% LTV. Cash-out refinance: "
            "conventional maximum 80% LTV; FHA maximum 80% LTV. Jumbo purchase: typically "
            "80% LTV maximum. Jumbo cash-out refinance: maximum 75–80% LTV depending on "
            "investor. LTV is calculated on the lesser of appraised value or purchase price."
        ),
    },
    {
        "kb_id": "KB-008",
        "title": "Cash-Out Refinance — Purpose Documentation and LTV Limits",
        "category": "jumbo",
        "subcategory": "refinance",
        "content_text": (
            "Cash-out refinance transactions require documentation of the use of proceeds. "
            "Business purposes (investment in a closely held entity, LLC, or operating "
            "business) are permitted but require a letter of explanation and may trigger "
            "additional investor scrutiny on jumbo products. Maximum cash-out on jumbo "
            "refinances is typically limited to $500,000 per transaction for LTV above 70%; "
            "higher cash-out amounts require LTV of 65% or below. The business investment "
            "purpose does not count as an employer gift or non-arm's-length transaction but "
            "must be disclosed. Senior underwriter review is required when cash-out purpose "
            "is a business investment and loan amount exceeds $1 million."
        ),
    },
]
