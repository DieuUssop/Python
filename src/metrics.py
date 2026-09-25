"""
metrics.py — Les indicateurs de performance et de risque.

Toutes les fonctions de ce fichier reçoivent le tableau "historique" produit
par Portfolio.historique() (étape 3), avec les colonnes :
    valeur, flux, apports_nets, gain

Indicateurs calculés :
    1. Rendements quotidiens "neutralisés" des apports
    2. TWR  : rendement pondéré par le temps (Time-Weighted Return)
    3. TRI  : taux de rendement interne (Money-Weighted Return)
    4. Volatilité annualisée
    5. Max drawdown (pire baisse depuis un plus haut)
    6. Rendements par année civile

Conventions (à rappeler dans le rapport) :
    - 252 jours de bourse par an pour annualiser la volatilité ;
    - 365 jours calendaires par an pour annualiser un rendement ;
    - achats, ventes et dividendes supposés faits en FIN de journée
      (au cours du jour).
"""

from statistics import NormalDist  # loi normale (module standard de Python)

import numpy as np
import pandas as pd

JOURS_BOURSE_PAR_AN = 252


# ======================================================================
# 1. Rendements quotidiens
# ======================================================================
def rendements_journaliers(histo):
    """Rendement de chaque jour, SANS l'effet des apports et des retraits.

    Problème : si j'achète pour 1 000 € aujourd'hui, la valeur du
    portefeuille monte de 1 000 €, mais je n'ai rien gagné. Il faut donc
    retirer l'effet des flux.

    Formule (pour le jour t) :
                valeur(t) − flux(t)
        r(t) = --------------------- − 1
                   valeur(t−1)

    Idée : on considère que les achats et les ventes se font au cours du
    jour, donc en FIN de journée. L'argent apporté aujourd'hui n'a pas encore
    "travaillé" : on le retire de la valeur du jour (et on rajoute l'argent
    retiré par une vente ou un dividende, car flux < 0 dans ce cas).

    Cas particulier : le tout premier jour (valeur de la veille = 0), on
    compare la valeur en fin de journée à l'argent apporté :
        r = valeur(t) / flux(t) − 1
    Ce rendement capte les frais d'achat et l'écart entre le prix payé et
    le cours de clôture.
    """
    # shift(1) décale d'une ligne : on obtient la valeur de la veille.
    # fill_value=0 : avant le 1er jour, le portefeuille valait 0.
    valeur_veille = histo["valeur"].shift(1, fill_value=0)
    flux = histo["flux"]

    # Cas général
    rendements = (histo["valeur"] - flux) / valeur_veille - 1

    # Premier jour (ou reprise après avoir tout vendu) : la veille valait 0.
    demarrage = (valeur_veille == 0) & (flux > 0)
    rendements[demarrage] = histo["valeur"][demarrage] / flux[demarrage] - 1

    # Les jours où rien n'était investi, le rendement n'a pas de sens.
    valides = (valeur_veille > 0) | demarrage
    return rendements[valides].rename("rendement")


def indice_base_100(rendements):
    """Transforme les rendements en un indice qui part de 100.

    Exemple : +10 % puis −5 %  ->  100 × 1,10 × 0,95 = 104,5
    C'est la courbe de "performance pure", comparable à un indice boursier.
    cumprod() = produit cumulé.
    """
    return 100 * (1 + rendements).cumprod()


# ======================================================================
# 2. TWR — rendement pondéré par le temps
# ======================================================================
def twr(rendements):
    """Rendement total pondéré par le temps, sur toute la période.

    TWR = (1 + r1) × (1 + r2) × ... × (1 + rn) − 1

    Il mesure la qualité des CHOIX D'INVESTISSEMENT, indépendamment du
    moment et du montant des apports. C'est la mesure utilisée par les
    gérants de fonds (norme GIPS) : un gérant ne choisit pas quand ses
    clients déposent de l'argent.
    """
    return (1 + rendements).prod() - 1


def annualiser(rendement_total, date_debut, date_fin):
    """Convertit un rendement sur une période en rendement "par an".

    rendement annualisé = (1 + rendement total) ^ (365 / nb de jours) − 1

    Exemple : +21 % en 2 ans  ->  1,21 ^ (1/2) − 1 = +10 % par an
    (et non 10,5 % : les gains se composent d'une année sur l'autre).
    """
    nb_jours = (pd.Timestamp(date_fin) - pd.Timestamp(date_debut)).days
    if nb_jours <= 0:
        return np.nan
    return (1 + rendement_total) ** (365 / nb_jours) - 1


