import { useState } from "react";
import type { SearchResults, KnowledgeItem, HistoricalRecord } from "../types";
import StepHelpPanel, { HelpButton, STEP_HELP } from "./StepHelp";

type Filters = SearchResults["query_filters_applied"];

// Rank ramp readable on Slate Blue: Spring → mid → Forest
const RANK_COLORS = ["#00ED64", "#4FB57A", "#00684A"];

function RankScore({ rank, score }: { rank: number; score?: number }) {
  const color = RANK_COLORS[rank - 1] ?? "var(--text-faint)";
  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      minWidth: 54,
      gap: 4,
      flexShrink: 0,
    }}>
      <span style={{
        fontSize: 18,
        fontWeight: "var(--fw-bold)",
        color,
        lineHeight: 1,
      }}>
        #{rank}
      </span>
      {score !== undefined && (
        <>
          <code style={{ fontSize: "var(--fs-base)", fontWeight: "var(--fw-bold)", color }}>
            {score.toFixed(3)}
          </code>
          <div style={{
            width: 36, height: 3,
            background: "var(--border)",
            borderRadius: 2,
            overflow: "hidden",
          }}>
            <div style={{
              width: `${Math.round(score * 100)}%`,
              height: "100%",
              background: color,
              borderRadius: 2,
            }} />
          </div>
          <span style={{
            fontSize: 9,
            color: "var(--text-faint)",
            letterSpacing: "0.04em",
            textTransform: "uppercase",
          }}>
            similarity
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
      padding: "2px 8px",
      borderRadius: "var(--radius-pill)",
      fontSize: 10,
      fontWeight: "var(--fw-semibold)",
      fontFamily: "Source Code Pro, monospace",
      background: active ? "rgba(0,104,74,0.22)" : "rgba(255,255,255,0.04)",
      border: `1px solid ${active ? "var(--accent)" : "var(--border)"}`,
      color: active ? "var(--mist)" : "var(--text-faint)",
    }}>
      {active && <span style={{ fontSize: 9 }}>✓</span>}
      {label}: {value}
    </span>
  );
}

function ResultCard({ rank, children }: { rank: number; children: React.ReactNode }) {
  const borderColor = RANK_COLORS[rank - 1] ?? "var(--border)";
  return (
    <div style={{
      background: "var(--surface-sunken)",
      border: "1px solid var(--border)",
      borderLeft: `3px solid ${borderColor}`,
      borderRadius: "var(--radius)",
      padding: "var(--space-3) var(--space-4)",
      display: "flex",
      gap: "var(--space-4)",
    }}>
      {children}
    </div>
  );
}

function KnowledgeItemCard({ item, rank, filters }: { item: KnowledgeItem; rank: number; filters: Filters }) {
  return (
    <ResultCard rank={rank}>
      <RankScore rank={rank} score={item.vector_score} />
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 6, minWidth: 0 }}>
        <code style={{
          fontSize: "var(--fs-sm)",
          color: "var(--accent-mark)",
          fontWeight: "var(--fw-semibold)",
        }}>
          {item.kb_id}
        </code>
        <div style={{
          fontSize: "var(--fs-base)",
          fontWeight: "var(--fw-semibold)",
          color: "var(--text)",
          lineHeight: "var(--lh-tight)",
        }}>
          {item.title}
        </div>
        <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
          <FilterPill
            label="category"
            value={item.category}
            active={!!filters.category && filters.category === item.category}
          />
          {item.subcategory && (
            <FilterPill label="subcategory" value={item.subcategory} active={false} />
          )}
        </div>
        <div style={{
          fontSize: "var(--fs-xs)",
          color: "var(--text-code)",
          lineHeight: "var(--lh-base)",
          maxHeight: 90,
          overflowY: "auto",
          background: "rgba(0,0,0,0.25)",
          border: "1px solid var(--border)",
          borderRadius: "var(--radius)",
          padding: "6px 10px",
        }}>
          {item.content_text?.slice(0, 400)}
          {(item.content_text?.length || 0) > 400 ? "..." : ""}
        </div>
      </div>
    </ResultCard>
  );
}

