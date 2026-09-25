"""
langues.py — Traduction du tableau de bord (français / anglais).

Principe :
    - dans le code, chaque texte affiché est écrit EN FRANÇAIS et passé à t() :
          t("Valeur actuelle")                       -> "Current value" en anglais
          t("Du {debut} au {fin}", debut=d, fin=f)   -> textes avec des valeurs
    - le dictionnaire TEXTES (fichier traductions.py) donne la version anglaise ;
      un texte absent du dictionnaire reste en français (rien ne plante) ;
    - td() traduit les DONNÉES (régions, secteurs, noms de scénarios...) qui
      viennent des calculs : ceux-ci restent en français, on traduit seulement
      au moment de l'affichage.

La langue est choisie dans la barre latérale (FR | EN) et mémorisée pour
chaque visiteur. Seul le tableau de bord est traduit : main.py, le rapport
PDF et les guides restent en français.

Pourquoi threading.local ? Sur un site en ligne, plusieurs visiteurs utilisent
l'application en même temps, chacun dans son propre "fil d'exécution"
(thread). Chaque fil a ainsi sa propre langue.
"""

import re
import threading

from .traductions import DONNEES, MOTIFS, TEXTES

LANGUES = {"fr": "FR", "en": "EN"}
_etat = threading.local()
MANQUANTS = set()            # textes sans traduction rencontrés (utile pour les tests)


def definir(code):
    """Choisit la langue du visiteur actuel ("fr" ou "en")."""
    _etat.code = code if code in LANGUES else "fr"


def langue():
    return getattr(_etat, "code", "fr")


def anglais():
    return langue() == "en"


def t(texte, **valeurs):
    """Traduit un texte écrit en français ; les {noms} sont remplacés par les valeurs."""
    if anglais():
        if texte in TEXTES:
            texte = TEXTES[texte]
        else:
            MANQUANTS.add(texte)
    return texte.format(**valeurs) if valeurs else texte


_MOTIFS = [(re.compile(m), r) for m, r in MOTIFS]


def td(valeur):
    """Traduit une donnée (région, secteur, scénario...). Les noms propres
    (sociétés, tickers) ne sont pas dans le dictionnaire et restent tels quels."""
    if not anglais() or not isinstance(valeur, str):
        return valeur
    if valeur in DONNEES:
        return DONNEES[valeur]
    for motif, remplacement in _MOTIFS:
        if motif.fullmatch(valeur):
            return motif.sub(remplacement, valeur)
    return valeur


# ----------------------------------------------------------------------
# Formats qui dépendent de la langue
# ----------------------------------------------------------------------
def date(d):
    """16/01/2017 en français, 16 Jan 2017 en anglais."""
    return d.strftime("%d %b %Y") if anglais() else d.strftime("%d/%m/%Y")


def eur(format_nombre):
    """Montant en euros dans un modèle Plotly : '%{y:,.0f} €' ou '€%{y:,.0f}'."""
    return f"€{format_nombre}" if anglais() else f"{format_nombre} €"


def eur_colonne(format_nombre):
    """Format d'une colonne de tableau Streamlit : '%.2f €' ou '€%.2f'."""
    return f"€{format_nombre}" if anglais() else f"{format_nombre} €"


def pct_colonne(format_nombre):
    """Format de pourcentage d'une colonne de tableau : '%.1f %%' ou '%.1f%%'."""
    return f"{format_nombre}%%" if anglais() else f"{format_nombre} %%"


def espace_pct():
    """Espace avant le signe % : oui en français, non en anglais."""
    return "" if anglais() else " "
