"""
vues_expositions.py — Onglet « Expositions » de l'espace « Analyse du portefeuille » :
à quoi le portefeuille est réellement exposé, et est-il vraiment diversifié ?

    1. Synthèse : une pastille par dimension (géographie, secteurs, devises,
       concentration, taux, diversification réelle) ;
    2. Constats : ce qu'on observe, le risque associé, des pistes ;
    3. Détail : écarts à l'indice, devises, concentration, corrélations.

Les calculs sont dans src/expositions.py (sans affichage, testés à part).
"""

import pandas as pd
import streamlit as st

from . import budget_risque, composition_etf, expositions as ex, indices
from . import graphiques_interactifs as gi
from . import interface as ui
from .interface import nombre, pct
from .langues import t, td

DIMENSIONS = {"geographie": "Géographie", "secteurs": "Secteurs", "devises": "Devises",
              "concentration": "Concentration", "taux": "Taux", "diversification": "Diversification réelle"}


def html(morceau):
    st.markdown(morceau, unsafe_allow_html=True)


def graphique(figure):
    st.plotly_chart(gi.theme_figure(figure), width="stretch", config=gi.CONFIG_PLOTLY)


@st.cache_data(show_spinner=False)
def _calculs(cle, _res):
    positions = _res["positions"]
    transp = ex.transparence(positions)
    div = ex.diversification(_res["prix_hist"], positions)
    try:
        budget = budget_risque.analyse_budget_risque(_res["prix_hist"], positions, 0.0)
        part_risque = budget["par_ligne"]["part_risque"]
    except Exception:
        part_risque = None
    try:
        from .analyse import charger_fiches
        fiches = charger_fiches()
    except Exception:
        fiches = None
    return transp, div, part_risque, ex.doublons_probables(positions, transp, fiches)


def _p0(x):
    return pct(x, signe=False, decimales=0)


def _p1(x):
    return pct(x, signe=False, decimales=1)


