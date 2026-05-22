"""
Retail Customer Support — demo records.

Three scenarios covering common return, exchange, and refund request types:
  A — Electronics return within policy window (clean approve path)
  B — Apparel return outside window, loyal customer with defect claim
  C — High-value appliance defect claim, far outside window (escalation path)
"""

DEMO_RECORDS = {
    "A": {
        "record_id": "REQ-001-A",
        "scenario": "A",
        "demo_record": True,
        "processing_status": "PENDING",
        "request_type": "return",
        "order_id": "ORD-887234",
        "product_category": "electronics",
        "product_name": "Sony WH-1000XM5 Headphones",
        "order_amount": 349.99,
        "days_since_purchase": 15,
        "loyalty_tier": "standard",
        "record_text": (
            "Emily Johnson requests return of Sony WH-1000XM5 wireless headphones purchased "
            "15 days ago for $349.99. Reason: Bluetooth pairing is unstable with her existing "
            "devices and the product does not meet expectations. Item is unopened in original "
            "factory-sealed packaging and customer has retained the receipt. Customer has been "
            "a member for 8 months with 2 prior orders and zero prior returns. Return window "
            "for electronics is 30 days with original packaging; this request falls within "
            "the policy window. Customer is requesting a full refund to her original payment "
            "method. No damage has been reported and the item is eligible for restocking."
        ),
    },
    "B": {
        "record_id": "REQ-001-B",
        "scenario": "B",
        "demo_record": True,
        "processing_status": "PENDING",
        "request_type": "return",
        "order_id": "ORD-443219",
        "product_category": "apparel",
        "product_name": "Patagonia Down Sweater Jacket",
        "order_amount": 229.00,
        "days_since_purchase": 53,
        "loyalty_tier": "gold",
        "record_text": (
            "Marcus Chen requests return of a Patagonia Down Sweater Jacket purchased 53 days "
            "ago for $229.00. The jacket developed a small tear at the left seam after "
            "approximately 8 wears; customer believes this constitutes a manufacturing defect. "
            "Standard return window is 30 days, placing this request 23 days outside the "
            "policy window. Customer is a Gold loyalty tier member with $2,400 in purchases "
            "over 3 years and zero prior return requests. The item has been worn and laundered "
            "and original packaging has not been retained. Customer requests an exchange for "
            "the same item or a full refund. Policy for defect claims allows exceptions at "
            "supervisor discretion for verified manufacturing defects within 90 days."
        ),
    },
    "C": {
        "record_id": "REQ-001-C",
        "scenario": "C",
        "demo_record": True,
        "processing_status": "PENDING",
        "request_type": "refund",
        "order_id": "ORD-996101",
        "product_category": "appliances",
        "product_name": "Dyson V15 Detect Vacuum",
        "order_amount": 749.99,
        "days_since_purchase": 102,
        "loyalty_tier": "silver",
        "record_text": (
            "Patricia Wu requests a full refund for a Dyson V15 Detect vacuum purchased "
            "102 days ago for $749.99. Customer claims the suction motor failed during normal "
            "use after approximately 90 days of operation. Standard return window is 30 days, "
            "placing this request 72 days outside the policy. Customer states this is a "
            "manufacturing defect covered by the 2-year manufacturer warranty but has not "
            "yet contacted Dyson warranty service. Account history shows 1 prior return in "
            "18 months, processed within the policy window. Customer is requesting a store "
            "refund rather than a manufacturer warranty claim. Per policy, out-of-window "
            "defect claims over $200 for appliances require escalation to senior support."
        ),
    },
}
