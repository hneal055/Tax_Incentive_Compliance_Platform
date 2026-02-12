"""
Audit Logging Service
Tracks all API key operations for compliance and security
"""
import logging
from datetime import datetime, timezone
from typing import Optional
from src.utils.database import prisma

logger = logging.getLogger(__name__)


class AuditLogService:
    """Service for managing audit logs"""
    
    @staticmethod
    async def log_action(
        organization_id: str,
        action: str,
        api_key_id: Optional[str] = None,
        actor_id: Optional[str] = None,
        metadata: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> None:
        """
        Log an API key action to the audit log
        
        Args:
            organization_id: Organization performing the action
            action: Action type (create, delete, rotate, revoke, update)
            api_key_id: ID of the API key involved (if applicable)
            actor_id: ID of the user performing the action
            metadata: Additional metadata as JSON string
            ip_address: IP address of the requester
            user_agent: User agent of the requester
        """
        try:
            await prisma.auditlog.create(
                data={
                    "organizationId": organization_id,
                    "action": action,
                    "apiKeyId": api_key_id,
                    "actorId": actor_id,
                    "metadata": metadata,
                    "ipAddress": ip_address,
                    "userAgent": user_agent,
                    "timestamp": datetime.now(timezone.utc)
                }
            )
            logger.info(f"Audit log created: {action} for org {organization_id}")
        except Exception as e:
            # Don't fail the main operation if audit logging fails
            logger.error(f"Failed to create audit log: {e}")
    
    @staticmethod
    async def get_logs(
        organization_id: str,
        api_key_id: Optional[str] = None,
        action: Optional[str] = None,
        limit: int = 100
    ):
        """
        Retrieve audit logs for an organization
        
        Args:
            organization_id: Organization to filter by
            api_key_id: Optional API key to filter by
            action: Optional action type to filter by
            limit: Maximum number of logs to return
            
        Returns:
            List of audit log records
        """
        where_clause = {"organizationId": organization_id}
        
        if api_key_id:
            where_clause["apiKeyId"] = api_key_id
        
        if action:
            where_clause["action"] = action
        
        return await prisma.auditlog.find_many(
            where=where_clause,
            order={"timestamp": "desc"},
            take=limit
        )


# Singleton instance
audit_log_service = AuditLogService()
