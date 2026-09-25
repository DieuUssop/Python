# Étape 7 — L'optimisation de Markowitz

## Objectif

Jusqu'ici, on **mesurait** le portefeuille. On va maintenant chercher à l'**améliorer**, grâce à la théorie moderne du portefeuille de **Harry Markowitz** (1952, prix Nobel 1990).

On répond à trois questions :

1. Quel est le portefeuille **le moins risqué possible** avec mes titres ?
2. Quel portefeuille offre le **meilleur rendement pour le risque pris** (Sharpe maximal) ?
3. Mon portefeuille actuel est-il **efficient**, ou pourrais-je faire mieux à risque égal ?

## A. Installer la mise à jour

1. Dézippe `mise_a_jour_etape7.zip` et copie son contenu dans `portfolio_tracker` (**Remplacer**).
2. Installe SciPy, la bibliothèque de calcul scientifique qui contient l'optimiseur :

```
python -m pip install scipy
```

Nouveaux fichiers : `src/optimisation.py`, `tests/test_optimisation.py`, `GUIDE_ETAPE_7.md`.
Fichiers modifiés : `src/config.py`, `src/analyse.py`, `src/graphiques.py`, `src/graphiques_interactifs.py`, `main.py`, `app.py`, `requirements.txt`, `README.md`.

## B. Lancer

**Version texte :**

```
python main.py
```

Une nouvelle partie s'ajoute à la fin (exemple, **tes chiffres seront différents**) :

```
OPTIMISATION DE MARKOWITZ (poids maximal par titre : 30%)

                          Rendement espéré   Volatilité    Sharpe
  Mon portefeuille                 9.96%        8.03%      0.93
  Variance minimale               11.36%        5.97%      1.48
  Sharpe maximal                  32.64%        9.21%      3.27

Répartition (en %) et ajustement vers le portefeuille de Sharpe maximal
                   nom  actuel %  var. min %  Sharpe max %  à acheter (+) / vendre (-) €
CW8.PA  Amundi MSCI World  31.5       9.0          0.0              -14200.0
...
```

Deux nouveaux graphiques : `graphique_frontiere.png` et `graphique_poids.png`.

**Tableau de bord :** `python -m streamlit run app.py`, puis le nouvel onglet **🎯 Optimisation**. Déplace le curseur « Poids maximal par titre » et observe la frontière se déformer.

**Tests :** `python -m pytest`. Résultat attendu : **38 passed**.

## C. Comprendre la théorie (le cœur de l'oral)

### 1. Les deux ingrédients

Pour chaque titre, on estime à partir de l'historique :

- **μ (mu)**, le **rendement annuel espéré** = moyenne des rendements quotidiens × 252 ;
- **Σ (sigma)**, la **matrice de covariance** annuelle = covariance des rendements quotidiens × 252. Sur sa diagonale se trouve la variance de chaque titre ; ailleurs, la façon dont deux titres varient ensemble.

### 2. Rendement et risque d'un portefeuille

Avec des poids w (par exemple 30 % LVMH, 20 % BNP…) :

```
rendement  = Σ wᵢ × μᵢ                    (moyenne pondérée : simple)
variance   = Σ Σ wᵢ × wⱼ × cov(i, j)       (pas une simple moyenne !)
```

**C'est là que réside la magie de la diversification.** Le rendement est une simple moyenne, mais le risque est **inférieur** à la moyenne des risques dès que les titres ne sont pas parfaitement corrélés.

> Exemple : deux titres indépendants de volatilité 20 %, à 50/50, donnent une volatilité de 20 % / √2 = **14,1 %**, et non 20 %. On a gagné en risque sans rien perdre en rendement. Un test automatique vérifie exactement ce calcul.

### 3. La frontière efficiente

Pour chaque niveau de rendement, il existe **un** portefeuille qui minimise le risque. L'ensemble de ces portefeuilles forme la **frontière efficiente** (la courbe noire du graphique).

- **Sous la frontière** : portefeuilles **inefficaces**. On pourrait obtenir plus de rendement pour le même risque.
- **Au-dessus** : **impossible** à atteindre avec ces titres.
- Les milliers de **points bleus** sont des portefeuilles tirés au hasard. Aucun ne dépasse la frontière : c'est une vérification visuelle de l'optimisation (elle est aussi testée automatiquement).

**Où est ton portefeuille (point orange) ?** Plus il est loin sous la frontière, plus il y a de marge d'amélioration.

### 4. Les deux portefeuilles remarquables

