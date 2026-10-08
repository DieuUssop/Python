"""
lecture_pdf.py — Lecture d'un avis d'opéré PDF par son CONTENU, quel que soit le courtier.

Les intitulés changent d'un courtier à l'autre (« Quantité : », « Nombre de titres »,
« Qté », « Buy 15 … at 85.12 »…), mais tout avis d'opéré contient les mêmes choses :

    - un code ISIN (reconnu à coup sûr grâce à sa clé de contrôle) ;
    - une date d'exécution ;
    - trois nombres liés par  quantité × cours = montant brut  (au centime près),
      et souvent  montant brut ± frais = montant net ;
    - un mot qui donne le sens (achat, vente, buy, sell, dividende…).

Ce module repère ces éléments sans se fier à la mise en page. Il sert :
    1. de seconde lecture quand la lecture par intitulés (import_fichier.lire_avis_opere)
       ne trouve rien ;
    2. à proposer, si rien n'est sûr, un formulaire pré-rempli (src/vues_pdf.py) avec les
       dates, codes et nombres trouvés : l'utilisateur choisit, rien n'est inventé.
"""

import itertools
import re
import unicodedata

import pandas as pd

from . import import_fichier as imp

# ----------------------------------------------------------------------
# 1. Texte « codé » : il s'affiche bien, mais l'extraction donne du charabia
# ----------------------------------------------------------------------
MOTS_COURANTS = re.compile(r"\b(?:le|la|les|de|des|du|et|en|au|date|cours|quantit|montant|frais|total|achat|vente|"
                           r"valeur|the|of|and|to|in|price|buy|sell|value|eur|usd)\w*", re.IGNORECASE)


def texte_illisible(texte):
    """Vrai si le texte extrait d'un PDF est inutilisable : glyphes sans correspondance
    « (cid:12) », caractères de contrôle ou privés, ou aucun mot courant."""
    brut = (texte or "").strip()
    if len(brut) < 20:
        return False                         # pas de texte du tout : c'est un scan, traité à part
    if brut.count("(cid:") >= 5:
        return True
    visibles = [c for c in brut if not c.isspace()]
    etranges = sum(1 for c in visibles if unicodedata.category(c) in ("Cc", "Co", "Cn", "Cs") or c == "�")
    if etranges > 0.15 * len(visibles):
        return True
    lettres = sum(c.isalpha() for c in visibles)
    if lettres < 0.25 * len(visibles):
        return True
    return len(brut) > 80 and len(MOTS_COURANTS.findall(brut)) < 2


# ----------------------------------------------------------------------
# 2. Dates (chiffres ou mois en lettres, français ou anglais)
# ----------------------------------------------------------------------
MOIS = {
    "janvier": 1, "janv": 1, "jan": 1, "january": 1, "fevrier": 2, "fevr": 2, "fev": 2, "feb": 2, "february": 2,
    "mars": 3, "mar": 3, "march": 3, "avril": 4, "avr": 4, "apr": 4, "april": 4, "mai": 5, "may": 5,
    "juin": 6, "jun": 6, "june": 6, "juillet": 7, "juil": 7, "jul": 7, "july": 7, "aout": 8, "aug": 8,
    "august": 8, "septembre": 9, "sept": 9, "sep": 9, "september": 9, "octobre": 10, "oct": 10, "october": 10,
    "novembre": 11, "nov": 11, "november": 11, "decembre": 12, "dec": 12, "december": 12,
}
_MOIS = "|".join(sorted(MOIS, key=len, reverse=True))
MOTIF_DATES = re.compile(
    r"(?<!\d)(?:(?P<j>\d{1,2})[/.\-](?P<m>\d{1,2})[/.\-](?P<a>\d{4}|\d{2})(?!\d)"
    r"|(?P<a2>\d{4})-(?P<m2>\d{2})-(?P<j2>\d{2})(?!\d)"
    rf"|(?P<j3>\d{{1,2}})(?:er)?[\s\-]+(?P<m3>{_MOIS})\.?[\s\-]+(?P<a3>\d{{4}})"
    rf"|(?P<m4>{_MOIS})\.?\s+(?P<j4>\d{{1,2}}),?\s+(?P<a4>\d{{4}}))",
    re.IGNORECASE)
MOTS_EXECUTION = re.compile(r"(?:ex[ée]cut\w*|n[ée]goci\w*|trade\s*date|transaction\s*date|date\s*d['’]\s*op[ée]r\w*|"
                            r"date\s*de\s*l['’]\s*op[ée]r\w*|date\s*de\s*paiement|pay(?:ment|able)\s*date|"
                            r"achat\s*le|vente\s*le)[^\n\d]{0,30}$", re.IGNORECASE)
MOTS_DATE_ECARTEE = re.compile(r"(?:[ée]dit\w*|[ée]mi[st]\w*|imprim\w*|r[èe]glement|settlement|livraison|"
                               r"value\s*date|date\s*de\s*valeur|valeur\s*:?|arr[êe]t[ée]\s*au|"
                               r",\s*le|^\s*le)[^\n\d]{0,25}$", re.IGNORECASE)


def _sans_accents(texte):
    return "".join(c for c in unicodedata.normalize("NFKD", texte) if not unicodedata.combining(c)).lower()


def _plat(texte):
    """Même texte, même longueur, sans accents (« décembre » -> « decembre ») : les positions
    trouvées dans la copie valent pour l'original."""
    return "".join((unicodedata.normalize("NFKD", c)[:1] or c) if len(unicodedata.normalize("NFKD", c)[:1]) == 1
                   else c for c in texte)


def dates(texte):
    """[(date « JJ/MM/AAAA », début, fin, contexte avant)] dans l'ordre du texte."""
    trouvees = []
    for m in MOTIF_DATES.finditer(_plat(texte)):
        g = m.groupdict()
        try:
            if g["j"]:
                j, mo, a = int(g["j"]), int(g["m"]), int(g["a"])
            elif g["a2"]:
                j, mo, a = int(g["j2"]), int(g["m2"]), int(g["a2"])
            elif g["j3"]:
                j, mo, a = int(g["j3"]), MOIS[_sans_accents(g["m3"]).rstrip(".")], int(g["a3"])
            else:
                j, mo, a = int(g["j4"]), MOIS[_sans_accents(g["m4"]).rstrip(".")], int(g["a4"])
        except (KeyError, ValueError):
            continue
        a = a + 2000 if a < 100 else a
        if not (1 <= j <= 31 and 1 <= mo <= 12 and 1990 <= a <= 2100):
            continue
        debut_ligne = texte.rfind("\n", 0, m.start()) + 1
        trouvees.append((f"{j:02d}/{mo:02d}/{a}", m.start(), m.end(), texte[debut_ligne:m.start()]))
    return trouvees


