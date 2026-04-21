import pandas as pd
import matplotlib.pyplot as plt

def afficher_repartition_segments(filepath):
    """
    US-07 : Calcule et affiche un graphique de la répartition des clients par segment.
    """
    try:
        # 1. Chargement des données
        df = pd.read_csv(filepath)
        
        # 2. Nettoyage et Calcul des segments (Sous-tâche 1)
        # On uniformise la casse et on enlève les espaces superflus 
        # pour éviter que "PME " et "PME" soient comptés séparément.
        df['segment_propre'] = df['segment'].astype(str).str.strip().str.capitalize()
        
        # Calcul du nombre de clients par segment
        repartition = df['segment_propre'].value_counts()
        
        # Affichage du calcul dans la console pour vérifier
        print("="*50)
        print("📊 RÉPARTITION DES CLIENTS PAR SEGMENT (US-07)")
        print("="*50)
        print(repartition)
        print("="*50)
        
        # 3. Intégration du graphique (Sous-tâche 2)
        # Création d'un graphique en barres clair et lisible
        plt.figure(figsize=(10, 6))
        bars = plt.bar(repartition.index, repartition.values, color=['#4C72B0', '#DD8452', '#55A868', '#C44E52'])
        
        # Personnalisation du graphique
        plt.title("Répartition des clients par segment", fontsize=14, fontweight='bold')
        plt.xlabel("Segment", fontsize=12)
        plt.ylabel("Nombre de clients", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Ajout des valeurs exactes au-dessus de chaque barre
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom')
            
        # Affichage
        plt.tight_layout()
        plt.show()
        
    except FileNotFoundError:
        print("Erreur : Le fichier CSV est introuvable.")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    afficher_repartition_segments('business_data.csv')