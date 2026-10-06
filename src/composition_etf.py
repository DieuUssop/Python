"""
composition_etf.py — Ce que contient VRAIMENT un ETF (analyse « en transparence »).

Un ETF MSCI World est enregistré comme un seul titre, coté à Paris en euros.
Mais il contient environ 1 400 actions de 23 pays, dont près de 73 % aux
États-Unis : son risque géographique, sectoriel et de change est celui de ces
actions, pas celui d'un titre français. Ce module donne, pour chaque grand
indice, sa répartition approximative par pays et par secteur, et reconnaît
l'indice suivi par chaque ETF.

SOURCES ET DATES (approximations, à mettre à jour une fois par an) :
    - MSCI World, ACWI, Emerging Markets, Europe : fiches MSCI au 30/09/2026
      (5 premiers pays et secteurs) ; pays suivants : ordres de grandeur
      habituels de l'indice, ramenés au total « autres pays » de la fiche ;
    - S&P 500, Nasdaq-100, Euro Stoxx 50, CAC 40, DAX, Russell 2000, emprunts
      d'État et obligations d'entreprises de la zone euro : ordres de grandeur
      2025-2026 (fiches des émetteurs d'ETF).
Les poids des indices bougent peu d'une année sur l'autre : l'approximation
suffit pour une analyse d'exposition (quelques points d'écart au plus).
"""

import re

import pandas as pd

DATE_SOURCE = "30/09/2026"

# ----------------------------------------------------------------------
# 1. Pays : code ISO-3 (carte du monde), devise, région du référentiel
# ----------------------------------------------------------------------
PAYS = {   # nom -> (ISO-3, devise, région)
    "États-Unis": ("USA", "USD", "États-Unis"), "Canada": ("CAN", "CAD", "Canada"),
    "Japon": ("JPN", "JPY", "Japon"), "Royaume-Uni": ("GBR", "GBP", "Royaume-Uni"),
    "Suisse": ("CHE", "CHF", "Suisse"), "France": ("FRA", "EUR", "Europe"),
    "Allemagne": ("DEU", "EUR", "Europe"), "Pays-Bas": ("NLD", "EUR", "Europe"),
    "Espagne": ("ESP", "EUR", "Europe"), "Italie": ("ITA", "EUR", "Europe"),
    "Belgique": ("BEL", "EUR", "Europe"), "Finlande": ("FIN", "EUR", "Europe"),
    "Irlande": ("IRL", "EUR", "Europe"), "Autriche": ("AUT", "EUR", "Europe"),
    "Portugal": ("PRT", "EUR", "Europe"), "Grèce": ("GRC", "EUR", "Émergents"),
    "Slovaquie": ("SVK", "EUR", "Europe"), "Slovénie": ("SVN", "EUR", "Europe"),
    "Luxembourg": ("LUX", "EUR", "Europe"),
    "Suède": ("SWE", "SEK", "Europe"), "Danemark": ("DNK", "DKK", "Europe"),
    "Norvège": ("NOR", "NOK", "Europe"), "Pologne": ("POL", "PLN", "Émergents"),
    "Hongrie": ("HUN", "HUF", "Émergents"), "Tchéquie": ("CZE", "CZK", "Émergents"),
    "Israël": ("ISR", "ILS", "Asie-Pacifique"),
    "Australie": ("AUS", "AUD", "Asie-Pacifique"), "Nouvelle-Zélande": ("NZL", "NZD", "Asie-Pacifique"),
    "Hong Kong": ("HKG", "HKD", "Asie-Pacifique"), "Singapour": ("SGP", "SGD", "Asie-Pacifique"),
    "Chine": ("CHN", "CNY", "Émergents"), "Taïwan": ("TWN", "TWD", "Émergents"),
    "Corée du Sud": ("KOR", "KRW", "Émergents"), "Inde": ("IND", "INR", "Émergents"),
    "Brésil": ("BRA", "BRL", "Émergents"), "Mexique": ("MEX", "MXN", "Émergents"),
    "Afrique du Sud": ("ZAF", "ZAR", "Émergents"), "Arabie saoudite": ("SAU", "SAR", "Émergents"),
    "Émirats arabes unis": ("ARE", "AED", "Émergents"), "Qatar": ("QAT", "QAR", "Émergents"),
    "Koweït": ("KWT", "KWD", "Émergents"), "Indonésie": ("IDN", "IDR", "Émergents"),
    "Malaisie": ("MYS", "MYR", "Émergents"), "Thaïlande": ("THA", "THB", "Émergents"),
    "Philippines": ("PHL", "PHP", "Émergents"), "Turquie": ("TUR", "TRY", "Émergents"),
    "Chili": ("CHL", "CLP", "Émergents"), "Pérou": ("PER", "PEN", "Émergents"),
    "Colombie": ("COL", "COP", "Émergents"), "Égypte": ("EGY", "EGP", "Émergents"),
}
AUTRES = "Autres pays"

