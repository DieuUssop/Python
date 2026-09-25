"""
attribution.py — Attribution de performance (modèle de Brinson-Fachler, 1985).

Question : le portefeuille a fait mieux (ou moins bien) que son indice de
référence. POURQUOI ? Le modèle décompose l'écart de rendement, région par
région, en trois effets :

  Effet ALLOCATION  = (wp − wb) × (rb − Rb)
      A-t-on surpondéré les régions qui ont fait mieux que l'indice global ?
  Effet SÉLECTION   = wb × (rp − rb)
      Dans chaque région, a-t-on choisi de meilleurs titres que l'indice ?
  Effet INTERACTION = (wp − wb) × (rp − rb)
      Effet croisé : surpondérer une région où l'on a aussi bien choisi.

  avec wp, wb : poids de la région dans le portefeuille et dans l'indice
       rp, rb : rendement de la région dans le portefeuille et dans l'indice
       Rb     : rendement total de l'indice

  Propriété : la somme des trois effets sur toutes les régions est égale
  à l'écart de rendement Rp − Rb (vérifié par un test automatique).

Mise en œuvre :
  - calcul MOIS PAR MOIS, avec les poids du début de chaque mois ;
  - les effets mensuels sont ensuite "reliés" par la méthode de Cariño (1999) :
    une simple somme ne tombe pas juste, car les rendements se composent
    (+10 % puis +10 % = +21 %, et non +20 %). Cariño pondère chaque mois par
        kₜ = [ln(1 + Rpₜ) − ln(1 + Rbₜ)] / (Rpₜ − Rbₜ)   divisé par
        K  = [ln(1 + Rp)  − ln(1 + Rb) ] / (Rp − Rb)
    de sorte que la somme des effets reliés est EXACTEMENT égale à Rp − Rb ;
  - indice de référence : poids régionaux du MSCI ACWI IMI (30/06/2026) et
    rendements d'un indice boursier par région, convertis en euros.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from .devises import (convertir_prix_historiques, detecter_devises, devises_etrangeres,
                      ticker_change)
from .market_data import obtenir_historique
from .stress import PROXIES_REGIONS

CHEMIN_CACHE_ATTRIBUTION = Path(__file__).resolve().parent.parent / "data" / "cache_attribution.csv"

# Poids régionaux de l'indice MSCI ACWI IMI au 30/06/2026 (source : MSCI, "A Complete
# Geographic Breakdown of the MSCI ACWI IMI"). Europe = EMEA hors Royaume-Uni et Suisse.
# Les poids sont renormalisés pour que leur somme fasse 100 %.
POIDS_INDICE_BRUTS = {
    "États-Unis": 62.7, "Europe": 8.7, "Japon": 5.6, "Royaume-Uni": 3.1, "Émergents": 12.3,
    "Suisse": 1.9, "Asie-Pacifique": 2.3, "Canada": 3.0,
}
POIDS_INDICE = {r: p / sum(POIDS_INDICE_BRUTS.values()) for r, p in POIDS_INDICE_BRUTS.items()}


# ----------------------------------------------------------------------
# 1. Le cœur du modèle, sur une période
# ----------------------------------------------------------------------
def brinson_fachler(wp, rp, wb, rb):
    """Effets d'allocation, de sélection et d'interaction pour une période.

    wp, rp : poids et rendements des régions dans le portefeuille (Series)
    wb, rb : poids et rendements des régions dans l'indice (Series)
    Une région absente de l'indice (wb = 0) prend rb = Rb ; une région
    absente du portefeuille (wp = 0) prend rp = rb.
    """
    regions = sorted(set(wp.index) | set(wb.index))
    wp = wp.reindex(regions).fillna(0.0)
    wb = wb.reindex(regions).fillna(0.0)
    Rb = float((wb * rb.reindex(regions).fillna(0.0)).sum())
    rb = rb.reindex(regions).fillna(Rb)
    rp = rp.reindex(regions)
    rp = rp.where(wp > 0, rb).fillna(rb)
    effets = pd.DataFrame({
        "allocation": (wp - wb) * (rb - Rb),
        "selection": wb * (rp - rb),
        "interaction": (wp - wb) * (rp - rb),
    })
    Rp = float((wp * rp).sum())
    return effets, Rp, Rb


# ----------------------------------------------------------------------
# 2. Rendements mensuels des indices régionaux, en euros
# ----------------------------------------------------------------------
def rendements_indices(debut, regions=None):
    """Télécharge un indice par région et le convertit en euros.
    Renvoie les cours quotidiens en euros (une colonne par région)."""
    regions = regions or list(POIDS_INDICE)
    proxies = {r: PROXIES_REGIONS[r] for r in regions if r in PROXIES_REGIONS}
    info = detecter_devises(list(proxies.values()))
    etrangeres = devises_etrangeres(info)
    change = [ticker_change(d) for d in etrangeres]
    brut, _ = obtenir_historique(list(proxies.values()) + change, debut,
                                 chemin_cache=CHEMIN_CACHE_ATTRIBUTION)
    taux = brut[change].copy()
    taux.columns = etrangeres
    cours = convertir_prix_historiques(brut[list(proxies.values())].ffill(), info, taux.ffill())
    return pd.DataFrame({r: cours[t] for r, t in proxies.items()})


# ----------------------------------------------------------------------
# 3. Attribution mois par mois
# ----------------------------------------------------------------------
def _coefficient_carino(rp, rb):
    """k = [ln(1 + rp) − ln(1 + rb)] / (rp − rb), et 1 / (1 + rp) si rp = rb."""
    if abs(rp - rb) < 1e-12:
        return 1 / (1 + rp)
    return (np.log1p(rp) - np.log1p(rb)) / (rp - rb)


def fins_de_mois(index):
    """Dernier jour de bourse de chaque mois."""
    serie = pd.Series(index, index=index)
    return list(serie.groupby(index.to_period("M")).last())


def attribution_mensuelle(valeur_par_titre, prix_hist, regions_titres, cours_indices,
                          poids_indice=POIDS_INDICE):
    """Attribution de Brinson-Fachler, mois par mois, puis cumulée.

    valeur_par_titre : valeur de chaque ligne chaque jour (euros)
    prix_hist        : cours de chaque titre chaque jour (euros)
    regions_titres   : {ticker: région}
    cours_indices    : cours des indices régionaux en euros (colonne = région)

    Renvoie un dictionnaire :
      "par_region" : poids moyens, rendements et effets cumulés par région
      "mensuel"    : effets et rendements de chaque mois
      "Rp", "Rb"   : rendements composés du portefeuille (sur ses positions) et de l'indice
    """
    dates = fins_de_mois(valeur_par_titre.index)
    prix = prix_hist.reindex(valeur_par_titre.index).ffill()
    indices = cours_indices.reindex(cours_indices.index.union(valeur_par_titre.index)).ffill()
    wb = pd.Series(poids_indice)

    mois, effets_mois = [], []
    poids_p_hist, rend_p_hist, rend_b_hist = [], [], []
    for d0, d1 in zip(dates[:-1], dates[1:]):
        v0 = valeur_par_titre.loc[d0]
        v0 = v0[v0 > 0]
        if v0.sum() <= 0:
            continue
        w = v0 / v0.sum()
        r = prix.loc[d1, w.index] / prix.loc[d0, w.index] - 1
        region = pd.Series({t: regions_titres.get(t, "Non classé") for t in w.index})
        wp = w.groupby(region).sum()
        rp = (w * r).groupby(region).sum() / wp
        rb = (indices.loc[d1] / indices.loc[d0] - 1).reindex(wb.index)
        effets, Rp, Rb = brinson_fachler(wp, rp, wb, rb)
        effets_mois.append(effets.assign(mois=d1))
        mois.append({"mois": d1, "Rp": Rp, "Rb": Rb, "ecart": Rp - Rb,
                     "allocation": effets["allocation"].sum(), "selection": effets["selection"].sum(),
                     "interaction": effets["interaction"].sum()})
        poids_p_hist.append(wp.rename(d1))
        rend_p_hist.append(rp.rename(d1))
        rend_b_hist.append(rb.rename(d1))

    if not mois:
        raise ValueError("Historique trop court : il faut au moins deux fins de mois.")
    mensuel = pd.DataFrame(mois).set_index("mois")
    Rp_total = float(np.prod(1 + mensuel["Rp"]) - 1)
    Rb_total = float(np.prod(1 + mensuel["Rb"]) - 1)

    # Lissage de Cariño : chaque mois est pondéré par k_t / K
    K = _coefficient_carino(Rp_total, Rb_total)
    facteurs = [_coefficient_carino(m["Rp"], m["Rb"]) / K for m in mois]
    effets_relies = [e.assign(**{c: e[c] * f for c in ["allocation", "selection", "interaction"]})
                     for e, f in zip(effets_mois, facteurs)]
    for colonne in ["allocation", "selection", "interaction"]:
        mensuel[colonne + "_relie"] = mensuel[colonne] * facteurs
    tous = pd.concat(effets_relies)
    cumul = tous.groupby(level=0)[["allocation", "selection", "interaction"]].sum()

    poids_p = pd.DataFrame(poids_p_hist).fillna(0.0)
    rend_p = pd.DataFrame(rend_p_hist)
    rend_b = pd.DataFrame(rend_b_hist)
    par_region = pd.DataFrame({
        "poids_portefeuille": poids_p.mean(),
        "poids_indice": wb,
        "rendement_portefeuille": (1 + rend_p.fillna(0.0)).prod() - 1,
        "rendement_indice": (1 + rend_b.fillna(0.0)).prod() - 1,
    }).join(cumul, how="outer").fillna(0.0)
    par_region["total"] = par_region[["allocation", "selection", "interaction"]].sum(axis=1)
    par_region = par_region.sort_values("poids_indice", ascending=False)

    return {
        "par_region": par_region,
        "mensuel": mensuel,
        "Rp": Rp_total,
        "Rb": Rb_total,
        "effets": par_region[["allocation", "selection", "interaction"]].sum(),
        "somme_effets": float(par_region["total"].sum()),      # = Rp − Rb grâce à Cariño
    }


def attribution_poche_actions(res, cours_indices, poids_indice=None):
    """Attribution de la POCHE ACTIONS du portefeuille.

    L'indice de référence est un indice d'actions : pour un portefeuille
    diversifié (actions + obligations + or), on compare donc seulement les
    actions à cet indice, comme le fait un gérant pour chaque "poche".
    Les obligations et l'or sont exclus du calcul.
    Le résultat contient en plus "part_actions" : poids actuel de la poche actions.
    """
    from .analyse import charger_referentiel      # import ici pour éviter un import circulaire
    referentiel = charger_referentiel()
    valeurs = res["valeur_par_titre"]
    vide = pd.Series(dtype=object)
    regions = referentiel["region"] if "region" in referentiel.columns else vide
    classes = referentiel["classe"] if "classe" in referentiel.columns else vide
    actions = [t for t in valeurs.columns if classes.get(t, "Actions") == "Actions"]
    if not actions:
        raise ValueError("aucune action dans le portefeuille (l'indice de référence est un indice actions)")
    resultat = attribution_mensuelle(valeurs[actions], res["prix_hist"],
                                     {t: regions.get(t, "Non classé") for t in actions},
                                     cours_indices, poids_indice or POIDS_INDICE)
    derniere = valeurs.iloc[-1]
    resultat["part_actions"] = float(derniere[actions].sum() / derniere.sum()) if derniere.sum() else 1.0
    return resultat
