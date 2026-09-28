"""
import_fichier.py — Importer un fichier de transactions dans (presque) n'importe quel format.

Un fichier exporté par une banque ou un courtier ne ressemble pas au format du
projet : colonnes nommées autrement, lignes de titre avant le tableau, codes
ISIN au lieu des tickers, montant total au lieu du prix unitaire, ventes
notées avec une quantité négative... Ce module traite ces cas en 4 étapes :

    1. lire_tableau_brut()        : lire le fichier tel quel (CSV ou Excel),
                                    trouver la ligne des titres de colonnes ;
    2. proposer_correspondance()  : deviner quelle colonne est la date, la
                                    quantité, le prix... (l'utilisateur peut corriger) ;
    3. appliquer_correspondance() : produire le tableau standard du projet
                                    (date, type, ticker, nom, quantite, prix, frais) ;
    4. resoudre_identifiants()    : trouver le ticker Yahoo Finance d'un code ISIN
                                    ou d'un nom de société ;
    5. harmoniser_devises()       : vérifier chaque prix avec le vrai cours du jour
                                    et le reconvertir dans la devise du titre si le
                                    fichier donne des montants en euros.

La correspondance des colonnes s'appuie sur leur NOM quand il est parlant, mais
aussi sur leur CONTENU (des dates, des codes ISIN, des nombres entiers...) et sur
la COHÉRENCE des chiffres (quantité × prix ± frais = montant) : un fichier sans
titres de colonnes ou aux colonnes mal nommées est donc compris quand même.
importer_automatiquement() enchaîne toutes les étapes et dit si le résultat est sûr.

Les étapes 1 à 3 n'ont besoin d'aucune connexion ; les étapes 4 et 5 interrogent
Yahoo Finance.
"""

import itertools
import math

import csv
import io
import re
import unicodedata

import pandas as pd

COLONNES = ["date", "type", "ticker", "nom", "quantite", "prix", "frais"]

# Champs que l'utilisateur fait correspondre à une colonne de son fichier
# (clé interne : libellé affiché). "identifiant" = ticker, code ISIN ou nom du titre.
CHAMPS = {
    "date": "Date de l'opération",
    "type": "Type d'opération",
    "identifiant": "Titre (ticker, ISIN ou nom)",
    "nom": "Nom du titre",
    "quantite": "Quantité",
    "prix": "Prix unitaire",
    "montant": "Montant total",
    "frais": "Frais",
    "devise": "Devise",
}
OBLIGATOIRES = ["date", "identifiant", "quantite"]          # + prix OU montant

# Noms de colonnes reconnus pour chaque champ (sans accents, en minuscules).
# L'ordre compte : le premier nom trouvé l'emporte.
NOMS_RECONNUS = {
    "date": ["date", "date operation", "date d'operation", "date de l'operation", "date execution",
             "date d'execution", "date de valeur", "date valeur", "trade date", "transaction date",
             "execution date", "jour"],
    "type": ["type", "type d'operation", "type operation", "operation", "sens", "nature",
             "nature de l'operation", "transaction type", "side", "action", "mouvement"],
    "identifiant": ["ticker", "symbole", "symbol", "code", "isin", "code isin", "isin code",
                    "valeur", "titre", "instrument", "produit", "product", "security", "libelle valeur"],
    "nom": ["nom", "name", "libelle", "designation", "nom du titre", "security name", "description",
            "produit", "product", "titre", "valeur"],
    "quantite": ["quantite", "qte", "qty", "quantity", "nombre", "nombre de titres", "nb titres",
                 "nb de titres", "parts", "shares", "units"],
    "prix": ["prix", "prix unitaire", "cours", "cours d'execution", "cours execute", "price",
             "unit price", "execution price", "prix d'execution"],
    "montant": ["montant", "montant net", "montant brut", "montant total", "total", "amount",
                "net amount", "valeur totale", "montant en eur", "montant eur", "total eur"],
    "frais": ["frais", "frais de courtage", "courtage", "commission", "commissions", "fees", "fee",
              "frais totaux"],
    "devise": ["devise", "currency", "monnaie", "devise de cotation", "ccy", "cur"],
}
# Colonnes à ne jamais interpréter (notes libres)
NOMS_EXCLUS = {"commentaire", "commentaires", "remarque", "remarques", "note", "notes", "observation",
               "observations", "comment", "comments", "memo", "info", "infos", "information"}
DEVISES = {"EUR", "USD", "GBP", "GBX", "CHF", "JPY", "CAD", "AUD", "HKD", "DKK", "SEK", "NOK", "CNY", "SGD"}
MOTIF_DATE = re.compile(r"^\d{1,4}[/\-.]\d{1,2}[/\-.]\d{1,4}")

# Types d'opération reconnus (mots-clés, sans accents, en minuscules)
MOTS_TYPES = {
    "ACHAT": ["achat", "buy", "bought", "purchase", "souscription", "acquisition", "achete"],
    "VENTE": ["vente", "sell", "sold", "sale", "cession", "vendu", "rachat"],
    "DIVIDENDE": ["dividende", "dividend", "coupon", "distribution", "detachement", "revenu"],
}
IGNORER = "IGNORER"
TYPES_POSSIBLES = ["ACHAT", "VENTE", "DIVIDENDE", IGNORER]

MOTIF_ISIN = re.compile(r"^[A-Z]{2}[A-Z0-9]{9}[0-9]$")
MOTIF_TICKER = re.compile(r"^[A-Z0-9^][A-Z0-9\-=&]{0,11}(\.[A-Z]{1,3})?$")

