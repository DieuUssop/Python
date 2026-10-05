"""
Réglages communs des tests : la base locale de titres et les comptes sont
créés dans un dossier temporaire, pour ne jamais toucher aux vraies données
du projet (data/base, data/comptes).
"""

import os
import shutil
import tempfile

DOSSIER_TEST = tempfile.mkdtemp(prefix="portfolio_tests_")
os.environ["PORTFOLIO_BASE"] = os.path.join(DOSSIER_TEST, "base")
os.environ["PORTFOLIO_COMPTES"] = os.path.join(DOSSIER_TEST, "comptes")
os.environ["PORTFOLIO_ITERATIONS"] = "2000"      # tests rapides (l'application en utilise 600 000)

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def dossiers_vides():
    """Chaque test démarre avec une base et des comptes vides."""
    for sous_dossier in ("base", "comptes"):
        shutil.rmtree(os.path.join(DOSSIER_TEST, sous_dossier), ignore_errors=True)
    yield
