"""
API route registry

Includes routers that exist. Missing modules are skipped to keep dev moving.
"""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()

def _include(module_path: str, mount_router_name: str = "router") -> None:
    try:
        mod = __import__(module_path, fromlist=[mount_router_name])
        sub = getattr(mod, mount_router_name)
        router.include_router(sub)
    except Exception as e:
        print(f"Router module missing, skipping: {module_path} ({e})")

# Core working routes
_include("src.api.jurisdictions")
_include("src.api.incentive_rules")

# Phase 1: Rule Engine MVP
_include("src.api.rule_engine")

# Future modules (only if present)
_include("src.api.calculations")
_include("src.api.productions")
_include("src.api.expenses")
_include("src.api.audit_logs")
_include("src.api.users")