def afficher(res, cle, code_indice):
    positions = res["positions"]
    with st.spinner(t("Analyse des expositions...")):
        transp, div, part_risque, doublons = _calculs(cle, res)
    fiche = indices.indice(code_indice)
    reference = fiche if fiche.composition else indices.indice("IUSQ.DE")   # actions : marché mondial par défaut

    # ------------------------------------------------------------------ en-tête et profil
    gauche, droite = st.columns([3, 1], vertical_alignment="bottom")
    with gauche:
        html(ui.titre_section(t("Expositions et diversification"),
                              t("Analyse en transparence : chaque ETF est réparti selon la composition de son "
                                "indice (approximation au {date})", date=composition_etf.DATE_SOURCE)))
    profil = droite.selectbox(t("Seuils adaptés au profil"), ex.PROFILS, format_func=td, index=1,
                              help=t("Les seuils d'alerte (devises, concentration, secteurs...) sont plus stricts "
                                     "pour un profil prudent que pour un profil dynamique."),
                              key="profil_expositions")
    constats = ex.diagnostic(positions, transp, div, profil=profil, f_pct=_p0, f_nom=td, doublons=doublons)
    niveaux = ex.synthese(constats)

    # ------------------------------------------------------------------ 1. synthèse
    pays = ex.repartition(transp, "pays", "Actions", normaliser=True).drop(ex.NON_CLASSE, errors="ignore")
    secteurs = ex.repartition(transp, "secteur", "Actions", normaliser=True).drop(ex.NON_CLASSE, errors="ignore")
    devises = ex.repartition(transp, "devise")
    conc = ex.concentration(positions, transp)
    tx = ex.taux(positions)
    chiffres = {
        "geographie": t("1er pays : {pays} {poids}", pays=td(pays.index[0]), poids=_p0(pays.iloc[0]))
        if len(pays) else "—",
        "secteurs": t("1er secteur : {secteur} {poids}", secteur=td(secteurs.index[0]), poids=_p0(secteurs.iloc[0]))
        if len(secteurs) else "—",
        "devises": t("Hors euro : {poids}", poids=_p0(devises.drop(["EUR", "Or"], errors="ignore").sum())),
        "concentration": t("Plus grosse ligne : {poids}", poids=_p1(conc["poids"].iloc[0])),
        "taux": t("Duration : {d} ans", d=nombre(tx["duration"], 1)) if tx else t("Pas d'obligations"),
        "diversification": t("Corrélation moyenne : {rho}", rho=nombre(div["moyenne"])),
    }
    html(ui.synthese([(t(DIMENSIONS[d]), niveaux[d], chiffres[d]) for d in ex.DIMENSIONS]))

    # ------------------------------------------------------------------ 2. constats
    a_traiter = [c for c in constats if c["niveau"] != "ok"]
    positifs = [c for c in constats if c["niveau"] == "ok"]

    def carte_constat(c):
        v = c["valeurs"]
        return ui.constat(c["niveau"], t(DIMENSIONS[c["dimension"]]), t(c["titre"], **v),
                          t(c["risque"], **v) if c["risque"] else "", [t(p, **v) for p in c["pistes"]])

    with st.container(border=True):
        html(ui.titre_section(t("Constats et pistes"),
                              t("{n} point(s) à surveiller ou à corriger", n=len(a_traiter)) if a_traiter
                              else t("Aucun point d'attention")))
        for c in a_traiter:
            html(carte_constat(c))
        if positifs:
            with st.expander(t("Points positifs ({n})", n=len(positifs)), expanded=not a_traiter):
                for c in positifs:
                    html(carte_constat(c))
        html(ui.note(t("Analyse pédagogique fondée sur des règles simples et des données passées : elle ne "
                       "constitue pas un conseil en investissement.")))

    # ------------------------------------------------------------------ 3. détail
    onglets = st.tabs([t("Géographie et secteurs"), t("Devises et taux"), t("Concentration"),
                       t("Corrélations")])
    ecarts = ex.ecarts_indice(transp, reference)
    nom_ref = t(reference.court)

    with onglets[0]:
        gauche, droite = st.columns(2, gap="medium")
        for colonne_st, cle_ecart, titre in [(gauche, "region", "Régions (poche actions)"),
                                             (droite, "secteur", "Secteurs (poche actions)")]:
            with colonne_st, st.container(border=True):
                html(ui.titre_section(t(titre), t("Portefeuille et {indice}", indice=nom_ref)))
                if cle_ecart in ecarts and len(ecarts[cle_ecart]):
                    tableau = ecarts[cle_ecart].sort_values("portefeuille", ascending=False)
                    graphique(gi.fig_comparaison(tableau, "portefeuille", "indice", t("Portefeuille"), nom_ref))
                else:
                    st.caption(t("Pas de poche actions à analyser."))
        if "pays" in ecarts and len(ecarts["pays"]):
            with st.container(border=True):
                html(ui.titre_section(t("Principaux écarts par pays"),
                                      t("Sur- et sous-pondérations de la poche actions face à {indice}",
                                        indice=nom_ref)))
                e = ecarts["pays"].head(10)
                st.dataframe(pd.DataFrame({
                    t("Pays"): [td(x) for x in e.index],
                    t("Portefeuille"): [_p1(v) for v in e["portefeuille"]],
                    nom_ref: [_p1(v) for v in e["indice"]],
                    t("Écart"): [pct(v, decimales=1) for v in e["ecart"]],
                }), hide_index=True, width="stretch")
        if part_risque is not None:
            with st.container(border=True):
                html(ui.titre_section(t("Part de la valeur et part du risque par région"),
                                      t("Une région qui apporte plus de risque que de valeur est plus volatile ou "
                                        "plus corrélée au reste")))
                r = ex.risque_par_groupe(transp, part_risque, "region")
                graphique(gi.fig_comparaison(r, "part_risque", "poids", t("Part du risque"), t("Part de la valeur")))

    with onglets[1]:
        gauche, droite = st.columns(2, gap="medium")
        with gauche, st.container(border=True):
            html(ui.titre_section(t("Exposition réelle aux devises"),
                                  t("Tout le portefeuille, ETF répartis selon les pays de leur indice")))
            graphique(gi.fig_anneau(devises, positions["valeur"].sum()))
            html(ui.note(t("Un ETF coté en euros reste exposé aux devises des actions qu'il contient, sauf s'il "
                           "est couvert (« EUR Hedged »). L'or, coté en dollars, est compté à part.")))
        with droite, st.container(border=True):
            html(ui.titre_section(t("Sensibilité aux taux"), t("Poche obligataire")))
            if tx:
                html(ui.grille([
                    ui.carte(t("Duration moyenne"), t("{d} ans", d=nombre(tx["duration"], 1)),
                             aide=t("Durée de vie moyenne pondérée des flux : mesure la sensibilité aux taux")),
                    ui.carte(t("Si les taux montent de 1 point"), pct(-tx["perte_1pt_pct"], decimales=1),
                             detail=t("≈ {montant}", montant=ui.euros(-tx["perte_1pt"]))),
                ]))
                html(ui.note(t("Approximation : variation du prix ≈ − duration × variation des taux. Les "
                               "obligations retrouvent ensuite un rendement plus élevé.")))
            else:
                st.caption(t("Le portefeuille ne contient pas d'obligations."))

    with onglets[2]:
        html(ui.grille([
            ui.carte(t("Lignes"), str(conc["nb_lignes"]),
                     detail=t("équivalent à {n} lignes de même poids", n=f"{conc['nb_effectif']:.0f}"),
                     aide=t("Nombre effectif = 1 / Σ poids² (inverse de l'indice de Herfindahl)")),
            ui.carte(t("5 premières lignes"), _p0(conc["top5"])),
            ui.carte(t("10 premières lignes"), _p0(conc["top10"])),
            ui.carte(t("Actions de plus de 5 %"), _p0(conc["actions_plus_5"]),
                     detail=t("Limite UCITS : 40 %"),
                     aide=t("Règle 5/10/40 des fonds : une ligne ≤ 10 %, et les lignes > 5 % ≤ 40 % au total")),
        ]))
        with st.container(border=True):
            html(ui.titre_section(t("Les plus grosses lignes"), t("Poids et poids cumulé")))
            w = conc["poids"].head(15)
            st.dataframe(pd.DataFrame({
                t("Titre"): [positions.at[k, "nom"] for k in w.index],
                t("Classe"): [td(positions.at[k, "classe"]) for k in w.index],
                t("Poids"): [_p1(v) for v in w],
                t("Cumul"): [_p1(v) for v in w.cumsum()],
            }), hide_index=True, width="stretch")

    with onglets[3]:
        _correlations(positions, div)


