import type { SearchResults, KnowledgeItem, HistoricalRecord } from "../types";

type Filters = SearchResults["query_filters_applied"];

const RANK_COLORS = ["#00ED64", "#00b84a", "#007a32"];

function RankScore({ rank, score }: { rank: number; score?: number }) {
  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      minWidth: 52,
      gap: 4,
      flexShrink: 0,
    }}>
      <span style={{
        fontSize: 18,
        fontWeight: 800,
        color: RANK_COLORS[rank - 1] ?? "var(--mdb-text-dim)",
        lineHeight: 1,
      }}>
        #{rank}
      </span>
      {score !== undefined && (
        <>
          <code style={{
            fontSize: 13,
            fontWeight: 700,
            color: RANK_COLORS[rank - 1] ?? "var(--mdb-text-dim)",
          }}>
            {score.toFixed(3)}
          </code>
          <div style={{ width: 36, height: 3, background: "var(--mdb-border)", borderRadius: 2 }}>
            <div style={{
              width: `${Math.round(score * 100)}%`,
              height: "100%",
              background: RANK_COLORS[rank - 1] ?? "var(--mdb-green)",
              borderRadius: 2,
            }} />
          </div>
          <span style={{ fontSize: 9, color: "var(--mdb-text-dim)", letterSpacing: "0.04em" }}>
            SIMILARITY
          </span>
        </>
      )}
    </div>
  );
}

function FilterPill({ label, value, active }: { label: string; value: string; active: boolean }) {
  return (
    <span style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 4,
      padding: "2px 7px",
      borderRadius: 99,
      fontSize: 10,
      fontWeight: 600,
      fontFamily: "Source Code Pro, monospace",
      background: active ? "rgba(0,237,100,0.12)" : "rgba(255,255,255,0.05)",
      border: `1px solid ${active ? "rgba(0,237,100,0.4)" : "var(--mdb-border)"}`,
      color: active ? "var(--mdb-green)" : "var(--mdb-text-dim)",
    }}>
      {active && <span style={{ fontSize: 9 }}>✓</span>}
      {label}: {value}
    </span>
  );
}

function KnowledgeItemCard({ item, rank, filters }: { item: KnowledgeItem; rank: number; filters: Filters }) {
  const borderColor = RANK_COLORS[rank - 1] ?? "var(--mdb-border)";
  return (
    <div style={{
      background: "rgba(0,0,0,0.2)",
      border: "1px solid var(--mdb-border)",
      borderLeft: `3px solid ${borderColor}`,
      borderRadius: "var(--radius)",
      padding: "12px 14px",
      display: "flex",
      gap: 14,
    }}>
      <RankScore rank={rank} score={item.vector_score} />

      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 6, minWidth: 0 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
          <code style={{ fontSize: 12, color: "var(--mdb-green)", fontWeight: 600 }}>
            {item.kb_id}
          </code>
        </div>

        <div style={{ fontSize: 13, fontWeight: 600, color: "var(--mdb-text)", lineHeight: 1.4 }}>
          {item.title}
        </div>

        <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
          <FilterPill
            label="category"
            value={item.category}
            active={!!filters.category && filters.category === item.category}
          />
          {item.subcategory && (
            <FilterPill
              label="subcategory"
              value={item.subcategory}
              active={false}
            />
          )}
        </div>

        <div style={{
          fontSize: 11,
          color: "var(--mdb-text-code)",
          lineHeight: 1.65,
          maxHeight: 90,
          overflowY: "auto",
          background: "rgba(0,0,0,0.2)",
          border: "1px solid var(--mdb-border)",
          borderRadius: "var(--radius)",
          padding: "6px 8px",
        }}>
          {item.content_text?.slice(0, 400)}
          {(item.content_text?.length || 0) > 400 ? "..." : ""}
        </div>
      </div>
    </div>
  );
}