function HistoricalRecordCard({ record, rank, filters }: { record: HistoricalRecord; rank: number; filters: Filters }) {
  const outcomeClass =
    record.outcome === "APPROVED" ? "badge-approved" :
    record.outcome === "DENIED"   ? "badge-denied"   : "badge-info";

  return (
    <ResultCard rank={rank}>
      <RankScore rank={rank} score={record.vector_score} />
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 6, minWidth: 0 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
          <code style={{
            fontSize: "var(--fs-sm)",
            color: "var(--text)",
            fontWeight: "var(--fw-semibold)",
          }}>
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
          <div style={{
            fontSize: "var(--fs-sm)",
            color: "var(--text)",
            lineHeight: "var(--lh-tight)",
          }}>
            {record.outcome_rationale}
          </div>
        )}
        {record.source_text && (
          <div style={{
            fontSize: "var(--fs-xs)",
            color: "var(--text-code)",
            lineHeight: "var(--lh-base)",
            maxHeight: 72,
            overflowY: "auto",
            background: "rgba(0,0,0,0.25)",
            border: "1px solid var(--border)",
            borderRadius: "var(--radius)",
            padding: "6px 10px",
          }}>
            {record.source_text?.slice(0, 280)}
            {(record.source_text?.length || 0) > 280 ? "..." : ""}
          </div>
        )}
      </div>
    </ResultCard>
  );
}

function SectionHeader({ title, collection }: { title: string; collection: string }) {
  return (
    <div style={{
      display: "flex",
      alignItems: "center",
      gap: "var(--space-2)",
      marginBottom: "var(--space-3)",
      paddingLeft: "var(--space-3)",
      borderLeft: "2px solid var(--accent)",
    }}>
      <span style={{
        fontSize: "var(--fs-sm)",
        fontWeight: "var(--fw-semibold)",
        color: "var(--text)",
      }}>
        {title}
      </span>
      <code className="code-inline" style={{ fontSize: 10 }}>{collection}</code>
    </div>
  );
}

export default function ContextPanel({ result }: { result: SearchResults }) {
  const [helpOpen, setHelpOpen] = useState(false);
  const { knowledge_base, historical_records, query_filters_applied, meta } = result;
  const activeFilterCount = Object.values(query_filters_applied).filter(Boolean).length;

  return (
    <section className="panel panel--retrieved fade-in">
      <div className="panel__header">
        <span className="step-pill step-pill--complete">✓</span>
        <span className="panel__title">Retrieved Context</span>
        <span className="panel__subtitle">
          {meta.knowledge_base_count} knowledge base · {meta.historical_records_count} historical records · {meta.embedding_model}
        </span>
        <div className="panel__spacer" />
        {activeFilterCount > 0 && (
          <span style={{
            fontSize: "var(--fs-xs)",
            color: "var(--mist)",
            background: "rgba(0,104,74,0.22)",
            border: "1px solid var(--accent)",
            borderRadius: "var(--radius-pill)",
            padding: "2px 10px",
            fontWeight: "var(--fw-semibold)",
          }}>
            {activeFilterCount} hard filter{activeFilterCount > 1 ? "s" : ""} applied
          </span>
        )}
        <HelpButton open={helpOpen} onToggle={() => setHelpOpen(o => !o)} />
      </div>

      {helpOpen && <StepHelpPanel content={STEP_HELP[4]} />}

      <div className="panel__body" style={{ display: "flex", flexDirection: "column", gap: "var(--space-5)" }}>
        <div style={{
          display: "flex",
          alignItems: "center",
          gap: "var(--space-4)",
          fontSize: "var(--fs-xs)",
          color: "var(--text-faint)",
          flexWrap: "wrap",
        }}>
          <span>
            <span style={{
              display: "inline-block", width: 10, height: 10,
              borderRadius: 2, background: RANK_COLORS[0],
              marginRight: 5, verticalAlign: "middle",
            }} />
            Rank by semantic similarity
          </span>
          <span style={{
            display: "inline-flex", alignItems: "center", gap: 4,
            padding: "1px 8px", borderRadius: "var(--radius-pill)",
            fontSize: 10, fontWeight: "var(--fw-semibold)",
            background: "rgba(0,104,74,0.22)", border: "1px solid var(--accent)",
            color: "var(--mist)",
          }}>
            ✓ field: value
          </span>
          <span>= active hard filter</span>
        </div>

        <div>
          <SectionHeader title="Knowledge Base Items" collection="demo_db.knowledge_base" />
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
            {knowledge_base.map((item, i) => (
              <KnowledgeItemCard key={item.kb_id} item={item} rank={i + 1} filters={query_filters_applied} />
            ))}
          </div>
        </div>

        <div>
          <SectionHeader title="Historical Records" collection="demo_db.historical_records" />
          <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-2)" }}>
            {historical_records.map((rec, i) => (
              <HistoricalRecordCard key={rec.record_id} record={rec} rank={i + 1} filters={query_filters_applied} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
