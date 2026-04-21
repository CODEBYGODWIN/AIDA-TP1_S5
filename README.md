# AIDA-TP1_S5 - Filtrage des Clients par Niveau de Risque

## 📋 Description
Système de filtrage des clients par niveau de risque (churn) afin d'identifier rapidement les cas prioritaires nécessitant une action immédiate.

## 🎯 Fonctionnalités

### 1. **Filtrage des Clients Prioritaires**
- Identifie les clients avec risque **MOYEN** ou **ÉLEVÉ**
- Combine avec le statut client (Inactif ou À relancer)
- Génère un CSV avec les clients à traiter en priorité

### 2. **Analyse des Risques**
- Distribution des niveaux de risque par nombre de clients
- Statistiques agrégées (CA moyen, satisfaction moyenne)
- Identification des clients à risque élevé

### 3. **Rapport Détaillé**
- Liste complète des clients prioritaires
- Données de chiffre d'affaires et satisfaction
- Export CSV pour suivi

## 📊 Résultats

### Distribution des Risques
- **MOYEN**: 155 clients (68.6%)
- **FAIBLE**: 41 clients (18.1%)
- **ÉLEVÉ**: 26 clients (11.5%)

### Clients Prioritaires
- **151 clients** nécessitent une action immédiate
- **CA total**: 639 149€
- **CA moyen par client**: 4 232€
- **Satisfaction moyenne**: 6.82/10

## 🚀 Utilisation

```bash
# Exécuter le filtrage
python3 filtre_risque.py
```

### Résultats Générés
- `clients_prioritaires.csv` : Liste complète des clients prioritaires

## 📈 Colonnes du CSV Résultat
- `id_client` : Identifiant unique
- `segment` : Type de client (PME, Grand compte, Particulier, etc.)
- `region` : Localisation
- `canal_acquisition` : Canal de vente
- `nb_commandes` : Nombre de commandes
- `chiffre_affaires` : CA généré
- `date_dernier_achat` : Dernière transaction
- `dernier_achat_jours` : Jours depuis dernier achat
- `satisfaction` : Score de satisfaction (0-10)
- `statut_client` : Actif, Inactif, À relancer
- `risque_churn` : Niveau de risque
- `potentiel_upsell` : Potentiel commercial
- `cout_support` : Coût du support

## 🔍 Logique de Filtrage

### Critères de Priorité
1. **Niveau de risque** : MOYEN ou ÉLEVÉ
2. **Statut client** : Inactif OU À relancer

### Clients Cibles
Les 151 clients prioritaires sont ceux qui :
- Présentent un risque de départ important
- Sont inactifs ou nécessitent un suivi

## 💡 Recommandations
- Contacter les clients à risque ÉLEVÉ en premier (26 clients)
- Reprendre contact avec les clients inactifs
- Proposer des solutions commerciales (upsell) aux plus gros CA