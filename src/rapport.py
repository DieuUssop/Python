"""
rapport.py — Génère un rapport PDF complet du portefeuille.

Bibliothèque utilisée : reportlab (python -m pip install reportlab).
Principe de reportlab "platypus" : on construit une LISTE d'éléments
(titres, paragraphes, tableaux, images...) appelée "story", puis reportlab
les place automatiquement sur les pages, en changeant de page si besoin.

Les graphiques sont ceux de graphiques.py (matplotlib), enregistrés en
mémoire (io.BytesIO) au lieu d'un fichier, puis insérés comme images.

⚠️ Les polices standard du PDF (Helvetica) ne contiennent pas tous les
caractères : on évite √, σ, μ, → ou le signe moins typographique « − ».
"""

import io
from datetime import date
from html import escape

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

from . import graphiques as g

# Couleurs (les mêmes que le tableau de bord)
MARINE = colors.HexColor("#0f2a4a")
BLEU = colors.HexColor("#1c5cab")
GRIS_TEXTE = colors.HexColor("#5f5e5a")
GRIS_CLAIR = colors.HexColor("#f3f5f8")
BORDURE = colors.HexColor("#e4e7ec")
VERT = colors.HexColor("#0b7a33")
ROUGE = colors.HexColor("#b42323")

LARGEUR_UTILE = A4[0] - 3.6 * cm      # largeur de page moins les marges


# ----------------------------------------------------------------------
# Mise en forme des nombres (caractères compatibles avec les polices PDF)
# ----------------------------------------------------------------------
def euros(x, signe=False, decimales=0):
    texte = f"{x:+,.{decimales}f}" if signe else f"{x:,.{decimales}f}"
    return texte.replace(",", " ").replace(".", ",").replace(" ", " ") + " €"


def pct(x, signe=True, decimales=2):
    texte = f"{x * 100:+.{decimales}f}" if signe else f"{x * 100:.{decimales}f}"
    return texte.replace(".", ",") + " %"


def nombre(x, decimales=2):
    return f"{x:.{decimales}f}".replace(".", ",")


# ----------------------------------------------------------------------
# Styles de texte
# ----------------------------------------------------------------------
def _styles():
    base = getSampleStyleSheet()
    return {
        "titre": ParagraphStyle("titre", parent=base["Title"], fontName="Helvetica-Bold",
                                fontSize=22, leading=26, textColor=colors.white, alignment=TA_LEFT),
        "surtitre": ParagraphStyle("surtitre", fontName="Helvetica-Bold", fontSize=8,
                                   textColor=colors.HexColor("#c9d6ea"), leading=10),
        "sous_titre_bandeau": ParagraphStyle("sb", fontName="Helvetica", fontSize=10,
                                             textColor=colors.HexColor("#e6ecf5"), leading=13),
        "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=15, leading=19,
                             textColor=MARINE, spaceBefore=6, spaceAfter=8),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
                             textColor=MARINE, spaceBefore=10, spaceAfter=5),
        "texte": ParagraphStyle("texte", fontName="Helvetica", fontSize=9.5, leading=13.5,
                                textColor=colors.HexColor("#1a1a19")),
        "note": ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=8, leading=11,
                               textColor=GRIS_TEXTE),
        "cellule": ParagraphStyle("cellule", fontName="Helvetica", fontSize=8.5, leading=11),
    }


# ----------------------------------------------------------------------
# Briques de mise en page
# ----------------------------------------------------------------------
def _bandeau(st, titre, sous_titre):
    """Bandeau bleu marine en haut de la première page."""
    contenu = [[Paragraph("MASTER G2C · GESTION DE PORTEFEUILLE", st["surtitre"])],
               [Paragraph(titre, st["titre"])],
               [Paragraph(escape(sous_titre), st["sous_titre_bandeau"])]]
    tableau = Table(contenu, colWidths=[LARGEUR_UTILE])
    tableau.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MARINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 16), ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, 0), 14), ("BOTTOMPADDING", (0, -1), (-1, -1), 14),
        ("TOPPADDING", (0, 1), (-1, -1), 2),
    ]))
    return tableau


