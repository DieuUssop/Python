# Optimisation et projection
<!-- chapitre: optim | ordre: 6 -->

Ce chapitre explique les deux onglets prospectifs de l'espace « Analyse du portefeuille ». L'onglet **Optimisation** applique la théorie de Markowitz à vos titres : frontière efficiente, portefeuilles de variance minimale et de Sharpe maximal, et tableau « de → à » des changements à faire. L'onglet **Projection** simule des milliers d'évolutions possibles de votre portefeuille par la méthode de Monte-Carlo. Chaque fiche donne la formule exacte du logiciel, un exemple chiffré et les limites à garder en tête.

## Que fait l'onglet Optimisation ? Le principe de Markowitz
<!-- fiche: optim-principe-markowitz | questions: c'est quoi l'optimisation de markowitz ; a quoi sert l'onglet optimisation ; comment le logiciel trouve le meilleur portefeuille ; pourquoi diversifier réduit le risque ; théorie moderne du portefeuille expliquée simplement ; que veut dire portefeuille optimal ; comment marche l'optimiseur ; markowitz c'est quoi au juste | mots: Markowitz, théorie moderne du portefeuille, diversification, optimisation, moyenne-variance, covariance, corrélation, allocation optimale, SLSQP | aller: Analyse du portefeuille/Optimisation | chiffres: sharpe, volatilite, nb_titres -->

L'onglet **Optimisation** cherche, **parmi les titres que vous détenez déjà**, d'autres répartitions qui offriraient un meilleur couple rendement / risque. Il n'ajoute aucun titre : il ne fait que changer les poids.

### L'idée de Markowitz (1952)

Un investisseur ne regarde pas seulement le rendement, mais aussi le risque. Or le risque d'un portefeuille n'est pas la moyenne des risques de ses titres : quand deux titres ne montent et ne baissent pas exactement ensemble (corrélation inférieure à 1), leurs variations se compensent en partie. On peut donc réduire le risque sans réduire le rendement.

### Les deux formules au cœur du calcul

```
Rendement espéré du portefeuille = Σ wᵢ × μᵢ            (wᵀ μ)
Variance du portefeuille         = Σ Σ wᵢ × wⱼ × covᵢⱼ   (wᵀ Σ w)
Volatilité                       = √variance
```

où `wᵢ` est le poids du titre i, `μᵢ` son rendement annuel espéré et `covᵢⱼ` la covariance annuelle entre les titres i et j.

### Exemple chiffré

Deux titres : A (rendement 8 %, volatilité 20 %) et B (rendement 4 %, volatilité 10 %), corrélation 0,2.

- Portefeuille 50 / 50 : rendement = 0,5 × 8 % + 0,5 × 4 % = **6 %**. Variance = 0,25 × 0,04 + 0,25 × 0,01 + 2 × 0,25 × 0,2 × 0,20 × 0,10 = 0,0145, soit une volatilité de **12,04 %**, nettement moins que la moyenne des volatilités (15 %).
- Portefeuille de variance minimale : 14,3 % de A et 85,7 % de B, volatilité **9,56 %**, plus faible que celle de B seul (10 %) alors qu'il contient un titre deux fois plus risqué.

C'est tout l'intérêt de la diversification.

### Ce que calcule le logiciel

1. le rendement espéré et la matrice de covariance de vos titres ;
2. le portefeuille de **variance minimale** (le moins risqué possible) ;
3. le portefeuille de **Sharpe maximal** (le meilleur rendement par unité de risque) ;
4. la **frontière efficiente** (40 points) ;
5. un nuage de 4 000 portefeuilles tirés au hasard, pour visualiser l'ensemble des possibles.

Trois cartes, sous le curseur du poids maximal, donnent, pour le portefeuille actuel, la variance minimale et le Sharpe maximal, le ratio de Sharpe, le rendement et la volatilité.

### Les contraintes retenues

- pas de vente à découvert : chaque poids est positif ou nul ;
- tout le capital est investi : la somme des poids vaut 100 % ;
- un poids maximal par titre, réglable avec le curseur [[Poids maximal par titre]].

L'optimisation numérique utilise la méthode SLSQP de la bibliothèque scipy (500 itérations au plus), en partant de poids égaux. Le tout reste un exercice académique : le logiciel le rappelle sous les résultats, ce n'est pas un conseil en investissement.

## Comment sont estimés le rendement espéré et le risque de chaque titre ?
<!-- fiche: optim-estimation-parametres | questions: d'où viennent les rendements espérés de l'optimisation ; comment est calculée la matrice de covariance ; pourquoi multiplier par 252 ; sur quelle période l'optimisation est elle calculée ; les rendements espérés sont ils des prévisions ; mu et sigma c'est quoi ; le rendement espéré de mon titre est énorme c'est normal ; l'optimisation prend elle les dividendes | mots: rendement espéré, mu, covariance, matrice de covariance, sigma, 252 jours, estimation, historique, annualisation | aller: Analyse du portefeuille/Optimisation | chiffres: volatilite -->

L'optimisation a besoin de deux ingrédients, estimés sur l'**historique** de vos titres.

### Les formules exactes

```
μ (rendement annuel espéré) = moyenne des rendements quotidiens × 252
Σ (covariance annuelle)      = covariance des rendements quotidiens × 252
Rendement quotidien          = cours du jour / cours de la veille − 1
```

252 est le nombre conventionnel de jours de bourse dans une année. Sur la diagonale de Σ figurent les variances de chaque titre ; ailleurs, la façon dont deux titres varient ensemble. La volatilité d'un titre seul vaut √(variance annuelle).

### Exemple

Un titre gagne en moyenne 0,04 % par jour, avec un écart-type quotidien de 1,2 % :

- μ = 0,0004 × 252 = **10,08 %** par an ;
- volatilité = 1,2 % × √252 = **19,05 %** par an.

### Sur quelle période ?

