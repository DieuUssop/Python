"""
stress.py — Stress tests : que perdrait le portefeuille ACTUEL si une crise
passée se reproduisait, ou si un choc hypothétique survenait ?

Deux familles de scénarios :

  1. Scénarios HISTORIQUES : on applique à chaque ligne actuelle la
     variation qu'elle a réellement subie pendant une crise passée
     (du plus haut au plus bas du marché).
     Si un titre n'existait pas encore (ou n'a pas d'historique), on utilise
     l'indice de sa région comme approximation ("proxy").

  2. Scénarios HYPOTHÉTIQUES :
     - baisse des actions de X % : perte ≈ bêta du portefeuille × X ;
     - baisse du dollar de 10 % : perte sur la part investie en dollars ;
     - hausse des taux de 1 point : perte ≈ duration × 1 % sur les obligations.

Limites : variations calculées en devise locale (effet de change ignoré dans
les scénarios historiques) et sur des cours hors dividendes.
"""

from pathlib import Path

import pandas as pd

from .market_data import obtenir_historique

CHEMIN_CACHE_STRESS = Path(__file__).resolve().parent.parent / "data" / "cache_stress.csv"

# (nom, date du plus haut, date du plus bas)
SCENARIOS_HISTORIQUES = [
    ("Crise financière (2008-2009)", "2008-09-01", "2009-03-09"),
    ("Crise de la dette européenne (2011)", "2011-07-01", "2011-09-22"),
    ("Krach du Covid (2020)", "2020-02-19", "2020-03-23"),
    ("Inflation et hausse des taux (2022)", "2022-01-03", "2022-10-12"),
    ("Mini-krach d'août 2024", "2024-07-16", "2024-08-05"),
]

# Indice représentatif de chaque région (codes Yahoo Finance)
PROXIES_REGIONS = {
    "États-Unis": "^GSPC", "Europe": "^STOXX50E", "Royaume-Uni": "^FTSE", "Suisse": "^SSMI",
    "Japon": "^N225", "Asie-Pacifique": "^AXJO", "Canada": "^GSPTSE", "Émergents": "EEM",
    "Monde (ETF)": "^GSPC",
}
PROXY_PAR_DEFAUT = "^GSPC"

# Pour les obligations et l'or, un indice ACTIONS serait une mauvaise
# approximation (en 2008, les emprunts d'État ont monté quand les actions
# chutaient). On utilise un fonds de la même catégorie, coté depuis 2007 au plus tard.
PROXIES_SECTEURS = {
    "Obligations d'État": "IEF", "Obligations indexées sur l'inflation": "TIP",
    "Obligations d'entreprises": "LQD", "Obligations à haut rendement": "HYG",
    "Obligations émergentes": "EMB", "Or": "GLD",
}


def _proxy(ligne):
    """Indice (ou fonds) servant d'approximation pour une ligne sans historique."""
    if ligne.get("classe", "Actions") != "Actions" and ligne.get("secteur") in PROXIES_SECTEURS:
        return PROXIES_SECTEURS[ligne.get("secteur")]
    return PROXIES_REGIONS.get(ligne.get("region"), PROXY_PAR_DEFAUT)


def telecharger_historique_long(tickers):
    """Cours depuis 2008 (cache séparé : data/cache_stress.csv)."""
    tous = sorted(set(tickers) | set(PROXIES_REGIONS.values()) | set(PROXIES_SECTEURS.values()))
    debut = pd.Timestamp(SCENARIOS_HISTORIQUES[0][1]) - pd.Timedelta(days=15)
    return obtenir_historique(tous, debut, chemin_cache=CHEMIN_CACHE_STRESS)


def _variation(serie, debut, fin):
    """Variation d'un cours entre deux dates (dernier cours connu à chaque date)."""
    serie = serie.dropna()
    if serie.empty or serie.index[0] > pd.Timestamp(debut) + pd.Timedelta(days=7):
        return None                        # le titre n'existait pas encore
    v0, v1 = serie.asof(pd.Timestamp(debut)), serie.asof(pd.Timestamp(fin))
    if pd.isna(v0) or pd.isna(v1) or v0 <= 0:
        return None
    return v1 / v0 - 1


