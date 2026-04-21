import csv

def count_at_risk_clients(file_path):
    at_risk = 0
    total = 0
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            # On normalise pour éviter les erreurs de casse ou d'espaces
            risk = row['risque_churn'].strip().lower()
            if risk != 'faible':
                at_risk += 1
    return at_risk, total

if __name__ == "__main__":
    file = 'business_data.csv'
    at_risk, total = count_at_risk_clients(file)
    percentage = (at_risk / total) * 100 if total > 0 else 0
    print(f"{at_risk} clients à risque ({percentage:.1f}%)")
