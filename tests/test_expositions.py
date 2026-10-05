"""
Tests de l'analyse des expositions et de la diversification réelle :
ETF « éclatés » selon leur indice, devise réelle, concentration, blocs de
titres corrélés, ratio de diversification, diagnostic.
"""

import numpy as np
import pandas as pd
import pytest

from src import composition_etf as ce
from src import expositions as ex
from src import indices


def _positions(lignes):
    """lignes : (ticker, nom, classe, pays, region, secteur, devise, valeur, duration)."""
    p = pd.DataFrame(lignes, columns=["ticker", "nom", "classe", "pays", "region", "secteur", "devise", "valeur",
                                      "duration"]).set_index("ticker")
    p["poids_pct"] = p["valeur"] / p["valeur"].sum() * 100
    return p


def test_compositions_completes():
    for indice in ce.PAYS_PAR_INDICE:
        assert ce.pays_de(indice).sum() == pytest.approx(1.0)
        assert all(p in ce.PAYS for p in ce.pays_de(indice).index), indice
    for indice in ce.SECTEURS_PAR_INDICE:
        assert ce.secteurs_de(indice).sum() == pytest.approx(1.0)
    assert ce.pays_de("MSCI World")["États-Unis"] == pytest.approx(0.7294, abs=0.001)
    assert ce.indice_suivi("XYZ.PA", "Lyxor MSCI World UCITS ETF") == "MSCI World"
    assert ce.indice_suivi("XYZ.PA", "Amundi MSCI Emerging Markets") == "MSCI Emerging Markets"
    assert ce.est_couvert("iShares S&P 500 EUR Hedged")


def test_etf_monde_eclate_et_devise_reelle():
    pos = _positions([("CW8.PA", "Amundi MSCI World", "Actions", "Monde", "Monde (ETF)", "ETF diversifié", "EUR",
                       10_000, None),
                      ("MC.PA", "LVMH", "Actions", "France", "Europe", "Consommation discrétionnaire", "EUR",
                       10_000, None)])
    tr = ex.transparence(pos)
    assert tr["poids"].sum() == pytest.approx(1.0)
    pays = ex.repartition(tr, "pays", "Actions", normaliser=True)
    assert pays["États-Unis"] == pytest.approx(0.5 * 0.7294, abs=0.002)        # coté en euros, mais américain
    assert pays["France"] == pytest.approx(0.5 + 0.5 * ce.pays_de("MSCI World")["France"], abs=0.002)
    devises = ex.repartition(tr, "devise")
    assert devises["USD"] == pytest.approx(0.5 * 0.7294, abs=0.002)            # risque de change réel
    carte = ex.carte_pays(tr, pos)
    assert carte.iloc[0]["iso3"] == "FRA" and carte["poids"].sum() == pytest.approx(1.0)


def test_obligations_or_et_taux():
    pos = _positions([("EUNH.DE", "iShares Core € Govt Bond", "Obligations", "Zone euro", "Europe",
                       "Obligations d'État", "EUR", 6_000, 7.0),
                      ("4GLD.DE", "Xetra-Gold", "Or", "Allemagne", "Monde", "Or", "EUR", 1_000, None),
                      ("CW8.PA", "Amundi MSCI World", "Actions", "Monde", "Monde (ETF)", "ETF diversifié", "EUR",
                       3_000, None)])
    tr = ex.transparence(pos)
    hors = ex.part_hors_carte(tr)
    assert hors["Obligations"] == pytest.approx(0.6) and hors["Or"] == pytest.approx(0.1)
    tx = ex.taux(pos)
    assert tx["duration"] == pytest.approx(7.0)
    assert tx["perte_1pt_pct"] == pytest.approx(0.6 * 7.0 * 0.01)             # ≈ duration × 1 % × poids


def test_concentration_regle_5_10_40():
    pos = _positions([("MC.PA", "LVMH", "Actions", "France", "Europe", "Consommation discrétionnaire", "EUR",
                       5_000, None),
                      ("AI.PA", "Air Liquide", "Actions", "France", "Europe", "Matériaux", "EUR", 3_000, None),
                      ("CW8.PA", "Amundi MSCI World", "Actions", "Monde", "Monde (ETF)", "ETF diversifié", "EUR",
                       2_000, None)])
    tr = ex.transparence(pos)
    c = ex.concentration(pos, tr)
    assert c["plus_grosse_action"] == ("MC.PA", pytest.approx(0.5))
    assert c["actions_plus_5"] == pytest.approx(0.8)                           # l'ETF ne compte pas
    assert c["nb_effectif"] == pytest.approx(1 / (0.5 ** 2 + 0.3 ** 2 + 0.2 ** 2))
    constats = ex.diagnostic(pos, tr)
    assert any(k["dimension"] == "concentration" and k["niveau"] == "alerte" for k in constats)
    assert ex.synthese(constats)["geographie"] == "alerte"                     # 80 % France


