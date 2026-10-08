"""
Tests de l'import "libre" : fichiers exportés par une banque ou un courtier
(lignes de titre, codes ISIN, montant total, quantité négative, lignes de frais).
"""

import pandas as pd
import pytest

from src import import_fichier as imp

RELEVE = (
    "Relevé des opérations;;;;;;;\n"
    "Compte : 12345678;;;;;;;\n"
    ";;;;;;;\n"
    "Date opération;Libellé;Code ISIN;Opération;Quantité;Cours;Montant net;Frais\n"
    "15/01/2024;LVMH;FR0000121014;Achat Comptant;3;780,00;-2 342,00;2,00\n"
    "22/05/2024;LVMH;FR0000121014;Coupons/Dividende;;;39,00;\n"
    "10/06/2024;;;Frais de garde;;;-5,00;\n"
    "18/09/2024;LVMH;FR0000121014;Vente Comptant;-1;700,00;698,00;2,00\n"
)


def test_ligne_des_titres_detectee_apres_les_lignes_de_titre():
    tableau, ligne = imp.lire_tableau_brut(RELEVE.encode("cp1252"))
    assert ligne == 3
    assert list(tableau.columns)[:3] == ["Date opération", "Libellé", "Code ISIN"]
    assert len(tableau) == 4


def test_correspondance_proposee():
    tableau, _ = imp.lire_tableau_brut(RELEVE.encode("cp1252"))
    c = imp.proposer_correspondance(tableau.columns)
    assert c["date"] == "Date opération" and c["type"] == "Opération"
    assert c["identifiant"] == "Code ISIN" and c["nom"] == "Libellé"
    assert c["quantite"] == "Quantité" and c["prix"] == "Cours"
    assert c["montant"] == "Montant net" and c["frais"] == "Frais"


def test_releve_de_courtier_converti():
    tableau, _ = imp.lire_tableau_brut(RELEVE.encode("cp1252"))
    c = imp.proposer_correspondance(tableau.columns)
    df, rapport = imp.appliquer_correspondance(tableau, c, identifiants={"FR0000121014": "MC.PA"})
    assert rapport["ignorees"] == 1                              # la ligne de frais de garde
    assert list(df["type"]) == ["ACHAT", "DIVIDENDE", "VENTE"]
    assert list(df["ticker"]) == ["MC.PA"] * 3
    assert list(df["quantite"]) == [3, 0, 1]                     # vente : quantité rendue positive
    assert list(df["prix"]) == pytest.approx([780.0, 39.0, 700.0])   # dividende : montant total


def test_prix_deduit_du_montant_net():
    # Sans colonne de cours : achat 2 342 € frais compris -> (2 342 − 2) / 3 = 780 ;
    # vente 698 € net -> (698 + 2) / 1 = 700
    tableau, _ = imp.lire_tableau_brut(RELEVE.encode("cp1252"))
    c = imp.proposer_correspondance(tableau.drop(columns="Cours").columns)
    df, _ = imp.appliquer_correspondance(tableau.drop(columns="Cours"), c)
    assert list(df["prix"]) == pytest.approx([780.0, 39.0, 700.0])


def test_sans_colonne_type_le_signe_decide():
    texte = "Date,Symbol,Qty,Price\n2024-01-15,AAPL,10,185\n2024-03-01,AAPL,-4,170\n"
    tableau, _ = imp.lire_tableau_brut(texte.encode())
    df, _ = imp.appliquer_correspondance(tableau, imp.proposer_correspondance(tableau.columns))
    assert list(df["type"]) == ["ACHAT", "VENTE"]
    assert list(df["quantite"]) == [10, 4]


def test_isin_vers_ticker_prefere_la_place_du_pays():
    def chercher(requete):          # réponse simulée du moteur de recherche de Yahoo
        return [{"symbol": "MOH.F", "quoteType": "EQUITY", "shortname": "LVMH"},
                {"symbol": "MC.PA", "quoteType": "EQUITY", "longname": "LVMH Moët Hennessy"},
                {"symbol": "LVMUY", "quoteType": "EQUITY"}]
    res = imp.resoudre_identifiants(["FR0000121014", "AAPL", "MC.PA"], tickers_connus={"AAPL"},
                                    chercher=chercher)
    assert list(res["ticker"]) == ["MC.PA", "AAPL", "MC.PA"]
    assert list(res["statut"]) == ["trouvé", "tel quel", "tel quel"]


def test_isin_introuvable_sans_connexion():
    def chercher(requete):
        raise OSError("pas d'Internet")
    # SAP (DE0007164600) : absent des tables intégrées, donc introuvable sans Internet
    res = imp.resoudre_identifiants(["DE0007164600"], chercher=chercher)
    assert res.iloc[0]["statut"] == "introuvable" and res.iloc[0]["ticker"] == ""


def test_nombres_formats_varies():
    valeurs = pd.Series(["1 234,50", "1.234,50", "1,234.50", "(12,5)", "12,50-", "", "3"])
    resultat = imp.convertir_nombres(valeurs)
    assert list(resultat[:5]) == pytest.approx([1234.5, 1234.5, 1234.5, -12.5, -12.5])
    assert pd.isna(resultat[5]) and resultat[6] == 3
