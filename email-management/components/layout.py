"""Mise en page principale de l'application Dash avec sidebar CSS."""

from dash import dcc, html

from config import MODE


def _card(title, value):
    """Carte statistique simple."""
    return html.Div(
        className="card",
        children=[
            html.Div(title, className="card-label"),
            html.Div(str(value), className="card-value"),
        ],
    )


def _nav_button(button_id, label):
    return html.Button(label, id=button_id, n_clicks=0, className="nav-btn")


def build_layout(kpis, emails, alert_message=""):
    """Construire la mise en page avec sidebar."""
    mode_label = "Simulation" if MODE != "real" else "Reel (IMAP/SMTP)"

    return html.Div(
        className="app-layout",
        children=[
            html.Aside(
                className="sidebar",
                children=[
                    html.Div("Email Dashboard", className="sidebar-title"),
                    _nav_button("nav-dashboard", "Dashboard"),
                    _nav_button("nav-emails", "Emails"),
                    _nav_button("nav-send", "Envoyer un email"),
                    _nav_button("nav-alerts", "Alertes"),
                    html.Div(f"Mode: {mode_label}", className="sidebar-footer"),
                ],
            ),
            html.Main(
                className="main-content",
                children=[
                    html.H1("Email Management Dashboard", className="page-title"),
                    dcc.Store(id="active-page", data="dashboard"),
                    html.Div(id="tab-content", children=[dashboard_tab(kpis, emails)]),
                    dcc.Store(id="stored-alert-message", data=alert_message),
                ],
            ),
        ],
    )


def dashboard_tab(kpis, emails, fig_day=None, fig_hour=None, fig_cat=None, table=None):
    """Contenu de l'onglet Dashboard."""
    return html.Div(
        children=[
            html.Div(
                className="cards-row",
                children=[
                    _card("Emails recus (total)", kpis.get("total_received", 0)),
                    _card("Emails envoyes (total)", kpis.get("total_sent", 0)),
                    _card("Commandes", kpis.get("orders", 0)),
                    _card("Reclamations", kpis.get("complaints", 0)),
                ],
            ),
            html.Div(
                className="charts-grid",
                children=[
                    html.Div(className="chart-box", children=[dcc.Graph(id="fig-per-day", figure=fig_day)]),
                    html.Div(className="chart-box", children=[dcc.Graph(id="fig-per-hour", figure=fig_hour)]),
                    html.Div(className="chart-box", children=[dcc.Graph(id="fig-by-category", figure=fig_cat)]),
                ],
            ),
            html.H3("5 derniers emails", className="section-title"),
            html.Div(id="latest-table", children=table if table is not None else []),
        ]
    )


def emails_tab(emails):
    """Contenu de l'onglet Emails."""
    options = []
    for item in emails[:20]:
        date_value = item.get("date")
        date_label = ""
        if date_value is not None:
            try:
                date_label = date_value.strftime("%Y-%m-%d %H:%M")
            except Exception:
                date_label = str(date_value)
        subject = item.get("subject", "(Sans objet)")
        options.append({"label": f"{date_label} - {subject}", "value": str(item.get("id"))})

    return html.Div(
        className="panel",
        children=[
            html.H3("Consulter le contenu d'un email", className="section-title"),
            html.Label("Email", className="form-label"),
            dcc.Dropdown(id="email-select", options=options, placeholder="Choisir un email...", className="form-dropdown"),
            html.Pre(id="email-body-view", className="email-body", children="Selectionnez un email pour afficher son contenu."),
        ]
    )


def send_tab():
    """Contenu de l'onglet envoi d'email."""
    return html.Div(
        className="panel",
        children=[
            html.H3("Envoyer un email (mode reel requis pour l'envoi)", className="section-title"),
            html.Label("Destinataire", className="form-label"),
            dcc.Input(id="send-to", type="text", placeholder="destinataire@email.com", className="form-input"),
            html.Label("Sujet", className="form-label"),
            dcc.Input(id="send-subject", type="text", placeholder="Sujet", className="form-input"),
            html.Label("Message", className="form-label"),
            dcc.Textarea(id="send-body", placeholder="Contenu du message", className="form-textarea"),
            html.Button("Envoyer", id="send-btn", n_clicks=0, className="primary-btn"),
            html.Div(id="send-result", className="result-box"),
        ]
    )


def alerts_tab():
    """Contenu de l'onglet alertes."""
    return html.Div(
        className="panel",
        children=[
            html.H3("Configurer une alerte", className="section-title"),
            html.Label("Categorie", className="form-label"),
            dcc.Dropdown(
                id="alert-category",
                options=[
                    {"label": "Commande", "value": "Commande"},
                    {"label": "Reclamation", "value": "Reclamation"},
                    {"label": "Devis", "value": "Devis"},
                    {"label": "Facture", "value": "Facture"},
                    {"label": "Autre", "value": "Autre"},
                ],
                value="Commande",
                className="form-dropdown",
            ),
            html.Label("Seuil (nombre d'emails)", className="form-label"),
            dcc.Input(id="alert-threshold", type="number", value=3, min=1, className="form-input"),
            html.Label("Periode", className="form-label"),
            dcc.RadioItems(
                id="alert-period",
                options=[{"label": "Derniere heure", "value": "heure"}, {"label": "Dernier jour", "value": "jour"}],
                value="jour",
                className="form-input",
            ),
            html.Button("Verifier l'alerte", id="alert-check-btn", n_clicks=0, className="primary-btn"),
            html.Div(id="alert-result", className="result-box"),
        ]
    )
