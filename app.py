import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="AIDA - US-20", page_icon="📝")

st.title("AIDA - Historique des actions")
st.write("US-20 : tracer les actions importantes et afficher un historique minimal.")

LOG_FILE = Path("logs.json")


def load_logs():
    if not LOG_FILE.exists():
        return []

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_logs(logs):
    with open(LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(logs, file, ensure_ascii=False, indent=2)


def add_log(action_type, description, author):
    logs = load_logs()

    new_log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type_action": action_type.strip(),
        "description": description.strip(),
        "auteur": author.strip(),
    }

    logs.append(new_log)
    save_logs(logs)


st.subheader("Ajouter une action importante")

with st.form("log_form"):
    action_type = st.selectbox(
        "Type d'action",
        [
            "Import de données",
            "Contrôle qualité",
            "Création d'action",
            "Mise à jour",
            "Validation",
            "Autre",
        ],
    )
    description = st.text_area("Description de l'action")
    author = st.text_input("Auteur", value="Ugo Bernard")

    submitted = st.form_submit_button("Enregistrer l'action")

    if submitted:
        if not description.strip():
            st.error("La description est obligatoire.")
        elif not author.strip():
            st.error("L'auteur est obligatoire.")
        else:
            add_log(action_type, description, author)
            st.success("Action enregistrée avec succès.")


st.subheader("Historique des actions")

logs = load_logs()

if logs:
    logs_df = pd.DataFrame(logs)

    expected_columns = ["timestamp", "type_action", "description", "auteur"]
    logs_df = logs_df.reindex(columns=expected_columns)

    st.info(f"{len(logs_df)} action(s) enregistrée(s).")
    st.dataframe(logs_df)

    st.subheader("Dernières actions")
    for log in reversed(logs[-5:]):
        st.write(
            f"- **{log['timestamp']}** | **{log['type_action']}** | "
            f"{log['description']} _(par {log['auteur']})_"
        )
else:
    st.warning("Aucune action enregistrée pour le moment.")