"""
simulation.py — Projection de la valeur future du portefeuille (Monte-Carlo).

Principe de la méthode de Monte-Carlo :
    On ne peut pas prédire LE futur, mais on peut simuler des MILLIERS de
    futurs possibles, tous cohérents avec le rendement et le risque du
    portefeuille. On regarde ensuite la distribution des résultats :
      - la médiane (1 chance sur 2 de faire mieux) ;
      - un scénario défavorable (5e percentile : 1 chance sur 20 de faire pire) ;
      - un scénario favorable (95e percentile) ;
      - la probabilité de perdre de l'argent, d'atteindre un objectif...

Deux méthodes de simulation, au choix :
    1. "normale" : mouvement brownien géométrique (le modèle de Black-Scholes).
       Chaque mois, le rendement est tiré dans une loi normale.
    2. "historique" (bootstrap) : chaque mois est construit en tirant au
       hasard 21 VRAIS rendements quotidiens du portefeuille. On garde ainsi
       les "queues épaisses" réelles (krachs plus fréquents que la loi normale).

Le pas de temps est le MOIS (et non le jour) : c'est suffisant pour une
projection à plusieurs années, et 20 fois plus rapide.
"""

import numpy as np
import pandas as pd

JOURS_BOURSE_PAR_AN = 252
JOURS_PAR_MOIS = 21
PERCENTILES = [5, 25, 50, 75, 95]
TAILLE_ECHANTILLON = 400      # scénarios conservés en entier (pour le nuage de points)

# Tranches de probabilité utilisées pour colorer le nuage de points
TRANCHES = [
    "5 % les plus défavorables",
    "Défavorable (5 à 25 %)",
    "Central (25 à 75 %)",
    "Favorable (75 à 95 %)",
    "5 % les plus favorables",
]


def classer_tranches(valeurs, p5, p25, p75, p95):
    """Classe chaque valeur dans une tranche de probabilité (numéro 0 à 4).

    Exemple : une valeur sous le 5e percentile fait partie des 5 % de
    scénarios les plus défavorables à cette date -> tranche 0.
    """
    valeurs = np.asarray(valeurs)
    return np.select([valeurs < p5, valeurs < p25, valeurs <= p75, valeurs <= p95], [0, 1, 2, 3], default=4)


def parametres_historiques(rendements):
    """Rendement annuel moyen et volatilité annuelle, à partir des rendements
    quotidiens du portefeuille (ceux du TWR, calculés à l'étape 4)."""
    mu = rendements.mean() * JOURS_BOURSE_PAR_AN
    sigma = rendements.std() * np.sqrt(JOURS_BOURSE_PAR_AN)
    return float(mu), float(sigma)


def _rendements_mensuels_normaux(generateur, mu, sigma, nb_simulations, nb_mois):
    """Log-rendements mensuels selon un mouvement brownien géométrique.

    Sur un mois (dt = 1/12 an) :
        log-rendement ~ Normale( (μ − σ²/2) × dt , σ × √dt )

    Pourquoi "− σ²/2" ? Le rendement moyen μ est une moyenne ARITHMÉTIQUE.
    Or la croissance composée est plus faible : +50 % puis −50 % donne
    une moyenne de 0 %, mais on finit à 0,75 (−25 %). Le terme −σ²/2
    corrige cet effet (lemme d'Itô).
    """
    dt = 1 / 12
    return generateur.normal((mu - sigma ** 2 / 2) * dt, sigma * np.sqrt(dt),
                             size=(nb_simulations, nb_mois))


def _rendements_mensuels_historiques(generateur, rendements, mu, nb_simulations, nb_mois):
    """Log-rendements mensuels par rééchantillonnage ("bootstrap") des vrais jours.

    Chaque mois = somme de 21 log-rendements quotidiens tirés au hasard
    (avec remise) parmi l'historique. Si un rendement annuel μ est imposé,
    on recentre les rendements quotidiens pour que leur moyenne corresponde
    à μ, en gardant leur forme (queues épaisses, asymétrie).
    """
    log_r = np.log1p(np.asarray(rendements, dtype=float))
    if mu is not None:
        sigma = np.std(np.expm1(log_r), ddof=1) * np.sqrt(JOURS_BOURSE_PAR_AN)
        cible = (mu - sigma ** 2 / 2) / JOURS_BOURSE_PAR_AN
        log_r = log_r - log_r.mean() + cible
    mensuels = np.empty((nb_simulations, nb_mois))
    for mois in range(nb_mois):          # une boucle par mois : peu de mémoire utilisée
        tirages = generateur.choice(log_r, size=(nb_simulations, JOURS_PAR_MOIS))
        mensuels[:, mois] = tirages.sum(axis=1)
    return mensuels


