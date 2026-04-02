from fastapi import APIRouter
from app.api.v1.endpoints import admin, budgets

router = APIRouter()
router.include_router(admin.router)
router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
