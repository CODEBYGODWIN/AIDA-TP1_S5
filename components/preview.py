import pandas as pd


COLONNES_REQUISES = [
    "id_client", "segment", "region", "canal_acquisition",
    "nb_commandes", "chiffre_affaires", "date_dernier_achat",
    "dernier_achat_jours", "satisfaction", "statut_client",
    "risque_churn", "potentiel_upsell", "cout_support"
]

MAX_LIGNES_APERCU = 50


def generer_apercu(df: pd.DataFrame) -> dict:
    """
    Génère les données d'aperçu tabulaire à partir d'un DataFrame.
    Retourne un dict avec colonnes, lignes et métadonnées d'affichage.
    """
    colonnes = list(df.columns)
    apercu_df = df.head(MAX_LIGNES_APERCU)
    lignes = apercu_df.values.tolist()

    return {
        "colonnes": colonnes,
        "lignes": lignes,
        "nb_lignes_total": len(df),
        "nb_lignes_affichees": len(apercu_df),
        "nb_colonnes": len(colonnes),
    }


def valider_colonnes(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    Vérifie que le DataFrame contient toutes les colonnes requises.
    Retourne (valide, colonnes_manquantes).
    """
    colonnes_manquantes = [c for c in COLONNES_REQUISES if c not in df.columns]
    return len(colonnes_manquantes) == 0, colonnes_manquantes
