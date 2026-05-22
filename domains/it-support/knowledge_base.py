"""
IT Support Ticket Triage — knowledge base.

Resolution procedures and troubleshooting guides across hardware, software,
and network categories. Each item's content_text is embedded by Voyage AI
so that relevant procedures surface when an incoming ticket is searched.
"""

KNOWLEDGE_BASE = [
    {
        "kb_id": "KB-001",
        "title": "Hard Drive Failure — Diagnosis and Replacement Procedure",
        "category": "hardware",
        "subcategory": "storage",
        "content_text": (
            "A Dell error code 2000-0142 confirms hard drive failure via built-in diagnostics. "
            "Verify warranty status in Dell TechDirect using the service tag before ordering a "
            "replacement. If under ProSupport warranty, initiate a next-business-day on-site "
            "dispatch for a technician to replace the drive and restore from backup. Back up any "
            "accessible data using a live USB environment if the drive is partially readable. "
            "Expected resolution time is 1–2 business days pending parts availability."
        ),
    },
    {
        "kb_id": "KB-002",
        "title": "Hardware Warranty Claim and Dispatch Process",
        "category": "hardware",
        "subcategory": "warranty",
        "content_text": (
            "All Dell assets under ProSupport contract are covered for parts and labor for the "
            "contract duration. Verify warranty status at dell.com/support using the service tag "
            "or asset tag. For on-site dispatch, open a case via Dell TechDirect and select "
            "'Dispatch' — a technician arrives next business day for ProSupport, or within 4 "
            "hours for ProSupport Critical. Document the case number in ServiceNow CMDB. "
            "End-of-warranty devices exceeding 60% of replacement value in repair cost should "
            "be flagged for the hardware refresh cycle."
        ),
    },
    {
        "kb_id": "KB-003",
        "title": "User Data Backup Verification Before Hardware Repair",
        "category": "hardware",
        "subcategory": "data-protection",
        "content_text": (
            "Before any hardware repair involving storage removal, confirm whether the device is "
            "enrolled in endpoint backup (CrashPlan or OneDrive for Business) and that the last "
            "backup completed within 24 hours. If backup is current, proceed directly to repair. "
            "If backup is stale or the drive is partially readable, boot from an IT-provisioned "
            "live USB and copy Documents, Desktop, and Downloads to OneDrive before repair. "
            "Log backup status and verification date in the ServiceNow ticket."
        ),
    },
    {
        "kb_id": "KB-004",
        "title": "Windows Cumulative Update Rollback Procedure",
        "category": "software",
        "subcategory": "os-updates",
        "content_text": (
            "When a Windows cumulative update causes application incompatibility, roll back the "
            "update on affected devices: Settings → Windows Update → Update History → Uninstall "
            "Updates, then remove the identified KB number. If rollback resolves the issue, "
            "quarantine the update in WSUS or Intune and open a vendor ticket to report the "
            "incompatibility. Do not roll back security patches without change advisory board "
            "approval unless a critical business process is affected. Test rollback on one device "
            "before deploying to all affected users."
        ),
    },
    {
        "kb_id": "KB-005",
        "title": "SAP GUI Compatibility with Windows OS Updates",
        "category": "software",
        "subcategory": "enterprise-apps",
        "content_text": (
            "SAP S/4HANA and SAP GUI are sensitive to Windows OS updates; ABAP runtime errors "
            "following a Windows update are a known compatibility vector. Check the SAP "
            "Compatibility Matrix (SAP Note 2580360) for the current GUI version against the "
            "installed Windows build. Immediate mitigation: roll back the Windows update per "
            "KB-004. Long-term fix: upgrade SAP GUI to the version certified for the new "
            "Windows build before re-deploying the update. Coordinate with the Finance "
            "application owner and SAP Basis team for any SAP-side changes."
        ),
    },
    {
        "kb_id": "KB-006",
        "title": "Cisco AnyConnect Error 442 — Virtual Adapter Resolution",
        "category": "network",
        "subcategory": "vpn",
        "content_text": (
            "AnyConnect error 442 (Failed to enable Virtual Adapter) is caused by a conflict "
            "between the Cisco VPN virtual adapter and the host OS network stack or a third-party "
            "security product. Resolution steps: (1) Uninstall and reinstall AnyConnect using "
            "the IT-managed MSI package. (2) In Device Manager, show hidden devices and delete "
            "any stale network adapters under Network Adapters. (3) Disable third-party VPN "
            "clients or firewall software with network filtering. (4) Run 'netsh int ip reset' "
            "and 'netsh winsock reset' as administrator, then reboot. Router changes are not "
            "typically required for this error."
        ),
    },
    {
        "kb_id": "KB-007",
        "title": "VPN Connectivity — Isolating Home Network vs. Client Issues",
        "category": "network",
        "subcategory": "vpn",
        "content_text": (
            "When a VPN failure is isolated to a single remote user and other users on the same "
            "ISP report no problems, the issue is likely client-side rather than gateway or ISP. "
            "Ask the user to test on a mobile hotspot to isolate the home router as a variable. "
            "Consumer routers occasionally block IKEv2 or DTLS; confirm AnyConnect is configured "
            "for SSL fallback. If the hotspot test also fails, escalate to network security — "
            "the issue may be a corrupted or expired machine certificate required for tunnel "
            "authentication, requiring certificate re-enrollment via SCEP."
        ),
    },
    {
        "kb_id": "KB-008",
        "title": "Escalation Criteria for Network and Security Issues",
        "category": "network",
        "subcategory": "escalation",
        "content_text": (
            "Escalate to the network security team when: (1) standard VPN remediation steps "
            "(reinstall, adapter reset, winsock reset) fail to restore connectivity; (2) the "
            "issue persists on a mobile hotspot, ruling out the user's home network; (3) the "
            "device certificate or user certificate store is suspected to be corrupted or "
            "expired. Network security will inspect the certificate store, verify SCEP enrollment "
            "status, and re-enroll the machine certificate if needed. Expected resolution time "
            "after escalation: 4–8 business hours."
        ),
    },
]
