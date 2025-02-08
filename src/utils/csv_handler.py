import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def load_tickets(attendees_file_path):
    """Load tickets data from CSV file."""
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
        df = pd.DataFrame(columns=[ 'First Name', 'Last Name', 'Email', 'Status', 
                                'Ticket Name', 'Public ID', 'Created Date', 'Validated At'])
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

def manage_onplace_tickets(action='add'):
    """Manage tickets created on-place"""
    onplace_file = os.getenv('onplace_tickets_file')
    
    # Create file if doesn't exist
    if not os.path.exists(onplace_file):
        df = pd.DataFrame(columns=['Created At', 'Public ID'])
        df.to_csv(onplace_file, index=False)
    
    tickets = pd.read_csv(onplace_file)
    current_count = len(tickets)
    
    if action == 'add':
        # Create / add new onplace ticket
        new_ticket = {
            'Created At': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            'Public ID': f'ONPLACE-{current_count + 1}'
        }
        tickets = pd.concat([tickets, pd.DataFrame([new_ticket])], ignore_index=True)
        tickets.to_csv(onplace_file, index=False)
        return current_count + 1, new_ticket['Created At']
    
    return current_count

def count_active_tickets(attendees_df):
    """Count all ACTIVE tickets in attendees dataframe"""
    return len(attendees_df[attendees_df['Status'] == 'ACTIVE'])

def count_validated_tickets():
    """Count all validated tickets"""
    validated_file = os.getenv('validated_tickets_file')
    if not os.path.exists(validated_file):
        return 0
    validated_df = pd.read_csv(validated_file)
    return len(validated_df)