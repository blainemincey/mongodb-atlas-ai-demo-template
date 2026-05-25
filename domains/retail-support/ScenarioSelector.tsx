import type { Scenario } from "../types";

const SCENARIOS = [
  {
    key: "A" as Scenario,
    label: "Scenario A",
    title: "Electronics Return — Within Window",
    subtitle: "Returns · Standard · 15 Days",
    detail: "Sony headphones, unopened, within 30-day policy. Clean approval path — surfaces standard electronics return policy and comparable in-window returns.",
  },
  {
    key: "B" as Scenario,
    label: "Scenario B",
    title: "Apparel Return — Outside Window, Defect",
    subtitle: "Returns · Gold Tier · 53 Days",
    detail: "Patagonia jacket with seam defect, 23 days outside the window. Gold loyalty tier with zero prior returns — demonstrates the defect exception policy and comparable Gold-tier approvals.",
  },
  {
    key: "C" as Scenario,
    label: "Scenario C",
    title: "High-Value Appliance — Refund Dispute",
    subtitle: "Refunds · Silver · 102 Days",
    detail: "Dyson vacuum claimed defect at 102 days, no manufacturer contact. High-value threshold triggers escalation path — shows senior review policy and comparable escalated cases.",
  },
];

interface Props {
  active: Scenario | null;
  onSelect: (s: Scenario) => void;
  disabled: boolean;
}

export default function ScenarioSelector({ active, onSelect, disabled }: Props) {
  return (
    <div style={{ marginTop: "var(--space-5)", marginBottom: "var(--space-2)" }}>
      <p className="eyebrow" style={{ marginBottom: "var(--space-3)" }}>
        Select Demo Scenario
      </p>
      <div style={{ display: "flex", gap: "var(--space-4)", flexWrap: "wrap" }}>
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
                background: isActive ? "var(--success-bg)" : "var(--surface)",
                border: `1px solid ${isActive ? "var(--brand)" : "var(--border)"}`,
                borderRadius: "var(--radius-lg)",
                padding: "var(--space-4) var(--space-5)",
                color: "var(--text)",
                cursor: disabled ? "not-allowed" : "pointer",
                opacity: disabled ? 0.7 : 1,
                boxShadow: isActive ? "var(--shadow-sm)" : "none",
                transition: "border-color 0.2s, background 0.2s, box-shadow 0.2s",
              }}
            >
              <div style={{ marginBottom: 6 }}>
                <span className="eyebrow eyebrow--accent">
                  {s.label}
                </span>
              </div>
              <div style={{
                fontSize: "var(--fs-md)",
                fontWeight: isActive ? "var(--fw-bold)" : "var(--fw-semibold)",
                color: "var(--text)",
                marginBottom: 2,
              }}>
                {s.title}
              </div>
              <div style={{
                fontSize: "var(--fs-sm)",
                color: "var(--accent-mark)",
                fontFamily: "Source Code Pro, monospace",
                marginBottom: 6,
              }}>
                {s.subtitle}
              </div>
              <div style={{
                fontSize: "var(--fs-sm)",
                color: "var(--text-muted)",
                lineHeight: "var(--lh-base)",
              }}>
                {s.detail}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