# Place de cotation préférée selon le pays de l'ISIN (suffixe Yahoo Finance)
SUFFIXE_PAR_PAYS = {
    "FR": [".PA"], "DE": [".DE", ".F"], "NL": [".AS"], "BE": [".BR"], "ES": [".MC"], "IT": [".MI"],
    "PT": [".LS"], "GB": [".L"], "CH": [".SW"], "US": [""], "JP": [".T"], "CA": [".TO"],
    "AU": [".AX"], "DK": [".CO"], "SE": [".ST"], "FI": [".HE"], "NO": [".OL"], "HK": [".HK"],
    "AT": [".VI"], "IE": [".PA", ".DE", ".AS", ".MI", ".L", ""], "LU": [".PA", ".DE", ".AS", ".MI", ".L", ""],
}


# ======================================================================
# Outils
# ======================================================================
def isin_valide(code):
    """Vrai si le code est un ISIN correct : format ET clé de contrôle (algorithme de Luhn).
    Ex. FR0000121014 (LVMH) -> vrai ; FR0000121015 -> faux (dernier chiffre erroné)."""
    code = str(code).strip().upper()
    if not MOTIF_ISIN.match(code):
        return False
    chiffres = "".join(str(int(c, 36)) for c in code[:-1])     # lettres : A = 10 ... Z = 35
    total = 0
    for i, c in enumerate(reversed(chiffres)):
        n = int(c) * (2 if i % 2 == 0 else 1)
        total += n - 9 if n > 9 else n
    return (10 - total % 10) % 10 == int(code[-1])

def normaliser(texte):
    """'  Quantité ' -> 'quantite' (sans accents, minuscules, espaces simples)."""
    texte = "".join(c for c in unicodedata.normalize("NFKD", str(texte)) if not unicodedata.combining(c))
    texte = texte.replace("﻿", "").replace("_", " ").replace("’", "'").strip().strip('"').lower()
    return re.sub(r"\s+", " ", texte)


def convertir_nombres(serie):
    """'1 234,50 €', '1.234,50', '1,234.50', '(12,5)' -> nombres. Cases vides -> NaN."""
    def un(valeur):
        if valeur is None or (isinstance(valeur, float) and pd.isna(valeur)):
            return float("nan")
        texte = str(valeur).strip()
        for caractere in [" ", " ", " ", "€", "$", "£", "EUR", "USD", "'"]:
            texte = texte.replace(caractere, "")
        if texte in ("", "-", "nan", "None"):
            return float("nan")
        negatif = texte.startswith("(") and texte.endswith(")")
        texte = texte.strip("()")
        if texte.endswith("-"):                          # "12,50-" (certains relevés)
            negatif, texte = True, texte[:-1]
        if "," in texte and "." in texte:                # le dernier séparateur est le décimal
            if texte.rfind(",") > texte.rfind("."):
                texte = texte.replace(".", "").replace(",", ".")
            else:
                texte = texte.replace(",", "")
        elif "," in texte:
            texte = texte.replace(",", ".") if texte.count(",") == 1 else texte.replace(",", "")
        elif texte.count(".") > 1:                       # "1.234.567"
            texte = texte.replace(".", "")
        try:
            nombre = float(texte)
        except ValueError:
            return float("nan")
        return -nombre if negatif else nombre
    return serie.map(un).astype(float)


def ordre_des_dates(serie):
    """Pour des dates écrites 03/04/2024 : jour d'abord (France) ou mois d'abord (États-Unis) ?
    Une seule date dont le premier nombre dépasse 12 (13/04) tranche pour "jour" ;
    une date dont le deuxième dépasse 12 (04/13) tranche pour "mois".
    Renvoie ("jour" ou "mois", ambigu : vrai si aucune date ne permet de trancher)."""
    parties = serie.astype(str).str.strip().str.extract(r"^(\d{1,2})[/\-.](\d{1,2})[/\-.]\d{2,4}")
    parties = parties.dropna().astype(int)
    if parties.empty:
        return "jour", False
    if (parties[0] > 12).any():
        return "jour", False
    if (parties[1] > 12).any():
        return "mois", False
    return "jour", bool((parties[0] != parties[1]).any())


def convertir_dates(serie, ordre=None):
    """'2024-01-15', '15/01/2024', '01/15/2024', '15.01.2024', '2024-01-15 00:00:00' -> dates.
    L'ordre jour/mois est déduit de l'ensemble de la colonne. Illisible -> NaT."""
    ordre = ordre or ordre_des_dates(serie)[0]
    texte = serie.astype(str).str.strip().str.replace(".", "/", regex=False).str.replace("T", " ", regex=False)
    iso = pd.to_datetime(texte.str[:10], format="%Y-%m-%d", errors="coerce")
    reste = iso.isna() & serie.notna()
    if reste.any():
        iso[reste] = pd.to_datetime(texte[reste].str.split(" ").str[0], dayfirst=(ordre == "jour"),
                                    errors="coerce")
    return iso.astype("datetime64[ns]")


# ======================================================================
# 1. Lecture brute
# ======================================================================
def _texte(brut):
    try:
        return brut.decode("utf-8-sig")
    except UnicodeDecodeError:
        return brut.decode("cp1252")


def _lignes_csv(texte):
    """Découpe un texte CSV en lignes de cellules, quel que soit le séparateur."""
    lignes = []
    for ligne in texte.splitlines():
        ligne = ligne.strip()
        # Ligne entière entre guillemets (tout était dans la colonne A d'Excel)
        if len(ligne) > 1 and ligne[0] == ligne[-1] == '"' and ligne.count('"') % 2 == 0 \
                and '","' not in ligne and '";"' not in ligne:
            ligne = ligne[1:-1].replace('""', '"')
        lignes.append(ligne)
    echantillon = [l for l in lignes if l][:40]
    separateur = max([";", ",", "\t", "|"], key=lambda s: sum(l.count(s) for l in echantillon))
    return [ligne for ligne in csv.reader(lignes, delimiter=separateur)], separateur


def feuilles_excel(brut):
    """Noms des feuilles d'un fichier Excel (liste vide pour un CSV)."""
    if brut[:2] != b"PK":
        return []
    return list(pd.ExcelFile(io.BytesIO(brut)).sheet_names)


