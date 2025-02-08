# Valideur de Billets (Ticket Validator)

Une application web Python conçue pour valider des billets lors d'événements. 
Elle permet également de rechercher des informations sur les billets en utilisant un ID Public ou les Nom/Prénom. 
L'application lit et écrit les données des billets à partir de fichiers CSV et fournit une interface web intuitive.

## Fonctionnalités

- Validation des billets par recherche via ID Public (destiné aux QR Code)
- Recherche de billets par Nom/Prénom, avec possibilité de validation manuelle du billet
- Affichage et écriture des résultats depuis des fichiers CSV
- Interface web conviviale
- Validation instantanée des billets
- Multi-client
- Gestion des statuts de billets (valide/non valide)
- Gestion de l'ajout de tickets vendus sur place, en dernière minute
- Affichage des statistiques de ventes et de validation
- Export des données de validation

## Structure du Projet

```
valideur-billet/
├── src/
│   ├── main.py               # Point d'entrée de l'application
│   ├── templates/            # Templates HTML
│   │   ├── index.html        # Page principale
│   ├── static/              
│   │   └── styles.css        # Styles CSS
│   └── utils/
│       ├── __init__.py
│       ├── csv_handler.py    # Gestion des fichiers CSV
│       └── validator.py      # Logique de validation
├── data/
│   ├── attendees.csv          # Données des billets extrait de l'outil de ticketing
│   ├── onplace_tickets.py    # Données des billets vendus sur place
│   └── onplace_tickets.py    # Données des billets validés avec horodatage
├── .env # Variables d'environnements, pour régler l'application rapidement
└── requirements.txt
```

## Installation

1. Créer l'environnement virtuel :
   ```bash
   python3 -m venv .venv
   ```

2. Activer l'environnement :
   ```bash
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

1. Démarrer l'application :
   ```bash
   python src/main.py
   ```

2. Accéder à l'interface web : `http://localhost:5000`

3. Pour valider un billet :
   - Scanner un QR Code ou entrer l'ID Public dans le champ Scanner un billet
   - Entrée ou bouton "Valider"
4. Pour rechercher un billet :
   - Taper le nom ou prénom
   - Cliquer sur "Rechercher"
   - Vérifier les informations affichées
   - Cliquer sur "Valider" pour marquer le billet comme utilisé

## Configuration

Le fichier CSV des billets doit contenir les colonnes suivantes :
- public_id
- first_name
- last_name
- ticket_type
- validated
- validation_date

## Développement

Pour exécuter les tests :
```bash
python -m pytest src/tests/
```

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.