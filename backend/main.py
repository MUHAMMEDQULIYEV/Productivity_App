"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import analytics, flashcards, language, notes, notifications, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle hooks."""
    # Start background scheduler
    from services.scheduler import scheduler

    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(
    title="Productivity & Language Learning API",
    version="1.0.0",
    description="Self-hosted productivity platform with language learning features.",
    lifespan=lifespan,
)

# ── CORS ────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(notes.router, prefix="/api", tags=["notes"])
app.include_router(flashcards.router, prefix="/api", tags=["flashcards"])
app.include_router(language.router, prefix="/api", tags=["language"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])
app.include_router(notifications.router, prefix="/api", tags=["notifications"])


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    """Simple liveness probe."""
    return {"status": "ok"}