- Les cours utilisés sont ceux de la période d'analyse du portefeuille, qui commence à votre première opération.
- Seuls les jours où **tous** vos titres actuels ont un rendement sont gardés. Un titre récemment introduit en bourse raccourcit donc la période pour tous les autres.
- Les cours sont convertis en euros et ne sont pas ajustés des dividendes (voir le chapitre sur les sources) : pour un titre qui distribue beaucoup, μ est un peu sous-estimé.

### Interprétation

μ n'est pas une prévision : c'est la moyenne observée sur le passé, extrapolée à un an. Sur une période courte et favorable, un titre peut afficher un μ de 40 % ou plus, ce qui ne dit rien de l'avenir. C'est la première source de fragilité de l'optimisation (voir la fiche sur les limites).

## Lire le graphique de la frontière efficiente
<!-- fiche: optim-frontiere-efficiente | questions: c'est quoi la frontière efficiente ; comment lire le graphique de l'optimisation ; que représentent les points bleus ; c'est quoi la droite en pointillés ; pourquoi aucun point ne dépasse la courbe ; ou est mon portefeuille sur le graphique ; que signifie l'étoile verte ; les petits points gris avec des noms | mots: frontière efficiente, efficient frontier, nuage de portefeuilles, droite de marché des capitaux, capital market line, portefeuille tangent, Dirichlet, graphique rendement risque | aller: Analyse du portefeuille/Optimisation | chiffres: sharpe, volatilite -->

Le graphique de la section « Frontière efficiente » place chaque portefeuille selon sa **volatilité annuelle** (axe horizontal) et son **rendement annuel espéré** (axe vertical). Le meilleur endroit est en haut à gauche : beaucoup de rendement pour peu de risque.

### Les éléments du graphique

| Élément | Ce qu'il représente |
|---|---|
| Points bleus (« Portefeuilles aléatoires ») | 4 000 répartitions tirées au hasard ; plus le bleu est foncé, plus le Sharpe est élevé (échelle à droite) |
| Courbe noire épaisse (« Frontière efficiente ») | pour chaque niveau de rendement, le portefeuille le moins risqué |
| Points gris avec un code | chaque titre seul (100 % du portefeuille sur ce titre) ; les codes ne s'affichent que jusqu'à 20 titres |
| Rond orange (« Mon portefeuille ») | votre répartition actuelle |
| Losange (« Variance minimale ») | le portefeuille le moins risqué |
| Étoile verte (« Sharpe maximal ») | le meilleur rendement par unité de risque |
| Droite en tirets (« Droite de marché des capitaux ») | combinaisons du placement sans risque et du portefeuille de Sharpe maximal |

Chaque portefeuille remarquable porte son Sharpe dans la légende. Survolez un point pour lire sa volatilité et son rendement.

### Comment est construite la frontière

