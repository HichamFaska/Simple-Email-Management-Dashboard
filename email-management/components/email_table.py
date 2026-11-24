"""Tableau des emails pour Dash."""

from dash import dash_table

from analytics.statistics import latest_emails


def build_email_table(emails, limit=5):
    """Construire un DataTable des derniers emails."""
    df = latest_emails(emails, limit=limit)
    if df.empty:
        return dash_table.DataTable(columns=[], data=[], page_size=5)

    display_df = df[["date", "from", "subject", "category"]].copy()
    if not display_df.empty:
        display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d %H:%M").fillna("")
    columns = [{"name": c.capitalize(), "id": c} for c in display_df.columns]
    return dash_table.DataTable(
        id="emails-table",
        columns=columns,
        data=display_df.to_dict("records"),
        page_size=5,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "padding": "8px", "fontFamily": "Arial"},
        style_header={"fontWeight": "bold", "backgroundColor": "#f2f4f7"},
    )
