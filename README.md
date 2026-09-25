# Portfolio Tracker — Outil de suivi et d'analyse de portefeuille

Projet de Master G2C · Année universitaire 2026-2027
Auteurs : *[Prénom NOM, Prénom NOM, Prénom NOM]*

Outil en Python qui lit l'historique des transactions d'un portefeuille (achats, ventes,
dividendes), le valorise aux cours de marché et calcule les indicateurs de performance et
de risque utilisés par les professionnels de la gestion. Les résultats sont présentés dans
un tableau de bord web interactif et dans un rapport PDF généré automatiquement.

## Fonctionnalités

| Domaine | Ce que fait l'outil |
|---|---|
| **Suivi** | PRU, plus-values latentes et réalisées, dividendes, frais, valorisation quotidienne, titres en devises étrangères convertis en euros |
| **Performance** | TWR (total, annualisé, par année civile), TRI, comparaison avec un indice de référence |
| **Risque** | Volatilité, maximum drawdown, VaR et CVaR (historique et paramétrique), corrélations |
| **Performance relative** | Ratios de Sharpe et de Sortino, bêta, alpha de Jensen, tracking error, ratio d'information |
| **Optimisation** | Markowitz : variance minimale, Sharpe maximal, frontière efficiente, droite de marché des capitaux |
| **Projection** | Simulation de Monte-Carlo (loi normale ou bootstrap historique), versements mensuels, objectif, nuage de points par tranche de probabilité |
| **Conseil patrimonial** | Profil de risque client (questionnaire inspiré de MiFID II), indicateur SRI, test d'adéquation ; fiscalité comparée CTO / PEA / assurance-vie (taux 2026) ; stress tests (5 crises historiques et chocs hypothétiques) |
| **Gestion d'actifs** | Attribution de performance de Brinson-Fachler face au MSCI ACWI (lissage de Cariño) ; budget de risque et parité des risques ; backtest de stratégies de rééquilibrage et d'investissement progressif |
| **Restitution** | Tableau de bord Streamlit en 3 espaces (analyse, conseil patrimonial, gestion d'actifs), version en ligne de commande, rapport PDF de synthèse |
| **Fiabilité** | 74 tests automatiques, contrôle croisé du gain total, cache hors ligne |

## Démarrage rapide

**Sous Windows**, double-cliquer sur :

- `lancer_tableau_de_bord.bat` : ouvre le tableau de bord dans le navigateur ;
- `lancer_analyse.bat` : analyse complète dans le terminal, graphiques et rapport PDF.

**En ligne de commande** (depuis le dossier du projet) :

```bash
python -m pip install -r requirements.txt           # une seule fois
python -m streamlit run app.py                      # tableau de bord web
python main.py                                      # analyse de data/transactions.csv
python main.py data/transactions_mondial.csv        # analyse d'un autre portefeuille
python generer_portefeuille_mondial.py              # crée le fonds actions monde (69 titres)
python -m pytest                                    # lance les 74 tests
```

Python 3.11 ou plus récent est nécessaire, ainsi qu'une connexion Internet au premier lancement.
Ensuite, un cache local permet de travailler hors ligne.

## Format du fichier de transactions

Fichier CSV, une ligne par opération :

```
date,type,ticker,nom,quantite,prix,frais
2024-01-15,ACHAT,CW8.PA,Amundi MSCI World,10,420.00,2.50
2024-05-22,DIVIDENDE,AI.PA,Air Liquide,0,26.40,0.00
2024-09-18,VENTE,TTE.PA,TotalEnergies,10,60.00,2.00
```

| Colonne | Signification |
|---|---|
| `date` | AAAA-MM-JJ (un jour non ouvré est rattaché au jour de bourse suivant) |
| `type` | `ACHAT`, `VENTE` ou `DIVIDENDE` |
| `ticker` | code Yahoo Finance (`MC.PA` pour LVMH à Paris, `AAPL` pour Apple, `ULVR.L` pour Unilever à Londres) |
| `quantite` | nombre de titres (0 pour un dividende) |
| `prix` | prix unitaire, ou montant total pour un dividende, **dans la devise de cotation** du titre (pence pour Londres) |
| `frais` | frais de courtage, **en euros** |

Le fichier `data/referentiel.csv` associe à chaque ticker sa région, son secteur et son pays
(répartitions affichées dans le tableau de bord et le rapport).

## Architecture

```
            app.py (tableau de bord)      main.py (terminal)      rapport.py (PDF)
                         \                     |                     /
                          +---------  src/analyse.py  --------------+
                                            |
      portfolio.py · market_data.py · devises.py · metrics.py · optimisation.py · simulation.py
```

Les modules de calcul ne dépendent ni de la source des données ni de l'affichage : ils sont
testés isolément. `app.py` et `main.py` ne font qu'**afficher** les résultats de `analyse.py`.

```
portfolio_tracker/
├── app.py                           # tableau de bord web (Streamlit)
├── main.py                          # version en ligne de commande + rapport PDF
├── generer_transactions.py          # enrichit data/transactions.csv (vrais cours et dividendes)
├── generer_portefeuille_mondial.py  # fonds actions monde : 69 titres, 8 devises
├── lancer_tableau_de_bord.bat       # raccourcis Windows
├── lancer_analyse.bat
├── requirements.txt · pytest.ini · .gitignore
├── data/
│   ├── transactions.csv             # portefeuille du particulier
│   ├── transactions_mondial.csv     # fonds actions monde (créé par le script)
│   └── referentiel.csv              # région, secteur, pays de chaque titre
├── src/
│   ├── config.py                    # réglages (indice, taux sans risque, VaR, poids max, projection)
│   ├── portfolio.py                 # transactions, PRU, plus-values, historique jour par jour
│   ├── market_data.py               # cours Yahoo Finance + cache hors ligne
│   ├── devises.py                   # détection des devises et conversion en euros
│   ├── metrics.py                   # TWR, TRI, volatilité, drawdown, Sharpe, bêta, VaR...
│   ├── optimisation.py              # Markowitz (SciPy, SLSQP)
│   ├── simulation.py                # Monte-Carlo
│   ├── profil.py                    # profil de risque client, SRI, adéquation
│   ├── fiscalite.py                 # CTO, PEA, assurance-vie (taux 2026)
│   ├── stress.py                    # stress tests historiques et hypothétiques
│   ├── attribution.py               # attribution de Brinson-Fachler
│   ├── budget_risque.py             # contributions au risque, parité des risques
│   ├── backtest.py                  # stratégies de rééquilibrage, DCA
│   ├── extensions.py                # calcule les six analyses ci-dessus (main.py, PDF)
│   ├── analyse.py                   # enchaînement complet de l'analyse
│   ├── graphiques.py                # graphiques matplotlib (rapport PDF)
│   ├── graphiques_interactifs.py    # graphiques Plotly (tableau de bord)
│   ├── interface.py                 # éléments visuels du tableau de bord
│   ├── vues_conseil.py              # espace « Conseil patrimonial » du tableau de bord
│   ├── vues_gestion.py              # espace « Gestion d'actifs » du tableau de bord
│   └── rapport.py                   # rapport PDF (reportlab)
├── assets/style.css · .streamlit/config.toml   # apparence du tableau de bord
├── tests/                           # 74 tests automatiques (pytest)
└── docs/                            # guides pas à pas des étapes du projet
```

## Tests

```bash
python -m pytest
```

Chaque formule est vérifiée sur un cas dont le résultat se calcule à la main : PRU avec frais,
rendement en présence d'apports, TWR indépendant des flux, TRI d'un placement simple, drawdown,
VaR, solution analytique de Markowitz à deux titres, médiane théorique du mouvement brownien
géométrique, conversion des devises, barèmes fiscaux, propriété d'Euler des contributions au
risque, égalité des effets de Brinson avec l'écart de performance, etc. Un test croise deux méthodes indépendantes de calcul
du gain total (ligne par ligne et jour par jour).

## Choix méthodologiques

- **PRU** : moyenne pondérée des prix d'achat, **frais d'achat inclus**. Une vente ne modifie pas le PRU.
- **Plus-value réalisée** : `quantité vendue × (prix de vente − PRU) − frais de vente`.
- **Valorisation** : dernier cours de clôture **non ajusté** (le cours réellement affiché en bourse).
- **Plus-value latente** : `quantité × (cours − PRU)`, hors frais de vente éventuels.
- **Gain total** : plus-values latentes + plus-values réalisées + dividendes (frais déjà déduits).
- **Historique** : chaque transaction est rattachée au premier jour de bourse suivant (ou égal à) sa date. Quantités cumulées × cours de clôture non ajustés = valeur quotidienne.
- **Flux** : un achat est un apport (+ montant + frais) ; une vente (− montant net de frais) et un dividende (− montant) sont des retraits. `gain = valeur − apports nets cumulés`.
- **Pourquoi des cours non ajustés ?** Les dividendes sont déjà comptés comme des flux. Utiliser des cours « ajustés des dividendes » les compterait deux fois.
- **Contrôle de cohérence** : le gain du dernier jour de l'historique est égal au gain total calculé position par position (test automatique).
- **Rendement quotidien** : `r(t) = (valeur(t) − flux(t)) / valeur(t−1) − 1`. Les flux sont supposés faits au cours du jour, donc en fin de journée. Le premier jour : `valeur / flux − 1`.
- **TWR** : produit des `(1 + r)` − 1 ; mesure la qualité des choix de placement, indépendamment des apports (norme GIPS).
- **TRI** : taux annuel qui annule la valeur actuelle nette des flux (achats < 0, ventes et dividendes > 0, valeur finale > 0). Il est résolu par dichotomie.
- **Annualisation** : rendement `(1 + R)^(365 / jours) − 1` ; volatilité `σ quotidien × √252`.
- **Max drawdown** : calculé sur l'indice base 100 (TWR), et non sur la valeur, pour ne pas confondre un retrait avec une perte.
- **Indice de référence** : ETF Amundi MSCI World capitalisant (CW8.PA), pour comparer à dividendes réinvestis. Il est modifiable dans `src/config.py`.
- **Taux sans risque** : 2,50 % par an (facilité de dépôt de la BCE au 16/09/2026). Simplification : taux constant sur toute la période.
- **Sharpe / Sortino** : moyenne des rendements excédentaires × 252, divisée par l'écart-type (Sharpe) ou la semi-déviation (Sortino) × √252.
- **Bêta / alpha** : `β = cov(rp, rb) / var(rb)` ; alpha de Jensen annualisé `= [moy(rp − rf) − β · moy(rb − rf)] × 252`.
- **VaR 95 % à 1 jour** : historique (5e percentile) et paramétrique gaussienne (`μ + z·σ`, z = −1,645). La CVaR est la perte moyenne au-delà de la VaR historique.
- **Markowitz** : μ = moyenne des rendements quotidiens × 252, Σ = covariance × 252 (sur tout l'historique disponible). Optimisation SLSQP (SciPy) sans vente à découvert, poids ∈ [0 ; poids max] (30 % par défaut), somme des poids = 100 %.
- **Limite de Markowitz** : très sensible aux rendements espérés estimés sur le passé (« erreur d'estimation ») ; cours non ajustés, donc dividendes absents de μ.
- **Monte-Carlo** : pas mensuel ; loi normale (mouvement brownien géométrique, log-rendement ~ N((μ − σ²/2)·dt, σ·√dt)) ou bootstrap de 21 rendements quotidiens historiques par mois (recentrés sur le rendement supposé). 5 000 scénarios, graine fixe (résultats reproductibles).
- **Devises** : prix saisis dans la devise de cotation Yahoo (pence pour Londres), frais en euros. Conversion au taux EURxxx=X du jour de l'opération (transactions) ou du jour de cotation (historique, valorisation).
- **Rapport PDF** : reportlab, graphiques matplotlib intégrés ; généré par `python main.py` ou depuis le tableau de bord.
- **Portefeuille actions monde** : allocation cible par région (États-Unis 55 %, Europe 18 %, Japon 6 %, Royaume-Uni 5 %, Émergents 5 %, Suisse 4 %, Asie-Pacifique 4 %, Canada 3 %), équipondération dans chaque région ; 2 M€ investis le 15/01/2024 ; souscription de 100 000 € et rééquilibrage chaque trimestre (bande de tolérance de 10 %) ; frais de 0,05 % (minimum 5 €).
- **Nuage de points Monte-Carlo** : 400 scénarios affichés tous les 6 mois, classés par tranche de probabilité (< 5 %, 5-25 %, 25-75 %, 75-95 %, > 95 %) selon les percentiles de l'ensemble des 5 000 scénarios.
- **Cache** : chaque récupération de cours est enregistrée dans `data/cache_prix.csv`. Si Yahoo Finance est injoignable, l'outil utilise ces derniers cours et l'indique.

- **Profil client** : 7 questions notées de 0 à 4 ; 5 profils (Sécuritaire à Offensif) avec limites de volatilité, de perte, de part d'actions et de SRI ; la tolérance aux pertes plafonne le profil. SRI : classes de risque de marché PRIIPs appliquées à la volatilité annuelle (approximation de la VEV).
- **Fiscalité (2026)** : flat tax 31,4 % (12,8 % + 18,6 % de prélèvements sociaux, LFSS 2026) ; PEA après 5 ans : 18,6 % ; assurance-vie : 17,2 % de prélèvements sociaux, 7,5 % après 8 ans au-delà de l'abattement de 4 600 € (9 200 € pour un couple).
- **Stress tests** : variation du plus haut au plus bas de 5 crises (2008, 2011, 2020, 2022, 2024) appliquée aux lignes actuelles ; indice régional si le titre n'était pas coté ; chocs hypothétiques via le bêta.
- **Attribution** : Brinson-Fachler mensuel par région, poids de début de mois, lissage de Cariño ; référence : poids régionaux du MSCI ACWI IMI au 30/06/2026 et indices régionaux convertis en euros.
- **Budget de risque** : contributions d'Euler `wᵢ(Σw)ᵢ/σ` ; parité des risques par la méthode de Spinu ; nombre effectif de paris `1/Σ(CRᵢ/σ)²`.
- **Backtest** : mêmes titres et poids de départ que le portefeuille actuel ; rééquilibrage mensuel, trimestriel ou annuel avec frais de 0,1 % ; investissement progressif sur 12 mois, liquidités rémunérées au taux sans risque.

## Limites

- Historique court (depuis 2024) : estimations de rendement espéré, bêta et alpha fragiles.
- Taux sans risque constant ; dividendes bruts ; fiscalité et frais de gestion non modélisés.
- Hypothèse de normalité (VaR paramétrique, Monte-Carlo par loi normale) : risques extrêmes sous-estimés.
- Optimisation de Markowitz sensible à l'erreur d'estimation des rendements espérés.
- Données Yahoo Finance gratuites, sans garantie d'exactitude.
- Fiscalité simplifiée (pas de barème progressif, plafonds de 150 000 € non modélisés) ; SRI approché par la volatilité.
- Stress tests et attribution calculés sur des indices hors dividendes et, pour les stress tests, en devise locale.

*Outil pédagogique : les résultats ne constituent pas un conseil en investissement.*
