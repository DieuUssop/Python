"""
theme.py — Mode clair / mode nuit (bleu foncé) du tableau de bord.

Le choix se fait dans l'en-tête de la barre latérale (« Clair | Nuit »). Il est
gardé pour la session et, pour un utilisateur connecté, dans ses préférences
(chiffrées avec le reste de son espace).

Trois niveaux :
    1. nos propres éléments HTML (cartes, notes, pastilles, tableaux…) : leurs
       couleurs sont des variables CSS (assets/style.css), redéfinies ici ;
    2. les composants de Streamlit (champs, menus, onglets, boutons…) : surchargés
       en CSS ; les tableaux de données, dessinés dans un canvas, sont inversés par
       un filtre CSS (les couleurs restent lisibles) ;
    3. les graphiques Plotly : couleurs de texte, grilles et bulles adaptées
       (graphiques_interactifs.theme_figure).
Le rapport PDF reste toujours en clair (il est fait pour être imprimé).
"""

import threading

THEMES = {"clair": "Clair", "nuit": "Nuit"}
_etat = threading.local()


def definir(code):
    _etat.code = code if code in THEMES else "clair"


def nuit():
    return getattr(_etat, "code", "clair") == "nuit"


# Couleurs des graphiques en mode nuit (texte, grilles, bulles d'information)
NUIT = {
    "fond": "#0f1b2d",
    "carte": "#16243a",
    "texte": "#e6ebf2",
    "texte_2": "#b4bfcd",
    "texte_3": "#8392a6",
    "grille": "#24364f",
    "bordure": "#2c4160",
}

# Couleurs « sombres » des graphiques en mode clair -> leur équivalent lisible sur fond bleu nuit
REMPLACEMENTS_NUIT = {
    "#1a1a19": "#e6ebf2",      # texte, courbe de la loi normale, médiane
    "#5f5e5a": "#b4bfcd",      # gris foncé (indice de référence, VaR normale)
    "#898781": "#8fa0b5",      # gris (axes, titres seuls)
    "#e1e0d9": "#24364f",      # grilles
    "#a3a39e": "#7d8ba0",      # gris clair (lignes inchangées)
    "#0d366b": "#9cc3f5",      # bleu très foncé (échelles)
    "#0f2a4a": "#9cc3f5",
    "#1c5cab": "#4d8fe0",
    "white": "#16243a",        # contours blancs des barres et des points
    "#ffffff": "#16243a",
    "#eceef1": "#1d2e47",      # pays sans exposition (carte du monde)
    "#f7f7f5": "#1d2e47",      # milieu de l'échelle des corrélations (corrélation nulle)
    "#cde2fb": "#1f3a5f",      # début de l'échelle bleue (nuage de la frontière efficiente)
}

