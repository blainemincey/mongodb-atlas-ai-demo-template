"""
IT Support Ticket Triage — demo records.

Three scenarios covering the most common help desk ticket types:
  A — Hardware boot failure (clean warranty dispatch path)
  B — Software ERP crash after OS update (multi-user incident)
  C — Remote VPN connectivity failure (borderline escalation)
"""

DEMO_RECORDS = {
    "A": {
        "record_id": "TKT-001-A",
        "scenario": "A",
        "demo_record": True,
        "processing_status": "PENDING",
        "ticket_type": "hardware",
        "priority": "high",
        "department": "Engineering",
        "asset_tag": "LT-4821",
        "record_text": (
            "Employee reports that their Dell XPS 15 laptop will not boot as of this morning. "
            "Device powers on — fans spin and power light illuminates — but the screen remains "
            "black and the OS never loads. Diagnostics via F12 boot menu show hard drive health "
            "check failed with error code 2000-0142. Asset tag LT-4821, assigned to Sarah Chen, "
            "Engineering department, purchased 28 months ago. Device is within the 3-year "
            "ProSupport warranty. Employee is currently unable to work and requests urgent "
            "resolution. IT has attempted a power cycle and external monitor connection; issue "
            "persists. No recent physical damage reported; device has not been dropped or "
            "exposed to liquid."
        ),
    },
    "B": {
        "record_id": "TKT-001-B",
        "scenario": "B",
        "demo_record": True,
        "processing_status": "PENDING",
        "ticket_type": "software",
        "priority": "medium",
        "department": "Finance",
        "asset_tag": "DT-2203",
        "record_text": (
            "Employee reports that the company ERP application (SAP S/4HANA) crashes immediately "
            "on launch since yesterday afternoon. Error message: 'Runtime error: ABAP memory "
            "overflow — transaction MIRO'. Issue began following the Windows 11 22H2 cumulative "
            "update pushed by IT at 14:00 on Tuesday. Asset tag DT-2203, assigned to Marcus Webb, "
            "Finance AP team. Two other Finance users on the same update report the same crash; "
            "users on the prior update are unaffected. SAP GUI version 7.70 patch 5 was working "
            "correctly before the Windows update. No recent changes to SAP configuration or user "
            "permissions. User needs access to process month-end invoices by Friday."
        ),
    },
    "C": {
        "record_id": "TKT-001-C",
        "scenario": "C",
        "demo_record": True,
        "processing_status": "PENDING",
        "ticket_type": "network",
        "priority": "high",
        "department": "Sales",
        "asset_tag": "LT-3307",
        "record_text": (
            "Employee reports inability to connect to the corporate VPN from home since Monday "
            "morning. Cisco AnyConnect client shows error: 'Secure gateway has rejected the "
            "agent's VPN connect or reconnect request — Reason 442: Failed to enable Virtual "
            "Adapter'. Issue is isolated to this user; other remote employees on the same ISP "
            "subnet report no VPN issues. Asset tag LT-3307, assigned to David Park, Sales team. "
            "Laptop OS: Windows 10 22H2. Home router is a consumer Netgear device; user has not "
            "changed any router settings. Network adapter driver version is current. Reinstalling "
            "AnyConnect did not resolve the issue. User is a senior account executive with active "
            "client commitments requiring CRM and internal tool access."
        ),
    },
}
