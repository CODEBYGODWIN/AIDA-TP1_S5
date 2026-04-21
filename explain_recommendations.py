import csv

def get_explanation(row):
    statut = row['statut_client'].strip().lower()
    jours = int(row['dernier_achat_jours'])
    
    if statut == 'actif' and jours < 180:
        return "Fidéliser", "Client actif avec un achat récent (moins de 180 jours)."
    elif statut in ['inactif', 'à relancer'] or jours > 360:
        return "Relancer", "Client inactif ou n'ayant pas commandé depuis plus d'un an."
    else:
        return "Surveiller", "Client avec un risque de départ ou un comportement à surveiller."

def display_explanations(file_path, limit=10):
    print(f"{'ID':<10} | {'Catégorie':<12} | {'Justification'}")
    print("-" * 80)
    
    count = 0
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if count >= limit:
                break
            
            try:
                cat, reason = get_explanation(row)
                client_id = row['id_client']
                print(f"{client_id:<10} | {cat:<12} | {reason}")
                count += 1
            except (ValueError, KeyError):
                continue

if __name__ == "__main__":
    display_explanations('business_data.csv')