Le logiciel fixe 40 rendements cibles, répartis régulièrement entre le rendement du portefeuille de variance minimale et le rendement maximal atteignable compte tenu du plafond par titre (on remplit les titres du plus rentable au moins rentable, chacun jusqu'au plafond). Pour chaque cible, il cherche les poids qui minimisent la variance `wᵀ Σ w`. Une cible impossible est simplement ignorée.

Sous la variance minimale, les portefeuilles sont « inefficaces » : on peut obtenir plus de rendement pour le même risque.

### Les portefeuilles aléatoires

Les poids sont tirés selon une loi de Dirichlet (tous positifs, somme égale à 100 %), avec un hasard fixé : le nuage est identique d'un affichage à l'autre. Ces portefeuilles ne respectent **pas** le plafond par titre. Comme la frontière est calculée avec ce plafond, quelques points peuvent dépasser légèrement une frontière très contrainte ; sans plafond, aucun ne la dépasse, ce qui vérifie visuellement l'optimisation.

### La droite de marché des capitaux

```
Rendement = taux sans risque + pente × volatilité
pente     = (rendement du Sharpe maximal − taux sans risque) / volatilité du Sharpe maximal
```

Elle part du taux sans risque (réglé dans [[Taux sans risque (% par an)]]) et touche la frontière au portefeuille de Sharpe maximal, d'où son autre nom de « portefeuille tangent ».

## Le réglage « Poids maximal par titre »
<!-- fiche: optim-poids-maximal | questions: à quoi sert le poids maximal par titre ; pourquoi l'optimiseur met tout sur deux titres ; comment limiter la concentration dans l'optimisation ; pourquoi je ne peux pas choisir 10 % ; le curseur ne propose que sans limite ; que veut dire sans limite ; quel plafond choisir ; la ligne en pointillés plafond 30 % | mots: poids maximal, plafond, contrainte, concentration, limite par ligne, OPCVM, diversification forcée, 30 % | aller: Analyse du portefeuille/Optimisation | chiffres: nb_titres -->

Le curseur [[Poids maximal par titre]], en haut de l'onglet Optimisation, fixe la part maximale qu'un titre peut prendre dans les portefeuilles optimisés (variance minimale, Sharpe maximal et frontière).

### Pourquoi un plafond ?

Sans limite, l'optimiseur concentre souvent tout sur 2 ou 3 titres : ceux qui ont le mieux marché par le passé. Le plafond impose un minimum de diversification. La valeur par défaut est **30 %**. Pour repère, la réglementation des fonds (OPCVM) limite chaque ligne à 10 %, avec une tolérance jusqu'à 40 % pour l'ensemble des lignes de plus de 5 %.

### Les valeurs proposées

10 %, 15 %, 20 %, 25 %, 30 %, 40 %, 50 % et « sans limite ». Seules les valeurs qui permettent d'investir 100 % du capital apparaissent :

```
condition : nombre de titres × poids maximal ≥ 100 %
```

Exemples :

- avec 3 titres, 30 % × 3 = 90 % : impossible. Le curseur ne propose que 40 %, 50 % et sans limite ;
- avec 5 titres, toutes les valeurs à partir de 20 % sont proposées ;
- avec 10 titres ou plus, toutes les valeurs sont proposées.

Si 30 % n'est pas possible (moins de 4 titres), le curseur démarre sur « sans limite ».

### Effet sur les résultats

Plus le plafond est bas, plus les portefeuilles optimisés ressemblent à un portefeuille équilibré, et plus leur Sharpe baisse un peu. Le plafond apparaît dans le graphique des répartitions comparées sous la forme d'une ligne verticale en tirets, légendée « Plafond 30 % par titre » (ou la valeur choisie).

Dans l'exemple à deux titres A (8 %, 20 %) et B (4 %, 10 %), corrélation 0,2, taux sans risque 2,5 % : sans limite, le Sharpe maximal place 56,3 % sur A (Sharpe 0,292) ; avec un plafond de 50 %, il est bloqué à 50 / 50 (Sharpe 0,291).

## Sharpe maximal ou variance minimale : lequel regarder ?
<!-- fiche: optim-sharpe-ou-variance | questions: quelle différence entre sharpe maximal et variance minimale ; quel portefeuille optimisé choisir ; le portefeuille de variance minimale c'est quoi ; portefeuille tangent explication ; pourquoi le sharpe maximal est plus risqué ; comment est calculé le sharpe dans l'optimisation ; lequel est le meilleur des deux | mots: Sharpe maximal, variance minimale, portefeuille tangent, minimum variance, ratio de Sharpe, rendement par unité de risque, allocation prudente | aller: Analyse du portefeuille/Optimisation | chiffres: sharpe, volatilite -->

Le logiciel calcule deux portefeuilles remarquables, avec les mêmes contraintes (poids positifs, somme 100 %, plafond par titre).

### Variance minimale

```
minimiser   wᵀ Σ w
```

C'est le portefeuille **le moins risqué possible** avec vos titres. Il **n'utilise pas les rendements espérés**, seulement les volatilités et les corrélations. C'est un avantage : les covariances s'estiment beaucoup mieux que les rendements. Il est souvent plus stable dans le temps.

### Sharpe maximal

```
Sharpe = (rendement espéré − taux sans risque) / volatilité
maximiser Sharpe   (en pratique : minimiser −Sharpe)
```

C'est le portefeuille qui offre **le meilleur rendement par unité de risque**. Combiné au placement sans risque, il donne la meilleure droite possible : c'est le portefeuille tangent. Il dépend directement des rendements espérés, donc de l'historique.

### Exemple

Titres A (8 %, 20 %) et B (4 %, 10 %), corrélation 0,2, taux sans risque 2,5 %, sans plafond :

| Portefeuille | Poids A / B | Rendement | Volatilité | Sharpe |
|---|---|---|---|---|
| Variance minimale | 14,3 % / 85,7 % | 4,57 % | 9,56 % | 0,22 |
| Sharpe maximal | 56,3 % / 43,7 % | 6,25 % | 12,87 % | 0,29 |

Le Sharpe est calculé ici sur le rendement espéré annuel (`wᵀ μ`) : il peut différer du ratio de Sharpe de l'onglet Performance, calculé sur les rendements réels du portefeuille.

### Lequel regarder ?

- **Variance minimale** : pour un investisseur prudent, ou si vous doutez des rendements passés.
- **Sharpe maximal** : pour la meilleure efficacité théorique, en acceptant qu'il exploite les titres qui ont le mieux marché.

Le sélecteur [[Comparer mon portefeuille à]] de la section « Répartitions comparées » permet d'afficher les changements à faire vers l'un ou l'autre. Par défaut, c'est le Sharpe maximal.

## Lire les « Répartitions comparées » : que faudrait-il changer ?
<!-- fiche: optim-repartitions-comparees | questions: comment lire les répartitions comparées ; que veulent dire les flèches vertes et rouges ; que dois je acheter ou vendre selon l'optimisation ; pourquoi certains titres n'apparaissent pas dans le graphique ; c'est quoi les barres actions obligations or ; que veut dire au total 35 % du portefeuille change de place ; vendre entièrement ça veut dire quoi ; titres inchangés pas affichés | mots: répartitions comparées, de à, flèches, rééquilibrage, renforcer, alléger, vendre entièrement, classes d'actifs, rotation, inchangé | aller: Analyse du portefeuille/Optimisation | chiffres: valeur_actuelle, nb_titres -->

La section « Répartitions comparées » traduit le résultat de l'optimisation en changements concrets, **à valeur totale inchangée et hors frais**. Choisissez d'abord la cible avec [[Comparer mon portefeuille à]] : [[Sharpe maximal]] ou [[Variance minimale]].

### 1. La phrase de synthèse

Elle cite les trois plus gros renforcements et les trois plus gros allègements, le nombre de titres qui sortent, la part du portefeuille qui change de place, et la classe d'actifs qui bouge le plus (si son poids varie d'au moins 5 points).

### 2. Les barres par classe d'actifs

Deux barres empilées à 100 % : « Actuel » et le portefeuille choisi, découpées en Actions, Obligations, Or, Monétaire. Elles n'apparaissent que si le portefeuille contient autre chose que des actions. Un titre absent du référentiel est compté comme une action.

### 3. Le graphique « de → à »

Pour chaque titre : un rond blanc au poids actuel et une flèche jusqu'au poids conseillé, avec l'étiquette « 40 % → 34,7 % ».

| Couleur | Sens | Règle du code |
|---|---|---|
| Vert, flèche vers la droite | À renforcer | écart positif |
| Rouge, flèche vers la gauche | À alléger | écart négatif |
| Rouge | À vendre entièrement | poids conseillé inférieur à 0,25 % |
| Non affiché | Inchangé | écart inférieur à 0,25 point en valeur absolue |

Le plus gros changement est en haut. Au plus 20 lignes sont dessinées ; une note sous le graphique indique le nombre de titres inchangés non affichés et le nombre de petits ajustements renvoyés au tableau détaillé.

### Les formules

```
écart    = poids conseillé − poids actuel
montant  = écart × valeur totale du portefeuille
rotation = Σ |écart| / 2
```

