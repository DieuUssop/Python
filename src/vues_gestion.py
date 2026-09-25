"""
vues_gestion.py — Espace "Gestion d'actifs" du tableau de bord :
attribution de performance, budget de risque, backtest de stratégies.

Appelé par app.py : vues_gestion.afficher(res, cle, taux_sans_risque).
"""

import pandas as pd
import streamlit as st

from . import attribution, backtest, budget_risque
from . import graphiques_interactifs as gi
from . import interface as ui
from .interface import euros, nombre, pct


def html(morceau):
    st.markdown(morceau, unsafe_allow_html=True)


def graphique(figure):
    st.plotly_chart(figure, width="stretch", config=gi.CONFIG_PLOTLY)


# ----------------------------------------------------------------------
# Calculs mis en cache ("_res" n'est pas haché : c'est "cle" qui identifie le calcul)
# ----------------------------------------------------------------------
@st.cache_data(show_spinner="Attribution de performance (téléchargement des indices régionaux)...")
def _calcul_attribution(cle, _res):
    debut = _res["historique"].index[0] - pd.Timedelta(days=10)
    cours_indices = attribution.rendements_indices(debut)
    return attribution.attribution_poche_actions(_res, cours_indices)


@st.cache_data(show_spinner="Calcul du budget de risque...")
def _calcul_budget(cle, _res, taux_sans_risque):
    return budget_risque.analyse_budget_risque(_res["prix_hist"], _res["positions"], taux_sans_risque)


@st.cache_data(show_spinner="Backtest des stratégies...")
def _calcul_backtest(cle, _res, frais, capital, nb_mois, taux_sans_risque):
    positions = _res["positions"]
    prix = _res["prix_hist"][list(positions.index)].ffill().dropna()
    poids = positions["poids_pct"] / 100
    courbes, stats = backtest.comparer_reequilibrages(prix, poids, frais, taux_sans_risque)
    courbes_dca, resume_dca = backtest.comparer_dca(prix, poids, capital, nb_mois, taux_sans_risque, frais)
    return courbes, stats, courbes_dca, resume_dca


# ----------------------------------------------------------------------
# Point d'entrée
# ----------------------------------------------------------------------
def afficher(res, cle, taux_sans_risque):
    onglets = st.tabs(["Attribution de performance", "Budget de risque", "Backtest de stratégies"])
    with onglets[0]:
        _attribution(res, cle)
    with onglets[1]:
        _budget(res, cle, taux_sans_risque)
    with onglets[2]:
        _backtest(res, cle, taux_sans_risque)


