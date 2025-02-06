# Valideur de Billets (Ticket Validator)

Une application web Python conçue pour valider des billets lors d'événements. Elle permet de rechercher des informations sur les billets en utilisant un ID Public ou les Nom/Prénom. L'application lit les données des billets à partir d'un fichier CSV et fournit une interface web intuitive.

## Fonctionnalités

- Recherche de billets par ID Public ou Nom/Prénom
- Affichage des résultats depuis un fichier CSV
- Interface web conviviale
- Validation instantanée des billets
- Gestion des statuts de billets (validé/non validé)
- Export des données de validation

## TODO
- Implémenter bouton valider/dévalider dans les résultats de recherche

## Structure du Projet

```
valideur-billet/
├── src/
│   ├── main.py               # Point d'entrée de l'application
│   ├── templates/            # Templates HTML
│   │   ├── index.html        # Page principale
│   │   └── results.html      # Page des résultats
│   ├── static/              
│   │   └── styles.css        # Styles CSS
│   └── utils/
│       ├── __init__.py
│       ├── csv_handler.py    # Gestion des fichiers CSV
│       └── validator.py      # Logique de validation
├── data/
│   └── tickets.csv          # Données des billets
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
   - Saisir l'ID Public ou les Nom/Prénom
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