function HistoricalRecordCard({ record, rank, filters }: { record: HistoricalRecord; rank: number; filters: Filters }) {
  const borderColor = RANK_COLORS[rank - 1] ?? "var(--mdb-border)";
  const outcomeClass =
    record.outcome === "APPROVED" ? "badge-approved" :
    record.outcome === "DENIED" ? "badge-denied" : "badge-info";

  return (
    <div style={{
      background: "rgba(0,0,0,0.2)",
      border: "1px solid var(--mdb-border)",
      borderLeft: `3px solid ${borderColor}`,
      borderRadius: "var(--radius)",
      padding: "12px 14px",
      display: "flex",
      gap: 14,
    }}>
      <RankScore rank={rank} score={record.vector_score} />

      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 6, minWidth: 0 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
          <code style={{ fontSize: 12, color: "var(--mdb-text)", fontWeight: 600 }}>
            {record.record_id}
          </code>
          <span className={`badge ${outcomeClass}`}>{record.outcome}</span>
        </div>

        <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
          <FilterPill
            label="category"
            value={record.category}
            active={!!filters.category && filters.category === record.category}
          />
          <FilterPill
            label="outcome"
            value={record.outcome}
            active={!!filters.outcome && filters.outcome === record.outcome}
          />
        </div>

        {record.outcome_rationale && (
          <div style={{ fontSize: 12, color: "var(--mdb-text)", lineHeight: 1.4 }}>
            {record.outcome_rationale}
          </div>
        )}

        {record.source_text && (
          <div style={{
            fontSize: 11,
            color: "var(--mdb-text-code)",
            lineHeight: 1.6,
            maxHeight: 72,
            overflowY: "auto",
            background: "rgba(0,0,0,0.2)",
            border: "1px solid var(--mdb-border)",
            borderRadius: "var(--radius)",
            padding: "6px 8px",
          }}>
            {record.source_text?.slice(0, 280)}
            {(record.source_text?.length || 0) > 280 ? "..." : ""}
          </div>
        )}
      </div>
    </div>
  );
}

export default function ContextPanel({ result }: { result: SearchResults }) {
  const { knowledge_base, historical_records, query_filters_applied, meta } = result;

  const activeFilterCount = Object.values(query_filters_applied).filter(Boolean).length;

  return (
    <section className="fade-in" style={{
      background: "var(--mdb-slate)",
      border: "1px solid var(--mdb-border)",
      borderRadius: "var(--radius-lg)",
      overflow: "hidden",
    }}>
      {/* Header */}
      <div style={{
        padding: "10px 18px",
        background: "rgba(255,255,255,0.03)",
        borderBottom: "1px solid var(--mdb-border)",
        display: "flex",
        alignItems: "center",
        gap: 10,
      }}>
        <span style={{
          width: 22, height: 22, borderRadius: "50%",
          background: "var(--mdb-green)",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 11, fontWeight: 700, color: "var(--mdb-dark)", flexShrink: 0,
        }}>✓</span>
        <span style={{ fontWeight: 600, fontSize: 13 }}>Retrieved Context</span>
        <span style={{ fontSize: 11, color: "var(--mdb-text-dim)" }}>
          {meta.knowledge_base_count} knowledge base · {meta.historical_records_count} historical records · {meta.embedding_model}
        </span>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 8 }}>
          {activeFilterCount > 0 && (
            <span style={{
              fontSize: 11,
              color: "var(--mdb-green)",
              background: "rgba(0,237,100,0.08)",
              border: "1px solid rgba(0,237,100,0.2)",
              borderRadius: 99,
              padding: "2px 10px",
            }}>
              {activeFilterCount} hard filter{activeFilterCount > 1 ? "s" : ""} applied
            </span>
          )}
        </div>
      </div>

      <div style={{ padding: "16px 18px", display: "flex", flexDirection: "column", gap: 24 }}>
        {/* Legend */}
        <div style={{
          display: "flex",
          alignItems: "center",
          gap: 16,
          fontSize: 11,
          color: "var(--mdb-text-dim)",
          flexWrap: "wrap",
        }}>
          <span>
            <span style={{
              display: "inline-block", width: 10, height: 10,
              borderRadius: 2, background: "var(--mdb-green)",
              marginRight: 5, verticalAlign: "middle",
            }} />
            Rank by semantic similarity
          </span>
          <span style={{
            display: "inline-flex", alignItems: "center", gap: 4,
            padding: "1px 7px", borderRadius: 99, fontSize: 10, fontWeight: 600,
            background: "rgba(0,237,100,0.12)", border: "1px solid rgba(0,237,100,0.4)",
            color: "var(--mdb-green)",
          }}>
            ✓ field: value
          </span>
          <span style={{ color: "var(--mdb-text-dim)" }}>= active hard filter</span>
        </div>

        {/* Knowledge Base */}
        <div>
          <p style={{ fontSize: 12, fontWeight: 600, marginBottom: 10, color: "var(--mdb-text)" }}>
            Knowledge Base Items{" "}
            <code style={{ fontSize: 10, color: "var(--mdb-text-dim)", fontWeight: 400 }}>
              demo_db.knowledge_base
            </code>
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {knowledge_base.map((item, i) => (
              <KnowledgeItemCard key={item.kb_id} item={item} rank={i + 1} filters={query_filters_applied} />
            ))}
          </div>
        </div>

        {/* Historical Records */}
        <div>
          <p style={{ fontSize: 12, fontWeight: 600, marginBottom: 10, color: "var(--mdb-text)" }}>
            Historical Records{" "}
            <code style={{ fontSize: 10, color: "var(--mdb-text-dim)", fontWeight: 400 }}>
              demo_db.historical_records
            </code>
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {historical_records.map((rec, i) => (
              <HistoricalRecordCard key={rec.record_id} record={rec} rank={i + 1} filters={query_filters_applied} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
