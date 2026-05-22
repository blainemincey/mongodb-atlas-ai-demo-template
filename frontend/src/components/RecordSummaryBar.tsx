import type { DemoRecord, OutputResult } from "../types";

function Pill({ label, value, highlight = false }: {
  label: string; value: React.ReactNode; highlight?: boolean;
}) {
  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      gap: 2,
      padding: "6px 12px",
      borderRadius: "var(--radius)",
      background: highlight ? "rgba(0,237,100,0.08)" : "rgba(0,0,0,0.2)",
      border: `1px solid ${highlight ? "rgba(0,237,100,0.3)" : "var(--mdb-border)"}`,
      transition: "background 0.4s, border-color 0.4s",
    }}>
      <span style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.07em" }}>
        {label}
      </span>
      <span style={{
        fontSize: 12,
        fontWeight: 600,
        color: highlight ? "var(--mdb-green)" : "var(--mdb-text)",
        fontFamily: "Source Code Pro, monospace",
        whiteSpace: "nowrap",
      }}>
        {value}
      </span>
    </div>
  );
}

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
        background: "var(--mdb-slate)",
        border: `1px solid ${updated ? "rgba(0,237,100,0.4)" : "var(--mdb-border)"}`,
        borderRadius: "var(--radius-lg)",
        padding: "10px 16px",
        display: "flex",
        alignItems: "center",
        flexWrap: "wrap",
        gap: 10,
        transition: "border-color 0.4s",
      }}
    >
      {/* Identity */}
      <div style={{ display: "flex", flexDirection: "column", gap: 1, marginRight: 4 }}>
        <span style={{ fontSize: 11, color: "var(--mdb-text-dim)" }}>
          {current.record_id}
        </span>
        <span style={{ fontSize: 13, fontWeight: 600, color: "var(--mdb-text)", whiteSpace: "nowrap" }}>
          Scenario {current.scenario}
        </span>
      </div>

      <div style={{ width: 1, height: 40, background: "var(--mdb-border)", flexShrink: 0 }} />

      {/* Key indicators */}
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", flex: 1 }}>
        <Pill
          label="record_embedding"
          value={current.record_embedding ? "stored · 1024 dims" : "null"}
          highlight={!!current.record_embedding}
        />
        {current.ai_determination && (
          <Pill label="ai_determination" value={current.ai_determination} highlight />
        )}
      </div>

      {/* Status badge */}
      <div style={{
        marginLeft: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-end",
        gap: 3,
      }}>
        <span style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.07em" }}>
          processing_status
        </span>
        <StatusBadge status={current.processing_status} />
      </div>
    </div>
  );
}
