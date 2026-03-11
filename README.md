# News Monitoring & Daily Digest Application

A full-stack application that scrapes Nigerian news websites, filters by topics, and generates automated daily email digests for senior executives.

## Quick Start

### Backend (FastAPI)
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
- API docs: http://localhost:8000/docs
- On first run, the database is created and seeded with 14 news sources and 3 topics.

### Frontend (React)
```bash
cd frontend
npm install
npm run dev
```
- Dashboard: http://localhost:5173

## Architecture

```
backend/
  app/
    main.py            ← FastAPI entry, scheduler, CORS
    config.py          ← Environment settings
    database.py        ← SQLAlchemy engine/session
    models.py          ← 6 ORM models
    schemas.py         ← Pydantic validation
    seed.py            ← Default sites/topics/settings
    routers/           ← 7 API routers (sites, topics, articles, recipients, digests, dashboard, settings)
    services/
      scraper.py       ← RSS + HTML fallback scraper
      topic_filter.py  ← Keyword-based topic assignment
      digest.py        ← HTML email generator
      email_sender.py  ← SMTP email delivery
      scheduler.py     ← Daily workflow orchestrator
      archive.py       ← 90-day cleanup
frontend/
  src/
    pages/             ← Dashboard, Articles, Sites, Topics, Recipients, EmailLogs, Settings
    components/        ← Layout with sidebar navigation
```

## Features

| Feature | Details |
|---------|---------|
| **Scraping** | RSS via feedparser, HTML fallback via httpx |
| **Topic Filtering** | Keyword matching against article titles |
| **Digest Email** | HTML formatted, grouped by topic, clickable headlines |
| **Scheduling** | APScheduler cron job (configurable time) |
| **Archive** | Auto-delete articles > 90 days |
| **Admin Dashboard** | Dark-themed React UI for managing everything |

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and configure:
- `DATABASE_URL` – SQLite (default) or PostgreSQL connection string
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` – Email server
- `DIGEST_HOUR`, `DIGEST_MINUTE` – When to run the daily digest (24h format)

## Manual Digest Trigger

Click **"▶ Run Digest Now"** on the dashboard, or `POST /api/dashboard/trigger-digest`.
