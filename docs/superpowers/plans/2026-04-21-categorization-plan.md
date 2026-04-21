# US-12 - Catégorisation des Clients Implementation Plan

**Goal:** Créer un script de classification des clients pour aider le manager à prioriser ses actions.

**Architecture:** Script Python utilisant une logique conditionnelle sur les colonnes `statut_client` et `dernier_achat_jours`.

---

### Task 1: Tests et Échantillon
- [ ] **Step 1: Créer un échantillon de test** (`tests/cat_sample.csv`)
- [ ] **Step 2: Écrire le test unitaire** (`tests/test_categorization.py`)
- [ ] **Step 3: Vérifier l'échec du test**
- [ ] **Step 4: Commit** (`test: add categorization tests`)

### Task 2: Implémentation
- [ ] **Step 1: Écrire la fonction de classification dans `categorize_clients.py`**
- [ ] **Step 2: Faire passer les tests**
- [ ] **Step 3: Commit** (`feat: implement client categorization logic`)

### Task 3: Validation Finale
- [ ] **Step 1: Exécuter sur les données réelles**
- [ ] **Step 2: Commit final** (`feat: complete US-12 - display client categorization KPI`)
