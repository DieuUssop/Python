"""
vues_conseil.py — Espace "Conseil patrimonial" du tableau de bord :
profil de risque du client, fiscalité des enveloppes, stress tests.

Appelé par app.py : vues_conseil.afficher(res, cle).
"""

import pandas as pd
import streamlit as st

from . import fiscalite, stress
from . import graphiques_interactifs as gi
from . import interface as ui
from . import profil as pf
from .interface import euros, pct


def html(morceau):
    st.markdown(morceau, unsafe_allow_html=True)


def graphique(figure):
    st.plotly_chart(figure, width="stretch", config=gi.CONFIG_PLOTLY)


# ----------------------------------------------------------------------
# Calculs mis en cache
# ----------------------------------------------------------------------
# Le paramètre "_res" commence par "_" : Streamlit ne cherche pas à le
# "hacher" (trop volumineux) ; c'est "cle" qui identifie le calcul.
@st.cache_data(show_spinner="Rejeu des crises passées (historique depuis 2008)...")
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
    onglets = st.tabs(["Profil client", "Fiscalité", "Stress tests"])
    with onglets[0]:
        _profil(res)
    with onglets[1]:
        _fiscalite(res)
    with onglets[2]:
        _stress(res, cle)


# ----------------------------------------------------------------------
# 1. Profil de risque et adéquation
# ----------------------------------------------------------------------
def _profil(res):
    ind = res["indicateurs"]
    gauche, droite = st.columns([3, 2], gap="medium")

    with gauche, st.container(border=True):
        html(ui.titre_section("Questionnaire client", "Inspiré du test d'adéquation MiFID II · 7 questions"))
        reponses = []
        for i, (question, options) in enumerate(pf.QUESTIONNAIRE):
            choix = st.radio(f"{i + 1}. {question}", range(len(options)), index=len(options) // 2,
                             format_func=lambda k, o=options: o[k][0], key=f"question_{i}")
            reponses.append(choix)

    resultat = pf.profil_depuis_reponses(reponses)
    profil = resultat["profil"]
    test = pf.adequation(profil, ind["volatilite"], ind["max_drawdown"], part_actions=1.0)

    with droite:
        html(ui.grille([
            ui.carte("Profil du client", profil.nom, detail=f"Score {resultat['score']} / {resultat['score_max']}"),
            ui.carte("Risque du portefeuille", f"SRI {test['sri']} / 7",
                     detail=f"Volatilité {pct(ind['volatilite'], signe=False)}"),
        ]))
        if resultat["plafonne_par_tolerance"]:
            html(ui.note(f"Le score correspond au profil « {resultat['profil_selon_score'].nom} », mais la "
                         "perte maximale acceptée plafonne le profil : le critère le plus prudent l'emporte.",
                         attention=True))
        html(ui.verdict(
            test["adapte"],
            "Portefeuille adapté au profil" if test["adapte"] else "Portefeuille trop risqué pour ce profil",
            profil.description if test["adapte"] else
            f"Pour respecter le profil, conserver environ {pct(test['part_risquee_conseillee'], signe=False, decimales=0)} "
            f"du capital sur ce portefeuille et placer {pct(test['part_sans_risque_conseillee'], signe=False, decimales=0)} "
            "sur un support sans risque (fonds en euros, monétaire).",
        ))
        with st.container(border=True):
            html(ui.titre_section("Indicateur de risque (SRI)", "Échelle PRIIPs de 1 à 7, estimée à partir de la volatilité"))
            html(ui.echelle_sri(test["sri"]))
            html(ui.titre_section("Test d'adéquation"))
            html(ui.tableau_criteres(test["criteres"], [
                lambda v: pct(v, signe=False, decimales=1), lambda v: pct(v, signe=False, decimales=1),
                lambda v: pct(v, signe=False, decimales=0), lambda v: f"{v:.0f}",
            ]))
            html(ui.note("Le portefeuille est entièrement investi en actions (ETF actions compris). "
                         "Le SRI réglementaire se calcule à partir de la VaR (Cornish-Fisher) : "
                         "la volatilité en donne ici une approximation."))


