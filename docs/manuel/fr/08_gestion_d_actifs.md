# Gestion d'actifs
<!-- chapitre: gestion | ordre: 8 -->

Ce chapitre présente l'espace « Gestion d'actifs », qui reprend les outils d'un gérant de portefeuille. L'onglet **Attribution de performance** explique l'écart avec un indice mondial par le modèle de Brinson-Fachler. L'onglet **Budget de risque** mesure d'où vient le risque et compare votre répartition à la parité des risques. L'onglet **Backtest de stratégies** teste le rééquilibrage et l'investissement progressif sur l'historique réel. Chaque fiche donne la formule exacte, un exemple chiffré et les limites.

## Que contient l'espace Gestion d'actifs ?
<!-- fiche: gestion-presentation | questions: à quoi sert l'espace gestion d'actifs ; ou trouver le backtest ; ou est le budget de risque ; ou est l'attribution de performance ; que puis je faire dans gestion d'actifs ; différence entre gestion d'actifs et analyse du portefeuille | mots: gestion d'actifs, asset management, attribution, budget de risque, backtest, parité des risques, rééquilibrage, DCA, gérant | aller: Gestion d'actifs -->

L'espace **Gestion d'actifs** se choisit dans le menu « Espace de travail » de la barre latérale. Il analyse le même portefeuille, avec les mêmes paramètres, que l'espace « Analyse du portefeuille ». Il comprend trois onglets.

| Onglet | Question à laquelle il répond |
|---|---|
| Attribution de performance | Pourquoi le portefeuille a-t-il fait mieux (ou moins bien) qu'un indice mondial ? Choix des régions ou choix des titres ? |
| Budget de risque | Quelles lignes apportent le plus de risque ? Que donnerait une répartition où chaque ligne apporte autant de risque ? |
| Backtest de stratégies | Aurait-il mieux valu rééquilibrer régulièrement ? Investir en une fois ou progressivement ? |

### À savoir

- L'attribution télécharge des indices régionaux : il faut Internet au premier affichage, ensuite un cache prend le relais.
- Le budget de risque et le backtest utilisent les cours déjà chargés pour l'analyse.
- Le diagnostic de diversification (régions, secteurs, devises, corrélations) se trouve dans l'onglet Expositions de l'espace « Analyse du portefeuille » : l'onglet Budget de risque le rappelle par une note.
- Les principaux résultats figurent aussi dans le rapport PDF (backtest avec 0,1 % de frais et comparaison sur 10 000 € en 12 mois).

En cas d'erreur, chaque onglet affiche un message « … indisponible » suivi de la cause, sans bloquer les autres.

## L'attribution de performance de Brinson-Fachler
<!-- fiche: gestion-brinson-fachler | questions: pourquoi mon portefeuille a fait moins bien que l'indice ; c'est quoi l'effet allocation ; c'est quoi l'effet sélection ; effet interaction explication ; comment lire l'attribution de performance ; brinson fachler formule ; est ce que j'ai bien choisi mes titres ou mes régions ; d'où vient ma surperformance | mots: attribution de performance, Brinson-Fachler, effet allocation, effet sélection, effet interaction, surperformance, sous-performance, écart à l'indice, régions | aller: Gestion d'actifs/Attribution de performance | chiffres: twr_total -->

L'onglet **Attribution de performance** décompose l'écart de rendement entre votre portefeuille et un indice de référence, **région par région**, en trois effets.

### Les formules exactes (pour un mois)

```
Effet allocation  = (wp − wb) × (rb − Rb)
Effet sélection   = wb × (rp − rb)
Effet interaction = (wp − wb) × (rp − rb)
```

- `wp`, `wb` : poids de la région dans le portefeuille et dans l'indice ;
- `rp`, `rb` : rendement de la région dans le portefeuille et dans l'indice ;
- `Rb` : rendement total de l'indice = Σ wb × rb.

La somme des trois effets sur toutes les régions est égale à l'écart `Rp − Rb`.

### L'intuition

- **Allocation** : avez-vous surpondéré les régions qui ont fait mieux que l'indice global ?
- **Sélection** : dans chaque région, vos titres ont-ils fait mieux que l'indice de cette région ?
- **Interaction** : effet croisé, positif si vous avez surpondéré une région où vous avez aussi bien choisi.

