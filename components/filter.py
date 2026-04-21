import pandas as pd


def _normaliser(valeur: str) -> str:
    """Normalise un segment : strip + title case."""
    return valeur.strip().title()


def get_segments(df: pd.DataFrame) -> list[str]:
    """Retourne la liste triée des segments uniques normalisés."""
    segments = df["segment"].dropna().map(_normaliser).unique().tolist()
    return sorted(set(segments))


def filtrer_par_segment(df: pd.DataFrame, segment: str) -> pd.DataFrame:
    """
    Filtre le DataFrame sur un segment donné (insensible à la casse et aux espaces).
    Si segment est vide ou 'Tous', retourne le DataFrame complet.
    """
    if not segment or segment == "Tous":
        return df
    masque = df["segment"].dropna().map(_normaliser) == segment
    return df[masque].reset_index(drop=True)
