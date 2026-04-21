import pandas as pd


def calculer_kpi(df: pd.DataFrame) -> dict:
    """US-05 + US-07: KPI total clients et répartition par segment."""
    df_clean = df.drop_duplicates(subset=df.columns.difference(["id_client"]))
    total_clients = int(df_clean["id_client"].nunique())

    repartition = (
        df["segment"].astype(str).str.strip().str.capitalize()
        .value_counts()
        .to_dict()
    )

    return {
        "total_clients": total_clients,
        "repartition_segments": repartition,
    }


def generer_recommandations(df: pd.DataFrame) -> tuple[list[dict], int]:
    """US-11: Recommandations pour clients à risque."""
    mots_cles_risque = {"élevé", "eleve", "high"}
    df = df.copy()
    df["risque_nettoye"] = df["risque_churn"].astype(str).str.lower().str.strip()
    satisfaction = pd.to_numeric(df["satisfaction"], errors="coerce")
    jours = pd.to_numeric(df["dernier_achat_jours"], errors="coerce")

    masque = (
        df["statut_client"].isin(["Inactif", "À relancer"])
        | df["risque_nettoye"].isin(mots_cles_risque)
        | (satisfaction < 6.0)
    )
    clients = df[masque].copy()
    clients["satisfaction_num"] = pd.to_numeric(clients["satisfaction"], errors="coerce")
    clients["jours_num"] = pd.to_numeric(clients["dernier_achat_jours"], errors="coerce")
    clients["risque_nettoye"] = clients["risque_churn"].astype(str).str.lower().str.strip()
    clients["recommandation"] = clients.apply(_recommandation, axis=1)

    cols = ["id_client", "segment", "risque_churn", "satisfaction", "dernier_achat_jours", "recommandation"]
    cols = [c for c in cols if c in clients.columns]
    rows = clients[cols].where(clients[cols].notna(), other=None).to_dict(orient="records")
    return rows, len(clients)


def _recommandation(row) -> str:
    sat = row.get("satisfaction_num")
    risque = row.get("risque_nettoye", "")
    jours = row.get("jours_num")

    if pd.notna(sat) and sat < 5.0:
        return "Appel immédiat par un manager : comprendre l'insatisfaction."
    if risque in {"élevé", "eleve", "high"}:
        return "Offre de rétention agressive (réduction 20 % ou service gratuit)."
    if pd.notna(jours) and jours > 365:
        return "Campagne email de réengagement sur les nouveautés."
    return "Appel de courtoisie (Customer Success) d'ici 2 semaines."
