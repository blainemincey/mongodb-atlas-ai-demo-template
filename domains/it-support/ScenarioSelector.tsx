import type { Scenario } from "../types";

const SCENARIOS = [
  {
    key: "A" as Scenario,
    label: "Scenario A",
    title: "Hardware — Laptop Boot Failure",
    subtitle: "Hardware · High Priority · Asset LT-4821",
    detail: "Dell hard drive failure (error 2000-0142) on an in-warranty device. Surfaces the replacement procedure and comparable resolved cases cleanly.",
  },
  {
    key: "B" as Scenario,
    label: "Scenario B",
    title: "Software — ERP Crash After Windows Update",
    subtitle: "Software · Medium Priority · Finance Team",
    detail: "SAP S/4HANA crashing on launch after a Windows update — three Finance users affected. Demonstrates the OS rollback KB and prior SAP compatibility incidents.",
  },
  {
    key: "C" as Scenario,
    label: "Scenario C",
    title: "Network — VPN Connection Failure",
    subtitle: "Network · High Priority · Remote User",
    detail: "Cisco AnyConnect error 442 isolating a single remote user. Borderline case — may resolve with standard steps or require escalation to network security.",
  },
];

interface Props {
  active: Scenario | null;
  onSelect: (s: Scenario) => void;
  disabled: boolean;
}

export default function ScenarioSelector({ active, onSelect, disabled }: Props) {
  return (
    <div style={{ marginTop: 24, marginBottom: 8 }}>
      <p style={{ fontSize: 11, color: "var(--mdb-text-dim)", marginBottom: 10, letterSpacing: "0.08em", textTransform: "uppercase" }}>
        Select Demo Scenario
      </p>
      <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
        {SCENARIOS.map((s) => {
          const isActive = active === s.key;
          return (
            <button
              key={s.key}
              onClick={() => onSelect(s.key)}
              disabled={disabled}
              style={{
                flex: 1,
                minWidth: 280,
                maxWidth: 480,
                textAlign: "left",
                background: isActive ? "var(--mdb-dark-green)" : "var(--mdb-slate)",
                border: `1px solid ${isActive ? "var(--mdb-green)" : "var(--mdb-border)"}`,
                borderRadius: "var(--radius-lg)",
                padding: "14px 18px",
                color: "var(--mdb-text)",
                cursor: disabled ? "not-allowed" : "pointer",
                opacity: disabled ? 0.7 : 1,
                transition: "border-color 0.2s, background 0.2s",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 6 }}>
                <div>
                  <span style={{ fontSize: 11, color: "var(--mdb-green)", fontWeight: 600, letterSpacing: "0.06em", textTransform: "uppercase" }}>
                    {s.label}
                  </span>
                </div>
                {isActive && <span style={{ fontSize: 10, color: "var(--mdb-green)", fontWeight: 700 }}>ACTIVE</span>}
              </div>
              <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 2 }}>{s.title}</div>
              <div style={{ fontSize: 12, color: "var(--mdb-green)", marginBottom: 6 }}>{s.subtitle}</div>
              <div style={{ fontSize: 12, color: "var(--mdb-text-dim)", lineHeight: 1.5 }}>{s.detail}</div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
