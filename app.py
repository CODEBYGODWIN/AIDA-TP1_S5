import pandas as pd
import streamlit as st

st.set_page_config(page_title="AIDA - US-03", page_icon="📊")

st.title("AIDA - Analyse de la qualité des données")
st.write("US-03 : détecter les valeurs manquantes ou incohérentes.")

uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])


def detect_missing_values(dataframe):
    missing_by_column = dataframe.isnull().sum()
    total_missing = int(missing_by_column.sum())
    rows_with_missing = dataframe[dataframe.isnull().any(axis=1)]
    return total_missing, missing_by_column, rows_with_missing


def detect_inconsistencies(dataframe):
    inconsistencies = {}

    duplicated_rows = dataframe[dataframe.duplicated()]
    inconsistencies["Lignes dupliquées"] = duplicated_rows

    if "age" in dataframe.columns:
        invalid_age = dataframe[
            dataframe["age"].notna() & ((dataframe["age"] < 0) | (dataframe["age"] > 120))
        ]
        inconsistencies["Âges incohérents"] = invalid_age

    if "email" in dataframe.columns:
        invalid_email = dataframe[
            dataframe["email"].notna() & (~dataframe["email"].astype(str).str.contains("@"))
        ]
        inconsistencies["Emails incohérents"] = invalid_email

    return inconsistencies


if uploaded_file is None:
    st.info("Importez un fichier CSV pour lancer l'analyse.")
else:
    try:
        df = pd.read_csv(uploaded_file)

        st.success("Fichier chargé avec succès.")
        st.write("Aperçu des données :")
        st.dataframe(df.head())

        st.subheader("Analyse des valeurs manquantes")
        total_missing, missing_by_column, rows_with_missing = detect_missing_values(df)

        if total_missing > 0:
            st.warning(f"{total_missing} valeur(s) manquante(s) détectée(s).")
            st.write("Valeurs manquantes par colonne :")
            st.dataframe(
                missing_by_column.reset_index().rename(
                    columns={"index": "Colonne", 0: "Valeurs manquantes"}
                )
            )

            if not rows_with_missing.empty:
                st.write("Lignes contenant des valeurs manquantes :")
                st.dataframe(rows_with_missing)
        else:
            st.success("Aucune valeur manquante détectée.")

        st.subheader("Analyse des incohérences")
        inconsistencies = detect_inconsistencies(df)

        inconsistency_found = False

        for label, result in inconsistencies.items():
            if not result.empty:
                inconsistency_found = True
                st.error(f"{label} détectée(s) : {len(result)}")
                st.dataframe(result)

        if not inconsistency_found:
            st.success("Aucune incohérence détectée.")

    except Exception as error:
        st.error(f"Erreur lors de la lecture du fichier : {error}")