def meilleure_feuille(brut):
    """La feuille Excel qui contient le plus de cellules remplies (le tableau des
    opérations plutôt qu'une feuille de notes). None pour un CSV."""
    feuilles = feuilles_excel(brut)
    if len(feuilles) <= 1:
        return feuilles[0] if feuilles else None
    toutes = pd.read_excel(io.BytesIO(brut), sheet_name=None, header=None, dtype=object)
    return max(feuilles, key=lambda f: int(toutes[f].notna().sum().sum()))


def _grille(brut, feuille=None):
    """Toutes les cellules du fichier, sous forme de liste de lignes (textes)."""
    if brut[:2] == b"PK":                                # .xlsx = archive ZIP
        try:
            feuille = feuille if feuille is not None else meilleure_feuille(brut)
            tableau = pd.read_excel(io.BytesIO(brut), sheet_name=feuille, header=None, dtype=object)
        except ImportError:
            raise ValueError("Pour lire un fichier Excel (.xlsx), installer openpyxl : "
                             "python -m pip install openpyxl. Ou l'enregistrer au format CSV.")
        grille = [["" if pd.isna(v) else str(v) for v in ligne] for ligne in tableau.itertuples(index=False)]
        return grille, "excel"
    return _lignes_csv(_texte(brut))


def detecter_ligne_entete(grille, limite=30):
    """Numéro (à partir de 0) de la ligne qui contient les titres de colonnes :
    parmi les premières lignes, la plus remplie qui contient surtout du texte."""
    meilleure, score_max = 0, -1
    for i, ligne in enumerate(grille[:limite]):
        cellules = [c.strip() for c in ligne if str(c).strip()]
        if len(cellules) < 2:
            continue
        textes = sum(1 for c in cellules if pd.isna(convertir_nombres(pd.Series([c]))[0]))
        if textes < len(cellules) * 0.6:
            continue                                     # plutôt une ligne de données
        if len(cellules) > score_max:
            meilleure, score_max = i, len(cellules)
    return meilleure


def _ressemble_a_des_donnees(ligne):
    """Une ligne qui contient une date ou un code ISIN n'est pas une ligne de titres."""
    return any(MOTIF_DATE.match(str(c).strip()) or isin_valide(c) for c in ligne)


def lire_tableau_brut(brut, feuille=None, ligne_entete=None):
    """Lit le fichier sans rien interpréter. Renvoie (tableau de textes, ligne d'en-tête utilisée).
    ligne_entete = -1 : le fichier n'a pas de ligne de titres (colonnes "Colonne 1", "Colonne 2"...)."""
    grille, _ = _grille(brut, feuille)
    if not any(any(str(c).strip() for c in ligne) for ligne in grille):
        raise ValueError("Le fichier est vide.")
    if ligne_entete is None:
        ligne_entete = detecter_ligne_entete(grille)
        premiere = next(i for i, l in enumerate(grille) if any(str(c).strip() for c in l))
        if _ressemble_a_des_donnees(grille[ligne_entete]) or \
                (ligne_entete == 0 and _ressemble_a_des_donnees(grille[premiere])):
            ligne_entete = -1
    if ligne_entete < 0:
        largeur = max(len(l) for l in grille)
        grille = [[f"Colonne {j + 1}" for j in range(largeur)]] + grille
        ligne_entete_effective = 0
    else:
        ligne_entete_effective = min(ligne_entete, len(grille) - 1)
    entete = [str(c).strip() or f"Colonne {j + 1}" for j, c in enumerate(grille[ligne_entete_effective])]
    vus = {}
    for j, nom in enumerate(entete):                     # noms en double : "Montant", "Montant (2)"
        vus[nom] = vus.get(nom, 0) + 1
        if vus[nom] > 1:
            entete[j] = f"{nom} ({vus[nom]})"
    largeur = len(entete)
    donnees = [(list(l) + [""] * largeur)[:largeur] for l in grille[ligne_entete_effective + 1:]]
    tableau = pd.DataFrame(donnees, columns=entete, dtype=object)
    tableau = _garder_le_bloc_principal(tableau)
    tableau = tableau[tableau.apply(lambda l: any(str(v).strip() for v in l), axis=1)]
    return tableau.reset_index(drop=True), ligne_entete


def _garder_le_bloc_principal(tableau):
    """Si la feuille contient un autre petit tableau à côté (résumé, notes), séparé
    par une colonne entièrement vide, on ne garde que le bloc le plus rempli."""
    remplies = tableau.apply(lambda c: c.astype(str).str.strip().ne("").sum())
    vides = [i for i, n in enumerate(remplies) if n == 0 and str(tableau.columns[i]).startswith("Colonne ")]
    if not vides:
        return tableau
    blocs, debut = [], 0
    for i in vides + [len(tableau.columns)]:
        if i > debut:
            blocs.append(list(range(debut, i)))
        debut = i + 1
    principal = max(blocs, key=lambda b: int(remplies.iloc[b].sum()))
    return tableau.iloc[:, principal]


# ======================================================================
# 2. Correspondance des colonnes
# ======================================================================
def _score_nom(nom_colonne, champ):
    """4 si le nom de la colonne est un nom reconnu pour ce champ, 3 s'il commence par lui, sinon 0."""
    n = normaliser(nom_colonne)
    for nom in NOMS_RECONNUS[champ]:
        if n == nom:
            return 4.0
    for nom in NOMS_RECONNUS[champ]:
        if n.startswith(nom + " "):
            return 3.0
    return 0.0


