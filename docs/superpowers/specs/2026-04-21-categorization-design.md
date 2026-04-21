# Design Spec: US-12 - Catégorisation des Clients

**Date** : 2026-04-21  
**Statut** : En revue  
**Auteur** : Gemini CLI (pour Théo Delporte)

## 1. Contexte
Le manager doit prioriser ses actions commerciales en classant les clients dans 3 catégories claires : Fidéliser, Relancer, Surveiller.

## 2. Objectifs
- Lire `business_data.csv`.
- Classer chaque client selon une logique hybride (statut + comportement).
- Afficher le bilan global dans le terminal.

## 3. Architecture
- **Composant** : `categorize_clients.py`
- **Langage** : Python 3
- **Logique de classification** :
    - **Fidéliser** : Statut "Actif" ET dernier achat < 180 jours.
    - **Relancer** : Statut "Inactif"/"À relancer" OU dernier achat > 360 jours.
    - **Surveiller** : Tout client ne rentrant pas dans les deux critères précédents.

## 4. Sortie attendue
Un résumé texte affichant le nombre de clients par catégorie.

## 5. Validation
Test unitaire simulant les 3 cas pour vérifier la robustesse de la logique.
