"""
mouvements.py — Ajouter de nouvelles opérations à un portefeuille existant.

Au lieu de renvoyer tout l'historique modifié, l'utilisateur envoie seulement
ses nouveaux mouvements (un avis d'opéré PDF, un export Excel des dernières
opérations, ou une saisie à la main). Ce module :

    1. repère les DOUBLONS : opération déjà présente (même date, même titre, même
       type, même quantité, prix à 0,5 % près) — cas d'un relevé qui chevauche
       l'ancien ; ils sont exclus par défaut ;
    2. CONTRÔLE la cohérence : vente de plus de titres que ceux détenus à cette
       date (bloquant), date dans le futur, quantité ou prix nul ;
    3. FUSIONNE l'ancien et le nouveau, trié par date.

Ajouter deux fois le même fichier ne change donc rien (les opérations sont
reconnues comme déjà présentes).
"""

import pandas as pd

COLONNES = ["date", "type", "ticker", "nom", "quantite", "prix", "frais"]
TOLERANCE_PRIX = 0.005
ORDRE_TYPES = {"ACHAT": 0, "DIVIDENDE": 1, "VENTE": 2}       # le même jour : achat avant vente


def lire(contenu):
    """Fichier au format du projet (octets ou DataFrame) -> tableau standard."""
    if isinstance(contenu, pd.DataFrame):
        tableau = contenu.copy()
    else:
        import io
        tableau = pd.read_csv(io.BytesIO(contenu) if isinstance(contenu, bytes) else io.StringIO(contenu))
    for c in COLONNES:
        if c not in tableau.columns:
            tableau[c] = "" if c in ("nom",) else 0.0
    tableau = tableau[COLONNES].copy()
    tableau["date"] = pd.to_datetime(tableau["date"])
    tableau["type"] = tableau["type"].astype(str).str.upper().str.strip()
    tableau["ticker"] = tableau["ticker"].astype(str).str.strip()
    for c in ["quantite", "prix", "frais"]:
        tableau[c] = pd.to_numeric(tableau[c], errors="coerce").fillna(0.0).astype(float)
    tableau["nom"] = tableau["nom"].fillna("").astype(str)
    return tableau


def en_csv(tableau):
    sortie = tableau[COLONNES].copy()
    sortie["date"] = pd.to_datetime(sortie["date"]).dt.strftime("%Y-%m-%d")
    return sortie.to_csv(index=False, float_format="%.6g").encode("utf-8")


def _trier(tableau):
    t = tableau.assign(_ordre=tableau["type"].map(ORDRE_TYPES).fillna(1))
    return t.sort_values(["date", "_ordre"], kind="stable").drop(columns="_ordre").reset_index(drop=True)


def _meme_operation(a, b):
    if a["date"] != b["date"] or a["ticker"] != b["ticker"] or a["type"] != b["type"]:
        return False
    if abs(a["quantite"] - b["quantite"]) > 1e-6:
        return False
    reference = max(abs(a["prix"]), abs(b["prix"]), 1e-9)
    return abs(a["prix"] - b["prix"]) / reference <= TOLERANCE_PRIX


def reperer_doublons(existant, nouvelles):
    """Série booléenne (index des nouvelles) : vrai si l'opération est déjà dans l'existant
    (ou en double dans les nouvelles elles-mêmes)."""
    deja = []
    vues = []
    par_cle = {}
    for _, e in existant.iterrows():
        par_cle.setdefault((e["date"], e["ticker"], e["type"]), []).append(e)
    for i, n in nouvelles.iterrows():
        candidats = par_cle.get((n["date"], n["ticker"], n["type"]), []) + vues
        doublon = any(_meme_operation(n, c) for c in candidats)
        deja.append(doublon)
        if not doublon:
            vues.append(n)
    return pd.Series(deja, index=nouvelles.index, dtype=bool)


def controler(fusion, aujourdhui=None):
    """Contrôles de cohérence sur le portefeuille fusionné.

    Renvoie une liste d'alertes : {"bloquant", "message", "valeurs", "ticker", "date"}.
    Les messages sont en français (clés de traduction)."""
    aujourdhui = pd.Timestamp(aujourdhui or pd.Timestamp.today().normalize())
    alertes = []
    for _, ligne in fusion[fusion["date"] > aujourdhui].iterrows():
        alertes.append({"bloquant": True, "ticker": ligne["ticker"], "date": ligne["date"],
                        "message": "Opération datée dans le futur : {titre}, le {date}.",
                        "valeurs": {"titre": ligne["nom"] or ligne["ticker"],
                                    "date": ligne["date"].strftime("%d/%m/%Y")}})
    for _, ligne in fusion[(fusion["type"] != "DIVIDENDE") & ((fusion["quantite"] <= 0) | (fusion["prix"] <= 0))].iterrows():
        alertes.append({"bloquant": True, "ticker": ligne["ticker"], "date": ligne["date"],
                        "message": "Quantité ou prix nul pour {titre}, le {date}.",
                        "valeurs": {"titre": ligne["nom"] or ligne["ticker"],
                                    "date": ligne["date"].strftime("%d/%m/%Y")}})
    detenu = {}
    for _, ligne in _trier(fusion).iterrows():
        signe = {"ACHAT": 1, "VENTE": -1}.get(ligne["type"], 0)
        detenu[ligne["ticker"]] = detenu.get(ligne["ticker"], 0.0) + signe * ligne["quantite"]
        if detenu[ligne["ticker"]] < -1e-6:
            alertes.append({"bloquant": True, "ticker": ligne["ticker"], "date": ligne["date"],
                            "message": "Vente de {quantite} {titre} le {date}, mais seulement {detenu} détenu(s) "
                                       "à cette date.",
                            "valeurs": {"titre": ligne["nom"] or ligne["ticker"], "quantite": f"{ligne['quantite']:g}",
                                        "date": ligne["date"].strftime("%d/%m/%Y"),
                                        "detenu": f"{detenu[ligne['ticker']] + ligne['quantite']:g}"}})
            detenu[ligne["ticker"]] = 0.0
    return alertes


