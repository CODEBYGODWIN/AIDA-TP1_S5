from flask import Flask, render_template, request, session, redirect, url_for, flash
import pandas as pd
import io

from components.preview import generer_apercu, valider_colonnes

app = Flask(__name__)
app.secret_key = "aida-secret-key"

TAILLE_MAX_FICHIER = 5 * 1024 * 1024  # 5 Mo


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
        flash(
            f"Colonnes manquantes dans le fichier : {', '.join(manquantes)}",
            "error"
        )
        return redirect(url_for("index"))

    apercu = generer_apercu(df)
    flash("Fichier importé avec succès.", "success")
    return render_template("preview.html", apercu=apercu, nom_fichier=fichier.filename)


if __name__ == "__main__":
    app.run(debug=True)
