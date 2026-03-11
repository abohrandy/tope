"""SQLAlchemy ORM models for the News Monitoring application."""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, Date
)
from app.database import Base


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False, unique=True)
    rss_feed = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    keywords = Column(Text, nullable=False)  # comma-separated
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(1000), nullable=False)
    url = Column(String(1000), nullable=False, unique=True, index=True)
    source = Column(String(255), nullable=True)
    topic = Column(String(255), nullable=True, default="General")
    published_date = Column(DateTime, nullable=True)
    date_scraped = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    sent_status = Column(Boolean, default=False, index=True)


class Digest(Base):
    __tablename__ = "digests"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    articles_sent = Column(Integer, default=0)
    email_sent_time = Column(DateTime, nullable=True)


class EmailRecipient(Base):
    __tablename__ = "email_recipients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    active = Column(Boolean, default=True)


class EmailSettings(Base):
    __tablename__ = "email_settings"

    id = Column(Integer, primary_key=True, index=True)
    sender_email = Column(String(255), nullable=True)
    smtp_host = Column(String(255), default="smtp.gmail.com")
    smtp_port = Column(Integer, default=587)
    smtp_user = Column(String(255), nullable=True)
    smtp_password = Column(String(255), nullable=True)
    subject_template = Column(String(500), default="Morning News Brief – {date}")
