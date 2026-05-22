import type { ClaimRecord } from "../types";

export interface SearchFilters {
  planType: string;
  state: string;
  outcome: string;
}

interface Props {
  claim: ClaimRecord;
  filters: SearchFilters;
  onFiltersChange: (f: SearchFilters) => void;
  loading: boolean;
  onSearch: (filters: Record<string, string | undefined>) => void;
  alreadyDone: boolean;
}

export default function SearchStep({ claim, filters, onFiltersChange, loading, onSearch, alreadyDone }: Props) {
  const { planType, state, outcome } = filters;

  function handleSearch() {
    onSearch({
      plan_type: planType || undefined,
      state: state || undefined,
      adjudication_outcome: outcome || undefined,
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
          Atlas Vector Search finds semantically relevant policies and prior cases
          while honoring the filters below as hard constraints — not hints.
        </p>

        {/* Filters */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 16, marginBottom: 14, alignItems: "flex-end" }}>
          <div>
            <label style={{ display: "block", fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 4 }}>
              plan_type
            </label>
            <select
              value={planType}
              onChange={(e) => onFiltersChange({ ...filters, planType: e.target.value })}
              style={filterStyle}
            >
              <option value="">Any</option>
              <option value="PPO">PPO</option>
              <option value="HMO">HMO</option>
              <option value="Medicare Advantage">Medicare Advantage</option>
            </select>
          </div>
          <div>
            <label style={{ display: "block", fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 4 }}>
              state
            </label>
            <select
              value={state}
              onChange={(e) => onFiltersChange({ ...filters, state: e.target.value })}
              style={filterStyle}
            >
              <option value="">Any</option>
              {["OH","TX","FL","IN","KY","TN","GA","NC","MI","WI","MN","IL","PA","NJ","WA","AZ","CO","CA","NY"].map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
          <div>
            <label style={{ display: "block", fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 4 }}>
              adjudication_outcome (prior claims)
            </label>
            <select
              value={outcome}
              onChange={(e) => onFiltersChange({ ...filters, outcome: e.target.value })}
              style={filterStyle}
            >
              <option value="">Any (approved + denied)</option>
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
          {" — numCandidates: 80, limit: 3 (policies), limit: 3 (prior claims), "}
          filter: {"{ plan_type: "}
          <code style={{ color: "var(--mdb-text)" }}>"{planType || "any"}"</code>
          {", state: "}
          <code style={{ color: "var(--mdb-text)" }}>"{state || "any"}"</code>
          {", adjudication_outcome: "}
          <code style={{ color: "var(--mdb-text)" }}>"{outcome || "any"}"</code>
          {" }"}
        </div>
      </div>
    </section>
  );
}
