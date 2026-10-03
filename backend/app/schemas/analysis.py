"""Pydantic v2 schemas — single source of truth for the ScamShield API contract."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field

# ── Enums ────────────────────────────────────────────────────────────────────

class Verdict(str, Enum):
    KNOWN_THREAT = "KNOWN_THREAT"
    SUSPICIOUS = "SUSPICIOUS"
    LOW_RISK = "LOW_RISK"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class InputType(str, Enum):
    MESSAGE = "message"
    URL = "url"
    SCREENSHOT = "screenshot"
    EMAIL = "email"


class EvidenceSource(str, Enum):
    RULE = "rule"
    ML = "ml"
    INTEL = "intel"


class IntelStatus(str, Enum):
    MATCH = "match"
    NO_MATCH = "no_match"
    UNAVAILABLE = "unavailable"


class SSEStage(str, Enum):
    READING = "reading"
    EXTRACTING_LINKS = "extracting_links"
    CHECKING_FEEDS = "checking_feeds"
    SCORING = "scoring"
    EXPLAINING = "explaining"
    COMPLETE = "complete"


# ── Sub-models ───────────────────────────────────────────────────────────────

class TextSpan(BaseModel):
    start: int
    end: int
    text: str


class Evidence(BaseModel):
    id: str
    label: str
    weight: float = Field(ge=0.0, le=1.0)
    source: EvidenceSource
    spans: list[TextSpan] = []
    detail: str = ""


class Category(BaseModel):
    label: str
    confidence: float = Field(ge=0.0, le=1.0)


class Entities(BaseModel):
    urls: list[str] = []
    phones: list[str] = []
    emails: list[str] = []
    upi_ids: list[str] = []


class IntelResult(BaseModel):
    status: IntelStatus
    provider: str


class URLResult(BaseModel):
    url: str
    ml_risk: float = Field(ge=0.0, le=1.0, default=0.0)
    features: dict = {}
    intel: IntelResult = Field(
        default_factory=lambda: IntelResult(
            status=IntelStatus.UNAVAILABLE, provider="none"
        )
    )


class OCRResult(BaseModel):
    text: str = ""
    confidence: float = Field(ge=0.0, le=1.0, default=0.0)


class Citation(BaseModel):
    source: str
    title: str
    page: int | None = None
    snippet: str
    url: str = ""


# ── Main response ────────────────────────────────────────────────────────────

class AnalysisResult(BaseModel):
    analysis_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    input_type: InputType
    verdict: Verdict
    risk_score: int = Field(ge=0, le=100)
    category: Category
    evidence: list[Evidence] = []
    entities: Entities = Field(default_factory=Entities)
    url_results: list[URLResult] = []
    ocr: OCRResult | None = None
    explanation: str = ""
    next_steps: list[str] = []
    citations: list[Citation] = []
    limitations: str = ""
    model_version: str = "0.1.0"
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# ── Request schemas ──────────────────────────────────────────────────────────

class MessageRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    input_type: InputType = InputType.MESSAGE
    ocr: OCRResult | None = None


class URLRequest(BaseModel):
    url: str = Field(min_length=1, max_length=2048)


class EmailRequest(BaseModel):
    raw_email: str = Field(min_length=1, max_length=50000)


# ── SSE ──────────────────────────────────────────────────────────────────────

class SSEEvent(BaseModel):
    stage: SSEStage
    progress: float = Field(ge=0.0, le=1.0)
    message: str = ""


# ── Feedback ─────────────────────────────────────────────────────────────────

class FeedbackRequest(BaseModel):
    analysis_id: str
    is_correct: bool
    comment: str = ""


# ── Copilot ──────────────────────────────────────────────────────────────────

class CopilotRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    analysis_id: str | None = None


class CopilotResponse(BaseModel):
    reply: str
    tool_calls: list[dict] = []
    citations: list[Citation] = []
