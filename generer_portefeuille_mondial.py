"""
generer_portefeuille_mondial.py — Construit l'historique d'un portefeuille
d'actions mondiales géré comme par un asset manager.

Le fichier produit (data/transactions_mondial.csv) NE REMPLACE PAS ton
fichier data/transactions.csv : c'est un second portefeuille, que tu peux
choisir dans le tableau de bord ou analyser avec :
    python main.py data/transactions_mondial.csv

La politique de gestion simulée (typique d'un fonds actions monde) :
    1. ALLOCATION CIBLE par grande région (proche du MSCI World + émergents) :
       États-Unis 55 %, Europe 18 %, Japon 6 %, Royaume-Uni 5 %, Émergents 5 %,
       Suisse 4 %, Asie-Pacifique 4 %, Canada 3 %.
       Dans chaque région, les titres sont équipondérés.
    2. INVESTISSEMENT INITIAL de 2 000 000 € le 15/01/2024.
    3. Chaque trimestre : SOUSCRIPTION de 100 000 € (nouveaux clients) et
       RÉÉQUILIBRAGE : on achète les lignes passées sous leur poids cible et
       on allège celles qui l'ont dépassé.
    4. DIVIDENDES : les vrais dividendes versés par chaque société.

Les prix sont les VRAIS cours de clôture (Yahoo Finance), dans la devise de
cotation de chaque titre (dollars, yens, pence...) : le programme les
convertira en euros lors de l'analyse (étape 8).

Lancement (depuis le dossier portfolio_tracker, avec Internet) :
    python generer_portefeuille_mondial.py
"""

import sys

import pandas as pd

from src.devises import detecter_devises, devises_etrangeres, ticker_change
from src.portfolio import Portfolio

FICHIER_REFERENTIEL = "data/referentiel.csv"
FICHIER_SORTIE = "data/transactions_mondial.csv"

DATE_DEBUT = "2024-01-15"
CAPITAL_INITIAL = 2_000_000          # euros
SOUSCRIPTION_TRIMESTRIELLE = 100_000  # euros
SEUIL_REEQUILIBRAGE = 0.10           # on ne touche pas une ligne à moins de 10 % de sa cible

POIDS_REGIONS = {
    "États-Unis": 0.55, "Europe": 0.18, "Japon": 0.06, "Royaume-Uni": 0.05,
    "Émergents": 0.05, "Suisse": 0.04, "Asie-Pacifique": 0.04, "Canada": 0.03,
}


def frais_courtage(montant):
    """Barème institutionnel : 0,05 % du montant, minimum 5 €."""
    return round(max(5.0, 0.0005 * montant), 2)


def telecharger_cours(tickers, debut):
    import yfinance as yf
    donnees = yf.download(list(tickers), start=debut, auto_adjust=False, progress=False)
    if donnees is None or donnees.empty:
        sys.exit("❌ Impossible de joindre Yahoo Finance. Vérifie ta connexion.")
    cours = donnees["Close"]
    if isinstance(cours, pd.Series):
        cours = cours.to_frame(name=list(tickers)[0])
    cours.index = pd.to_datetime(cours.index).tz_localize(None).normalize()
    return cours.sort_index()


def dividendes(ticker, debut):
    import yfinance as yf
    try:
        div = yf.Ticker(ticker).dividends
    except Exception:
        return pd.Series(dtype=float)
    if div is None or len(div) == 0:
        return pd.Series(dtype=float)
    div.index = pd.to_datetime(div.index).tz_localize(None).normalize()
    return div[div.index >= pd.Timestamp(debut)]


def dates_de_gestion(calendrier):
    """Date initiale, puis premier jour de bourse de chaque trimestre."""
    debut = calendrier[calendrier >= pd.Timestamp(DATE_DEBUT)][0]
    dates = [debut]
    for trimestre in pd.date_range(debut, calendrier[-1], freq="QS")[0:]:
        suivants = calendrier[calendrier >= trimestre]
        if len(suivants) and suivants[0] > debut:
            dates.append(suivants[0])
    return sorted(set(dates))


