"""
construire_base_titres.py — Remplit la base locale de titres (data/base/).

À lancer UNE FOIS avec Internet (puis de temps en temps pour la mettre à jour) :

    python construire_base_titres.py               construction complète (≈ 1 h)
    python construire_base_titres.py --mise-a-jour  ajoute seulement les derniers jours (quelques minutes)
    python construire_base_titres.py --liste        liste des titres seulement, sans les cours (2 min)

Ce que fait le script :
    1. il récupère la composition des grands indices boursiers sur Wikipédia
       (S&P 500, Russell 1000, Nasdaq-100, CAC 40, SBF 120, DAX, MDAX, SDAX,
       FTSE 100, FTSE 250, Euro Stoxx 50, AEX, BEL 20, IBEX 35, FTSE MIB, SMI,
       OMX Stockholm 30, OMX Copenhague 25, OMX Helsinki 25, OBX, ATX, PSI,
       Nikkei 225, S&P/TSX 60, S&P/ASX 200, Hang Seng...) : ≈ 3 500 actions ;
    2. il y ajoute une soixantaine d'ETF courants et les titres du référentiel ;
    3. il télécharge les cours de clôture quotidiens depuis 2015 (depuis 2007
       pour les indices et les taux de change, utiles aux stress tests),
       par lots de 100 titres, avec une pause entre chaque lot ;
    4. il enregistre tout dans data/base/ (≈ 40 à 60 Mo).

Si le script s'arrête (coupure Internet, fenêtre fermée), relancez-le : il
reprend là où il s'était arrêté. Une source indisponible est simplement
ignorée (Wikipédia change parfois la présentation de ses tableaux).
Les titres que Yahoo Finance ne reconnaît pas sont listés dans data/base/echecs.csv.

Bibliothèque nécessaire en plus : lxml (python -m pip install lxml), pour
lire les tableaux de Wikipédia.
"""

import io
import json
import re
import sys
import time
import urllib.request

import pandas as pd

from src import base_titres as base
from src import fond_de_carte
from src.devises import devise_par_suffixe
from src.import_fichier import convertir_code_global, isin_valide

DEBUT_ACTIONS = "2015-01-01"
DEBUT_INDICES = "2007-01-01"
TAILLE_LOT = 100
PAUSE = 2.0                       # secondes entre deux lots (pour ne pas être bloqué par Yahoo)
FICHIER_PROGRESSION = base.DOSSIER / "progression.json"

