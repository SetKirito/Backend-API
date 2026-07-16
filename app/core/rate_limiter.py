from collections import defaultdict, deque
from time import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int = 5, window_seconds: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time()
        window_start = now - self.window_seconds
        bucket = self.requests[client_ip]

        while bucket and bucket[0] <= window_start:
            bucket.popleft()

        if len(bucket) >= self.limit:
            return JSONResponse(status_code=429, content={"success": False, "message": "Too many requests"})

        bucket.append(now)
        return await call_next(request)
