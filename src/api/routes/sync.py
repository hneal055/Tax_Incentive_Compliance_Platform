"""
Sync and Webhook API endpoints
"""
import uuid
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from typing import List, Optional, Any

from src.api.middleware.auth import verify_token
from src.models.errors import BudgetNotFoundError
from src.utils.database import prisma

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Sync & Webhooks"])


class SyncChange(BaseModel):
    type: str
    account_id: Optional[str] = None
    field: Optional[str] = None
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None


class SyncRequest(BaseModel):
    source: str
    sync_type: str  # "full" | "incremental"
    changes: List[SyncChange] = []


class SyncResponse(BaseModel):
    budget_id: str
    sync_id: str
    status: str
    synced_at: datetime
    conflicts: List[dict] = []


class WebhookRegisterRequest(BaseModel):
    url: str
    events: List[str]
    secret: str


class WebhookRegisterResponse(BaseModel):
    webhook_id: str
    url: str
    events: List[str]
    status: str
    created_at: datetime


@router.post(
    "/budgets/{budget_id}/sync",
    response_model=SyncResponse,
    summary="Bidirectional sync with MMB Connector",
)
async def sync_budget(
    budget_id: str,
    sync_request: SyncRequest,
    _token: dict = Depends(verify_token),
):
    """
    Bidirectional sync endpoint for the MMB Connector.
    Accepts change sets and applies them to the budget.
    """
    budget = await prisma.budget.find_unique(where={"id": budget_id})
    if not budget:
        raise BudgetNotFoundError(budget_id)

    conflicts: List[dict] = []
    synced_at = datetime.now(timezone.utc)

    # Apply incremental changes
    if sync_request.sync_type == "incremental":
        for change in sync_request.changes:
            if change.type == "account_update" and change.account_id:
                account = await prisma.budgetaccount.find_unique(
                    where={"id": change.account_id}
                )
                if account and change.field == "amount":
                    await prisma.budgetaccount.update(
                        where={"id": change.account_id},
                        data={"amount": float(change.new_value)},
                    )

    # Log sync
    sync_log = await prisma.synclog.create(
        data={
            "id": str(uuid.uuid4()),
            "budgetId": budget_id,
            "source": sync_request.source,
            "syncType": sync_request.sync_type,
            "status": "completed",
            "conflicts": conflicts if conflicts else None,
        }
    )

    return SyncResponse(
        budget_id=budget_id,
        sync_id=sync_log.id,
        status="completed",
        synced_at=synced_at,
        conflicts=conflicts,
    )


@router.post(
    "/webhooks/register",
    response_model=WebhookRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a webhook for real-time notifications",
)
async def register_webhook(
    request: WebhookRegisterRequest,
    _token: dict = Depends(verify_token),
):
    """
    Register a webhook endpoint to receive real-time notifications.
    """
    webhook = await prisma.webhookregistration.create(
        data={
            "id": str(uuid.uuid4()),
            "url": request.url,
            "events": request.events,
            "secret": request.secret,
            "active": True,
        }
    )

    return WebhookRegisterResponse(
        webhook_id=webhook.id,
        url=webhook.url,
        events=webhook.events,
        status="active",
        created_at=webhook.createdAt,
    )
