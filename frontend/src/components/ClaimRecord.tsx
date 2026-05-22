import type { ClaimRecord as ClaimType } from "../types";

function Field({ label, value, mono = false, highlight = false }: {
  label: string; value: React.ReactNode; mono?: boolean; highlight?: boolean;
}) {
  return (
    <div style={{
      display: "flex",
      gap: 8,
      padding: "5px 0",
      borderBottom: "1px solid rgba(255,255,255,0.04)",
      background: highlight ? "rgba(0,237,100,0.06)" : "transparent",
      transition: "background 0.4s",
    }}>
      <span style={{ minWidth: 220, fontSize: 11, color: "var(--mdb-text-dim)", flexShrink: 0 }}>
        {label}
      </span>
      <span style={{
        fontSize: 12,
        color: highlight ? "var(--mdb-green)" : "var(--mdb-text)",
        fontFamily: mono ? "Source Code Pro, monospace" : "inherit",
        wordBreak: "break-word",
      }}>
        {value}
      </span>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const cls =
    status === "PENDED" ? "badge-pended" :
    status === "READY_FOR_REVIEW" ? "badge-ready" :
    status === "APPROVED" ? "badge-approved" : "badge-info";
  return <span className={`badge ${cls}`}>{status}</span>;
}

interface Props {
  claim: ClaimType;
  updated: boolean;
}

export default function ClaimRecord({ claim, updated }: Props) {
  const procedures = claim.procedure_codes || [];

  return (
    <section style={{
      background: "var(--mdb-slate)",
      border: "1px solid var(--mdb-border)",
      borderRadius: "var(--radius-lg)",
      overflow: "hidden",
    }}
    className={updated ? "highlight-update" : ""}
    >
      {/* Section header */}
      <div style={{
        padding: "10px 18px",
        background: "rgba(255,255,255,0.03)",
        borderBottom: "1px solid var(--mdb-border)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexWrap: "wrap",
        gap: 8,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{
            width: 8, height: 8, borderRadius: "50%",
            background: "var(--mdb-green)",
            display: "inline-block",
          }} />
          <span style={{ fontWeight: 600, fontSize: 13 }}>
            Claim Record
          </span>
          <code style={{
            fontSize: 11,
            color: "var(--mdb-green)",
            background: "rgba(0,237,100,0.1)",
            padding: "1px 6px",
            borderRadius: 3,
          }}>
            healthcare_demo.claims
          </code>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <StatusBadge status={claim.adjudication_status} />
          <span style={{ fontSize: 11, color: "var(--mdb-text-dim)" }}>
            {claim.claim_id}
          </span>
        </div>
      </div>

      <div style={{ padding: "14px 18px", display: "flex", flexDirection: "column", gap: 0 }}>
        {/* Member + Plan */}
        <p style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6 }}>
          Member &amp; Plan
        </p>
        <Field label="member_name" value={claim.member_name} />
        <Field label="member_id" value={claim.member_id} mono />
        <Field label="plan_name" value={claim.plan_name} />
        <Field label="plan_type / state" value={`${claim.plan_type} · ${claim.state}`} />

        {/* Diagnosis */}
        <p style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6, marginTop: 14 }}>
          Diagnosis
        </p>
        <Field label="primary_diagnosis_code" value={claim.primary_diagnosis_code} mono />
        <Field label="primary_diagnosis_description" value={claim.primary_diagnosis_description} />

        {/* Procedures */}
        <p style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6, marginTop: 14 }}>
          Procedure Codes
        </p>
        {procedures.map((p) => (
          <Field key={p.code}
            label={`${p.type} ${p.code}`}
            value={`${p.description}${p.billed_amount ? ` · $${p.billed_amount.toLocaleString()}` : ""}`}
          />
        ))}

        <Field label="total_billed_amount"
          value={`$${(claim.total_billed_amount || 0).toLocaleString("en-US", { minimumFractionDigits: 2 })}`}
        />

        {/* Adjudication */}
        <p style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6, marginTop: 14 }}>
          Adjudication
        </p>
        <Field label="adjudication_status" value={<StatusBadge status={claim.adjudication_status} />} />
        <Field label="pend_reason_code" value={claim.pend_reason_code} mono />
        <Field label="pend_reason_description" value={claim.pend_reason_description} />

        {/* Embedding status */}
        <p style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6, marginTop: 14 }}>
          Voyage AI Embedding (stored in this document)
        </p>
        <Field label="clinical_embedding"
          value={
            claim.clinical_embedding
              ? <span style={{ color: "var(--mdb-green)" }}>
                  {claim.clinical_embedding} · model: {claim.embedding_model}
                </span>
              : <span style={{ color: "var(--mdb-text-dim)" }}>null — not yet generated</span>
          }
        />
        <Field label="embedding_generated_at"
          value={claim.embedding_generated_at || "null"}
          mono
        />

        {/* Clinical Notes */}
        <p style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6, marginTop: 14 }}>
          Clinical Notes (unstructured — embedded by Voyage AI)
        </p>
        <div style={{
          background: "rgba(0,0,0,0.25)",
          border: "1px solid var(--mdb-border)",
          borderRadius: "var(--radius)",
          padding: "10px 12px",
          maxHeight: 200,
          overflowY: "auto",
          fontSize: 11,
          lineHeight: 1.7,
          color: "var(--mdb-text-code)",
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
        }}>
          {claim.clinical_notes}
        </div>

        {/* AI Rationale (written back) */}
        {claim.ai_rationale && (
          <>
            <p style={{ fontSize: 10, color: "var(--mdb-green)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6, marginTop: 14, fontWeight: 600 }}>
              AI-Generated Rationale (written back to this record)
            </p>
            <Field label="ai_determination" value={claim.ai_determination || ""} highlight />
            <Field label="ai_rationale_generated_at" value={claim.ai_rationale_generated_at || ""} mono />
            <Field label="ai_supporting_policies" value={(claim.ai_supporting_policies || []).join(", ")} mono highlight />
            <Field label="ai_comparable_cases" value={(claim.ai_comparable_cases || []).join(", ")} mono highlight />
          </>
        )}

        {/* Status history */}
        {claim.status_history && claim.status_history.length > 0 && (
          <>
            <p style={{ fontSize: 10, color: "var(--mdb-text-dim)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6, marginTop: 14 }}>
              Status History
            </p>
            {claim.status_history.map((h, i) => (
              <Field key={i}
                label={h.timestamp?.slice(0, 19) || ""}
                value={`${h.status} — ${h.note}`}
                highlight={i === claim.status_history!.length - 1 && !!claim.ai_rationale}
              />
            ))}
          </>
        )}
      </div>
    </section>
  );
}
