"""
backtest.py — Tester des stratégies de gestion sur l'historique réel.

Question : avec les MÊMES titres et les MÊMES poids de départ que le
portefeuille actuel, quelle stratégie aurait le mieux fonctionné ?

1. RÉÉQUILIBRAGE
   - Achat-conservation ("buy and hold") : on achète une fois, on ne touche
     plus à rien ; les poids dérivent avec les cours (les gagnants grossissent).
   - Rééquilibrage mensuel, trimestriel ou annuel : on revient aux poids
     cibles à intervalles réguliers (on vend ce qui a monté, on achète ce qui
     a baissé), en payant des frais sur les montants échangés.

2. INVESTISSEMENT EN UNE FOIS OU PROGRESSIF ("DCA", Dollar Cost Averaging)
   - En une fois : tout le capital est investi le premier jour ;
   - Progressif : le capital est investi en 12 parts égales, une par mois ;
     l'argent en attente est rémunéré au taux sans risque.
   En moyenne, sur un marché haussier, investir en une fois gagne plus ;
   l'investissement progressif réduit le risque de "mal tomber".

Limite : cours hors dividendes (les rendements sont donc un peu sous-estimés,
de la même façon pour toutes les stratégies).
"""

import numpy as np
import pandas as pd

JOURS_BOURSE_PAR_AN = 252
FREQUENCES = {"Achat-conservation": None, "Rééquilibrage mensuel": "M",
              "Rééquilibrage trimestriel": "Q", "Rééquilibrage annuel": "Y"}


def _dates_reequilibrage(index, frequence):
    """Premier jour de bourse de chaque mois / trimestre / année (hors le 1er jour)."""
    if frequence is None:
        return set()
    periodes = index.to_period(frequence)
    premiers = pd.Series(index, index=index).groupby(periodes).first()
    return set(premiers.iloc[1:])


def simuler_strategie(prix, poids_cibles, frequence=None, frais=0.001, capital=100.0):
    """Valeur quotidienne d'un portefeuille géré selon une stratégie.

    prix         : cours quotidiens (une colonne par titre, en euros)
    poids_cibles : poids de départ et cibles de rééquilibrage (Series, somme = 1)
    frequence    : None (achat-conservation), "M", "Q" ou "Y"
    frais        : frais en % des montants achetés ou vendus

    Renvoie (valeurs quotidiennes, rotation totale = somme des montants échangés / valeur).
    """
    prix = prix[poids_cibles.index].ffill().dropna()
    w = poids_cibles.to_numpy(dtype=float)
    cours = prix.to_numpy()
    quantites = capital * w / cours[0] * (1 - frais)
    rebal = _dates_reequilibrage(prix.index, frequence)
    valeurs = np.empty(len(prix))
    rotation = 0.0
    for i, date in enumerate(prix.index):
        valeur = float(quantites @ cours[i])
        if date in rebal:
            actuelles = quantites * cours[i]
            cibles = w * valeur
            echange = np.abs(cibles - actuelles).sum()
            cout = frais * echange
            rotation += echange / valeur
            quantites = (w * (valeur - cout)) / cours[i]
            valeur -= cout
        valeurs[i] = valeur
    return pd.Series(valeurs, index=prix.index), rotation


def statistiques(valeurs, taux_sans_risque=0.0):
    """Rendement annualisé, volatilité, max drawdown et Sharpe d'une série de valeurs."""
    r = valeurs.pct_change().dropna()
    annees = (valeurs.index[-1] - valeurs.index[0]).days / 365
    total = valeurs.iloc[-1] / valeurs.iloc[0] - 1
    annualise = (1 + total) ** (1 / annees) - 1 if annees > 0 else np.nan
    vol = r.std() * np.sqrt(JOURS_BOURSE_PAR_AN)
    drawdown = (valeurs / valeurs.cummax() - 1).min()
    return {"rendement_total": total, "rendement_annualise": annualise, "volatilite": vol,
            "max_drawdown": drawdown, "sharpe": (annualise - taux_sans_risque) / vol if vol else np.nan}


def comparer_reequilibrages(prix, poids_cibles, frais=0.001, taux_sans_risque=0.0):
    """Toutes les stratégies de rééquilibrage, en base 100."""
    courbes, lignes = {}, []
    for nom, frequence in FREQUENCES.items():
        valeurs, rotation = simuler_strategie(prix, poids_cibles, frequence, frais)
        courbes[nom] = valeurs
        stats = statistiques(valeurs, taux_sans_risque)
        annees = (valeurs.index[-1] - valeurs.index[0]).days / 365
        stats["rotation_annuelle"] = rotation / annees if annees > 0 else 0.0
        lignes.append({"strategie": nom, **stats})
    return pd.DataFrame(courbes), pd.DataFrame(lignes).set_index("strategie")


def comparer_dca(prix, poids_cibles, capital=10_000.0, nb_mois=12, taux_sans_risque=0.0,
                 frais=0.001):
    """Investir tout de suite ou en nb_mois versements mensuels égaux.

    Les deux stratégies achètent le même panier (poids cibles, sans
    rééquilibrage ensuite). Renvoie les deux courbes de valeur (en euros)
    et un résumé.
    """
    prix = prix[poids_cibles.index].ffill().dropna()
    w = poids_cibles.to_numpy(dtype=float)
    cours = prix.to_numpy()
    # Indice du panier : valeur de 1 € investi le premier jour (sans rééquilibrage)
    panier = (w / cours[0]) @ cours.T
    panier = pd.Series(panier, index=prix.index)

    # En une fois
    une_fois = capital * (1 - frais) * panier

    # Progressif : un versement le premier jour de bourse de chacun des nb_mois premiers mois
    premiers = pd.Series(prix.index, index=prix.index).groupby(prix.index.to_period("M")).first()
    dates_versement = list(premiers.iloc[:nb_mois])
    part = capital / len(dates_versement)
    taux_jour = (1 + taux_sans_risque) ** (1 / JOURS_BOURSE_PAR_AN) - 1
    unites, liquidites, valeurs = 0.0, float(capital), []
    for date in prix.index:
        liquidites *= 1 + taux_jour                     # l'argent en attente rapporte le taux sans risque
        if date in dates_versement:
            montant = min(part, liquidites)
            liquidites -= montant
            unites += montant * (1 - frais) / panier[date]
        valeurs.append(unites * panier[date] + liquidites)
    progressif = pd.Series(valeurs, index=prix.index)

    resume = pd.DataFrame({
        "valeur_finale": [une_fois.iloc[-1], progressif.iloc[-1]],
        "gain": [une_fois.iloc[-1] - capital, progressif.iloc[-1] - capital],
        "pire_valeur": [une_fois.min(), progressif.min()],
    }, index=["En une fois", f"Progressif ({nb_mois} mois)"])
    return pd.DataFrame({"En une fois": une_fois, f"Progressif ({nb_mois} mois)": progressif}), resume
