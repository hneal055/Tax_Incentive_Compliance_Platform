"""
PilotForge - Tax Incentive Intelligence for Film & TV
Copyright (c) 2025-2026 Howard Neal - PilotForge

Main FastAPI application for tax incentive calculation and compliance verification.
"""
from contextlib import asynccontextmanager
import logging
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from src.utils.config import settings
from src.utils.database import prisma
from src.api.routes import router
from src.services.monitoring_service import monitoring_service
from src.services.scheduler_service import scheduler_service


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("🎬 Starting PilotForge")
    logger.info("   Tax Incentive Intelligence for Film & TV")
    try:
        await prisma.connect()
        logger.info("✅ Database connected")
    except Exception as e:
        logger.warning(f"⚠️  Database connection failed: {e}")
        logger.warning("   Application will run with limited functionality")
        # Don't raise in case we're running tests or without a database
    
    # Initialize monitoring services
    try:
        await monitoring_service.initialize()
        await scheduler_service.initialize()
        logger.info("✅ Monitoring services initialized")
    except Exception as e:
        logger.warning(f"⚠️  Monitoring service initialization failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down PilotForge")
    
    # Shutdown monitoring services
    try:
        await scheduler_service.shutdown()
        await monitoring_service.shutdown()
        logger.info("✅ Monitoring services shut down")
    except Exception as e:
        logger.error(f"❌ Monitoring service shutdown failed: {e}")
    
    # Shutdown database
    try:
        if prisma.is_connected():
            await prisma.disconnect()
            logger.info("✅ Database disconnected")
    except Exception as e:
        logger.error(f"❌ Database disconnection failed: {e}")


# Create FastAPI app
app = FastAPI(
    title="PilotForge API",
    description="Tax Incentive Intelligence for Film & TV Productions",
    version="v1",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5200",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5200",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(router, prefix=f"/api/{settings.API_VERSION}")


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    try:
        # Check database connection
        await prisma.query_raw("SELECT 1")
        db_status = "connected"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        db_status = "disconnected"
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": db_status,
                "error": str(e)
            }
        )
    
    # Check monitoring service
    monitoring_status = "active" if scheduler_service._is_running else "inactive"
    
    return {
        "status": "healthy",
        "database": db_status,
        "monitoring": monitoring_status,
        "version": settings.API_VERSION,
        "environment": "production"
    }


# Serve frontend SPA
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    # Mount static assets (JS/CSS/images) at /assets
    assets_dir = frontend_dist / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")
    logger.info(f"✅ Frontend mounted from {frontend_dist}")


# Error handlers — must be defined AFTER mounts so frontend_dist is available.
# The 404 handler doubles as the SPA catch-all: non-API 404s get index.html,
# which lets redirect_slashes work correctly for API paths (no catch-all route
# that would shadow it).
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    path = request.url.path
    if path.startswith("/api/") or path.startswith("/assets"):
        return JSONResponse(
            status_code=404,
            content={"detail": "Resource not found", "path": path}
        )
    index = frontend_dist / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return JSONResponse(status_code=404, content={"detail": "Not found"})


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error(f"Internal error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": "An unexpected error occurred"}
    )




# Startup banner
@app.on_event("startup")
async def startup_banner():
    """Display startup banner"""
    print("\n" + "=" * 70)
    print("🎬  PilotForge")
    print("   Tax Incentive Intelligence for Film & TV")
    print("=" * 70)
    print(f"📊 API Version: {settings.API_VERSION}")
    print(f"🌍 Environment: {settings.ENVIRONMENT}")
    print(f"🔗 Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🚀 API: http://{settings.HOST}:{settings.PORT}/api/{settings.API_VERSION}")
    print("=" * 70 + "\n")


# Development server (optional - for direct python execution)
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )

