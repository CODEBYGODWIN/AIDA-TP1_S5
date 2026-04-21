import pandas as pd
from components.actions import enrichir_statuts

# Ordre de priorité d'affichage des statuts
ORDRE_PRIORITE: list[str] = [
    "Rétention urgente",
    "Upsell prioritaire",
    "À surveiller",
    "Upsell possible",
    "Fidèle",
    "Inconnu",
]

# Colonnes affichées dans la liste des actions
COLONNES_LISTE = [
    "id_client", "segment", "region",
    "chiffre_affaires", "satisfaction",
    "risque_churn", "potentiel_upsell",
    "statut_action",
]


def construire_liste_actions(df: pd.DataFrame, filtre_statut: str = "Tous") -> dict:
    """
    Enrichit le DataFrame, filtre par statut si demandé,
    trie par priorité et retourne les données pour le template.
    """
    df_enrichi = enrichir_statuts(df)

    statuts_disponibles = ["Tous"] + ORDRE_PRIORITE

    if filtre_statut and filtre_statut != "Tous":
        df_filtre = df_enrichi[df_enrichi["statut_action"] == filtre_statut].copy()
    else:
        df_filtre = df_enrichi.copy()

    # Tri selon l'ordre de priorité métier
    ordre_map = {s: i for i, s in enumerate(ORDRE_PRIORITE)}
    df_filtre["_priorite"] = df_filtre["statut_action"].map(
        lambda s: ordre_map.get(s, 99)
    )
    df_filtre = df_filtre.sort_values("_priorite").drop(columns=["_priorite"])

    colonnes = [c for c in COLONNES_LISTE if c in df_filtre.columns]
    lignes = df_filtre[colonnes].values.tolist()

    comptage = {
        s: int((df_enrichi["statut_action"] == s).sum())
        for s in ORDRE_PRIORITE
        if (df_enrichi["statut_action"] == s).any()
    }

    return {
        "colonnes": colonnes,
        "lignes": lignes,
        "nb_total": len(df_enrichi),
        "nb_affiches": len(df_filtre),
        "statuts_disponibles": statuts_disponibles,
        "comptage": comptage,
    }
