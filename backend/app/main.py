"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging

from app.api.v1 import router as api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PilotForge Tax Incentive Compliance Platform",
    description="API for managing film and television tax incentives",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    return {"message": "PilotForge Platform", "version": "1.0.0", "docs": "/docs", "demo": "/static/index.html"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    try:
        from app.db.session import engine, Base
        from scripts.add_georgia import add_georgia
        from scripts.seed_georgia import seed_georgia
        logger.info("🚀 Running database initialization...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables created")
        add_georgia()
        seed_georgia()
        logger.info("✅ Startup complete!")
    except Exception as e:
        logger.error(f"Startup error: {e}")
