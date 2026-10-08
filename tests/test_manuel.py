"""
Tests du manuel et de l'assistant « Poser une question » (src/manuel.py).

1. Le manuel est bien formé : chaque fiche a son identifiant unique, au moins 5 vraies
   formulations de questions, et des métadonnées valides (« aller », « chiffres »).
2. Chaque élément d'écran cité [[ainsi]] existe vraiment dans le logiciel (sinon le manuel
   parlerait d'un bouton qui n'existe plus).
3. Banc d'essai : tests/questions_assistant.csv contient des questions réelles, écrites à
   part des fiches, avec la ou les fiches qui y répondent. L'assistant doit trouver la bonne
   fiche en premier dans au moins 85 % des cas, et parmi les 3 premières dans au moins 95 %.
"""

import ast
import csv
from pathlib import Path

from src import manuel
from src.vues_manuel import CHIFFRES

RACINE = Path(__file__).resolve().parent.parent
ESPACES_ONGLETS = {
    "Analyse du portefeuille": {"Vue d'ensemble", "Positions", "Performance", "Risque", "Expositions",
                                "Optimisation", "Projection", "Transactions"},
    "Conseil patrimonial": {"Fiscalité", "Stress tests"},
    "Gestion d'actifs": {"Attribution de performance", "Budget de risque", "Backtest de stratégies"},
    "Manuel et aide": set(),
}


def _fiches():
    return manuel.toutes_les_fiches(manuel.charger("fr"))


def _chaines_du_code():
    """Toutes les chaînes de caractères écrites dans app.py et src/*.py."""
    chaines = set()
    for fichier in [RACINE / "app.py", *sorted((RACINE / "src").glob("*.py"))]:
        for noeud in ast.walk(ast.parse(fichier.read_text(encoding="utf-8"))):
            if isinstance(noeud, ast.Constant) and isinstance(noeud.value, str):
                chaines.add(noeud.value)
    return chaines


def test_manuel_bien_forme():
    chapitres = manuel.charger("fr")
    fiches = manuel.toutes_les_fiches(chapitres)
    assert len(chapitres) >= 10 and len(fiches) >= 200
    identifiants = [f.ident for f in fiches]
    assert len(identifiants) == len(set(identifiants)), "identifiants de fiches en double"
    for f in fiches:
        assert len(f.questions) >= 5, f"{f.ident} : moins de 5 formulations de questions"
        assert f.texte.strip(), f"{f.ident} : fiche vide"
        if f.aller:
            espace, onglet = manuel.destination(f)
            assert espace in ESPACES_ONGLETS, f"{f.ident} : espace inconnu {espace}"
            assert not onglet or onglet in ESPACES_ONGLETS[espace], f"{f.ident} : onglet inconnu {onglet}"
        for cle in f.chiffres:
            assert cle in CHIFFRES, f"{f.ident} : chiffre inconnu {cle}"


def test_elements_d_ecran_cites_existent():
    chaines = _chaines_du_code()
    absents = {libelle: fiches for libelle, fiches in manuel.elements_ecran(manuel.charger("fr")).items()
               if libelle not in chaines}
    assert not absents, f"éléments d'écran introuvables dans le code : {absents}"


def _banc():
    with (RACINE / "tests" / "questions_assistant.csv").open(encoding="utf-8") as f:
        return [(l["question"], set(l["fiches_acceptees"].split(","))) for l in csv.DictReader(f, delimiter=";")]


def test_banc_d_essai_de_l_assistant():
    index = manuel.index("fr")
    connues = {f.ident for f in index.fiches}
    banc = _banc()
    assert len(banc) >= 100
    premier = trois = 0
    for question, attendues in banc:
        assert attendues <= connues, f"fiche inconnue dans le banc d'essai : {attendues - connues}"
        trouvees = [f.ident for _, f in index.chercher(question, 3)]
        premier += bool(trouvees) and trouvees[0] in attendues
        trois += bool(attendues & set(trouvees))
    assert premier / len(banc) >= 0.85, f"bonne fiche en premier : {premier / len(banc):.0%}"
    assert trois / len(banc) >= 0.95, f"bonne fiche parmi les 3 premières : {trois / len(banc):.0%}"


def test_fautes_de_frappe_et_hors_sujet():
    """Une faute de frappe est corrigée ; une question sans rapport ne reçoit pas de « réponse »."""
    assert manuel.repondre("comment suprimer une operaton")["reponse"].ident == "import-modifier-supprimer"
    assert manuel.repondre("mot de pase oublié")["reponse"].ident == "compte-mot-de-passe-oublie"
    assert manuel.repondre("meteo demain")["reponse"] is None


def test_racines_et_synonymes():
    assert manuel.mots("supprimer une opération") == manuel.mots("effacer les opérations")
    assert manuel.mots("mot de passe") == manuel.mots("mdp")


# ----------------------------------------------------------------------
# Manuel anglais : mêmes fiches, libellés d'écran anglais existants, banc d'essai anglais
# ----------------------------------------------------------------------
def test_manuel_anglais():
    from src.traductions import DONNEES, TEXTES
    fr = {f.ident for f in _fiches()}
    en = manuel.toutes_les_fiches(manuel.charger("en"))
    assert {f.ident for f in en} == fr, "le manuel anglais doit avoir les mêmes fiches que le français"
    assert all(len(f.questions) >= 5 for f in en)
    connus = set(TEXTES.values()) | set(DONNEES.values()) | _chaines_du_code()
    absents = {l: f for l, f in manuel.elements_ecran(manuel.charger("en")).items() if l not in connus}
    assert not absents, f"libellés anglais introuvables : {absents}"


def test_banc_d_essai_anglais():
    index = manuel.index("en")
    with (RACINE / "tests" / "questions_assistant_en.csv").open(encoding="utf-8") as f:
        banc = [(l["question"], set(l["fiches_acceptees"].split(","))) for l in csv.DictReader(f, delimiter=";")]
    bons = sum(1 for q, ok in banc if (r := index.chercher(q, 1)) and r[0][1].ident in ok)
    assert bons / len(banc) >= 0.85, f"bonne fiche en premier (anglais) : {bons / len(banc):.0%}"


# ----------------------------------------------------------------------
# Bulle d'aide : résumé court de chaque fiche
# ----------------------------------------------------------------------
def test_resume_des_fiches_pour_la_bulle():
    for fiche in _fiches():
        resume, _ = manuel.resume_fiche(fiche)
        assert resume.strip(), f"{fiche.ident} : résumé vide"
        assert resume.count("```") % 2 == 0, f"{fiche.ident} : bloc de code coupé"
        assert "[[" not in resume
