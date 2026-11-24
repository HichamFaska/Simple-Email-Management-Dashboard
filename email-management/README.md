# Email Management Dashboard (prototype)

Prototype pédagogique d'un tableau de bord de gestion et d'analyse d'emails (Dash + Plotly + Pandas).

## Prérequis

- Python 3.10+ recommandé

## Installation

```bash
cd email-management
pip install -r requirements.txt
```

## Lancement

```bash
python app.py
```

Ouvrir ensuite l'URL affichée dans le terminal (par défaut: `http://127.0.0.1:8050`).

## Mode simulation (par défaut)

Sans configuration, l'application fonctionne en **mode simulation** :

- Emails fictifs chargés depuis `data/sample_emails.py` (>= 30 emails).
- Les graphiques et statistiques utilisent ces données.
- L'envoi d'email est simulé (compteur incrémenté, aucun message réellement envoyé).

## Mode réel (IMAP/SMTP)

1. Copier le fichier d'exemple :

```bash
cp .env.example .env
```

2. Renseigner les variables dans `.env` (exemple Gmail) :

- `EMAIL_MODE=real`
- `IMAP_HOST`, `IMAP_PORT`, `IMAP_USER`, `IMAP_PASSWORD`, `IMAP_MAILBOX`
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM`
- `ALERT_TO` (destinataire des alertes)
- `ALERT_SEND_EMAIL=true` si vous voulez envoyer un email d'alerte

> Ne jamais committer le fichier `.env`.

## Fonctionnalités

- Dashboard : KPI, graphes (par jour, par heure, répartition par catégorie), tableau des 5 derniers emails.
- Emails : sélection d'un email pour afficher le contenu.
- Envoyer un email : formulaire (fonctionne réellement en mode `real`).
- Alertes : choix catégorie/seuil/période, notification dans l'interface (et email optionnel).

## Structure du projet

Voir l'arborescence demandée dans le sujet (dossiers `services`, `analytics`, `alerts`, `data`, `components`).