La rotation est la part du portefeuille à déplacer : chaque euro vendu est racheté ailleurs, d'où la division par 2.

### Exemple vérifié

Portefeuille de 50 000 €, cible Sharpe maximal :

| Titre | Classe | Actuel | Conseillé | Montant | Sens |
|---|---|---|---|---|---|
| Action X | Actions | 30 % | 0,1 % | −14 950 € | Vendre entièrement |
| Fonds obligataire | Obligations | 10 % | 30 % | +10 000 € | Renforcer |
| Or | Or | 5 % | 20 % | +7 500 € | Renforcer |
| ETF Monde | Actions | 40 % | 34,7 % | −2 650 € | Alléger |
| Action Y | Actions | 15 % | 15,2 % | +100 € | Inchangé |

Rotation = (29,9 + 20 + 15 + 5,3 + 0,2) / 2 = **35,2 %**. La synthèse dit : renforcer Fonds obligataire et Or ; alléger Action X et ETF Monde ; 1 titre sort entièrement ; 35 % du portefeuille change de place ; la part en actions passe de 85 % à 50 %.

Notez que « Vendre entièrement » est affiché dès que le poids conseillé passe sous 0,25 %, même si le montant calculé n'est pas tout à fait égal à la valeur de la ligne.

## Le tableau « Détail des ajustements » : combien acheter ou vendre ?
<!-- fiche: optim-detail-ajustements | questions: combien dois je acheter de chaque titre ; ou voir les montants à acheter et vendre ; le tableau des ajustements ; colonne conseillé c'est quoi ; les frais sont ils compris dans les montants ; je ne trouve pas un titre dans le graphique des flèches ; exporter les ordres à passer | mots: détail des ajustements, montants, acheter, vendre, ordres, arbitrage, conseillé, réallocation | aller: Analyse du portefeuille/Optimisation | chiffres: valeur_actuelle -->

Sous le graphique « de → à », le panneau replié [[Détail des ajustements (montants à acheter / vendre)]] liste **tous** les titres, y compris les inchangés et ceux qui ne tiennent pas dans le graphique.

### Les colonnes

| Colonne | Contenu |
|---|---|
| Titre | nom du titre |
| Classe | classe d'actifs (Actions, Obligations, Or…) |
| Actuel | poids actuel, en % |
| Conseillé | poids dans le portefeuille cible choisi, en % |
| Acheter / vendre | `(poids conseillé − poids actuel) × valeur totale`, en euros, signé |
| Action | Renforcer, Alléger, Vendre entièrement ou Inchangé |

Les lignes sont triées du plus gros changement au plus petit. La somme des montants est nulle : les ventes financent les achats.

### Exemple

Portefeuille de 50 000 €, une ligne pèse 10 % et le portefeuille cible lui donne 30 % : montant = (0,30 − 0,10) × 50 000 = **+10 000 €** à acheter.

### Ce que les montants ne comprennent pas

