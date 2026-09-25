"""
profil.py — Profil de risque du client et adéquation du portefeuille.

Contexte réglementaire :
    Depuis la directive européenne MiFID II (2018), un conseiller doit évaluer
    le profil de son client AVANT de lui recommander un placement : ses
    connaissances, sa situation financière, ses objectifs et sa tolérance aux
    pertes. C'est le "test d'adéquation" (suitability).

Ce module :
    1. propose un questionnaire simplifié de 7 questions (0 à 4 points chacune) ;
    2. en déduit un profil : Sécuritaire, Prudent, Équilibré, Dynamique, Offensif ;
    3. calcule l'indicateur de risque SRI (échelle de 1 à 7 affichée sur les
       documents d'information des produits financiers, règlement PRIIPs) ;
    4. vérifie si le portefeuille est adapté au profil, et sinon propose
       une solution simple.
"""

from dataclasses import dataclass

# ----------------------------------------------------------------------
# 1. Le questionnaire : (question, [(réponse, points), ...])
# ----------------------------------------------------------------------
QUESTIONNAIRE = [
    ("Horizon de placement", [
        ("Moins de 2 ans", 0), ("2 à 5 ans", 1), ("5 à 8 ans", 2), ("8 à 15 ans", 3), ("Plus de 15 ans", 4)]),
    ("Objectif principal", [
        ("Préserver le capital", 0), ("Obtenir des revenus réguliers", 1), ("Croissance modérée", 2),
        ("Croissance du capital", 3), ("Rendement maximal", 4)]),
    ("Si vos placements baissaient de 20 % en 3 mois, vous…", [
        ("Vendez tout", 0), ("Vendez une partie", 1), ("Attendez sans rien faire", 2),
        ("Conservez sans inquiétude", 3), ("Rachetez à bon prix", 4)]),
    ("Perte maximale acceptable sur une année", [
        ("0 à 5 %", 0), ("5 à 10 %", 1), ("10 à 20 %", 2), ("20 à 30 %", 3), ("Plus de 30 %", 4)]),
    ("Connaissance et expérience des marchés actions", [
        ("Aucune", 0), ("Notions générales", 1), ("Placements en fonds (OPCVM, ETF)", 2),
        ("Investissement régulier en actions", 3), ("Expérience professionnelle", 4)]),
    ("Part de votre patrimoine financier placée ici", [
        ("Plus de 75 %", 0), ("50 à 75 %", 1), ("25 à 50 %", 2), ("10 à 25 %", 3), ("Moins de 10 %", 4)]),
    ("Épargne de précaution (3 à 6 mois de dépenses) disponible par ailleurs", [
        ("Non", 0), ("En partie", 2), ("Oui", 4)]),
]
INDEX_QUESTION_PERTE = 3        # la question sur la perte acceptable


# ----------------------------------------------------------------------
# 2. Les profils et leurs limites
# ----------------------------------------------------------------------
@dataclass
class Profil:
    nom: str
    score_min: int
    volatilite_max: float     # volatilité annuelle maximale
    drawdown_max: float       # pire baisse acceptable (positive)
    actions_max: float        # part maximale d'actions
    sri_max: int              # indicateur de risque maximal (1 à 7)
    description: str


PROFILS = [
    Profil("Sécuritaire", 0, 0.03, 0.05, 0.10, 2, "Priorité absolue à la préservation du capital."),
    Profil("Prudent", 7, 0.07, 0.12, 0.30, 3, "Recherche de régularité, faible tolérance aux baisses."),
    Profil("Équilibré", 13, 0.12, 0.20, 0.60, 4, "Compromis entre rendement et sécurité."),
    Profil("Dynamique", 19, 0.18, 0.30, 0.85, 5, "Recherche de performance, accepte des baisses marquées."),
    Profil("Offensif", 24, 0.30, 0.45, 1.00, 6, "Rendement maximal sur le long terme, forte tolérance au risque."),
]
NOMS_PROFILS = [p.nom for p in PROFILS]


