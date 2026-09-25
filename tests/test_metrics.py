"""
Tests des indicateurs de performance et de risque (étape 4).
Chaque test utilise un cas simple dont on connaît le résultat à la main.
"""

import numpy as np
import pandas as pd
import pytest

from src import metrics


def histo_fictif(dates, valeurs, flux):
    """Fabrique un petit "historique" comme celui de Portfolio.historique()."""
    h = pd.DataFrame({"valeur": valeurs, "flux": flux}, index=pd.to_datetime(dates))
    h["apports_nets"] = h["flux"].cumsum()
    h["gain"] = h["valeur"] - h["apports_nets"]
    return h


def test_rendements_neutralisent_les_flux():
    # J1 : achat 10 titres à 100 € + 5 € de frais, cours 100 -> r = 1000/1005 − 1
    # J2 : dividende de 20 € (flux −20), cours inchangé   -> r = (1000 + 20)/1000 − 1 = +2 %
    # J3 : vente de 4 titres à 120 € (flux −480), cours 100 -> 120
    #                                                       -> r = (720 + 480)/1000 − 1 = +20 %
    h = histo_fictif(["2024-01-01", "2024-01-02", "2024-01-03"],
                     [1000, 1000, 720], [1005, -20, -480])
    r = metrics.rendements_journaliers(h)
    assert r.iloc[0] == pytest.approx(1000 / 1005 - 1)
    assert r.iloc[1] == pytest.approx(0.02)
    assert r.iloc[2] == pytest.approx(0.20)


def test_twr_independant_des_apports():
    # Le cours fait +10 % le 2e jour et +10 % le 3e jour.
    # Le 2e jour, on rachète pour 5 000 € au cours du jour.
    # TWR = 1,1 × 1,1 − 1 = 21 %, quel que soit le montant apporté.
    # (Valeurs : J1 = 1000 ; J2 = 1100 + 5000 = 6100 ; J3 = 6100 × 1,1 = 6710)
    h = histo_fictif(["2024-01-01", "2024-01-02", "2024-01-03"],
                     [1000, 6100, 6710], [1000, 5000, 0])
    r = metrics.rendements_journaliers(h)
    # 1er jour : achat au cours du jour -> 0 %
    assert metrics.twr(r) == pytest.approx(0.21)


def test_annualisation():
    # +21 % en 730 jours (2 ans) -> +10 % par an
    assert metrics.annualiser(0.21, "2024-01-01", "2025-12-31") == pytest.approx(0.10)


def test_tri_simple():
    # On investit 1000 €, un an plus tard le portefeuille vaut 1100 € -> TRI = 10 %
    h = histo_fictif(["2024-01-01", "2024-12-31"], [1000, 1100], [1000, 0])
    assert metrics.tri(h) == pytest.approx(0.10, abs=1e-6)


def test_volatilite():
    # Rendements +1 %, −1 %, +1 %, −1 % : écart-type (échantillon) = 0,011547
    r = pd.Series([0.01, -0.01, 0.01, -0.01])
    attendu = np.std([0.01, -0.01, 0.01, -0.01], ddof=1) * np.sqrt(252)
    assert metrics.volatilite_annualisee(r) == pytest.approx(attendu)


def test_max_drawdown():
    # 100 -> 120 -> 90 -> 130 : pire baisse = 90 / 120 − 1 = −25 %
    dates = pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"])
    indice = pd.Series([100, 120, 90, 130], index=dates)
    dd = metrics.max_drawdown(indice)
    assert dd["max_drawdown"] == pytest.approx(-0.25)
    assert dd["date_sommet"] == dates[1]
    assert dd["date_creux"] == dates[2]
    assert dd["date_recuperation"] == dates[3]


def test_drawdown_non_recupere():
    dates = pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"])
    dd = metrics.max_drawdown(pd.Series([100, 80, 90], index=dates))
    assert dd["max_drawdown"] == pytest.approx(-0.20)
    assert dd["date_recuperation"] is None


def test_rendements_annuels():
    # +10 % en 2024, puis +10 % et −10 % en 2025 -> 2025 : 1,1 × 0,9 − 1 = −1 %
    r = pd.Series([0.10, 0.10, -0.10],
                  index=pd.to_datetime(["2024-06-01", "2025-03-01", "2025-09-01"]))
    annuels = metrics.rendements_annuels(r)
    assert annuels[2024] == pytest.approx(0.10)
    assert annuels[2025] == pytest.approx(-0.01)