### Exemple vérifié

| Région | wp | rp | wb | rb |
|---|---|---|---|---|
| États-Unis | 50 % | +10 % | 70 % | +8 % |
| Europe | 50 % | +2 % | 30 % | +4 % |

Rb = 0,7 × 8 % + 0,3 × 4 % = **6,8 %** ; Rp = 0,5 × 10 % + 0,5 × 2 % = **6,0 %** ; écart **−0,8 point**.

| Région | Allocation | Sélection | Interaction |
|---|---|---|---|
| États-Unis | (−0,2) × (8 − 6,8) = −0,24 | 0,7 × 2 = +1,40 | (−0,2) × 2 = −0,40 |
| Europe | 0,2 × (4 − 6,8) = −0,56 | 0,3 × (−2) = −0,60 | 0,2 × (−2) = −0,40 |
| **Total** | **−0,80** | **+0,80** | **−0,80** |

Somme : −0,80 + 0,80 − 0,80 = **−0,80 point**, soit exactement l'écart. Lecture : la sélection de titres américains a été bonne, mais la surpondération de l'Europe, qui a fait moins bien que l'indice, a coûté.

### Ce qui est affiché

Six cartes (Portefeuille, Indice de référence, Écart, Effet allocation, Effet sélection, Effet interaction), le graphique « Effets par région », le graphique « Effets cumulés dans le temps » et le tableau « Détail par région ». Dans ce tableau, les poids du portefeuille sont des **moyennes mensuelles** et les rendements des régions sont **composés** sur la période.

### Règles particulières

- une région absente de l'indice prend `rb = Rb` : ses effets d'allocation et de sélection sont nuls, tout passe dans l'**interaction** ;
- une région absente du portefeuille prend `rp = rb` : seul l'effet d'allocation joue.

## Pourquoi un « lissage de Cariño » ? Le calcul mois par mois
<!-- fiche: gestion-carino | questions: c'est quoi le lissage de cariño ; pourquoi la somme des effets mensuels ne donne pas l'écart ; comment sont additionnés les mois dans l'attribution ; que montre le graphique des effets cumulés ; pourquoi calculer l'attribution chaque mois ; attribution multi périodes ; linking des effets | mots: Cariño, lissage, linking, multi-période, composition, effets cumulés, mois par mois, coefficient logarithmique | aller: Gestion d'actifs/Attribution de performance -->

L'attribution est calculée **mois par mois**, avec les poids du début de chaque mois, puis les mois sont reliés.

### Le problème

Les rendements se composent : +10 % puis +10 % donnent +21 %, pas +20 %. Additionner les écarts mensuels ne redonne donc pas l'écart total.

### La méthode de Cariño (1999)

Chaque effet mensuel est multiplié par un facteur `kₜ / K` :

```
kₜ = [ln(1 + Rpₜ) − ln(1 + Rbₜ)] / (Rpₜ − Rbₜ)     (rendements du mois t)
K  = [ln(1 + Rp)  − ln(1 + Rb)]  / (Rp − Rb)       (rendements composés de toute la période)
si les deux rendements sont égaux : k = 1 / (1 + R)
effet relié du mois t = effet du mois t × kₜ / K
```

Ainsi, la somme des effets reliés est **exactement** égale à l'écart composé `Rp − Rb`. Un test automatique du logiciel le vérifie.

### Exemple vérifié

Deux mois : portefeuille +10 % puis +10 % (Rp = 21 %), indice +5 % puis +5 % (Rb = 10,25 %).

- Écart réel : 21 % − 10,25 % = **10,75 points** ; somme des écarts mensuels : 5 + 5 = 10 points.
- kₜ = (ln 1,10 − ln 1,05) / 0,05 = 0,9304 ; K = (ln 1,21 − ln 1,1025) / 0,1075 = 0,8655.
- Facteur = 0,9304 / 0,8655 = **1,075** ; chaque mois vaut 5 × 1,075 = 5,375 points ; total **10,75 points**. Le compte est juste.