# ----------------------------------------------------------------------
# 2. Répartition des indices par pays (en %, total = 100)
# ----------------------------------------------------------------------
def _completer(principaux, suivants, total_autres):
    """Pays principaux (fiche officielle) + pays suivants ramenés au total « autres »."""
    somme = sum(suivants.values())
    resultat = dict(principaux)
    for pays, poids in suivants.items():
        resultat[pays] = poids * total_autres / somme
    return resultat


# Pays « suivants » des indices développés (ordres de grandeur relatifs)
_SUIVANTS_DEVELOPPES = {
    "Suisse": 2.4, "Allemagne": 2.3, "Australie": 1.6, "Pays-Bas": 1.1, "Suède": 0.8, "Espagne": 0.8,
    "Italie": 0.7, "Danemark": 0.55, "Hong Kong": 0.5, "Singapour": 0.4, "Finlande": 0.25, "Belgique": 0.25,
    "Israël": 0.2, "Norvège": 0.15, "Irlande": 0.15, "Nouvelle-Zélande": 0.05, "Autriche": 0.05,
    "Portugal": 0.04,
}
_SUIVANTS_EMERGENTS = {
    "Afrique du Sud": 3.3, "Arabie saoudite": 2.8, "Mexique": 1.8, "Émirats arabes unis": 1.3,
    "Malaisie": 1.2, "Indonésie": 1.1, "Thaïlande": 1.0, "Pologne": 0.9, "Qatar": 0.7, "Koweït": 0.7,
    "Grèce": 0.5, "Turquie": 0.4, "Chili": 0.4, "Philippines": 0.4, "Pérou": 0.3, "Hongrie": 0.25,
    "Tchéquie": 0.15, "Colombie": 0.1, "Égypte": 0.05,
}
_SUIVANTS_EUROPE = {
    "Suède": 5.5, "Danemark": 3.8, "Espagne": 4.8, "Italie": 4.5, "Finlande": 1.6, "Belgique": 1.6,
    "Norvège": 1.0, "Irlande": 0.8, "Autriche": 0.3, "Portugal": 0.3, "Pologne": 0.2,
}

_MONDE = _completer({"États-Unis": 72.94, "Japon": 5.91, "Royaume-Uni": 3.41, "Canada": 3.29, "France": 2.24},
                    _SUIVANTS_DEVELOPPES, 12.21)
_EMERGENTS = _completer({"Taïwan": 28.94, "Corée du Sud": 21.4, "Chine": 19.8, "Inde": 10.65, "Brésil": 4.09},
                        _SUIVANTS_EMERGENTS, 15.12)
# ACWI ≈ 89,5 % pays développés + 10,5 % émergents (fiche MSCI : États-Unis 64,21 %, Japon 5,2 %,
# Taïwan 3,46 %, Royaume-Uni 3 %, Canada 2,9 %) : on combine les deux répartitions.
_PART_EMERGENTS_ACWI = 0.12
_ACWI = {p: _MONDE.get(p, 0) * (1 - _PART_EMERGENTS_ACWI) + _EMERGENTS.get(p, 0) * _PART_EMERGENTS_ACWI
         for p in set(_MONDE) | set(_EMERGENTS)}
_EUROPE = _completer({"Royaume-Uni": 22.55, "France": 14.79, "Suisse": 14.16, "Allemagne": 13.62,
                      "Pays-Bas": 9.45}, _SUIVANTS_EUROPE, 25.44)
# Pays développés hors États-Unis et Canada (MSCI EAFE, FTSE Developed ex-North America)
_EAFE = {p: v for p, v in _MONDE.items() if p not in ("États-Unis", "Canada")}

