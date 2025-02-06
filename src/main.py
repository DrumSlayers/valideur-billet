from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import pandas as pd
from utils.csv_handler import load_tickets
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
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        results = validate_ticket(attendees_tickets_data, public_id, first_name, last_name)
        
    return render_template('index.html', results=results, event_name=os.getenv('event_name'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = None
    if request.method == 'POST':
        public_id = request.form.get('public_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        results = search_tickets(attendees_tickets_data, public_id, first_name, last_name)
    
    return render_template('index.html', results=results, event_name=os.getenv('event_name'))

if __name__ == '__main__':
    app.run(debug=os.getenv('debug'))