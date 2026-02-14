"""
PilotForge - Tax Incentive Intelligence for Film & TV
Copyright (c) 2026 PilotForge - Tax Incentive Compliance Platform
All Rights Reserved.

PROPRIETARY AND CONFIDENTIAL
This software is proprietary and confidential. Unauthorized copying,
distribution, modification, or use is strictly prohibited.

Main FastAPI application for tax incentive calculation and compliance verification.
"""
import os
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.utils.config import settings
from src.utils.database import prisma
from src.api.routes import router
from src.core.api_key_middleware import ApiKeyMiddleware

# Optional services - only import if enabled
try:
    from src.services.monitoring_service import monitoring_service
    from src.services.scheduler_service import scheduler_service
    from src.services.rate_limit_service import rate_limit_service
    from src.services.news_monitor import news_monitor_service
    from src.services.llm_summarization import llm_summarization_service
    from src.services.notification_service import (
        email_notification_service,
        slack_notification_service
    )
    OPTIONAL_SERVICES_AVAILABLE = True
except ImportError as e:
    OPTIONAL_SERVICES_AVAILABLE = False
    logging.warning(f"Optional services not available: {e}")


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Handles graceful startup with optional service initialization.
    """
    # ============================================================================
    # STARTUP
    # ============================================================================
    logger.info("=" * 70)
    logger.info("🎬  PilotForge - Tax Incentive Intelligence for Film & TV")
    logger.info("=" * 70)
    
    # 1. Database Connection (CRITICAL - but don't crash if it fails)
    try:
        await prisma.connect()
        logger.info("✅ Database connected")
    except Exception as e:
        logger.warning(f"⚠️  Database connection failed: {e}")
        logger.warning("   Application will continue with limited functionality")
        logger.warning("   Some API endpoints may not work without database")
    
    # 2. Optional Monitoring Services (only if enabled via environment)
    if OPTIONAL_SERVICES_AVAILABLE and getattr(settings, 'ENABLE_MONITORING', False):
        try:
            logger.info("Initializing monitoring services...")
            await monitoring_service.initialize()
            await news_monitor_service.initialize()
            await llm_summarization_service.initialize()
            await email_notification_service.initialize()
            await slack_notification_service.initialize()
            await scheduler_service.initialize()
            logger.info("✅ Monitoring services initialized")
        except Exception as e:
            logger.warning(f"⚠️  Monitoring service initialization failed: {e}")
            logger.warning("   Application will continue without monitoring")
    else:
        logger.info("ℹ️  Monitoring services disabled")
    
    # 3. Optional Rate Limiting (only if Redis is configured)
    if OPTIONAL_SERVICES_AVAILABLE and getattr(settings, 'ENABLE_RATE_LIMITING', False):
        try:
            redis_url = getattr(settings, 'REDIS_URL', 'redis://localhost:6379')
            await rate_limit_service.initialize(redis_url)
            logger.info("✅ Rate limiting initialized")
        except Exception as e:
            logger.warning(f"⚠️  Rate limiting initialization failed: {e}")
            logger.warning("   Application will continue without rate limiting")
    else:
        logger.info("ℹ️  Rate limiting disabled")
    
    logger.info("=" * 70)
    logger.info(f"🚀 PilotForge API ready at /api/{settings.API_VERSION}")
    logger.info(f"📚 Documentation available at /docs")
    logger.info("=" * 70)
    
    yield
    
    # ============================================================================
    # SHUTDOWN
    # ============================================================================
    logger.info("=" * 70)
    logger.info("🛑 Shutting down PilotForge")
    logger.info("=" * 70)
    
    # 1. Shutdown monitoring services
    if OPTIONAL_SERVICES_AVAILABLE and getattr(settings, 'ENABLE_MONITORING', False):
        try:
            await scheduler_service.shutdown()
            await monitoring_service.shutdown()
            await llm_summarization_service.shutdown()
            await slack_notification_service.shutdown()
            logger.info("✅ Monitoring services shut down")
        except Exception as e:
            logger.error(f"❌ Monitoring service shutdown failed: {e}")
    
    # 2. Shutdown rate limiting service
    if OPTIONAL_SERVICES_AVAILABLE and getattr(settings, 'ENABLE_RATE_LIMITING', False):
        try:
            await rate_limit_service.shutdown()
            logger.info("✅ Rate limiting shut down")
        except Exception as e:
            logger.error(f"❌ Rate limiting shutdown failed: {e}")
    
    # 3. Disconnect from database
    try:
        if prisma.is_connected():
            await prisma.disconnect()
            logger.info("✅ Database disconnected")
    except Exception as e:
        logger.error(f"❌ Database disconnection failed: {e}")
    
    logger.info("=" * 70)
    logger.info("👋 PilotForge shutdown complete")
    logger.info("=" * 70)


# ============================================================================
# CREATE FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="PilotForge API",
    description="Tax Incentive Intelligence for Film & TV Productions",
    version=settings.API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"/api/{settings.API_VERSION}/openapi.json"
)


# ============================================================================
# MIDDLEWARE CONFIGURATION
# ============================================================================

# 1. CORS Middleware - Allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5200",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5200",
        "http://127.0.0.1:8000",
        "https://*.onrender.com",  # Render deployments
        "*"  # Allow all origins (restrict in production if needed)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. API Key Middleware - Rate limiting and permissions
app.add_middleware(ApiKeyMiddleware)


# ============================================================================
# API ROUTES
# ============================================================================

# Include all API routes with /api prefix
app.include_router(router, prefix="/api")


# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@app.get("/health", tags=["Health"], response_model=Dict[str, str])
async def health_check():
    """
    Simple health check endpoint for deployment platforms.
    
    Always returns 200 OK to indicate the service is running.
    Does NOT check database or other services to avoid blocking.
    
    Use /health/detailed for comprehensive health information.
    """
    return {
        "status": "healthy",
        "service": "pilotforge",
        "version": settings.API_VERSION
    }


@app.get("/health/detailed", tags=["Health"])
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check with database and service status.
    
    This endpoint checks:
    - Database connectivity
    - Monitoring service status
    - Rate limiting status
    
    Use this for monitoring dashboards, not for deployment health checks.
    """
    health_status = {
        "status": "healthy",
        "service": "pilotforge",
        "version": settings.API_VERSION,
        "environment": getattr(settings, 'ENVIRONMENT', 'development'),
        "database": "unknown",
        "monitoring": "disabled",
        "rate_limiting": "disabled"
    }
    
    # Check database connection
    try:
        await prisma.query_raw("SELECT 1")
        health_status["database"] = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["database"] = "disconnected"
        health_status["status"] = "degraded"
    
    # Check monitoring service
    if OPTIONAL_SERVICES_AVAILABLE and getattr(settings, 'ENABLE_MONITORING', False):
        try:
            health_status["monitoring"] = "active" if scheduler_service._is_running else "inactive"
        except Exception:
            health_status["monitoring"] = "error"
    
    # Check rate limiting
    if OPTIONAL_SERVICES_AVAILABLE and getattr(settings, 'ENABLE_RATE_LIMITING', False):
        health_status["rate_limiting"] = "active"
    
    return health_status


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information and navigation.
    """
    return {
        "message": "Welcome to PilotForge",
        "tagline": "Tax Incentive Intelligence for Film & TV",
        "version": settings.API_VERSION,
        "status": "running",
        "endpoints": {
            "documentation": "/docs",
            "redoc": "/redoc",
            "api": f"/api/{settings.API_VERSION}",
            "health": "/health",
            "detailed_health": "/health/detailed"
        }
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    """Handle 404 Not Found errors"""
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Resource not found",
            "path": str(request.url.path),
            "method": request.method
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    """Handle 500 Internal Server errors"""
    logger.error(f"Internal error on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )


# ============================================================================
# STATIC FILE SERVING (FRONTEND)
# ============================================================================

# Serve frontend static files from the build directory
# This must be LAST to avoid catching API routes
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"

if frontend_dist.exists() and frontend_dist.is_dir():
    # Production build exists - serve it
    app.mount(
        "/",
        StaticFiles(directory=str(frontend_dist), html=True),
        name="frontend"
    )
    logger.info(f"✅ Frontend static files mounted from {frontend_dist}")
else:
    # Fallback to legacy static directory if it exists
    static_dir = Path(__file__).parent / "static"
    if static_dir.exists() and static_dir.is_dir():
        app.mount(
            "/",
            StaticFiles(directory=str(static_dir), html=True),
            name="static"
        )
        logger.info(f"⚠️  Serving legacy static files from {static_dir}")
    else:
        logger.warning("⚠️  No frontend build found - API-only mode")
        logger.warning(f"   Expected: {frontend_dist}")
        logger.warning("   Run: cd frontend && npm run build")


# ============================================================================
# DEVELOPMENT SERVER (OPTIONAL)
# ============================================================================

if __name__ == "__main__":
    """
    Development server entry point.
    
    For production deployment, use:
        uvicorn src.main:app --host 0.0.0.0 --port $PORT --workers 1
    
    For local development, run:
        python -m uvicorn src.main:app --reload
    """
    import uvicorn
    
    # Read PORT from environment (Render, Railway, etc.) or default to 8000
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    # Development mode settings
    reload = os.environ.get("RELOAD", "true").lower() == "true"
    log_level = os.environ.get("LOG_LEVEL", "info").lower()
    
    logger.info(f"Starting development server on {host}:{port}")
    
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level
    )