# ----------------------------------------------------------------------
# 1. Attribution de performance (Brinson-Fachler)
# ----------------------------------------------------------------------
def _attribution(res, cle):
    try:
        a = _calcul_attribution(cle, res)
    except Exception as erreur:
        st.warning(f"Attribution indisponible : {erreur}")
        return
    effets = a["effets"]
    ecart = a["Rp"] - a["Rb"]
    html(ui.grille([
        ui.carte("Portefeuille", pct(a["Rp"]), detail="Rendement des positions (composé)"),
        ui.carte("Indice de référence", pct(a["Rb"]), detail="MSCI ACWI (poids régionaux)"),
        ui.carte("Écart", pct(ecart), detail=ui.pastille("surperformance" if ecart >= 0 else "sous-performance",
                                                          ui.tendance(ecart))),
        ui.carte("Effet allocation", pct(effets["allocation"]), detail="Choix des régions"),
        ui.carte("Effet sélection", pct(effets["selection"]), detail="Choix des titres"),
        ui.carte("Effet interaction", pct(effets["interaction"]), detail="Effet croisé"),
    ]))

    if a["part_actions"] < 0.995:
        html(ui.note(f"Portefeuille diversifié : l'attribution porte sur la poche actions "
                     f"({pct(a['part_actions'], signe=False, decimales=0)} du portefeuille aujourd'hui), "
                     "comparée à un indice actions. Les obligations et l'or sont exclus du calcul."))
    hors_indice = a["par_region"].loc[~a["par_region"].index.isin(attribution.POIDS_INDICE), "poids_portefeuille"].sum()
    if hors_indice > 0.2:
        html(ui.note(f"{pct(hors_indice, signe=False, decimales=0)} du portefeuille n'est pas classé dans une "
                     "région de l'indice (ETF monde, titres absents du référentiel) : l'attribution est surtout "
                     "pertinente pour un portefeuille de lignes directes comme le fonds actions monde.",
                     attention=True))

    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section("Effets par région", "La somme de tous les effets est égale à l'écart avec l'indice"))
        graphique(gi.fig_effets_attribution(a["par_region"]))
    with droite, st.container(border=True):
        html(ui.titre_section("Effets cumulés dans le temps", "Lissage de Cariño"))
        cumul = a["mensuel"][["allocation_relie", "selection_relie", "interaction_relie"]].cumsum()
        cumul.columns = ["Allocation", "Sélection", "Interaction"]
        graphique(gi.fig_lignes(cumul, format_y=".1%", hauteur=400))

    with st.container(border=True):
        html(ui.titre_section("Détail par région"))
        p = a["par_region"]
        st.dataframe(pd.DataFrame({
            "Région": p.index,
            "Poids portefeuille": [pct(v, signe=False, decimales=1) for v in p["poids_portefeuille"]],
            "Poids indice": [pct(v, signe=False, decimales=1) for v in p["poids_indice"]],
            "Rendement portefeuille": [pct(v) for v in p["rendement_portefeuille"]],
            "Rendement indice": [pct(v) for v in p["rendement_indice"]],
            "Allocation": [pct(v) for v in p["allocation"]],
            "Sélection": [pct(v) for v in p["selection"]],
            "Interaction": [pct(v) for v in p["interaction"]],
            "Total": [pct(v) for v in p["total"]],
        }), hide_index=True, width="stretch")
        html(ui.note("Lecture : un effet d'allocation positif signifie que le portefeuille a surpondéré des "
                     "régions qui ont fait mieux que l'indice ; un effet de sélection positif, qu'il a choisi "
                     "dans une région des titres qui ont fait mieux que l'indice de cette région. "
                     "Indices régionaux hors dividendes, convertis en euros."))


# ----------------------------------------------------------------------
# 2. Budget de risque et parité des risques
# ----------------------------------------------------------------------
def _budget(res, cle, taux_sans_risque):
    try:
        b = _calcul_budget(cle, res, taux_sans_risque)
    except Exception as erreur:
        st.warning(f"Budget de risque indisponible : {erreur}")
        return
    actuel = b["comparaison"].loc["Portefeuille actuel"]
    premiere = b["par_ligne"].iloc[0]
    html(ui.grille([
        ui.carte("Volatilité", pct(actuel["volatilite"], signe=False), detail="Estimée sur l'historique"),
        ui.carte("Ratio de diversification", nombre(actuel["ratio_diversification"]),
                 detail="1 = aucune diversification"),
        ui.carte("Nombre effectif de paris", f"{actuel['nb_effectif_paris']:.1f}".replace(".", ","),
                 detail=f"pour {len(b['par_ligne'])} lignes"),
        ui.carte("Plus gros contributeur", pct(premiere["part_risque"], signe=False, decimales=1),
                 detail=f"{premiere['nom']} ({pct(premiere['poids'], signe=False, decimales=1)} de la valeur)"),
    ]))

    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section("Part de la valeur et part du risque",
                              "Les 20 plus gros contributeurs au risque"))
        graphique(gi.fig_poids_et_risque(b["par_ligne"]))
    with droite, st.container(border=True):
        html(ui.titre_section("Par région"))
        r = b["par_region"]
        st.dataframe(pd.DataFrame({
            "Région": r.index,
            "Part de la valeur": [pct(v, signe=False, decimales=1) for v in r["poids"]],
            "Part du risque": [pct(v, signe=False, decimales=1) for v in r["part_risque"]],
        }), hide_index=True, width="stretch")
        html(ui.note("Une ligne dont la part du risque dépasse sa part de la valeur est plus volatile "
                     "ou plus corrélée au reste du portefeuille que la moyenne."))

    with st.container(border=True):
        html(ui.titre_section("Quatre façons de répartir les mêmes titres",
                              "La parité des risques égalise la contribution de chaque ligne au risque"))
        c = b["comparaison"]
        st.dataframe(pd.DataFrame({
            "Allocation": c.index,
            "Rendement espéré": [pct(v) for v in c["rendement"]],
            "Volatilité": [pct(v, signe=False) for v in c["volatilite"]],
            "Sharpe": [nombre(v) for v in c["sharpe"]],
            "Ratio de diversification": [nombre(v) for v in c["ratio_diversification"]],
            "Nombre effectif de paris": [f"{v:.1f}".replace(".", ",") for v in c["nb_effectif_paris"]],
            "Contribution maximale": [pct(v, signe=False, decimales=1) for v in c["part_max"]],
        }), hide_index=True, width="stretch")
        with st.expander("Voir les poids de chaque allocation"):
            p = b["poids"]
            st.dataframe(p.assign(**{col: (p[col] * 100).round(2) for col in p.columns if col != "nom"}),
                         width="stretch")


