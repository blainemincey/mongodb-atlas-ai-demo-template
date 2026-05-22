"""
Retail Customer Support — knowledge base.

Return policies and exception guidelines across returns, exchanges, and
refunds categories. Each item's content_text is embedded by Voyage AI
so that relevant policies surface when an incoming request is searched.
"""

KNOWLEDGE_BASE = [
    {
        "kb_id": "KB-001",
        "title": "Electronics Return Policy — Window and Condition Requirements",
        "category": "returns",
        "subcategory": "electronics",
        "content_text": (
            "Electronics may be returned within 30 days of purchase with original packaging "
            "and a valid receipt. Items must be unopened or undamaged to qualify for a full "
            "refund. Software, digital downloads, and opened in-ear headphones or earbuds are "
            "non-returnable due to hygiene and licensing restrictions. Opened items above $200 "
            "in value are subject to a restocking review before a refund is issued. Items "
            "returned in original factory-sealed condition are processed without restocking "
            "assessment."
        ),
    },
    {
        "kb_id": "KB-002",
        "title": "Apparel and Footwear Return Policy",
        "category": "returns",
        "subcategory": "apparel",
        "content_text": (
            "Apparel and footwear may be returned within 30 days of purchase if unworn, "
            "unwashed, and with all original tags attached. Items that have been worn or "
            "laundered are not eligible under the standard return policy. Exception: items "
            "with a verified manufacturing defect — such as seam failures, material "
            "separation, or hardware malfunction — may be returned for exchange or store "
            "credit within 90 days at supervisor discretion. Proof of defect, in the form "
            "of customer-submitted photos or in-store inspection, is required for any "
            "out-of-window defect claim."
        ),
    },
    {
        "kb_id": "KB-003",
        "title": "Manufacturing Defect Claims — Exception Criteria",
        "category": "returns",
        "subcategory": "defects",
        "content_text": (
            "Manufacturing defects — including seam failures, material separation, and "
            "hardware or motor malfunction under normal use — are eligible for return or "
            "exchange beyond the standard return window up to 90 days from purchase. "
            "The customer must provide evidence of the defect through photos submitted "
            "with the request or an in-store physical inspection. Gold and Platinum loyalty "
            "tier customers receive extended consideration and are given priority in "
            "supervisor review queues for defect exception claims."
        ),
    },
    {
        "kb_id": "KB-004",
        "title": "Loyalty Program Return Benefits",
        "category": "returns",
        "subcategory": "loyalty",
        "content_text": (
            "Loyalty tier members receive extended return windows compared to the standard "
            "30-day policy. Gold tier members have a 45-day return window and are eligible "
            "for one courtesy return per 12-month period beyond the window at supervisor "
            "discretion. Platinum tier members have a 60-day return window and two courtesy "
            "returns per 12-month period. Standard tier members are held to the 30-day "
            "standard policy with no extended window. All courtesy returns must be documented "
            "in the ticket notes by the approving supervisor."
        ),
    },
    {
        "kb_id": "KB-005",
        "title": "Exchange Policy — Same-Category Substitution",
        "category": "exchanges",
        "subcategory": "general",
        "content_text": (
            "Exchanges for same-category items are processed at the original price point; "
            "any price difference is refunded to the customer or charged as appropriate. "
            "Exchanges for defective items do not require original packaging — the defective "
            "item is accepted in its current condition. Exchanges are available for items "
            "within the standard policy window or for items approved under a defect exception. "
            "Size and color exchanges on apparel are processed as same-category swaps and "
            "do not require manager approval when within the return window."
        ),
    },
    {
        "kb_id": "KB-006",
        "title": "Refund Processing — Methods and Timeline",
        "category": "refunds",
        "subcategory": "processing",
        "content_text": (
            "Refunds to the original payment method are processed within 3 to 5 business "
            "days of the return being received and inspected. Store credit refunds are "
            "applied immediately upon approval. Cash refunds for in-store purchases over "
            "$50 require manager authorization before disbursement. Out-of-window refunds "
            "approved as exceptions are issued as store credit by default; the customer may "
            "request escalation to receive a refund to the original payment method instead."
        ),
    },
    {
        "kb_id": "KB-007",
        "title": "High-Value Item Returns — Escalation Threshold",
        "category": "refunds",
        "subcategory": "escalation",
        "content_text": (
            "Return and refund requests for items with an order value over $500 that are "
            "submitted beyond the standard 30-day return window require escalation to senior "
            "customer support before any decision is made. The senior agent is responsible "
            "for verifying defect evidence, reviewing the customer's full account history, "
            "and consulting with the relevant category team before issuing an approval, "
            "denial, or referral to manufacturer warranty. This threshold applies regardless "
            "of loyalty tier."
        ),
    },
    {
        "kb_id": "KB-008",
        "title": "Out-of-Window Return — Supervisor Discretion Guidelines",
        "category": "returns",
        "subcategory": "exceptions",
        "content_text": (
            "A supervisor may approve an out-of-window return under the following "
            "circumstances: documented manufacturing defects supported by photographic "
            "evidence or in-store inspection; natural disasters or hospitalization that "
            "prevented a timely return; or at their discretion for Gold or Platinum loyalty "
            "tier customers with a clean account history and no prior courtesy returns "
            "within the last 12 months. All supervisor-approved exceptions must be "
            "documented in the ticket notes with the stated reason for approval."
        ),
    },
]
