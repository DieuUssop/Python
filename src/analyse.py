"""
analyse.py — Toute l'analyse du portefeuille en UNE fonction.

Cette fonction enchaîne les étapes 1 à 5 (+ les devises de l'étape 8) :
    transactions -> devises -> cours -> conversion en euros
                 -> valorisation -> historique -> indicateurs

Elle est utilisée par le tableau de bord (app.py) et par main.py. Elle ne
contient aucun affichage : elle renvoie seulement des résultats. Avantage :
on peut la tester sans lancer l'interface.
"""

from pathlib import Path

import pandas as pd

from . import config
from .devises import (convertir_cours, convertir_prix_historiques, convertir_transactions,
                      detecter_devises, devises_etrangeres, ticker_change)
from .market_data import obtenir_cours, obtenir_historique
from .metrics import (calculer_indicateurs, calculer_indicateurs_avances,
                      matrice_correlation)
from .portfolio import Portfolio


CHEMIN_REFERENTIEL = Path(__file__).resolve().parent.parent / "data" / "referentiel.csv"


def charger_referentiel():
    """Région, secteur et pays de chaque titre (fichier data/referentiel.csv).
    Renvoie un tableau vide si le fichier n'existe pas."""
    if not CHEMIN_REFERENTIEL.exists():
        return pd.DataFrame(columns=["region", "secteur", "pays"])
    return pd.read_csv(CHEMIN_REFERENTIEL).set_index("ticker")


def analyse_complete(source_csv,
                     indice=config.INDICE_REFERENCE,
                     taux_sans_risque=config.TAUX_SANS_RISQUE,
                     niveau_var=config.NIVEAU_CONFIANCE_VAR):
    """Lance toute l'analyse et renvoie un dictionnaire de résultats.

    source_csv : chemin du fichier de transactions, ou fichier déjà ouvert
                 (par exemple un fichier envoyé depuis le tableau de bord).
    """
    # Étape 1 : les transactions, telles que saisies (vérification du fichier)
    brut = Portfolio(source_csv)
    titres = brut.tous_les_tickers()
    tous = titres + ([indice] if indice not in titres else [])

    # Étape 8 : devise de chaque titre et taux de change nécessaires
    info_devises = detecter_devises(tous)
    etrangeres = devises_etrangeres(info_devises)
    tickers_change = [ticker_change(d) for d in etrangeres]

    # Étape 3 : historique des cours (titres + indice + taux de change, en un seul
    # téléchargement : le cache hors ligne contient ainsi tout le nécessaire)
    prix_hist_brut, source_hist = obtenir_historique(tous + tickers_change, brut.date_debut())
    if indice not in prix_hist_brut.columns:
        raise ValueError(f"Impossible de récupérer l'historique de l'indice {indice}.")
    manquants = [t for t in tickers_change if t not in prix_hist_brut.columns]
    if manquants:
        raise ValueError(f"Taux de change introuvables : {manquants}")

    taux_hist = prix_hist_brut[tickers_change].copy()
    taux_hist.columns = etrangeres
    # On ne garde que les jours où au moins un titre a coté (les marchés des
    # changes cotent aussi certains jours fériés boursiers).
    colonnes_titres = [c for c in tous if c in prix_hist_brut.columns]
    prix_hist = prix_hist_brut[colonnes_titres].dropna(how="all")

    # Conversion en euros (si nécessaire) des transactions et des cours passés
    if etrangeres:
        portefeuille = Portfolio(convertir_transactions(brut.transactions, info_devises, taux_hist))
        prix_hist = convertir_prix_historiques(prix_hist, info_devises, taux_hist)
    else:
        portefeuille = brut

    # Étape 2 : cours actuels (et taux de change actuels), puis valorisation
    prix, source_cours = obtenir_cours(portefeuille.tickers() + tickers_change)
    taux_actuels = {d: prix.pop(t) for d, t in zip(etrangeres, tickers_change) if t in prix}
    if len(taux_actuels) < len(etrangeres):
        raise ValueError("Taux de change actuels introuvables.")
    prix = convertir_cours(prix, info_devises, taux_actuels)
    positions = portefeuille.valoriser(prix)
    positions["devise"] = [info_devises.get(t, ("EUR", 1.0))[0] for t in positions.index]
    # Classement de chaque ligne (utile pour un portefeuille très diversifié)
    referentiel = charger_referentiel()
    for colonne in ["region", "secteur", "pays"]:
        positions[colonne] = positions.index.map(referentiel[colonne].to_dict()).fillna("Non classé") \
            if colonne in referentiel.columns else "Non classé"
    resume = portefeuille.resume_valorise(prix)

    # Étape 3 (suite) : historique du portefeuille, en euros
    histo = portefeuille.historique(prix_hist)

    # Étapes 4 et 5 : indicateurs
    indicateurs = calculer_indicateurs(histo)
    avances = calculer_indicateurs_avances(
        histo, indicateurs["rendements"], prix_hist[indice], taux_sans_risque, niveau_var
    )
    correlations = matrice_correlation(prix_hist, portefeuille.tickers())

    return {
        "transactions": portefeuille.transactions,
        "positions": positions,
        "resume": resume,
        "historique": histo,
        "indicateurs": indicateurs,
        "avances": avances,
        "correlations": correlations,
        "prix_hist": prix_hist,
        "valeur_par_titre": portefeuille.valeur_par_titre,
        "date_ouverture": portefeuille.date_debut(),
        "devises": info_devises,
        "taux_actuels": taux_actuels,
        "source_cours": source_cours,
        "source_historique": source_hist,
    }
