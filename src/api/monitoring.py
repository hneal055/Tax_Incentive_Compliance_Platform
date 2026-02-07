"""
Monitoring API endpoints for real-time jurisdiction monitoring
"""
from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from datetime import datetime, timezone

from src.models.monitoring import (
    MonitoringSourceCreate,
    MonitoringSourceUpdate,
    MonitoringSourceResponse,
    MonitoringSourceList,
    MonitoringEventUpdate,
    MonitoringEventResponse,
    MonitoringEventList,
    UnreadCountResponse,
)
from src.utils.database import prisma

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])


# Event endpoints
@router.get("/events", response_model=MonitoringEventList, summary="Get monitoring events")
async def get_monitoring_events(
    jurisdiction_id: Optional[str] = Query(None, description="Filter by jurisdiction ID"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    unread_only: bool = Query(False, description="Show only unread events"),
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page (max 100)"),
):
    """
    Retrieve monitoring events with optional filtering and pagination.
    
    - **jurisdiction_id**: Filter by jurisdiction
    - **event_type**: Filter by event type (incentive_change, new_program, expiration, news)
    - **severity**: Filter by severity (info, warning, critical)
    - **unread_only**: Show only unread events
    - **page**: Page number for pagination
    - **page_size**: Number of items per page
    """
    where = {}
    
    if jurisdiction_id:
        where["jurisdictionId"] = jurisdiction_id
    
    if event_type:
        where["eventType"] = event_type
    
    if severity:
        where["severity"] = severity
    
    if unread_only:
        where["readAt"] = None
    
    # Calculate offset for pagination
    skip = (page - 1) * page_size
    
    events = await prisma.monitoringevent.find_many(
        where=where if where else None,
        order={"detectedAt": "desc"},
        skip=skip,
        take=page_size,
    )
    
    total = await prisma.monitoringevent.count(
        where=where if where else None
    )
    
    return {
        "total": total,
        "events": events,
    }


@router.get("/events/unread", response_model=UnreadCountResponse, summary="Get unread event count")
async def get_unread_count(
    jurisdiction_id: Optional[str] = Query(None, description="Filter by jurisdiction ID"),
):
    """
    Get count of unread monitoring events.
    
    - **jurisdiction_id**: Optional filter by jurisdiction
    """
    where = {"readAt": None}
    
    if jurisdiction_id:
        where["jurisdictionId"] = jurisdiction_id
    
    count = await prisma.monitoringevent.count(where=where)
    
    return {"unreadCount": count}


@router.patch("/events/{event_id}/read", response_model=MonitoringEventResponse, summary="Mark event as read")
async def mark_event_as_read(event_id: str):
    """
    Mark a monitoring event as read.
    
    - **event_id**: The ID of the event to mark as read
    """
    # Check if event exists
    event = await prisma.monitoringevent.find_unique(
        where={"id": event_id}
    )
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found"
        )
    
    # Update readAt timestamp
    updated_event = await prisma.monitoringevent.update(
        where={"id": event_id},
        data={"readAt": datetime.now(timezone.utc)}
    )
    
    return updated_event


# Source endpoints
@router.get("/sources", response_model=MonitoringSourceList, summary="Get monitoring sources")
async def get_monitoring_sources(
    jurisdiction_id: Optional[str] = Query(None, description="Filter by jurisdiction ID"),
    source_type: Optional[str] = Query(None, description="Filter by source type"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
):
    """
    Retrieve monitoring sources with optional filtering.
    
    - **jurisdiction_id**: Filter by jurisdiction
    - **source_type**: Filter by source type (rss, api, webpage)
    - **active**: Filter by active status
    """
    where = {}
    
    if jurisdiction_id:
        where["jurisdictionId"] = jurisdiction_id
    
    if source_type:
        where["sourceType"] = source_type
    
    if active is not None:
        where["active"] = active
    
    sources = await prisma.monitoringsource.find_many(
        where=where if where else None,
        order={"createdAt": "desc"},
    )
    
    return {
        "total": len(sources),
        "sources": sources,
    }


@router.post("/sources", response_model=MonitoringSourceResponse, status_code=status.HTTP_201_CREATED, summary="Create monitoring source")
async def create_monitoring_source(source: MonitoringSourceCreate):
    """
    Create a new monitoring source.
    
    - **jurisdictionId**: ID of the jurisdiction to monitor
    - **sourceType**: Type of source (rss, api, webpage)
    - **url**: URL of the monitoring source
    - **checkInterval**: Check interval in seconds (default: 3600)
    - **active**: Whether source is active (default: true)
    """
    # Verify jurisdiction exists
    jurisdiction = await prisma.jurisdiction.find_unique(
        where={"id": source.jurisdictionId}
    )
    
    if not jurisdiction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jurisdiction with ID {source.jurisdictionId} not found"
        )
    
    # Validate source type
    valid_source_types = ["rss", "api", "webpage"]
    if source.sourceType not in valid_source_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid source type. Must be one of: {', '.join(valid_source_types)}"
        )
    
    new_source = await prisma.monitoringsource.create(
        data=source.model_dump()
    )
    
    return new_source
