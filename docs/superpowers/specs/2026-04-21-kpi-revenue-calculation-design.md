# Design Spec: US-06 - Calcul du Chiffre d'Affaires Total

**Date** : 2026-04-21  
**Statut** : En revue  
**Auteur** : Gemini CLI (pour Théo Delporte)

## 1. Contexte
Dans le cadre du cours de management de projet, nous devons implémenter un KPI simple affichant le chiffre d'affaires (CA) total à partir d'un fichier CSV existant.

## 2. Objectifs
- Lire le fichier `business_data.csv`.
- Extraire et sommer les valeurs de la colonne `chiffre_affaires`.
- Afficher le résultat brut dans le terminal.

## 3. Architecture
- **Langage** : Python 3
- **Entrée** : `business_data.csv`
- **Sortie** : Terminal (Valeur brute)

## 4. Détails d'implémentation
Le script `calculate_revenue.py` effectuera les étapes suivantes :
1. Importer le module `csv`.
2. Initialiser une variable `total_revenue` à 0.
3. Ouvrir `business_data.csv`.
4. Utiliser `csv.DictReader` pour accéder aux colonnes par leur nom.
5. Boucler sur chaque ligne, convertir `chiffre_affaires` en float et l'ajouter au total.
6. Gérer les erreurs de conversion (données manquantes ou mal formées).
7. Afficher `total_revenue`.

## 5. Validation (Tests)
- Vérifier que le script s'exécute sans erreur.
- Comparer le résultat avec une somme manuelle ou Excel sur un échantillon pour confirmer l'exactitude.