def scenarios_historiques(positions, prix_longs):
    """Applique chaque crise passée au portefeuille actuel.

    positions  : tableau des positions (poids_pct, region, valeur)
    prix_longs : cours historiques longs (titres + indices régionaux)

    Renvoie (resume, detail) :
      resume : une ligne par scénario (perte en %, en euros, part estimée par proxy)
      detail : pour chaque scénario et chaque ligne, la variation utilisée et sa source
    """
    poids = positions["poids_pct"] / 100
    valeur = positions["valeur"].sum()
    resume, detail = [], []
    for nom, debut, fin in SCENARIOS_HISTORIQUES:
        total, part_proxy = 0.0, 0.0
        for ticker, ligne in positions.iterrows():
            variation = _variation(prix_longs[ticker], debut, fin) if ticker in prix_longs else None
            source = "titre"
            if variation is None:
                proxy = _proxy(ligne)
                variation = _variation(prix_longs[proxy], debut, fin) if proxy in prix_longs else None
                if variation is None and PROXY_PAR_DEFAUT in prix_longs:
                    proxy = PROXY_PAR_DEFAUT
                    variation = _variation(prix_longs[proxy], debut, fin)
                source = f"indice {proxy}"
                part_proxy += poids[ticker]
            variation = variation if variation is not None else 0.0
            total += poids[ticker] * variation
            detail.append({"scenario": nom, "ticker": ticker, "nom": ligne["nom"],
                           "variation": variation, "source": source})
        resume.append({"scenario": nom, "debut": pd.Timestamp(debut), "fin": pd.Timestamp(fin),
                       "variation": total, "perte_euros": total * valeur, "part_proxy": part_proxy})
    return pd.DataFrame(resume), pd.DataFrame(detail)


def scenarios_hypothetiques(positions, beta, chocs_actions=(-0.10, -0.20, -0.35), choc_dollar=-0.10,
                            choc_taux=0.01):
    """Chocs simples :
    - baisse des marchés actions de X % : variation du portefeuille ≈ β × X ;
    - baisse du dollar : variation = choc × part des titres cotés en dollars ;
    - hausse des taux de 1 point : chaque fonds obligataire perd environ
      duration × 1 % (la duration mesure la sensibilité d'une obligation aux taux).
    """
    valeur = positions["valeur"].sum()
    lignes = []
    for choc in chocs_actions:
        v = beta * choc
        lignes.append({"scenario": f"Baisse des actions de {abs(choc):.0%}".replace(".", ","),
                       "hypothese": f"bêta {beta:.2f} × {choc:.0%}".replace(".", ","),
                       "variation": v, "perte_euros": v * valeur})
    if "devise" in positions.columns:
        part_usd = positions.loc[positions["devise"] == "USD", "valeur"].sum() / valeur
        v = choc_dollar * part_usd
        lignes.append({"scenario": f"Baisse du dollar de {abs(choc_dollar):.0%}",
                       "hypothese": f"{part_usd:.0%} du portefeuille en dollars",
                       "variation": v, "perte_euros": v * valeur})
    if "duration" in positions.columns and positions["duration"].notna().any():
        poids = positions["valeur"] / valeur
        v = -choc_taux * float((poids * positions["duration"].fillna(0.0)).sum())
        duration_moyenne = float((poids * positions["duration"].fillna(0.0)).sum()
                                 / poids[positions["duration"].notna()].sum())
        lignes.append({"scenario": f"Hausse des taux de {choc_taux * 100:.0f} point",
                       "hypothese": f"duration moyenne des obligations {duration_moyenne:.1f} ans".replace(".", ","),
                       "variation": v, "perte_euros": v * valeur})
    return pd.DataFrame(lignes)
