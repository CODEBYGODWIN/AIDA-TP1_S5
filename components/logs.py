import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs.json")

TYPES_ACTION = [
    "Import de données",
    "Contrôle qualité",
    "Création d'action",
    "Mise à jour",
    "Validation",
    "Autre",
]


def load_logs() -> list[dict]:
    if not LOG_FILE.exists():
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_logs(logs: list[dict]) -> None:
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def add_log(action_type: str, description: str, author: str) -> dict:
    """Ajoute une entrée dans le fichier de logs et retourne l'entrée créée."""
    logs = load_logs()
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type_action": action_type.strip(),
        "description": description.strip(),
        "auteur": author.strip(),
    }
    logs.append(entry)
    save_logs(logs)
    return entry


def get_recent_logs(n: int = 5) -> list[dict]:
    return load_logs()[-n:]
