"""Graphiques Plotly pour le dashboard."""

import plotly.express as px

from analytics.statistics import emails_by_category, emails_per_day, emails_per_hour


def fig_emails_per_day(emails):
    """Courbe du nombre d'emails par jour."""
    df = emails_per_day(emails)
    if df.empty:
        fig = px.line(title="Emails recus par jour")
        fig.update_layout(xaxis_title="Jour", yaxis_title="Nombre d'emails")
        return fig
    fig = px.line(df, x="day", y="count", markers=True, title="Emails recus par jour")
    fig.update_layout(xaxis_title="Jour", yaxis_title="Nombre d'emails")
    return fig


def fig_emails_per_hour(emails):
    """Barres du nombre d'emails par heure."""
    df = emails_per_hour(emails)
    fig = px.bar(df, x="hour", y="count", title="Emails recus par heure")
    fig.update_layout(xaxis_title="Heure (0-23)", yaxis_title="Nombre d'emails")
    return fig


def fig_emails_by_category(emails):
    """Diagramme circulaire par categorie."""
    df = emails_by_category(emails)
    if df.empty:
        fig = px.pie(names=["Aucun"], values=[1], title="Repartition par categorie")
        return fig
    fig = px.pie(df, names="category", values="count", title="Repartition par categorie")
    return fig
