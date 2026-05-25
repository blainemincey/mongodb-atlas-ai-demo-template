"""
IT Support Ticket Triage — historical records.

Past resolved tickets used as analogues during vector search. Outcomes:
  RESOLVED           — fixed by standard procedure
  ESCALATED          — routed to specialist team
  CLOSED_NO_ACTION   — could not reproduce or user error
"""

HISTORICAL_RECORDS = [
    {
        "record_id": "HIST-001",
        "category": "hardware",
        "outcome": "RESOLVED",
        "outcome_rationale": (
            "Dell error 2000-0142 confirmed hard drive failure. On-site technician dispatched "
            "under ProSupport warranty; replacement SSD installed and OS restored from CrashPlan "
            "backup within 2 business days."
        ),
        "source_text": (
            "Engineering employee reported Dell XPS 15 (asset LT-3981) failing to boot with "
            "black screen. F12 diagnostics returned error 2000-0142; hard drive health check "
            "failed. Device was within 36-month ProSupport warranty. IT verified CrashPlan "
            "backup was current, dispatched Dell technician, drive replaced and data restored."
        ),
    },
    {
        "record_id": "HIST-002",
        "category": "hardware",
        "outcome": "ESCALATED",
        "outcome_rationale": (
            "Three Dell laptops in the same team reported boot failures within one week, all "
            "showing error 2000-0142. Batch failure pattern escalated to hardware engineering "
            "and vendor for potential Product Quality Notification investigation."
        ),
        "source_text": (
            "Multiple laptops in the Data Science team failed to boot within a 5-day window, "
            "all with drive diagnostic error 2000-0142. One device also showed GPU artifacts "
            "suggesting a possible board issue. Pattern escalated to hardware engineering; Dell "
            "opened a PQN investigation for the batch."
        ),
    },
    {
        "record_id": "HIST-003",
        "category": "software",
        "outcome": "RESOLVED",
        "outcome_rationale": (
            "Windows 11 cumulative update caused SAP GUI ABAP runtime crash. Update rolled back "
            "on all 12 affected Finance desktops; SAP GUI returned to normal. Update quarantined "
            "in WSUS pending SAP GUI upgrade to compatible version."
        ),
        "source_text": (
            "Finance AP team reported SAP S/4HANA crashing on launch after IT pushed a Windows "
            "cumulative update. Error: ABAP memory overflow on transaction MIRO. Affected 12 "
            "users on the new build; users on the prior build were unaffected. Windows update "
            "rolled back; SAP Basis confirmed GUI 7.70 patch 6 resolves the compatibility issue "
            "long-term."
        ),
    },
    {
        "record_id": "HIST-004",
        "category": "software",
        "outcome": "ESCALATED",
        "outcome_rationale": (
            "SAP crash persisted after Windows update rollback, indicating secondary profile "
            "corruption. Escalated to SAP Basis team; user profile rebuilt and targeted "
            "application server refresh applied."
        ),
        "source_text": (
            "Single Finance user continued experiencing SAP S/4HANA crashes after the Windows "
            "update rollback that resolved the issue for other users. Further investigation "
            "revealed the user's SAP profile had become corrupted during the failed update "
            "sequence. SAP Basis team rebuilt the profile and performed a system refresh."
        ),
    },
    {
        "record_id": "HIST-005",
        "category": "network",
        "outcome": "RESOLVED",
        "outcome_rationale": (
            "AnyConnect error 442 resolved by clearing stale hidden network adapters in Device "
            "Manager and running netsh winsock reset. VPN connection restored within 30 minutes "
            "of ticket opening."
        ),
        "source_text": (
            "Remote Sales employee reported Cisco AnyConnect error 442 from home. Other users "
            "on same ISP subnet had no issues. IT support cleared stale hidden adapters from "
            "Device Manager, ran 'netsh winsock reset', rebooted. VPN connectivity restored "
            "immediately. No router changes required."
        ),
    },
    {
        "record_id": "HIST-006",
        "category": "network",
        "outcome": "ESCALATED",
        "outcome_rationale": (
            "AnyConnect error 442 persisted after standard steps including hotspot test. Traced "
            "to expired machine certificate in the device's certificate store. Network security "
            "re-enrolled the certificate via SCEP; VPN restored."
        ),
        "source_text": (
            "Remote employee's AnyConnect error 442 was not resolved by reinstall, adapter "
            "reset, or winsock reset. Hotspot test also failed, ruling out the home router. "
            "Network security found the machine certificate required for VPN tunnel auth had "
            "expired and not auto-renewed. Certificate re-enrolled via SCEP; VPN restored."
        ),
    },
    {
        "record_id": "HIST-007",
        "category": "hardware",
        "outcome": "RESOLVED",
        "outcome_rationale": (
            "Laptop boot failure traced to failed RAM module rather than storage; memtest86 "
            "confirmed single DIMM failure. ProSupport dispatch; RAM replaced on-site with no "
            "data loss."
        ),
        "source_text": (
            "Employee reported Dell Latitude 5530 failing to boot with black screen. Disk "
            "diagnostics showed no errors. IT booted from live USB and ran memtest86; identified "
            "single DIMM failure. ProSupport dispatch arranged; on-site technician replaced RAM "
            "module. Device returned to service same day."
        ),
    },
    {
        "record_id": "HIST-008",
        "category": "software",
        "outcome": "CLOSED_NO_ACTION",
        "outcome_rationale": (
            "Reported ERP crash could not be reproduced. Investigation revealed user had "
            "installed an unauthorized third-party add-in. Removal resolved all crashes; ticket "
            "closed with user education note."
        ),
        "source_text": (
            "User reported intermittent SAP crashes suspected to follow a Windows update. IT "
            "could not reproduce on a clean device. Found the user had installed an unapproved "
            "third-party SAP add-in not authorized by IT. Removal of the add-in resolved all "
            "crashes; ticket closed with a note to user about the approved software policy."
        ),
    },
]