# ----------------------------------------------------------------------
# 2. Fiscalité des enveloppes
# ----------------------------------------------------------------------
def _fiscalite(res):
    resume = res["resume"]
    anciennete = (res["historique"].index[-1] - res["date_ouverture"]).days / 365.25

    with st.container(border=True):
        html(ui.titre_section("Hypothèses", f"Portefeuille ouvert le {res['date_ouverture']:%d/%m/%Y} "
                                             f"(ancienneté : {anciennete:.1f} ans) · taux 2026"))
        a, b = st.columns(2)
        situation = a.radio("Situation familiale (abattement assurance-vie)", ["célibataire", "couple"],
                            horizontal=True, format_func=str.capitalize)
        croissance = b.slider("Rendement annuel supposé pour les sorties futures (%)", 0.0, 10.0, 5.0, 0.5) / 100

    # Sortie aujourd'hui
    lignes = fiscalite.comparer_enveloppes(resume["gain_total"], resume["montant_investi"], anciennete,
                                           resume["dividendes"], situation)
    cartes = []
    for ligne in lignes:
        attente = ligne["annees_avant_avantage"]
        detail = ("Pas d'avantage lié à la durée" if attente is None else
                  "Avantage fiscal acquis" if attente == 0 else f"Avantage fiscal dans {attente:.1f} an(s)")
        cartes.append(ui.carte(f"Sortie {ligne['enveloppe']}", euros(ligne["gain_net"], signe=True),
                               detail=ui.pastille(f"impôts {pct(ligne['taux_effectif'], signe=False, decimales=1)}",
                                                  "neutre") + f" {detail}"))
    html(ui.titre_section("Si tout était vendu aujourd'hui", f"Gain brut : {euros(resume['gain_total'], signe=True)}"))
    html(ui.grille(cartes))

    tableau = pd.DataFrame([{
        "Enveloppe": l["enveloppe"],
        "Gain brut": euros(l["gain_brut"], signe=True),
        "Impôt sur le revenu": euros(l["impot_revenu"]),
        "Prélèvements sociaux": euros(l["prelevements_sociaux"]),
        "Gain net": euros(l["gain_net"], signe=True),
        "Performance brute": pct(l["performance_brute"]),
        "Performance nette": pct(l["performance_nette"]),
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
        html(ui.titre_section("Gain net selon l'année de sortie",
                              f"Hypothèse : {pct(croissance, signe=False, decimales=1)} par an · "
                              "sauts : 5 ans pour le PEA, 8 ans pour l'assurance-vie"))
        graphique(gi.fig_fiscalite_horizon(pd.DataFrame(courbes, index=annees)))
    with droite, st.container(border=True):
        part, exclus = fiscalite.eligibilite_pea(res["positions"])
        html(ui.titre_section("Éligibilité au PEA", "Actions européennes (UE / EEE) et fonds éligibles"))
        html(ui.grille([ui.carte("Part éligible au PEA", pct(part, signe=False, decimales=0),
                                 detail=f"{len(exclus)} ligne(s) non éligible(s)")]))
        remarques = []
        if part < 1:
            remarques.append("Seule la part éligible peut être logée dans un PEA ; le reste irait sur un "
                             "compte-titres ou en unités de compte d'assurance-vie.")
        if resume["montant_investi"] > 150_000:
            remarques.append("Le montant investi dépasse le plafond de versements du PEA (150 000 €) et le "
                             "seuil de 150 000 € de primes au-delà duquel l'assurance-vie est taxée à 12,8 % "
                             "au lieu de 7,5 % après 8 ans (non modélisé).")
        remarques.append("Taux 2026 : flat tax de 31,4 % (12,8 % + 18,6 % de prélèvements sociaux) ; "
                         "assurance-vie : prélèvements sociaux maintenus à 17,2 %.")
        for r in remarques:
            html(ui.note(r))


# ----------------------------------------------------------------------
# 3. Stress tests
# ----------------------------------------------------------------------
def _stress(res, cle):
    try:
        historiques, detail, hypothetiques, source = _calcul_stress(cle, res)
    except Exception as erreur:
        st.warning(f"Stress tests indisponibles : {erreur}")
        return

    pire = historiques.loc[historiques["variation"].idxmin()]
    html(ui.grille([
        ui.carte("Pire scénario historique", pct(pire["variation"]), detail=pire["scenario"]),
        ui.carte("Perte correspondante", euros(pire["perte_euros"], signe=True),
                 detail=f"Sur {euros(res['resume']['valeur_actuelle'])} aujourd'hui"),
        ui.carte("Bêta du portefeuille", f"{res['avances']['beta']:.2f}".replace(".", ","),
                 detail="Sensibilité aux marchés actions"),
    ]))

    gauche, droite = st.columns(2, gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section("Crises passées rejouées sur le portefeuille actuel",
                              "Variation du plus haut au plus bas du marché"))
        graphique(gi.fig_barres_signees(historiques["variation"] * 100, historiques["scenario"],
                                        lambda v: f"{v:+.1f} %".replace(".", ",")))
    with droite, st.container(border=True):
        html(ui.titre_section("Chocs hypothétiques", "Actions : bêta × choc · Dollar : part investie en dollars"))
        graphique(gi.fig_barres_signees(hypothetiques["variation"] * 100, hypothetiques["scenario"],
                                        lambda v: f"{v:+.1f} %".replace(".", ",")))

    with st.container(border=True):
        html(ui.titre_section("Détail des scénarios historiques"))
        st.dataframe(pd.DataFrame({
            "Scénario": historiques["scenario"],
            "Période": [f"{d:%d/%m/%Y} → {f:%d/%m/%Y}" for d, f in zip(historiques["debut"], historiques["fin"])],
            "Variation": [pct(v) for v in historiques["variation"]],
            "Gain / perte": [euros(v, signe=True) for v in historiques["perte_euros"]],
            "Part estimée par un indice": [pct(v, signe=False, decimales=0) for v in historiques["part_proxy"]],
        }), hide_index=True, width="stretch")
        scenario = st.selectbox("Voir le détail ligne par ligne", historiques["scenario"])
        lignes = detail[detail["scenario"] == scenario].sort_values("variation")
        st.dataframe(pd.DataFrame({
            "Titre": lignes["nom"], "Variation": [pct(v) for v in lignes["variation"]], "Source": lignes["source"],
        }), hide_index=True, width="stretch", height=300)
        html(ui.note("Quand un titre n'était pas encore coté, l'indice boursier de sa région sert "
                     "d'approximation. Variations en devise locale, hors dividendes. "
                     f"Données : {source}."))
