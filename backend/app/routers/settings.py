"""Router for email settings."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import EmailSettings
from app.schemas import EmailSettingsUpdate, EmailSettingsOut

router = APIRouter(prefix="/api/settings", tags=["Settings"])


@router.get("/email", response_model=EmailSettingsOut)
def get_email_settings(db: Session = Depends(get_db)):
    settings = db.query(EmailSettings).first()
    if not settings:
        raise HTTPException(404, "Email settings not configured.")
    return settings


@router.put("/email", response_model=EmailSettingsOut)
def update_email_settings(payload: EmailSettingsUpdate, db: Session = Depends(get_db)):
    settings = db.query(EmailSettings).first()
    if not settings:
        settings = EmailSettings()
        db.add(settings)
    for key, val in payload.model_dump(exclude_unset=True).items():
        setattr(settings, key, val)
    db.commit()
    db.refresh(settings)
    return settings