def profil_par_nom(nom):
    return next(p for p in PROFILS if p.nom == nom)


def profil_depuis_reponses(indices_reponses):
    """Calcule le profil à partir des réponses (indice de la réponse choisie
    pour chaque question).

    Règle de prudence : la tolérance aux pertes PLAFONNE le profil. Un client
    qui n'accepte que 5 % de perte ne peut pas être "Dynamique", même avec un
    score total élevé (le critère le plus prudent l'emporte).
    """
    score = sum(QUESTIONNAIRE[q][1][r][1] for q, r in enumerate(indices_reponses))
    rang = max(i for i, p in enumerate(PROFILS) if score >= p.score_min)
    rang_plafond = indices_reponses[INDEX_QUESTION_PERTE]     # 0 à 4 -> même échelle que les profils
    plafonne = rang_plafond < rang
    return {
        "score": score,
        "score_max": sum(max(pts for _, pts in options) for _, options in QUESTIONNAIRE),
        "profil": PROFILS[min(rang, rang_plafond)],
        "profil_selon_score": PROFILS[rang],
        "plafonne_par_tolerance": plafonne,
    }


# ----------------------------------------------------------------------
# 3. L'indicateur de risque SRI (1 à 7)
# ----------------------------------------------------------------------
# Classes de risque de marché du règlement PRIIPs, selon la "volatilité
# équivalente à la VaR" (VEV). On l'approche ici par la volatilité annuelle.
SEUILS_SRI = [(0.005, 1), (0.05, 2), (0.12, 3), (0.20, 4), (0.30, 5), (0.80, 6)]


def indicateur_sri(volatilite):
    """Classe de risque de 1 (très faible) à 7 (très élevé)."""
    for seuil, classe in SEUILS_SRI:
        if volatilite < seuil:
            return classe
    return 7


# ----------------------------------------------------------------------
# 4. Test d'adéquation
# ----------------------------------------------------------------------
def part_actions(positions):
    """Part de la valeur investie en actions (colonne "classe" des positions).
    Sans information sur la classe d'actifs, tout est considéré comme actions."""
    if "classe" not in positions.columns or positions["valeur"].sum() <= 0:
        return 1.0
    valeurs = positions["valeur"]
    return float(valeurs[positions["classe"] == "Actions"].sum() / valeurs.sum())


def adequation(profil, volatilite, max_drawdown, part_actions=1.0):
    """Compare le risque du portefeuille aux limites du profil.

    Renvoie la liste des critères (avec leur statut) et, si le portefeuille
    est trop risqué, une proposition : la part à conserver en actions, le
    reste étant placé sans risque (fonds euros, monétaire). Mélanger un
    portefeuille de volatilité σ avec un actif sans risque divise la
    volatilité dans la même proportion : part = volatilité max / σ.
    """
    sri = indicateur_sri(volatilite)
    volatilite, max_drawdown = float(volatilite), abs(float(max_drawdown))
    criteres = [
        ("Volatilité annuelle", volatilite, profil.volatilite_max, bool(volatilite <= profil.volatilite_max)),
        ("Pire baisse historique", max_drawdown, profil.drawdown_max, bool(max_drawdown <= profil.drawdown_max)),
        ("Part d'actions", part_actions, profil.actions_max, bool(part_actions <= profil.actions_max + 1e-9)),
        ("Indicateur de risque (SRI)", sri, profil.sri_max, bool(sri <= profil.sri_max)),
    ]
    adapte = all(c[3] for c in criteres)
    part_risquee = 1.0 if adapte else min(1.0, profil.volatilite_max / volatilite,
                                          profil.actions_max / max(part_actions, 1e-9))
    return {
        "sri": sri,
        "criteres": criteres,
        "adapte": adapte,
        "part_risquee_conseillee": part_risquee,
        "part_sans_risque_conseillee": 1 - part_risquee,
    }
