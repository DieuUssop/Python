"""
expositions.py — À quoi le portefeuille est-il VRAIMENT exposé ? Et est-il
vraiment diversifié ?

1. ANALYSE EN TRANSPARENCE
   Chaque ETF est « éclaté » selon la composition de l'indice qu'il suit
   (composition_etf.py) : un ETF MSCI World de 10 000 € devient ≈ 7 300 €
   d'actions américaines, 590 € d'actions japonaises, etc. Les actions détenues
   en direct gardent leur pays, leur secteur et leur devise de cotation.

2. LES EXPOSITIONS (en % de la valeur)
   - géographie : pays et régions (poche actions et poche obligations) ;
   - secteurs : poche actions ;
   - devises : exposition RÉELLE au risque de change, sur tout le portefeuille
     (un ETF monde coté en euros reste exposé au dollar, sauf s'il est couvert) ;
   - concentration : poids des plus grosses lignes, règle 5/10/40 des fonds UCITS ;
   - taux : sensibilité (duration) de la poche obligataire.

3. LA DIVERSIFICATION RÉELLE (corrélations)
   Dix lignes qui montent et baissent ensemble ne valent qu'UN pari. On regroupe
   les titres par « blocs » de titres très corrélés (classification hiérarchique),
   et on mesure :
   - la corrélation moyenne pondérée entre les lignes ;
   - le ratio de diversification Σ wᵢσᵢ / σₚ (1 = aucune diversification) ;
   - le nombre de blocs indépendants ;
   - la corrélation moyenne les jours de forte baisse (les corrélations
     montent pendant les crises : c'est là que la diversification est utile).

4. LE DIAGNOSTIC
   Des règles simples, aux seuils documentés et adaptés au profil du client,
   produisent des constats (vert / orange / rouge), le risque associé et des
   pistes. Analyse pédagogique : ce n'est pas un conseil en investissement.
"""

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, leaves_list, linkage
from scipy.spatial.distance import squareform

from . import composition_etf as ce

SANS_PAYS = "Sans pays (or)"
NON_CLASSE = "Non classé"
REGIONS_FONDS = {"Monde", "Monde (ETF)", "Zone euro", "Émergents"}
SEUIL_BLOC = 0.7                 # corrélation à partir de laquelle deux titres forment un même « pari »

# Indices « larges » dont une action en direct fait probablement aussi partie
GRANDS_INDICES = ["S&P 500", "Nasdaq-100", "CAC 40", "DAX", "Euro Stoxx 50", "FTSE 100", "SMI", "AEX",
                  "Nikkei 225", "S&P/TSX 60", "S&P/ASX 200", "IBEX 35", "FTSE MIB", "BEL 20", "Hang Seng"]


# ======================================================================
# 1. Analyse en transparence
# ======================================================================
def _est_un_fonds(ticker, ligne):
    return (ticker in ce.ETF_INDICE or str(ligne.get("secteur", "")) == "ETF diversifié"
            or str(ligne.get("region", "")) in REGIONS_FONDS or str(ligne.get("pays", "")) in REGIONS_FONDS
            or "ETF" in str(ligne.get("nom", "")) or "UCITS" in str(ligne.get("nom", "")))


def _devise_obligations(indice, devise_cotation):
    if indice is None:
        return devise_cotation
    if "euro" in indice or "zone euro" in indice:
        return "EUR"
    return "USD"


