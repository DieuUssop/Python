"""
vues_conseil.py — Espace "Conseil patrimonial" du tableau de bord :
fiscalité des enveloppes et stress tests.

Appelé par app.py : vues_conseil.afficher(res, cle).
Les textes affichés passent par t() (traduction) ; les données issues des
calculs (noms de profils, de scénarios...) passent par td() à l'affichage.
"""

import pandas as pd
import streamlit as st

from . import fiscalite, langues, stress
from . import graphiques_interactifs as gi
from . import interface as ui
from .interface import euros, nombre, pct
from .langues import t, td


def html(morceau):
    st.markdown(morceau, unsafe_allow_html=True)


def graphique(figure):
    st.plotly_chart(gi.theme_figure(figure), width="stretch", config=gi.CONFIG_PLOTLY)


# ----------------------------------------------------------------------
# Calculs mis en cache
# ----------------------------------------------------------------------
# Le paramètre "_res" commence par "_" : Streamlit ne cherche pas à le
# "hacher" (trop volumineux) ; c'est "cle" qui identifie le calcul.
@st.cache_data(show_spinner=False)
def _calcul_stress(cle, _res):
    positions = _res["positions"]
    prix_longs, source = stress.telecharger_historique_long(positions.index)
    historiques, detail = stress.scenarios_historiques(positions, prix_longs)
    hypothetiques = stress.scenarios_hypothetiques(positions, _res["avances"]["beta"])
    return historiques, detail, hypothetiques, source


# ----------------------------------------------------------------------
# Point d'entrée
# ----------------------------------------------------------------------
def afficher(res, cle):
    onglets = st.tabs([t("Fiscalité"), t("Stress tests")])
    with onglets[0]:
        _fiscalite(res)
    with onglets[1]:
        _stress(res, cle)


# ----------------------------------------------------------------------
# 1. Fiscalité des enveloppes
# ----------------------------------------------------------------------
def _fiscalite(res):
    resume = res["resume"]
    anciennete = (res["historique"].index[-1] - res["date_ouverture"]).days / 365.25

    with st.container(border=True):
        html(ui.titre_section(t("Hypothèses"), t("Portefeuille ouvert le {date} (ancienneté : {n} ans) · taux 2026",
                                                  date=langues.date(res["date_ouverture"]),
                                                  n=nombre(anciennete, 1))))
        a, b = st.columns(2)
        situation = a.radio(t("Situation familiale (abattement assurance-vie)"), ["célibataire", "couple"],
                            horizontal=True, format_func=lambda s: td(s).capitalize())
        croissance = b.slider(t("Rendement annuel supposé pour les sorties futures (%)"), 0.0, 10.0, 5.0, 0.5) / 100

    # Sortie aujourd'hui
    lignes = fiscalite.comparer_enveloppes(resume["gain_total"], resume["montant_investi"], anciennete,
                                           resume["dividendes"], situation)
    cartes = []
    for ligne in lignes:
        attente = ligne["annees_avant_avantage"]
        detail = (t("Pas d'avantage lié à la durée") if attente is None else
                  t("Avantage fiscal acquis") if attente == 0 else
                  t("Avantage fiscal dans {n} an(s)", n=nombre(attente, 1)))
        cartes.append(ui.carte(t("Sortie {enveloppe}", enveloppe=td(ligne["enveloppe"])),
                               euros(ligne["gain_net"], signe=True),
                               detail=ui.pastille(t("impôts {taux}", taux=pct(ligne["taux_effectif"], signe=False,
                                                                                decimales=1)), "neutre")
                               + f" {detail}"))
    html(ui.titre_section(t("Si tout était vendu aujourd'hui"),
                          t("Gain brut : {montant}", montant=euros(resume["gain_total"], signe=True))))
    html(ui.grille(cartes))

    tableau = pd.DataFrame([{
        t("Enveloppe"): td(l["enveloppe"]),
        t("Gain brut"): euros(l["gain_brut"], signe=True),
        t("Impôt sur le revenu"): euros(l["impot_revenu"]),
        t("Prélèvements sociaux"): euros(l["prelevements_sociaux"]),
        t("Gain net"): euros(l["gain_net"], signe=True),
        t("Performance brute"): pct(l["performance_brute"]),
        t("Performance nette"): pct(l["performance_nette"]),
    } for l in lignes])
    st.dataframe(tableau, hide_index=True, width="stretch")

    # Gain net selon l'année de sortie
    valeur = resume["valeur_actuelle"]
    annees = list(range(0, 21))
    courbes = {}
    for enveloppe in ["CTO", "PEA", "Assurance-vie"]:
        courbes[enveloppe] = []
        for n in annees:
            gain = resume["gain_total"] + valeur * ((1 + croissance) ** n - 1)
            impot = fiscalite.impot_sortie(gain, anciennete + n, enveloppe, resume["dividendes"], situation)
            courbes[enveloppe].append(gain - impot["total"])
    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section(t("Gain net selon l'année de sortie"),
                              t("Hypothèse : {taux} par an · sauts : 5 ans pour le PEA, 8 ans pour l'assurance-vie",
                                taux=pct(croissance, signe=False, decimales=1))))
        graphique(gi.fig_fiscalite_horizon(pd.DataFrame(courbes, index=annees)))
    with droite, st.container(border=True):
        part, exclus = fiscalite.eligibilite_pea(res["positions"])
        html(ui.titre_section(t("Éligibilité au PEA"), t("Actions européennes (UE / EEE) et fonds éligibles")))
        html(ui.grille([ui.carte(t("Part éligible au PEA"), pct(part, signe=False, decimales=0),
                                 detail=t("{n} ligne(s) non éligible(s)", n=len(exclus)))]))
        remarques = []
        if part < 1:
            remarques.append(t("Seule la part éligible peut être logée dans un PEA ; le reste irait sur un "
                               "compte-titres ou en unités de compte d'assurance-vie."))
        if resume["montant_investi"] > 150_000:
            remarques.append(t("Le montant investi dépasse le plafond de versements du PEA (150 000 €) et le "
                               "seuil de 150 000 € de primes au-delà duquel l'assurance-vie est taxée à 12,8 % "
                               "au lieu de 7,5 % après 8 ans (non modélisé)."))
        remarques.append(t("Taux 2026 : flat tax de 31,4 % (12,8 % + 18,6 % de prélèvements sociaux) ; "
                           "assurance-vie : prélèvements sociaux maintenus à 17,2 %."))
        for r in remarques:
            html(ui.note(r))


