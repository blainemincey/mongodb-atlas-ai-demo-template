"""
AI output generation — Mortgage Underwriting.

Two implementation options are provided. Option A is active by default and
requires no additional API keys. Switch to Option B for a real LLM call.
"""


def generate_output(
    record: dict,
    knowledge_items: list[dict],
    historical_records: list[dict],
    timestamp: str,
) -> str:
    """
    Generate an underwriting recommendation for a mortgage loan application.
    """

    # =========================================================================
    # OPTION A — Template engine (ACTIVE by default, no API key required)
    # =========================================================================

    record_id = record.get("record_id", "UNKNOWN")
    loan_type = (record.get("loan_type") or "").lower()
    loan_amount = record.get("loan_amount", 0)
    fico_score = record.get("fico_score", 0)
    dti_ratio = record.get("dti_ratio", 0.0)
    ltv_ratio = record.get("ltv_ratio", 0.0)
    property_type = (record.get("property_type") or "").replace("_", " ")

    # Determination logic
    if (
        loan_type == "conventional"
        and fico_score >= 720
        and dti_ratio <= 0.43
        and ltv_ratio <= 0.80
    ):
        determination = "APPROVED"
    elif loan_type == "fha" and fico_score >= 580 and dti_ratio <= 0.43:
        determination = "APPROVED"
    elif dti_ratio > 0.50 or (loan_type == "fha" and fico_score < 580):
        determination = "DENIED"
    else:
        determination = "REFER_TO_SENIOR_UNDERWRITER"

    top_kb = knowledge_items[0] if knowledge_items else {}
    kb_title = top_kb.get("title", "N/A")
    kb_category = top_kb.get("category", "N/A")
    kb_excerpt = (top_kb.get("content_text") or "")[:300]
    kb_long = len(top_kb.get("content_text") or "") > 300

    hist_lines = []
    for h in historical_records[:2]:
        hid = h.get("record_id", "")
        outcome = h.get("outcome", "")
        rationale = (h.get("outcome_rationale") or "")[:160]
        hist_lines.append(f"  - {hid} ({outcome}): {rationale}")
    hist_block = "\n".join(hist_lines) if hist_lines else "  - No comparable loans retrieved."

    if determination == "APPROVED":
        required_action = "Release for commitment issuance. Standard conditions apply."
    elif determination == "DENIED":
        if dti_ratio > 0.50:
            deficiency = f"debt-to-income ratio of {dti_ratio:.0%} exceeds maximum"
        elif loan_type == "fha" and fico_score < 580:
            deficiency = f"FICO score of {fico_score} is below FHA minimum of 580"
        else:
            deficiency = "profile does not meet underwriting criteria"
        required_action = f"Issue adverse action notice citing {deficiency}."
    else:
        required_action = (
            "Route to senior underwriter queue for review of non-standard qualifying "
            "factors. Do not issue commitment until senior review is complete."
        )

    output = f"""\
UNDERWRITING RECOMMENDATION
Record:  {record_id}
Generated: {timestamp}

DETERMINATION: {determination}

LOAN SUMMARY
  Loan type:    {loan_type.upper()}
  Loan amount:  ${loan_amount:,.0f}
  FICO score:   {fico_score}
  DTI ratio:    {dti_ratio:.0%}
  LTV ratio:    {ltv_ratio:.0%}
  Property:     {property_type}

APPLICABLE GUIDELINE
Guideline: {kb_title}
Category:  {kb_category}
Excerpt:   {kb_excerpt}{"..." if kb_long else ""}

COMPARABLE LOANS
{hist_block}

REQUIRED ACTION
{required_action}

---
DRAFT — Requires human underwriter review before issuance."""

    return output

    # =========================================================================
    # OPTION B — LLM call via Anthropic SDK (commented out)
    #
    # To use: uncomment this block, comment out Option A above, and add
    # ANTHROPIC_API_KEY to your .env file and config.py Settings class.
    # =========================================================================

    # import anthropic
    #
    # kb_context = "\n\n".join(
    #     f"[{item.get('kb_id', '')}] {item.get('title', '')}\n{item.get('content_text', '')}"
    #     for item in knowledge_items
    # )
    # hist_context = "\n\n".join(
    #     f"[{h.get('record_id', '')}] Outcome: {h.get('outcome', '')}\n"
    #     f"Rationale: {h.get('outcome_rationale', '')}\n{h.get('source_text', '')}"
    #     for h in historical_records
    # )
    # record_text = record.get("record_text", "")
    #
    # prompt = f"""\
    # You are a mortgage underwriting assistant. Based on the loan application
    # below and the retrieved lending guidelines and comparable past loans,
    # produce a structured underwriting recommendation.
    #
    # LOAN APPLICATION:
    # {record_text}
    #
    # LENDING GUIDELINES:
    # {kb_context}
    #
    # COMPARABLE PAST LOANS:
    # {hist_context}
    #
    # Generated at: {timestamp}
    #
    # Provide: DETERMINATION (APPROVED/DENIED/REFER_TO_SENIOR_UNDERWRITER),
    # the most applicable guideline, comparable cases, and required action.
    # """
    #
    # client = anthropic.Anthropic()
    # message = client.messages.create(
    #     model="claude-sonnet-4-6",
    #     max_tokens=1024,
    #     messages=[{"role": "user", "content": prompt}],
    # )
    # return message.content[0].text