# (nom de l'indice, page Wikipédia, suffixe Yahoo à ajouter aux tickers)
SOURCES = [
    ("S&P 500", "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", ""),
    ("Nasdaq-100", "https://en.wikipedia.org/wiki/Nasdaq-100", ""),
    ("Dow Jones", "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average", ""),
    ("Russell 1000", "https://en.wikipedia.org/wiki/Russell_1000_Index", ""),
    ("CAC 40", "https://en.wikipedia.org/wiki/CAC_40", ".PA"),
    ("SBF 120", "https://fr.wikipedia.org/wiki/SBF_120", ".PA"),
    ("CAC Mid 60", "https://fr.wikipedia.org/wiki/CAC_Mid_60", ".PA"),
    ("DAX", "https://en.wikipedia.org/wiki/DAX", ".DE"),
    ("MDAX", "https://en.wikipedia.org/wiki/MDAX", ".DE"),
    ("SDAX", "https://en.wikipedia.org/wiki/SDAX", ".DE"),
    ("TecDAX", "https://en.wikipedia.org/wiki/TecDAX", ".DE"),
    ("FTSE 100", "https://en.wikipedia.org/wiki/FTSE_100_Index", ".L"),
    ("FTSE 250", "https://en.wikipedia.org/wiki/FTSE_250_Index", ".L"),
    ("Euro Stoxx 50", "https://en.wikipedia.org/wiki/EURO_STOXX_50", None),
    ("AEX", "https://en.wikipedia.org/wiki/AEX_index", ".AS"),
    ("AMX", "https://en.wikipedia.org/wiki/AMX_index", ".AS"),
    ("BEL 20", "https://en.wikipedia.org/wiki/BEL_20", ".BR"),
    ("IBEX 35", "https://en.wikipedia.org/wiki/IBEX_35", ".MC"),
    ("FTSE MIB", "https://en.wikipedia.org/wiki/FTSE_MIB", ".MI"),
    ("SMI", "https://en.wikipedia.org/wiki/Swiss_Market_Index", ".SW"),
    ("SMIM", "https://en.wikipedia.org/wiki/SMI_MID", ".SW"),
    ("OMX Stockholm 30", "https://en.wikipedia.org/wiki/OMX_Stockholm_30", ".ST"),
    ("OMX Copenhagen 25", "https://en.wikipedia.org/wiki/OMX_Copenhagen_25", ".CO"),
    ("OMX Helsinki 25", "https://en.wikipedia.org/wiki/OMX_Helsinki_25", ".HE"),
    ("OBX", "https://en.wikipedia.org/wiki/OBX_Index", ".OL"),
    ("ATX", "https://en.wikipedia.org/wiki/Austrian_Traded_Index", ".VI"),
    ("PSI", "https://en.wikipedia.org/wiki/PSI-20", ".LS"),
    ("ISEQ 20", "https://en.wikipedia.org/wiki/ISEQ_20", ".IR"),
    ("Nikkei 225", "https://en.wikipedia.org/wiki/Nikkei_225", ".T"),
    ("S&P/TSX 60", "https://en.wikipedia.org/wiki/S%26P/TSX_60", ".TO"),
    ("S&P/ASX 200", "https://en.wikipedia.org/wiki/S%26P/ASX_200", ".AX"),
    ("Hang Seng", "https://en.wikipedia.org/wiki/Hang_Seng_Index", ".HK"),
]

