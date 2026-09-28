"""
Tests de la lecture tolérante des fichiers de transactions : un fichier
préparé ou réenregistré avec Excel doit être lu comme le fichier d'origine.
"""

import pandas as pd

from src.portfolio import lire_fichier_transactions

ORIGINAL = ("date,type,ticker,nom,quantite,prix,frais\n"
            "2024-01-15,ACHAT,CW8.PA,Amundi MSCI World,10,420.00,2.50\n"
            "2024-05-22,DIVIDENDE,CW8.PA,Amundi MSCI World,0,26.40,0.00\n"
            "2024-09-18,VENTE,CW8.PA,Amundi MSCI World,4,460.50,2.50\n")


def _identique(df):
    ref = lire_fichier_transactions(ORIGINAL.encode())
    colonnes = ["date", "type", "ticker", "quantite", "prix", "frais"]
    return df[colonnes].reset_index(drop=True).equals(ref[colonnes].reset_index(drop=True))


def test_csv_excel_francais_points_virgules():
    # Excel en français : séparateur ";", virgule décimale, dates JJ/MM/AAAA, encodage Windows
    texte = ("date;type;ticker;nom;quantité;prix;frais\r\n"
             "15/01/2024;Achat;CW8.PA;Amundi MSCI World;10;420,00;2,50\r\n"
             "22/05/2024;Dividende;CW8.PA;Amundi MSCI World;0;26,40;0\r\n"
             "18/09/2024;Vente;CW8.PA;Amundi MSCI World;4;460,50;2,50\r\n")
    assert _identique(lire_fichier_transactions(texte.encode("cp1252")))


def test_lignes_entre_guillemets_et_bom():
    # Tout le texte dans la colonne A d'Excel : chaque ligne est enregistrée entre guillemets
    texte = "\r\n".join(f'"{ligne}"' for ligne in ORIGINAL.strip().splitlines())
    assert _identique(lire_fichier_transactions(texte.encode("utf-8-sig")))


def test_colonnes_et_types_en_anglais():
    texte = (ORIGINAL.replace("date,type,ticker,nom,quantite,prix,frais", "Date,Type,Ticker,Name,Quantity,Price,Fees")
             .replace("ACHAT", "Buy").replace("VENTE", "Sell").replace("DIVIDENDE", "Dividend"))
    assert _identique(lire_fichier_transactions(texte.encode()))


def test_message_clair_si_colonne_manquante():
    try:
        lire_fichier_transactions(b"a,b\n1,2\n")
    except ValueError as erreur:
        assert "Colonne(s) manquante(s)" in str(erreur)
    else:
        raise AssertionError("une erreur était attendue")


def test_fichier_excel():
    import io
    tampon = io.BytesIO()
    lire_fichier_transactions(ORIGINAL.encode()).to_excel(tampon, index=False)
    assert _identique(lire_fichier_transactions(tampon.getvalue()))