def simuler(valeur_initiale, mu, sigma, annees=10, versement_mensuel=0.0,
            nb_simulations=5000, methode="normale", rendements_historiques=None,
            objectif=None, date_depart=None, graine=42):
    """Simule l'évolution du portefeuille mois par mois.

    valeur_initiale   : valeur actuelle du portefeuille (€)
    mu, sigma         : rendement annuel moyen et volatilité annuelle supposés
    annees            : horizon de la projection
    versement_mensuel : somme ajoutée à la fin de chaque mois (€)
    methode           : "normale" ou "historique"
    objectif          : montant à atteindre (€), facultatif
    graine            : fixe le hasard pour que les résultats soient reproductibles

    Renvoie un dictionnaire avec les percentiles mois par mois et les
    statistiques de la valeur finale.
    """
    nb_mois = int(round(annees * 12))
    generateur = np.random.default_rng(graine)

    if methode == "normale":
        log_r = _rendements_mensuels_normaux(generateur, mu, sigma, nb_simulations, nb_mois)
    elif methode == "historique":
        if rendements_historiques is None or len(rendements_historiques) < 20:
            raise ValueError("La méthode historique nécessite l'historique des rendements quotidiens.")
        log_r = _rendements_mensuels_historiques(generateur, rendements_historiques, mu,
                                                 nb_simulations, nb_mois)
    else:
        raise ValueError(f"Méthode inconnue : {methode}")

    # Évolution mois par mois : valeur × croissance du mois + versement.
    croissance = np.exp(log_r)
    valeurs = np.empty((nb_simulations, nb_mois + 1))
    valeurs[:, 0] = valeur_initiale
    for mois in range(nb_mois):
        valeurs[:, mois + 1] = valeurs[:, mois] * croissance[:, mois] + versement_mensuel

    # Dates de l'axe du temps (fin de chaque mois à partir d'aujourd'hui).
    depart = pd.Timestamp(date_depart) if date_depart is not None else pd.Timestamp.today().normalize()
    dates = [depart + pd.DateOffset(months=m) for m in range(nb_mois + 1)]

    trajectoires = pd.DataFrame(
        np.percentile(valeurs, PERCENTILES, axis=0).T,
        index=pd.DatetimeIndex(dates), columns=[f"p{p}" for p in PERCENTILES],
    )
    trajectoires["apports"] = valeur_initiale + versement_mensuel * np.arange(nb_mois + 1)

    # Un échantillon de scénarios complets (les tirages sont déjà aléatoires :
    # les premiers suffisent), pour dessiner le nuage de points.
    echantillon = pd.DataFrame(valeurs[:TAILLE_ECHANTILLON].T, index=trajectoires.index)

    finales = valeurs[:, -1]
    total_apporte = trajectoires["apports"].iloc[-1]
    resultat = {
        "trajectoires": trajectoires,
        "echantillon": echantillon,
        "valeurs_finales": finales,
        "total_apporte": float(total_apporte),
        "mediane": float(np.median(finales)),
        "moyenne": float(finales.mean()),
        "p5": float(np.percentile(finales, 5)),
        "p95": float(np.percentile(finales, 95)),
        "proba_perte": float((finales < total_apporte).mean()),
        "proba_objectif": float((finales >= objectif).mean()) if objectif else None,
        "objectif": objectif,
        "parametres": {"mu": mu, "sigma": sigma, "annees": annees, "versement_mensuel": versement_mensuel,
                       "methode": methode, "nb_simulations": nb_simulations},
    }
    # Rendement annualisé médian (sans versements, pour pouvoir l'interpréter).
    if versement_mensuel == 0 and valeur_initiale > 0:
        resultat["rendement_annualise_median"] = (resultat["mediane"] / valeur_initiale) ** (1 / annees) - 1
    return resultat


def points_nuage(sim, graine=0):
    """Prépare le nuage de points : la valeur de chaque scénario de l'échantillon
    à intervalles réguliers (tous les 6 mois, ou tous les ans au-delà de 15 ans),
    avec sa tranche de probabilité à cette date.

    Les points d'une même date sont légèrement décalés horizontalement
    ("jitter") pour ne pas s'empiler en une seule colonne illisible.
    """
    t, e = sim["trajectoires"], sim["echantillon"]
    nb_mois = len(t) - 1
    pas = 6 if nb_mois <= 180 else 12
    indices = list(range(pas, nb_mois + 1, pas))
    if not indices or indices[-1] != nb_mois:
        indices.append(nb_mois)

    generateur = np.random.default_rng(graine)
    largeur_jours = pas * 30 * 0.35                   # décalage maximal de part et d'autre
    morceaux = []
    for i in indices:
        valeurs = e.iloc[i].to_numpy()
        tranches = classer_tranches(valeurs, t["p5"].iloc[i], t["p25"].iloc[i],
                                    t["p75"].iloc[i], t["p95"].iloc[i])
        decalage = pd.to_timedelta(generateur.uniform(-1, 1, len(valeurs)) * largeur_jours, unit="D")
        morceaux.append(pd.DataFrame({
            "date": t.index[i] + decalage,
            "date_reelle": t.index[i],
            "valeur": valeurs,
            "tranche": tranches,
            "scenario": np.arange(1, len(valeurs) + 1),
        }))
    return pd.concat(morceaux, ignore_index=True)
