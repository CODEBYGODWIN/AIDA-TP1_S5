import pandas as pd

# Mapping des valeurs brutes (CSV dirty) vers la forme canonique
_MAP_RISQUE: dict[str, str] = {
    "faible": "Faible",
    "moy": "Moyen",
    "moyen": "Moyen",
    "eleve": "Élevé",
    "elevé": "Élevé",
    "élevé": "Élevé",
    "high": "Élevé",
}

# Seuil à partir duquel le potentiel upsell est considéré élevé
SEUIL_UPSELL = 70.0


def normaliser_risque(valeur: str) -> str:
    """Convertit les variantes brutes de risque_churn en valeur canonique."""
    return _MAP_RISQUE.get(str(valeur).strip().lower(), "Inconnu")


def calculer_statut_action(risque: str, upsell: float) -> str:
    """Retourne le statut d'action recommandé pour un client."""
    if risque == "Élevé":
        return "Rétention urgente"
    if risque == "Moyen" and upsell >= SEUIL_UPSELL:
        return "Upsell prioritaire"
    if risque == "Moyen":
        return "À surveiller"
    if risque == "Faible" and upsell >= SEUIL_UPSELL:
        return "Upsell possible"
    if risque == "Faible":
        return "Fidèle"
    return "Inconnu"


def enrichir_statuts(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute la colonne statut_action au DataFrame."""
    df = df.copy()
    risque_norm = df["risque_churn"].astype(str).map(normaliser_risque)
    upsell_num = pd.to_numeric(df["potentiel_upsell"], errors="coerce").fillna(0.0)
    df["statut_action"] = [
        calculer_statut_action(r, u) for r, u in zip(risque_norm, upsell_num)
    ]
    return df


def compter_statuts(df: pd.DataFrame) -> dict[str, int]:
    """Retourne le nombre de clients par statut d'action."""
    if "statut_action" not in df.columns:
        df = enrichir_statuts(df)
    return df["statut_action"].value_counts().to_dict()
