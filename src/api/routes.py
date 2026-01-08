"""
API route registry

- Central place to mount versioned routers.
- Safe-import optional modules (so the API can boot while phases build out).
- Reduces warning spam on --reload.
"""

from __future__ import annotations

import importlib
import logging
import os
from typing import Dict, List

from fastapi import APIRouter

logger = logging.getLogger(__name__)

api_router = APIRouter()

# Track what happened so we can show it in /api/<ver>/ and avoid log spam on reload
_INCLUDED: List[str] = []
_MISSING_ONCE: set[str] = set()
_FAILED_ONCE: set[str] = set()


def _truthy(v: str | None) -> bool:
    return (v or "").strip().lower() in {"1", "true", "yes", "y", "on"}


# If 1, missing/invalid "core" modules raise (useful in CI)
ROUTES_STRICT = _truthy(os.getenv("ROUTES_STRICT"))
# If 1, suppress missing-module logs for optional modules
ROUTES_QUIET = _truthy(os.getenv("ROUTES_QUIET"))


def _safe_include(
    module_path: str,
    *,
    attr_name: str = "router",
    required: bool = False,
    mount_prefix: str = "",
    tags: List[str] | None = None,
) -> bool:
    """
    Import a module and include its router if present.
    Returns True if included; False if missing or failed.

    required=True will raise if missing when ROUTES_STRICT=1.
    """
    try:
        mod = importlib.import_module(module_path)
        subrouter = getattr(mod, attr_name, None)
        if subrouter is None:
            msg = f"Router attr missing, skipping: {module_path}.{attr_name}"
            if required and ROUTES_STRICT:
                raise AttributeError(msg)
            if msg not in _FAILED_ONCE:
                logger.warning(msg)
                _FAILED_ONCE.add(msg)
            return False

        api_router.include_router(subrouter, prefix=mount_prefix, tags=tags)
        _INCLUDED.append(module_path)
        return True

    except ModuleNotFoundError as e:
        if required and ROUTES_STRICT:
            raise

        key = f"{module_path}|missing"
        if (not ROUTES_QUIET) and (key not in _MISSING_ONCE):
            logger.info("Optional router missing (ok for now): %s (%s)", module_path, e)
            _MISSING_ONCE.add(key)
        return False

    except Exception as e:
        key = f"{module_path}|failed"
        if key not in _FAILED_ONCE:
            logger.exception("Router load failed, skipping: %s (%s)", module_path, e)
            _FAILED_ONCE.add(key)

        if required and ROUTES_STRICT:
            raise
        return False


# --- Core modules (should exist) ---
_safe_include("src.api.jurisdictions", required=True, tags=["Jurisdictions"])
_safe_include("src.api.incentive_rules", required=True, tags=["Incentive Rules"])
_safe_include("src.api.rule_engine", required=True, tags=["Rule Engine"])  # POST /rule-engine/evaluate

# --- Phase modules (may not exist yet) ---
_safe_include("src.api.calculations", required=False, tags=["Calculations"])
_safe_include("src.api.productions", required=False, tags=["Productions"])
_safe_include("src.api.expenses", required=False, tags=["Expenses"])
_safe_include("src.api.users", required=False, tags=["Users"])
_safe_include("src.api.audit_logs", required=False, tags=["Audit Logs"])


@api_router.get("/")
def index() -> Dict[str, object]:
    """
    Lightweight index for humans + quick smoke tests.
    (Swagger is still at /docs.)
    """
    return {
        "routes": {
            "jurisdictions": "/jurisdictions",
            "incentive_rules": "/incentive-rules",
            "rule_engine_evaluate": "/rule-engine/evaluate",
            "calculations": "/calculations",
            "productions": "/productions",
            "expenses": "/expenses",
            "users": "/users",
            "audit_logs": "/audit-logs",
        },
        "loaded_modules": sorted(set(_INCLUDED)),
        "strict_mode": ROUTES_STRICT,
        "quiet_mode": ROUTES_QUIET,
    }


# Export name expected by src.main
router = api_router
