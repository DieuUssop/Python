# Étape 4 — Mesurer la performance et le risque

## Objectif

Jusqu'ici, on savait **combien** le portefeuille a rapporté en euros. On va maintenant répondre aux vraies questions d'un gérant :

- **Est-ce que mes choix de placement sont bons ?** → TWR
- **Quel rendement a obtenu mon argent, compte tenu de quand je l'ai placé ?** → TRI
- **Quel risque ai-je pris ?** → volatilité, max drawdown

## A. Installer la mise à jour

1. Dézippe `mise_a_jour_etape4.zip`.
2. Copie son contenu dans ton dossier `portfolio_tracker` et choisis **Remplacer**.
3. Aucune nouvelle bibliothèque à installer.

Nouveaux fichiers : `src/metrics.py`, `tests/test_metrics.py`, `GUIDE_ETAPE_4.md`.
Fichiers modifiés : `src/graphiques.py`, `main.py`, `README.md`.

## B. Lancer le programme

```
python main.py
```

Une nouvelle partie s'ajoute à la fin (exemple, **tes chiffres seront différents**) :

```
PERFORMANCE ET RISQUE
Période analysée          : du 15/01/2024 au 24/09/2026

Performance
  TWR total               : +21.48 %
  TWR annualisé           : +7.49 %
  TRI (annuel)            : +5.07 %

Risque
  Volatilité annualisée   : 12.39 %
  Max drawdown            : -15.82 %
      du plus haut le 16/01/2026 au plus bas le 08/09/2026
      plus haut pas encore retrouvé
  Meilleur jour           : +7.47 % le 10/01/2025
  Pire jour               : -4.50 % le 12/06/2024

Rendement par année civile (TWR)
  2024                    : +9.02 %
  2025                    : +25.48 %
  2026                    : -11.20 %
```

Un nouveau graphique `graphique_performance.png` apparaît :

- **en haut** : la performance « pure » du portefeuille, en base 100 ;
- **en bas** : le drawdown, c'est-à-dire la baisse par rapport au dernier plus haut.

Tests : `python -m pytest`. Résultat attendu : **22 passed**.

## C. Comprendre les indicateurs (c'est le cœur de la soutenance)

### 1. Le rendement quotidien « nettoyé » des apports

Si tu achètes pour 1 000 € aujourd'hui, la valeur du portefeuille monte de 1 000 €, mais tu n'as rien gagné. On retire donc l'argent apporté :

```
            valeur(t) − flux(t)
r(t) =  ---------------------  − 1
             valeur(t−1)
```

On considère que les achats et ventes se font **au cours du jour**, donc en fin de journée : l'argent apporté aujourd'hui n'a pas encore « travaillé ».

> Anecdote à raconter : ma première version supposait les achats faits en *début* de journée. Un test automatique a montré que cette hypothèse faussait le rendement les jours d'achat. C'est exactement à ça que servent les tests.

### 2. TWR, le rendement pondéré par le temps

On enchaîne les rendements quotidiens :

```
TWR = (1 + r1) × (1 + r2) × … × (1 + rn) − 1
```

**Ce qu'il mesure : la qualité des choix de placement**, peu importe quand et combien tu as investi. C'est la mesure officielle des gérants de fonds (normes GIPS), car un gérant ne décide pas quand ses clients déposent de l'argent. C'est aussi la seule mesure qu'on peut comparer à un indice comme le CAC 40.

**Annualisé** : `(1 + TWR)^(365 / nombre de jours) − 1`
Exemple : +21 % en 2 ans donne **+10 % par an**, et non 10,5 %, car les gains se composent.

### 3. TRI, le rendement pondéré par l'argent

C'est le taux `i` qui rend nulle la somme actualisée de tous les flux :

```
Σ  flux / (1 + i)^(années écoulées)  = 0
```

Du point de vue de l'investisseur : un achat est négatif (l'argent sort), une vente ou un dividende est positif. Le dernier jour, on fait « comme si » on vendait tout.

**Ce qu'il mesure : le rendement réellement obtenu par TON argent.** Il dépend du calendrier : investir beaucoup juste avant une hausse améliore le TRI.

Aucune formule ne donne `i` directement. On le trouve **par dichotomie** : on essaie un taux, on regarde si le résultat est trop haut ou trop bas, et on coupe l'intervalle en deux, 200 fois de suite.

### TWR ou TRI : pourquoi deux mesures ?

| | TWR | TRI |
|---|---|---|
| Question | Mes choix de titres sont-ils bons ? | Combien mon argent a-t-il rapporté ? |
| Dépend des apports ? | Non | Oui |
| Utilisé par | les gérants, pour se comparer à un indice | l'investisseur, le private equity |

**Si ton TRI est plus faible que ton TWR**, tu as investi davantage au mauvais moment (juste avant des baisses). S'il est plus élevé, ton timing a été bon. C'est une excellente analyse à mettre dans ton rapport.

### 4. La volatilité

C'est l'écart-type des rendements quotidiens, ramené à l'année :

```
volatilité annuelle = écart-type quotidien × √252
```

Il y a environ **252 jours de bourse** par an. Pourquoi une racine carrée ? Si les jours sont indépendants, les *variances* s'additionnent (× 252), donc l'écart-type est multiplié par √252.

Ordres de grandeur : un fonds monétaire ≈ 0,5 %, un fonds actions monde ≈ 15 %, une action seule ≈ 25-35 %.

### 5. Le max drawdown

C'est la **pire perte subie** : la baisse maximale entre un plus haut et le plus bas qui suit.

Exemple : 100 → 120 → 90 → 130. Le max drawdown est 90 / 120 − 1 = **−25 %**.

On le calcule sur l'indice base 100, **pas sur la valeur en euros**. Sinon, une simple vente (qui fait baisser la valeur) serait prise pour une perte.

C'est l'indicateur qui « parle » le plus à un client : « Au pire moment, vous auriez perdu 25 % ».

## D. Exercices

1. Compare ton **TWR annualisé** et ton **TRI**. Lequel est le plus élevé ? Explique pourquoi avec ton calendrier d'achats.
2. Regarde les dates du **meilleur** et du **pire jour**. Correspondent-elles à un jour de transaction ? Si oui, vérifie le prix saisi dans le CSV : un prix très différent du cours du jour crée un faux rendement ce jour-là.
3. Sur `graphique_performance.png`, repère la période du max drawdown. Que s'est-il passé sur les marchés à ce moment ? (Une phrase de contexte économique dans le rapport, c'est un vrai plus.)
4. Calcule à la main le TWR de l'année 2024 à partir de l'indice base 100 : ouvre `data/historique.csv` et… tu verras qu'il manque une colonne. Ce sera un bon exercice d'ajout de code pour toi : ajoute la colonne `indice` au fichier exporté.

## E. Si ça ne marche pas

| Message | Solution |
|---|---|
| `No module named 'src.metrics'` | `metrics.py` n'a pas été copié dans le dossier `src` |
| `ImportError: cannot import name 'graphique_performance'` | `src/graphiques.py` n'a pas été remplacé |
| TRI affiché `+nan %` | Aucune solution trouvée entre −99 % et +1 000 % par an : cas très rare, envoie-moi une capture |

Prochaine étape, la **5** : les indicateurs avancés. On compare le portefeuille à un indice de référence (MSCI World ou CAC 40) avec le bêta, l'alpha et la tracking error. On ajoute aussi les ratios de Sharpe et de Sortino, la VaR et la matrice de corrélation entre tes titres.
