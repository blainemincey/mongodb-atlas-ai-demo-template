import type { DemoRecord, EmbeddingResult, SearchResults, OutputResult, KnowledgeItem, HistoricalRecord } from "./types";

const BASE = "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return res.json();
}

export const api = {
  getRecord: (scenario: string) =>
    request<DemoRecord>(`/records/${scenario}/record`),

  generateEmbedding: (scenario: string) =>
    request<EmbeddingResult>(`/records/${scenario}/embed`, { method: "POST" }),

  runSearch: (scenario: string, filters: Record<string, string | undefined>) =>
    request<SearchResults>(`/search/${scenario}`, {
      method: "POST",
      body: JSON.stringify({ filters }),
    }),

  softResetAll: () =>
    request<{ status: string; records_reset: { record_id: string; scenario: string; embedding_preserved: boolean }[]; message: string }>(
      `/records/reset-all`,
      { method: "POST" }
    ),

  generateOutput: (
    scenario: string,
    knowledge_items: KnowledgeItem[],
    historical_records: HistoricalRecord[]
  ) =>
    request<OutputResult>(`/records/${scenario}/output`, {
      method: "POST",
      body: JSON.stringify({ knowledge_items, historical_records }),
    }),

  fetchDoc: (name: "readme" | "runbook" | "script") =>
    request<{ name: string; title: string; content: string }>(`/docs/${name}`),
};
