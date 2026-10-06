"""
ocr.py — Lire le texte d'un PDF « image » (reconnaissance de caractères, OCR).

Pourquoi ? Un PDF peut contenir du VRAI texte (exporté par la banque : chaque
caractère est enregistré) ou seulement une IMAGE de la page (scan, photo, ou
page web imprimée avec « Microsoft Print to PDF »). Dans le second cas, il
n'y a aucun caractère à lire : il faut d'abord « regarder » l'image et y
reconnaître les lettres et les chiffres.

Moteurs utilisés (le premier disponible) :
    1. RapidOCR (bibliothèque Python, fonctionne hors connexion, installée avec
       requirements-ocr.txt et dans les installateurs) ;
    2. Tesseract, s'il est installé sur l'ordinateur.

Précautions :
    - la page peut être tournée (impression en paysage) : on essaie les 4 sens et
      on garde celui où l'on reconnaît le plus de mots utiles ;
    - un code ISIN mal lu (lettre O au lieu du chiffre 0…) est corrigé, et validé
      par sa clé de contrôle ;
    - les opérations lues ainsi sont TOUJOURS montrées pour vérification.
"""

import io
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

MOTS_UTILES = re.compile(r"quantit|cours|courtage|achat|vente|isin|ex[ée]cut|montant|brut|net|date|d[ée]bit|"
                         r"cr[ée]dit|op[ée]ration|frais", re.IGNORECASE)
_MOTEUR = {}


# ----------------------------------------------------------------------
# Moteurs de reconnaissance
# ----------------------------------------------------------------------
def _rapidocr():
    """Moteur RapidOCR (deux versions de la bibliothèque existent), ou None."""
    if "rapid" not in _MOTEUR:
        moteur = None
        try:
            from rapidocr_onnxruntime import RapidOCR
            moteur = ("ancien", RapidOCR())
        except Exception:
            try:
                from rapidocr import RapidOCR
                moteur = ("nouveau", RapidOCR())
            except Exception:
                moteur = None
        _MOTEUR["rapid"] = moteur
    return _MOTEUR["rapid"]


def _tesseract():
    return shutil.which("tesseract")


def disponible():
    """Vrai si un moteur de reconnaissance de caractères est installé."""
    return _rapidocr() is not None or _tesseract() is not None


def _boites_rapidocr(image):
    import numpy as np
    version, moteur = _rapidocr()
    tableau = np.array(image.convert("RGB"))
    if version == "ancien":
        resultat, _ = moteur(tableau)
        resultat = resultat or []
        return [(min(p[0] for p in b), min(p[1] for p in b), max(p[0] for p in b), max(p[1] for p in b), t)
                for b, t, _score in resultat]
    sortie = moteur(tableau)
    boites, textes = getattr(sortie, "boxes", None), getattr(sortie, "txts", None)
    if boites is None or textes is None:
        return []
    return [(min(p[0] for p in b), min(p[1] for p in b), max(p[0] for p in b), max(p[1] for p in b), t)
            for b, t in zip(boites, textes)]


def _boites_tesseract(image):
    with tempfile.TemporaryDirectory() as dossier:
        chemin = Path(dossier) / "page.png"
        image.save(chemin)
        langues = "fra+eng" if "fra" in subprocess.run([_tesseract(), "--list-langs"], capture_output=True,
                                                         text=True).stdout else "eng"
        sortie = subprocess.run([_tesseract(), str(chemin), "-", "-l", langues, "--psm", "6", "tsv"],
                                capture_output=True, text=True, timeout=120).stdout
    boites = []
    for ligne in sortie.splitlines()[1:]:
        c = ligne.split("\t")
        if len(c) == 12 and c[11].strip():
            x, y, l, h = (int(v) for v in c[6:10])
            boites.append((x, y, x + l, y + h, c[11]))
    return boites