# ETF courants (les tickers inconnus de Yahoo seront simplement écartés)
ETF = {
    # ETF éligibles PEA et UCITS cotés en euros
    "CW8.PA": "Amundi MSCI World", "EWLD.PA": "Amundi PEA MSCI World", "WPEA.PA": "iShares MSCI World Swap PEA",
    "ESE.PA": "BNP Paribas Easy S&P 500", "PE500.PA": "Amundi PEA S&P 500", "PUST.PA": "Amundi PEA Nasdaq-100",
    "PAEEM.PA": "Amundi PEA MSCI Emerging Markets", "AEEM.PA": "Amundi MSCI Emerging Markets",
    "CAC.PA": "Amundi CAC 40", "MSE.PA": "Amundi Euro Stoxx 50", "C50.PA": "Amundi Euro Stoxx 50 II",
    "IWDA.AS": "iShares Core MSCI World", "EUNL.DE": "iShares Core MSCI World (Xetra)",
    "VWCE.DE": "Vanguard FTSE All-World Acc", "VWRL.AS": "Vanguard FTSE All-World Dist",
    "VUSA.AS": "Vanguard S&P 500", "SXR8.DE": "iShares Core S&P 500 (Xetra)", "CSPX.L": "iShares Core S&P 500",
    "EIMI.L": "iShares Core MSCI EM IMI", "IS3N.DE": "iShares Core MSCI EM IMI (Xetra)",
    "EXS1.DE": "iShares Core DAX", "EUNK.DE": "iShares Core MSCI Europe", "MEUD.PA": "Amundi Stoxx Europe 600",
    "IUSQ.DE": "iShares MSCI ACWI", "SPYI.DE": "SPDR MSCI ACWI IMI", "EQQQ.DE": "Invesco Nasdaq-100",
    # Obligations et or (UCITS)
    "IBCA.DE": "iShares € Govt Bond 1-3yr", "EUNH.DE": "iShares Core € Govt Bond", "IBCI.DE": "iShares € Inflation Linked",
    "EUN5.DE": "iShares Core € Corp Bond", "EUNW.DE": "iShares € High Yield Corp Bond", "4GLD.DE": "Xetra-Gold",
    "DBXN.DE": "Xtrackers II Eurozone Government Bond 1C", "XEON.DE": "Xtrackers II EUR Overnight Rate Swap",
    "CSH2.PA": "Amundi Smart Overnight Return",
    # ETF américains très courants
    "SPY": "SPDR S&P 500", "VOO": "Vanguard S&P 500", "IVV": "iShares Core S&P 500", "VTI": "Vanguard Total Stock Market",
    "QQQ": "Invesco QQQ", "DIA": "SPDR Dow Jones", "IWM": "iShares Russell 2000", "VEA": "Vanguard FTSE Developed",
    "VWO": "Vanguard FTSE Emerging", "EFA": "iShares MSCI EAFE", "EEM": "iShares MSCI Emerging Markets",
    "VT": "Vanguard Total World", "AGG": "iShares Core US Aggregate Bond", "BND": "Vanguard Total Bond",
    "TLT": "iShares 20+ Year Treasury", "IEF": "iShares 7-10 Year Treasury", "SHY": "iShares 1-3 Year Treasury",
    "TIP": "iShares TIPS", "LQD": "iShares IG Corporate Bond", "HYG": "iShares High Yield Corporate Bond",
    "EMB": "iShares JPM USD EM Bond", "GLD": "SPDR Gold", "IAU": "iShares Gold", "SLV": "iShares Silver",
    "VNQ": "Vanguard Real Estate", "XLK": "Technology Select Sector SPDR", "XLF": "Financial Select Sector SPDR",
    "XLE": "Energy Select Sector SPDR", "XLV": "Health Care Select Sector SPDR", "ARKK": "ARK Innovation",
}
# Indices, taux de change et fonds de référence (historique depuis 2007)
MARCHE = ["^GSPC", "^NDX", "^DJI", "^FCHI", "^STOXX50E", "^STOXX", "^GDAXI", "^FTSE", "^SSMI", "^N225",
          "^AXJO", "^GSPTSE", "^HSI", "^AEX", "^IBEX", "FTSEMIB.MI",
          "EURUSD=X", "EURGBP=X", "EURCHF=X", "EURJPY=X", "EURCAD=X", "EURAUD=X", "EURHKD=X", "EURDKK=X",
          "EURSEK=X", "EURNOK=X", "EURPLN=X", "EURSGD=X"]

SECTEURS = {   # secteurs GICS (anglais) -> noms du référentiel
    "information technology": "Technologie", "technology": "Technologie", "health care": "Santé",
    "healthcare": "Santé", "financials": "Finance", "financial": "Finance", "consumer discretionary":
    "Consommation discrétionnaire", "consumer staples": "Consommation de base", "industrials": "Industrie",
    "energy": "Énergie", "materials": "Matériaux", "basic materials": "Matériaux", "utilities":
    "Services publics", "real estate": "Immobilier", "communication services": "Communication",
    "telecommunications": "Communication", "telecommunication services": "Communication",
}
PAYS_PAR_SUFFIXE = {   # suffixe -> (pays, région du référentiel)
    "": ("États-Unis", "États-Unis"), ".PA": ("France", "Europe"), ".DE": ("Allemagne", "Europe"),
    ".F": ("Allemagne", "Europe"), ".AS": ("Pays-Bas", "Europe"), ".BR": ("Belgique", "Europe"),
    ".MC": ("Espagne", "Europe"), ".MI": ("Italie", "Europe"), ".LS": ("Portugal", "Europe"),
    ".IR": ("Irlande", "Europe"), ".VI": ("Autriche", "Europe"), ".HE": ("Finlande", "Europe"),
    ".CO": ("Danemark", "Europe"), ".ST": ("Suède", "Europe"), ".OL": ("Norvège", "Europe"),
    ".L": ("Royaume-Uni", "Royaume-Uni"), ".SW": ("Suisse", "Suisse"), ".T": ("Japon", "Japon"),
    ".TO": ("Canada", "Canada"), ".AX": ("Australie", "Asie-Pacifique"), ".HK": ("Hong Kong", "Asie-Pacifique"),
}


