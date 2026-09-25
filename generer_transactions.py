"""
generer_transactions.py — Enrichit data/transactions.csv avec un grand nombre
d'opérations RÉALISTES.

Pourquoi un script plutôt qu'une liste de lignes à copier ?
    Si on invente les prix, ils ne correspondent pas aux vrais cours du
    jour : le programme croit alors à un gain ou une perte le jour de
    l'achat, et les indicateurs (volatilité, meilleur jour...) sont faussés.
    Ce script va donc chercher sur Yahoo Finance :
      - le VRAI cours de clôture de chaque jour d'opération ;
      - les VRAIS dividendes versés par chaque action, calculés selon le
        nombre de titres détenus à la date de détachement.

Ce que fait le script :
    1. Sauvegarde ton fichier actuel dans data/transactions_sauvegarde.csv
    2. Ajoute les opérations de la liste PLAN ci-dessous
    3. Recale les prix de tes opérations existantes sur les vrais cours
       (voir RECALER_PRIX_EXISTANTS)
    4. Remplace les dividendes saisis à la main par les vrais dividendes
    5. Vérifie que le fichier final est cohérent (pas de vente à découvert)

Lancement (depuis le dossier portfolio_tracker) :
    python generer_transactions.py

Pour revenir en arrière : supprime data/transactions.csv et renomme
data/transactions_sauvegarde.csv en transactions.csv.
"""

import shutil
import sys

import pandas as pd

from src.portfolio import Portfolio

FICHIER = "data/transactions.csv"
SAUVEGARDE = "data/transactions_sauvegarde.csv"

# True : les prix de tes opérations déjà présentes sont remplacés par le
# vrai cours de clôture du jour (recommandé, car ils avaient été inventés).
RECALER_PRIX_EXISTANTS = True

# Noms affichés pour chaque ticker (Yahoo Finance, toutes cotées en euros).
NOMS = {
    "CW8.PA": "Amundi MSCI World",
    "MC.PA": "LVMH",
    "AI.PA": "Air Liquide",
    "TTE.PA": "TotalEnergies",
    "SAN.PA": "Sanofi",
    "SU.PA": "Schneider Electric",
    "OR.PA": "L'Oreal",
    "BNP.PA": "BNP Paribas",
    "AIR.PA": "Airbus",
    "SAF.PA": "Safran",
    "DG.PA": "Vinci",
    "EL.PA": "EssilorLuxottica",
    "ASML.AS": "ASML",
    "SAP.DE": "SAP",
    "ESE.PA": "BNP Paribas Easy S&P 500",
}

# ----------------------------------------------------------------------
# Le plan d'opérations : (date, type, ticker, quantité)
# Le prix n'est PAS saisi : il est récupéré automatiquement.
# Une date tombant un week-end ou un jour férié est décalée au jour de
# bourse suivant.
# ----------------------------------------------------------------------
PLAN = [
    # --- 2024 : construction du portefeuille ---
    ("2024-02-05", "ACHAT", "SU.PA", 6),
    ("2024-02-20", "ACHAT", "OR.PA", 3),
    ("2024-03-04", "ACHAT", "BNP.PA", 20),
    ("2024-03-18", "ACHAT", "AIR.PA", 8),
    ("2024-04-15", "ACHAT", "ASML.AS", 2),
    ("2024-05-06", "ACHAT", "SAP.DE", 6),
    ("2024-05-21", "ACHAT", "DG.PA", 8),
    ("2024-06-10", "ACHAT", "ESE.PA", 50),
    ("2024-07-08", "ACHAT", "SAF.PA", 5),
    ("2024-08-05", "ACHAT", "BNP.PA", 15),   # achat pendant le mini-krach d'août 2024
    ("2024-09-09", "ACHAT", "EL.PA", 4),
    ("2024-10-14", "VENTE", "AIR.PA", 3),
    ("2024-11-12", "ACHAT", "OR.PA", 2),
    ("2024-12-02", "ACHAT", "ESE.PA", 40),
    # --- 2025 ---
    ("2025-01-20", "ACHAT", "ASML.AS", 1),
    ("2025-02-10", "VENTE", "BNP.PA", 15),
    ("2025-03-10", "ACHAT", "SAF.PA", 3),
    ("2025-04-07", "ACHAT", "SU.PA", 4),     # achat pendant la baisse d'avril 2025
    ("2025-04-08", "ACHAT", "ESE.PA", 60),
    ("2025-05-12", "VENTE", "SAP.DE", 2),
    ("2025-06-16", "ACHAT", "DG.PA", 5),
    ("2025-07-15", "ACHAT", "EL.PA", 2),
    ("2025-09-08", "VENTE", "OR.PA", 5),     # sortie complète de L'Oréal
    ("2025-10-06", "ACHAT", "AIR.PA", 4),
    ("2025-11-17", "ACHAT", "BNP.PA", 10),
    # --- 2026 ---
    ("2026-01-12", "ACHAT", "ASML.AS", 1),
    ("2026-02-09", "VENTE", "SAF.PA", 4),
    ("2026-03-16", "ACHAT", "SAP.DE", 3),
    ("2026-04-13", "ACHAT", "ESE.PA", 50),
    ("2026-05-18", "VENTE", "DG.PA", 6),
    ("2026-06-15", "ACHAT", "SU.PA", 3),
    ("2026-07-20", "VENTE", "ESE.PA", 40),
    ("2026-09-07", "ACHAT", "EL.PA", 2),
]

# Investissement programmé : 1 part de l'ETF MSCI World le 5 de chaque mois,
# de juillet 2024 à septembre 2026 (stratégie "DCA", très courante).
for date in pd.date_range("2024-07-05", "2026-09-05", freq="MS") + pd.Timedelta(days=4):
    PLAN.append((date.strftime("%Y-%m-%d"), "ACHAT", "CW8.PA", 1))


