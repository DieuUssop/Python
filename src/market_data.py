"""
market_data.py — Récupération des cours de bourse.

Rôle de ce fichier :
    Aller chercher sur Internet (via Yahoo Finance) le dernier cours connu
    de chaque titre du portefeuille.

Pourquoi un fichier séparé de portfolio.py ?
    Principe de "séparation des responsabilités" :
      - portfolio.py  fait les CALCULS (il ne sait pas d'où viennent les prix),
      - market_data.py va chercher les DONNÉES.
    Avantages : on peut tester les calculs sans Internet, et si un jour on
    change de source de données, on ne modifie que ce fichier.

Sécurité : le cache
    Yahoo Finance est gratuit mais pas toujours fiable (panne, pas de
    connexion Wi-Fi le jour de la soutenance...). Chaque fois qu'on récupère
    des cours, on les enregistre dans data/cache_prix.csv. Si Internet ne
    répond pas, on réutilise ces derniers cours enregistrés.
"""

from pathlib import Path

import pandas as pd

# Emplacement du fichier cache : dossier "data" à la racine du projet.
# Path(__file__) = ce fichier ; .parent = dossier src ; .parent = racine.
CHEMIN_CACHE = Path(__file__).resolve().parent.parent / "data" / "cache_prix.csv"


def telecharger_derniers_cours(tickers):
    """Télécharge le dernier cours de clôture de chaque ticker.

    Paramètre : tickers = liste de codes Yahoo, ex. ["MC.PA", "AI.PA"]
    Renvoie   : dictionnaire {ticker: cours}, ex. {"MC.PA": 612.3, ...}
    """
    # On importe yfinance ici (et pas en haut du fichier) pour que le reste
    # du projet fonctionne même si yfinance n'est pas installé.
    import yfinance as yf

    # On demande les 5 derniers jours (et pas seulement aujourd'hui) : le
    # week-end ou un jour férié, il n'y a pas de cotation du jour.
    # auto_adjust=False : on veut le VRAI cours affiché en bourse, pas un
    # cours "ajusté" des dividendes (on s'en servira à l'étape 3).
    donnees = yf.download(
        list(tickers),
        period="5d",
        auto_adjust=False,
        progress=False,
    )
    if donnees is None or donnees.empty:
        raise ConnectionError("Yahoo Finance n'a renvoyé aucune donnée.")

    clotures = donnees["Close"]
    # Si un seul ticker est demandé, pandas peut renvoyer une "Series"
    # (une seule colonne) : on la transforme en tableau pour simplifier.
    if isinstance(clotures, pd.Series):
        clotures = clotures.to_frame(name=list(tickers)[0])

    # ffill() ("forward fill") recopie la dernière valeur connue vers le bas,
    # puis iloc[-1] prend la dernière ligne = le cours le plus récent.
    derniers = clotures.ffill().iloc[-1]

    # On ne garde que les tickers pour lesquels on a bien un cours.
    return {t: float(derniers[t]) for t in derniers.index if pd.notna(derniers[t])}


def _sauver_cache(prix):
    """Enregistre les cours dans data/cache_prix.csv (avec la date du jour)."""
    tableau = pd.DataFrame({"ticker": list(prix), "cours": list(prix.values())})
    tableau["date_maj"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
    CHEMIN_CACHE.parent.mkdir(parents=True, exist_ok=True)
    tableau.to_csv(CHEMIN_CACHE, index=False)


def _lire_cache():
    """Relit les cours enregistrés lors d'une précédente exécution."""
    if not CHEMIN_CACHE.exists():
        return {}, None
    tableau = pd.read_csv(CHEMIN_CACHE)
    date_maj = tableau["date_maj"].iloc[0] if len(tableau) else None
    return dict(zip(tableau["ticker"], tableau["cours"])), date_maj


def obtenir_cours(tickers):
    """Fonction principale : renvoie les cours ET leur provenance.

    Renvoie un tuple (prix, source) :
        prix   = {ticker: cours}
        source = texte expliquant d'où viennent les cours
    """
    tickers = list(tickers)
    try:
        prix = telecharger_derniers_cours(tickers)
        _sauver_cache(prix)
        source = "Yahoo Finance (en direct)"
    except Exception as erreur:
        # "except" attrape n'importe quel problème (pas d'Internet, Yahoo en
        # panne...) pour que le programme ne plante pas.
        prix, date_maj = _lire_cache()
        if not prix:
            raise RuntimeError(
                "Impossible de récupérer les cours : pas de connexion à Yahoo "
                f"Finance et aucun cache disponible.\nDétail : {erreur}"
            )
        source = f"cache local du {date_maj} (Yahoo Finance injoignable)"

    manquants = [t for t in tickers if t not in prix]
    if manquants:
        print(f"⚠️  Aucun cours trouvé pour : {manquants} (ticker mal écrit ?)")
    return prix, source


# ======================================================================
# Étape 3 : historique des cours (un cours par jour de bourse)
# ======================================================================
CHEMIN_CACHE_HISTO = CHEMIN_CACHE.parent / "cache_historique.csv"


def telecharger_historique(tickers, debut):
    """Télécharge les cours de clôture quotidiens depuis la date "debut".

    Renvoie un tableau :
        - une ligne par jour de bourse (l'index = les dates),
        - une colonne par ticker.
    """
    import yfinance as yf

    donnees = yf.download(
        list(tickers),
        start=pd.Timestamp(debut).strftime("%Y-%m-%d"),
        auto_adjust=False,   # cours réels, non ajustés (voir le guide)
        progress=False,
    )
    if donnees is None or donnees.empty:
        raise ConnectionError("Yahoo Finance n'a renvoyé aucune donnée.")

    clotures = donnees["Close"]
    if isinstance(clotures, pd.Series):
        clotures = clotures.to_frame(name=list(tickers)[0])

    # On enlève le fuseau horaire éventuel des dates, pour pouvoir les
    # comparer aux dates du fichier de transactions.
    clotures.index = pd.to_datetime(clotures.index).tz_localize(None).normalize()
    return clotures


def obtenir_historique(tickers, debut, chemin_cache=None):
    """Comme obtenir_cours(), mais pour l'historique : Internet, sinon cache.

    chemin_cache : fichier de cache à utiliser (par défaut data/cache_historique.csv).
    Les stress tests (étape 10) utilisent leur propre cache, pour ne pas
    écraser celui de l'analyse courante.

    Renvoie un tuple (tableau_des_cours, source).
    """
    tickers = list(tickers)
    cache = chemin_cache or CHEMIN_CACHE_HISTO
    try:
        histo = telecharger_historique(tickers, debut)
        histo.to_csv(cache)
        source = "Yahoo Finance (en direct)"
    except Exception as erreur:
        if not cache.exists():
            raise RuntimeError(
                "Impossible de récupérer l'historique : pas de connexion à Yahoo "
                f"Finance et aucun cache disponible.\nDétail : {erreur}"
            )
        # index_col=0 : la 1re colonne (les dates) sert d'index.
        histo = pd.read_csv(cache, index_col=0, parse_dates=True)
        source = "cache local (Yahoo Finance injoignable)"

    manquants = [t for t in tickers if t not in histo.columns]
    if manquants:
        print(f"⚠️  Pas d'historique pour : {manquants} (ticker mal écrit ?)")
    return histo, source
