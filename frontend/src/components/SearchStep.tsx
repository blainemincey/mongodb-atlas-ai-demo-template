import { useState } from "react";
import type { DemoRecord } from "../types";
import StepHelpPanel, { HelpButton, STEP_HELP } from "./StepHelp";

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

export default function SearchStep({ filters, onFiltersChange, loading, onSearch, alreadyDone }: Props) {
  const [helpOpen, setHelpOpen] = useState(false);
  const { category, outcome } = filters;

  function handleSearch() {
    onSearch({
      category: category || undefined,
      outcome: outcome || undefined,
    });
  }

  const selectStyle: React.CSSProperties = {
    background: "var(--surface-sunken)",
    border: "1px solid var(--border)",
    borderRadius: "var(--radius)",
    padding: "6px 10px",
    color: "var(--text)",
    fontSize: "var(--fs-sm)",
    fontFamily: "inherit",
    outline: "none",
    minWidth: 110,
  };

  return (
    <section className="panel">
      <div className="panel__header">
        <span className={`step-pill ${alreadyDone ? "step-pill--complete" : "step-pill--idle"}`}>
          {alreadyDone ? "✓" : "3"}
        </span>
        <span className="panel__title">Atlas Vector Search</span>
        <span className="panel__subtitle">Semantic similarity + hard metadata filters</span>
        <div className="panel__spacer" />
        <HelpButton open={helpOpen} onToggle={() => setHelpOpen(o => !o)} />
      </div>

      {helpOpen && <StepHelpPanel content={STEP_HELP[3]} />}

      <div className="panel__body">
        <p style={{
          fontSize: "var(--fs-sm)",
          color: "var(--text-muted)",
          marginBottom: "var(--space-3)",
          lineHeight: "var(--lh-base)",
        }}>
          Atlas Vector Search finds semantically relevant knowledge base items and historical records
          while honoring the filters below as hard constraints — not hints.
        </p>

        <div style={{
          display: "flex", flexWrap: "wrap", gap: "var(--space-4)",
          marginBottom: "var(--space-3)", alignItems: "flex-end",
        }}>
          <div>
            <label className="eyebrow" style={{ display: "block", marginBottom: 4 }}>category</label>
            <select
              value={category}
              onChange={(e) => onFiltersChange({ ...filters, category: e.target.value })}
              style={selectStyle}
            >
              <option value="">Any</option>
              {/* BEGIN_DOMAIN:category_options — replaced by scripts/init_domain.py */}
              <option value="hardware">Hardware</option>
              <option value="software">Software</option>
              <option value="network">Network</option>
              {/* END_DOMAIN:category_options */}
            </select>
          </div>
          <div>
            <label className="eyebrow" style={{ display: "block", marginBottom: 4 }}>outcome (historical records)</label>
            <select
              value={outcome}
              onChange={(e) => onFiltersChange({ ...filters, outcome: e.target.value })}
              style={selectStyle}
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
            style={{ minWidth: 140 }}
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
          background: "var(--surface-sunken)",
          border: "1px solid var(--border)",
          borderRadius: "var(--radius)",
          padding: "8px 12px",
          fontSize: "var(--fs-xs)",
          color: "var(--text-muted)",
          fontFamily: "Source Code Pro, monospace",
        }}>
          <span style={{ color: "var(--accent-mark)", fontWeight: 600 }}>$vectorSearch</span>
          {" — numCandidates: 80, limit: 3 (knowledge_base), limit: 3 (historical_records), "}
          filter: {"{ category: "}
          <span style={{ color: "var(--text)" }}>"{category || "any"}"</span>
          {", outcome: "}
          <span style={{ color: "var(--text)" }}>"{outcome || "any"}"</span>
          {" }"}
        </div>
      </div>
    </section>
  );
}
