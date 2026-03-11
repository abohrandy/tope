"""Email sender service – sends HTML digest via SMTP."""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

from app.database import SessionLocal
from app.models import EmailSettings, EmailRecipient

logger = logging.getLogger(__name__)


def _get_settings_and_recipients():
    """Load email config and active recipients from the DB."""
    db = SessionLocal()
    try:
        settings = db.query(EmailSettings).first()
        recipients = (
            db.query(EmailRecipient)
            .filter(EmailRecipient.active == True)
            .all()
        )
        return settings, [r.email for r in recipients]
    finally:
        db.close()


def send_digest_email(html_body: str, subject: str) -> bool:
    """Send the digest email to all active recipients. Returns True on success."""
    settings, recipient_emails = _get_settings_and_recipients()

    if not settings or not settings.sender_email:
        logger.warning("Email settings not configured – skipping send.")
        return False

    if not recipient_emails:
        logger.warning("No active recipients – skipping send.")
        return False

    if not settings.smtp_user or not settings.smtp_password:
        logger.warning("SMTP credentials not set – skipping send.")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = settings.sender_email
        msg["To"] = ", ".join(recipient_emails)
        msg["Subject"] = subject

        # Plain-text fallback
        plain = "Your daily news digest is available. Please view this email in an HTML-capable client."
        msg.attach(MIMEText(plain, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(settings.smtp_user, settings.smtp_password)
            server.sendmail(settings.sender_email, recipient_emails, msg.as_string())

        logger.info(f"Digest email sent to {len(recipient_emails)} recipients.")
        return True

    except Exception as e:
        logger.error(f"Email send error: {e}")
        return False
