from __future__ import annotations
import time
import uuid
import logging
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Dict, Callable
from collections import defaultdict
from .config import settings

logger = logging.getLogger(__name__)

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add unique request ID to each request for tracing."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting by IP address."""
    
    def __init__(self, app, rpm: int = 60):
        super().__init__(app)
        self.rpm = rpm
        self.requests: Dict[str, list] = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting for health checks
        if request.url.path in ["/healthz", "/version"]:
            return await call_next(request)
        
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        minute_ago = now - 60
        
        # Clean old requests
        self.requests[client_ip] = [ts for ts in self.requests[client_ip] if ts > minute_ago]
        
        # Check limit
        if len(self.requests[client_ip]) >= self.rpm:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            raise HTTPException(status_code=429, detail="Too many requests")
        
        # Record request
        self.requests[client_ip].append(now)
        
        return await call_next(request)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Log requests with request ID."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = getattr(request.state, "request_id", "unknown")
        start_time = time.time()
        
        logger.info(f"[{request_id}] {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        logger.info(f"[{request_id}] {response.status_code} {duration:.3f}s")
        
        return response
