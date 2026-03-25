from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

app = FastAPI(
    title="Tax Incentive Compliance Platform API",
    description="API for managing tax incentive compliance for film and TV productions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Tax Incentive Compliance Platform API",
        "status": "operational",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "clients": "/api/v1/clients",
            "incentives": "/api/v1/incentives",
            "reports": "/api/v1/reports",
            "stats": "/api/v1/stats",
            "health": "/api/v1/health"
        },
        "note": "Expenses endpoint is temporarily on hold"
    }

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}