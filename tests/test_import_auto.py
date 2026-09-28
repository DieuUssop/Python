"""
Tests de la détection automatique : colonnes reconnues par leur contenu,
codes ISIN vérifiés, ordre jour/mois des dates, et prix reconvertis dans la
devise du titre grâce aux vrais cours (ici simulés).
"""

import pandas as pd
import pytest

from src import import_fichier as imp


def test_cle_de_controle_isin():
    assert imp.isin_valide("FR0000121014")         # LVMH
    assert imp.isin_valide("US0378331005")         # Apple
    assert not imp.isin_valide("FR0000121015")     # dernier chiffre faux
    assert not imp.isin_valide("LVMH")


def test_ordre_des_dates():
    assert imp.ordre_des_dates(pd.Series(["03/04/2024", "13/04/2024"])) == ("jour", False)
    assert imp.ordre_des_dates(pd.Series(["03/04/2024", "04/13/2024"])) == ("mois", False)
    assert imp.ordre_des_dates(pd.Series(["03/04/2024"])) == ("jour", True)     # ambigu : jour d'abord
    assert imp.convertir_dates(pd.Series(["04/13/2024", "01/02/2024"]))[1] == pd.Timestamp("2024-01-02")


# Relevé SANS ligne de titres, colonnes dans le désordre :
# nom ; quantité ; montant net ; date ; ISIN ; cours ; frais
SANS_ENTETE = (
    "LVMH;3;2342,00;15/01/2024;FR0000121014;780,00;2,00\n"
    "TotalEnergies;10;650,00;05/02/2024;FR0000120271;64,50;5,00\n"
    "Air Liquide;5;853,50;20/03/2024;FR0000120073;170,20;2,50\n"
    "LVMH;2;912,20;18/04/2024;FR0000121014;455,10;2,00\n"
)


def test_colonnes_reconnues_par_leur_contenu():
    tableau, ligne = imp.lire_tableau_brut(SANS_ENTETE.encode())
    assert ligne == -1 and len(tableau) == 4                 # pas de ligne de titres
    c = imp.proposer_correspondance(tableau)
    assert c["date"] == "Colonne 4" and c["identifiant"] == "Colonne 5" and c["nom"] == "Colonne 1"
    assert c["quantite"] == "Colonne 2" and c["prix"] == "Colonne 6"
    assert c["montant"] == "Colonne 3" and c["frais"] == "Colonne 7"
    assert imp.confiance(tableau, c)                         # les chiffres sont cohérents


def test_titres_de_colonnes_sans_signification():
    texte = "A;B;C;D;E;F;G\n" + SANS_ENTETE
    tableau, _ = imp.lire_tableau_brut(texte.encode())
    c = imp.proposer_correspondance(tableau)
    assert (c["quantite"], c["prix"], c["montant"]) == ("B", "F", "C")


# ----------------------------------------------------------------------
# Devises
# ----------------------------------------------------------------------
DATES = pd.bdate_range("2024-01-08", "2024-01-26")
HISTORIQUE = pd.DataFrame({"AAPL": 185.0, "EURUSD=X": 1.09, "ULVR.L": 4000.0, "EURGBP=X": 0.86,
                           "MC.PA": 780.0}, index=DATES)
INFO = {"AAPL": ("USD", 1.0), "ULVR.L": ("GBP", 0.01), "MC.PA": ("EUR", 1.0)}


def _transactions(lignes):
    return pd.DataFrame(lignes, columns=["date", "type", "ticker", "nom", "quantite", "prix", "frais"]) \
        .assign(date=lambda d: pd.to_datetime(d["date"]))


def test_prix_en_euros_reconvertis_en_dollars():
    t = _transactions([["2024-01-15", "ACHAT", "AAPL", "Apple", 10, 185 / 1.09, 1.0],
                       ["2024-01-22", "DIVIDENDE", "AAPL", "Apple", 0, 10.0, 0.0]])
    resultat, rapport = imp.harmoniser_devises(t, INFO, HISTORIQUE)
    assert resultat.loc[0, "prix"] == pytest.approx(185.0)
    assert resultat.loc[1, "prix"] == pytest.approx(10.9)       # dividende reçu en euros, lui aussi
    assert rapport["conversions"][0]["lecture"] == "euros"