# ----------------------------------------------------------------------
# 2. Stress tests
# ----------------------------------------------------------------------
def _stress(res, cle):
    try:
        with st.spinner(t("Rejeu des crises passées (historique depuis 2008)...")):
            historiques, detail, hypothetiques, source = _calcul_stress(cle, res)
    except Exception as erreur:
        st.warning(t("Stress tests indisponibles : {erreur}", erreur=erreur))
        return

    pire = historiques.loc[historiques["variation"].idxmin()]
    html(ui.grille([
        ui.carte(t("Pire scénario historique"), pct(pire["variation"]), detail=td(pire["scenario"])),
        ui.carte(t("Perte correspondante"), euros(pire["perte_euros"], signe=True),
                 detail=t("Sur {montant} aujourd'hui", montant=euros(res["resume"]["valeur_actuelle"]))),
        ui.carte(t("Bêta du portefeuille"), nombre(res["avances"]["beta"]),
                 detail=t("Sensibilité aux marchés actions")),
    ]))

    def texte_pct(v):
        return pct(v / 100, decimales=1)

    gauche, droite = st.columns(2, gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section(t("Crises passées rejouées sur le portefeuille actuel"),
                              t("Variation du plus haut au plus bas du marché")))
        graphique(gi.fig_barres_signees(historiques["variation"] * 100, historiques["scenario"].map(td), texte_pct))
    with droite, st.container(border=True):
        html(ui.titre_section(t("Chocs hypothétiques"),
                              t("Actions : bêta × choc · Dollar : part investie en dollars · Taux : duration")))
        graphique(gi.fig_barres_signees(hypothetiques["variation"] * 100, hypothetiques["scenario"].map(td),
                                        texte_pct))

    with st.container(border=True):
        html(ui.titre_section(t("Détail des scénarios historiques")))
        st.dataframe(pd.DataFrame({
            t("Scénario"): historiques["scenario"].map(td),
            t("Période"): [f"{langues.date(d)} → {langues.date(f)}"
                           for d, f in zip(historiques["debut"], historiques["fin"])],
            t("Variation"): [pct(v) for v in historiques["variation"]],
            t("Gain / perte"): [euros(v, signe=True) for v in historiques["perte_euros"]],
            t("Part estimée par un indice"): [pct(v, signe=False, decimales=0) for v in historiques["part_proxy"]],
        }), hide_index=True, width="stretch")
        scenario = st.selectbox(t("Voir le détail ligne par ligne"), list(historiques["scenario"]), format_func=td)
        lignes = detail[detail["scenario"] == scenario].sort_values("variation")
        st.dataframe(pd.DataFrame({
            t("Titre"): lignes["nom"], t("Variation"): [pct(v) for v in lignes["variation"]],
            t("Source"): lignes["source"].map(td),
        }), hide_index=True, width="stretch", height=300)
        html(ui.note(t("Quand un titre n'était pas encore coté, l'indice boursier de sa région (ou un fonds "
                       "obligataire de même catégorie) sert d'approximation. Variations en devise locale, hors "
                       "dividendes. Données : {source}.",
                       source=source if not langues.anglais() else
                       ("Yahoo Finance (live)" if "direct" in source.lower() else "local cache"))))
