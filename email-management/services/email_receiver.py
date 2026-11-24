"""Reception des emails via IMAP (mode reel)."""

import imaplib
import email

from config import IMAP_HOST, IMAP_PORT, IMAP_USER, IMAP_PASSWORD, IMAP_MAILBOX
from services.email_parser import parse_email_message


def fetch_recent_emails(limit=5):
    """Recuperer les derniers emails de la boite IMAP configuree."""
    if not IMAP_USER or not IMAP_PASSWORD:
        raise ValueError("IMAP_USER et IMAP_PASSWORD doivent etre definis.")

    connection = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    try:
        connection.login(IMAP_USER, IMAP_PASSWORD)
        connection.select(IMAP_MAILBOX)
        status, data = connection.search(None, "ALL")
        if status != "OK":
            return []

        ids = data[0].split()
        latest_ids = ids[-limit:] if ids else []
        messages = []
        for msg_id in reversed(latest_ids):
            status, msg_data = connection.fetch(msg_id, "(RFC822)")
            if status != "OK" or not msg_data or not msg_data[0]:
                continue
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            messages.append(parse_email_message(msg, message_id=msg_id.decode(errors="ignore")))
        return messages
    finally:
        try:
            connection.logout()
        except Exception:
            pass
