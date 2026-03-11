"""Scraping service – fetches articles from news sites via RSS or HTML fallback."""

import logging
from datetime import datetime, timezone
from typing import List, Dict, Optional
from urllib.parse import urlparse

import feedparser
import httpx
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Site, Article

logger = logging.getLogger(__name__)


def _parse_published(entry) -> Optional[datetime]:
    """Try to extract a publish datetime from a feed entry."""
    for attr in ("published_parsed", "updated_parsed"):
        tp = getattr(entry, attr, None)
        if tp:
            try:
                from time import mktime
                return datetime.fromtimestamp(mktime(tp), tz=timezone.utc)
            except Exception:
                pass
    return None


def _scrape_rss(site: Site) -> List[Dict]:
    """Parse an RSS feed and return article dicts."""
    articles = []
    try:
        feed = feedparser.parse(site.rss_feed)
        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            if not title or not link:
                continue
            articles.append({
                "title": title,
                "url": link,
                "source": site.name,
                "published_date": _parse_published(entry),
            })
        logger.info(f"RSS: {site.name} → {len(articles)} articles")
    except Exception as e:
        logger.error(f"RSS error for {site.name}: {e}")
    return articles


def _scrape_html(site: Site) -> List[Dict]:
    """Fallback HTML scraper using httpx + basic parsing."""
    articles = []
    try:
        resp = httpx.get(site.url, timeout=30, follow_redirects=True, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NewsMonitor/1.0"
        })
        resp.raise_for_status()
        html = resp.text

        # Simple regex-based link extraction for headlines
        import re
        # Look for <a> tags with article-like hrefs
        domain = urlparse(site.url).netloc
        pattern = re.compile(
            r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]{20,})</a>',
            re.IGNORECASE,
        )
        seen_urls = set()
        for match in pattern.finditer(html):
            href, text = match.group(1).strip(), match.group(2).strip()
            # Normalise relative URLs
            if href.startswith("/"):
                href = f"https://{domain}{href}"
            # Only keep links from the same domain
            if domain not in href:
                continue
            # Skip navigation / short text
            if len(text) < 25 or href in seen_urls:
                continue
            seen_urls.add(href)
            articles.append({
                "title": text,
                "url": href,
                "source": site.name,
                "published_date": None,
            })
        logger.info(f"HTML: {site.name} → {len(articles)} articles")
    except Exception as e:
        logger.error(f"HTML scrape error for {site.name}: {e}")
    return articles


def scrape_site(site: Site) -> List[Dict]:
    """Scrape a single site – RSS first, HTML fallback."""
    if site.rss_feed:
        articles = _scrape_rss(site)
        if articles:
            return articles
    return _scrape_html(site)


def run_scraper() -> int:
    """Scrape all active sites and save new articles. Returns count of new articles."""
    db: Session = SessionLocal()
    new_count = 0
    try:
        sites = db.query(Site).filter(Site.is_active == True).all()
        logger.info(f"Scraping {len(sites)} active sites…")

        for site in sites:
            articles = scrape_site(site)
            for art in articles:
                # Duplicate check
                exists = db.query(Article).filter(Article.url == art["url"]).first()
                if exists:
                    continue
                db.add(Article(
                    title=art["title"],
                    url=art["url"],
                    source=art["source"],
                    published_date=art["published_date"],
                    date_scraped=datetime.now(timezone.utc),
                ))
                new_count += 1

        db.commit()
        logger.info(f"Scraper finished – {new_count} new articles saved.")
    except Exception as e:
        db.rollback()
        logger.error(f"Scraper error: {e}")
    finally:
        db.close()
    return new_count
