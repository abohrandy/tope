"""CRUD router for topics."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Topic
from app.schemas import TopicCreate, TopicUpdate, TopicOut

router = APIRouter(prefix="/api/topics", tags=["Topics"])


@router.get("/", response_model=List[TopicOut])
def list_topics(db: Session = Depends(get_db)):
    return db.query(Topic).order_by(Topic.name).all()


@router.post("/", response_model=TopicOut, status_code=201)
def create_topic(payload: TopicCreate, db: Session = Depends(get_db)):
    existing = db.query(Topic).filter(Topic.name == payload.name).first()
    if existing:
        raise HTTPException(400, "A topic with this name already exists.")
    topic = Topic(**payload.model_dump())
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


@router.put("/{topic_id}", response_model=TopicOut)
def update_topic(topic_id: int, payload: TopicUpdate, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(404, "Topic not found.")
    for key, val in payload.model_dump(exclude_unset=True).items():
        setattr(topic, key, val)
    db.commit()
    db.refresh(topic)
    return topic


@router.delete("/{topic_id}", status_code=204)
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(404, "Topic not found.")
    db.delete(topic)
    db.commit()