def profil_colonne(serie):
    """Ce que contient une colonne : part de dates, d'ISIN, de nombres, d'entiers..."""
    valeurs = serie.astype(str).str.strip()
    valeurs = valeurs[(valeurs != "") & (valeurs.str.lower() != "nan")]
    if valeurs.empty:
        return {"vide": True}
    nombres = convertir_nombres(valeurs)
    part = lambda masque: float(masque.mean()) if len(masque) else 0.0
    majuscules = valeurs.str.upper()
    avec_date = valeurs.str.match(MOTIF_DATE.pattern)
    dates = convertir_dates(valeurs[avec_date]) if avec_date.any() else pd.Series(dtype="datetime64[ns]")
    types = valeurs.map(classer_type) != IGNORER
    devises = majuscules.isin(DEVISES)
    tickers = majuscules.str.match(MOTIF_TICKER.pattern) & nombres.isna() & ~types & ~devises
    return {
        "vide": False,
        "remplissage": len(valeurs) / max(len(serie), 1),
        "dates": part(dates.notna()) * part(avec_date),
        "isin": part(valeurs.map(isin_valide)),
        "tickers": part(tickers),
        "types": part(types),
        "devises": part(devises),
        "nombres": part(nombres.notna()),
        "entiers": part((nombres.dropna() % 1 == 0)),
        "moyenne": float(nombres.abs().mean()) if nombres.notna().any() else 0.0,
        "distincts": valeurs.nunique() / len(valeurs),
        "longueur": float(valeurs.str.len().mean()),
    }


def _score_contenu(p, champ):
    """Vraisemblance (0 à 5) qu'une colonne de profil p corresponde au champ, d'après son contenu."""
    if p.get("vide"):
        return 0.0
    texte = (1 - p["nombres"]) * (1 - p["dates"])
    if champ == "date":
        return 5 * p["dates"]
    if champ == "identifiant":
        return 6 * p["isin"] + 3 * p["tickers"] * texte
    if champ == "type":
        return 5 * p["types"] * (1 if p["distincts"] < 0.5 else 0.5)
    if champ == "devise":
        return 5 * p["devises"]
    if champ == "nom":
        return (3 * texte * (1 - p["isin"]) * (1 - p["types"]) * (1 - p["devises"])
                * (1 - 0.4 * p["tickers"]) * min(1, p["longueur"] / 6) * p["remplissage"])
    return 0.0


def _coherence(tableau, q, prix, montant, frais):
    """Part des lignes où quantité × prix ± frais ≈ montant (écart < 1 %)."""
    Q = convertir_nombres(tableau[q]).abs()
    P = convertir_nombres(tableau[prix]).abs()
    M = convertir_nombres(tableau[montant]).abs()
    F = convertir_nombres(tableau[frais]).abs().fillna(0) if frais else 0.0
    valides = Q.notna() & P.notna() & M.notna() & (Q > 0) & (M > 0)
    if valides.sum() == 0:
        return 0.0
    brut = Q * P
    ok = ((brut - M).abs() <= 0.01 * M + 0.02) | ((brut + F - M).abs() <= 0.01 * M + 0.02) | \
         ((brut - F - M).abs() <= 0.01 * M + 0.02)
    return float(ok[valides].mean())


def proposer_correspondance(tableau_ou_colonnes):
    """Devine, pour chaque champ, la colonne du fichier qui lui correspond.

    - avec une simple liste de noms de colonnes : d'après les noms seulement ;
    - avec le tableau lu (lire_tableau_brut) : d'après les noms ET le contenu,
      puis la cohérence des nombres (quantité × prix ± frais = montant).

    Renvoie {champ: nom de colonne ou None}. Une colonne n'est utilisée qu'une fois.
    """
    if isinstance(tableau_ou_colonnes, pd.DataFrame):
        tableau = tableau_ou_colonnes
        colonnes = list(tableau.columns)
        profils = {c: profil_colonne(tableau[c]) for c in colonnes}
    else:
        tableau, colonnes, profils = None, list(tableau_ou_colonnes), None
    numeriques = ["quantite", "prix", "montant", "frais"]

    # 1. Les champs "texte" (date, titre, type, devise, nom) : nom de colonne + contenu
    candidats = []
    colonnes_utiles = [c for c in colonnes if normaliser(c) not in NOMS_EXCLUS]
    for champ in CHAMPS:
        for c in colonnes_utiles:
            nom = _score_nom(c, champ)
            if profils is None:
                score = nom
            elif champ in numeriques:
                p = profils[c]
                score = nom * (p.get("nombres", 0) >= 0.6) if not p.get("vide") else nom * 0.5
            else:
                p = profils[c]
                plausible = 1.0 if p.get("vide") else {
                    "date": p.get("dates", 0), "devise": p.get("devises", 0),
                    "type": 1.0,
                }.get(champ, 1 - p.get("nombres", 0))
                score = nom * max(plausible, 0.2) + _score_contenu(p, champ)
            if score >= 2:
                candidats.append((score, champ, c))
    proposition, prises = {champ: None for champ in CHAMPS}, set()
    for score, champ, c in sorted(candidats, key=lambda x: -x[0]):
        if proposition[champ] is None and c not in prises:
            proposition[champ] = c
            prises.add(c)
    if tableau is None:
        return proposition

    # 2. Les nombres sans nom parlant : on essaie les combinaisons et on garde
    #    celle où quantité × prix ± frais = montant tombe juste le plus souvent.
    restants = [f for f in numeriques if proposition[f] is None]
    libres = [c for c in colonnes_utiles if c not in prises and not profils[c].get("vide")
              and profils[c]["nombres"] >= 0.8 and profils[c]["dates"] < 0.5][:6]
    if restants and libres:
        meilleur, score_max = None, -math.inf
        for choix in itertools.product(libres + [None], repeat=len(restants)):
            utilises = [c for c in choix if c]
            if len(utilises) != len(set(utilises)):
                continue
            essai = dict(proposition, **dict(zip(restants, choix)))
            q, p_, m, f = (essai[k] for k in numeriques)
            score = 0.0
            if not q:
                score -= 5
            else:
                score += 2 * profils[q]["entiers"]
            if not p_ and not m:
                score -= 5
            if q and p_ and m:
                score += 6 * _coherence(tableau, q, p_, m, f)
            if f and (p_ or m):
                reference = profils[m]["moyenne"] if m else profils[p_]["moyenne"] * max(profils[q]["moyenne"] if q else 1, 1)
                score += 1 if profils[f]["moyenne"] < 0.05 * max(reference, 1e-9) else -2
            if q and p_ and not m and profils[p_]["entiers"] > profils[q]["entiers"]:
                score -= 1                               # le prix est rarement plus "entier" que la quantité
            score += 0.3 * len(utilises)
            if score > score_max:
                meilleur, score_max = dict(zip(restants, choix)), score
        proposition.update(meilleur or {})
    return proposition


