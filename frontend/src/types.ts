export type Scenario = "A" | "B" | "C";

export type Step = 1 | 2 | 3 | 4 | 5;

export interface DemoRecord {
  _id?: string;
  record_id: string;
  scenario: string;
  record_text: string;
  record_embedding?: string; // serialized as "<vector:N dims>" from backend
  processing_status: string;
  embedding_model?: string;
  embedding_generated_at?: string | null;
  ai_output?: string | null;
  ai_determination?: string | null;
  ai_output_generated_at?: string | null;
  ai_supporting_kb_ids?: string[];
  ai_comparable_record_ids?: string[];
  [key: string]: unknown; // domain-specific fields pass through
}

export interface EmbeddingResult {
  status: string;
  record_id: string;
  embedding_model: string;
  embedding_dimensions: number;
  embedding_preview: number[];
  generated_at: string;
  message: string;
}

export interface KnowledgeItem {
  kb_id: string;
  title: string;
  category: string;
  subcategory?: string;
  content_text: string;
  vector_score?: number;
  [key: string]: unknown;
}

export interface HistoricalRecord {
  record_id: string;
  category: string;
  outcome: string;
  outcome_rationale?: string;
  source_text?: string;
  vector_score?: number;
  [key: string]: unknown;
}

export interface SearchResults {
  knowledge_base: KnowledgeItem[];
  historical_records: HistoricalRecord[];
  query_filters_applied: Record<string, string | null>;
  meta: Record<string, string | number>;
}

export interface OutputResult {
  output: string;
  determination: string;
  supporting_kb_ids: string[];
  comparable_record_ids: string[];
  updated_record: DemoRecord;
}
