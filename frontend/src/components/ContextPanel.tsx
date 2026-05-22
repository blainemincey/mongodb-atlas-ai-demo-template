import type { SearchResult, PolicyResult, PriorClaimResult } from "../types";

type Filters = SearchResult["query_filters_applied"];

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

function AutoScopePill({ value }: { value: string }) {
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
      background: "rgba(100,160,255,0.08)",
      border: "1px solid rgba(100,160,255,0.25)",
      color: "rgba(140,190,255,0.8)",
    }}>
      auto · clinical_area: {value}
    </span>
  );
}

function PolicyCard({ policy, rank, filters }: { policy: PolicyResult; rank: number; filters: Filters }) {
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
      <RankScore rank={rank} score={policy.vector_score} />

      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 6, minWidth: 0 }}>
        {/* Header */}
        <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
          <code style={{ fontSize: 12, color: "var(--mdb-green)", fontWeight: 600 }}>
            {policy.policy_id}
          </code>
        </div>

        <div style={{ fontSize: 13, fontWeight: 600, color: "var(--mdb-text)", lineHeight: 1.4 }}>
          {policy.title}
        </div>

        {/* Filter match pills */}
        <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
          <AutoScopePill value={policy.clinical_area} />
          <FilterPill
            label="subcategory"
            value={policy.subcategory}
            active={false}
          />
        </div>

        {/* Criteria excerpt */}
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
          {policy.criteria_text?.slice(0, 400)}
          {(policy.criteria_text?.length || 0) > 400 ? "..." : ""}
        </div>
      </div>
    </div>
  );
}

function PriorClaimCard({ claim, rank, filters }: { claim: PriorClaimResult; rank: number; filters: Filters }) {
  const borderColor = RANK_COLORS[rank - 1] ?? "var(--mdb-border)";
  const outcomeClass =
    claim.adjudication_outcome === "APPROVED" ? "badge-approved" :
    claim.adjudication_outcome === "DENIED" ? "badge-denied" : "badge-info";

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
      <RankScore rank={rank} score={claim.vector_score} />

      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 6, minWidth: 0 }}>
        {/* Header */}
        <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
          <code style={{ fontSize: 12, color: "var(--mdb-text)", fontWeight: 600 }}>
            {claim.claim_id}
          </code>
          <span className={`badge ${outcomeClass}`}>{claim.adjudication_outcome}</span>
        </div>

        {/* Diagnosis */}
        <div style={{ fontSize: 12, color: "var(--mdb-text)", lineHeight: 1.4 }}>
          {claim.primary_diagnosis_description}
        </div>

        {/* Filter match pills — green when this field was a hard filter constraint */}
        <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
          <FilterPill
            label="plan_type"
            value={claim.plan_type}
            active={!!filters.plan_type && filters.plan_type === claim.plan_type}
          />
          <FilterPill
            label="state"
            value={claim.state}
            active={!!filters.state && filters.state === claim.state}
          />
          {claim.service_date && (
            <FilterPill label="service_date" value={claim.service_date} active={false} />
          )}
          <FilterPill
            label="outcome"
            value={claim.adjudication_outcome}
            active={!!filters.adjudication_outcome && filters.adjudication_outcome === claim.adjudication_outcome}
          />
        </div>

        {/* Clinical note excerpt */}
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
          {claim.clinical_note?.slice(0, 280)}
          {(claim.clinical_note?.length || 0) > 280 ? "..." : ""}
        </div>
      </div>
    </div>
  );
}

export default function ContextPanel({ result }: { result: SearchResult }) {
  const { policies, prior_claims, query_filters_applied, meta } = result;

  // clinical_area is auto-inferred from the claim's procedure codes, not a user-set constraint
  const userFilters = { ...query_filters_applied, clinical_area: undefined };
  const activeFilterCount = Object.values(userFilters).filter(Boolean).length;

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
          {meta.policy_count} policies · {meta.prior_claim_count} prior claims · {meta.embedding_model}
        </span>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 8 }}>
          {query_filters_applied.clinical_area && (
            <span style={{
              fontSize: 11,
              color: "rgba(140,190,255,0.8)",
              background: "rgba(100,160,255,0.08)",
              border: "1px solid rgba(100,160,255,0.25)",
              borderRadius: 99,
              padding: "2px 10px",
            }}>
              auto-scoped: {query_filters_applied.clinical_area}
            </span>
          )}
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
          <span style={{ color: "var(--mdb-text-dim)" }}>= user hard filter</span>
          <span style={{
            display: "inline-flex", alignItems: "center", gap: 4,
            padding: "1px 7px", borderRadius: 99, fontSize: 10, fontWeight: 600,
            background: "rgba(100,160,255,0.08)", border: "1px solid rgba(100,160,255,0.25)",
            color: "rgba(140,190,255,0.8)",
          }}>
            auto · clinical_area: imaging
          </span>
          <span style={{ color: "var(--mdb-text-dim)" }}>= inferred from claim procedure codes</span>
        </div>

        {/* Policies */}
        <div>
          <p style={{ fontSize: 12, fontWeight: 600, marginBottom: 10, color: "var(--mdb-text)" }}>
            Coverage Policies{" "}
            <code style={{ fontSize: 10, color: "var(--mdb-text-dim)", fontWeight: 400 }}>
              healthcare_demo.policies
            </code>
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {policies.map((p, i) => (
              <PolicyCard key={p.policy_id} policy={p} rank={i + 1} filters={query_filters_applied} />
            ))}
          </div>
        </div>

        {/* Prior Claims */}
        <div>
          <p style={{ fontSize: 12, fontWeight: 600, marginBottom: 10, color: "var(--mdb-text)" }}>
            Comparable Prior Cases{" "}
            <code style={{ fontSize: 10, color: "var(--mdb-text-dim)", fontWeight: 400 }}>
              healthcare_demo.prior_claims
            </code>
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {prior_claims.map((c, i) => (
              <PriorClaimCard key={c.claim_id} claim={c} rank={i + 1} filters={query_filters_applied} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
