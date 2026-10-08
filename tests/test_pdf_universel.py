"""
Banc d'essai de la lecture des PDF « quel que soit le courtier » (src/lecture_pdf.py).

Les avis d'opéré fictifs de tests/avis_fictifs.py imitent des mises en page très différentes
(intitulés avec ou sans deux-points, deux colonnes, anglais, quantité fractionnaire, date en
toutes lettres, plusieurs opérations, dividende, montant net seul, texte « codé », scans).
Chacun doit donner la bonne date, le bon sens, le bon ISIN, la bonne quantité, le bon cours
et les bons frais — par la chaîne complète (import_fichier.grille_pdf), ET par la seule
lecture du contenu, qui ne se fie à aucun intitulé.
"""

import pandas as pd
import pytest

from src import import_fichier as imp
from src import lecture_pdf as lp
from src import ocr
from tests import avis_fictifs as af

AVEC_IMAGE = {"scan", "scan_deux_colonnes", "texte_code", "scan_abime"}
# Lus par d'autres moyens que le seul contenu : intitulés au-dessus des valeurs, relevé de positions
HORS_CONTENU_SEUL = {"colonnes_sans_traits", "releve_de_positions"}


def _verifier(lignes, attendus, nom):
    for a in attendus:
        ligne = next((l for l in lignes if l["isin"] == a["isin"]), None)
        assert ligne is not None, f"{nom} : {a['isin']} non trouvé"
        assert ligne["date"] == a["date"], f"{nom} : date {ligne['date']}"
        assert imp.classer_type(ligne["sens"]) == a["sens"], f"{nom} : sens {ligne['sens']}"
        assert abs(ligne["quantite"]) == pytest.approx(a["quantite"]), f"{nom} : quantité {ligne['quantite']}"
        if a["cours"] is not None:
            assert ligne["cours"] == pytest.approx(a["cours"]), f"{nom} : cours {ligne['cours']}"
        if a["montant"] is not None:
            assert ligne["montant"] == pytest.approx(a["montant"]), f"{nom} : montant {ligne['montant']}"
        if a["frais"] is not None:
            assert (ligne["frais"] or 0) == pytest.approx(a["frais"], abs=0.011), f"{nom} : frais {ligne['frais']}"


def _depuis_grille(grille):
    lignes = []
    for brute in grille[1:]:
        l = dict(zip(grille[0], brute))
        q, c, f, m = imp.convertir_nombres(pd.Series([l["Quantité"], l["Cours"], l["Frais"] or "0", l["Montant"]]))
        lignes.append({"date": l["Date"], "sens": l["Sens"], "isin": l["ISIN"], "quantite": q,
                       "cours": c, "frais": f, "montant": m})
    return lignes


@pytest.mark.parametrize("nom", list(af.MODELES))
def test_chaine_complete(nom):
    if nom in AVEC_IMAGE and not ocr.disponible():
        with pytest.raises(imp.PdfIllisible):
            imp.grille_pdf(af.construire(nom))
        return
    if nom in AVEC_IMAGE:
        # Lecture d'image : selon le moteur installé (RapidOCR ou Tesseract), le texte reconnu varie.
        # Exigence minimale : ne JAMAIS donner de valeurs fausses (au pire, le formulaire s'ouvre).
        try:
            grille, _ = imp.grille_pdf(af.construire(nom))
        except (imp.PdfIllisible, imp.PdfNonReconnu):
            return
    else:
        grille, _ = imp.grille_pdf(af.construire(nom))
    _verifier(_depuis_grille(grille), af.attendu(nom), nom)


@pytest.mark.parametrize("nom", [n for n in af.MODELES if n not in AVEC_IMAGE | HORS_CONTENU_SEUL])
def test_lecture_par_le_contenu_seul(nom):
    """Sans aucun intitulé connu : ISIN, date, et quantité × cours = montant."""
    texte = "\n".join(p["texte"] for p in imp._pages_pdf(af.construire(nom)))
    operations = lp.lire_par_le_contenu(texte)
    assert operations and all(o["sur"] for o in operations), nom
    _verifier(operations, af.attendu(nom), nom)


