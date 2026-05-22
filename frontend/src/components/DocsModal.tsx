import { useState, useEffect, useCallback } from "react";
import { marked } from "marked";
import { api } from "../api";

type DocName = "readme" | "runbook" | "script";

interface Props {
  doc: DocName | null;
  onClose: () => void;
}

export default function DocsModal({ doc, onClose }: Props) {
  const [content, setContent] = useState<string | null>(null);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async (name: DocName) => {
    setLoading(true);
    setError(null);
    setContent(null);
    try {
      const res = await api.fetchDoc(name);
      setTitle(res.title);
      setContent(marked.parse(res.content) as string);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (doc) load(doc);
  }, [doc, load]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  if (!doc) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        onClick={onClose}
        style={{
          position: "fixed", inset: 0,
          background: "rgba(0,0,0,0.55)",
          zIndex: 200,
        }}
      />

      {/* Side panel */}
      <div style={{
        position: "fixed", top: 0, right: 0, bottom: 0,
        width: "min(780px, 90vw)",
        background: "var(--mdb-slate)",
        borderLeft: "1px solid var(--mdb-border)",
        zIndex: 201,
        display: "flex",
        flexDirection: "column",
      }}>
        {/* Header */}
        <div style={{
          display: "flex", alignItems: "center", justifyContent: "space-between",
          padding: "14px 20px",
          borderBottom: "1px solid var(--mdb-border)",
          background: "var(--mdb-dark)",
          flexShrink: 0,
        }}>
          <span style={{ fontWeight: 600, fontSize: 14, color: "var(--mdb-text)" }}>
            {title || "Loading…"}
          </span>
          <button
            onClick={onClose}
            style={{
              background: "transparent", border: "none", color: "var(--mdb-text-dim)",
              fontSize: 18, lineHeight: 1, padding: "2px 6px", cursor: "pointer",
            }}
            title="Close (Esc)"
          >
            ✕
          </button>
        </div>

        {/* Body */}
        <div style={{ flex: 1, overflowY: "auto", padding: "20px 28px" }}>
          {loading && (
            <div style={{ color: "var(--mdb-text-dim)", fontSize: 13 }}>Loading…</div>
          )}
          {error && (
            <div style={{ color: "var(--mdb-error)", fontSize: 13 }}>{error}</div>
          )}
          {content && (
            <div
              className="docs-content"
              dangerouslySetInnerHTML={{ __html: content }}
            />
          )}
        </div>
      </div>
    </>
  );
}
