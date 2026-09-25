"""
generer_portefeuille_diversifie.py — Construit l'historique d'un portefeuille
DIVERSIFIÉ (multi-actifs) géré depuis janvier 2017 pour un client "Équilibré".

Le fichier produit (data/transactions_diversifie.csv) NE REMPLACE PAS ton
fichier data/transactions.csv : c'est un portefeuille de plus, que tu peux
choisir dans le tableau de bord ou analyser avec :
    python main.py data/transactions_diversifie.csv

La politique de gestion simulée (typique d'un mandat "Équilibré") :
    1. ALLOCATION STRATÉGIQUE : 60 % actions, 35 % obligations, 5 % or.
       - Actions : 39 sociétés, toutes les grandes régions du monde et les
         11 secteurs ; dans chaque région, les titres sont équipondérés.
       - Obligations : 10 fonds indiciels (ETF) : emprunts d'État de la zone
         euro et des États-Unis (courts, moyens, longs), obligations indexées
         sur l'inflation, obligations d'entreprises, haut rendement, émergents.
       - Or : un titre adossé à de l'or physique (Xetra-Gold).
    2. INVESTISSEMENT INITIAL de 500 000 € le 16/01/2017 (près de 10 ans
       d'historique : on dépasse les 5 ans du PEA et les 8 ans de
       l'assurance-vie, et on traverse le Covid et la hausse des taux de 2022).
    3. Chaque trimestre : VERSEMENT de 10 000 € et RÉÉQUILIBRAGE vers
       l'allocation cible (on ne touche pas une ligne proche de sa cible).
    4. DIVIDENDES et COUPONS : les vrais montants versés par chaque titre
       (les coupons des fonds obligataires sont versés comme des dividendes).

Les prix sont les VRAIS cours de clôture (Yahoo Finance), dans la devise de
cotation de chaque titre : le programme les convertit en euros lors de l'analyse.

Lancement (depuis le dossier portfolio_tracker, avec Internet) :
    python generer_portefeuille_diversifie.py
"""

import pandas as pd

from generer_portefeuille_mondial import dividendes, telecharger_cours
from src.devises import detecter_devises, devises_etrangeres, ticker_change
from src.portfolio import Portfolio

FICHIER_REFERENTIEL = "data/referentiel.csv"
FICHIER_SORTIE = "data/transactions_diversifie.csv"

DATE_DEBUT = "2017-01-16"
CAPITAL_INITIAL = 500_000            # euros
VERSEMENT_TRIMESTRIEL = 10_000       # euros
SEUIL_REEQUILIBRAGE = 0.10           # on ne touche pas une ligne à moins de 10 % de sa cible

# ----------------------------------------------------------------------
# Allocation cible
# ----------------------------------------------------------------------
# ACTIONS (60 %) : poids de chaque région, puis titres équipondérés dans la région
ACTIONS = {
    "États-Unis": (0.30, ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "JPM", "V", "UNH",
                          "JNJ", "PG", "KO", "XOM", "CAT", "NEE", "LIN", "PLD"]),
    "Europe": (0.12, ["MC.PA", "TTE.PA", "SAN.PA", "AI.PA", "SU.PA", "ASML.AS", "SAP.DE",
                      "ALV.DE", "IBE.MC"]),
    "Royaume-Uni": (0.04, ["AZN.L", "HSBA.L", "ULVR.L"]),
    "Suisse": (0.03, ["NESN.SW", "ROG.SW"]),
    "Japon": (0.04, ["7203.T", "8306.T", "6861.T"]),
    "Asie-Pacifique": (0.02, ["BHP.AX", "0700.HK"]),
    "Canada": (0.02, ["RY.TO", "CNQ.TO"]),
    "Émergents": (0.03, ["TSM", "INFY"]),
}
# OBLIGATIONS (35 %) : poids de chaque fonds
OBLIGATIONS = {
    "IBCA.DE": 0.04,   # États zone euro 1-3 ans (peu sensible aux taux)
    "EUNH.DE": 0.08,   # États zone euro, toutes maturités
    "IBCI.DE": 0.03,   # États zone euro indexés sur l'inflation
    "EUN5.DE": 0.06,   # Entreprises zone euro, bien notées
    "EUNW.DE": 0.02,   # Entreprises zone euro, haut rendement
    "IEF": 0.03,       # États-Unis 7-10 ans
    "TLT": 0.02,       # États-Unis 20 ans et plus (très sensible aux taux)
    "TIP": 0.02,       # États-Unis indexés sur l'inflation
    "LQD": 0.02,       # Entreprises américaines bien notées
    "EMB": 0.03,       # Dettes des pays émergents (en dollars)
}
# OR (5 %)
OR = {"4GLD.DE": 0.05}