def _correlations(positions, div):
    if len(div["correlations"]) < 2:
        st.caption(t("Au moins deux lignes sont nécessaires."))
        return
    crise = div["crise"]
    html(ui.grille([
        ui.carte(t("Corrélation moyenne"), nombre(div["moyenne"]), detail=t("pondérée par les poids"),
                 aide=t("Corrélation typique entre deux euros investis dans deux lignes différentes")),
        ui.carte(t("Ratio de diversification"), nombre(div["ratio"]), detail=t("1 = aucune diversification"),
                 aide=t("Somme des volatilités pondérées / volatilité du portefeuille")),
        ui.carte(t("Blocs indépendants"), str(div["nb_blocs"]),
                 detail=t("pour {n} lignes", n=len(div["poids"])),
                 aide=t("Groupes de titres corrélés à plus de 0,7 : chacun ne compte que pour un pari")),
        ui.carte(t("Les jours de forte baisse"), nombre(crise) if crise is not None else "—",
                 detail=t("corrélation moyenne (10 % pires jours)"),
                 aide=t("Les corrélations montent pendant les crises : la diversification protège alors moins")),
    ]))
    n = len(div["correlations"])
    vues = ["titre", "classe", "region", "secteur"]
    noms_vues = {"titre": t("Par titre"), "classe": t("Par classe d'actifs"), "region": t("Par région"),
                 "secteur": t("Par secteur")}
    vues = [v for v in vues if v == "titre" or (v in positions.columns and positions[v].nunique() > 1)]
    defaut = "titre" if n <= 20 or len(vues) == 1 else vues[1]
    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        vue = st.segmented_control(t("Afficher"), vues, default=defaut, format_func=lambda v: noms_vues[v],
                                   key="vue_correlations") or defaut
        if vue == "titre":
            html(ui.titre_section(t("Corrélations entre les titres"),
                                  t("Titres regroupés par blocs qui évoluent ensemble · rouge = évoluent ensemble, "
                                    "bleu = en sens inverse")))
            graphique(gi.fig_correlations(div["correlations"], div["ordre"], positions["nom"].to_dict()))
        else:
            groupes = positions[vue].map(td)
            corr, _ = ex.correlations_par_groupe(div["rendements"], div["poids"], groupes)
            html(ui.titre_section(t("Corrélations entre groupes"),
                                  t("Rendement de chaque groupe (lignes pondérées par leur poids)")))
            graphique(gi.fig_correlations(corr, ex.ordre_regroupement(corr)))
        html(ui.note(t("Corrélations historiques des rendements quotidiens ({n} jours) : elles ne sont pas "
                       "garanties à l'avenir.", n=div["nb_jours"])))
    with droite:
        with st.container(border=True):
            html(ui.titre_section(t("Paires les plus corrélées")))
            st.dataframe(pd.DataFrame({
                t("Titres"): [f"{positions.at[a, 'nom']} / {positions.at[b, 'nom']}" for a, b, _ in div["paires"]],
                t("Corrélation"): [nombre(v) for _, _, v in div["paires"]],
                t("Lien"): [t(ex.qualificatif(v)) for _, _, v in div["paires"]],
            }), hide_index=True, width="stretch")
        with st.container(border=True):
            html(ui.titre_section(t("Lignes qui diversifient le mieux"),
                                  t("Corrélation avec le reste du portefeuille")))
            d = div["diversifiants"]
            st.dataframe(pd.DataFrame({
                t("Titre"): [positions.at[k, "nom"] for k in d.index],
                t("Corrélation"): [nombre(v) for v in d.values],
                t("Poids"): [_p1(div["poids"].get(k, 0)) for k in d.index],
            }), hide_index=True, width="stretch")
        if div["blocs"]:
            with st.container(border=True):
                html(ui.titre_section(t("Blocs de titres corrélés"), t("Corrélation moyenne supérieure à 0,7")))
                for b in div["blocs"][:5]:
                    st.markdown(t("**{poids}** · {noms} (corrélation {rho})", poids=_p1(b["poids"]),
                                  noms=", ".join(str(positions.at[k, "nom"]) for k in b["tickers"]),
                                  rho=nombre(b["correlation"])))