### Le découpage en mois

Le logiciel prend le dernier jour de bourse de chaque mois de l'historique (la dernière date disponible compte comme fin du mois en cours) et calcule chaque mois d'une fin de mois à la suivante. Il faut au moins deux fins de mois ; sinon le message « Historique trop court : il faut au moins deux fins de mois » s'affiche.

### Le graphique « Effets cumulés dans le temps »

Il trace la somme cumulée des effets reliés d'allocation, de sélection et d'interaction, mois après mois. Les trois courbes finissent sur les valeurs des cartes. Une courbe qui monte régulièrement signale un effet persistant ; un saut, un mois exceptionnel.

### Limite

Les poids sont figés au début de chaque mois : un achat ou une vente en cours de mois n'est pris en compte que le mois suivant. Le rendement « Portefeuille » est donc celui des positions, et peut différer légèrement du TWR de l'onglet Performance.

## Quel indice de référence pour l'attribution ? Régions et poids
<!-- fiche: gestion-indice-reference-attribution | questions: à quel indice est comparé mon portefeuille dans l'attribution ; pourquoi ce n'est pas l'indice choisi dans les paramètres ; poids des régions de l'indice msci acwi ; quels indices sont utilisés pour chaque région ; l'indice de l'attribution inclut il les dividendes ; pourquoi les etats unis pèsent 63 % | mots: MSCI ACWI IMI, indice de référence, benchmark, poids régionaux, S&P 500, Euro Stoxx 50, Nikkei, indices régionaux, conversion en euros | aller: Gestion d'actifs/Attribution de performance -->

L'attribution compare votre portefeuille à un **indice actions mondial reconstitué**, et **non** à l'indice choisi avec le menu [[Indice de référence]] des Paramètres. La carte « Indice de référence » le précise : « MSCI ACWI (poids régionaux) ».

### Les poids de l'indice

Ce sont les poids régionaux du **MSCI ACWI IMI au 30/06/2026**, renormalisés pour que leur somme fasse 100 % (la somme brute vaut 99,6 %) :

| Région | Poids brut | Poids utilisé | Indice représentatif |
|---|---|---|---|
| États-Unis | 62,7 % | 62,95 % | S&P 500 (^GSPC) |
| Émergents | 12,3 % | 12,35 % | EEM |
| Europe (hors Royaume-Uni et Suisse) | 8,7 % | 8,73 % | Euro Stoxx 50 (^STOXX50E) |
| Japon | 5,6 % | 5,62 % | Nikkei 225 (^N225) |
| Royaume-Uni | 3,1 % | 3,11 % | FTSE 100 (^FTSE) |
| Canada | 3,0 % | 3,01 % | ^GSPTSE |
| Asie-Pacifique | 2,3 % | 2,31 % | ^AXJO |
| Suisse | 1,9 % | 1,91 % | ^SSMI |

```
poids utilisé = poids brut / 99,6
```

### Le calcul

Chaque mois, le rendement de l'indice est `Rb = Σ poids de la région × rendement de son indice`. Les cours des indices sont **convertis en euros** avec les taux de change, pour être comparables à votre portefeuille.

### Comment vos titres sont classés

Chaque titre est rangé dans une région d'après le référentiel de titres du logiciel. Un titre absent du référentiel est classé « Non classé ».

### Limites

