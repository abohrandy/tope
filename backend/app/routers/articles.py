"""Router for listing and filtering articles."""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models import Article
from app.schemas import ArticleOut

router = APIRouter(prefix="/api/articles", tags=["Articles"])


@router.get("/", response_model=List[ArticleOut])
def list_articles(
    source: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    sent: Optional[bool] = Query(None),
    date_from: Optional[str] = Query(None, description="YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="YYYY-MM-DD"),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(Article)

    if source:
        q = q.filter(Article.source == source)
    if topic:
        q = q.filter(Article.topic == topic)
    if sent is not None:
        q = q.filter(Article.sent_status == sent)
    if date_from:
        q = q.filter(Article.date_scraped >= datetime.fromisoformat(date_from))
    if date_to:
        q = q.filter(Article.date_scraped <= datetime.fromisoformat(date_to + "T23:59:59"))
    if search:
        q = q.filter(Article.title.ilike(f"%{search}%"))

    total = q.count()
    articles = (
        q.order_by(desc(Article.date_scraped))
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return articles
