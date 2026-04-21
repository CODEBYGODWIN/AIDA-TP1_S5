import pandas as pd
import numpy as np

def generate_recommendation(row):
    """
    Applique les règles métier pour générer une recommandation personnalisée.
    """
    # Nettoyage rapide du risque pour uniformiser (gestion de 'Élevé', 'eleve', 'HIGH')
    risque = str(row['risque_churn']).strip().lower()
    satisfaction = row['satisfaction']
    jours_inactif = row['dernier_achat_jours']
    
    # Règle 1 : Insatisfaction critique
    if pd.notna(satisfaction) and satisfaction < 5.0:
        return "Appel immédiat par un manager : Comprendre l'insatisfaction profonde."
    
    # Règle 2 : Risque de churn très élevé
    elif risque in ['élevé', 'eleve', 'high']:
        return "Proposer une offre de rétention agressive (réduction de 20% ou service gratuit)."
        
    # Règle 3 : Client inactif depuis très longtemps (> 1 an)
    elif pd.notna(jours_inactif) and jours_inactif > 365:
        return "Campagne email de réengagement avec un point sur les nouveautés."
        
    # Règle 4 : Cas par défaut pour les autres clients considérés "à risque"
    else:
        return "Planifier un appel de courtoisie (Customer Success) d'ici 2 semaines."

def afficher_recommandations_clients_risque(filepath):
    """
    US-11 : Génère et affiche les recommandations pour les clients à risque.
    """
    try:
        df = pd.read_csv(filepath)
        
        # 1. Identification des clients à risque
        # Pour cet exemple, on filtre les clients inactifs, à relancer, 
        # ou ayant un risque de churn perçu comme élevé.
        mots_cles_risque = ['élevé', 'eleve', 'high']
        df['risque_nettoye'] = df['risque_churn'].astype(str).str.lower().str.strip()
        
        clients_a_risque = df[
            (df['statut_client'].isin(['Inactif', 'À relancer'])) | 
            (df['risque_nettoye'].isin(mots_cles_risque)) |
            (df['satisfaction'] < 6.0)
        ].copy()
        
        # 2. Application de la logique métier (Sous-tâche 2)
        clients_a_risque['recommandation'] = clients_a_risque.apply(generate_recommendation, axis=1)
        
        # 3. Affichage dans l'interface/console (Sous-tâche 3)
        print("="*80)
        print("🚨 TABLEAU DE BORD : RECOMMANDATIONS POUR CLIENTS À RISQUE (US-11)")
        print("="*80)
        
        # On affiche un sous-ensemble pertinent de colonnes pour la démonstration
        affichage = clients_a_risque[['id_client', 'segment', 'risque_churn', 'satisfaction', 'recommandation']]
        
        # Affichage des 10 premiers cas pour que ce soit lisible
        print(affichage.head(10).to_string(index=False))
        print("="*80)
        print(f"Total de clients nécessitant une action : {len(clients_a_risque)}")
        
        return clients_a_risque

    except Exception as e:
        print(f"Erreur lors du traitement : {e}")

if __name__ == "__main__":
    afficher_recommandations_clients_risque('business_data.csv')