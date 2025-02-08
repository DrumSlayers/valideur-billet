from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import pandas as pd
from utils.csv_handler import load_tickets, manage_onplace_tickets, count_active_tickets, count_validated_tickets
from utils.validator import validate_ticket, search_tickets
app = Flask(__name__)

load_dotenv()

# Load ticket data from CSV
attendees_tickets_data = load_tickets(os.getenv('attendees_tickets_file'))

@app.route('/', methods=['GET', 'POST'])
def validate():
    results = None
    if request.method == 'POST':
        public_id = request.form.get('public_id')
        
        if public_id == 'specialqrcode:add-onplace-ticket':
            # Handle on-place ticket creation
            count, timestamp = manage_onplace_tickets('add')
            results = [{
                'Public ID': f'ONPLACE-{count}',
                'First Name': 'SUR',
                'Last Name': 'PLACE',
                'Status': 'ACTIVE',
                'Ticket Name': 'Billet sur place',
                'Validated': True
            }], f"✅ Billet sur place #{count} créé à {timestamp}"
            # Utiliser le nouveau compte retourné par manage_onplace_tickets
            onplace_count = count
        else:
            # Normal ticket validation
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            results = validate_ticket(attendees_tickets_data, public_id, first_name, last_name)
            # Obtenir le compte après la validation
            onplace_count = manage_onplace_tickets('count')
    else:
        # Pour les requêtes GET
        onplace_count = manage_onplace_tickets('count')
    
    # Calculer les compteurs après toute action
    tickets_count = count_active_tickets(attendees_tickets_data)
    validated_tickets_count = count_validated_tickets()
        
    return render_template('index.html', 
                        results=results, 
                        event_name=os.getenv('event_name'),
                        onplace_count=onplace_count,
                        tickets_count=tickets_count,
                        validated_tickets_count=validated_tickets_count)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = None
    if request.method == 'POST':
        public_id = request.form.get('public_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        results = search_tickets(attendees_tickets_data, public_id, first_name, last_name)
    
    # Ajouter les compteurs à la route de recherche
    tickets_count = count_active_tickets(attendees_tickets_data)
    validated_tickets_count = count_validated_tickets()
    
    return render_template('index.html', 
                        results=results, 
                        event_name=os.getenv('event_name'),
                        tickets_count=tickets_count,
                        validated_tickets_count=validated_tickets_count)

if __name__ == '__main__':
    app.run(debug=os.getenv('debug'), host="0.0.0.0")