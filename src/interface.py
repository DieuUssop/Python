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


# ----------------------------------------------------------------------
# Mise en forme des nombres (à la française)
# ----------------------------------------------------------------------
def euros(x, signe=False):
    """1234.5 -> '1 235 €' (ou '+1 235 €' avec signe=True)."""
    texte = f"{x:+,.0f}" if signe else f"{x:,.0f}"
    return texte.replace(",", " ") + " €"      # espace fine insécable


def pct(x, signe=True, decimales=2):
    """0.1234 -> '+12,34 %'."""
    texte = f"{x * 100:+.{decimales}f}" if signe else f"{x * 100:.{decimales}f}"
    return texte.replace(".", ",") + " %"


def nombre(x, decimales=2):
    """1.234 -> '1,23'."""
    return f"{x:.{decimales}f}".replace(".", ",")


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
    """Petite étiquette colorée : verte (positive), rouge (negative) ou grise."""
    return f'<span class="pastille {sens}">{escape(texte)}</span>'


def entete(titre, surtitre, sous_titre, source, date_donnees):
    """Bandeau bleu en haut de la page."""
    en_direct = "direct" in source.lower()
    point = "point-vert" if en_direct else "point-orange"
    libelle = "Cours en direct · Yahoo Finance" if en_direct else "Cours en cache (hors ligne)"
    return (
        '<div class="entete">'
        '<div class="entete-gauche">'
        f'<div class="entete-surtitre">{escape(surtitre)}</div>'
        f'<div class="entete-titre">{escape(titre)}</div>'
        f'<div class="entete-sous-titre">{escape(sous_titre)}</div>'
        '</div>'
        '<div class="entete-droite">'
        f'<div class="entete-badge"><span class="point {point}"></span>{libelle}</div>'
        f'<div class="entete-date">Données au {escape(date_donnees)}</div>'
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


def marque(nom, sous_titre):
    """Nom de l'application en haut de la barre latérale."""
    return (f'<div class="marque"><div class="marque-nom">{escape(nom)}</div>'
            f'<div class="marque-sous-titre">{escape(sous_titre)}</div></div>')


def bloc_titre(texte):
    """Petit titre de rubrique dans la barre latérale."""
    return f'<div class="bloc-titre">{escape(texte)}</div>'


def infos(lignes):
    """Liste "intitulé : valeur" en petits caractères (barre latérale)."""
    contenu = "<br>".join(f"<b>{escape(k)}</b> · {escape(v)}" for k, v in lignes)
    return f'<div class="infos">{contenu}</div>'


def pied_de_page(texte):
    return f'<div class="pied">{escape(texte)}</div>'


def echelle_sri(classe):
    """Échelle de risque 1 à 7, la classe du portefeuille mise en évidence
    (comme sur les documents d'information des produits financiers)."""
    cases = "".join(
        f'<div class="sri-case{" sri-active" if i == classe else ""}">{i}</div>' for i in range(1, 8)
    )
    return ('<div class="sri"><div class="sri-legende"><span>Risque plus faible</span>'
            f'<span>Risque plus élevé</span></div><div class="sri-cases">{cases}</div></div>')


def tableau_criteres(criteres, formats):
    """Tableau HTML des critères d'adéquation : critère, portefeuille, limite, statut."""
    lignes = ""
    for (nom, valeur, limite, ok), fmt in zip(criteres, formats):
        statut = pastille("Conforme", "positive") if ok else pastille("Dépassé", "negative")
        lignes += (f"<tr><td>{escape(nom)}</td><td class='num'>{escape(fmt(valeur))}</td>"
                   f"<td class='num'>{escape(fmt(limite))}</td><td>{statut}</td></tr>")
    return ('<table class="criteres"><thead><tr><th>Critère</th><th class="num">Portefeuille</th>'
            f'<th class="num">Limite du profil</th><th>Statut</th></tr></thead><tbody>{lignes}</tbody></table>')


def verdict(ok, titre, texte):
    """Encadré vert (adapté) ou rouge (non adapté)."""
    return (f'<div class="verdict {"ok" if ok else "ko"}"><div class="verdict-titre">{escape(titre)}</div>'
            f'<div class="verdict-texte">{escape(texte)}</div></div>')
