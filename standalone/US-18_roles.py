"""
US-18 — Gabriel Pincemin (Cyber)
Gestion des rôles admin / user
Branche : feature/US-18-pincemin-gabriel-roles

User Story :
    En tant qu'administrateur, je veux distinguer au minimum un rôle admin
    et un rôle user afin de limiter certaines actions critiques.

Critères d'acceptation :
    - Deux rôles définis
    - Actions limitées selon le rôle
    - Rôles pris en compte dans l'interface

Note : ce module s'appuie sur US-17 (contrôle d'accès) et le complète
en ajoutant la gestion CRUD des comptes et l'attribution des rôles.
"""

from datetime import datetime


# ─────────────────────────────────────────────
# ÉTAPE 1 — Définir les rôles et leurs droits
# ─────────────────────────────────────────────

ROLES_DISPONIBLES = {
    "admin": {
        "description": "Accès complet — peut créer/modifier/supprimer des comptes",
        "peut_creer_compte":      True,
        "peut_changer_role":      True,
        "peut_supprimer_compte":  True,
        "peut_voir_logs":         True,
        "peut_importer_csv":      True,
        "peut_voir_donnees":      True,
    },
    "user": {
        "description": "Accès limité — consultation et analyse uniquement",
        "peut_creer_compte":      False,
        "peut_changer_role":      False,
        "peut_supprimer_compte":  False,
        "peut_voir_logs":         False,
        "peut_importer_csv":      True,
        "peut_voir_donnees":      True,
    },
}


# ─────────────────────────────────────────────
# ÉTAPE 2 — Gestionnaire de comptes utilisateurs
# ─────────────────────────────────────────────

class GestionnaireComptes:
    """
    Gère la création, modification et suppression des comptes.
    Toutes les actions critiques vérifient le rôle de celui qui agit.
    """

    def __init__(self):
        # Compte admin initial (seeder)
        self.comptes = {
            "gabriel.pincemin": {"role": "admin", "actif": True, "cree_le": "2025-01-01"},
        }

    def _verifier_permission(self, demandeur: str, permission: str) -> bool:
        """Vérifie si le demandeur a la permission requise."""
        compte = self.comptes.get(demandeur)
        if not compte or not compte["actif"]:
            return False
        role = compte["role"]
        return ROLES_DISPONIBLES.get(role, {}).get(permission, False)

    # ── Créer un compte ──────────────────────────────────────
    def creer_compte(self, demandeur: str, nouvel_utilisateur: str, role: str) -> dict:
        """
        Crée un nouveau compte utilisateur.
        Seul un admin peut effectuer cette action.
        """
        # Vérification du droit
        if not self._verifier_permission(demandeur, "peut_creer_compte"):
            return {"succes": False, "message": f"🚫 '{demandeur}' n'est pas autorisé à créer des comptes."}

        # Vérification que le rôle demandé existe
        if role not in ROLES_DISPONIBLES:
            return {"succes": False, "message": f"🚫 Rôle '{role}' inexistant. Choisir parmi : {list(ROLES_DISPONIBLES.keys())}"}

        # Vérification que le compte n'existe pas déjà
        if nouvel_utilisateur in self.comptes:
            return {"succes": False, "message": f"🚫 Le compte '{nouvel_utilisateur}' existe déjà."}

        # Création du compte
        self.comptes[nouvel_utilisateur] = {
            "role": role,
            "actif": True,
            "cree_le": datetime.today().strftime("%Y-%m-%d"),
        }
        return {"succes": True, "message": f"✅ Compte '{nouvel_utilisateur}' créé avec le rôle '{role}'."}

    # ── Changer le rôle ──────────────────────────────────────
    def changer_role(self, demandeur: str, cible: str, nouveau_role: str) -> dict:
        """
        Change le rôle d'un utilisateur existant.
        Seul un admin peut effectuer cette action.
        """
        if not self._verifier_permission(demandeur, "peut_changer_role"):
            return {"succes": False, "message": f"🚫 '{demandeur}' n'est pas autorisé à modifier les rôles."}

        if cible not in self.comptes:
            return {"succes": False, "message": f"🚫 Utilisateur '{cible}' introuvable."}

        if nouveau_role not in ROLES_DISPONIBLES:
            return {"succes": False, "message": f"🚫 Rôle '{nouveau_role}' inexistant."}

        ancien_role = self.comptes[cible]["role"]
        self.comptes[cible]["role"] = nouveau_role
        return {
            "succes": True,
            "message": f"✅ Rôle de '{cible}' changé : '{ancien_role}' → '{nouveau_role}'."
        }

    # ── Supprimer un compte ──────────────────────────────────
    def supprimer_compte(self, demandeur: str, cible: str) -> dict:
        """
        Supprime un compte utilisateur.
        Seul un admin peut effectuer cette action.
        Un admin ne peut pas se supprimer lui-même.
        """
        if not self._verifier_permission(demandeur, "peut_supprimer_compte"):
            return {"succes": False, "message": f"🚫 '{demandeur}' n'est pas autorisé à supprimer des comptes."}

        if demandeur == cible:
            return {"succes": False, "message": "🚫 Un administrateur ne peut pas supprimer son propre compte."}

        if cible not in self.comptes:
            return {"succes": False, "message": f"🚫 Utilisateur '{cible}' introuvable."}

        del self.comptes[cible]
        return {"succes": True, "message": f"✅ Compte '{cible}' supprimé."}

    # ── Lister les comptes ───────────────────────────────────
    def lister_comptes(self, demandeur: str) -> dict:
        """Liste tous les comptes (admin uniquement)."""
        if not self._verifier_permission(demandeur, "peut_voir_logs"):
            return {"succes": False, "message": f"🚫 '{demandeur}' n'est pas autorisé à lister les comptes."}

        lignes = [f"  {'Utilisateur':<25} {'Rôle':<10} {'Actif':<6} {'Créé le'}"]
        lignes.append("  " + "-" * 55)
        for nom, info in self.comptes.items():
            lignes.append(f"  {nom:<25} {info['role']:<10} {'oui' if info['actif'] else 'non':<6} {info['cree_le']}")
        return {"succes": True, "message": "\n".join(lignes)}


# ─────────────────────────────────────────────
# TESTS RAPIDES
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Tests gestion des rôles (US-18) ===\n")

    gestion = GestionnaireComptes()

    # Créer des comptes (par l'admin)
    print(gestion.creer_compte("gabriel.pincemin", "emmanuel.yohore", "user")["message"])
    print(gestion.creer_compte("gabriel.pincemin", "ronan.dupas",     "user")["message"])
    print(gestion.creer_compte("gabriel.pincemin", "theo.delporte",   "user")["message"])

    # Un user tente de créer un compte → refusé
    print(gestion.creer_compte("emmanuel.yohore", "hacker", "admin")["message"])

    # Changer le rôle d'un user → admin
    print(gestion.changer_role("gabriel.pincemin", "ronan.dupas", "admin")["message"])

    # Un user tente de changer un rôle → refusé
    print(gestion.changer_role("emmanuel.yohore", "theo.delporte", "admin")["message"])

    # Lister les comptes (admin)
    print("\n--- Liste des comptes ---")
    print(gestion.lister_comptes("gabriel.pincemin")["message"])

    # Un user tente de lister → refusé
    print(gestion.lister_comptes("emmanuel.yohore")["message"])

    # Supprimer un compte
    print(gestion.supprimer_compte("gabriel.pincemin", "theo.delporte")["message"])

    # Auto-suppression → refusée
    print(gestion.supprimer_compte("gabriel.pincemin", "gabriel.pincemin")["message"])