def date_execution(texte, ligne_operation=None):
    """La date d'exécution : celle qui suit un mot « exécution / négociation / trade date »,
    sinon celle de la ligne de l'opération, sinon la première qui n'est pas une date d'édition,
    de règlement ou de valeur."""
    toutes = dates(texte)
    for d, debut, fin, avant in toutes:
        execution = MOTS_EXECUTION.search(avant)
        ecartee = MOTS_DATE_ECARTEE.search(avant)
        # « Confirmation d'exécution d'ordre — Édité le 13/03 » : le mot le plus proche l'emporte
        if execution and not (ecartee and ecartee.start() > execution.start()):
            return d
    if ligne_operation:
        sur_la_ligne = dates(ligne_operation)
        if sur_la_ligne:
            return sur_la_ligne[0][0]
    for d, debut, fin, avant in toutes:
        if not MOTS_DATE_ECARTEE.search(avant):
            return d
    return toutes[0][0] if toutes else None


# ----------------------------------------------------------------------
# 3. Nombres (formats français et anglais, milliers séparés par des espaces)
# ----------------------------------------------------------------------
_ESPACES = "    "
MOTIF_MORCEAU = re.compile(r"(?<![\w.,/:])([+\-]?)(\d+(?:[.,']\d+)*)(?![\w/:])(?!\s*%)")
LIGNES_SANS_MONTANT = re.compile(r"compte|account|client|n°|num[ée]ro|r[ée]f[ée]rence|reference|order\s*id|"
                                 r"ordre\s*n|iban|bic|siren|siret|t[ée]l[ée]phone|phone|\bt[ée]l\b|\bfax\b|code\s*postal|"
                                 r"\brcs\b|capital\s*(?:social\s*)?de",
                                 re.IGNORECASE)


def _valeurs(texte_nombre):
    """Lectures possibles d'un nombre écrit : « 3,512 » = 3,512 (français) ou 3 512 (anglais)."""
    lectures = set()
    principal = imp.convertir_nombres(pd.Series([texte_nombre])).iloc[0]
    if principal == principal:
        lectures.add(round(abs(principal), 6))
    nu = texte_nombre.lstrip("+-")
    if re.fullmatch(r"\d{1,3},\d{3}", nu):                      # « 3,512 » : aussi 3 512 à l'anglaise
        lectures.add(float(nu.replace(",", "")))
    if re.fullmatch(r"\d{1,3}\.\d{3}", nu):                     # « 1.705 » : aussi 1 705 à l'allemande
        lectures.add(float(nu.replace(".", "")))
    return lectures


def nombres(texte):
    """Tous les nombres candidats du texte : [dict(valeur, debut, fin, ecrit, signe, ligne)].
    Les dates, heures, codes ISIN et numéros de compte sont écartés. Un nombre écrit avec des
    espaces (« 1 440,00 ») donne plusieurs candidats : « 1 440,00 » et « 1 » + « 440,00 » —
    la cohérence quantité × cours = montant tranchera."""
    masque = list(texte)
    for d in dates(texte):
        masque[d[1]:d[2]] = " " * (d[2] - d[1])
    for m in re.finditer(r"[A-Z]{2}[A-Z0-9]{9}\d", texte):
        masque[m.start():m.end()] = " " * 12
    for m in re.finditer(r"\d{1,2}:\d{2}(?::\d{2})?", texte):
        masque[m.start():m.end()] = " " * (m.end() - m.start())
    propre = "".join(masque)
    candidats = []
    debut_ligne = 0
    for ligne in propre.split("\n"):
        if not LIGNES_SANS_MONTANT.search(ligne):
            morceaux = [m for m in MOTIF_MORCEAU.finditer(ligne)]
            for i, m in enumerate(morceaux):
                # le morceau seul, puis regroupé avec les suivants séparés par une espace (milliers)
                groupe, fin = m.group(2), m.end()
                suites = [(groupe, fin)]
                if re.fullmatch(r"\d{1,3}", groupe):
                    for suivant in morceaux[i + 1:]:
                        entre = ligne[fin:suivant.start()]
                        if suivant.group(1) or not entre or entre.strip(_ESPACES) or len(entre) > 2 or \
                                not re.fullmatch(r"\d{3}(?:[.,]\d+)?", suivant.group(2)):
                            break
                        groupe, fin = groupe + suivant.group(2), suivant.end()
                        suites.append((groupe, fin))
                        if not re.fullmatch(r"\d+", groupe):
                            break
                for ecrit, fin_ecrit in suites:
                    if len(re.sub(r"\D", "", ecrit)) >= 9 and not re.search(r"[.,]", ecrit):
                        continue                                 # identifiant, pas un montant
                    for valeur in _valeurs(m.group(1) + ecrit):
                        if valeur > 0:
                            candidats.append({"valeur": valeur, "debut": debut_ligne + m.start(),
                                              "fin": debut_ligne + fin_ecrit, "ecrit": m.group(1) + ecrit,
                                              "signe": m.group(1), "ligne": ligne.strip()})
        debut_ligne += len(ligne) + 1
    return candidats


# ----------------------------------------------------------------------
# 4. Le trio quantité × cours = montant
# ----------------------------------------------------------------------
MOTS_QUANTITE = re.compile(r"quantit|qt[ée]|nombre|titres?\b|parts?\b|actions?\b|shares?\b|units?\b|nominal|"
                           r"buy|sell|bought|sold|achat|vente", re.IGNORECASE)
MOTS_COURS = re.compile(r"cours|prix|price|\bat\b|@|unitaire|dividende\s*unitaire|par\s*action", re.IGNORECASE)
MOTS_BRUT = re.compile(r"brut|gross|value|valeur|montant|amount|total|consideration", re.IGNORECASE)
MOTS_FRAIS = re.compile(r"courtage|commission|frais|fees?|costs?|brokerage|ttf|taxe\s*sur\s*les\s*transactions|"
                        r"transactions\s*financi[eè]res|stamp\s*duty", re.IGNORECASE)
MOTS_NET = re.compile(r"\bnet|total|d[ée]bit|cr[ée]dit|à\s*payer|to\s*pay|settlement\s*amount", re.IGNORECASE)


def _contexte(texte, candidat, avant=28):
    """Les derniers caractères avant le nombre, sur la même ligne."""
    debut = max(0, candidat["debut"] - avant, texte.rfind("\n", 0, candidat["debut"]) + 1)
    return texte[debut:candidat["debut"]]


def _se_chevauchent(*candidats):
    zones = sorted((c["debut"], c["fin"]) for c in candidats)
    return any(a[1] > b[0] for a, b in zip(zones, zones[1:]))


def trio(texte, candidats=None):
    """Meilleur trio (quantité, cours, montant brut, frais, montant net) ou None (voir trios)."""
    liste = trios(texte, candidats)
    return liste[0] if liste else None


