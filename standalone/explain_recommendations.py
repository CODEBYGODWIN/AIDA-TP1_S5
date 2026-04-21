import csv
import os

def get_explanation(row):
    try:
        # Nettoyage des clés au cas où il y aurait des espaces ou des caractères invisibles
        row = {k.strip(): v for k, v in row.items()}
        statut = row['statut_client'].strip().lower()
        jours = int(row['dernier_achat_jours'])
        
        if statut == 'actif' and jours < 180:
            return "Fidéliser", "Client actif avec un achat récent (moins de 180 jours)."
        elif statut in ['inactif', 'à relancer'] or jours > 360:
            return "Relancer", "Client inactif ou n'ayant pas commandé depuis plus d'un an."
        else:
            return "Surveiller", "Client avec un risque de départ ou un comportement à surveiller."
    except (ValueError, KeyError):
        return None, None

def display_explanations(file_path, limit=10):
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        return

    print(f"{'ID':<10} | {'Catégorie':<12} | {'Justification'}")
    print("-" * 85)
    
    count = 0
    # Utilisation de utf-8-sig pour gérer les fichiers venant de Excel/Windows avec BOM
    with open(file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if count >= limit:
                break
            
            # On nettoie les clés pour éviter les KeyError
            clean_row = {k.strip(): v for k, v in row.items()}
            cat, reason = get_explanation(clean_row)
            if cat:
                client_id = clean_row.get('id_client', 'Inconnu')
                print(f"{client_id:<10} | {cat:<12} | {reason}")
                count += 1

if __name__ == "__main__":
    csv_file = 'business_data.csv'
    display_explanations(csv_file)
