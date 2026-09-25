"""
main.py — Version "texte" du projet : affiche toute l'analyse dans le terminal,
enregistre les graphiques et génère le rapport PDF.

Pour le lancer, dans le terminal (depuis le dossier portfolio_tracker) :
    python main.py                                  -> analyse data/transactions.csv
    python main.py data/transactions_mondial.csv    -> analyse un autre fichier

Tous les calculs sont faits par src/analyse.py (la même fonction que le
tableau de bord) : ce fichier se contente d'AFFICHER les résultats.
"""

import sys

import numpy as np

from src import config
from src.analyse import analyse_complete
from src.graphiques import (graphique_comparaison, graphique_correlations, graphique_frontiere,
                            graphique_historique, graphique_performance, graphique_poids,
                            graphique_projection, graphique_projection_nuage)
from src.extensions import calculer_extensions
from src.optimisation import optimiser_portefeuille
from src.simulation import parametres_historiques, simuler

# Le fichier à analyser peut être donné après "python main.py" ; sinon, fichier par défaut.
FICHIER_TRANSACTIONS = sys.argv[1] if len(sys.argv) > 1 else "data/transactions.csv"
FICHIER_RAPPORT = "rapport_portefeuille.pdf"


def pct(x):
    """Affiche un nombre comme un pourcentage : 0.1234 -> '+12.34 %'."""
    return f"{x * 100:+.2f} %"


def titre(texte):
    print()
    print("=" * 90)
    print(texte)
    print("=" * 90)


# ----------------------------------------------------------------------
# 1. Toute l'analyse (étapes 1 à 5 + devises)
# ----------------------------------------------------------------------
print(f"Analyse de {FICHIER_TRANSACTIONS} : récupération des cours et calculs en cours...")
res = analyse_complete(FICHIER_TRANSACTIONS)
positions, r, histo = res["positions"], res["resume"], res["historique"]
ind, av, prix_hist = res["indicateurs"], res["avances"], res["prix_hist"]
print(f"Source des cours : {res['source_cours']}")

# ----------------------------------------------------------------------
# 2. Positions et résumé (étape 2)
# ----------------------------------------------------------------------
titre("POSITIONS VALORISÉES (en euros)")
colonnes = ["nom", "devise", "quantite", "pru", "cours", "valeur", "pv_latente", "pv_latente_pct", "poids_pct"]
affichage = positions[colonnes].rename(columns={
    "quantite": "qté", "pv_latente": "+/- value €", "pv_latente_pct": "+/- value %", "poids_pct": "poids %",
})
print(affichage.round(2).to_string())

# Répartition par région et par secteur (grâce à data/referentiel.csv)
for colonne, libelle in [("region", "RÉGION"), ("secteur", "SECTEUR")]:
    if positions[colonne].nunique() > 1:
        repartition_groupe = positions.groupby(colonne)["poids_pct"].agg(["sum", "count"])
        repartition_groupe.columns = ["poids %", "nb lignes"]
        print()
        print(f"Répartition par {libelle.lower()} :")
        print(repartition_groupe.sort_values("poids %", ascending=False).round(1).to_string())

if res["taux_actuels"]:
    print()
    print("Taux de change utilisés (pour 1 €) : "
          + ", ".join(f"{taux:.4f} {devise}" for devise, taux in res["taux_actuels"].items()))

titre("RÉSUMÉ")
print(f"Nombre de lignes détenues : {r['nb_lignes']}")
print(f"Montant investi (au PRU)  : {r['montant_investi']:>12,.2f} €")
print(f"Valeur actuelle           : {r['valeur_actuelle']:>12,.2f} €")
print(f"Plus-values latentes      : {r['pv_latentes']:>12,.2f} €")
print(f"Plus-values réalisées     : {r['pv_realisees']:>12,.2f} €")
print(f"Dividendes perçus         : {r['dividendes']:>12,.2f} €")
print(f"Frais payés               : {r['frais_totaux']:>12,.2f} €")
print("-" * 45)
print(f"GAIN TOTAL                : {r['gain_total']:>12,.2f} €")

