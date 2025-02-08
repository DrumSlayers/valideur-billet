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
    onplace_count = manage_onplace_tickets('count')
    
    if request.method == 'POST':
        public_id = request.form.get('public_id')
        
        if public_id == 'specialqrcode:add-onplace-ticket':
            # Handle on-place ticket creation
            onplace_count, timestamp = manage_onplace_tickets('add')
            results = [{
                'Public ID': f'ONPLACE-{onplace_count}',
                'First Name': 'SUR',
                'Last Name': 'PLACE',
                'Status': 'ACTIVE',
                'Ticket Name': 'Billet sur place',
                'Validated': True
            }], f"✅ Billet sur place #{onplace_count} créé à {timestamp}"
        else:
            # Normal ticket validation
            results = validate_ticket(attendees_tickets_data, public_id)
    
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
    onplace_count = manage_onplace_tickets('count')
    
    if request.method == 'POST':
        public_id = request.form.get('public_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        results = search_tickets(attendees_tickets_data, public_id, first_name, last_name)
    
    tickets_count = count_active_tickets(attendees_tickets_data)
    validated_tickets_count = count_validated_tickets()
    
    return render_template('index.html', 
                        results=results, 
                        event_name=os.getenv('event_name'),
                        onplace_count=onplace_count,
                        tickets_count=tickets_count,
                        validated_tickets_count=validated_tickets_count)

if __name__ == '__main__':
    app.run(debug=os.getenv('debug'), host="0.0.0.0")