def test_texte_code_detecte():
    texte = "".join(p["texte"] for p in imp._pages_pdf(af.construire("texte_code")))
    assert lp.texte_illisible(texte) and "AVIS" not in texte
    assert not lp.texte_illisible("AVIS D'OPERE\nQuantité : 5\nCours : 650,20 EUR\nMontant brut : 3 251,00 EUR")
    assert lp.texte_illisible("(cid:12)(cid:45)(cid:3)(cid:8)(cid:22)(cid:19) (cid:4)(cid:7)")


def test_dates_ecrites_de_toutes_les_facons():
    lues = [d[0] for d in lp.dates("le 15 décembre 2023 · 05-Feb-2024 · 02.04.2024 · 2024-03-21 · Mar 7, 2024 · "
                                   "1er janvier 2025")]
    assert lues == ["15/12/2023", "05/02/2024", "02/04/2024", "21/03/2024", "07/03/2024", "01/01/2025"]
    # la date d'exécution l'emporte sur les dates d'édition et de règlement
    texte = "Édité le 16/03/2024\nNégocié le 15/03/2024\nDate de règlement : 19/03/2024"
    assert lp.date_execution(texte) == "15/03/2024"
    assert lp.date_execution("Confirmation d'exécution d'ordre Édité le 13/03/2024\nDate d'exécution 12/03/2024") \
        == "12/03/2024"


def test_milliers_separes_par_des_espaces():
    """« 2 720,00 1 440,00 » : 2 titres à 720,00 = 1 440,00 (et non 2 720,00)."""
    t = lp.trio("18/01/2024 ACHAT FR0000121014 LVMH 2 720,00 1 440,00")
    assert (t["quantite"]["valeur"], t["cours"]["valeur"], t["brut"]["valeur"]) == (2, 720, 1440)
    # les numéros de compte, de téléphone et les heures ne sont pas des montants
    valeurs = {c["valeur"] for c in lp.nombres("Compte n° 508 123 456 78\nTél. 01 23 45 67 89\nà 10:12:31")}
    assert not valeurs, valeurs


def test_vrais_isin_riches_en_lettres_et_faux_isin():
    assert imp.isin_plausible("IE00B3XXRP09")              # Vanguard S&P 500 : 5 chiffres seulement
    assert not imp.isin_plausible("EUR0NEXPAR15")          # « EURONEXT PARIS » mal lu
    assert not imp.isin_plausible("ZZ0000000005")          # pays inexistant


def _incoherent():
    """Un document sans intitulés connus et dont les chiffres ne collent pas (5 × 650,20 ≠ 3 250,00)."""
    return af._pdf([(60, 50, "Document"), (60, 80, "LVMH FR0000121014 Achat 5 650,20 3 250,00 le 04/03/2024")])


def test_document_non_reconnu_formulaire_pre_rempli():
    with pytest.raises(imp.PdfNonReconnu):
        imp.grille_pdf(_incoherent())
    texte = "\n".join(p["texte"] for p in imp._pages_pdf(_incoherent()))
    c = lp.candidats([texte])
    assert c["isins"][0][0] == "FR0000121014" and c["date_proposee"] == "04/03/2024" and c["sens"] == "ACHAT"
    assert {5.0, 650.2, 3250.0} <= {n["valeur"] for n in c["nombres"]}
    assert all("[" in n["contexte"] for n in c["nombres"])          # chaque nombre montré dans son contexte
    # l'import automatique ne devine rien : il passe la main au formulaire
    r = imp.importer_automatiquement(_incoherent(), chercher=lambda q: [], marche=lambda t: ({}, None))
    assert not r["sur"] and r["raison"] == imp.MESSAGE_NON_RECONNU


# ----------------------------------------------------------------------
# Départage par les cours du marché
# ----------------------------------------------------------------------
def _ambigu():
    """Deux lectures cohérentes : 20 × 36,00 = 720,00 et 4 × 180,00 = 720,00 (la seconde a des
    intitulés et passe en tête) ; seul le cours du marché (36 €) permet de trancher."""
    return af._pdf([(60, 50, "Avis"), (60, 80, "Achat LVMH FR0000121014 le 04/03/2024"),
                    (60, 98, "20 36,00 720,00"), (60, 116, "quantité 4 cours 180,00")])


