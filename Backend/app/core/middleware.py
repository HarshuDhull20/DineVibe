# app/core/middleware.py

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict

# ===============================
# Simple Rate Limit Storage
# ===============================

REQUEST_LOG = defaultdict(list)
RATE_LIMIT = 100  # requests per 1 minute


class SecurityMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        client_ip = request.client.host

        # ===============================
        # Basic Rate Limiting
        # ===============================

        current_time = time.time()
        REQUEST_LOG[client_ip] = [
            t for t in REQUEST_LOG[client_ip]
            if current_time - t < 60
        ]

        if len(REQUEST_LOG[client_ip]) > RATE_LIMIT:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"}
            )

        REQUEST_LOG[client_ip].append(current_time)

        # ===============================
        # Continue Request
        # ===============================

        response = await call_next(request)

        # ===============================
        # Security Headers
        # ===============================

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # ===============================
        # Response Time Header
        # ===============================

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(round(process_time, 4))

        return response
