import csv
import os
from datetime import datetime

ACTIONS_FILE = os.path.join(os.path.dirname(__file__), '..', 'actions.csv')

TYPES_ACTION = [
    "Appel téléphonique",
    "Email commercial",
    "Réunion en personne",
    "Offre spéciale",
    "Suivi relance",
    "Réévaluation satisfaction",
    "Autre",
]

PRIORITES = ["Faible", "Moyen", "Élevé", "Critique"]

STATUTS = ["Planifiée", "En cours", "Complétée", "Annulée"]

COLONNES = [
    "id_action", "id_client", "type_action", "description",
    "priorite", "statut", "date_creation", "date_echeance",
    "responsable", "notes",
]


def _chemin() -> str:
    return os.path.abspath(ACTIONS_FILE)


def charger_actions() -> list[dict]:
    chemin = _chemin()
    if not os.path.exists(chemin):
        return []
    with open(chemin, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _sauvegarder(actions: list[dict]) -> None:
    chemin = _chemin()
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLONNES)
        writer.writeheader()
        writer.writerows(actions)


def _prochain_id() -> str:
    actions = charger_actions()
    if not actions:
        return "ACT001"
    nums = [int(a["id_action"][3:]) for a in actions if a.get("id_action", "").startswith("ACT")]
    return f"ACT{max(nums) + 1:03d}" if nums else "ACT001"


def creer_action(
    id_client: str,
    type_action: str,
    description: str,
    priorite: str,
    date_echeance: str,
    responsable: str,
    notes: str = "",
) -> dict:
    action = {
        "id_action": _prochain_id(),
        "id_client": id_client.strip().upper(),
        "type_action": type_action,
        "description": description.strip(),
        "priorite": priorite,
        "statut": "Planifiée",
        "date_creation": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "date_echeance": date_echeance,
        "responsable": responsable.strip(),
        "notes": notes.strip(),
    }
    actions = charger_actions()
    actions.append(action)
    _sauvegarder(actions)
    return action
