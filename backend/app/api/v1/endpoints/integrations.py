"""Largo + PilotForge integration endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
import json
from datetime import datetime

from app.db.session import get_db
from app.models.jurisdiction import Jurisdiction
from app.models.program import Program

router = APIRouter(prefix="/integrations", tags=["integrations"])


# ─── Pydantic Schemas ─────────────────────────────────────────────────────────

class LargoProjectData(BaseModel):
    project_name: str = Field(..., example="The Last Frontier")
    genre: str = Field(..., example="Drama")
    budget: float = Field(..., gt=0, example=2500000)
    locations: List[str] = Field(..., example=["Georgia", "Atlanta"])
    audience_score: Optional[float] = Field(None, ge=0, le=100, example=78.5)
    include_logo: Optional[bool] = Field(False, description="Include promotional logo for bonus")
    local_hire_pct: Optional[float] = Field(0.0, ge=0, le=1, description="Fraction of crew that are local residents")
    diversity_score: Optional[float] = Field(0.0, ge=0, le=1, description="Diversity score for key creative roles")


class IncentiveRecommendation(BaseModel):
    jurisdiction: str
    program_name: str
    program_id: str
    estimated_credit: float
    credit_rate: float
    qualified_spend: float
    qualified_categories: List[str]
    bonuses_applied: List[dict]
    pre_application_checklist: List[dict]
    audit_readiness_score: int
    eligible: bool
    ineligibility_reason: Optional[str] = None
    transferable: bool
    sunset_date: Optional[str] = None


class LargoIntegrationResponse(BaseModel):
    project_name: str
    genre: str
    budget: float
    locations: List[str]
    audience_score: Optional[float]
    recommendations: List[IncentiveRecommendation]
    total_estimated_credits: float
    generated_at: str


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _location_matches(locations: List[str], jurisdiction_name: str) -> bool:
    """Check if any of the project locations match a jurisdiction."""
    jur_lower = jurisdiction_name.lower()
    return any(jur_lower in loc.lower() or loc.lower() in jur_lower for loc in locations)


def _evaluate_program(
    program: Program,
    jurisdiction: Jurisdiction,
    data: LargoProjectData,
) -> IncentiveRecommendation:
    """Evaluate a program against project data and return a recommendation."""
    rules = {}
    if program.rules:
        try:
            rules = json.loads(program.rules) if isinstance(program.rules, str) else program.rules
        except Exception:
            rules = {}

    base_rate: float = rules.get("base_credit_rate", 0.0)
    qualified_spend = data.budget * 0.80  # Assume 80% of budget qualifies
    bonuses_applied: List[dict] = []
    ineligibility_reason: Optional[str] = None
    eligible = True

    # ── Eligibility checks ────────────────────────────────────────────────────
    min_reqs: List[dict] = rules.get("minimum_requirements", [])
    for req in min_reqs:
        req_id = req.get("id", "")
        if req_id == "min_spend" and qualified_spend < 500_000:
            eligible = False
            ineligibility_reason = req.get("message", "Minimum spend not met")
        if req_id == "georgia_filming" and not _location_matches(data.locations, jurisdiction.name):
            eligible = False
            ineligibility_reason = req.get(
                "message", f"Must film in {jurisdiction.name}"
            )

    # ── Bonus logic ───────────────────────────────────────────────────────────
    effective_rate = base_rate

    if eligible:
        # Promotional logo bonus
        for bonus in rules.get("bonus_conditions", []):
            if bonus.get("id") == "promotional_logo" and data.include_logo:
                rate = bonus.get("rate", 0.0)
                effective_rate += rate
                bonuses_applied.append({
                    "name": bonus.get("name", "Promotional Logo"),
                    "rate": rate,
                    "amount": qualified_spend * rate,
                })

        # Local hire bonus
        local_hire = rules.get("local_hire_bonus", {})
        if local_hire and (data.local_hire_pct or 0) >= local_hire.get("threshold", 1.0):
            rate = local_hire.get("rate", 0.0)
            effective_rate += rate
            bonuses_applied.append({
                "name": "Local Hire Bonus",
                "rate": rate,
                "amount": qualified_spend * rate,
            })

        # Diversity bonus
        diversity = rules.get("diversity_bonus", {})
        if diversity and (data.diversity_score or 0) >= diversity.get("threshold", 1.0):
            rate = diversity.get("rate", 0.0)
            effective_rate += rate
            bonuses_applied.append({
                "name": "Diversity Bonus",
                "rate": rate,
                "amount": qualified_spend * rate,
            })

    estimated_credit = qualified_spend * effective_rate if eligible else 0.0

    # ── Transferability ───────────────────────────────────────────────────────
    transferability = rules.get("transferability", {})
    transferable: bool = transferability.get("allowed", False)

    return IncentiveRecommendation(
        jurisdiction=jurisdiction.name,
        program_name=program.name,
        program_id=str(program.id),
        estimated_credit=round(estimated_credit, 2),
        credit_rate=round(effective_rate, 4),
        qualified_spend=round(qualified_spend, 2),
        qualified_categories=rules.get("qualified_expenditure_categories", []),
        bonuses_applied=bonuses_applied,
        pre_application_checklist=rules.get("checklist", []),
        audit_readiness_score=85,  # Placeholder for demo
        eligible=eligible,
        ineligibility_reason=ineligibility_reason,
        transferable=transferable,
        sunset_date=rules.get("sunset_date"),
    )


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/largo/project", response_model=LargoIntegrationResponse)
async def evaluate_largo_project(
    data: LargoProjectData,
    db: Session = Depends(get_db),
):
    """
    Accept project metadata from Largo and return incentive recommendations.

    Evaluates all active programs against the project's budget, locations,
    and optional parameters (logo, local hire, diversity score).
    """
    # Fetch all active programs with their jurisdictions
    programs = (
        db.query(Program, Jurisdiction)
        .join(Jurisdiction, Program.jurisdiction_id == Jurisdiction.id)
        .filter(Program.active == True)
        .all()
    )

    if not programs:
        raise HTTPException(status_code=404, detail="No active incentive programs found")

    recommendations: List[IncentiveRecommendation] = []
    for program, jurisdiction in programs:
        rec = _evaluate_program(program, jurisdiction, data)
        recommendations.append(rec)

    # Sort by estimated credit descending (eligible first)
    recommendations.sort(key=lambda r: (r.eligible, r.estimated_credit), reverse=True)

    total = sum(r.estimated_credit for r in recommendations if r.eligible)

    return LargoIntegrationResponse(
        project_name=data.project_name,
        genre=data.genre,
        budget=data.budget,
        locations=data.locations,
        audience_score=data.audience_score,
        recommendations=recommendations,
        total_estimated_credits=round(total, 2),
        generated_at=datetime.utcnow().isoformat() + "Z",
    )


@router.get("/largo/demo-payload")
async def get_demo_payload():
    """Return a sample Largo project payload for testing."""
    return {
        "project_name": "Peach State Chronicles",
        "genre": "Drama",
        "budget": 2500000,
        "locations": ["Georgia", "Atlanta", "Savannah"],
        "audience_score": 78.5,
        "include_logo": True,
        "local_hire_pct": 0.20,
        "diversity_score": 0.25,
    }
