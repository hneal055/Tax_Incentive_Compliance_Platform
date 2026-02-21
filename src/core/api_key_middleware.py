"""
Middleware for API key rate limiting and permission checks
"""
import logging
from typing import Optional, Callable
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timezone
import time

from src.utils.database import prisma
from src.services.rate_limit_service import rate_limit_service
from src.services.usage_analytics_service import usage_analytics_service

logger = logging.getLogger(__name__)


class ApiKeyMiddleware(BaseHTTPMiddleware):
    """
    Middleware for API key rate limiting, permission checks, and usage tracking
    """
    
    def __init__(self, app, exclude_paths: Optional[list] = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            "/"
        ]
    
    async def dispatch(self, request: Request, call_next: Callable):
        """Process request through rate limiting and permission checks"""
        
        # Skip middleware for excluded paths
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)
        
        # Extract API key from header
        api_key = request.headers.get("X-API-Key")
        
        if not api_key:
            # No API key provided - continue without rate limiting
            # (JWT authentication will handle this)
            return await call_next(request)
        
        start_time = time.time()
        
        try:
            # Verify and get API key from database
            api_key_record = await self._verify_and_get_api_key(api_key)
            
            if not api_key_record:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid API key"}
                )
            
            # Check if key is expired
            if api_key_record.expiresAt and api_key_record.expiresAt < datetime.now(timezone.utc):
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "API key has expired"}
                )
            
            # Check rate limit
            try:
                allowed, remaining, reset_time = await rate_limit_service.check_rate_limit(
                    api_key_id=api_key_record.id
                )
            except HTTPException as e:
                # Rate limit exceeded
                return JSONResponse(
                    status_code=e.status_code,
                    content={"detail": e.detail},
                    headers=e.headers or {}
                )
            
            # Check permissions for the endpoint
            if not await self._check_permissions(request, api_key_record):
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "Insufficient permissions for this endpoint"}
                )
            
            # Add rate limit headers to request state for response
            request.state.rate_limit_remaining = remaining
            request.state.rate_limit_reset = reset_time
            
            # Process request
            response = await call_next(request)
            
            # Add rate limit headers to response
            response.headers["X-RateLimit-Limit"] = str(rate_limit_service.default_limit)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_time)
            
            # Track usage (async, non-blocking)
            response_time = int((time.time() - start_time) * 1000)  # ms
            await usage_analytics_service.record_usage(
                api_key_id=api_key_record.id,
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code,
                response_time=response_time
            )
            
            # Note: lastUsedAt is updated via usage analytics service
            # to avoid adding a database write to every request
            
            return response
            
        except Exception as e:
            logger.error(f"Error in API key middleware: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"}
            )
    
    async def _verify_and_get_api_key(self, api_key: str):
        """Verify API key and retrieve from database"""
        from src.core.auth import hash_api_key
        
        hashed_key = hash_api_key(api_key)
        
        try:
            api_key_record = await prisma.apikey.find_first(
                where={"key": hashed_key}
            )
            return api_key_record
        except Exception as e:
            logger.error(f"Error verifying API key: {e}")
            return None
    
    async def _check_permissions(self, request: Request, api_key_record) -> bool:
        """Check if API key has required permissions for the endpoint"""
        # Define permission requirements for different endpoint patterns
        
        # Admin-only endpoints
        admin_patterns = [
            "/api/v1/api-keys/webhooks",
            "/api/v1/api-keys/audit-logs",
            "/api/v1/api-keys/bulk"
        ]
        
        # Write endpoints (require 'write' or 'admin' permission)
        write_methods = ["POST", "PUT", "PATCH", "DELETE"]
        
        # Check for admin-only endpoints
        for pattern in admin_patterns:
            if request.url.path.startswith(pattern):
                return "admin" in api_key_record.permissions
        
        # Check for write operations
        if request.method in write_methods:
            return "write" in api_key_record.permissions or "admin" in api_key_record.permissions
        
        # Read operations require at least 'read' permission
        return "read" in api_key_record.permissions