def transparence(positions):
    """Tableau « éclaté » : une ligne par (titre détenu, pays, secteur).

    Colonnes : ticker, nom, classe, pays, region, secteur, devise, poids (fraction
    de la valeur totale), indice (indice suivi si c'est un ETF, sinon None).
    """
    total = positions["valeur"].sum()
    lignes = []
    for ticker, p in positions.iterrows():
        w = float(p["valeur"] / total) if total else 0.0
        classe = p.get("classe", "Actions")
        nom = p.get("nom", ticker)
        devise_cot = p.get("devise", "EUR")
        base = {"ticker": ticker, "nom": nom, "classe": classe}
        if classe == "Or":
            lignes.append({**base, "pays": SANS_PAYS, "region": SANS_PAYS, "secteur": None,
                           "devise": "Or", "poids": w, "indice": None})
            continue
        indice = ce.indice_suivi(ticker, nom) if (_est_un_fonds(ticker, p) or classe == "Obligations") else None
        couvert = ce.est_couvert(nom)
        if indice is None:
            pays = p.get("pays", NON_CLASSE)
            if pays in ("Zone euro",) and classe == "Obligations":
                indice = "Emprunts d'État zone euro"
            elif pays not in ce.PAYS:
                region = p.get("region", NON_CLASSE)
                lignes.append({**base, "pays": NON_CLASSE, "region": region if region not in REGIONS_FONDS
                               else NON_CLASSE, "secteur": p.get("secteur") if classe == "Actions" else None,
                               "devise": devise_cot, "poids": w, "indice": None})
                continue
            else:
                devise = devise_cot if classe == "Actions" else _devise_obligations(None, devise_cot)
                lignes.append({**base, "pays": pays, "region": ce.region_du_pays(pays),
                               "secteur": p.get("secteur") if classe == "Actions" else None,
                               "devise": "EUR" if couvert else devise, "poids": w, "indice": None})
                continue
        repartition = ce.pays_de(indice)
        secteurs = ce.secteurs_de(indice) if classe == "Actions" else None
        for pays, part in repartition.items():
            if classe == "Actions":
                devise = "EUR" if couvert else (ce.devise_du_pays(pays) or devise_cot)
            else:
                devise = "EUR" if couvert else _devise_obligations(indice, devise_cot)
            if secteurs is None:
                lignes.append({**base, "pays": pays, "region": ce.region_du_pays(pays),
                               "secteur": NON_CLASSE if classe == "Actions" else None,
                               "devise": devise, "poids": w * part, "indice": indice})
            else:                                   # pays × secteurs (hypothèse : même mix sectoriel partout)
                for secteur, ps in secteurs.items():
                    lignes.append({**base, "pays": pays, "region": ce.region_du_pays(pays), "secteur": secteur,
                                   "devise": devise, "poids": w * part * ps, "indice": indice})
    return pd.DataFrame(lignes, columns=["ticker", "nom", "classe", "pays", "region", "secteur", "devise",
                                         "poids", "indice"])


def repartition(transp, colonne, classe=None, normaliser=False):
    """Poids par modalité de `colonne` (pays, region, secteur, devise, classe), triés.

    classe : limiter à une classe d'actifs (ex. "Actions") ;
    normaliser : poids en % de cette classe (sinon en % de tout le portefeuille)."""
    t = transp if classe is None else transp[transp["classe"] == classe]
    s = t.groupby(colonne, dropna=True)["poids"].sum().sort_values(ascending=False)
    if normaliser and s.sum() > 0:
        s = s / s.sum()
    return s


def carte_pays(transp, positions):
    """Données de la carte du monde (poche actions) : un pays par ligne.

    Colonnes : pays, iso3, poids (en % de la poche actions), valeur (€), nb_titres, titres."""
    actions = transp[(transp["classe"] == "Actions") & transp["pays"].isin(ce.PAYS)]
    if actions.empty:
        return pd.DataFrame(columns=["pays", "iso3", "poids", "valeur", "nb_titres", "titres"])
    total_actions = transp.loc[transp["classe"] == "Actions", "poids"].sum()
    valeur_totale = positions["valeur"].sum()
    lignes = []
    for pays, groupe in actions.groupby("pays"):
        par_titre = groupe.groupby("nom")["poids"].sum().sort_values(ascending=False)
        lignes.append({"pays": pays, "iso3": ce.iso3(pays), "poids": groupe["poids"].sum() / total_actions,
                       "valeur": groupe["poids"].sum() * valeur_totale, "nb_titres": len(par_titre),
                       "titres": list(par_titre.index)})
    return pd.DataFrame(lignes).sort_values("poids", ascending=False).reset_index(drop=True)


def part_hors_carte(transp):
    """Part du portefeuille absente de la carte, par classe (obligations, or, non classé)."""
    hors = transp[~((transp["classe"] == "Actions") & transp["pays"].isin(ce.PAYS))]
    return hors.groupby("classe")["poids"].sum()


# ======================================================================
# 2. Concentration et taux
# ======================================================================
def concentration(positions, transp):
    """Indicateurs de concentration, ligne par ligne (un ETF diversifié n'est pas
    une concentration : la règle 5/10/40 porte sur les émetteurs en direct)."""
    w = (positions["valeur"] / positions["valeur"].sum()).sort_values(ascending=False)
    directs = [t for t in w.index if transp.loc[transp["ticker"] == t, "indice"].isna().all()
               and positions.at[t, "classe"] == "Actions"]
    w_directs = w[directs]
    return {
        "top5": float(w.head(5).sum()),
        "top10": float(w.head(10).sum()),
        "nb_lignes": int(len(w)),
        "nb_effectif": float(1 / (w ** 2).sum()) if len(w) else 0.0,
        "plus_grosse_action": (w_directs.index[0], float(w_directs.iloc[0])) if len(w_directs) else None,
        "actions_plus_5": float(w_directs[w_directs > 0.05].sum()),
        "nb_actions_plus_5": int((w_directs > 0.05).sum()),
        "poids": w,
    }


