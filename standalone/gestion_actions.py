import csv
import sys
from datetime import datetime
import os

class GestionnaireActions:
    """Gère les actions de suivi commerciale"""
    
    def __init__(self):
        self.fichier_actions = 'actions.csv'
        self.fichier_clients_prioritaires = 'clients_prioritaires.csv'
        self.colonnes_actions = [
            'id_action', 'id_client', 'type_action', 'description', 
            'priorite', 'statut', 'date_creation', 'date_echeance', 
            'responsable', 'notes'
        ]
        self.initialiser_fichier()
    
    def initialiser_fichier(self):
        """Crée le fichier actions.csv s'il n'existe pas"""
        if not os.path.exists(self.fichier_actions):
            with open(self.fichier_actions, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.colonnes_actions)
                writer.writeheader()
            print(f"✓ Fichier {self.fichier_actions} créé")
    
    def charger_clients_prioritaires(self):
        """Charge les clients prioritaires disponibles"""
        clients = []
        try:
            with open(self.fichier_clients_prioritaires, 'r', encoding='utf-8') as f:
                lecteur = csv.DictReader(f)
                clients = list(lecteur)
        except FileNotFoundError:
            print(f"✗ Fichier {self.fichier_clients_prioritaires} non trouvé")
        return clients
    
    def charger_actions(self):
        """Charge toutes les actions existantes"""
        actions = []
        try:
            with open(self.fichier_actions, 'r', encoding='utf-8') as f:
                lecteur = csv.DictReader(f)
                actions = list(lecteur)
        except FileNotFoundError:
            pass
        return actions
    
    def generer_id_action(self):
        """Génère un ID unique pour une action"""
        actions = self.charger_actions()
        if not actions:
            return 'ACT001'
        
        derniers_ids = [a['id_action'] for a in actions if a['id_action']]
        if not derniers_ids:
            return 'ACT001'
        
        numero = max([int(id[3:]) for id in derniers_ids])
        return f'ACT{numero + 1:03d}'
    
    def creer_action_interactive(self):
        """Crée une action via un formulaire interactif"""
        print("\n" + "="*80)
        print("📝 FORMULAIRE DE CRÉATION D'ACTION")
        print("="*80)
        
        # Afficher les clients disponibles
        clients = self.charger_clients_prioritaires()
        if not clients:
            print("✗ Aucun client prioritaire disponible")
            return False
        
        print("\n🔍 Clients prioritaires disponibles:")
        for i, client in enumerate(clients[:10], 1):
            print(f"  {i}. {client.get('id_client', '?'):8s} | {client.get('segment', '?'):15s} | "
                  f"CA: {client.get('chiffre_affaires', '0'):10s}€ | Risque: {client.get('risque_churn', '?')}")
        
        if len(clients) > 10:
            print(f"  ... et {len(clients) - 10} autres")
        
        # Demander l'ID client
        print("\n📌 Sélection du client:")
        while True:
            id_client = input("  → ID du client (ex: C0082): ").strip().upper()
            if any(c['id_client'] == id_client for c in clients):
                break
            print("  ✗ ID invalide, veuillez réessayer")
        
        # Type d'action
        print("\n📋 Type d'action disponible:")
        types_actions = [
            "Appel téléphonique",
            "Email commercial",
            "Réunion en personne",
            "Offre spéciale",
            "Suivi relance",
            "Réévaluation satisfaction",
            "Autre"
        ]
        for i, type_action in enumerate(types_actions, 1):
            print(f"  {i}. {type_action}")
        
        while True:
            try:
                choix = int(input("  → Choisir le numéro: "))
                if 1 <= choix <= len(types_actions):
                    type_action = types_actions[choix - 1]
                    if choix == 7:
                        type_action = input("  → Préciser le type: ").strip()
                    break
                print("  ✗ Choix invalide")
            except ValueError:
                print("  ✗ Veuillez entrer un nombre")
        
        # Description
        print("\n📝 Description:")
        description = input("  → Brève description de l'action: ").strip()
        
        # Priorité
        print("\n⚡ Priorité:")
        priorites = ["Faible", "Moyen", "Élevé", "Critique"]
        for i, p in enumerate(priorites, 1):
            print(f"  {i}. {p}")
        
        while True:
            try:
                choix = int(input("  → Choisir le niveau (1-4): "))
                if 1 <= choix <= 4:
                    priorite = priorites[choix - 1]
                    break
                print("  ✗ Choix invalide")
            except ValueError:
                print("  ✗ Veuillez entrer un nombre")
        
        # Date d'échéance
        print("\n📅 Date d'échéance:")
        while True:
            date_echeance = input("  → Format JJ/MM/YYYY (ex: 25/04/2026): ").strip()
            try:
                datetime.strptime(date_echeance, '%d/%m/%Y')
                break
            except ValueError:
                print("  ✗ Format invalide")
        
        # Responsable
        print("\n👤 Responsable:")
        responsable = input("  → Nom du commercial: ").strip()
        
        # Notes additionnelles
        print("\n📌 Notes additionnelles (optionnel):")
        notes = input("  → Notes: ").strip()
        
        # Créer l'action
        id_action = self.generer_id_action()
        date_creation = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        action = {
            'id_action': id_action,
            'id_client': id_client,
            'type_action': type_action,
            'description': description,
            'priorite': priorite,
            'statut': 'Planifiée',
            'date_creation': date_creation,
            'date_echeance': date_echeance,
            'responsable': responsable,
            'notes': notes
        }
        
        # Sauvegarder
        self.sauvegarder_action(action)
        
        print("\n" + "="*80)
        print(f"✅ Action {id_action} créée avec succès!")
        print("="*80)
        
        return True
    
    def sauvegarder_action(self, action):
        """Sauvegarde une action dans le CSV"""
        actions = self.charger_actions()
        actions.append(action)
        
        with open(self.fichier_actions, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.colonnes_actions)
            writer.writeheader()
            writer.writerows(actions)
    
    def afficher_actions(self, filtre_statut=None, filtre_priorite=None):
        """Affiche les actions avec filtres optionnels"""
        actions = self.charger_actions()
        
        if filtre_statut:
            actions = [a for a in actions if a.get('statut', '').lower() == filtre_statut.lower()]
        
        if filtre_priorite:
            actions = [a for a in actions if a.get('priorite', '').lower() == filtre_priorite.lower()]
        
        if not actions:
            print("ℹ️  Aucune action trouvée")
            return
        
        print("\n" + "="*120)
        print("📊 LISTE DES ACTIONS")
        print("="*120)
        print(f"{'ID':8} | {'Client':8} | {'Type':20} | {'Priorité':10} | {'Statut':12} | {'Responsable':15} | {'Échéance'}")
        print("-"*120)
        
        for action in actions:
            print(f"{action.get('id_action', '?'):8} | {action.get('id_client', '?'):8} | "
                  f"{action.get('type_action', '?'):20} | {action.get('priorite', '?'):10} | "
                  f"{action.get('statut', '?'):12} | {action.get('responsable', '?'):15} | "
                  f"{action.get('date_echeance', '?')}")
        
        print("="*120)
        print(f"Total: {len(actions)} action(s)")
    
    def afficher_action_details(self, id_action):
        """Affiche les détails d'une action"""
        actions = self.charger_actions()
        action = next((a for a in actions if a['id_action'] == id_action), None)
        
        if not action:
            print(f"✗ Action {id_action} non trouvée")
            return
        
        print("\n" + "="*80)
        print(f"📋 DÉTAILS ACTION {id_action}")
        print("="*80)
        print(f"Client               : {action.get('id_client', '?')}")
        print(f"Type d'action        : {action.get('type_action', '?')}")
        print(f"Description          : {action.get('description', '?')}")
        print(f"Priorité             : {action.get('priorite', '?')}")
        print(f"Statut               : {action.get('statut', '?')}")
        print(f"Date création        : {action.get('date_creation', '?')}")
        print(f"Date d'échéance      : {action.get('date_echeance', '?')}")
        print(f"Responsable          : {action.get('responsable', '?')}")
        print(f"Notes                : {action.get('notes', 'N/A')}")
        print("="*80)
    
    def mettre_a_jour_statut(self, id_action, nouveau_statut):
        """Met à jour le statut d'une action"""
        actions = self.charger_actions()
        trouve = False
        
        for action in actions:
            if action['id_action'] == id_action:
                action['statut'] = nouveau_statut
                trouve = True
                break
        
        if not trouve:
            print(f"✗ Action {id_action} non trouvée")
            return False
        
        with open(self.fichier_actions, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.colonnes_actions)
            writer.writeheader()
            writer.writerows(actions)
        
        print(f"✅ Statut de {id_action} mis à jour: {nouveau_statut}")
        return True
    
    def afficher_actions_par_client(self, id_client):
        """Affiche toutes les actions d'un client"""
        actions = self.charger_actions()
        actions_client = [a for a in actions if a.get('id_client') == id_client]
        
        if not actions_client:
            print(f"\nℹ️  Aucune action pour le client {id_client}")
            return
        
        print(f"\n" + "="*100)
        print(f"📋 ACTIONS POUR LE CLIENT {id_client}")
        print("="*100)
        
        for action in actions_client:
            print(f"\n  • {action.get('type_action', '?')} ({action.get('priorite', '?')})")
            print(f"    Statut: {action.get('statut', '?')} | Échéance: {action.get('date_echeance', '?')}")
            print(f"    Description: {action.get('description', '?')}")
            print(f"    Responsable: {action.get('responsable', '?')}")
    
    def generer_rapport_actions(self):
        """Génère un rapport récapitulatif des actions"""
        actions = self.charger_actions()
        
        if not actions:
            print("ℹ️  Aucune action enregistrée")
            return
        
        # Statistiques
        stats_statut = {}
        stats_priorite = {}
        stats_type = {}
        
        for action in actions:
            statut = action.get('statut', 'Non défini')
            stats_statut[statut] = stats_statut.get(statut, 0) + 1
            
            priorite = action.get('priorite', 'Non défini')
            stats_priorite[priorite] = stats_priorite.get(priorite, 0) + 1
            
            type_action = action.get('type_action', 'Non défini')
            stats_type[type_action] = stats_type.get(type_action, 0) + 1
        
        print("\n" + "="*80)
        print("📊 RAPPORT DES ACTIONS")
        print("="*80)
        
        print(f"\nTotal d'actions: {len(actions)}")
        
        print("\n📈 Par Statut:")
        for statut, count in sorted(stats_statut.items()):
            pourcentage = (count / len(actions)) * 100
            print(f"  • {statut:20s}: {count:3d} ({pourcentage:5.1f}%)")
        
        print("\n⚡ Par Priorité:")
        for priorite, count in sorted(stats_priorite.items()):
            pourcentage = (count / len(actions)) * 100
            print(f"  • {priorite:20s}: {count:3d} ({pourcentage:5.1f}%)")
        
        print("\n📋 Par Type d'action:")
        for type_action, count in sorted(stats_type.items(), key=lambda x: x[1], reverse=True):
            pourcentage = (count / len(actions)) * 100
            print(f"  • {type_action:30s}: {count:3d} ({pourcentage:5.1f}%)")
        
        # Actions urgentes (critiques + planifiées)
        actions_urgentes = [a for a in actions if a.get('priorite') == 'Critique' and a.get('statut') != 'Complétée']
        if actions_urgentes:
            print(f"\n🚨 Actions CRITIQUES à traiter: {len(actions_urgentes)}")
            for action in actions_urgentes[:5]:
                print(f"  • {action['id_action']}: {action['id_client']} - {action['type_action']}")
        
        print("\n" + "="*80)

