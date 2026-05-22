"""
AI output generation — Legal Contract Review.

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
    Generate a legal assessment recommendation for a contract clause review.
    """

    # =========================================================================
    # OPTION A — Template engine (ACTIVE by default, no API key required)
    # =========================================================================

    record_id = record.get("record_id", "UNKNOWN")
    clause_type = (record.get("clause_type") or "unknown").lower()
    risk_level = (record.get("risk_level") or "low").lower()
    contract_type = record.get("contract_type", "N/A")
    jurisdiction = record.get("jurisdiction", "N/A")

    top_kb = knowledge_items[0] if knowledge_items else {}
    top_hist = historical_records[0] if historical_records else {}
    hist_outcome = top_hist.get("outcome", "")

    # Determination logic
    if risk_level == "critical":
        determination = "ESCALATE_TO_COUNSEL"
    elif risk_level == "high":
        if hist_outcome in ("FLAG_FOR_REVISION", "ESCALATE_TO_COUNSEL"):
            determination = "FLAG_FOR_REVISION"
        else:
            determination = "FLAG_FOR_REVISION"
    elif risk_level == "low":
        if hist_outcome == "ACCEPTABLE":
            determination = "ACCEPTABLE"
        else:
            determination = "FLAG_FOR_REVISION"
    else:
        determination = "FLAG_FOR_REVISION"

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
    hist_block = "\n".join(hist_lines) if hist_lines else "  - No comparable reviews retrieved."

    if determination == "ACCEPTABLE":
        next_action = "Clause meets market-standard terms. Approved for execution."
    elif determination == "FLAG_FOR_REVISION":
        next_action = (
            "Return clause to counterparty with redline comments. "
            "Do not execute until revised."
        )
    else:
        next_action = (
            "Route to senior counsel immediately. "
            "Do not proceed with execution pending review."
        )

    output = f"""\
CONTRACT CLAUSE REVIEW
Record: {record_id} | Clause: {clause_type.upper()} | Contract: {contract_type}
Risk Level: {risk_level.upper()} | Jurisdiction: {jurisdiction}
Generated: {timestamp}

DETERMINATION: {determination}

APPLICABLE STANDARD
Standard: {kb_title}
Category:  {kb_category}
Excerpt:   {kb_excerpt}{"..." if kb_long else ""}

COMPARABLE PAST REVIEWS
{hist_block}

RECOMMENDED ACTION
{next_action}

---
DRAFT — Requires attorney review before action."""

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
    # You are a legal contract review system. Based on the contract clause below
    # and the retrieved contract standards and comparable past clause reviews,
    # produce a structured legal assessment recommendation.
    #
    # CLAUSE TEXT:
    # {record_text}
    #
    # CONTRACT STANDARDS:
    # {kb_context}
    #
    # COMPARABLE PAST REVIEWS:
    # {hist_context}
    #
    # Generated at: {timestamp}
    #
    # Provide: DETERMINATION (ACCEPTABLE/FLAG_FOR_REVISION/ESCALATE_TO_COUNSEL),
    # the most applicable contract standard, comparable past reviews, and a
    # specific recommended action.
    # """
    #
    # client = anthropic.Anthropic()
    # message = client.messages.create(
    #     model="claude-sonnet-4-6",
    #     max_tokens=1024,
    #     messages=[{"role": "user", "content": prompt}],
    # )
    # return message.content[0].text
