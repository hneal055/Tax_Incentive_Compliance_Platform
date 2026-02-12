"""
Configuration module - re-exports settings from utils.config
This allows imports from both 'src.core.config' and 'app.core.config'
"""
from src.utils.config import settings, Settings, require_database_url

__all__ = ["settings", "Settings", "require_database_url"]