def trios(texte, candidats=None, nombre=6):
    """Trios (quantité, cours, montant brut, frais, montant net) cohérents, du plus probable au
    moins probable (au plus `nombre`, valeurs distinctes).

    quantité × cours doit retomber sur un autre nombre du texte au centime près (montant brut),
    ou, à défaut, sur montant net ∓ frais. Le score favorise une quantité entière, un cours et
    une quantité placés près de leurs intitulés, et un montant net cohérent avec les frais.
    Les suivants servent à départager avec les cours du marché (arbitrer_par_le_marche)."""
    candidats = candidats if candidats is not None else nombres(texte)
    uniques = {}
    for c in candidats:
        uniques.setdefault((c["valeur"], c["debut"], c["fin"]), c)
    candidats = list(uniques.values())
    par_valeur = {}
    for c in candidats:
        par_valeur.setdefault(round(c["valeur"], 2), []).append(c)
    trouves = []
    petits = [c for c in candidats if c["valeur"] < 1e7]
    for q, p in itertools.permutations(petits, 2):
        if _se_chevauchent(q, p) or q["valeur"] > 1e6:
            continue
        produit = q["valeur"] * p["valeur"]
        if produit < 0.5:
            continue
        cibles = [b for cle in (round(produit, 2), round(produit + 0.005, 2), round(produit - 0.005, 2))
                  for b in par_valeur.get(cle, [])]
        for b in cibles:
            if b is q or b is p or _se_chevauchent(q, p, b) or abs(b["valeur"] - produit) > 0.0101:
                continue
            if q["valeur"] == 1 and p["valeur"] == b["valeur"] and not MOTS_QUANTITE.search(_contexte(texte, q)):
                continue                          # 1 × x = x : coïncidence, sauf « Quantité : 1 »
            score = _score_trio(texte, q, p, b)
            frais, net = _frais_et_net(texte, candidats, b, (q, p))
            score += 3 if net is not None else 0
            trouves.append((score, {"quantite": q, "cours": p, "brut": b, "frais": frais, "net": net}))
    if not trouves:
        # Pas de montant brut écrit : quantité × cours ± frais = montant net
        frais_etiquetes = [c for c in candidats if MOTS_FRAIS.search(_contexte(texte, c))]
        for q, p in itertools.permutations(petits, 2):
            if _se_chevauchent(q, p):
                continue
            if q["valeur"] == 1 and not MOTS_QUANTITE.search(_contexte(texte, q)):
                continue
            produit = q["valeur"] * p["valeur"]
            for f in frais_etiquetes:
                if f is q or f is p:
                    continue
                for total in (produit + f["valeur"], produit - f["valeur"]):
                    for n in par_valeur.get(round(total, 2), []):
                        if n in (q, p, f) or _se_chevauchent(q, p, n) or abs(n["valeur"] - total) > 0.0101:
                            continue
                        trouves.append((_score_trio(texte, q, p, n), {"quantite": q, "cours": p, "brut": None,
                                                                      "frais": f["valeur"], "net": n["valeur"]}))
    trouves.sort(key=lambda x: -x[0])
    resultat, vus = [], set()
    for score, t in trouves:
        cle = (round(t["quantite"]["valeur"], 6), round(t["cours"]["valeur"], 6))
        if cle in vus:
            continue
        vus.add(cle)
        resultat.append(dict(t, score=score))
        if len(resultat) >= nombre:
            break
    return resultat


def _score_trio(texte, q, p, b):
    score = 0.0
    if float(q["valeur"]).is_integer():
        score += 2
    if MOTS_QUANTITE.search(_contexte(texte, q)) or MOTS_QUANTITE.search(texte[q["fin"]:q["fin"] + 10]):
        score += 2
    if MOTS_COURS.search(_contexte(texte, p)):
        score += 2
    if MOTS_BRUT.search(_contexte(texte, b)):
        score += 1
    if MOTS_FRAIS.search(_contexte(texte, q) + _contexte(texte, p)):
        score -= 4
    if q["ligne"] == p["ligne"] == b["ligne"]:
        score += 1
    # quantité avant le cours avant le montant : l'ordre habituel d'une ligne d'opération
    if q["debut"] < p["debut"] < b["debut"]:
        score += 0.5
    return score


def _frais_et_net(texte, candidats, brut, exclus=()):
    """Frais : nombres précédés de « courtage, commission, frais, costs… » ; montant net : un
    nombre égal à brut ± frais. Si aucun frais n'est écrit, un écart brut/net plausible (< 5 %)
    entre deux nombres sert de frais."""
    etiquetes = [c for c in candidats if c is not brut and c not in exclus
                 and MOTS_FRAIS.search(_contexte(texte, c, 45)) and not _se_chevauchent(c, brut)]
    vus, frais = set(), 0.0
    for c in etiquetes:
        if c["debut"] in vus:
            continue
        vus.add(c["debut"])
        frais += c["valeur"]
    for c in candidats:
        if c is brut or _se_chevauchent(c, brut) or c in exclus:
            continue
        for total in (brut["valeur"] + frais, brut["valeur"] - frais) if frais else ():
            if abs(c["valeur"] - total) < 0.011:
                return round(frais, 2), c["valeur"]
    if not frais:
        for c in candidats:
            ecart = abs(c["valeur"] - brut["valeur"])
            if c is not brut and c not in exclus and not _se_chevauchent(c, brut) and 0 < ecart < 0.05 * brut["valeur"] \
                    and MOTS_NET.search(_contexte(texte, c, 30)):
                return round(ecart, 2), c["valeur"]
    return (round(frais, 2) if frais else None), None


# ----------------------------------------------------------------------
# 5. Une opération par code ISIN
# ----------------------------------------------------------------------
MOTIF_SENS = re.compile(r"(?<![a-zà-ÿ])(rachat|achat|vente|souscription|buy|sell|bought|sold|kauf|verkauf|"
                        r"dividende|dividend|coupon|distribution)", re.IGNORECASE)
MOTIF_DEVISE = re.compile(r"(?<![A-Z])(EUR|USD|GBP|GBX|CHF|JPY|CAD|AUD|HKD|DKK|SEK|NOK)(?![A-Z])|(€|\$|£)")
SYMBOLES = {"€": "EUR", "$": "USD", "£": "GBP"}


def isins(texte):
    """Codes ISIN valides et réalistes, dans l'ordre : [(isin, position)]."""
    vus, liste = set(), []
    for m in imp.MOTIF_ISIN_TEXTE.finditer(texte):
        code = m.group(1)
        if imp.isin_plausible(code):
            liste.append((code, m.start()))
            vus.add(code)
    return liste


