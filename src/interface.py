"""
interface.py — Les "briques" visuelles du tableau de bord.

Chaque fonction renvoie un petit morceau de HTML, mis en forme par le
fichier assets/style.css. app.py les affiche avec :
    st.markdown(morceau_html, unsafe_allow_html=True)

Pourquoi du HTML ? Les composants de base de Streamlit sont pratiques mais
peu personnalisables. Ces briques donnent un rendu plus soigné (cartes,
bandeau, pastilles colorées) tout en gardant app.py lisible.

⚠️ Streamlit interprète le texte comme du Markdown : une ligne HTML qui
commence par 4 espaces serait affichée comme du code. On construit donc
chaque morceau sur une seule ligne, sans indentation.
"""

from html import escape

from .langues import anglais, t, td


# ----------------------------------------------------------------------
# Mise en forme des nombres (à la française, ou à l'anglaise si l'anglais
# est choisi dans la barre latérale)
# ----------------------------------------------------------------------
def euros(x, signe=False):
    """1234.5 -> '1 235 €' (ou '+1 235 €' avec signe=True) ; en anglais '€1,235'."""
    if anglais():
        prefixe = "-" if x < 0 else ("+" if signe else "")
        return f"{prefixe}€{abs(x):,.0f}"
    texte = f"{x:+,.0f}" if signe else f"{x:,.0f}"
    return texte.replace(",", "\u202f") + " €"      # espace fine insécable


def pct(x, signe=True, decimales=2):
    """0.1234 -> '+12,34 %' ; en anglais '+12.34%'."""
    texte = f"{x * 100:+.{decimales}f}" if signe else f"{x * 100:.{decimales}f}"
    return texte + "%" if anglais() else texte.replace(".", ",") + " %"


def nombre(x, decimales=2):
    """1.234 -> '1,23' ; en anglais '1.23'."""
    texte = f"{x:.{decimales}f}"
    return texte if anglais() else texte.replace(".", ",")


def tendance(x):
    """Classe CSS selon le signe : 'positive', 'negative' ou 'neutre'."""
    if x > 0:
        return "positive"
    if x < 0:
        return "negative"
    return "neutre"


# ----------------------------------------------------------------------
# Briques HTML
# ----------------------------------------------------------------------
def pastille(texte, sens="neutre"):
    """Petite étiquette colorée : verte (positive), rouge (negative), orange (attention) ou grise."""
    return f'<span class="pastille {sens}">{escape(texte)}</span>'


def entete(titre, surtitre, sous_titre, source, date_donnees):
    """Bandeau bleu en haut de la page."""
    en_direct = "direct" in source.lower()
    point = "point-vert" if en_direct else "point-orange"
    libelle = t("Cours en direct · Yahoo Finance") if en_direct else t("Cours en cache (hors ligne)")
    return (
        '<div class="entete">'
        '<div class="entete-gauche">'
        f'<div class="entete-surtitre">{escape(surtitre)}</div>'
        f'<div class="entete-titre">{escape(titre)}</div>'
        f'<div class="entete-sous-titre">{escape(sous_titre)}</div>'
        '</div>'
        '<div class="entete-droite">'
        f'<div class="entete-badge"><span class="point {point}"></span>{libelle}</div>'
        f'<div class="entete-date">{escape(t("Données au {date}", date=date_donnees))}</div>'
        '</div>'
        '</div>'
    )


def carte(label, valeur, detail="", aide=""):
    """Une carte de chiffre clé.

    label  : intitulé (ex. "Valeur actuelle")
    valeur : le chiffre, déjà mis en forme (ex. "45 113 €")
    detail : ligne sous le chiffre, peut contenir une pastille (HTML)
    aide   : texte affiché au survol du petit "?"
    """
    bulle = f'<span class="kpi-aide" title="{escape(aide)}">?</span>' if aide else ""
    ligne_detail = f'<div class="kpi-detail">{detail}</div>' if detail else ""
    return (
        '<div class="kpi">'
        f'<div class="kpi-label">{escape(label)}{bulle}</div>'
        f'<div class="kpi-valeur">{escape(valeur)}</div>'
        f'{ligne_detail}'
        '</div>'
    )


