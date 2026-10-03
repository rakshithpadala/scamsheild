"""ORM models for persisting analysis results and feedback."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)

from backend.app.db.base import Base


class AnalysisRecord(Base):
    """Stores every analysis result for the history page."""

    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    analysis_id = Column(String(36), unique=True, nullable=False, index=True)
    input_type = Column(String(20), nullable=False)           # message|url|screenshot|email
    input_text = Column(Text, nullable=False, default="")     # original text (or OCR text)
    verdict = Column(String(30), nullable=False)
    risk_score = Column(Integer, nullable=False)
    category_label = Column(String(50), nullable=False, default="other")
    category_confidence = Column(Float, nullable=False, default=0.0)
    result_json = Column(JSON, nullable=False)                # full AnalysisResult serialised
    created_at = Column(
        DateTime, nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )


class FeedbackRecord(Base):
    """Optional user feedback on an analysis."""

    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    analysis_id = Column(String(36), nullable=False, index=True)
    is_correct = Column(Boolean, nullable=False)
    comment = Column(Text, nullable=False, default="")
    created_at = Column(
        DateTime, nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