def _cartes(elements, colonnes=3):
    """Grille de chiffres clés : [(intitulé, valeur, couleur facultative), ...]."""
    style_label = ParagraphStyle("l", fontName="Helvetica-Bold", fontSize=7, leading=9,
                                 textColor=GRIS_TEXTE)
    lignes, ligne = [], []
    for element in elements:
        label, valeur = element[0], element[1]
        couleur = element[2] if len(element) > 2 else colors.HexColor("#1a1a19")
        style_valeur = ParagraphStyle("v", fontName="Helvetica-Bold", fontSize=14, leading=18,
                                      textColor=couleur)
        # escape() : un "&" (ex. "S&P 500") serait sinon lu comme une balise par reportlab
        ligne.append([Paragraph(escape(label.upper()), style_label), Paragraph(escape(valeur), style_valeur)])
        if len(ligne) == colonnes:
            lignes.append(ligne)
            ligne = []
    if ligne:
        lignes.append(ligne + [""] * (colonnes - len(ligne)))
    largeur = LARGEUR_UTILE / colonnes
    tableau = Table(lignes, colWidths=[largeur] * colonnes)
    tableau.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.6, BORDURE),
        ("INNERGRID", (0, 0), (-1, -1), 0.6, BORDURE),
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return tableau


def _tableau(entetes, lignes, largeurs=None, alignement_droite_a_partir_de=1):
    """Tableau de données avec en-tête bleu et lignes alternées."""
    donnees = [entetes] + lignes
    largeurs = largeurs or [LARGEUR_UTILE / len(entetes)] * len(entetes)
    tableau = Table(donnees, colWidths=largeurs, repeatRows=1)
    style = [
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.3),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 0), (-1, 0), BLEU),
        ("ALIGN", (alignement_droite_a_partir_de, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, BORDURE),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(donnees)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), GRIS_CLAIR))
    tableau.setStyle(TableStyle(style))
    return tableau


def _image_graphique(fonction, *arguments, largeur=LARGEUR_UTILE):
    """Dessine un graphique matplotlib en mémoire et le renvoie comme image PDF."""
    tampon = io.BytesIO()
    fonction(*arguments, tampon)          # les fonctions de graphiques.py acceptent un fichier en mémoire
    tampon.seek(0)
    largeur_px, hauteur_px = ImageReader(tampon).getSize()
    tampon.seek(0)
    return Image(tampon, width=largeur, height=largeur * hauteur_px / largeur_px)


def _pied_de_page(canvas, doc):
    """Dessiné sur chaque page : ligne, titre du rapport et numéro de page."""
    canvas.saveState()
    canvas.setStrokeColor(BORDURE)
    canvas.line(1.8 * cm, 1.5 * cm, A4[0] - 1.8 * cm, 1.5 * cm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRIS_TEXTE)
    canvas.drawString(1.8 * cm, 1.05 * cm,
                      f"Rapport de suivi de portefeuille · {date.today():%d/%m/%Y} · "
                      "Outil pédagogique, ne constitue pas un conseil en investissement")
    canvas.drawRightString(A4[0] - 1.8 * cm, 1.05 * cm, f"Page {doc.page}")
    canvas.restoreState()


def _couleur(x):
    return VERT if x > 0 else ROUGE if x < 0 else colors.HexColor("#1a1a19")


