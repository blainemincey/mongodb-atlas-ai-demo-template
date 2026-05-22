"""
Insurance Claims P&C — demo records.

Three scenarios covering common auto and property claim types:
  A — Auto collision, rear-end impact (clean approval path)
  B — Homeowners water damage, coverage dispute (sudden vs. gradual)
  C — Auto total loss with ACV dispute (investigation path)
"""

DEMO_RECORDS = {
    "A": {
        "record_id": "CLM-001-A",
        "scenario": "A",
        "demo_record": True,
        "processing_status": "PENDING",
        "claim_type": "auto_collision",
        "policy_type": "comprehensive",
        "incident_date": "2025-05-10",
        "claim_amount": 8400,
        "deductible": 500,
        "policy_number": "AUTO-887234",
        "record_text": (
            "Jennifer Martinez reports a rear-end collision on Highway 101 on May 10, 2025. "
            "Her 2022 Honda Accord was stopped at a red light when struck from behind by a "
            "2019 Ford F-150 driven by the at-fault party. A police report was filed at the "
            "scene (case number 2025-05-10-1842), and the other driver admitted fault to the "
            "responding officer. Damage is confined to the rear bumper, trunk lid, and tail "
            "light assembly. Three independent repair estimates were obtained ranging from "
            "$7,800 to $8,400; the preferred estimate of $8,400 is from a certified network "
            "shop. No injuries were reported by either party. Claimant requests a rental "
            "vehicle for the estimated 7-day repair period. Policy is current with no lapses "
            "in coverage over the past 36 months."
        ),
    },
    "B": {
        "record_id": "CLM-001-B",
        "scenario": "B",
        "demo_record": True,
        "processing_status": "PENDING",
        "claim_type": "property_water",
        "policy_type": "homeowners",
        "incident_date": "2025-05-14",
        "claim_amount": 18500,
        "deductible": 1000,
        "policy_number": "HO-443219",
        "record_text": (
            "Robert Kim reports water damage to his kitchen and dining room discovered on "
            "May 14, 2025, upon returning home after a 4-day trip. The damage source is "
            "identified as a failed supply line beneath the kitchen sink. A restoration "
            "contractor has submitted an estimate of $18,500 covering water extraction, "
            "structural drying, flooring replacement, and cabinet repair. The policy covers "
            "sudden and accidental water discharge but explicitly excludes gradual leakage "
            "and continuous seepage. Property inspection conducted by an insurer-assigned "
            "adjuster reveals cabinet base staining consistent with prolonged moisture "
            "exposure estimated at 2 to 6 weeks prior to discovery. The contractor's "
            "documentation notes deteriorated supply line fitting with visible mineral "
            "deposits indicative of long-term aging. A coverage dispute exists: the "
            "insurer's preliminary assessment suggests gradual leakage preceded the "
            "final supply line failure."
        ),
    },
    "C": {
        "record_id": "CLM-001-C",
        "scenario": "C",
        "demo_record": True,
        "processing_status": "PENDING",
        "claim_type": "auto_total_loss",
        "policy_type": "comprehensive",
        "incident_date": "2025-05-01",
        "claim_amount": 31200,
        "deductible": 500,
        "policy_number": "AUTO-996101",
        "record_text": (
            "Thomas Brown reports a total loss of his 2021 Toyota Camry XSE following a "
            "collision on May 1, 2025. The vehicle was declared a total loss by the "
            "assigned adjuster, with structural repair costs exceeding 75% of the "
            "vehicle's actual cash value. The insurer's ACV determination is $29,500, "
            "based on comparable market vehicles of the same year, make, model, trim, "
            "and mileage. The claimant disputes this valuation, providing three private "
            "market listings for comparable vehicles priced between $31,200 and $33,400, "
            "citing aftermarket upgrades including a premium audio system and custom "
            "alloy wheels as justification for the higher value. The claimant requests "
            "settlement at $31,200. Salvage value has been assessed at $4,200. The "
            "claimant requests to retain the salvage for independent sale, which under "
            "policy language would reduce the settlement by the assessed salvage value."
        ),
    },
}
