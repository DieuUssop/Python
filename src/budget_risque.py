"""
budget_risque.py — D'où vient le risque du portefeuille ? Et l'allocation en
"parité des risques" (risk parity).

1. CONTRIBUTION AU RISQUE
   Le poids d'une ligne ne dit pas quelle part du RISQUE elle apporte : une
   action très volatile et très corrélée aux autres pèse plus dans le risque
   que dans la valeur. Pour chaque ligne i :

       contribution marginale   CMᵢ = (Σ w)ᵢ / σₚ
       contribution au risque   CRᵢ = wᵢ × CMᵢ
       en pourcentage           CRᵢ / σₚ      (la somme fait 100 %)

   Propriété d'Euler : Σ CRᵢ = σₚ (vérifiée par un test automatique).

2. PARITÉ DES RISQUES
   Allocation où chaque ligne contribue AUTANT au risque. Elle n'utilise
   PAS les rendements espérés, très mal estimés (voir la limite de
   Markowitz) : seulement les volatilités et les corrélations.
   Calcul (méthode de Spinu, 2013) : on minimise
       ½ wᵀΣw − (1/n) × Σ ln(wᵢ)
   puis on renormalise les poids pour que leur somme fasse 100 %.

3. INDICATEURS DE DIVERSIFICATION
   - ratio de diversification = Σ wᵢσᵢ / σₚ (1 = aucune diversification) ;
   - nombre effectif de paris = 1 / Σ (CRᵢ/σₚ)² : "combien de lignes
     indépendantes" le portefeuille représente vraiment du point de vue du risque.
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from .optimisation import estimer_parametres, variance_minimale


def contributions(poids, cov):
    """Contributions de chaque ligne au risque (volatilité) du portefeuille."""
    w = np.asarray(poids, dtype=float)
    S = np.asarray(cov, dtype=float)
    sigma = float(np.sqrt(w @ S @ w))
    marginale = S @ w / sigma
    contribution = w * marginale
    return {"volatilite": sigma, "marginale": marginale, "contribution": contribution,
            "part": contribution / sigma}


def parite_des_risques(cov):
    """Poids tels que chaque ligne apporte la même part du risque."""
    S = np.asarray(cov, dtype=float)
    n = len(S)
    depart = 1 / np.sqrt(np.diag(S))            # départ : inverse des volatilités
    depart = depart / depart.sum()
    objectif = lambda w: 0.5 * w @ S @ w - np.sum(np.log(w)) / n
    gradient = lambda w: S @ w - 1 / (n * w)
    res = minimize(objectif, depart, jac=gradient, method="L-BFGS-B",
                   bounds=[(1e-9, None)] * n, options={"maxiter": 2000, "ftol": 1e-15, "gtol": 1e-12})
    w = res.x / res.x.sum()
    return w


def indicateurs(poids, cov, mu, taux_sans_risque):
    """Rendement espéré, volatilité, Sharpe et indicateurs de diversification."""
    w = np.asarray(poids, dtype=float)
    c = contributions(w, cov)
    vols = np.sqrt(np.diag(np.asarray(cov)))
    rendement = float(w @ np.asarray(mu))
    return {
        "rendement": rendement,
        "volatilite": c["volatilite"],
        "sharpe": (rendement - taux_sans_risque) / c["volatilite"],
        "ratio_diversification": float(w @ vols / c["volatilite"]),
        "nb_effectif_paris": float(1 / np.sum(c["part"] ** 2)),
        "part_max": float(c["part"].max()),
    }


def analyse_budget_risque(prix_hist, positions, taux_sans_risque):
    """Contributions au risque du portefeuille actuel et comparaison avec
    trois allocations : équipondérée, parité des risques, variance minimale."""
    tickers = list(positions.index)
    mu, cov = estimer_parametres(prix_hist, tickers)
    poids_actuels = (positions["poids_pct"] / 100).reindex(tickers).to_numpy()
    c = contributions(poids_actuels, cov)

    par_ligne = pd.DataFrame({
        "nom": positions["nom"],
        "region": positions.get("region", "Non classé"),
        "poids": poids_actuels,
        "volatilite": np.sqrt(np.diag(cov)),
        "contribution": c["contribution"],
        "part_risque": c["part"],
    }, index=tickers)
    par_ligne["ratio_risque_poids"] = par_ligne["part_risque"] / par_ligne["poids"]
    par_region = par_ligne.groupby("region")[["poids", "part_risque"]].sum() \
        .sort_values("part_risque", ascending=False)

    allocations = {
        "Portefeuille actuel": poids_actuels,
        "Équipondéré": np.full(len(tickers), 1 / len(tickers)),
        "Parité des risques": parite_des_risques(cov),
        "Variance minimale": variance_minimale(mu, cov),
    }
    comparaison = pd.DataFrame({nom: indicateurs(w, cov, mu, taux_sans_risque)
                                for nom, w in allocations.items()}).T
    poids = pd.DataFrame(allocations, index=tickers)
    poids.insert(0, "nom", positions["nom"])
    return {"par_ligne": par_ligne.sort_values("part_risque", ascending=False),
            "par_region": par_region, "comparaison": comparaison, "poids": poids,
            "volatilite": c["volatilite"]}
