"""
indices.py — Les indices de référence proposés dans le tableau de bord.

Quatre familles :
    - Actions      : grands indices, suivis par un ETF capitalisant (dividendes
                     réinvestis) quand c'est possible, sinon l'indice de prix ;
    - Obligations  : emprunts d'État et obligations d'entreprises de la zone euro ;
    - Monétaire    : €STR, le taux au jour le jour de la BCE ;
    - Mixtes       : indices COMPOSITES calculés par l'outil, X % actions
                     (MSCI World) et Y % obligations (emprunts d'État zone euro),
                     rééquilibrés chaque mois. Ils correspondent aux profils
                     prudent, équilibré et dynamique du conseil patrimonial.

Un indice peut avoir plusieurs tickers « candidats » : le premier dont Yahoo
Finance (ou la base locale) fournit l'historique est utilisé.

Les cours sont téléchargés SANS ajustement des dividendes (voir market_data.py) :
un ETF capitalisant (dividendes réinvestis dans le fonds) donne donc une
performance « dividendes compris », un ETF distribuant ou un indice de prix une
performance « hors dividendes ». Les libellés le précisent.
"""

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class Indice:
    code: str                     # identifiant (ticker, ou code du composite)
    nom: str                      # libellé long (français ; traduit à l'affichage)
    court: str                    # libellé court
    famille: str                  # Actions, Obligations, Monétaire, Mixtes
    candidats: list = field(default_factory=list)   # tickers possibles (indice simple)
    poids: dict = field(default_factory=dict)       # composite : {poche: part}
    composition: str = None       # clé de composition_etf (pays, secteurs) de la poche actions
    part_actions: float = 1.0


ACTIONS_MONDE = ["CW8.PA", "IWDA.AS", "EUNL.DE"]
OBLIG_ETAT_EURO = ["DBXN.DE", "EUNH.DE"]       # Xtrackers Eurozone Govt Bond 1C (capitalisant), sinon iShares

LISTE = [
    # --- Actions ---
    Indice("CW8.PA", "MSCI World (ETF CW8, dividendes réinvestis)", "MSCI World", "Actions",
           ["CW8.PA", "IWDA.AS"], composition="MSCI World"),
    Indice("IUSQ.DE", "MSCI ACWI, monde avec émergents (ETF, dividendes réinvestis)", "MSCI ACWI", "Actions",
           ["IUSQ.DE", "VWCE.DE"], composition="MSCI ACWI"),
    Indice("ESE.PA", "S&P 500 (ETF ESE, dividendes réinvestis)", "S&P 500", "Actions",
           ["ESE.PA", "PE500.PA"], composition="S&P 500"),
    Indice("PUST.PA", "Nasdaq-100 (ETF, dividendes réinvestis)", "Nasdaq-100", "Actions",
           ["PUST.PA", "EQQQ.DE"], composition="Nasdaq-100"),
    Indice("MEUD.PA", "Stoxx Europe 600 (ETF, dividendes réinvestis)", "Stoxx Europe 600", "Actions",
           ["MEUD.PA", "EUNK.DE"], composition="MSCI Europe"),
    Indice("^STOXX50E", "Euro Stoxx 50 (hors dividendes)", "Euro Stoxx 50", "Actions",
           ["^STOXX50E", "MSE.PA"], composition="Euro Stoxx 50"),
    Indice("^FCHI", "CAC 40 (hors dividendes)", "CAC 40", "Actions", ["^FCHI", "CAC.PA"], composition="CAC 40"),
    Indice("PAEEM.PA", "MSCI Marchés émergents (ETF, dividendes réinvestis)", "MSCI Émergents", "Actions",
           ["PAEEM.PA", "AEEM.PA"], composition="MSCI Emerging Markets"),
    # --- Obligations ---
    Indice("DBXN.DE", "Emprunts d'État zone euro (ETF, coupons réinvestis)", "Emprunts d'État €", "Obligations",
           OBLIG_ETAT_EURO, part_actions=0.0),
    Indice("EUN5.DE", "Obligations d'entreprises en euros (ETF, hors coupons)", "Oblig. entreprises €",
           "Obligations", ["EUN5.DE"], part_actions=0.0),
    # --- Monétaire ---
    Indice("XEON.DE", "Monétaire €STR (ETF, intérêts réinvestis)", "€STR", "Monétaire", ["XEON.DE", "CSH2.PA"],
           part_actions=0.0),
    # --- Mixtes (composites) ---
    Indice("MIXTE_20", "Mixte prudent : 20 % actions monde / 80 % obligations €", "Mixte 20/80", "Mixtes",
           poids={"actions": 0.20, "obligations": 0.80}, composition="MSCI World", part_actions=0.20),
    Indice("MIXTE_60", "Mixte équilibré : 60 % actions monde / 40 % obligations €", "Mixte 60/40", "Mixtes",
           poids={"actions": 0.60, "obligations": 0.40}, composition="MSCI World", part_actions=0.60),
    Indice("MIXTE_80", "Mixte dynamique : 80 % actions monde / 20 % obligations €", "Mixte 80/20", "Mixtes",
           poids={"actions": 0.80, "obligations": 0.20}, composition="MSCI World", part_actions=0.80),
]
INDICES = {i.code: i for i in LISTE}
POCHES = {"actions": ACTIONS_MONDE, "obligations": OBLIG_ETAT_EURO}
FAMILLES = ["Actions", "Obligations", "Monétaire", "Mixtes"]


