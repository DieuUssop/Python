"""
optimisation.py — L'optimisation de portefeuille de Markowitz (1952).

L'idée de Harry Markowitz (prix Nobel d'économie 1990) :
    Un investisseur ne regarde pas seulement le rendement, mais aussi le
    RISQUE. Grâce à la diversification, on peut réduire le risque d'un
    portefeuille sans réduire son rendement, en combinant des titres qui
    ne bougent pas exactement ensemble (corrélation < 1).

Ce fichier calcule :
    1. le rendement espéré et la matrice de covariance des titres ;
    2. le portefeuille de VARIANCE MINIMALE (le moins risqué possible) ;
    3. le portefeuille de SHARPE MAXIMAL (le "portefeuille tangent") ;
    4. la FRONTIÈRE EFFICIENTE : pour chaque niveau de rendement, le
       portefeuille le moins risqué ;
    5. un nuage de portefeuilles tirés au hasard, pour visualiser.

Contraintes retenues (réalistes pour un particulier) :
    - pas de vente à découvert : chaque poids ≥ 0 ;
    - tout le capital est investi : somme des poids = 100 % ;
    - un poids maximal par titre (ex. 30 %) pour éviter de tout mettre
      sur un seul titre.

L'optimisation numérique utilise scipy.optimize.minimize (méthode SLSQP),
qui sait gérer ce type de contraintes.
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize

JOURS_BOURSE_PAR_AN = 252


# ======================================================================
# 1. Les paramètres : rendements espérés et covariances
# ======================================================================
def estimer_parametres(prix_hist, tickers):
    """Estime, à partir de l'historique, les deux ingrédients de Markowitz.

    μ (mu)   : rendement annuel espéré de chaque titre
               = moyenne des rendements quotidiens × 252
    Σ (sigma): matrice de covariance annuelle
               = covariance des rendements quotidiens × 252
               (sur la diagonale : la variance de chaque titre ;
                ailleurs : comment deux titres varient ensemble)

    ⚠️ Hypothèse forte : on suppose que le passé est représentatif du futur.
    """
    rendements = prix_hist[list(tickers)].pct_change().dropna()
    mu = rendements.mean() * JOURS_BOURSE_PAR_AN
    cov = rendements.cov() * JOURS_BOURSE_PAR_AN
    return mu, cov


def performance(poids, mu, cov):
    """Rendement et volatilité d'un portefeuille de poids donnés.

    rendement  = Σ poids_i × μ_i              = wᵀ μ
    variance   = Σ Σ poids_i × poids_j × cov_ij = wᵀ Σ w
    volatilité = √variance

    La formule de la variance est le cœur de la diversification : quand les
    covariances sont faibles, la variance du portefeuille est plus petite
    que la moyenne des variances des titres.
    """
    w = np.asarray(poids)
    rendement = float(w @ np.asarray(mu))
    volatilite = float(np.sqrt(w @ np.asarray(cov) @ w))
    return rendement, volatilite


def sharpe(poids, mu, cov, taux_sans_risque):
    rendement, volatilite = performance(poids, mu, cov)
    return (rendement - taux_sans_risque) / volatilite


# ======================================================================
# 2. Outil commun : l'optimiseur sous contraintes
# ======================================================================
def _optimiser(fonction_a_minimiser, n, poids_max, contraintes_en_plus=()):
    """Cherche les poids qui MINIMISENT une fonction, sous contraintes.

    - bounds       : chaque poids entre 0 et poids_max
    - constraints  : somme des poids = 1 (+ éventuellement d'autres)
    - point de départ : poids égaux (1/n chacun)
    """
    if n * poids_max < 1 - 1e-9:
        raise ValueError(
            f"Impossible : avec {n} titres et un poids maximal de {poids_max:.0%}, "
            f"on ne peut pas investir 100 % du capital."
        )
    contraintes = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}, *contraintes_en_plus]
    resultat = minimize(
        fonction_a_minimiser,
        x0=np.full(n, 1 / n),
        method="SLSQP",
        bounds=[(0, poids_max)] * n,
        constraints=contraintes,
        options={"maxiter": 500, "ftol": 1e-12},
    )
    if not resultat.success:
        raise RuntimeError(f"L'optimisation n'a pas convergé : {resultat.message}")
    poids = np.clip(resultat.x, 0, None)
    return poids / poids.sum()     # on nettoie les minuscules erreurs numériques


# ======================================================================
# 3. Les deux portefeuilles remarquables
# ======================================================================
def variance_minimale(mu, cov, poids_max=1.0):
    """Le portefeuille le MOINS RISQUÉ possible (volatilité minimale)."""
    cov_np = np.asarray(cov)
    return _optimiser(lambda w: w @ cov_np @ w, len(mu), poids_max)


def sharpe_maximal(mu, cov, taux_sans_risque, poids_max=1.0):
    """Le portefeuille qui offre le MEILLEUR RENDEMENT PAR UNITÉ DE RISQUE.

    C'est le "portefeuille tangent" : en le combinant avec le placement
    sans risque, on obtient la meilleure droite possible (la "Capital
    Market Line"). On maximise le Sharpe en minimisant son opposé.
    """
    return _optimiser(lambda w: -sharpe(w, mu, cov, taux_sans_risque), len(mu), poids_max)


def _rendement_maximal_atteignable(mu, poids_max):
    """Rendement le plus haut possible avec les contraintes : on remplit
    les titres du plus rentable au moins rentable, jusqu'à poids_max chacun."""
    reste, total = 1.0, 0.0
    for m in sorted(np.asarray(mu), reverse=True):
        part = min(poids_max, reste)
        total += part * m
        reste -= part
        if reste <= 1e-12:
            break
    return total


# ======================================================================
# 4. La frontière efficiente
# ======================================================================
def frontiere_efficiente(mu, cov, poids_max=1.0, nb_points=40):
    """Pour une série de rendements cibles, le portefeuille le moins risqué.

    On part du rendement du portefeuille de variance minimale (en dessous,
    les portefeuilles sont "inefficaces" : on peut faire mieux à risque égal)
    jusqu'au rendement maximal atteignable.

    Renvoie un tableau : rendement, volatilité, et les poids de chaque point.
    """
    cov_np, mu_np = np.asarray(cov), np.asarray(mu)
    r_min = performance(variance_minimale(mu, cov, poids_max), mu, cov)[0]
    r_max = _rendement_maximal_atteignable(mu, poids_max)

    points = []
    for cible in np.linspace(r_min, r_max, nb_points):
        contrainte = {"type": "eq", "fun": lambda w, c=cible: w @ mu_np - c}
        try:
            w = _optimiser(lambda w: w @ cov_np @ w, len(mu), poids_max, [contrainte])
        except RuntimeError:
            continue                      # point impossible : on l'ignore
        r, v = performance(w, mu, cov)
        points.append({"rendement": r, "volatilite": v, **dict(zip(mu.index, w))})
    return pd.DataFrame(points)


# ======================================================================
# 5. Portefeuilles aléatoires (pour visualiser le nuage des possibles)
# ======================================================================
def portefeuilles_aleatoires(mu, cov, taux_sans_risque, nombre=4000, graine=42):
    """Tire des poids au hasard (loi de Dirichlet : positifs, somme = 1).

    Tous ces portefeuilles se situent SOUS ou SUR la frontière efficiente :
    c'est une belle vérification visuelle de l'optimisation.
    """
    generateur = np.random.default_rng(graine)
    poids = generateur.dirichlet(np.ones(len(mu)), size=nombre)
    rendements = poids @ np.asarray(mu)
    volatilites = np.sqrt(np.einsum("ij,jk,ik->i", poids, np.asarray(cov), poids))
    return pd.DataFrame({
        "rendement": rendements,
        "volatilite": volatilites,
        "sharpe": (rendements - taux_sans_risque) / volatilites,
    })


# ======================================================================
# Tout en une fois
# ======================================================================
def optimiser_portefeuille(prix_hist, positions, taux_sans_risque, poids_max=0.30,
                           nb_points=40):
    """Compare le portefeuille actuel aux portefeuilles optimaux.

    positions : le tableau de Portfolio.valoriser() (poids actuels, valeur).
    Renvoie un dictionnaire avec les poids, les performances et la frontière.
    """
    tickers = list(positions.index)
    mu, cov = estimer_parametres(prix_hist, tickers)

    poids_actuels = (positions["poids_pct"] / 100).reindex(tickers).to_numpy()
    w_min = variance_minimale(mu, cov, poids_max)
    w_sharpe = sharpe_maximal(mu, cov, taux_sans_risque, poids_max)

    def resume(w):
        r, v = performance(w, mu, cov)
        return {"rendement": r, "volatilite": v, "sharpe": (r - taux_sans_risque) / v}

    poids = pd.DataFrame({
        "nom": positions["nom"],
        "actuel": poids_actuels,
        "variance_min": w_min,
        "sharpe_max": w_sharpe,
    }, index=tickers)

    # Montants à acheter (+) ou vendre (−) pour atteindre le portefeuille
    # de Sharpe maximal, à valeur totale inchangée (hors frais).
    valeur_totale = positions["valeur"].sum()
    poids["ecart_euros_sharpe_max"] = (poids["sharpe_max"] - poids["actuel"]) * valeur_totale

    return {
        "mu": mu,
        "cov": cov,
        "poids": poids,
        "actuel": resume(poids_actuels),
        "variance_min": resume(w_min),
        "sharpe_max": resume(w_sharpe),
        "frontiere": frontiere_efficiente(mu, cov, poids_max, nb_points),
        "aleatoires": portefeuilles_aleatoires(mu, cov, taux_sans_risque),
        "titres_seuls": pd.DataFrame({"rendement": mu, "volatilite": np.sqrt(np.diag(cov)),
                                      "nom": positions["nom"]}),
        "taux_sans_risque": taux_sans_risque,
        "poids_max": poids_max,
    }
