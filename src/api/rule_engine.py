"""
Rule Engine API (MVP)
POST /api/v1/rule-engine/evaluate
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.rule_engine.engine import evaluate
from src.rule_engine.models import EvaluateRequest, EvaluateResponse


router = APIRouter(prefix="/rule-engine", tags=["Rule Engine"])


@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_rule_engine(payload: EvaluateRequest) -> EvaluateResponse:
    try:
        return evaluate(payload)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rule evaluation failed: {e}")
