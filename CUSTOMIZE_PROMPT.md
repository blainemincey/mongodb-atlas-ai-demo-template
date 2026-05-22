# Customization Prompt

This file explains how to adapt the template to a new domain in a single
Claude Code session. Fill out the Domain Brief below, then paste it into
Claude Code with the instruction:

> "Using the domain brief in CUSTOMIZE_PROMPT.md, fill in all the TODO
> placeholders across this codebase."

Claude will update `demo_records.py`, `knowledge_base.py`,
`historical_records.py`, `llm.py`, `ScenarioSelector.tsx`, `App.tsx`, and
`setup.py` in one pass.

---

## What to fill in

You need five things. Nothing else in the codebase requires domain knowledge.

1. **Three demo records** — the records the audience will watch get processed
   live. Each needs a rich text blob (`record_text`) and any structured fields
   that make your domain recognizable (amounts, IDs, categories, etc.).

2. **Knowledge base** — 5–15 reference items that the vector search should
   retrieve. These are your rules, policies, guidelines, documentation, or
   product specs. The richer the text, the better the search results.

3. **Historical records** — 5–15 past examples with outcomes. These provide
   the "comparable cases" the AI output step references. Include at least one
   APPROVED and one DENIED for each scenario so the demo shows contrast.

4. **Scenario UI labels** — short titles and one-line descriptions shown on the
   scenario picker cards.

5. **Output section shape** — what the AI output should say. Describe the
   sections (header, determination, supporting rationale, action required, etc.)
   and how to pull values from the record and retrieved context.

---

## Domain Brief Template

Copy this section, fill it in, and paste it as your prompt.

```
## Domain Brief

**Domain:** [One sentence — what kind of records are being processed, and
what decision or output is being produced? e.g. "Mortgage underwriting —
loan applications are reviewed against lending guidelines and comparable
past loans to produce a draft underwriting recommendation."]

**Record text field:** [What is record_text in this domain? What goes in it?
e.g. "The loan officer's narrative summary of the applicant, including income
sources, employment history, and any risk flags noted during intake."]

**Filter fields:**
- knowledge_base: category = [e.g. loan_type], subcategory = [e.g. product]
- historical_records: category = [e.g. loan_type], outcome = [e.g. APPROVED / DENIED]

---

### Scenario A — [name]

**UI title:** [e.g. "Straightforward Approval"]
**UI subtitle:** [e.g. "Conventional · 30yr Fixed"]
**UI detail:** [one-sentence hook e.g. "Strong borrower profile, DTI 28%, 740 FICO. Standard conforming loan — should surface approval-supporting guidelines and comparable approvals."]

**record_id:** REC-001-A
**Extra structured fields:**
[List any domain-specific fields you want in the document, e.g.:]
  loan_type: "conventional"
  loan_amount: 425000
  fico_score: 742
  dti_ratio: 0.28
  ltv_ratio: 0.80
  property_type: "single_family"

**record_text:**
[Write the full unstructured text blob for this record. Make it realistic and
rich — this is what Voyage AI will embed, and it needs to semantically match
your knowledge base items. 3–8 sentences.]

---

### Scenario B — [name]

**UI title:**
**UI subtitle:**
**UI detail:**

**record_id:** REC-001-B
**Extra structured fields:**
[...]

**record_text:**
[...]

---

### Scenario C — [name]

**UI title:**
**UI subtitle:**
**UI detail:**

**record_id:** REC-001-C
**Extra structured fields:**
[...]

**record_text:**
[...]

---

### Knowledge Base

[Provide 5–10 entries. Each entry needs: kb_id, title, category, subcategory
(optional), and content_text. The content_text is what gets embedded — make it
dense with domain terminology that will match your record_text values above.]

KB-001
title: [...]
category: [...]
content_text: [...]

KB-002
[...]

[continue...]

---

### Historical Records

[Provide 5–10 entries. Each needs: record_id, category, outcome (APPROVED or
DENIED), outcome_rationale (1–2 sentences), and source_text (the text that
gets embedded — should be similar to your record_text values so the right
historical records surface for each scenario).]

HIST-001
category: [...]
outcome: APPROVED
outcome_rationale: [...]
source_text: [...]

HIST-002
category: [...]
outcome: DENIED
outcome_rationale: [...]
source_text: [...]

[continue...]

---

### AI Output Format

[Describe what the output text should look like. What sections? What
determination values are possible (e.g. APPROVE / DENY / REQUEST_MORE_INFO)?
How should the retrieved knowledge base items and historical records be
referenced? Example:]

Sections:
1. Header: record_id, generated timestamp, DETERMINATION value
2. DETERMINATION: one of APPROVE / DENY / REFER_TO_UNDERWRITER
3. BASIS: 2–3 sentences citing the top knowledge base item by title
4. COMPARABLE CASES: bullet list of historical record IDs with outcome
5. ACTION REQUIRED: what happens next (conditional on determination)

Determination logic:
- APPROVE if [conditions from record fields]
- DENY if [conditions]
- REFER_TO_UNDERWRITER otherwise

---

### Setup smoke test query

[One search string that should retrieve your most relevant knowledge base
items. Used in scripts/setup.py Step 8 to verify indexes are working.]

"[e.g. conventional mortgage conforming loan DTI ratio income verification]"
```

