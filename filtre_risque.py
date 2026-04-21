import csv
import sys
from collections import defaultdict

def charger_donnees(chemin_csv):
    """Charge le fichier CSV des clients"""
    try:
        donnees = []
        with open(chemin_csv, 'r', encoding='utf-8') as f:
            lecteur = csv.DictReader(f)
            donnees = list(lecteur)
        print(f"✓ Fichier chargé: {len(donnees)} clients")
        return donnees
    except FileNotFoundError:
        print(f"✗ Erreur: Fichier '{chemin_csv}' non trouvé")
        sys.exit(1)

def normaliser_risque(risque):
    """Normalise les valeurs de risque"""
    if not risque:
        return None
    return risque.strip().lower()

def obtenir_entetes(donnees):
    """Récupère l'en-tête du CSV"""
    if donnees:
        return list(donnees[0].keys())
    return []

def obtenir_statistiques_risque(donnees):
    """Calcule les statistiques de distribution des risques"""
    stats = defaultdict(int)
    for client in donnees:
        risque = normaliser_risque(client.get('risque_churn', ''))
        if risque:
            stats[risque] += 1
    return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))

def filtrer_clients_prioritaires(donnees):
    """Filtre les clients prioritaires (risque élevé/moyen + statut inactif/à relancer)"""
    prioritaires = []
    for client in donnees:
        risque = normaliser_risque(client.get('risque_churn', ''))
        statut = normaliser_risque(client.get('statut_client', ''))
        
        # Critères: risque élevé/moyen ET (inactif OU à relancer)
        if risque in ['élevé', 'moyen'] and statut in ['inactif', 'à relancer']:
            prioritaires.append(client)
    
    return prioritaires

def filtrer_par_risque(donnees, niveau_risque='élevé'):
    """Filtre les clients par niveau de risque spécifique"""
    niveau_norm = normaliser_risque(niveau_risque)
    return [c for c in donnees if normaliser_risque(c.get('risque_churn', '')) == niveau_norm]

def sauvegarder_csv(donnees, chemin_fichier, entetes):
    """Sauvegarde les données dans un CSV"""
    if not donnees:
        return 0
    
    with open(chemin_fichier, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=entetes)
        writer.writeheader()
        writer.writerows(donnees)
    
    return len(donnees)

def convertir_en_float(val):
    """Convertit une valeur en float, retourne 0 si impossible"""
    try:
        return float(val) if val and val.strip() else 0
    except (ValueError, AttributeError):
        return 0

def main():
    print("🚀 Démarrage du filtre de risque...\n")
    
    # Charger les données
    donnees = charger_donnees('business_data.csv')
    entetes = obtenir_entetes(donnees)
    
    # Statistiques des risques
    print("📊 Distribution des niveaux de risque:")
    stats = obtenir_statistiques_risque(donnees)
    for risque, count in stats.items():
        pourcentage = (count / len(donnees)) * 100
        print(f"  • {risque.upper()}: {count} clients ({pourcentage:.1f}%)")
    
    # Filtrer les clients prioritaires
    print("\n🔴 CLIENTS PRIORITAIRES (risque élevé/moyen + Inactif/À relancer):")
    clients_prioritaires = filtrer_clients_prioritaires(donnees)
    print(f"⚠️  {len(clients_prioritaires)} client(s) nécessite(nt) une action immédiate!\n")
    
    # Afficher les clients prioritaires
    if clients_prioritaires:
        print("📋 Détail des clients prioritaires:")
        print("-" * 100)
        for i, client in enumerate(clients_prioritaires[:10], 1):
            ca = convertir_en_float(client.get('chiffre_affaires', 0))
            satisfaction = client.get('satisfaction', 'N/A')
            print(f"{i:2d}. {client.get('id_client', '?'):8s} | {client.get('segment', '?'):15s} | "
                  f"Risque: {client.get('risque_churn', '?'):8s} | Statut: {client.get('statut_client', '?'):12s} | "
                  f"CA: {ca:8.2f}€ | Sat: {satisfaction}/10")
        
        if len(clients_prioritaires) > 10:
            print(f"... et {len(clients_prioritaires) - 10} autres")
        print("-" * 100)
    
    # Statistiques clients prioritaires
    print("\n📈 Statistiques des clients prioritaires:")
    if clients_prioritaires:
        ca_total = sum(convertir_en_float(c.get('chiffre_affaires', 0)) for c in clients_prioritaires)
        ca_moyen = ca_total / len(clients_prioritaires) if clients_prioritaires else 0
        satisfaction_moyen = sum(convertir_en_float(c.get('satisfaction', 0)) for c in clients_prioritaires) / len(clients_prioritaires) if clients_prioritaires else 0
        
        print(f"  • Nombre total: {len(clients_prioritaires)}")
        print(f"  • CA total: {ca_total:.2f}€")
        print(f"  • CA moyen: {ca_moyen:.2f}€")
        print(f"  • Satisfaction moyenne: {satisfaction_moyen:.2f}/10")
    
    # Sauvegarder les résultats
    print("\n💾 Sauvegarde des résultats...")
    nb_saved = sauvegarder_csv(clients_prioritaires, 'clients_prioritaires.csv', entetes)
    print(f"✅ {nb_saved} client(s) exporté(s) vers clients_prioritaires.csv")
    
    # Afficher aussi les clients à risque élevé
    print("\n📊 CLIENTS AVEC RISQUE ÉLEVÉ (toutes statuts):")
    clients_eleves = filtrer_par_risque(donnees, 'élevé')
    print(f"Nombre: {len(clients_eleves)}")
    for i, client in enumerate(clients_eleves[:5], 1):
        ca = convertir_en_float(client.get('chiffre_affaires', 0))
        satisfaction = client.get('satisfaction', 'N/A')
        print(f"{i}. {client.get('id_client', '?'):8s} | {client.get('segment', '?'):15s} | "
              f"CA: {ca:8.2f}€ | Sat: {satisfaction}/10")
    if len(clients_eleves) > 5:
        print(f"... et {len(clients_eleves) - 5} autres")
    
    print("\n✅ Analyse complétée avec succès!")

if __name__ == "__main__":
    main()
