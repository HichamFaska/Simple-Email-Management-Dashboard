"""Extraction des champs utiles a partir d'un message email brut."""

from email.utils import parsedate_to_datetime


def parse_email_message(message, message_id=None):
    """Transformer un message email en dictionnaire simple."""
    subject = message.get("Subject", "(Sans objet)")
    sender = message.get("From", "Inconnu")
    recipient = message.get("To", "Inconnu")
    date_raw = message.get("Date")
    parsed_date = None

    if date_raw:
        try:
            parsed_date = parsedate_to_datetime(date_raw)
        except Exception:
            parsed_date = None

    body = _extract_body(message)
    return {
        "id": message_id,
        "from": sender,
        "to": recipient,
        "subject": subject,
        "body": body,
        "date": parsed_date,
    }


def _extract_body(message):
    """Extraire le texte du message (priorite au plain text)."""
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if content_type == "text/plain" and "attachment" not in disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode(errors="ignore")
        return "(Contenu non textuel)"
    payload = message.get_payload(decode=True)
    if payload:
        return payload.decode(errors="ignore")
    return str(message.get_payload() or "")
