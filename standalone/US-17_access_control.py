"""
US-17 — Gabriel Pincemin (Cyber)
Contrôle d'accès
Branche : feature/US-17-pincemin-gabriel-access

User Story :
    En tant qu'administrateur, je veux qu'un utilisateur non autorisé
    ne puisse pas accéder aux données sensibles afin de protéger
    les informations métier.

Critères d'acceptation :
    - Accès refusé si non autorisé
    - Vérification du rôle utilisateur
    - Données protégées
"""

# ─────────────────────────────────────────────
# ÉTAPE 1 — Définir les rôles et permissions
# ─────────────────────────────────────────────

# Les rôles disponibles dans l'application
ROLES = ["admin", "user", "invite"]

# Permissions par ressource : qui peut accéder à quoi ?
PERMISSIONS = {
    "données_clients":    ["admin", "user"],   # admins et users
    "données_sensibles":  ["admin"],            # admins seulement
    "logs":               ["admin"],            # admins seulement
    "dashboard":          ["admin", "user"],
    "rapport_risque":     ["admin", "user"],
}


# ─────────────────────────────────────────────
# ÉTAPE 2 — Base d'utilisateurs (simulée)
# ─────────────────────────────────────────────

# En production ce serait une base de données
UTILISATEURS = {
    "gabriel.pincemin": {"role": "admin",  "actif": True},
    "emmanuel.yohore":  {"role": "user",   "actif": True},
    "ronan.dupas":      {"role": "user",   "actif": True},
    "inconnu":          {"role": "invite", "actif": True},
    "compte_bloque":    {"role": "user",   "actif": False},
}


# ─────────────────────────────────────────────
# ÉTAPE 3 — Récupérer le rôle d'un utilisateur
# ─────────────────────────────────────────────

def get_role(nom_utilisateur: str) -> str | None:
    """
    Retourne le rôle de l'utilisateur s'il existe et est actif.
    Retourne None sinon.
    """
    utilisateur = UTILISATEURS.get(nom_utilisateur)
    if utilisateur is None:
        return None          # Utilisateur inconnu
    if not utilisateur["actif"]:
        return None          # Compte désactivé
    return utilisateur["role"]


# ─────────────────────────────────────────────
# ÉTAPE 4 — Vérifier les droits d'accès
# ─────────────────────────────────────────────

def verifier_acces(nom_utilisateur: str, ressource: str) -> dict:
    """
    Vérifie si un utilisateur a le droit d'accéder à une ressource.

    Retourne un dictionnaire avec :
        - "autorise" (bool)  : True si l'accès est accordé
        - "message"  (str)   : Message clair pour l'interface
    """
    # Étape 4a : l'utilisateur existe-t-il ?
    role = get_role(nom_utilisateur)
    if role is None:
        return {
            "autorise": False,
            "message": f"🚫 Accès refusé : l'utilisateur '{nom_utilisateur}' est inconnu ou désactivé."
        }

    # Étape 4b : la ressource existe-t-elle ?
    roles_autorises = PERMISSIONS.get(ressource)
    if roles_autorises is None:
        return {
            "autorise": False,
            "message": f"🚫 Accès refusé : la ressource '{ressource}' n'existe pas."
        }

    # Étape 4c : le rôle est-il autorisé ?
    if role not in roles_autorises:
        return {
            "autorise": False,
            "message": (
                f"🚫 Accès refusé : le rôle '{role}' de '{nom_utilisateur}' "
                f"ne permet pas d'accéder à '{ressource}'."
            )
        }

    # Accès accordé
    return {
        "autorise": True,
        "message": f"✅ Accès accordé : '{nom_utilisateur}' ({role}) → '{ressource}'"
    }


# ─────────────────────────────────────────────
# ÉTAPE 5 — Décorateur de protection (bonus)
# ─────────────────────────────────────────────

def proteger(ressource: str):
    """
    Décorateur Python qui protège une fonction par contrôle d'accès.
    Utilisation :

        @proteger("données_sensibles")
        def lire_donnees(utilisateur):
            return "données confidentielles"
    """
    def decorator(func):
        def wrapper(utilisateur, *args, **kwargs):
            resultat = verifier_acces(utilisateur, ressource)
            if not resultat["autorise"]:
                print(resultat["message"])
                return None
            return func(utilisateur, *args, **kwargs)
        return wrapper
    return decorator


# Exemple d'utilisation du décorateur
@proteger("données_sensibles")
def lire_donnees_sensibles(utilisateur):
    return "📊 Données confidentielles : CA, risque client, marges..."


# ─────────────────────────────────────────────
# TESTS RAPIDES
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Tests contrôle d'accès (US-17) ===\n")

    cas = [
        ("gabriel.pincemin", "données_sensibles"),  # admin → ok
        ("emmanuel.yohore",  "données_sensibles"),  # user → refusé
        ("inconnu",          "dashboard"),           # invite → refusé
        ("compte_bloque",    "dashboard"),           # désactivé → refusé
        ("ronan.dupas",      "données_clients"),     # user → ok
        ("gabriel.pincemin", "logs"),                # admin → ok
    ]

    for utilisateur, ressource in cas:
        r = verifier_acces(utilisateur, ressource)
        print(r["message"])

    print("\n=== Test décorateur @proteger ===\n")
    print("Admin :", lire_donnees_sensibles("gabriel.pincemin"))
    print("User  :", lire_donnees_sensibles("emmanuel.yohore"))
