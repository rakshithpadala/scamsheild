import knownThreat from "./known_threat.json";
import suspicious from "./suspicious.json";
import lowRisk from "./low_risk.json";
import insufficientEvidence from "./insufficient_evidence.json";
import type { AnalysisResult } from "../lib/types";

export const FIXTURES: Record<string, AnalysisResult> = {
  known_threat: knownThreat as unknown as AnalysisResult,
  suspicious: suspicious as unknown as AnalysisResult,
  low_risk: lowRisk as unknown as AnalysisResult,
  insufficient_evidence: insufficientEvidence as unknown as AnalysisResult,
};

export { knownThreat, suspicious, lowRisk, insufficientEvidence };
