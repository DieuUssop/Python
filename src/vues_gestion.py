"""
vues_gestion.py — Espace "Gestion d'actifs" du tableau de bord :
attribution de performance, budget de risque, backtest de stratégies.

Appelé par app.py : vues_gestion.afficher(res, cle, taux_sans_risque).
Les textes affichés passent par t() (traduction) ; les données issues des
calculs (régions, stratégies...) passent par td() à l'affichage.
"""

import pandas as pd
import streamlit as st

from . import attribution, backtest, budget_risque
from . import graphiques_interactifs as gi
from . import interface as ui
from .interface import euros, nombre, pct
from .langues import t, td


def html(morceau):
    st.markdown(morceau, unsafe_allow_html=True)


def graphique(figure):
    st.plotly_chart(figure, width="stretch", config=gi.CONFIG_PLOTLY)


# ----------------------------------------------------------------------
# Calculs mis en cache ("_res" n'est pas haché : c'est "cle" qui identifie le calcul)
# ----------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def _calcul_attribution(cle, _res):
    debut = _res["historique"].index[0] - pd.Timedelta(days=10)
    cours_indices = attribution.rendements_indices(debut)
    return attribution.attribution_poche_actions(_res, cours_indices)


@st.cache_data(show_spinner=False)
def _calcul_budget(cle, _res, taux_sans_risque):
    return budget_risque.analyse_budget_risque(_res["prix_hist"], _res["positions"], taux_sans_risque)


@st.cache_data(show_spinner=False)
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
    onglets = st.tabs([t("Attribution de performance"), t("Budget de risque"), t("Backtest de stratégies")])
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
        with st.spinner(t("Attribution de performance (téléchargement des indices régionaux)...")):
            a = _calcul_attribution(cle, res)
    except Exception as erreur:
        st.warning(t("Attribution indisponible : {erreur}", erreur=erreur))
        return
    effets = a["effets"]
    ecart = a["Rp"] - a["Rb"]
    html(ui.grille([
        ui.carte(t("Portefeuille"), pct(a["Rp"]), detail=t("Rendement des positions (composé)")),
        ui.carte(t("Indice de référence"), pct(a["Rb"]), detail=t("MSCI ACWI (poids régionaux)")),
        ui.carte(t("Écart"), pct(ecart), detail=ui.pastille(t("surperformance") if ecart >= 0
                                                            else t("sous-performance"), ui.tendance(ecart))),
        ui.carte(t("Effet allocation"), pct(effets["allocation"]), detail=t("Choix des régions")),
        ui.carte(t("Effet sélection"), pct(effets["selection"]), detail=t("Choix des titres")),
        ui.carte(t("Effet interaction"), pct(effets["interaction"]), detail=t("Effet croisé")),
    ]))

    if a["part_actions"] < 0.995:
        html(ui.note(t("Portefeuille diversifié : l'attribution porte sur la poche actions ({part} du portefeuille "
                       "aujourd'hui), comparée à un indice actions. Les obligations et l'or sont exclus du calcul.",
                       part=pct(a["part_actions"], signe=False, decimales=0))))
    hors_indice = a["par_region"].loc[~a["par_region"].index.isin(attribution.POIDS_INDICE), "poids_portefeuille"].sum()
    if hors_indice > 0.2:
        html(ui.note(t("{part} du portefeuille n'est pas classé dans une région de l'indice (ETF monde, titres "
                       "absents du référentiel) : l'attribution est surtout pertinente pour un portefeuille de "
                       "lignes directes comme le fonds actions monde.",
                       part=pct(hors_indice, signe=False, decimales=0)), attention=True))

    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section(t("Effets par région"), t("La somme de tous les effets est égale à l'écart avec l'indice")))
        graphique(gi.fig_effets_attribution(a["par_region"]))
    with droite, st.container(border=True):
        html(ui.titre_section(t("Effets cumulés dans le temps"), t("Lissage de Cariño")))
        cumul = a["mensuel"][["allocation_relie", "selection_relie", "interaction_relie"]].cumsum()
        cumul.columns = [t("Allocation"), t("Sélection"), t("Interaction")]
        graphique(gi.fig_lignes(cumul, format_y=".1%", hauteur=400))

    with st.container(border=True):
        html(ui.titre_section(t("Détail par région")))
        p = a["par_region"]
        st.dataframe(pd.DataFrame({
            t("Région"): [td(r) for r in p.index],
            t("Poids portefeuille"): [pct(v, signe=False, decimales=1) for v in p["poids_portefeuille"]],
            t("Poids indice"): [pct(v, signe=False, decimales=1) for v in p["poids_indice"]],
            t("Rendement portefeuille"): [pct(v) for v in p["rendement_portefeuille"]],
            t("Rendement indice"): [pct(v) for v in p["rendement_indice"]],
            t("Allocation"): [pct(v) for v in p["allocation"]],
            t("Sélection"): [pct(v) for v in p["selection"]],
            t("Interaction"): [pct(v) for v in p["interaction"]],
            "Total": [pct(v) for v in p["total"]],
        }), hide_index=True, width="stretch")
        html(ui.note(t("Lecture : un effet d'allocation positif signifie que le portefeuille a surpondéré des "
                       "régions qui ont fait mieux que l'indice ; un effet de sélection positif, qu'il a choisi "
                       "dans une région des titres qui ont fait mieux que l'indice de cette région. "
                       "Indices régionaux hors dividendes, convertis en euros.")))


