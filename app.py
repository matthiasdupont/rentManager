from flask import Flask, request, jsonify
from datetime import date, datetime
from calendar import monthrange
import os

app = Flask(__name__)

def calculate_proration(monthly_rent: float, start_date: date, end_date: date, month_year: str):
    """
    Calcule le prorata de loyer pour une période donnée dans un mois spécifique
    """
    try:
        year, month = map(int, month_year.split('-'))
        target_month_start = date(year, month, 1)
        _, last_day = monthrange(year, month)
        target_month_end = date(year, month, last_day)
    except ValueError:
        raise ValueError("Format de mois invalide. Utilisez YYYY-MM")
    
    if start_date > end_date:
        raise ValueError("La date de début doit être antérieure à la date de fin")
    
    # Calcul de la période d'occupation dans le mois cible
    occupation_start = max(start_date, target_month_start)
    occupation_end = min(end_date, target_month_end)
    
    # Si aucune occupation dans ce mois
    if occupation_start > occupation_end:
        return {
            "monthly_rent": monthly_rent,
            "prorated_amount": 0.0,
            "days_in_month": last_day,
            "days_occupied": 0,
            "daily_rate": monthly_rent / last_day,
            "calculation_details": f"Aucune occupation en {month_year}"
        }
    
    # Calcul des jours
    days_in_month = last_day
    days_occupied = (occupation_end - occupation_start).days + 1
    daily_rate = monthly_rent / days_in_month
    prorated_amount = daily_rate * days_occupied
    
    calculation_details = (
        f"Période d'occupation: {occupation_start} à {occupation_end} "
        f"({days_occupied} jours sur {days_in_month})"
    )
    
    return {
        "monthly_rent": monthly_rent,
        "prorated_amount": round(prorated_amount, 2),
        "days_in_month": days_in_month,
        "days_occupied": days_occupied,
        "daily_rate": round(daily_rate, 2),
        "calculation_details": calculation_details
    }

@app.route('/')
def hello_world():
    return jsonify({
        "message": "Hello World - API de calcul de prorata de loyer",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "calculate": "/calculate-proration"
        }
    })

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "environment": os.getenv("ENVIRONMENT", "development")
    })

@app.route('/calculate-proration', methods=['POST'])
def calculate_rent_proration():
    """
    Calcule le prorata de loyer pour une période donnée
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Données JSON requises"}), 400
        
        # Validation des champs requis
        required_fields = ['monthly_rent', 'start_date', 'end_date', 'month_year']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "error": f"Champs manquants: {', '.join(missing_fields)}"
            }), 400
        
        # Conversion des dates
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        result = calculate_proration(
            monthly_rent=float(data['monthly_rent']),
            start_date=start_date,
            end_date=end_date,
            month_year=data['month_year']
        )
        
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Erreur interne du serveur"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)