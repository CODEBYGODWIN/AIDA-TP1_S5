# Design Spec: US-08 - Visualisation des Clients à Risque

**Date** : 2026-04-21  
**Statut** : En revue  
**Auteur** : Gemini CLI (pour Théo Delporte)

## 1. Contexte
Pour anticiper les pertes de clients (churn), le manager a besoin d'un indicateur (KPI) montrant le nombre de clients présentant un risque moyen ou élevé.

## 2. Objectifs
- Lire le fichier `business_data.csv`.
- Identifier les clients "à risque" (ceux qui ne sont pas en risque "Faible").
- Afficher dans le terminal :
    1. Le nombre total de clients à risque.
    2. Le pourcentage que cela représente par rapport à la base totale.

## 3. Architecture
- **Langage** : Python 3
- **Entrée** : `business_data.csv`
- **Sortie** : Terminal (Texte brut)

## 4. Détails d'implémentation
Le script `calculate_risk.py` suivra cette logique :
1. Importer `csv`.
2. Initialiser `total_clients = 0` et `at_risk_clients = 0`.
3. Parcourir le fichier :
    - Incrémenter `total_clients`.
    - Normaliser la valeur de la colonne `risque_churn` (passage en minuscules, suppression des espaces superflus).
    - Si la valeur normalisée n'est pas "faible" : incrémenter `at_risk_clients`.
4. Calculer le pourcentage.
5. Afficher le résultat sous la forme : `X clients à risque (Y.Y%)`.

## 5. Validation (Tests)
- Test unitaire vérifiant le compte sur un petit fichier CSV contenant les différents formats de risque ("Faible", "faible", "Moyen", "Élevé", "HIGH").
- Exécution sur les données réelles.
