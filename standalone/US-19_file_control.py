"""
US-19 — Gabriel Pincemin (Cyber)
Contrôle des fichiers importés
Branche : feature/US-19-pincemin-gabriel-file-control

User Story :
    En tant qu'administrateur, je veux contrôler les fichiers importés
    afin de réduire les risques liés à des entrées invalides ou dangereuses.

Critères d'acceptation :
    - Vérification du type de fichier
    - Validation du contenu
    - Fichier rejeté si invalide
"""

import os
import csv

# ─────────────────────────────────────────────
# ÉTAPE 1 — Vérifier l'extension du fichier
# ─────────────────────────────────────────────
def check_extension(filepath: str) -> bool:
    """
    Vérifie que le fichier a bien l'extension .csv
    Retourne True si valide, False sinon.
    """
    _, ext = os.path.splitext(filepath)
    return ext.lower() == ".csv"


# ─────────────────────────────────────────────
# ÉTAPE 2 — Vérifier la taille du fichier
# ─────────────────────────────────────────────
MAX_SIZE_MB = 10  # Taille maximale autorisée

def check_size(filepath: str) -> bool:
    """
    Vérifie que le fichier ne dépasse pas MAX_SIZE_MB mégaoctets.
    Retourne True si valide, False sinon.
    """
    size_bytes = os.path.getsize(filepath)
    size_mb = size_bytes / (1024 * 1024)
    return size_mb <= MAX_SIZE_MB


# ─────────────────────────────────────────────
# ÉTAPE 3 — Vérifier la structure du contenu
# ─────────────────────────────────────────────
COLONNES_REQUISES = {"id_client", "nom", "chiffre_affaires", "segment", "risque"}

def check_content(filepath: str) -> bool:
    """
    Ouvre le fichier CSV et vérifie que les colonnes requises sont présentes.
    Retourne True si valide, False sinon.
    """
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                return False  # Fichier vide ou illisible
            colonnes_presentes = set(reader.fieldnames)
            # Vérifie que toutes les colonnes requises sont présentes
            return COLONNES_REQUISES.issubset(colonnes_presentes)
    except Exception:
        return False  # Toute erreur de lecture → rejeté


# ─────────────────────────────────────────────
# ÉTAPE 4 — Fonction principale de contrôle
# ─────────────────────────────────────────────
def controler_fichier(filepath: str) -> dict:
    """
    Contrôle complet d'un fichier importé.

    Retourne un dictionnaire avec :
        - "valide"  (bool)  : True si le fichier passe tous les contrôles
        - "message" (str)   : Message clair pour l'utilisateur
    """
    # Vérification 1 : extension
    if not check_extension(filepath):
        return {
            "valide": False,
            "message": f"❌ Fichier rejeté : l'extension '{os.path.splitext(filepath)[1]}' n'est pas autorisée. Utilisez un fichier .csv."
        }

    # Vérification 2 : taille
    if not check_size(filepath):
        return {
            "valide": False,
            "message": f"❌ Fichier rejeté : le fichier dépasse {MAX_SIZE_MB} Mo."
        }

    # Vérification 3 : contenu / colonnes
    if not check_content(filepath):
        return {
            "valide": False,
            "message": f"❌ Fichier rejeté : colonnes requises manquantes. Colonnes attendues : {', '.join(COLONNES_REQUISES)}"
        }

    # Tout est bon
    return {
        "valide": True,
        "message": "✅ Fichier accepté : le fichier est valide et peut être importé."
    }


# ─────────────────────────────────────────────
# TESTS RAPIDES (à lancer directement)
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import tempfile

    # --- Test 1 : mauvaise extension ---
    resultat = controler_fichier("donnees.xlsx")
    print("Test 1 (mauvaise extension) :", resultat["message"])

    # --- Test 2 : fichier CSV valide (créé temporairement) ---
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write("id_client,nom,chiffre_affaires,segment,risque\n")
        f.write("1,Alice,50000,Premium,Faible\n")
        f.write("2,Bob,12000,Standard,Élevé\n")
        tmp_valide = f.name

    resultat = controler_fichier(tmp_valide)
    print("Test 2 (CSV valide)        :", resultat["message"])
    os.unlink(tmp_valide)

    # --- Test 3 : colonnes manquantes ---
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write("id_client,nom\n")
        f.write("1,Alice\n")
        tmp_incomplet = f.name

    resultat = controler_fichier(tmp_incomplet)
    print("Test 3 (colonnes manquantes):", resultat["message"])
    os.unlink(tmp_incomplet)
