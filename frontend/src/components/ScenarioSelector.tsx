import type { Scenario } from "../types";

const SCENARIOS = [
  {
    key: "A" as Scenario,
    label: "Scenario A",
    title: "MRI Prior Authorization",
    subtitle: "Lumbar Spine · CPT 72148",
    detail: "58-year-old male, PPO/OH. Pended for medical-necessity review. 14-week lumbar radiculopathy with conservative treatment history.",
    pend: "PA-MN-001",
  },
  {
    key: "B" as Scenario,
    label: "Scenario B",
    title: "Specialty Drug Infusion",
    subtitle: "Infliximab (Remicade) · HCPCS J1745",
    detail: "44-year-old female, PPO/TX. High-cost biologic ($18,420). Step-therapy compliance review triggered by adjudication engine.",
    pend: "MN-DRUG-HCB-002",
  },
  {
    key: "C" as Scenario,
    label: "Scenario C",
    title: "GLP-1 Prior Authorization",
    subtitle: "Semaglutide (Wegovy) 2.4mg · HCPCS S0148",
    detail: "52-year-old female, PPO/FL. Morbid obesity (BMI 38.2) with T2DM, hypertension, and sleep apnea. Pended for lifestyle program documentation.",
    pend: "PA-OBE-GLP1-001",
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
                  {" · "}
                  <span style={{ fontSize: 11, color: "var(--mdb-text-dim)" }}>Pend: {s.pend}</span>
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
