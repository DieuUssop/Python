"""
Tests de la lecture des PDF : relevé avec un tableau d'opérations, avis
d'opéré (texte), PDF scanné refusé avec un message clair.
"""

import io

import pandas as pd

import pytest

import pdfplumber  # noqa: E402,F401  (bibliothèque de lecture des PDF)
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle  # noqa: E402
from reportlab.lib import colors  # noqa: E402

from src import import_fichier as imp  # noqa: E402


def _releve():
    sortie = io.BytesIO()
    donnees = [["Date opération", "Libellé", "Code ISIN", "Sens", "Quantité", "Cours", "Frais"],
               ["15/01/2024", "LVMH", "FR0000121014", "Achat", "2", "810,40", "1,99"],
               ["12/09/2024", "AIR LIQUIDE", "FR0000120073", "Achat", "5", "172,10", "1,99"]]
    tableau = Table(donnees)
    tableau.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.grey)]))
    SimpleDocTemplate(sortie, pagesize=A4).build([tableau])
    return sortie.getvalue()


def _avis():
    sortie = io.BytesIO()
    c = canvas.Canvas(sortie, pagesize=A4)
    y = 800
    for ligne in ["AVIS D'OPERE", "Date d'édition : 01/04/2025", "Opération : ACHAT AU COMPTANT",
                  "Valeur : APPLE INC", "Code ISIN : US0378331005", "Date d'exécution : 05/02/2025",
                  "Quantité : 15", "Cours d'exécution : 182,50 USD", "Courtage : 5,00 EUR",
                  "Montant net : 2 742,50 EUR"]:
        c.drawString(60, y, ligne)
        y -= 22
    c.save()
    return sortie.getvalue()


def _scan():
    sortie = io.BytesIO()
    c = canvas.Canvas(sortie, pagesize=A4)
    c.rect(50, 50, 200, 200, fill=1)                    # un dessin, aucun texte
    c.save()
    return sortie.getvalue()


def test_releve_pdf_lu_comme_un_tableau():
    tableau, _ = imp.lire_tableau_brut(_releve())
    corr = imp.proposer_correspondance(tableau)
    assert corr["date"] == "Date opération" and corr["identifiant"] == "Code ISIN"
    assert corr["quantite"] == "Quantité" and len(tableau) == 2


def test_avis_opere_pdf():
    grille, nature = imp.grille_pdf(_avis())
    assert nature == "pdf_avis"
    ligne = dict(zip(grille[0], grille[1]))
    assert ligne["Date"] == "05/02/2025"                # date d'exécution, pas d'édition
    assert ligne["ISIN"] == "US0378331005" and ligne["Quantité"] == "15"
    assert ligne["Cours"] == "182,50" and ligne["Devise"] == "USD"
    assert ligne["Sens"].upper() == "ACHAT"


def test_pdf_scanne_refuse():
    """Un PDF sans texte ni opération lisible est refusé avec un message clair."""
    with pytest.raises(imp.PdfIllisible):
        imp.grille_pdf(_scan())
    resultat = imp.importer_automatiquement(_scan())
    assert not resultat["sur"] and "PDF" in resultat["raison"]


def _avis_en_tableau():
    """Avis d'opéré où intitulés et valeurs sont rangés en tableau (mise en page de
    nombreux courtiers en ligne) ; la date d'édition précède la date d'exécution."""
    from reportlab.platypus import Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    sortie = io.BytesIO()
    style = getSampleStyleSheet()["Normal"]
    entete = ["Date/heure d'exécution", "Sens", "Code ISIN", "Libellé", "Quantité", "Cours", "Montant brut"]
    valeurs = ["12/03/2025 09:01:12", "Vente", "FR0000120073", "AIR LIQUIDE", "3", "185,20", "555,60"]
    tableau = Table([entete, valeurs])
    tableau.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.grey)]))
    frais = Table([["Courtage", "1,99 EUR"], ["Montant net", "553,61 EUR"]])
    SimpleDocTemplate(sortie, pagesize=A4).build([
        Paragraph("AVIS D'OPÉRÉ — Édité le 14/03/2025", style), Spacer(1, 10), tableau, Spacer(1, 10), frais])
    return sortie.getvalue()


def test_avis_opere_en_tableau():
    grille, nature = imp.grille_pdf(_avis_en_tableau())
    assert nature == "pdf_avis"
    ligne = dict(zip(grille[0], grille[1]))
    assert ligne["Date"] == "12/03/2025"                # exécution, pas édition
    assert ligne["ISIN"] == "FR0000120073" and ligne["Quantité"] == "3"
    assert ligne["Sens"].lower() == "vente" and ligne["Cours"] == "185,20"
    assert ligne["Frais"] == "1.99"


