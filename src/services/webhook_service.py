"""
Webhook Notification Service
Sends webhook notifications for API key events
"""
import logging
import json
import hmac
import hashlib
from datetime import datetime, timezone
from typing import Optional
import httpx
from src.utils.database import prisma

logger = logging.getLogger(__name__)


class WebhookService:
    """Service for sending webhook notifications"""
    
    @staticmethod
    async def send_webhook(
        organization_id: str,
        event: str,
        payload: dict
    ) -> None:
        """
        Send webhook notifications for an event
        
        Args:
            organization_id: Organization to send webhooks for
            event: Event type (api_key_expiring, api_key_expired, etc.)
            payload: Event payload data
        """
        # Get webhook configurations for this organization
        webhooks = await prisma.webhookconfig.find_many(
            where={
                "organizationId": organization_id,
                "active": True
            }
        )
        
        # Filter webhooks that are subscribed to this event
        relevant_webhooks = [w for w in webhooks if event in w.events]
        
        if not relevant_webhooks:
            logger.debug(f"No webhooks configured for event {event}")
            return
        
        # Send to each webhook
        async with httpx.AsyncClient(timeout=10.0) as client:
            for webhook in relevant_webhooks:
                try:
                    await WebhookService._send_single_webhook(
                        client, webhook, event, payload
                    )
                except Exception as e:
                    logger.error(f"Failed to send webhook to {webhook.url}: {e}")
    
    @staticmethod
    async def _send_single_webhook(
        client: httpx.AsyncClient,
        webhook,
        event: str,
        payload: dict
    ):
        """Send a single webhook notification"""
        # Prepare webhook payload
        webhook_payload = {
            "event": event,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": payload
        }
        
        payload_json = json.dumps(webhook_payload)
        
        # Create signature if secret is configured
        headers = {"Content-Type": "application/json"}
        if webhook.secret:
            signature = hmac.new(
                webhook.secret.encode(),
                payload_json.encode(),
                hashlib.sha256
            ).hexdigest()
            headers["X-Webhook-Signature"] = f"sha256={signature}"
        
        # Send webhook
        response = await client.post(
            webhook.url,
            content=payload_json,
            headers=headers
        )
        
        if response.status_code >= 400:
            logger.warning(
                f"Webhook returned status {response.status_code}: {webhook.url}"
            )
        else:
            logger.info(f"Webhook sent successfully to {webhook.url}")
    
    @staticmethod
    async def notify_key_expiring(
        organization_id: str,
        api_key_id: str,
        api_key_name: str,
        expires_at: datetime
    ):
        """Notify about an API key that is expiring soon"""
        await WebhookService.send_webhook(
            organization_id,
            "api_key_expiring",
            {
                "api_key_id": api_key_id,
                "api_key_name": api_key_name,
                "expires_at": expires_at.isoformat()
            }
        )
    
    @staticmethod
    async def notify_key_expired(
        organization_id: str,
        api_key_id: str,
        api_key_name: str
    ):
        """Notify about an API key that has expired"""
        await WebhookService.send_webhook(
            organization_id,
            "api_key_expired",
            {
                "api_key_id": api_key_id,
                "api_key_name": api_key_name
            }
        )
    
    @staticmethod
    async def notify_key_created(
        organization_id: str,
        api_key_id: str,
        api_key_name: str
    ):
        """Notify about a new API key creation"""
        await WebhookService.send_webhook(
            organization_id,
            "api_key_created",
            {
                "api_key_id": api_key_id,
                "api_key_name": api_key_name
            }
        )
    
    @staticmethod
    async def notify_key_revoked(
        organization_id: str,
        api_key_id: str,
        api_key_name: str
    ):
        """Notify about an API key revocation"""
        await WebhookService.send_webhook(
            organization_id,
            "api_key_revoked",
            {
                "api_key_id": api_key_id,
                "api_key_name": api_key_name
            }
        )


# Singleton instance
webhook_service = WebhookService()