def _segments(texte):
    """Découpe le texte en une zone par opération. Un seul ISIN (même répété) : tout le texte.
    Plusieurs ISIN différents : chaque zone va du début de la ligne de son ISIN au début de la
    ligne de l'ISIN suivant."""
    trouves = isins(texte)
    distincts = list(dict.fromkeys(code for code, _ in trouves))
    if len(distincts) <= 1:
        return [(distincts[0] if distincts else None, texte, texte)]
    debuts = []
    for code, position in trouves:
        if debuts and debuts[-1][0] == code:
            continue
        debuts.append((code, texte.rfind("\n", 0, position) + 1))
    segments = []
    for i, (code, debut) in enumerate(debuts):
        fin = debuts[i + 1][1] if i + 1 < len(debuts) else len(texte)
        segments.append((code, texte[debut:fin], texte))
    return segments


def _sens(segment, isin):
    trouves = list(MOTIF_SENS.finditer(segment))
    if not trouves:
        return None
    position = segment.find(isin) if isin else 0
    return min(trouves, key=lambda m: abs(m.start() - position)).group(1)


def _devise(segment, cours):
    """Devise écrite juste après (ou juste avant) le cours, sinon la plus fréquente du texte."""
    apres = segment[cours["fin"]:cours["fin"] + 6] if cours else ""
    avant = segment[max(0, cours["debut"] - 5):cours["debut"]] if cours else ""
    for zone in (apres, avant):
        m = MOTIF_DEVISE.search(zone)
        if m:
            return m.group(1) or SYMBOLES[m.group(2)]
    toutes = [m.group(1) or SYMBOLES[m.group(2)] for m in MOTIF_DEVISE.finditer(segment)]
    return max(set(toutes), key=toutes.count) if toutes else ""


def _libelle(segment, isin):
    nom = imp._nom_apres_isin(segment, isin) if isin else ""
    if nom and re.search(r"[A-Za-z]{2}", nom) and not re.match(r"^(?:at|@|\))", nom):
        return nom.strip(" ()")
    if isin:
        ligne = next((l for l in segment.splitlines() if isin in l), "")
        avant = ligne.split(isin)[0]
        avant = MOTIF_SENS.sub(" ", avant)
        avant = re.sub(r"\b(?:isin|code|valeur|titre|instrument)\b\s*:?|[():]|[+\-]?\d[\d\s.,]*", " ", avant,
                       flags=re.IGNORECASE)
        avant = re.sub(r"\s{2,}", " ", avant).strip(" -·")
        avant = re.sub(r"^(?:(?:de|du|des|d'|of|au|le|la|les|l')\s*)+", "", avant, flags=re.IGNORECASE).strip()
        if re.search(r"[A-Za-z]{2}", avant):
            return avant
    m = imp.MOTIFS_AVIS["libelle"].search(segment)
    return m.group(1).strip() if m else ""


def lire_par_le_contenu(texte):
    """Opérations lues sans se fier aux intitulés : liste de dict(date, sens, isin, libelle,
    quantite, cours, devise, frais, montant, sur). « sur » est vrai si les quatre éléments
    essentiels sont trouvés (ISIN, date, trio cohérent, mot donnant le sens)."""
    operations = []
    for isin, segment, tout in _segments(texte):
        if not isin:
            continue
        ligne = next((l for l in segment.splitlines() if isin in l), "")
        date = date_execution(segment, ligne) or date_execution(tout, ligne)
        tous = trios(segment)
        t = tous[0] if tous else None
        sens = _sens(segment, isin) or (_sens(tout, isin) if len(_segments(texte)) == 1 else None)
        if sens is None and t and t["quantite"]["signe"]:
            sens = "VENTE" if t["quantite"]["signe"] == "-" else "ACHAT"
        operations.append({
            "date": date, "sens": sens, "isin": isin, "libelle": _libelle(segment, isin)[:60],
            "quantite": float(t["quantite"]["valeur"]) if t else None,
            "cours": float(t["cours"]["valeur"]) if t else None,
            "devise": _devise(segment, t["cours"] if t else None),
            "frais": t["frais"] if t else None,
            "montant": (float(t["brut"]["valeur"]) if t and t["brut"] else (t["net"] if t else None)),
            "sur": bool(date and t and sens),
            "net": t["net"] if t else None,
            # autres lectures cohérentes, pour départager avec les cours du marché
            "alternatives": [{"quantite": float(a["quantite"]["valeur"]), "cours": float(a["cours"]["valeur"]),
                              "frais": a["frais"], "montant": float(a["brut"]["valeur"]) if a["brut"] else a["net"]}
                             for a in tous[1:]],
        })
        if date and tous:
            # toutes les lectures cohérentes (la meilleure comprise), quelle que soit la lecture retenue
            ALTERNATIVES[(isin, date)] = [{"quantite": float(a["quantite"]["valeur"]), "cours": float(a["cours"]["valeur"]),
                                           "frais": a["frais"]} for a in tous]
    return operations


# Lectures alternatives des dernières opérations lues : (isin, date) -> [alternatives, quantité, cours]
ALTERNATIVES = {}


def arbitrer_par_le_marche(transactions, historique, isin_par_ticker, tolerance=0.15, proche=0.05):
    """Départage par les cours du marché : si le cours lu s'écarte de plus de 15 % du cours de
    clôture du jour de l'opération alors qu'une autre lecture cohérente du document (quantité ×
    cours = montant) tombe à moins de 5 % de ce cours, c'est cette autre lecture qui est retenue.
    Renvoie (transactions, notes)."""
    if historique is None or transactions is None or transactions.empty:
        return transactions, []
    t = transactions.copy()
    notes = []
    for i, ligne in t.iterrows():
        isin = isin_par_ticker.get(ligne["ticker"])
        if not isin or ligne["type"] not in ("ACHAT", "VENTE") or ligne["ticker"] not in historique.columns:
            continue
        date = pd.Timestamp(ligne["date"]).strftime("%d/%m/%Y")
        entree = ALTERNATIVES.get((isin, date))
        if not entree:
            continue
        cours_marche = imp._valeur_au(historique[ligne["ticker"]], pd.Timestamp(ligne["date"]))
        if not cours_marche or cours_marche != cours_marche:
            continue
        if abs(ligne["prix"] / cours_marche - 1) <= tolerance:
            continue
        meilleure = min(entree, key=lambda a: abs(a["cours"] / cours_marche - 1))
        if abs(meilleure["cours"] / cours_marche - 1) <= proche:
            t.at[i, "quantite"] = meilleure["quantite"]
            t.at[i, "prix"] = meilleure["cours"]
            if meilleure["frais"] is not None:
                t.at[i, "frais"] = meilleure["frais"]
            notes.append({"ticker": ligne["ticker"], "date": date, "ancien": float(ligne["prix"]),
                          "nouveau": meilleure["cours"], "marche": float(cours_marche)})
    return t, notes