- les **frais** de courtage ;
- les **impôts** sur les plus-values réalisées en vendant (voir l'espace Conseil patrimonial, onglet Fiscalité) ;
- l'arrondi au nombre entier de parts.

Il n'y a pas d'export d'ordres de bourse : le logiciel n'est relié à aucun courtier. Les ordres sont à passer vous-même auprès de votre établissement.

## Les limites de l'optimisation de Markowitz
<!-- fiche: optim-limites | questions: peut on faire confiance à l'optimisation ; pourquoi l'optimiseur recommande des choses absurdes ; limites de markowitz ; erreur d'estimation c'est quoi ; faut il suivre les recommandations de l'onglet optimisation ; les résultats changent beaucoup quand je change le plafond ; pourquoi le sharpe maximal mise sur les titres qui ont le plus monté | mots: limites, erreur d'estimation, maximiseur d'erreurs, instabilité, surapprentissage, rendements passés, biais, robustesse | aller: Analyse du portefeuille/Optimisation -->

L'optimisation de Markowitz est un outil pédagogique puissant, mais ses résultats doivent être lus avec prudence. Le logiciel l'affiche lui-même sous les résultats.

### 1. L'erreur d'estimation

Les rendements espérés μ sont la moyenne des rendements passés. Or une moyenne estimée sur quelques années est très imprécise. Ordre de grandeur : pour un titre de volatilité 20 % observé pendant 3 ans, l'erreur type sur le rendement annuel moyen vaut 20 % / √3 ≈ **11,5 points**. Un μ estimé à 10 % est donc compatible avec un vrai rendement compris entre environ −13 % et +33 %.

L'optimiseur prend ces chiffres au pied de la lettre : il **surexploite les titres qui ont le mieux marché** et délaisse ceux qui ont baissé. On le surnomme parfois « maximiseur d'erreurs ».

### 2. L'instabilité

Une petite variation des données (un mois de plus, un plafond différent) peut changer fortement les poids du Sharpe maximal. Le portefeuille de variance minimale, qui n'utilise pas μ, est plus stable.

### 3. Les hypothèses du modèle

- le risque se résume à la volatilité (les krachs, plus fréquents que ne le prévoit la loi normale, ne sont pas mieux pris en compte) ;
- les corrélations sont supposées stables, alors qu'elles montent souvent en période de crise ;
- un seul horizon, sans frais ni impôts de transaction.

### 4. Les limites propres au logiciel

- seuls vos titres actuels sont considérés ;
- la période d'estimation commence à votre première opération et se limite aux jours où tous les titres ont un cours ;
- cours hors dividendes.

### Comment s'en servir intelligemment

- comparez surtout votre portefeuille à la **variance minimale** ;
- abaissez le [[Poids maximal par titre]] pour obtenir des répartitions plus raisonnables ;
- voyez les écarts comme des pistes de réflexion, pas comme des ordres ;
- complétez avec l'onglet « Budget de risque » de l'espace Gestion d'actifs, dont la parité des risques n'utilise pas non plus les rendements espérés.

## Pourquoi l'onglet Optimisation demande-t-il au moins 2 titres ?
<!-- fiche: optim-deux-titres | questions: l'onglet optimisation est vide ; message il faut au moins 2 titres ; je n'ai qu'un etf pourquoi pas d'optimisation ; optimisation impossible pourquoi ; erreur l'optimisation n'a pas convergé ; comment optimiser un portefeuille avec un seul fonds | mots: deux titres, un seul titre, ETF unique, optimisation impossible, erreur, convergence, message | aller: Analyse du portefeuille/Optimisation | chiffres: nb_titres -->

Optimiser, c'est choisir une **répartition entre plusieurs titres**. Avec un seul titre, il n'y a qu'une répartition possible : 100 % sur ce titre. L'onglet affiche alors le message : « L'optimisation compare plusieurs répartitions entre titres : il faut au moins 2 titres dans le portefeuille. »

Le nombre de titres pris en compte est celui des **positions actuelles** du portefeuille.

### Si vous détenez un seul ETF

Un ETF monde contient des centaines d'actions, mais le logiciel le traite comme **un seul titre** dans l'optimisation : il ne peut pas modifier la composition interne du fonds. Pour utiliser l'onglet, il faut au moins deux lignes (par exemple un ETF actions et un ETF obligataire).

### Le message « Optimisation impossible »

Ce message, suivi d'une explication, apparaît en cas d'échec du calcul. Causes possibles :

- l'optimiseur numérique n'a pas convergé (message « L'optimisation n'a pas convergé ») ;
- un titre n'a pas assez d'historique commun avec les autres pour estimer les covariances.

Essayez un autre [[Poids maximal par titre]] ou [[Actualiser les cours]]. Si la frontière seule échoue alors que les deux portefeuilles remarquables sont calculés, le logiciel trace une frontière approchée (voir la fiche correspondante).

Avec 2 ou 3 titres, le curseur du poids maximal ne propose que des plafonds compatibles avec un investissement à 100 % et démarre sur « sans limite ».

## Pourquoi la frontière efficiente est-elle « approchée » ?
<!-- fiche: optim-frontiere-approchee | questions: pourquoi c'est écrit frontière efficiente approchée ; la courbe de la frontière est en escalier ; la frontière n'apparait pas correctement ; que veut dire approchée dans la légende ; l'optimiseur n'a trouvé aucun point de la frontière ; frontière bizarre avec un titre récent | mots: frontière approchée, enveloppe, solution de secours, nuage, approximation, convergence, historique court | aller: Analyse du portefeuille/Optimisation -->

Quand la légende du graphique indique « Frontière efficiente (approchée) », c'est que l'optimiseur n'a pas réussi à calculer au moins deux points de la frontière exacte. Le logiciel utilise alors une **solution de secours** tirée du nuage des 4 000 portefeuilles aléatoires.

### Comment est construite la frontière approchée

1. les portefeuilles aléatoires sont triés par volatilité croissante ;
2. on ne garde que ceux dont le rendement atteint le meilleur rendement déjà rencontré à une volatilité plus faible (le « maximum cumulé »).

```
garder un portefeuille si : rendement ≥ meilleur rendement des portefeuilles moins risqués
```

On obtient l'**enveloppe supérieure** du nuage : pour chaque niveau de risque, le meilleur rendement déjà atteint par un portefeuille tiré au hasard.

### Exemple

Portefeuilles triés par volatilité : (8 % ; 4 %), (9 % ; 5 %), (10 % ; 4,5 %), (11 % ; 6 %). Le troisième est écarté (4,5 % < 5 %) ; l'enveloppe passe par les trois autres.

### Causes fréquentes

- un titre avec un historique trop court ;
- des contraintes très serrées (plafond bas avec peu de titres) ;
- un échec numérique de l'optimiseur sur certains rendements cibles.

### Ce que cela change

La frontière approchée est **légèrement en dessous** de la vraie frontière (un tirage au hasard n'atteint jamais exactement l'optimum) et peut avoir un aspect en escalier. Elle reste utile pour situer votre portefeuille. Elle ignore le plafond par titre, puisque les portefeuilles aléatoires ne le respectent pas. Les cartes « Variance minimale » et « Sharpe maximal » restent, elles, calculées exactement.

## Qu'est-ce qu'une projection de Monte-Carlo ?
<!-- fiche: optim-monte-carlo-principe | questions: c'est quoi monte carlo ; comment marche l'onglet projection ; combien vaudra mon portefeuille dans 10 ans ; comment le logiciel simule le futur ; pourquoi 5000 scénarios ; les résultats changent ils à chaque fois ; simulation de la valeur future du portefeuille ; à quoi sert la projection | mots: Monte-Carlo, simulation, projection, scénarios, mouvement brownien géométrique, futur, horizon, 5000 simulations | aller: Analyse du portefeuille/Projection | chiffres: valeur_actuelle, twr_annualise, volatilite -->

On ne peut pas prédire **le** futur, mais on peut simuler des **milliers de futurs possibles**, tous cohérents avec le rendement et le risque du portefeuille, puis étudier la distribution des résultats. C'est la méthode de Monte-Carlo, utilisée dans l'onglet **Projection**.

### Ce que fait le logiciel

1. Il part de la **valeur actuelle** de votre portefeuille.
2. Il simule **5 000 scénarios**, **mois par mois**, jusqu'à l'horizon choisi.
3. Chaque mois, la valeur est multipliée par une croissance tirée au hasard, puis le versement mensuel est ajouté :

```
Valeur(mois + 1) = Valeur(mois) × exp(log-rendement du mois) + versement mensuel
```

4. À chaque date, il calcule les percentiles 5, 25, 50, 75 et 95 des 5 000 valeurs.

Le pas de temps est le **mois** (et non le jour) : c'est suffisant pour une projection à plusieurs années et environ 20 fois plus rapide.

### Ce qui est affiché

- quatre cartes : [[Scénario défavorable]] (5e percentile), [[Scénario médian]], [[Scénario favorable]] (95e percentile) et [[Probabilité de perte]], plus [[Objectif atteint]] si un objectif est saisi ;
- l'éventail ou le nuage de points des trajectoires ;
- la distribution de la valeur finale et ses phrases de lecture.

### Résultats reproductibles

Le hasard est fixé par une « graine » : avec les mêmes hypothèses, vous obtenez exactement les mêmes chiffres à chaque affichage. Changer un réglage relance une nouvelle simulation.

### Exemple

100 000 €, rendement 7 %, volatilité 15 %, 10 ans, sans versement, loi normale : médiane **178 727 €**, scénario défavorable **81 876 €**, scénario favorable **389 613 €**, probabilité de perte **10,4 %**. La théorie donne une médiane de 179 948 € : l'écart vient du nombre fini de scénarios.

## Les hypothèses réglables de la projection
<!-- fiche: optim-hypotheses-projection | questions: comment changer l'horizon de la projection ; ajouter un versement mensuel dans la simulation ; comment fixer un objectif ; quel rendement mettre dans la projection ; pourquoi le curseur de volatilité est grisé ; d'où vient le rendement proposé par défaut ; le rendement historique affiché est de 35 % mais le curseur s'arrête à 20 ; simuler un plan d'épargne mensuel | mots: hypothèses, horizon, versement mensuel, objectif, rendement supposé, volatilité supposée, épargne programmée, paramètres de simulation | aller: Analyse du portefeuille/Projection | chiffres: valeur_actuelle, volatilite -->

Le cadre « Hypothèses de la simulation », en haut de l'onglet Projection, rappelle dans son sous-titre le **rendement et la volatilité historiques** du portefeuille, puis propose six réglages.

| Réglage | Plage | Valeur de départ |
|---|---|---|
| [[Horizon (années)]] | 1 à 30 ans | 10 ans |
| [[Versement mensuel (€)]] | 0 à 1 000 000 €, pas de 100 € | 0 € |
| [[Objectif (€, facultatif)]] | 0 à 100 000 000 €, pas de 5 000 € | 0 (pas d'objectif) |
| [[Méthode]] | [[Loi normale]] ou [[Historique (bootstrap)]] | Loi normale |
| [[Rendement annuel supposé (%)]] | −5 % à 20 %, pas de 0,5 | rendement historique |
| [[Volatilité annuelle (%)]] | 1 % à 50 %, pas de 0,5 | volatilité historique |

### D'où viennent les valeurs historiques

Elles sont calculées sur les rendements quotidiens du portefeuille (ceux de la performance TWR) :

```
rendement historique  = moyenne des rendements quotidiens × 252
volatilité historique = écart-type des rendements quotidiens × √252
```

Les curseurs démarrent sur ces valeurs, **arrondies au 0,5 point le plus proche** et **ramenées dans la plage** du curseur. Exemple : un rendement historique de 12,3 % donne un curseur à 12,5 % ; un rendement historique de 35 % est ramené à 20 %.

### Conseils

- Un rendement historique obtenu sur une courte période favorable est trop optimiste : **réduisez-le** pour une projection prudente.
- Le **versement mensuel** est ajouté à la fin de chaque mois. Le montant investi total vaut `valeur actuelle + versement × nombre de mois`.
- L'**objectif** ajoute une carte de probabilité et une ligne horizontale pointillée sur l'éventail.

### Pourquoi la volatilité est grisée

Avec la méthode historique, le curseur de volatilité est désactivé : la dispersion vient des vrais jours de bourse du portefeuille, tirés au hasard. Le curseur de rendement reste actif (voir la fiche sur les deux méthodes).

Les montants sont **nominaux** : ni l'inflation, ni les impôts, ni les frais ne sont déduits.

## Méthode normale ou méthode historique (bootstrap) ?
<!-- fiche: optim-methode-normale-historique | questions: quelle différence entre loi normale et historique dans la projection ; c'est quoi le bootstrap ; quelle méthode choisir pour la simulation ; pourquoi la méthode historique donne un scénario défavorable plus bas ; mouvement brownien géométrique expliqué ; pourquoi moins sigma carré sur 2 ; la loi normale sous-estime les krachs ; queues épaisses dans la simulation | mots: loi normale, bootstrap, historique, mouvement brownien géométrique, Black-Scholes, lemme d'Itô, queues épaisses, rééchantillonnage, krach | aller: Analyse du portefeuille/Projection | chiffres: volatilite, asymetrie, kurtosis -->

Le bouton [[Méthode]] propose deux façons de tirer au hasard le rendement de chaque mois.

### 1. Loi normale (mouvement brownien géométrique)

C'est le modèle de Black-Scholes. Sur un mois (dt = 1/12 an), le log-rendement suit :

```
log-rendement mensuel ~ Normale( moyenne = (μ − σ²/2) × 1/12 , écart-type = σ × √(1/12) )
```

Avec μ = 7 % et σ = 15 % : moyenne mensuelle = (0,07 − 0,01125) / 12 = **0,490 %**, écart-type mensuel = 0,15 × 0,2887 = **4,33 %**.

**Pourquoi « − σ²/2 » ?** Le rendement μ est une moyenne arithmétique, mais la croissance composée est plus faible : +50 % puis −50 % donnent une moyenne de 0 %, mais on finit à 0,75, soit −25 %. Le terme −σ²/2 corrige cet effet (lemme d'Itô).

### 2. Historique (bootstrap)

Chaque mois est construit en tirant au hasard, **avec remise**, **21 vrais rendements quotidiens** du portefeuille, et en additionnant leurs logarithmes. On garde ainsi la forme réelle des rendements : **queues épaisses** (krachs plus fréquents que dans la loi normale) et asymétrie.

Le rendement est ensuite **recentré** sur le curseur [[Rendement annuel supposé (%)]] :

```
σ        = écart-type des rendements quotidiens × √252
cible    = (μ − σ²/2) / 252                 (log-rendement quotidien moyen visé)
log-rendements recentrés = log-rendements − leur moyenne + cible
```

Exemple : μ = 7 %, σ = 15 % : cible = 0,05875 / 252 = 0,0233 % par jour, soit 0,490 % sur 21 jours, comme pour la loi normale. Seule la forme de la distribution change.

Cette méthode exige au moins 20 rendements quotidiens dans l'historique.

### Laquelle choisir ?

- **Loi normale** : simple, standard, réglable (vous choisissez la volatilité). Elle sous-estime les krachs.
- **Historique** : plus réaliste sur les extrêmes, mais limitée aux événements de votre période d'analyse. Si votre historique ne contient aucun krach, elle n'en inventera pas.

Comparez les deux : un scénario défavorable nettement plus bas en méthode historique signale des queues épaisses dans votre portefeuille (voir aussi l'onglet Risque).

## Lire l'éventail et le nuage de points de la projection
<!-- fiche: optim-eventail-nuage | questions: comment lire le graphique de la projection ; que représentent les zones bleues ; c'est quoi le nuage de points de la simulation ; pourquoi les points sont de couleurs différentes ; la ligne orange en pointillés c'est quoi ; la courbe médiane est elle un scénario ; afficher les deux graphiques ; pourquoi l'éventail s'élargit avec le temps | mots: éventail, fan chart, nuage de points, percentiles, tranches de probabilité, médiane, argent investi, trajectoires | aller: Analyse du portefeuille/Projection | chiffres: valeur_actuelle -->

Le sélecteur [[Affichage]] propose trois vues : [[Éventail]] (par défaut), [[Nuage de points]] ou [[Les deux]].

### L'éventail

| Élément | Signification |
|---|---|
| Zone bleu clair | 90 % des scénarios (entre le 5e et le 95e percentile) |
| Zone bleu plus foncé | 50 % des scénarios (entre le 25e et le 75e percentile) |
| Courbe bleue | scénario médian (50e percentile) |
| Tirets orange | argent investi (valeur de départ + versements cumulés) |
| Ligne pointillée « Objectif » | votre objectif, s'il est saisi |

Survolez la courbe pour lire, à chaque date, la médiane et la fourchette à 90 %.

**Attention** : les percentiles sont calculés **date par date**. La courbe médiane n'est pas un scénario réel : aucun scénario ne reste toujours au milieu.

L'éventail **s'élargit avec l'horizon** : c'est l'incertitude qui s'accumule. En loi normale, l'écart-type des log-rendements cumulés grandit comme σ × √années.

### Le nuage de points

Chaque point est **un scénario à une date donnée**. Le logiciel affiche les **400 premiers scénarios**, tous les 6 mois (tous les ans si l'horizon dépasse 15 ans), plus la date finale. Les points d'une même date sont légèrement décalés horizontalement pour rester lisibles.

Chaque point est coloré selon sa tranche **à cette date** :

| Couleur | Tranche |
|---|---|
| Rouge foncé | 5 % les plus défavorables (sous le 5e percentile) |
| Rouge clair | Défavorable (5 à 25 %) |
| Gris | Central (25 à 75 %) |
| Bleu clair | Favorable (75 à 95 %) |
| Bleu foncé | 5 % les plus favorables (au-dessus du 95e percentile) |

Des repères complètent le nuage : médiane, seuils des 5 % et des 95 % (pointillés) et argent investi. Survolez un point pour voir son numéro de scénario et sa date : un même scénario peut changer de tranche au fil du temps.

Le nuage rend visible la **dispersion réelle** des résultats, que l'éventail résume.

## La distribution de la valeur finale : pourquoi n'est-elle pas symétrique ?
<!-- fiche: optim-distribution-finale | questions: pourquoi la moyenne est plus haute que la médiane ; comment lire l'histogramme de la valeur finale ; c'est quoi une loi log normale ; à quoi sert l'échelle logarithmique ; pourquoi la courbe est penchée à gauche avec une longue queue à droite ; quel chiffre retenir moyenne ou médiane ; que veut dire P5 et P95 ; les scénarios extrêmes n'apparaissent pas | mots: distribution finale, log-normale, histogramme, moyenne, médiane, échelle logarithmique, asymétrie, P5, P95, percentile | aller: Analyse du portefeuille/Projection | chiffres: valeur_actuelle, volatilite -->

Le graphique « Distribution de la valeur finale » est un histogramme : la valeur du portefeuille à l'horizon, pour chacun des 5 000 scénarios. Il porte trois repères verticaux : **Montant investi** (tirets orange), **Médiane** (trait plein) et **Moyenne** (pointillés), ainsi qu'une zone bleutée « 90 % des scénarios (P5 à P95) ».

### Pourquoi la distribution est log-normale

Les rendements se **composent** : la valeur finale est un **produit** de croissances mensuelles. C'est donc son **logarithme** (une somme) qui suit à peu près une loi normale. La valeur elle-même suit une loi **log-normale** : bornée à gauche (on ne peut pas perdre plus de 100 %), avec une longue queue à droite (les gains composés n'ont pas de plafond).

Sans versement et en loi normale :

```
médiane = valeur initiale × exp((μ − σ²/2) × T)
moyenne = valeur initiale × exp(μ × T)
moyenne / médiane = exp(σ² × T / 2)
```

### Exemple

100 000 €, μ = 7 %, σ = 15 %, T = 10 ans :

- médiane théorique = 100 000 × exp(0,5875) ≈ **179 948 €** (simulée : 178 727 €) ;
- moyenne théorique = 100 000 × exp(0,70) ≈ **201 375 €** (simulée : 199 757 €) ;
- rapport = exp(0,1125) ≈ 1,12 : la moyenne dépasse la médiane d'environ 12 %.

### Moyenne ou médiane ?

Quelques scénarios très favorables tirent la **moyenne** vers le haut. La **médiane** (une chance sur deux de faire mieux) est le repère le plus représentatif. Le logiciel l'écrit dans les phrases de lecture dès que la moyenne dépasse la médiane de plus de 2 %.

### P5 et P95

- **P5** : 5 % des scénarios finissent en dessous (« 1 chance sur 20 de faire pire »). Dans l'exemple : 81 876 €.
- **P95** : 5 % des scénarios finissent au-dessus. Dans l'exemple : 389 613 €.

La première phrase de lecture résume : « Dans 90 % des scénarios, la valeur dans 10 ans se situe entre … et … ».

### L'échelle logarithmique

L'interrupteur [[Échelle logarithmique]] trace l'histogramme du logarithme de la valeur. La cloche redevient à peu près **symétrique**, centrée sur la médiane. Les graduations restent en euros (par exemple 50 k€, 100 k€, 200 k€, 500 k€).

### Ce qui n'est pas affiché

Pour la lisibilité, l'axe s'arrête aux percentiles 0,5 et 99,5 (élargi si besoin pour montrer le montant investi) : les 1 % de scénarios les plus extrêmes ne sont pas dessinés, mais ils comptent dans tous les chiffres. Avec des versements mensuels, la loi n'est plus exactement log-normale, mais la forme reste la même.

## Probabilité de perte, de doubler ou d'atteindre un objectif
<!-- fiche: optim-probabilites | questions: comment est calculée la probabilité de perte ; quelle chance j'ai d'atteindre mon objectif ; probabilité de doubler mon capital ; la probabilité de perte tient elle compte de l'inflation ; scénario défavorable ça veut dire quoi ; 1 chance sur 20 de faire pire ; pourquoi la probabilité de perte augmente avec les versements | mots: probabilité de perte, objectif, doubler, scénario défavorable, scénario favorable, chance de succès, risque de perte, percentile | aller: Analyse du portefeuille/Projection | chiffres: valeur_actuelle, montant_investi -->

Les cartes et les phrases de l'onglet Projection comptent simplement la **part des 5 000 scénarios** qui remplissent une condition, à l'horizon choisi.

### Les formules

```
total investi             = valeur actuelle + versement mensuel × nombre de mois
probabilité de perte      = part des scénarios dont la valeur finale < total investi
probabilité de doubler    = part des scénarios dont la valeur finale ≥ 2 × total investi
probabilité de l'objectif = part des scénarios dont la valeur finale ≥ objectif
scénario défavorable      = 5e percentile des valeurs finales
scénario médian           = 50e percentile
scénario favorable        = 95e percentile
```

### Exemple vérifié

100 000 €, versement de 200 € par mois, 10 ans, μ = 7 %, σ = 15 %, loi normale, objectif 250 000 € :

- total investi = 100 000 + 200 × 120 = **124 000 €** ;
- probabilité de perte = **10,6 %** ;
- probabilité de doubler (finir au-dessus de 248 000 €) = **35,9 %** ;
- probabilité d'atteindre 250 000 € = **35,2 %** ;
- scénario défavorable 104 075 €, médian 211 406 €, favorable 439 552 €.

### Interprétation

- « Scénario défavorable » ne veut pas dire « pire cas » : 1 scénario sur 20 fait encore moins bien.
- La probabilité de perte compare la valeur finale à la **somme versée**, sans la rémunérer : finir à 124 500 € pour 124 000 € versés n'est pas une perte au sens du logiciel, mais c'est un mauvais placement.
- Elle diminue en général avec l'horizon, car la hausse moyenne s'accumule plus vite que la dispersion.

### Limites

Tous les montants sont **nominaux** : ni l'inflation, ni les impôts, ni les frais ne sont déduits. Une perte de pouvoir d'achat n'est donc pas comptée comme une perte. Ces probabilités dépendent entièrement du rendement et de la volatilité choisis.

## Une projection n'est pas une prévision
<!-- fiche: optim-pas-une-prevision | questions: la projection est elle fiable ; est ce que mon portefeuille vaudra vraiment ça dans 10 ans ; peut on se fier au scénario médian ; pourquoi la projection est trop optimiste ; garantie de résultat de la simulation ; limites de monte carlo ; la projection prend elle en compte l'inflation et les impôts | mots: prévision, fiabilité, limites, hypothèses, incertitude, garantie, inflation, avertissement | aller: Analyse du portefeuille/Projection | chiffres: twr_annualise, volatilite -->

Une projection de Monte-Carlo répond à la question : **« si les hypothèses se vérifient, quelle est la gamme des résultats possibles ? »**. Elle ne dit pas ce qui va se passer. Le logiciel le rappelle dans l'encadré « Comment lire cette projection ? » : la médiane n'est pas une prévision, c'est le milieu des possibles.

### Ce que la projection suppose

- un rendement et une volatilité **constants** sur tout l'horizon ;
- des mois **indépendants** les uns des autres (pas de cycles, pas de tendance) ;
- pour la loi normale, des rendements sans queues épaisses ;
- pour la méthode historique, un avenir qui ressemble aux jours de votre période d'analyse ;
- une composition du portefeuille qui ne change pas.

### Ce qu'elle ignore

- l'inflation, les impôts et les frais : les montants sont nominaux et bruts ;
- les changements de stratégie, retraits ou arbitrages ;
- les événements absents de l'historique ou du modèle.

### Pourquoi elle peut être trop optimiste

Le rendement proposé par défaut est le rendement **historique** du portefeuille. Sur une période courte et favorable, il peut être très élevé. Exemple : sur 10 ans avec 100 000 €, passer de 7 % à 4 % de rendement supposé (volatilité 15 %) ramène la médiane théorique de 179 948 € à 100 000 × exp((0,04 − 0,01125) × 10) ≈ **133 309 €**.

### Comment l'utiliser

- testez plusieurs rendements, dont un prudent ;
- comparez la loi normale et la méthode historique ;
- regardez surtout la **fourchette** P5 – P95 plutôt qu'un chiffre unique ;
- relancez l'analyse régulièrement, à mesure que l'historique s'allonge.
