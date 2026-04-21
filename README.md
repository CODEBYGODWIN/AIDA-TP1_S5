# AIDA — Tableau de bord client

AIDA est une application web Flask permettant d'importer un fichier CSV de clients, de visualiser leur segmentation et leur risque de churn, et de créer des actions de suivi commerciales.

---

## Prérequis

- Python 3.10 ou supérieur
- pip

---

## Installation

**1. Cloner le dépôt**

```bash
git clone https://github.com/CODEBYGODWIN/AIDA-TP1_S5.git
cd AIDA-TP1_S5
```

**2. Créer un environnement virtuel** (recommandé)

```bash
python -m venv venv
```

Activer l'environnement :

- Windows : `venv\Scripts\activate`
- macOS / Linux : `source venv/bin/activate`

**3. Installer les dépendances**

```bash
pip install -r requirements.txt
```

---

## Lancer l'application

```bash
python app.py
```

Ouvre ensuite [http://127.0.0.1:5000](http://127.0.0.1:5000) dans ton navigateur.

---

## Utilisation

### 1. Importer les données

Sur la page **Importer**, charge le fichier `business_data.csv` fourni dans le dépôt (ou tout autre fichier CSV respectant le même format). L'application valide les colonnes requises et stocke les données pour la session.

### 2. Apercu des données

La page **Apercu** affiche la liste des clients avec leur statut d'action calculé automatiquement (Rétention urgente, Upsell prioritaire, À surveiller, etc.). Un filtre par segment est disponible en haut de page.

### 3. Actions de suivi

La page **Actions** liste toutes les actions créées, filtrables par statut (Planifiée, En cours, Complétée, Annulée).

### 4. Créer une action

La page **+ Créer** permet de créer une action de suivi pour un client : type d'action, priorité, responsable, date d'échéance et notes. Les actions sont sauvegardées dans `actions.csv`.

### 5. Tableau de bord

La page **Dashboard** affiche le nombre total de clients uniques (KPI US-05) et un graphique de répartition par segment (US-07).

### 6. Recommandations automatiques

La page **Recommandations** liste les clients identifiés comme à risque (churn élevé, inactivité, satisfaction basse) avec une action suggérée pour chacun (US-11).

---

## Format du fichier CSV

Le fichier CSV doit contenir au minimum les colonnes suivantes :

| Colonne | Description |
|---|---|
| `id_client` | Identifiant unique du client |
| `segment` | Segment commercial (PME, Grand compte, etc.) |
| `statut_client` | Actif, Inactif ou À relancer |
| `risque_churn` | Faible, Moyen ou Élevé |
| `potentiel_upsell` | Score numérique (0–100) |
| `satisfaction` | Score de satisfaction (0–10) |
| `dernier_achat_jours` | Nombre de jours depuis le dernier achat |

---

## Structure du projet

```
AIDA-TP1_S5/
├── app.py                  # Application Flask (routes)
├── business_data.csv       # Jeu de données exemple
├── actions.csv             # Actions créées (généré automatiquement)
├── requirements.txt
├── components/
│   ├── preview.py          # Génération de l'apercu
│   ├── filter.py           # Filtrage par segment
│   ├── actions.py          # Calcul des statuts d'action
│   ├── action_list.py      # Construction de la liste d'actions
│   ├── action_manager.py   # Création et persistance des actions (US-14)
│   └── kpi.py              # KPI, répartition segments, recommandations (US-05/07/11)
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── preview.html
│   ├── actions.html
│   ├── creer_action.html
│   ├── dashboard.html
│   └── recommandations.html
├── standalone/             # Scripts autonomes (hors app web)
│   ├── US-17_access_control.py
│   ├── US-18_roles.py
│   ├── US-19_file_control.py
│   └── ...
└── tests/
    ├── test_calculate_revenue.py
    ├── test_calculate_risk.py
    └── test_categorization.py
```

---

## Lancer les tests

```bash
pytest tests/
```
