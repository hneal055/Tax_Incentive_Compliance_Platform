"""
/maximize  —  PilotForge Incentive Maximizer API
=================================================
Resolves jurisdiction layers from a lat/lng or explicit codes,
applies the local_rules stacking engine, and returns a fully-broken-
down incentive package.

Routes
------
POST /maximize          Full maximize (lat/lng or codes + spend)
GET  /maximize/lookup   Resolve which jurisdictions a point falls in
"""

from typing import List, Optional
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.utils.database import prisma
from maximizer import PilotForgeMaximizer

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/maximize", tags=["Maximizer"])

_engine = None

def _get_engine() -> PilotForgeMaximizer:
    global _engine
    if _engine is None:
        _engine = PilotForgeMaximizer()
    return _engine


# ── Request / Response models ─────────────────────────────────────────────────

class MaximizeRequest(BaseModel):
    lat: Optional[float] = Field(None, description="Latitude (WGS-84)")
    lng: Optional[float] = Field(None, description="Longitude (WGS-84)")
    jurisdiction_codes: Optional[List[str]] = Field(
        None, description="Explicit jurisdiction codes (overrides lat/lng)"
    )
    project_type: str = Field("all", description="Project type filter (e.g. 'film', 'solar')")
    qualified_spend: Optional[float] = Field(
        None, description="Qualified production spend in USD — enables real dollar calculation"
    )
    spend_by_location: Optional[dict] = Field(
        None,
        description=(
            "Per-jurisdiction qualifying spend (CODE → USD). "
            "Rules for a jurisdiction use its entry instead of qualified_spend. "
            "Useful for split-location shoots where a city/county bonus "
            "(e.g. IL-CHICAGO-BONUS) should only apply to Chicago-local spend. "
            "Example: {\"IL\": 5000000, \"IL-COOK\": 2000000}"
        ),
    )


class RuleDetail(BaseModel):
    jurisdiction_name: str
    rule_key: str
    rule_type: str
    raw_value: float
    value_unit: str
    computed_value: float


class MaximizeResponse(BaseModel):
    resolved_state: Optional[str]
    jurisdictions_evaluated: int
    qualified_spend: Optional[float]
    total_incentive_usd: float
    effective_rate: Optional[float]
    breakdown: dict
    applied_rules: List[RuleDetail]
    overridden_rules: List[RuleDetail]
    warnings: List[str]
    recommendations: List[str]


class LookupResponse(BaseModel):
    resolved_state: Optional[str]
    jurisdictions: List[dict]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _to_rule_detail(r) -> RuleDetail:
    return RuleDetail(
        jurisdiction_name=r.jurisdiction_name,
        rule_key=r.rule_key,
        rule_type=r.rule_type,
        raw_value=r.raw_value,
        value_unit=r.value_unit,
        computed_value=r.computed_value,
    )


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("", response_model=MaximizeResponse)
async def maximize(req: MaximizeRequest):
    """
    Return the optimal incentive stack for a location or jurisdiction list.

    - Provide **lat + lng** to auto-resolve US state + sub-jurisdictions.
    - Provide **jurisdiction_codes** to target specific jurisdictions.
    - Add **qualified_spend** to convert percentage rules to real dollar values.
    """
    if req.jurisdiction_codes is None and (req.lat is None or req.lng is None):
        raise HTTPException(
            status_code=422,
            detail="Provide either lat+lng or jurisdiction_codes",
        )

    try:
        engine = _get_engine()
        result = engine.maximize(
            lat=req.lat,
            lng=req.lng,
            jurisdiction_codes=req.jurisdiction_codes,
            project_type=req.project_type,
            qualified_spend=req.qualified_spend,
            spend_by_location=req.spend_by_location,
        )
    except Exception as exc:
        logger.error(f"Maximizer error: {exc}")
        raise HTTPException(status_code=500, detail=f"Maximizer error: {exc}")

    return MaximizeResponse(
        resolved_state=result.resolved_state,
        jurisdictions_evaluated=result.jurisdictions_evaluated,
        qualified_spend=result.qualified_spend,
        total_incentive_usd=result.total_incentive_usd,
        effective_rate=result.effective_rate,
        breakdown=result.breakdown,
        applied_rules=[_to_rule_detail(r) for r in result.applied_rules],
        overridden_rules=[_to_rule_detail(r) for r in result.overridden_rules],
        warnings=result.warnings,
        recommendations=result.recommendations,
    )


@router.get("/lookup", response_model=LookupResponse)
async def lookup_jurisdictions(lat: float, lng: float):
    """
    Resolve which jurisdictions (state + sub-jurisdictions) contain a point.
    Useful for populating jurisdiction selectors in the frontend.
    """
    try:
        engine = _get_engine()
        jurisdictions, state_code = engine.resolve_jurisdictions_by_location(lat, lng)
    except Exception as exc:
        logger.error(f"Lookup error: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))

    return LookupResponse(
        resolved_state=state_code,
        jurisdictions=[
            {"id": j["id"], "name": j["name"], "code": j["code"], "type": j["type"]}
            for j in jurisdictions
        ],
    )
