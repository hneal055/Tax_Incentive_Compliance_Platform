"""
APScheduler setup for background feed ingestion.

Uses AsyncIOScheduler (runs jobs as coroutines on the FastAPI event loop).
Start/stop is hooked into the FastAPI lifespan in src/main.py.
"""
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

_scheduler = AsyncIOScheduler(timezone="UTC")

INGEST_INTERVAL_HOURS = 4


def get_scheduler() -> AsyncIOScheduler:
    return _scheduler


def start_scheduler() -> None:
    """Register jobs and start the scheduler. Called once at application startup."""
    from src.services.feed_ingestion import ingest_all_sources

    _scheduler.add_job(
        ingest_all_sources,
        trigger=IntervalTrigger(hours=INGEST_INTERVAL_HOURS),
        id="feed_ingestion",
        name="RSS/Atom Feed Ingestion",
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=300,  # allow up to 5 min late before skipping
    )

    _scheduler.start()
    logger.info(f"✅ Scheduler started — feed ingestion every {INGEST_INTERVAL_HOURS}h")


def stop_scheduler() -> None:
    """Gracefully shut down the scheduler. Called at application shutdown."""
    if _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("✅ Scheduler stopped")
