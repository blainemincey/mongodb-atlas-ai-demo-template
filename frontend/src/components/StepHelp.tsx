export interface HelpContent {
  what: string;
  why: string;
  technical: string;
}

// Talking points for each demo step — edit here to tune presenter guidance.
export const STEP_HELP: Record<number, HelpContent> = {
  1: {
    what: "MongoDB stores this record as a native document with schema-flexible fields: structured metadata, an unstructured text blob, and the AI fields that will be added next — all in the same collection, no preprocessing or staging layer required.",
    why: "Traditional AI pipelines start with an ETL step: copy data out of the operational database, transform it, and load it into a separate AI processing system. That copy introduces sync lag and a second data tier to operate. Here, the operational record is the AI input — in place, from day one.",
    technical: "The record_embedding and ai_output fields don't exist on this document yet. MongoDB's document model lets you add them in the next two steps using the same update_one call you'd use for any other field — no schema migrations, no new collections.",
  },
  2: {
    what: "Voyage AI's voyage-3 model converts the record text into a 1,024-dimensional vector, which is written directly into this MongoDB document as record_embedding — alongside the operational data, in the same collection, using the same driver connection.",
    why: "Dedicated vector stores require a sync mechanism: when the source record changes, the vector must be regenerated and re-synced to an external system. Co-locating the embedding in the document makes the record self-contained and eliminates that operational burden entirely.",
    technical: "Storing the embedding once at write time means Voyage AI is called exactly once per record. Every subsequent vector search reuses the stored vector — no per-query API calls, no rate-limit exposure at scale. Same text always produces the same vector.",
  },
  3: {
    what: "Atlas Vector Search runs a $vectorSearch aggregation stage against two collections simultaneously — knowledge base and historical records — returning semantically relevant documents ranked by cosine similarity, all within the same MongoDB cluster and driver connection.",
    why: "Dedicated vector databases require a separate service call, a separate connection, and a join back to the operational database to retrieve full document context. Atlas Vector Search is a stage in an aggregation pipeline: no round-trip to a separate service, no external dependency at query time.",
    technical: "The filters here are pre-filters — Atlas eliminates non-matching documents before scoring any vectors. Scoring runs only over the qualifying subset. This is a hard constraint enforced by the index, not a hint: a document that fails the filter never appears in results regardless of its similarity score.",
  },
  4: {
    what: "These are the top matches from the knowledge base and historical records collections, ranked by cosine similarity to the embedded record. They form the grounding context the output step uses to generate a reasoned, sourced response.",
    why: "In a typical RAG setup, vector results come from a separate store and require a secondary lookup to retrieve full document context. Here the knowledge base and historical records are MongoDB collections — fetched in the same pipeline, no cross-system join, no cache-consistency risk.",
    technical: "Similarity scores reflect cosine distance in 1,024-dimensional space — semantic meaning, not keyword overlap. A score above ~0.80 indicates strong thematic alignment with the record text. Active filter pills show which documents satisfied the hard constraints set in Step 3.",
  },
  5: {
    what: "Assembles a structured output grounded in the retrieved context, then writes it back to the original record in a single update_one call — updating processing_status, ai_output, ai_determination, and the reference IDs that link the output to its source material.",
    why: "AI pipelines that store results in a separate table or external system require joins to reconstruct the full decision context. Here the entire audit trail — operational fields, embedding metadata, AI determination, and the specific documents that supported it — lives in one MongoDB document.",
    technical: "The ai_supporting_kb_ids and ai_comparable_record_ids fields store the exact IDs of the documents retrieved in Steps 3–4. Any downstream system or auditor querying this record gets the complete picture in a single document fetch — what the record said, what was retrieved, and what the AI concluded.",
  },
};

interface ButtonProps {
  open: boolean;
  onToggle: () => void;
}

export function HelpButton({ open, onToggle }: ButtonProps) {
  return (
    <button
      onClick={onToggle}
      title={open ? "Close help" : "What MongoDB Atlas does here"}
      style={{
        width: 22,
        height: 22,
        borderRadius: "50%",
        background: open ? "var(--accent)" : "var(--surface-sunken)",
        border: `1px solid ${open ? "var(--accent)" : "var(--border-strong)"}`,
        color: open ? "var(--mist)" : "var(--text-muted)",
        fontSize: "var(--fs-xs)",
        fontWeight: "var(--fw-bold)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: 0,
        flexShrink: 0,
        transition: "all 0.15s",
      }}
    >
      ?
    </button>
  );
}

interface PanelProps {
  content: HelpContent;
}

export default function StepHelpPanel({ content }: PanelProps) {
  return (
    <div
      className="fade-in"
      style={{
        padding: "var(--space-3) var(--space-4) var(--space-4)",
        background: "var(--surface-raised)",
        borderBottom: "1px solid var(--border)",
        display: "flex",
        flexDirection: "column",
        gap: "var(--space-3)",
      }}
    >
      <Row
        label="What MongoDB Atlas does here"
        text={content.what}
        labelClass="eyebrow eyebrow--accent"
        textColor="var(--text)"
      />
      <Row
        label="Why it matters"
        text={content.why}
        labelClass="eyebrow"
        textColor="var(--text)"
        accent
      />
      <Row
        label="Technical detail"
        text={content.technical}
        labelClass="eyebrow"
        textColor="var(--text-muted)"
      />
    </div>
  );
}

function Row({
  label,
  text,
  labelClass,
  textColor,
  accent = false,
}: {
  label: string;
  text: string;
  labelClass: string;
  textColor: string;
  accent?: boolean;
}) {
  return (
    <div style={{
      borderLeft: accent ? "2px solid var(--accent)" : "2px solid transparent",
      paddingLeft: accent ? "var(--space-3)" : 0,
    }}>
      <p className={labelClass} style={{ marginBottom: 3 }}>
        {label}
      </p>
      <p style={{
        fontSize: "var(--fs-sm)",
        color: textColor,
        lineHeight: "var(--lh-base)",
        margin: 0,
      }}>
        {text}
      </p>
    </div>
  );
}
