"""Classification simple des emails a partir de mots-cles."""

import re

CATEGORIES = ["Commande", "Reclamation", "Devis", "Facture", "Autre"]

KEYWORDS = {
    "Commande": ["commande", "order", "achat", "achete"],
    "Reclamation": ["reclamation", "plainte", "insatisfait", "retard", "remboursement", "probleme"],
    "Devis": ["devis", "quote", "quotation", "tarif", "prix", "estimation", "proposition"],
    "Facture": ["facture", "invoice", "facturation", "paiement", "recu", "billing"],
}


def classify_email(subject, body):
    """Classifier un email selon des mots-cles simples."""
    text = f"{subject or ''} {body or ''}".lower()

    for category, words in KEYWORDS.items():
        for word in words:
            if re.search(rf"\b{re.escape(word)}\b", text):
                return category
    return "Autre"
