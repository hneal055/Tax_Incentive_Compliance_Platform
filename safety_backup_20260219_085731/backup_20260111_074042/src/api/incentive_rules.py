"""
Incentive Rule API endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import Optional
import json

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
    
    # Prepare data with proper Prisma relationships
    rule_dict = rule.model_dump()
    jurisdiction_id = rule_dict.pop("jurisdictionId")
    
    # Convert requirements dict to JSON string if not empty
    if rule_dict.get("requirements"):
        rule_dict["requirements"] = json.dumps(rule_dict["requirements"])
    else:
        rule_dict["requirements"] = json.dumps({})
    
    new_rule = await prisma.incentiverule.create(
        data={
            **rule_dict,
            "jurisdiction": {
                "connect": {"id": jurisdiction_id}
            }
        }
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
    
    # Handle jurisdiction update
    if "jurisdictionId" in update_data:
        jurisdiction_id = update_data.pop("jurisdictionId")
        jurisdiction = await prisma.jurisdiction.find_unique(
            where={"id": jurisdiction_id}
        )
        if not jurisdiction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Jurisdiction with ID {jurisdiction_id} not found"
            )
        update_data["jurisdiction"] = {"connect": {"id": jurisdiction_id}}
    
    # Handle requirements JSON
    if "requirements" in update_data:
        update_data["requirements"] = json.dumps(update_data["requirements"])
    
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
