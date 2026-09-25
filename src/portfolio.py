"""
portfolio.py — Le cœur du projet : la classe Portfolio.

Rôle de ce fichier :
    1. Lire l'historique des transactions (fichier CSV).
    2. Rejouer ces transactions dans l'ordre chronologique.
    3. En déduire, pour chaque titre :
         - la quantité détenue,
         - le PRU (Prix de Revient Unitaire),
         - les plus-values réalisées (ventes),
         - les dividendes perçus.

Convention du fichier CSV :
    - type = ACHAT, VENTE ou DIVIDENDE
    - pour un ACHAT / une VENTE : "prix" = prix unitaire d'une action
    - pour un DIVIDENDE : "quantite" = 0 et "prix" = montant TOTAL reçu
    - "frais" = frais de courtage en euros
"""

# On importe pandas, la bibliothèque de référence pour manipuler des tableaux
# de données en Python. "pd" est le surnom qu'on lui donne par convention.
import pandas as pd


# Les seuls types de transaction que l'on accepte.
TYPES_VALIDES = {"ACHAT", "VENTE", "DIVIDENDE"}


class Portfolio:
    """
    Une "classe" est un plan de construction. Ici, elle décrit ce qu'est un
    portefeuille : des données (les transactions, les positions) et des
    actions possibles sur ces données (les méthodes, écrites avec "def").
    """

    def __init__(self, chemin_csv):
        """
        __init__ est appelée automatiquement quand on crée un portefeuille :
            mon_portefeuille = Portfolio("data/transactions.csv")
        "self" désigne le portefeuille lui-même.
        """
        self.transactions = self._charger_transactions(chemin_csv)
        # On calcule les positions dès la création du portefeuille.
        self.positions = self._calculer_positions()

    # ------------------------------------------------------------------
    # 1. Lecture et vérification des données
    # ------------------------------------------------------------------
    def _charger_transactions(self, chemin_csv):
        """Lit le CSV et vérifie qu'il est cohérent.

        Le "_" au début du nom signale une méthode interne : elle sert à la
        classe elle-même, l'utilisateur n'a pas besoin de l'appeler.
        """
        # On accepte soit un fichier CSV, soit un tableau pandas déjà prêt
        # (utile à l'étape 8 : transactions converties en euros).
        if isinstance(chemin_csv, pd.DataFrame):
            df = chemin_csv.copy()
            df["date"] = pd.to_datetime(df["date"])
        else:
            # read_csv transforme le fichier en "DataFrame" (un tableau pandas).
            # parse_dates convertit la colonne "date" en vraies dates.
            df = pd.read_csv(chemin_csv, parse_dates=["date"])

        # Mise en forme : "achat " devient "ACHAT" (majuscules, sans espaces).
        df["type"] = df["type"].str.strip().str.upper()
        df["ticker"] = df["ticker"].str.strip().str.upper()

        # Contrôles de cohérence : mieux vaut une erreur claire qu'un
        # résultat faux sans s'en rendre compte.
        types_inconnus = set(df["type"]) - TYPES_VALIDES
        if types_inconnus:
            raise ValueError(f"Type(s) de transaction inconnu(s) : {types_inconnus}")

        if (df["prix"] < 0).any() or (df["quantite"] < 0).any():
            raise ValueError("Les prix et les quantités doivent être positifs.")

        # On trie par date : l'ordre compte pour calculer le PRU.
        return df.sort_values("date").reset_index(drop=True)

    # ------------------------------------------------------------------
    # 2. Calcul des positions (quantité, PRU, plus-values réalisées)
    # ------------------------------------------------------------------
    def _calculer_positions(self):
        """Rejoue toutes les transactions une par une.

        Règles de calcul (méthode du PRU, utilisée en France) :
          * ACHAT : le PRU devient la moyenne pondérée entre l'ancien stock
                    et les nouveaux titres. Les frais d'achat sont inclus
                    dans le PRU (ils augmentent le coût de revient).
                    nouveau PRU = (qté × PRU + q × prix + frais) / (qté + q)
          * VENTE : le PRU ne change pas. On calcule la plus-value réalisée :
                    PV = q × (prix de vente − PRU) − frais
          * DIVIDENDE : on ajoute le montant reçu au total des dividendes.
        """
        # Un dictionnaire : pour chaque ticker, on stocke ses informations.
        positions = {}

        # iterrows() parcourt le tableau ligne par ligne.
        for _, t in self.transactions.iterrows():
            ticker = t["ticker"]

            # Première fois qu'on voit ce titre : on crée une fiche vide.
            if ticker not in positions:
                positions[ticker] = {
                    "nom": t["nom"],
                    "quantite": 0.0,
                    "pru": 0.0,
                    "pv_realisee": 0.0,
                    "dividendes": 0.0,
                    "frais_totaux": 0.0,
                }
            p = positions[ticker]
            p["frais_totaux"] += t["frais"]

            if t["type"] == "ACHAT":
                cout_ancien = p["quantite"] * p["pru"]
                cout_nouveau = t["quantite"] * t["prix"] + t["frais"]
                p["quantite"] += t["quantite"]
                p["pru"] = (cout_ancien + cout_nouveau) / p["quantite"]

            elif t["type"] == "VENTE":
                if t["quantite"] > p["quantite"]:
                    raise ValueError(
                        f"Vente impossible le {t['date'].date()} : on vend "
                        f"{t['quantite']} {ticker} mais on n'en détient que "
                        f"{p['quantite']}."
                    )
                p["pv_realisee"] += t["quantite"] * (t["prix"] - p["pru"]) - t["frais"]
                p["quantite"] -= t["quantite"]
                # Si on a tout vendu, le PRU repart de zéro.
                if p["quantite"] == 0:
                    p["pru"] = 0.0

            elif t["type"] == "DIVIDENDE":
                p["dividendes"] += t["prix"] - t["frais"]

        # On transforme le dictionnaire en tableau pandas, plus pratique.
        tableau = pd.DataFrame.from_dict(positions, orient="index")
        tableau.index.name = "ticker"
        # Montant investi encore en portefeuille = quantité × PRU.
        tableau["montant_investi"] = tableau["quantite"] * tableau["pru"]
        return tableau

    # ------------------------------------------------------------------
    # 3. Méthodes utiles pour la suite du projet
    # ------------------------------------------------------------------
    def positions_ouvertes(self):
        """Renvoie uniquement les titres encore détenus (quantité > 0)."""
        return self.positions[self.positions["quantite"] > 0]

    def tickers(self):
        """Liste des codes des titres encore détenus (ex. ["MC.PA", ...])."""
        return list(self.positions_ouvertes().index)

    def resume(self):
        """Renvoie un petit résumé chiffré du portefeuille."""
        return {
            "nb_lignes": len(self.positions_ouvertes()),
            "montant_investi": self.positions["montant_investi"].sum(),
            "pv_realisees": self.positions["pv_realisee"].sum(),
            "dividendes": self.positions["dividendes"].sum(),
            "frais_totaux": self.positions["frais_totaux"].sum(),
        }

    # ------------------------------------------------------------------
    # 4. Valorisation aux cours du marché (étape 2)
    # ------------------------------------------------------------------
    def valoriser(self, prix):
        """Calcule la valeur actuelle de chaque ligne à partir des cours.

        Paramètre : prix = dictionnaire {ticker: cours}, fourni par
                    market_data.py (ou inventé dans les tests).

        Formules :
          valeur             = quantité × cours
          plus-value latente = valeur − montant investi
                             = quantité × (cours − PRU)
          plus-value en %    = plus-value latente / montant investi
          poids              = valeur de la ligne / valeur totale

        "Latente" = non encaissée : c'est ce qu'on gagnerait (ou perdrait)
        si on vendait tout aujourd'hui, hors frais de vente.
        """
        # .copy() évite de modifier le tableau d'origine par erreur.
        tableau = self.positions_ouvertes().copy()

        # .map() va chercher, pour chaque ticker, son cours dans le dictionnaire.
        tableau["cours"] = tableau.index.map(prix)

        if tableau["cours"].isna().any():
            manquants = list(tableau.index[tableau["cours"].isna()])
            raise ValueError(f"Cours manquant pour : {manquants}")

        tableau["valeur"] = tableau["quantite"] * tableau["cours"]
        tableau["pv_latente"] = tableau["valeur"] - tableau["montant_investi"]
        tableau["pv_latente_pct"] = tableau["pv_latente"] / tableau["montant_investi"] * 100
        tableau["poids_pct"] = tableau["valeur"] / tableau["valeur"].sum() * 100

        # On trie par poids décroissant : les plus grosses lignes en premier.
        return tableau.sort_values("valeur", ascending=False)

    def resume_valorise(self, prix):
        """Résumé complet, y compris la valeur de marché.

        Performance globale (en €) = ce que le portefeuille a rapporté
        depuis le début, tout compris :
            plus-values latentes + plus-values réalisées + dividendes
        (les frais sont déjà déduits dans le PRU et dans les plus-values)
        """
        tableau = self.valoriser(prix)
        r = self.resume()
        r["valeur_actuelle"] = tableau["valeur"].sum()
        r["pv_latentes"] = tableau["pv_latente"].sum()
        r["gain_total"] = r["pv_latentes"] + r["pv_realisees"] + r["dividendes"]
        return r

    # ------------------------------------------------------------------
    # 5. Historique jour par jour (étape 3)
    # ------------------------------------------------------------------
    def tous_les_tickers(self):
        """Tous les titres détenus à un moment donné, même vendus depuis.
        (Il faut leur historique : ils ont compté dans la valeur passée.)"""
        return list(self.positions.index)

    def date_debut(self):
        """Date de la toute première transaction."""
        return self.transactions["date"].min()

    def historique(self, prix_hist):
        """Reconstitue la vie du portefeuille, jour de bourse par jour de bourse.

        Paramètre : prix_hist = tableau des cours de clôture
                    (une ligne par jour, une colonne par ticker).

        Renvoie un tableau avec, pour chaque jour :
          valeur              = Σ (quantité détenue ce jour-là × cours du jour)
          flux                = argent que l'investisseur a mis (+) ou
                                récupéré (−) ce jour-là :
                                  ACHAT     : + (quantité × prix + frais)
                                  VENTE     : − (quantité × prix − frais)
                                  DIVIDENDE : − (montant − frais)
          apports_nets        = somme de tous les flux depuis le début
                                = argent "de sa poche" encore investi
          gain                = valeur − apports_nets
                                = ce que le portefeuille a rapporté à cette date

        Le dernier jour, "gain" doit être égal au "GAIN TOTAL" de l'étape 2 :
        c'est une vérification croisée de nos deux méthodes de calcul.
        """
        # --- a) Le calendrier : les jours de bourse depuis le 1er achat ---
        prix = prix_hist.sort_index()
        prix = prix[prix.index >= self.date_debut()]
        if prix.empty:
            raise ValueError("Aucun cours disponible après la première transaction.")
        calendrier = prix.index

        manquants = [t for t in self.tous_les_tickers() if t not in prix.columns]
        if manquants:
            raise ValueError(f"Historique de cours manquant pour : {manquants}")

        # --- b) On rattache chaque transaction à un jour de bourse ---
        # Une opération saisie un samedi est rattachée au lundi suivant.
        # searchsorted() donne la position du 1er jour du calendrier >= la date.
        t = self.transactions.copy()
        position = calendrier.searchsorted(t["date"])
        position = position.clip(max=len(calendrier) - 1)  # sécurité : date future
        t["jour"] = calendrier[position]

        # --- c) Variation de quantité de chaque transaction ---
        # ACHAT : +quantité, VENTE : −quantité, DIVIDENDE : 0
        signe = t["type"].map({"ACHAT": 1, "VENTE": -1, "DIVIDENDE": 0})
        t["variation_qte"] = signe * t["quantite"]

        # --- d) Flux d'argent de chaque transaction (voir la docstring) ---
        montant = t["quantite"] * t["prix"]
        t["flux"] = 0.0
        t.loc[t["type"] == "ACHAT", "flux"] = montant + t["frais"]
        t.loc[t["type"] == "VENTE", "flux"] = -(montant - t["frais"])
        t.loc[t["type"] == "DIVIDENDE", "flux"] = -(t["prix"] - t["frais"])

        # --- e) Quantité détenue chaque jour, pour chaque titre ---
        # pivot_table : on range les variations dans un tableau
        #   lignes = jours, colonnes = tickers (somme si plusieurs le même jour).
        # reindex : on ajoute tous les jours du calendrier (0 = rien ne bouge).
        # cumsum  : somme cumulée -> la quantité détenue à chaque date.
        variations = t.pivot_table(index="jour", columns="ticker",
                                   values="variation_qte", aggfunc="sum")
        quantites = variations.reindex(calendrier).fillna(0).cumsum()

        # --- f) Valeur du portefeuille chaque jour ---
        # ffill : un jour férié sur une seule place, on garde le dernier cours.
        # bfill : sécurité si le tout premier cours manque.
        cours = prix[quantites.columns].ffill().bfill()
        valeur_par_titre = quantites * cours
        valeur = valeur_par_titre.sum(axis=1)
        # On garde la valeur de chaque ligne jour par jour : elle sert à
        # l'attribution de performance (étape 10).
        self.valeur_par_titre = valeur_par_titre

        # --- g) Flux, apports nets et gain ---
        flux = t.groupby("jour")["flux"].sum().reindex(calendrier).fillna(0)

        resultat = pd.DataFrame({
            "valeur": valeur,
            "flux": flux,
            "apports_nets": flux.cumsum(),
        })
        resultat["gain"] = resultat["valeur"] - resultat["apports_nets"]
        resultat.index.name = "date"
        return resultat
