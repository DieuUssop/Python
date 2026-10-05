"""
comptes.py — Les comptes utilisateurs et leur espace personnel chiffré.

Chaque utilisateur crée un compte (identifiant + mot de passe) et enregistre
ses portefeuilles dans son espace. Personne d'autre ne peut les lire.

Organisation sur le disque (dossier data/comptes/) :
    comptes.json          identifiant, sels et empreinte de chaque compte
                          (AUCUN mot de passe, AUCUNE donnée de portefeuille)
    3f9a2c.../            un dossier par compte, au nom aléatoire
        index.enc         la liste chiffrée de ses portefeuilles (noms, dates)
        8b1e....enc       chaque portefeuille, chiffré

Sécurité (voir coffre.py) :
    - mot de passe remplacé par une empreinte salée (PBKDF2, 600 000 itérations) ;
    - données chiffrées avec une clé tirée du mot de passe, gardée en mémoire ;
    - message d'erreur identique pour un identifiant inconnu ou un mauvais mot
      de passe (on ne révèle pas quels comptes existent) ;
    - blocage d'une minute après 5 essais ratés.
"""

import json
import os
import re
import shutil
import time
import uuid
from pathlib import Path

import pandas as pd

from . import coffre

DOSSIER = Path(os.environ.get("PORTFOLIO_COMPTES", Path(__file__).resolve().parent.parent / "data" / "comptes"))
MOTIF_IDENTIFIANT = re.compile(r"^[a-z0-9._-]{3,30}$")
LONGUEUR_MIN = 8
ESSAIS_MAX = 5
DUREE_BLOCAGE = 60                 # secondes


class ErreurCompte(Exception):
    """Erreur à afficher à l'utilisateur. Le message (en français) sert aussi de clé
    de traduction ; les valeurs variables sont gardées à part."""

    def __init__(self, message, **valeurs):
        super().__init__(message)
        self.message, self.valeurs = message, valeurs

    def __str__(self):
        return self.message.format(**self.valeurs)


# ======================================================================
# Le registre des comptes
# ======================================================================
def _dossier():
    return Path(DOSSIER)


