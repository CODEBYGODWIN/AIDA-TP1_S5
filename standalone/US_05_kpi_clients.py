import pandas as pd

def kpi_nombre_total_clients(filepath):
    """
    US-05 : Calcule et affiche le KPI du nombre total de clients.
    """
    try:
        # 1. Chargement des données métier
        df = pd.read_csv(filepath)
        
        # 2. Calcul du total de clients (Sous-tâche 1)
        # On supprime les doublons parfaits (ex: la ligne DUP003 est identique à C0074)
        # pour s'assurer que le calcul du KPI est rigoureusement correct.
        df_cleaned = df.drop_duplicates(subset=df.columns.difference(['id_client']))
        
        # On compte le nombre d'identifiants uniques restants
        total_clients = df_cleaned['id_client'].nunique()
        
        # 3. Affichage du KPI (Sous-tâche 2)
        print("="*50)
        print("📈 TABLEAU DE BORD MANAGER - VISION GLOBALE")
        print("="*50)
        print(f"👥 KPI : Nombre total de clients uniques -> {total_clients}")
        print("="*50)
        
        return total_clients

    except FileNotFoundError:
        print("Erreur : Le fichier CSV est introuvable. Veuillez vérifier le chemin.")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")

# Exécution de la fonction avec votre base de données
if __name__ == "__main__":
    kpi_nombre_total_clients('business_data.csv')