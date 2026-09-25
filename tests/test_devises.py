"""
Tests de la conversion des devises (étape 8).
Rappel : "EURUSD=X" = nombre de dollars pour 1 euro, donc
         prix en euros = prix en dollars / taux.
"""

import pandas as pd
import pytest

from src import devises
from src.portfolio import Portfolio


def test_devise_par_suffixe():
    assert devises.devise_par_suffixe("MC.PA") == "EUR"
    assert devises.devise_par_suffixe("SAP.DE") == "EUR"
    assert devises.devise_par_suffixe("AAPL") == "USD"
    assert devises.devise_par_suffixe("ULVR.L") == "GBp"
    assert devises.devise_par_suffixe("^GSPC") == "USD"


def test_pence_convertis_en_livres():
    # Les actions de Londres sont cotées en pence : facteur 0,01
    assert devises.normaliser("GBp") == ("GBP", 0.01)
    assert devises.normaliser("USD") == ("USD", 1.0)


def test_conversion_cours_historiques():
    dates = pd.to_datetime(["2024-01-02", "2024-01-03"])
    prix = pd.DataFrame({"AAPL": [110.0, 120.0], "MC.PA": [700.0, 710.0]}, index=dates)
    taux = pd.DataFrame({"USD": [1.10, 1.20]}, index=dates)
    info = {"AAPL": ("USD", 1.0), "MC.PA": ("EUR", 1.0)}
    eur = devises.convertir_prix_historiques(prix, info, taux)
    assert list(eur["AAPL"]) == pytest.approx([100.0, 100.0])   # 110/1,10 et 120/1,20
    assert list(eur["MC.PA"]) == [700.0, 710.0]                 # déjà en euros


def test_taux_manquant_un_jour_ferie():
    # Pas de taux le 3 janvier : on prend le dernier connu (celui du 2)
    dates = pd.to_datetime(["2024-01-02", "2024-01-03"])
    prix = pd.DataFrame({"AAPL": [110.0, 110.0]}, index=dates)
    taux = pd.DataFrame({"USD": [1.10]}, index=dates[:1])
    eur = devises.convertir_prix_historiques(prix, {"AAPL": ("USD", 1.0)}, taux)
    assert eur["AAPL"].iloc[1] == pytest.approx(100.0)


def test_conversion_transactions_au_taux_du_jour():
    # Achat de 10 AAPL à 110 $ quand 1 € = 1,10 $ -> 100 € par action.
    # Les frais (en euros) ne sont pas convertis.
    transactions = pd.DataFrame({
        "date": pd.to_datetime(["2024-01-02"]), "type": ["ACHAT"], "ticker": ["AAPL"],
        "nom": ["Apple"], "quantite": [10], "prix": [110.0], "frais": [2.0],
    })
    taux = pd.DataFrame({"USD": [1.10]}, index=pd.to_datetime(["2024-01-02"]))
    t = devises.convertir_transactions(transactions, {"AAPL": ("USD", 1.0)}, taux)
    assert t["prix"].iloc[0] == pytest.approx(100.0)
    assert t["prix_devise"].iloc[0] == 110.0
    assert t["devise"].iloc[0] == "USD"
    # Le PRU en euros inclut les frais : (10 × 100 + 2) / 10 = 100,20 €
    assert Portfolio(t).positions.loc["AAPL", "pru"] == pytest.approx(100.2)


def test_conversion_cours_actuels():
    info = {"AAPL": ("USD", 1.0), "ULVR.L": ("GBP", 0.01), "MC.PA": ("EUR", 1.0)}
    eur = devises.convertir_cours({"AAPL": 125.0, "ULVR.L": 4250.0, "MC.PA": 600.0},
                                  info, {"USD": 1.25, "GBP": 0.85})
    assert eur["AAPL"] == pytest.approx(100.0)
    assert eur["ULVR.L"] == pytest.approx(50.0)     # 4 250 pence = 42,50 £ = 50 €
    assert eur["MC.PA"] == 600.0


def test_risque_de_change():
    # L'action ne bouge pas en dollars (100 $), mais le dollar baisse :
    # 1 € passe de 1,00 $ à 1,25 $ -> en euros, l'action perd 20 %.
    dates = pd.to_datetime(["2024-01-02", "2024-06-03"])
    prix = pd.DataFrame({"AAPL": [100.0, 100.0]}, index=dates)
    taux = pd.DataFrame({"USD": [1.00, 1.25]}, index=dates)
    eur = devises.convertir_prix_historiques(prix, {"AAPL": ("USD", 1.0)}, taux)
    assert eur["AAPL"].iloc[1] / eur["AAPL"].iloc[0] - 1 == pytest.approx(-0.20)