def grille(cartes):
    """Aligne plusieurs cartes sur une ligne (elles passent à la ligne sur petit écran)."""
    return f'<div class="kpi-grille" style="--colonnes:{len(cartes)}">' + "".join(cartes) + '</div>'


def titre_section(titre, sous_titre=""):
    """Titre (et sous-titre facultatif) placé en haut d'un encadré."""
    ligne = f'<div class="section-sous-titre">{escape(sous_titre)}</div>' if sous_titre else ""
    return f'<div class="section"><div class="section-titre">{escape(titre)}</div>{ligne}</div>'


def note(texte, attention=False):
    """Encadré discret pour une remarque ou un avertissement."""
    classe = "note attention" if attention else "note"
    return f'<div class="{classe}">{escape(texte)}</div>'


def marque(nom, sous_titre, monogramme="PT"):
    """En-tête de la barre latérale : monogramme dans un carré arrondi, nom et sous-titre."""
    return (f'<div class="marque"><div class="marque-mono">{escape(monogramme)}</div>'
            f'<div><div class="marque-nom">{escape(nom)}</div>'
            f'<div class="marque-sous-titre">{escape(sous_titre)}</div></div></div>')


def initiales(identifiant):
    """'kevin.brule' -> 'KB' ; 'kevin' -> 'KE'."""
    import re
    morceaux = [m for m in re.split(r"[._\-\s]+", str(identifiant)) if m]
    if len(morceaux) >= 2:
        return (morceaux[0][0] + morceaux[1][0]).upper()
    return str(identifiant)[:2].upper() or "?"


def compte_connecte(identifiant):
    """Pastille aux initiales et identifiant de l'utilisateur connecté."""
    return (f'<div class="compte"><div class="compte-avatar">{escape(initiales(identifiant))}</div>'
            f'<div class="compte-ident">{escape(identifiant)}</div></div>')


def separateur():
    """Fine ligne de séparation (barre latérale)."""
    return '<div class="separateur"></div>'


def bloc_titre(texte):
    """Petit titre de rubrique dans la barre latérale."""
    return f'<div class="bloc-titre">{escape(texte)}</div>'


def infos(lignes):
    """Liste "intitulé : valeur" en petits caractères (barre latérale)."""
    contenu = "<br>".join(f"<b>{escape(k)}</b> · {escape(v)}" for k, v in lignes)
    return f'<div class="infos">{contenu}</div>'


def pied_de_page(texte):
    return f'<div class="pied">{escape(texte)}</div>'


NIVEAUX = {"ok": ("Bon", "positive"), "attention": ("À surveiller", "attention"), "alerte": ("À corriger", "negative")}


def pastille_niveau(niveau):
    """Pastille verte « Bon », orange « À surveiller » ou rouge « À corriger »."""
    if niveau is None:
        return pastille(t("Non concerné"), "neutre")
    texte, sens = NIVEAUX[niveau]
    return pastille(t(texte), sens)


def synthese(cases):
    """Cases de synthèse : [(nom, niveau, chiffre clé), ...]."""
    contenu = "".join(
        f'<div class="synthese-case"><div class="synthese-nom">{escape(nom)}</div>{pastille_niveau(niveau)}'
        f'<div class="synthese-chiffre">{escape(chiffre)}</div></div>' for nom, niveau, chiffre in cases)
    return f'<div class="synthese">{contenu}</div>'


def constat(niveau, dimension, titre, risque="", pistes=()):
    """Un constat du diagnostic : niveau, ce qu'on observe, le risque, les pistes."""
    liste = "".join(f"<li>{escape(p)}</li>" for p in pistes)
    return (f'<div class="constat {niveau}"><div class="constat-entete">{pastille_niveau(niveau)}'
            f'<span class="constat-dimension">{escape(dimension)}</span></div>'
            f'<div class="constat-titre">{escape(titre)}</div>'
            + (f'<div class="constat-risque">{escape(risque)}</div>' if risque else "")
            + (f'<ul class="constat-pistes">{liste}</ul>' if liste else "") + '</div>')
