"""
Authentication API endpoints
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timezone

from src.api.middleware.auth import create_access_token
from src.utils.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


class TokenRequest(BaseModel):
    api_key: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


@router.post(
    "/token",
    response_model=TokenResponse,
    summary="Get JWT access token",
)
async def create_token(request: TokenRequest):
    """
    Exchange an API key for a JWT access token.
    The token is valid for ACCESS_TOKEN_EXPIRE_MINUTES minutes.
    """
    valid_keys = [k.strip() for k in settings.VALID_API_KEYS.split(",") if k.strip()]

    # If no keys configured, allow any non-empty key (development mode)
    if valid_keys and request.api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    if not request.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required",
        )

    token = create_access_token(
        data={"sub": "api_client", "api_key": request.api_key}
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