# ----------------------------------------------------------------------
# 3. Backtest
# ----------------------------------------------------------------------
def _backtest(res, cle, taux_sans_risque):
    with st.container(border=True):
        html(ui.titre_section("Paramètres", "Mêmes titres et mêmes poids de départ que le portefeuille actuel"))
        a, b, c = st.columns(3)
        frais = a.slider("Frais de transaction (%)", 0.0, 0.5, 0.10, 0.05) / 100
        capital = b.number_input("Capital pour la comparaison DCA (€)", min_value=1000, max_value=10_000_000,
                                 value=10_000, step=1000)
        nb_mois = c.slider("Durée de l'investissement progressif (mois)", 3, 24, 12)
    try:
        courbes, stats, courbes_dca, resume_dca = _calcul_backtest(cle, res, frais, capital, nb_mois,
                                                                    taux_sans_risque)
    except Exception as erreur:
        st.warning(f"Backtest indisponible : {erreur}")
        return

    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section("Rééquilibrer ou non ?", f"Base 100 · frais de {pct(frais, signe=False)} par transaction"))
        graphique(gi.fig_lignes(courbes, format_y=".1f", base100=True))
    with droite, st.container(border=True):
        html(ui.titre_section("Résultats"))
        st.dataframe(pd.DataFrame({
            "Stratégie": stats.index,
            "Rendement annualisé": [pct(v) for v in stats["rendement_annualise"]],
            "Volatilité": [pct(v, signe=False) for v in stats["volatilite"]],
            "Max drawdown": [pct(v) for v in stats["max_drawdown"]],
            "Sharpe": [nombre(v) for v in stats["sharpe"]],
            "Rotation / an": [pct(v, signe=False, decimales=0) for v in stats["rotation_annuelle"]],
        }), hide_index=True, width="stretch")
        html(ui.note("Rééquilibrer revient à vendre ce qui a monté pour acheter ce qui a baissé : cela "
                     "maintient le risque voulu, mais coûte des frais et peut freiner la performance "
                     "quand une tendance dure."))

    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section("Investir en une fois ou progressivement ?",
                              f"{euros(capital)} investis dès le premier jour ou en {nb_mois} versements mensuels"))
        graphique(gi.fig_lignes(courbes_dca, format_y=",.0f", suffixe=" €"))
    with droite, st.container(border=True):
        html(ui.titre_section("Comparaison"))
        st.dataframe(pd.DataFrame({
            "Stratégie": resume_dca.index,
            "Valeur finale": [euros(v) for v in resume_dca["valeur_finale"]],
            "Gain": [euros(v, signe=True) for v in resume_dca["gain"]],
            "Valeur la plus basse": [euros(v) for v in resume_dca["pire_valeur"]],
        }), hide_index=True, width="stretch")
        html(ui.note("Sur un marché haussier, investir en une fois rapporte en général davantage ; "
                     "l'investissement progressif réduit le risque d'investir juste avant une baisse. "
                     "L'argent en attente est rémunéré au taux sans risque."))