- **Indices hors dividendes** : les indices régionaux ignorent les dividendes. Vos cours n'en tiennent pas compte non plus, ce qui garde la comparaison homogène, mais les deux rendements sont sous-estimés, d'autant plus que les régions distribuent beaucoup.
- **Un seul indice par région**, souvent de grandes capitalisations (Euro Stoxx 50 pour l'Europe).
- **Attribution par région seulement**, pas par secteur.
- Les poids de l'indice sont fixes sur toute la période.

## Attribution d'un portefeuille diversifié ou d'un ETF monde
<!-- fiche: gestion-attribution-poche-actions | questions: pourquoi mes obligations ne sont pas dans l'attribution ; c'est quoi la poche actions ; mon etf monde est non classé dans l'attribution ; message n'est pas classé dans une région de l'indice ; attribution indisponible aucune action ; l'attribution a t elle un sens pour un seul etf ; pourquoi tout est dans l'effet interaction | mots: poche actions, portefeuille diversifié, obligations exclues, ETF monde, non classé, interaction, attribution indisponible, lignes directes | aller: Gestion d'actifs/Attribution de performance -->

### Seule la poche actions est analysée

L'indice de référence est un indice d'**actions**. Pour un portefeuille diversifié (actions, obligations, or), le logiciel compare donc seulement les **actions** à cet indice, comme le fait un gérant pour chaque « poche ». Les obligations et l'or sont exclus. Un titre absent du référentiel est considéré comme une action.

Si les actions représentent moins de 99,5 % du portefeuille, une note l'indique avec leur poids actuel : « l'attribution porte sur la poche actions (x % du portefeuille aujourd'hui) ». S'il n'y a aucune action, l'onglet affiche « Attribution indisponible » avec la mention « aucune action dans le portefeuille ».

### Le cas des ETF monde

Un ETF monde est rangé dans la région « Monde (ETF) », qui n'existe pas dans l'indice. Le logiciel lui applique la règle des régions absentes de l'indice (`wb = 0`, `rb = Rb`) :

```
allocation  = wp × (Rb − Rb) = 0
sélection   = 0 × (rp − Rb)  = 0
interaction = wp × (rp − Rb)
```

Tout l'écart de cette ligne passe dans l'**effet d'interaction**. Exemple : un ETF monde qui pèse 50 % et fait 9 % quand l'indice fait 6,8 % donne une interaction de 0,5 × 2,2 = **+1,1 point**. Les régions de l'indice absentes du portefeuille produisent alors un effet d'allocation (par exemple, une Europe à 30 % dans l'indice et 0 % chez vous, qui fait 4 % contre 6,8 % : (0 − 0,3) × (4 − 6,8) = **+0,84 point**).

### L'avertissement affiché

Si plus de 20 % du portefeuille n'est pas classé dans une région de l'indice (ETF monde, titres absents du référentiel), une note prévient que l'attribution est surtout pertinente pour un **portefeuille de lignes directes**, comme le portefeuille d'exemple « actions monde ». Pour un portefeuille composé d'un ou deux ETF, l'onglet Performance (comparaison à l'indice, alpha, tracking error) est plus parlant.

## Le budget de risque : quelles lignes apportent le plus de risque ?
<!-- fiche: gestion-contributions-risque | questions: quelle ligne apporte le plus de risque à mon portefeuille ; c'est quoi la contribution au risque ; pourquoi la part du risque est différente du poids ; plus gros contributeur au risque ; contribution marginale explication ; budget de risque comment lire ; propriété d'euler | mots: budget de risque, contribution au risque, contribution marginale, Euler, part du risque, risk budgeting, volatilité, décomposition du risque | aller: Gestion d'actifs/Budget de risque | chiffres: volatilite, nb_titres -->

Le poids d'une ligne ne dit pas quelle part du **risque** elle apporte : une action très volatile et très corrélée au reste du portefeuille pèse plus dans le risque que dans la valeur. L'onglet **Budget de risque** fait cette décomposition.

### Les formules exactes

```
volatilité du portefeuille σp = √(wᵀ Σ w)
contribution marginale    CMᵢ = (Σ w)ᵢ / σp
contribution au risque    CRᵢ = wᵢ × CMᵢ
part du risque               = CRᵢ / σp          (la somme fait 100 %)
```

`Σ` est la matrice de covariance annuelle, estimée comme dans l'onglet Optimisation (rendements quotidiens × 252, sur la période commune de vos titres actuels).

**Propriété d'Euler** : la somme des contributions est exactement égale à la volatilité du portefeuille (Σ CRᵢ = σp). Un test automatique le vérifie.

### Exemple vérifié

Deux titres à 50 / 50 : A (volatilité 20 %), B (volatilité 10 %), corrélation 0,2 (covariance 0,004).

- σp = √(0,25 × 0,04 + 0,25 × 0,01 + 2 × 0,25 × 0,004) = **12,04 %** ;
- CM_A = (0,04 × 0,5 + 0,004 × 0,5) / 0,1204 = 0,1827 ; CR_A = 0,5 × 0,1827 = 0,0914 ;
- CM_B = (0,004 × 0,5 + 0,01 × 0,5) / 0,1204 = 0,0581 ; CR_B = 0,0291 ;
- parts du risque : A **75,9 %**, B **24,1 %**, pour des poids de 50 / 50.

### Ce qui est affiché

- trois cartes : « Volatilité actuelle », « Plus gros contributeur » (sa part du risque, son nom et sa part de la valeur) et « Volatilité en parité des risques » ;
- le graphique « Part de la valeur et part du risque » : pour les 20 plus gros contributeurs, une barre gris-bleu clair (part de la valeur) et une barre bleue (part du risque).

### Interprétation

Une ligne dont la **part du risque dépasse sa part de la valeur** est plus volatile ou plus corrélée au reste que la moyenne. Une part du risque négative est possible pour une ligne qui baisse quand les autres montent (couverture).

### Limites

Le risque est mesuré par la seule volatilité, sur la période observée. Les corrélations peuvent changer, surtout en crise.

## La parité des risques (risk parity)
<!-- fiche: gestion-parite-risques | questions: c'est quoi la parité des risques ; risk parity explication ; pourquoi la parité des risques n'utilise pas les rendements ; comment est calculée la parité des risques ; all weather bridgewater ; volatilité en parité des risques ; faut il passer en parité des risques ; méthode de spinu | mots: parité des risques, risk parity, equal risk contribution, ERC, Spinu, All Weather, allocation sans rendement espéré, contributions égales | aller: Gestion d'actifs/Budget de risque | chiffres: volatilite -->

La **parité des risques** est une répartition où **chaque ligne contribue autant** au risque du portefeuille. Elle a été popularisée par le fonds « All Weather » de Bridgewater.

### Pourquoi elle est intéressante

Elle n'utilise **pas les rendements espérés**, très mal estimés, mais seulement les volatilités et les corrélations. C'est une réponse directe à la principale limite de Markowitz (voir le chapitre sur l'optimisation).

### Le calcul (méthode de Spinu, 2013)

Le logiciel minimise la fonction :

```
½ wᵀ Σ w − (1/n) × Σ ln(wᵢ)
```

en partant de poids inversement proportionnels aux volatilités (méthode L-BFGS-B de scipy, poids strictement positifs). Les poids obtenus sont ensuite renormalisés pour que leur somme fasse 100 %. À l'optimum, toutes les contributions au risque sont égales.

### Exemple vérifié

Titres A (volatilité 20 %) et B (volatilité 10 %), corrélation 0,2, rendements espérés 8 % et 4 %, taux sans risque 2,5 % :

| Allocation | Poids A / B | Volatilité | Parts du risque | Sharpe |
|---|---|---|---|---|
| Portefeuille 50 / 50 | 50 % / 50 % | 12,04 % | 75,9 % / 24,1 % | 0,29 |
| Parité des risques | 33,3 % / 66,7 % | 10,33 % | 50 % / 50 % | 0,27 |

Le titre le plus volatil reçoit moins de poids. Avec deux titres, la parité des risques revient à pondérer par l'inverse des volatilités (1/0,20 et 1/0,10, soit 1/3 et 2/3).

### Interprétation

La parité des risques réduit en général la volatilité et augmente la diversification du risque. Elle ne maximise pas le rendement : son Sharpe peut être inférieur, comme dans l'exemple. Avec des actions et des obligations, elle donne beaucoup de poids aux obligations, moins volatiles.

### Limites

- les fonds de parité des risques utilisent souvent un effet de levier pour relever le rendement : ce n'est pas le cas ici ;
- les poids dépendent des volatilités et corrélations passées ;
- aucun plafond par titre n'est appliqué.

## Comparer quatre répartitions : ratio de diversification et nombre effectif de paris
<!-- fiche: gestion-quatre-allocations | questions: c'est quoi le nombre effectif de paris ; ratio de diversification formule ; comment lire le tableau quatre façons de répartir les mêmes titres ; équipondéré c'est quoi ; contribution maximale ça veut dire quoi ; mon portefeuille a 30 lignes mais seulement 5 paris ; voir les poids de la parité des risques | mots: nombre effectif de paris, ratio de diversification, équipondéré, variance minimale, contribution maximale, concentration du risque, comparaison d'allocations | aller: Gestion d'actifs/Budget de risque | chiffres: nb_titres, sharpe -->

Le tableau « Quatre façons de répartir les mêmes titres » compare, avec **vos titres actuels** :

| Allocation | Principe |
|---|---|
| Portefeuille actuel | vos poids d'aujourd'hui |
| Équipondéré | le même poids pour chaque ligne (1/n) |
| Parité des risques | chaque ligne apporte la même part du risque |
| Variance minimale | la volatilité la plus faible possible, **sans plafond par titre** |

Attention : cette variance minimale n'applique aucun plafond, contrairement à celle de l'onglet Optimisation (plafond réglable). Elle peut donc être plus concentrée.

### Les colonnes et leurs formules

```
Rendement espéré         = Σ wᵢ × μᵢ                     (μ = moyenne quotidienne × 252)
Volatilité               = √(wᵀ Σ w)
Sharpe                   = (rendement espéré − taux sans risque) / volatilité
Ratio de diversification = Σ wᵢ × σᵢ / σp
Nombre effectif de paris = 1 / Σ (part du risqueᵢ)²
Contribution maximale    = plus grande part du risque d'une ligne
```

### Exemple vérifié

Deux titres A (20 %) et B (10 %), corrélation 0,2, à 50 / 50 :

- ratio de diversification = (0,5 × 0,20 + 0,5 × 0,10) / 0,1204 = **1,25** ;
- nombre effectif de paris = 1 / (0,759² + 0,241²) = **1,58** ;
- contribution maximale = 75,9 %.

En parité des risques : ratio 1,29, nombre effectif de paris **2,0**, contribution maximale 50 %.

### Interprétation

- **Ratio de diversification** : 1 signifie aucune diversification (tous les titres parfaitement corrélés) ; plus il est élevé, plus les titres se compensent.
- **Nombre effectif de paris** : combien de lignes « indépendantes » le portefeuille représente vraiment du point de vue du risque. Il vaut n si toutes les lignes contribuent également, 1 si une seule ligne porte tout le risque. Un portefeuille de 69 lignes peut ne valoir qu'une trentaine de paris.
- **Contribution maximale** : la dépendance à une seule ligne.

Le panneau [[Voir les poids de chaque allocation]] affiche les poids (en %) de chaque titre dans les quatre allocations.

### Limites

Les rendements espérés sont historiques (même fragilité que dans l'onglet Optimisation) ; les autres colonnes ne dépendent que des volatilités et corrélations passées.

## Le backtest : faut-il rééquilibrer son portefeuille ?
<!-- fiche: gestion-backtest-reequilibrage | questions: faut il rééquilibrer mon portefeuille ; rééquilibrage mensuel trimestriel ou annuel lequel est le mieux ; c'est quoi l'achat conservation ; comment lire le backtest ; buy and hold ou rééquilibrage ; le backtest utilise t il mes vraies opérations ; quand a lieu le rééquilibrage | mots: backtest, rééquilibrage, achat-conservation, buy and hold, mensuel, trimestriel, annuel, poids cibles, stratégie, simulation historique | aller: Gestion d'actifs/Backtest de stratégies | chiffres: volatilite, max_drawdown -->

L'onglet **Backtest de stratégies** rejoue l'historique réel avec **les mêmes titres et les mêmes poids de départ** que votre portefeuille actuel, selon quatre stratégies.

| Stratégie | Règle |
|---|---|
| Achat-conservation | on achète une fois, on ne touche plus à rien : les poids dérivent avec les cours |
| Rééquilibrage mensuel | retour aux poids de départ le premier jour de bourse de chaque mois |
| Rééquilibrage trimestriel | le premier jour de bourse de chaque trimestre |
| Rééquilibrage annuel | le premier jour de bourse de chaque année |

Le premier jour de la période n'est pas un jour de rééquilibrage. Toutes les stratégies paient les frais sur l'achat initial.

### Ce n'est pas votre historique réel

Le backtest suppose que vous aviez acheté **dès le début** les poids actuels. Il ignore vos vraies opérations. La période commence au premier jour où **tous** vos titres actuels ont un cours, dans la période d'analyse du portefeuille.

### Le mécanisme du rééquilibrage

```
montant échangé = Σ |valeur cible de la ligne − valeur actuelle de la ligne|
frais           = taux de frais × montant échangé
nouvelle valeur = valeur − frais, répartie selon les poids cibles
```

### Ce qui est affiché

- le graphique « Rééquilibrer ou non ? », en base 100 ;
- le tableau « Résultats » : Rendement annualisé, Volatilité, Max drawdown, Sharpe, Rotation / an.

```
Rendement annualisé = (valeur finale / valeur initiale)^(365 / nombre de jours) − 1
Volatilité          = écart-type des rendements quotidiens × √252
Max drawdown        = plus forte baisse depuis un plus haut
Sharpe              = (rendement annualisé − taux sans risque) / volatilité
```

Exemple de Sharpe : rendement annualisé 8 %, volatilité 14 %, taux sans risque 2,5 % : (8 − 2,5) / 14 = **0,39**.

### Interprétation

Rééquilibrer revient à **vendre ce qui a monté pour acheter ce qui a baissé**. Cela maintient le risque voulu, mais coûte des frais et freine la performance quand une tendance dure (les gagnants sont allégés trop tôt). En marché sans tendance, avec des allers-retours, le rééquilibrage peut au contraire être payant. L'achat-conservation laisse grossir les gagnants : son risque dérive avec le temps.

## Les frais et la rotation du backtest
<!-- fiche: gestion-backtest-frais-rotation | questions: c'est quoi la rotation par an ; combien coûtent les rééquilibrages ; comment régler les frais de transaction du backtest ; que veut dire rotation 40 % ; frais de courtage dans le backtest ; pourquoi le rééquilibrage mensuel rapporte moins | mots: frais de transaction, rotation, turnover, coûts, courtage, frais de rééquilibrage, coût du rééquilibrage | aller: Gestion d'actifs/Backtest de stratégies | chiffres: frais_totaux -->

### Le réglage

Le curseur [[Frais de transaction (%)]] va de 0 à 0,5 %, par pas de 0,05, avec **0,10 %** au départ. Les frais s'appliquent aux montants achetés ou vendus, y compris à l'achat initial. Le sous-titre du graphique rappelle le taux choisi.

### La rotation

```
rotation d'un rééquilibrage = montant échangé / valeur du portefeuille
Rotation / an = somme des rotations / nombre d'années de la période (jours / 365)
```

Le montant échangé compte les ventes **et** les achats : une rotation de 10 % correspond à 5 % du portefeuille vendu et 5 % racheté.

### Exemple vérifié

Deux titres à 50 / 50 sur 100 €. Après un mois, A a pris 10 % et B a perdu 10 % : les lignes valent 55 € et 45 €. Le rééquilibrage ramène chaque ligne à 50 € :

- montant échangé = |50 − 55| + |50 − 45| = **10 €** ;
- frais à 0,1 % = **0,01 €** ;
- rotation = 10 / 100 = **10 %**.

Avec les frais de l'achat initial (0,1 %), le portefeuille vaut 99,90 € avant ce rééquilibrage et 99,89 € après.

### Interprétation

Plus la fréquence est élevée, plus la rotation et les frais montent. La colonne « Rotation / an » permet d'estimer le coût annuel : rotation × taux de frais. Par exemple, 40 % de rotation par an à 0,1 % coûtent 0,04 % par an. Les écarts de performance entre stratégies viennent souvent davantage de l'effet de tendance que des frais.

### Limites

Les frais sont proportionnels : pas de frais fixes par ordre, pas d'écart achat-vente, pas d'impôt sur les plus-values réalisées lors des ventes (qui pèse sur un compte-titres).

## Investir en une fois ou progressivement (DCA) ?
<!-- fiche: gestion-dca | questions: vaut il mieux investir en une fois ou petit à petit ; c'est quoi le dca ; dollar cost averaging explication ; investissement progressif sur 12 mois ; que devient l'argent en attente ; valeur la plus basse c'est quoi ; pourquoi investir en une fois rapporte plus ; lisser ses achats en bourse | mots: DCA, dollar cost averaging, investissement progressif, versements programmés, lump sum, en une fois, market timing, liquidités | aller: Gestion d'actifs/Backtest de stratégies -->

La seconde partie de l'onglet **Backtest de stratégies** compare deux façons d'investir un même capital dans le même panier de titres (poids actuels, sans rééquilibrage ensuite).

### Les réglages

- [[Capital pour la comparaison DCA (€)]] : de 1 000 € à 10 000 000 €, par pas de 1 000, **10 000 €** au départ ;
- [[Durée de l'investissement progressif (mois)]] : de 3 à 24 mois, **12** au départ ;
- les frais du curseur [[Frais de transaction (%)]] s'appliquent à chaque achat.

### Les deux stratégies

- **En une fois** : tout le capital est investi le premier jour de la période.
- **Progressif** : le capital est divisé en parts égales, investies le premier jour de bourse de chacun des premiers mois. L'argent en attente est rémunéré au **taux sans risque** des Paramètres :

```
part mensuelle = capital / nombre de mois
taux quotidien des liquidités = (1 + taux sans risque)^(1/252) − 1
valeur = parts du panier détenues × valeur du panier + liquidités
```

### Exemple

10 000 € sur 12 mois : 833,33 € par mois. Avec 0,1 % de frais, chaque versement achète pour 833,33 × 0,999 = **832,50 €** de titres. Avec un taux sans risque de 2,5 %, les liquidités rapportent (1,025)^(1/252) − 1 ≈ **0,0098 %** par jour de bourse.

### Ce qui est affiché

Le graphique des deux courbes de valeur, en euros, et le tableau « Comparaison » : Valeur finale, Gain (valeur finale − capital) et Valeur la plus basse atteinte pendant la période.

### Interprétation

Sur un marché haussier, investir **en une fois** rapporte en général davantage : l'argent travaille plus tôt. L'investissement **progressif** réduit le risque d'investir juste avant une baisse : sa valeur la plus basse est souvent plus élevée, d'autant qu'une partie reste en liquidités au début. C'est un compromis entre rendement espéré et regret.

### Limites

- un seul historique : le résultat dépend entièrement de la période observée ;
- si la période compte moins de mois que la durée choisie, le capital est réparti sur les mois disponibles ;
- cours hors dividendes.

## Les limites du backtest
<!-- fiche: gestion-backtest-limites | questions: peut on se fier au backtest ; le backtest garantit il les résultats futurs ; pourquoi le backtest est court ; backtest indisponible que faire ; les dividendes sont ils inclus dans le backtest ; biais du backtest | mots: limites, backtest, biais, surapprentissage, période courte, hors dividendes, performance passée, robustesse | aller: Gestion d'actifs/Backtest de stratégies -->

Un backtest dit ce qui **aurait** marché sur une période passée. Il ne garantit rien pour l'avenir.

### Les limites propres au logiciel

- **Une seule période** : celle de votre portefeuille, à partir du jour où tous vos titres actuels ont un cours. Si l'un de vos titres est récent, la période est courte, et les conclusions fragiles.
- **Cours hors dividendes** : les rendements sont un peu sous-estimés, de la même façon pour toutes les stratégies.
- **Titres choisis aujourd'hui** : le backtest teste des titres que vous détenez **maintenant**, souvent parce qu'ils ont bien marché. C'est un biais de sélection.
- **Frais simplifiés** : proportionnels, sans impôt sur les ventes.
- **Pas de vos vraies opérations** : les poids de départ sont vos poids actuels.

### Bonne pratique

Comparez les stratégies entre elles plutôt que de retenir un chiffre absolu, et regardez ensemble rendement, volatilité, max drawdown et rotation.

### En cas de message « Backtest indisponible »

Le message est suivi de la cause. Il apparaît par exemple si l'historique commun de vos titres est vide ou trop court. Vérifiez vos cours avec [[Actualiser les cours]].
