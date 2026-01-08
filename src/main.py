"""
Tax-Incentive Compliance Platform
Main application entry point
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from src.api.routes import router
from src.utils.config import settings
from src.utils.database import prisma
from src.utils.startup_banner import print_api_urls

# ----------------------------
# Logging
# ----------------------------
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def _is_truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y", "on"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events.

    Supports running without a database by setting:
      SKIP_DB=1
    """
    logger.info("Starting Tax-Incentive Compliance Platform")

    skip_db = _is_truthy(os.getenv("SKIP_DB"))

    if skip_db:
        logger.warning("SKIP_DB=1 set — starting without database connection")
    else:
        try:
            await prisma.connect()
            logger.info("Database connected")
        except Exception as e:
            # Fail fast in normal mode; in dev you can set SKIP_DB=1
            logger.exception("Database connection failed")
            raise e

    # Print helpful URLs for local dev
    try:
        print_api_urls(api_version=settings.API_VERSION, host="localhost", port=8000)
    except Exception:
        # Never crash startup just because banner printing failed
        logger.debug("startup_banner.print_api_urls failed", exc_info=True)

    yield

    logger.info("Shutting down Tax-Incentive Compliance Platform")

    if not skip_db:
        try:
            await prisma.disconnect()
            logger.info("Database disconnected")
        except Exception:
            logger.debug("Database disconnect failed", exc_info=True)


app = FastAPI(
    title=getattr(settings, "API_TITLE", "Tax-Incentive Compliance Platform"),
    description="Jurisdictional Rule Engine for Film & Television Tax Incentives",
    version=getattr(settings, "API_VERSION", "v1"),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ----------------------------
# Middleware
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=getattr(settings, "ALLOWED_ORIGINS", ["*"]),
    allow_credentials=getattr(settings, "ALLOW_CREDENTIALS", True),
    allow_methods=getattr(settings, "ALLOWED_METHODS", ["*"]),
    allow_headers=getattr(settings, "ALLOWED_HEADERS", ["*"]),
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# ----------------------------
# Routes
# ----------------------------
app.include_router(router, prefix=f"/api/{getattr(settings, 'API_VERSION', 'v1')}")


@app.get("/")
async def root() -> Dict[str, str]:
    return {
        "message": "Tax-Incentive Compliance Platform",
        "version": getattr(settings, "API_VERSION", "v1"),
        "status": "running",
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.

    If SKIP_DB=1, database will report as 'skipped'.
    Otherwise runs a simple DB probe.
    """
    skip_db = _is_truthy(os.getenv("SKIP_DB"))

    if skip_db:
        return {
            "status": "healthy",
            "database": "skipped",
            "api_version": getattr(settings, "API_VERSION", "v1"),
        }

    try:
        # Prisma raw probe
        await prisma.execute_raw("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"

    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "database": db_status,
        "api_version": getattr(settings, "API_VERSION", "v1"),
    }

