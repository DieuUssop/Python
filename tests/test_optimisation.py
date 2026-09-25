"""
Tests de l'optimisation de Markowitz (étape 7).
Dans les cas simples, les solutions exactes se calculent à la main :
on vérifie que l'optimiseur numérique les retrouve.
"""

import numpy as np
import pandas as pd
import pytest

from src import optimisation as opt


def parametres(mu, vols, correlation=0.0):
    """Fabrique μ et Σ pour des titres de volatilités données."""
    noms = [f"T{i}" for i in range(len(mu))]
    vols = np.array(vols)
    corr = np.full((len(mu), len(mu)), correlation)
    np.fill_diagonal(corr, 1.0)
    cov = np.outer(vols, vols) * corr
    return pd.Series(mu, index=noms), pd.DataFrame(cov, index=noms, columns=noms)


def test_performance():
    # 50/50 entre deux titres indépendants à 20 % de volatilité :
    # volatilité = √(0,25 × 0,04 + 0,25 × 0,04) = 0,2 / √2 ≈ 14,1 %
    mu, cov = parametres([0.08, 0.06], [0.2, 0.2])
    r, v = opt.performance([0.5, 0.5], mu, cov)
    assert r == pytest.approx(0.07)
    assert v == pytest.approx(0.2 / np.sqrt(2))


def test_variance_minimale_deux_titres():
    # Formule exacte (2 titres) : w1 = (σ2² − σ12) / (σ1² + σ2² − 2 σ12)
    mu, cov = parametres([0.08, 0.05], [0.25, 0.15], correlation=0.3)
    s1, s2, s12 = cov.iloc[0, 0], cov.iloc[1, 1], cov.iloc[0, 1]
    w1 = (s2 - s12) / (s1 + s2 - 2 * s12)
    w = opt.variance_minimale(mu, cov)
    assert w[0] == pytest.approx(w1, abs=1e-4)
    assert w.sum() == pytest.approx(1)


def test_diversification_reduit_le_risque():
    # Le portefeuille de variance minimale est moins risqué que chaque titre seul.
    mu, cov = parametres([0.08, 0.06, 0.07], [0.2, 0.25, 0.3], correlation=0.2)
    w = opt.variance_minimale(mu, cov)
    _, v = opt.performance(w, mu, cov)
    assert v < np.sqrt(np.diag(cov)).min()


def test_sharpe_maximal_titres_independants():
    # Titres non corrélés : poids optimaux proportionnels à (μ − rf) / σ²
    rf = 0.02
    mu, cov = parametres([0.10, 0.06, 0.08], [0.20, 0.10, 0.25])
    attendu = (mu - rf) / np.diag(cov)
    attendu = attendu / attendu.sum()
    w = opt.sharpe_maximal(mu, cov, rf)
    assert np.allclose(w, attendu.to_numpy(), atol=1e-3)


def test_poids_maximal_respecte():
    mu, cov = parametres([0.20, 0.05, 0.06, 0.07], [0.2, 0.2, 0.2, 0.2])
    w = opt.sharpe_maximal(mu, cov, 0.02, poids_max=0.30)
    assert w.max() <= 0.30 + 1e-6
    assert w.min() >= -1e-9
    assert w.sum() == pytest.approx(1)


def test_poids_maximal_impossible():
    # 3 titres à 30 % maximum = 90 % : impossible d'investir 100 %
    mu, cov = parametres([0.08, 0.06, 0.07], [0.2, 0.2, 0.2])
    with pytest.raises(ValueError):
        opt.variance_minimale(mu, cov, poids_max=0.30)


def test_frontiere_efficiente():
    mu, cov = parametres([0.10, 0.06, 0.08], [0.25, 0.12, 0.18], correlation=0.3)
    f = opt.frontiere_efficiente(mu, cov, nb_points=15)
    # Sur la frontière efficiente, plus de rendement = plus de risque.
    assert (f["volatilite"].diff().dropna() >= -1e-6).all()
    # Aucun portefeuille aléatoire n'est "au-dessus" de la frontière :
    # à rendement égal, la frontière est toujours au moins aussi peu risquée.
    alea = opt.portefeuilles_aleatoires(mu, cov, 0.02, nombre=2000)
    dans_la_zone = alea[(alea["rendement"] >= f["rendement"].min()) &
                        (alea["rendement"] <= f["rendement"].max())]
    vol_frontiere = np.interp(dans_la_zone["rendement"], f["rendement"], f["volatilite"])
    assert (dans_la_zone["volatilite"].to_numpy() >= vol_frontiere - 1e-3).all()
