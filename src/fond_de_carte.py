"""
fond_de_carte.py — Contours des pays pour la carte du monde, utilisables HORS CONNEXION.

Par défaut, Plotly télécharge le fond de carte sur Internet à chaque affichage :
sans connexion, la carte resterait vide. On garde donc une copie locale des
contours des pays (Natural Earth, domaine public, échelle 1:110 000 000) dans
data/base/pays.geojson.

Ce fichier est téléchargé une seule fois, avec Internet :
    - par construire_base_titres.py (construction de la base) ;
    - par fabriquer_installateur.ps1 (version installée) ;
    - ou automatiquement par le tableau de bord, la première fois qu'il en a besoin.
Les coordonnées sont arrondies (≈ 1 km) pour alléger le fichier (≈ 400 Ko).
"""

import json
import urllib.request

from . import base_titres

SOURCES = [
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson",
    "https://cdn.jsdelivr.net/gh/nvkelso/natural-earth-vector@master/geojson/ne_110m_admin_0_countries.geojson",
]
EXCLUS = {"ATA"}                    # Antarctique : prend de la place, aucune bourse


def chemin():
    return base_titres._dossier() / "pays.geojson"


def _arrondir(coordonnees, decimales=2):
    if isinstance(coordonnees, (int, float)):
        return round(coordonnees, decimales)
    return [_arrondir(c, decimales) for c in coordonnees]


def simplifier(geojson):
    """Garde le code ISO-3 (identifiant) et le nom de chaque pays, coordonnées arrondies."""
    pays = []
    for f in geojson.get("features", []):
        prop = f.get("properties", {})
        code = prop.get("ADM0_A3") or prop.get("ISO_A3") or prop.get("iso_a3") or f.get("id")
        if not code or code in EXCLUS or code == "-99":
            continue
        pays.append({"type": "Feature", "id": code, "properties": {"nom": prop.get("NAME") or prop.get("name", "")},
                     "geometry": {"type": f["geometry"]["type"],
                                  "coordinates": _arrondir(f["geometry"]["coordinates"])}})
    return {"type": "FeatureCollection", "features": pays}


def telecharger(delai=20):
    """Télécharge et enregistre le fond de carte. Renvoie True si c'est fait."""
    for url in SOURCES:
        try:
            demande = urllib.request.Request(url, headers={"User-Agent": "portfolio_tracker"})
            with urllib.request.urlopen(demande, timeout=delai) as reponse:
                donnees = simplifier(json.loads(reponse.read().decode("utf-8")))
            if len(donnees["features"]) < 100:
                continue
            chemin().parent.mkdir(parents=True, exist_ok=True)
            temporaire = chemin().with_suffix(".tmp")
            temporaire.write_text(json.dumps(donnees, separators=(",", ":")), encoding="utf-8")
            temporaire.replace(chemin())
            return True
        except Exception:
            continue
    return False


_CACHE = {}


def charger(telecharger_si_absent=True):
    """Le fond de carte (dict GeoJSON), ou None s'il n'est pas disponible."""
    fichier = chemin()
    if not fichier.exists() and telecharger_si_absent and not _CACHE.get("essai"):
        _CACHE["essai"] = True                       # un seul essai par session
        telecharger(delai=8)
    if not fichier.exists():
        return None
    cle = (str(fichier), fichier.stat().st_mtime)
    if _CACHE.get("cle") != cle:
        _CACHE["cle"], _CACHE["donnees"] = cle, json.loads(fichier.read_text(encoding="utf-8"))
    return _CACHE["donnees"]
