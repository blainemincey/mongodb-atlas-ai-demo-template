import { useState, useEffect, useRef } from "react";
import DocsModal from "./DocsModal";

type DocName = "readme" | "runbook" | "script";

const DOCS: { name: DocName; label: string }[] = [
  { name: "readme",  label: "README" },
  { name: "runbook", label: "Runbook" },
  { name: "script",  label: "Demo Script" },
];

interface Props {
  onReset?: () => void;
  resetEnabled?: boolean;
  resetting?: boolean;
  demoName?: string;
}

export default function Header({ onReset, resetEnabled = false, resetting = false, demoName = "Atlas AI Demo" }: Props) {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [activeDoc, setActiveDoc] = useState<DocName | null>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!dropdownOpen) return;
    const handler = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [dropdownOpen]);

  return (
    <>
      <header style={{
        background: "var(--bg)",
        borderBottom: "1px solid var(--border)",
        padding: "0 var(--space-5)",
        height: 56,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        position: "sticky",
        top: 0,
        zIndex: 100,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-4)" }}>
          <img
            src="/mongodb-leaf.svg"
            alt="MongoDB"
            width={110}
            height={28}
            style={{ display: "block", flexShrink: 0 }}
          />
          <div style={{ display: "flex", alignItems: "baseline", gap: "var(--space-3)" }}>
            <span style={{
              fontWeight: "var(--fw-semibold)",
              fontSize: "var(--fs-md)",
              color: "var(--text)",
              letterSpacing: "-0.01em",
            }}>
              {demoName}
            </span>
            <span style={{
              fontSize: "var(--fs-sm)",
              color: "var(--text-faint)",
            }}>
              Atlas · Voyage AI · Vector Search
            </span>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
          <span style={{
            fontSize: "var(--fs-xs)",
            color: "var(--text-muted)",
            padding: "3px 10px",
            border: "1px solid var(--border)",
            borderRadius: "var(--radius)",
          }}>
            One platform · Operational + AI
          </span>

          <div ref={dropdownRef} style={{ position: "relative" }}>
            <button
              className="btn-secondary"
              onClick={() => setDropdownOpen(o => !o)}
              style={{ fontSize: "var(--fs-xs)", padding: "5px 10px", display: "flex", alignItems: "center", gap: 6 }}
            >
              Docs
              <span style={{ fontSize: 9, opacity: 0.7 }}>{dropdownOpen ? "▲" : "▼"}</span>
            </button>

            {dropdownOpen && (
              <div style={{
                position: "absolute",
                top: "calc(100% + 6px)",
                right: 0,
                background: "var(--surface-raised)",
                border: "1px solid var(--border)",
                borderRadius: "var(--radius)",
                minWidth: 160,
                zIndex: 150,
                overflow: "hidden",
                boxShadow: "var(--shadow-md)",
              }}>
                {DOCS.map((d, i) => (
                  <button
                    key={d.name}
                    onClick={() => { setActiveDoc(d.name); setDropdownOpen(false); }}
                    style={{
                      display: "block",
                      width: "100%",
                      textAlign: "left",
                      background: "transparent",
                      border: "none",
                      borderBottom: i < DOCS.length - 1 ? "1px solid var(--border)" : "none",
                      borderRadius: 0,
                      padding: "10px 14px",
                      fontSize: "var(--fs-sm)",
                      fontWeight: 400,
                      color: "var(--text)",
                      cursor: "pointer",
                    }}
                    onMouseEnter={e => (e.currentTarget.style.background = "var(--surface)")}
                    onMouseLeave={e => (e.currentTarget.style.background = "transparent")}
                  >
                    {d.label}
                  </button>
                ))}
              </div>
            )}
          </div>

          {onReset && (
            <button
              className="btn-secondary"
              onClick={onReset}
              disabled={!resetEnabled || resetting}
              style={{ fontSize: "var(--fs-xs)", padding: "5px 12px", whiteSpace: "nowrap" }}
              title="Soft reset: clears AI output and restores PENDING status. Preserves embeddings."
            >
              {resetting ? "Resetting..." : "Reset Demo"}
            </button>
          )}
        </div>
      </header>

      <DocsModal doc={activeDoc} onClose={() => setActiveDoc(null)} />
    </>
  );
}