# ----------------------------------------------------------------------
# 3. Historique (étape 3)
# ----------------------------------------------------------------------
titre("HISTORIQUE")
print(f"Source de l'historique : {res['source_historique']}")
print(f"Période : du {histo.index[0]:%d/%m/%Y} au {histo.index[-1]:%d/%m/%Y} ({len(histo)} jours de bourse)")
print()
print("Valeur en fin de mois :")
fin_de_mois = histo.resample("ME").last()[["valeur", "apports_nets", "gain"]]
fin_de_mois.index = fin_de_mois.index.strftime("%m/%Y")
print(fin_de_mois.round(0).to_string())
print()
print(f"Plus haut : {histo['valeur'].max():,.2f} € le {histo['valeur'].idxmax():%d/%m/%Y}")
print(f"Gain au dernier jour (historique) : {histo['gain'].iloc[-1]:,.2f} €  "
      f"(à comparer au GAIN TOTAL ci-dessus)")

# ----------------------------------------------------------------------
# 4. Performance et risque (étape 4)
# ----------------------------------------------------------------------
titre("PERFORMANCE ET RISQUE")
print(f"Période analysée          : du {ind['date_debut']:%d/%m/%Y} au {ind['date_fin']:%d/%m/%Y}")
print()
print("Performance")
print(f"  TWR total               : {pct(ind['twr_total'])}")
print(f"  TWR annualisé           : {pct(ind['twr_annualise'])}")
print(f"  TRI (annuel)            : {pct(ind['tri_annuel'])}")
print()
print("Risque")
print(f"  Volatilité annualisée   : {ind['volatilite'] * 100:.2f} %")
print(f"  Max drawdown            : {pct(ind['max_drawdown'])}")
print(f"      du plus haut le {ind['date_sommet']:%d/%m/%Y} au plus bas le {ind['date_creux']:%d/%m/%Y}")
if ind["date_recuperation"] is None:
    print("      plus haut pas encore retrouvé")
else:
    print(f"      plus haut retrouvé le {ind['date_recuperation']:%d/%m/%Y}")
date_max, r_max = ind["meilleur_jour"]
date_min, r_min = ind["pire_jour"]
print(f"  Meilleur jour           : {pct(r_max)} le {date_max:%d/%m/%Y}")
print(f"  Pire jour               : {pct(r_min)} le {date_min:%d/%m/%Y}")
print()
print("Rendement par année civile (TWR)")
for annee, r_an in ind["rendements_annuels"].items():
    print(f"  {annee}                    : {pct(r_an)}")

# ----------------------------------------------------------------------
# 5. Indicateurs avancés (étape 5)
# ----------------------------------------------------------------------
niveau = f"{config.NIVEAU_CONFIANCE_VAR:.0%}"
titre("INDICATEURS AVANCÉS")
print(f"Taux sans risque retenu   : {config.TAUX_SANS_RISQUE:.2%} par an")
print()
print("Rendement ajusté du risque          Portefeuille      Indice")
print(f"  Ratio de Sharpe                   {av['sharpe']:>10.2f}  {av['sharpe_indice']:>10.2f}")
print(f"  Ratio de Sortino                  {av['sortino']:>10.2f}")
print(f"  Volatilité annualisée             {ind['volatilite']:>10.2%}  {av['volatilite_indice']:>10.2%}")
print(f"  TWR sur la période                {av['twr_portefeuille_meme_periode']:>+10.2%}  {av['twr_indice']:>+10.2%}")
print()
print(f"Comparaison avec : {config.NOM_INDICE}")
print(f"  Bêta                    : {av['beta']:.2f}")
print(f"  Alpha de Jensen (annuel): {pct(av['alpha'])}")
print(f"  Corrélation             : {av['correlation_indice']:.2f}")
print(f"  Tracking error          : {av['tracking_error']:.2%}")
print(f"  Ratio d'information     : {av['ratio_information']:.2f}")
print()
print(f"Risque de perte sur 1 jour (niveau de confiance {niveau})")
print(f"  VaR historique          : {av['var_historique']:.2%}  soit {av['var_euros']:,.0f} €")
print(f"  VaR paramétrique        : {av['var_parametrique']:.2%}")
print(f"  CVaR (Expected Shortfall): {av['cvar']:.2%}  soit {av['cvar_euros']:,.0f} €")
print()
correlations = res["correlations"]
if len(correlations) <= 15:
    print("Matrice de corrélation (titres détenus)")
    print((correlations.round(2) + 0.0).to_string())  # + 0.0 évite d'afficher « -0.00 »
