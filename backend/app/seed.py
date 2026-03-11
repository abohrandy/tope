"""Seed default data into the database."""

from app.database import SessionLocal
from app.models import Site, Topic, EmailSettings


DEFAULT_SITES = [
    {"name": "Proshare", "url": "https://www.proshareng.com/", "rss_feed": None},
    {"name": "The Guardian Nigeria", "url": "https://guardian.ng/", "rss_feed": "https://guardian.ng/feed/"},
    {"name": "ThisDay Live", "url": "https://www.thisdaylive.com/", "rss_feed": "https://www.thisdaylive.com/feed/"},
    {"name": "The Cable", "url": "https://www.thecable.ng/", "rss_feed": "https://www.thecable.ng/feed"},
    {"name": "Punch Nigeria", "url": "https://punchng.com/", "rss_feed": "https://punchng.com/feed/"},
    {"name": "Vanguard Nigeria", "url": "https://www.vanguardngr.com/", "rss_feed": "https://www.vanguardngr.com/feed/"},
    {"name": "The Nigeria Lawyer", "url": "https://thenigerialawyer.com/", "rss_feed": "https://thenigerialawyer.com/feed/"},
    {"name": "BusinessDay", "url": "https://businessday.ng/", "rss_feed": "https://businessday.ng/feed/"},
    {"name": "Lawyard", "url": "https://www.lawyard.ng/category/news/", "rss_feed": None},
    {"name": "NCDC COVID-19", "url": "https://covid19.ncdc.gov.ng/", "rss_feed": None},
    {"name": "NIPC", "url": "https://nipc.gov.ng/", "rss_feed": None},
    {"name": "Nairametrics", "url": "https://nairametrics.com/category/nigeria-business-news/", "rss_feed": "https://nairametrics.com/feed/"},
    {"name": "Proshare Business", "url": "https://www.proshareng.com/business", "rss_feed": None},
    {"name": "Financial Nigeria", "url": "http://www.financialnigeria.com/", "rss_feed": None},
]

DEFAULT_TOPICS = [
    {"name": "Legal", "keywords": "court,lawyer,judgment,justice,litigation,tribunal,law,legal,ruling"},
    {"name": "Economy", "keywords": "inflation,gdp,finance,cbn,economy,economic,fiscal,budget,revenue,trade"},
    {"name": "Banking", "keywords": "bank,interest rate,monetary policy,deposit,lending,apex bank,banking,fintech"},
]


def seed_database():
    """Insert default sites, topics, and email settings if tables are empty."""
    db = SessionLocal()
    try:
        # Seed sites
        if db.query(Site).count() == 0:
            for s in DEFAULT_SITES:
                db.add(Site(**s))
            db.commit()
            print(f"✓ Seeded {len(DEFAULT_SITES)} default sites")

        # Seed topics
        if db.query(Topic).count() == 0:
            for t in DEFAULT_TOPICS:
                db.add(Topic(**t))
            db.commit()
            print(f"✓ Seeded {len(DEFAULT_TOPICS)} default topics")

        # Seed email settings
        if db.query(EmailSettings).count() == 0:
            db.add(EmailSettings(
                sender_email="",
                smtp_host="smtp.gmail.com",
                smtp_port=587,
                subject_template="Morning News Brief – {date}",
            ))
            db.commit()
            print("✓ Seeded default email settings")

    finally:
        db.close()
