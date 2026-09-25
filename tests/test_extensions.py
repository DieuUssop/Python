"""
Tests des extensions (étape 10) : profil client, fiscalité, stress tests,
attribution de performance, budget de risque, backtest.
Chaque test utilise un cas dont le résultat se calcule à la main.
"""

import numpy as np
import pandas as pd
import pytest

from src import attribution, backtest, budget_risque, fiscalite, profil, stress


# ----------------------------------------------------------------------
# Profil client
# ----------------------------------------------------------------------
def test_profil_selon_score():
    # Réponses maximales partout -> score maximal -> Offensif
    maxi = [len(options) - 1 for _, options in profil.QUESTIONNAIRE]
    res = profil.profil_depuis_reponses(maxi)
    assert res["score"] == res["score_max"] == 28
    assert res["profil"].nom == "Offensif"


def test_tolerance_aux_pertes_plafonne_le_profil():
    # Score élevé mais perte acceptable de 0 à 5 % -> plafonné à "Sécuritaire"
    reponses = [len(options) - 1 for _, options in profil.QUESTIONNAIRE]
    reponses[profil.INDEX_QUESTION_PERTE] = 0
    res = profil.profil_depuis_reponses(reponses)
    assert res["profil"].nom == "Sécuritaire"
    assert res["plafonne_par_tolerance"]


def test_indicateur_sri():
    assert profil.indicateur_sri(0.003) == 1
    assert profil.indicateur_sri(0.08) == 3
    assert profil.indicateur_sri(0.15) == 4
    assert profil.indicateur_sri(0.25) == 5
    assert profil.indicateur_sri(0.90) == 7


def test_adequation_et_part_sans_risque():
    # Profil Équilibré : volatilité max 12 %. Portefeuille à 16 % de volatilité
    # -> garder 12 / 16 = 75 % en actions, 25 % sans risque.
    res = profil.adequation(profil.profil_par_nom("Équilibré"), volatilite=0.16,
                            max_drawdown=-0.15, part_actions=0.5)
    assert not res["adapte"]
    assert res["part_risquee_conseillee"] == pytest.approx(0.75)


# ----------------------------------------------------------------------
# Fiscalité (taux 2026)
# ----------------------------------------------------------------------
def test_cto_flat_tax():
    # 10 000 € de gain sur un compte-titres -> 31,4 % = 3 140 €
    assert fiscalite.impot_sortie(10_000, 2, "CTO")["total"] == pytest.approx(3140)


def test_cto_moins_value_n_efface_pas_les_dividendes():
    # Moins-value de 2 000 € et 1 000 € de dividendes : gain total −1 000 €,
    # mais les dividendes restent imposés -> 314 €
    assert fiscalite.impot_sortie(-1000, 2, "CTO", dividendes=1000)["total"] == pytest.approx(314)


def test_pea_avant_et_apres_5_ans():
    assert fiscalite.impot_sortie(10_000, 3, "PEA")["total"] == pytest.approx(3140)
    assert fiscalite.impot_sortie(10_000, 6, "PEA")["total"] == pytest.approx(1860)   # 18,6 % seulement


def test_assurance_vie_apres_8_ans():
    # 10 000 € de gain : 17,2 % de prélèvements sociaux = 1 720 €
    # + 7,5 % sur (10 000 − 4 600) = 405 € -> 2 125 €
    assert fiscalite.impot_sortie(10_000, 9, "Assurance-vie")["total"] == pytest.approx(2125)
    # Couple : abattement de 9 200 € -> 1 720 + 7,5 % × 800 = 1 780 €
    assert fiscalite.impot_sortie(10_000, 9, "Assurance-vie", situation="couple")["total"] == pytest.approx(1780)


def test_eligibilite_pea():
    positions = pd.DataFrame({"valeur": [600, 400], "pays": ["France", "États-Unis"]},
                             index=["MC.PA", "AAPL"])
    part, exclus = fiscalite.eligibilite_pea(positions)
    assert part == pytest.approx(0.6)
    assert exclus == ["AAPL"]


