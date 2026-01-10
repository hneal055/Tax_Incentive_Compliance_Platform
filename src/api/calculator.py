"""
Calculator API endpoints - Tax credit calculations
"""
from fastapi import APIRouter, HTTPException, status
import json
from typing import Dict, Any

from src.models.calculator import (
    SimpleCalculateRequest,
    SimpleCalculateResponse,
    CompareCalculateRequest,
    CompareCalculateResponse,
    ComparisonResult
)
from src.utils.database import prisma

router = APIRouter(prefix="/calculate", tags=["Calculator"])


def parse_json_field(field: Any) -> Dict:
    """Parse JSON field that might be string or dict"""
    if isinstance(field, str):
        return json.loads(field)
    return field if field else {}


@router.post("/simple", response_model=SimpleCalculateResponse, summary="Calculate tax credit for single rule")
async def calculate_simple(request: SimpleCalculateRequest):
    """
    Calculate estimated tax credit for a production using a specific incentive rule.
    
    - **productionBudget**: Total production budget
    - **jurisdictionId**: Target jurisdiction
    - **ruleId**: Specific incentive rule to apply
    - **qualifyingBudget**: Optional override for qualifying budget
    
    Returns detailed calculation with requirements check.
    """
    
    # Get jurisdiction
    jurisdiction = await prisma.jurisdiction.find_unique(
        where={"id": request.jurisdictionId}
    )
    
    if not jurisdiction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jurisdiction not found"
        )
    
    # Get rule
    rule = await prisma.incentiverule.find_unique(
        where={"id": request.ruleId}
    )
    
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incentive rule not found"
        )
    
    # Verify rule belongs to jurisdiction
    if rule.jurisdictionId != request.jurisdictionId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rule does not belong to specified jurisdiction"
        )
    
    # Use qualifying budget or default to total budget
    qualifying_budget = request.qualifyingBudget if request.qualifyingBudget else request.productionBudget
    
    # Calculate credit
    if rule.percentage:
        estimated_credit = qualifying_budget * (rule.percentage / 100)
    elif rule.fixedAmount:
        estimated_credit = rule.fixedAmount
    else:
        estimated_credit = 0
    
    # Check minimum spend
    meets_minimum = True
    if rule.minSpend:
        meets_minimum = qualifying_budget >= rule.minSpend
        if not meets_minimum:
            estimated_credit = 0
    
    # Apply maximum cap
    under_maximum = True
    if rule.maxCredit and estimated_credit > rule.maxCredit:
        estimated_credit = rule.maxCredit
        under_maximum = False
    
    # Parse requirements
    requirements = parse_json_field(rule.requirements)
    
    # Generate notes
    notes = []
    if not meets_minimum:
        notes.append(f"⚠️ Does not meet minimum spend requirement of ${rule.minSpend:,.0f}")
    if not under_maximum:
        notes.append(f"ℹ️ Credit capped at maximum of ${rule.maxCredit:,.0f}")
    if rule.percentage:
        notes.append(f"💡 Rate: {rule.percentage}% of qualifying budget")
    if requirements:
        notes.append(f"📋 Additional requirements apply - see requirements field")
    
    return SimpleCalculateResponse(
        jurisdiction=jurisdiction.name,
        ruleName=rule.ruleName,
        ruleCode=rule.ruleCode,
        incentiveType=rule.incentiveType,
        totalBudget=request.productionBudget,
        qualifyingBudget=qualifying_budget,
        percentage=rule.percentage,
        estimatedCredit=estimated_credit,
        meetsMinimumSpend=meets_minimum,
        minimumSpendRequired=rule.minSpend,
        underMaximumCap=under_maximum,
        maximumCapAmount=rule.maxCredit,
        requirements=requirements,
        notes=notes
    )


