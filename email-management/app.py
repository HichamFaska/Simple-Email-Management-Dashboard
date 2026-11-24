"""Point d'entree de l'application Dash."""

from dash import Dash, Input, Output, State, html

import config
from alerts.alert_manager import check_alert, send_alert_email
from analytics.classifier import classify_email
from analytics.statistics import compute_kpis
from components.charts import fig_emails_by_category, fig_emails_per_day, fig_emails_per_hour
from components.email_table import build_email_table
from components.layout import alerts_tab, build_layout, dashboard_tab, emails_tab, send_tab
from data.sample_emails import build_sample_emails
from services.email_receiver import fetch_recent_emails
from services.email_sender import send_email

app = Dash(__name__)
app.title = "Email Management Dashboard"

# Stockage en memoire (pas de base de donnees).
INBOX = build_sample_emails()
SENT_COUNT = 0


def get_emails():
    """Retourner les emails selon le mode (simulation ou reel)."""
    if config.is_simulation():
        return INBOX

    try:
        fetched = fetch_recent_emails(limit=20)
        for item in fetched:
            item["category"] = classify_email(item.get("subject", ""), item.get("body", ""))
        return fetched if fetched else INBOX
    except Exception:
        return INBOX


app.layout = build_layout(compute_kpis(INBOX, SENT_COUNT), INBOX)


@app.callback(Output("tab-content", "children"), Input("main-tabs", "value"))
def render_tab(tab_value):
    emails = get_emails()
    if tab_value == "tab-dashboard":
        kpis = compute_kpis(emails, SENT_COUNT)
        return dashboard_tab(
            kpis,
            emails,
            fig_day=fig_emails_per_day(emails),
            fig_hour=fig_emails_per_hour(emails),
            fig_cat=fig_emails_by_category(emails),
            table=build_email_table(emails, limit=5),
        )
    if tab_value == "tab-emails":
        return emails_tab(emails)
    if tab_value == "tab-send":
        return send_tab()
    if tab_value == "tab-alerts":
        return alerts_tab()
    return html.Div("Onglet inconnu.")


@app.callback(Output("email-body-view", "children"), Input("email-select", "value"))
def show_email_body(email_id):
    if email_id is None or email_id == "":
        return "Selectionnez un email pour afficher son contenu."
    emails = get_emails()
    for item in emails:
        if str(item.get("id")) == str(email_id):
            body = item.get("body", "")
            return body or "(Message vide)"
    return "Email introuvable."


@app.callback(
    Output("send-result", "children"),
    Input("send-btn", "n_clicks"),
    State("send-to", "value"),
    State("send-subject", "value"),
    State("send-body", "value"),
    prevent_initial_call=True,
)
def handle_send_email(n_clicks, to_address, subject, body):
    global SENT_COUNT
    if not to_address or not subject or not body:
        return "Merci de remplir le destinataire, le sujet et le message."

    if config.is_simulation():
        SENT_COUNT += 1
        return "Mode simulation: email enregistre localement (non envoye)."

    try:
        send_email(to_address, subject, body)
        SENT_COUNT += 1
        return "Email envoye avec succes."
    except Exception as exc:
        return f"Erreur lors de l'envoi: {exc}"


@app.callback(
    Output("alert-result", "children"),
    Input("alert-check-btn", "n_clicks"),
    State("alert-category", "value"),
    State("alert-threshold", "value"),
    State("alert-period", "value"),
    prevent_initial_call=True,
)
def handle_alert_check(n_clicks, category, threshold, period):
    emails = get_emails()
    try:
        threshold_value = int(threshold)
    except (TypeError, ValueError):
        return "Le seuil doit etre un nombre entier."

    result = check_alert(emails, category, threshold_value, period)
    message = result["message"]

    if result["triggered"] and config.ALERT_SEND_EMAIL and config.ALERT_TO:
        sent_ok, send_msg = send_alert_email(
            config.ALERT_TO, category, result["count"], period, threshold_value
        )
        message = f"{message} {send_msg}"

    color = "#c0392b" if result["triggered"] else "#1e7e34"
    return html.Div(message, style={"color": color, "fontWeight": "bold"})


if __name__ == "__main__":
    app.run(debug=True)