def doublons_probables(positions, transp, fiches=None):
    """Actions détenues en direct qui font probablement AUSSI partie d'un ETF détenu.

    fiches : fiche des titres (colonne « indices » de la base locale, si disponible)."""
    etf = transp.dropna(subset=["indice"]).groupby("indice")["poids"].sum()
    etf = etf[[i for i in etf.index if i in ce.SECTEURS_PAR_INDICE]]        # ETF actions seulement
    if etf.empty:
        return []
    resultat = []
    for ticker, p in positions.iterrows():
        if p.get("classe") != "Actions" or not transp.loc[transp["ticker"] == ticker, "indice"].isna().all():
            continue
        appartenance = ""
        if fiches is not None and ticker in fiches.index and "indices" in fiches.columns:
            appartenance = str(fiches.at[ticker, "indices"] or "")
        pays = p.get("pays")
        for indice in etf.index:
            dans = indice in appartenance
            if indice in ("MSCI World", "MSCI ACWI", "MSCI EAFE") and pays in ce.pays_de(indice).index:
                dans = dans or any(g in appartenance for g in GRANDS_INDICES) or not appartenance
            elif indice == "MSCI Europe":
                dans = dans or (ce.region_du_pays(pays) in ("Europe", "Royaume-Uni", "Suisse")
                                and (not appartenance or any(g in appartenance for g in GRANDS_INDICES)))
            elif indice in ("S&P 500", "US Total Market"):
                dans = dans or (pays == "États-Unis" and (not appartenance or "S&P 500" in appartenance))
            if dans:
                resultat.append({"ticker": ticker, "nom": p.get("nom", ticker), "indice": indice})
                break
    return resultat


def taux(positions):
    """Sensibilité aux taux de la poche obligataire.

    duration moyenne (pondérée, en années) et perte estimée si les taux montent
    de 1 point : ≈ duration × 1 % × valeur (approximation au premier ordre)."""
    if "classe" not in positions.columns:
        return None
    oblig = positions[positions["classe"] == "Obligations"]
    if oblig.empty:
        return None
    d = pd.to_numeric(oblig.get("duration"), errors="coerce")
    valeurs = oblig["valeur"][d.notna()]
    if valeurs.sum() <= 0:
        return None
    duration = float((d.dropna() * valeurs).sum() / valeurs.sum())
    total = positions["valeur"].sum()
    perte = float((d.dropna() * valeurs).sum() * 0.01)
    return {"duration": duration, "part_obligations": float(oblig["valeur"].sum() / total),
            "perte_1pt": perte, "perte_1pt_pct": perte / total,
            "couverture": float(valeurs.sum() / oblig["valeur"].sum())}


# ======================================================================
# 3. Écarts à l'indice de référence et part du risque
# ======================================================================
def ecarts_indice(transp, fiche_indice):
    """Sur- / sous-pondérations de la poche actions par rapport à l'indice choisi.

    Renvoie {"classe": DataFrame, "pays": DataFrame, "secteur": DataFrame, "region": DataFrame} ;
    chaque DataFrame a les colonnes portefeuille, indice, ecart (fractions)."""
    resultat = {}
    part_actions = transp.loc[transp["classe"] == "Actions", "poids"].sum()
    classes = transp.groupby("classe")["poids"].sum()
    cible = pd.Series({"Actions": fiche_indice.part_actions, "Obligations": 1 - fiche_indice.part_actions})
    if fiche_indice.famille == "Monétaire":
        cible = pd.Series({"Monétaire": 1.0})
    tableau = pd.DataFrame({"portefeuille": classes, "indice": cible}).fillna(0.0)
    tableau["ecart"] = tableau["portefeuille"] - tableau["indice"]
    resultat["classe"] = tableau.sort_values("portefeuille", ascending=False)
    if fiche_indice.composition and part_actions > 0:
        for colonne, reference in [("pays", ce.pays_de(fiche_indice.composition)),
                                   ("secteur", ce.secteurs_de(fiche_indice.composition))]:
            if reference is None:
                continue
            port = repartition(transp, colonne, "Actions", normaliser=True)
            port = port.drop(NON_CLASSE, errors="ignore")
            tableau = pd.DataFrame({"portefeuille": port, "indice": reference}).fillna(0.0)
            tableau["ecart"] = tableau["portefeuille"] - tableau["indice"]
            tableau = tableau[(tableau["portefeuille"] >= 0.005) | (tableau["indice"] >= 0.005)]
            resultat[colonne] = tableau.sort_values("ecart", key=abs, ascending=False)
        reg_ref = ce.pays_de(fiche_indice.composition).groupby(ce.region_du_pays).sum()
        port = repartition(transp, "region", "Actions", normaliser=True).drop(NON_CLASSE, errors="ignore")
        tableau = pd.DataFrame({"portefeuille": port, "indice": reg_ref}).fillna(0.0)
        tableau["ecart"] = tableau["portefeuille"] - tableau["indice"]
        resultat["region"] = tableau.sort_values("portefeuille", ascending=False)
    return resultat