---

## Worked Example — Mortgage Underwriting

This is a complete, filled-in brief. Use it as a reference for the level of
detail that produces good demo content.

```
## Domain Brief

**Domain:** Mortgage underwriting — loan applications are reviewed against
lending guidelines and comparable past loans to produce a draft underwriting
recommendation (Approve, Deny, or Refer to Senior Underwriter).

**Record text field:** The loan officer's narrative intake summary capturing
the applicant's income sources, employment history, credit context, and any
risk flags or compensating factors noted during initial review.

**Filter fields:**
- knowledge_base: category = loan_type (e.g. "conventional", "FHA", "jumbo")
- historical_records: category = loan_type, outcome = APPROVED / DENIED

---

### Scenario A — Strong Conventional

**UI title:** Conventional Purchase — Strong Profile
**UI subtitle:** Conventional · 30yr Fixed · $425K
**UI detail:** 742 FICO, 28% DTI, 20% down. Straightforward conforming loan — should surface approval-supporting guidelines and comparable approvals with clean documentation.

**record_id:** REC-001-A
**Extra structured fields:**
  loan_type: "conventional"
  loan_amount: 425000
  fico_score: 742
  dti_ratio: 0.28
  ltv_ratio: 0.80
  property_type: "single_family"
  processing_status: "PENDING"

**record_text:**
Applicant is a 38-year-old software engineer employed for 6 years at the same
technology company with base salary of $142,000 and documented year-end bonus
averaging $18,000 over the past two years. W-2 income verified; no gaps in
employment. FICO 742 with two minor derogatory marks both greater than 48
months old and no collections or judgments. Total monthly obligations $1,640
against gross income $13,333, yielding front-end DTI of 22% and back-end DTI
of 28%. Purchase price $531,250 with 20% down payment of $106,250 sourced
from savings with 60 days of bank statements provided. Property is a
single-family residence in a stable market with appraised value matching
purchase price. No gift funds. Loan amount $425,000 within conforming limit.

---

### Scenario B — Borderline FHA

**UI title:** FHA Purchase — Elevated DTI
**UI subtitle:** FHA · 30yr Fixed · $287K
**UI detail:** 638 FICO, 43% DTI, 3.5% down. Borderline profile with compensating factors — demonstrates how the system surfaces FHA guidelines and finds analogous borderline approvals.

**record_id:** REC-001-B
**Extra structured fields:**
  loan_type: "FHA"
  loan_amount: 287000
  fico_score: 638
  dti_ratio: 0.43
  ltv_ratio: 0.965
  property_type: "single_family"
  processing_status: "PENDING"

**record_text:**
Applicant is a 31-year-old registered nurse employed 2.5 years at a regional
hospital with hourly base pay equivalent to $68,000 annually plus documented
overtime averaging $9,200 per year over 24 months. FICO 638 following a
medical collection of $2,100 from 2021 that has since been paid and disputed;
no foreclosures or bankruptcies. Total monthly debt obligations of $2,260
against gross income of $6,433 yields back-end DTI of 43%. Down payment of
$10,500 (3.5%) sourced from savings; no gift funds. Compensating factors
include 14 months of verified PITI reserves, stable two-year employment in
essential healthcare, and zero late payments on any installment account in the
past 24 months. Property is a single-family home with appraised value
consistent with purchase price.

---

### Scenario C — High-LTV Jumbo

**UI title:** Jumbo Refinance — Asset Depletion
**UI subtitle:** Jumbo · 15yr Fixed · $1.1M
**UI detail:** Retired borrower, income via asset depletion. Complex qualification requiring specialist review — shows how the system flags non-standard cases and pulls relevant jumbo guidelines.

**record_id:** REC-001-C
**Extra structured fields:**
  loan_type: "jumbo"
  loan_amount: 1100000
  fico_score: 798
  dti_ratio: 0.38
  ltv_ratio: 0.73
  property_type: "single_family"
  processing_status: "PENDING"

**record_text:**
Applicant is a 67-year-old retired executive qualifying on asset depletion
methodology. Verified liquid assets of $4,200,000 across brokerage and
retirement accounts; monthly asset depletion income calculated at $9,722 per
$2.1M eligible assets amortized over 216 months per jumbo guidelines. FICO
798 with no derogatory history. Existing mortgage on subject property carries
a balance of $380,000 at 6.875%; refinance to $1,100,000 cash-out to fund
business investment in family LLC. Property appraised at $1,505,000. LTV
73%. Total monthly obligations $4,800 (proposed PITI $6,200 plus existing
obligations $1,100 on refinance payoff), DTI 38% using asset depletion income.
Loan amount $1,100,000 exceeds conforming limit; requires jumbo investor
approval. Business purpose cash-out requires additional documentation review.

---

### Knowledge Base

KB-001
title: Conventional Conforming — DTI and Reserve Requirements
category: conventional
content_text: Conforming conventional loans require a maximum back-end
debt-to-income ratio of 45% for borrowers with FICO scores of 720 or above,
and 43% for scores between 680 and 719. Reserves of two months PITI are
required for primary residences; six months for investment properties. Gift
funds are permitted for the full down payment on primary residence
conventional loans when sourced from eligible donors with a signed gift letter
and transfer documentation. Derogatory credit items must be a minimum of 24
months seasoned for manual underwriting approval; automated approvals may
allow shorter seasoning. Loan amounts must not exceed the current conforming
loan limit as published by FHFA for the subject property county.

KB-002
title: FHA Financing — DTI Thresholds and Compensating Factors
category: FHA
content_text: FHA guidelines permit a maximum back-end DTI of 43% without
compensating factors for borrowers with FICO scores of 580 or above. Back-end
DTI up to 50% may be approved with two or more documented compensating factors,
which include: verified cash reserves equal to or exceeding three months PITI,
minimal increase in housing payment (less than 5% above current housing
expense), no discretionary debt, and residual income meeting VA residual
income thresholds for the borrower's region. Minimum FICO of 580 for 3.5%
down payment; scores below 580 require 10% down. Collections do not require
payoff unless the total balance exceeds $2,000 for non-medical collections.

KB-003
title: Jumbo Loan — Asset Depletion Income Methodology
category: jumbo
content_text: For borrowers without traditional employment income, asset
depletion methodology may be used to establish qualifying income. Eligible
assets include verified liquid accounts (checking, savings, brokerage) and
70% of vested retirement accounts for borrowers age 59.5 or older. The
qualifying income is calculated by dividing eligible assets by the loan term
in months (e.g., 180 or 360). Assets must be fully documented with 60 days
of statements showing account ownership and sufficient balance. Business
assets or assets encumbered by liens are not eligible. Cash-out proceeds
from the subject transaction may not be included in asset calculations.

KB-004
title: Employment and Income — Two-Year History Requirements
category: conventional
content_text: Borrowers must demonstrate a two-year history of employment
or self-employment. Gaps in employment of more than 30 days require a written
explanation. Overtime and bonus income may be used if received for a minimum
of two years and likely to continue, as evidenced by a verification of
employment from the current employer. Part-time income requires a two-year
history at the same employer. Recent graduates may substitute their field of
study for employment history if beginning a career in their area of education.
Rental income from investment properties requires two years of tax returns
with Schedule E and current lease agreements.

KB-005
title: Jumbo Loan — Credit and Reserve Requirements
category: jumbo
content_text: Jumbo loans exceeding the conforming loan limit require a
minimum FICO score of 720 for loan-to-value ratios above 70%, and 700 for
LTVs at or below 70%. Maximum LTV of 80% applies to primary residence
purchase transactions; 75% for cash-out refinances. Minimum reserves of
12 months PITI are required for all jumbo transactions. Business-purpose
cash-out or loans with non-standard income documentation require senior
underwriter sign-off and may require investor pre-approval before
commitment issuance. Maximum DTI of 43% applies without exception.

---

### Historical Records

HIST-001
category: conventional
outcome: APPROVED
outcome_rationale: Strong compensating factors — 780 FICO, 24% DTI, 12 months
reserves — outweighed a minor employment gap. Conforming amount, standard
property type. Clean automated approval.
source_text: Borrower is a 35-year-old marketing manager, employed 3 years at
current firm, FICO 780, base salary $118,000. 3-month employment gap in 2022
explained by voluntary career transition with documentation. Back-end DTI 24%.
Down payment 25% from seasoned savings. Single-family primary residence,
appraised value matched purchase price. Reserves 12 months. Conventional
conforming. No derogatory credit in 7 years.

HIST-002
category: conventional
outcome: DENIED
outcome_rationale: DTI exceeded guideline maximum with no compensating
factors. Borrower was advised to pay down revolving debt and reapply.
source_text: Borrower is a 29-year-old retail manager, FICO 672, DTI 52%.
Multiple open credit card accounts with high utilization (78% aggregate).
Conventional loan request $340,000 at 95% LTV. No reserves beyond minimum
down payment. Employment 18 months at current employer. DTI exceeded 45%
maximum with no documented compensating factors present. Application denied.

HIST-003
category: FHA
outcome: APPROVED
outcome_rationale: DTI of 47% approved under FHA compensating factor
provision. Two qualifying compensating factors documented: 4 months reserves
and less than 5% housing payment increase.
source_text: Borrower is a 28-year-old teacher, FICO 614, DTI 47%. Stable
public-sector employment 3 years. Medical collection $1,800 from 2020, paid.
FHA loan $198,000 at 96.5% LTV. Compensating factors: 4 months PITI reserves
verified; housing payment increase from current rent of $1,340 to proposed
PITI $1,390 (3.7% increase). FHA manual underwrite approved.

HIST-004
category: jumbo
outcome: APPROVED
outcome_rationale: Asset depletion methodology well-documented with 60-day
statements. FICO 810, reserves 36 months. Senior underwriter approved after
confirming eligible asset calculation and business-purpose disclosure.
source_text: Retired applicant age 69, FICO 810, qualifying via asset
depletion on $3.8M verified liquid assets. Monthly income $10,555 on 360-month
amortization. DTI 36%. Jumbo loan $875,000, LTV 68%. 36 months PITI reserves.
Cash-out for documented investment purpose with LLC operating agreement
provided. Senior underwriter reviewed asset depletion worksheet and approved.

HIST-005
category: jumbo
outcome: DENIED
outcome_rationale: LTV exceeded 75% maximum for cash-out jumbo refinance.
Borrower declined reduced loan amount option.
source_text: Applicant age 58, FICO 762, requesting jumbo cash-out refinance
$1.4M on property valued $1.7M (LTV 82%). DTI 41% with W-2 income. Cash-out
purpose: home renovation. Jumbo guideline maximum LTV for cash-out refinance
is 75%. Property would need to appraise at $1.87M or loan amount reduce to
$1.275M to meet LTV threshold. Borrower declined reduced loan amount. Denied.

---

### AI Output Format

Sections:
1. Header line: "UNDERWRITING RECOMMENDATION — [record_id] — Generated: [timestamp]"
2. DETERMINATION: one of APPROVE / DENY / REFER_TO_SENIOR_UNDERWRITER
3. ANALYSIS: 3–4 sentences using the top knowledge base item as the governing
   guideline. Reference the specific DTI, FICO, LTV, and loan_type from the record.
   Cite the knowledge base item by title.
4. COMPARABLE LOANS: bullet list of top 2 historical record IDs, their outcome,
   and a one-sentence analogy to the current application.
5. REQUIRED ACTION: what happens next.
   - APPROVE: "Release for commitment issuance pending title and final conditions."
   - DENY: "Issue adverse action notice. Cite [specific deficiency]."
   - REFER: "Route to senior underwriter queue. Flag [specific issue] for review."

Determination logic:
- APPROVE if FICO >= 720 AND DTI <= 0.43 AND LTV <= 0.80 for conventional;
  or FICO >= 580 AND DTI <= 0.43 for FHA (or DTI <= 0.50 with 2+ compensating
  factors noted in record_text)
- DENY if DTI > 0.50 with no compensating factors OR LTV exceeds guideline max
- REFER_TO_SENIOR_UNDERWRITER otherwise (borderline, non-standard income,
  jumbo, or compensating factors present but manual review required)

---

### Setup smoke test query

"conventional mortgage conforming loan DTI ratio FICO credit score income
verification employment history"
```

---

## How to invoke

Once you've filled out your domain brief (or decided to use the example above),
open this repo in Claude Code and run:

```
@CUSTOMIZE_PROMPT.md

Using the domain brief in the "Worked Example" section above (or the filled-in
template section, whichever applies), fill in all the TODO placeholders across
this codebase. Specifically:

1. backend/data/demo_records.py — replace all three stub records
2. backend/data/knowledge_base.py — replace all five stub KB items
3. backend/data/historical_records.py — replace all five stub historical records
4. frontend/src/components/ScenarioSelector.tsx — update title/subtitle/detail
5. frontend/src/App.tsx — update SCENARIO_CONFIG labels and descriptions
6. backend/services/llm.py — rewrite the Option A output template section
7. scripts/setup.py — update the smoke test query string

Keep all field names, router paths, and architecture exactly as-is. Only
replace domain content (text, titles, labels, output logic). When done, run:
  cd backend && python -c "from data.demo_records import DEMO_RECORDS; print('ok')"
  cd frontend && npm run build
```