else:
    # Trop de titres pour afficher la matrice : on liste les paires les plus liées.
    paires = correlations.where(~np.tril(np.ones(correlations.shape, dtype=bool))).stack()
    print(f"Corrélation moyenne entre les {len(correlations)} titres : {paires.mean():.2f}")
    print("Paires les plus corrélées :")
    for (a, b), c in paires.sort_values(ascending=False).head(5).items():
        print(f"  {a:<10} / {b:<10} : {c:.2f}")

# ----------------------------------------------------------------------
# 6. Optimisation de Markowitz (étape 7)
# ----------------------------------------------------------------------
opti = optimiser_portefeuille(prix_hist, positions, config.TAUX_SANS_RISQUE, config.POIDS_MAX)
titre(f"OPTIMISATION DE MARKOWITZ (poids maximal par titre : {config.POIDS_MAX:.0%})")
print("                          Rendement espéré   Volatilité    Sharpe")
for cle, nom in [("actuel", "Mon portefeuille"), ("variance_min", "Variance minimale"),
                 ("sharpe_max", "Sharpe maximal")]:
    p = opti[cle]
    print(f"  {nom:<22}  {p['rendement']:>14.2%}  {p['volatilite']:>11.2%}  {p['sharpe']:>8.2f}")
print()
repartition = opti["poids"].copy()
for col in ["actuel", "variance_min", "sharpe_max"]:
    repartition[col] = (repartition[col] * 100).round(1)
repartition["ecart_euros_sharpe_max"] = repartition["ecart_euros_sharpe_max"].round(0)
repartition = repartition.rename(columns={
    "actuel": "actuel %", "variance_min": "var. min %", "sharpe_max": "Sharpe max %",
    "ecart_euros_sharpe_max": "à acheter (+) / vendre (-) €",
})
print(repartition.sort_values("actuel %", ascending=False).to_string())
print()
print("⚠️  Exercice académique : ceci n'est pas un conseil en investissement.")

# ----------------------------------------------------------------------
# 7. Projection Monte-Carlo (étape 8)
# ----------------------------------------------------------------------
mu, sigma = parametres_historiques(ind["rendements"])
sim = simuler(
    r["valeur_actuelle"], mu, sigma,
    annees=config.HORIZON_PROJECTION, versement_mensuel=config.VERSEMENT_MENSUEL,
    nb_simulations=config.NB_SIMULATIONS, methode=config.METHODE_SIMULATION,
    rendements_historiques=ind["rendements"], date_depart=histo.index[-1],
)
titre(f"PROJECTION MONTE-CARLO À {config.HORIZON_PROJECTION} ANS "
      f"({config.NB_SIMULATIONS} scénarios, méthode {config.METHODE_SIMULATION})")
print(f"Hypothèses (historiques) : rendement moyen {mu:.2%} par an, volatilité {sigma:.2%}")
print(f"Versement mensuel        : {config.VERSEMENT_MENSUEL:,.0f} €")
print()
print(f"  Départ + versements            : {sim['total_apporte']:>12,.0f} €")
print(f"  Scénario défavorable (5 %)    : {sim['p5']:>12,.0f} €")
print(f"  Scénario médian               : {sim['mediane']:>12,.0f} €")
print(f"  Scénario favorable (95 %)     : {sim['p95']:>12,.0f} €")
print(f"  Probabilité de finir en perte : {sim['proba_perte']:>12.1%}")
print()
print("⚠️  Une projection n'est pas une prévision : elle suppose que le rendement et")
print("    le risque passés se reproduisent.")

# ----------------------------------------------------------------------
# 8. Conseil patrimonial et gestion d'actifs (étape 10)
# ----------------------------------------------------------------------
print()
print("Calcul des analyses complémentaires (stress tests, attribution...)")
ext = calculer_extensions(res)

titre(f"CONSEIL PATRIMONIAL — profil {ext['profil'].nom} (réglable dans src/config.py)")
adeq = ext["adequation"]
print(f"Indicateur de risque SRI : {adeq['sri']} / 7")
for nom, valeur, limite, ok in adeq["criteres"]:
    format_valeur = (lambda v: f"{v:.0f}") if "SRI" in nom else (lambda v: f"{v:.1%}")
    print(f"  {nom:<28} {format_valeur(valeur):>8}   limite {format_valeur(limite):>6}   "
          f"{'conforme' if ok else 'DÉPASSÉ'}")
if adeq["adapte"]:
    print("-> Portefeuille adapté au profil.")
