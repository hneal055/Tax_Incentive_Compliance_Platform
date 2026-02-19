"""
Service layer for Tax Incentive Analysis
"""
import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from src.models.incentive import (
    AnalyzeResponse,
    IncentiveAnalysisResponse,
    IncentiveProgram,
    IncentiveDeadline,
    IncentiveRecommendation,
    JurisdictionIncentiveResponse,
)
from src.models.errors import BudgetNotFoundError, AnalysisNotFoundError
from src.utils.database import prisma

logger = logging.getLogger(__name__)

# Placeholder incentive rules per jurisdiction
JURISDICTION_RULES = {
    "CA": {
        "program_name": "California Film & TV Tax Credit 3.0",
        "credit_rate": 0.25,
        "eligibility_status": "eligible",
        "requirements": [
            "Minimum spend of $1,000,000 in California",
            "Crew list submission required",
            "Application must be submitted before filming begins",
        ],
        "deadline_description": "Application deadline",
        "deadline_offset_days": 90,
    },
    "GA": {
        "program_name": "Georgia Entertainment Industry Investment Act",
        "credit_rate": 0.30,
        "eligibility_status": "eligible",
        "requirements": [
            "Minimum spend of $500,000 in Georgia",
            "At least 50% of production in Georgia",
        ],
        "deadline_description": "Credit certification deadline",
        "deadline_offset_days": 180,
    },
    "NY": {
        "program_name": "New York State Film Tax Credit",
        "credit_rate": 0.25,
        "eligibility_status": "eligible",
        "requirements": [
            "Minimum spend of $1,000,000 in New York",
            "At least 75% of shooting days in New York",
        ],
        "deadline_description": "Application deadline",
        "deadline_offset_days": 60,
    },
}


class IncentiveService:
    """Service for tax incentive analysis"""

    async def analyze_budget(
        self,
        budget_id: str,
        jurisdictions: Optional[List[str]] = None,
    ) -> AnalyzeResponse:
        """Trigger incentive analysis for a budget."""
        budget = await prisma.budget.find_unique(where={"id": budget_id})
        if not budget:
            raise BudgetNotFoundError(budget_id)

        analysis_jurisdictions = jurisdictions or budget.jurisdictions

        # Calculate eligible spend per jurisdiction
        accounts = await prisma.budgetaccount.find_many(
            where={"budgetId": budget_id, "eligibleForIncentives": True}
        )
        total_eligible = sum(a.amount for a in accounts)

        programs = []
        total_benefit = 0.0
        for jur in analysis_jurisdictions:
            rule = JURISDICTION_RULES.get(jur)
            if rule is None:
                continue
            eligible_spend = total_eligible
            estimated_benefit = eligible_spend * rule["credit_rate"]
            total_benefit += estimated_benefit
            deadline_date = datetime.now(timezone.utc) + timedelta(
                days=rule["deadline_offset_days"]
            )
            programs.append(
                {
                    "jurisdiction": jur,
                    "programName": rule["program_name"],
                    "eligibleSpend": eligible_spend,
                    "creditRate": rule["credit_rate"],
                    "estimatedBenefit": estimated_benefit,
                    "eligibilityStatus": rule["eligibility_status"],
                    "requirements": rule["requirements"],
                    "deadlines": [
                        {
                            "type": "application",
                            "date": deadline_date.isoformat(),
                            "description": rule["deadline_description"],
                        }
                    ],
                }
            )

        # Create analysis record
        analysis = await prisma.incentiveanalysis.create(
            data={
                "id": str(uuid.uuid4()),
                "budgetId": budget_id,
                "totalEstimatedBenefit": total_benefit,
                "status": "completed",
            }
        )

        # Create program records
        for program in programs:
            await prisma.incentiveprogram.create(
                data={
                    "id": str(uuid.uuid4()),
                    "analysisId": analysis.id,
                    "jurisdiction": program["jurisdiction"],
                    "programName": program["programName"],
                    "eligibleSpend": program["eligibleSpend"],
                    "creditRate": program["creditRate"],
                    "estimatedBenefit": program["estimatedBenefit"],
                    "eligibilityStatus": program["eligibilityStatus"],
                    "requirements": program["requirements"],
                    "deadlines": program["deadlines"],
                }
            )

        estimated_completion = datetime.now(timezone.utc) + timedelta(minutes=1)
        return AnalyzeResponse(
            analysis_id=analysis.id,
            budget_id=budget_id,
            status="completed",
            estimated_completion=estimated_completion,
        )

    async def get_analysis(self, budget_id: str) -> IncentiveAnalysisResponse:
        """Get the latest incentive analysis for a budget."""
        budget = await prisma.budget.find_unique(where={"id": budget_id})
        if not budget:
            raise BudgetNotFoundError(budget_id)

        analysis = await prisma.incentiveanalysis.find_first(
            where={"budgetId": budget_id},
            order={"analysisDate": "desc"},
            include={"programs": True},
        )
        if not analysis:
            raise AnalysisNotFoundError(budget_id)

        incentives = []
        for p in (analysis.programs or []):
            raw_deadlines = p.deadlines or []
            deadlines = []
            for d in raw_deadlines:
                try:
                    deadlines.append(
                        IncentiveDeadline(
                            type=d.get("type", ""),
                            date=datetime.fromisoformat(d["date"]),
                            description=d.get("description", ""),
                        )
                    )
                except (ValueError, KeyError) as exc:
                    logger.warning(
                        "Skipping deadline with invalid date in program %s: %s",
                        p.id,
                        exc,
                    )
            incentives.append(
                IncentiveProgram(
                    jurisdiction=p.jurisdiction,
                    program_name=p.programName,
                    eligible_spend=p.eligibleSpend,
                    credit_rate=p.creditRate,
                    estimated_benefit=p.estimatedBenefit,
                    eligibility_status=p.eligibilityStatus,
                    requirements=p.requirements,
                    deadlines=deadlines,
                )
            )

        recommendations = []
        if analysis.totalEstimatedBenefit > 0:
            recommendations.append(
                IncentiveRecommendation(
                    type="optimization",
                    description="Review eligible expense categories to maximize qualifying spend",
                    potential_additional_benefit=analysis.totalEstimatedBenefit * 0.05,
                )
            )

        return IncentiveAnalysisResponse(
            budget_id=budget_id,
            analysis_date=analysis.analysisDate,
            total_estimated_benefit=analysis.totalEstimatedBenefit,
            incentives=incentives,
            recommendations=recommendations,
        )

    async def get_jurisdiction_incentive(
        self, budget_id: str, jurisdiction: str
    ) -> JurisdictionIncentiveResponse:
        """Get incentive analysis for a specific jurisdiction."""
        analysis_response = await self.get_analysis(budget_id)
        matching = [i for i in analysis_response.incentives if i.jurisdiction == jurisdiction]
        if not matching:
            return JurisdictionIncentiveResponse(
                budget_id=budget_id,
                jurisdiction=jurisdiction,
                analysis_date=analysis_response.analysis_date,
                incentive=None,
                message=f"No incentive data found for jurisdiction {jurisdiction}",
            )
        return JurisdictionIncentiveResponse(
            budget_id=budget_id,
            jurisdiction=jurisdiction,
            analysis_date=analysis_response.analysis_date,
            incentive=matching[0],
        )


incentive_service = IncentiveService()
