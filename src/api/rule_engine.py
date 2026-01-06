"""
Rule Engine API routes

POST /api/v1/rule-engine/evaluate
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

from src.rule_engine.engine import evaluate
from src.rule_engine.models import EvaluateRequest, EvaluateResponse

router = APIRouter(prefix="/rule-engine", tags=["Rule Engine"])


class EvaluateRequestPayload(BaseModel):
    """
    Wrapper payload to keep the API stable even if your internal models evolve.

    Accepts either:
      - {"jurisdiction_code": "...", "expenses": [...], ...}  (direct fields)
      - {"request": {...}}                                   (wrapped)
    """
    request: Dict[str, Any] | None = None

    # Allow passthrough of direct fields
    jurisdiction_code: str | None = None
    production: Any | None = None
    production_start_date: Any | None = None
    expenses: Any | None = None


def _normalize_payload(payload: EvaluateRequestPayload) -> Dict[str, Any]:
    if payload.request is not None:
        return payload.request

    # Build dict from direct fields
    d: Dict[str, Any] = {}
    if payload.jurisdiction_code is not None:
        d["jurisdiction_code"] = payload.jurisdiction_code
    if payload.production is not None:
        d["production"] = payload.production
    if payload.production_start_date is not None:
        d["production_start_date"] = payload.production_start_date
    if payload.expenses is not None:
        d["expenses"] = payload.expenses
    return d


@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate_rule_engine(payload: EvaluateRequestPayload) -> EvaluateResponse:
    """
    Evaluate a jurisdiction rule against submitted expenses.
    """
    data = _normalize_payload(payload)

    try:
        req = EvaluateRequest.model_validate(data)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid request: {e}")

    try:
        return evaluate(req)
    except FileNotFoundError as e:
        # Unknown jurisdiction rule file
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        # Unknown jurisdiction / invalid rule data
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {e}")
