"""Configuration centralisee, chargee depuis l'environnement ou le fichier .env."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# "simulation" utilise les donnees fictives, "real" utilise IMAP/SMTP.
MODE = os.getenv("EMAIL_MODE", "simulation").strip().lower()

IMAP_HOST = os.getenv("IMAP_HOST", "imap.gmail.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
IMAP_USER = os.getenv("IMAP_USER", "")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD", "")
IMAP_MAILBOX = os.getenv("IMAP_MAILBOX", "INBOX")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)

ALERT_TO = os.getenv("ALERT_TO", "")
ALERT_SEND_EMAIL = os.getenv("ALERT_SEND_EMAIL", "false").strip().lower() in {
    "1",
    "true",
    "yes",
}


def is_simulation():
    """Verifier si l'application tourne sans service externe."""
    return MODE != "real"


def is_mail_configured():
    """Verifier que les identifiants necessaires sont presents."""
    return bool(IMAP_USER and IMAP_PASSWORD and SMTP_USER and SMTP_PASSWORD)
