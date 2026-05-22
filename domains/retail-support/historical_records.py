"""
Retail Customer Support — historical records.

Past resolved requests used as analogues during vector search. Outcomes:
  APPROVE    — request approved under policy or approved exception
  DENY       — request declined; customer directed to alternative if applicable
  ESCALATE   — routed to senior customer support for further review
"""

HISTORICAL_RECORDS = [
    {
        "record_id": "HIST-001",
        "category": "returns",
        "outcome": "APPROVE",
        "outcome_rationale": (
            "Electronics return submitted 18 days after purchase with original packaging "
            "and receipt. Item was within the 30-day standard return window and met all "
            "condition requirements; request approved and full refund issued to original "
            "payment method."
        ),
        "source_text": (
            "Customer requested return of a Bose SoundLink Bluetooth speaker purchased "
            "18 days prior, citing dissatisfaction with sound quality. Item arrived in "
            "original factory-sealed packaging with receipt. Return window and condition "
            "requirements were fully satisfied. Refund of $249.00 processed to original "
            "credit card within 5 business days."
        ),
    },
    {
        "record_id": "HIST-002",
        "category": "returns",
        "outcome": "DENY",
        "outcome_rationale": (
            "Apparel return submitted 65 days after purchase with no defect evidence and "
            "no special circumstances; request fell well outside the 30-day standard window "
            "and did not meet criteria for any policy exception."
        ),
        "source_text": (
            "Customer submitted a return request for a fleece pullover 65 days after "
            "purchase, citing a change of mind. No defect was claimed and no photos were "
            "provided. Customer was Standard tier with no applicable loyalty extension. "
            "Request was denied per standard policy; customer was advised that the return "
            "window had closed and no exception criteria applied."
        ),
    },
    {
        "record_id": "HIST-003",
        "category": "returns",
        "outcome": "APPROVE",
        "outcome_rationale": (
            "Gold loyalty tier customer reported a seam failure at 42 days, 12 days outside "
            "the standard window. Manufacturing defect was confirmed by in-store inspection "
            "and supervisor approved the return as a defect exception."
        ),
        "source_text": (
            "Gold tier customer returned a Columbia fleece jacket 42 days after purchase "
            "citing a seam failure at the right shoulder after normal wear. Customer brought "
            "the item in-store; associate confirmed visible manufacturing defect at the "
            "seam. Supervisor approved return as a defect exception per the 90-day defect "
            "policy. Exchange for the same item was processed at no additional charge."
        ),
    },
    {
        "record_id": "HIST-004",
        "category": "refunds",
        "outcome": "ESCALATE",
        "outcome_rationale": (
            "Customer claimed motor failure on a $680 stand mixer at 95 days post-purchase, "
            "exceeding the standard return window. Request was escalated to senior support "
            "per the high-value out-of-window policy threshold."
        ),
        "source_text": (
            "Silver tier customer submitted a refund request for a KitchenAid stand mixer "
            "purchased 95 days prior, claiming the motor stopped working during normal use. "
            "Order value of $679.99 exceeded the $500 escalation threshold for out-of-window "
            "high-value items. Request was routed to senior customer support for defect "
            "verification and account review before a determination was made."
        ),
    },
    {
        "record_id": "HIST-005",
        "category": "refunds",
        "outcome": "APPROVE",
        "outcome_rationale": (
            "Senior support confirmed motor failure on the escalated stand mixer claim after "
            "reviewing customer-submitted photos. Gold loyalty tier and clean account history "
            "supported approval; store credit issued as the exception refund method."
        ),
        "source_text": (
            "Following escalation of the KitchenAid stand mixer refund claim, senior support "
            "reviewed the customer-submitted photos showing visible motor burnout consistent "
            "with a manufacturing defect. Customer held Gold loyalty status with a clean "
            "prior return history. Senior agent approved the refund as a defect exception "
            "and issued store credit for $679.99."
        ),
    },
    {
        "record_id": "HIST-006",
        "category": "returns",
        "outcome": "DENY",
        "outcome_rationale": (
            "Silver tier customer claimed a defect on a coffee maker at 110 days, well "
            "outside the 90-day defect exception window. Customer was directed to contact "
            "the manufacturer for warranty service instead."
        ),
        "source_text": (
            "Silver tier customer requested a return on a Breville coffee maker purchased "
            "110 days prior, claiming the heating element failed. The 90-day manufacturing "
            "defect exception window had passed and the customer had not contacted Breville "
            "warranty service. Return request was denied; customer was directed to Breville's "
            "2-year manufacturer warranty program for resolution."
        ),
    },
    {
        "record_id": "HIST-007",
        "category": "exchanges",
        "outcome": "APPROVE",
        "outcome_rationale": (
            "Customer requested a size exchange on an apparel item within the return window. "
            "Same-category swap was processed without issues and no manager approval was "
            "required."
        ),
        "source_text": (
            "Customer purchased a running jacket and requested a size exchange from medium "
            "to large 12 days after purchase. Item was within the 30-day return window and "
            "tags were still attached. Associate processed the same-category exchange at the "
            "original price point; no price difference applied. Transaction completed at the "
            "service desk without supervisor involvement."
        ),
    },
    {
        "record_id": "HIST-008",
        "category": "returns",
        "outcome": "ESCALATE",
        "outcome_rationale": (
            "Customer disputed a defect claim on a laptop valued at $899 beyond the standard "
            "return window and had not contacted the manufacturer warranty service. High-value "
            "threshold and lack of warranty contact triggered escalation per policy."
        ),
        "source_text": (
            "Standard tier customer submitted a return request for a Dell laptop at 55 days "
            "post-purchase, claiming the display developed dead pixels during normal use. "
            "Order value of $899.00 exceeded the $500 escalation threshold. Customer had "
            "not contacted Dell warranty support prior to submitting the store return request. "
            "Request was escalated to senior customer support for defect review and "
            "determination on whether to process a store exception or refer to manufacturer."
        ),
    },
]