def risque_par_groupe(transp, part_risque_par_ligne, colonne):
    """Part du risque par groupe (pays, région, secteur, devise, classe).

    La contribution au risque de chaque ligne (budget_risque.py) est répartie
    entre ses groupes au prorata de son exposition (ETF éclatés)."""
    t = transp.copy()
    poids_ligne = t.groupby("ticker")["poids"].transform("sum")
    t["part_risque"] = t["ticker"].map(part_risque_par_ligne).fillna(0.0) * t["poids"] / poids_ligne
    g = t.groupby(colonne).agg(poids=("poids", "sum"), part_risque=("part_risque", "sum"))
    return g.sort_values("part_risque", ascending=False)


# ======================================================================
# 4. Corrélations et diversification réelle
# ======================================================================
def rendements_quotidiens(prix_hist, tickers):
    return prix_hist[list(tickers)].ffill().pct_change().dropna(how="all").dropna()


def ordre_regroupement(correlations):
    """Ordre des titres qui place côte à côte ceux qui bougent ensemble
    (classification hiérarchique, distance = 1 − corrélation, lien moyen)."""
    c = correlations.fillna(0.0)
    if len(c) < 3:
        return list(c.index)
    distance = np.clip(1 - c.to_numpy(), 0, 2)
    np.fill_diagonal(distance, 0)
    z = linkage(squareform(distance, checks=False), method="average")
    return [c.index[i] for i in leaves_list(z)]


def blocs_correles(correlations, poids, seuil=SEUIL_BLOC):
    """Groupes de titres dont la corrélation moyenne dépasse `seuil` : chacun est
    en pratique UN seul pari. Renvoie (liste de blocs ≥ 2 titres, nombre total de blocs)."""
    c = correlations.fillna(0.0)
    if len(c) < 2:
        return [], len(c)
    distance = np.clip(1 - c.to_numpy(), 0, 2)
    np.fill_diagonal(distance, 0)
    z = linkage(squareform(distance, checks=False), method="average")
    etiquettes = fcluster(z, t=1 - seuil, criterion="distance")
    blocs = []
    for k in np.unique(etiquettes):
        membres = [c.index[i] for i in np.where(etiquettes == k)[0]]
        if len(membres) < 2:
            continue
        sous = c.loc[membres, membres].to_numpy()
        moyenne = float(sous[np.triu_indices(len(membres), 1)].mean())
        blocs.append({"tickers": membres, "poids": float(poids.reindex(membres).fillna(0).sum()),
                      "correlation": moyenne})
    blocs.sort(key=lambda b: b["poids"], reverse=True)
    return blocs, int(len(np.unique(etiquettes)))


def correlation_moyenne_ponderee(correlations, poids):
    """Σ_{i≠j} wᵢwⱼρᵢⱼ / Σ_{i≠j} wᵢwⱼ : la corrélation « typique » entre deux euros investis."""
    w = poids.reindex(correlations.index).fillna(0).to_numpy()
    c = correlations.fillna(0).to_numpy()
    produit = np.outer(w, w)
    np.fill_diagonal(produit, 0)
    return float((produit * c).sum() / produit.sum()) if produit.sum() > 0 else float("nan")


def ratio_diversification(rendements, poids):
    """Σ wᵢσᵢ / σₚ : 1 = aucune diversification ; plus il est élevé, plus les
    lignes se compensent."""
    w = poids.reindex(rendements.columns).fillna(0).to_numpy()
    cov = rendements.cov().to_numpy()
    vol_p = float(np.sqrt(w @ cov @ w))
    return float(w @ np.sqrt(np.diag(cov)) / vol_p) if vol_p > 0 else float("nan")


def paires_extremes(correlations, n=5):
    """Les n paires les plus corrélées."""
    c = correlations.where(np.triu(np.ones(correlations.shape, dtype=bool), 1))
    paires = c.stack().sort_values(ascending=False)
    return [(a, b, float(v)) for (a, b), v in paires.head(n).items()]