def _rendements_deux_blocs(n=600, graine=1):
    alea = np.random.default_rng(graine)
    f1, f2 = alea.normal(0, 0.01, n), alea.normal(0, 0.01, n)
    r = {f"A{i}": f1 + alea.normal(0, 0.003, n) for i in range(3)}
    r.update({f"B{i}": f2 + alea.normal(0, 0.003, n) for i in range(3)})
    return pd.DataFrame(r)


def test_regroupement_et_blocs_correles():
    r = _rendements_deux_blocs()
    melange = r[["A0", "B0", "A1", "B1", "A2", "B2"]]
    ordre = ex.ordre_regroupement(melange.corr())
    blocs_ordre = ["".join(sorted(set(x[0] for x in ordre[:3]))), "".join(sorted(set(x[0] for x in ordre[3:])))]
    assert sorted(blocs_ordre) == ["A", "B"]                                   # les deux familles côte à côte
    poids = pd.Series(1 / 6, index=melange.columns)
    blocs, nb = ex.blocs_correles(melange.corr(), poids)
    assert nb == 2 and len(blocs) == 2
    assert blocs[0]["poids"] == pytest.approx(0.5) and blocs[0]["correlation"] > 0.8


def test_ratio_de_diversification():
    alea = np.random.default_rng(3)
    x = alea.normal(0, 0.01, 500)
    identiques = pd.DataFrame({"a": x, "b": x * 1.0})
    assert ex.ratio_diversification(identiques, pd.Series({"a": 0.5, "b": 0.5})) == pytest.approx(1.0)
    independants = pd.DataFrame({"a": x, "b": alea.normal(0, 0.01, 500)})
    assert ex.ratio_diversification(independants, pd.Series({"a": 0.5, "b": 0.5})) == pytest.approx(np.sqrt(2),
                                                                                                    abs=0.1)
    c = pd.DataFrame([[1, 0.5, 0], [0.5, 1, 0.2], [0, 0.2, 1]], index=list("abc"), columns=list("abc"))
    w = pd.Series({"a": 0.5, "b": 0.25, "c": 0.25})
    attendu = (2 * (0.5 * 0.25 * 0.5 + 0.5 * 0.25 * 0 + 0.25 * 0.25 * 0.2)) / (2 * (0.125 + 0.125 + 0.0625))
    assert ex.correlation_moyenne_ponderee(c, w) == pytest.approx(attendu)


def test_ecarts_indice_et_indices_composites():
    pos = _positions([("ESE.PA", "BNP Paribas Easy S&P 500", "Actions", "États-Unis", "États-Unis",
                       "ETF diversifié", "EUR", 1_000, None)])
    e = ex.ecarts_indice(ex.transparence(pos), indices.indice("CW8.PA"))
    assert e["pays"].loc["États-Unis", "ecart"] == pytest.approx(1 - ce.pays_de("MSCI World")["États-Unis"])
    jours = pd.bdate_range("2024-01-01", "2024-04-30")
    prix = pd.DataFrame({"A": np.linspace(100, 120, len(jours)), "B": np.full(len(jours), 50.0)}, index=jours)
    serie = indices.serie_composite(prix, {"A": 0.6, "B": 0.4})
    assert serie.iloc[0] == pytest.approx(100)
    # sur le premier mois, sans rééquilibrage : 60 × (cours A / cours initial A) + 40
    fin_janvier = serie.loc[:"2024-01-31"].index[-1]
    assert serie[fin_janvier] == pytest.approx(60 * prix.at[fin_janvier, "A"] / 100 + 40)
    assert indices.est_composite("MIXTE_60") and not indices.est_composite("CW8.PA")
    assert set(indices.tickers_a_telecharger("MIXTE_60")) >= {"CW8.PA", "DBXN.DE", "EUNH.DE"}
