import io
import os

import pandas as pd
from flask import Flask, flash, redirect, render_template, request, session, url_for

from components.preview import generer_apercu, valider_colonnes
from components.filter import filtrer_par_segment, get_segments
from components.actions import enrichir_statuts, compter_statuts

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "aida-dev-secret")


def _df_depuis_session() -> pd.DataFrame | None:
    data = session.get("csv_data")
    if data is None:
        return None
    return pd.read_json(io.StringIO(data), orient="split")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    fichier = request.files.get("fichier")
    if not fichier or fichier.filename == "":
        flash("Aucun fichier sélectionné.", "error")
        return redirect(url_for("index"))

    try:
        df = pd.read_csv(fichier, encoding="utf-8-sig")
    except Exception as e:
        flash(f"Erreur de lecture du fichier : {e}", "error")
        return redirect(url_for("index"))

    valide, manquantes = valider_colonnes(df)
    if not valide:
        flash(f"Colonnes manquantes : {', '.join(manquantes)}", "error")
        return redirect(url_for("index"))

    session["csv_data"] = df.to_json(orient="split")
    session["nom_fichier"] = fichier.filename
    return redirect(url_for("preview"))


@app.route("/preview", methods=["GET"])
def preview():
    df = _df_depuis_session()
    if df is None:
        flash("Aucune donnée chargée. Importez d'abord un fichier CSV.", "error")
        return redirect(url_for("index"))

    segment_actif = request.args.get("segment", "Tous")
    df_filtre = filtrer_par_segment(df, segment_actif)

    # US-15 : enrichir avec le statut d'action
    df_enrichi = enrichir_statuts(df_filtre)
    resume_statuts = compter_statuts(df_enrichi)

    apercu = generer_apercu(df_enrichi)
    segments = ["Tous"] + get_segments(df)

    return render_template(
        "preview.html",
        apercu=apercu,
        nom_fichier=session.get("nom_fichier", "données"),
        segments=segments,
        segment_actif=segment_actif,
        resume_statuts=resume_statuts,
    )


if __name__ == "__main__":
    app.run(debug=True)
