"""
AI output generation — Healthcare Prior Authorization.

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
    Generate a prior authorization recommendation for a healthcare request.
    """

    # =========================================================================
    # OPTION A — Template engine (ACTIVE by default, no API key required)
    # =========================================================================

    record_id = record.get("record_id", "UNKNOWN")
    service_type = (record.get("service_type") or "unknown").lower()
    plan_type = (record.get("plan_type") or "unknown").upper()
    member_id = record.get("member_id", "N/A")

    top_kb = knowledge_items[0] if knowledge_items else {}
    top_hist = historical_records[0] if historical_records else {}
    hist_outcome = top_hist.get("outcome", "")

    # Determination logic
    if service_type == "medical_imaging":
        if hist_outcome == "APPROVED":
            determination = "APPROVED"
        elif hist_outcome == "DENIED":
            determination = "DENIED"
        else:
            determination = "PEND_FOR_REVIEW"
    elif service_type == "specialty_pharmacy":
        if hist_outcome == "APPROVED":
            determination = "APPROVED"
        elif hist_outcome == "DENIED":
            determination = "DENIED"
        else:
            determination = "PEND_FOR_REVIEW — PENDING ADDITIONAL DOCUMENTATION"
    else:  # behavioral_health or other
        if hist_outcome == "APPROVED":
            determination = "APPROVED"
        else:
            determination = "PEND_FOR_REVIEW — CLINICAL REVIEW REQUIRED"

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
    hist_block = "\n".join(hist_lines) if hist_lines else "  - No comparable cases retrieved."

    if determination == "APPROVED":
        next_action = (
            "Approve for requested service/drug. Issue authorization number."
        )
    elif determination == "DENIED":
        next_action = (
            "Issue denial with clinical rationale. Member has appeal rights within 60 days."
        )
    else:
        next_action = (
            "Request additional clinical documentation from requesting provider. "
            "Decision pending."
        )

    output = f"""\
PRIOR AUTHORIZATION RECOMMENDATION
Request: {record_id} | Service: {service_type.upper()} | Plan: {plan_type}
Member: {member_id}
Generated: {timestamp}

DETERMINATION: {determination}

APPLICABLE COVERAGE POLICY
Policy: {kb_title}
Category: {kb_category}
Excerpt: {kb_excerpt}{"..." if kb_long else ""}

COMPARABLE PRIOR AUTH CASES
{hist_block}

RECOMMENDED ACTION
{next_action}

---
DRAFT — Requires clinical reviewer sign-off before action."""

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
    # You are a prior authorization clinical review system. Based on the request
    # below and the retrieved coverage policies and comparable past cases, produce
    # a structured authorization recommendation.
    #
    # REQUEST TEXT:
    # {record_text}
    #
    # COVERAGE POLICIES:
    # {kb_context}
    #
    # COMPARABLE PRIOR AUTH CASES:
    # {hist_context}
    #
    # Generated at: {timestamp}
    #
    # Provide: DETERMINATION (APPROVED/DENIED/PEND_FOR_REVIEW), the most
    # applicable coverage policy, comparable cases, and a specific recommended
    # action.
    # """
    #
    # client = anthropic.Anthropic()
    # message = client.messages.create(
    #     model="claude-sonnet-4-6",
    #     max_tokens=1024,
    #     messages=[{"role": "user", "content": prompt}],
    # )
    # return message.content[0].text
