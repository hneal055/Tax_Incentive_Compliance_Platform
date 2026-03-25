"""
PilotForge - Tax Incentive Intelligence for Film & TV
Copyright (c) 2025-2026 Howard Neal - PilotForge

Main FastAPI application for tax incentive calculation and compliance verification.
"""
from contextlib import asynccontextmanager
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.utils.config import settings
from src.utils.database import prisma
from src.utils.auth_utils import hash_password
from src.utils.seed import run_migrations, seed_all
from src.utils.scheduler import start_scheduler, stop_scheduler
from src.api.routes import router


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

ADMIN_EMAIL = "admin@pilotforge.com"
ADMIN_PASSWORD = "pilotforge2024"


async def _seed_admin() -> None:
    """Create the default admin account on first boot (idempotent)."""
    count = await prisma.user.count()
    if count == 0:
        await prisma.user.create(data={
            "email": ADMIN_EMAIL,
            "passwordHash": hash_password(ADMIN_PASSWORD),
            "role": "admin",
            "isActive": True,
        })
        logger.info(f"✅ Admin user created: {ADMIN_EMAIL}")
    else:
        logger.info("ℹ️  Admin user already exists — skipping seed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager — startup and shutdown."""

    # ── Startup ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("🎬  PilotForge — Tax Incentive Intelligence for Film & TV")
    print(f"📊  API Version : {settings.API_VERSION}")
    print(f"🌍  Environment : {settings.APP_ENV}")
    print(f"🔗  Docs        : http://{settings.APP_HOST}:{settings.APP_PORT}/docs")
    print("=" * 70 + "\n")

    logger.info("🎬 Starting PilotForge")

    # Database init — isolated so a DB failure degrades gracefully
    try:
        run_migrations()
        await prisma.connect()
        logger.info("✅ Database connected")
        await _seed_admin()
        await seed_all()
    except Exception as e:
        logger.warning(f"⚠️  Database init failed: {e}")
        logger.warning("   Application will run with limited functionality")

    # Scheduler starts unconditionally after DB init — never silently skipped
    try:
        start_scheduler()
    except Exception as e:
        logger.error(f"❌ Scheduler failed to start: {e}")

    yield

    # ── Shutdown ──────────────────────────────────────────────────────────────
    logger.info("🛑 Shutting down PilotForge")
    stop_scheduler()
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
        "http://localhost:8000",
        "http://localhost:8001",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(router, prefix=f"/api/{settings.API_VERSION}")


# Mount frontend static files if build exists
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
    logger.info(f"✅ Frontend mounted from {frontend_dist}")
else:
    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
        logger.info(f"✅ Static files mounted from {static_dir}")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to PilotForge",
        "tagline": "Tax Incentive Intelligence for Film & TV",
        "version": settings.API_VERSION,
        "status": "running",
        "docs": "/docs",
        "api": f"/api/{settings.API_VERSION}"
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    try:
        await prisma.query_raw("SELECT 1")
        db_status = "connected"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected", "error": str(e)}
        )

    return {
        "status": "healthy",
        "database": db_status,
        "version": settings.API_VERSION,
        "environment": "production"
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found", "path": str(request.url.path)}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": "An unexpected error occurred"}
    )


# Development server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
