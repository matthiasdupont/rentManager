# Rent Proration API - Flask Version

Une API Flask simple pour calculer le prorata de loyer quand un locataire arrive ou quitte un logement en cours de mois.

## Structure du projet

```
rent-proration-api/
├── app.py              # Application Flask principale
├── requirements.txt    # Dépendances Python
├── Dockerfile         # Configuration Docker pour GCP
├── app.yaml          # Configuration App Engine
└── README.md         # Documentation
```

## Installation locale

1. Installer les dépendances:
   ```bash
   pip install -r requirements.txt
   ```

2. Lancer l'application:
   ```bash
   python app.py
   ```

L'API sera disponible sur `http://localhost:8080`

## Déploiement sur GCP

### Option 1: Cloud Run

```bash
# Déployer sur Cloud Run
gcloud run deploy rent-proration-api \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated
```

### Option 2: App Engine

```bash
# Déployer sur App Engine
gcloud app deploy
```

## Utilisation de l'API

### Endpoints disponibles:

- `GET /` - Hello World avec informations sur l'API
- `GET /health` - Vérification de santé de l'API
- `POST /calculate-proration` - Calcul du prorata de loyer

### Exemple d'utilisation:

```bash
# Test de l'endpoint Hello World
curl https://your-service-url/

# Test de santé
curl https://your-service-url/health

# Calcul de prorata
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "monthly_rent": 1200,
    "start_date": "2025-06-10",
    "end_date": "2025-06-20",
    "month_year": "2025-06"
  }' \
  https://your-service-url/calculate-proration
```

### Réponse exemple:

```json
{
  "monthly_rent": 1200,
  "prorated_amount": 440.0,
  "days_in_month": 30,
  "days_occupied": 11,
  "daily_rate": 40.0,
  "calculation_details": "Période d'occupation: 2025-06-10 à 2025-06-20 (11 jours sur 30)"
}
```