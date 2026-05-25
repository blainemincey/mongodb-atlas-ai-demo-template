import { useState, useEffect } from "react";
import type { Scenario, Step, DemoRecord, EmbeddingResult, SearchResults, OutputResult } from "./types";
import { api } from "./api";
import Header from "./components/Header";
import ScenarioSelector from "./components/ScenarioSelector";
import StepTabs from "./components/StepIndicator";
import RecordSummaryBar from "./components/RecordSummaryBar";
import RecordCard from "./components/RecordCard";
import EmbeddingStep from "./components/EmbeddingStep";
import SearchStep, { type SearchFilters } from "./components/SearchStep";
import ContextPanel from "./components/ContextPanel";
import OutputPanel from "./components/OutputPanel";

// BEGIN_DOMAIN:scenario_config — replaced by scripts/init_domain.py
const SCENARIO_CONFIG: Record<Scenario, { label: string; description: string }> = {
  A: { label: "Hardware — Boot Failure", description: "Laptop disk failure under warranty — surfaces standard replacement procedure" },
  B: { label: "Software — ERP Crash", description: "Post-update SAP crash affecting Finance team — surfaces rollback procedure" },
  C: { label: "Network — VPN Failure", description: "Remote VPN connectivity failure — borderline resolution vs. escalation" },
};
// END_DOMAIN:scenario_config

type DemoState = {
  scenario: Scenario | null;
  step: Step;
  activeTab: Step;
  record: DemoRecord | null;
  embedding: EmbeddingResult | null;
  searchFilters: SearchFilters;
  searchResult: SearchResults | null;
  aiOutput: OutputResult | null;
  loading: boolean;
  error: string | null;
};

const initial: DemoState = {
  scenario: null,
  step: 1,
  activeTab: 1,
  record: null,
  embedding: null,
  searchFilters: { category: "", outcome: "" },
  searchResult: null,
  aiOutput: null,
  loading: false,
  error: null,
};

export default function App() {
  const [state, setState] = useState<DemoState>(initial);
  const [demoName, setDemoName] = useState<string>("Atlas AI Demo");

  useEffect(() => {
    api.getDemoName().then(setDemoName).catch(() => {});
  }, []);

  function set(patch: Partial<DemoState>) {
    setState((s) => ({ ...s, ...patch }));
  }

  async function selectScenario(scenario: Scenario) {
    set({ ...initial, scenario, loading: true, error: null });
    try {
      const record = await api.getRecord(scenario);
      set({ scenario, record, step: 1, activeTab: 1, loading: false });
    } catch (e: unknown) {
      set({ loading: false, error: String(e) });
    }
  }

  async function runEmbed() {
    if (!state.scenario) return;
    set({ loading: true, error: null });
    try {
      const embedding = await api.generateEmbedding(state.scenario);
      const record = await api.getRecord(state.scenario);
      set({ embedding, record, step: 2, activeTab: 3, loading: false });
    } catch (e: unknown) {
      set({ loading: false, error: String(e) });
    }
  }

  async function runSearch(filters: Record<string, string | undefined>) {
    if (!state.scenario) return;
    set({ loading: true, error: null });
    try {
      const searchResult = await api.runSearch(state.scenario, filters);
      set({ searchResult, step: 3, activeTab: 4, loading: false });
    } catch (e: unknown) {
      set({ loading: false, error: String(e) });
    }
  }

  async function runSoftReset() {
    set({ loading: true, error: null });
    try {
      await api.softResetAll();
      setState(initial);
    } catch (e: unknown) {
      set({ loading: false, error: String(e) });
    }
  }

  async function runOutput() {
    if (!state.scenario || !state.searchResult) return;
    set({ loading: true, error: null });
    try {
      const aiOutput = await api.generateOutput(
        state.scenario,
        state.searchResult.knowledge_base,
        state.searchResult.historical_records
      );
      set({ aiOutput, step: 5, activeTab: 5, loading: false });
    } catch (e: unknown) {
      set({ loading: false, error: String(e) });
    }
  }

  const { scenario, step, activeTab, record, embedding, searchFilters, searchResult, aiOutput, loading, error } = state;

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <Header
        onReset={runSoftReset}
        resetEnabled={!!record}
        resetting={loading}
        demoName={demoName}
      />

      <main style={{ flex: 1, maxWidth: 1200, margin: "0 auto", padding: "0 24px 48px", width: "100%" }}>
        <ScenarioSelector active={scenario} onSelect={selectScenario} disabled={loading} />

        {error && (
          <div style={{
            margin: "12px 0",
            padding: "10px 16px",
            background: "rgba(255,105,96,0.12)",
            border: "1px solid rgba(255,105,96,0.3)",
            borderRadius: "var(--radius)",
            color: "var(--mdb-error)",
            fontSize: 13,
          }}>
            {error}
          </div>
        )}

        {record && (
          <div style={{ display: "flex", flexDirection: "column", gap: 12, marginTop: 16 }}>
            {/* Record summary — always visible, updates in place when AI output writes back */}
            <RecordSummaryBar record={record} output={aiOutput} />

            {/* Tab nav */}
            <StepTabs
              step={step}
              activeTab={activeTab}
              onTabClick={(tab) => set({ activeTab: tab })}
            />

            {/* Active tab panel */}
            <div className="fade-in" key={activeTab} style={{ marginTop: 4 }}>
              {activeTab === 1 && (
                <RecordCard
                  record={aiOutput ? aiOutput.updated_record : record}
                  updated={!!aiOutput}
                />
              )}

              {activeTab === 2 && (
                <EmbeddingStep
                  embedding={embedding}
                  loading={loading}
                  onEmbed={runEmbed}
                  alreadyDone={step >= 2}
                />
              )}

              {activeTab === 3 && (
                <SearchStep
                  record={record}
                  filters={searchFilters}
                  onFiltersChange={(f) => set({ searchFilters: f })}
                  loading={loading}
                  onSearch={runSearch}
                  alreadyDone={step >= 3}
                />
              )}

              {activeTab === 4 && searchResult && (
                <ContextPanel result={searchResult} />
              )}

              {activeTab === 4 && !searchResult && (
                <div style={{ padding: "40px 0", textAlign: "center", color: "var(--mdb-text-dim)", fontSize: 13 }}>
                  Run Vector Search (tab 3) to retrieve knowledge base items and historical records.
                </div>
              )}

              {activeTab === 5 && (
                <OutputPanel
                  result={aiOutput}
                  loading={loading}
                  onGenerate={runOutput}
                />
              )}
            </div>
          </div>
        )}

        {!record && !loading && !error && (
          <div style={{ textAlign: "center", marginTop: 80, color: "var(--mdb-text-dim)" }}>
            <div style={{ fontSize: 48, marginBottom: 16 }}>⬆</div>
            <p style={{ fontSize: 16, marginBottom: 8 }}>Select a demo scenario above to begin.</p>
            <p style={{ fontSize: 13 }}>
              {Object.entries(SCENARIO_CONFIG).map(([k, v], i, arr) => (
                <span key={k}>{v.label}{i < arr.length - 1 ? " · " : ""}</span>
              ))}
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
