import type { Scenario } from "../types";

const SCENARIOS = [
  {
    key: "A" as Scenario,
    label: "Scenario A",
    title: "Auto Collision — Rear-End Impact",
    subtitle: "Auto · Comprehensive · $8,400",
    detail: "Clear liability with police report, admitted fault. Surfaces collision coverage guidelines and comparable approved claims cleanly.",
  },
  {
    key: "B" as Scenario,
    label: "Scenario B",
    title: "Homeowners — Water Damage Dispute",
    subtitle: "Property · Homeowners · $18,500",
    detail: "Coverage dispute between sudden failure and gradual leakage. Demonstrates the property exclusion policy and how comparable investigation cases are surfaced.",
  },
  {
    key: "C" as Scenario,
    label: "Scenario C",
    title: "Auto Total Loss — ACV Dispute",
    subtitle: "Auto · Comprehensive · $31,200",
    detail: "Total loss with claimant disputing actual cash value based on aftermarket upgrades. Illustrates the investigation path and ACV dispute resolution procedure.",
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