def test_depart_par_les_cours_du_marche():
    historique = pd.DataFrame({"MC.PA": [35.8, 36.1]}, index=pd.to_datetime(["2024-03-01", "2024-03-04"]))
    r = imp.importer_automatiquement(
        _ambigu(), chercher=lambda q: [{"symbol": "MC.PA", "quoteType": "EQUITY", "longname": "LVMH"}],
        marche=lambda t: ({"MC.PA": ("EUR", 1.0)}, historique))
    assert r["sur"]
    ligne = r["transactions"].iloc[0]
    assert (ligne["quantite"], ligne["prix"]) == (20, 36.0)
    assert r["resume"]["arbitrages"][0]["nouveau"] == 36.0


# ----------------------------------------------------------------------
# Modèles appris
# ----------------------------------------------------------------------
def _avis_maison(sens, nominal, px, mt, frais, date):
    return af._pdf([(60, 40, "Maison de Titres Imaginaire"), (60, 60, "Confirmation"), (60, 90, f"Sens : {sens}"),
                    (60, 108, "Valeur LVMH FR0000121014"), (60, 126, f"Jour {date}"),
                    (60, 144, f"Nominal {nominal}   Px moyen {px}   Mt {mt}"), (60, 162, f"Comm. {frais}")])


def test_modele_appris_apres_le_formulaire():
    premier = _avis_maison("S", "25", "62,10", "1 552,50", "7,76", "15/12/2023")
    with pytest.raises(imp.PdfNonReconnu):                       # intitulés inconnus, sens en code
        imp.grille_pdf(premier)
    texte = "\n".join(p["texte"] for p in imp._pages_pdf(premier))
    assert lp.apprendre(texte, {"date": "15/12/2023", "type": "VENTE", "quantite": 25, "cours": 62.10,
                                "frais": 7.76, "montant": 1552.50})
    modele = lp.charger_modeles()[0]
    assert modele["champs"]["quantite"]["etiquette"] == "nominal" and modele["sens"] == {"s": "VENTE"}
    assert "LVMH" not in str(modele["empreinte"]) and "1552" not in str(modele)     # ni nom ni montant en clair
    imp._GRILLES_PDF.clear()
    grille, nature = imp.grille_pdf(_avis_maison("S", "40", "30,00", "1 200,00", "3,00", "02/02/2024"))
    assert nature == "pdf_modele"
    assert grille[1][:2] == ["02/02/2024", "VENTE"] and grille[1][4:6] == ["40", "30"]
    imp._GRILLES_PDF.clear()
    with pytest.raises(imp.PdfNonReconnu):                       # code de sens jamais vu : on redemande
        imp.grille_pdf(_avis_maison("A", "40", "30,00", "1 200,00", "3,00", "02/02/2024"))


# ----------------------------------------------------------------------
# Position des mots, OCR, contrôles
# ----------------------------------------------------------------------
def test_intitules_au_dessus_des_valeurs():
    page = imp._pages_pdf(af.construire("colonnes_sans_traits"))[0]
    assert "Frais : 2,12" in page["paires"] and "Quantité : 12" in page["paires"]
    assert "Frais : 2,12" not in page["texte"]                   # gardées à part : pas comptées deux fois


def test_chiffres_mal_lus_par_l_ocr():
    assert ocr.reparer_nombres("Cours : 65O,2O EUR  Montant 3 25l,OO") == "Cours : 650,20 EUR  Montant 3 251,00"
    assert ocr.reparer_nombres("SOS FR0000121014 Quantité : 5 BOLLORE") == "SOS FR0000121014 Quantité : 5 BOLLORE"


def test_controles_apres_lecture():
    transactions = pd.DataFrame({"date": pd.to_datetime(["2024-03-09", "2024-03-04", "2024-03-04"]),
                                 "type": ["ACHAT", "ACHAT", "ACHAT"], "ticker": ["MC.PA", "AI.PA", "AI.PA"],
                                 "nom": ["", "", ""], "quantite": [5.0, 10.0, 10.0], "prix": [650.0, 170.0, 170.0],
                                 "frais": [1.0, 90.0, 90.0]})
    avis = pd.DataFrame([["04/03/2024", "ACHAT", "FR0000121014", "LVMH", "5", "650,20", "EUR", "9,75", "3 300,00"]],
                        columns=imp.COLONNES_AVIS)
    textes = [m["texte"] for m in lp.controles(avis, transactions)]
    assert any("ne correspond pas" in x for x in textes)          # 5 × 650,20 ± 9,75 ≠ 3 300
    assert any("jour sans bourse" in x for x in textes)           # samedi 09/03/2024
    assert any("plus de 3 %" in x for x in textes)                # 90 € de frais pour 1 700 €
    assert any("deux fois" in x for x in textes)


