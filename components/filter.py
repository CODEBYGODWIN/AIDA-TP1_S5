import pandas as pd


def _normaliser(valeur: str) -> str:
    return valeur.strip().title()


def get_segments(df: pd.DataFrame) -> list[str]:
    segments = df["segment"].dropna().map(_normaliser).unique().tolist()
    return sorted(set(segments))


def filtrer_par_segment(df: pd.DataFrame, segment: str) -> pd.DataFrame:
    if not segment or segment == "Tous":
        return df
    masque = df["segment"].dropna().map(_normaliser) == segment
    return df[masque].reset_index(drop=True)