def en_ligne_avis(operation):
    """dict -> ligne au format import_fichier.COLONNES_AVIS (textes)."""
    def nombre(x):
        return "" if x is None else f"{x:.6f}".rstrip("0").rstrip(".")
    sens = operation["sens"] or "ACHAT"
    quantite = operation["quantite"]
    return [operation["date"] or "", sens, operation["isin"], operation["libelle"] or operation["isin"],
            nombre(quantite), nombre(operation["cours"]), operation["devise"] or "",
            nombre(operation["frais"]) if operation["frais"] else "", nombre(operation["montant"])]


# ----------------------------------------------------------------------
# 6. Pour le formulaire de secours : tout ce qui a été trouvé
# ----------------------------------------------------------------------
def candidats(textes):
    """Ce que contient le document, pour pré-remplir le formulaire (src/vues_pdf.py) :
    dates, codes ISIN (avec un libellé), nombres (avec leur contexte), sens, devise,
    meilleure proposition, et le texte lu."""
    texte = "\n".join(textes)
    proposition = next(iter(lire_par_le_contenu(texte)), None)
    vus, liste_nombres = set(), []
    # « 5 650,20 » peut être 5 650,20 ou « 5 » puis « 650,20 » : toutes les lectures sont proposées
    for c in nombres(texte):
        cle = (c["ecrit"], c["debut"])
        if cle in vus or c["valeur"] == 0:
            continue
        vus.add(cle)
        contexte = re.sub(r"\s+", " ", (texte[max(0, c["debut"] - 30):c["debut"]] + "[" + c["ecrit"] + "]"
                                        + texte[c["fin"]:c["fin"] + 12]).replace("\n", " ")).strip()
        liste_nombres.append({"valeur": c["valeur"], "ecrit": c["ecrit"], "contexte": contexte})
    sens_trouve = MOTIF_SENS.search(texte)
    return {
        "dates": list(dict.fromkeys(d[0] for d in dates(texte))),
        "date_proposee": date_execution(texte),
        "isins": [(code, _libelle(texte, code)) for code in dict.fromkeys(c for c, _ in isins(texte))],
        "nombres": liste_nombres,
        "sens": imp.classer_type(sens_trouve.group(1)) if sens_trouve else None,
        "devise": _devise(texte, None) or "EUR",
        "proposition": proposition,
        "texte": texte,
    }


# ----------------------------------------------------------------------
# 7. Modèles appris : le formulaire complété une fois sert pour les avis suivants du même type
# ----------------------------------------------------------------------
# Un « modèle » retient, pour un type de document (reconnu à son vocabulaire), l'intitulé qui
# précède chaque information (« Nominal », « Qté exécutée », « Px moyen »…). Il ne contient
# aucun montant ni aucun nom en clair : le vocabulaire du document est gardé sous forme
# d'empreintes (hachage), et seuls les intitulés choisis sont lisibles.
SEUIL_MODELE = 0.6
MOTIF_CODE_SENS = re.compile(r"\b(sens|op[ée]ration|op\.|nature|type|side)\s*:?\s*([A-Za-z]{1,12})\b", re.IGNORECASE)
CHAMPS_MODELE = ("quantite", "cours", "frais", "montant")


def _fichier_modeles():
    from .base_titres import DOSSIER
    return DOSSIER / "modeles_pdf.json"


def _empreinte(texte):
    """Vocabulaire du document (mots de 3 lettres ou plus, sans chiffres), haché."""
    import hashlib
    mots = set(re.findall(r"[a-z]{3,}", _sans_accents(texte or "")))
    mots -= set(MOIS)
    return {hashlib.sha1(m.encode()).hexdigest()[:10] for m in mots}


