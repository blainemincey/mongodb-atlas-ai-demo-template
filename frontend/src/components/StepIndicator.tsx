import type { Step } from "../types";

const STEPS: { n: Step; label: string }[] = [
  { n: 1, label: "Operational Record" },
  { n: 2, label: "Voyage Embedding" },
  { n: 3, label: "Vector Search" },
  { n: 4, label: "Retrieved Context" },
  { n: 5, label: "Rationale + Write-back" },
];

// Tab n is enabled when step progress has reached the unlock threshold.
// Steps 4 and 5 unlock together once search is complete (step >= 3).
function isEnabled(n: Step, step: Step): boolean {
  if (n <= 2) return step >= 1;
  if (n === 3) return step >= 2;
  return step >= 3; // tabs 4 and 5
}

function isComplete(n: Step, step: Step): boolean {
  if (n === 1) return false; // claim record is live, never "done"
  if (n === 4) return step >= 3;
  return step >= n;
}

interface Props {
  step: Step;
  activeTab: Step;
  onTabClick: (tab: Step) => void;
}

export default function StepTabs({ step, activeTab, onTabClick }: Props) {
  return (
    <div style={{
      display: "flex",
      borderBottom: "1px solid var(--mdb-border)",
      overflowX: "auto",
      gap: 0,
    }}>
      {STEPS.map((s) => {
        const enabled = isEnabled(s.n, step);
        const complete = isComplete(s.n, step);
        const active = activeTab === s.n;

        return (
          <button
            key={s.n}
            onClick={() => enabled && onTabClick(s.n)}
            disabled={!enabled}
            style={{
              background: "transparent",
              border: "none",
              borderBottom: active
                ? "2px solid var(--mdb-green)"
                : "2px solid transparent",
              borderRadius: 0,
              padding: "10px 16px",
              display: "flex",
              alignItems: "center",
              gap: 7,
              cursor: enabled ? "pointer" : "not-allowed",
              opacity: enabled ? 1 : 0.35,
              whiteSpace: "nowrap",
              transition: "border-color 0.15s, opacity 0.15s",
              flexShrink: 0,
            }}
          >
            {/* Step circle */}
            <span style={{
              width: 20, height: 20,
              borderRadius: "50%",
              background: complete
                ? "var(--mdb-green)"
                : active
                  ? "transparent"
                  : "var(--mdb-border)",
              border: active && !complete ? "2px solid var(--mdb-green)" : "none",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 10,
              fontWeight: 700,
              color: complete
                ? "var(--mdb-dark)"
                : active
                  ? "var(--mdb-green)"
                  : "var(--mdb-text-dim)",
              flexShrink: 0,
              transition: "background 0.2s",
            }}>
              {complete ? "✓" : s.n}
            </span>

            {/* Label */}
            <span style={{
              fontSize: 12,
              fontWeight: active ? 600 : 400,
              color: active
                ? "var(--mdb-text)"
                : complete
                  ? "var(--mdb-text-dim)"
                  : "var(--mdb-text-dim)",
            }}>
              {s.label}
            </span>
          </button>
        );
      })}
    </div>
  );
}