# ======================================================================
# 3. TRI — taux de rendement interne (rendement pondéré par l'argent)
# ======================================================================
def tri(histo):
    """Taux de rendement interne annuel, vu par l'investisseur.

    C'est le taux annuel "i" tel que la valeur actualisée de tous les flux
    soit nulle :

        Σ  CF_k / (1 + i) ^ (jours_k / 365)  = 0

    avec, du point de vue de l'investisseur :
        - un achat  = argent qui SORT de sa poche   -> CF négatif
        - une vente, un dividende = argent qui ENTRE -> CF positif
        - le dernier jour, on fait "comme si" on vendait tout : + valeur finale

    Contrairement au TWR, le TRI dépend du CALENDRIER des apports : avoir
    beaucoup investi juste avant une hausse améliore le TRI.

    Il n'existe pas de formule directe pour trouver i : on le cherche par
    DICHOTOMIE (on coupe l'intervalle en deux jusqu'à trouver la solution).
    """
    flux = histo.loc[histo["flux"] != 0, "flux"]
    cash_flows = -flux                                   # point de vue investisseur
    date_fin = histo.index[-1]
    cash_flows = pd.concat([cash_flows, pd.Series({date_fin: histo["valeur"].iloc[-1]})])
    cash_flows = cash_flows.groupby(level=0).sum()       # regroupe un même jour

    annees = np.array([(d - cash_flows.index[0]).days / 365 for d in cash_flows.index])
    montants = cash_flows.to_numpy()

    def valeur_actuelle_nette(i):
        return np.sum(montants / (1 + i) ** annees)

    # Dichotomie entre −99 % et +1 000 % par an.
    bas, haut = -0.99, 10.0
    if valeur_actuelle_nette(bas) * valeur_actuelle_nette(haut) > 0:
        return np.nan  # pas de solution dans l'intervalle
    for _ in range(200):
        milieu = (bas + haut) / 2
        if valeur_actuelle_nette(bas) * valeur_actuelle_nette(milieu) <= 0:
            haut = milieu
        else:
            bas = milieu
    return (bas + haut) / 2


# ======================================================================
# 4. Volatilité
# ======================================================================
def volatilite_annualisee(rendements):
    """Écart-type des rendements quotidiens, ramené à l'année.

    volatilité annuelle = écart-type quotidien × √252

    Pourquoi √252 ? Si les rendements quotidiens sont indépendants, les
    variances s'additionnent : variance annuelle = 252 × variance quotidienne,
    donc écart-type annuel = √252 × écart-type quotidien.

    Interprétation : avec une volatilité de 15 %, le rendement d'une année
    s'écarte "typiquement" de ± 15 % de sa moyenne.
    """
    return rendements.std() * np.sqrt(JOURS_BOURSE_PAR_AN)


# ======================================================================
# 5. Max drawdown
# ======================================================================
def serie_drawdown(indice):
    """Pour chaque jour : baisse par rapport au plus haut atteint jusque-là.

    drawdown(t) = indice(t) / max(indice jusqu'à t) − 1   (toujours ≤ 0)
    cummax() = maximum cumulé ("le plus haut atteint jusqu'ici").
    """
    return indice / indice.cummax() - 1


def max_drawdown(indice):
    """Pire baisse subie : du plus haut au plus bas suivant.

    On le calcule sur l'INDICE base 100, et pas sur la valeur du
    portefeuille : sinon un simple retrait d'argent ressemblerait à une
    perte, et un apport masquerait une vraie baisse.

    Renvoie un dictionnaire : la baisse, la date du sommet, la date du creux
    et la date de retour au sommet (None si pas encore revenu).
    """
    dd = serie_drawdown(indice)
    date_creux = dd.idxmin()
    date_sommet = indice[:date_creux].idxmax()
    apres = indice[date_creux:]
    revenu = apres[apres >= indice[date_sommet]]
    return {
        "max_drawdown": dd.min(),
        "date_sommet": date_sommet,
        "date_creux": date_creux,
        "date_recuperation": revenu.index[0] if len(revenu) else None,
    }


# ======================================================================
# 6. Rendements par année civile
# ======================================================================
def rendements_annuels(rendements):
    """TWR de chaque année civile (2024, 2025, ...).

    groupby(année) regroupe les jours par année, puis on compose les
    rendements de chaque groupe.
    """
    return rendements.groupby(rendements.index.year).apply(twr)