def preparer(existant, nouvelles):
    """Analyse des nouvelles opérations avant enregistrement.

    Renvoie (nouvelles avec les colonnes « inclure » et « statut », alertes)."""
    existant, nouvelles = lire(existant), lire(nouvelles)
    doublons = reperer_doublons(existant, nouvelles)
    nouvelles = nouvelles.assign(inclure=~doublons,
                                 statut=["déjà dans le portefeuille" if d else "nouvelle" for d in doublons])
    return nouvelles, controler(fusionner(existant, nouvelles))


def fusionner(existant, nouvelles):
    """Ancien + nouvelles opérations retenues (colonne « inclure » si présente), triées par date."""
    existant, retenues = lire(existant), nouvelles
    if "inclure" in retenues.columns:
        retenues = retenues[retenues["inclure"].astype(bool)]
    retenues = lire(retenues[COLONNES])
    return _trier(pd.concat([existant, retenues], ignore_index=True))


def fusionner_operations(existant, nouvelles):
    """Fonction tout-en-un : (fusion, doublons exclus, alertes)."""
    preparees, alertes = preparer(existant, nouvelles)
    return fusionner(existant, preparees), preparees[~preparees["inclure"]], alertes


# ======================================================================
# Modifier ou supprimer des opérations existantes (onglet « Transactions »)
# ======================================================================
CHAMPS_MODIFIABLES = ["date", "quantite", "prix", "frais"]


def appliquer_modifications(source, edite):
    """Applique les modifications faites dans le tableau éditable.

    source : le fichier du portefeuille (octets ou tableau), lignes numérotées dans l'ordre du fichier ;
    edite  : tableau édité, indexé par le numéro de ligne d'origine, avec les colonnes modifiables
             et une colonne booléenne « supprimer ». Les lignes absentes (filtrées) sont inchangées.

    Renvoie (nouveau tableau trié par date, supprimées, corrections) où corrections est une liste
    de dictionnaires {ligne, champ, avant, apres}."""
    source = lire(source)
    nouveau = source.copy()
    a_supprimer = []
    corrections = []
    for ligne, valeurs in edite.iterrows():
        if ligne not in nouveau.index:
            continue
        if bool(valeurs.get("supprimer", False)):
            a_supprimer.append(ligne)
            continue
        for champ in CHAMPS_MODIFIABLES:
            if champ not in valeurs.index:
                continue
            avant, apres = nouveau.at[ligne, champ], valeurs[champ]
            if champ == "date":
                apres = pd.Timestamp(apres)
                change = pd.Timestamp(avant).normalize() != apres.normalize()
            else:
                apres = float(apres) if apres == apres and apres is not None else 0.0
                change = abs(float(avant) - apres) > 1e-9
            if change:
                corrections.append({"ligne": ligne, "champ": champ, "avant": avant, "apres": apres})
                nouveau.at[ligne, champ] = apres
    supprimees = source.loc[a_supprimer]
    nouveau = nouveau.drop(index=a_supprimer)
    return _trier(nouveau), supprimees, corrections


def positions_finales(tableau):
    """Quantité détenue à la fin, par titre."""
    signe = tableau["type"].map({"ACHAT": 1, "VENTE": -1}).fillna(0)
    return (signe * tableau["quantite"]).groupby(tableau["ticker"]).sum()


def titres_disparus(avant, apres):
    """Titres détenus avant la modification et qui ne le sont plus après."""
    q_avant, q_apres = positions_finales(lire(avant)), positions_finales(lire(apres))
    return [t for t in q_avant.index if q_avant[t] > 1e-6 and q_apres.get(t, 0) <= 1e-6]


# ======================================================================
# Division ou regroupement d'actions (avis d'opération sur titres)
# ======================================================================
def appliquer_division(source, ticker, date, facteur):
    """Ramène les opérations d'un titre antérieures à une division (ou à un regroupement) dans
    les unités d'après : quantité × facteur, prix ÷ facteur (les cours de Yahoo Finance sont
    eux-mêmes ajustés de cette façon). Les dividendes (montants totaux) ne changent pas.
    Renvoie (nouveau tableau, nombre d'opérations ajustées)."""
    tableau = lire(source)
    date = pd.Timestamp(date)
    concernees = (tableau["ticker"] == ticker) & (tableau["date"] < date) & tableau["type"].isin(["ACHAT", "VENTE"])
    tableau.loc[concernees, "quantite"] = tableau.loc[concernees, "quantite"] * facteur
    tableau.loc[concernees, "prix"] = tableau.loc[concernees, "prix"] / facteur
    return tableau, int(concernees.sum())
