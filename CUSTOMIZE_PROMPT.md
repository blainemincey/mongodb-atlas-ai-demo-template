# Atlas AI Demo — Customization Guide

> **How to use:** In Claude Code, type `@CUSTOMIZE_PROMPT.md` and send.
> Claude will interview you, generate all sample data, and fill in the
> template. You don't need to read or edit this file — just reference it.

---

<!--
=============================================================================
INSTRUCTIONS FOR CLAUDE — follow this protocol when this file is loaded.
Do not summarize or explain this file to the user. Start the interview
immediately with Step 1.
=============================================================================

STEP 1 — Ask all domain questions in a single message
───────────────────────────────────────────────────────────────────────────
Post the following to the user exactly as written:

---
I'll customize this Atlas AI demo template for your domain. I need a few
inputs, then I'll generate the sample data and fill in everything for you.

Please answer these — any format is fine:

1. **Domain & purpose:** What kind of records are being processed, and what
   decision or output does the system produce? (1–2 sentences, e.g. "Mortgage
   underwriting — loan applications reviewed against lending guidelines to
   produce an approval recommendation.")

2. **Scenario A:** A name and one-sentence hook. What makes this case
   interesting for a demo? (e.g. "Clean approval — strong borrower profile,
   should surface matching guidelines and comparable approvals cleanly.")

3. **Scenario B:** Same format.

4. **Scenario C:** Same format. Ideally pick a case that contrasts with A and
   B — a borderline case, a denial, or a non-standard qualification method.

5. **Record fields:** What structured fields belong on a record beyond the
   main text blob? List field names and example values.
   (e.g. `loan_type: "conventional"`, `amount: 425000`, `risk_tier: "low"`)
   If you're not sure, just describe the domain and I'll infer reasonable ones.

6. **Outcome values:** What should the AI output's determination say?
   (e.g. `APPROVE / DENY / REFER_TO_REVIEWER` or `PASS / FAIL / NEEDS_REVIEW`)
---

STEP 2 — Generate all content from the answers
───────────────────────────────────────────────────────────────────────────
Once the user answers Step 1, generate the following without asking more
questions. Infer sensible values for anything not explicitly specified.

A. demo_records.py — three records, one per scenario:
   - All structured fields from answer 5, with values appropriate to each scenario
   - A `record_text` blob (4–7 sentences, realistic and rich — this gets
     embedded by Voyage AI, so pack it with domain terminology that will
     semantically match the knowledge base items you generate below)
   - `processing_status: "PENDING"` on all three

B. knowledge_base.py — 6–8 items:
   - Fields: kb_id, title, category, subcategory (optional), content_text
   - Derive 2–3 categories from the scenario types (e.g. "conventional",
     "FHA", "jumbo" for mortgage; "hardware", "software", "network" for IT)
   - content_text: 3–5 sentences of realistic reference content — rules,
     criteria, guidelines, or product specs for the domain
   - Ensure at least 2 KB items are semantically close to each scenario's
     record_text so vector search surfaces them naturally

C. historical_records.py — 6–8 items:
   - Fields: record_id, category, outcome (use values from answer 6),
     outcome_rationale (1–2 sentences), source_text (3–5 sentences)
   - source_text should resemble the record_text style — same domain, similar
     terminology — so vector search matches the right analogues to each scenario
   - Include at least one outcome=APPROVED and one outcome=DENIED per scenario

D. llm.py Option A output template:
   - Rewrite the output f-string block in generate_output() to match the domain
   - Use the determination values from answer 6
   - Include determination logic that inspects record fields (e.g. if
     record.get("risk_tier") == "low": determination = "APPROVE")
   - Sections should follow a natural structure for the domain: header,
     determination, analysis citing top KB item, comparable cases, next action

E. ScenarioSelector.tsx — title, subtitle, detail for each of A / B / C

F. App.tsx SCENARIO_CONFIG — label and description for each scenario

G. SearchStep.tsx — update the category filter <select> options to match the
   categories used in the knowledge base (replace the single "General" option)

H. setup.py smoke test query — a domain-specific search string (line ~274)
   that should retrieve the most relevant knowledge base items

STEP 3 — Show a preview and ask for approval
───────────────────────────────────────────────────────────────────────────
Before writing any files, show a compact summary in this format:

DOMAIN: [one-line description]

RECORDS
  Scenario A: [title] — [record_id], [2–3 key field: value pairs]
  Scenario B: [title] — [record_id], [2–3 key field: value pairs]
  Scenario C: [title] — [record_id], [2–3 key field: value pairs]

KNOWLEDGE BASE: [N] items
  Categories: [list]
  Sample: "[KB-001 title]", "[KB-002 title]", ...

HISTORICAL RECORDS: [N] items — [X] approved, [Y] denied
  Sample: [HIST-001: outcome], [HIST-002: outcome], ...

OUTPUT DETERMINATION VALUES: [list from answer 6]

Then ask: "Does this look right, or anything you'd like to adjust before I
write the files?"

Incorporate any feedback, then proceed to Step 4.

STEP 4 — Handle credentials
───────────────────────────────────────────────────────────────────────────
Ask the user:

"Two more things before I write the files:

1. **MongoDB Atlas connection string** — do you have it now, or will you add
   it to .env later? (Get one from: Atlas UI → Connect → Drivers)

2. **Voyage AI API key** — do you have it now, or will you add it later?
   (Get one from: https://dash.voyageai.com/api-keys)

Paste them here if you have them — they'll go into .env which is already in
.gitignore and will never be committed. If you'd rather add them later, I'll
create a .env with placeholder values."

Handle the response:
- If both provided: write `.env` with real MONGODB_URI and VOYAGE_API_KEY
  values, DB_NAME=demo_db, DEMO_NAME="[domain name] Demo", other fields from
  .env.example defaults
- If one or both deferred: copy .env.example to .env with placeholder values
  intact; note clearly which values still need to be filled in before running
  setup.py
- Either way: confirm .env is in .gitignore (it already is — just verify)

STEP 5 — Write all files and verify
───────────────────────────────────────────────────────────────────────────
Write all files from Step 2, plus .env from Step 4.

Then run both verification commands:
  cd backend && python -c "
  from data.demo_records import DEMO_RECORDS
  from data.knowledge_base import KNOWLEDGE_BASE
  from data.historical_records import HISTORICAL_RECORDS
  print('imports ok')
  print(f'{len(DEMO_RECORDS)} records, {len(KNOWLEDGE_BASE)} KB items, {len(HISTORICAL_RECORDS)} historical records')
  "

  cd frontend && npm run build

Report results. Then close with:

  Next steps:
  1. [If .env has placeholders] Fill in MONGODB_URI and VOYAGE_API_KEY in .env
  2. python scripts/setup.py    — seeds data, creates Atlas Vector Search indexes
  3. ./start.sh                 — starts backend + frontend
  4. Open http://localhost:5173

=============================================================================
END OF CLAUDE INSTRUCTIONS
=============================================================================
-->

---

## Worked Example (reference)

If you want to see what a completed domain brief looks like before running
the interview, the mortgage underwriting example below shows the level of
detail that produces good demo content. You can also use it as a fast-path:

> `@CUSTOMIZE_PROMPT.md` — skip the interview and use the mortgage underwriting
> example at the bottom of this file to fill in the template instead.

```
Domain: Mortgage underwriting — loan applications reviewed against lending
guidelines and comparable past loans to produce a draft underwriting
recommendation (APPROVE / DENY / REFER_TO_SENIOR_UNDERWRITER).

Record fields: loan_type, loan_amount, fico_score, dti_ratio, ltv_ratio,
property_type

Scenario A — Strong Conventional
  UI title: Conventional Purchase — Strong Profile
  UI subtitle: Conventional · 30yr Fixed · $425K
  UI detail: 742 FICO, 28% DTI, 20% down. Straightforward conforming loan —
    surfaces approval-supporting guidelines and comparable approvals.
  record_text: Applicant is a 38-year-old software engineer employed 6 years
    at the same firm, base salary $142,000, year-end bonus averaging $18,000.
    W-2 income verified; no employment gaps. FICO 742, two minor derogatories
    both >48 months old, no collections. Back-end DTI 28%. Purchase price
    $531,250, 20% down from seasoned savings, 60-day statements provided.
    Single-family primary residence, appraised value matches purchase price.
    Loan amount $425,000 within conforming limit.

Scenario B — Borderline FHA
  UI title: FHA Purchase — Elevated DTI
  UI subtitle: FHA · 30yr Fixed · $287K
  UI detail: 638 FICO, 43% DTI, 3.5% down. Borderline profile with
    compensating factors — demonstrates how the system surfaces FHA
    guidelines and finds analogous approved cases.
  record_text: Applicant is a 31-year-old registered nurse, employed 2.5
    years at a regional hospital, base $68,000 plus $9,200 documented
    overtime. FICO 638 following a $2,100 medical collection from 2021 now
    paid; no foreclosures or bankruptcies. DTI 43%. Down payment 3.5% from
    savings. Compensating factors: 14 months PITI reserves, zero late
    payments on installment accounts in 24 months.

Scenario C — Jumbo Asset Depletion
  UI title: Jumbo Refinance — Asset Depletion
  UI subtitle: Jumbo · 15yr Fixed · $1.1M
  UI detail: Retired borrower qualifying on asset depletion. Complex
    non-standard income requiring specialist review.
  record_text: Retired applicant age 67, FICO 798, qualifying via asset
    depletion on $4.2M verified liquid assets; monthly income $9,722
    calculated on $2.1M eligible assets amortized over 216 months. DTI
    38%. Cash-out refinance $1.1M on property appraised at $1.505M (LTV
    73%). Cash-out purpose: business investment in family LLC. Loan exceeds
    conforming limit; requires jumbo investor approval.

Knowledge base categories: conventional, FHA, jumbo
Historical record outcomes: APPROVED, DENIED

Output sections:
  UNDERWRITING RECOMMENDATION — [record_id] — [timestamp]
  DETERMINATION: APPROVE / DENY / REFER_TO_SENIOR_UNDERWRITER
  ANALYSIS: 3–4 sentences citing top KB item by title, referencing FICO/DTI/LTV
  COMPARABLE LOANS: bullet list of top 2 HIST IDs with outcome and one-sentence analogy
  REQUIRED ACTION: conditional on determination
    APPROVE → "Release for commitment issuance."
    DENY → "Issue adverse action notice citing [deficiency]."
    REFER → "Route to senior underwriter queue."

Determination logic:
  APPROVE if (loan_type == "conventional" and fico >= 720 and dti <= 0.43 and ltv <= 0.80)
         or (loan_type == "FHA" and fico >= 580 and dti <= 0.43)
  DENY if dti > 0.50 or (loan_type == "FHA" and fico < 580)
  REFER_TO_SENIOR_UNDERWRITER otherwise

Smoke test query: "conventional mortgage conforming loan DTI FICO income
  verification employment history"
```