def _avis_image():
    """Avis d'opéré « imprimé en PDF » : la page n'est qu'une IMAGE, tournée d'un quart de tour."""
    from PIL import Image, ImageDraw, ImageFont
    image = Image.new("RGB", (1700, 1200), "white")
    dessin = ImageDraw.Draw(image)
    try:
        police = ImageFont.truetype("DejaVuSans.ttf", 30)
    except OSError:
        police = ImageFont.load_default()
    y = 80
    for ligne in ["Avis d'Operation", "Le 28/09/2026",
                  "28/09/2026   VENTE COMPTANT   FR0013380607   AM.C.C.40 UC.ETF C   2 473,90",
                  "QUANTITE : -60", "COURS : +41,295      BRUT : +2 477,70", "COURTAGE : +3,80   TVA : +0,00",
                  "Heure Execution: 16:40:51"]:
        dessin.text((80, y), ligne, fill="black", font=police)
        y += 70
    image = image.rotate(90, expand=True)
    sortie = io.BytesIO()
    image.save(sortie, format="PDF", resolution=150)
    return sortie.getvalue()


def test_avis_opere_image_par_reconnaissance_de_caracteres():
    from src import ocr
    if not ocr.disponible():          # moteur de reconnaissance absent : le PDF image est refusé proprement
        with pytest.raises(imp.PdfIllisible):
            imp.grille_pdf(_avis_image())
        return
    grille, nature = imp.grille_pdf(_avis_image())
    ligne = dict(zip(grille[0], grille[1]))
    assert nature == "pdf_ocr"
    assert ligne["ISIN"] == "FR0013380607" and ligne["Date"] == "28/09/2026"
    assert ligne["Sens"].upper() == "VENTE"
    nombres = imp.convertir_nombres(pd.Series([ligne["Quantité"], ligne["Cours"]]))
    assert abs(nombres[0]) == 60 and nombres[1] == pytest.approx(41.295)


def test_avis_opere_mots_colles():
    """Texte tel que le rend parfois la reconnaissance de caractères : mots collés, ISIN mal lu."""
    from src import ocr
    texte = ocr.reparer_isin("Le 28/09/2026\n28/09/2026VENTECOMPTANT FRO013380607AM.C.C.40UC.ETFC 2473,90\n"
                             "QUANTITE:-60\nCOURS:+41,295BRUT:+2477,70\nCOURTAGE:+3,80TVA:+0,00")
    date, sens, isin, libelle, quantite, cours, _, frais, _ = imp.lire_avis_opere(texte)
    assert (date, sens.upper(), isin, quantite, cours, frais) == (
        "28/09/2026", "VENTE", "FR0013380607", "-60", "+41,295", "3.80")
    assert libelle == "AM.C.C.40UC.ETFC"


def test_isin_mal_lu_corrige():
    from src import ocr
    assert ocr.reparer_isin("FRO013380607") == "FR0013380607"         # O lu au lieu de 0
    assert ocr.reparer_isin("FRO0013380607") == "FR0013380607"        # un caractère en trop
    assert ocr.reparer_isin("FR0000121015") == "FR0000121015"         # clé fausse : rien n'est inventé
    texte = ocr.reparer_isin("Lieu: EURONEXTPARIS  FRO013380607")       # un mot n'est jamais pris pour un ISIN
    assert "EURONEXTPARIS" in texte and imp.MOTIF_ISIN_TEXTE.findall(texte)[0] == "FR0013380607"
    assert not imp.isin_plausible("EUR0NEXPAR15")


def test_avis_bourse_direct_format_pdf():
    """Avis Bourse Direct téléchargé avec « Format PDF » : la case « Désignation » du tableau
    contient aussi QUANTITE, COURS… ; le libellé ne doit garder que le nom du titre."""
    texte = ("Format PDF Le 28/09/2026\nDate Désignation Débit (€) Crédit (€)\n"
             "28/09/2026 VENTE COMPTANT FR0013380607 AM.C.C.40 UC.ETF C 2 473,90\nQUANTITE : -60\n"
             "COURS : +41,295 BRUT : +2 477,70\nCOURTAGE : +3,80 TVA : +0,00\n"
             "Heure Execution: 16:40:51 Lieu: EURONEXT - EURONEXT PARIS\n")
    case = texte.split("COMPTANT ", 1)[0][-6:] + "COMPTANT FR0013380607 AM.C.C.40 UC.ETF C\nQUANTITE : -60"
    tableau = [[["Date", "Désignation", "Débit (€)", "Crédit (€)"], ["28/09/2026", case, "", "2 473,90"]]]
    ligne = imp.lire_avis_opere(texte, tableau)
    assert ligne[:4] == ["28/09/2026", "VENTE", "FR0013380607", "AM.C.C.40 UC.ETF C"]
    assert ligne[4] == "-60" and ligne[7] == "3.80"


def test_isin_etf_reconnu_sans_internet():
    """L'ISIN d'un avis d'opéré (FR0013380607 = Amundi CAC 40 Acc) est reconnu hors connexion,
    et chaque ISIN de la table intégrée a une clé de contrôle valide."""
    from src import base_titres
    for isin in base_titres.ISIN_ETF:
        assert imp.isin_valide(isin), isin
    sans_internet = lambda requete: (_ for _ in ()).throw(OSError("hors connexion"))
    tableau = imp.resoudre_identifiants(["FR0013380607"], chercher=sans_internet)
    assert tableau.loc[0, "ticker"] == "CACC.PA" and tableau.loc[0, "statut"] == "trouvé"
