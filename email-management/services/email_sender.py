"""Envoi des emails via SMTP (mode reel)."""

import smtplib
from email.mime.text import MIMEText

from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM


def send_email(to_address, subject, body):
    """Envoyer un email simple en texte brut."""
    if not SMTP_USER or not SMTP_PASSWORD:
        raise ValueError("SMTP_USER et SMTP_PASSWORD doivent etre definis.")

    message = MIMEText(body, "plain", "utf-8")
    message["Subject"] = subject
    message["From"] = SMTP_FROM or SMTP_USER
    message["To"] = to_address

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(message["From"], [to_address], message.as_string())
    return True
