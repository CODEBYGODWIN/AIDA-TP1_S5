import csv

def calculate_total_revenue(file_path):
    total = 0.0
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                total += float(row['chiffre_affaires'])
            except (ValueError, KeyError):
                continue
    return total

if __name__ == "__main__":
    print(calculate_total_revenue('business_data.csv'))
