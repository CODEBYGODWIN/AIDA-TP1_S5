import os
import tempfile

import pandas as pd
from flask import Flask, flash, redirect, render_template, request, session, url_for

from components.preview import generer_apercu, valider_colonnes
from components.filter import filtrer_par_segment, get_segments
from components.actions import enrichir_statuts, compter_statuts
from components.action_list import construire_liste_actions
from components.action_manager import (
    creer_action, charger_actions, TYPES_ACTION, PRIORITES, STATUTS,
)
from components.kpi import calculer_kpi, generer_recommandations

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "aida-dev-secret")

_DATA_DIR = os.path.join(tempfile.gettempdir(), "aida_data")
os.makedirs(_DATA_DIR, exist_ok=True)


def _df_depuis_session() -> pd.DataFrame | None:
    chemin = session.get("csv_path")
    if not chemin or not os.path.exists(chemin):
        return None
    return pd.read_json(chemin, orient="split")


def _sauvegarder_df(df: pd.DataFrame) -> str:
    chemin = os.path.join(_DATA_DIR, "current.json")
    df.to_json(chemin, orient="split", force_ascii=False)
    return chemin


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

    session["csv_path"] = _sauvegarder_df(df)
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


@app.route("/actions", methods=["GET"])
def liste_actions():
    df = _df_depuis_session()
    if df is None:
        flash("Aucune donnée chargée. Importez d'abord un fichier CSV.", "error")
        return redirect(url_for("index"))

    filtre_statut = request.args.get("statut", "Tous")
    data = construire_liste_actions(df, filtre_statut)

    return render_template(
        "actions.html",
        data=data,
        filtre_statut=filtre_statut,
        nom_fichier=session.get("nom_fichier", "données"),
    )


@app.route("/creer-action", methods=["GET", "POST"])
def creer_action_view():
    df = _df_depuis_session()
    clients = []
    if df is not None and "id_client" in df.columns:
        clients = sorted(df["id_client"].dropna().unique().tolist())

    if request.method == "POST":
        id_client = request.form.get("id_client", "").strip()
        type_action = request.form.get("type_action", "")
        description = request.form.get("description", "").strip()
        priorite = request.form.get("priorite", "")
        date_echeance = request.form.get("date_echeance", "")
        responsable = request.form.get("responsable", "").strip()
        notes = request.form.get("notes", "").strip()

        erreurs = []
        if not id_client:
            erreurs.append("L'identifiant client est requis.")
        if not type_action:
            erreurs.append("Le type d'action est requis.")
        if not description:
            erreurs.append("La description est requise.")
        if not priorite:
            erreurs.append("La priorité est requise.")
        if not date_echeance:
            erreurs.append("La date d'échéance est requise.")
        if not responsable:
            erreurs.append("Le responsable est requis.")

        if erreurs:
            for e in erreurs:
                flash(e, "error")
        else:
            action = creer_action(id_client, type_action, description, priorite,
                                  date_echeance, responsable, notes)
            flash(f"Action {action['id_action']} créée avec succès pour le client {id_client}.", "success")
            return redirect(url_for("creer_action_view"))

    actions_existantes = charger_actions()
    return render_template(
        "creer_action.html",
        clients=clients,
        types_action=TYPES_ACTION,
        priorites=PRIORITES,
        actions_existantes=actions_existantes[-10:],
    )


@app.route("/dashboard")
def dashboard():
    df = _df_depuis_session()
    if df is None:
        flash("Aucune donnée chargée. Importez d'abord un fichier CSV.", "error")
        return redirect(url_for("index"))

    kpi = calculer_kpi(df)
    return render_template(
        "dashboard.html",
        kpi=kpi,
        nom_fichier=session.get("nom_fichier", "données"),
    )


@app.route("/recommandations")
def recommandations():
    df = _df_depuis_session()
    if df is None:
        flash("Aucune donnée chargée. Importez d'abord un fichier CSV.", "error")
        return redirect(url_for("index"))

    recs, total = generer_recommandations(df)
    return render_template(
        "recommandations.html",
        recommandations=recs,
        total=total,
        nom_fichier=session.get("nom_fichier", "données"),
    )


if __name__ == "__main__":
    app.run(debug=True)