# ----------------------------------------------------------------------
# 2. Budget de risque et parité des risques
# ----------------------------------------------------------------------
def _budget(res, cle, taux_sans_risque):
    try:
        with st.spinner(t("Calcul du budget de risque...")):
            b = _calcul_budget(cle, res, taux_sans_risque)
    except Exception as erreur:
        st.warning(t("Budget de risque indisponible : {erreur}", erreur=erreur))
        return
    actuel = b["comparaison"].loc["Portefeuille actuel"]
    premiere = b["par_ligne"].iloc[0]
    html(ui.grille([
        ui.carte(t("Volatilité"), pct(actuel["volatilite"], signe=False), detail=t("Estimée sur l'historique")),
        ui.carte(t("Ratio de diversification"), nombre(actuel["ratio_diversification"]),
                 detail=t("1 = aucune diversification")),
        ui.carte(t("Nombre effectif de paris"), nombre(actuel["nb_effectif_paris"], 1),
                 detail=t("pour {n} lignes", n=len(b["par_ligne"]))),
        ui.carte(t("Plus gros contributeur"), pct(premiere["part_risque"], signe=False, decimales=1),
                 detail=t("{nom} ({part} de la valeur)", nom=premiere["nom"],
                          part=pct(premiere["poids"], signe=False, decimales=1))),
    ]))

    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section(t("Part de la valeur et part du risque"),
                              t("Les 20 plus gros contributeurs au risque")))
        graphique(gi.fig_poids_et_risque(b["par_ligne"]))
    with droite, st.container(border=True):
        html(ui.titre_section(t("Par région")))
        r = b["par_region"]
        st.dataframe(pd.DataFrame({
            t("Région"): [td(x) for x in r.index],
            t("Part de la valeur"): [pct(v, signe=False, decimales=1) for v in r["poids"]],
            t("Part du risque"): [pct(v, signe=False, decimales=1) for v in r["part_risque"]],
        }), hide_index=True, width="stretch")
        html(ui.note(t("Une ligne dont la part du risque dépasse sa part de la valeur est plus volatile "
                       "ou plus corrélée au reste du portefeuille que la moyenne.")))

    with st.container(border=True):
        html(ui.titre_section(t("Quatre façons de répartir les mêmes titres"),
                              t("La parité des risques égalise la contribution de chaque ligne au risque")))
        c = b["comparaison"]
        st.dataframe(pd.DataFrame({
            t("Allocation"): [td(x) for x in c.index],
            t("Rendement espéré"): [pct(v) for v in c["rendement"]],
            t("Volatilité"): [pct(v, signe=False) for v in c["volatilite"]],
            "Sharpe": [nombre(v) for v in c["sharpe"]],
            t("Ratio de diversification"): [nombre(v) for v in c["ratio_diversification"]],
            t("Nombre effectif de paris"): [nombre(v, 1) for v in c["nb_effectif_paris"]],
            t("Contribution maximale"): [pct(v, signe=False, decimales=1) for v in c["part_max"]],
        }), hide_index=True, width="stretch")
        with st.expander(t("Voir les poids de chaque allocation")):
            p = b["poids"]
            p = p.assign(**{col: (p[col] * 100).round(2) for col in p.columns if col != "nom"})
            st.dataframe(p.rename(columns={col: td(col) if col != "nom" else t("Titre") for col in p.columns}),
                         width="stretch")


