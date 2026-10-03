"""Pydantic request and response schemas for ScamShield API."""
from typing import List, Optional

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="Message text or OCR extracted text")
    url: Optional[str] = Field(None, description="Optional extracted URL")

class PipelineStage(BaseModel):
    name: str
    status: str
    detail: Optional[str] = None

class AnalyzeResponse(BaseModel):
    verdict: str = Field(..., description="SAFE, SUSPICIOUS, KNOWN, or INSUFFICIENT")
    risk_score: float = Field(..., description="Risk score from 0.0 to 100.0")
    category: str = Field(..., description="Identified scam category or benign")
    highlighted_phrases: List[str] = Field(default_factory=list, description="Suspicious trigger phrases found in input")
    explanation: str = Field(..., description="Plain-language explanation of verdict")
    stages: List[PipelineStage] = Field(default_factory=list, description="Stepper pipeline execution details")

class HealthResponse(BaseModel):
    status: str
    version: str
    provider: str