PAYS_PAR_INDICE = {
    "MSCI World": _MONDE,
    "MSCI ACWI": _ACWI,
    "MSCI Emerging Markets": _EMERGENTS,
    "MSCI Europe": _EUROPE,
    "MSCI EAFE": _EAFE,
    "S&P 500": {"États-Unis": 100},
    "Russell 2000": {"États-Unis": 100},
    "US Total Market": {"États-Unis": 100},
    "Nasdaq-100": {"États-Unis": 96.0, "Pays-Bas": 1.4, "Royaume-Uni": 1.3, "Canada": 0.8, "Chine": 0.5},
    "Euro Stoxx 50": {"France": 35, "Allemagne": 31, "Pays-Bas": 15, "Espagne": 9, "Italie": 7, "Belgique": 2,
                      "Finlande": 1},
    "CAC 40": {"France": 100},
    "DAX": {"Allemagne": 100},
    # Obligations
    "Emprunts d'État zone euro": {"France": 23.5, "Italie": 21.5, "Allemagne": 18, "Espagne": 14,
                                  "Belgique": 4.5, "Pays-Bas": 4, "Autriche": 3, "Portugal": 2, "Finlande": 1.5,
                                  "Irlande": 1.5, "Slovaquie": 0.6, "Slovénie": 0.4, "Luxembourg": 0.2},
    "Obligations d'entreprises euro": {"France": 27, "Allemagne": 14, "États-Unis": 13, "Pays-Bas": 7,
                                       "Italie": 6, "Espagne": 6, "Royaume-Uni": 6, "Suède": 2, "Belgique": 2,
                                       "Irlande": 2, "Japon": 2, "Suisse": 2},
    "Haut rendement euro": {"France": 20, "Italie": 15, "Allemagne": 12, "États-Unis": 9, "Espagne": 7,
                            "Royaume-Uni": 7, "Pays-Bas": 6, "Suède": 3, "Luxembourg": 3},
    "Emprunts d'État américains": {"États-Unis": 100},
    "Obligations d'entreprises américaines": {"États-Unis": 85, "Royaume-Uni": 4, "Canada": 3, "Japon": 3,
                                              "France": 2, "Allemagne": 2},
    "Obligations émergentes en dollars": {"Mexique": 7, "Arabie saoudite": 7, "Indonésie": 6, "Turquie": 5,
                                          "Chili": 4, "Brésil": 4, "Émirats arabes unis": 4, "Qatar": 4,
                                          "Colombie": 4, "Philippines": 4, "Afrique du Sud": 3, "Pérou": 3,
                                          "Égypte": 3, "Pologne": 2, "Chine": 3, "Inde": 2},
}

