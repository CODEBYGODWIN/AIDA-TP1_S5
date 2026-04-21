from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
import io

from components.preview import generer_apercu, valider_colonnes
from components.filter import get_segments, filtrer_par_segment

app = Flask(__name__)
app.secret_key = "aida-secret-key"

TAILLE_MAX_FICHIER = 5 * 1024 * 1024  # 5 Mo


def _df_depuis_session() -> pd.DataFrame | None:
    """Recharge le DataFrame depuis les données stockées en session."""
    data = session.get("csv_data")
    if data is None:
        return None
    return pd.read_json(io.StringIO(data), orient="split")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    fichier = request.files.get("fichier_csv")

    if not fichier or fichier.filename == "":
        flash("Aucun fichier sélectionné.", "error")
        return redirect(url_for("index"))

    if not fichier.filename.endswith(".csv"):
        flash("Le fichier doit être au format CSV.", "error")
        return redirect(url_for("index"))

    contenu = fichier.read()
    if len(contenu) > TAILLE_MAX_FICHIER:
        flash("Le fichier dépasse la taille maximale autorisée (5 Mo).", "error")
        return redirect(url_for("index"))

    try:
        df = pd.read_csv(io.BytesIO(contenu))
    except Exception:
        flash("Impossible de lire le fichier CSV. Vérifiez son format.", "error")
        return redirect(url_for("index"))

    valide, manquantes = valider_colonnes(df)
    if not valide:
        flash(f"Colonnes manquantes : {', '.join(manquantes)}", "error")
        return redirect(url_for("index"))

    # Stocke le DataFrame en session pour le filtrage
    session["csv_data"] = df.to_json(orient="split")
    session["nom_fichier"] = fichier.filename

    flash("Fichier importé avec succès.", "success")
    return redirect(url_for("preview"))


@app.route("/preview", methods=["GET"])
def preview():
    df = _df_depuis_session()
    if df is None:
        flash("Aucune donnée chargée. Importez d'abord un fichier CSV.", "error")
        return redirect(url_for("index"))

    segment_actif = request.args.get("segment", "Tous")
    df_filtre = filtrer_par_segment(df, segment_actif)

    apercu = generer_apercu(df_filtre)
    segments = ["Tous"] + get_segments(df)

    return render_template(
        "preview.html",
        apercu=apercu,
        nom_fichier=session.get("nom_fichier", "données"),
        segments=segments,
        segment_actif=segment_actif,
    )


if __name__ == "__main__":
    app.run(debug=True)