def main():
    # 1. L'univers d'investissement et les poids cibles
    ref = pd.read_csv(FICHIER_REFERENTIEL)
    univers = ref[ref["region"].isin(POIDS_REGIONS) & (ref["secteur"] != "ETF diversifié")].copy()
    tickers = list(univers["ticker"])
    noms = dict(zip(univers["ticker"], univers["nom"]))
    print(f"⏳ Univers : {len(tickers)} actions dans {len(POIDS_REGIONS)} régions")

    # 2. Devises et cours (titres + taux de change), en un seul téléchargement
    info = detecter_devises(tickers)
    etrangeres = devises_etrangeres(info)
    tickers_change = [ticker_change(d) for d in etrangeres]
    print(f"⏳ Téléchargement des cours et de {len(etrangeres)} taux de change "
          f"({', '.join(etrangeres)})...")
    debut_telechargement = (pd.Timestamp(DATE_DEBUT) - pd.Timedelta(days=10)).strftime("%Y-%m-%d")
    cours = telecharger_cours(tickers + tickers_change, debut_telechargement)

    manquants = [t for t in tickers if t not in cours.columns or cours[t].dropna().empty]
    if manquants:
        print(f"⚠️  Titres introuvables, retirés de l'univers : {manquants}")
        univers = univers[~univers["ticker"].isin(manquants)]
        tickers = list(univers["ticker"])

    # Poids cible : poids de la région / nombre de titres de la région
    nb_par_region = univers["region"].value_counts()
    poids = {t: POIDS_REGIONS[r] / nb_par_region[r] for t, r in zip(univers["ticker"], univers["region"])}
    total_poids = sum(poids.values())
    poids = {t: w / total_poids for t, w in poids.items()}

    cours = cours.ffill()
    calendrier = cours.index

    def prix_local(t, d):
        return cours.at[d, t]

    def prix_euros(t, d):
        devise, facteur = info[t]
        taux = 1.0 if devise == "EUR" else cours.at[d, ticker_change(devise)]
        return cours.at[d, t] * facteur / taux

    # 3. Investissement initial, puis souscriptions et rééquilibrages trimestriels
    quantites = {t: 0 for t in tickers}
    lignes = []
    dates = dates_de_gestion(calendrier)
    for numero, d in enumerate(dates):
        apport = CAPITAL_INITIAL if numero == 0 else SOUSCRIPTION_TRIMESTRIELLE
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
                "quantite": abs(n), "prix": round(float(prix_local(t, d)), 2),
                "frais": frais_courtage(abs(n) * pe),
            })
    operations = pd.DataFrame(lignes)
    print(f"✅ {len(dates)} dates de gestion : investissement initial + {len(dates) - 1} rééquilibrages")

    # 4. Dividendes réels, selon la quantité détenue la veille du détachement
    print("⏳ Récupération des dividendes (une requête par titre, patience)...")
    signe = operations["type"].map({"ACHAT": 1, "VENTE": -1})
    operations["variation"] = signe * operations["quantite"]
    lignes_div = []
    for t in tickers:
        for date_div, par_action in dividendes(t, DATE_DEBUT).items():
            detenu = operations.loc[(operations["ticker"] == t) & (operations["date"] < date_div), "variation"].sum()
            if detenu <= 0:
                continue
            # Sécurité pour Londres : cours en pence mais dividende parfois publié en livres.
            if info[t][1] == 0.01:
                cours_jour = cours[t].asof(date_div)
                if pd.notna(cours_jour) and par_action / cours_jour < 0.001:
                    par_action *= 100
            lignes_div.append({"date": date_div, "type": "DIVIDENDE", "ticker": t, "nom": noms[t],
                               "quantite": 0, "prix": round(detenu * par_action, 2), "frais": 0.0})

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
    print(f"   {nb.get('ACHAT', 0)} achats, {nb.get('VENTE', 0)} ventes, {nb.get('DIVIDENDE', 0)} dividendes")
    print(f"   {len(tickers)} actions · capital initial {CAPITAL_INITIAL:,.0f} € · "
          f"souscriptions {SOUSCRIPTION_TRIMESTRIELLE:,.0f} € par trimestre".replace(",", " "))
    print()
    print("Pour l'analyser :")
    print(f"   python main.py {FICHIER_SORTIE}")
    print("   ou choisis ce fichier dans la barre latérale du tableau de bord.")


if __name__ == "__main__":
    main()
