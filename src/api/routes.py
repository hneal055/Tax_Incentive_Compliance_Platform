"""
API router aggregation

This file is intentionally defensive: missing optional routers will not crash app startup.
"""
from __future__ import annotations

import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter()


def _safe_include(module_path: str, attr: str = "router") -> None:
    try:
        mod = __import__(module_path, fromlist=[attr])
        sub_router = getattr(mod, attr)
        router.include_router(sub_router)
        logger.info("Included router: %s", module_path)
    except ModuleNotFoundError as e:
        logger.warning("Router module missing, skipping: %s (%s)", module_path, e)
    except Exception as e:
        logger.exception("Failed including router %s: %s", module_path, e)


# Core routers (expected to exist)
_safe_include("src.api.jurisdictions")
_safe_include("src.api.incentive_rules")

# Optional/phase routers (may not exist yet)
_safe_include("src.api.calculations")
_safe_include("src.api.productions")
_safe_include("src.api.expenses")
_safe_include("src.api.audit_logs")
_safe_include("src.api.users")
