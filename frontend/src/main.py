"""
PilotForge - Tax Incentive Intelligence for Film & TV

Main FastAPI application for tax incentive calculation and compliance verification.
"""
from fastapi import FastAPIccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# Import your API routers here
try: fastapi.middleware.cors import CORSMiddleware
    from src.api.routes import router as api_router
except ImportError:
    api_router = None import settings
from src.utils.database import prisma
app = FastAPI(outes import router
    title="PilotForge - Tax Incentive Intelligence",
    version="0.1.0"
) Configure logging
logging.basicConfig(
# CORS middleware (adjust origins as needed)L.upper(), logging.INFO),
app.add_middleware(me)s - %(name)s - %(levelname)s - %(message)s",
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:5173", "http://127.0.0.1:5173"]er(__name__)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)sync def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
# Health endpoint
@app.get("/health") Starting PilotForge")
async def health(): Tax Incentive Intelligence for Film & TV")
    return {"status": "healthy"}
        await prisma.connect()
# Include API routers if availablennected")
if api_router:eption as e:  # noqa: BLE001
    app.include_router(api_router, prefix="/api/0.1.0")}")
        raise
# Optionally, add a root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to PilotForge API"}
    logger.info("🛑 Shutting down PilotForge")
    try:
        await prisma.disconnect()
        logger.info("✅ Database disconnected")
    except Exception as e:  # noqa: BLE001
        logger.error(f"❌ Database disconnection failed: {e}")


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)


# Include API routes under the configured prefix (e.g. /api/0.1.0)
app.include_router(router, prefix="/api/0.1.0")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information."""
    return {
        "message": "Welcome to PilotForge",
        "tagline": "Tax Incentive Intelligence for Film & TV",
        "version": settings.API_VERSION,
        "status": "running",
        "docs": "/docs",
        "api": settings.API_PREFIX,
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    try:
        # Check database connection
        await prisma.query_raw("SELECT 1")
        db_status = "connected"
    except Exception as e:  # noqa: BLE001
        logger.error(f"Health check failed: {e}")
        db_status = "disconnected"
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": db_status,
                "error": str(e),
            },
        )

    return {
        "status": "healthy",
        "database": db_status,
        "version": settings.API_VERSION,
        "environment": settings.APP_ENV,
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):  # noqa: ANN001, D401
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found", "path": str(request.url.path)},
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):  # noqa: ANN001, D401
    """Handle 500 errors."""
    logger.error(f"Internal error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred",
        },
    )


# Startup banner
@app.on_event("startup")
async def startup_banner() -> None:
    """Display startup banner."""
    print("\n" + "=" * 70)
    print("🎬  PilotForge")
    print("   Tax Incentive Intelligence for Film & TV")
    print("=" * 70)
    print(f"📊 API Version: {settings.API_VERSION}")
    print(f"🌍 Environment: {settings.APP_ENV}")
    print(f"🔗 Docs: http://{settings.APP_HOST}:{settings.APP_PORT}/docs")
    print(f"🚀 API: http://{settings.APP_HOST}:{settings.APP_PORT}{settings.API_PREFIX}")
    print("=" * 70 + "\n")


# Development server (optional - for direct python execution)
if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower(),
    )
