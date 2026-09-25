"""
app.py — Le tableau de bord web du projet (Streamlit).

Lancement (depuis le dossier portfolio_tracker) :
    python -m streamlit run app.py

Une page s'ouvre dans ton navigateur (adresse http://localhost:8501).
Pour arrêter : Ctrl + C dans le terminal.

Organisation :
    - les CALCULS sont dans src/ (analyse.py, optimisation.py...) ;
    - les GRAPHIQUES sont dans src/graphiques_interactifs.py ;
    - l'APPARENCE est dans assets/style.css, .streamlit/config.toml et
      src/interface.py (cartes, bandeau, pastilles) ;
    - les TRADUCTIONS (français / anglais) sont dans src/langues.py et
      src/traductions.py : chaque texte affiché passe par t("texte en français") ;
    - ce fichier se contente d'ASSEMBLER la page.

Comment fonctionne Streamlit ?
    Le fichier est exécuté de haut en bas à chaque interaction (clic,
    changement de réglage...). Chaque st.quelquechose() ajoute un élément
    à la page.
"""

import io
from pathlib import Path

import streamlit as st

from src import config, langues
from src import graphiques_interactifs as gi
from src import interface as ui
from src import vues_conseil, vues_gestion
from src.analyse import analyse_complete
from src.interface import euros, nombre, pct, tendance
from src.langues import t, td
from src.optimisation import optimiser_portefeuille
from src.simulation import parametres_historiques, simuler

FICHIER_PAR_DEFAUT = Path("data/transactions.csv")
# Tous les fichiers de transactions disponibles (ex. transactions_mondial.csv)
FICHIERS_DISPONIBLES = sorted(Path("data").glob("transactions*.csv"),
                              key=lambda f: (f != FICHIER_PAR_DEFAUT, f.name))
FICHIERS_DISPONIBLES = [f for f in FICHIERS_DISPONIBLES if "sauvegarde" not in f.name]
NOMS_PORTEFEUILLES = {"transactions.csv": "Mon portefeuille",
                      "transactions_mondial.csv": "Portefeuille actions monde",
                      "transactions_diversifie.csv": "Portefeuille diversifié (multi-actifs)"}
FEUILLE_DE_STYLE = Path("assets/style.css")

# Indices de référence proposés dans le menu : {code Yahoo: nom affiché}
INDICES = {
    "CW8.PA": "MSCI World (ETF CW8, dividendes réinvestis)",
    "ESE.PA": "S&P 500 (ETF ESE, dividendes réinvestis)",
    "^FCHI": "CAC 40 (hors dividendes)",
    "^STOXX50E": "Euro Stoxx 50 (hors dividendes)",
}
NOMS_COURTS = {"CW8.PA": "MSCI World", "ESE.PA": "S&P 500", "^FCHI": "CAC 40", "^STOXX50E": "Euro Stoxx 50"}

# ----------------------------------------------------------------------
# Langue du visiteur (choisie plus bas avec le sélecteur FR | EN de la barre
# latérale, et mémorisée dans st.session_state)
# ----------------------------------------------------------------------
langues.definir(st.session_state.get("langue", "fr"))

# ----------------------------------------------------------------------
# Configuration de la page (doit être la première commande Streamlit)
# ----------------------------------------------------------------------
st.set_page_config(page_title=t("Suivi de portefeuille"), page_icon="📈", layout="wide")

