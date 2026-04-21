import csv

def categorize_clients(file_path):
    stats = {"Fidéliser": 0, "Relancer": 0, "Surveiller": 0}
    
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                statut = row['statut_client'].strip().lower()
                jours = int(row['dernier_achat_jours'])
                risque = row['risque_churn'].strip().lower()
                
                # Logique de classification
                if statut == 'actif' and jours < 180:
                    cat = "Fidéliser"
                elif statut in ['inactif', 'à relancer'] or jours > 360:
                    cat = "Relancer"
                else:
                    cat = "Surveiller"
                
                stats[cat] += 1
            except (ValueError, KeyError):
                continue
    return stats

if __name__ == "__main__":
    file = 'business_data.csv'
    results = categorize_clients(file)
    print("--- Rapport de Catégorisation Client ---")
    for cat, count in results.items():
        print(f"{cat}: {count} clients")
