"""Largo + SceneIQ integration endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
import json
from datetime import datetime
import uuid

from app.db.session import get_db
from app.models.jurisdiction import Jurisdiction
from app.models.program import Program
from app.models.largo_project import LargoProject

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
    film_lease_partner: Optional[bool] = Field(False, description="Project qualifies as a film-lease production company in a designated facility")


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

class MaximumPossibleCreditSummary(BaseModel):
    jurisdiction: str
    program_name: str
    program_id: str
    base_credit_rate: float
    maximum_credit_rate: float
    maximum_credit_percent: float
    qualified_spend_assumption: Optional[float] = None
    maximum_credit_amount: Optional[float] = None
    required_conditions: List[str]
    stackable_components: List[dict]
    additional_benefits: List[dict]


class MaximumPossibleCreditResponse(BaseModel):
    summaries: List[MaximumPossibleCreditSummary]
    best_case_headline: Optional[str] = None
    generated_at: str

# ─── Helpers ──────────────────────────────────────────────────────────────────

def _location_matches(locations: List[str], jurisdiction_name: str) -> bool:
    """Check if any of the project locations match a jurisdiction."""
    jur_lower = jurisdiction_name.lower()
    return any(jur_lower in loc.lower() or loc.lower() in jur_lower for loc in locations)


def _parse_json_maybe(value):
    """Parse a JSON string if needed, otherwise return value as-is."""
    if value is None:
        return None
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return None
    return value



def _compute_maximum_possible_credit(program: Program, jurisdiction: Jurisdiction, budget: Optional[float] = None) -> MaximumPossibleCreditSummary:
    """Compute a best-case credit summary by stacking all additive credit components."""
    rules = {}
    if program.rules:
        try:
            rules = json.loads(program.rules) if isinstance(program.rules, str) else program.rules
        except Exception:
            rules = {}

    base_rate = float(rules.get("base_credit_rate", 0.0) or 0.0)
    maximum_rate = base_rate

    required_conditions: List[str] = []
    stackable_components: List[dict] = [
        {
            "name": "Base Credit",
            "rate": round(base_rate, 4),
            "percent": round(base_rate * 100, 2),
            "condition": f"Project must include filming in {jurisdiction.name}",
        }
    ]

    min_reqs = rules.get("minimum_requirements", []) or []
    for req in min_reqs:
        msg = req.get("message")
        if msg:
            required_conditions.append(msg)

    for bonus in rules.get("bonus_conditions", []) or []:
        rate = float(bonus.get("rate", 0.0) or 0.0)
        if rate <= 0:
            continue

        maximum_rate += rate
        condition_text = bonus.get("description") or bonus.get("condition") or "Bonus qualification required"
        required_conditions.append(condition_text)
        stackable_components.append(
            {
                "name": bonus.get("name", bonus.get("id", "Bonus")),
                "rate": round(rate, 4),
                "percent": round(rate * 100, 2),
                "condition": condition_text,
            }
        )

    local_hire = rules.get("local_hire_bonus", {}) or {}
    local_hire_rate = float(local_hire.get("rate", 0.0) or 0.0)
    if local_hire_rate > 0:
        maximum_rate += local_hire_rate
        condition_text = local_hire.get("description") or local_hire.get("condition") or "Local hire threshold required"
        required_conditions.append(condition_text)
        stackable_components.append(
            {
                "name": "Local Hire Bonus",
                "rate": round(local_hire_rate, 4),
                "percent": round(local_hire_rate * 100, 2),
                "condition": condition_text,
            }
        )

    diversity = rules.get("diversity_bonus", {}) or {}
    diversity_rate = float(diversity.get("rate", 0.0) or 0.0)
    if diversity_rate > 0:
        maximum_rate += diversity_rate
        condition_text = diversity.get("description") or diversity.get("condition") or "Diversity threshold required"
        required_conditions.append(condition_text)
        stackable_components.append(
            {
                "name": "Diversity Bonus",
                "rate": round(diversity_rate, 4),
                "percent": round(diversity_rate * 100, 2),
                "condition": condition_text,
            }
        )

    additional_benefits: List[dict] = []
    sales_tax_exemption = rules.get("sales_tax_exemption") or {}
    if isinstance(sales_tax_exemption, dict) and sales_tax_exemption:
        additional_benefits.append(
            {
                "type": "sales_tax_exemption",
                "rate": sales_tax_exemption.get("rate"),
                "description": sales_tax_exemption.get("description"),
            }
        )

    qualified_spend_assumption = None
    maximum_credit_amount = None
    if budget is not None:
        qualified_spend_assumption = round(budget * 0.80, 2)
        maximum_credit_amount = round(qualified_spend_assumption * maximum_rate, 2)

    deduped_conditions = list(dict.fromkeys([c for c in required_conditions if c]))

    return MaximumPossibleCreditSummary(
        jurisdiction=jurisdiction.name,
        program_name=program.name,
        program_id=str(program.id),
        base_credit_rate=round(base_rate, 4),
        maximum_credit_rate=round(maximum_rate, 4),
        maximum_credit_percent=round(maximum_rate * 100, 2),
        qualified_spend_assumption=qualified_spend_assumption,
        maximum_credit_amount=maximum_credit_amount,
        required_conditions=deduped_conditions,
        stackable_components=stackable_components,
        additional_benefits=additional_benefits,
    )

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
        if (req_id.endswith("_filming") or req.get("rule_type") == "location") and not _location_matches(data.locations, jurisdiction.name):
            eligible = False
            ineligibility_reason = req.get(
                "message", f"Must film in {jurisdiction.name}"
            )

    # ── Bonus logic ───────────────────────────────────────────────────────────
    effective_rate = base_rate

    if eligible:
        # Generic bonus handling so jurisdiction-specific rule variants can be encoded in JSON.
        for bonus in rules.get("bonus_conditions", []):
            bonus_id = bonus.get("id")
            applies_to = bonus.get("applies_to")
            rate = bonus.get("rate", 0.0)

            if bonus_id == "promotional_logo" and data.include_logo:
                effective_rate += rate
                bonuses_applied.append({
                    "name": bonus.get("name", "Promotional Logo"),
                    "rate": rate,
                    "amount": qualified_spend * rate,
                })
                continue

            if applies_to == "sub_jurisdiction":
                locations = bonus.get("locations", [])
                if any(_location_matches(data.locations, loc) for loc in locations):
                    effective_rate += rate
                    bonuses_applied.append({
                        "name": bonus.get("name", "Sub-Jurisdiction Bonus"),
                        "rate": rate,
                        "amount": qualified_spend * rate,
                    })
                continue

            if applies_to == "film_lease_partner" and (data.film_lease_partner or False):
                effective_rate += rate
                bonuses_applied.append({
                    "name": bonus.get("name", "Film-Lease Partner Bonus"),
                    "rate": rate,
                    "amount": qualified_spend * rate,
                })
                continue

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

    response = LargoIntegrationResponse(
        project_name=data.project_name,
        genre=data.genre,
        budget=data.budget,
        locations=data.locations,
        audience_score=data.audience_score,
        recommendations=recommendations,
        total_estimated_credits=round(total, 2),
        generated_at=datetime.utcnow().isoformat() + "Z",
    )

    # Persist inbound request + computed response for UI history and analytics.
    try:
        submission = LargoProject(
            id=str(uuid.uuid4()),
            project_name=data.project_name,
            largo_data=json.dumps(data.model_dump()),
            incentive_recommendations=json.dumps(response.model_dump()),
        )
        db.add(submission)
        db.commit()
    except Exception:
        db.rollback()

    return response


@router.get("/largo/project-history")
async def get_project_history(
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Return recent unique project names submitted through the integration."""
    rows = (
        db.query(LargoProject.project_name)
        .order_by(LargoProject.created_at.desc())
        .limit(limit * 5)
        .all()
    )

    seen = set()
    projects: List[str] = []
    for (name,) in rows:
        if not name:
            continue
        key = name.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        projects.append(name.strip())
        if len(projects) >= limit:
            break

    return {"projects": projects}


