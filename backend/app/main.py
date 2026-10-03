"""FastAPI application entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.health import router as health_router
from backend.app.db.base import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: create tables. Shutdown: nothing special for SQLite."""
    init_db()
    yield


app = FastAPI(
    title="ScamShield AI",
    description="Multimodal personal digital-safety assistant (India-focused)",
    version="0.1.0",
    lifespan=lifespan,
)

# ── CORS (allow Vite dev server) ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────────────────
app.include_router(health_router)
# Future: analyze_router, copilot_router, feedback_router, etc.
