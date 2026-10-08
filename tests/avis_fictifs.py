"""
avis_fictifs.py — Avis d'opéré FICTIFS aux mises en page variées, fabriqués à la volée
(reportlab) pour le banc d'essai de la lecture des PDF (tests/test_pdf_universel.py).

Les mises en page imitent des familles de documents courantes (courtier en ligne français,
banque de réseau, courtier européen en anglais, néo-courtier, tableau, avis de dividende,
texte « codé », scan) ; noms, chiffres et numéros sont inventés. Chaque modèle donne le
résultat attendu : date, sens, ISIN, quantité, cours, frais (None = non vérifié).
"""

import io
from pathlib import Path

DONNEES = Path(__file__).resolve().parent / "donnees"


def _pdf(lignes, police="Helvetica", taille=10, tableaux=()):
    """lignes : [(x, y, texte)] en points depuis le haut de la page A4 ;
    tableaux : [(x, y, [largeurs], [[cellules]])] dessinés avec des traits (vrais tableaux)."""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    sortie = io.BytesIO()
    c = canvas.Canvas(sortie, pagesize=A4)
    hauteur = A4[1]
    c.setFont(police, taille)
    for x, y, texte in lignes:
        c.drawString(x, hauteur - y, texte)
    for x, y, largeurs, cellules in tableaux:
        h = 18
        for i, ligne in enumerate(cellules):
            xx = x
            for largeur, cellule in zip(largeurs, ligne):
                c.rect(xx, hauteur - y - (i + 1) * h, largeur, h)
                c.drawString(xx + 3, hauteur - y - (i + 1) * h + 5, cellule)
                xx += largeur
    c.showPage()
    c.save()
    return sortie.getvalue()


def _scan(brut):
    """Le même document, mais en image (scan) : plus aucun texte intégré."""
    import pypdfium2
    page = pypdfium2.PdfDocument(brut)[0]
    image = page.render(scale=200 / 72).to_pil().convert("L")
    sortie = io.BytesIO()
    image.save(sortie, format="PDF", resolution=200)
    return sortie.getvalue()


def _colonnes(paires, x1=60, x2=300, y=200, pas=18):
    """Intitulés à gauche, valeurs alignées à droite (mise en page « deux colonnes »)."""
    return [l for i, (a, b) in enumerate(paires) for l in ((x1, y + i * pas, a), (x2, y + i * pas, b))]


MODELES = {}


def modele(nom, attendu):
    def deco(f):
        MODELES[nom] = (f, attendu)
        return f
    return deco


def A(date, sens, isin, quantite, cours, frais=None, devise="EUR", montant=None):
    """Résultat attendu. Dividende : cours=None et montant = montant brut versé."""
    return {"date": date, "sens": sens, "isin": isin, "quantite": quantite, "cours": cours, "frais": frais,
            "devise": devise, "montant": montant}


@modele("courtier_ligne_2026", [A("28/09/2026", "VENTE", "FR0013380607", 60, 41.295, 3.80)])
def _bd_2026():
    return _pdf([(60, 60, "Format PDF Le 28/09/2026"), (60, 100, "Date Désignation Débit (€) Crédit (€)"),
                 (60, 120, "28/09/2026 VENTE COMPTANT FR0013380607 AM.C.C.40 UC.ETF C 2 473,90"),
                 (60, 138, "QUANTITE : -60"), (60, 156, "COURS : +41,295 BRUT : +2 477,70"),
                 (60, 174, "COURTAGE : +3,80 TVA : +0,00"),
                 (60, 192, "Heure Execution: 16:40:51 Lieu: EURONEXT - EURONEXT PARIS")])


