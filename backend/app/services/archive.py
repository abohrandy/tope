"""Archive service – deletes articles older than 90 days."""

import logging
from datetime import datetime, timezone, timedelta

from app.database import SessionLocal
from app.models import Article

logger = logging.getLogger(__name__)

RETENTION_DAYS = 90


def cleanup_old_articles():
    """Delete articles older than RETENTION_DAYS."""
    db = SessionLocal()
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)
        count = db.query(Article).filter(Article.date_scraped < cutoff).delete()
        db.commit()
        if count:
            logger.info(f"Archive cleanup: deleted {count} articles older than {RETENTION_DAYS} days.")
    except Exception as e:
        db.rollback()
        logger.error(f"Archive cleanup error: {e}")
    finally:
        db.close()
