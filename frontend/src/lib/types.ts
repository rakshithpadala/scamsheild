/**
 * ScamShield AI — TypeScript types mirroring backend/app/schemas/analysis.py
 * This file is the frontend source of truth. Keep in sync with Pydantic schemas.
 */

// ── Enums ────────────────────────────────────────────────────────────────────

export type Verdict =
  | "KNOWN_THREAT"
  | "SUSPICIOUS"
  | "LOW_RISK"
  | "INSUFFICIENT_EVIDENCE";

export type InputType = "message" | "url" | "screenshot" | "email";

export type EvidenceSource = "rule" | "ml" | "intel";

export type IntelStatus = "match" | "no_match" | "unavailable";

export type SSEStage =
  | "reading"
  | "extracting_links"
  | "checking_feeds"
  | "scoring"
  | "explaining"
  | "complete";

// ── Sub-models ───────────────────────────────────────────────────────────────

export interface TextSpan {
  start: number;
  end: number;
  text: string;
}

export interface Evidence {
  id: string;
  label: string;
  weight: number; // 0–1
  source: EvidenceSource;
  spans: TextSpan[];
  detail: string;
}

export interface Category {
  label: string;
  confidence: number; // 0–1
}

export interface Entities {
  urls: string[];
  phones: string[];
  emails: string[];
  upi_ids: string[];
}

export interface IntelResult {
  status: IntelStatus;
  provider: string;
}

export interface URLResult {
  url: string;
  ml_risk: number; // 0–1
  features: Record<string, number | string | boolean>;
  intel: IntelResult;
}

export interface OCRResult {
  text: string;
  confidence: number; // 0–1
}

export interface Citation {
  source: string;
  title: string;
  page: number | null;
  snippet: string;
  url: string;
}

// ── Main response ────────────────────────────────────────────────────────────

export interface AnalysisResult {
  analysis_id: string;
  input_type: InputType;
  verdict: Verdict;
  risk_score: number; // 0–100
  category: Category;
  evidence: Evidence[];
  entities: Entities;
  url_results: URLResult[];
  ocr: OCRResult | null;
  explanation: string;
  next_steps: string[];
  citations: Citation[];
  limitations: string;
  model_version: string;
  created_at: string; // ISO datetime
}

// ── Request types ────────────────────────────────────────────────────────────

export interface MessageRequest {
  text: string;
}

export interface URLRequest {
  url: string;
}

export interface EmailRequest {
  raw_email: string;
}

// ── SSE ──────────────────────────────────────────────────────────────────────

export interface SSEEvent {
  stage: SSEStage;
  progress: number; // 0–1
  message: string;
}

// ── Feedback ─────────────────────────────────────────────────────────────────

export interface FeedbackRequest {
  analysis_id: string;
  is_correct: boolean;
  comment: string;
}

// ── Copilot ──────────────────────────────────────────────────────────────────

export interface CopilotRequest {
  message: string;
  analysis_id?: string;
}

export interface CopilotResponse {
  reply: string;
  tool_calls: Record<string, unknown>[];
  citations: Citation[];
}

// ── Verdict metadata (UI helpers) ────────────────────────────────────────────

export const VERDICT_META: Record<
  Verdict,
  { label: string; color: string; bg: string }
> = {
  KNOWN_THREAT: {
    label: "Known Threat",
    color: "#FF4D5E",
    bg: "rgba(255,77,94,0.12)",
  },
  SUSPICIOUS: {
    label: "Suspicious",
    color: "#FFB020",
    bg: "rgba(255,176,32,0.12)",
  },
  LOW_RISK: {
    label: "Low Risk",
    color: "#2DD4A0",
    bg: "rgba(45,212,160,0.12)",
  },
  INSUFFICIENT_EVIDENCE: {
    label: "Insufficient Evidence",
    color: "#8B95A7",
    bg: "rgba(139,149,167,0.12)",
  },
};