# ----------------------------------------------------------------------
# 3. Répartition des indices actions par secteur (en %)
# ----------------------------------------------------------------------
SECTEURS_PAR_INDICE = {
    "MSCI World": {"Technologie": 31.78, "Finance": 15.74, "Industrie": 10.8, "Santé": 9.2,
                   "Consommation discrétionnaire": 8.36, "Communication": 8.31, "Consommation de base": 4.77,
                   "Énergie": 4.03, "Matériaux": 3.21, "Services publics": 2.3, "Immobilier": 1.52},
    "MSCI ACWI": {"Technologie": 33.21, "Finance": 16.17, "Industrie": 10.27, "Santé": 8.42,
                  "Consommation discrétionnaire": 8.24, "Communication": 8.01, "Consommation de base": 4.51,
                  "Énergie": 3.96, "Matériaux": 3.51, "Services publics": 2.25, "Immobilier": 1.45},
    "MSCI Emerging Markets": {"Technologie": 43.78, "Finance": 19.35, "Consommation discrétionnaire": 7.39,
                              "Industrie": 6.34, "Communication": 5.86, "Matériaux": 5.77, "Énergie": 3.4,
                              "Santé": 2.72, "Consommation de base": 2.58, "Services publics": 1.86,
                              "Immobilier": 0.95},
    "MSCI Europe": {"Finance": 25.5, "Industrie": 18.61, "Santé": 12.72, "Technologie": 9.75,
                    "Consommation de base": 8.25, "Consommation discrétionnaire": 6.0, "Matériaux": 5.43,
                    "Énergie": 5.36, "Services publics": 4.78, "Communication": 3.08, "Immobilier": 0.53},
    "MSCI EAFE": {"Finance": 23, "Industrie": 18, "Santé": 10.5, "Consommation discrétionnaire": 10,
                  "Technologie": 9, "Consommation de base": 7.5, "Matériaux": 6, "Communication": 5,
                  "Énergie": 4, "Services publics": 3.5, "Immobilier": 2},
    "S&P 500": {"Technologie": 34, "Finance": 13, "Consommation discrétionnaire": 10.5, "Communication": 10,
                "Santé": 9, "Industrie": 8.5, "Consommation de base": 5, "Énergie": 3, "Services publics": 2.4,
                "Immobilier": 2, "Matériaux": 1.8},
    "US Total Market": {"Technologie": 33, "Finance": 13.5, "Consommation discrétionnaire": 10.5,
                        "Communication": 9.5, "Santé": 9.5, "Industrie": 9.5, "Consommation de base": 4.5,
                        "Énergie": 3, "Immobilier": 2.5, "Services publics": 2.5, "Matériaux": 2},
    "Nasdaq-100": {"Technologie": 51, "Communication": 16, "Consommation discrétionnaire": 13, "Santé": 5,
                   "Consommation de base": 5, "Industrie": 4.5, "Services publics": 1.5, "Matériaux": 1.5,
                   "Finance": 1, "Énergie": 0.5, "Immobilier": 1},
    "Russell 2000": {"Finance": 18, "Industrie": 17, "Santé": 16, "Technologie": 14,
                     "Consommation discrétionnaire": 10, "Immobilier": 6, "Énergie": 5, "Matériaux": 4.5,
                     "Services publics": 3, "Consommation de base": 3, "Communication": 2.5},
    "Euro Stoxx 50": {"Finance": 20, "Technologie": 16, "Industrie": 16, "Consommation discrétionnaire": 15,
                      "Consommation de base": 7, "Santé": 6, "Services publics": 6, "Énergie": 5,
                      "Communication": 5, "Matériaux": 4},
    "CAC 40": {"Consommation discrétionnaire": 22, "Industrie": 20, "Santé": 10, "Consommation de base": 10,
               "Finance": 10, "Matériaux": 8, "Énergie": 7, "Technologie": 6, "Communication": 3,
               "Services publics": 3, "Immobilier": 1},
    "DAX": {"Industrie": 25, "Finance": 20, "Technologie": 15, "Consommation discrétionnaire": 12, "Santé": 7,
            "Communication": 7, "Matériaux": 6, "Services publics": 5, "Immobilier": 1, "Consommation de base": 1,
            "Énergie": 1},
}

