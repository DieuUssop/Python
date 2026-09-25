"""
devises.py — Gestion des titres cotés dans une autre devise que l'euro.

Problème : une action américaine (Apple, "AAPL") est cotée en dollars.
Pour l'additionner à des actions françaises, il faut tout convertir en
euros, au taux de change DU JOUR concerné :
    - un achat de 2023 est converti au taux de change de 2023 ;
    - la valeur d'aujourd'hui est convertie au taux d'aujourd'hui.

Conséquence intéressante : la performance d'un titre étranger en euros
combine DEUX effets, la variation du cours ET la variation de la devise.
Une action américaine qui monte de 10 % en dollars peut ne rien rapporter
en euros si le dollar a baissé de 10 % face à l'euro : c'est le RISQUE DE
CHANGE.

Convention du fichier de transactions :
    - "prix" (prix unitaire ou montant de dividende) est saisi dans la
      devise de cotation du titre, telle qu'affichée par Yahoo Finance
      (dollars pour AAPL, pence pour les actions de Londres "...L") ;
    - "frais" est toujours en euros (frais facturés par un courtier français).

Taux de change Yahoo Finance : "EURUSD=X" = nombre de dollars pour 1 euro.
    prix en euros = prix en dollars / taux EURUSD
"""

from pathlib import Path

import pandas as pd

CHEMIN_CACHE_DEVISES = Path(__file__).resolve().parent.parent / "data" / "cache_devises.csv"

# Devise selon le suffixe du ticker Yahoo (utilisé si Yahoo ne répond pas).
SUFFIXES = {
    ".PA": "EUR", ".AS": "EUR", ".DE": "EUR", ".F": "EUR", ".MI": "EUR", ".MC": "EUR",
    ".BR": "EUR", ".LS": "EUR", ".HE": "EUR", ".VI": "EUR", ".IR": "EUR",
    ".L": "GBp", ".SW": "CHF", ".TO": "CAD", ".T": "JPY", ".HK": "HKD", ".AX": "AUD",
    ".ST": "SEK", ".CO": "DKK", ".OL": "NOK",
}
INDICES_CONNUS = {
    "^FCHI": "EUR", "^STOXX50E": "EUR", "^GDAXI": "EUR",
    "^GSPC": "USD", "^IXIC": "USD", "^DJI": "USD", "^FTSE": "GBP", "^N225": "JPY",
}


def devise_par_suffixe(ticker):
    """Devise probable d'après le code du ticker (sans Internet)."""
    if ticker in INDICES_CONNUS:
        return INDICES_CONNUS[ticker]
    if "." in ticker:
        suffixe = ticker[ticker.rfind("."):]
        return SUFFIXES.get(suffixe, "EUR")
    return "USD"          # pas de suffixe : action américaine (AAPL, MSFT...)


def normaliser(devise):
    """Renvoie (devise, facteur). Les actions de Londres sont cotées en
    PENCE (GBp) : 1 250 GBp = 12,50 GBP, d'où un facteur de 0,01."""
    if devise in ("GBp", "GBX"):
        return "GBP", 0.01
    return (devise or "EUR").upper(), 1.0


def detecter_devises(tickers):
    """Devise de chaque ticker : {ticker: (devise, facteur)}.

    On interroge Yahoo Finance (information exacte), avec un cache pour ne
    pas le refaire à chaque lancement. En cas d'échec : règle du suffixe.
    """
    cache = {}
    if CHEMIN_CACHE_DEVISES.exists():
        tableau = pd.read_csv(CHEMIN_CACHE_DEVISES)
        cache = dict(zip(tableau["ticker"], tableau["devise"]))

    brutes = {}
    for ticker in tickers:
        if ticker in cache:
            brutes[ticker] = cache[ticker]
            continue
        try:
            import yfinance as yf
            brutes[ticker] = yf.Ticker(ticker).fast_info["currency"]
        except Exception:
            brutes[ticker] = devise_par_suffixe(ticker)
        cache[ticker] = brutes[ticker]

    try:
        CHEMIN_CACHE_DEVISES.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame({"ticker": list(cache), "devise": list(cache.values())}).to_csv(
            CHEMIN_CACHE_DEVISES, index=False)
    except OSError:
        pass
    return {t: normaliser(d) for t, d in brutes.items()}


def devises_etrangeres(info_devises):
    """Liste des devises autres que l'euro présentes dans le portefeuille."""
    return sorted({d for d, _ in info_devises.values() if d != "EUR"})


def ticker_change(devise):
    """Code Yahoo du taux de change : 'USD' -> 'EURUSD=X'."""
    return f"EUR{devise}=X"


def _taux_aligne(taux_hist, devise, dates):
    """Taux de change de la devise pour chaque date demandée (dernier connu)."""
    serie = taux_hist[devise].dropna().sort_index()
    if serie.empty:
        raise ValueError(f"Aucun taux de change disponible pour {devise}.")
    aligne = serie.reindex(serie.index.union(pd.DatetimeIndex(dates).unique())).ffill().bfill()
    return aligne.reindex(dates)


def convertir_prix_historiques(prix_hist, info_devises, taux_hist):
    """Convertit en euros chaque colonne de cours cotée dans une devise étrangère."""
    resultat = prix_hist.copy()
    for ticker in resultat.columns:
        devise, facteur = info_devises.get(ticker, ("EUR", 1.0))
        if devise == "EUR" and facteur == 1.0:
            continue
        if devise == "EUR":
            resultat[ticker] = resultat[ticker] * facteur
            continue
        taux = _taux_aligne(taux_hist, devise, resultat.index)
        resultat[ticker] = resultat[ticker] * facteur / taux
    return resultat


def convertir_cours(prix, info_devises, taux_actuels):
    """Convertit en euros les derniers cours {ticker: cours}."""
    resultat = {}
    for ticker, cours in prix.items():
        devise, facteur = info_devises.get(ticker, ("EUR", 1.0))
        resultat[ticker] = cours * facteur if devise == "EUR" else cours * facteur / taux_actuels[devise]
    return resultat


def convertir_transactions(transactions, info_devises, taux_hist):
    """Convertit en euros les prix des transactions, au taux du jour de l'opération.

    Deux colonnes sont ajoutées pour garder une trace : "devise" et
    "prix_devise" (le prix d'origine, tel que saisi).
    """
    t = transactions.copy()
    t["devise"] = t["ticker"].map(lambda x: info_devises.get(x, ("EUR", 1.0))[0])
    t["prix_devise"] = t["prix"]
    for devise in t["devise"].unique():
        masque = t["devise"] == devise
        facteurs = t.loc[masque, "ticker"].map(lambda x: info_devises[x][1])
        if devise == "EUR":
            t.loc[masque, "prix"] = t.loc[masque, "prix"] * facteurs
            continue
        taux = _taux_aligne(taux_hist, devise, pd.DatetimeIndex(t.loc[masque, "date"]))
        t.loc[masque, "prix"] = t.loc[masque, "prix"].to_numpy() * facteurs.to_numpy() / taux.to_numpy()
    return t
