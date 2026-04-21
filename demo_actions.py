#!/usr/bin/env python3
"""
Script de démonstration - Création automatique d'actions
Crée quelques actions d'exemple pour montrer le fonctionnement
"""

import csv
import os
from datetime import datetime, timedelta

def demo_creer_actions():
    """Crée des actions de démonstration"""
    
    fichier_actions = 'actions.csv'
    colonnes = [
        'id_action', 'id_client', 'type_action', 'description', 
        'priorite', 'statut', 'date_creation', 'date_echeance', 
        'responsable', 'notes'
    ]
    
    # Charger les actions existantes
    actions_existantes = []
    if os.path.exists(fichier_actions):
        with open(fichier_actions, 'r', encoding='utf-8') as f:
            lecteur = csv.DictReader(f)
            actions_existantes = list(lecteur)
    
    # Actions de démonstration
    actions_demo = [
        {
            'id_action': 'ACT001',
            'id_client': 'C0219',
            'type_action': 'Appel téléphonique',
            'description': 'Relance client inactif - risque élevé',
            'priorite': 'Critique',
            'statut': 'Planifiée',
            'date_creation': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'date_echeance': (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y'),
            'responsable': 'Jean Dupont',
            'notes': 'Contact prioritaire - gros chiffre d\'affaires'
        },
        {
            'id_action': 'ACT002',
            'id_client': 'C0071',
            'type_action': 'Offre spéciale',
            'description': 'Proposition d\'offre commerciale pour retenir',
            'priorite': 'Élevé',
            'statut': 'Planifiée',
            'date_creation': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'date_echeance': (datetime.now() + timedelta(days=3)).strftime('%d/%m/%Y'),
            'responsable': 'Marie Martin',
            'notes': 'PME inactif depuis longtemps'
        },
        {
            'id_action': 'ACT003',
            'id_client': 'C0082',
            'type_action': 'Email commercial',
            'description': 'Envoi de newsletter + proposition upsell',
            'priorite': 'Moyen',
            'statut': 'En cours',
            'date_creation': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'date_echeance': (datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y'),
            'responsable': 'Pierre Bernard',
            'notes': 'Suivi régulier'
        },
        {
            'id_action': 'ACT004',
            'id_client': 'C0121',
            'type_action': 'Réunion en personne',
            'description': 'Visite client pour réévaluation des besoins',
            'priorite': 'Élevé',
            'statut': 'Planifiée',
            'date_creation': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'date_echeance': (datetime.now() + timedelta(days=5)).strftime('%d/%m/%Y'),
            'responsable': 'Anne Leclerc',
            'notes': 'Association - risque moyen mais inactif'
        },
    ]
    
    # Fusionner et sauvegarder
    all_actions = actions_existantes + actions_demo
    
    with open(fichier_actions, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=colonnes)
        writer.writeheader()
        writer.writerows(all_actions)
    
    print("✅ Actions de démonstration créées!")
    print(f"   {len(actions_demo)} nouvelle(s) action(s) ajoutée(s)")
    print(f"   Total d'actions: {len(all_actions)}")

if __name__ == "__main__":
    demo_creer_actions()