@router.get("/largo/available-locations")
async def get_available_locations(db: Session = Depends(get_db)):
    """Return selectable locations from jurisdictions and historical submissions."""
    names = set()

    # Jurisdictions from active program config.
    jurisdictions = db.query(Jurisdiction.name).all()
    for (name,) in jurisdictions:
        if name:
            names.add(name.strip())

    # Locations used in prior submissions.
    history = (
        db.query(LargoProject.largo_data)
        .order_by(LargoProject.created_at.desc())
        .limit(300)
        .all()
    )
    for (raw,) in history:
        payload = _parse_json_maybe(raw) or {}
        if isinstance(payload, dict):
            for loc in payload.get("locations", []):
                if isinstance(loc, str) and loc.strip():
                    names.add(loc.strip())

    # Demo defaults for first-run UX.
    for loc in ["Georgia", "Atlanta", "Savannah", "Louisiana", "New Orleans", "Baton Rouge", "New Jersey", "Newark", "Jersey City", "Camden", "Trenton"]:
        names.add(loc)

    return {"locations": sorted(names)}


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

@router.get("/largo/maximum-possible-credit", response_model=MaximumPossibleCreditResponse)
async def get_maximum_possible_credit(
    jurisdiction: Optional[str] = Query(default=None, description="Optional jurisdiction name filter (e.g., New Jersey)"),
    budget: Optional[float] = Query(default=None, gt=0, description="Optional total budget for dollar-denominated maximum estimate"),
    db: Session = Depends(get_db),
):
    """Return best-case stacked credit summaries for active programs."""
    query = (
        db.query(Program, Jurisdiction)
        .join(Jurisdiction, Program.jurisdiction_id == Jurisdiction.id)
        .filter(Program.active == True)
    )

    if jurisdiction:
        q = f"%{jurisdiction.strip().lower()}%"
        query = query.filter(Jurisdiction.name.ilike(q))

    programs = query.all()
    if not programs:
        raise HTTPException(status_code=404, detail="No active incentive programs found")

    summaries = [_compute_maximum_possible_credit(program, jur, budget) for program, jur in programs]
    summaries.sort(key=lambda s: s.maximum_credit_rate, reverse=True)

    best = summaries[0] if summaries else None
    headline = None
    if best:
        has_sales_tax = any(b.get("type") == "sales_tax_exemption" for b in best.additional_benefits)
        headline = f"Up to {best.maximum_credit_percent}%"
        if has_sales_tax:
            headline += " + sales tax exemption"

    return MaximumPossibleCreditResponse(
        summaries=summaries,
        best_case_headline=headline,
        generated_at=datetime.utcnow().isoformat() + "Z",
    )