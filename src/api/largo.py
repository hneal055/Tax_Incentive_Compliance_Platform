"""
Largo / MMB Connector integration endpoint.
Accepts a project submission and returns incentive analysis.
"""
import logging
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from src.utils.database import prisma

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/integrations", tags=["Integrations"])


class LargoProject(BaseModel):
    title: str
    production_type: Optional[str] = "feature_film"
    budget_total: Optional[float] = 0
    budget_qualifying: Optional[float] = None
    jurisdictions: Optional[List[str]] = []
    start_date: Optional[str] = None
    production_company: Optional[str] = None


@router.post("/largo/project", summary="Evaluate a project from Largo or MMB Connector")
async def evaluate_largo_project(project: LargoProject):
    jurisdiction_codes = [j.upper() for j in (project.jurisdictions or [])]
    if not jurisdiction_codes:
        all_j = await prisma.jurisdiction.find_many(where={"active": True}, order={"name": "asc"})
        jurisdiction_codes = [j.code for j in all_j]

    results = []
    for code in jurisdiction_codes:
        j = await prisma.jurisdiction.find_first(
            where={"OR": [{"code": code}, {"name": {"contains": code}}], "active": True}
        )
        if not j:
            continue
        rules = await prisma.incentiverule.find_many(
            where={"jurisdictionId": j.id, "active": True},
            order={"percentage": "desc"}
        )
        if not rules:
            continue
        top_rule = rules[0]
        qualifying = project.budget_qualifying or (project.budget_total * 0.8 if project.budget_total else 0)
        rate = (top_rule.percentage or 0) / 100
        max_credit = top_rule.maxCredit
        estimated_credit = qualifying * rate
        if max_credit:
            estimated_credit = min(estimated_credit, max_credit)
        min_spend = top_rule.minSpend or 0
        qualifies = qualifying >= min_spend if min_spend else True
        results.append({
            "jurisdiction_id": j.id,
            "jurisdiction_name": j.name,
            "jurisdiction_code": j.code,
            "country": j.country,
            "website": j.website,
            "top_rule": {
                "name": top_rule.ruleName,
                "code": top_rule.ruleCode,
                "incentive_type": top_rule.incentiveType,
                "percentage": top_rule.percentage,
                "min_spend": top_rule.minSpend,
                "max_credit": top_rule.maxCredit,
            },
            "analysis": {
                "budget_total": project.budget_total,
                "budget_qualifying": qualifying,
                "estimated_credit": round(estimated_credit, 2),
                "effective_rate": round(estimated_credit / project.budget_total * 100, 2) if project.budget_total else 0,
                "meets_minimum_spend": qualifies,
                "recommendation": "Strong candidate" if qualifies and estimated_credit > 0 else "Does not qualify",
            }
        })

    results.sort(key=lambda x: x["analysis"]["estimated_credit"], reverse=True)

    return {
        "project": {
            "title": project.title,
            "production_type": project.production_type,
            "budget_total": project.budget_total,
            "budget_qualifying": project.budget_qualifying,
            "production_company": project.production_company,
        },
        "total_jurisdictions_analyzed": len(results),
        "top_recommendation": results[0] if results else None,
        "all_results": results,
        "powered_by": "PilotForge Rules Engine v1 — Scene Reader Studio Technologies LLC"
    }
