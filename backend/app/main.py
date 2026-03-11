"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from app.database import engine, Base
from app.config import settings
from app.seed import seed_database
from app.services.scheduler import run_daily_digest

# ── Logging ───────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)

# ── APScheduler ───────────────────────────────────────
scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables, seed data, and start the scheduler on startup."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created.")

    # Seed defaults
    seed_database()

    # Schedule daily digest
    scheduler.add_job(
        run_daily_digest,
        "cron",
        hour=settings.DIGEST_HOUR,
        minute=settings.DIGEST_MINUTE,
        id="daily_digest",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(
        f"Scheduler started – daily digest at {settings.DIGEST_HOUR:02d}:{settings.DIGEST_MINUTE:02d}"
    )

    yield

    scheduler.shutdown()
    logger.info("Scheduler shut down.")


# ── App ───────────────────────────────────────────────
app = FastAPI(
    title="News Monitor API",
    description="Collects Nigerian news headlines and generates daily email digests.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────
from app.routers import sites, topics, articles, recipients, digests, dashboard, settings as settings_router

app.include_router(sites.router)
app.include_router(topics.router)
app.include_router(articles.router)
app.include_router(recipients.router)
app.include_router(digests.router)
app.include_router(dashboard.router)
app.include_router(settings_router.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "News Monitor API"}
