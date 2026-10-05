"""
base_titres.py — La base locale de titres : la "mémoire" de l'outil.

Elle permet de travailler HORS CONNEXION et d'aller plus vite en ligne.
Elle contient trois choses, dans le dossier data/base/ :

    1. titres.csv  : la fiche de chaque titre connu (ticker Yahoo, nom, ISIN,
                     pays, région, secteur, classe d'actifs, devise, indices) ;
    2. cours/      : les cours de clôture quotidiens (depuis 2015 pour les
                     actions, 2007 pour les indices et les taux de change),
                     rangés en 32 "paquets" compressés (fichiers .npz) ;
    3. memoire.csv : les correspondances apprises au fil des imports
                     (code ISIN, nom de société, ticker Bloomberg... -> ticker
                     Yahoo). Une recherche faite une fois n'est plus refaite.

La base se remplit de deux façons :
    - une fois pour toutes avec le script construire_base_titres.py
      (≈ 4 000 titres, à lancer avec Internet) ;
    - automatiquement : chaque cours téléchargé pendant une analyse y est ajouté.

Pourquoi des paquets ? Écrire un seul gros fichier de 30 Mo à chaque analyse
serait lent ; avec 32 paquets, on ne réécrit que ceux qui ont changé.
Pourquoi le format .npz (NumPy) ? Il est compact, rapide à lire, et ne dépend
d'aucune bibliothèque supplémentaire.

La mémoire est commune à tous les utilisateurs de l'application, mais elle ne
contient AUCUNE donnée de portefeuille : seulement des correspondances entre
codes de titres (ex. FR0000121014 -> MC.PA).
"""

import hashlib
import os
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

# Dossier de la base (la variable d'environnement PORTFOLIO_BASE permet d'en utiliser un autre, ex. pour les tests)
DOSSIER = Path(os.environ.get("PORTFOLIO_BASE", Path(__file__).resolve().parent.parent / "data" / "base"))
NB_PAQUETS = 32
COLONNES_TITRES = ["ticker", "nom", "isin", "pays", "region", "secteur", "classe", "devise", "indices"]
COLONNES_MEMOIRE = ["identifiant", "ticker", "nom", "source", "date"]

_memoire_paquets = {}            # paquets déjà lus : {chemin: (date de modification, tableau)}


# ======================================================================
# Outils
# ======================================================================
def _dossier():
    return Path(DOSSIER)


def _chemin_paquet(numero):
    return _dossier() / "cours" / f"paquet_{numero:02d}.npz"


def paquet_de(ticker):
    """Numéro du paquet (0 à 31) qui contient ce ticker (toujours le même)."""
    return int(hashlib.md5(str(ticker).encode("utf-8")).hexdigest(), 16) % NB_PAQUETS


