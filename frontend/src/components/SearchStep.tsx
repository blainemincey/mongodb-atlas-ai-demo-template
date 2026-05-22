import type { DemoRecord } from "../types";

export interface SearchFilters {
  category: string;
  outcome: string;
}

interface Props {
  record: DemoRecord;
  filters: SearchFilters;
  onFiltersChange: (f: SearchFilters) => void;
  loading: boolean;
  onSearch: (filters: Record<string, string | undefined>) => void;
  alreadyDone: boolean;
}

export default function SearchStep({ record, filters, onFiltersChange, loading, onSearch, alreadyDone }: Props) {
  const { category, outcome } = filters;

  function handleSearch() {
    onSearch({
      category: category || undefined,
      outcome: outcome || undefined,
    });
  }

  const filterStyle: React.CSSProperties = {
    background: "rgba(0,0,0,0.2)",
    border: "1px solid var(--mdb-border)",
    borderRadius: "var(--radius)",
    padding: "5px 10px",
    color: "var(--mdb-text)",
    fontSize: 12,
    fontFamily: "inherit",
    outline: "none",
    minWidth: 100,
  };

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
        gap: 10,
      }}>
        <span style={{
          width: 22, height: 22,
          borderRadius: "50%",
          background: alreadyDone ? "var(--mdb-green)" : "var(--mdb-border)",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 11, fontWeight: 700,
          color: alreadyDone ? "var(--mdb-dark)" : "var(--mdb-text-dim)",
          flexShrink: 0,
        }}>
          {alreadyDone ? "✓" : "3"}
        </span>
        <span style={{ fontWeight: 600, fontSize: 13 }}>Atlas Vector Search</span>
        <span style={{ fontSize: 11, color: "var(--mdb-text-dim)" }}>
          Semantic similarity + hard metadata filters
        </span>
      </div>

      <div style={{ padding: "14px 18px" }}>
        <p style={{ fontSize: 12, color: "var(--mdb-text-dim)", marginBottom: 12, lineHeight: 1.6 }}>
          Atlas Vector Search finds semantically relevant knowledge base items and historical records
          while honoring the filters below as hard constraints — not hints.
        </p>

        {/* Filters */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 16, marginBottom: 14, alignItems: "flex-end" }}>
          <div>
            <label style={{ display: "block", fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 4 }}>
              category
            </label>
            <select
              value={category}
              onChange={(e) => onFiltersChange({ ...filters, category: e.target.value })}
              style={filterStyle}
            >
              <option value="">Any</option>
              {/* TODO: Replace these options with domain-specific categories */}
              <option value="general">General</option>
            </select>
          </div>
          <div>
            <label style={{ display: "block", fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 4 }}>
              outcome (historical records)
            </label>
            <select
              value={outcome}
              onChange={(e) => onFiltersChange({ ...filters, outcome: e.target.value })}
              style={filterStyle}
            >
              <option value="">Any</option>
              <option value="APPROVED">APPROVED only</option>
              <option value="DENIED">DENIED only</option>
            </select>
          </div>
          <button
            className="btn-primary"
            onClick={handleSearch}
            disabled={loading}
            style={{ minWidth: 120 }}
          >
            {loading ? (
              <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span className="spinner" style={{ width: 14, height: 14 }} />
                Searching...
              </span>
            ) : alreadyDone ? "Re-run Search" : "Run Vector Search"}
          </button>
        </div>

        <div style={{
          background: "rgba(0,0,0,0.2)",
          border: "1px solid var(--mdb-border)",
          borderRadius: "var(--radius)",
          padding: "8px 12px",
          fontSize: 11,
          color: "var(--mdb-text-dim)",
        }}>
          <code style={{ color: "var(--mdb-green)" }}>$vectorSearch</code>
          {" — numCandidates: 80, limit: 3 (knowledge_base), limit: 3 (historical_records), "}
          filter: {"{ category: "}
          <code style={{ color: "var(--mdb-text)" }}>"{category || "any"}"</code>
          {", outcome: "}
          <code style={{ color: "var(--mdb-text)" }}>"{outcome || "any"}"</code>
          {" }"}
        </div>
      </div>
    </section>
  );
}
