"""
Tests de la simulation de Monte-Carlo (étape 8).
Astuce : avec une volatilité nulle, il n'y a plus de hasard, et le résultat
se calcule à la main.
"""

import numpy as np
import pandas as pd
import pytest

from src import simulation


def test_sans_risque_croissance_exacte():
    # σ = 0 : 1 000 € à 6 % par an pendant 10 ans -> 1000 × e^(0,06 × 10)
    sim = simulation.simuler(1000, mu=0.06, sigma=0.0, annees=10, nb_simulations=100)
    assert sim["mediane"] == pytest.approx(1000 * np.exp(0.6), rel=1e-9)
    assert sim["p5"] == pytest.approx(sim["p95"], rel=1e-9)
    assert sim["proba_perte"] == 0


def test_versements_sans_rendement():
    # Rendement nul, sans risque : on retrouve exactement l'argent versé.
    sim = simulation.simuler(1000, mu=0.0, sigma=0.0, annees=5, versement_mensuel=100,
                             nb_simulations=50)
    assert sim["total_apporte"] == 1000 + 100 * 60
    assert sim["mediane"] == pytest.approx(7000)


def test_mediane_mouvement_brownien():
    # Théorie : la médiane de la valeur finale vaut V0 × e^((μ − σ²/2) × T)
    mu, sigma, annees = 0.07, 0.15, 10
    sim = simulation.simuler(1000, mu, sigma, annees=annees, nb_simulations=20000, graine=1)
    theorie = 1000 * np.exp((mu - sigma ** 2 / 2) * annees)
    assert sim["mediane"] == pytest.approx(theorie, rel=0.03)


def test_plus_de_risque_plus_de_dispersion():
    a = simulation.simuler(1000, 0.06, 0.10, annees=10, nb_simulations=5000)
    b = simulation.simuler(1000, 0.06, 0.25, annees=10, nb_simulations=5000)
    assert (b["p95"] - b["p5"]) > (a["p95"] - a["p5"])
    assert b["proba_perte"] > a["proba_perte"]


def test_bootstrap_rendement_constant():
    # Méthode historique avec un rendement quotidien constant de 0,1 % :
    # chaque mois = 21 jours à +0,1 %, donc aucune dispersion.
    rendements = pd.Series([0.001] * 100)
    sim = simulation.simuler(1000, mu=None, sigma=None, annees=1, methode="historique",
                             rendements_historiques=rendements, nb_simulations=200)
    assert sim["mediane"] == pytest.approx(1000 * 1.001 ** (21 * 12))
    assert sim["p5"] == pytest.approx(sim["p95"])


def test_probabilite_objectif():
    sim = simulation.simuler(1000, mu=0.05, sigma=0.0, annees=1, objectif=1000, nb_simulations=10)
    assert sim["proba_objectif"] == 1.0


def test_methode_inconnue_refusee():
    with pytest.raises(ValueError):
        simulation.simuler(1000, 0.05, 0.1, methode="magique")


# ----------------------------------------------------------------------
# Nuage de points par tranche de probabilité
# ----------------------------------------------------------------------
def test_classer_tranches():
    # Seuils : 5e = 10, 25e = 20, 75e = 30, 95e = 40
    valeurs = [5, 15, 25, 35, 45]
    assert list(simulation.classer_tranches(valeurs, 10, 20, 30, 40)) == [0, 1, 2, 3, 4]


def test_proportions_des_tranches():
    # Sur un grand nombre de scénarios, les tranches doivent contenir
    # environ 5 %, 20 %, 50 %, 20 % et 5 % des points.
    sim = simulation.simuler(1000, 0.06, 0.15, annees=5, nb_simulations=20000, graine=3)
    t = sim["trajectoires"].iloc[-1]
    tranches = simulation.classer_tranches(sim["valeurs_finales"], t["p5"], t["p25"], t["p75"], t["p95"])
    parts = np.bincount(tranches, minlength=5) / len(tranches)
    assert np.allclose(parts, [0.05, 0.20, 0.50, 0.20, 0.05], atol=0.01)


def test_points_nuage():
    sim = simulation.simuler(1000, 0.06, 0.15, annees=10, nb_simulations=1000)
    points = simulation.points_nuage(sim)
    # 10 ans, un relevé tous les 6 mois -> 20 dates × 400 scénarios de l'échantillon
    assert len(points) == 20 * simulation.TAILLE_ECHANTILLON
    assert set(points["tranche"].unique()) <= {0, 1, 2, 3, 4}
    assert sim["echantillon"].shape == (121, simulation.TAILLE_ECHANTILLON)
