from fastapi import FastAPI
from fastapi. middleware.cors import CORSMiddleware

app = FastAPI(
    title="Tax Incentive Compliance Platform",
    description="API for managing tax incentive compliance",
    version="1.0.0"
)

# Mount frontend static files if build exists
from pathlib import Path
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Tax Incentive Compliance Platform API",
        "status": "operational"
    }

@app. get("/health")
async def health_check():
    return {"status": "healthy"}

# Add your routes here
# Example: 
# @app.get("/api/v1/incentives")
# async def get_incentives():
#     return {"incentives": []}

if __name__ == "__main__": 
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