@modele("courtier_ligne_2023_tableau", [A("15/12/2023", "ACHAT", "FR0010315770", 12, 280.15, 0.99)])
def _bd_2023():
    return _pdf([(60, 50, "AVIS D'EXECUTION"), (60, 68, "Paris, le 18/12/2023"),
                 (60, 86, "Compte titres n° 508 123 456 78"),
                 (60, 250, "Courtage : 0,99 EUR"), (60, 268, "Net à débiter : 3 362,79 EUR")],
                tableaux=[(40, 120, [62, 90, 80, 120, 50, 50, 70],
                           [["Date", "Opération", "Code", "Libellé", "Quantité", "Cours", "Montant"],
                            ["15/12/2023", "ACHAT COMPTANT", "FR0010315770", "LYXOR MSCI WORLD", "12", "280,15",
                             "3 361,80"]])], taille=8)


@modele("courtier_etiquettes", [A("04/03/2024", "ACHAT", "FR0000121014", 5, 650.20, 9.75)])
def _boursorama():
    return _pdf([(60, 50, "AVIS D'OPERE"), (380, 50, "Paris, le 05/03/2024"),
                 (60, 90, "ACHAT AU COMPTANT"), (60, 110, "Valeur : LVMH (FR0000121014)"),
                 (60, 128, "Date d'exécution : 04/03/2024 à 10:12:31"), (60, 146, "Quantité : 5"),
                 (60, 164, "Cours : 650,20 EUR"), (60, 182, "Montant brut : 3 251,00 EUR"),
                 (60, 200, "Courtage : 9,75 EUR"), (60, 218, "Montant net : 3 260,75 EUR"),
                 (60, 236, "Date de règlement : 06/03/2024")])


@modele("deux_colonnes_sans_deux_points", [A("12/03/2024", "ACHAT", "FR0000120073", 10, 170.50, 1.95)])
def _fortuneo():
    return _pdf([(60, 50, "Confirmation d'exécution d'ordre"), (400, 50, "Édité le 13/03/2024")]
                + _colonnes([("Sens", "Achat"), ("Valeur", "AIR LIQUIDE"), ("Code ISIN", "FR0000120073"),
                             ("Date d'exécution", "12/03/2024"), ("Quantité", "10"), ("Cours", "170,50 €"),
                             ("Montant brut", "1 705,00 €"), ("Frais de courtage", "1,95 €"),
                             ("Montant net débité", "1 706,95 €")]))


@modele("anglais_sans_etiquette_quantite", [A("07/05/2024", "ACHAT", "IE00B3XXRP09", 15, 85.12, 2.00)])
def _degiro():
    return _pdf([(60, 50, "Transaction confirmation"), (60, 70, "Client number 12345678"),
                 (60, 100, "Date 07-05-2024 14:32"),
                 (60, 130, "Buy 15 VANGUARD S&P 500 UCITS ETF IE00B3XXRP09 at 85.12 EUR"),
                 (60, 150, "Value EUR 1,276.80"), (60, 170, "Transaction costs EUR 2.00"),
                 (60, 190, "Total EUR 1,278.80")])


@modele("quantite_fractionnaire", [A("02/04/2024", "ACHAT", "IE00B4L5Y983", 3.512, 82.34, 1.00)])
def _trade_republic():
    return _pdf([(60, 50, "RÉCAPITULATIF DE L'OPÉRATION"), (60, 70, "Date 02.04.2024"),
                 (60, 90, "Ordre d'achat exécuté"),
                 (60, 120, "POSITION QUANTITÉ PRIX MONTANT"),
                 (60, 138, "iShares Core MSCI World USD (Acc) 3,512 titres 82,34 EUR 289,18 EUR"),
                 (60, 156, "ISIN : IE00B4L5Y983"),
                 (60, 186, "Frais externes 1,00 EUR"), (60, 204, "Total 290,18 EUR")])


