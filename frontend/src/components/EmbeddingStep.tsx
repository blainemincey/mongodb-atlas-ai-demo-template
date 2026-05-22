import type { EmbeddingResult } from "../types";

interface Props {
  embedding: EmbeddingResult | null;
  loading: boolean;
  onEmbed: () => void;
  alreadyDone: boolean;
}

export default function EmbeddingStep({ embedding, loading, onEmbed, alreadyDone }: Props) {
  return (
    <section style={{
      background: "var(--mdb-slate)",
      border: "1px solid var(--mdb-border)",
      borderRadius: "var(--radius-lg)",
      overflow: "hidden",
    }}>
      <div style={{
        padding: "10px 18px",
        background: "rgba(255,255,255,0.03)",
        borderBottom: "1px solid var(--mdb-border)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{
            width: 22, height: 22,
            borderRadius: "50%",
            background: embedding ? "var(--mdb-green)" : "var(--mdb-border)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 11, fontWeight: 700,
            color: embedding ? "var(--mdb-dark)" : "var(--mdb-text-dim)",
            flexShrink: 0,
          }}>
            {embedding ? "✓" : "2"}
          </span>
          <span style={{ fontWeight: 600, fontSize: 13 }}>Voyage AI Embedding</span>
          <span style={{ fontSize: 11, color: "var(--mdb-text-dim)" }}>voyage-3 · 1024 dims · stored in MongoDB</span>
        </div>
        <button
          className={embedding ? "btn-secondary" : "btn-primary"}
          onClick={onEmbed}
          disabled={loading || (alreadyDone && !!embedding)}
          style={{ minWidth: 140 }}
        >
          {loading && !embedding ? (
            <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <span className="spinner" style={{ width: 14, height: 14 }} />
              Embedding...
            </span>
          ) : embedding ? "Re-embed" : "Generate Embedding"}
        </button>
      </div>

      <div style={{ padding: "14px 18px" }}>
        {!embedding && !loading && (
          <p style={{ color: "var(--mdb-text-dim)", fontSize: 13 }}>
            Click <strong style={{ color: "var(--mdb-text)" }}>Generate Embedding</strong> to have Voyage AI embed the clinical notes
            and write the vector directly into this MongoDB document — no separate vector store.
          </p>
        )}

        {loading && !embedding && (
          <p style={{ color: "var(--mdb-text-dim)", fontSize: 13, display: "flex", alignItems: "center", gap: 8 }}>
            <span className="spinner" />
            Calling Voyage AI voyage-3 · writing vector to MongoDB document...
          </p>
        )}

        {embedding && (
          <div className="fade-in" style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {/* Key stats */}
            <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
              {[
                { label: "Embedding Model", value: embedding.embedding_model },
                { label: "Dimensions", value: embedding.embedding_dimensions.toLocaleString() },
                { label: "Storage", value: "MongoDB document" },
                { label: "Generated", value: embedding.generated_at?.slice(0, 19).replace("T", " ") + " UTC" },
              ].map((item) => (
                <div key={item.label} style={{
                  flex: 1,
                  minWidth: 150,
                  background: "rgba(0,0,0,0.2)",
                  border: "1px solid var(--mdb-border)",
                  borderRadius: "var(--radius)",
                  padding: "8px 12px",
                }}>
                  <div style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.07em" }}>
                    {item.label}
                  </div>
                  <div style={{ fontSize: 13, fontWeight: 600, color: "var(--mdb-green)", marginTop: 2 }}>
                    {item.value}
                  </div>
                </div>
              ))}
            </div>

            {/* Vector preview */}
            <div>
              <p style={{ fontSize: 11, color: "var(--mdb-text-dim)", marginBottom: 4 }}>
                Vector preview (first 8 of 1,024 dimensions):
              </p>
              <code style={{
                display: "block",
                background: "rgba(0,0,0,0.25)",
                border: "1px solid var(--mdb-border)",
                borderRadius: "var(--radius)",
                padding: "8px 12px",
                color: "var(--mdb-green)",
                fontSize: 11,
                letterSpacing: "0.03em",
              }}>
                [{embedding.embedding_preview.map((v) => v.toFixed(6)).join(", ")}, ...]
              </code>
            </div>

            <p style={{
              fontSize: 12,
              color: "var(--mdb-text-dim)",
              borderLeft: "2px solid var(--mdb-green)",
              paddingLeft: 10,
              lineHeight: 1.6,
            }}>
              {embedding.message}
            </p>
          </div>
        )}
      </div>
    </section>
  );
}
