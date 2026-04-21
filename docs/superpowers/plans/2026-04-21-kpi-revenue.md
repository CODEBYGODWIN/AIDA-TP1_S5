# US-06 - KPI Chiffre d'Affaires Total Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Créer un script Python simple qui calcule et affiche la somme brute de la colonne `chiffre_affaires` du fichier `business_data.csv`.

**Architecture:** Script autonome utilisant le module `csv` natif de Python pour garantir la portabilité sans dépendances externes.

**Tech Stack:** Python 3, CSV module.

---

### Task 1: Environnement et Fichier de Test

**Files:**
- Create: `tests/test_calculate_revenue.py`
- Create: `tests/data_sample.csv`

- [ ] **Step 1: Créer un échantillon de données CSV pour les tests**

```csv
id_client,chiffre_affaires
C1,100.50
C2,200.00
C3,50.25
```

- [ ] **Step 2: Écrire le test unitaire initial (TDD)**

```python
import unittest
import os
import csv
from calculate_revenue import calculate_total_revenue

class TestRevenueCalculation(unittest.TestCase):
    def setUp(self):
        self.test_file = 'tests/data_sample.csv'
        with open(self.test_file, 'w', newline='') as f:
            f.write("id_client,chiffre_affaires\nC1,100.50\nC2,200.00\nC3,50.25")

    def test_calculate_total_revenue(self):
        result = calculate_total_revenue(self.test_file)
        self.assertEqual(result, 350.75)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 3: Lancer le test pour vérifier qu'il échoue (car le fichier n'existe pas encore)**

Run: `python3 -m unittest tests/test_calculate_revenue.py`
Expected: `ModuleNotFoundError: No module named 'calculate_revenue'`

- [ ] **Step 4: Commit**

```bash
git add tests/test_calculate_revenue.py
git commit -m "test: add failing test for revenue calculation"
```

### Task 2: Implémentation du calcul

**Files:**
- Create: `calculate_revenue.py`

- [ ] **Step 1: Écrire la fonction de calcul minimale**

```python
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
```

- [ ] **Step 2: Lancer le test pour vérifier qu'il passe**

Run: `python3 -m unittest tests/test_calculate_revenue.py`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add calculate_revenue.py
git commit -m "feat: implement revenue calculation logic"
```

### Task 3: Validation finale sur les données réelles

- [ ] **Step 1: Exécuter le script sur le vrai fichier**

Run: `python3 calculate_revenue.py`
Expected: Une valeur brute (ex: `832045.12`)

- [ ] **Step 2: Ajouter le script final au repo**

```bash
git add calculate_revenue.py
git commit -m "feat: complete US-06 - display total revenue KPI"
```