# ----------------------------------------------------------------------
# Formats : relevé de positions, PDF protégé, divisions d'actions
# ----------------------------------------------------------------------
def test_releve_de_positions_en_portefeuille_de_depart():
    grille, nature = imp.grille_pdf(af.construire("releve_de_positions"))
    assert nature == "pdf_positions" and len(grille) == 4         # 3 positions, une seule fois chacune
    assert all(l[1] == "ACHAT" and l[0] == "31/12/2023" for l in grille[1:])


def test_pdf_protege_par_mot_de_passe():
    import io
    from reportlab.lib import pdfencrypt
    from reportlab.pdfgen import canvas
    sortie = io.BytesIO()
    c = canvas.Canvas(sortie, encrypt=pdfencrypt.StandardEncryption("secret", ownerPassword="x", strength=128))
    c.drawString(60, 700, "Avis d'opéré · Achat LVMH FR0000121014 le 04/03/2024 Quantité : 5 Cours : 650,20 "
                          "Montant brut : 3 251,00")
    c.showPage()
    c.save()
    protege = sortie.getvalue()
    assert imp.est_protege(protege)
    with pytest.raises(imp.PdfProtege):
        imp.grille_pdf(protege)
    with pytest.raises(ValueError):
        imp.dechiffrer_pdf(protege, "mauvais")
    clair = imp.dechiffrer_pdf(protege, "secret")
    assert not imp.est_protege(clair)
    grille, _ = imp.grille_pdf(clair)
    assert grille[1][2] == "FR0000121014"


def test_division_d_actions():
    ost = lp.lire_ost("AVIS D'OPERATION SUR TITRES\nDivision du nominal\nMICHELIN FR0000121261\n"
                      "Parité : 1 action ancienne pour 4 actions nouvelles\nDate d'effet : 16/06/2023")
    assert (ost["nature"], ost["facteur"], ost["date"]) == ("division", 4.0, "16/06/2023")
    regroupement = lp.lire_ost("Regroupement d'actions WORLDLINE FR0011981968 : 10 actions anciennes pour 1 action "
                               "nouvelle, à compter du 02/05/2024")
    assert regroupement["facteur"] == pytest.approx(0.1) and regroupement["libelle"] == "WORLDLINE"
    assert lp.lire_ost("Achat LVMH FR0000121014 le 04/03/2024") is None
    from src import mouvements
    contenu = ("date,type,ticker,nom,quantite,prix,frais\n2022-03-01,ACHAT,ML.PA,Michelin,10,120,2\n"
               "2023-01-10,DIVIDENDE,ML.PA,Michelin,0,45,0\n2023-09-01,ACHAT,ML.PA,Michelin,8,28,1\n").encode()
    ajuste, n = mouvements.appliquer_division(contenu, "ML.PA", pd.Timestamp("2023-06-16"), 4.0)
    assert n == 1
    assert list(ajuste["quantite"]) == [40, 0, 8] and list(ajuste["prix"]) == [30, 45, 28]


# ----------------------------------------------------------------------
# Rapport anonymisé et vrais avis
# ----------------------------------------------------------------------
def test_rapport_anonymise():
    texte = ("Monsieur Jean DUPONT\n12 rue des Lilas\n14000 CAEN\nCompte n° 508 123 456 78 - IBAN FR76 3000 4000 "
             "0312 3456 7890 143\njean.dupont@mail.fr Tél. 06 12 34 56 78\n"
             "Achat LVMH FR0000121014 le 04/03/2024 Quantité : 5 Cours : 650,20 Montant : 3 251,00")
    propre = lp.anonymiser(texte)
    for prive in ("DUPONT", "Lilas", "CAEN", "508 123", "FR76", "jean.dupont", "06 12"):
        assert prive not in propre, prive
    for utile in ("FR0000121014", "04/03/2024", "650,20", "3 251,00", "Quantité"):
        assert utile in propre, utile
    rapport = lp.rapport_anonymise([texte], nom_fichier="avis.pdf")
    assert "DUPONT" not in rapport and "FR0000121014" in rapport


def _vrais_avis():
    import csv
    from pathlib import Path
    dossier = Path(__file__).resolve().parent / "donnees" / "vrais_avis"
    with (dossier / "attendus.csv").open(encoding="utf-8") as f:
        lignes = list(csv.DictReader(f, delimiter=";"))
    return dossier, lignes


