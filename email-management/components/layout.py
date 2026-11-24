"""Mise en page principale de l'application Dash avec sidebar Tailwind."""

from dash import dcc, html

from config import MODE


def _card(title, value):
    """Carte statistique simple."""
    return html.Div(
        className="bg-white border border-slate-200 rounded-lg p-4 flex-1 min-w-[180px] shadow-sm",
        children=[
            html.Div(title, className="text-slate-500 text-sm"),
            html.Div(str(value), className="text-2xl font-semibold text-slate-800 mt-1"),
        ],
    )


def _nav_button(button_id, label):
    return html.Button(
        label,
        id=button_id,
        n_clicks=0,
        className="w-full text-left px-4 py-2 rounded-md hover:bg-slate-700 text-slate-100 transition",
    )


def build_layout(kpis, emails, alert_message=""):
    """Construire la mise en page avec sidebar."""
    mode_label = "Simulation" if MODE != "real" else "Reel (IMAP/SMTP)"

    return html.Div(
        className="min-h-screen bg-slate-100 flex",
        children=[
            html.Aside(
                className="w-64 bg-slate-900 text-white flex flex-col p-4 gap-2",
                children=[
                    html.Div("Email Dashboard", className="text-lg font-bold mb-4 px-2"),
                    _nav_button("nav-dashboard", "Dashboard"),
                    _nav_button("nav-emails", "Emails"),
                    _nav_button("nav-send", "Envoyer un email"),
                    _nav_button("nav-alerts", "Alertes"),
                    html.Div(className="flex-1"),
                    html.Div(f"Mode: {mode_label}", className="text-xs text-slate-300 px-2 pt-4 border-t border-slate-700"),
                ],
            ),
            html.Main(
                className="flex-1 p-6",
                children=[
                    html.H1("Email Management Dashboard", className="text-2xl font-bold text-slate-800 mb-4"),
                    dcc.Store(id="active-page", data="dashboard"),
                    html.Div(id="tab-content", children=[dashboard_tab(kpis, emails)], className="mt-2"),
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
                className="flex flex-wrap gap-4 mb-6",
                children=[
                    _card("Emails recus (total)", kpis.get("total_received", 0)),
                    _card("Emails envoyes (total)", kpis.get("total_sent", 0)),
                    _card("Commandes", kpis.get("orders", 0)),
                    _card("Reclamations", kpis.get("complaints", 0)),
                ],
            ),
            html.Div(
                className="grid grid-cols-1 lg:grid-cols-3 gap-4",
                children=[
                    html.Div(className="bg-white rounded-lg border border-slate-200 p-2", children=[dcc.Graph(id="fig-per-day", figure=fig_day)]),
                    html.Div(className="bg-white rounded-lg border border-slate-200 p-2", children=[dcc.Graph(id="fig-per-hour", figure=fig_hour)]),
                    html.Div(className="bg-white rounded-lg border border-slate-200 p-2", children=[dcc.Graph(id="fig-by-category", figure=fig_cat)]),
                ],
            ),
            html.H3("5 derniers emails", className="text-lg font-semibold text-slate-800 mt-6 mb-2"),
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
        className="bg-white rounded-lg border border-slate-200 p-4 max-w-3xl",
        children=[
            html.H3("Consulter le contenu d'un email", className="text-lg font-semibold text-slate-800 mb-3"),
            dcc.Dropdown(id="email-select", options=options, placeholder="Choisir un email...", className="mb-3"),
            html.Pre(
                id="email-body-view",
                className="whitespace-pre-wrap bg-slate-50 p-3 rounded border border-slate-200 text-sm text-slate-700 min-h-[120px]",
                children="Selectionnez un email pour afficher son contenu.",
            ),
        ]
    )


def send_tab():
    """Contenu de l'onglet envoi d'email."""
    return html.Div(
        className="bg-white rounded-lg border border-slate-200 p-4 max-w-2xl",
        children=[
            html.H3("Envoyer un email (mode reel requis pour l'envoi)", className="text-lg font-semibold text-slate-800 mb-3"),
            html.Label("Destinataire", className="block text-sm text-slate-600 mb-1"),
            dcc.Input(id="send-to", type="text", placeholder="destinataire@email.com", className="w-full border border-slate-300 rounded px-3 py-2 mb-3"),
            html.Label("Sujet", className="block text-sm text-slate-600 mb-1"),
            dcc.Input(id="send-subject", type="text", placeholder="Sujet", className="w-full border border-slate-300 rounded px-3 py-2 mb-3"),
            html.Label("Message", className="block text-sm text-slate-600 mb-1"),
            dcc.Textarea(id="send-body", placeholder="Contenu du message", className="w-full border border-slate-300 rounded px-3 py-2 mb-3 h-36"),
            html.Button("Envoyer", id="send-btn", n_clicks=0, className="bg-slate-900 text-white px-4 py-2 rounded hover:bg-slate-700"),
            html.Div(id="send-result", className="mt-3 text-slate-700"),
        ]
    )


def alerts_tab():
    """Contenu de l'onglet alertes."""
    return html.Div(
        className="bg-white rounded-lg border border-slate-200 p-4 max-w-2xl",
        children=[
            html.H3("Configurer une alerte", className="text-lg font-semibold text-slate-800 mb-3"),
            html.Label("Categorie", className="block text-sm text-slate-600 mb-1"),
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
                className="mb-3",
            ),
            html.Label("Seuil (nombre d'emails)", className="block text-sm text-slate-600 mb-1"),
            dcc.Input(id="alert-threshold", type="number", value=3, min=1, className="w-full border border-slate-300 rounded px-3 py-2 mb-3"),
            html.Label("Periode", className="block text-sm text-slate-600 mb-1"),
            dcc.RadioItems(
                id="alert-period",
                options=[{"label": "Derniere heure", "value": "heure"}, {"label": "Dernier jour", "value": "jour"}],
                value="jour",
                className="mb-3",
            ),
            html.Button("Verifier l'alerte", id="alert-check-btn", n_clicks=0, className="bg-slate-900 text-white px-4 py-2 rounded hover:bg-slate-700"),
            html.Div(id="alert-result", className="mt-3 p-3 rounded bg-slate-50 border border-slate-200"),
        ]
    )