def menu_principal():
    """Menu principal de gestion des actions"""
    gestionnaire = GestionnaireActions()
    
    while True:
        print("\n" + "="*80)
        print("🎯 GESTION DES ACTIONS DE SUIVI CLIENT")
        print("="*80)
        print("\n1. ➕ Créer une nouvelle action")
        print("2. 📋 Afficher toutes les actions")
        print("3. 🔍 Voir les détails d'une action")
        print("4. 🔄 Mettre à jour le statut d'une action")
        print("5. 👤 Afficher les actions d'un client")
        print("6. 📊 Voir le rapport des actions")
        print("7. 🚪 Quitter")
        
        choix = input("\nChoisir une option (1-7): ").strip()
        
        if choix == '1':
            gestionnaire.creer_action_interactive()
        
        elif choix == '2':
            filtre_statut = input("Filtrer par statut (optionnel, Entrée pour tous): ").strip() or None
            filtre_priorite = input("Filtrer par priorité (optionnel, Entrée pour tous): ").strip() or None
            gestionnaire.afficher_actions(filtre_statut, filtre_priorite)
        
        elif choix == '3':
            id_action = input("ID de l'action à consulter: ").strip().upper()
            gestionnaire.afficher_action_details(id_action)
        
        elif choix == '4':
            id_action = input("ID de l'action: ").strip().upper()
            print("\nStatuts disponibles: Planifiée, En cours, Complétée, Annulée")
            nouveau_statut = input("Nouveau statut: ").strip()
            gestionnaire.mettre_a_jour_statut(id_action, nouveau_statut)
        
        elif choix == '5':
            id_client = input("ID du client: ").strip().upper()
            gestionnaire.afficher_actions_par_client(id_client)
        
        elif choix == '6':
            gestionnaire.generer_rapport_actions()
        
        elif choix == '7':
            print("\n👋 Au revoir!")
            break
        
        else:
            print("\n✗ Option invalide")

if __name__ == "__main__":
    menu_principal()