def _ecrire_atomique(chemin, ecrire):
    """Écrit dans un fichier temporaire puis le renomme : un arrêt brutal
    (coupure, fenêtre fermée) ne laisse jamais de fichier à moitié écrit."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    temporaire = chemin.with_name(chemin.name + ".tmp")
    ecrire(temporaire)
    os.replace(temporaire, chemin)


def normaliser_nom(texte):
    """'LVMH Moët Hennessy - Louis Vuitton SE' -> 'lvmh moet hennessy louis vuitton'."""
    texte = "".join(c for c in unicodedata.normalize("NFKD", str(texte)) if not unicodedata.combining(c))
    texte = re.sub(r"[^a-z0-9 ]", " ", texte.lower())
    mots = [m for m in texte.split() if m not in {"se", "sa", "inc", "plc", "ag", "nv", "corp", "co", "ltd",
                                                   "the", "group", "holding", "holdings", "company", "spa",
                                                   "asa", "ab", "oyj", "class", "a", "b", "reg", "corporation"}]
    return " ".join(mots)


# ======================================================================
# 1. Les cours
# ======================================================================
def _lire_paquet(numero):
    chemin = _chemin_paquet(numero)
    if not chemin.exists():
        return pd.DataFrame(dtype="float32")
    date_modif = chemin.stat().st_mtime
    deja = _memoire_paquets.get(str(chemin))
    if deja and deja[0] == date_modif:
        return deja[1]
    with np.load(chemin, allow_pickle=False) as donnees:
        index = pd.to_datetime(donnees["dates"].astype("int64"), unit="D")
        tableau = pd.DataFrame(donnees["valeurs"], index=index, columns=[str(t) for t in donnees["tickers"]])
    _memoire_paquets[str(chemin)] = (date_modif, tableau)
    return tableau


def _ecrire_paquet(numero, tableau):
    tableau = tableau.sort_index()
    tableau = tableau.loc[:, tableau.notna().any()]
    dates = ((tableau.index - pd.Timestamp("1970-01-01")).days).to_numpy().astype("int32")

    def ecrire(chemin):
        with open(chemin, "wb") as f:
            np.savez_compressed(f, dates=dates, tickers=np.array(tableau.columns, dtype="U24"),
                                valeurs=tableau.to_numpy(dtype="float32"))
    _ecrire_atomique(_chemin_paquet(numero), ecrire)
    _memoire_paquets.pop(str(_chemin_paquet(numero)), None)


def tickers_avec_cours():
    """Liste de tous les tickers dont la base contient des cours."""
    tous = []
    for numero in range(NB_PAQUETS):
        tous += list(_lire_paquet(numero).columns)
    return sorted(tous)


def lire_cours(tickers, debut=None):
    """Cours de clôture des tickers demandés (ceux qui sont dans la base).
    Renvoie un tableau (une colonne par ticker trouvé), éventuellement vide."""
    morceaux = []
    par_paquet = {}
    for t in dict.fromkeys(tickers):
        par_paquet.setdefault(paquet_de(t), []).append(t)
    for numero, liste in par_paquet.items():
        paquet = _lire_paquet(numero)
        presents = [t for t in liste if t in paquet.columns]
        if presents:
            morceaux.append(paquet[presents])
    if not morceaux:
        return pd.DataFrame()
    resultat = pd.concat(morceaux, axis=1).astype("float64")
    if debut is not None:
        resultat = resultat[resultat.index >= pd.Timestamp(debut)]
    resultat = resultat.dropna(how="all")
    return resultat[[t for t in tickers if t in resultat.columns]]


def ajouter_cours(tableau):
    """Ajoute (ou met à jour) des cours dans la base. Les nouvelles valeurs
    l'emportent sur les anciennes ; seuls les paquets modifiés sont réécrits.
    Renvoie le nombre de tickers ajoutés ou mis à jour."""
    if tableau is None or tableau.empty:
        return 0
    tableau = tableau.copy()
    index = pd.to_datetime(tableau.index)
    if index.tz is not None:
        index = index.tz_localize(None)
    tableau.index = index.normalize()
    tableau = tableau.loc[:, tableau.notna().any()]
    tableau = tableau[~tableau.index.duplicated(keep="last")]
    par_paquet = {}
    for t in tableau.columns:
        par_paquet.setdefault(paquet_de(str(t)), []).append(t)
    modifies = 0
    for numero, colonnes in par_paquet.items():
        ancien = _lire_paquet(numero)
        nouveau = tableau[colonnes].astype("float32")
        fusion = nouveau.combine_first(ancien) if not ancien.empty else nouveau
        fusion = fusion.astype("float32")
        if not ancien.empty and fusion.shape == ancien.shape and \
                fusion.loc[ancien.index, ancien.columns].equals(ancien):
            continue                                     # rien de nouveau : on ne réécrit pas
        _ecrire_paquet(numero, fusion)
        modifies += len(colonnes)
    return modifies


def derniers_cours(tickers):
    """{ticker: (dernier cours, date)} pour les tickers présents dans la base."""
    cours = lire_cours(tickers)
    resultat = {}
    for t in cours.columns:
        serie = cours[t].dropna()
        if not serie.empty:
            resultat[t] = (float(serie.iloc[-1]), serie.index[-1])
    return resultat


def derniere_date():
    """Date du cours le plus récent de la base (None si la base est vide)."""
    dates = [p.index.max() for p in (_lire_paquet(n) for n in range(NB_PAQUETS)) if not p.empty]
    return max(dates) if dates else None


# ======================================================================
# 2. La fiche des titres
# ======================================================================
_memoire_titres = {}


def lire_titres():
    """Fiche de tous les titres connus (tableau indexé par le ticker)."""
    chemin = _dossier() / "titres.csv"
    if not chemin.exists():
        return pd.DataFrame(columns=COLONNES_TITRES).set_index("ticker")
    date_modif = chemin.stat().st_mtime
    deja = _memoire_titres.get(str(chemin))
    if deja and deja[0] == date_modif:
        return deja[1].copy()
    tableau = pd.read_csv(chemin, dtype=str, keep_default_na=False)
    for c in COLONNES_TITRES:
        if c not in tableau.columns:
            tableau[c] = ""
    tableau = tableau[COLONNES_TITRES].drop_duplicates("ticker", keep="last").set_index("ticker")
    _memoire_titres[str(chemin)] = (date_modif, tableau)
    return tableau.copy()


def ajouter_titres(lignes):
    """Ajoute ou complète des fiches de titres (liste de dictionnaires).
    Une information déjà connue n'est remplacée que par une valeur non vide."""
    if not lignes:
        return
    existants = lire_titres()
    nouveaux = pd.DataFrame(lignes, dtype=str).fillna("")
    for c in COLONNES_TITRES:
        if c not in nouveaux.columns:
            nouveaux[c] = ""
    nouveaux = nouveaux[COLONNES_TITRES].drop_duplicates("ticker", keep="last").set_index("ticker")
    fusion = existants.copy()
    for ticker, ligne in nouveaux.iterrows():
        if ticker in fusion.index:
            for c in fusion.columns:
                if str(ligne[c]).strip():
                    fusion.at[ticker, c] = ligne[c]
        else:
            fusion.loc[ticker] = ligne
    _ecrire_atomique(_dossier() / "titres.csv",
                     lambda chemin: fusion.reset_index().to_csv(chemin, index=False, encoding="utf-8"))


