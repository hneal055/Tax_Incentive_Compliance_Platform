"""
Application configuration (Pydantic v2)

Loads from environment variables and .env file at project root.
"""
from __future__ import annotations

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core API settings
    API_TITLE: str = "Tax-Incentive Compliance Platform"
    API_VERSION: str = "v1"
    LOG_LEVEL: str = "INFO"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]

    # Database
    DATABASE_URL: str

    # Pydantic Settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