# On charge la feuille de style (si elle est présente).
if FEUILLE_DE_STYLE.exists():
    st.markdown(f"<style>{FEUILLE_DE_STYLE.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def html(morceau):
    """Affiche un morceau de HTML produit par src/interface.py."""
    st.markdown(morceau, unsafe_allow_html=True)


def graphique(figure):
    """Affiche un graphique Plotly sur toute la largeur disponible."""
    st.plotly_chart(figure, width="stretch", config=gi.CONFIG_PLOTLY)


# ----------------------------------------------------------------------
# Calculs (mis en cache)
# ----------------------------------------------------------------------
# @st.cache_data : Streamlit garde le résultat en mémoire. Tant que les
# paramètres ne changent pas, la fonction n'est pas relancée : la page
# reste rapide. ttl=3600 : le résultat expire au bout d'une heure.
# Les messages d'attente sont affichés à l'appel (st.spinner), dans la langue choisie.
@st.cache_data(ttl=3600, show_spinner=False)
def charger(contenu_csv, indice, taux_sans_risque, niveau_var):
    return analyse_complete(io.BytesIO(contenu_csv), indice, taux_sans_risque, niveau_var)


@st.cache_data(show_spinner=False)
def optimiser(contenu_csv, indice, taux_sans_risque, niveau_var, poids_max):
    res = charger(contenu_csv, indice, taux_sans_risque, niveau_var)
    return optimiser_portefeuille(res["prix_hist"], res["positions"], taux_sans_risque, poids_max)


@st.cache_data(show_spinner=False)
def projeter(valeur, mu, sigma, annees, versement, methode, objectif, rendements, date_depart):
    return simuler(valeur, mu, sigma, annees=annees, versement_mensuel=versement,
                   nb_simulations=config.NB_SIMULATIONS, methode=methode,
                   rendements_historiques=rendements, objectif=objectif or None,
                   date_depart=date_depart)


@st.cache_data(show_spinner=False)
def produire_rapport(contenu_csv, indice, taux_sans_risque, niveau_var, nom_indice):
    """Construit le rapport PDF en mémoire et renvoie son contenu (octets).
    Le rapport PDF reste en français, quelle que soit la langue du tableau de bord."""
    from src.rapport import generer_rapport      # nécessite reportlab
    res = charger(contenu_csv, indice, taux_sans_risque, niveau_var)
    try:
        opti = optimiser_portefeuille(res["prix_hist"], res["positions"], taux_sans_risque, config.POIDS_MAX)
    except Exception:
        opti = None                              # ex. trop peu de titres pour le poids maximal
    rendements = res["indicateurs"]["rendements"]
    mu, sigma = parametres_historiques(rendements)
    sim = simuler(res["resume"]["valeur_actuelle"], mu, sigma, annees=config.HORIZON_PROJECTION,
                  versement_mensuel=config.VERSEMENT_MENSUEL, nb_simulations=config.NB_SIMULATIONS,
                  methode=config.METHODE_SIMULATION, rendements_historiques=rendements,
                  date_depart=res["historique"].index[-1])
    from src.extensions import calculer_extensions   # profil et fiscalité : réglages de src/config.py
    extensions = calculer_extensions(res, taux_sans_risque)
    tampon = io.BytesIO()
    generer_rapport(res, tampon, nom_indice, taux_sans_risque, niveau_var, opti=opti, sim=sim,
                    extensions=extensions)
    return tampon.getvalue()


# ======================================================================
# BARRE LATÉRALE : les réglages
# ======================================================================
with st.sidebar:
    html(ui.marque("Portfolio Tracker", t("Outil de suivi de portefeuille")))

    # Sélecteur de langue : un clic relance la page dans l'autre langue.
    st.segmented_control("Langue / Language", list(langues.LANGUES), format_func=langues.LANGUES.get,
                         default="fr", key="langue", label_visibility="collapsed")

    html(ui.bloc_titre(t("Espace de travail")))
    espace = st.radio(
        "Espace de travail", ["Analyse du portefeuille", "Conseil patrimonial", "Gestion d'actifs"],
        format_func=t, label_visibility="collapsed",
        captions=[t("Performance, risque, optimisation, projection"),
                  t("Profil client, fiscalité, stress tests"),
                  t("Attribution, budget de risque, backtest")],
    )

    html(ui.bloc_titre(t("Données")))
    fichier_choisi = None
    if FICHIERS_DISPONIBLES:
        fichier_choisi = st.selectbox(
            t("Portefeuille"), FICHIERS_DISPONIBLES,
            format_func=lambda f: t(NOMS_PORTEFEUILLES[f.name]) if f.name in NOMS_PORTEFEUILLES else f.name,
            help=t("Fichiers data/transactions*.csv du projet"),
        )
    fichier_envoye = st.file_uploader(
        t("Ou envoyer un autre fichier (CSV)"), type=["csv"],
        help=t("Prioritaire sur le portefeuille choisi ci-dessus"),
    )

    html(ui.bloc_titre(t("Paramètres d'analyse")))
    code_indice = st.selectbox(
        t("Indice de référence"), options=list(INDICES),
        index=list(INDICES).index(config.INDICE_REFERENCE) if config.INDICE_REFERENCE in INDICES else 0,
        format_func=lambda code: t(INDICES[code]),
    )
    taux_sans_risque = st.number_input(
        t("Taux sans risque (% par an)"), min_value=0.0, max_value=10.0,
        value=config.TAUX_SANS_RISQUE * 100, step=0.25, format="%.2f",
        help=t("Taux de la facilité de dépôt de la BCE : 2,50 % depuis le 16/09/2026"),
    ) / 100
    niveau_var = st.select_slider(
        t("Niveau de confiance de la VaR"), options=[0.90, 0.95, 0.99],
        value=config.NIVEAU_CONFIANCE_VAR, format_func=lambda v: pct(v, signe=False, decimales=0),
    )

    st.write("")
    if st.button(t("Actualiser les cours"), icon=":material/refresh:", width="stretch"):
        st.cache_data.clear()   # on oublie les résultats en mémoire...
        st.rerun()              # ... et on relance la page

# ======================================================================
# CHARGEMENT DES DONNÉES
# ======================================================================
if fichier_envoye is not None:
    contenu = fichier_envoye.getvalue()
    nom_fichier = fichier_envoye.name
elif fichier_choisi is not None:
    contenu = fichier_choisi.read_bytes()
    nom_fichier = fichier_choisi.name
else:
    st.error(t("Aucun fichier de transactions : envoyez un fichier CSV depuis la barre latérale."))
    st.stop()

try:
    with st.spinner(t("Récupération des cours et calcul des indicateurs...")):
        res = charger(contenu, code_indice, taux_sans_risque, niveau_var)
except Exception as erreur:  # message clair plutôt qu'un plantage
    st.error(t("Impossible d'analyser le portefeuille : {erreur}", erreur=erreur))
    st.stop()

resume = res["resume"]
positions = res["positions"]
histo = res["historique"]
ind = res["indicateurs"]
av = res["avances"]
nom_indice = t(INDICES[code_indice])
nom_court = NOMS_COURTS[code_indice]
date_debut, date_fin = langues.date(histo.index[0]), langues.date(histo.index[-1])
en_direct = "direct" in res["source_cours"].lower()

with st.sidebar:
    html(ui.bloc_titre(t("Informations")))
    html(ui.infos([
        (t("Fichier"), nom_fichier),
        (t("Opérations"), str(len(res["transactions"]))),
        (t("Période"), f"{date_debut} → {date_fin}"),
        (t("Cours"), res["source_cours"] if not langues.anglais()
         else ("Yahoo Finance (live)" if en_direct else "Local cache (Yahoo Finance unavailable)")),
    ] + [(t("1 € en {devise}", devise=devise), nombre(taux, 4)) for devise, taux in res["taux_actuels"].items()]))

    html(ui.bloc_titre(t("Rapport")))
    cle_rapport = (hash(contenu), code_indice, taux_sans_risque, niveau_var)
    if st.button(t("Préparer le rapport PDF"), icon=":material/picture_as_pdf:", width="stretch",
                 help=t("Le rapport PDF est rédigé en français.")):
        try:
            with st.spinner(t("Génération du rapport...")):
                st.session_state["rapport"] = (cle_rapport, produire_rapport(
                    contenu, code_indice, taux_sans_risque, niveau_var, INDICES[code_indice]))
        except ImportError:
            st.error(t("Installer reportlab : python -m pip install reportlab"))
    # On ne propose le téléchargement que si le rapport correspond aux réglages actuels.
    if st.session_state.get("rapport", (None,))[0] == cle_rapport:
        st.download_button(
            t("Télécharger le rapport"), data=st.session_state["rapport"][1],
            file_name=f"rapport_portefeuille_{histo.index[-1]:%Y%m%d}.pdf", mime="application/pdf",
            icon=":material/download:", width="stretch", type="primary",
        )
    with st.expander(t("Méthodologie")):
        st.markdown(t(
            "- **TWR** : rendement pondéré par le temps, neutre vis-à-vis des apports.\n"
            "- **TRI** : taux de rendement interne des flux de l'investisseur.\n"
            "- **Volatilité** : écart-type quotidien × √252.\n"
            "- **VaR / CVaR** : méthode historique, horizon 1 jour.\n"
            "- **Markowitz** : optimisation SLSQP, sans vente à découvert.\n\n"
            "Détails dans le fichier README.md du projet."
        ))

# ======================================================================
# EN-TÊTE ET CHIFFRES CLÉS
# ======================================================================
html(ui.entete(
    titre=t("Suivi de portefeuille"),
    surtitre=t("Gestion de portefeuille"),
    sous_titre=t("Du {debut} au {fin}  ·  {n} lignes  ·  Référence : {indice}",
                 debut=date_debut, fin=date_fin, n=resume["nb_lignes"], indice=nom_court),
    source=res["source_cours"],
    date_donnees=date_fin,
))

rendement_investi = resume["gain_total"] / resume["montant_investi"]
html(ui.grille([
    ui.carte(t("Valeur actuelle"), euros(resume["valeur_actuelle"]),
             detail=t("Investi au PRU : {montant}", montant=euros(resume["montant_investi"])),
             aide=t("Quantité × dernier cours, pour chaque ligne détenue")),
    ui.carte(t("Gain total"), euros(resume["gain_total"], signe=True),
             detail=ui.pastille(pct(rendement_investi), tendance(rendement_investi)) + t(" sur le capital investi"),
             aide=t("Plus-values latentes + plus-values réalisées + dividendes")),
    ui.carte(t("Perf. annualisée"), pct(ind["twr_annualise"]),
             detail=ui.pastille(t("TWR total {valeur}", valeur=pct(ind["twr_total"])), tendance(ind["twr_total"])),
             aide=t("Rendement pondéré par le temps (TWR) : mesure la qualité des choix, hors effet des apports")),
    ui.carte(t("Volatilité"), pct(ind["volatilite"], signe=False),
             detail=f"{nom_court} : {pct(av['volatilite_indice'], signe=False)}",
             aide=t("Écart-type des rendements quotidiens × √252")),
    ui.carte("Sharpe", nombre(av["sharpe"]),
             detail=f"{nom_court} : {nombre(av['sharpe_indice'])}",
             aide=t("Ratio de Sharpe : (rendement − taux sans risque) / volatilité")),
    ui.carte("Max drawdown", pct(ind["max_drawdown"]),
             detail=t("Le {date}", date=langues.date(ind["date_creux"])),
             aide=t("Pire baisse depuis un plus haut")),
]))

# ======================================================================
# ONGLETS
# ======================================================================
PIED_DE_PAGE = t("Données de marché : Yahoo Finance · Taux sans risque : BCE · "
                 "Outil pédagogique — ne constitue pas un conseil en investissement.")
cle_calculs = (hash(contenu), code_indice, taux_sans_risque, niveau_var)

# Les deux espaces supplémentaires (étape 10) ont leur propre fichier.
if espace == "Conseil patrimonial":
    vues_conseil.afficher(res, cle_calculs)
    html(ui.pied_de_page(PIED_DE_PAGE))
    st.stop()
if espace == "Gestion d'actifs":
    vues_gestion.afficher(res, cle_calculs, taux_sans_risque)
    html(ui.pied_de_page(PIED_DE_PAGE))
    st.stop()

onglets = st.tabs([t("Vue d'ensemble"), t("Positions"), t("Performance"), t("Risque"), t("Optimisation"),
                   t("Projection"), t("Transactions")])

# ----------------------------------------------------------------------
# 1. Vue d'ensemble
# ----------------------------------------------------------------------
with onglets[0]:
    gauche, droite = st.columns([2, 1], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section(t("Évolution du portefeuille"), t("Valeur de marché et capital investi (apports nets)")))
        graphique(gi.fig_valeur_et_apports(histo))
    with droite, st.container(border=True):
        html(ui.titre_section(t("Répartition"), t("Poids de chaque ligne dans la valeur totale")))
        graphique(gi.fig_repartition(positions))

    # Répartition par classe d'actifs, région et secteur (si le référentiel classe les titres)
    groupes = [(c, t(libelle)) for c, libelle in [("classe", "Par classe d'actifs"), ("region", "Par région"),
                                                  ("secteur", "Par secteur")]
               if c in positions.columns and positions[c].nunique() > 1]
    if groupes:
        for colonne_st, (colonne, libelle) in zip(st.columns(len(groupes), gap="medium"), groupes):
            with colonne_st, st.container(border=True):
                html(ui.titre_section(libelle, t("{n} groupes · poids en % de la valeur",
                                                 n=positions[colonne].nunique())))
                graphique(gi.fig_repartition_groupes(positions, colonne))

    html(ui.grille([
        ui.carte(t("Plus-values latentes"), euros(resume["pv_latentes"], signe=True),
                 detail=ui.pastille(t("non réalisées"), tendance(resume["pv_latentes"]))),
        ui.carte(t("Plus-values réalisées"), euros(resume["pv_realisees"], signe=True),
                 detail=ui.pastille(t("encaissées"), tendance(resume["pv_realisees"]))),
        ui.carte(t("Dividendes et coupons"), euros(resume["dividendes"]), detail=t("Montants bruts perçus")),
        ui.carte(t("Frais de courtage"), euros(resume["frais_totaux"]), detail=t("Depuis l'origine")),
    ]))

# ----------------------------------------------------------------------
# 2. Positions
# ----------------------------------------------------------------------
with onglets[1]:
    with st.container(border=True):
        html(ui.titre_section(t("Positions détenues"), t("Cliquer sur un titre de colonne pour trier")))
        tableau = positions[["nom", "classe", "region", "secteur", "devise", "quantite", "pru", "cours", "valeur",
                             "pv_latente", "pv_latente_pct", "poids_pct", "dividendes"]].reset_index()
        for colonne in ["classe", "region", "secteur"]:          # données traduites à l'affichage
            tableau[colonne] = tableau[colonne].map(td)
        # column_config : nom affiché et format de chaque colonne.
        st.dataframe(
            tableau, hide_index=True, width="stretch",
            column_config={
                "ticker": st.column_config.TextColumn("Ticker", width="small"),
                "nom": st.column_config.TextColumn(t("Titre"), width="medium"),
                "classe": st.column_config.TextColumn(t("Classe")),
                "region": st.column_config.TextColumn(t("Région")),
                "secteur": st.column_config.TextColumn(t("Secteur")),
                "devise": st.column_config.TextColumn(t("Devise"), width="small",
                                                      help=t("Devise de cotation (montants convertis en euros)")),
                "quantite": st.column_config.NumberColumn(t("Quantité"), format="%d"),
                "pru": st.column_config.NumberColumn(t("PRU"), format=langues.eur_colonne("%.2f")),
                "cours": st.column_config.NumberColumn(t("Cours"), format=langues.eur_colonne("%.2f")),
                "valeur": st.column_config.NumberColumn(t("Valeur"), format=langues.eur_colonne("%.0f")),
                "pv_latente": st.column_config.NumberColumn(t("+/- value"), format=langues.eur_colonne("%+.0f")),
                "pv_latente_pct": st.column_config.NumberColumn(t("+/- value %"),
                                                                format=langues.pct_colonne("%+.2f")),
                "poids_pct": st.column_config.ProgressColumn(
                    t("Poids"), format=langues.pct_colonne("%.1f"), min_value=0,
                    max_value=float(tableau["poids_pct"].max())),
                "dividendes": st.column_config.NumberColumn(t("Dividendes"), format=langues.eur_colonne("%.0f")),
            },
        )
    with st.container(border=True):
        html(ui.titre_section(t("Plus-values latentes par ligne"), t("En euros, au dernier cours connu")))
        graphique(gi.fig_plus_values(positions))

# ----------------------------------------------------------------------
# 3. Performance
# ----------------------------------------------------------------------
with onglets[2]:
    ecart = av["twr_portefeuille_meme_periode"] - av["twr_indice"]
    html(ui.grille([
        ui.carte(t("TWR total"), pct(ind["twr_total"]), detail=t("Depuis le {date}", date=date_debut)),
        ui.carte(t("TWR annualisé"), pct(ind["twr_annualise"]), detail=t("Base 365 jours")),
        ui.carte(t("TRI annuel"), pct(ind["tri_annuel"]), detail=t("Rendement de l'argent investi"),
                 aide=t("Taux de rendement interne : dépend du calendrier des apports")),
        ui.carte(t("Écart avec {indice}", indice=nom_court), pct(ecart),
                 detail=ui.pastille(t("surperformance") if ecart >= 0 else t("sous-performance"), tendance(ecart)),
                 aide=t("TWR du portefeuille − TWR de l'indice, sur la même période")),
    ]))

    with st.container(border=True):
        html(ui.titre_section(t("Portefeuille et {indice}", indice=nom_court),
                              t("Base 100 à la première date commune")))
        graphique(gi.fig_comparaison_indice(av, nom_indice))

    gauche, droite = st.columns(2, gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section(t("Rendement par année civile"), t("TWR du portefeuille et de l'indice")))
        graphique(gi.fig_rendements_annuels(ind, av, nom_court))
    with droite, st.container(border=True):
        recup = ind["date_recuperation"]
        html(ui.titre_section(
            "Drawdown",
            t("Du plus haut du {sommet} au plus bas du {creux} · ",
              sommet=langues.date(ind["date_sommet"]), creux=langues.date(ind["date_creux"]))
            + (t("plus haut non retrouvé") if recup is None else t("retrouvé le {date}", date=langues.date(recup))),
        ))
        graphique(gi.fig_drawdown(ind))

    html(ui.grille([
        ui.carte(t("Bêta"), nombre(av["beta"]), detail=t("1 = comme l'indice"),
                 aide=t("Sensibilité du portefeuille aux mouvements de l'indice")),
        ui.carte(t("Alpha de Jensen"), pct(av["alpha"]),
                 detail=ui.pastille(t("annuel"), tendance(av["alpha"])),
                 aide=t("Performance non expliquée par l'exposition au marché (MEDAF)")),
        ui.carte(t("Corrélation"), nombre(av["correlation_indice"]), detail=t("Avec {indice}", indice=nom_court)),
        ui.carte("Tracking error", pct(av["tracking_error"], signe=False), detail=t("Annualisée"),
                 aide=t("Volatilité de l'écart de rendement avec l'indice")),
        ui.carte(t("Ratio d'information"), nombre(av["ratio_information"]), detail=t("Écart / tracking error")),
    ]))

# ----------------------------------------------------------------------
# 4. Risque
# ----------------------------------------------------------------------
with onglets[3]:
    niveau = pct(niveau_var, signe=False, decimales=0)
    html(ui.grille([
        ui.carte(t("Ratio de Sharpe"), nombre(av["sharpe"]), detail=f"{nom_court} : {nombre(av['sharpe_indice'])}",
                 aide=t("(Rendement − taux sans risque) / volatilité")),
        ui.carte(t("Ratio de Sortino"), nombre(av["sortino"]), detail=t("Ne pénalise que les baisses")),
        ui.carte(t("VaR {niveau} · 1 jour", niveau=niveau), euros(av["var_euros"]),
                 detail=ui.pastille(pct(-av["var_historique"]), "negative") + t(" méthode historique"),
                 aide=t("Dans {niveau} des jours, la perte ne dépasse pas ce montant", niveau=niveau)),
        ui.carte("CVaR · Expected Shortfall", euros(av["cvar_euros"]),
                 detail=ui.pastille(pct(-av["cvar"]), "negative") + t(" au-delà de la VaR"),
                 aide=t("Perte moyenne les jours où la VaR est dépassée")),
    ]))

    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section(t("Distribution des rendements quotidiens"),
                              t("VaR paramétrique (loi normale) : {valeur}",
                                valeur=pct(av["var_parametrique"], signe=False))))
        graphique(gi.fig_distribution_rendements(ind, av, niveau_var))
        html(ui.note(t("Si la VaR historique dépasse la VaR paramétrique, les pertes extrêmes sont plus "
                       "fréquentes que ne le prévoit la loi normale (« queues épaisses »).")))
    with droite, st.container(border=True):
        html(ui.titre_section(t("Corrélations"), t("Rendements quotidiens des titres détenus")))
        graphique(gi.fig_correlations(res["correlations"]))

