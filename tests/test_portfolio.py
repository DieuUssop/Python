"""
Tests automatiques : on vérifie les calculs sur des cas simples dont on
connaît le résultat à la main.

Pour les lancer :  python -m pytest
"""

import pytest

from src.portfolio import Portfolio


def ecrire_csv(tmp_path, lignes):
    """Crée un petit fichier CSV temporaire pour un test."""
    fichier = tmp_path / "transactions.csv"
    entete = "date,type,ticker,nom,quantite,prix,frais\n"
    fichier.write_text(entete + "\n".join(lignes), encoding="utf-8")
    return fichier


def test_pru_deux_achats(tmp_path):
    # 10 titres à 100 € + 10 titres à 200 €, sans frais -> PRU = 150 €
    f = ecrire_csv(tmp_path, [
        "2024-01-01,ACHAT,AAA,Test,10,100,0",
        "2024-02-01,ACHAT,AAA,Test,10,200,0",
    ])
    p = Portfolio(f)
    assert p.positions.loc["AAA", "quantite"] == 20
    assert p.positions.loc["AAA", "pru"] == pytest.approx(150)


def test_frais_inclus_dans_pru(tmp_path):
    # 10 titres à 100 € + 10 € de frais -> PRU = 1010 / 10 = 101 €
    f = ecrire_csv(tmp_path, ["2024-01-01,ACHAT,AAA,Test,10,100,10"])
    assert Portfolio(f).positions.loc["AAA", "pru"] == pytest.approx(101)


def test_vente_plus_value(tmp_path):
    # Achat 10 à 100 €, vente 4 à 130 € avec 2 € de frais
    # PV = 4 × (130 − 100) − 2 = 118 € ; il reste 6 titres, PRU inchangé
    f = ecrire_csv(tmp_path, [
        "2024-01-01,ACHAT,AAA,Test,10,100,0",
        "2024-03-01,VENTE,AAA,Test,4,130,2",
    ])
    pos = Portfolio(f).positions.loc["AAA"]
    assert pos["pv_realisee"] == pytest.approx(118)
    assert pos["quantite"] == 6
    assert pos["pru"] == pytest.approx(100)


def test_dividende(tmp_path):
    f = ecrire_csv(tmp_path, [
        "2024-01-01,ACHAT,AAA,Test,10,100,0",
        "2024-06-01,DIVIDENDE,AAA,Test,0,25,0",
    ])
    assert Portfolio(f).positions.loc["AAA", "dividendes"] == pytest.approx(25)


def test_vente_trop_grande_refusee(tmp_path):
    f = ecrire_csv(tmp_path, [
        "2024-01-01,ACHAT,AAA,Test,5,100,0",
        "2024-02-01,VENTE,AAA,Test,10,100,0",
    ])
    with pytest.raises(ValueError):
        Portfolio(f)


def test_type_inconnu_refuse(tmp_path):
    f = ecrire_csv(tmp_path, ["2024-01-01,CADEAU,AAA,Test,5,100,0"])
    with pytest.raises(ValueError):
        Portfolio(f)


# ----------------------------------------------------------------------
# Étape 2 : valorisation aux cours du marché
# ----------------------------------------------------------------------
def test_valorisation(tmp_path):
    # 10 AAA au PRU de 100 €, cours actuel 120 € -> valeur 1200 €, PV +200 € (+20 %)
    # 5 BBB au PRU de 200 €, cours actuel 160 € -> valeur 800 €, PV −200 € (−20 %)
    f = ecrire_csv(tmp_path, [
        "2024-01-01,ACHAT,AAA,Test A,10,100,0",
        "2024-01-01,ACHAT,BBB,Test B,5,200,0",
    ])
    tab = Portfolio(f).valoriser({"AAA": 120, "BBB": 160})
    assert tab.loc["AAA", "valeur"] == pytest.approx(1200)
    assert tab.loc["AAA", "pv_latente"] == pytest.approx(200)
    assert tab.loc["AAA", "pv_latente_pct"] == pytest.approx(20)
    assert tab.loc["BBB", "pv_latente_pct"] == pytest.approx(-20)
    # Poids : 1200 / 2000 = 60 % et 800 / 2000 = 40 %
    assert tab.loc["AAA", "poids_pct"] == pytest.approx(60)
    assert tab["poids_pct"].sum() == pytest.approx(100)


def test_ligne_vendue_non_valorisee(tmp_path):
    # Un titre entièrement vendu ne doit plus apparaître dans la valorisation.
    f = ecrire_csv(tmp_path, [
        "2024-01-01,ACHAT,AAA,Test,10,100,0",
        "2024-01-01,ACHAT,BBB,Test,10,100,0",
        "2024-02-01,VENTE,BBB,Test,10,110,0",
    ])
    p = Portfolio(f)
    assert p.tickers() == ["AAA"]
    assert list(p.valoriser({"AAA": 100}).index) == ["AAA"]