def diversifiants(rendements, poids, n=5):
    """Lignes les moins corrélées au RESTE du portefeuille (corrélation entre la
    ligne et le portefeuille sans elle)."""
    w = poids.reindex(rendements.columns).fillna(0)
    resultat = {}
    for t in rendements.columns:
        reste = w.drop(t)
        if reste.sum() <= 0:
            continue
        r_reste = rendements[reste.index] @ (reste / reste.sum())
        resultat[t] = float(np.corrcoef(rendements[t], r_reste)[0, 1])
    return pd.Series(resultat).sort_values().head(n)


def correlation_en_crise(rendements, poids, quantile=0.10, minimum=30):
    """Corrélation moyenne pondérée les jours où le portefeuille fait partie de
    ses 10 % pires journées (None si trop peu de jours)."""
    w = poids.reindex(rendements.columns).fillna(0)
    r_port = rendements @ (w / w.sum())
    jours = r_port[r_port <= r_port.quantile(quantile)].index
    if len(jours) < minimum:
        return None
    sous = rendements.loc[jours]
    sous = sous.loc[:, sous.std() > 0]
    return correlation_moyenne_ponderee(sous.corr(), w)


def correlations_par_groupe(rendements, poids, groupes):
    """Corrélations entre les rendements des sous-portefeuilles (un par groupe).

    groupes : Series ticker -> groupe (classe, région, secteur…)."""
    w = poids.reindex(rendements.columns).fillna(0)
    series = {}
    for nom, membres in groupes.reindex(rendements.columns).groupby(groupes.reindex(rendements.columns)):
        tickers = list(membres.index)
        wg = w[tickers]
        if wg.sum() <= 0:
            continue
        series[nom] = rendements[tickers] @ (wg / wg.sum())
    tableau = pd.DataFrame(series)
    poids_groupes = pd.Series({g: float(w[groupes.reindex(rendements.columns) == g].sum()) for g in tableau.columns})
    return tableau.corr(), poids_groupes


def diversification(prix_hist, positions):
    """Tous les indicateurs de diversification réelle."""
    tickers = [t for t in positions.index if t in prix_hist.columns]
    poids = (positions["valeur"] / positions["valeur"].sum()).reindex(tickers)
    rendements = rendements_quotidiens(prix_hist, tickers)
    rendements = rendements.loc[:, rendements.std() > 0]
    poids = poids.reindex(rendements.columns)
    corr = rendements.corr()
    blocs, nb_blocs = blocs_correles(corr, poids)
    return {
        "correlations": corr,
        "ordre": ordre_regroupement(corr),
        "poids": poids,
        "rendements": rendements,
        "moyenne": correlation_moyenne_ponderee(corr, poids),
        "ratio": ratio_diversification(rendements, poids),
        "blocs": blocs,
        "nb_blocs": nb_blocs,
        "paires": paires_extremes(corr),
        "diversifiants": diversifiants(rendements, poids),
        "crise": correlation_en_crise(rendements, poids),
        "nb_jours": len(rendements),
    }


def qualificatif(rho):
    a = abs(rho)
    return "très forte" if a >= 0.8 else "forte" if a >= 0.6 else "modérée" if a >= 0.3 else "faible"


# ======================================================================
# 5. Le diagnostic : constats, risques, pistes
# ======================================================================
# Seuils par famille de profil (prudent, équilibré, dynamique)
SEUILS = {
    "prudent":   {"devises": (0.30, 0.50), "emergents": (0.10, 0.20), "ligne": (0.05, 0.10),
                  "duration": (5.0, 8.0)},
    "equilibre": {"devises": (0.50, 0.70), "emergents": (0.20, 0.30), "ligne": (0.07, 0.10),
                  "duration": (7.0, 10.0)},
    "dynamique": {"devises": (0.70, 0.85), "emergents": (0.25, 0.40), "ligne": (0.10, 0.15),
                  "duration": (8.0, 12.0)},
}
PROFILS = ["Prudent", "Équilibré", "Dynamique"]       # choix proposés dans l'onglet « Expositions »
FAMILLE_PROFIL = {"Prudent": "prudent", "Équilibré": "equilibre", "Dynamique": "dynamique"}
DIMENSIONS = ["geographie", "secteurs", "devises", "concentration", "taux", "diversification"]
NIVEAUX = ["ok", "attention", "alerte"]


def _niveau(valeur, seuils):
    return "alerte" if valeur > seuils[1] else "attention" if valeur > seuils[0] else "ok"


def _constat(dimension, niveau, titre, risque="", pistes=(), **valeurs):
    """Un constat : textes en français (clés de traduction) + valeurs à insérer."""
    return {"dimension": dimension, "niveau": niveau, "titre": titre, "risque": risque,
            "pistes": list(pistes), "valeurs": valeurs}