# ======================================================================
# 3. La mémoire des correspondances (ISIN, noms, Bloomberg... -> ticker)
# ======================================================================
def _cle(identifiant):
    return re.sub(r"\s+", " ", str(identifiant).strip().upper())


def lire_memoire():
    chemin = _dossier() / "memoire.csv"
    if not chemin.exists():
        return pd.DataFrame(columns=COLONNES_MEMOIRE)
    return pd.read_csv(chemin, dtype=str, keep_default_na=False)


def memoriser(identifiant, ticker, nom="", source="recherche"):
    """Retient qu'un identifiant (ISIN, nom, code Bloomberg...) correspond à un ticker."""
    if not identifiant or not ticker:
        return
    memoire = lire_memoire()
    cle = _cle(identifiant)
    memoire = memoire[memoire["identifiant"] != cle]
    memoire.loc[len(memoire)] = [cle, str(ticker).upper(), nom or "", source,
                                 pd.Timestamp.now().strftime("%Y-%m-%d")]
    try:
        _ecrire_atomique(_dossier() / "memoire.csv",
                         lambda chemin: memoire.to_csv(chemin, index=False, encoding="utf-8"))
    except OSError:
        pass                                             # dossier en lecture seule : tant pis


def chercher_localement(identifiant):
    """Cherche un titre sans Internet : dans la mémoire, puis dans la fiche des
    titres (code ISIN, ticker, nom). Renvoie une liste de résultats au même
    format que le moteur de recherche de Yahoo ({"symbol", "longname", ...})."""
    cle = _cle(identifiant)
    memoire = lire_memoire()
    trouve = memoire[memoire["identifiant"] == cle]
    if not trouve.empty:
        ligne = trouve.iloc[-1]
        return [{"symbol": ligne["ticker"], "longname": ligne["nom"], "quoteType": "EQUITY", "local": True}]
    titres = lire_titres()
    if titres.empty:
        return []
    if cle in titres.index:
        return [{"symbol": cle, "longname": titres.at[cle, "nom"], "quoteType": "EQUITY", "local": True}]
    if "isin" in titres.columns:
        par_isin = titres[titres["isin"].str.upper() == cle]
        if not par_isin.empty:
            return [{"symbol": t, "longname": par_isin.at[t, "nom"], "quoteType": "EQUITY", "local": True}
                    for t in par_isin.index]
    nom = normaliser_nom(identifiant)
    if len(nom) >= 3:
        noms = titres["nom"].map(normaliser_nom)
        exacts = titres[noms == nom]
        if exacts.empty:                                 # "LVMH" dans "LVMH Moët Hennessy Louis Vuitton"
            exacts = titres[noms.str.split().str[0] == nom] if " " not in nom else exacts
        return [{"symbol": t, "longname": exacts.at[t, "nom"], "quoteType": "EQUITY", "local": True}
                for t in exacts.index[:5]]
    return []


def resume():
    """Quelques chiffres sur la base (pour l'afficher)."""
    return {"titres": len(lire_titres()), "titres_avec_cours": len(tickers_avec_cours()),
            "derniere_date": derniere_date(), "memoire": len(lire_memoire())}
