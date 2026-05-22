import type { Scenario } from "../types";

const SCENARIOS = [
  {
    key: "A" as Scenario,
    label: "Scenario A",
    title: "Limitation of Liability — Mutual Cap",
    subtitle: "Liability · SaaS Services · Low Risk",
    detail: "Mutual 12-month fee cap with standard carve-outs. Surfaces market-standard liability guidelines and comparable acceptable clauses.",
  },
  {
    key: "B" as Scenario,
    label: "Scenario B",
    title: "Indemnification — One-Sided Clause",
    subtitle: "Liability · Vendor Agreement · High Risk",
    detail: "Vendor proposes broad company indemnification with no reciprocal obligations. Demonstrates how the system flags one-sided provisions against standard market terms.",
  },
  {
    key: "C" as Scenario,
    label: "Scenario C",
    title: "IP Assignment — No Carve-Outs",
    subtitle: "IP · Consulting Agreement · Critical Risk",
    detail: "Overbroad IP assignment covering all consultant work during the term with no pre-existing IP carve-outs. Escalation path — requires senior counsel review.",
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
