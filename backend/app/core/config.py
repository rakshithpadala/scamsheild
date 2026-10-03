"""Application settings loaded from environment / .env file."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_ROOT = Path(__file__).resolve().parents[3]  # repo root (ScamSheild/)


class Settings(BaseSettings):
    """All config is read from .env at repo root; never hard-code secrets."""

    model_config = SettingsConfigDict(
        env_file=str(_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── LLM ──────────────────────────────────────────────────────────────
    LLM_PROVIDER: str = "template"  # gemini | groq | ollama | template
    LLM_MODEL: str = ""
    USE_LLM_EXPLANATION: bool = False
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""

    # ── Database ─────────────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite:///./scamshield.db"

    # ── Paths (derived, not from env) ────────────────────────────────────
    @property
    def repo_root(self) -> Path:
        return _ROOT

    @property
    def ml_artifacts_dir(self) -> Path:
        return _ROOT / "ml" / "artifacts"

    @property
    def knowledge_base_dir(self) -> Path:
        return _ROOT / "knowledge_base"


@lru_cache
def get_settings() -> Settings:
    return Settings()
