"""
AI output generation — Retail Customer Support.

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
    Generate a service recommendation for a retail return, exchange, or refund request.
    """

    # =========================================================================
    # OPTION A — Template engine (ACTIVE by default, no API key required)
    # =========================================================================

    record_id = record.get("record_id", "UNKNOWN")
    request_type = (record.get("request_type") or "unknown").upper()
    order_id = record.get("order_id", "N/A")
    product_name = record.get("product_name", "N/A")
    order_amount = record.get("order_amount", 0.0)
    days_since_purchase = record.get("days_since_purchase", 0)
    loyalty_tier = (record.get("loyalty_tier") or "standard").lower()
    product_category = (record.get("product_category") or "").lower()

    top_kb = knowledge_items[0] if knowledge_items else {}
    top_hist = historical_records[0] if historical_records else {}
    hist_outcome = top_hist.get("outcome", "")

    # Determination logic
    days = record.get("days_since_purchase", 999)
    order_amount_val = record.get("order_amount", 0.0)

    # Return window thresholds by loyalty tier
    window = {"platinum": 60, "gold": 45}.get(loyalty_tier, 30)

    if days <= window:
        determination = "APPROVE — WITHIN RETURN POLICY"
    elif order_amount_val > 500 and days > 30:
        determination = "ESCALATE — HIGH-VALUE OUT-OF-WINDOW REQUEST"
    elif days <= 90 and hist_outcome in ("APPROVE",):
        determination = "APPROVE — DEFECT EXCEPTION AUTHORIZED"
    elif hist_outcome == "ESCALATE":
        determination = "ESCALATE — REQUIRES SENIOR REVIEW"
    else:
        determination = "DENY — OUTSIDE RETURN POLICY WINDOW"

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
    hist_block = "\n".join(hist_lines) if hist_lines else "  - No comparable requests retrieved."

    if "APPROVE" in determination:
        next_action = (
            "Process return/refund. Issue refund to original payment method or "
            "store credit per customer preference."
        )
    elif "DENY" in determination:
        next_action = (
            "Decline return. Advise customer to contact the manufacturer for "
            "warranty claims if applicable."
        )
    else:
        next_action = (
            "Route to senior customer support. Flag for high-value exception review."
        )

    output = f"""\
CUSTOMER SUPPORT RECOMMENDATION
Request: {record_id} | Type: {request_type} | Order: {order_id}
Product: {product_name} | Amount: ${order_amount_val:.2f}
Loyalty Tier: {loyalty_tier.upper()} | Days Since Purchase: {days_since_purchase}
Generated: {timestamp}

DETERMINATION: {determination}

APPLICABLE RETURN POLICY
Policy: {kb_title}
Category: {kb_category}
Excerpt: {kb_excerpt}{"..." if kb_long else ""}

COMPARABLE PAST REQUESTS
{hist_block}

RECOMMENDED ACTION
{next_action}

---
DRAFT — Requires agent review before action."""

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
    # You are a retail customer support system. Based on the return/refund request
    # below and the retrieved return policies and comparable past requests, produce
    # a structured service recommendation.
    #
    # REQUEST TEXT:
    # {record_text}
    #
    # RETURN POLICIES:
    # {kb_context}
    #
    # COMPARABLE PAST REQUESTS:
    # {hist_context}
    #
    # Generated at: {timestamp}
    #
    # Provide: DETERMINATION (APPROVE/DENY/ESCALATE), the most applicable policy,
    # comparable past cases, and a specific recommended action.
    # """
    #
    # client = anthropic.Anthropic()
    # message = client.messages.create(
    #     model="claude-sonnet-4-6",
    #     max_tokens=1024,
    #     messages=[{"role": "user", "content": prompt}],
    # )
    # return message.content[0].text
