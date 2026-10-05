"""
Tests de la base locale de titres : stockage des cours, fiche des titres,
mémoire des correspondances, et fonctionnement hors connexion.
"""

import os

import numpy as np
import pandas as pd

from src import base_titres as base

DATES = pd.bdate_range("2024-01-01", "2024-03-29")


def _cours(tickers, depart=100.0):
    return pd.DataFrame({t: depart + np.arange(len(DATES)) + i for i, t in enumerate(tickers)}, index=DATES)


def test_ajout_et_lecture_des_cours():
    base.ajouter_cours(_cours(["MC.PA", "AAPL", "EURUSD=X"]))
    lu = base.lire_cours(["AAPL", "MC.PA", "INCONNU"], debut="2024-02-01")
    assert list(lu.columns) == ["AAPL", "MC.PA"]
    assert lu.index[0] >= pd.Timestamp("2024-02-01")
    assert lu["MC.PA"].iloc[-1] == float(100 + len(DATES) - 1)
    assert base.derniere_date() == DATES[-1]


def test_mise_a_jour_des_cours():
    base.ajouter_cours(_cours(["MC.PA"]))
    nouveaux = pd.DataFrame({"MC.PA": [999.0]}, index=[pd.Timestamp("2024-04-01")])
    assert base.ajouter_cours(nouveaux) == 1
    assert base.lire_cours(["MC.PA"])["MC.PA"].iloc[-1] == 999.0
    assert base.ajouter_cours(nouveaux) == 0                        # rien de neuf : pas de réécriture


def test_fiche_des_titres_et_recherche_locale():
    base.ajouter_titres([
        {"ticker": "MC.PA", "nom": "LVMH Moët Hennessy Louis Vuitton SE", "isin": "FR0000121014", "pays": "France"},
        {"ticker": "MSFT", "nom": "Microsoft Corporation"},
    ])
    assert base.chercher_localement("FR0000121014")[0]["symbol"] == "MC.PA"
    assert base.chercher_localement("Microsoft")[0]["symbol"] == "MSFT"
    assert base.chercher_localement("LVMH")[0]["symbol"] == "MC.PA"
    assert base.chercher_localement("Société inconnue") == []


def test_memoire_des_correspondances():
    assert base.chercher_localement("MC FP Equity") == []
    base.memoriser("mc fp equity", "MC.PA", "LVMH")
    assert base.chercher_localement("MC FP EQUITY")[0]["symbol"] == "MC.PA"


def test_historique_hors_connexion_depuis_la_base(tmp_path):
    # Sans Internet et sans cache, les cours viennent de la base locale
    from src import market_data
    base.ajouter_cours(_cours(["MC.PA"]))

    def sans_internet(*a, **k):
        raise ConnectionError("pas d'Internet")
    original = market_data.telecharger_historique
    market_data.telecharger_historique = sans_internet
    try:
        histo, source = market_data.obtenir_historique(["MC.PA"], "2024-01-15",
                                                        chemin_cache=tmp_path / "cache_absent.csv")
    finally:
        market_data.telecharger_historique = original
    assert "MC.PA" in histo.columns and "injoignable" in source