# ----------------------------------------------------------------------
# Stress tests
# ----------------------------------------------------------------------
def test_stress_historique_avec_proxy():
    # A a une vraie histoire (−40 %). B n'existait pas : on prend l'indice de sa région (−20 %).
    dates = pd.to_datetime(["2008-08-15", "2008-09-01", "2009-03-09", "2024-01-02"])
    prix = pd.DataFrame({
        "A": [100, 100, 60, 90],
        "B": [np.nan, np.nan, np.nan, 50],
        "^GSPC": [1000, 1000, 800, 1500],
    }, index=dates)
    positions = pd.DataFrame({"nom": ["A", "B"], "region": ["Europe", "États-Unis"],
                              "poids_pct": [50.0, 50.0], "valeur": [5000, 5000]}, index=["A", "B"])
    resume, _ = stress.scenarios_historiques(positions, prix)
    crise = resume.iloc[0]
    assert crise["variation"] == pytest.approx(0.5 * -0.40 + 0.5 * -0.20)
    assert crise["part_proxy"] == pytest.approx(0.5)


def test_stress_hypothetique_beta():
    positions = pd.DataFrame({"valeur": [1000.0], "devise": ["EUR"]}, index=["X"])
    res = stress.scenarios_hypothetiques(positions, beta=1.2, chocs_actions=(-0.20,))
    assert res.iloc[0]["variation"] == pytest.approx(-0.24)


# ----------------------------------------------------------------------
# Attribution de performance
# ----------------------------------------------------------------------
def test_brinson_somme_des_effets_egale_ecart():
    wp = pd.Series({"US": 0.7, "Europe": 0.3})
    rp = pd.Series({"US": 0.05, "Europe": 0.02})
    wb = pd.Series({"US": 0.6, "Europe": 0.4})
    rb = pd.Series({"US": 0.04, "Europe": 0.01})
    effets, Rp, Rb = attribution.brinson_fachler(wp, rp, wb, rb)
    assert Rp == pytest.approx(0.7 * 0.05 + 0.3 * 0.02)
    assert Rb == pytest.approx(0.6 * 0.04 + 0.4 * 0.01)
    assert effets.to_numpy().sum() == pytest.approx(Rp - Rb)
    # Allocation US : (0,7 − 0,6) × (0,04 − 0,028) = 0,0012
    assert effets.loc["US", "allocation"] == pytest.approx(0.0012)
    # Sélection Europe : 0,4 × (0,02 − 0,01) = 0,004
    assert effets.loc["Europe", "selection"] == pytest.approx(0.004)


def test_attribution_mensuelle_portefeuille_identique_a_l_indice():
    # Le portefeuille détient exactement l'indice : aucun effet.
    dates = pd.bdate_range("2024-01-01", "2024-04-30")
    indice = pd.Series(np.linspace(100, 120, len(dates)), index=dates)
    valeurs = pd.DataFrame({"T": 1000 * indice / 100}, index=dates)
    prix = pd.DataFrame({"T": indice}, index=dates)
    res = attribution.attribution_mensuelle(valeurs, prix, {"T": "US"},
                                            pd.DataFrame({"US": indice}), poids_indice={"US": 1.0})
    assert res["somme_effets"] == pytest.approx(0, abs=1e-12)
    assert res["Rp"] == pytest.approx(res["Rb"])


# ----------------------------------------------------------------------
# Budget de risque
# ----------------------------------------------------------------------
def test_contributions_somme_egale_volatilite():
    cov = np.array([[0.04, 0.01], [0.01, 0.09]])
    c = budget_risque.contributions([0.6, 0.4], cov)
    assert c["contribution"].sum() == pytest.approx(c["volatilite"])
    assert c["part"].sum() == pytest.approx(1.0)


