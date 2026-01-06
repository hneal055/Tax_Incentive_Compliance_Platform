# writer
$path="src\api\routes.py"; New-Item -ItemType Directory -Force -Path (Split-Path $path) | Out-Null; @'
"""
API route registry

- Central place to mount versioned routers.
- Safe-import optional modules (so the API can boot while phases build out).
"""
from __future__ import annotations

import importlib
import logging
from typing import Dict

from fastapi import APIRouter

logger = logging.getLogger(__name__)

api_router = APIRouter()


def _safe_include(module_path: str, attr_name: str = "router") -> bool:
    """
    Import a module and include its router if present.
    Returns True if included; False if missing or failed.
    """
    try:
        mod = importlib.import_module(module_path)
        router = getattr(mod, attr_name, None)
        if router is None:
            logger.warning("Router attr missing, skipping: %s.%s", module_path, attr_name)
            return False

        api_router.include_router(router)
        return True

    except ModuleNotFoundError as e:
        logger.warning("Router module missing, skipping: %s (%s)", module_path, e)
        return False
    except Exception as e:
        logger.exception("Router load failed, skipping: %s (%s)", module_path, e)
        return False


# Core modules (should exist)
_safe_include("src.api.jurisdictions")
_safe_include("src.api.incentive_rules")
_safe_include("src.api.rule_engine")  # POST /rule-engine/evaluate

# Phase modules (may not exist yet)
_safe_include("src.api.calculations")
_safe_include("src.api.productions")
_safe_include("src.api.expenses")
_safe_include("src.api.users")
_safe_include("src.api.audit_logs")


@api_router.get("/")
def index() -> Dict[str, str]:
    """
    Lightweight index for humans + quick smoke tests.
    (Swagger is still at /docs.)
    """
    return {
        "jurisdictions": "/jurisdictions",
        "incentive_rules": "/incentive-rules",
        "rule_engine_evaluate": "/rule-engine/evaluate",
        "calculations": "/calculations",
        "productions": "/productions",
        "expenses": "/expenses",
        "users": "/users",
        "audit_logs": "/audit-logs",
    }


# Export name expected by src.main
router = api_router
'@ | Out-File -FilePath $path -Encoding utf8
