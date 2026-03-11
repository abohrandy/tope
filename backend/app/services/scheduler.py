"""Scheduler service – orchestrates the daily digest workflow."""

import logging
from datetime import datetime, timezone, date

from app.database import SessionLocal
from app.models import Article, Digest, EmailSettings
from app.services.scraper import run_scraper
from app.services.topic_filter import filter_articles
from app.services.digest import generate_digest
from app.services.email_sender import send_digest_email
from app.services.archive import cleanup_old_articles

logger = logging.getLogger(__name__)


def run_daily_digest():
    """
    Full daily workflow:
    1. Scrape all active sites
    2. Filter articles by topic
    3. Generate digest HTML from unsent articles
    4. Send email
    5. Mark articles as sent
    6. Clean up old articles
    """
    logger.info("═══ Daily Digest Workflow Started ═══")

    # Step 1 – Scrape
    new_count = run_scraper()
    logger.info(f"Step 1: Scraped {new_count} new articles.")

    # Step 2 – Topic filtering
    filter_articles()
    logger.info("Step 2: Topic filtering complete.")

    # Step 3 – Generate digest
    html, article_ids = generate_digest()
    if not html:
        logger.info("No articles to send. Workflow finished.")
        return

    # Step 4 – Determine subject
    db = SessionLocal()
    try:
        settings = db.query(EmailSettings).first()
        subject_template = settings.subject_template if settings else "Morning News Brief – {date}"
        subject = subject_template.replace("{date}", date.today().strftime("%B %d, %Y"))

        # Step 4 – Send email
        sent = send_digest_email(html, subject)

        # Step 5 – Mark articles as sent
        if sent:
            db.query(Article).filter(Article.id.in_(article_ids)).update(
                {Article.sent_status: True}, synchronize_session="fetch"
            )

        # Log digest
        digest = Digest(
            date=date.today(),
            articles_sent=len(article_ids),
            email_sent_time=datetime.now(timezone.utc) if sent else None,
        )
        db.add(digest)
        db.commit()
        logger.info(f"Step 5: {'Sent' if sent else 'Generated (not sent – check email config)'} digest with {len(article_ids)} articles.")

    except Exception as e:
        db.rollback()
        logger.error(f"Digest workflow error: {e}")
    finally:
        db.close()

    # Step 6 – Cleanup
    cleanup_old_articles()
    logger.info("═══ Daily Digest Workflow Complete ═══")
