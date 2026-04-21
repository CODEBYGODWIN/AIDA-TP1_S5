# Design Spec: US-13 - Justification des Recommandations

**Date** : 2026-04-21  
**Statut** : En revue  
**Auteur** : Gemini CLI (pour Théo Delporte)

## 1. Contexte
Pour que le manager ait confiance dans les recommandations (US-12), il doit comprendre la logique derrière chaque classification.

## 2. Objectifs
- Afficher une liste de clients (échantillon).
- Pour chaque client, afficher sa catégorie (Fidéliser, Relancer, Surveiller).
- Fournir une phrase d'explication simple et compréhensible.

## 3. Architecture
- **Composant** : `explain_recommendations.py`
- **Langage** : Python 3
- **Dictionnaire des justifications** :
    - **Fidéliser** : "Client actif avec un achat très récent (moins de 180 jours)."
    - **Relancer** : "Client inactif ou n'ayant pas commandé depuis plus d'un an."
    - **Surveiller** : "Client avec un risque de départ identifié ou un comportement instable."

## 4. Sortie attendue
Liste formatée dans le terminal : `ID: [ID] | Catégorie: [CAT] | Pourquoi: [EXPLICATION]`

## 5. Validation
Vérifier que l'explication correspond bien à la catégorie attribuée.