# ======================================================================
# Tout en une fois
# ======================================================================
def calculer_indicateurs(histo):
    """Calcule tous les indicateurs et les renvoie dans un dictionnaire."""
    r = rendements_journaliers(histo)
    indice = indice_base_100(r)
    debut, fin = r.index[0], r.index[-1]
    perf_totale = twr(r)
    dd = max_drawdown(indice)
    return {
        "date_debut": debut,
        "date_fin": fin,
        "twr_total": perf_totale,
        "twr_annualise": annualiser(perf_totale, debut, fin),
        "tri_annuel": tri(histo),
        "volatilite": volatilite_annualisee(r),
        "meilleur_jour": (r.idxmax(), r.max()),
        "pire_jour": (r.idxmin(), r.min()),
        **dd,
        "rendements_annuels": rendements_annuels(r),
        "rendements": r,
        "indice": indice,
        "drawdown": serie_drawdown(indice),
    }


# ######################################################################
# ÉTAPE 5 — INDICATEURS AVANCÉS
# ######################################################################


def taux_journalier(taux_annuel):
    """Convertit un taux annuel en taux par jour de bourse.
    (1 + taux journalier) ^ 252 = 1 + taux annuel
    """
    return (1 + taux_annuel) ** (1 / JOURS_BOURSE_PAR_AN) - 1


# ======================================================================
# 7. Sharpe et Sortino : le rendement obtenu par unité de risque
# ======================================================================
def ratio_sharpe(rendements, taux_sans_risque):
    """Ratio de Sharpe annualisé.

                rendement moyen − taux sans risque
    Sharpe = ------------------------------------
                         volatilité

    Il répond à : "est-ce que le risque pris a été bien payé ?"
    Ordres de grandeur : < 0 mauvais ; 0,5 correct ; > 1 très bon.

    Calcul sur les rendements quotidiens "excédentaires" (au-delà du taux
    sans risque), puis annualisation : moyenne × 252 et écart-type × √252.
    """
    excedent = rendements - taux_journalier(taux_sans_risque)
    return excedent.mean() * JOURS_BOURSE_PAR_AN / (excedent.std() * np.sqrt(JOURS_BOURSE_PAR_AN))


def ratio_sortino(rendements, taux_sans_risque):
    """Ratio de Sortino : comme Sharpe, mais ne pénalise que les BAISSES.

    Critique de Sharpe : la volatilité compte les fortes hausses comme du
    "risque". Or un investisseur ne se plaint pas des hausses !
    Sortino remplace la volatilité par la "semi-déviation" : on ne garde
    que les jours où le rendement est sous le taux sans risque.

        semi-déviation = √( moyenne( min(excédent, 0)² ) ) × √252
    """
    excedent = rendements - taux_journalier(taux_sans_risque)
    baisses = excedent.clip(upper=0)          # les hausses sont remplacées par 0
    semi_deviation = np.sqrt((baisses ** 2).mean()) * np.sqrt(JOURS_BOURSE_PAR_AN)
    return excedent.mean() * JOURS_BOURSE_PAR_AN / semi_deviation


# ======================================================================
# 8. Comparaison avec un indice de référence
# ======================================================================
def rendements_indice(prix_indice, calendrier):
    """Rendements quotidiens de l'indice, sur les mêmes jours que le portefeuille.

    reindex + ffill : on aligne l'indice sur le calendrier du portefeuille.
    pct_change()   : variation en % d'un jour à l'autre (cours(t)/cours(t−1) − 1).
    """
    prix = prix_indice.reindex(calendrier).ffill()
    return prix.pct_change().rename("indice")


def aligner(rendements, rendements_bench):
    """Ne garde que les jours où l'on a les deux rendements."""
    tableau = pd.concat([rendements, rendements_bench], axis=1, join="inner").dropna()
    return tableau.iloc[:, 0], tableau.iloc[:, 1]


def beta_alpha(rendements, rendements_bench, taux_sans_risque):
    """Bêta et alpha de Jensen (modèle de marché / MEDAF).

    Bêta = cov(portefeuille, indice) / var(indice)
        - bêta = 1   : le portefeuille bouge comme l'indice ;
        - bêta = 1,2 : quand l'indice fait +1 %, le portefeuille fait
                       en moyenne +1,2 % (plus risqué que le marché) ;
        - bêta = 0,8 : plus défensif que le marché.

    Alpha (annualisé) = rendement en excès du portefeuille
                        − bêta × rendement en excès de l'indice
        = la performance qui ne s'explique PAS par l'exposition au marché.
          Alpha > 0 : le choix des titres a créé de la valeur.
    """
    rp, rb = aligner(rendements, rendements_bench)
    rf = taux_journalier(taux_sans_risque)
    beta = np.cov(rp, rb, ddof=1)[0, 1] / np.var(rb, ddof=1)
    alpha_jour = (rp - rf).mean() - beta * (rb - rf).mean()
    return beta, alpha_jour * JOURS_BOURSE_PAR_AN


