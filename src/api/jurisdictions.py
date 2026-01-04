"""
Jurisdiction API endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
import uuid

from src.models.jurisdiction import (
    JurisdictionCreate,
    JurisdictionUpdate,
    JurisdictionResponse,
    JurisdictionList
)

router = APIRouter(prefix="/jurisdictions", tags=["Jurisdictions"])

# Mock database (in-memory storage)
mock_jurisdictions = [
    {
        "id": "1",
        "name": "California",
        "code": "CA",
        "country": "USA",
        "type": "state",
        "description": "California Film & Television Tax Credit Program",
        "website": "https://film.ca.gov",
        "active": True,
        "createdAt": datetime.now(),
        "updatedAt": datetime.now()
    },
    {
        "id": "2",
        "name": "Georgia",
        "code": "GA",
        "country": "USA",
        "type": "state",
        "description": "Georgia Film Tax Credit",
        "website": "https://www.georgia.org/industries/film-entertainment",
        "active": True,
        "createdAt": datetime.now(),
        "updatedAt": datetime.now()
    },
    {
        "id": "3",
        "name": "New York",
        "code": "NY",
        "country": "USA",
        "type": "state",
        "description": "NY Film Production Tax Credit",
        "website": "https://esd.ny.gov/film-tax-credit-programs",
        "active": True,
        "createdAt": datetime.now(),
        "updatedAt": datetime.now()
    },
    {
        "id": "4",
        "name": "British Columbia",
        "code": "BC",
        "country": "Canada",
        "type": "province",
        "description": "BC Film Incentive Programs",
        "website": "https://www2.gov.bc.ca/gov/content/taxes/income-taxes/corporate/credits/film-media",
        "active": True,
        "createdAt": datetime.now(),
        "updatedAt": datetime.now()
    }
]


@router.get("/", response_model=JurisdictionList, summary="Get all jurisdictions")
async def get_jurisdictions(
    country: str | None = None,
    type: str | None = None,
    active: bool | None = None
):
    """
    Retrieve all jurisdictions with optional filtering.
    
    - **country**: Filter by country (e.g., USA, Canada)
    - **type**: Filter by type (state, province, country)
    - **active**: Filter by active status
    """
    filtered = mock_jurisdictions.copy()
    
    if country:
        filtered = [j for j in filtered if j["country"].lower() == country.lower()]
    if type:
        filtered = [j for j in filtered if j["type"].lower() == type.lower()]
    if active is not None:
        filtered = [j for j in filtered if j["active"] == active]
    
    return {
        "total": len(filtered),
        "jurisdictions": filtered
    }


@router.get("/{jurisdiction_id}", response_model=JurisdictionResponse, summary="Get jurisdiction by ID")
async def get_jurisdiction(jurisdiction_id: str):
    """
    Retrieve a specific jurisdiction by ID.
    
    - **jurisdiction_id**: The unique identifier of the jurisdiction
    """
    jurisdiction = next((j for j in mock_jurisdictions if j["id"] == jurisdiction_id), None)
    
    if not jurisdiction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jurisdiction with ID {jurisdiction_id} not found"
        )
    
    return jurisdiction


@router.post("/", response_model=JurisdictionResponse, status_code=status.HTTP_201_CREATED, summary="Create jurisdiction")
async def create_jurisdiction(jurisdiction: JurisdictionCreate):
    """
    Create a new jurisdiction.
    
    - **name**: Full name of the jurisdiction
    - **code**: Short code (e.g., CA, NY, BC)
    - **country**: Country name
    - **type**: Type of jurisdiction (state, province, country)
    """
    # Check if code already exists
    if any(j["code"].upper() == jurisdiction.code.upper() for j in mock_jurisdictions):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Jurisdiction with code '{jurisdiction.code}' already exists"
        )
    
    new_jurisdiction = {
        "id": str(uuid.uuid4()),
        **jurisdiction.model_dump(),
        "createdAt": datetime.now(),
        "updatedAt": datetime.now()
    }
    
    mock_jurisdictions.append(new_jurisdiction)
    return new_jurisdiction


@router.put("/{jurisdiction_id}", response_model=JurisdictionResponse, summary="Update jurisdiction")
async def update_jurisdiction(jurisdiction_id: str, jurisdiction: JurisdictionUpdate):
    """
    Update an existing jurisdiction.
    
    - **jurisdiction_id**: The ID of the jurisdiction to update
    - Only provided fields will be updated
    """
    existing = next((j for j in mock_jurisdictions if j["id"] == jurisdiction_id), None)
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jurisdiction with ID {jurisdiction_id} not found"
        )
    
    # Update only provided fields
    update_data = jurisdiction.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        existing[field] = value
    
    existing["updatedAt"] = datetime.now()
    
    return existing


@router.delete("/{jurisdiction_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete jurisdiction")
async def delete_jurisdiction(jurisdiction_id: str):
    """
    Delete a jurisdiction.
    
    - **jurisdiction_id**: The ID of the jurisdiction to delete
    """
    global mock_jurisdictions
    
    jurisdiction = next((j for j in mock_jurisdictions if j["id"] == jurisdiction_id), None)
    
    if not jurisdiction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jurisdiction with ID {jurisdiction_id} not found"
        )
    
    mock_jurisdictions = [j for j in mock_jurisdictions if j["id"] != jurisdiction_id]
    return None