def poids_cibles():
    """Poids cible de chaque ligne (la somme fait 100 %)."""
    poids = {}
    for poids_region, titres in ACTIONS.values():
        for t in titres:
            poids[t] = poids_region / len(titres)
    poids.update(OBLIGATIONS)
    poids.update(OR)
    return poids


def frais_courtage(montant):
    """Barème d'une banque privée : 0,10 % du montant, minimum 5 €."""
    return round(max(5.0, 0.001 * montant), 2)


def dates_de_gestion(calendrier):
    """Date initiale, puis premier jour de bourse de chaque trimestre."""
    debut = calendrier[calendrier >= pd.Timestamp(DATE_DEBUT)][0]
    dates = [debut]
    for trimestre in pd.date_range(debut, calendrier[-1], freq="QS"):
        suivants = calendrier[calendrier >= trimestre]
        if len(suivants) and suivants[0] > debut:
            dates.append(suivants[0])
    return sorted(set(dates))


def main():
    # 1. L'univers et les poids cibles
    poids = poids_cibles()
    ref = pd.read_csv(FICHIER_REFERENTIEL).set_index("ticker")
    absents = [t for t in poids if t not in ref.index]
    if absents:
        raise SystemExit(f"❌ Titres absents de {FICHIER_REFERENTIEL} : {absents}")
    tickers = list(poids)
    noms = ref["nom"].to_dict()
    classes = ref.loc[tickers, "classe"].value_counts()
    print(f"⏳ Univers : {len(tickers)} lignes ("
          + ", ".join(f"{n} {c.lower()}" for c, n in classes.items()) + ")")

    # 2. Devises et cours (titres + taux de change), en un seul téléchargement
    info = detecter_devises(tickers)
    etrangeres = devises_etrangeres(info)
    tickers_change = [ticker_change(d) for d in etrangeres]
    print(f"⏳ Téléchargement de 10 ans de cours et de {len(etrangeres)} taux de change "
          f"({', '.join(etrangeres)})... (1 à 2 minutes)")
    debut_telechargement = (pd.Timestamp(DATE_DEBUT) - pd.Timedelta(days=10)).strftime("%Y-%m-%d")
    cours = telecharger_cours(tickers + tickers_change, debut_telechargement)

    manquants = [t for t in tickers if t not in cours.columns or cours[t].dropna().empty]
    if manquants:
        print(f"⚠️  Titres introuvables, retirés : {manquants} (les autres poids sont ajustés)")
        tickers = [t for t in tickers if t not in manquants]
    total = sum(poids[t] for t in tickers)
    poids = {t: poids[t] / total for t in tickers}

    cours = cours.ffill()
    calendrier = cours.index

    def prix_euros(t, d):
        devise, facteur = info[t]
        taux = 1.0 if devise == "EUR" else cours.at[d, ticker_change(devise)]
        return cours.at[d, t] * facteur / taux

    # 3. Investissement initial, puis versements et rééquilibrages trimestriels
    quantites = {t: 0 for t in tickers}
    lignes = []
    dates = dates_de_gestion(calendrier)
    for numero, d in enumerate(dates):
        apport = CAPITAL_INITIAL if numero == 0 else VERSEMENT_TRIMESTRIEL
        disponibles = [t for t in tickers if pd.notna(cours.at[d, t])]
        valeur = sum(quantites[t] * prix_euros(t, d) for t in disponibles)
        total = valeur + apport
        for t in disponibles:
            pe = prix_euros(t, d)
            cible = poids[t] * total
            ecart = cible - quantites[t] * pe
            if numero > 0 and abs(ecart) < SEUIL_REEQUILIBRAGE * cible:
                continue                               # ligne proche de sa cible : on n'y touche pas
            n = int(ecart / pe)                        # arrondi vers zéro
            n = max(n, -quantites[t])                  # on ne vend pas plus que ce qu'on a
            if n == 0:
                continue
            quantites[t] += n
            lignes.append({
                "date": d, "type": "ACHAT" if n > 0 else "VENTE", "ticker": t, "nom": noms[t],
                "quantite": abs(n), "prix": round(float(cours.at[d, t]), 2),
                "frais": frais_courtage(abs(n) * pe),
            })
    operations = pd.DataFrame(lignes)
    print(f"✅ {len(dates)} dates de gestion : investissement initial + {len(dates) - 1} rééquilibrages")

    # 4. Dividendes et coupons réels, selon la quantité détenue la veille du détachement
    print("⏳ Récupération des dividendes et coupons (une requête par titre, patience)...")
    signe = operations["type"].map({"ACHAT": 1, "VENTE": -1})
    operations["variation"] = signe * operations["quantite"]
    lignes_div = []
    for t in tickers:
        for date_div, par_titre in dividendes(t, DATE_DEBUT).items():
            detenu = operations.loc[(operations["ticker"] == t) & (operations["date"] < date_div), "variation"].sum()
            if detenu <= 0:
                continue
            # Sécurité pour Londres : cours en pence mais dividende parfois publié en livres.
            if info[t][1] == 0.01:
                cours_jour = cours[t].asof(date_div)
                if pd.notna(cours_jour) and par_titre / cours_jour < 0.001:
                    par_titre *= 100
            lignes_div.append({"date": date_div, "type": "DIVIDENDE", "ticker": t, "nom": noms[t],
                               "quantite": 0, "prix": round(detenu * par_titre, 2), "frais": 0.0})

    # 5. Assemblage, tri et écriture
    colonnes = ["date", "type", "ticker", "nom", "quantite", "prix", "frais"]
    final = pd.concat([operations[colonnes], pd.DataFrame(lignes_div, columns=colonnes)])
    ordre = final["type"].map({"ACHAT": 0, "DIVIDENDE": 1, "VENTE": 2})
    final = final.assign(_o=ordre).sort_values(["date", "_o", "ticker"]).drop(columns="_o")
    final["date"] = pd.to_datetime(final["date"]).dt.strftime("%Y-%m-%d")
    final["quantite"] = final["quantite"].astype(int)
    final.to_csv(FICHIER_SORTIE, index=False, float_format="%.2f")

    Portfolio(FICHIER_SORTIE)          # vérification (ventes à découvert, types...)
    nb = final["type"].value_counts()
    print()
    print(f"✅ {FICHIER_SORTIE} créé : {len(final)} opérations")
    print(f"   {nb.get('ACHAT', 0)} achats, {nb.get('VENTE', 0)} ventes, "
          f"{nb.get('DIVIDENDE', 0)} dividendes et coupons")
    print(f"   {len(tickers)} lignes · 60 % actions / 35 % obligations / 5 % or · "
          f"capital initial {CAPITAL_INITIAL:,.0f} € · versements {VERSEMENT_TRIMESTRIEL:,.0f} € "
          "par trimestre".replace(",", " "))
    print()
    print("Pour l'analyser :")
    print(f"   python main.py {FICHIER_SORTIE}")
    print("   ou choisis « Portefeuille diversifié » dans la barre latérale du tableau de bord.")


if __name__ == "__main__":
    main()
