from fastapi import FastAPI, HTTPException as FastAPIHTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import error_logger


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(FastAPIHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)


async def http_exception_handler(request: Request, exc: FastAPIHTTPException) -> JSONResponse:
    detail = exc.detail if isinstance(exc.detail, str) else "Bad request"
    error_logger.error(
        "HTTP exception\nMethod: %s\nURL: %s\nStatus: %s\nMessage: %s",
        request.method,
        request.url.path,
        exc.status_code,
        detail,
    )
    return JSONResponse(status_code=exc.status_code, content={"success": False, "message": detail})


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    error_logger.error(
        "Validation error\nMethod: %s\nURL: %s\nMessage: %s",
        request.method,
        request.url.path,
        str(exc),
    )
    return JSONResponse(status_code=422, content={"success": False, "message": "Validation error"})


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    error_logger.exception(
        "Unhandled exception\nMethod: %s\nURL: %s\nMessage: %s",
        request.method,
        request.url.path,
        str(exc),
    )
    return JSONResponse(status_code=500, content={"success": False, "message": "Internal server error"})
