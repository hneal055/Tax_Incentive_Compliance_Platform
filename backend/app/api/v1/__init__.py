from fastapi import APIRouter
from app.api.v1.endpoints import admin, integrations

router = APIRouter()
router.include_router(admin.router)
router.include_router(integrations.router)
