import type { RationaleResult } from "../types";

interface Props {
  result: RationaleResult | null;
  loading: boolean;
  onGenerate: () => void;
}

function determinationColor(det: string) {
  if (det.includes("APPROVE")) return "var(--mdb-green)";
  if (det.includes("DENY")) return "var(--mdb-error)";
  return "var(--mdb-warn)";
}

export default function RationalePanel({ result, loading, onGenerate }: Props) {
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
          <span style={{ fontWeight: 600, fontSize: 13 }}>AI Rationale + Write-back</span>
          <span style={{ fontSize: 11, color: "var(--mdb-text-dim)" }}>
            Template generates · MongoDB stores · claim updates in place
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
          ) : result ? "Regenerate" : "Generate Rationale"}
        </button>
      </div>

      <div style={{ padding: "14px 18px" }}>
        {!result && !loading && (
          <p style={{ color: "var(--mdb-text-dim)", fontSize: 13, lineHeight: 1.6 }}>
            Click <strong style={{ color: "var(--mdb-text)" }}>Generate Rationale</strong> to assemble a structured
            reviewer-voice recommendation grounded in the retrieved policy criteria and prior case analogues,
            then write it back into the same claim record.
            Watch the claim document above update in place — adjudication status, rationale, and timestamp
            all written to the same MongoDB document that held the operational data.
          </p>
        )}

        {loading && (
          <p style={{ color: "var(--mdb-text-dim)", fontSize: 13, display: "flex", alignItems: "center", gap: 8 }}>
            <span className="spinner" />
            Assembling grounded rationale from retrieved context · writing back to MongoDB...
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
              <span style={{ fontSize: 11, color: "var(--mdb-text-dim)" }}>AI Recommendation:</span>
              <span style={{
                fontSize: 14,
                fontWeight: 700,
                color: determinationColor(result.determination),
              }}>
                {result.determination}
              </span>
              <span style={{ fontSize: 11, color: "var(--mdb-text-dim)", marginLeft: "auto" }}>
                Draft · Human reviewer attestation required
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
                  Supporting Policies Written to Record
                </div>
                {result.supporting_policy_ids.map((id) => (
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
                  Comparable Cases Written to Record
                </div>
                {result.comparable_case_ids.map((id) => (
                  <code key={id} style={{ display: "block", fontSize: 12, color: "var(--mdb-green)" }}>{id}</code>
                ))}
              </div>
            </div>

            {/* Full rationale text */}
            <div>
              <p style={{ fontSize: 11, color: "var(--mdb-text-dim)", marginBottom: 6 }}>
                Full rationale (written to <code>claims.ai_rationale</code>):
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
                {result.rationale}
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
              The claim record above now reflects: <code style={{ color: "var(--mdb-text)" }}>adjudication_status: READY_FOR_REVIEW</code>,
              the full rationale text, supporting policy IDs, comparable case IDs, and an updated status history entry —
              all written back to the same MongoDB document that holds the operational data.
              Operational data, embeddings, retrieval, and AI output: one platform.
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
