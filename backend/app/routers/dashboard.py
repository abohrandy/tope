"""Dashboard stats and digest trigger endpoint."""

from datetime import datetime, timezone, date
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Article, Site, Topic, EmailRecipient, Digest
from app.schemas import DashboardStats

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    today = date.today()

    articles_today = (
        db.query(Article)
        .filter(Article.date_scraped >= datetime.combine(today, datetime.min.time()))
        .count()
    )
    total_articles = db.query(Article).count()
    active_sources = db.query(Site).filter(Site.is_active == True).count()
    active_topics = db.query(Topic).count()
    active_recipients = db.query(EmailRecipient).filter(EmailRecipient.active == True).count()

    last_digest = db.query(Digest).order_by(Digest.date.desc()).first()

    return DashboardStats(
        articles_today=articles_today,
        total_articles=total_articles,
        active_sources=active_sources,
        active_topics=active_topics,
        active_recipients=active_recipients,
        last_digest_date=str(last_digest.date) if last_digest else None,
        last_digest_articles=last_digest.articles_sent if last_digest else None,
    )


@router.post("/trigger-digest")
async def trigger_digest(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Manually trigger the daily digest workflow."""
    from app.services.scheduler import run_daily_digest
    background_tasks.add_task(run_daily_digest)
    return {"message": "Digest workflow triggered in background."}