def _lignes(boites):
    """Boîtes de mots -> lignes de texte (même hauteur = même ligne, de gauche à droite)."""
    if not boites:
        return ""
    hauteurs = sorted(b[3] - b[1] for b in boites)
    tolerance = max(4, hauteurs[len(hauteurs) // 2] * 0.6)
    lignes = []
    for b in sorted(boites, key=lambda b: (b[1] + b[3]) / 2):
        centre = (b[1] + b[3]) / 2
        if lignes and abs(lignes[-1]["centre"] - centre) <= tolerance:
            lignes[-1]["boites"].append(b)
        else:
            lignes.append({"centre": centre, "boites": [b]})
    return "\n".join("  ".join(b[4] for b in sorted(l["boites"], key=lambda b: b[0])) for l in lignes)


def texte_image(image):
    """Texte reconnu dans une image (PIL), lignes reconstituées."""
    boites = _boites_rapidocr(image) if _rapidocr() is not None else _boites_tesseract(image)
    return _lignes(boites)


def _score(texte):
    from .import_fichier import MOTIF_ISIN_TEXTE, isin_plausible
    isins = sum(1 for c in MOTIF_ISIN_TEXTE.findall(reparer_isin(texte)) if isin_plausible(c))
    return 5 * isins + len(MOTS_UTILES.findall(texte)) + len(texte) / 2000


def texte_pdf(brut, echelle=3):
    """Texte de chaque page d'un PDF image (liste de textes). Essaie les 4 orientations."""
    import pypdfium2
    document = pypdfium2.PdfDocument(io.BytesIO(brut))
    pages = []
    for i in range(len(document)):
        image = document[i].render(scale=echelle).to_pil()
        meilleur, score_max = "", -1
        for angle in (0, 90, 270, 180):
            texte = texte_image(image.rotate(angle, expand=True) if angle else image)
            score = _score(texte)
            if score > score_max:
                meilleur, score_max = texte, score
            if score >= 8:                       # orientation manifestement bonne : inutile d'essayer les autres
                break
        pages.append(reparer_isin(meilleur))
    return pages


# ----------------------------------------------------------------------
# Corrections des erreurs de lecture classiques
# ----------------------------------------------------------------------
_CHIFFRES = str.maketrans({"O": "0", "o": "0", "I": "1", "l": "1", "S": "5", "B": "8", "Z": "2"})


def reparer_isin(texte):
    """« FRO013380607 » (lettre O lue à la place du chiffre 0), ou « FRO0013380607 » (un
    caractère en trop) -> « FR0013380607 ». Une correction n'est retenue que si la clé de
    contrôle de l'ISIN corrigé est valide : une mauvaise correction est impossible."""
    from .import_fichier import isin_plausible as isin_valide

    def candidats(code):
        """(ISIN possible, nombre de caractères du texte qu'il remplace)."""
        traduit = code[:2] + code[2:].translate(_CHIFFRES)
        prefixes = [(code[:12], 12), (traduit[:12], 12)]
        suppressions = [(c[:13][:i] + c[:13][i + 1:], 13) for c in (code, traduit) if len(c) >= 13
                        for i in range(12, 1, -1)]
        # un chiffre (ou un O, un I…) juste après les 12 caractères : sans doute un caractère lu en double
        en_double = len(code) > 12 and code[12] in "0123456789OoIlSBZ"
        return suppressions + prefixes if en_double else prefixes + suppressions

    def corriger(m):
        brut = m.group(0)
        if sum(ch.isdigit() for ch in brut[2:14]) < 5:       # un mot (« EURONEXTPARIS »), pas un code
            return brut
        for candidat, longueur in candidats(brut):
            if len(candidat) == 12 and isin_valide(candidat):
                reste = brut[longueur:]
                return candidat + (" " + reste if reste else "")
        return brut

    return re.sub(r"(?<![A-Z0-9])[A-Z]{2}[A-Z0-9OoIlSBZ]{10}[A-Z0-9OoIlSBZ.]*", corriger, texte)