CSS_NUIT = """
<style>
:root {
    --primaire: #4d8fe0;
    --primaire-fonce: #a9cbf5;
    --texte: #e6ebf2;
    --texte-2: #b4bfcd;
    --texte-3: #8392a6;
    --bordure: #24364f;
    --fond-carte: #16243a;
    --fond-doux: #13233a;
    --positif: #5fd08c;
    --positif-fond: rgba(95, 208, 140, 0.14);
    --negatif: #ff8a80;
    --negatif-fond: rgba(255, 138, 128, 0.14);
    --neutre-fond: #1d2e47;
    --attention: #f0a95b;
    --fond-barre: #0b1524;
    --fond-actif: rgba(77, 143, 224, 0.18);
    --fond-survol: rgba(77, 143, 224, 0.08);
    --mono-fond: #2a5ea8;
    --entete-debut: #13335e;
    --entete-fin: #1f4f8f;
}

/* Page et barre latérale */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: #0f1b2d !important; color: var(--texte); }
header[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stSidebar"] { background: var(--fond-barre) !important; border-right-color: var(--bordure) !important; }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li, .stApp h1, .stApp h2, .stApp h3,
.stApp h4, [data-testid="stWidgetLabel"] p, [data-testid="stRadio"] label p, [data-testid="stCheckbox"] label p,
[data-testid="stToggle"] label p { color: var(--texte); }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p { color: var(--texte-3) !important; }
.stApp a { color: #7fb0ee; }
hr { border-color: var(--bordure) !important; }

/* Encadrés, onglets, panneaux repliables */
[data-testid="stVerticalBlockBorderWrapper"], [data-testid="stExpander"] details {
    border-color: var(--bordure) !important; background: transparent;
}
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary p { color: var(--texte-2) !important; }
.stTabs [data-baseweb="tab-list"] { border-bottom-color: var(--bordure) !important; }
.stTabs [data-baseweb="tab"] p { color: var(--texte-2); }
.stTabs [aria-selected="true"] p { color: #ffffff; }
.stTabs [data-baseweb="tab-highlight"] { background-color: var(--primaire) !important; }
.stTabs [data-baseweb="tab-border"] { background-color: var(--bordure) !important; }

/* Champs de saisie, listes déroulantes, cases */
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="textarea"],
[data-baseweb="select"] > div, [data-testid="stNumberInputContainer"] {
    background-color: #16243a !important; border-color: var(--bordure) !important; color: var(--texte) !important;
}
[data-baseweb="input"] input, [data-baseweb="base-input"] input, [data-baseweb="textarea"] textarea,
[data-baseweb="select"] input, [data-baseweb="select"] div { color: var(--texte) !important; }
[data-baseweb="select"] svg, [data-baseweb="input"] svg { fill: var(--texte-2) !important; }
[data-testid="stNumberInputStepDown"], [data-testid="stNumberInputStepUp"] {
    background-color: #1d2e47 !important; color: var(--texte) !important;
}
[data-baseweb="popover"] [data-baseweb="menu"], [data-baseweb="popover"] ul, [data-baseweb="popover"] li {
    background-color: #16243a !important; color: var(--texte) !important;
}
[data-baseweb="popover"] li:hover, [data-baseweb="popover"] li[aria-selected="true"] { background-color: #1f3352 !important; }
[data-baseweb="tag"] { background-color: #2a5ea8 !important; }
[data-baseweb="tooltip"] div, [data-testid="stTooltipContent"] { background-color: #1d2e47 !important; color: var(--texte) !important; }

/* Boutons */
button[data-testid="stBaseButton-secondary"], button[data-testid="stBaseButton-segmented_control"],
[data-testid="stDownloadButton"] button[data-testid="stBaseButton-secondary"] {
    background-color: #16243a !important; border-color: var(--bordure) !important; color: var(--texte) !important;
}
button[data-testid="stBaseButton-secondary"]:hover { border-color: var(--primaire) !important; }
button[data-testid="stBaseButton-segmented_controlActive"] {
    background-color: rgba(77, 143, 224, 0.22) !important; border-color: var(--primaire) !important; color: #ffffff !important;
}
button[data-testid="stBaseButton-primary"] { background-color: #2f6fc4 !important; border-color: #2f6fc4 !important; }
button[data-testid="stBaseButton-tertiary"], button[data-testid="stBaseButton-tertiary"] p { color: #7fb0ee !important; }

/* Envoi de fichier, curseurs, alertes */
[data-testid="stFileUploaderDropzone"] { background-color: #16243a !important; border-color: #3a5273 !important; }
[data-testid="stFileUploaderDropzone"] span, [data-testid="stFileUploaderDropzone"] small { color: var(--texte-2) !important; }
[data-testid="stSliderTickBarMin"], [data-testid="stSliderTickBarMax"], [data-testid="stSliderThumbValue"] { color: var(--texte-2) !important; }
[data-testid="stAlertContainer"], [data-testid="stAlert"] > div { background-color: #16243a !important; color: var(--texte) !important; }

/* Tableaux de données : dessinés dans un canvas, on les inverse (couleurs conservées par la rotation de teinte) */
[data-testid="stDataFrame"], [data-testid="stDataEditor"], [data-testid="stTable"] {
    filter: invert(0.9) hue-rotate(180deg);
}

/* Nos éléments aux couleurs fixes */
.pastille.attention { color: #f5c07a; background: rgba(240, 169, 91, 0.14); }
.constat { box-shadow: none; }
.constat.alerte { background: rgba(255, 138, 128, 0.07); }
.constat.attention { background: rgba(240, 169, 91, 0.07); }
.kpi, [data-testid="stVerticalBlockBorderWrapper"] { box-shadow: none !important; }
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] { border-color: #3a5273 !important; }
</style>
"""