def _ressemblance(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0


def charger_modeles():
    import json
    fichier = _fichier_modeles()
    try:
        return json.loads(fichier.read_text(encoding="utf-8")) if fichier.exists() else []
    except (OSError, ValueError):
        return []


def _enregistrer_modeles(modeles):
    import json
    fichier = _fichier_modeles()
    try:
        fichier.parent.mkdir(parents=True, exist_ok=True)
        fichier.write_text(json.dumps(modeles[-50:], ensure_ascii=False, indent=1), encoding="utf-8")
    except OSError:
        pass                                     # dossier en lecture seule : on n'apprend pas


def _mots_avant(ligne_avant):
    """Les (au plus) trois derniers mots avant une valeur : son intitulé."""
    mots = re.findall(r"[a-z]+", _sans_accents(ligne_avant))
    return " ".join(mots[-3:])


def _etiquette_de(texte, valeur):
    """Intitulé et rang de la valeur sur sa ligne (rang = nombre de valeurs entre l'intitulé et
    elle). Les écritures « entières » (« 3 251,00 ») sont préférées à leurs morceaux."""
    if valeur is None:
        return None
    possibles = [c for c in nombres(texte) if abs(c["valeur"] - abs(valeur)) <= max(0.0051, 1e-6 * abs(valeur))]
    if not possibles:
        return None
    c = max(possibles, key=lambda x: x["fin"] - x["debut"])
    debut_ligne = texte.rfind("\n", 0, c["debut"]) + 1
    avant = texte[debut_ligne:c["debut"]]
    # découper ce qui précède en « morceaux de mots » séparés par des nombres :
    # l'intitulé est le dernier morceau qui contient des mots ; le rang compte les nombres après lui
    morceaux = re.split(r"[+\-]?\d[\d\s.,']*", avant)
    for rang, morceau in enumerate(reversed(morceaux)):
        etiquette = _mots_avant(morceau)
        if etiquette:
            return {"etiquette": etiquette, "rang": rang}
    return None


def apprendre(texte, operation):
    """Retient le modèle d'un document après que l'utilisateur a complété le formulaire.
    operation : dict(date « JJ/MM/AAAA », type, quantite, cours, frais, montant)."""
    champs = {nom: _etiquette_de(texte, operation.get(nom)) for nom in CHAMPS_MODELE}
    champs = {k: v for k, v in champs.items() if v}
    if not champs.get("quantite") or not champs.get("cours"):
        return False                              # rien de réutilisable
    date = next((d for d in dates(texte) if d[0] == operation.get("date")), None)
    modele = {"empreinte": sorted(_empreinte(texte)), "champs": champs, "type": operation.get("type"),
              "date": _mots_avant(date[3]) if date else "", "sens": {}}
    # sens écrit en code (« Sens : A », « Op. : S ») : on retient la correspondance code -> type
    code = MOTIF_CODE_SENS.search(texte)
    if code and not MOTIF_SENS.search(texte) and operation.get("type"):
        modele["sens"] = {code.group(2).lower(): operation["type"]}
    anciens = [m for m in charger_modeles() if _ressemblance(set(m["empreinte"]), set(modele["empreinte"])) >= 0.85]
    for ancien in anciens:                       # garder les codes de sens déjà appris
        modele["sens"] = {**ancien.get("sens", {}), **modele["sens"]}
    modeles = [m for m in charger_modeles()
               if _ressemblance(set(m["empreinte"]), set(modele["empreinte"])) < 0.85]
    _enregistrer_modeles(modeles + [modele])
    return True


def _valeur_apres(texte, etiquette, rang):
    """La valeur qui suit l'intitulé (au rang donné) sur sa ligne, sinon la première de la ligne
    suivante."""
    lignes = texte.split("\n")
    for i, ligne in enumerate(lignes):
        plat = _sans_accents(ligne)
        mots = [(m.group(0), m.end()) for m in re.finditer(r"[a-z]+", plat)]
        cible = etiquette.split()
        for j in range(len(mots) - len(cible) + 1):
            if [w for w, _ in mots[j:j + len(cible)]] == cible:
                fin = mots[j + len(cible) - 1][1]
                apres = nombres(ligne[fin:])
                # écritures entières, dans l'ordre
                entieres = []
                for c in sorted(apres, key=lambda c: (c["debut"], -(c["fin"] - c["debut"]))):
                    if not entieres or c["debut"] >= entieres[-1]["fin"]:
                        entieres.append(c)
                if len(entieres) > rang:
                    return entieres[rang]["valeur"]
                if not entieres and i + 1 < len(lignes):
                    suivante = nombres(lignes[i + 1])
                    if suivante:
                        return suivante[0]["valeur"]
    return None


def lire_avec_modele(texte, modeles=None):
    """Opération lue avec le modèle appris le plus ressemblant (dict comme lire_par_le_contenu),
    ou None. Le résultat doit rester cohérent : quantité × cours = montant (à 1 % près) quand le
    modèle connaît l'intitulé du montant."""
    modeles = modeles if modeles is not None else charger_modeles()
    if not modeles:
        return None
    empreinte = _empreinte(texte)
    meilleur = max(modeles, key=lambda m: _ressemblance(set(m["empreinte"]), empreinte))
    if _ressemblance(set(meilleur["empreinte"]), empreinte) < SEUIL_MODELE:
        return None
    valeurs = {nom: _valeur_apres(texte, ch["etiquette"], ch["rang"]) for nom, ch in meilleur["champs"].items()}
    trouves = isins(texte)
    if not (trouves and valeurs.get("quantite") and valeurs.get("cours")):
        return None
    q, p, montant = valeurs["quantite"], valeurs["cours"], valeurs.get("montant")
    if montant and abs(q * p - montant) > 0.01 * montant + 0.011 and \
            abs(q * p + (valeurs.get("frais") or 0) - montant) > 0.011 and \
            abs(q * p - (valeurs.get("frais") or 0) - montant) > 0.011:
        return None
    date = None
    if meilleur.get("date"):
        for d in dates(texte):
            if _mots_avant(d[3]) == meilleur["date"]:
                date = d[0]
                break
    date = date or date_execution(texte)
    isin = trouves[0][0]
    sens = _sens(texte, isin)
    if not sens:
        code = MOTIF_CODE_SENS.search(texte)
        sens = meilleur.get("sens", {}).get(code.group(2).lower()) if code else meilleur.get("type")
        if not sens:
            return None                          # code de sens jamais vu : on redemande
    return {"date": date, "sens": sens, "isin": isin, "libelle": _libelle(texte, isin)[:60], "quantite": q,
            "cours": p, "devise": _devise(texte, None), "frais": valeurs.get("frais"),
            "montant": montant or round(q * p, 2), "sur": bool(date), "net": None, "alternatives": []}


# ----------------------------------------------------------------------
# 8. Position des mots : intitulés au-dessus des valeurs (colonnes sans traits de tableau)
# ----------------------------------------------------------------------
def _cellules(mots, ecart=7.0):
    """Mots d'une ligne -> cellules (mots proches regroupés) : [(x0, x1, texte)]."""
    cellules = []
    for m in sorted(mots, key=lambda m: m["x0"]):
        if cellules and m["x0"] - cellules[-1][1] <= ecart:
            x0, _, texte = cellules[-1]
            cellules[-1] = (x0, m["x1"], texte + " " + m["text"])
        else:
            cellules.append((m["x0"], m["x1"], m["text"]))
    return cellules


def texte_par_colonnes(mots):
    """À partir des mots d'une page et de leur position (pdfplumber.extract_words), écrit
    « intitulé : valeur » pour chaque valeur placée sous un intitulé : une ligne d'intitulés
    sans chiffres, suivie d'une ligne de valeurs alignées dessous. Ces lignes s'ajoutent au
    texte de la page pour la lecture par intitulés et par le contenu."""
    lignes = []
    for m in sorted(mots or [], key=lambda m: (round(m["top"]), m["x0"])):
        if lignes and abs(lignes[-1][0] - m["top"]) <= 3:
            lignes[-1][1].append(m)
        else:
            lignes.append([m["top"], [m]])
    paires = []
    for (_, haut), (_, bas) in zip(lignes, lignes[1:]):
        intitules, valeurs = _cellules(haut), _cellules(bas)
        if len(intitules) < 2 or len(valeurs) < 2 or any(re.search(r"\d", c[2]) for c in intitules):
            continue
        if not any(re.search(r"\d", c[2]) for c in valeurs):
            continue
        for x0, x1, valeur in valeurs:
            centre = (x0 + x1) / 2
            # l'intitulé qui recouvre le plus la valeur, sinon le plus proche à gauche
            recouvrement = [(min(x1, b) - max(x0, a), texte) for a, b, texte in intitules]
            meilleur = max(recouvrement)
            if meilleur[0] <= 0:
                gauche = [(centre - a, texte) for a, b, texte in intitules if a <= centre]
                if not gauche:
                    continue
                meilleur = (0, min(gauche)[1])
            paires.append(f"{meilleur[1]} : {valeur}")
    return "\n".join(paires)


# ----------------------------------------------------------------------
# 9. Contrôles après lecture
# ----------------------------------------------------------------------
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def controles(tableau_avis, transactions):
    """Points à vérifier après la lecture d'un PDF : liste de {"texte": modèle de phrase,
    "valeurs": {...}} (traduits à l'affichage).

    tableau_avis : lignes lues (colonnes import_fichier.COLONNES_AVIS), avec le montant écrit ;
    transactions : opérations obtenues (date, type, ticker, quantite, prix, frais)."""
    messages = []
    # 1. montant écrit = quantité × cours ± frais (à 1 % près)
    if tableau_avis is not None and "Montant" in getattr(tableau_avis, "columns", []):
        for _, l in tableau_avis.iterrows():
            q, c, f, m = imp.convertir_nombres(pd.Series([l.get("Quantité"), l.get("Cours"), l.get("Frais") or "0",
                                                          l.get("Montant")]))
            if any(v != v for v in (q, c, m)) or imp.classer_type(l.get("Sens", "")) == "DIVIDENDE":
                continue
            f = 0.0 if f != f else f
            brut = abs(q) * c
            if min(abs(m - brut), abs(m - brut - f), abs(m - brut + f)) > 0.01 * max(brut, 1) + 0.02:
                messages.append({"texte": "{isin} : le montant écrit ({montant}) ne correspond pas à quantité × cours "
                                          "± frais ({calcul}) : vérifiez la quantité et le cours.",
                                 "valeurs": {"isin": l.get("ISIN", ""), "montant": f"{m:.2f}",
                                             "calcul": f"{brut:.2f}"}})
    if transactions is None or transactions.empty:
        return messages
    for _, l in transactions.iterrows():
        date = pd.Timestamp(l["date"])
        # 2. jour sans bourse (samedi, dimanche) : souvent la date d'édition prise pour l'exécution
        if date.weekday() >= 5 and l["type"] in ("ACHAT", "VENTE"):
            messages.append({"texte": "{ticker} : opération datée d'un {jour} ({date}), jour sans bourse : vérifiez "
                                      "la date d'exécution.",
                             "valeurs": {"ticker": l["ticker"], "jour": JOURS[date.weekday()],
                                         "date": date.strftime("%d/%m/%Y")}})
        # 3. frais inhabituels (plus de 3 % du montant)
        brut = abs(l["quantite"]) * l["prix"]
        if l["type"] in ("ACHAT", "VENTE") and brut > 0 and l["frais"] > 0.03 * brut:
            messages.append({"texte": "{ticker} : frais de {frais} pour un montant de {montant} (plus de 3 %) : "
                                      "vérifiez les frais.",
                             "valeurs": {"ticker": l["ticker"], "frais": f"{l['frais']:.2f}", "montant": f"{brut:.2f}"}})
    # 4. même opération deux fois (plusieurs PDF, ou un avis en double dans le même fichier)
    cles = transactions[["date", "type", "ticker", "quantite", "prix"]].astype(str).agg("|".join, axis=1)
    for cle in cles[cles.duplicated()].unique():
        ticker, date = cle.split("|")[2], pd.Timestamp(cle.split("|")[0]).strftime("%d/%m/%Y")
        messages.append({"texte": "{ticker} : la même opération apparaît deux fois ({date}) : avis envoyé en double ?",
                         "valeurs": {"ticker": ticker, "date": date}})
    return messages


# ----------------------------------------------------------------------
# 10. Rapport anonymisé : pour envoyer un PDF mal lu sans données personnelles
# ----------------------------------------------------------------------
MOTS_PERSONNELS = re.compile(r"\b(?:m\.|mme|mlle|monsieur|madame|mademoiselle|mr|mrs|ms|titulaire|client|"
                             r"cliente|adresse|address|n[ée]e?\s+le|nom|name|holder)\b", re.IGNORECASE)


MOTIF_RUE = re.compile(r"\b\d{1,4}\s*(?:bis|ter)?,?\s+(?:rue|avenue|av\.|boulevard|bd|place|chemin|all[ée]e|impasse|"
                       r"route|quai|square|street|road|lieu-dit|r[ée]sidence)\b", re.IGNORECASE)


def anonymiser(texte):
    """Texte sans données personnelles : lignes de nom et d'adresse, adresses électroniques,
    IBAN, téléphones, codes postaux et numéros de compte ou de référence sont masqués.
    Restent : codes ISIN, dates, montants et intitulés, qui suffisent à corriger la lecture."""
    lignes = []
    for ligne in (texte or "").split("\n"):
        if MOTS_PERSONNELS.search(ligne) or re.search(r"\b\d{5}\s+[A-ZÉÈ][A-Za-zÉÈéèêëàâîïôûüç\- ]{2,}$", ligne) \
                or MOTIF_RUE.search(ligne):
            lignes.append("[ligne masquée : nom ou adresse]")
            continue
        ligne = re.sub(r"[\w.+\-]+@[\w\-]+\.[\w.]+", "[e-mail]", ligne)
        ligne = re.sub(r"\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){3,7}(?:\s?[A-Z0-9]{1,4})?\b",
                       lambda m: m.group(0) if imp.isin_plausible(m.group(0).replace(" ", "")) else "[IBAN]", ligne)
        ligne = re.sub(r"(?:\+33\s?|\b0)[1-9](?:[\s.\-]?\d{2}){4}\b", "[téléphone]", ligne)
        if LIGNES_SANS_MONTANT.search(ligne):
            ligne = re.sub(r"\d[\d\s\-/.]{3,}\d|\d{4,}", "[numéro]", ligne)
        else:
            # longues suites de chiffres sans virgule (numéros), en gardant les ISIN, dates et montants
            ligne = re.sub(r"(?<![A-Z0-9])\d{7,}(?![,.]\d)", "[numéro]", ligne)
        lignes.append(ligne)
    return "\n".join(lignes)


def rapport_anonymise(textes, resultat=None, nom_fichier=""):
    """Texte à envoyer au créateur du logiciel pour améliorer la lecture d'un PDF."""
    texte = anonymiser("\n".join(textes))
    c = candidats([texte])
    lignes = ["Portfolio Tracker — rapport de lecture d'un PDF (anonymisé)",
              f"Fichier : {re.sub(r'[^A-Za-z0-9._ -]', '_', nom_fichier)}",
              f"Texte « codé » : {'oui' if texte_illisible(chr(10).join(textes)) else 'non'}",
              f"Codes ISIN : {[i for i, _ in c['isins']]}",
              f"Dates : {c['dates']} · date proposée : {c['date_proposee']}",
              f"Proposition : {c['proposition']}"]
    if resultat:
        lignes.append(f"Saisie de l'utilisateur : {resultat}")
    lignes += ["", "=== Texte lu (anonymisé) ===", texte]
    return "\n".join(lignes)


# ----------------------------------------------------------------------
# 11. Relevé de portefeuille (positions et prix de revient) : un portefeuille de départ
# ----------------------------------------------------------------------
MOTS_RELEVE_POSITIONS = re.compile(
    r"relev[ée]\s*(?:de|du)\s*(?:portefeuille|compte[\s-]*titres|titres|positions)|portefeuille\s*titres|"
    r"[ée]tat\s*(?:du|de)\s*portefeuille|valorisation\s*(?:du|de)\s*portefeuille|inventaire\s*(?:du|de)\s*portefeuille|"
    r"estimation\s*(?:du|de)\s*portefeuille|portfolio\s*(?:statement|valuation)|statement\s*of\s*holdings|"
    r"positions\s*(?:au|as\s*of)", re.IGNORECASE)
MOTS_DATE_RELEVE = re.compile(r"(?:\bau|arr[êe]t[ée]\s*au|as\s*of|valoris\w*|situation|en\s*date\s*du|date)\s*:?\s*$",
                              re.IGNORECASE)


def est_un_releve_de_positions(texte):
    return bool(MOTS_RELEVE_POSITIONS.search(texte or "")) and len({c for c, _ in isins(texte)}) >= 1


def lire_releve_positions(texte):
    """Positions d'un relevé de portefeuille : pour chaque ISIN, quantité × cours = valorisation
    (au centime près) et le prix de revient unitaire (PRU) : le nombre restant de la ligne le plus
    proche du cours, confirmé si quantité × (cours − PRU) = plus-value écrite. Renvoie une liste
    de dict (date du relevé, isin, libelle, quantite, cours, pru, devise) ou [] si une ligne n'est
    pas sûre."""
    if not est_un_releve_de_positions(texte):
        return []
    toutes = dates(texte)
    date = next((d[0] for d in toutes if MOTS_DATE_RELEVE.search(d[3])), toutes[0][0] if toutes else None)
    positions = []
    for isin, segment, _ in _segments(texte):
        if not isin:
            continue
        ligne = next((l for l in segment.splitlines() if isin in l), segment)
        meilleurs = trios(ligne) or trios(segment)
        if not meilleurs:
            return []
        t = meilleurs[0]
        q, cours = t["quantite"], t["cours"]
        utilises = [q, cours, t["brut"]] if t["brut"] else [q, cours]
        restants = [c for c in nombres(ligne) if not any(_se_chevauchent(c, u) for u in utilises if u)]
        pru = None
        etiquete = [c for c in restants if MOTS_PRU.search(_contexte(ligne, c, 30))]
        if etiquete:
            pru = etiquete[0]["valeur"]
        else:
            proches = [c for c in restants if cours["valeur"] / 3 <= c["valeur"] <= cours["valeur"] * 3]
            # confirmation : la plus-value latente écrite = quantité × (cours − PRU)
            for c in proches:
                plus_value = abs(q["valeur"] * (cours["valeur"] - c["valeur"]))
                if any(abs(r["valeur"] - plus_value) < 0.02 for r in restants if r is not c):
                    pru = c["valeur"]
                    break
            if pru is None and proches:
                pru = min(proches, key=lambda c: abs(c["valeur"] - cours["valeur"]))["valeur"]
        positions.append({"date": date, "isin": isin, "libelle": _libelle(ligne, isin)[:60],
                          "quantite": float(q["valeur"]), "cours": float(cours["valeur"]),
                          "pru": float(pru) if pru else None, "devise": _devise(ligne, cours)})
    return positions


MOTS_PRU = re.compile(r"pru|prix\s*de\s*revient|prix\s*moyen|\bpam\b|cost\s*(?:price|basis)|average\s*(?:cost|price)",
                      re.IGNORECASE)


def positions_en_lignes_avis(positions):
    """Chaque position devient un achat au PRU (à défaut au cours), à la date du relevé."""
    def nombre(x):
        return f"{x:.6f}".rstrip("0").rstrip(".")
    return [[p["date"] or "", "ACHAT", p["isin"], p["libelle"] or p["isin"], nombre(p["quantite"]),
             nombre(p["pru"] or p["cours"]), p["devise"] or "", "", nombre(p["quantite"] * (p["pru"] or p["cours"]))]
            for p in positions]


# ----------------------------------------------------------------------
# 12. Opérations sur titres : division (split) ou regroupement d'actions
# ----------------------------------------------------------------------
MOTS_DIVISION = re.compile(r"division\s*(?:du\s*nominal|d['’]\s*actions?|des\s*actions)?|\bsplit\b|fractionnement",
                           re.IGNORECASE)
MOTS_REGROUPEMENT = re.compile(r"regroupement|reverse\s*split|consolidation\s*d", re.IGNORECASE)
MOTIF_DIVISE_PAR = re.compile(r"divis[ée]e?s?\s*par\s*(\d+)", re.IGNORECASE)
MOTIF_PARITE = re.compile(r"(?:parit[ée]|ratio|rapport\s*d['’]\s*[ée]change)?\s*:?\s*(\d+)\s*(?:actions?|titres?|shares?)?"
                          r"\s*(?:anciennes?|old|existantes?)?\s*(?:pour|contre|for|:|→|->)\s*(\d+)\s*"
                          r"(?:actions?|titres?|shares?)?\s*(?:nouvelles?|new)", re.IGNORECASE)
MOTIF_PARITE_SIMPLE = re.compile(r"(?:parit[ée]|ratio)\s*:?\s*(\d+)\s*(?:pour|:|/|for)\s*(\d+)", re.IGNORECASE)
MOTS_DATE_EFFET = re.compile(r"(?:effet|ex[\s-]*date|d[ée]tachement|[àa]\s*compter\s*du|effective|r[ée]alis[ée]e?\s*le|"
                             r"date\s*de\s*l['’]\s*op[ée]ration)[^\n\d]{0,25}$", re.IGNORECASE)


def lire_ost(texte):
    """Avis de division ou de regroupement d'actions : dict(nature, isin, libelle, date,
    facteur) — facteur = nombre de titres nouveaux pour 1 ancien (4 pour une division par 4,
    0,1 pour un regroupement de 10 en 1) — ou None."""
    division, regroupement = MOTS_DIVISION.search(texte or ""), MOTS_REGROUPEMENT.search(texte or "")
    trouves = isins(texte or "")
    if not (division or regroupement) or not trouves:
        return None
    facteur = None
    m = MOTIF_DIVISE_PAR.search(texte)
    if m and int(m.group(1)) > 1:
        facteur = float(m.group(1)) if division else 1 / float(m.group(1))
    else:
        m = MOTIF_PARITE.search(texte) or MOTIF_PARITE_SIMPLE.search(texte)
        if m:
            a, b = float(m.group(1)), float(m.group(2))
            if a > 0 and b > 0 and a != b:
                # « 1 ancienne pour 4 nouvelles » (division) ; « 10 anciennes pour 1 nouvelle » (regroupement)
                facteur = b / a if MOTIF_PARITE.search(texte) else (max(a, b) / min(a, b) if division
                                                                     else min(a, b) / max(a, b))
    if not facteur or facteur == 1:
        return None
    toutes = dates(texte)
    date = next((d[0] for d in toutes if MOTS_DATE_EFFET.search(d[3])), None) or date_execution(texte)
    isin = trouves[0][0]
    ligne = next((l for l in texte.splitlines() if isin in l), "")
    avant = MOTS_REGROUPEMENT.sub(" ", MOTS_DIVISION.sub(" ", ligne.split(isin)[0]))
    avant = re.sub(r"\b(?:d['’]\s*actions?|isin|code|valeur|titre)\b\s*:?", " ", avant, flags=re.IGNORECASE)
    libelle = " ".join(avant.split()[-4:]).strip(" :-(") or _libelle(texte, isin)
    return {"nature": "division" if facteur > 1 else "regroupement", "isin": isin,
            "libelle": libelle[:60], "date": date, "facteur": facteur}