def tracking_error(rendements, rendements_bench):
    """Tracking error et ratio d'information.

    Tracking error = volatilité de l'ÉCART de rendement avec l'indice.
        Faible (< 2 %) : le portefeuille "colle" à l'indice (gestion passive).
        Élevée (> 5 %) : gestion très différente de l'indice.

    Ratio d'information = écart de rendement moyen annualisé / tracking error
        = l'écart avec l'indice a-t-il été "payé" ? (comme Sharpe, mais
          relativement à l'indice). > 0,5 est considéré comme bon.
    """
    rp, rb = aligner(rendements, rendements_bench)
    ecart = rp - rb
    te = ecart.std() * np.sqrt(JOURS_BOURSE_PAR_AN)
    ratio_info = ecart.mean() * JOURS_BOURSE_PAR_AN / te
    return te, ratio_info


# ======================================================================
# 9. Value at Risk (VaR) et Expected Shortfall (CVaR)
# ======================================================================
def var_cvar(rendements, niveau=0.95):
    """Perte quotidienne "exceptionnelle" à un niveau de confiance donné.

    VaR 95 % : la perte qu'on ne dépasse que 5 % des jours
               (= environ 1 jour de bourse sur 20, soit une fois par mois).

    Deux méthodes :
      - HISTORIQUE : on prend directement le 5e percentile des rendements
        passés. Aucune hypothèse, mais on suppose que le passé se répète.
      - PARAMÉTRIQUE (gaussienne) : on suppose que les rendements suivent
        une loi normale : VaR = −(moyenne + z × écart-type), avec z = −1,645
        à 95 %. Simple, mais SOUS-ESTIME les krachs : les vrais rendements
        ont des "queues épaisses" (les grosses baisses sont plus fréquentes
        que ce que prévoit la loi normale).

    CVaR (Expected Shortfall) : la perte MOYENNE les jours où la VaR est
    dépassée. Répond à : "et quand ça va mal, ça va mal comment ?"
    C'est la mesure privilégiée par les régulateurs bancaires (Bâle III).

    Les résultats sont des nombres POSITIFS (= pertes).
    """
    seuil = 1 - niveau                                  # 0,05
    var_hist = -rendements.quantile(seuil)
    z = NormalDist().inv_cdf(seuil)                     # −1,645 à 95 %
    var_param = -(rendements.mean() + z * rendements.std())
    cvar = -rendements[rendements <= -var_hist].mean()
    return {"var_historique": var_hist, "var_parametrique": var_param, "cvar": cvar}


# ======================================================================
# 10. Corrélations entre les titres
# ======================================================================
def matrice_correlation(prix_hist, tickers):
    """Corrélation des rendements quotidiens entre chaque paire de titres.

    +1 : les deux titres montent et baissent toujours ensemble ;
     0 : aucun lien ;
    −1 : quand l'un monte, l'autre baisse.

    Intérêt : la DIVERSIFICATION. Des titres peu corrélés entre eux
    réduisent le risque global du portefeuille (base de Markowitz, étape 7).
    """
    rendements = prix_hist[list(tickers)].pct_change().dropna()
    matrice = rendements.corr()
    matrice.index.name = matrice.columns.name = None   # retire l'étiquette "Ticker"
    return matrice


# ======================================================================
# Tout en une fois (étape 5)
# ======================================================================
def calculer_indicateurs_avances(histo, rendements, prix_indice, taux_sans_risque,
                                 niveau_var=0.95):
    """Calcule tous les indicateurs avancés et les renvoie dans un dictionnaire."""
    rb_complet = rendements_indice(prix_indice, histo.index)
    rp, rb = aligner(rendements, rb_complet)

    beta, alpha = beta_alpha(rp, rb, taux_sans_risque)
    te, ratio_info = tracking_error(rp, rb)
    risques = var_cvar(rendements, niveau_var)
    valeur_actuelle = histo["valeur"].iloc[-1]

    return {
        "sharpe": ratio_sharpe(rendements, taux_sans_risque),
        "sortino": ratio_sortino(rendements, taux_sans_risque),
        "beta": beta,
        "alpha": alpha,
        "correlation_indice": rp.corr(rb),
        "tracking_error": te,
        "ratio_information": ratio_info,
        "twr_indice": twr(rb),
        "twr_portefeuille_meme_periode": twr(rp),
        "sharpe_indice": ratio_sharpe(rb, taux_sans_risque),
        "volatilite_indice": volatilite_annualisee(rb),
        **risques,
        # Conversion de la VaR en euros, sur la valeur actuelle du portefeuille
        "var_euros": risques["var_historique"] * valeur_actuelle,
        "cvar_euros": risques["cvar"] * valeur_actuelle,
        "indice_portefeuille": indice_base_100(rp),
        "indice_reference": indice_base_100(rb),
        "rendements_annuels_indice": rendements_annuels(rb),
    }
