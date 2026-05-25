import type { Scenario } from "../types";

const SCENARIOS = [
  {
    key: "A" as Scenario,
    label: "Scenario A",
    title: "Medical Imaging — Knee MRI",
    subtitle: "Medical · PPO · MBR-44821",
    detail: "Orthopedic MRI after 6 weeks conservative treatment. Surfaces imaging authorization criteria and comparable approved cases cleanly.",
  },
  {
    key: "B" as Scenario,
    label: "Scenario B",
    title: "Specialty Pharmacy — Biologic DMARD",
    subtitle: "Pharmacy · HMO · Step Therapy Exception",
    detail: "Adalimumab request after two DMARD failures. Demonstrates step therapy KB and how the system finds comparable exception-approved cases.",
  },
  {
    key: "C" as Scenario,
    label: "Scenario C",
    title: "Behavioral Health — Residential Treatment",
    subtitle: "Behavioral Health · PPO · Severe MDD",
    detail: "28-day residential request after two prior inpatient admissions. Complex multi-criteria case — illustrates PEND path and level-of-care guidelines.",
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
