"""
AI output generation — Insurance Claims P&C.

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
    Generate a claims handling recommendation for an insurance claim.
    """

    # =========================================================================
    # OPTION A — Template engine (ACTIVE by default, no API key required)
    # =========================================================================

    record_id = record.get("record_id", "UNKNOWN")
    claim_type = (record.get("claim_type") or "unknown").lower()
    policy_number = record.get("policy_number", "N/A")
    claim_amount = record.get("claim_amount", 0)
    deductible = record.get("deductible", 0)

    top_kb = knowledge_items[0] if knowledge_items else {}
    top_hist = historical_records[0] if historical_records else {}
    hist_outcome = top_hist.get("outcome", "")

    # Determination logic
    if claim_type == "auto_collision":
        if hist_outcome == "NEEDS_INVESTIGATION":
            determination = "NEEDS_INVESTIGATION — DISPUTED LIABILITY"
        else:
            determination = "APPROVED"
    elif claim_type == "property_water":
        if hist_outcome == "DENIED":
            determination = "DENIED — GRADUAL DAMAGE EXCLUSION"
        elif hist_outcome == "NEEDS_INVESTIGATION":
            determination = "NEEDS_INVESTIGATION — COVERAGE DISPUTE"
        else:
            determination = "APPROVED"
    elif claim_type == "auto_total_loss":
        if hist_outcome == "NEEDS_INVESTIGATION":
            determination = "NEEDS_INVESTIGATION — ACV DISPUTE"
        else:
            determination = "APPROVED"
    else:
        determination = "NEEDS_INVESTIGATION — MANUAL REVIEW REQUIRED"

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
    hist_block = "\n".join(hist_lines) if hist_lines else "  - No comparable claims retrieved."

    if determination == "APPROVED":
        next_action = (
            f"Approve claim. Process payment for "
            f"${claim_amount - deductible:,.0f} (claim amount less deductible)."
        )
    elif "DENIED" in determination:
        next_action = (
            "Issue denial with policy language citation. "
            "Advise claimant of appeal rights."
        )
    else:
        next_action = (
            "Assign to field adjuster for investigation. "
            "Notify claimant of pending review."
        )

    output = f"""\
CLAIMS RECOMMENDATION
Claim: {record_id} | Type: {claim_type.upper()} | Policy: {policy_number}
Claim Amount: ${claim_amount:,.0f} | Deductible: ${deductible:,.0f}
Generated: {timestamp}

DETERMINATION: {determination}

APPLICABLE COVERAGE GUIDELINE
Guideline: {kb_title}
Category:  {kb_category}
Excerpt:   {kb_excerpt}{"..." if kb_long else ""}

COMPARABLE PAST CLAIMS
{hist_block}

RECOMMENDED ACTION
{next_action}

---
DRAFT — Requires adjuster review before action."""

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
    # You are an insurance claims handling system. Based on the claim below and
    # the retrieved coverage guidelines and comparable past claim decisions,
    # produce a structured claims handling recommendation.
    #
    # CLAIM TEXT:
    # {record_text}
    #
    # COVERAGE GUIDELINES:
    # {kb_context}
    #
    # COMPARABLE PAST CLAIMS:
    # {hist_context}
    #
    # Generated at: {timestamp}
    #
    # Provide: DETERMINATION (APPROVED/DENIED/NEEDS_INVESTIGATION), the most
    # applicable coverage guideline, comparable past claims, and a specific
    # recommended action with rationale.
    # """
    #
    # client = anthropic.Anthropic()
    # message = client.messages.create(
    #     model="claude-sonnet-4-6",
    #     max_tokens=1024,
    #     messages=[{"role": "user", "content": prompt}],
    # )
    # return message.content[0].text