# ----------------------------------------------------------------------
# 5. Optimisation de Markowitz
# ----------------------------------------------------------------------
with onglets[4]:
    n_titres = len(positions)
    # Seuls les poids maximaux qui permettent d'investir 100 % sont proposés.
    choix_possibles = [p for p in [0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 1.0] if p * n_titres >= 1]
    defaut = config.POIDS_MAX if config.POIDS_MAX in choix_possibles else choix_possibles[-1]

    reglage, _ = st.columns([1, 2])
    poids_max = reglage.select_slider(
        t("Poids maximal par titre"), options=choix_possibles, value=defaut,
        format_func=lambda v: t("sans limite") if v == 1.0 else pct(v, signe=False, decimales=0),
        help=t("Sans limite, l'optimiseur concentre souvent tout sur 2 ou 3 titres."),
    )
    try:
        with st.spinner(t("Optimisation en cours...")):
            opti = optimiser(contenu, code_indice, taux_sans_risque, niveau_var, poids_max)
    except Exception as erreur:
        st.error(t("Optimisation impossible : {erreur}", erreur=erreur))
        st.stop()

    cartes = []
    for cle, nom in [("actuel", "Mon portefeuille"), ("variance_min", "Variance minimale"),
                     ("sharpe_max", "Sharpe maximal")]:
        p = opti[cle]
        cartes.append(ui.carte(
            t(nom), f"Sharpe {nombre(p['sharpe'])}",
            detail=t("Rendement {r} · Volatilité {v}", r=pct(p["rendement"]), v=pct(p["volatilite"], signe=False)),
        ))
    html(ui.grille(cartes))

    with st.container(border=True):
        html(ui.titre_section(t("Frontière efficiente"),
                              t("Chaque point bleu est un portefeuille tiré au hasard : aucun ne dépasse la frontière")))
        graphique(gi.fig_frontiere(opti))

    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section(t("Répartitions comparées"), t("Poids actuels et poids optimaux")))
        graphique(gi.fig_poids(opti))
    with droite, st.container(border=True):
        html(ui.titre_section(t("Ajustements vers le Sharpe maximal"), t("À valeur totale inchangée, hors frais")))
        ajustements = opti["poids"][["nom", "actuel", "sharpe_max", "ecart_euros_sharpe_max"]]
        ajustements = ajustements.assign(actuel=ajustements["actuel"] * 100,
                                         sharpe_max=ajustements["sharpe_max"] * 100)
        st.dataframe(
            ajustements.sort_values("ecart_euros_sharpe_max"), hide_index=True, width="stretch",
            column_config={
                "nom": st.column_config.TextColumn(t("Titre")),
                "actuel": st.column_config.NumberColumn(t("Actuel"), format=langues.pct_colonne("%.1f")),
                "sharpe_max": st.column_config.NumberColumn(t("Optimal"), format=langues.pct_colonne("%.1f")),
                "ecart_euros_sharpe_max": st.column_config.NumberColumn(
                    t("Acheter / vendre"), format=langues.eur_colonne("%+.0f")),
            },
        )
        html(ui.note(t("Exercice académique, pas un conseil en investissement. Les rendements espérés "
                       "sont estimés sur le passé : l'optimiseur surexploite les titres qui ont le mieux "
                       "marché, sans garantie pour l'avenir."), attention=True))

