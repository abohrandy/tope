"""Pydantic schemas for request/response validation."""

from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr


# ── Sites ──────────────────────────────────────────────
class SiteBase(BaseModel):
    name: str
    url: str
    rss_feed: Optional[str] = None
    is_active: bool = True


class SiteCreate(SiteBase):
    pass


class SiteUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    rss_feed: Optional[str] = None
    is_active: Optional[bool] = None


class SiteOut(SiteBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Topics ─────────────────────────────────────────────
class TopicBase(BaseModel):
    name: str
    keywords: str  # comma-separated


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    name: Optional[str] = None
    keywords: Optional[str] = None


class TopicOut(TopicBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Articles ───────────────────────────────────────────
class ArticleOut(BaseModel):
    id: int
    title: str
    url: str
    source: Optional[str] = None
    topic: Optional[str] = None
    published_date: Optional[datetime] = None
    date_scraped: Optional[datetime] = None
    sent_status: bool = False

    class Config:
        from_attributes = True


# ── Email Recipients ───────────────────────────────────
class RecipientBase(BaseModel):
    name: str
    email: str
    active: bool = True


class RecipientCreate(RecipientBase):
    pass


class RecipientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    active: Optional[bool] = None


class RecipientOut(RecipientBase):
    id: int

    class Config:
        from_attributes = True


# ── Digests ────────────────────────────────────────────
class DigestOut(BaseModel):
    id: int
    date: date
    articles_sent: int
    email_sent_time: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Email Settings ─────────────────────────────────────
class EmailSettingsBase(BaseModel):
    sender_email: Optional[str] = None
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    subject_template: str = "Morning News Brief – {date}"


class EmailSettingsUpdate(EmailSettingsBase):
    pass


class EmailSettingsOut(EmailSettingsBase):
    id: int

    class Config:
        from_attributes = True


# ── Dashboard ──────────────────────────────────────────
class DashboardStats(BaseModel):
    articles_today: int
    total_articles: int
    active_sources: int
    active_topics: int
    active_recipients: int
    last_digest_date: Optional[str] = None
    last_digest_articles: Optional[int] = None
