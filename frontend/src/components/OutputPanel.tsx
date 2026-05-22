import type { OutputResult } from "../types";

interface Props {
  result: OutputResult | null;
  loading: boolean;
  onGenerate: () => void;
}

function determinationColor(det: string) {
  if (det.includes("APPROVE")) return "var(--mdb-green)";
  if (det.includes("DENY")) return "var(--mdb-error)";
  return "var(--mdb-warn)";
}

export default function OutputPanel({ result, loading, onGenerate }: Props) {
  return (
    <section style={{
      background: "var(--mdb-slate)",
      border: `1px solid ${result ? "var(--mdb-green)" : "var(--mdb-border)"}`,
      borderRadius: "var(--radius-lg)",
      overflow: "hidden",
      transition: "border-color 0.4s",
    }}>
      <div style={{
        padding: "10px 18px",
        background: result ? "rgba(0,237,100,0.08)" : "rgba(255,255,255,0.03)",
        borderBottom: "1px solid var(--mdb-border)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{
            width: 22, height: 22, borderRadius: "50%",
            background: result ? "var(--mdb-green)" : "var(--mdb-border)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 11, fontWeight: 700,
            color: result ? "var(--mdb-dark)" : "var(--mdb-text-dim)",
            flexShrink: 0,
          }}>
            {result ? "✓" : "5"}
          </span>
          <span style={{ fontWeight: 600, fontSize: 13 }}>AI Output + Write-back</span>
          <span style={{ fontSize: 11, color: "var(--mdb-text-dim)" }}>
            Template generates · MongoDB stores · record updates in place
          </span>
        </div>
        <button
          className={result ? "btn-secondary" : "btn-primary"}
          onClick={onGenerate}
          disabled={loading}
          style={{ minWidth: 160 }}
        >
          {loading ? (
            <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <span className="spinner" style={{ width: 14, height: 14 }} />
              Generating...
            </span>
          ) : result ? "Regenerate" : "Generate Output"}
        </button>
      </div>

      <div style={{ padding: "14px 18px" }}>
        {!result && !loading && (
          <p style={{ color: "var(--mdb-text-dim)", fontSize: 13, lineHeight: 1.6 }}>
            Click <strong style={{ color: "var(--mdb-text)" }}>Generate Output</strong> to assemble
            a structured AI output grounded in the retrieved knowledge base items and historical records,
            then write it back into the same record document.
            Watch the record above update in place — processing status, AI output, and timestamp
            all written to the same MongoDB document that held the operational data.
          </p>
        )}

        {loading && (
          <p style={{ color: "var(--mdb-text-dim)", fontSize: 13, display: "flex", alignItems: "center", gap: 8 }}>
            <span className="spinner" />
            Assembling output from retrieved context · writing back to MongoDB...
          </p>
        )}

        {result && (
          <div className="fade-in" style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            {/* Determination badge */}
            <div style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              padding: "10px 14px",
              background: "rgba(0,0,0,0.2)",
              border: "1px solid var(--mdb-border)",
              borderRadius: "var(--radius)",
            }}>
              <span style={{ fontSize: 11, color: "var(--mdb-text-dim)" }}>AI Determination:</span>
              <span style={{
                fontSize: 14,
                fontWeight: 700,
                color: determinationColor(result.determination),
              }}>
                {result.determination}
              </span>
              <span style={{ fontSize: 11, color: "var(--mdb-text-dim)", marginLeft: "auto" }}>
                Draft · Human review required
              </span>
            </div>

            {/* Supporting IDs */}
            <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
              <div style={{
                flex: 1, minWidth: 200,
                background: "rgba(0,237,100,0.06)",
                border: "1px solid rgba(0,237,100,0.2)",
                borderRadius: "var(--radius)",
                padding: "8px 12px",
              }}>
                <div style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 4 }}>
                  Supporting Knowledge Base IDs Written to Record
                </div>
                {result.supporting_kb_ids.map((id) => (
                  <code key={id} style={{ display: "block", fontSize: 12, color: "var(--mdb-green)" }}>{id}</code>
                ))}
              </div>
              <div style={{
                flex: 1, minWidth: 200,
                background: "rgba(0,237,100,0.06)",
                border: "1px solid rgba(0,237,100,0.2)",
                borderRadius: "var(--radius)",
                padding: "8px 12px",
              }}>
                <div style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 4 }}>
                  Comparable Record IDs Written to Record
                </div>
                {result.comparable_record_ids.map((id) => (
                  <code key={id} style={{ display: "block", fontSize: 12, color: "var(--mdb-green)" }}>{id}</code>
                ))}
              </div>
            </div>

            {/* Full output text */}
            <div>
              <p style={{ fontSize: 11, color: "var(--mdb-text-dim)", marginBottom: 6 }}>
                Full output (written to <code>records.ai_output</code>):
              </p>
              <div style={{
                background: "rgba(0,0,0,0.25)",
                border: "1px solid var(--mdb-border)",
                borderRadius: "var(--radius)",
                padding: "12px 14px",
                fontSize: 12,
                lineHeight: 1.8,
                color: "var(--mdb-text-code)",
                whiteSpace: "pre-wrap",
                wordBreak: "break-word",
                maxHeight: 480,
                overflowY: "auto",
              }}>
                {result.output}
              </div>
            </div>

            <div style={{
              padding: "8px 12px",
              background: "rgba(0,237,100,0.08)",
              border: "1px solid rgba(0,237,100,0.25)",
              borderRadius: "var(--radius)",
              fontSize: 12,
              color: "var(--mdb-text-dim)",
              lineHeight: 1.6,
            }}>
              <strong style={{ color: "var(--mdb-green)" }}>Write-back complete.</strong>{" "}
              The record above now reflects: <code style={{ color: "var(--mdb-text)" }}>processing_status: READY_FOR_REVIEW</code>,
              the full AI output, supporting KB IDs, comparable record IDs —
              all written back to the same MongoDB document that holds the operational data.
              Operational data, embeddings, retrieval, and AI output: one platform.
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
