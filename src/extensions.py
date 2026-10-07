"""
extensions.py — Calcule en une fois les analyses complémentaires de l'étape 10, pour
main.py et le rapport PDF (le tableau de bord les calcule onglet par onglet).

Chaque analyse est indépendante : si l'une échoue (par exemple faute de
connexion pour télécharger l'historique depuis 2008), les autres sont
tout de même calculées et l'erreur est notée dans "erreurs".
"""

import pandas as pd

from . import attribution, backtest, budget_risque, config, fiscalite, stress


def calculer_extensions(res, taux_sans_risque=config.TAUX_SANS_RISQUE, situation=config.SITUATION_FAMILIALE):
    resume, positions = res["resume"], res["positions"]
    ext = {"erreurs": {}}

    # 1. Fiscalité
    anciennete = (res["historique"].index[-1] - res["date_ouverture"]).days / 365.25
    ext["anciennete"] = anciennete
    ext["fiscalite"] = fiscalite.comparer_enveloppes(resume["gain_total"], resume["montant_investi"],
                                                      anciennete, resume["dividendes"], situation)
    ext["part_pea"] = fiscalite.eligibilite_pea(positions)[0]

    # 2. Stress tests
    try:
        prix_longs, _ = stress.telecharger_historique_long(positions.index)
        ext["stress"], _ = stress.scenarios_historiques(positions, prix_longs)
    except Exception as erreur:
        ext["erreurs"]["stress"] = str(erreur)
    ext["stress_hypothetiques"] = stress.scenarios_hypothetiques(positions, res["avances"]["beta"])

    # 3. Attribution de performance
    try:
        indices = attribution.rendements_indices(res["historique"].index[0] - pd.Timedelta(days=10))
        ext["attribution"] = attribution.attribution_poche_actions(res, indices)
    except Exception as erreur:
        ext["erreurs"]["attribution"] = str(erreur)

    # 4. Budget de risque
    try:
        ext["budget"] = budget_risque.analyse_budget_risque(res["prix_hist"], positions, taux_sans_risque)
    except Exception as erreur:
        ext["erreurs"]["budget"] = str(erreur)

    # 5. Backtest
    try:
        prix = res["prix_hist"][list(positions.index)].ffill().dropna()
        poids = positions["poids_pct"] / 100
        _, ext["backtest"] = backtest.comparer_reequilibrages(prix, poids, 0.001, taux_sans_risque)
        _, ext["dca"] = backtest.comparer_dca(prix, poids, 10_000, 12, taux_sans_risque, 0.001)
    except Exception as erreur:
        ext["erreurs"]["backtest"] = str(erreur)

    return ext