# ======================================================================
# 1. Composition des indices (Wikipédia)
# ======================================================================
def lire_page(url):
    demande = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (projet etudiant portfolio_tracker)"})
    with urllib.request.urlopen(demande, timeout=30) as reponse:
        return reponse.read().decode("utf-8", errors="replace")


def _colonne(tableau, mots):
    for c in tableau.columns:
        nom = " ".join(map(str, c)) if isinstance(c, tuple) else str(c)
        nom = nom.lower()
        if any(re.search(rf"\b{m}\b", nom) for m in mots):
            return c
    return None


def normaliser_ticker(brut, suffixe):
    """Code lu sur Wikipédia -> ticker Yahoo Finance (ou None)."""
    texte = re.sub(r"\[.*?\]", "", str(brut)).strip().upper()
    texte = texte.split("\n")[0].split(",")[0].strip()
    if not texte or texte in ("NAN", "-", "—"):
        return None
    texte = re.sub(r":\s+", ":", texte)                     # "NYSE: MMM" -> "NYSE:MMM"
    if " " in texte or ":" in texte or suffixe is None:      # "MC FP", "EPA:MC", "AAPL.O"...
        converti = convertir_code_global(texte)
        if converti:
            return converti
    m = re.match(r"^([A-Z0-9][A-Z0-9.\- ]{0,12}?)(\.[A-Z]{1,3})$", texte)
    if m and m.group(2) in base_suffixes():
        return m.group(1).replace(" ", "-") + m.group(2)
    if suffixe is None:
        return None                                      # indice multinational : il faut un suffixe explicite
    racine = texte.rstrip(".").replace(" ", "-")
    if suffixe in ("", ".TO", ".L"):
        racine = racine.replace(".", "-")                 # BRK.B -> BRK-B ; BT.A -> BT-A
    if suffixe == ".HK" and racine.isdigit():
        racine = racine.zfill(4)
    if not re.match(r"^[A-Z0-9][A-Z0-9\-&]{0,11}$", racine):
        return None
    return racine + suffixe


def base_suffixes():
    from src.import_fichier import SUFFIXES_YAHOO
    return SUFFIXES_YAHOO


def composition(nom_indice, url, suffixe):
    """Liste de dictionnaires (fiches de titres) d'après la page Wikipédia d'un indice."""
    tableaux = pd.read_html(io.StringIO(lire_page(url)))
    titres = []
    for tableau in tableaux:
        if len(tableau) < 10:
            continue
        col_ticker = _colonne(tableau, ["ticker", "symbol", "symbole", "code", "epic", "mnémonique", "mnemonique",
                                        "ticker symbol", "tickersymbol"])
        col_nom = _colonne(tableau, ["company", "security", "name", "constituent", "société", "societe",
                                     "entreprise", "nom", "issuer"])
        if col_ticker is None or col_nom is None or col_ticker == col_nom:
            continue
        col_secteur = _colonne(tableau, ["gics sector", "sector", "secteur", "industry", "icb industry"])
        col_isin = _colonne(tableau, ["isin"])
        for _, ligne in tableau.iterrows():
            ticker = normaliser_ticker(ligne[col_ticker], suffixe)
            if not ticker:
                continue
            secteur_brut = str(ligne[col_secteur]).strip() if col_secteur is not None else ""
            isin = str(ligne[col_isin]).strip().upper() if col_isin is not None else ""
            suff = ticker[ticker.rfind("."):] if "." in ticker else ""
            pays, region = PAYS_PAR_SUFFIXE.get(suff, ("", ""))
            titres.append({
                "ticker": ticker, "nom": re.sub(r"\[.*?\]", "", str(ligne[col_nom])).strip(),
                "isin": isin if isin_valide(isin) else "", "pays": pays, "region": region,
                "secteur": SECTEURS.get(secteur_brut.lower(), secteur_brut if secteur_brut.lower() != "nan" else ""),
                "classe": "Actions", "devise": devise_par_suffixe(ticker), "indices": nom_indice,
            })
        if titres:
            break                                        # le premier tableau exploitable suffit
    return titres