def test_gain_total(tmp_path):
    # PV latente 10 × (120 − 100) = 200 ; dividende 30 -> gain total 230
    f = ecrire_csv(tmp_path, [
        "2024-01-01,ACHAT,AAA,Test,10,100,0",
        "2024-06-01,DIVIDENDE,AAA,Test,0,30,0",
    ])
    r = Portfolio(f).resume_valorise({"AAA": 120})
    assert r["valeur_actuelle"] == pytest.approx(1200)
    assert r["gain_total"] == pytest.approx(230)


def test_cours_manquant_refuse(tmp_path):
    f = ecrire_csv(tmp_path, ["2024-01-01,ACHAT,AAA,Test,10,100,0"])
    with pytest.raises(ValueError):
        Portfolio(f).valoriser({})


# ----------------------------------------------------------------------
# Étape 3 : historique jour par jour
# ----------------------------------------------------------------------
import pandas as pd  # noqa: E402


def cours_fictifs(dates, **colonnes):
    """Fabrique un petit tableau de cours : cours_fictifs(dates, AAA=[...])."""
    return pd.DataFrame(colonnes, index=pd.to_datetime(dates))


def test_historique_valeur_et_apports(tmp_path):
    # Lundi : achat de 10 AAA à 100 € (+ 5 € de frais) -> on a investi 1005 €
    # Cours : 100 lundi, 110 mardi, 90 mercredi
    f = ecrire_csv(tmp_path, ["2024-01-01,ACHAT,AAA,Test,10,100,5"])
    prix = cours_fictifs(["2024-01-01", "2024-01-02", "2024-01-03"], AAA=[100, 110, 90])
    h = Portfolio(f).historique(prix)
    assert list(h["valeur"]) == [1000, 1100, 900]
    assert list(h["apports_nets"]) == [1005, 1005, 1005]
    assert list(h["gain"]) == [-5, 95, -105]


def test_historique_vente_et_dividende(tmp_path):
    # Jour 1 : achat 10 à 100. Jour 2 : dividende 20 €. Jour 3 : vente 4 à 120.
    f = ecrire_csv(tmp_path, [
        "2024-01-01,ACHAT,AAA,Test,10,100,0",
        "2024-01-02,DIVIDENDE,AAA,Test,0,20,0",
        "2024-01-03,VENTE,AAA,Test,4,120,0",
    ])
    prix = cours_fictifs(["2024-01-01", "2024-01-02", "2024-01-03"], AAA=[100, 100, 120])
    h = Portfolio(f).historique(prix)
    # Quantités : 10, 10, 6  -> valeurs : 1000, 1000, 720
    assert list(h["valeur"]) == [1000, 1000, 720]
    # Apports : 1000, puis 1000 − 20 = 980, puis 980 − 480 = 500
    assert list(h["apports_nets"]) == [1000, 980, 500]


def test_transaction_le_week_end(tmp_path):
    # Achat saisi le samedi 6 janvier 2024 -> rattaché au lundi 8 janvier.
    f = ecrire_csv(tmp_path, ["2024-01-06,ACHAT,AAA,Test,1,100,0"])
    prix = cours_fictifs(["2024-01-05", "2024-01-08", "2024-01-09"], AAA=[100, 100, 100])
    h = Portfolio(f).historique(prix)
    assert h.index[0] == pd.Timestamp("2024-01-08")
    assert h.loc["2024-01-08", "apports_nets"] == 100


def test_coherence_historique_et_etape_2(tmp_path):
    # Vérification croisée : le gain du dernier jour de l'historique doit être
    # égal au gain total calculé à l'étape 2 avec les mêmes derniers cours.
    f = ecrire_csv(tmp_path, [
        "2024-01-01,ACHAT,AAA,Test,10,100,2",
        "2024-01-02,ACHAT,BBB,Test,5,50,1",
        "2024-01-03,DIVIDENDE,AAA,Test,0,12,0",
        "2024-01-04,VENTE,AAA,Test,3,130,2",
        "2024-01-05,ACHAT,AAA,Test,2,125,2",
    ])
    dates = ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08"]
    prix = cours_fictifs(dates, AAA=[100, 105, 110, 130, 125, 140], BBB=[50, 50, 48, 47, 52, 55])
    p = Portfolio(f)
    h = p.historique(prix)
    derniers = {"AAA": 140, "BBB": 55}
    assert h["gain"].iloc[-1] == pytest.approx(p.resume_valorise(derniers)["gain_total"])
