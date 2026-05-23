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
        background: "var(--mdb-dark)",
        borderBottom: "1px solid var(--mdb-border)",
        padding: "0 24px",
        height: 56,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        position: "sticky",
        top: 0,
        zIndex: 100,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          {/* MongoDB leaf logo */}
          <svg width="28" height="28" viewBox="0 0 256 549" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M136.03 0C136.03 0 71.02 66.47 71.02 274.28c0 134.01 63.02 189.9 63.02 189.9l5.97 6.07V0h-3.98z" fill="#00ED64"/>
            <path d="M141.77 464.25s63.22-55.91 63.22-189.97C204.99 66.47 141.77 0 141.77 0h-3.75v470.25l3.75-6z" fill="#00684A"/>
            <path d="M138.02 470.25l-5.97-6.07c-2.41 1.91-4.97 3.86-4.97 3.86L138.02 549l10.97-80.69s-2.55-1.95-4.97-3.86l-5.97 6.07-.03-.27z" fill="#00ED64"/>
          </svg>
          <div>
            <span style={{
              fontWeight: 600,
              fontSize: 15,
              color: "var(--mdb-text)",
              letterSpacing: "-0.02em",
            }}>
              MongoDB Atlas
            </span>
            <span style={{
              marginLeft: 10,
              fontSize: 12,
              color: "var(--mdb-text-dim)",
            }}>
              {demoName} · Voyage AI + Vector Search
            </span>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{
            fontSize: 11,
            color: "var(--mdb-text-dim)",
            padding: "3px 8px",
            border: "1px solid var(--mdb-border)",
            borderRadius: "var(--radius)",
          }}>
            One platform · Operational + AI
          </span>

          {/* Docs dropdown */}
          <div ref={dropdownRef} style={{ position: "relative" }}>
            <button
              className="btn-secondary"
              onClick={() => setDropdownOpen(o => !o)}
              style={{ fontSize: 11, padding: "5px 10px", display: "flex", alignItems: "center", gap: 5 }}
            >
              Docs
              <span style={{ fontSize: 9, opacity: 0.7 }}>{dropdownOpen ? "▲" : "▼"}</span>
            </button>

            {dropdownOpen && (
              <div style={{
                position: "absolute",
                top: "calc(100% + 6px)",
                right: 0,
                background: "var(--mdb-slate)",
                border: "1px solid var(--mdb-border)",
                borderRadius: "var(--radius)",
                minWidth: 140,
                zIndex: 150,
                overflow: "hidden",
                boxShadow: "0 4px 16px rgba(0,0,0,0.4)",
              }}>
                {DOCS.map(d => (
                  <button
                    key={d.name}
                    onClick={() => { setActiveDoc(d.name); setDropdownOpen(false); }}
                    style={{
                      display: "block",
                      width: "100%",
                      textAlign: "left",
                      background: "transparent",
                      border: "none",
                      borderBottom: "1px solid var(--mdb-border)",
                      borderRadius: 0,
                      padding: "9px 14px",
                      fontSize: 12,
                      color: "var(--mdb-text)",
                      cursor: "pointer",
                    }}
                    onMouseEnter={e => (e.currentTarget.style.background = "var(--mdb-slate-light)")}
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
              style={{ fontSize: 11, padding: "5px 12px", whiteSpace: "nowrap" }}
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
