"""
Application configuration (Pydantic v2)

Loads from environment variables and .env file at project root.
"""
from __future__ import annotations

import json
from typing import List, Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _coerce_list(value: Any) -> List[str]:
    """
    Accepts:
      - list[str]
      - "*" -> ["*"]
      - JSON list string: '["http://localhost:3000"]'
      - comma-separated: "a,b,c"
      - empty/None -> []
    """
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return []
        if s == "*":
            return ["*"]
        # Try JSON first
        if (s.startswith("[") and s.endswith("]")) or (s.startswith('"') and s.endswith('"')):
            try:
                parsed = json.loads(s)
                if isinstance(parsed, list):
                    return [str(x).strip() for x in parsed if str(x).strip()]
            except Exception:
                pass
        # Comma-separated fallback
        return [p.strip() for p in s.split(",") if p.strip()]
    # Fallback
    return [str(value).strip()] if str(value).strip() else []


class Settings(BaseSettings):
    # Core API settings
    API_TITLE: str = "Tax-Incentive Compliance Platform"
    API_VERSION: str = "v1"
    LOG_LEVEL: str = "INFO"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]

    # Database (required)
    DATABASE_URL: str

    # Pydantic Settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Allow env vars to be strings or lists
    @field_validator("ALLOWED_ORIGINS", "ALLOWED_METHODS", "ALLOWED_HEADERS", mode="before")
    @classmethod
    def _validate_lists(cls, v: Any) -> List[str]:
        return _coerce_list(v)


# Singleton settings object
settings = Settings()
