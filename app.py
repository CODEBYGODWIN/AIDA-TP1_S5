import pandas as pd
import streamlit as st
from pandas.errors import EmptyDataError, ParserError

st.set_page_config(page_title="AIDA - US-04", page_icon="⚠️")

st.title("AIDA - Vérification de fichier CSV")
st.write("US-04 : afficher un message d'erreur clair si le fichier est invalide.")

uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])


def validate_csv(file):
    if file is None:
        return False, "Aucun fichier sélectionné.", None

    if not file.name.lower().endswith(".csv"):
        return False, "Fichier invalide : veuillez sélectionner un fichier au format CSV.", None

    try:
        df = pd.read_csv(file)

        if df.empty:
            return False, "Le fichier CSV est vide.", None

        if len(df.columns) == 0:
            return False, "Le fichier CSV ne contient aucune colonne exploitable.", None

        return True, "Fichier valide : import possible.", df

    except EmptyDataError:
        return False, "Le fichier est vide ou ne contient aucune donnée lisible.", None

    except ParserError:
        return False, "Le fichier CSV est mal formaté ou illisible.", None

    except UnicodeDecodeError:
        return False, "Le fichier n'utilise pas un encodage texte lisible.", None

    except Exception:
        return False, "Le fichier est invalide ou ne peut pas être traité.", None


if st.button("Vérifier le fichier"):
    is_valid, message, dataframe = validate_csv(uploaded_file)

    if is_valid:
        st.success(message)
        st.write("Aperçu des données :")
        st.dataframe(dataframe.head())
    else:
        st.error(message)