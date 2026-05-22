"""
AI output generation.

Two implementation options are provided below. Option A is active by default
and requires no additional API keys. Switch to Option B when you want a real
LLM call instead of a template-assembled output.
"""


def generate_output(
    record: dict,
    knowledge_items: list[dict],
    historical_records: list[dict],
    timestamp: str,
) -> str:
    """
    Generate AI output for a processed record given retrieved context.

    Args:
        record:             The demo record document from MongoDB.
        knowledge_items:    Top-k results from knowledge_base vector search.
        historical_records: Top-k results from historical_records vector search.
        timestamp:          ISO-formatted UTC timestamp string.

    Returns:
        A string containing the AI output to be written back to the record.
    """

    # =========================================================================
    # OPTION A — Template engine (ACTIVE by default, no API key required)
    #
    # Assembles structured output from the retrieved context using f-strings.
    # Replace or extend the sections below to match your domain's output format.
    # =========================================================================

    record_id = record.get("record_id", "UNKNOWN")

    top_kb = knowledge_items[0] if knowledge_items else {}
    kb_title = top_kb.get("title", "N/A")
    kb_category = top_kb.get("category", "N/A")
    kb_excerpt = (top_kb.get("content_text", "") or "")[:300]

    hist_lines = []
    for h in historical_records[:2]:
        hid = h.get("record_id", "")
        outcome = h.get("outcome", "")
        rationale = (h.get("outcome_rationale", "") or "")[:160]
        hist_lines.append(f"  - {hid} ({outcome}): {rationale}")
    hist_block = "\n".join(hist_lines) if hist_lines else "  - No comparable records retrieved."

    output = f"""\
AI OUTPUT
Record: {record_id}
Generated: {timestamp}

RETRIEVED KNOWLEDGE BASE MATCH
Item: {kb_title}
Category: {kb_category}
Excerpt: {kb_excerpt}{'...' if len(top_kb.get('content_text', '') or '') > 300 else ''}

COMPARABLE HISTORICAL RECORDS
{hist_block}

DETERMINATION
[TODO: Replace this section with domain-specific output logic.
 Use record fields, knowledge_items, and historical_records to
 generate a meaningful recommendation or decision for your domain.]

---
DRAFT — Requires human review before use."""

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
    # record_id = record.get("record_id", "")
    #
    # prompt = f"""\
    # You are processing record {record_id}. Based on the retrieved knowledge base
    # items and historical examples below, generate a structured output for this record.
    #
    # RECORD TEXT:
    # {record_text}
    #
    # KNOWLEDGE BASE ITEMS:
    # {kb_context}
    #
    # HISTORICAL RECORDS:
    # {hist_context}
    #
    # Generated at: {timestamp}
    #
    # Provide a structured determination with supporting rationale.
    # """
    #
    # client = anthropic.Anthropic()
    # message = client.messages.create(
    #     model="claude-sonnet-4-6",
    #     max_tokens=1024,
    #     messages=[{"role": "user", "content": prompt}],
    # )
    # return message.content[0].text