# ----------------------------------------------------------------------
# 6. Projection (Monte-Carlo)
# ----------------------------------------------------------------------
with onglets[5]:
    rendements = ind["rendements"]
    mu_hist, sigma_hist = parametres_historiques(rendements)

    with st.container(border=True):
        html(ui.titre_section(t("Hypothèses de la simulation"),
                              t("Valeurs historiques du portefeuille : rendement {r}, volatilité {v}",
                                r=pct(mu_hist), v=pct(sigma_hist, signe=False))))
        a, b, c = st.columns(3)
        annees = a.slider(t("Horizon (années)"), 1, 30, config.HORIZON_PROJECTION)
        versement = b.number_input(t("Versement mensuel (€)"), min_value=0, max_value=1_000_000,
                                   value=int(config.VERSEMENT_MENSUEL), step=100)
        objectif = c.number_input(t("Objectif (€, facultatif)"), min_value=0, max_value=100_000_000,
                                  value=0, step=5000, help=t("0 = pas d'objectif"))
        a, b, c = st.columns(3)
        methode = a.radio(t("Méthode"), ["normale", "historique"], horizontal=True,
                          format_func=lambda m: t("Loi normale") if m == "normale" else t("Historique (bootstrap)"),
                          help=t("Historique : tire au hasard de vrais jours de bourse du portefeuille, "
                                 "ce qui conserve les krachs réels."))
        mu = b.slider(t("Rendement annuel supposé (%)"), -5.0, 20.0,
                      float(min(max(round(mu_hist * 200) / 2, -5.0), 20.0)), 0.5,
                      help=t("Par défaut : rendement historique. Le réduire donne une projection plus prudente.")) / 100
        sigma = c.slider(t("Volatilité annuelle (%)"), 1.0, 50.0,
                         float(min(max(round(sigma_hist * 200) / 2, 1.0), 50.0)), 0.5,
                         disabled=(methode == "historique"),
                         help=t("Avec la méthode historique, la volatilité réelle est utilisée.")) / 100

    with st.spinner(t("Simulation de Monte-Carlo...")):
        sim = projeter(resume["valeur_actuelle"], mu, sigma, annees, float(versement), methode,
                       float(objectif), rendements, histo.index[-1])

    cartes = [
        ui.carte(t("Scénario défavorable"), euros(sim["p5"]), detail=t("1 chance sur 20 de faire pire")),
        ui.carte(t("Scénario médian"), euros(sim["mediane"]), detail=t("1 chance sur 2 de faire mieux")),
        ui.carte(t("Scénario favorable"), euros(sim["p95"]), detail=t("1 chance sur 20 de faire mieux")),
        ui.carte(t("Probabilité de perte"), pct(sim["proba_perte"], signe=False, decimales=1),
                 detail=t("Sous {montant} investis", montant=euros(sim["total_apporte"])),
                 aide=t("Part des scénarios qui finissent sous la valeur de départ + versements")),
    ]
    if sim["proba_objectif"] is not None:
        cartes.append(ui.carte(t("Objectif atteint"), pct(sim["proba_objectif"], signe=False, decimales=1),
                               detail=t("Objectif : {montant}", montant=euros(sim["objectif"]))))
    html(ui.grille(cartes))

    affichage = st.segmented_control(
        t("Affichage"), ["Éventail", "Nuage de points", "Les deux"], default="Éventail", format_func=t,
        help=t("Nuage de points : chaque point est un scénario, coloré selon sa tranche de probabilité."),
    ) or "Éventail"
    if affichage in ("Éventail", "Les deux"):
        with st.container(border=True):
            html(ui.titre_section(t("Projection sur {n} ans", n=annees),
                                  t("{n} scénarios simulés · zones : 50 % et 90 % des scénarios",
                                    n=config.NB_SIMULATIONS)))
            graphique(gi.fig_projection(sim))
    if affichage in ("Nuage de points", "Les deux"):
        with st.container(border=True):
            html(ui.titre_section(
                t("Scénarios par tranche de probabilité"),
                t("{n} scénarios affichés · rouge = défavorable, gris = central, bleu = favorable · "
                  "survoler un point pour le détail", n=len(sim["echantillon"].columns))))
            graphique(gi.fig_projection_nuage(sim))

    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section(t("Distribution de la valeur finale")))
        graphique(gi.fig_distribution_finale(sim))
    with droite, st.container(border=True):
        html(ui.titre_section(t("Comment lire cette projection ?")))
        st.markdown(t(
            "- Chaque scénario est un **futur possible**, tiré au hasard mais cohérent avec le "
            "rendement et le risque choisis.\n"
            "- La **médiane** n'est pas une prévision : c'est le milieu des possibles.\n"
            "- L'écart entre scénarios défavorable et favorable **grandit avec l'horizon** : "
            "c'est l'incertitude qui s'accumule.\n"
            "- La méthode **historique** conserve les vrais krachs du portefeuille ; la **loi "
            "normale** les sous-estime."
        ))
        html(ui.note(t("Une projection n'est pas une prévision : elle suppose que les hypothèses "
                       "se vérifient, ce qui n'est jamais garanti."), attention=True))

