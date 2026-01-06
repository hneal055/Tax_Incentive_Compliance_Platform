"""
Rule Engine API

Contract stability (default response):
  Always returns:
    - jurisdiction_code
    - total_eligible_spend
    - total_incentive_amount
    - breakdown[]

Payload tightening:
  - No large trace/meta unless explicitly requested via ?debug=true

Error mapping:
  - Unknown jurisdiction / rule file -> 404
  - Bad request payload -> 422 (FastAPI validation)
  - Engine runtime error -> 500 (safe message)
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src.rule_engine.engine import evaluate
from src.rule_engine.models import EvaluateRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/rule-engine", tags=["Rule Engine"])


class BreakdownItem(BaseModel):
    # Keep this aligned with what your engine produces
    rule_id: str
    rule_name: str
    rule_type: str

    eligible_spend: Any
    rate: Any
    raw_amount: Any
    applied_amount: Any

    capped: bool
    cap_amount: Any

    skipped: bool
    skip_reason: Optional[str] = None


class EvaluateStableResponse(BaseModel):
    jurisdiction_code: str
    total_eligible_spend: Any
    total_incentive_amount: Any
    breakdown: List[BreakdownItem]

    # Optional debug bundle (only returned when ?debug=true)
    debug: Optional[Dict[str, Any]] = None


@router.post("/evaluate", response_model=EvaluateStableResponse)
def evaluate_rule_engine(
    req: EvaluateRequest,
    debug: bool = Query(False, description="Include debug fields (trace/meta/warnings). Off by default."),
) -> Dict[str, Any]:
    code = (getattr(req, "jurisdiction_code", "") or "").strip().upper()

    try:
        res = evaluate(req)

        # Tight, stable default payload
        payload: Dict[str, Any] = {
            "jurisdiction_code": getattr(res, "jurisdiction_code", code),
            "total_eligible_spend": getattr(res, "total_eligible_spend", 0),
            "total_incentive_amount": getattr(res, "total_incentive_amount", 0),
            "breakdown": [
                (b.model_dump() if hasattr(b, "model_dump") else dict(b))  # type: ignore[arg-type]
                for b in (getattr(res, "breakdown", []) or [])
            ],
        }

        if debug:
            payload["debug"] = {
                "warnings": getattr(res, "warnings", None),
                "meta": getattr(res, "meta", None),
                "trace": getattr(res, "trace", None),
                "compliance_flags": getattr(res, "compliance_flags", None),
            }

        return payload

    except FileNotFoundError:
        # Clean 404 (no filesystem path leakage)
        raise HTTPException(status_code=404, detail=f"Rule not found for jurisdiction '{code}'")

    except HTTPException:
        # If something upstream already raised one, pass through
        raise

    except Exception as e:
        logger.exception("Unhandled rule engine error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
