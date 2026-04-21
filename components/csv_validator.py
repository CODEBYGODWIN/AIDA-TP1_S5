import pandas as pd
from pandas.errors import EmptyDataError, ParserError


def validate_csv(file) -> tuple[bool, str, pd.DataFrame | None]:
    """
    Valide un fichier CSV uploadé.
    Retourne (valide, message, dataframe_ou_None).
    """
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