# ----------------------------------------------------------------------
# 7. Transactions
# ----------------------------------------------------------------------
with onglets[6]:
    transactions = res["transactions"]
    with st.container(border=True):
        html(ui.titre_section(t("Historique des opérations")))
        gauche, droite = st.columns(2)
        choix_types = gauche.multiselect(t("Type"), ["ACHAT", "VENTE", "DIVIDENDE"],
                                         default=["ACHAT", "VENTE", "DIVIDENDE"], format_func=td)
        choix_titres = droite.multiselect(t("Titres"), sorted(transactions["nom"].unique()),
                                          placeholder=t("Tous les titres"))

        filtre = transactions["type"].isin(choix_types)
        if choix_titres:
            filtre &= transactions["nom"].isin(choix_titres)
        selection = transactions[filtre].sort_values("date", ascending=False)

        st.caption(t("{n} opération(s) affichée(s) sur {total}", n=len(selection), total=len(transactions)))
        st.dataframe(
            selection.assign(type=selection["type"].map(td)), hide_index=True, width="stretch",
            column_config={
                "date": st.column_config.DateColumn("Date", format="DD MMM YYYY" if langues.anglais()
                                                    else "DD/MM/YYYY"),
                "type": st.column_config.TextColumn(t("Type")),
                "ticker": st.column_config.TextColumn("Ticker"),
                "nom": st.column_config.TextColumn(t("Titre")),
                "quantite": st.column_config.NumberColumn(t("Quantité"), format="%d"),
                "prix": st.column_config.NumberColumn(t("Prix / montant (€)"), format=langues.eur_colonne("%.2f")),
                "frais": st.column_config.NumberColumn(t("Frais"), format=langues.eur_colonne("%.2f")),
                "devise": st.column_config.TextColumn(t("Devise")),
                "prix_devise": st.column_config.NumberColumn(t("Prix en devise"), format="%.2f",
                                                             help=t("Prix saisi, avant conversion en euros")),
            },
        )
        # Le fichier téléchargé garde le format d'origine (types ACHAT / VENTE / DIVIDENDE)
        st.download_button(
            t("Télécharger la sélection (CSV)"), icon=":material/download:",
            data=selection.to_csv(index=False).encode("utf-8"),
            file_name="transactions_selection.csv", mime="text/csv",
        )

# ======================================================================
# PIED DE PAGE
# ======================================================================
html(ui.pied_de_page(PIED_DE_PAGE))
