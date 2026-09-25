# Étape 3 — Reconstituer l'historique du portefeuille jour par jour

## Objectif

Jusqu'ici, le programme donnait une **photo** du portefeuille aujourd'hui. Il va maintenant produire le **film** : la valeur du portefeuille chaque jour de bourse, depuis ton premier achat.

C'est l'étape la plus importante du projet. Les rendements, la volatilité, le ratio de Sharpe et le max drawdown (étapes 4 et 5) se calculent tous à partir de cette série quotidienne.

Tu obtiendras :

- un tableau de la valeur **en fin de chaque mois** ;
- le **plus haut** atteint par le portefeuille ;
- un **graphique** `graphique_historique.png` ;
- un fichier `data/historique.csv` avec toutes les données jour par jour.

## A. Installer la mise à jour

Même méthode qu'à l'étape 2 :

1. Dézippe `mise_a_jour_etape3.zip`.
2. Copie tout son contenu dans ton dossier `portfolio_tracker` et choisis **Remplacer**.
   Ton fichier `transactions.csv` n'est pas touché.
3. Installe la bibliothèque de graphiques :

```
python -m pip install matplotlib
```

Nouveaux fichiers : `src/graphiques.py`, `GUIDE_ETAPE_3.md`.
Fichiers modifiés : `src/portfolio.py`, `src/market_data.py`, `main.py`, `tests/test_portfolio.py`, `README.md`, `requirements.txt`.

## B. Lancer le programme

```
python main.py
```

Le début est identique à l'étape 2. Une nouvelle partie **HISTORIQUE** s'ajoute à la fin (les chiffres ci-dessous sont un exemple, **les tiens seront différents**) :

```
HISTORIQUE
Source de l'historique : Yahoo Finance (en direct)
Période : du 15/01/2024 au 24/09/2026 (681 jours de bourse)

Valeur en fin de mois :
          valeur  apports_nets    gain
01/2024   4250.0        4202.0    48.0
02/2024   6610.0        6544.0    66.0
...

Plus haut : ... € le ...
Gain au dernier jour (historique) : ... €  (à comparer au GAIN TOTAL ci-dessus)
```

**Vérifie que les deux gains sont égaux** : celui de la ligne « GAIN TOTAL » et celui de la ligne « Gain au dernier jour ». On les obtient par deux méthodes de calcul différentes, donc s'ils sont égaux, les calculs sont cohérents. Un petit écart est possible si la bourse est ouverte au moment où tu lances le programme (les cours bougent entre les deux téléchargements).

Ensuite, ouvre `graphique_historique.png` dans la colonne de gauche de VS Code :

- la **courbe bleue** = ce que vaut le portefeuille ;
- la **ligne orange en escalier** = l'argent que tu as mis de ta poche ;
- **l'écart entre les deux** = ton gain (ou ta perte) à chaque date.

Lance aussi les tests : `python -m pytest`. Résultat attendu : **14 passed**.

## C. Comprendre la méthode (à savoir expliquer à l'oral)

### 1. Les quantités détenues chaque jour

Pour chaque titre, on part de 0 et on ajoute les achats et retire les ventes au fil du temps. Exemple avec TotalEnergies :

| Date | Opération | Quantité détenue |
|---|---|---|
| avant le 05/04/2024 | — | 0 |
| 05/04/2024 | achat de 20 | 20 |
| 18/09/2024 | vente de 10 | 10 |

En pandas, c'est une **somme cumulée** (`cumsum`).

### 2. La valeur du jour

```
valeur du jour = Σ (quantité détenue × cours de clôture du jour)
```

### 3. Les flux et les apports nets

Un **flux** est de l'argent qui entre dans le portefeuille ou qui en sort :

| Opération | Flux | Pourquoi |
|---|---|---|
| Achat | + (quantité × prix + frais) | tu sors de l'argent de ta poche |
| Vente | − (quantité × prix − frais) | l'argent revient dans ta poche |
| Dividende | − montant | l'argent revient dans ta poche |

Les **apports nets** sont la somme de tous les flux depuis le début : l'argent encore « investi de ta poche ». On en déduit :

```
gain = valeur − apports nets
```

### 4. Deux détails qui montrent ta rigueur

- **Transactions le week-end** : une opération datée d'un samedi est rattachée au lundi suivant, car il n'y a pas de cours le week-end.
- **Cours non ajustés** : Yahoo propose aussi des cours « ajustés des dividendes ». Comme nous comptons déjà les dividendes dans les flux, les cours ajustés les compteraient **deux fois**. On utilise donc les cours réels. C'est typiquement le genre de question qu'un professeur peut poser.

### 5. Le lien avec l'étape suivante

Une simple variation de la valeur ne mesure pas la performance. Quand tu achètes pour 1 000 €, la valeur monte de 1 000 € sans que tu aies gagné quoi que ce soit. À l'étape 4, on calculera un rendement qui **neutralise ces apports** : le TWR (rendement pondéré par le temps). C'est pour ça qu'on a besoin de la colonne `flux`.

## D. Exercices

1. Ouvre `data/historique.csv` dans VS Code. Trouve le jour de la vente TotalEnergies (18/09/2024) : que devient la colonne `flux` ce jour-là ? Et les `apports_nets` ?
2. Sur le graphique, repère les marches de la ligne orange et associe chacune à une transaction de ton fichier.
3. Question pour le rapport : pourquoi le gain peut-il être négatif les premiers jours, même si le cours n'a pas bougé ? (Indice : les frais.)

## E. Si ça ne marche pas

| Message | Solution |
|---|---|
| `No module named 'matplotlib'` | `python -m pip install matplotlib` |
| `Invalid frequency: ME` | Ta version de pandas est ancienne : `python -m pip install --upgrade pandas` |
| `Historique de cours manquant pour : [...]` | Un ticker est mal écrit ou n'existe plus sur Yahoo |
| Le graphique ne s'affiche pas | Clique sur `graphique_historique.png` dans la colonne de gauche de VS Code |

Quand tout fonctionne, envoie-moi une capture du graphique. L'**étape 4** calculera les vrais indicateurs de performance et de risque : rendement TWR, TRI, volatilité et max drawdown.