def univers(sources=SOURCES):
    """Tous les titres à mettre dans la base, sans doublon."""
    from src.analyse import charger_referentiel
    titres = {}

    def ajouter(fiche, prioritaire=False):
        """Fusionne avec une fiche déjà vue : on garde les informations non vides
        (celles du référentiel du projet l'emportent sur celles de Wikipédia)."""
        ancien = titres.get(fiche["ticker"])
        if ancien:
            indices = set(filter(None, ancien["indices"].split(";"))) | {fiche["indices"]}
            if prioritaire:
                fiche = {**ancien, **{k: v for k, v in fiche.items() if v}}
            else:
                fiche = {**fiche, **{k: v for k, v in ancien.items() if v}}
            fiche["indices"] = ";".join(sorted(indices))
        titres[fiche["ticker"]] = fiche

    for nom, url, suffixe in sources:
        try:
            liste = composition(nom, url, suffixe)
            print(f"   {nom:<20} {len(liste):>5} titres")
            for fiche in liste:
                ajouter(fiche)
        except ImportError:
            sys.exit("❌ Installer lxml pour lire Wikipédia : python -m pip install lxml")
        except Exception as erreur:
            print(f"   {nom:<20}  ignoré ({type(erreur).__name__})")
    for ticker, nom in ETF.items():
        suff = ticker[ticker.rfind("."):] if "." in ticker else ""
        classe = "Obligations" if any(m in nom for m in ("Bond", "Treasury", "TIPS", "Govt", "Corp")) else \
            ("Or" if "Gold" in nom else "Actions")
        ajouter({"ticker": ticker, "nom": nom, "isin": "", "pays": PAYS_PAR_SUFFIXE.get(suff, ("", ""))[0],
                 "region": "Monde (ETF)" if classe == "Actions" else "", "secteur": "ETF diversifié" if classe == "Actions" else "",
                 "classe": classe, "devise": devise_par_suffixe(ticker), "indices": "ETF"})
    referentiel = charger_referentiel()
    for ticker, ligne in referentiel.iterrows():
        ajouter({"ticker": ticker, "nom": ligne.get("nom", ""), "isin": "", "pays": ligne.get("pays", ""),
                 "region": ligne.get("region", ""), "secteur": ligne.get("secteur", ""),
                 "classe": ligne.get("classe", "Actions") or "Actions", "devise": devise_par_suffixe(ticker),
                 "indices": "Référentiel"}, prioritaire=True)
    return list(titres.values())


# ======================================================================
# 2. Téléchargement des cours, par lots
# ======================================================================
def telecharger_lot(tickers, debut):
    import yfinance as yf
    for essai in range(3):
        try:
            donnees = yf.download(list(tickers), start=debut, auto_adjust=False, progress=False)
            if donnees is None or donnees.empty:
                return pd.DataFrame()
            cours = donnees["Close"]
            if isinstance(cours, pd.Series):
                cours = cours.to_frame(name=list(tickers)[0])
            index = pd.to_datetime(cours.index)
            cours.index = (index.tz_localize(None) if index.tz is not None else index).normalize()
            return cours.dropna(axis=1, how="all")
        except Exception as erreur:
            attente = 30 * (essai + 1)
            print(f"      Yahoo indisponible ({type(erreur).__name__}), nouvel essai dans {attente} s...")
            time.sleep(attente)
    return pd.DataFrame()


