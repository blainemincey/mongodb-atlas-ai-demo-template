import type { DemoRecord } from "../types";

function Field({ label, value, mono = false, highlight = false }: {
  label: string; value: React.ReactNode; mono?: boolean; highlight?: boolean;
}) {
  return (
    <div style={{
      display: "flex",
      gap: 8,
      padding: "5px 0",
      borderBottom: "1px solid rgba(255,255,255,0.04)",
      background: highlight ? "rgba(0,237,100,0.06)" : "transparent",
      transition: "background 0.4s",
    }}>
      <span style={{ minWidth: 220, fontSize: 11, color: "var(--mdb-text-dim)", flexShrink: 0 }}>
        {label}
      </span>
      <span style={{
        fontSize: 12,
        color: highlight ? "var(--mdb-green)" : "var(--mdb-text)",
        fontFamily: mono ? "Source Code Pro, monospace" : "inherit",
        wordBreak: "break-word",
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
  return <span className={`badge ${cls}`}>{status}</span>;
}

interface Props {
  record: DemoRecord;
  updated: boolean;
}

export default function RecordCard({ record, updated }: Props) {
  return (
    <section style={{
      background: "var(--mdb-slate)",
      border: "1px solid var(--mdb-border)",
      borderRadius: "var(--radius-lg)",
      overflow: "hidden",
    }}
    className={updated ? "highlight-update" : ""}
    >
      {/* Section header */}
      <div style={{
        padding: "10px 18px",
        background: "rgba(255,255,255,0.03)",
        borderBottom: "1px solid var(--mdb-border)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexWrap: "wrap",
        gap: 8,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{
            width: 8, height: 8, borderRadius: "50%",
            background: "var(--mdb-green)",
            display: "inline-block",
          }} />
          <span style={{ fontWeight: 600, fontSize: 13 }}>
            Record
          </span>
          <code style={{
            fontSize: 11,
            color: "var(--mdb-green)",
            background: "rgba(0,237,100,0.1)",
            padding: "1px 6px",
            borderRadius: 3,
          }}>
            demo_db.records
          </code>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <StatusBadge status={record.processing_status} />
          <span style={{ fontSize: 11, color: "var(--mdb-text-dim)" }}>
            {record.record_id}
          </span>
        </div>
      </div>

      <div style={{ padding: "14px 18px", display: "flex", flexDirection: "column", gap: 0 }}>
        {/* Processing status */}
        <p style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6 }}>
          Status
        </p>
        <Field label="processing_status" value={<StatusBadge status={record.processing_status} />} />
        <Field label="scenario" value={record.scenario} mono />

        {/* Embedding status */}
        <p style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6, marginTop: 14 }}>
          Voyage AI Embedding (stored in this document)
        </p>
        <Field label="record_embedding"
          value={
            record.record_embedding
              ? <span style={{ color: "var(--mdb-green)" }}>
                  {record.record_embedding} · model: {record.embedding_model}
                </span>
              : <span style={{ color: "var(--mdb-text-dim)" }}>null — not yet generated</span>
          }
        />
        <Field label="embedding_generated_at"
          value={record.embedding_generated_at || "null"}
          mono
        />

        {/* Record Text */}
        <p style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6, marginTop: 14 }}>
          Record Text (unstructured — embedded by Voyage AI)
        </p>
        <div style={{
          background: "rgba(0,0,0,0.25)",
          border: "1px solid var(--mdb-border)",
          borderRadius: "var(--radius)",
          padding: "10px 12px",
          maxHeight: 200,
          overflowY: "auto",
          fontSize: 11,
          lineHeight: 1.7,
          color: "var(--mdb-text-code)",
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
        }}>
          {record.record_text}
        </div>

        {/* AI Output (written back) */}
        {record.ai_output && (
          <>
            <p style={{ fontSize: 10, color: "var(--mdb-green)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6, marginTop: 14, fontWeight: 600 }}>
              AI Output (written back to this record)
            </p>
            <Field label="ai_determination" value={record.ai_determination || ""} highlight />
            <Field label="ai_output_generated_at" value={record.ai_output_generated_at || ""} mono />
            <Field label="ai_supporting_kb_ids" value={(record.ai_supporting_kb_ids || []).join(", ")} mono highlight />
            <Field label="ai_comparable_record_ids" value={(record.ai_comparable_record_ids || []).join(", ")} mono highlight />
          </>
        )}
      </div>
    </section>
  );
}
