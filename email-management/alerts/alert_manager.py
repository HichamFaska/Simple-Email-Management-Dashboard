"""Gestion des alertes: verification de seuil et notification optionnelle."""

from datetime import datetime, timedelta

from analytics.statistics import _to_dataframe
from services.email_sender import send_email


def _filter_by_period(emails, period):
    """Filtrer les emails par periode (heure ou jour)."""
    df = _to_dataframe(emails)
    if df.empty or df["date"].isna().all():
        return df

    now = datetime.now()
    if period == "heure":
        cutoff = now - timedelta(hours=1)
    else:
        cutoff = now - timedelta(days=1)
    return df[df["date"] >= cutoff]


def check_alert(emails, category, threshold, period):
    """Verifier si le nombre d'emails depasse le seuil pour la categorie/period."""
    df = _filter_by_period(emails, period)
    if df.empty:
        count = 0
    else:
        count = int((df["category"] == category).sum())

    triggered = count >= int(threshold)
    message = (
        f"Alerte: {count} email(s) dans la categorie '{category}' "
        f"sur la derniere {period} (seuil: {threshold})."
    )
    return {
        "triggered": triggered,
        "count": count,
        "message": message if triggered else "Aucune alerte declenchee.",
    }


def send_alert_email(to_address, category, count, period, threshold):
    """Envoyer un email d'alerte si une adresse est fournie."""
    if not to_address:
        return False, "Aucune adresse de destination configuree (ALERT_TO)."

    subject = f"[Alerte Dashboard] {category} - seuil depasse"
    body = (
        f"Une alerte a ete declenchee par le dashboard email.\n\n"
        f"Categorie: {category}\n"
        f"Periode: derniere {period}\n"
        f"Nombre detecte: {count}\n"
        f"Seuil: {threshold}\n"
    )
    try:
        send_email(to_address, subject, body)
        return True, "Email d'alerte envoye."
    except Exception as exc:
        return False, f"Echec d'envoi de l'alerte: {exc}"
