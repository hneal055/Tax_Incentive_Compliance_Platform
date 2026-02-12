"""
Reports API endpoints - PDF Report Generation
Enhanced multi-page professional reports
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from datetime import datetime
import json

from src.models.report import (
    GenerateComparisonReportRequest,
    GenerateComplianceReportRequest,
    GenerateScenarioReportRequest,
    ReportResponse,
)
from src.utils.database import prisma
from src.utils.pdf_generator import pdf_generator
from src.utils.pdf_generator_enhanced import enhanced_pdf_generator

router = APIRouter(prefix="/reports", tags=["Reports"])


def parse_json_field(field):
    """Parse JSON field that might be string or dict"""
    if isinstance(field, str):
        try:
            return json.loads(field)
        except Exception:
            return {}
    return field if field else {}


@router.post("/comparison", summary="Generate jurisdiction comparison PDF report")
async def generate_comparison_report(request: GenerateComparisonReportRequest):
    """
    Generate a professional 4-page PDF report comparing tax incentives across multiple jurisdictions.

    Returns a downloadable PDF with:
    - Page 1: Executive summary and recommended location
    - Page 2: Detailed jurisdiction analysis with program specifics
    - Page 3: Requirements & eligibility criteria for each location
    - Page 4: Recommendations, action plan, and next steps
    """
    jurisdictions = await prisma.jurisdiction.find_many(
        where={"id": {"in": request.jurisdictionIds}}
    )
    if len(jurisdictions) != len(request.jurisdictionIds):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more jurisdictions not found",
        )

    comparisons = []
    for jurisdiction in jurisdictions:
        rules = await prisma.incentiverule.find_many(
            where={"jurisdictionId": jurisdiction.id, "active": True}
        )
        if not rules:
            continue
        best_credit = 0
        best_rule = None
        for rule in rules:
            if rule.percentage:
                credit = request.budget * (rule.percentage / 100)
            elif rule.fixedAmount:
                credit = rule.fixedAmount
            else:
                credit = 0

            if rule.minSpend and request.budget < rule.minSpend:
                credit = 0
            if rule.maxCredit and credit > rule.maxCredit:
                credit = rule.maxCredit
            if credit > best_credit:
                best_credit = credit
                best_rule = rule

        if best_rule:
            comparisons.append(
                {
                    "jurisdiction": jurisdiction.name,
                    "jurisdictionId": jurisdiction.id,
                    "ruleName": best_rule.ruleName,
                    "ruleCode": best_rule.ruleCode,
                    "incentiveType": best_rule.incentiveType,
                    "percentage": best_rule.percentage,
                    "estimatedCredit": best_credit,
                    "rank": 0,  # Will be set after sorting
                }
            )

    comparisons.sort(key=lambda x: x["estimatedCredit"], reverse=True)
    for i, comp in enumerate(comparisons):
        comp["rank"] = i + 1
    if not comparisons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No applicable incentive programs found for the selected jurisdictions",
        )
    best_option = comparisons[0]

    pdf_bytes = enhanced_pdf_generator.generate_comparison_report(
        production_title=request.productionTitle,
        budget=request.budget,
        comparisons=comparisons,
        best_option=best_option,
    )
    filename = f"comparison_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.post("/compliance", summary="Generate compliance verification PDF report")
async def generate_compliance_report(request: GenerateComplianceReportRequest):
    """
    Generate a professional PDF report verifying production compliance with incentive requirements.

    Returns a downloadable PDF with:
    - Compliance status
    - Requirements checklist with pass/fail indicators
    - Detailed verification of each requirement
    - Action items for achieving compliance
    """
    rule = await prisma.incentiverule.find_unique(where={"id": request.ruleId})
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incentive rule not found"
        )

    jurisdiction = await prisma.jurisdiction.find_unique(
        where={"id": rule.jurisdictionId}
    )
    if not jurisdiction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Jurisdiction not found"
        )

    requirements_data = parse_json_field(rule.requirements)
    requirement_checks = []
    requirements_met = 0
    requirements_not_met = 0

    # Minimum spend
    if rule.minSpend:
        if request.productionBudget >= rule.minSpend:
            requirement_checks.append(
                {
                    "requirement": "minimum_spend",
                    "description": f"Minimum spend of ${rule.minSpend:,.0f}",
                    "status": "met",
                }
            )
            requirements_met += 1
        else:
            requirement_checks.append(
                {
                    "requirement": "minimum_spend",
                    "description": f"Minimum spend of ${rule.minSpend:,.0f}",
                    "status": "not_met",
                }
            )
            requirements_not_met += 1

    # Shoot days
    if "minShootDays" in requirements_data and getattr(request, "shootDays", None):
        min_days = requirements_data["minShootDays"]
        if request.shootDays >= min_days:
            requirement_checks.append(
                {
                    "requirement": "shoot_days",
                    "description": f"Minimum {min_days} shoot days",
                    "status": "met",
                }
            )
            requirements_met += 1
        else:
            requirement_checks.append(
                {
                    "requirement": "shoot_days",
                    "description": f"Minimum {min_days} shoot days",
                    "status": "not_met",
                }
            )
            requirements_not_met += 1

    # Local hiring
    local_hire_keys = ["californiaResidents", "georgiaResident", "localHirePercentage"]
    for key in local_hire_keys:
        if (
            key in requirements_data
            and getattr(request, "localHirePercentage", None) is not None
        ):
            required_pct = requirements_data[key]
            if request.localHirePercentage >= required_pct:
                requirement_checks.append(
                    {
                        "requirement": "local_hiring",
                        "description": f"Minimum {required_pct}% local hiring",
                        "status": "met",
                    }
                )
                requirements_met += 1
            else:
                requirement_checks.append(
                    {
                        "requirement": "local_hiring",
                        "description": f"Minimum {required_pct}% local hiring",
                        "status": "not_met",
                    }
                )
                requirements_not_met += 1
            break

    # Promo logo
    if (
        "georgiaPromo" in requirements_data or "logoInCredits" in requirements_data
    ) and hasattr(request, "hasPromoLogo"):
        if request.hasPromoLogo:
            requirement_checks.append(
                {
                    "requirement": "promotional_logo",
                    "description": "Include jurisdiction logo in credits",
                    "status": "met",
                }
            )
            requirements_met += 1
        else:
            requirement_checks.append(
                {
                    "requirement": "promotional_logo",
                    "description": "Include jurisdiction logo in credits",
                    "status": "not_met",
                }
            )
            requirements_not_met += 1

    # Cultural test
    if "culturalTest" in requirements_data and hasattr(request, "hasCulturalTest"):
        if request.hasCulturalTest:
            requirement_checks.append(
                {
                    "requirement": "cultural_test",
                    "description": "Pass cultural test for content",
                    "status": "met",
                }
            )
            requirements_met += 1
        else:
            requirement_checks.append(
                {
                    "requirement": "cultural_test",
                    "description": "Pass cultural test for content",
                    "status": "not_met",
                }
            )
            requirements_not_met += 1

    overall_status = "compliant" if requirements_not_met == 0 else "non_compliant"

    estimated_credit = None
    if overall_status == "compliant":
        if rule.percentage:
            estimated_credit = request.productionBudget * (rule.percentage / 100)
            if rule.maxCredit and estimated_credit > rule.maxCredit:
                estimated_credit = rule.maxCredit

    pdf_bytes = pdf_generator.generate_compliance_report(
        production_title=request.productionTitle,
        jurisdiction=jurisdiction.name,
        rule_name=rule.ruleName,
        requirements=requirement_checks,
        overall_status=overall_status,
        estimated_credit=estimated_credit,
    )
    filename = f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.post("/scenario", summary="Generate scenario analysis PDF report")
async def generate_scenario_report(request: GenerateScenarioReportRequest):
    """
    Generate a professional PDF report analyzing multiple production scenarios.

    Returns a downloadable PDF with:
    - Scenario comparison across different budget levels
    - ROI analysis for each scenario
    - Optimization recommendations
    - Break-even analysis
    """
    jurisdiction = await prisma.jurisdiction.find_unique(
        where={"id": request.jurisdictionId}
    )
    if not jurisdiction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Jurisdiction not found"
        )

    rules = await prisma.incentiverule.find_many(
        where={"jurisdictionId": request.jurisdictionId, "active": True}
    )
    if not rules:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active incentive rules found for this jurisdiction",
        )

    scenario_results = []
    for scenario in request.scenarios:
        scenario_budget = scenario.get("budget", request.baseProductionBudget)
        best_credit = 0
        best_rule = None
        for rule in rules:
            if rule.percentage:
                credit = scenario_budget * (rule.percentage / 100)
            elif rule.fixedAmount:
                credit = rule.fixedAmount
            else:
                credit = 0

            if rule.minSpend and scenario_budget < rule.minSpend:
                credit = 0
            if rule.maxCredit and credit > rule.maxCredit:
                credit = rule.maxCredit
            if credit > best_credit:
                best_credit = credit
                best_rule = rule

        if best_rule:
            scenario_results.append(
                {
                    "name": scenario.get(
                        "name", f"Scenario {len(scenario_results) + 1}"
                    ),
                    "budget": scenario_budget,
                    "estimatedCredit": best_credit,
                    "effectiveRate": (
                        (best_credit / scenario_budget * 100)
                        if scenario_budget > 0
                        else 0
                    ),
                    "ruleName": best_rule.ruleName,
                    "percentage": best_rule.percentage,
                }
            )

    scenario_results.sort(key=lambda x: x["estimatedCredit"], reverse=True)
    if not scenario_results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No qualifying scenarios found",
        )
    best_scenario = scenario_results[0]

    pdf_bytes = pdf_generator.generate_scenario_report(
        production_title=request.productionTitle,
        jurisdiction=jurisdiction.name,
        base_budget=request.baseProductionBudget,
        scenarios=scenario_results,
        best_scenario=best_scenario,
    )
    filename = f"scenario_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