@modele("anglais_mois_en_lettres_usd", [A("05/02/2024", "ACHAT", "US0378331005", 20, 185.20, 1.00, "USD")])
def _saxo():
    return _pdf([(60, 50, "Trade Confirmation"), (60, 70, "Account 9876543"),
                 (60, 100, "Trade date: 05-Feb-2024"), (60, 118, "Value date: 07-Feb-2024"),
                 (60, 140, "Bought 20 Apple Inc. (ISIN US0378331005)"), (60, 158, "Price 185.20 USD"),
                 (60, 176, "Trade value 3,704.00 USD"), (60, 194, "Commission 1.00 USD"),
                 (60, 212, "Total -3,705.00 USD")])


@modele("banque_date_en_toutes_lettres", [A("15/12/2023", "VENTE", "FR0000120271", 25, 62.10, 7.76)])
def _banque():
    return _pdf([(60, 50, "Banque Fictive du Centre"), (60, 68, "Le 16 décembre 2023"),
                 (60, 100, "Exécuté le 15 décembre 2023 sur Euronext Paris"),
                 (60, 118, "Opération : VENTE"), (60, 136, "Valeur : TOTALENERGIES SE"),
                 (60, 154, "Code valeur : FR0000120271"), (60, 172, "Nombre de titres : 25"),
                 (60, 190, "Prix unitaire : 62,10 €"), (60, 208, "Montant brut : 1 552,50 €"),
                 (60, 226, "Commission : 7,76 €"), (60, 244, "Net à créditer : 1 544,74 €")])


@modele("deux_operations_sans_tableau", [A("18/01/2024", "ACHAT", "FR0000121014", 2, 720.00),
                                         A("22/01/2024", "VENTE", "FR0000120271", 10, 61.50)])
def _deux_operations():
    return _pdf([(60, 50, "Récapitulatif des opérations exécutées"), (60, 70, "Arrêté au 31/01/2024"),
                 (60, 110, "18/01/2024 ACHAT FR0000121014 LVMH 2 720,00 1 440,00"),
                 (60, 128, "22/01/2024 VENTE FR0000120271 TOTALENERGIES 10 61,50 615,00")])


@modele("avis_de_dividende", [A("01/04/2024", "DIVIDENDE", "FR0000120271", 40, None, montant=31.60)])
def _dividende():
    return _pdf([(60, 50, "AVIS DE PAIEMENT DE DIVIDENDE"), (60, 80, "Valeur : TOTALENERGIES SE FR0000120271"),
                 (60, 98, "Date de paiement : 01/04/2024"), (60, 116, "Nombre de titres : 40"),
                 (60, 134, "Dividende unitaire : 0,79 EUR"), (60, 152, "Montant brut : 31,60 EUR"),
                 (60, 170, "Prélèvements sociaux : 5,44 EUR"), (60, 188, "Net crédité : 26,16 EUR")])


@modele("montant_net_seulement", [A("08/02/2024", "ACHAT", "FR0000131104", 8, 95.40, 2.50)])
def _net_seulement():
    return _pdf([(60, 50, "Avis d'opéré"), (60, 80, "Achat le 08/02/2024"),
                 (60, 98, "BNP PARIBAS FR0000131104"), (60, 116, "Quantité 8"), (60, 134, "Cours 95,40"),
                 (60, 152, "Frais 2,50"), (60, 170, "Montant net 765,70")])


@modele("texte_code", [A("04/03/2024", "ACHAT", "FR0000121014", 5, 650.20, 9.75)])
def _code():
    """PDF dont la police a un encodage « maison » : la page s'affiche correctement, mais le texte
    extrait est du charabia (« H]PZ K.VWLYL » pour « AVIS D'OPERE »), comme chez certaines banques.
    Fabriqué une fois (police DejaVu dont les codes de caractères sont décalés) et rangé dans
    tests/donnees/ pour ne pas dépendre de fontTools."""
    return (DONNEES / "avis_texte_code.pdf").read_bytes()


