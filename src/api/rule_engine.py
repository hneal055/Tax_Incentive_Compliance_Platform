from __future__ import annotations

import logging
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from src.rule_engine.engine import evaluate
from src.rule_engine.models import EvaluateRequest, EvaluateResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/rule-engine", tags=["Rule Engine"])


@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate_rule_engine(req: EvaluateRequest) -> EvaluateResponse:
    """
    Evaluate a production + expenses against the jurisdiction's tax incentive rule.

    Canonical rule lookup:
      - rules/<CODE>.json via src.rule_engine.registry

    Errors:
      - 404 if rule file is missing for requested jurisdiction
      - 422 if request validation fails (handled by FastAPI/Pydantic)
      - 500 for unexpected errors
    """
    try:
        return evaluate(req)

    except FileNotFoundError as e:
        # Unknown jurisdiction rule file (canonical behavior)
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except ValidationError as e:
        logger.exception("Rule engine response validation error")
        raise HTTPException(status_code=500, detail="Rule engine response schema invalid")

    except Exception as e:
        logger.exception("Unhandled rule engine error")
        raise HTTPException(status_code=500, detail="Internal Server Error")