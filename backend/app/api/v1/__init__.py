from fastapi import APIRouter
from app.api.v1.endpoints import admin

router = APIRouter()
router.include_router(admin.router)
