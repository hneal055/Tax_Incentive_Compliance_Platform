"""
Incentive Rule API endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import Optional

from src.models.incentive_rule import (
    IncentiveRuleCreate,
    IncentiveRuleUpdate,
    IncentiveRuleResponse,
    IncentiveRuleList
)
from src.utils.database import prisma

router = APIRouter(prefix="/incentive-rules", tags=["Incentive Rules"])


@router.get("/", response_model=IncentiveRuleList, summary="Get all incentive rules")
async def get_incentive_rules(
    jurisdiction_id: Optional[str] = None,
    incentive_type: Optional[str] = None,
    active: Optional[bool] = None
):
    """Retrieve all incentive rules with optional filtering."""
    where = {}
    if jurisdiction_id:
        where["jurisdictionId"] = jurisdiction_id
    if incentive_type:
        where["incentiveType"] = {"equals": incentive_type, "mode": "insensitive"}
    if active is not None:
        where["active"] = active
    
    rules = await prisma.incentiverule.find_many(
        where=where if where else None,
        order={"ruleName": "asc"}
    )
    
    return {
        "total": len(rules),
        "rules": rules
    }


@router.get("/{rule_id}", response_model=IncentiveRuleResponse, summary="Get incentive rule by ID")
async def get_incentive_rule(rule_id: str):
    """Retrieve a specific incentive rule by ID."""
    rule = await prisma.incentiverule.find_unique(
        where={"id": rule_id}
    )
    
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incentive rule with ID {rule_id} not found"
        )
    
    return rule


@router.post("/", response_model=IncentiveRuleResponse, status_code=status.HTTP_201_CREATED, summary="Create incentive rule")
async def create_incentive_rule(rule: IncentiveRuleCreate):
    """Create a new incentive rule."""
    # Check if jurisdiction exists
    jurisdiction = await prisma.jurisdiction.find_unique(
        where={"id": rule.jurisdictionId}
    )
    
    if not jurisdiction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jurisdiction with ID {rule.jurisdictionId} not found"
        )
    
    # Check if rule code already exists
    existing = await prisma.incentiverule.find_first(
        where={"ruleCode": {"equals": rule.ruleCode, "mode": "insensitive"}}
    )
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Incentive rule with code '{rule.ruleCode}' already exists"
        )
    
    new_rule = await prisma.incentiverule.create(
        data=rule.model_dump()
    )
    
    return new_rule


@router.put("/{rule_id}", response_model=IncentiveRuleResponse, summary="Update incentive rule")
async def update_incentive_rule(rule_id: str, rule: IncentiveRuleUpdate):
    """Update an existing incentive rule."""
    existing = await prisma.incentiverule.find_unique(
        where={"id": rule_id}
    )
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incentive rule with ID {rule_id} not found"
        )
    
    update_data = rule.model_dump(exclude_unset=True)
    
    # If updating jurisdictionId, verify it exists
    if "jurisdictionId" in update_data:
        jurisdiction = await prisma.jurisdiction.find_unique(
            where={"id": update_data["jurisdictionId"]}
        )
        if not jurisdiction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Jurisdiction with ID {update_data['jurisdictionId']} not found"
            )
    
    updated = await prisma.incentiverule.update(
        where={"id": rule_id},
        data=update_data
    )
    
    return updated


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete incentive rule")
async def delete_incentive_rule(rule_id: str):
    """Delete an incentive rule."""
    existing = await prisma.incentiverule.find_unique(
        where={"id": rule_id}
    )
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incentive rule with ID {rule_id} not found"
        )
    
    await prisma.incentiverule.delete(
        where={"id": rule_id}
    )
    
    return None
