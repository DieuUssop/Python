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
                         r"price|quantity|trade|buy|sell|proceeds|commission|settle|symbol|"
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


def ameliorer(image):
    """Image plus facile à lire : niveaux de gris, contraste étiré, page redressée (inclinaison
    estimée par le profil des lignes, de −3° à +3°), puis noir et blanc (seuil d'Otsu)."""
    import numpy as np
    from PIL import ImageOps
    gris = ImageOps.autocontrast(image.convert("L"), cutoff=2)
    # inclinaison : l'angle qui rend les lignes de texte les plus nettes (variance des sommes par ligne)
    petit = gris.resize((max(1, gris.width // 4), max(1, gris.height // 4)))
    meilleur, variance_max = 0.0, -1.0
    for angle in [a / 2 for a in range(-6, 7)]:
        essai = np.asarray(petit.rotate(angle, expand=False, fillcolor=255), dtype=float)
        variance = float(np.var((essai < 128).sum(axis=1)))
        if variance > variance_max:
            meilleur, variance_max = angle, variance
    if meilleur:
        gris = gris.rotate(meilleur, expand=True, fillcolor=255)
    # seuil d'Otsu
    histogramme = np.bincount(np.asarray(gris).ravel(), minlength=256).astype(float)
    total, cumul, moyenne_totale = histogramme.sum(), 0.0, (np.arange(256) * histogramme).sum()
    poids_fond, somme_fond, seuil, ecart_max = 0.0, 0.0, 128, -1.0
    for niveau in range(256):
        poids_fond += histogramme[niveau]
        if poids_fond == 0 or poids_fond == total:
            continue
        somme_fond += niveau * histogramme[niveau]
        m1, m2 = somme_fond / poids_fond, (moyenne_totale - somme_fond) / (total - poids_fond)
        ecart = poids_fond * (total - poids_fond) * (m1 - m2) ** 2
        if ecart > ecart_max:
            seuil, ecart_max = niveau, ecart
    return gris.point(lambda v: 255 if v > seuil else 0)


def fond_sombre(image):
    """Vrai si une bonne part de la page a un fond sombre (page imprimée en « mode sombre »,
    lignes de tableau en couleur foncée) : texte clair sur fond foncé, mal lu tel quel."""
    import numpy as np
    gris = np.asarray(image.convert("L").resize((max(1, image.width // 8), max(1, image.height // 8))))
    return float((gris < 100).mean()) > 0.25


def normaliser_polarite(image):
    """Texte noir sur fond blanc partout, quelle que soit la couleur du fond de chaque zone :
    un point est du texte s'il s'écarte nettement du fond qui l'entoure (fond estimé par un
    filtre médian puis un flou). Les longs traits (bordures de tableau) sont ensuite effacés,
    car ils gênent la reconnaissance des cases."""
    import numpy as np
    from PIL import Image, ImageFilter
    gris = image.convert("L")
    pixels = np.asarray(gris).astype(np.int16)
    fond = np.asarray(gris.filter(ImageFilter.MedianFilter(9)).filter(ImageFilter.BoxBlur(6))).astype(np.int16)
    texte = np.abs(pixels - fond) > 55
    # traits : suites de points alignés bien plus longues qu'une lettre (≈ 4 hauteurs de ligne)
    try:
        from scipy.ndimage import binary_opening
        longueur = max(40, gris.height // 40)
        traits = binary_opening(texte, structure=np.ones((longueur, 1), dtype=bool)) | \
            binary_opening(texte, structure=np.ones((1, longueur * 3), dtype=bool))
        texte &= ~traits
    except ImportError:
        texte[texte.mean(axis=1) > 0.35, :] = False
    return Image.fromarray(np.where(texte, 0, 255).astype(np.uint8))


def texte_pdf(brut, echelle=3, pretraitement=False):
    """Texte de chaque page d'un PDF image (liste de textes).

    Page à fond sombre (texte clair) : polarité ramenée à « noir sur blanc » et bordures de
    tableau effacées, en résolution plus fine. Orientation : la page droite est lue d'abord ;
    les 3 autres sens ne sont essayés que si elle ne donne presque rien (impression en paysage).
    pretraitement : redresser et nettoyer l'image avant lecture (seconde tentative, plus lente)."""
    import pypdfium2
    document = pypdfium2.PdfDocument(io.BytesIO(brut))
    images = []
    for i in range(len(document)):                       # rendu des pages (rapide, une par une)
        image = document[i].render(scale=echelle).to_pil()
        if fond_sombre(image):
            image = ("sombre", document[i].render(scale=max(echelle, 4)).to_pil())
        else:
            image = ("clair", image)
        images.append(image)

    def lire(element):
        nature, image = element
        if nature == "sombre":
            image = normaliser_polarite(image)
        elif pretraitement:
            image = ameliorer(image)
        meilleur, score_max = "", -1
        for angle in (0, 90, 270, 180):
            texte = texte_image(image.rotate(angle, expand=True) if angle else image)
            score = _score(texte)
            if score > score_max:
                meilleur, score_max = texte, score
            # orientation manifestement bonne : des codes ISIN, ou un long texte avec des mots attendus
            if score >= 8 or (len(texte.strip()) >= 300 and len(MOTS_UTILES.findall(texte)) >= 4):
                break
        return reparer_nombres(reparer_isin(meilleur))

    # les pages sont lues en parallèle (le moteur travaille hors de Python : gain réel)
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max(1, min(4, len(images)))) as executeur:
        return list(executeur.map(lire, images))


_CONFUSIONS = str.maketrans({"O": "0", "o": "0", "I": "1", "l": "1", "|": "1", "S": "5", "B": "8"})


def reparer_nombres(texte):
    """Chiffres lus comme des lettres dans un nombre (« 1O5,OO » -> « 105,00 », « 65O,2O »
    -> « 650,20 ») : seulement dans un groupe qui contient déjà au moins deux vrais chiffres,
    une virgule ou un point décimal, et aucune autre lettre ; les mots ne sont jamais modifiés."""
    def corriger(m):
        groupe = m.group(0)
        if sum(ch.isdigit() for ch in groupe) < 2 or not re.search(r"[.,]", groupe):
            return groupe
        return groupe.translate(_CONFUSIONS)
    return re.sub(r"(?<![A-Za-z0-9])[0-9OoIl|SB][0-9OoIl|SB ]*[.,][0-9OoIl|SB]{1,4}(?![A-Za-z0-9])", corriger, texte)


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