def _ecrire(chemin, octets):
    """Écriture "atomique" : fichier temporaire puis renommage (jamais de fichier à moitié écrit)."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    temporaire = chemin.with_name(chemin.name + ".tmp")
    temporaire.write_bytes(octets)
    os.replace(temporaire, chemin)


def _lire_registre():
    chemin = _dossier() / "comptes.json"
    if not chemin.exists():
        return {"version": 1, "comptes": {}}
    return json.loads(chemin.read_text(encoding="utf-8"))


def _ecrire_registre(registre):
    _ecrire(_dossier() / "comptes.json", json.dumps(registre, indent=1, ensure_ascii=False).encode("utf-8"))


def normaliser_identifiant(identifiant):
    return str(identifiant).strip().lower()


def nombre_de_comptes():
    return len(_lire_registre()["comptes"])


# ======================================================================
# Création et connexion
# ======================================================================
def creer_compte(identifiant, mot_de_passe, confirmation=None):
    """Crée un compte et renvoie la session ouverte."""
    identifiant = normaliser_identifiant(identifiant)
    if not MOTIF_IDENTIFIANT.match(identifiant):
        raise ErreurCompte("Identifiant invalide : 3 à 30 caractères parmi lettres minuscules, chiffres, « . », "
                           "« _ » et « - ».")
    if len(mot_de_passe) < LONGUEUR_MIN:
        raise ErreurCompte("Le mot de passe doit contenir au moins {n} caractères.", n=LONGUEUR_MIN)
    if confirmation is not None and confirmation != mot_de_passe:
        raise ErreurCompte("Les deux mots de passe ne sont pas identiques.")
    registre = _lire_registre()
    if identifiant in registre["comptes"]:
        raise ErreurCompte("Cet identifiant est déjà utilisé.")
    fiche = {
        "dossier": uuid.uuid4().hex,
        "sel_empreinte": coffre.nouveau_sel(),
        "sel_cle": coffre.nouveau_sel(),
        "iterations": coffre.ITERATIONS,
        "cree": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
        "echecs": 0,
        "bloque_jusqua": 0,
    }
    fiche["empreinte"] = coffre.empreinte(mot_de_passe, fiche["sel_empreinte"], fiche["iterations"])
    registre["comptes"][identifiant] = fiche
    _ecrire_registre(registre)
    session = Session(identifiant, fiche, coffre.cle_de_chiffrement(mot_de_passe, fiche["sel_cle"], fiche["iterations"]))
    session._sauver_index([])
    return session


def connecter(identifiant, mot_de_passe):
    """Ouvre la session d'un compte. Même message d'erreur pour un identifiant
    inconnu et un mauvais mot de passe."""
    identifiant = normaliser_identifiant(identifiant)
    registre = _lire_registre()
    fiche = registre["comptes"].get(identifiant)
    if fiche is None:
        coffre.empreinte(mot_de_passe, coffre.nouveau_sel())      # même durée de calcul qu'un vrai essai
        raise ErreurCompte("Identifiant ou mot de passe incorrect.")
    attente = int(fiche.get("bloque_jusqua", 0) - time.time())
    if attente > 0:
        raise ErreurCompte("Trop d'essais ratés : réessayez dans {n} secondes.", n=attente)
    if not coffre.verifier(mot_de_passe, fiche["sel_empreinte"], fiche["empreinte"], fiche["iterations"]):
        fiche["echecs"] = fiche.get("echecs", 0) + 1
        if fiche["echecs"] >= ESSAIS_MAX:
            fiche["echecs"], fiche["bloque_jusqua"] = 0, time.time() + DUREE_BLOCAGE
        _ecrire_registre(registre)
        raise ErreurCompte("Identifiant ou mot de passe incorrect.")
    if fiche.get("echecs"):
        fiche["echecs"] = 0
        _ecrire_registre(registre)
    return Session(identifiant, fiche, coffre.cle_de_chiffrement(mot_de_passe, fiche["sel_cle"], fiche["iterations"]))


# ======================================================================
# L'espace personnel d'un utilisateur connecté
# ======================================================================
class Session:
    """Un utilisateur connecté. La clé de chiffrement n'existe qu'ici, en mémoire."""

    def __init__(self, identifiant, fiche, cle):
        self.identifiant = identifiant
        self.dossier = _dossier() / fiche["dossier"]
        self._cle = cle
        self.derniere_activite = time.time()

    def __repr__(self):                     # la clé n'apparaît jamais dans un affichage
        return f"Session({self.identifiant!r})"

    # -- index (liste des portefeuilles) --
    def _index(self):
        chemin = self.dossier / "index.enc"
        if not chemin.exists():
            return []
        return json.loads(coffre.dechiffrer(self._cle, chemin.read_bytes()).decode("utf-8"))

    def _sauver_index(self, index):
        _ecrire(self.dossier / "index.enc", coffre.chiffrer(self._cle, json.dumps(index, ensure_ascii=False)))

    # -- portefeuilles --
    def lister(self):
        """Portefeuilles de l'utilisateur : liste de dictionnaires (id, nom, cree, maj, operations)."""
        return sorted(self._index(), key=lambda p: p["nom"].lower())

    def enregistrer(self, nom, contenu, identifiant=None):
        """Enregistre (ou remplace) un portefeuille ; contenu = fichier CSV au format du projet (octets)."""
        nom = str(nom).strip() or "Portefeuille"
        index = self._index()
        if identifiant is None:
            existant = next((p for p in index if p["nom"].lower() == nom.lower()), None)
            identifiant = existant["id"] if existant else uuid.uuid4().hex
        maintenant = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
        operations = max(0, contenu.count(b"\n") - 1) if isinstance(contenu, bytes) else 0
        _ecrire(self.dossier / f"{identifiant}.enc", coffre.chiffrer(self._cle, contenu))
        fiche = next((p for p in index if p["id"] == identifiant), None)
        if fiche:
            fiche.update({"nom": nom, "maj": maintenant, "operations": operations})
        else:
            index.append({"id": identifiant, "nom": nom, "cree": maintenant, "maj": maintenant,
                          "operations": operations})
        self._sauver_index(index)
        return identifiant

    def lire(self, identifiant):
        """Contenu (octets, CSV en clair) d'un portefeuille de l'utilisateur."""
        if identifiant not in {p["id"] for p in self._index()}:
            raise ErreurCompte("Portefeuille introuvable.")
        return coffre.dechiffrer(self._cle, (self.dossier / f"{identifiant}.enc").read_bytes())

    def renommer(self, identifiant, nom):
        index = self._index()
        for p in index:
            if p["id"] == identifiant:
                p["nom"] = str(nom).strip() or p["nom"]
        self._sauver_index(index)

    def supprimer(self, identifiant):
        index = [p for p in self._index() if p["id"] != identifiant]
        (self.dossier / f"{identifiant}.enc").unlink(missing_ok=True)
        self._sauver_index(index)

    # -- compte --
    def changer_mot_de_passe(self, ancien, nouveau, confirmation=None):
        """Vérifie l'ancien mot de passe, puis RECHIFFRE toutes les données avec la nouvelle clé."""
        registre = _lire_registre()
        fiche = registre["comptes"][self.identifiant]
        if not coffre.verifier(ancien, fiche["sel_empreinte"], fiche["empreinte"], fiche["iterations"]):
            raise ErreurCompte("Mot de passe actuel incorrect.")
        if len(nouveau) < LONGUEUR_MIN:
            raise ErreurCompte("Le mot de passe doit contenir au moins {n} caractères.", n=LONGUEUR_MIN)
        if confirmation is not None and confirmation != nouveau:
            raise ErreurCompte("Les deux mots de passe ne sont pas identiques.")
        index = self._index()
        contenus = {p["id"]: self.lire(p["id"]) for p in index}       # tout est déchiffré en mémoire...
        fiche["sel_empreinte"], fiche["sel_cle"] = coffre.nouveau_sel(), coffre.nouveau_sel()
        fiche["iterations"] = coffre.ITERATIONS
        fiche["empreinte"] = coffre.empreinte(nouveau, fiche["sel_empreinte"], fiche["iterations"])
        nouvelle_cle = coffre.cle_de_chiffrement(nouveau, fiche["sel_cle"], fiche["iterations"])
        for identifiant, contenu in contenus.items():                  # ... puis rechiffré
            _ecrire(self.dossier / f"{identifiant}.enc", coffre.chiffrer(nouvelle_cle, contenu))
        self._cle = nouvelle_cle
        self._sauver_index(index)
        _ecrire_registre(registre)

    def supprimer_compte(self, mot_de_passe):
        """Supprime définitivement le compte et toutes ses données (droit à l'effacement)."""
        registre = _lire_registre()
        fiche = registre["comptes"].get(self.identifiant)
        if fiche is None or not coffre.verifier(mot_de_passe, fiche["sel_empreinte"], fiche["empreinte"],
                                                fiche["iterations"]):
            raise ErreurCompte("Mot de passe incorrect.")
        shutil.rmtree(self.dossier, ignore_errors=True)
        del registre["comptes"][self.identifiant]
        _ecrire_registre(registre)
        self._cle = None