| Portefeuille | Ce qu'on cherche | Sur le graphique |
|---|---|---|
| **Variance minimale** (losange vert d'eau) | Le risque le plus faible possible | Le point le plus à gauche de la frontière |
| **Sharpe maximal** (étoile verte) | Le meilleur rendement par unité de risque | Là où la droite pointillée touche la frontière |

La **droite pointillée** est la **droite de marché des capitaux** (Capital Market Line). Elle part du taux sans risque et touche la frontière au portefeuille de Sharpe maximal, qu'on appelle aussi le **portefeuille tangent**. En combinant ce portefeuille avec un placement sans risque, on obtient les meilleures combinaisons rendement/risque possibles : c'est le **théorème de séparation de Tobin**.

### 5. Comment l'ordinateur trouve la solution

C'est un problème d'**optimisation sous contraintes** :

```
minimiser    wᵀ Σ w           (la variance)
sous contraintes :
    Σ wᵢ = 100 %              (tout le capital est investi)
    0 ≤ wᵢ ≤ poids max        (pas de vente à découvert, pas de concentration)
```

On utilise `scipy.optimize.minimize` avec la méthode **SLSQP** (Sequential Least Squares Programming), qui gère ce type de contraintes. Les tests vérifient que l'optimiseur retrouve les **solutions exactes** connues. Par exemple, pour 2 titres :

```
w₁ = (σ₂² − σ₁₂) / (σ₁² + σ₂² − 2 σ₁₂)
```

### 6. Pourquoi un poids maximal ?

Sans limite, l'optimiseur met souvent **tout sur 2 ou 3 titres** : ceux qui ont le mieux marché dans le passé. C'est dangereux. Pour comparaison, la réglementation des fonds (OPCVM) limite chaque ligne à 10 %, avec une tolérance jusqu'à 40 % pour l'ensemble des lignes dépassant 5 %.

## D. Les limites de Markowitz (indispensable dans le rapport)

Un professeur attend un **regard critique**. Voici les principales limites :

1. **L'erreur d'estimation.** μ est estimé sur moins de 3 ans : c'est très imprécis. L'optimiseur « croit » ces chiffres et surexploite les titres qui ont le mieux marché récemment. Un Sharpe optimal très élevé (> 2) doit te mettre la puce à l'oreille : il est presque certainement trop optimiste. Michaud (1989) a surnommé Markowitz un « maximiseur d'erreurs ».
2. **L'instabilité.** Change un peu la période et les poids optimaux changent beaucoup.
3. **L'hypothèse de normalité.** La variance ne mesure pas bien le risque de krach (on l'a vu avec la VaR à l'étape 5).
4. **Les dividendes.** On utilise des cours non ajustés : les dividendes ne sont pas dans μ, ce qui désavantage les titres à fort rendement (TotalEnergies, BNP…).
5. **Les frais et les impôts.** Rééquilibrer coûte des frais de courtage et déclenche des impôts sur les plus-values. Ils sont ignorés ici.

**Pistes d'amélioration** (à citer, sans forcément les coder) : le modèle de **Black-Litterman** (1992), les estimateurs « shrinkage » de **Ledoit-Wolf** pour Σ, ou la **parité des risques** (risk parity), qui n'utilise pas μ du tout.

## E. Exercices

1. Ton portefeuille (point orange) est-il loin de la frontière ? Calcule de combien tu pourrais réduire la volatilité **à rendement égal**. Lis sur la frontière la volatilité correspondant à ton rendement.
2. Dans le tableau de bord, passe le poids maximal de 30 % à « sans limite ». Combien de titres restent dans le portefeuille de Sharpe maximal ? Qu'en penses-tu ?
3. Le portefeuille de variance minimale contient-il beaucoup de ton ETF MSCI World ? Explique pourquoi avec la corrélation et la diversification.
4. **Question pour le rapport** : suivrais-tu les ajustements proposés ? Argumente avec les limites de la partie D.

## F. Si ça ne marche pas

| Message | Solution |
|---|---|
| `No module named 'scipy'` | `python -m pip install scipy` |
| `Impossible : avec N titres et un poids maximal de …` | Pas assez de titres pour ce poids maximal : augmente `POIDS_MAX` dans `src/config.py` |
| `L'optimisation n'a pas convergé` | Rare. Change légèrement `POIDS_MAX` et relance, ou envoie-moi une capture |

Prochaine étape, la **8** (bonus) : une **simulation de Monte-Carlo** pour projeter la valeur future du portefeuille, un **rapport PDF** généré automatiquement et la **gestion des devises** pour pouvoir ajouter des actions américaines.