def frais_courtage(montant):
    """Barème type d'un courtier en ligne : 0,1 % du montant, minimum 1,99 €."""
    return round(max(1.99, 0.001 * montant), 2)


def telecharger(tickers, debut):
    """Cours de clôture réels (non ajustés) depuis 'debut'."""
    import yfinance as yf

    donnees = yf.download(list(tickers), start=debut, auto_adjust=False, progress=False)
    if donnees is None or donnees.empty:
        sys.exit("❌ Impossible de joindre Yahoo Finance. Vérifie ta connexion.")
    cours = donnees["Close"]
    if isinstance(cours, pd.Series):
        cours = cours.to_frame(name=list(tickers)[0])
    cours.index = pd.to_datetime(cours.index).tz_localize(None).normalize()
    return cours


def dividendes_reels(ticker, debut):
    """Dividendes par action versés depuis 'debut' (date de détachement)."""
    import yfinance as yf

    div = yf.Ticker(ticker).dividends
    if div is None or len(div) == 0:
        return pd.Series(dtype=float)
    div.index = pd.to_datetime(div.index).tz_localize(None).normalize()
    return div[div.index >= debut]


def main():
    # 1. Sauvegarde
    shutil.copy(FICHIER, SAUVEGARDE)
    print(f"✅ Sauvegarde de ton fichier actuel : {SAUVEGARDE}")

    existant = pd.read_csv(FICHIER, parse_dates=["date"])
    existant["type"] = existant["type"].str.strip().str.upper()
    existant["nouveau"] = False
    # On retire les dividendes saisis à la main : ils seront remplacés par les vrais.
    operations = existant[existant["type"] != "DIVIDENDE"].copy()

    # 2. Nouvelles opérations
    nouvelles = pd.DataFrame(PLAN, columns=["date", "type", "ticker", "quantite"])
    nouvelles["date"] = pd.to_datetime(nouvelles["date"])
    nouvelles["nom"] = nouvelles["ticker"].map(NOMS)
    nouvelles["prix"] = float("nan")
    nouvelles["frais"] = float("nan")
    nouvelles["nouveau"] = True
    operations = pd.concat([operations, nouvelles], ignore_index=True)

    # 3. Récupération des vrais cours
    tickers = sorted(operations["ticker"].unique())
    debut = operations["date"].min()
    print(f"⏳ Téléchargement des cours de {len(tickers)} titres depuis le {debut:%d/%m/%Y}...")
    cours = telecharger(tickers, debut.strftime("%Y-%m-%d"))

    for i, op in operations.iterrows():
        serie = cours[op["ticker"]].dropna()
        serie = serie[serie.index >= op["date"]]
        if serie.empty:
            sys.exit(f"❌ Pas de cours pour {op['ticker']} après le {op['date']:%d/%m/%Y}.")
        if op["nouveau"] or RECALER_PRIX_EXISTANTS:
            operations.at[i, "date"] = serie.index[0]          # jour de bourse réel
            operations.at[i, "prix"] = round(float(serie.iloc[0]), 2)
        if op["nouveau"]:
            montant = op["quantite"] * operations.at[i, "prix"]
            operations.at[i, "frais"] = frais_courtage(montant)

    # 4. Vrais dividendes, selon la quantité détenue la veille du détachement
    signe = operations["type"].map({"ACHAT": 1, "VENTE": -1})
    operations["variation"] = signe * operations["quantite"]
    lignes_div = []
    print("⏳ Récupération des dividendes réels...")
    for ticker in tickers:
        for date_div, montant_par_action in dividendes_reels(ticker, debut).items():
            avant = operations[(operations["ticker"] == ticker) & (operations["date"] < date_div)]
            quantite = avant["variation"].sum()
            if quantite > 0:
                lignes_div.append({
                    "date": date_div, "type": "DIVIDENDE", "ticker": ticker,
                    "nom": operations.loc[operations["ticker"] == ticker, "nom"].iloc[0],
                    "quantite": 0, "prix": round(quantite * montant_par_action, 2),
                    "frais": 0.0,
                })

    # 5. Assemblage, tri par date et écriture
    colonnes = ["date", "type", "ticker", "nom", "quantite", "prix", "frais"]
    final = pd.concat([operations[colonnes], pd.DataFrame(lignes_div, columns=colonnes)])
    # Le même jour : les achats d'abord, puis les dividendes, puis les ventes.
    ordre = final["type"].map({"ACHAT": 0, "DIVIDENDE": 1, "VENTE": 2})
    final = final.assign(_ordre=ordre).sort_values(["date", "_ordre"]).drop(columns="_ordre")
    final["date"] = pd.to_datetime(final["date"]).dt.strftime("%Y-%m-%d")
    final["quantite"] = final["quantite"].astype(int)
    final.to_csv(FICHIER, index=False, float_format="%.2f")

    # 6. Vérification : si une vente dépasse la quantité détenue, Portfolio le signale.
    try:
        p = Portfolio(FICHIER)
    except ValueError as erreur:
        shutil.copy(SAUVEGARDE, FICHIER)
        sys.exit(f"❌ Fichier incohérent, ton ancien fichier a été restauré.\n{erreur}")

    nb = final["type"].value_counts()
    print()
    print(f"✅ {FICHIER} mis à jour : {len(final)} opérations")
    print(f"   {nb.get('ACHAT', 0)} achats, {nb.get('VENTE', 0)} ventes, "
          f"{nb.get('DIVIDENDE', 0)} dividendes")
    print(f"   {len(p.tickers())} lignes détenues aujourd'hui : {', '.join(p.tickers())}")
    print()
    print("Tu peux maintenant lancer : python main.py")


if __name__ == "__main__":
    main()
