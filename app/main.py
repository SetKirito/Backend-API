from fastapi import FastAPI

from app.api.contact import router as contact_router
from app.core.config import settings
from app.core.database import lifespan
from app.core.exception_handlers import register_exception_handlers
from app.core.middleware import RequestLoggingMiddleware

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(RequestLoggingMiddleware)
register_exception_handlers(app)
app.include_router(contact_router)