def test_vrais_avis_anonymises():
    """Chaque vrai avis déposé dans tests/donnees/vrais_avis (voir son README) est lu exactement."""
    dossier, lignes = _vrais_avis()
    for fichier in sorted({l["fichier"] for l in lignes}):
        grille, _ = imp.grille_pdf((dossier / fichier).read_bytes())
        attendus = [af.A(l["date"], l["sens"], l["isin"], float(l["quantite"]), float(l["cours"]),
                         float(l["frais"]) if l["frais"] else None) for l in lignes if l["fichier"] == fichier]
        _verifier(_depuis_grille(grille), attendus, fichier)


def test_isin_hors_connexion():
    from src import base_titres
    for isin in base_titres.ISIN_ACTIONS:
        assert imp.isin_valide(isin), isin
    assert base_titres.chercher_localement("FR0000120578")[0]["symbol"] == "SAN.PA"
    assert base_titres.chercher_localement("US0378331005")[0]["symbol"] == "AAPL"


# ----------------------------------------------------------------------
# Vrai relevé Interactive Brokers imprimé en « mode sombre » (texte lu par la reconnaissance de
# caractères, numéro de compte masqué) : une ligne par opération, symboles sans ISIN, virgules
# parfois perdues par la reconnaissance (« -23418 » pour -234,18 ; « 72712714286 » pour 72,712714286)
# ----------------------------------------------------------------------
def test_releve_interactive_brokers_lu_ligne_par_ligne():
    from pathlib import Path
    texte = (Path(__file__).resolve().parent / "donnees" / "vrais_avis" / "interactive_brokers_ocr.txt").read_text(
        encoding="utf-8")
    operations = lp.lire_lignes_operations(texte)
    assert len(operations) == 17 and all(o["sur"] for o in operations)
    attendu = [("13/07/2026", "ACHAT", "ESE", 7, 33.454), ("03/08/2026", "ACHAT", "ESE", 15, 33.08),
               ("19/08/2026", "ACHAT", "ESE", 14, 33.608), ("07/09/2026", "ACHAT", "ESE", 28, 33.626),
               ("09/09/2026", "ACHAT", "ESE", 1, 33.3142), ("18/09/2026", "VENTE", "ESE", 11, 33.765),
               ("18/09/2026", "VENTE", "ESE", 2, 33.761), ("02/10/2025", "ACHAT", "ESE", 34, 28.8068),
               ("10/10/2025", "ACHAT", "LYSX", 8, 62.52), ("19/08/2026", "ACHAT", "MSE", 7, 73.67),
               ("07/09/2026", "ACHAT", "MSE", 7, 72.712714286), ("18/09/2026", "VENTE", "MSE", 6, 70.99),
               ("10/10/2025", "ACHAT", "PAEJ", 23, 21.551), ("19/08/2026", "ACHAT", "PAEJ", 19, 26.7353),
               ("07/09/2026", "ACHAT", "PAEJ", 19, 27.74), ("18/09/2026", "VENTE", "PAEJ", 20, 27.125),
               ("18/09/2026", "ACHAT", "RMS", 1, 1339.0)]
    for o, (date, sens, titre, q, p) in zip(operations, attendu):
        assert (o["date"], o["sens"], o["isin"]) == (date, sens, titre)
        assert o["quantite"] == q and o["cours"] == pytest.approx(p)
    assert all(abs(o["quantite"] * o["cours"] - o["montant"]) <= 0.011 for o in operations)


def test_page_en_mode_sombre_remise_en_noir_sur_blanc():
    from PIL import Image, ImageDraw
    image = Image.new("L", (900, 200), 30)                    # fond sombre, texte clair, une bordure claire
    dessin = ImageDraw.Draw(image)
    dessin.rectangle([10, 10, 890, 190], outline=230, width=3)
    dessin.text((40, 80), "BUY 7 33.4540 -234.18", fill=230)
    assert ocr.fond_sombre(image)
    propre = ocr.normaliser_polarite(image)
    import numpy as np
    pixels = np.asarray(propre)
    assert pixels.mean() > 200                                # fond devenu blanc
    assert (pixels[60:110, 30:400] < 128).any()               # le texte est resté (en noir)
    assert (pixels[10:14, 100:800] > 128).all()               # la bordure a été effacée
