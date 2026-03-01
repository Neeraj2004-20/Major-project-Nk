"""
Middleware & Error Handling
Rate limiting, custom error handling, request validation
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Callable
import time
from collections import defaultdict
from datetime import datetime, timedelta
from config import settings
from monitoring import performance_monitor, logger


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware - prevent abuse"""
    
    def __init__(self, app, requests_per_window: int = None, window_seconds: int = None):
        super().__init__(app)
        self.requests_per_window = requests_per_window or settings.API_RATE_LIMIT
        self.window_seconds = window_seconds or settings.RATE_LIMIT_WINDOW
        self.requests = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        if not settings.API_RATE_LIMIT or settings.ENV == 'development':
            return await call_next(request)
        
        client_ip = request.client.host
        now = time.time()
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < self.window_seconds
        ]
        
        # Check limit
        if len(self.requests[client_ip]) >= self.requests_per_window:
            logger.warning(f"⚠️ Rate limit exceeded for {client_ip}")
            return JSONResponse(
                status_code=429,
                content={"detail": f"Too many requests. Max {self.requests_per_window} per {self.window_seconds}s"}
            )
        
        self.requests[client_ip].append(now)
        return await call_next(request)


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """Track performance metrics"""
    
    async def dispatch(self, request: Request, call_next):
        if not settings.MONITOR_PERFORMANCE:
            return await call_next(request)
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            performance_monitor.record_request(
                endpoint=request.url.path,
                method=request.method,
                duration=duration,
                status_code=response.status_code
            )
            
            return response
        
        except Exception as e:
            duration = time.time() - start_time
            performance_monitor.record_request(
                endpoint=request.url.path,
                method=request.method,
                duration=duration,
                status_code=500,
                error=str(e)
            )
            raise


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Custom error handling"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        
        except HTTPException:
            raise
        
        except Exception as e:
            logger.error(f"Unhandled error at {request.url.path}: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "error_type": type(e).__name__,
                    "timestamp": datetime.now().isoformat()
                }
            )


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Validate and log requests"""
    
    async def dispatch(self, request: Request, call_next):
        # Log request
        if settings.LOG_REQUESTS:
            logger.info(f"[REQ] {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        # Log response
        if settings.LOG_REQUESTS:
            logger.info(f"[RES] {response.status_code} - {request.url.path}")
        
        return response


# Exception handlers
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle generic exceptions"""
    logger.error(f"Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An error occurred",
            "type": type(exc).__name__,
            "timestamp": datetime.now().isoformat()
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )


async def validation_exception_handler(request: Request, exc: Exception):
    """Handle validation errors"""
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "error": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )
