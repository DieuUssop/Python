# Étape 8 — Les bonus : Monte-Carlo, devises et rapport PDF

## Objectif

Trois fonctionnalités qui distinguent un projet « très bien » d'un projet « excellent » :

1. **Projection Monte-Carlo** : combien vaudra le portefeuille dans 10 ans ? Pas une réponse unique, mais un éventail de scénarios avec leurs probabilités.
2. **Devises étrangères** : pouvoir ajouter Apple, Microsoft ou une action de Londres, converties automatiquement en euros.
3. **Rapport PDF** : un document de 7 pages généré automatiquement, idéal à joindre au rapport écrit.

## A. Installer la mise à jour

1. Dézippe `mise_a_jour_etape8.zip` et copie son contenu dans `portfolio_tracker` (**Remplacer**).
2. Installe reportlab, la bibliothèque qui crée les PDF :

```
python -m pip install reportlab
```

Nouveaux fichiers : `src/simulation.py`, `src/devises.py`, `src/rapport.py`, `tests/test_simulation.py`, `tests/test_devises.py`, `GUIDE_ETAPE_8.md`.
Fichiers modifiés : `main.py`, `app.py`, `src/analyse.py`, `src/portfolio.py`, `src/config.py`, `src/graphiques.py`, `src/graphiques_interactifs.py`, `requirements.txt`, `README.md`.

3. Lance les tests : `python -m pytest`. Résultat attendu : **52 passed**.

## B. Lancer

**Version texte :** `python main.py`

- Une nouvelle section **PROJECTION MONTE-CARLO** s'affiche à la fin.
- Le fichier **`rapport_portefeuille.pdf`** est créé dans ton dossier. Ouvre-le !

**Tableau de bord :** `python -m streamlit run app.py`

- Nouvel onglet **Projection**, avec des curseurs : horizon, versement mensuel, rendement supposé, objectif, méthode.
- Dans la barre latérale, rubrique **Rapport** : clique sur « Préparer le rapport PDF », puis sur « Télécharger le rapport ».

## C. La simulation de Monte-Carlo

### Le principe

On ne peut pas prédire **le** futur, mais on peut en simuler **des milliers**, tous cohérents avec le rendement et le risque du portefeuille. Ensuite, on regarde la distribution des résultats :

| Résultat | Signification |
|---|---|
| Scénario **médian** | 1 chance sur 2 de faire mieux, 1 sur 2 de faire moins bien |
| Scénario **défavorable** (5e percentile) | 1 chance sur 20 de faire pire |
| Scénario **favorable** (95e percentile) | 1 chance sur 20 de faire mieux |
| **Probabilité de perte** | Part des scénarios qui finissent sous l'argent investi |

Sur le graphique en éventail, la zone foncée contient 50 % des scénarios et la zone claire 90 %. L'éventail **s'élargit avec le temps** : l'incertitude s'accumule.

### Méthode 1 : la loi normale (mouvement brownien géométrique)

Chaque mois, le log-rendement est tiré au hasard dans une loi normale :

```
log-rendement mensuel ~ Normale( (μ − σ²/2) / 12 ,  σ / √12 )
```

C'est le modèle de **Black-Scholes**. D'où vient le terme **− σ²/2** ? Il y a une différence entre moyenne arithmétique et croissance composée. Un exemple : +50 % puis −50 % donne une moyenne de 0 %, pourtant 100 € deviennent 150 €, puis 75 €, soit une **perte** de 25 %. Plus la volatilité est forte, plus cet écart est grand (c'est le **lemme d'Itô**).

> Un test automatique vérifie que la médiane simulée est bien égale à la valeur théorique V₀ × e^((μ − σ²/2) × T).

### Méthode 2 : le rééchantillonnage historique (bootstrap)

Chaque mois simulé est construit en tirant au hasard **21 vrais jours de bourse** de ton portefeuille. Avantage : on garde les **vrais krachs** (les queues épaisses), que la loi normale sous-estime.

Compare les deux méthodes dans le tableau de bord : le scénario défavorable est-il plus sévère avec la méthode historique ?

### Les limites (à écrire dans le rapport)

