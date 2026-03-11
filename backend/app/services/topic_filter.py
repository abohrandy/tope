"""Topic filtering service – assigns topics to articles based on keyword matching."""

import logging
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Article, Topic

logger = logging.getLogger(__name__)


def filter_articles():
    """Assign topics to all articles that have topic='General' or topic is None."""
    db: Session = SessionLocal()
    try:
        topics = db.query(Topic).all()
        keyword_map = {}
        for topic in topics:
            words = [w.strip().lower() for w in topic.keywords.split(",") if w.strip()]
            keyword_map[topic.name] = words

        # Get unclassified articles
        articles = (
            db.query(Article)
            .filter((Article.topic == None) | (Article.topic == "General"))
            .all()
        )

        classified = 0
        for article in articles:
            title_lower = article.title.lower()
            matched_topic = None
            for topic_name, keywords in keyword_map.items():
                for kw in keywords:
                    if kw in title_lower:
                        matched_topic = topic_name
                        break
                if matched_topic:
                    break

            article.topic = matched_topic or "General"
            if matched_topic:
                classified += 1

        db.commit()
        logger.info(f"Topic filter: {classified}/{len(articles)} articles classified.")
    except Exception as e:
        db.rollback()
        logger.error(f"Topic filter error: {e}")
    finally:
        db.close()
