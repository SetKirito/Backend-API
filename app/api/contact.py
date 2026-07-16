from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.contact_controller import ContactController
from app.core.database import SessionLocal
from app.repositories.contact_repository import ContactRepository
from app.schemas.contact import ContactRequest
from app.services.ai_service import AIService
from app.services.contact_service import ContactService
from app.services.email_service import EmailService

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/api/health")
async def health():
    return {"status": "ok"}


@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    repository = ContactRepository(db)
    service = ContactService(repository, ai_service=AIService(), email_service=EmailService())
    controller = ContactController(service)
    return await controller.get_metrics()


@router.post("/api/contact", status_code=201)
async def create_contact(data: ContactRequest, db: Session = Depends(get_db)):
    repository = ContactRepository(db)
    service = ContactService(repository, ai_service=AIService(), email_service=EmailService())
    controller = ContactController(service)
    return await controller.create_contact(data)
