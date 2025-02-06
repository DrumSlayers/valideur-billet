import pandas as pd
from .csv_handler import load_validated_tickets, save_validated_ticket
import os
from dotenv import load_dotenv
load_dotenv()

def validate_ticket(tickets_df, public_id=None, first_name=None, last_name=None):
    """
    Search and validate tickets based on provided criteria
    """
    validated_tickets = load_validated_tickets(os.getenv('validated_tickets_file'))
    
    # Find matching ticket
    if public_id:
        results = tickets_df[tickets_df['Public ID'].str.lower() == public_id.lower()]
    elif first_name and last_name:
        results = tickets_df[(tickets_df['First Name'].str.lower() == first_name.lower()) & 
                        (tickets_df['Last Name'].str.lower() == last_name.lower())]
    elif first_name:
        results = tickets_df[tickets_df['First Name'].str.lower() == first_name.lower()]
    elif last_name:
        results = tickets_df[tickets_df['Last Name'].str.lower() == last_name.lower()]
    else:
        return [], None

    if results.empty:
        return [], None
    
    # Convert results to list of dictionaries
    results_list = results.to_dict('records')
    
    # Check if ticket was already validated and is Active/Valid
    for ticket in results_list:
        already_validated = validated_tickets[
            validated_tickets['Public ID'] == ticket['Public ID']
        ]

        if ticket['Status'] != "ACTIVE":
            return results_list, f"🛑 Billet annulé (Motif: {ticket['Status']} )"
        
        if not already_validated.empty:
            ticket['Validated'] = True
            return results_list, f"⚠️ Billet déjà validé le {already_validated.iloc[0]['Validated At']}"

    
    # If not already validated, save first result
    ticket_data = results_list[0].copy()
    save_validated_ticket(ticket_data, os.getenv('validated_tickets_file'))
    
    # Mark ticket as validated
    for ticket in results_list:
        ticket['Validated'] = True
    
    return results_list, "✅ Billet validé avec succès!"

def search_tickets(df, public_id=None, first_name=None, last_name=None):
    # If nothing given, return all tickets
    if not any([public_id, first_name, last_name]):
        results = df.to_dict('records')
    else:
        # Filter mask creation
        mask = pd.Series(True, index=df.index)
        if public_id:
            mask &= df['Public ID'].str.contains(public_id, case=False, na=False)
        if first_name:
            mask &= df['First Name'].str.contains(first_name, case=False, na=False)
        if last_name:
            mask &= df['Last Name'].str.contains(last_name, case=False, na=False)
        
        results = df[mask].to_dict('records')
    
    # Load validated tickets to check status
    validated_tickets = load_validated_tickets(os.getenv('validated_tickets_file'))
    
    for ticket in results:
        is_validated = not validated_tickets[
            validated_tickets['Public ID'] == ticket['Public ID']
        ].empty
        ticket['Validated'] = is_validated
    
    return results, "🔎 Résultat(s) de la recherche"