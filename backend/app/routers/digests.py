"""Router for digest email logs."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models import Digest
from app.schemas import DigestOut

router = APIRouter(prefix="/api/digests", tags=["Digests"])


@router.get("/", response_model=List[DigestOut])
def list_digests(db: Session = Depends(get_db)):
    return db.query(Digest).order_by(desc(Digest.date)).limit(100).all()
