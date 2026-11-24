"""Calcul des statistiques a partir d'une liste d'emails."""

from collections import Counter
from datetime import datetime

import pandas as pd

from analytics.classifier import classify_email


def _to_dataframe(emails):
    """Construire un DataFrame pandas a partir d'emails en memoire."""
    rows = []
    for email_item in emails:
        category = email_item.get("category") or classify_email(
            email_item.get("subject", ""), email_item.get("body", "")
        )
        rows.append(
            {
                "id": email_item.get("id"),
                "from": email_item.get("from", "Inconnu"),
                "to": email_item.get("to", "Inconnu"),
                "subject": email_item.get("subject", "(Sans objet)"),
                "body": email_item.get("body", ""),
                "date": email_item.get("date"),
                "category": category,
            }
        )
    df = pd.DataFrame(rows)
    if not df.empty and "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def build_email_dataframe(emails):
    """Retourner un DataFrame enrichi (avec categorie)."""
    return _to_dataframe(emails)


def compute_kpis(emails, sent_count=0):
    """Calculer les cartes statistiques du dashboard."""
    df = _to_dataframe(emails)
    total_received = len(df)
    category_counts = df["category"].value_counts().to_dict() if not df.empty else {}
    return {
        "total_received": total_received,
        "total_sent": sent_count,
        "orders": int(category_counts.get("Commande", 0)),
        "complaints": int(category_counts.get("Reclamation", 0)),
    }


def emails_per_day(emails):
    """Compter les emails recus par jour."""
    df = _to_dataframe(emails)
    if df.empty or df["date"].isna().all():
        return pd.DataFrame({"day": [], "count": []})
    tmp = df.dropna(subset=["date"]).copy()
    tmp["day"] = tmp["date"].dt.date
    grouped = tmp.groupby("day").size().reset_index(name="count")
    grouped["day"] = pd.to_datetime(grouped["day"])
    return grouped.sort_values("day")


def emails_per_hour(emails):
    """Compter les emails recus par heure (0-23)."""
    df = _to_dataframe(emails)
    if df.empty or df["date"].isna().all():
        return pd.DataFrame({"hour": [], "count": []})
    tmp = df.dropna(subset=["date"]).copy()
    tmp["hour"] = tmp["date"].dt.hour
    grouped = tmp.groupby("hour").size().reset_index(name="count")
    all_hours = pd.DataFrame({"hour": list(range(24))})
    merged = all_hours.merge(grouped, on="hour", how="left").fillna({"count": 0})
    merged["count"] = merged["count"].astype(int)
    return merged


def emails_by_category(emails):
    """Compter les emails par categorie."""
    df = _to_dataframe(emails)
    if df.empty:
        return pd.DataFrame({"category": [], "count": []})
    grouped = df.groupby("category").size().reset_index(name="count")
    return grouped.sort_values("count", ascending=False)


def latest_emails(emails, limit=5):
    """Retourner les derniers emails tries par date decroissante."""
    df = _to_dataframe(emails)
    if df.empty:
        return df
    df = df.sort_values("date", ascending=False, na_position="last").head(limit)
    return df
