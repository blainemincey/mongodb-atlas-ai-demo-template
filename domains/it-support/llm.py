"""
AI output generation — IT Support Ticket Triage.

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
    Generate a triage recommendation for an IT support ticket.
    """

    # =========================================================================
    # OPTION A — Template engine (ACTIVE by default, no API key required)
    # =========================================================================

    record_id = record.get("record_id", "UNKNOWN")
    ticket_type = (record.get("ticket_type") or "unknown").upper()
    priority = (record.get("priority") or "unknown").upper()
    department = record.get("department", "")
    asset_tag = record.get("asset_tag", "N/A")

    top_kb = knowledge_items[0] if knowledge_items else {}
    top_hist = historical_records[0] if historical_records else {}
    hist_outcome = top_hist.get("outcome", "")

    # Determination logic
    if ticket_type in ("HARDWARE",) and hist_outcome == "RESOLVED":
        determination = "RESOLVED — DISPATCH STANDARD PROCEDURE"
    elif ticket_type == "SOFTWARE" and hist_outcome == "RESOLVED":
        determination = "RESOLVED — APPLY KNOWN FIX"
    elif hist_outcome == "ESCALATED" or not knowledge_items:
        determination = "ESCALATED — ROUTE TO SPECIALIST"
    elif ticket_type == "NETWORK":
        determination = "RESOLVED — APPLY STANDARD STEPS"
    else:
        determination = "RESOLVED — APPLY KNOWN FIX"

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
    hist_block = "\n".join(hist_lines) if hist_lines else "  - No comparable tickets retrieved."

    if "DISPATCH" in determination:
        next_action = (
            "Verify warranty status and initiate on-site dispatch. "
            "Confirm endpoint backup is current before technician arrival."
        )
    elif "SPECIALIST" in determination:
        next_action = (
            "Assign to specialist queue and notify user of escalated handling. "
            "Expected response within 4–8 business hours."
        )
    else:
        next_action = (
            "Apply the resolution procedure above. "
            "Confirm with user after each step before proceeding to the next."
        )

    output = f"""\
IT SUPPORT TICKET RECOMMENDATION
Ticket: {record_id} | Type: {ticket_type} | Priority: {priority}
Department: {department} | Asset: {asset_tag}
Generated: {timestamp}

DETERMINATION: {determination}

APPLICABLE RESOLUTION PROCEDURE
Procedure: {kb_title}
Category:  {kb_category}
Excerpt:   {kb_excerpt}{"..." if kb_long else ""}

COMPARABLE PAST TICKETS
{hist_block}

RECOMMENDED NEXT ACTION
{next_action}

---
DRAFT — Requires technician review before action."""

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
    # You are an IT support triage system. Based on the ticket below and the
    # retrieved resolution procedures and comparable past tickets, produce a
    # structured triage recommendation.
    #
    # TICKET TEXT:
    # {record_text}
    #
    # RESOLUTION PROCEDURES:
    # {kb_context}
    #
    # COMPARABLE PAST TICKETS:
    # {hist_context}
    #
    # Generated at: {timestamp}
    #
    # Provide: DETERMINATION (RESOLVED/ESCALATED/CLOSED_NO_ACTION), the most
    # applicable procedure, comparable cases, and a specific next action.
    # """
    #
    # client = anthropic.Anthropic()
    # message = client.messages.create(
    #     model="claude-sonnet-4-6",
    #     max_tokens=1024,
    #     messages=[{"role": "user", "content": prompt}],
    # )
    # return message.content[0].text