def _progression():
    if FICHIER_PROGRESSION.exists():
        return set(json.loads(FICHIER_PROGRESSION.read_text(encoding="utf-8")))
    return set()


def _sauver_progression(faits):
    FICHIER_PROGRESSION.parent.mkdir(parents=True, exist_ok=True)
    FICHIER_PROGRESSION.write_text(json.dumps(sorted(faits)), encoding="utf-8")


def telecharger(tickers, debut, deja_faits=None, nom="titres"):
    deja_faits = set() if deja_faits is None else deja_faits
    a_faire = [t for t in tickers if t not in deja_faits]
    echecs = []
    lots = [a_faire[i:i + TAILLE_LOT] for i in range(0, len(a_faire), TAILLE_LOT)]
    for numero, lot in enumerate(lots, 1):
        cours = telecharger_lot(lot, debut)
        base.ajouter_cours(cours)
        trouves = set(cours.columns)
        echecs += [t for t in lot if t not in trouves]
        deja_faits |= set(lot)
        _sauver_progression(deja_faits)
        print(f"   lot {numero}/{len(lots)} : {len(trouves)}/{len(lot)} {nom} trouvés")
        time.sleep(PAUSE)
    return echecs


def main():
    arguments = set(sys.argv[1:])
    debut_chrono = time.time()
    if "--mise-a-jour" in arguments:
        tickers = base.tickers_avec_cours()
        if not tickers:
            sys.exit("❌ La base est vide : lancer d'abord  python construire_base_titres.py")
        derniere = base.derniere_date()
        debut = (derniere - pd.Timedelta(days=7)).strftime("%Y-%m-%d")
        print(f"⏳ Mise à jour de {len(tickers)} titres depuis le {debut}...")
        telecharger(tickers, debut, set(), nom="titres")
        print(f"✅ Base à jour (dernier cours : {base.derniere_date():%d/%m/%Y})")
        if not fond_de_carte.chemin().exists():
            fond_de_carte.telecharger()
        return

    print("⏳ 1. Composition des indices (Wikipédia)...")
    titres = univers()
    base.ajouter_titres(titres)
    print(f"✅ {len(titres)} titres dans la fiche des titres (data/base/titres.csv)")
    if fond_de_carte.telecharger():
        print("✅ Fond de carte du monde enregistré (data/base/pays.geojson)")
    else:
        print("   Fond de carte non téléchargé : la carte du monde s'affichera seulement avec Internet")
    if "--liste" in arguments:
        return

    deja_faits = _progression()
    if deja_faits:
        print(f"↻ Reprise : {len(deja_faits)} titres déjà téléchargés")
    print(f"⏳ 2. Indices et taux de change depuis {DEBUT_INDICES}...")
    telecharger(MARCHE, DEBUT_INDICES, deja_faits, nom="indices / taux")
    tickers = [f["ticker"] for f in titres]
    print(f"⏳ 3. Cours de {len(tickers)} titres depuis {DEBUT_ACTIONS} (par lots de {TAILLE_LOT}, patience)...")
    telecharger(tickers, DEBUT_ACTIONS, deja_faits)

    tous_echecs = [t for t in tickers if t not in set(base.tickers_avec_cours())]
    pd.DataFrame({"ticker": tous_echecs}).to_csv(base.DOSSIER / "echecs.csv", index=False)
    FICHIER_PROGRESSION.unlink(missing_ok=True)
    r = base.resume()
    duree = (time.time() - debut_chrono) / 60
    print()
    print(f"✅ Base construite en {duree:.0f} min : {r['titres_avec_cours']} titres avec cours, "
          f"dernier cours du {r['derniere_date']:%d/%m/%Y}")
    if tous_echecs:
        print(f"   {len(tous_echecs)} tickers non reconnus par Yahoo Finance (liste : data/base/echecs.csv)")
    print("   L'application fonctionne maintenant hors connexion pour tous ces titres.")


if __name__ == "__main__":
    main()
