"""
coffre.py — Les outils de sécurité des comptes : empreinte du mot de passe et
chiffrement des données.

1. L'EMPREINTE du mot de passe (pour vérifier la connexion)
   Le mot de passe n'est JAMAIS enregistré. On enregistre seulement son
   empreinte : le résultat d'une fonction à sens unique (PBKDF2-HMAC-SHA256),
   calculée avec un "sel" aléatoire propre à chaque compte et répétée
   600 000 fois. À la connexion, on refait le calcul et on compare.
   - le sel empêche d'utiliser des tables d'empreintes précalculées ;
   - les 600 000 répétitions rendent chaque essai lent (≈ 0,5 s) : tester
     des millions de mots de passe prendrait des années.

2. Le CHIFFREMENT des portefeuilles
   Une clé de chiffrement est DÉRIVÉE du mot de passe (même fonction, avec un
   autre sel). Elle n'existe qu'en mémoire, pendant la session : elle n'est
   jamais écrite sur le disque. Les données sont chiffrées avec Fernet
   (bibliothèque cryptography) : chiffrement AES + code d'authentification,
   qui détecte toute modification du fichier.

Conséquence voulue : sans le mot de passe, personne ne peut lire les données,
pas même l'administrateur de l'application. Mot de passe oublié = données perdues.
"""

import base64
import hashlib
import hmac
import os

from cryptography.fernet import Fernet, InvalidToken

ITERATIONS = int(os.environ.get("PORTFOLIO_ITERATIONS", 600_000))   # recommandation OWASP 2023


class DonneesIllisibles(Exception):
    """Mauvaise clé, ou fichier modifié / abîmé."""


def nouveau_sel():
    """16 octets aléatoires (générateur cryptographique du système), en hexadécimal."""
    return os.urandom(16).hex()


def _pbkdf2(mot_de_passe, sel, iterations=None):
    return hashlib.pbkdf2_hmac("sha256", mot_de_passe.encode("utf-8"), bytes.fromhex(sel),
                               iterations or ITERATIONS)


def empreinte(mot_de_passe, sel, iterations=None):
    """Empreinte du mot de passe (texte hexadécimal), à enregistrer à la place du mot de passe."""
    return _pbkdf2(mot_de_passe, sel, iterations).hex()


def verifier(mot_de_passe, sel, empreinte_attendue, iterations=None):
    """Vrai si le mot de passe correspond à l'empreinte. La comparaison se fait en temps
    constant (hmac.compare_digest) pour ne rien révéler par la durée du calcul."""
    return hmac.compare_digest(empreinte(mot_de_passe, sel, iterations), empreinte_attendue)


def cle_de_chiffrement(mot_de_passe, sel, iterations=None):
    """Clé Fernet dérivée du mot de passe (à garder seulement en mémoire)."""
    return base64.urlsafe_b64encode(_pbkdf2(mot_de_passe, sel, iterations))


def chiffrer(cle, donnees):
    """Octets en clair -> octets chiffrés."""
    if isinstance(donnees, str):
        donnees = donnees.encode("utf-8")
    return Fernet(cle).encrypt(donnees)


def dechiffrer(cle, donnees):
    """Octets chiffrés -> octets en clair. Lève DonneesIllisibles si la clé est
    mauvaise ou si le fichier a été modifié."""
    try:
        return Fernet(cle).decrypt(donnees)
    except (InvalidToken, ValueError) as erreur:
        raise DonneesIllisibles("données illisibles (mauvais mot de passe ou fichier modifié)") from erreur