def diagnostic(positions, transp, div=None, profil="Équilibré", f_pct=None, f_nom=None, doublons=None):
    """Liste des constats, du plus grave au moins grave.

    f_pct, f_nom : fonctions de mise en forme (pourcentage, nom de pays ou de
    secteur traduit). Les textes restent en français : ce sont des clés de
    traduction, traduites à l'affichage avec leurs valeurs."""
    f_pct = f_pct or (lambda x: f"{x * 100:.0f} %")
    f_nom = f_nom or (lambda x: x)
    s = SEUILS[FAMILLE_PROFIL.get(profil, "equilibre")]
    constats = []
    actions = transp[transp["classe"] == "Actions"]
    part_actions = actions["poids"].sum()

    # --- Géographie (poche actions, comparée au marché mondial MSCI ACWI) ---
    if part_actions > 0.05:
        pays = repartition(transp, "pays", "Actions", normaliser=True).drop(NON_CLASSE, errors="ignore")
        monde = ce.pays_de("MSCI ACWI")
        for nom_pays, poids in pays.head(3).items():
            ecart = poids - monde.get(nom_pays, 0)
            if ecart > 0.25 or (nom_pays != "États-Unis" and poids > 0.40):
                constats.append(_constat(
                    "geographie", "alerte", "{pays} pèse {poids} de la poche actions ({monde} dans le marché mondial).",
                    "Votre performance dépend fortement de l'économie, de la politique et de la monnaie d'un seul "
                    "pays. Un choc local (récession, élection, réglementation) toucherait une grande partie du "
                    "portefeuille.",
                    ["Diversifier une partie de cette poche avec un ETF monde (MSCI World ou ACWI).",
                     "Renforcer les zones sous-représentées plutôt que de vendre, si la fiscalité l'impose."],
                    pays=f_nom(nom_pays), poids=f_pct(poids), monde=f_pct(monde.get(nom_pays, 0))))
            elif ecart > 0.15:
                constats.append(_constat(
                    "geographie", "attention", "{pays} pèse {poids} de la poche actions ({monde} dans le marché mondial).",
                    "Surpondération marquée d'un pays par rapport au marché mondial.",
                    ["Vérifier que ce choix est volontaire (conviction, biais domestique)."],
                    pays=f_nom(nom_pays), poids=f_pct(poids), monde=f_pct(monde.get(nom_pays, 0))))
        france = pays.get("France", 0)
        if france > 0.15 and france > 4 * monde.get("France", 0):
            constats.append(_constat(
                "geographie", "attention", "Biais domestique : la France représente {poids} de la poche actions.",
                "Les investisseurs surpondèrent souvent leur propre pays : le patrimoine (emploi, immobilier) "
                "est alors déjà exposé à la même économie.",
                ["Un ETF monde éligible au PEA permet de garder l'enveloppe tout en diversifiant."],
                poids=f_pct(france)))
        emergents = repartition(transp, "region", "Actions", normaliser=True).get("Émergents", 0)
        if emergents > s["emergents"][0]:
            constats.append(_constat(
                "geographie", _niveau(emergents, s["emergents"]),
                "Les pays émergents représentent {poids} de la poche actions.",
                "Marchés plus volatils, avec des risques politiques, de gouvernance et de change plus élevés.",
                ["Limiter cette poche selon le profil, ou la faire porter par un ETF large plutôt que par "
                 "quelques titres."], poids=f_pct(emergents)))
        if not any(c["dimension"] == "geographie" for c in constats):
            top = pays.index[0] if len(pays) else "—"
            constats.append(_constat("geographie", "ok", "Répartition géographique proche du marché mondial "
                                     "(premier pays : {pays}, {poids}).",
                                     pays=f_nom(top), poids=f_pct(pays.iloc[0] if len(pays) else 0)))

        # --- Secteurs ---
        secteurs = repartition(transp, "secteur", "Actions", normaliser=True).drop(NON_CLASSE, errors="ignore")
        ref = ce.secteurs_de("MSCI ACWI")
        alerte_secteur = False
        for nom_sect, poids in secteurs.head(3).items():
            ecart = poids - ref.get(nom_sect, 0)
            if poids > 0.40 or ecart > 0.15:
                niveau = "alerte"
            elif poids > 0.30 or ecart > 0.08:
                niveau = "attention"
            else:
                continue
            alerte_secteur = True
            constats.append(_constat(
                "secteurs", niveau, "Le secteur {secteur} pèse {poids} de la poche actions ({monde} dans le "
                "marché mondial).",
                "Le portefeuille dépend d'un seul cycle économique : un retournement du secteur (valorisations, "
                "taux, réglementation) pèserait lourd sur la performance.",
                ["Équilibrer avec des secteurs peu représentés, notamment défensifs (santé, consommation de "
                 "base, services publics).", "Un ETF monde équipondéré ou sectoriel peut corriger le biais."],
                secteur=f_nom(nom_sect), poids=f_pct(poids), monde=f_pct(ref.get(nom_sect, 0))))
        defensifs = sum(secteurs.get(x, 0) for x in ["Santé", "Consommation de base", "Services publics"])
        if len(secteurs) and defensifs < 0.10:
            constats.append(_constat(
                "secteurs", "attention", "Peu de secteurs défensifs : {poids} (santé, consommation de base, "
                "services publics).",
                "Ces secteurs amortissent généralement les baisses de marché : sans eux, le portefeuille "
                "souffre davantage en récession.",
                ["Ajouter une poche défensive pour lisser les baisses."], poids=f_pct(defensifs)))
            alerte_secteur = True
        if not alerte_secteur and len(secteurs):
            constats.append(_constat("secteurs", "ok", "Répartition sectorielle équilibrée (premier secteur : "
                                     "{secteur}, {poids}).", secteur=f_nom(secteurs.index[0]),
                                     poids=f_pct(secteurs.iloc[0])))

    # --- Devises (tout le portefeuille) ---
    devises = repartition(transp, "devise")
    hors_euro = float(devises.drop(["EUR", "Or"], errors="ignore").sum())
    if hors_euro > s["devises"][0]:
        principale = devises.drop(["EUR", "Or"], errors="ignore")
        constats.append(_constat(
            "devises", _niveau(hors_euro, s["devises"]),
            "{poids} du portefeuille est exposé à des devises étrangères, dont {devise} pour {poids_devise}.",
            "Une baisse de ces devises face à l'euro réduit la performance, même si les titres montent : "
            "une baisse de 10 % du dollar coûterait environ {perte} au portefeuille.",
            ["Pour une partie de la poche, choisir des ETF couverts en euros (« EUR Hedged »).",
             "Le risque de change diversifie aussi : le dollar monte souvent en période de crise. Couvrir "
             "partiellement est un compromis courant."],
            poids=f_pct(hors_euro), devise=principale.index[0], poids_devise=f_pct(principale.iloc[0]),
            perte=f_pct(devises.get("USD", 0) * 0.10)))
    else:
        constats.append(_constat("devises", "ok", "Risque de change limité : {poids} hors euro.",
                                 poids=f_pct(hors_euro)))

    # --- Concentration ---
    conc = concentration(positions, transp)
    grosse = conc["plus_grosse_action"]
    if grosse and grosse[1] > s["ligne"][0]:
        constats.append(_constat(
            "concentration", _niveau(grosse[1], s["ligne"]),
            "Une seule action, {nom}, représente {poids} du portefeuille.",
            "Le risque propre à une entreprise (résultats, procès, scandale) n'est pas diversifié : une chute "
            "de 30 % de ce titre coûterait {perte} au portefeuille.",
            ["Réduire la ligne progressivement ou la compléter par des titres du même secteur.",
             "Repère réglementaire : un fonds UCITS ne peut pas dépasser 10 % sur un émetteur."],
            nom=positions.at[grosse[0], "nom"], poids=f_pct(grosse[1]), perte=f_pct(grosse[1] * 0.30)))
    if conc["actions_plus_5"] > 0.40:
        constats.append(_constat(
            "concentration", "alerte", "Les {n} actions de plus de 5 % totalisent {poids} (règle 5/10/40 dépassée).",
            "Règle des fonds UCITS : les lignes de plus de 5 % ne doivent pas dépasser 40 % au total. "
            "Au-delà, le portefeuille dépend de quelques entreprises.",
            ["Ramener certaines lignes sous 5 % ou ajouter des ETF diversifiés."],
            n=conc["nb_actions_plus_5"], poids=f_pct(conc["actions_plus_5"])))
    if doublons:
        noms = ", ".join(d["nom"] for d in doublons[:4]) + ("…" if len(doublons) > 4 else "")
        constats.append(_constat(
            "concentration", "attention", "{noms} : détenu(s) en direct ET probablement aussi via votre ETF {indice}.",
            "L'exposition réelle à ces entreprises est plus forte que leur seule ligne ne le laisse penser.",
            ["En tenir compte avant de renforcer ces lignes."], noms=noms, indice=doublons[0]["indice"]))
    if not any(c["dimension"] == "concentration" for c in constats):
        constats.append(_constat("concentration", "ok", "Aucune ligne trop concentrée ({n} lignes, équivalent à "
                                 "{eff} lignes de même poids).", n=conc["nb_lignes"],
                                 eff=f"{conc['nb_effectif']:.0f}"))

    # --- Taux ---
    tx = taux(positions)
    if tx:
        constats.append(_constat(
            "taux", _niveau(tx["duration"], s["duration"]),
            "Duration moyenne des obligations : {duration} ans. Une hausse des taux de 1 point coûterait "
            "environ {perte} au portefeuille.",
            "Plus la duration est longue, plus le prix des obligations baisse quand les taux montent "
            "(et monte quand ils baissent)." if tx["duration"] > s["duration"][0] else "",
            ["Raccourcir la duration (obligations 1-3 ans) pour réduire la sensibilité aux taux."]
            if tx["duration"] > s["duration"][0] else [],
            duration=f"{tx['duration']:.1f}".replace(".", ","), perte=f_pct(tx["perte_1pt_pct"])))

    # --- Diversification réelle (corrélations) ---
    if div is not None:
        for bloc in div["blocs"][:3]:
            if bloc["poids"] < 0.15 or len(bloc["tickers"]) < 2:
                continue
            noms = ", ".join(str(positions.at[t, "nom"]) for t in bloc["tickers"][:4]) + \
                ("…" if len(bloc["tickers"]) > 4 else "")
            constats.append(_constat(
                "diversification", "alerte" if bloc["poids"] >= 0.25 else "attention",
                "{n} lignes très corrélées entre elles ({rho} en moyenne) pèsent {poids} : {noms}. "
                "{n} lignes, mais en pratique un seul pari.",
                "La diversification n'est qu'apparente : ces titres baissent ensemble.",
                ["Remplacer une partie de ce bloc par des actifs peu corrélés (autres secteurs, obligations, or).",
                 "Ou regrouper ces lignes dans un seul ETF du même thème, moins risqué."],
                n=len(bloc["tickers"]), rho=f"{bloc['correlation']:.2f}".replace(".", ","),
                poids=f_pct(bloc["poids"]), noms=noms))
        moyenne = div["moyenne"]
        if moyenne == moyenne and moyenne > 0.45:
            constats.append(_constat(
                "diversification", "alerte" if moyenne > 0.6 else "attention",
                "Corrélation moyenne élevée entre les lignes : {rho}.",
                "Les lignes évoluent dans le même sens : le portefeuille se comporte presque comme un seul actif.",
                ["Ajouter des classes d'actifs différentes (obligations, or) ou d'autres zones."],
                rho=f"{moyenne:.2f}".replace(".", ",")))
        if div["crise"] is not None and moyenne == moyenne and div["crise"] > moyenne + 0.10:
            constats.append(_constat(
                "diversification", "attention",
                "Les jours de forte baisse, la corrélation moyenne monte à {crise} (contre {rho} en temps normal).",
                "La diversification protège moins quand on en a le plus besoin : c'est typique des crises.",
                ["Voir les stress tests (espace « Conseil patrimonial ») pour mesurer l'impact d'une crise."],
                crise=f"{div['crise']:.2f}".replace(".", ","), rho=f"{moyenne:.2f}".replace(".", ",")))
        amortisseurs = div["diversifiants"][div["diversifiants"] < 0.2]
        poids_amort = float(div["poids"].reindex(amortisseurs.index).sum())
        if poids_amort >= 0.05:
            noms = ", ".join(str(positions.at[t, "nom"]) for t in amortisseurs.index[:3])
            constats.append(_constat(
                "diversification", "ok", "Amortisseurs présents : {noms} ({poids}) évoluent peu avec le reste "
                "du portefeuille.", noms=noms, poids=f_pct(poids_amort)))
        if not any(c["dimension"] == "diversification" and c["niveau"] != "ok" for c in constats):
            constats.append(_constat(
                "diversification", "ok", "Diversification réelle satisfaisante : {blocs} blocs indépendants pour "
                "{n} lignes, ratio de diversification {ratio}.", blocs=div["nb_blocs"], n=len(div["poids"]),
                ratio=f"{div['ratio']:.2f}".replace(".", ",")))

    ordre = {"alerte": 0, "attention": 1, "ok": 2}
    constats.sort(key=lambda c: (ordre[c["niveau"]], DIMENSIONS.index(c["dimension"])))
    return constats


def synthese(constats):
    """Niveau de chaque dimension : le plus grave de ses constats (None si non concernée)."""
    resultat = {}
    for d in DIMENSIONS:
        niveaux = [c["niveau"] for c in constats if c["dimension"] == d]
        resultat[d] = max(niveaux, key=NIVEAUX.index) if niveaux else None
    return resultat