def test_prix_en_livres_ramenes_en_pence():
    t = _transactions([["2024-01-15", "ACHAT", "ULVR.L", "Unilever", 20, 40.0, 1.0]])
    resultat, rapport = imp.harmoniser_devises(t, INFO, HISTORIQUE)
    assert resultat.loc[0, "prix"] == pytest.approx(4000.0)
    assert rapport["conversions"][0]["lecture"] == "devise"


def test_prix_deja_dans_la_bonne_devise_et_alerte():
    t = _transactions([["2024-01-15", "ACHAT", "AAPL", "Apple", 10, 185.5, 1.0],
                       ["2024-01-16", "ACHAT", "MC.PA", "LVMH", 1, 2340.0, 1.0]])   # 3 fois le cours : erreur
    resultat, rapport = imp.harmoniser_devises(t, INFO, HISTORIQUE)
    assert list(resultat["prix"]) == pytest.approx([185.5, 2340.0])
    assert rapport["conversions"] == []
    assert [a["ticker"] for a in rapport["alertes"]] == ["MC.PA"]


def test_import_automatique_complet():
    # Relevé d'une banque française : action américaine désignée par son ISIN, montants en euros
    texte = ("Date;Valeur;Code ISIN;Opération;Qté;Cours;Montant;Frais\n"
             "15/01/2024;APPLE INC;US0378331005;Achat;10;169,72;-1 698,20;1,00\n"
             "16/01/2024;LVMH;FR0000121014;Achat;2;780,00;-1 562,00;2,00\n")
    def chercher(requete):
        return {"US0378331005": [{"symbol": "AAPL", "quoteType": "EQUITY", "longname": "Apple Inc."}],
                "FR0000121014": [{"symbol": "MC.PA", "quoteType": "EQUITY"}]}.get(requete, [])
    resultat = imp.importer_automatiquement(texte.encode(), chercher=chercher,
                                            marche=lambda t: (INFO, HISTORIQUE))
    assert resultat["sur"]
    t = resultat["transactions"]
    assert list(t["ticker"]) == ["AAPL", "MC.PA"]
    assert t.loc[0, "prix"] == pytest.approx(185.0, rel=1e-3)   # reconverti en dollars
    assert t.loc[1, "prix"] == pytest.approx(780.0)


def test_import_automatique_demande_aide_si_doute():
    texte = "X;Y\n1;2\n3;4\n"
    assert not imp.importer_automatiquement(texte.encode(), marche=lambda t: ({}, None))["sur"]


def test_classeur_excel_la_bonne_feuille_est_choisie():
    import io
    tampon = io.BytesIO()
    with pd.ExcelWriter(tampon, engine="openpyxl") as w:
        pd.DataFrame({"Notes": ["Mon portefeuille"]}).to_excel(w, sheet_name="Notes", index=False)
        pd.DataFrame({"Date": ["2024-01-16", "2024-02-01"], "Ticker": ["MC.PA", "AAPL"], "Quantité": [3, 5],
                      "Prix": [740.0, 186.0]}).to_excel(w, sheet_name="Opérations", index=False, startrow=2)
    brut = tampon.getvalue()
    assert imp.meilleure_feuille(brut) == "Opérations"
    tableau, ligne = imp.lire_tableau_brut(brut)
    assert ligne == 2 and len(tableau) == 2


def test_informations_autour_du_tableau_ignorees():
    # Titre au-dessus, colonne de commentaires, ligne vide, total et source sous le tableau,
    # petit tableau de résumé à droite : seules les 2 opérations sont gardées
    texte = ("Mon portefeuille PEA;;;;;;;;;\n"
             ";;;;;;;;;\n"
             "Date;Code;Quantité;Prix;Frais;Commentaire;;Résumé;Valeur\n"
             "16/01/2024;MC.PA;3;740,00;2,00;conseil de mon oncle;;Nombre de lignes;2\n"
             "02/04/2024;TTE.PA;20;64,00;2,00;;;Frais totaux;4\n"
             ";;;;;;;;\n"
             "Total;;;;4,00;;;;\n"
             "Source : relevé de la banque;;;;;;;;\n")
    r = imp.importer_automatiquement(texte.encode(), chercher=lambda q: [], marche=lambda t: ({}, None))
    assert r["sur"]
    assert list(r["transactions"]["ticker"]) == ["MC.PA", "TTE.PA"]
    assert list(r["transactions"]["nom"]) == ["MC.PA", "TTE.PA"]      # le résumé n'est pas pris pour un nom
