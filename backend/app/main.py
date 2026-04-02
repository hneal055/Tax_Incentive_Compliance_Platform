"""Main FastAPI application."""

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import router as api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="PilotForge Tax Incentive Compliance Platform",
    description="API for managing film and television tax incentives",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo purposes; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Serve static files (HTML/CSS/JS for demo pages)
# Get the backend directory (one level up from this file)
backend_dir = os.path.dirname(os.path.dirname(__file__))
static_dir = os.path.join(backend_dir, "static")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    logger.info(f"Serving static files from {static_dir}")
else:
    logger.warning(f"Static directory not found at {static_dir}")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "PilotForge Tax Incentive Compliance Platform",
        "version": "1.0.0",
        "docs": "/docs",
        "demo": "/static/index.html",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    """Initialize database and seed data on startup."""
    try:
        from app.db.session import engine, Base
        from scripts.add_georgia import add_georgia
        from scripts.seed_georgia import seed_georgia

        logger.info("🚀 Running database initialization...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables created")

        # Add Georgia jurisdiction if not present
        add_georgia()

        # Seed Georgia program rules
        seed_georgia()

        logger.info("✅ Startup complete!")
    except Exception as e:
        logger.error(f"Startup error: {e}")
