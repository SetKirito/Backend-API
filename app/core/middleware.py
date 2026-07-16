import time
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.logging import request_logger, error_logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()
        client_ip = request.client.host if request.client else "unknown"

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            error_logger.exception(
                "Exception occurred\nTime: %s\nMethod: %s\nURL: %s\nStatus: 500\nIP: %s\nDuration: %.2f ms",
                request.method,
                request.url.path,
                client_ip,
                duration_ms,
            )
            raise

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        request_logger.info(
            "Time: %s\nMethod: %s\nURL: %s\nStatus: %s\nIP: %s\nDuration: %.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            client_ip,
            duration_ms,
        )
        return response
