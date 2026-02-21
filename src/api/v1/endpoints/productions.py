"""
Production API endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import Optional
from datetime import date, datetime
import logging

from src.models.production import (
    ProductionCreate,
    ProductionUpdate,
    ProductionResponse,
    ProductionList,
    ProductionQuickCreate
)
from src.utils.database import prisma

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/productions", tags=["Productions"])


@router.get("/", response_model=ProductionList, summary="Get all productions")
async def get_productions(
    production_type: Optional[str] = None,
    active: Optional[bool] = None
):
    """Retrieve all productions with optional filtering."""
    logger.info("GET productions called")
    where = {}
    if production_type:
        where["productionType"] = {"equals": production_type, "mode": "insensitive"}
    
    productions = await prisma.production.find_many(
        where=where if where else None,
        order={"createdAt": "desc"}
    )
    
    logger.info(f"Found {len(productions)} productions")
    return {
        "total": len(productions),
        "productions": productions
    }


@router.post("/quick", response_model=ProductionResponse, status_code=status.HTTP_201_CREATED, summary="Quick create production")
async def quick_create_production(production: ProductionQuickCreate):
    """Quick create a production with minimal required fields. Auto-fills defaults."""
    try:
        logger.info(f"Quick creating production: {production.title}")
        
        # Get first jurisdiction as default if not provided
        jurisdiction_id = production.jurisdictionId
        if not jurisdiction_id:
            first_jurisdiction = await prisma.jurisdiction.find_first()
            if not first_jurisdiction:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No jurisdictions available. Please create a jurisdiction first."
                )
            jurisdiction_id = first_jurisdiction.id
        
        # Convert date to datetime for Prisma
        if production.startDate:
            start_datetime = datetime.combine(production.startDate, datetime.min.time())
        else:
            start_datetime = datetime.now()
        
        # Create with defaults
        new_production = await prisma.production.create(
            data={
                "title": production.title,
                "productionType": production.productionType or "feature",
                "jurisdictionId": jurisdiction_id,
                "budgetTotal": production.budget,
                "budgetQualifying": production.budget * 0.85,
                "startDate": start_datetime,
                "productionCompany": production.productionCompany or "Default Company",
                "status": production.status or "planning",
            }
        )
        
        logger.info(f"Quick production created: {new_production.id}")
        return new_production
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error quick creating production: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating production: {str(e)}"
        )


@router.post("/", response_model=ProductionResponse, status_code=status.HTTP_201_CREATED, summary="Create production")
async def create_production(production: ProductionCreate):
    """Create a new production with all required fields."""
    try:
        logger.info(f"Creating production: {production.title}")
        
        # Verify jurisdiction exists
        jurisdiction = await prisma.jurisdiction.find_unique(
            where={"id": production.jurisdictionId}
        )
        
        if not jurisdiction:
            logger.error(f"Jurisdiction not found: {production.jurisdictionId}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Jurisdiction with ID {production.jurisdictionId} not found"
            )
        
        data = production.model_dump()
        # Convert date to datetime for Prisma
        for field in ["startDate", "endDate", "wrapDate"]:
            if data.get(field) and isinstance(data[field], date):
                data[field] = datetime.combine(data[field], datetime.min.time())
        
        new_production = await prisma.production.create(data=data)
        
        logger.info(f"Production created: {new_production.id}")
        return new_production
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error creating production: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating production: {str(e)}"
        )


@router.get("/{production_id}", response_model=ProductionResponse, summary="Get production by ID")
async def get_production(production_id: str):
    """Retrieve a specific production by ID."""
    production = await prisma.production.find_unique(
        where={"id": production_id}
    )
    
    if not production:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Production with ID {production_id} not found"
        )
    
    return production


@router.put("/{production_id}", response_model=ProductionResponse, summary="Update production")
async def update_production(production_id: str, production: ProductionUpdate):
    """Update an existing production."""
    existing = await prisma.production.find_unique(
        where={"id": production_id}
    )
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Production with ID {production_id} not found"
        )
    
    update_data = production.model_dump(exclude_unset=True)
    # Convert dates to datetimes
    for field in ["startDate", "endDate", "wrapDate"]:
        if update_data.get(field) and isinstance(update_data[field], date):
            update_data[field] = datetime.combine(update_data[field], datetime.min.time())
    
    updated = await prisma.production.update(
        where={"id": production_id},
        data=update_data
    )
    
    return updated


@router.delete("/{production_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete production")
async def delete_production(production_id: str):
    """Delete a production."""
    existing = await prisma.production.find_unique(
        where={"id": production_id}
    )
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Production with ID {production_id} not found"
        )
    
    await prisma.production.delete(
        where={"id": production_id}
    )
    
    return None