- **Le rendement supposé est déterminant.** Par défaut, c'est le rendement historique de ton portefeuille, calculé sur moins de 3 ans : il peut être très optimiste. Dans le tableau de bord, réduis-le à 5 ou 6 % par an (ordre de grandeur de long terme des actions) pour une projection plus prudente.
- Les rendements sont supposés **indépendants** d'un mois à l'autre : pas de cycles économiques.
- Il n'y a ni **inflation**, ni **impôts**, ni **frais de gestion**.

## D. Les devises étrangères

### Comment ajouter une action étrangère

Dans `data/transactions.csv`, saisis le prix **dans la devise de cotation**, comme sur Yahoo Finance :

```
2024-03-04,ACHAT,AAPL,Apple,10,175.10,1.99
2024-06-03,ACHAT,ULVR.L,Unilever,20,4226.00,1.99
```

- **AAPL** : prix en **dollars** (175,10 $) ;
- **ULVR.L** (Londres) : prix en **pence** (4 226 pence = 42,26 £). C'est ainsi que Yahoo affiche les actions britanniques ;
- **frais** : toujours en **euros** (frais facturés par ton courtier français).

Le programme détecte seul la devise de chaque titre. Il convertit ensuite chaque transaction **au taux de change du jour de l'opération**, puis la valeur actuelle au taux d'aujourd'hui. Les tableaux indiquent la devise de chaque ligne.

### Le risque de change

Une action étrangère expose à **deux risques** : la variation du cours et celle de la devise.

> Exemple (vérifié par un test) : l'action reste à 100 $, mais l'euro passe de 1,00 $ à 1,25 $. En euros, l'action vaut 100 € puis 80 € : **−20 %**, alors qu'elle n'a pas bougé en dollars !

C'est une excellente remarque à faire à l'oral. Elle explique aussi pourquoi certains ETF sont « couverts contre le risque de change » (*hedged*).

## E. Le rapport PDF

Le rapport contient 7 pages :

1. **Synthèse** : chiffres clés et évolution du portefeuille ;
2. **Positions** : tableau détaillé et corrélations ;
3. **Performance** : comparaison avec l'indice et rendements annuels ;
4. **Risque** : drawdown, volatilité, Sharpe, VaR ;
5. **Optimisation** de Markowitz ;
6. **Projection** Monte-Carlo ;
7. **Méthodologie** et limites.

Il est généré avec **reportlab**. Le principe : on construit une liste d'éléments (titres, tableaux, images) et reportlab les répartit automatiquement sur les pages. Les graphiques sont ceux de matplotlib, dessinés en mémoire puis insérés comme images.

**Conseil :** joins ce PDF en annexe de votre rapport écrit. Il montre que l'outil produit un livrable exploitable par un client, ce qui est un vrai plus pour un Master G2C.

## F. Exercices

1. Dans l'onglet Projection, fixe un **objectif** (par exemple le double de la valeur actuelle). Quelle est la probabilité de l'atteindre en 10 ans ? Et en 20 ans ?
2. Compare un versement de **0 €** et de **200 € par mois** sur 20 ans. Que devient la probabilité de perte ? Explique l'effet de l'investissement régulier.
3. Ajoute une action américaine dans ton fichier de transactions (voir la partie D). Relance et observe sa ligne dans les positions : sa performance en euros est-elle égale à sa performance en dollars ?
4. Ouvre le rapport PDF et relis-le comme le ferait ton professeur : que faudrait-il ajouter ou retirer ?

## G. Si ça ne marche pas

| Problème | Solution |
|---|---|
| `No module named 'reportlab'` | `python -m pip install reportlab` |
| « Taux de change introuvables » | Pas d'Internet au premier lancement avec un titre étranger : connecte-toi et relance |
| Une action étrangère a une valeur 100 fois trop grande ou trop petite | Vérifie que le prix est saisi comme sur Yahoo (en pence pour Londres) |
| Le PDF ne s'ouvre pas | Ferme-le dans ton lecteur PDF avant de relancer `python main.py` (Windows bloque un fichier ouvert) |

Prochaine et dernière étape, la **9** : les finitions. On préparera la documentation, le plan du rapport écrit et la soutenance (plan de présentation, démonstration, questions probables du jury).