# ======================================================================
# Le rapport
# ======================================================================
def generer_rapport(res, destination, nom_indice, taux_sans_risque, niveau_var,
                    opti=None, sim=None, extensions=None):
    """Construit le rapport PDF.

    res         : résultat de analyse_complete()
    destination : nom de fichier ("rapport.pdf") ou fichier en mémoire (io.BytesIO)
    opti, sim   : résultats de l'optimisation et de la simulation (facultatifs)
    extensions  : résultat de extensions.calculer_extensions() (facultatif)
    """
    st = _styles()
    resume, positions, histo = res["resume"], res["positions"], res["historique"]
    ind, av = res["indicateurs"], res["avances"]
    debut, fin = f"{histo.index[0]:%d/%m/%Y}", f"{histo.index[-1]:%d/%m/%Y}"
    indice_court = nom_indice.split(" (")[0]      # "MSCI World (ETF...)" -> "MSCI World"
    story = []

    # ---------------- Page 1 : synthèse ----------------
    story.append(_bandeau(st, "Rapport de suivi de portefeuille",
                          f"Période du {debut} au {fin} · {resume['nb_lignes']} lignes · "
                          f"Référence : {nom_indice}"))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Synthèse", st["h1"]))
    rendement_investi = resume["gain_total"] / resume["montant_investi"]
    story.append(_cartes([
        ("Valeur actuelle", euros(resume["valeur_actuelle"])),
        ("Gain total", euros(resume["gain_total"], signe=True), _couleur(resume["gain_total"])),
        ("Gain / capital investi", pct(rendement_investi), _couleur(rendement_investi)),
        ("Performance annualisée (TWR)", pct(ind["twr_annualise"]), _couleur(ind["twr_annualise"])),
        ("TRI annuel", pct(ind["tri_annuel"]), _couleur(ind["tri_annuel"])),
        ("Volatilité annuelle", pct(ind["volatilite"], signe=False)),
        ("Ratio de Sharpe", nombre(av["sharpe"])),
        ("Max drawdown", pct(ind["max_drawdown"]), ROUGE),
        (f"VaR {niveau_var:.0%} à 1 jour", euros(av["var_euros"])),
    ]))
    story.append(Spacer(1, 12))
    story.append(_image_graphique(g.graphique_historique, histo))
    story.append(Spacer(1, 6))
    story.append(_cartes([
        ("Montant investi (au PRU)", euros(resume["montant_investi"])),
        ("Plus-values latentes", euros(resume["pv_latentes"], signe=True), _couleur(resume["pv_latentes"])),
        ("Plus-values réalisées", euros(resume["pv_realisees"], signe=True), _couleur(resume["pv_realisees"])),
        ("Dividendes perçus (bruts)", euros(resume["dividendes"])),
        ("Frais de courtage", euros(resume["frais_totaux"])),
        ("Source des cours", res["source_cours"].split(" (")[0]),
    ]))
    story.append(PageBreak())

    # ---------------- Page 2 : positions ----------------
    story.append(Paragraph("Positions détenues", st["h1"]))
    lignes = []
    for ticker, p in positions.iterrows():
        lignes.append([ticker, Paragraph(escape(str(p["nom"])), st["cellule"]), f"{p['quantite']:g}",
                       euros(p["pru"], decimales=2), euros(p["cours"], decimales=2),
                       euros(p["valeur"]), pct(p["pv_latente_pct"] / 100, decimales=1),
                       pct(p["poids_pct"] / 100, signe=False, decimales=1)])
    story.append(_tableau(
        ["Ticker", "Titre", "Qté", "PRU", "Cours", "Valeur", "+/- value", "Poids"], lignes,
        largeurs=[2.0 * cm, 4.6 * cm, 1.2 * cm, 2.0 * cm, 2.0 * cm, 2.1 * cm, 1.8 * cm, 1.7 * cm],
        alignement_droite_a_partir_de=2,
    ))
    if "devise" in positions.columns and (positions["devise"] != "EUR").any():
        par_devise = positions.loc[positions["devise"] != "EUR", "devise"].value_counts()
        resume_devises = ", ".join(f"{d} : {n} titre{'s' if n > 1 else ''}" for d, n in par_devise.items())
        story.append(Spacer(1, 4))
        story.append(Paragraph(escape(f"Titres en devise étrangère, convertis en euros au taux du jour ({resume_devises})."),
                               st["note"]))

    # Répartition par région et par secteur (si le référentiel classe les titres)
    groupes = [(c, t) for c, t in [("region", "Région"), ("secteur", "Secteur")]
               if c in positions.columns and positions[c].nunique() > 1]
    for colonne, libelle in groupes:
        repartition = positions.groupby(colonne).agg(poids=("poids_pct", "sum"), valeur=("valeur", "sum"),
                                                     lignes=("poids_pct", "size")).sort_values("poids", ascending=False)
        story.append(KeepTogether([
            Paragraph(f"Répartition par {libelle.lower()}", st["h2"]),
            _tableau([libelle, "Lignes", "Valeur", "Poids"],
                     [[escape(str(g)), str(int(r["lignes"])), euros(r["valeur"]), pct(r["poids"] / 100, signe=False, decimales=1)]
                      for g, r in repartition.iterrows()],
                     largeurs=[7 * cm, 2.5 * cm, 4 * cm, LARGEUR_UTILE - 13.5 * cm]),
        ]))

    # Corrélations : lisibles seulement pour un nombre raisonnable de titres
    if len(res["correlations"]) <= 20:
        story.append(Spacer(1, 10))
        story.append(_image_graphique(g.graphique_correlations, res["correlations"],
                                      largeur=LARGEUR_UTILE * 0.8))
    else:
        corr = res["correlations"].to_numpy()
        n = len(corr)
        moyenne = (corr.sum() - n) / (n * n - n)     # moyenne hors diagonale (la diagonale vaut 1)
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"Corrélation moyenne entre les {n} titres : {nombre(moyenne)}.", st["note"]))
    story.append(PageBreak())

    # ---------------- Page 3 : performance ----------------
    story.append(Paragraph("Performance", st["h1"]))
    story.append(_image_graphique(g.graphique_comparaison, av, nom_indice))
    story.append(Spacer(1, 6))
    annuels_p, annuels_i = ind["rendements_annuels"], av["rendements_annuels_indice"]
    lignes = [[str(a), pct(annuels_p[a]), pct(annuels_i[a]) if a in annuels_i.index else "-",
               pct(annuels_p[a] - annuels_i[a]) if a in annuels_i.index else "-"]
              for a in annuels_p.index]
    story.append(KeepTogether([
        Paragraph("Rendement par année civile (TWR)", st["h2"]),
        _tableau(["Année", "Portefeuille", indice_court, "Écart"], lignes),
    ]))
    story.append(Spacer(1, 6))
    story.append(KeepTogether([
        Paragraph("Comparaison avec l'indice", st["h2"]),
        _tableau(["Indicateur", "Valeur", "Lecture"], [
            ["Bêta", nombre(av["beta"]), "Sensibilité au marché (1 = comme l'indice)"],
            ["Alpha de Jensen (annuel)", pct(av["alpha"]), "Performance non expliquée par le marché"],
            ["Corrélation", nombre(av["correlation_indice"]), "Lien avec l'indice (de -1 à 1)"],
            ["Tracking error", pct(av["tracking_error"], signe=False), "Volatilité de l'écart avec l'indice"],
            ["Ratio d'information", nombre(av["ratio_information"]), "Écart de rendement / tracking error"],
        ], largeurs=[5 * cm, 3 * cm, LARGEUR_UTILE - 8 * cm], alignement_droite_a_partir_de=1),
    ]))
    story.append(PageBreak())

    # ---------------- Page 4 : risque ----------------
    story.append(Paragraph("Risque", st["h1"]))
    story.append(_image_graphique(g.graphique_performance, ind))
    story.append(Spacer(1, 6))
    recup = ind["date_recuperation"]
    story.append(_tableau(["Indicateur", "Portefeuille", indice_court], [
        ["Volatilité annuelle", pct(ind["volatilite"], signe=False), pct(av["volatilite_indice"], signe=False)],
        ["Ratio de Sharpe", nombre(av["sharpe"]), nombre(av["sharpe_indice"])],
        ["Ratio de Sortino", nombre(av["sortino"]), "-"],
        ["Max drawdown", pct(ind["max_drawdown"]), "-"],
        [f"VaR historique {niveau_var:.0%} (1 jour)",
         f"{pct(av['var_historique'], signe=False)} soit {euros(av['var_euros'])}", "-"],
        [f"VaR paramétrique {niveau_var:.0%} (1 jour)", pct(av["var_parametrique"], signe=False), "-"],
        ["CVaR (Expected Shortfall)", f"{pct(av['cvar'], signe=False)} soit {euros(av['cvar_euros'])}", "-"],
    ], largeurs=[6.5 * cm, 5.5 * cm, LARGEUR_UTILE - 12 * cm]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        f"Pire baisse : du plus haut du {ind['date_sommet']:%d/%m/%Y} au plus bas du "
        f"{ind['date_creux']:%d/%m/%Y}"
        + (", plus haut non retrouvé à ce jour." if recup is None else f", plus haut retrouvé le {recup:%d/%m/%Y}.")
        + f" Taux sans risque retenu : {pct(taux_sans_risque, signe=False)} par an.", st["note"]))

    # ---------------- Page 5 : optimisation ----------------
    if opti is not None:
        story.append(PageBreak())
        story.append(Paragraph(escape(f"Optimisation de Markowitz (poids maximal {opti['poids_max']:.0%} par titre)"),
                               st["h1"]))
        story.append(_image_graphique(g.graphique_frontiere, opti))
        story.append(Spacer(1, 6))
        story.append(_tableau(["Portefeuille", "Rendement espéré", "Volatilité", "Sharpe"], [
            [nom, pct(opti[cle]["rendement"]), pct(opti[cle]["volatilite"], signe=False),
             nombre(opti[cle]["sharpe"])]
            for cle, nom in [("actuel", "Portefeuille actuel"), ("variance_min", "Variance minimale"),
                             ("sharpe_max", "Sharpe maximal")]
        ]))
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            "Paramètres estimés sur l'historique des cours : l'optimisation surexploite les titres "
            "qui ont le mieux performé dans le passé (erreur d'estimation). Résultats à interpréter "
            "avec prudence.", st["note"]))

    # ---------------- Page 6 : projection ----------------
    if sim is not None:
        story.append(PageBreak())
        prm = sim["parametres"]
        story.append(Paragraph(f"Projection à {prm['annees']:g} ans (simulation de Monte-Carlo)", st["h1"]))
        story.append(_image_graphique(g.graphique_projection, sim, largeur=LARGEUR_UTILE * 0.86))
        story.append(_image_graphique(g.graphique_projection_nuage, sim, largeur=LARGEUR_UTILE * 0.86))
        story.append(Spacer(1, 4))
        cartes = [
            ("Scénario défavorable (5 %)", euros(sim["p5"])),
            ("Scénario médian", euros(sim["mediane"])),
            ("Scénario favorable (95 %)", euros(sim["p95"])),
            ("Départ + versements", euros(sim["total_apporte"])),
            ("Probabilité de perte", pct(sim["proba_perte"], signe=False, decimales=1)),
        ]
        if sim.get("proba_objectif") is not None:
            cartes.append((f"Objectif {euros(sim['objectif'])}", pct(sim["proba_objectif"], signe=False, decimales=1)))
        else:
            cartes.append(("Versement mensuel", euros(prm["versement_mensuel"])))
        story.append(_cartes(cartes))
        story.append(Spacer(1, 4))
        methode = "loi normale (mouvement brownien géométrique)" if prm["methode"] == "normale" \
            else "rééchantillonnage des rendements historiques (bootstrap)"
        nb_scenarios = f"{prm['nb_simulations']:,}".replace(",", "\u00a0")   # 5000 -> "5 000"
        story.append(Paragraph(
            f"Hypothèses : rendement annuel moyen {pct(prm['mu'])}, volatilité "
            f"{pct(prm['sigma'], signe=False)}, {nb_scenarios} scénarios, méthode : {methode}. "
            "Une projection n'est pas une prévision : elle décrit un éventail de possibles si les "
            "hypothèses se vérifient.", st["note"]))

    # ---------------- Conseil patrimonial et gestion d'actifs ----------------
    if extensions is not None:
        ext = extensions
        story.append(PageBreak())
        story.append(Paragraph("Conseil patrimonial", st["h1"]))
        adeq = ext["adequation"]
        story.append(_cartes([
            ("Profil retenu", ext["profil"].nom),
            ("Indicateur de risque (SRI)", f"{adeq['sri']} / 7"),
            ("Adéquation", "Adapté" if adeq["adapte"] else "Trop risqué", VERT if adeq["adapte"] else ROUGE),
        ]))
        story.append(Spacer(1, 6))
        fmt = lambda nom, v: f"{v:.0f}" if "SRI" in nom else pct(v, signe=False, decimales=1)
        story.append(_tableau(["Critère", "Portefeuille", "Limite du profil", "Statut"],
                              [[nom, fmt(nom, v), fmt(nom, lim), "Conforme" if ok else "Dépassé"]
                               for nom, v, lim, ok in adeq["criteres"]]))
        if not adeq["adapte"]:
            story.append(Spacer(1, 4))
            story.append(Paragraph(escape(
                f"Pour respecter le profil : conserver environ {pct(adeq['part_risquee_conseillee'], signe=False, decimales=0)} "
                f"du capital sur ce portefeuille et placer le reste sur un support sans risque."), st["note"]))

        story.append(KeepTogether([
            Paragraph(f"Fiscalité d'une vente totale aujourd'hui (ancienneté {nombre(ext['anciennete'], 1)} ans, taux 2026)",
                      st["h2"]),
            _tableau(["Enveloppe", "Impôt sur le revenu", "Prélèvements sociaux", "Gain net", "Performance nette"],
                     [[l["enveloppe"], euros(l["impot_revenu"]), euros(l["prelevements_sociaux"]),
                       euros(l["gain_net"], signe=True), pct(l["performance_nette"])] for l in ext["fiscalite"]]),
            Spacer(1, 3),
            Paragraph(escape(f"Part du portefeuille éligible au PEA : {pct(ext['part_pea'], signe=False, decimales=0)}. "
                             "Flat tax 31,4 % (12,8 % + 18,6 %) ; PEA après 5 ans : 18,6 % ; assurance-vie après "
                             "8 ans : 7,5 % après abattement + 17,2 %."), st["note"]),
        ]))

        lignes_stress = []
        if "stress" in ext:
            lignes_stress += [[l["scenario"], f"{l['debut']:%m/%Y} - {l['fin']:%m/%Y}", pct(l["variation"], decimales=1),
                               euros(l["perte_euros"], signe=True)] for _, l in ext["stress"].iterrows()]
        lignes_stress += [[l["scenario"], "hypothétique", pct(l["variation"], decimales=1),
                           euros(l["perte_euros"], signe=True)] for _, l in ext["stress_hypothetiques"].iterrows()]
        story.append(KeepTogether([
            Paragraph("Stress tests", st["h2"]),
            _tableau(["Scénario", "Période", "Variation", "Gain / perte"], lignes_stress,
                     largeurs=[7.5 * cm, 3.4 * cm, 2.6 * cm, LARGEUR_UTILE - 13.5 * cm]),
        ]))

        story.append(PageBreak())
        story.append(Paragraph("Gestion d'actifs", st["h1"]))
        if "attribution" in ext:
            a = ext["attribution"]
            p_ = a["par_region"]
            story.append(Paragraph(escape(f"Attribution de performance face au MSCI ACWI : portefeuille {pct(a['Rp'])}, "
                                          f"indice {pct(a['Rb'])}, écart {pct(a['Rp'] - a['Rb'])}"), st["h2"]))
            story.append(_tableau(["Région", "Poids ptf", "Poids indice", "Allocation", "Sélection", "Interaction"],
                                  [[escape(str(r)), pct(l["poids_portefeuille"], signe=False, decimales=1),
                                    pct(l["poids_indice"], signe=False, decimales=1), pct(l["allocation"]),
                                    pct(l["selection"]), pct(l["interaction"])] for r, l in p_.iterrows()]
                                  + [["Total", "", "", pct(a["effets"]["allocation"]), pct(a["effets"]["selection"]),
                                      pct(a["effets"]["interaction"])]]))
            story.append(Spacer(1, 3))
            story.append(Paragraph("Modèle de Brinson-Fachler, calcul mensuel relié par la méthode de Cariño ; "
                                   "indices régionaux hors dividendes convertis en euros.", st["note"]))
        if "budget" in ext:
            c = ext["budget"]["comparaison"]
            story.append(KeepTogether([
                Paragraph("Budget de risque : quatre répartitions des mêmes titres", st["h2"]),
                _tableau(["Allocation", "Rendement espéré", "Volatilité", "Sharpe", "Nb effectif de paris"],
                         [[n, pct(l["rendement"]), pct(l["volatilite"], signe=False), nombre(l["sharpe"]),
                           nombre(l["nb_effectif_paris"], 1)] for n, l in c.iterrows()]),
            ]))
        if "backtest" in ext:
            bt = ext["backtest"]
            story.append(KeepTogether([
                Paragraph("Backtest : rééquilibrer ou non (frais de 0,1 %)", st["h2"]),
                _tableau(["Stratégie", "Rendement annualisé", "Volatilité", "Max drawdown", "Rotation / an"],
                         [[n, pct(l["rendement_annualise"]), pct(l["volatilite"], signe=False),
                           pct(l["max_drawdown"]), pct(l["rotation_annuelle"], signe=False, decimales=0)]
                          for n, l in bt.iterrows()]),
                Spacer(1, 3),
                Paragraph(escape("Investir 10 000 € : " + " ; ".join(
                    f"{n.lower()} -> {euros(l['valeur_finale'])}" for n, l in ext["dca"].iterrows()) + "."), st["note"]),
            ]))

    # ---------------- Méthodologie ----------------
    story.append(PageBreak())
    story.append(Paragraph("Méthodologie", st["h1"]))
    points = [
        "<b>PRU</b> : moyenne pondérée des prix d'achat, frais d'achat inclus.",
        "<b>Valorisation</b> : dernier cours de clôture non ajusté ; titres étrangers convertis "
        "en euros au taux de change du jour (transactions converties au taux du jour de l'opération).",
        "<b>Rendement quotidien</b> : r(t) = (valeur(t) - flux(t)) / valeur(t-1) - 1, les flux "
        "étant supposés intervenir en fin de journée.",
        "<b>TWR</b> : produit des (1 + r) - 1, indépendant du calendrier des apports (norme GIPS). "
        "<b>TRI</b> : taux annuel annulant la valeur actuelle nette des flux de l'investisseur.",
        "<b>Volatilité</b> : écart-type des rendements quotidiens multiplié par racine de 252.",
        "<b>Sharpe / Sortino</b> : rendement excédentaire annualisé divisé par la volatilité "
        "(Sharpe) ou par la semi-déviation (Sortino).",
        "<b>Bêta / alpha</b> : modèle de marché (MEDAF) estimé sur les rendements quotidiens.",
        "<b>VaR / CVaR</b> : méthode historique (percentile) et paramétrique (loi normale), horizon 1 jour.",
        "<b>Markowitz</b> : optimisation sous contraintes (SLSQP), sans vente à découvert, poids plafonnés.",
        "<b>Monte-Carlo</b> : trajectoires mensuelles simulées ; percentiles de la valeur finale.",
        "<b>Profil client</b> : questionnaire inspiré de MiFID II ; SRI estimé à partir de la volatilité (classes PRIIPs).",
        "<b>Fiscalité</b> : taux 2026 (flat tax 31,4 %, PEA après 5 ans, assurance-vie après 8 ans).",
        "<b>Stress tests</b> : crises passées rejouées (indice régional si le titre n'était pas coté) et chocs hypothétiques.",
        "<b>Attribution</b> : Brinson-Fachler mensuel par région, lissage de Cariño, référence MSCI ACWI IMI.",
        "<b>Budget de risque</b> : contributions d'Euler au risque ; parité des risques (méthode de Spinu).",
    ]
    for point in points:
        story.append(Paragraph("• " + point, st["texte"]))
        story.append(Spacer(1, 3))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Limites : les rendements passés ne préjugent pas des rendements futurs ; taux sans risque "
        "constant sur la période ; dividendes bruts (avant fiscalité) ; les estimations reposent sur "
        "un historique court. Données de marché : Yahoo Finance. Taux sans risque : BCE.", st["note"]))

    doc = SimpleDocTemplate(
        destination, pagesize=A4,
        leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.6 * cm, bottomMargin=2.0 * cm,
        title="Rapport de suivi de portefeuille", author="Master G2C",
    )
    doc.build(story, onFirstPage=_pied_de_page, onLaterPages=_pied_de_page)
