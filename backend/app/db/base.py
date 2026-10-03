"""SQLAlchemy 2 engine, session factory, and Base for SQLite."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.app.core.config import get_settings

_settings = get_settings()

engine = create_engine(
    _settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite requires this
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


def get_db() -> Session:  # type: ignore[misc]
    """FastAPI dependency — yields a DB session, closes on teardown."""
    db = SessionLocal()
    try:
        yield db  # type: ignore[misc]
    finally:
        db.close()


def init_db() -> None:
    """Create all tables. Called once at startup."""
    Base.metadata.create_all(bind=engine)
