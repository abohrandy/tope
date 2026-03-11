"""CRUD router for email recipients."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import EmailRecipient
from app.schemas import RecipientCreate, RecipientUpdate, RecipientOut

router = APIRouter(prefix="/api/recipients", tags=["Email Recipients"])


@router.get("/", response_model=List[RecipientOut])
def list_recipients(db: Session = Depends(get_db)):
    return db.query(EmailRecipient).order_by(EmailRecipient.name).all()


@router.post("/", response_model=RecipientOut, status_code=201)
def create_recipient(payload: RecipientCreate, db: Session = Depends(get_db)):
    existing = db.query(EmailRecipient).filter(EmailRecipient.email == payload.email).first()
    if existing:
        raise HTTPException(400, "A recipient with this email already exists.")
    rec = EmailRecipient(**payload.model_dump())
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


@router.put("/{recipient_id}", response_model=RecipientOut)
def update_recipient(recipient_id: int, payload: RecipientUpdate, db: Session = Depends(get_db)):
    rec = db.query(EmailRecipient).filter(EmailRecipient.id == recipient_id).first()
    if not rec:
        raise HTTPException(404, "Recipient not found.")
    for key, val in payload.model_dump(exclude_unset=True).items():
        setattr(rec, key, val)
    db.commit()
    db.refresh(rec)
    return rec


@router.delete("/{recipient_id}", status_code=204)
def delete_recipient(recipient_id: int, db: Session = Depends(get_db)):
    rec = db.query(EmailRecipient).filter(EmailRecipient.id == recipient_id).first()
    if not rec:
        raise HTTPException(404, "Recipient not found.")
    db.delete(rec)
    db.commit()