@modele("scan", [A("04/03/2024", "ACHAT", "FR0000121014", 5, 650.20, 9.75)])
def _scan_boursorama():
    return _scan(_pdf([(60, 50, "AVIS D'OPERE"), (60, 90, "ACHAT AU COMPTANT"),
                       (60, 110, "Valeur : LVMH (FR0000121014)"), (60, 128, "Date d'exécution : 04/03/2024"),
                       (60, 146, "Quantité : 5"), (60, 164, "Cours : 650,20 EUR"),
                       (60, 182, "Montant brut : 3 251,00 EUR"), (60, 200, "Courtage : 9,75 EUR"),
                       (60, 218, "Montant net : 3 260,75 EUR")], taille=12))


@modele("frais_multiples_et_bruit", [A("15/03/2024", "ACHAT", "FR0000120073", 30, 172.46, 20.69)])
def _frais_multiples():
    return _pdf([(60, 40, "Société de Bourse Fictive - Tél. 01 23 45 67 89"), (60, 58, "Réf. ordre : 2024031512345"),
                 (380, 40, "Édité le 16/03/2024"), (60, 90, "Achat au comptant"),
                 (60, 108, "AIR LIQUIDE - FR0000120073"), (60, 126, "Négocié le 15/03/2024 à 11:02"),
                 (60, 144, "Qté 30 Prix 172,46 Montant 5 173,80"), (60, 162, "Courtage 5,17"),
                 (60, 180, "Taxe sur les transactions financières 15,52"), (60, 198, "Net à débiter 5 194,49"),
                 (60, 216, "Date de règlement : 19/03/2024")])


@modele("usd_avec_contre_valeur_euros", [A("21/03/2024", "ACHAT", "US5949181045", 12, 415.23, 4.50, "USD")])
def _usd_conversion():
    return _pdf([(60, 50, "Confirmation d'ordre"), (60, 80, "Achat de 12 MICROSOFT CORP US5949181045"),
                 (60, 98, "Date d'exécution 21/03/2024"), (60, 116, "Cours d'exécution : 415,2300 USD"),
                 (60, 134, "Montant brut : 4 982,76 USD"), (60, 152, "Taux de change : 1,0850"),
                 (60, 170, "Contre-valeur : 4 592,40 EUR"), (60, 188, "Commission : 4,50 EUR")])


@modele("quantite_un", [A("10/05/2024", "VENTE", "FR0000121014", 1, 812.40, 1.99)])
def _quantite_un():
    return _pdf([(60, 50, "Avis d'opéré du 10/05/2024"), (60, 80, "Vente LVMH FR0000121014"),
                 (60, 98, "Quantité : 1"), (60, 116, "Cours : 812,40"), (60, 134, "Montant : 812,40"),
                 (60, 152, "Frais : 1,99"), (60, 170, "Net : 810,41")])


@modele("scan_deux_colonnes", [A("12/03/2024", "ACHAT", "FR0000120073", 10, 170.50, 1.95)])
def _scan_deux_colonnes():
    return _scan(_pdf([(60, 50, "Confirmation d'exécution d'ordre")]
                      + _colonnes([("Sens", "Achat"), ("Valeur", "AIR LIQUIDE"), ("Code ISIN", "FR0000120073"),
                                   ("Date d'exécution", "12/03/2024"), ("Quantité", "10"), ("Cours", "170,50 €"),
                                   ("Montant brut", "1 705,00 €"), ("Frais de courtage", "1,95 €"),
                                   ("Montant net débité", "1 706,95 €")]), taille=12))


@modele("colonnes_sans_traits", [A("18/03/2024", "ACHAT", "FR0000120578", 12, 88.40, 2.12)])
def _colonnes_sans_traits():
    """Intitulés sur une ligne, valeurs alignées dessous, sans traits de tableau : les frais ne
    sont reconnus qu'en associant chaque valeur à l'intitulé placé au-dessus."""
    entetes = [(40, "Date d'exécution"), (125, "Sens"), (165, "Valeur"), (235, "Code ISIN"), (320, "Quantité"),
               (375, "Cours"), (425, "Montant brut"), (500, "Frais")]
    valeurs = [(40, "18/03/2024"), (125, "Achat"), (165, "SANOFI"), (235, "FR0000120578"), (320, "12"),
               (375, "88,40"), (425, "1 060,80"), (500, "2,12")]
    return _pdf([(40, 50, "Opération exécutée")] + [(x, 100, t) for x, t in entetes]
                + [(x, 118, t) for x, t in valeurs], taille=8)


