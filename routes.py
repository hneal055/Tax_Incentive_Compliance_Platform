from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from fastapi import APIRouter
from src.api.incentive_rules import router as incentive_rules_router
# Add other routers as needed

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

# Only here should you include the router
app.include_router(router, prefix="/api/v1")

router = APIRouter()
router.include_router(incentive_rules_router, prefix="/incentive-rules", tags=["Incentive Rules"])