# ----------------------------------------------------------------------
# Étape 5 : indicateurs avancés
# ----------------------------------------------------------------------
def serie(valeurs):
    """Petite série de rendements datée (jours ouvrés à partir du 1er janvier 2024)."""
    return pd.Series(valeurs, index=pd.bdate_range("2024-01-01", periods=len(valeurs)))


def test_sharpe():
    # Taux sans risque 0 ; rendements 2 %, 0 %, 2 %, 0 % -> moyenne 1 %
    r = serie([0.02, 0.0, 0.02, 0.0])
    ecart_type = np.std([0.02, 0.0, 0.02, 0.0], ddof=1)
    attendu = 0.01 * 252 / (ecart_type * np.sqrt(252))
    assert metrics.ratio_sharpe(r, 0.0) == pytest.approx(attendu)


def test_sortino():
    # Rendements 2 %, −1 %, 2 %, −1 % ; moyenne 0,5 %
    # Semi-déviation : √((0,01² + 0,01²) / 4) = 0,007071 par jour
    r = serie([0.02, -0.01, 0.02, -0.01])
    attendu = 0.005 * 252 / (np.sqrt(0.0002 / 4) * np.sqrt(252))
    assert metrics.ratio_sortino(r, 0.0) == pytest.approx(attendu)


def test_beta_deux_fois_le_marche():
    # Le portefeuille fait exactement 2 × l'indice -> bêta = 2, alpha = 0
    rb = serie([0.01, -0.02, 0.015, 0.005, -0.01])
    beta, alpha = metrics.beta_alpha(2 * rb, rb, 0.0)
    assert beta == pytest.approx(2)
    assert alpha == pytest.approx(0, abs=1e-12)


def test_alpha_positif():
    # Le portefeuille fait l'indice + 0,01 % chaque jour -> bêta 1, alpha 0,01 % × 252
    rb = serie([0.01, -0.02, 0.015, 0.005, -0.01])
    beta, alpha = metrics.beta_alpha(rb + 0.0001, rb, 0.0)
    assert beta == pytest.approx(1)
    assert alpha == pytest.approx(0.0001 * 252)


def test_tracking_error():
    # Écart avec l'indice : +0,1 %, −0,1 %, +0,1 %, −0,1 %
    rb = serie([0.01, -0.02, 0.015, 0.005])
    ecarts = np.array([0.001, -0.001, 0.001, -0.001])
    te, _ = metrics.tracking_error(rb + ecarts, rb)
    assert te == pytest.approx(np.std(ecarts, ddof=1) * np.sqrt(252))


def test_var_historique_et_cvar():
    # 101 rendements de −5 % à +5 % par pas de 0,1 %.
    # Le 5e percentile est −4,5 % -> VaR = 4,5 %.
    # Les jours au-delà : −5 %, −4,9 %, ..., −4,5 % -> perte moyenne 4,75 % = CVaR.
    r = serie(np.arange(-50, 51) / 1000)
    res = metrics.var_cvar(r, 0.95)
    assert res["var_historique"] == pytest.approx(0.045)
    assert res["cvar"] == pytest.approx(0.0475)


def test_var_parametrique():
    # Moyenne 0, écart-type σ -> VaR 95 % = 1,645 × σ
    r = serie([0.01, -0.01, 0.01, -0.01])
    sigma = np.std([0.01, -0.01, 0.01, -0.01], ddof=1)
    assert metrics.var_cvar(r, 0.95)["var_parametrique"] == pytest.approx(1.6448536 * sigma, rel=1e-6)


def test_correlations():
    # B vaut toujours 2 × A -> mêmes rendements -> corrélation +1
    dates = pd.bdate_range("2024-01-01", periods=5)
    prix = pd.DataFrame({"A": [10, 11, 10.5, 12, 11.8]}, index=dates)
    prix["B"] = 2 * prix["A"]
    m = metrics.matrice_correlation(prix, ["A", "B"])
    assert m.loc["A", "B"] == pytest.approx(1)
    assert m.loc["A", "A"] == pytest.approx(1)


def test_rendements_indice_jour_ferie():
    # L'indice n'a pas coté le 2e jour : on garde le cours de la veille (rendement 0)
    calendrier = pd.bdate_range("2024-01-01", periods=3)
    prix = pd.Series([100, 110], index=[calendrier[0], calendrier[2]])
    r = metrics.rendements_indice(prix, calendrier)
    assert r.iloc[1] == pytest.approx(0)
    assert r.iloc[2] == pytest.approx(0.10)
