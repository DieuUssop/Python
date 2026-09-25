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
    - ce fichier se contente d'ASSEMBLER la page.

Comment fonctionne Streamlit ?
    Le fichier est exécuté de haut en bas à chaque interaction (clic,
    changement de réglage...). Chaque st.quelquechose() ajoute un élément
    à la page.
"""

import io
from pathlib import Path

import streamlit as st

from src import config
from src import graphiques_interactifs as gi
from src import interface as ui
from src import vues_conseil, vues_gestion
from src.analyse import analyse_complete
from src.interface import euros, nombre, pct, tendance
from src.optimisation import optimiser_portefeuille
from src.simulation import parametres_historiques, simuler

FICHIER_PAR_DEFAUT = Path("data/transactions.csv")
# Tous les fichiers de transactions disponibles (ex. transactions_mondial.csv)
FICHIERS_DISPONIBLES = sorted(Path("data").glob("transactions*.csv"),
                              key=lambda f: (f != FICHIER_PAR_DEFAUT, f.name))
FICHIERS_DISPONIBLES = [f for f in FICHIERS_DISPONIBLES if "sauvegarde" not in f.name]
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
# Configuration de la page (doit être la première commande Streamlit)
# ----------------------------------------------------------------------
st.set_page_config(page_title="Suivi de portefeuille · Master G2C", page_icon="📈", layout="wide")

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
@st.cache_data(ttl=3600, show_spinner="Récupération des cours et calcul des indicateurs...")
def charger(contenu_csv, indice, taux_sans_risque, niveau_var):
    return analyse_complete(io.BytesIO(contenu_csv), indice, taux_sans_risque, niveau_var)


@st.cache_data(show_spinner="Optimisation en cours...")
def optimiser(contenu_csv, indice, taux_sans_risque, niveau_var, poids_max):
    res = charger(contenu_csv, indice, taux_sans_risque, niveau_var)
    return optimiser_portefeuille(res["prix_hist"], res["positions"], taux_sans_risque, poids_max)


@st.cache_data(show_spinner="Simulation de Monte-Carlo...")
def projeter(valeur, mu, sigma, annees, versement, methode, objectif, rendements, date_depart):
    return simuler(valeur, mu, sigma, annees=annees, versement_mensuel=versement,
                   nb_simulations=config.NB_SIMULATIONS, methode=methode,
                   rendements_historiques=rendements, objectif=objectif or None,
                   date_depart=date_depart)


@st.cache_data(show_spinner=False)
def produire_rapport(contenu_csv, indice, taux_sans_risque, niveau_var, nom_indice):
    """Construit le rapport PDF en mémoire et renvoie son contenu (octets)."""
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
    html(ui.marque("Portfolio Tracker", "Master G2C · Outil de suivi de portefeuille"))

    html(ui.bloc_titre("Espace de travail"))
    espace = st.radio(
        "Espace de travail", ["Analyse du portefeuille", "Conseil patrimonial", "Gestion d'actifs"],
        label_visibility="collapsed",
        captions=["Performance, risque, optimisation, projection",
                  "Profil client, fiscalité, stress tests",
                  "Attribution, budget de risque, backtest"],
    )

    html(ui.bloc_titre("Données"))
    fichier_choisi = None
    if FICHIERS_DISPONIBLES:
        fichier_choisi = st.selectbox(
            "Portefeuille", FICHIERS_DISPONIBLES,
            format_func=lambda f: {"transactions.csv": "Mon portefeuille",
                                   "transactions_mondial.csv": "Portefeuille actions monde"}.get(f.name, f.name),
            help="Fichiers data/transactions*.csv du projet",
        )
    fichier_envoye = st.file_uploader(
        "Ou envoyer un autre fichier (CSV)", type=["csv"],
        help="Prioritaire sur le portefeuille choisi ci-dessus",
    )

    html(ui.bloc_titre("Paramètres d'analyse"))
    code_indice = st.selectbox(
        "Indice de référence", options=list(INDICES),
        index=list(INDICES).index(config.INDICE_REFERENCE) if config.INDICE_REFERENCE in INDICES else 0,
        format_func=lambda code: INDICES[code],
    )
    taux_sans_risque = st.number_input(
        "Taux sans risque (% par an)", min_value=0.0, max_value=10.0,
        value=config.TAUX_SANS_RISQUE * 100, step=0.25, format="%.2f",
        help="Taux de la facilité de dépôt de la BCE : 2,50 % depuis le 16/09/2026",
    ) / 100
    niveau_var = st.select_slider(
        "Niveau de confiance de la VaR", options=[0.90, 0.95, 0.99],
        value=config.NIVEAU_CONFIANCE_VAR, format_func=lambda v: f"{v:.0%}",
    )

    st.write("")
    if st.button("Actualiser les cours", icon=":material/refresh:", width="stretch"):
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
    st.error("Aucun fichier de transactions : envoyez un fichier CSV depuis la barre latérale.")
    st.stop()

try:
    res = charger(contenu, code_indice, taux_sans_risque, niveau_var)
except Exception as erreur:  # message clair plutôt qu'un plantage
    st.error(f"Impossible d'analyser le portefeuille : {erreur}")
    st.stop()

resume = res["resume"]
positions = res["positions"]
histo = res["historique"]
ind = res["indicateurs"]
av = res["avances"]
nom_indice = INDICES[code_indice]
nom_court = NOMS_COURTS[code_indice]
date_debut, date_fin = f"{histo.index[0]:%d/%m/%Y}", f"{histo.index[-1]:%d/%m/%Y}"

with st.sidebar:
    html(ui.bloc_titre("Informations"))
    html(ui.infos([
        ("Fichier", nom_fichier),
        ("Opérations", str(len(res["transactions"]))),
        ("Période", f"{date_debut} → {date_fin}"),
        ("Cours", res["source_cours"]),
    ] + [(f"1 € en {devise}", nombre(taux, 4)) for devise, taux in res["taux_actuels"].items()]))

    html(ui.bloc_titre("Rapport"))
    cle_rapport = (hash(contenu), code_indice, taux_sans_risque, niveau_var)
    if st.button("Préparer le rapport PDF", icon=":material/picture_as_pdf:", width="stretch"):
        try:
            with st.spinner("Génération du rapport..."):
                st.session_state["rapport"] = (cle_rapport, produire_rapport(
                    contenu, code_indice, taux_sans_risque, niveau_var, nom_indice))
        except ImportError:
            st.error("Installer reportlab : python -m pip install reportlab")
    # On ne propose le téléchargement que si le rapport correspond aux réglages actuels.
    if st.session_state.get("rapport", (None,))[0] == cle_rapport:
        st.download_button(
            "Télécharger le rapport", data=st.session_state["rapport"][1],
            file_name=f"rapport_portefeuille_{histo.index[-1]:%Y%m%d}.pdf", mime="application/pdf",
            icon=":material/download:", width="stretch", type="primary",
        )
    with st.expander("Méthodologie"):
        st.markdown(
            "- **TWR** : rendement pondéré par le temps, neutre vis-à-vis des apports.\n"
            "- **TRI** : taux de rendement interne des flux de l'investisseur.\n"
            "- **Volatilité** : écart-type quotidien × √252.\n"
            "- **VaR / CVaR** : méthode historique, horizon 1 jour.\n"
            "- **Markowitz** : optimisation SLSQP, sans vente à découvert.\n\n"
            "Détails dans le fichier README.md du projet."
        )

# ======================================================================
# EN-TÊTE ET CHIFFRES CLÉS
# ======================================================================
html(ui.entete(
    titre="Suivi de portefeuille",
    surtitre="Master G2C · Gestion de portefeuille",
    sous_titre=f"Du {date_debut} au {date_fin}  ·  {resume['nb_lignes']} lignes  ·  Référence : {nom_court}",
    source=res["source_cours"],
    date_donnees=date_fin,
))

rendement_investi = resume["gain_total"] / resume["montant_investi"]
html(ui.grille([
    ui.carte("Valeur actuelle", euros(resume["valeur_actuelle"]),
             detail=f"Investi au PRU : {euros(resume['montant_investi'])}",
             aide="Quantité × dernier cours, pour chaque ligne détenue"),
    ui.carte("Gain total", euros(resume["gain_total"], signe=True),
             detail=ui.pastille(pct(rendement_investi), tendance(rendement_investi)) + " sur le capital investi",
             aide="Plus-values latentes + plus-values réalisées + dividendes"),
    ui.carte("Perf. annualisée", pct(ind["twr_annualise"]),
             detail=ui.pastille(f"TWR total {pct(ind['twr_total'])}", tendance(ind["twr_total"])),
             aide="Rendement pondéré par le temps (TWR) : mesure la qualité des choix, hors effet des apports"),
    ui.carte("Volatilité", pct(ind["volatilite"], signe=False),
             detail=f"{nom_court} : {pct(av['volatilite_indice'], signe=False)}",
             aide="Écart-type des rendements quotidiens × √252"),
    ui.carte("Sharpe", nombre(av["sharpe"]),
             detail=f"{nom_court} : {nombre(av['sharpe_indice'])}",
             aide="Ratio de Sharpe : (rendement − taux sans risque) / volatilité"),
    ui.carte("Max drawdown", pct(ind["max_drawdown"]),
             detail=f"Le {ind['date_creux']:%d/%m/%Y}",
             aide="Pire baisse depuis un plus haut"),
]))

# ======================================================================
# ONGLETS
# ======================================================================
PIED_DE_PAGE = ("Données de marché : Yahoo Finance · Taux sans risque : BCE · "
                "Outil pédagogique réalisé dans le cadre du Master G2C — ne constitue pas un conseil en investissement.")
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

onglets = st.tabs(["Vue d'ensemble", "Positions", "Performance", "Risque", "Optimisation",
                   "Projection", "Transactions"])

# ----------------------------------------------------------------------
# 1. Vue d'ensemble
# ----------------------------------------------------------------------
with onglets[0]:
    gauche, droite = st.columns([2, 1], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section("Évolution du portefeuille", "Valeur de marché et capital investi (apports nets)"))
        graphique(gi.fig_valeur_et_apports(histo))
    with droite, st.container(border=True):
        html(ui.titre_section("Répartition", "Poids de chaque ligne dans la valeur totale"))
        graphique(gi.fig_repartition(positions))

    # Répartition par région et par secteur (si le référentiel classe les titres)
    groupes = [(c, t) for c, t in [("region", "Par région"), ("secteur", "Par secteur")]
               if positions[c].nunique() > 1]
    if groupes:
        for colonne_st, (colonne, libelle) in zip(st.columns(len(groupes), gap="medium"), groupes):
            with colonne_st, st.container(border=True):
                html(ui.titre_section(libelle, f"{positions[colonne].nunique()} groupes · poids en % de la valeur"))
                graphique(gi.fig_repartition_groupes(positions, colonne))

    html(ui.grille([
        ui.carte("Plus-values latentes", euros(resume["pv_latentes"], signe=True),
                 detail=ui.pastille("non réalisées", tendance(resume["pv_latentes"]))),
        ui.carte("Plus-values réalisées", euros(resume["pv_realisees"], signe=True),
                 detail=ui.pastille("encaissées", tendance(resume["pv_realisees"]))),
        ui.carte("Dividendes perçus", euros(resume["dividendes"]), detail="Montants bruts"),
        ui.carte("Frais de courtage", euros(resume["frais_totaux"]), detail="Depuis l'origine"),
    ]))

# ----------------------------------------------------------------------
# 2. Positions
# ----------------------------------------------------------------------
with onglets[1]:
    with st.container(border=True):
        html(ui.titre_section("Positions détenues", "Cliquer sur un titre de colonne pour trier"))
        tableau = positions[["nom", "region", "secteur", "devise", "quantite", "pru", "cours", "valeur",
                             "pv_latente", "pv_latente_pct", "poids_pct", "dividendes"]].reset_index()
        # column_config : nom affiché et format de chaque colonne.
        st.dataframe(
            tableau, hide_index=True, width="stretch",
            column_config={
                "ticker": st.column_config.TextColumn("Ticker", width="small"),
                "nom": st.column_config.TextColumn("Titre", width="medium"),
                "region": st.column_config.TextColumn("Région"),
                "secteur": st.column_config.TextColumn("Secteur"),
                "devise": st.column_config.TextColumn("Devise", width="small",
                                                      help="Devise de cotation (montants convertis en euros)"),
                "quantite": st.column_config.NumberColumn("Quantité", format="%d"),
                "pru": st.column_config.NumberColumn("PRU", format="%.2f €"),
                "cours": st.column_config.NumberColumn("Cours", format="%.2f €"),
                "valeur": st.column_config.NumberColumn("Valeur", format="%.0f €"),
                "pv_latente": st.column_config.NumberColumn("+/- value", format="%+.0f €"),
                "pv_latente_pct": st.column_config.NumberColumn("+/- value %", format="%+.2f %%"),
                "poids_pct": st.column_config.ProgressColumn(
                    "Poids", format="%.1f %%", min_value=0, max_value=float(tableau["poids_pct"].max())),
                "dividendes": st.column_config.NumberColumn("Dividendes", format="%.0f €"),
            },
        )
    with st.container(border=True):
        html(ui.titre_section("Plus-values latentes par ligne", "En euros, au dernier cours connu"))
        graphique(gi.fig_plus_values(positions))

# ----------------------------------------------------------------------
# 3. Performance
# ----------------------------------------------------------------------
with onglets[2]:
    ecart = av["twr_portefeuille_meme_periode"] - av["twr_indice"]
    html(ui.grille([
        ui.carte("TWR total", pct(ind["twr_total"]), detail=f"Depuis le {date_debut}"),
        ui.carte("TWR annualisé", pct(ind["twr_annualise"]), detail="Base 365 jours"),
        ui.carte("TRI annuel", pct(ind["tri_annuel"]), detail="Rendement de l'argent investi",
                 aide="Taux de rendement interne : dépend du calendrier des apports"),
        ui.carte(f"Écart avec {nom_court}", pct(ecart),
                 detail=ui.pastille("surperformance" if ecart >= 0 else "sous-performance", tendance(ecart)),
                 aide="TWR du portefeuille − TWR de l'indice, sur la même période"),
    ]))

    with st.container(border=True):
        html(ui.titre_section(f"Portefeuille et {nom_court}", "Base 100 à la première date commune"))
        graphique(gi.fig_comparaison_indice(av, nom_indice))

    gauche, droite = st.columns(2, gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section("Rendement par année civile", "TWR du portefeuille et de l'indice"))
        graphique(gi.fig_rendements_annuels(ind, av, nom_court))
    with droite, st.container(border=True):
        recup = ind["date_recuperation"]
        html(ui.titre_section(
            "Drawdown",
            f"Du plus haut du {ind['date_sommet']:%d/%m/%Y} au plus bas du {ind['date_creux']:%d/%m/%Y} · "
            + ("plus haut non retrouvé" if recup is None else f"retrouvé le {recup:%d/%m/%Y}"),
        ))
        graphique(gi.fig_drawdown(ind))

    html(ui.grille([
        ui.carte("Bêta", nombre(av["beta"]), detail="1 = comme l'indice",
                 aide="Sensibilité du portefeuille aux mouvements de l'indice"),
        ui.carte("Alpha de Jensen", pct(av["alpha"]),
                 detail=ui.pastille("annuel", tendance(av["alpha"])),
                 aide="Performance non expliquée par l'exposition au marché (MEDAF)"),
        ui.carte("Corrélation", nombre(av["correlation_indice"]), detail=f"Avec {nom_court}"),
        ui.carte("Tracking error", pct(av["tracking_error"], signe=False), detail="Annualisée",
                 aide="Volatilité de l'écart de rendement avec l'indice"),
        ui.carte("Ratio d'information", nombre(av["ratio_information"]), detail="Écart / tracking error"),
    ]))

# ----------------------------------------------------------------------
# 4. Risque
# ----------------------------------------------------------------------
with onglets[3]:
    niveau = f"{niveau_var:.0%}"
    html(ui.grille([
        ui.carte("Ratio de Sharpe", nombre(av["sharpe"]), detail=f"{nom_court} : {nombre(av['sharpe_indice'])}",
                 aide="(Rendement − taux sans risque) / volatilité"),
        ui.carte("Ratio de Sortino", nombre(av["sortino"]), detail="Ne pénalise que les baisses"),
        ui.carte(f"VaR {niveau} · 1 jour", euros(av["var_euros"]),
                 detail=ui.pastille(pct(-av["var_historique"]), "negative") + " méthode historique",
                 aide=f"Dans {niveau} des jours, la perte ne dépasse pas ce montant"),
        ui.carte("CVaR · Expected Shortfall", euros(av["cvar_euros"]),
                 detail=ui.pastille(pct(-av["cvar"]), "negative") + " au-delà de la VaR",
                 aide="Perte moyenne les jours où la VaR est dépassée"),
    ]))

    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section("Distribution des rendements quotidiens",
                              f"VaR paramétrique (loi normale) : {pct(av['var_parametrique'], signe=False)}"))
        graphique(gi.fig_distribution_rendements(ind, av, niveau_var))
        html(ui.note("Si la VaR historique dépasse la VaR paramétrique, les pertes extrêmes sont plus "
                     "fréquentes que ne le prévoit la loi normale (« queues épaisses »)."))
    with droite, st.container(border=True):
        html(ui.titre_section("Corrélations", "Rendements quotidiens des titres détenus"))
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
        "Poids maximal par titre", options=choix_possibles, value=defaut,
        format_func=lambda v: "sans limite" if v == 1.0 else f"{v:.0%}",
        help="Sans limite, l'optimiseur concentre souvent tout sur 2 ou 3 titres.",
    )
    try:
        opti = optimiser(contenu, code_indice, taux_sans_risque, niveau_var, poids_max)
    except Exception as erreur:
        st.error(f"Optimisation impossible : {erreur}")
        st.stop()

    cartes = []
    for cle, nom in [("actuel", "Mon portefeuille"), ("variance_min", "Variance minimale"),
                     ("sharpe_max", "Sharpe maximal")]:
        p = opti[cle]
        cartes.append(ui.carte(
            nom, f"Sharpe {nombre(p['sharpe'])}",
            detail=f"Rendement {pct(p['rendement'])} · Volatilité {pct(p['volatilite'], signe=False)}",
        ))
    html(ui.grille(cartes))

    with st.container(border=True):
        html(ui.titre_section("Frontière efficiente",
                              "Chaque point bleu est un portefeuille tiré au hasard : aucun ne dépasse la frontière"))
        graphique(gi.fig_frontiere(opti))

    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section("Répartitions comparées", "Poids actuels et poids optimaux"))
        graphique(gi.fig_poids(opti))
    with droite, st.container(border=True):
        html(ui.titre_section("Ajustements vers le Sharpe maximal", "À valeur totale inchangée, hors frais"))
        ajustements = opti["poids"][["nom", "actuel", "sharpe_max", "ecart_euros_sharpe_max"]]
        ajustements = ajustements.assign(actuel=ajustements["actuel"] * 100,
                                         sharpe_max=ajustements["sharpe_max"] * 100)
        st.dataframe(
            ajustements.sort_values("ecart_euros_sharpe_max"), hide_index=True, width="stretch",
            column_config={
                "nom": st.column_config.TextColumn("Titre"),
                "actuel": st.column_config.NumberColumn("Actuel", format="%.1f %%"),
                "sharpe_max": st.column_config.NumberColumn("Optimal", format="%.1f %%"),
                "ecart_euros_sharpe_max": st.column_config.NumberColumn(
                    "Acheter / vendre", format="%+.0f €"),
            },
        )
        html(ui.note("Exercice académique, pas un conseil en investissement. Les rendements espérés "
                     "sont estimés sur le passé : l'optimiseur surexploite les titres qui ont le mieux "
                     "marché, sans garantie pour l'avenir.", attention=True))

# ----------------------------------------------------------------------
# 6. Projection (Monte-Carlo)
# ----------------------------------------------------------------------
with onglets[5]:
    rendements = ind["rendements"]
    mu_hist, sigma_hist = parametres_historiques(rendements)

    with st.container(border=True):
        html(ui.titre_section("Hypothèses de la simulation",
                              f"Valeurs historiques du portefeuille : rendement {pct(mu_hist)}, "
                              f"volatilité {pct(sigma_hist, signe=False)}"))
        a, b, c = st.columns(3)
        annees = a.slider("Horizon (années)", 1, 30, config.HORIZON_PROJECTION)
        versement = b.number_input("Versement mensuel (€)", min_value=0, max_value=1_000_000,
                                   value=int(config.VERSEMENT_MENSUEL), step=100)
        objectif = c.number_input("Objectif (€, facultatif)", min_value=0, max_value=100_000_000,
                                  value=0, step=5000, help="0 = pas d'objectif")
        a, b, c = st.columns(3)
        methode = a.radio("Méthode", ["normale", "historique"], horizontal=True,
                          format_func=lambda m: "Loi normale" if m == "normale" else "Historique (bootstrap)",
                          help="Historique : tire au hasard de vrais jours de bourse du portefeuille, "
                               "ce qui conserve les krachs réels.")
        mu = b.slider("Rendement annuel supposé (%)", -5.0, 20.0,
                      float(min(max(round(mu_hist * 200) / 2, -5.0), 20.0)), 0.5,
                      help="Par défaut : rendement historique. Le réduire donne une projection plus prudente.") / 100
        sigma = c.slider("Volatilité annuelle (%)", 1.0, 50.0,
                         float(min(max(round(sigma_hist * 200) / 2, 1.0), 50.0)), 0.5,
                         disabled=(methode == "historique"),
                         help="Avec la méthode historique, la volatilité réelle est utilisée.") / 100

    sim = projeter(resume["valeur_actuelle"], mu, sigma, annees, float(versement), methode,
                   float(objectif), rendements, histo.index[-1])

    cartes = [
        ui.carte("Scénario défavorable", euros(sim["p5"]), detail="1 chance sur 20 de faire pire"),
        ui.carte("Scénario médian", euros(sim["mediane"]), detail="1 chance sur 2 de faire mieux"),
        ui.carte("Scénario favorable", euros(sim["p95"]), detail="1 chance sur 20 de faire mieux"),
        ui.carte("Probabilité de perte", pct(sim["proba_perte"], signe=False, decimales=1),
                 detail=f"Sous {euros(sim['total_apporte'])} investis",
                 aide="Part des scénarios qui finissent sous la valeur de départ + versements"),
    ]
    if sim["proba_objectif"] is not None:
        cartes.append(ui.carte("Objectif atteint", pct(sim["proba_objectif"], signe=False, decimales=1),
                               detail=f"Objectif : {euros(sim['objectif'])}"))
    html(ui.grille(cartes))

    affichage = st.segmented_control(
        "Affichage", ["Éventail", "Nuage de points", "Les deux"], default="Éventail",
        help="Nuage de points : chaque point est un scénario, coloré selon sa tranche de probabilité.",
    ) or "Éventail"
    if affichage in ("Éventail", "Les deux"):
        with st.container(border=True):
            html(ui.titre_section(f"Projection sur {annees} ans",
                                  f"{config.NB_SIMULATIONS} scénarios simulés · zones : 50 % et 90 % des scénarios"))
            graphique(gi.fig_projection(sim))
    if affichage in ("Nuage de points", "Les deux"):
        with st.container(border=True):
            html(ui.titre_section(
                "Scénarios par tranche de probabilité",
                f"{len(sim['echantillon'].columns)} scénarios affichés · rouge = défavorable, "
                "gris = central, bleu = favorable · survoler un point pour le détail"))
            graphique(gi.fig_projection_nuage(sim))

    gauche, droite = st.columns([3, 2], gap="medium")
    with gauche, st.container(border=True):
        html(ui.titre_section("Distribution de la valeur finale"))
        graphique(gi.fig_distribution_finale(sim))
    with droite, st.container(border=True):
        html(ui.titre_section("Comment lire cette projection ?"))
        st.markdown(
            "- Chaque scénario est un **futur possible**, tiré au hasard mais cohérent avec le "
            "rendement et le risque choisis.\n"
            "- La **médiane** n'est pas une prévision : c'est le milieu des possibles.\n"
            "- L'écart entre scénarios défavorable et favorable **grandit avec l'horizon** : "
            "c'est l'incertitude qui s'accumule.\n"
            "- La méthode **historique** conserve les vrais krachs du portefeuille ; la **loi "
            "normale** les sous-estime."
        )
        html(ui.note("Une projection n'est pas une prévision : elle suppose que les hypothèses "
                     "se vérifient, ce qui n'est jamais garanti.", attention=True))

# ----------------------------------------------------------------------
# 7. Transactions
# ----------------------------------------------------------------------
with onglets[6]:
    transactions = res["transactions"]
    with st.container(border=True):
        html(ui.titre_section("Historique des opérations"))
        gauche, droite = st.columns(2)
        choix_types = gauche.multiselect("Type", ["ACHAT", "VENTE", "DIVIDENDE"],
                                         default=["ACHAT", "VENTE", "DIVIDENDE"])
        choix_titres = droite.multiselect("Titres", sorted(transactions["nom"].unique()),
                                          placeholder="Tous les titres")

        filtre = transactions["type"].isin(choix_types)
        if choix_titres:
            filtre &= transactions["nom"].isin(choix_titres)
        selection = transactions[filtre].sort_values("date", ascending=False)

        st.caption(f"{len(selection)} opération(s) affichée(s) sur {len(transactions)}")
        st.dataframe(
            selection, hide_index=True, width="stretch",
            column_config={
                "date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                "type": st.column_config.TextColumn("Type"),
                "ticker": st.column_config.TextColumn("Ticker"),
                "nom": st.column_config.TextColumn("Titre"),
                "quantite": st.column_config.NumberColumn("Quantité", format="%d"),
                "prix": st.column_config.NumberColumn("Prix / montant (€)", format="%.2f €"),
                "frais": st.column_config.NumberColumn("Frais", format="%.2f €"),
                "devise": st.column_config.TextColumn("Devise"),
                "prix_devise": st.column_config.NumberColumn("Prix en devise", format="%.2f",
                                                             help="Prix saisi, avant conversion en euros"),
            },
        )
        st.download_button(
            "Télécharger la sélection (CSV)", icon=":material/download:",
            data=selection.to_csv(index=False).encode("utf-8"),
            file_name="transactions_selection.csv", mime="text/csv",
        )

# ======================================================================
# PIED DE PAGE
# ======================================================================
html(ui.pied_de_page(PIED_DE_PAGE))
