"""
Tests de la lecture des PDF : relevé avec un tableau d'opérations, avis
d'opéré (texte), PDF scanné refusé avec un message clair.
"""

import io

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
    with pytest.raises(imp.PdfIllisible):
        imp.grille_pdf(_scan())
    resultat = imp.importer_automatiquement(_scan())
    assert not resultat["sur"] and "scanné" in resultat["raison"]