def _scan_abime(brut, angle=2.2):
    """Scan de mauvaise qualité : gris pâle sur fond gris, grain, page de travers."""
    import random
    import pypdfium2
    from PIL import Image
    page = pypdfium2.PdfDocument(brut)[0]
    image = page.render(scale=170 / 72).to_pil().convert("L")
    image = image.point(lambda v: 95 + int(v * 0.55))                 # contraste écrasé
    hasard = random.Random(7)
    bruit = Image.effect_noise(image.size, 18).point(lambda v: v - 128)
    pixels = image.load()
    grain = bruit.load()
    for _ in range(image.width * image.height // 40):                 # quelques points parasites
        x, y = hasard.randrange(image.width), hasard.randrange(image.height)
        pixels[x, y] = max(0, min(255, pixels[x, y] + grain[x, y]))
    image = image.rotate(angle, expand=True, fillcolor=205)
    sortie = io.BytesIO()
    image.save(sortie, format="PDF", resolution=170)
    return sortie.getvalue()


@modele("scan_abime", [A("04/03/2024", "ACHAT", "FR0000121014", 5, 650.20, 9.75)])
def _scan_mauvais():
    return _scan_abime(_pdf([(60, 50, "AVIS D'OPERE"), (60, 90, "ACHAT AU COMPTANT"),
                             (60, 110, "Valeur : LVMH (FR0000121014)"), (60, 128, "Date d'exécution : 04/03/2024"),
                             (60, 146, "Quantité : 5"), (60, 164, "Cours : 650,20 EUR"),
                             (60, 182, "Montant brut : 3 251,00 EUR"), (60, 200, "Courtage : 9,75 EUR"),
                             (60, 218, "Montant net : 3 260,75 EUR")], taille=11))


# Relevé de portefeuille : une position = un achat au PRU, daté du jour du relevé
@modele("releve_de_positions", [A("31/12/2023", "ACHAT", "FR0000121014", 10, 650.20, montant=6502.00),
                                A("31/12/2023", "ACHAT", "FR0000120073", 25, 140.10, montant=3502.50),
                                A("31/12/2023", "ACHAT", "IE00B4L5Y983", 40, 80.25, montant=3210.00)])
def _releve_positions():
    return _pdf([(40, 40, "RELEVÉ DE PORTEFEUILLE"), (40, 58, "Compte-titres n° 12345678 - Positions au 31/12/2023"),
                 (40, 90, "Valeur                        Code ISIN       Quantité   PRU       Cours     Valorisation   +/- value"),
                 (40, 108, "LVMH                          FR0000121014    10         650,20    731,00    7 310,00       808,00"),
                 (40, 126, "AIR LIQUIDE                   FR0000120073    25         140,10    176,12    4 403,00       900,50"),
                 (40, 144, "ISHARES CORE MSCI WORLD       IE00B4L5Y983    40         80,25     86,90     3 476,00       266,00"),
                 (40, 170, "Total                                                                       15 189,00")],
                taille=8)


def construire(nom):
    return MODELES[nom][0]()


def attendu(nom):
    return MODELES[nom][1]


if __name__ == "__main__":                       # python -m tests.avis_fictifs dossier : écrit les PDF
    import sys
    from pathlib import Path
    dossier = Path(sys.argv[1] if len(sys.argv) > 1 else "avis_fictifs")
    dossier.mkdir(exist_ok=True)
    for nom in MODELES:
        (dossier / f"{nom}.pdf").write_bytes(construire(nom))
        print(dossier / f"{nom}.pdf")