else:
    print(f"-> Trop risqué : garder {adeq['part_risquee_conseillee']:.0%} sur ce portefeuille et placer "
          f"{adeq['part_sans_risque_conseillee']:.0%} sans risque.")

print()
print(f"Fiscalité d'une vente totale aujourd'hui (ancienneté {ext['anciennete']:.1f} ans, taux 2026) :")
for l in ext["fiscalite"]:
    print(f"  {l['enveloppe']:<14} impôts {l['impots']:>12,.0f} €   gain net {l['gain_net']:>12,.0f} €   "
          f"performance nette {l['performance_nette']:+.2%}")
print(f"  Part du portefeuille éligible au PEA : {ext['part_pea']:.0%}")

print()
print("Stress tests : crises passées rejouées sur le portefeuille actuel")
if "stress" in ext:
    for _, l in ext["stress"].iterrows():
        print(f"  {l['scenario']:<38} {l['variation']:+.1%}  soit {l['perte_euros']:>+12,.0f} €")
else:
    print(f"  indisponible : {ext['erreurs']['stress']}")
for _, l in ext["stress_hypothetiques"].iterrows():
    print(f"  {l['scenario']:<38} {l['variation']:+.1%}  ({l['hypothese']})")

titre("GESTION D'ACTIFS")
if "attribution" in ext:
    a = ext["attribution"]
    print(f"Attribution de performance face au MSCI ACWI : portefeuille {a['Rp']:+.2%}, "
          f"indice {a['Rb']:+.2%}, écart {a['Rp'] - a['Rb']:+.2%}")
    for effet, valeur in a["effets"].items():
        print(f"  Effet {effet:<12} : {valeur:+.2%}")
else:
    print(f"Attribution indisponible : {ext['erreurs']['attribution']}")

if "budget" in ext:
    b = ext["budget"]
    print()
    print("Budget de risque : 5 plus gros contributeurs au risque")
    for t, l in b["par_ligne"].head(5).iterrows():
        print(f"  {l['nom']:<28} {l['poids']:>6.1%} de la valeur   {l['part_risque']:>6.1%} du risque")
    print()
    print((b["comparaison"][["rendement", "volatilite", "sharpe", "nb_effectif_paris"]] * [100, 100, 1, 1])
          .round(2).rename(columns={"rendement": "rendement %", "volatilite": "volatilité %",
                                    "nb_effectif_paris": "nb effectif de paris"}).to_string())

if "backtest" in ext:
    print()
    print("Backtest : rééquilibrer ou non (mêmes titres, mêmes poids de départ, frais 0,1 %)")
    bt = ext["backtest"]
    for nom, l in bt.iterrows():
        print(f"  {nom:<28} {l['rendement_annualise']:+.2%} par an   volatilité {l['volatilite']:.2%}   "
              f"max drawdown {l['max_drawdown']:+.2%}")
    print("Investir 10 000 € en une fois ou en 12 mois :")
    for nom, l in ext["dca"].iterrows():
        print(f"  {nom:<28} valeur finale {l['valeur_finale']:>10,.0f} €")

# ----------------------------------------------------------------------
# 9. Graphiques et rapport PDF
# ----------------------------------------------------------------------
histo.round(2).to_csv("data/historique.csv")
graphique_historique(histo, "graphique_historique.png")
graphique_performance(ind, "graphique_performance.png")
graphique_comparaison(av, config.NOM_INDICE, "graphique_comparaison.png")
graphique_correlations(res["correlations"], "graphique_correlations.png")
graphique_frontiere(opti, "graphique_frontiere.png")
graphique_poids(opti, "graphique_poids.png")
graphique_projection(sim, "graphique_projection.png")
graphique_projection_nuage(sim, "graphique_projection_nuage.png")

try:
    from src.rapport import generer_rapport
    generer_rapport(res, FICHIER_RAPPORT, config.NOM_INDICE, config.TAUX_SANS_RISQUE,
                    config.NIVEAU_CONFIANCE_VAR, opti=opti, sim=sim, extensions=ext)
    rapport = f", {FICHIER_RAPPORT}"
except ImportError:
    rapport = ""
    print()
    print("ℹ️  Rapport PDF non généré : installe reportlab (python -m pip install reportlab)")

print()
print("Fichiers créés : data/historique.csv, 8 graphiques (graphique_*.png)" + rapport)