@router.post("/compare", response_model=CompareCalculateResponse, summary="Compare tax credits across jurisdictions")
async def calculate_compare(request: CompareCalculateRequest):
    """
    Compare estimated tax credits across multiple jurisdictions.
    
    - **productionBudget**: Total production budget
    - **jurisdictionIds**: List of 2-10 jurisdictions to compare
    - **qualifyingBudget**: Optional override for qualifying budget
    
    Returns ranked comparison of all jurisdictions with best recommendation.
    """
    
    if len(request.jurisdictionIds) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must compare at least 2 jurisdictions"
        )
    
    if len(request.jurisdictionIds) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot compare more than 10 jurisdictions at once"
        )
    
    # Get all jurisdictions
    jurisdictions = await prisma.jurisdiction.find_many(
        where={"id": {"in": request.jurisdictionIds}}
    )
    
    if len(jurisdictions) != len(request.jurisdictionIds):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more jurisdictions not found"
        )
    
    qualifying_budget = request.qualifyingBudget if request.qualifyingBudget else request.productionBudget
    
    # Calculate for each jurisdiction (use best rule for each)
    comparisons = []
    
    for jurisdiction in jurisdictions:
        # Get all active rules for this jurisdiction
        rules = await prisma.incentiverule.find_many(
            where={
                "jurisdictionId": jurisdiction.id,
                "active": True
            }
        )
        
        if not rules:
            # No active rules - add with zero credit
            comparisons.append({
                "jurisdiction": jurisdiction.name,
                "jurisdictionId": jurisdiction.id,
                "ruleName": "No active programs",
                "ruleCode": "NONE",
                "incentiveType": "none",
                "percentage": None,
                "estimatedCredit": 0,
                "meetsRequirements": False
            })
            continue
        
        # Calculate credit for each rule, take the best one
        best_credit = 0
        best_rule = rules[0]
        meets_requirements = False
        
        for rule in rules:
            # Calculate credit
            if rule.percentage:
                credit = qualifying_budget * (rule.percentage / 100)
            elif rule.fixedAmount:
                credit = rule.fixedAmount
            else:
                credit = 0
            
            # Check minimum
            meets_min = True
            if rule.minSpend:
                meets_min = qualifying_budget >= rule.minSpend
                if not meets_min:
                    credit = 0
            
            # Apply cap
            if rule.maxCredit and credit > rule.maxCredit:
                credit = rule.maxCredit
            
            # Track best
            if credit > best_credit:
                best_credit = credit
                best_rule = rule
                meets_requirements = meets_min
        
        comparisons.append({
            "jurisdiction": jurisdiction.name,
            "jurisdictionId": jurisdiction.id,
            "ruleName": best_rule.ruleName,
            "ruleCode": best_rule.ruleCode,
            "incentiveType": best_rule.incentiveType,
            "percentage": best_rule.percentage,
            "estimatedCredit": best_credit,
            "meetsRequirements": meets_requirements
        })
    
    # Sort by estimated credit (descending)
    comparisons.sort(key=lambda x: x["estimatedCredit"], reverse=True)
    
    # Add rank and calculate savings
    for i, comp in enumerate(comparisons):
        comp["rank"] = i + 1
        comp["savings"] = comp["estimatedCredit"]
    
    # Best and worst
    best = comparisons[0]
    worst = comparisons[-1]
    savings_vs_worst = best["estimatedCredit"] - worst["estimatedCredit"]
    
    # Convert to Pydantic models
    comparison_results = [ComparisonResult(**comp) for comp in comparisons]
    best_result = ComparisonResult(**best)
    
    # Generate notes
    notes = []
    notes.append(f"🏆 Best option: {best['jurisdiction']} with ${best['estimatedCredit']:,.0f} credit")
    notes.append(f"💰 Saves ${savings_vs_worst:,.0f} vs lowest option ({worst['jurisdiction']})")
    
    if best["percentage"]:
        notes.append(f"📊 Top rate: {best['percentage']}% ({best['ruleName']})")
    
    return CompareCalculateResponse(
        totalBudget=request.productionBudget,
        comparisons=comparison_results,
        bestOption=best_result,
        savingsVsWorst=savings_vs_worst,
        notes=notes
    )


@router.get("/jurisdiction/{jurisdiction_id}", summary="Get all rules for a jurisdiction with budget estimate")
async def calculate_jurisdiction_options(
    jurisdiction_id: str,
    budget: float
):
    """
    Get all available incentive rules for a jurisdiction with estimated credits.
    
    Useful for seeing all options in one place.
    """
    
    # Get jurisdiction
    jurisdiction = await prisma.jurisdiction.find_unique(
        where={"id": jurisdiction_id}
    )
    
    if not jurisdiction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jurisdiction not found"
        )
    
    # Get all rules
    rules = await prisma.incentiverule.find_many(
        where={
            "jurisdictionId": jurisdiction_id,
            "active": True
        }
    )
    
    if not rules:
        return {
            "jurisdiction": jurisdiction.name,
            "jurisdictionId": jurisdiction_id,
            "budget": budget,
            "options": [],
            "message": "No active incentive programs available"
        }
    
    # Calculate for each rule
    options = []
    for rule in rules:
        # Calculate
        if rule.percentage:
            credit = budget * (rule.percentage / 100)
        elif rule.fixedAmount:
            credit = rule.fixedAmount
        else:
            credit = 0
        
        # Check requirements
        meets_min = True
        if rule.minSpend:
            meets_min = budget >= rule.minSpend
            if not meets_min:
                credit = 0
        
        if rule.maxCredit and credit > rule.maxCredit:
            credit = rule.maxCredit
        
        options.append({
            "ruleName": rule.ruleName,
            "ruleCode": rule.ruleCode,
            "ruleId": rule.id,
            "incentiveType": rule.incentiveType,
            "percentage": rule.percentage,
            "estimatedCredit": credit,
            "meetsMinimum": meets_min,
            "minimumRequired": rule.minSpend,
            "maximumCap": rule.maxCredit
        })
    
    # Sort by credit amount
    options.sort(key=lambda x: x["estimatedCredit"], reverse=True)
    
    return {
        "jurisdiction": jurisdiction.name,
        "jurisdictionId": jurisdiction_id,
        "budget": budget,
        "options": options,
        "bestOption": options[0] if options else None
    }
