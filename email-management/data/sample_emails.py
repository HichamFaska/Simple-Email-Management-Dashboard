"""Donnees fictives pour le mode simulation."""

from datetime import datetime, timedelta


def build_sample_emails():
    """Generer au moins 30 emails fictifs avec des dates et categories variees."""
    now = datetime.now()
    base = now.replace(minute=0, second=0, microsecond=0)

    raw = [
        # Commandes
        ("client1@shop.com", "orders@company.com", "Nouvelle commande #1001", "Bonjour, je souhaite confirmer ma commande de 3 articles.", base - timedelta(days=0, hours=2)),
        ("client2@shop.com", "orders@company.com", "Commande #1002 passee", "Veuillez trouver ma commande pour le lot A.", base - timedelta(days=1, hours=3)),
        ("client3@shop.com", "orders@company.com", "Achat en ligne - suivi", "Merci de traiter ma commande rapidement.", base - timedelta(days=2, hours=1)),
        ("client4@shop.com", "orders@company.com", "Confirmation commande urgente", "Je confirme la commande ref 5521.", base - timedelta(days=3, hours=6)),
        ("client5@shop.com", "orders@company.com", "Nouvelle demande d'achat", "Pouvez-vous enregistrer ma commande du jour?", base - timedelta(days=4, hours=4)),
        ("client6@shop.com", "orders@company.com", "Commande annulee puis reprise", "Je reprends la commande precedente.", base - timedelta(days=5, hours=2)),
        # Reclamations
        ("client7@mail.com", "support@company.com", "Reclamation sur livraison", "Le colis est arrive en retard et abime.", base - timedelta(days=0, hours=5)),
        ("client8@mail.com", "support@company.com", "Plainte produit defaillant", "Le produit ne fonctionne pas, je souhaite un remboursement.", base - timedelta(days=1, hours=7)),
        ("client9@mail.com", "support@company.com", "Service insatisfaisant", "Je suis tres mecontent du service recu.", base - timedelta(days=2, hours=8)),
        ("client10@mail.com", "support@company.com", "Reclamation facture incorrecte", "Le montant facture ne correspond pas a mon devis.", base - timedelta(days=3, hours=9)),
        ("client11@mail.com", "support@company.com", "Retard non justifie", "Probleme de livraison, merci de repondre rapidement.", base - timedelta(days=4, hours=10)),
        # Devis
        ("prospect1@mail.com", "sales@company.com", "Demande de devis", "Bonjour, pouvez-vous m'envoyer un devis pour 20 licences?", base - timedelta(days=0, hours=1)),
        ("prospect2@mail.com", "sales@company.com", "Quotation request", "Je souhaite un devis detaille pour votre service.", base - timedelta(days=1, hours=2)),
        ("prospect3@mail.com", "sales@company.com", "Prix et proposition", "Pouvez-vous nous proposer un prix pour ce projet?", base - timedelta(days=2, hours=3)),
        ("prospect4@mail.com", "sales@company.com", "Demande tarif", "Quel est le tarif pour une prestation mensuelle?", base - timedelta(days=3, hours=4)),
        ("prospect5@mail.com", "sales@company.com", "Estimation budget", "Merci de fournir une estimation pour nos besoins.", base - timedelta(days=5, hours=5)),
        # Factures
        ("client12@billing.com", "billing@company.com", "Question sur facture", "Je n'ai pas recu ma facture du mois dernier.", base - timedelta(days=0, hours=6)),
        ("client13@billing.com", "billing@company.com", "Facture impayee", "Merci de preciser la date de paiement de la facture.", base - timedelta(days=1, hours=8)),
        ("client14@billing.com", "billing@company.com", "Recu de paiement", "Veuillez m'envoyer le recu pour ma derniere facture.", base - timedelta(days=2, hours=9)),
        ("client15@billing.com", "billing@company.com", "Facturation mensuelle", "Pouvez-vous corriger le montant de ma facture?", base - timedelta(days=4, hours=11)),
        # Autres
        ("info@partner.com", "contact@company.com", "Prise de contact", "Bonjour, nous aimerions discuter d'un partenariat.", base - timedelta(days=0, hours=4)),
        ("rh@company.com", "contact@company.com", "Candidature spontanee", "Veuillez trouver ci-joint mon CV pour un poste.", base - timedelta(days=1, hours=12)),
        ("it@company.com", "contact@company.com", "Mise a jour systeme", "La maintenance est prevue ce week-end.", base - timedelta(days=2, hours=13)),
        ("news@media.com", "contact@company.com", "Invitation evenement", "Nous vous invitons a notre conference.", base - timedelta(days=3, hours=14)),
        ("client16@mail.com", "contact@company.com", "Question generale", "Avez-vous des horaires d'ouverture elargis?", base - timedelta(days=4, hours=15)),
        ("client17@mail.com", "contact@company.com", "Demande d'information", "Merci de me renseigner sur vos services.", base - timedelta(days=5, hours=16)),
        ("client18@mail.com", "contact@company.com", "Relance interne", "Peut-on planifier un point demain matin?", base - timedelta(days=6, hours=8)),
        ("client19@mail.com", "contact@company.com", "Accuse de reception", "Bien recu, merci pour votre retour.", base - timedelta(days=6, hours=18)),
        ("client20@mail.com", "contact@company.com", "Note de service", "Merci de prendre connaissance de la note.", base - timedelta(days=7, hours=9)),
        ("client21@mail.com", "contact@company.com", "Feedback utilisateur", "Votre application est utile, quelques suggestions.", base - timedelta(days=7, hours=20)),
        ("client22@mail.com", "contact@company.com", "Demande support", "J'ai besoin d'aide pour acceder a mon compte.", base - timedelta(days=8, hours=10)),
    ]

    emails = []
    for idx, (sender, recipient, subject, body, created_at) in enumerate(raw, start=1):
        emails.append(
            {
                "id": idx,
                "from": sender,
                "to": recipient,
                "subject": subject,
                "body": body,
                "date": created_at,
            }
        )
    return emails
