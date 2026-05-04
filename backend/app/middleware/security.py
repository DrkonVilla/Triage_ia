from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger(__name__)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls=100, period=60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.requests = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        
        if client_ip in self.requests:
            timestamps = [t for t in self.requests[client_ip] if current_time - t < self.period]
            if len(timestamps) >= self.calls:
                raise HTTPException(status_code=429, detail="Demasiadas solicitudes")
            self.requests[client_ip] = timestamps
        else:
            self.requests[client_ip] = []
        
        self.requests[client_ip].append(current_time)
        return await call_next(request)