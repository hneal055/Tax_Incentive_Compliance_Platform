"""Main FastAPI application."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1 import router as api_router

app = FastAPI(
    title="Tax Incentive Compliance Platform",
    description="API for managing film and television tax incentives",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Serve static files (rules viewer, integration demo, etc.)
# Walk up from app/main.py → app/ → backend/ → static/
_here = os.path.dirname(os.path.abspath(__file__))
_static_dir = os.path.join(_here, "..", "static")
_static_dir = os.path.normpath(_static_dir)
app.mount("/static", StaticFiles(directory=_static_dir), name="static")

@app.get("/")
async def root():
    return {
        "message": "Tax Incentive Compliance Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