def confiance(tableau, correspondance):
    """La correspondance est-elle assez sûre pour analyser sans demander ?
    Oui si les colonnes de nombres ont un nom parlant, ou si les chiffres sont cohérents."""
    q, p, m = (correspondance.get(k) for k in ("quantite", "prix", "montant"))
    if correspondance_complete(correspondance):
        return False
    noms_ok = _score_nom(q, "quantite") > 0 and ((p and _score_nom(p, "prix") > 0) or (m and _score_nom(m, "montant") > 0))
    coherent = bool(q and p and m and _coherence(tableau, q, p, m, correspondance.get("frais")) >= 0.8)
    date_ok = _score_nom(correspondance["date"], "date") > 0 or profil_colonne(tableau[correspondance["date"]]).get("dates", 0) >= 0.9
    return bool((noms_ok or coherent) and date_ok)


def classer_type(valeur):
    """'Achat Comptant' -> ACHAT, 'Coupons/Dividende' -> DIVIDENDE, 'Frais de garde' -> IGNORER."""
    texte = normaliser(valeur)
    for type_, mots in MOTS_TYPES.items():
        if any(re.search(rf"\b{mot}", texte) for mot in mots):
            return type_
    return IGNORER


def correspondance_complete(correspondance):
    """Liste des champs obligatoires qui ne sont pas encore associés à une colonne."""
    manquants = [c for c in OBLIGATOIRES if not correspondance.get(c)]
    if not correspondance.get("prix") and not correspondance.get("montant"):
        manquants.append("prix")
    return manquants


# ======================================================================
# 3. Application : production du tableau standard
# ======================================================================
def appliquer_correspondance(tableau, correspondance, types=None, identifiants=None,
                             montant_inclut_frais=True):
    """Transforme le tableau brut en transactions au format du projet.

    correspondance : {champ: colonne} (voir proposer_correspondance)
    types          : {valeur du fichier: ACHAT / VENTE / DIVIDENDE / IGNORER}
                     (par défaut : classer_type) ; sans colonne "type", le signe de
                     la quantité décide (négative = vente)
    identifiants   : {valeur du fichier: ticker Yahoo} (ISIN ou noms convertis)
    montant_inclut_frais : le montant total est-il net des frais ? (achat = quantité
                     × prix + frais ; vente = quantité × prix − frais)

    Renvoie (transactions, rapport) ; rapport = {"ignorees": n, "hors_tableau": n,
    "erreurs": [{"n", "motif", "lignes"}]}. Les lignes sans date ni titre (total, note sous le
    tableau...) sont écartées sans erreur ; les autres colonnes du fichier sont ignorées.
    """
    manquants = correspondance_complete(correspondance)
    if manquants:
        raise ValueError("Colonne(s) à indiquer : " + ", ".join(CHAMPS[m] for m in manquants))
    col = lambda champ: tableau[correspondance[champ]] if correspondance.get(champ) else None

    df = pd.DataFrame(index=tableau.index)
    df["date"] = convertir_dates(col("date"))
    if correspondance.get("devise"):
        df["devise_fichier"] = col("devise").astype(str).str.strip().str.upper().replace({"GBX": "GBP"})
    identifiant = col("identifiant").astype(str).str.strip()
    df["identifiant"] = identifiant
    df["ticker"] = identifiant.map(lambda x: (identifiants or {}).get(x, x)).str.strip().str.upper()
    df["nom"] = col("nom").astype(str).str.strip() if correspondance.get("nom") else identifiant
    quantite = convertir_nombres(col("quantite"))
    prix = convertir_nombres(col("prix")) if correspondance.get("prix") else None
    montant = convertir_nombres(col("montant")) if correspondance.get("montant") else None
    frais = convertir_nombres(col("frais")).abs().fillna(0.0) if correspondance.get("frais") else 0.0

    # Type d'opération
    if correspondance.get("type"):
        valeurs = col("type").astype(str).str.strip()
        dictionnaire = types or {}
        df["type"] = valeurs.map(lambda v: dictionnaire.get(v, classer_type(v)))
    else:
        df["type"] = "ACHAT"
        df.loc[quantite < 0, "type"] = "VENTE"
        if montant is not None:
            df.loc[(quantite.fillna(0) == 0) & (montant.abs() > 0), "type"] = "DIVIDENDE"

    q = quantite.abs().fillna(0.0)
    m = montant.abs() if montant is not None else None
    f = frais if isinstance(frais, pd.Series) else pd.Series(frais, index=df.index)

    # Prix unitaire : donné directement, ou déduit du montant total
    if prix is not None:
        p = prix.abs()
    else:
        p = pd.Series(float("nan"), index=df.index)
    if m is not None:
        a_deduire = p.isna() & (q > 0)
        brut = m.copy()
        if montant_inclut_frais:
            brut = brut.where(df["type"] != "ACHAT", m - f).where(df["type"] != "VENTE", m + f)
        p = p.where(~a_deduire, brut / q.where(q > 0))

    # Dividendes : montant TOTAL reçu dans la colonne prix, quantité 0
    est_div = df["type"] == "DIVIDENDE"
    if m is not None:
        total_div = m.where(m.notna(), p * q.where(q > 0, 1))
    else:
        total_div = p * q.where(q > 0, 1)
    p = p.where(~est_div, total_div)
    q = q.where(~est_div, 0.0)

    df["quantite"], df["prix"], df["frais"] = q, p, f

    # Lignes qui ne sont pas des opérations (total, note, commentaire sous le tableau) :
    # ni date ni titre -> simplement écartées, sans erreur
    hors_tableau = df["date"].isna() & df["identifiant"].str.lower().isin(["", "nan", "none"])
    rapport = {"ignorees": int(((df["type"] == IGNORER) & ~hors_tableau).sum()), "erreurs": [],
               "hors_tableau": int(hors_tableau.sum())}
    df = df[(df["type"] != IGNORER) & ~hors_tableau]
    controles = [
        (lambda d: d["date"].isna(), "date illisible"),
        (lambda d: d["prix"].isna(), "prix ou montant manquant"),
        (lambda d: (d["quantite"] <= 0) & (d["type"] != "DIVIDENDE"), "quantité nulle"),
        (lambda d: d["ticker"].isin(["", "NAN", "NONE"]), "titre manquant"),
    ]
    for controle, message in controles:
        masque = controle(df)                          # recalculé après chaque suppression
        if masque.any():
            lignes = ", ".join(str(i + 1) for i in df.index[masque][:5]) + ("…" if masque.sum() > 5 else "")
            rapport["erreurs"].append({"n": int(masque.sum()), "motif": message, "lignes": lignes})
            df = df[~masque]
    df["quantite"] = df["quantite"].round(6)
    colonnes = COLONNES + (["devise_fichier"] if "devise_fichier" in df.columns else [])
    resultat = df[colonnes].sort_values("date", kind="stable").reset_index(drop=True)
    return resultat, rapport


