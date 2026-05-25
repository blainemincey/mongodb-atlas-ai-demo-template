import type { DemoRecord, OutputResult } from "../types";

function StatusBadge({ status }: { status: string }) {
  const cls =
    status === "PENDING" ? "badge-pended" :
    status === "READY_FOR_REVIEW" ? "badge-ready" :
    status === "APPROVED" ? "badge-approved" : "badge-info";
  return <span className={`badge ${cls}`}>{status.replace(/_/g, " ")}</span>;
}

interface Props {
  record: DemoRecord;
  output: OutputResult | null;
}

export default function RecordSummaryBar({ record, output }: Props) {
  const current = output ? output.updated_record : record;
  const updated = !!output;

  return (
    <div
      className={updated ? "highlight-update" : ""}
      style={{
        background: "var(--surface)",
        border: `1px solid ${updated ? "var(--success-border)" : "var(--border)"}`,
        borderRadius: "var(--radius-lg)",
        padding: "var(--space-3) var(--space-4)",
        display: "flex",
        alignItems: "center",
        flexWrap: "wrap",
        gap: "var(--space-3)",
        boxShadow: "var(--shadow-sm)",
        transition: "border-color 0.4s",
      }}
    >
      <div style={{ display: "flex", flexDirection: "column", gap: 1, marginRight: 4 }}>
        <span style={{ fontSize: "var(--fs-xs)", color: "var(--text-faint)" }}>
          {current.record_id}
        </span>
        <span style={{
          fontSize: "var(--fs-base)",
          fontWeight: "var(--fw-semibold)",
          color: "var(--text)",
          whiteSpace: "nowrap",
        }}>
          Scenario {current.scenario}
        </span>
      </div>

      <div style={{ width: 1, height: 36, background: "var(--border)", flexShrink: 0 }} />

      <div style={{ display: "flex", gap: "var(--space-2)", flexWrap: "wrap", flex: 1 }}>
        <div className={`kv-tile ${current.record_embedding ? "kv-tile--accent" : ""}`}>
          <span className="kv-tile__label">record_embedding</span>
          <span className="kv-tile__value">
            {current.record_embedding ? "stored · 1024 dims" : "null"}
          </span>
        </div>
        {current.ai_determination && (
          <div className="kv-tile kv-tile--accent">
            <span className="kv-tile__label">ai_determination</span>
            <span className="kv-tile__value">{current.ai_determination}</span>
          </div>
        )}
      </div>

      <div style={{
        marginLeft: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-end",
        gap: 3,
      }}>
        <span className="eyebrow">processing_status</span>
        <StatusBadge status={current.processing_status} />
      </div>
    </div>
  );
}