# ----------------------------------------------------------------------
# 4. Quel indice suit chaque ETF ?
# ----------------------------------------------------------------------
ETF_INDICE = {
    "CW8.PA": "MSCI World", "EWLD.PA": "MSCI World", "WPEA.PA": "MSCI World", "IWDA.AS": "MSCI World",
    "EUNL.DE": "MSCI World", "SWDA.L": "MSCI World", "URTH": "MSCI World",
    "VWCE.DE": "MSCI ACWI", "VWRL.AS": "MSCI ACWI", "IUSQ.DE": "MSCI ACWI", "SPYI.DE": "MSCI ACWI",
    "VT": "MSCI ACWI", "ACWI": "MSCI ACWI",
    "ESE.PA": "S&P 500", "PE500.PA": "S&P 500", "VUSA.AS": "S&P 500", "SXR8.DE": "S&P 500", "CSPX.L": "S&P 500",
    "SPY": "S&P 500", "VOO": "S&P 500", "IVV": "S&P 500", "DIA": "S&P 500",
    "PUST.PA": "Nasdaq-100", "EQQQ.DE": "Nasdaq-100", "QQQ": "Nasdaq-100",
    "PAEEM.PA": "MSCI Emerging Markets", "AEEM.PA": "MSCI Emerging Markets", "EIMI.L": "MSCI Emerging Markets",
    "IS3N.DE": "MSCI Emerging Markets", "VWO": "MSCI Emerging Markets", "EEM": "MSCI Emerging Markets",
    "CAC.PA": "CAC 40", "CACC.PA": "CAC 40", "C40.PA": "CAC 40", "MSE.PA": "Euro Stoxx 50", "C50.PA": "Euro Stoxx 50", "EXS1.DE": "DAX",
    "EUNK.DE": "MSCI Europe", "MEUD.PA": "MSCI Europe",
    "VEA": "MSCI EAFE", "EFA": "MSCI EAFE", "VTI": "US Total Market", "IWM": "Russell 2000",
    "IBCA.DE": "Emprunts d'État zone euro", "EUNH.DE": "Emprunts d'État zone euro", "DBXN.DE": "Emprunts d'État zone euro",
    "IBCI.DE": "Emprunts d'État zone euro", "EUN5.DE": "Obligations d'entreprises euro",
    "EUNW.DE": "Haut rendement euro", "TLT": "Emprunts d'État américains", "IEF": "Emprunts d'État américains",
    "SHY": "Emprunts d'État américains", "TIP": "Emprunts d'État américains", "AGG": "Emprunts d'État américains",
    "BND": "Emprunts d'État américains", "LQD": "Obligations d'entreprises américaines",
    "HYG": "Obligations d'entreprises américaines", "EMB": "Obligations émergentes en dollars",
}
# Reconnaissance par le nom, pour les ETF absents de la liste ci-dessus (ordre important)
MOTIFS_NOM = [
    (r"all[- ]?world|acwi|total world", "MSCI ACWI"),
    (r"emerging|émergent|\bem\b|\bem imi\b", "MSCI Emerging Markets"),
    (r"msci world|developed world|\bworld\b|monde", "MSCI World"),
    (r"nasdaq", "Nasdaq-100"),
    (r"s&p ?500|sp ?500", "S&P 500"),
    (r"stoxx europe 600|europe 600|msci europe|stoxx 600", "MSCI Europe"),
    (r"euro ?stoxx ?50", "Euro Stoxx 50"),
    (r"cac ?40|\bc\.c\.40\b", "CAC 40"),           # « AM.C.C.40 UC.ETF C » : libellé abrégé d'un avis
    (r"\bdax\b", "DAX"),
    (r"eafe|developed markets ex|ftse developed", "MSCI EAFE"),
    (r"russell 2000", "Russell 2000"),
    (r"total (stock|us|u\.s\.) market", "US Total Market"),
    (r"(€|eur|euro).*(govt|gov|government|state|souverain|état)", "Emprunts d'État zone euro"),
    (r"(€|eur|euro).*(high yield|haut rendement)", "Haut rendement euro"),
    (r"(€|eur|euro).*(corp|entreprise)", "Obligations d'entreprises euro"),
    (r"treasury|us aggregate|total bond", "Emprunts d'État américains"),
]
_MOTIFS_NOM = [(re.compile(m, re.IGNORECASE), i) for m, i in MOTIFS_NOM]
MOTIF_COUVERT = re.compile(r"hedged|couvert|\(eur h\)|eur hdg|\bhdg\b", re.IGNORECASE)


def indice_suivi(ticker, nom=""):
    """Indice suivi par un ETF (clé de PAYS_PAR_INDICE), ou None si inconnu."""
    if ticker in ETF_INDICE:
        return ETF_INDICE[ticker]
    for motif, indice in _MOTIFS_NOM:
        if motif.search(str(nom or "")):
            return indice
    return None


def est_couvert(nom):
    """Vrai si le nom de l'ETF indique une couverture du risque de change (« EUR Hedged »)."""
    return bool(MOTIF_COUVERT.search(str(nom or "")))


def pays_de(indice):
    """Répartition par pays d'un indice, en fractions (total = 1)."""
    poids = pd.Series(PAYS_PAR_INDICE[indice], dtype=float)
    return poids / poids.sum()


def secteurs_de(indice):
    """Répartition par secteur d'un indice actions, en fractions (total = 1), ou None."""
    if indice not in SECTEURS_PAR_INDICE:
        return None
    poids = pd.Series(SECTEURS_PAR_INDICE[indice], dtype=float)
    return poids / poids.sum()


def iso3(pays):
    return PAYS.get(pays, (None,))[0]


def devise_du_pays(pays):
    return PAYS.get(pays, (None, None))[1]


def region_du_pays(pays):
    return PAYS.get(pays, (None, None, None))[2]
