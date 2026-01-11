"""
Introducing PilotForge - Tax Incentive Intelligence for Film & TV
Copyright (c) 2025-2026 Howard Neal
All Rights Reserved (or "Licensed under MIT License" if using MIT)

Main FastAPI application for tax incentive calculation and compliance verification.
PilotForge
> Tax Incentive Intelligence for Film & TV
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging
from typing import Dict

from src.api.routes import router
from src.utils.database import prisma
from src.utils.config import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting PilotForge")
    await prisma.connect()
    logger.info("Database connected")
    
    yield
    
    # Shutdown
    logger.info("Shutting down PilotForge")
    await prisma.disconnect()
    logger.info("Database disconnected")


app = FastAPI(
    title=settings.API_TITLE,
    description="Tax Incentive Intelligence for Film & TV Productions",
    version=settings.API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.include_router(router, prefix=f"/api/{settings.API_VERSION}")


@app.get("/")
async def root() -> Dict[str, str]:
    return {
        "message": "Welcome to PilotForge", "tagline": "Tax Incentive Intelligence for Film & TV",
        "version": settings.API_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    try:
        await prisma.execute_raw("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "database": db_status,
        "api_version": settings.API_VERSION
    }
