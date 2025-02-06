import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def load_tickets(attendees_file_path):
    """Charge les données des billets à partir d'un fichier CSV."""
    try:
        data = pd.read_csv(attendees_file_path)
        return data
    except Exception as e:
        print(f"Erreur lors du chargement des données : {e}")
        return None

def load_validated_tickets(validated_tickets_file):
    """Load previously validated tickets"""
    try:
        return pd.read_csv(validated_tickets_file)
    except FileNotFoundError:
        # Create empty DataFrame with required columns
        df = pd.DataFrame(columns=['Public ID', 'First Name', 'Last Name', 'Status', 
                                'Ticket Name', 'Validated At'])
        df.to_csv(validated_tickets_file, index=False)
        return df

def save_validated_ticket(ticket, validated_tickets_file):
    """Save a newly validated ticket"""
    validated_tickets = load_validated_tickets(validated_tickets_file)
    
    # Add validation timestamp
    ticket['Validated At'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    
    # Append new validation
    validated_tickets = pd.concat([validated_tickets, pd.DataFrame([ticket])], ignore_index=True)
    validated_tickets.to_csv(validated_tickets_file, index=False)