def indice(code):
    """Fiche de l'indice (un ticker inconnu devient un indice actions simple)."""
    if code in INDICES:
        return INDICES[code]
    return Indice(code, code, code, "Actions", [code])


def est_composite(code):
    return bool(indice(code).poids)


def tickers_a_telecharger(code):
    """Tous les tickers dont l'indice peut avoir besoin."""
    fiche = indice(code)
    if fiche.poids:
        return [t for poche in fiche.poids for t in POCHES[poche]]
    return list(fiche.candidats or [code])


def _premier_disponible(prix, candidats, minimum=20):
    for t in candidats:
        if t in prix.columns and prix[t].notna().sum() >= minimum:
            return t
    return None


def serie_composite(prix, poids, frequence="ME"):
    """Indice composite rééquilibré : poids fixes remis en place à chaque fin de période.

    prix  : tableau de cours (une colonne par composante, en euros)
    poids : {colonne: part}, total = 1
    Renvoie une série en base 100.
    """
    cours = prix[list(poids)].ffill().dropna()
    if cours.empty:
        raise ValueError("pas de cours communs pour l'indice composite")
    w = pd.Series(poids, dtype=float)
    w = w / w.sum()
    valeur = 100.0
    parts = valeur * w / cours.iloc[0]               # nombre de « parts » de chaque composante
    fins = set(cours.groupby(cours.index.to_period(frequence[0])).tail(1).index)
    serie = []
    for date, ligne in cours.iterrows():
        valeur = float((parts * ligne).sum())
        serie.append(valeur)
        if date in fins:                             # rééquilibrage au cours de clôture
            parts = valeur * w / ligne
    return pd.Series(serie, index=cours.index, name="composite")


def construire(prix, code):
    """Série de l'indice `code` à partir des cours téléchargés (en euros).

    Indice simple : premier candidat disponible. Composite : calculé.
    Renvoie (série, tickers utilisés)."""
    fiche = indice(code)
    if fiche.poids:
        choisis = {}
        for poche, part in fiche.poids.items():
            t = _premier_disponible(prix, POCHES[poche])
            if t is None:
                raise ValueError(f"historique introuvable pour la poche {poche} de {fiche.court}")
            choisis[t] = part
        return serie_composite(prix, choisis), list(choisis)
    t = _premier_disponible(prix, fiche.candidats or [code], minimum=1)
    if t is None:
        raise ValueError(f"Impossible de récupérer l'historique de l'indice {code}.")
    return prix[t].rename(code), [t]