# ----------------------------------------------------------------------
# 3. Backtest
# ----------------------------------------------------------------------
def _backtest(res, cle, taux_sans_risque):
    with st.container(border=True):
        html(ui.titre_section(t("Paramètres"), t("Mêmes titres et mêmes poids de départ que le portefeuille actuel")))
        a, b, c = st.columns(3)
        frais = a.slider(t("Frais de transaction (%)"), 0.0, 0.5, 0.10, 0.05) / 100
        capital = b.number_input(t("Capital pour la comparaison DCA (€)"), min_value=1000, max_value=10_000_000,
                                 value=10_000, step=1000)
        nb_mois = c.slider(t("Durée de l'investissement progressif (mois)"), 3, 24, 12)
    try:
        with st.spinner(t("Backtest des stratégies...")):
            courbes, stats, courbes_dca, resume_dca = _calcul_backtest(cle, res, frais, capital, nb_mois,
                                                                        taux_sans_risque)
    except Exception as erreur:
        st.warning(t("Backtest indisponible : {erreur}", erreur=erreur))
        return

    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section(t("Rééquilibrer ou non ?"),
                              t("Base 100 · frais de {frais} par transaction", frais=pct(frais, signe=False))))
        graphique(gi.fig_lignes(courbes, format_y=".1f", base100=True))
    with droite, st.container(border=True):
        html(ui.titre_section(t("Résultats")))
        st.dataframe(pd.DataFrame({
            t("Stratégie"): [td(x) for x in stats.index],
            t("Rendement annualisé"): [pct(v) for v in stats["rendement_annualise"]],
            t("Volatilité"): [pct(v, signe=False) for v in stats["volatilite"]],
            "Max drawdown": [pct(v) for v in stats["max_drawdown"]],
            "Sharpe": [nombre(v) for v in stats["sharpe"]],
            t("Rotation / an"): [pct(v, signe=False, decimales=0) for v in stats["rotation_annuelle"]],
        }), hide_index=True, width="stretch")
        html(ui.note(t("Rééquilibrer revient à vendre ce qui a monté pour acheter ce qui a baissé : cela "
                       "maintient le risque voulu, mais coûte des frais et peut freiner la performance "
                       "quand une tendance dure.")))

    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section(t("Investir en une fois ou progressivement ?"),
                              t("{montant} investis dès le premier jour ou en {n} versements mensuels",
                                montant=euros(capital), n=nb_mois)))
        graphique(gi.fig_lignes(courbes_dca, format_y=",.0f", euros=True))
    with droite, st.container(border=True):
        html(ui.titre_section(t("Comparaison")))
        st.dataframe(pd.DataFrame({
            t("Stratégie"): [td(x) for x in resume_dca.index],
            t("Valeur finale"): [euros(v) for v in resume_dca["valeur_finale"]],
            t("Gain"): [euros(v, signe=True) for v in resume_dca["gain"]],
            t("Valeur la plus basse"): [euros(v) for v in resume_dca["pire_valeur"]],
        }), hide_index=True, width="stretch")
        html(ui.note(t("Sur un marché haussier, investir en une fois rapporte en général davantage ; "
                       "l'investissement progressif réduit le risque d'investir juste avant une baisse. "
                       "L'argent en attente est rémunéré au taux sans risque.")))