def message_erreur(erreur):
    """{"n": 2, "motif": "date illisible", "lignes": "3, 7"} -> phrase en français."""
    return f"{erreur['n']} ligne(s) avec {erreur['motif']} (lignes {erreur['lignes']}) : ignorée(s)"


def en_csv(transactions):
    """Tableau standard -> fichier CSV au format du projet (octets)."""
    sortie = transactions[COLONNES].copy()
    sortie["date"] = sortie["date"].dt.strftime("%Y-%m-%d")
    return sortie.to_csv(index=False, float_format="%.6g").encode("utf-8")


# ======================================================================
# 4. Des codes ISIN et des noms vers les tickers Yahoo Finance
# ======================================================================
def nature_identifiant(valeur, tickers_connus=()):
    """'isin', 'ticker' (déjà utilisable) ou 'nom' (à rechercher)."""
    texte = str(valeur).strip().upper()
    if MOTIF_ISIN.match(texte):
        return "isin"
    if texte in tickers_connus or ("." in texte and MOTIF_TICKER.match(texte)):
        return "ticker"
    return "nom"


def _chercher_yahoo(requete):
    """Résultats du moteur de recherche de Yahoo Finance : liste de dicts
    (symbol, shortname, longname, quoteType)."""
    try:
        import yfinance as yf
        if hasattr(yf, "Search"):
            return list(yf.Search(requete, max_results=8, news_count=0).quotes)
    except Exception:
        pass
    import json
    import urllib.parse
    import urllib.request
    adresse = ("https://query2.finance.yahoo.com/v1/finance/search?quotesCount=8&newsCount=0&q="
               + urllib.parse.quote(requete))
    demande = urllib.request.Request(adresse, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(demande, timeout=10) as reponse:
        return json.loads(reponse.read().decode("utf-8")).get("quotes", [])


def _meilleur_resultat(resultats, isin=None):
    """Choisit la cotation la plus pertinente : action ou fonds, place du pays de l'ISIN,
    puis cotation en euros (Paris, Francfort, Amsterdam, Milan), puis la première."""
    utiles = [r for r in resultats if r.get("symbol") and r.get("quoteType", "EQUITY") in
              ("EQUITY", "ETF", "MUTUALFUND", "INDEX")]
    if not utiles:
        return None
    ordre = SUFFIXE_PAR_PAYS.get(isin[:2], []) if isin else []
    ordre = ordre + [".PA", ".DE", ".AS", ".MI", ""]
    def rang(r):
        symbole = r["symbol"]
        suffixe = symbole[symbole.rfind("."):] if "." in symbole else ""
        return ordre.index(suffixe) if suffixe in ordre else len(ordre)
    return min(utiles, key=rang)


def resoudre_identifiants(valeurs, noms=None, tickers_connus=(), chercher=None):
    """Pour chaque identifiant du fichier, propose un ticker Yahoo Finance.

    valeurs : identifiants distincts (tickers, codes ISIN ou noms)
    noms    : {identifiant: nom du titre} si le fichier contient aussi le nom
    chercher: fonction de recherche (remplaçable dans les tests)

    Renvoie un tableau : identifiant, nature, ticker proposé, nom trouvé, statut
    ("tel quel", "trouvé", "introuvable").
    """
    chercher = chercher or _chercher_yahoo
    lignes = []
    for valeur in valeurs:
        valeur = str(valeur).strip()
        nature = nature_identifiant(valeur, tickers_connus)
        ticker, nom, statut = valeur.upper(), (noms or {}).get(valeur, ""), "tel quel"
        if nature != "ticker":
            requetes = [valeur] + ([noms[valeur]] if noms and noms.get(valeur) and nature == "isin" else [])
            resultat = None
            for requete in requetes:
                try:
                    resultat = _meilleur_resultat(chercher(requete), valeur.upper() if nature == "isin" else None)
                except Exception:
                    resultat = None
                if resultat:
                    break
            if resultat:
                ticker = resultat["symbol"]
                nom = nom or resultat.get("longname") or resultat.get("shortname") or ""
                statut = "trouvé"
            else:
                ticker, statut = ("" if nature == "isin" else valeur.upper()), "introuvable"
        lignes.append({"identifiant": valeur, "nature": nature, "ticker": ticker, "nom": nom, "statut": statut})
    return pd.DataFrame(lignes, columns=["identifiant", "nature", "ticker", "nom", "statut"])


# ======================================================================
# Lecture directe (fichier déjà au format du projet, ou presque)
# ======================================================================
def lire_directement(brut):
    """Essaie de lire le fichier sans aide : renvoie les transactions standard, ou
    lève ValueError si une colonne obligatoire n'est pas reconnue.
    Les fichiers qui contiennent des codes ISIN passent aussi par l'assistant."""
    tableau, _ = lire_tableau_brut(brut)
    correspondance = proposer_correspondance(tableau)
    manquants = correspondance_complete(correspondance)
    if manquants:
        raise ValueError(
            f"Colonne(s) manquante(s) ou non reconnue(s) : {', '.join(CHAMPS[m] for m in manquants)}. "
            f"Colonnes lues : {', '.join(map(str, tableau.columns))}. "
            "Le fichier doit contenir les colonnes date, type, ticker, nom, quantite, prix, frais "
            "(un modèle est téléchargeable dans la barre latérale du tableau de bord)."
        )
    transactions, rapport = appliquer_correspondance(tableau, correspondance, montant_inclut_frais=True)
    if rapport["erreurs"] or rapport["ignorees"]:
        raise ValueError("Certaines lignes n'ont pas pu être lues : "
                         + " ; ".join(message_erreur(e) for e in rapport["erreurs"])
                         + (f" ; {rapport['ignorees']} ligne(s) d'un type non reconnu" if rapport["ignorees"] else ""))
    return transactions


# ======================================================================
# 5. Devises : vérifier les prix avec les vrais cours et les reconvertir
# ======================================================================
# Convention du projet : le prix d'un achat ou d'une vente est dans l'unité
# de cotation du titre (dollars pour Apple, pence pour Londres), les frais en
# euros. Beaucoup de relevés bancaires donnent au contraire des montants déjà
# convertis en euros. Pour chaque titre, on compare le prix du fichier au vrai
# cours de clôture du jour, selon trois lectures possibles :
#     "cotation" : prix dans l'unité de cotation (ex. 4 000 pence)
#     "devise"   : prix dans la devise principale (ex. 40,00 livres)
#     "euros"    : prix converti en euros (ex. 46,50 €)
# et on garde la lecture qui colle le mieux au marché.
ECART_TOLERE = 0.25            # au-delà de 25 % d'écart avec le cours du jour : alerte


def _valeur_au(serie, date):
    serie = serie.dropna()
    if serie.empty or date < serie.index[0] - pd.Timedelta(days=7):
        return float("nan")
    return float(serie.asof(date))


def harmoniser_devises(transactions, info_devises, historique, mode="auto"):
    """Ramène les prix dans l'unité de cotation de chaque titre.

    info_devises : {ticker: (devise, facteur)} (src/devises.py)
    historique   : cours de clôture (tickers) et taux de change (EURxxx=X), par date
    mode         : "auto" (d'après les cours), "cotation" (rien à convertir) ou "euros"
                   (tous les montants du fichier sont en euros)

    Renvoie (transactions corrigées, rapport) ; rapport = {"conversions": [{ticker, lecture}],
    "alertes": [{ticker, lignes, ecart}], "verifie": bool}.
    """
    t = transactions.copy()
    rapport = {"conversions": [], "alertes": [], "verifie": historique is not None}
    colonne_devise = "devise_fichier" in t.columns
    for ticker, lignes in t.groupby("ticker"):
        devise, facteur = info_devises.get(ticker, ("EUR", 1.0))
        change = f"EUR{devise}=X"
        echanges = lignes[lignes["type"].isin(["ACHAT", "VENTE"])]
        cours = historique[ticker] if historique is not None and ticker in historique.columns else None
        taux_serie = historique[change] if historique is not None and change in historique.columns else None

        def taux_du(date):
            if devise == "EUR":
                return 1.0
            return _valeur_au(taux_serie, date) if taux_serie is not None else float("nan")

        lectures = {"cotation": lambda p, d: p,
                    "devise": lambda p, d: p / facteur,
                    "euros": lambda p, d: p * taux_du(d) / facteur}
        possibles = ["cotation"] if devise == "EUR" and facteur == 1.0 else ["cotation", "devise", "euros"]
        if facteur == 1.0 and "devise" in possibles:
            possibles.remove("devise")                   # identique à "cotation"
        if mode == "cotation":
            possibles = ["cotation"]
        elif mode == "euros" and devise != "EUR":
            possibles = ["euros"]
        if colonne_devise and mode == "auto":            # la colonne "Devise" du fichier restreint les lectures
            devises_lignes = set(echanges["devise_fichier"].dropna())
            if devises_lignes == {"EUR"} and devise != "EUR":
                possibles = ["euros"]
            elif devises_lignes == {devise}:
                possibles = [x for x in possibles if x != "euros"]

        # Écart (en log) entre le prix lu et le cours du jour, pour chaque lecture
        ecarts = {}
        if cours is not None:
            for lecture in possibles:
                valeurs = []
                for _, l in echanges.iterrows():
                    reference = _valeur_au(cours, l["date"])
                    lu = lectures[lecture](l["prix"], l["date"])
                    if reference > 0 and lu > 0 and not math.isnan(lu):
                        valeurs.append(abs(math.log(lu / reference)))
                if valeurs:
                    ecarts[lecture] = float(pd.Series(valeurs).median())
        if ecarts:
            choix = min(ecarts, key=ecarts.get)
            if ecarts[choix] > math.log(1 + ECART_TOLERE):
                choix = "cotation" if "cotation" in possibles else possibles[0]
            # Par prudence, on ne convertit que si l'autre lecture est nettement meilleure (> 2 %)
            # (ex. le franc suisse vaut presque un euro : les deux lectures sont proches)
            elif choix != "cotation" and "cotation" in ecarts and ecarts["cotation"] - ecarts[choix] < 0.02:
                choix = "cotation"
        else:
            choix = possibles[0] if len(possibles) == 1 else "cotation"

        if choix != "cotation":
            index = lignes.index
            t.loc[index, "prix"] = [lectures[choix](p, d) for p, d in zip(lignes["prix"], lignes["date"])]
            rapport["conversions"].append({"ticker": ticker, "lecture": choix, "devise": devise})

        # Contrôle qualité : prix très éloignés du cours du jour (mauvais ticker, division d'actions...)
        if cours is not None:
            douteuses = []
            for i, l in t.loc[echanges.index].iterrows():
                reference = _valeur_au(cours, l["date"])
                if reference > 0 and l["prix"] > 0 and abs(math.log(l["prix"] / reference)) > math.log(1 + ECART_TOLERE):
                    douteuses.append((i + 1, l["prix"] / reference - 1))
            if douteuses:
                rapport["alertes"].append({"ticker": ticker, "lignes": len(douteuses),
                                           "ecart": float(pd.Series([e for _, e in douteuses]).median())})
    if colonne_devise:
        t = t.drop(columns="devise_fichier")
    return t, rapport


def donnees_de_marche(transactions, chemin_cache=None):
    """Devises et cours historiques nécessaires à harmoniser_devises (connexion Internet)."""
    from pathlib import Path

    from .devises import detecter_devises, devises_etrangeres, ticker_change
    from .market_data import obtenir_historique
    tickers = sorted(transactions["ticker"].unique())
    info = detecter_devises(tickers)
    changes = [ticker_change(d) for d in devises_etrangeres(info)]
    debut = (transactions["date"].min() - pd.Timedelta(days=10)).strftime("%Y-%m-%d")
    cache = chemin_cache or Path(__file__).resolve().parent.parent / "data" / "cache_import.csv"
    historique, _ = obtenir_historique(tickers + changes, debut, chemin_cache=cache)
    return info, historique


# ======================================================================
# Tout en une fois
# ======================================================================
def importer_automatiquement(brut, chercher=None, marche=donnees_de_marche):
    """Enchaîne toutes les étapes sans intervention.

    Renvoie un dictionnaire :
        "sur"          : vrai si le résultat est fiable (sinon ouvrir l'assistant)
        "transactions" : transactions au format du projet (ou None)
        "resume"       : ce que l'outil a compris (pour l'afficher)
        "raison"       : pourquoi ce n'est pas sûr (si "sur" est faux)
    """
    resume = {}
    try:
        tableau, ligne = lire_tableau_brut(brut)
    except Exception as erreur:
        return {"sur": False, "transactions": None, "resume": resume, "raison": str(erreur)}
    correspondance = proposer_correspondance(tableau)
    resume["correspondance"] = correspondance
    resume["sans_entete"] = ligne < 0
    if not confiance(tableau, correspondance):
        manquants = correspondance_complete(correspondance)
        raison = ("Colonne(s) non reconnue(s) : " + ", ".join(CHAMPS[m] for m in manquants)) if manquants \
            else "Colonnes reconnues, mais sans certitude sur les quantités, prix et montants."
        return {"sur": False, "transactions": None, "resume": resume, "raison": raison}
    ordre, ambigu = ordre_des_dates(tableau[correspondance["date"]])
    resume["ordre_dates"], resume["dates_ambigues"] = ordre, ambigu

    # Codes ISIN et noms -> tickers
    colonne_id = correspondance["identifiant"]
    identifiants = [v for v in tableau[colonne_id].astype(str).str.strip().unique() if v and v != "nan"]
    noms = {}
    if correspondance.get("nom"):
        for v, n in zip(tableau[colonne_id].astype(str).str.strip(), tableau[correspondance["nom"]].astype(str)):
            if v and n.strip() and n != "nan":
                noms.setdefault(v, n.strip())
    from .analyse import charger_referentiel
    connus = set(charger_referentiel().index)
    a_chercher = [v for v in identifiants if nature_identifiant(v, connus) != "ticker"]
    correspondances_titres, noms_trouves = {}, {}
    if a_chercher:
        resolution = resoudre_identifiants(a_chercher, noms, connus, chercher=chercher)
        resume["titres_convertis"] = int((resolution["statut"] == "trouvé").sum())
        if (resolution["statut"] == "introuvable").any():
            return {"sur": False, "transactions": None, "resume": resume,
                    "raison": "Titre(s) introuvable(s) : " + ", ".join(resolution.loc[resolution["statut"] == "introuvable", "identifiant"])}
        correspondances_titres = dict(zip(resolution["identifiant"], resolution["ticker"]))
        noms_trouves = {tk: n for tk, n in zip(resolution["ticker"], resolution["nom"]) if n}

    transactions, rapport = appliquer_correspondance(tableau, correspondance, identifiants=correspondances_titres)
    if rapport["erreurs"] or transactions.empty:
        return {"sur": False, "transactions": None, "resume": resume,
                "raison": " ; ".join(message_erreur(e) for e in rapport["erreurs"]) or "Aucune transaction lue."}
    if not correspondance.get("nom") and noms_trouves:
        transactions["nom"] = [noms_trouves.get(tk, n) for tk, n in zip(transactions["ticker"], transactions["nom"])]
    resume["ignorees"] = rapport["ignorees"]

    # Devises : vérification avec les cours du marché (si Internet est disponible)
    try:
        info, historique = marche(transactions)
    except Exception:
        info, historique = {}, None
    transactions, rapport_devises = harmoniser_devises(transactions, info, historique)
    resume["devises"] = rapport_devises
    resume["operations"] = len(transactions)
    resume["titres"] = int(transactions["ticker"].nunique())
    return {"sur": True, "transactions": transactions, "resume": resume, "raison": ""}
