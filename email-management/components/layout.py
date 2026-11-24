"""Mise en page principale de l'application Dash."""

from dash import dcc, html

from config import MODE


def _card(title, value):
    """Carte statistique simple."""
    return html.Div(
        style={
            "backgroundColor": "#ffffff",
            "border": "1px solid #dce3ea",
            "borderRadius": "8px",
            "padding": "16px",
            "minWidth": "180px",
            "flex": "1",
        },
        children=[
            html.Div(title, style={"color": "#5b6b7a", "fontSize": "14px"}),
            html.Div(value, style={"fontSize": "28px", "fontWeight": "bold", "color": "#1f2d3d"}),
        ],
    )


def build_layout(kpis, emails, alert_message=""):
    """Construire la mise en page complete du dashboard."""
    mode_label = "Simulation" if MODE != "real" else "Reel (IMAP/SMTP)"

    return html.Div(
        style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f5f7fb", "minHeight": "100vh"},
        children=[
            html.Div(
                style={"padding": "20px 24px", "maxWidth": "1200px", "margin": "0 auto"},
                children=[
                    html.Div(
                        style={"display": "flex", "justifyContent": "space-between", "flexWrap": "wrap", "gap": "8px"},
                        children=[
                            html.H1("Email Management Dashboard", style={"margin": "0", "color": "#1f2d3d"}),
                            html.Div(
                                f"Mode: {mode_label}",
                                style={"alignSelf": "center", "padding": "6px 10px", "backgroundColor": "#e8eef5", "borderRadius": "6px"},
                            ),
                        ],
                    ),
                    dcc.Tabs(
                        id="main-tabs",
                        value="tab-dashboard",
                        children=[
                            dcc.Tab(label="Dashboard", value="tab-dashboard"),
                            dcc.Tab(label="Emails", value="tab-emails"),
                            dcc.Tab(label="Envoyer un email", value="tab-send"),
                            dcc.Tab(label="Alertes", value="tab-alerts"),
                        ],
                    ),
                    html.Div(id="tab-content", children=[dashboard_tab(kpis, emails)], style={"marginTop": "16px"}),
                    dcc.Store(id="stored-alert-message", data=alert_message),
                ],
            )
        ],
    )


def dashboard_tab(kpis, emails, fig_day=None, fig_hour=None, fig_cat=None, table=None):
    """Contenu de l'onglet Dashboard."""
    return html.Div(
        children=[
            html.Div(
                style={"display": "flex", "gap": "12px", "flexWrap": "wrap", "marginBottom": "16px"},
                children=[
                    _card("Emails recus (total)", kpis.get("total_received", 0)),
                    _card("Emails envoyes (total)", kpis.get("total_sent", 0)),
                    _card("Commandes", kpis.get("orders", 0)),
                    _card("Reclamations", kpis.get("complaints", 0)),
                ],
            ),
            html.Div(
                style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(280px, 1fr))", "gap": "16px"},
                children=[
                    dcc.Graph(id="fig-per-day", figure=fig_day),
                    dcc.Graph(id="fig-per-hour", figure=fig_hour),
                    dcc.Graph(id="fig-by-category", figure=fig_cat),
                ],
            ),
            html.H3("5 derniers emails"),
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
        children=[
            html.H3("Consulter le contenu d'un email"),
            dcc.Dropdown(id="email-select", options=options, placeholder="Choisir un email...", style={"maxWidth": "700px"}),
            html.Pre(
                id="email-body-view",
                style={"whiteSpace": "pre-wrap", "backgroundColor": "#ffffff", "padding": "12px", "border": "1px solid #dce3ea", "borderRadius": "6px", "marginTop": "12px"},
            ),
        ]
    )


def send_tab():
    """Contenu de l'onglet envoi d'email."""
    return html.Div(
        style={"maxWidth": "700px"},
        children=[
            html.H3("Envoyer un email (mode reel requis pour l'envoi)"),
            html.Label("Destinataire"),
            dcc.Input(id="send-to", type="text", placeholder="destinataire@email.com", style={"width": "100%", "marginBottom": "8px"}),
            html.Label("Sujet"),
            dcc.Input(id="send-subject", type="text", placeholder="Sujet", style={"width": "100%", "marginBottom": "8px"}),
            html.Label("Message"),
            dcc.Textarea(id="send-body", placeholder="Contenu du message", style={"width": "100%", "height": "140px", "marginBottom": "8px"}),
            html.Button("Envoyer", id="send-btn", n_clicks=0, style={"padding": "10px 14px"}),
            html.Div(id="send-result", style={"marginTop": "12px", "color": "#1f2d3d"}),
        ]
    )


def alerts_tab():
    """Contenu de l'onglet alertes."""
    return html.Div(
        style={"maxWidth": "700px"},
        children=[
            html.H3("Configurer une alerte"),
            html.Label("Categorie"),
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
                style={"marginBottom": "8px"},
            ),
            html.Label("Seuil (nombre d'emails)"),
            dcc.Input(id="alert-threshold", type="number", value=3, min=1, style={"width": "100%", "marginBottom": "8px"}),
            html.Label("Periode"),
            dcc.RadioItems(
                id="alert-period",
                options=[{"label": "Derniere heure", "value": "heure"}, {"label": "Dernier jour", "value": "jour"}],
                value="jour",
                style={"marginBottom": "8px"},
            ),
            html.Button("Verifier l'alerte", id="alert-check-btn", n_clicks=0, style={"padding": "10px 14px"}),
            html.Div(id="alert-result", style={"marginTop": "12px", "padding": "10px", "borderRadius": "6px", "backgroundColor": "#ffffff"}),
        ]
    )