def test_parite_des_risques_titres_independants():
    # Titres indépendants : poids proportionnels à 1 / volatilité
    vols = np.array([0.10, 0.20, 0.40])
    w = budget_risque.parite_des_risques(np.diag(vols ** 2))
    attendu = (1 / vols) / (1 / vols).sum()
    assert np.allclose(w, attendu, atol=1e-5)
    parts = budget_risque.contributions(w, np.diag(vols ** 2))["part"]
    assert np.allclose(parts, 1 / 3, atol=1e-5)


# ----------------------------------------------------------------------
# Backtest
# ----------------------------------------------------------------------
def test_achat_conservation():
    # A double, B ne bouge pas, 50/50 sans frais -> 100 devient 150
    dates = pd.bdate_range("2024-01-01", periods=3)
    prix = pd.DataFrame({"A": [10, 15, 20], "B": [10, 10, 10]}, index=dates)
    valeurs, _ = backtest.simuler_strategie(prix, pd.Series({"A": 0.5, "B": 0.5}), None, frais=0.0)
    assert valeurs.iloc[-1] == pytest.approx(150)


def test_reequilibrage_rachete_ce_qui_baisse():
    # A fait +100 % puis −50 % ; B ne bouge pas.
    # Sans rééquilibrage : on revient à 100. Avec rééquilibrage en milieu de période :
    # 150 -> 75/75 -> A perd 50 % -> 37,5 + 75 = 112,5
    dates = pd.to_datetime(["2024-01-31", "2024-02-01", "2024-02-02"])
    prix = pd.DataFrame({"A": [10, 20, 10], "B": [10, 10, 10]}, index=dates)
    poids = pd.Series({"A": 0.5, "B": 0.5})
    sans, _ = backtest.simuler_strategie(prix, poids, None, frais=0.0)
    avec, _ = backtest.simuler_strategie(prix, poids, "M", frais=0.0)   # rééquilibre le 1er février
    assert sans.iloc[-1] == pytest.approx(100)
    assert avec.iloc[-1] == pytest.approx(112.5)


def test_dca_prix_constant():
    # Prix constant et taux nul : investir en une fois ou progressivement revient au même.
    dates = pd.bdate_range("2024-01-01", "2024-12-31")
    prix = pd.DataFrame({"A": 50.0, "B": 20.0}, index=dates)
    _, resume = backtest.comparer_dca(prix, pd.Series({"A": 0.5, "B": 0.5}), capital=1200,
                                      nb_mois=12, frais=0.0)
    assert resume["valeur_finale"].iloc[0] == pytest.approx(1200)
    assert resume["valeur_finale"].iloc[1] == pytest.approx(1200)


def test_carino_la_somme_des_effets_egale_l_ecart_compose():
    # Portefeuille 100 % US qui bat l'indice ; indice 50 % US / 50 % Europe.
    # Sur plusieurs mois, les effets reliés doivent sommer exactement à Rp − Rb (composés).
    dates = pd.bdate_range("2024-01-01", "2024-06-28")
    us = pd.Series(100 * 1.002 ** np.arange(len(dates)), index=dates)
    eu = pd.Series(100 * 0.999 ** np.arange(len(dates)), index=dates)
    titre = us * (1 + 0.0005 * np.arange(len(dates)))           # le titre fait mieux que son indice
    valeurs = pd.DataFrame({"T": titre}, index=dates)
    res = attribution.attribution_mensuelle(valeurs, pd.DataFrame({"T": titre}), {"T": "US"},
                                            pd.DataFrame({"US": us, "Europe": eu}),
                                            poids_indice={"US": 0.5, "Europe": 0.5})
    assert res["somme_effets"] == pytest.approx(res["Rp"] - res["Rb"], rel=1e-9)
    assert res["effets"]["allocation"] > 0      # surpondérer les US (qui montent) a rapporté
    assert res["effets"]["selection"] > 0       # le titre a battu son indice
