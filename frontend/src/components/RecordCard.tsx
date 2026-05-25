import { useState } from "react";
import type { DemoRecord } from "../types";
import StepHelpPanel, { HelpButton, STEP_HELP } from "./StepHelp";

function Field({ label, value, mono = false, highlight = false }: {
  label: string; value: React.ReactNode; mono?: boolean; highlight?: boolean;
}) {
  const valueClass = `field-row__value${mono ? " field-row__value--mono" : ""}`;
  return (
    <div className={`field-row${highlight ? " field-row--highlight" : ""}`}>
      <span className="field-row__label">{label}</span>
      <span className={valueClass}>{value}</span>
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
  const [helpOpen, setHelpOpen] = useState(false);
  return (
    <section className={`panel ${updated ? "highlight-update" : ""}`}>
      <div className="panel__header">
        <span style={{
          width: 8, height: 8, borderRadius: "50%",
          background: "var(--brand)",
          display: "inline-block",
        }} />
        <span className="panel__title">Record</span>
        <code className="code-inline">demo_db.records</code>
        <div className="panel__spacer" />
        <StatusBadge status={record.processing_status} />
        <span className="panel__subtitle" style={{ fontFamily: "Source Code Pro, monospace" }}>
          {record.record_id}
        </span>
        <HelpButton open={helpOpen} onToggle={() => setHelpOpen(o => !o)} />
      </div>

      {helpOpen && <StepHelpPanel content={STEP_HELP[1]} />}

      <div className="panel__body" style={{ display: "flex", flexDirection: "column", gap: 0 }}>
        <p className="eyebrow" style={{ marginBottom: "var(--space-2)" }}>Status</p>
        <Field label="processing_status" value={<StatusBadge status={record.processing_status} />} />
        <Field label="scenario" value={record.scenario} mono />

        <p className="eyebrow" style={{ marginBottom: "var(--space-2)", marginTop: "var(--space-4)" }}>
          Voyage AI Embedding <code className="code-inline" style={{ marginLeft: 6 }}>stored in this document</code>
        </p>
        <Field
          label="record_embedding"
          value={
            record.record_embedding
              ? <span style={{ color: "var(--mist)" }}>
                  {record.record_embedding} · model: {record.embedding_model}
                </span>
              : <span style={{ color: "var(--text-faint)" }}>null — not yet generated</span>
          }
        />
        <Field
          label="embedding_generated_at"
          value={record.embedding_generated_at || "null"}
          mono
        />

        <p className="eyebrow" style={{ marginBottom: "var(--space-2)", marginTop: "var(--space-4)" }}>
          Record Text <span className="muted" style={{ textTransform: "none", letterSpacing: 0, fontWeight: 400 }}>— unstructured, embedded by Voyage AI</span>
        </p>
        <div style={{
          background: "var(--surface-sunken)",
          border: "1px solid var(--border)",
          borderRadius: "var(--radius)",
          padding: "var(--space-3) var(--space-3)",
          maxHeight: 200,
          overflowY: "auto",
          fontSize: "var(--fs-xs)",
          lineHeight: "var(--lh-loose)",
          color: "var(--text-code)",
          fontFamily: "Source Code Pro, monospace",
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
        }}>
          {record.record_text}
        </div>

        {record.ai_output && (
          <>
            <p className="eyebrow eyebrow--accent" style={{ marginBottom: "var(--space-2)", marginTop: "var(--space-4)" }}>
              AI Output — written back to this record
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
