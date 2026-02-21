"""
Usage Analytics Service
Tracks and analyzes API key usage
"""
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional
from src.utils.database import prisma

logger = logging.getLogger(__name__)


class UsageAnalyticsService:
    """Service for tracking and analyzing API key usage"""
    
    RECENT_ACTIVITY_LIMIT = 10  # Number of recent activities to return
    
    @staticmethod
    async def record_usage(
        api_key_id: str,
        endpoint: str,
        method: str,
        status_code: int,
        response_time: int
    ) -> None:
        """
        Record an API key usage event
        
        Args:
            api_key_id: API key that was used
            endpoint: Endpoint that was accessed
            method: HTTP method
            status_code: Response status code
            response_time: Response time in milliseconds
        """
        try:
            await prisma.apikeyusage.create(
                data={
                    "apiKeyId": api_key_id,
                    "endpoint": endpoint,
                    "method": method,
                    "statusCode": status_code,
                    "responseTime": response_time,
                    "timestamp": datetime.now(timezone.utc)
                }
            )
        except Exception as e:
            # Don't fail the request if usage tracking fails
            logger.error(f"Failed to record usage: {e}")
    
    @staticmethod
    async def get_analytics(
        api_key_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> dict:
        """
        Get usage analytics for an API key
        
        Args:
            api_key_id: API key to analyze
            start_date: Start of date range (defaults to 30 days ago)
            end_date: End of date range (defaults to now)
            
        Returns:
            Dictionary with analytics data
        """
        # Default to last 30 days
        if not end_date:
            end_date = datetime.now(timezone.utc)
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        # Get all usage records in date range
        usage_records = await prisma.apikeyusage.find_many(
            where={
                "apiKeyId": api_key_id,
                "timestamp": {
                    "gte": start_date,
                    "lte": end_date
                }
            },
            order={"timestamp": "desc"}
        )
        
        # Calculate analytics
        total_requests = len(usage_records)
        successful_requests = sum(1 for r in usage_records if 200 <= r.statusCode < 400)
        failed_requests = total_requests - successful_requests
        
        # Average response time
        avg_response_time = 0.0
        if total_requests > 0:
            avg_response_time = sum(r.responseTime for r in usage_records) / total_requests
        
        # Group by endpoint
        requests_by_endpoint = {}
        for record in usage_records:
            requests_by_endpoint[record.endpoint] = requests_by_endpoint.get(record.endpoint, 0) + 1
        
        # Group by method
        requests_by_method = {}
        for record in usage_records:
            requests_by_method[record.method] = requests_by_method.get(record.method, 0) + 1
        
        # Get recent activity (last N requests)
        recent_activity = usage_records[:UsageAnalyticsService.RECENT_ACTIVITY_LIMIT]
        
        return {
            "totalRequests": total_requests,
            "successfulRequests": successful_requests,
            "failedRequests": failed_requests,
            "averageResponseTime": round(avg_response_time, 2),
            "requestsByEndpoint": requests_by_endpoint,
            "requestsByMethod": requests_by_method,
            "recentActivity": [
                {
                    "id": r.id,
                    "apiKeyId": r.apiKeyId,
                    "endpoint": r.endpoint,
                    "method": r.method,
                    "statusCode": r.statusCode,
                    "responseTime": r.responseTime,
                    "timestamp": r.timestamp
                }
                for r in recent_activity
            ]
        }


# Singleton instance
usage_analytics_service = UsageAnalyticsService()
