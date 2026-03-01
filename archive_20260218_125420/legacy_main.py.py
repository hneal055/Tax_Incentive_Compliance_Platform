from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Tax Incentive Compliance Platform API",
    description="API for managing tax incentive compliance for film and TV productions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routes
try:
    from routes import router
    # Include all routes under /api/v1 prefix
    app.include_router(router, prefix="/api/v1")
    print("✅ Successfully loaded API routes from routes.py")
except ImportError as e:
    print(f"❌ Error importing routes: {e}")
    print("   Please check that routes.py exists and has no syntax errors")

# Root endpoint (separate from the router)
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

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("🚀 Starting Tax Incentive Compliance Platform API...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔗 Health Check: http://localhost:8000/api/v1/health")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
