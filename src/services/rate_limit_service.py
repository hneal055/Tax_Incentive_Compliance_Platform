"""
Rate Limiting Service using Redis
Implements per-API-key rate limiting
"""
import logging
from typing import Optional
from datetime import datetime, timedelta
import redis.asyncio as redis
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class RateLimitService:
    """Redis-based rate limiting service for API keys"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.default_limit = 1000  # requests per window
        self.default_window = 3600  # 1 hour in seconds
    
    async def initialize(self, redis_url: str = "redis://localhost:6379"):
        """
        Initialize Redis connection
        
        Args:
            redis_url: Redis connection URL
        """
        try:
            self.redis_client = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            # Test connection
            await self.redis_client.ping()
            logger.info("✅ Rate limiting service initialized with Redis")
        except Exception as e:
            logger.warning(f"⚠️  Redis connection failed: {e}")
            logger.warning("   Rate limiting will be disabled")
            self.redis_client = None
    
    async def shutdown(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("✅ Rate limiting service shut down")
    
    async def check_rate_limit(
        self,
        api_key_id: str,
        limit: Optional[int] = None,
        window: Optional[int] = None
    ) -> tuple[bool, int, int]:
        """
        Check if API key has exceeded rate limit
        
        Args:
            api_key_id: The API key ID to check
            limit: Maximum requests per window (defaults to self.default_limit)
            window: Time window in seconds (defaults to self.default_window)
            
        Returns:
            Tuple of (allowed: bool, remaining: int, reset_time: int)
            
        Raises:
            HTTPException: If rate limit is exceeded
        """
        if not self.redis_client:
            # If Redis is not available, allow all requests
            return (True, 999999, 0)
        
        limit = limit or self.default_limit
        window = window or self.default_window
        
        key = f"rate_limit:{api_key_id}"
        
        try:
            # Get current count
            current = await self.redis_client.get(key)
            
            if current is None:
                # First request in this window
                await self.redis_client.setex(key, window, 1)
                return (True, limit - 1, window)
            
            current_count = int(current)
            
            if current_count >= limit:
                # Rate limit exceeded
                ttl = await self.redis_client.ttl(key)
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Try again in {ttl} seconds.",
                    headers={"Retry-After": str(ttl)}
                )
            
            # Increment counter
            new_count = await self.redis_client.incr(key)
            ttl = await self.redis_client.ttl(key)
            
            return (True, limit - new_count, ttl)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            # On error, allow the request (fail open)
            return (True, limit, window)
    
    async def reset_rate_limit(self, api_key_id: str):
        """
        Reset rate limit for an API key
        
        Args:
            api_key_id: The API key ID to reset
        """
        if not self.redis_client:
            return
        
        key = f"rate_limit:{api_key_id}"
        try:
            await self.redis_client.delete(key)
            logger.info(f"Rate limit reset for key {api_key_id}")
        except Exception as e:
            logger.error(f"Failed to reset rate limit: {e}")
    
    async def get_current_usage(self, api_key_id: str) -> dict:
        """
        Get current rate limit usage for an API key
        
        Args:
            api_key_id: The API key ID to check
            
        Returns:
            Dictionary with usage information
        """
        if not self.redis_client:
            return {
                "current": 0,
                "limit": self.default_limit,
                "remaining": self.default_limit,
                "reset_in": 0
            }
        
        key = f"rate_limit:{api_key_id}"
        
        try:
            current = await self.redis_client.get(key)
            current_count = int(current) if current else 0
            ttl = await self.redis_client.ttl(key) if current else 0
            
            return {
                "current": current_count,
                "limit": self.default_limit,
                "remaining": max(0, self.default_limit - current_count),
                "reset_in": ttl if ttl > 0 else self.default_window
            }
        except Exception as e:
            logger.error(f"Failed to get rate limit usage: {e}")
            return {
                "current": 0,
                "limit": self.default_limit,
                "remaining": self.default_limit,
                "reset_in": self.default_window
            }


# Singleton instance
rate_limit_service = RateLimitService()
