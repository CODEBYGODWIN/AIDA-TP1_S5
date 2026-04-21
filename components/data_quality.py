import pandas as pd


def detect_missing_values(df: pd.DataFrame) -> tuple[int, pd.Series, pd.DataFrame]:
    """Retourne le total de valeurs manquantes, le détail par colonne, et les lignes concernées."""
    missing_by_column = df.isnull().sum()
    total_missing = int(missing_by_column.sum())
    rows_with_missing = df[df.isnull().any(axis=1)]
    return total_missing, missing_by_column, rows_with_missing


def detect_inconsistencies(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Retourne un dict des incohérences détectées (doublons, âges invalides, emails invalides)."""
    inconsistencies: dict[str, pd.DataFrame] = {}

    duplicated_rows = df[df.duplicated()]
    if not duplicated_rows.empty:
        inconsistencies["Lignes dupliquées"] = duplicated_rows

    if "age" in df.columns:
        invalid_age = df[
            df["age"].notna() & ((df["age"] < 0) | (df["age"] > 120))
        ]
        if not invalid_age.empty:
            inconsistencies["Âges incohérents"] = invalid_age

    if "email" in df.columns:
        invalid_email = df[
            df["email"].notna() & (~df["email"].astype(str).str.contains("@"))
        ]
        if not invalid_email.empty:
            inconsistencies["Emails incohérents"] = invalid_email

    return inconsistencies


def rapport_qualite(df: pd.DataFrame) -> dict:
    """Résumé de la qualité des données pour affichage dans le template."""
    total_missing, missing_by_col, rows_missing = detect_missing_values(df)
    inconsistencies = detect_inconsistencies(df)

    return {
        "total_manquants": total_missing,
        "manquants_par_colonne": missing_by_col[missing_by_col > 0].to_dict(),
        "nb_lignes_manquantes": len(rows_missing),
        "incoherences": {k: len(v) for k, v in inconsistencies.items()},
        "qualite_ok": total_missing == 0 and len(inconsistencies) == 0,
    }
