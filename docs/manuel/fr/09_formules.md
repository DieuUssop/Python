# Toutes les formules
<!-- chapitre: formules | ordre: 9 -->

Ce chapitre donne, indicateur par indicateur, la formule exacte utilisée par le logiciel, telle qu'elle est écrite dans son code, avec un petit exemple chiffré, son interprétation et ses limites. Chaque fiche se lit seule. Les conventions communes (252 jours de bourse, base 365 jours, montants en euros) sont rappelées dans la première fiche.

## Les conventions de calcul communes à tous les indicateurs
<!-- fiche: formule-conventions | questions: pourquoi 252 jours ; c'est quoi la base 365 ; les achats sont comptés en début ou en fin de journée ; tous les calculs sont ils en euros ; quelles conventions utilise le logiciel ; pourquoi annualiser avec racine de 252 ; un achat le samedi est compté quand ; hypothèses de calcul du logiciel | mots: conventions, 252 jours, 365 jours, annualisation, fin de journée, euros, cours de clôture, hypothèses -->

Tous les indicateurs reposent sur les mêmes conventions, inscrites dans le code.

| Convention | Valeur retenue |
|---|---|
| Jours de bourse par an (volatilité, Sharpe, alpha, tracking error) | 252 |
| Jours par an pour annualiser un rendement (TWR, TRI) | 365 jours calendaires |
| Moment des opérations | en fin de journée, au cours du jour |
| Cours utilisé | cours de clôture, non ajusté des dividendes |
| Monnaie | tout est converti en euros |
| Taux sans risque | constant sur toute la période (2,50 % par défaut) |

### Deux annualisations différentes

- Une **moyenne** de rendements quotidiens est multipliée par 252.
- Un **écart-type** quotidien est multiplié par √252 ≈ 15,87 : si les jours sont indépendants, les variances s'additionnent, donc l'écart-type croît comme la racine du temps.
- Un **rendement total** est composé sur 365 jours : `(1 + R) ^ (365 / nombre de jours) − 1`.

### Les jours sans cotation

Une opération saisie un jour sans bourse (un samedi) est rattachée au jour de bourse suivant. Un jour férié sur une seule place, le dernier cours connu du titre est repris.

## Comment est calculé le rendement de chaque jour, sans l'effet des apports ?
<!-- fiche: formule-rendement-quotidien | questions: comment est calculé le rendement quotidien ; pourquoi mon achat ne compte pas comme un gain ; rendement journalier neutre aux apports ; formule du rendement d'un jour ; un apport fait monter la valeur mais pas la performance ; le premier jour le rendement est négatif pourquoi ; comment les flux sont retirés de la performance | mots: rendement quotidien, rendement journalier, flux, apports, retraits, neutralisation, premier jour, frais d'achat | aller: Analyse du portefeuille/Performance -->

Un achat de 1 000 € fait monter la valeur du portefeuille de 1 000 €, sans aucun gain. Le logiciel retire donc l'effet des flux.

### La formule

```
r(t) = (valeur(t) − flux(t)) / valeur(t−1) − 1
```

avec, pour chaque jour, `flux` = argent apporté (+) ou récupéré (−) :

- ACHAT : `+ (quantité × prix + frais)` ;
- VENTE : `− (quantité × prix − frais)` ;
- DIVIDENDE : `− (montant − frais)`.

Le premier jour (ou après avoir tout vendu), la veille vaut 0 : `r = valeur(t) / flux(t) − 1`. Ce rendement capte les frais d'achat et l'écart entre le prix payé et le cours de clôture. Les jours où rien n'est investi sont exclus.

### Exemple

- Veille : 10 000 €. Achat du jour : 1 000 €. Valeur le soir : 11 200 €. `r = (11 200 − 1 000) / 10 000 − 1 = +2,00 %`.
- Premier jour : 10 titres achetés 500 € avec 2,50 € de frais (flux 5 002,50 €), clôture à 505 € (valeur 5 050 €) : `r = 5 050 / 5 002,50 − 1 = +0,95 %`.

### Limite

L'opération est supposée faite au cours de clôture : le rendement du jour d'achat inclut l'écart entre votre prix et cette clôture.

Ces rendements servent au TWR, à la volatilité, au Sharpe, à la VaR et à la projection.

## Le TWR : rendement pondéré par le temps
<!-- fiche: formule-twr | questions: c'est quoi le twr ; comment est calculé le twr total ; time weighted return formule ; performance pondérée par le temps ; pourquoi mon twr est différent de mon gain en pourcentage ; twr ou rendement simple ; la performance des gérants de fonds | mots: TWR, time-weighted return, rendement pondéré par le temps, performance, GIPS, composition, base 100 | aller: Analyse du portefeuille/Performance | chiffres: twr_total, twr_annualise -->

Le TWR (*time-weighted return*) mesure la qualité des choix d'investissement, indépendamment du moment et du montant des apports. C'est la mesure des gérants de fonds (norme GIPS) : un gérant ne choisit pas quand ses clients déposent de l'argent.

### La formule

```
TWR = (1 + r1) × (1 + r2) × … × (1 + rn) − 1
```

où les `r` sont les rendements quotidiens neutralisés des apports (voir la fiche précédente). La courbe « base 100 » de l'onglet Performance est le même produit, cumulé jour après jour : `indice(t) = 100 × Π (1 + r)`.

### Exemple

+10 % un jour, puis −5 % le suivant : `1,10 × 0,95 − 1 = +4,5 %`, et non +5 %.

### Interprétation

Deux investisseurs qui détiennent les mêmes titres dans les mêmes proportions ont le même TWR, même si l'un a investi 1 000 € et l'autre 100 000 €, ou à des dates différentes. Le TWR se compare donc directement à un indice.

### Limite

Il ignore l'effet du calendrier de vos apports : pour mesurer ce que votre argent a réellement rapporté, voyez le TRI. Le TWR « par année civile » applique la même formule aux jours de chaque année.

## Le TWR annualisé
<!-- fiche: formule-twr-annualise | questions: comment est calculée la performance annualisée ; twr annualisé formule ; pourquoi base 365 jours ; rendement par an ; perf annualisée énorme sur 3 mois ; convertir une performance totale en annuelle ; 21 % en deux ans ça fait combien par an | mots: annualisation, TWR annualisé, performance annualisée, rendement annuel, base 365, composition | aller: Analyse du portefeuille/Performance | chiffres: twr_annualise, twr_total -->

C'est le chiffre « Perf. annualisée » des chiffres clés et la carte « TWR annualisé » de l'onglet Performance.

### La formule

```
TWR annualisé = (1 + TWR total) ^ (365 / nombre de jours) − 1
```

Le nombre de jours est l'écart en jours calendaires entre le premier et le dernier rendement quotidien de l'historique.

### Exemple

+21 % en 730 jours : `1,21 ^ (365 / 730) − 1 = +10 %` par an, et non 10,5 % : les gains se composent d'une année sur l'autre.

### Interprétation

C'est le rendement constant qui, chaque année, aurait mené au même résultat. Il permet de comparer des périodes de durées différentes.

### Limites

- Sur une période courte, il **extrapole** : +5 % en 91 jours donne environ +21,6 % par an, ce qui ne dit rien de l'année à venir. Méfiez-vous du TWR annualisé sur moins d'un an.
- Il est vide de sens si le premier et le dernier jour sont confondus (le logiciel affiche alors « n.d. »).

## Le TRI : rendement de l'argent investi
<!-- fiche: formule-tri | questions: c'est quoi le tri ; taux de rendement interne formule ; money weighted return ; différence entre tri et twr ; pourquoi mon tri est négatif alors que le twr est positif ; comment est calculé le tri annuel ; tri n.d. pourquoi ; rendement de mon argent | mots: TRI, taux de rendement interne, IRR, money-weighted return, rendement pondéré par les capitaux, actualisation, dichotomie, flux | aller: Analyse du portefeuille/Performance | chiffres: tri_annuel, twr_annualise -->

Le TRI est le rendement annuel vu par l'investisseur : il tient compte du montant et de la date de chaque apport.

### La formule

C'est le taux annuel `i` qui annule la valeur actualisée de tous les flux :

```
Σ CF_k / (1 + i) ^ (jours_k / 365) = 0
```

- achat : argent qui sort de votre poche, `CF < 0` ;
- vente, dividende : argent qui rentre, `CF > 0` ;
- le dernier jour, on fait comme si tout était vendu : `+ valeur finale` ;
- `jours_k` : nombre de jours depuis le premier flux.

Il n'existe pas de formule directe : le logiciel cherche `i` par dichotomie (200 itérations) entre −99 % et +1 000 % par an. Sans solution dans cet intervalle, il affiche « n.d. ».

### Exemple : TWR et TRI s'opposent

10 000 € investis, +20 % la première année (12 000 €). Vous ajoutez alors 50 000 €, puis le portefeuille perd 10 % (55 800 €).

- TWR : `1,20 × 0,90 − 1 = +8 %` sur deux ans, soit +3,9 % par an.
- TRI : −6,05 % par an, car la baisse a frappé une somme cinq fois plus grosse que la hausse.

### Interprétation

Un TRI supérieur au TWR signifie que vos apports sont bien tombés ; inférieur, qu'ils sont arrivés avant une baisse.

## La volatilité annualisée
<!-- fiche: formule-volatilite | questions: comment est calculée la volatilité ; pourquoi racine de 252 ; volatilité formule écart type ; ma volatilité est de 15 % ça veut dire quoi ; volatilite du portefeuille annualisée ; mesure du risque du portefeuille ; c'est quoi l'écart-type des rendements | mots: volatilité, écart-type, risque, annualisation, racine de 252, dispersion, sigma | aller: Analyse du portefeuille/Risque | chiffres: volatilite -->

### La formule

```
Volatilité annuelle = écart-type des rendements quotidiens × √252
```

L'écart-type est l'écart-type d'échantillon (division par n − 1), calculé sur les rendements quotidiens neutralisés des apports.

### Pourquoi √252 ?

Si les rendements quotidiens sont indépendants, leurs variances s'additionnent : variance annuelle = 252 × variance quotidienne, donc écart-type annuel = √252 × écart-type quotidien.

### Exemple

Un écart-type quotidien de 1 % donne `1 % × √252 = 15,87 %` par an.

### Interprétation

Avec une volatilité de 15 %, le rendement d'une année s'écarte « typiquement » de 15 points de sa moyenne. La carte affiche aussi la volatilité de l'indice de référence sur la même période.

### Limites

- La volatilité compte les hausses comme les baisses : le ratio de Sortino corrige ce point.
- La règle √252 suppose des jours indépendants ; elle sous-estime le risque quand les baisses s'enchaînent.
- Elle ne décrit pas les pertes extrêmes : voyez la VaR, la CVaR et le max drawdown.

## Le max drawdown (pire baisse)
<!-- fiche: formule-max-drawdown | questions: c'est quoi le max drawdown ; comment est calculée la pire baisse ; drawdown formule ; perte maximale depuis un plus haut ; pourquoi mon drawdown ne compte pas mes retraits ; date du creux et date de récupération ; plus haut non retrouvé ça veut dire quoi | mots: max drawdown, drawdown, perte maximale, plus haut, creux, récupération, base 100 | aller: Analyse du portefeuille/Performance | chiffres: max_drawdown -->

### La formule

```
drawdown(t) = indice(t) / plus haut de l'indice jusqu'à t − 1      (toujours ≤ 0)
Max drawdown = le plus bas de ces valeurs
```

Le calcul porte sur l'**indice base 100** (le TWR cumulé), et non sur la valeur du portefeuille : sinon un simple retrait d'argent ressemblerait à une perte, et un apport masquerait une vraie baisse.

Le logiciel donne aussi la date du sommet, la date du creux et la date à laquelle le sommet a été retrouvé (« plus haut non retrouvé » si ce n'est pas encore le cas).

### Exemple

L'indice passe de 100 à 120, tombe à 90, remonte à 110. Max drawdown : `90 / 120 − 1 = −25 %`. Le sommet de 120 n'est pas retrouvé.

### Interprétation

C'est la pire perte qu'aurait subie un investisseur entré au plus mauvais moment et sorti au pire. Après une baisse de 25 %, il faut une hausse de 33 % pour revenir au sommet.

### Limites

Il dépend de la période observée : un portefeuille récent n'a peut-être pas encore connu de crise. Les stress tests complètent cette mesure.

## Le ratio de Sharpe
<!-- fiche: formule-sharpe | questions: c'est quoi le ratio de sharpe ; comment est calculé le sharpe ; formule du ratio de sharpe ; mon sharpe est négatif c'est grave ; quel est un bon ratio de sharpe ; le sharpe change quand je modifie le taux sans risque ; rendement par unité de risque | mots: ratio de Sharpe, Sharpe, rendement excédentaire, taux sans risque, rendement ajusté du risque, prime de risque | aller: Analyse du portefeuille/Risque | chiffres: sharpe, volatilite -->

Le ratio de Sharpe répond à la question : le risque pris a-t-il été bien payé ?

### La formule

```
taux sans risque quotidien rf_j = (1 + taux annuel) ^ (1/252) − 1
excédent(t) = r(t) − rf_j
Sharpe = moyenne(excédent) × 252 / (écart-type(excédent) × √252)
```

Le taux annuel est celui des [[Paramètres]] (2,50 % par défaut).

### Exemple

Rendement quotidien moyen 0,05 %, écart-type quotidien 1 %, taux sans risque 2,50 % (soit 0,0098 % par jour) :
`(0,05 % − 0,0098 %) × 252 / (1 % × √252) ≈ 10,13 % / 15,87 % ≈ 0,64`.

### Interprétation

Repères donnés par le code : négatif, mauvais (moins bien qu'un placement sans risque) ; 0,5, correct ; au-delà de 1, très bon. La carte affiche aussi le Sharpe de l'indice sur la même période.

### Limites

- La volatilité pénalise aussi les hausses (voir le Sortino).
- Le taux sans risque est constant sur toute la période, alors qu'il a varié : sur plusieurs années, le Sharpe est approximatif.
- Sur une courte période, il est très instable.

## Le ratio de Sortino
<!-- fiche: formule-sortino | questions: c'est quoi le ratio de sortino ; différence entre sharpe et sortino ; semi deviation formule ; sortino plus élevé que sharpe pourquoi ; ratio qui ne pénalise que les baisses ; comment est calculé le sortino ; downside deviation | mots: ratio de Sortino, semi-déviation, downside deviation, risque de baisse, Sharpe, taux sans risque | aller: Analyse du portefeuille/Risque | chiffres: sortino, sharpe -->

Critique du Sharpe : la volatilité compte les fortes hausses comme du risque. Le Sortino ne pénalise que les jours sous le taux sans risque.

### La formule

```
excédent(t) = r(t) − rf_j
baisses(t) = min(excédent(t), 0)
semi-déviation = √( moyenne des baisses² ) × √252
Sortino = moyenne(excédent) × 252 / semi-déviation
```

La moyenne des carrés porte sur **tous** les jours : les jours de hausse comptent pour 0. Le taux `rf_j` est le même que pour le Sharpe.

### Exemple

Excédent annuel moyen de 8 %, volatilité de 16 % et semi-déviation de 10 % : Sharpe `8 / 16 = 0,50`, Sortino `8 / 10 = 0,80`.

### Interprétation

Un Sortino nettement supérieur au Sharpe indique que la volatilité vient surtout des hausses. S'ils sont proches, hausses et baisses sont d'ampleur comparable.

### Limite

Comme le Sharpe, il dépend du taux sans risque retenu et de la période.

## Le bêta
<!-- fiche: formule-beta | questions: c'est quoi le bêta ; comment est calculé le beta du portefeuille ; beta supérieur à 1 ça veut dire quoi ; beta formule covariance variance ; mon portefeuille est-il plus risqué que le marché ; sensibilité à l'indice ; beta face à un indice obligataire | mots: bêta, beta, sensibilité, covariance, variance, MEDAF, CAPM, risque systématique, indice de référence | aller: Analyse du portefeuille/Performance | chiffres: beta -->

### La formule

```
Bêta = covariance(r_portefeuille, r_indice) / variance(r_indice)
```

- Rendements quotidiens du portefeuille et de l'indice de référence, sur les seuls jours communs.
- L'indice est aligné sur le calendrier du portefeuille (dernier cours connu reporté), puis `r = cours(t) / cours(t−1) − 1`.
- Covariance et variance d'échantillon (division par n − 1).

### Exemple

Covariance quotidienne de 0,00012 et variance quotidienne de l'indice de 0,00010 : `bêta = 1,2`. Quand l'indice fait +1 %, le portefeuille fait en moyenne +1,2 %.

### Interprétation

- 1 : le portefeuille bouge comme l'indice ;
- au-dessus de 1 : plus sensible, plus risqué que le marché ;
- en dessous de 1 : plus défensif.

Le bêta sert aussi aux stress tests hypothétiques (baisse des actions de X % ≈ bêta × X).

### Limites

Le bêta mesure une sensibilité à un marché d'actions : face à un indice obligataire ou monétaire, il a peu de sens, et l'onglet Performance le signale. Il dépend de l'indice choisi dans [[Indice de référence]].

## L'alpha de Jensen
<!-- fiche: formule-alpha | questions: c'est quoi l'alpha ; comment est calculé l'alpha de jensen ; alpha positif ça veut dire quoi ; formule alpha medaf ; mon alpha est négatif ; performance non expliquée par le marché ; alpha annuel | mots: alpha, alpha de Jensen, MEDAF, CAPM, surperformance, sélection de titres, rendement anormal | aller: Analyse du portefeuille/Performance | chiffres: alpha, beta -->

### La formule

```
alpha quotidien = moyenne(r_p − rf_j) − bêta × moyenne(r_i − rf_j)
Alpha annuel = alpha quotidien × 252
```

`r_p` et `r_i` sont les rendements quotidiens du portefeuille et de l'indice sur les jours communs, `rf_j` le taux sans risque quotidien `(1 + taux) ^ (1/252) − 1`.

### Exemple

Moyennes quotidiennes : portefeuille 0,06 %, indice 0,04 %, bêta 1,2, taux sans risque 2,50 % :
`[(0,06 % − 0,0098 %) − 1,2 × (0,04 % − 0,0098 %)] × 252 ≈ +3,5 %` par an.

### Interprétation

L'alpha est la performance qui ne s'explique **pas** par l'exposition au marché (modèle de marché, MEDAF). Positif : le choix des titres, ou un biais absent de l'indice, a créé de la valeur. Négatif : le risque de marché pris n'a pas été rémunéré.

### Limites

- Il dépend de l'indice choisi : un indice mal adapté (par exemple le CAC 40 hors dividendes) fausse l'alpha.
- Il dépend du taux sans risque, supposé constant.
- Sur une courte période, il est surtout du bruit statistique.

## La tracking error
<!-- fiche: formule-tracking-error | questions: c'est quoi la tracking error ; comment est calculée la tracking error ; erreur de suivi formule ; tracking error élevée ça veut dire quoi ; mon portefeuille colle-t-il à l'indice ; gestion passive ou active ; écart de suivi | mots: tracking error, erreur de suivi, écart de suivi, gestion passive, gestion active, volatilité de l'écart | aller: Analyse du portefeuille/Performance | chiffres: tracking_error -->

### La formule

```
écart(t) = r_portefeuille(t) − r_indice(t)
Tracking error = écart-type(écart) × √252
```

Calcul sur les jours communs au portefeuille et à l'indice.

### Exemple

Un écart quotidien d'écart-type 0,3 % donne `0,3 % × √252 ≈ 4,76 %` par an.

### Interprétation

C'est la volatilité de l'écart avec l'indice. Repères du code :

- moins de 2 % : le portefeuille « colle » à l'indice (gestion passive) ;
- plus de 5 % : gestion très différente de l'indice.

Une tracking error élevée n'est ni bonne ni mauvaise en soi : elle mesure l'audace de la gestion. Le ratio d'information dit si cette audace a payé.

### Limites

Elle dépend de l'indice choisi. Un portefeuille d'actions européennes comparé au MSCI World aura forcément une tracking error élevée.

## Le ratio d'information
<!-- fiche: formule-ratio-information | questions: c'est quoi le ratio d'information ; information ratio formule ; comment est calculé le ratio d'information ; quel est un bon ratio d'information ; ratio d'information négatif ; l'écart avec l'indice a-t-il été payé | mots: ratio d'information, information ratio, tracking error, surperformance, gestion active, écart moyen | aller: Analyse du portefeuille/Performance -->

### La formule

```
Ratio d'information = moyenne(r_portefeuille − r_indice) × 252 / tracking error
```

C'est l'écart de rendement moyen annualisé, divisé par la tracking error (voir la fiche précédente).

### Exemple

Écart quotidien moyen de 0,02 % (soit 5,04 % par an) et tracking error de 4,76 % : `5,04 / 4,76 ≈ 1,06`.

### Interprétation

C'est l'équivalent du Sharpe, mais relativement à l'indice : l'écart avec l'indice a-t-il été « payé » ? Le code retient comme repère qu'un ratio supérieur à 0,5 est considéré comme bon. Négatif : le portefeuille a fait moins bien que l'indice.

### Ne pas confondre

La carte « Écart avec » l'indice, en haut de l'onglet Performance, est l'écart des **TWR composés** sur la même période (`TWR portefeuille − TWR indice`), alors que le ratio d'information utilise la **moyenne arithmétique** des écarts quotidiens. Les deux peuvent légèrement différer.

### Limite

Comme la tracking error, il n'a de sens qu'avec un indice comparable au portefeuille.

## La VaR historique
<!-- fiche: formule-var-historique | questions: comment est calculée la var historique ; value at risk méthode historique ; que veut dire var 95 % 1 jour ; la var en euros c'est quoi ; perte d'un mauvais jour ; percentile des rendements ; var historique formule | mots: VaR, value at risk, VaR historique, quantile, percentile, perte maximale, niveau de confiance, 1 jour | aller: Analyse du portefeuille/Risque | chiffres: var_historique, valeur_actuelle -->

### La formule

```
VaR historique = − quantile(1 − niveau) des rendements quotidiens
VaR en euros = VaR historique × valeur actuelle du portefeuille
```

Le niveau se règle en haut de l'onglet Risque, avec [[Niveau de confiance de la VaR]] : 90, 95 (par défaut) ou 99 %. Le quantile est calculé par la bibliothèque pandas, avec interpolation linéaire entre deux observations. Le résultat est un nombre positif : une perte.

### Exemple

Sur 20 jours, les cinq pires rendements sont −3,1 %, −2,4 %, −1,8 %, −1,5 % et −1,2 %. Le quantile 5 % tombe entre le pire et le deuxième pire jour : `−3,1 % + 0,95 × 0,7 % ≈ −2,44 %`. VaR 95 % = 2,44 %. Sur 100 000 €, environ 2 440 €.

### Interprétation

« Dans 95 % des jours, la perte ne dépasse pas ce montant. » La VaR 95 % est donc dépassée environ un jour de bourse sur vingt. C'est la carte « VaR · 1 jour » de l'onglet Risque.

### Limites

- Aucune hypothèse de loi, mais le passé est supposé se répéter : une crise absente de l'historique est invisible.
- Elle ne dit rien de l'ampleur de la perte au-delà du seuil : c'est le rôle de la CVaR.
- Sur un historique court, elle repose sur très peu de jours.

## La VaR selon la loi normale
<!-- fiche: formule-var-normale | questions: var paramétrique formule ; var gaussienne ; var loi normale comment est elle calculée ; pourquoi 1,645 ; la var normale sous-estime les krachs ; var variance covariance ; différence var historique et var normale | mots: VaR paramétrique, VaR gaussienne, loi normale, 1,645, quantile, écart-type, moyenne, queues épaisses | aller: Analyse du portefeuille/Risque | chiffres: var_parametrique, var_historique -->

### La formule

```
VaR loi normale = − (moyenne + z × écart-type)
```

- `moyenne` et `écart-type` : ceux des rendements quotidiens ;
- `z` : quantile de la loi normale centrée réduite au seuil `1 − niveau` : −1,282 à 90 %, −1,645 à 95 %, −2,326 à 99 %.

### Exemple

Moyenne quotidienne 0,05 %, écart-type 1,2 %, niveau 95 % : `−(0,05 % − 1,645 × 1,2 %) ≈ 1,92 %`, soit environ 1 924 € sur 100 000 €.

### Interprétation

C'est la perte d'un mauvais jour si les rendements suivaient une loi normale de même moyenne et de même volatilité. Le tableau de l'onglet Risque l'affiche à côté de la VaR historique, de la VaR Cornish-Fisher et de la CVaR, en pourcentage et en euros.

### Limites

Les vrais rendements ont des « queues épaisses » : les grosses baisses sont plus fréquentes que ne le prévoit la loi normale. Elle **sous-estime** donc souvent les krachs, surtout à 99 %. Le test de Jarque-Bera indique si la loi normale est rejetée pour votre portefeuille ; dans ce cas, la lecture automatique conseille de prendre cette VaR avec prudence.

## La VaR Cornish-Fisher et son domaine de validité
<!-- fiche: formule-var-cornish-fisher | questions: c'est quoi la var cornish fisher ; formule de cornish fisher ; pourquoi cornish fisher affiche n.d. ; var corrigée de l'asymétrie et de la kurtosis ; la var cornish fisher est plus petite que la var normale pourquoi ; domaine de validité cornish fisher ; var priips | mots: Cornish-Fisher, VaR modifiée, asymétrie, kurtosis, quantile corrigé, PRIIPs, n.d., validité | aller: Analyse du portefeuille/Risque | chiffres: var_cornish_fisher, asymetrie, kurtosis -->

On garde la formule de la loi normale, mais le quantile `z` est corrigé avec l'asymétrie `S` et la kurtosis en excès `K` (développement de Cornish-Fisher).

### La formule

```
z_cf = z + (z² − 1)·S/6 + (z³ − 3z)·K/24 − (2z³ − 5z)·S²/36
VaR Cornish-Fisher = − (moyenne + z_cf × écart-type)
```

### Exemple

Moyenne 0,05 %, écart-type 1,2 %, `S = −0,5`, `K = 3` :

- à 95 % : `z_cf ≈ −1,722` au lieu de −1,645, VaR 2,02 % au lieu de 1,92 % ;
- à 99 % : `z_cf ≈ −3,301` au lieu de −2,326, VaR 3,91 % au lieu de 2,74 %.

### Interprétation

Une asymétrie négative rend toujours la VaR plus prudente. L'effet des queues épaisses dépend du niveau : à 99 %, la VaR augmente ; à 95 %, elle peut au contraire baisser un peu, car une distribution à queues épaisses a aussi un centre plus « pointu ». C'est la méthode retenue pour l'indicateur de risque réglementaire des PRIIPs.

### Domaine de validité

La correction n'a de sens que si elle conserve l'ordre des quantiles. Le logiciel vérifie que la dérivée `1 + z·S/3 + (3z² − 3)·K/24 − (6z² − 5)·S²/36` reste positive pour `z` de −4 à +4 (par pas de 0,1). Sinon, ou avec moins de 4 jours, la VaR est affichée « n.d. », avec la mention « Cornish-Fisher n.d. : asymétrie ou kurtosis trop fortes ». Exemple : sans asymétrie, `K` doit rester entre environ −0,5 et 8.

## La CVaR (Expected Shortfall)
<!-- fiche: formule-cvar | questions: c'est quoi la cvar ; expected shortfall formule ; différence entre var et cvar ; perte moyenne au-delà de la var ; comment est calculée la cvar ; pourquoi la cvar est plus grande que la var ; mesure bâle 3 | mots: CVaR, Expected Shortfall, ES, perte moyenne, queue de distribution, VaR conditionnelle, Bâle III | aller: Analyse du portefeuille/Risque | chiffres: cvar, var_historique -->

### La formule

```
CVaR = − moyenne des rendements quotidiens r tels que r ≤ − VaR historique
CVaR en euros = CVaR × valeur actuelle
```

### Exemple

Avec les 20 jours de la fiche « VaR historique » (VaR 95 % de 2,44 %), un seul jour est pire que −2,44 % : −3,1 %. CVaR = 3,1 %. Sur 1 000 jours, elle serait la moyenne des 50 pires journées environ.

### Interprétation

La VaR répond à « jusqu'où va un mauvais jour ? », la CVaR à « et quand ça va mal, ça va mal comment ? ». Elle est toujours au moins égale à la VaR historique. C'est la mesure privilégiée par les régulateurs bancaires (Bâle III). Carte « CVaR · Expected Shortfall » de l'onglet Risque.

### Limites

Elle repose sur peu de jours (5 % de l'historique à 95 %, 1 % à 99 %) : sur un historique court, elle est instable. Comme la VaR historique, elle ignore les crises absentes de la période observée.

## L'asymétrie (skewness)
<!-- fiche: formule-asymetrie | questions: c'est quoi l'asymétrie ; skewness formule ; asymétrie négative ça veut dire quoi ; coefficient d'asymétrie des rendements ; distribution asymétrique ; comment est calculée l'asymétrie | mots: asymétrie, skewness, moment d'ordre 3, distribution, queue gauche, fortes baisses | aller: Analyse du portefeuille/Risque | chiffres: asymetrie -->

### La formule

L'asymétrie est calculée par la bibliothèque pandas : coefficient d'échantillon corrigé du biais (coefficient de Fisher-Pearson ajusté).

```
d = r − moyenne(r) ;  m2 = moyenne(d²) ;  m3 = moyenne(d³)
S = [m3 / m2^(3/2)] × √(n(n − 1)) / (n − 2)
```

### Interprétation

- 0 pour une loi normale (symétrique) ;
- négative : les fortes baisses sont plus fréquentes ou plus violentes que les fortes hausses (cas courant des actions) ;
- positive : les fortes hausses l'emportent.

La lecture automatique de l'onglet Risque considère la distribution « à peu près symétrique » quand `|S|` est inférieur à 0,3.

### Exemple

Une série de petits gains réguliers ponctuée de quelques fortes chutes a une asymétrie négative, même si sa moyenne est positive.

### Limites

Un seul jour extrême peut changer fortement l'asymétrie : elle est instable sur un historique court. Il faut au moins 4 jours ; sinon, elle vaut 0 par convention.

L'asymétrie sert au test de Jarque-Bera et à la VaR Cornish-Fisher.

## La kurtosis en excès (queues épaisses)
<!-- fiche: formule-kurtosis | questions: c'est quoi la kurtosis ; kurtosis en excès formule ; queues épaisses ça veut dire quoi ; kurtosis positive ; aplatissement ; leptokurtique ; jours à plus de 3 écarts types | mots: kurtosis, kurtosis en excès, aplatissement, queues épaisses, fat tails, leptokurtique, moment d'ordre 4, jours extrêmes | aller: Analyse du portefeuille/Risque | chiffres: kurtosis -->

### La formule

Calculée par pandas, directement en **excès** (la loi normale vaut 0), corrigée du biais d'échantillon :

```
g2 = moyenne(d⁴) / moyenne(d²)² − 3
K = [(n + 1) × g2 + 6] × (n − 1) / [(n − 2)(n − 3)]
```

avec `d = r − moyenne(r)`.

### Interprétation

- 0 : autant de journées extrêmes que la loi normale ;
- positive : « queues épaisses », les journées extrêmes (dans les deux sens) sont plus fréquentes que prévu. La lecture automatique parle de queues nettement épaisses au-delà de 1.

### Les jours extrêmes

L'onglet Risque compte aussi la part des jours à plus de 3 écarts-types de la moyenne, contre 0,27 % selon la loi normale (`2 × (1 − Φ(3))`). Exemple : 1,2 % de jours extrêmes observés, c'est environ 4,4 fois plus que la loi normale.

### Limites

Comme l'asymétrie, elle est très sensible à quelques jours et instable sur un historique court (minimum 4 jours, sinon 0). Elle sert au test de Jarque-Bera et à la VaR Cornish-Fisher.

## Le test de Jarque-Bera
<!-- fiche: formule-jarque-bera | questions: c'est quoi le test de jarque bera ; normalité rejetée ça veut dire quoi ; p value jarque bera ; mes rendements suivent ils une loi normale ; formule jarque bera ; pourquoi p inférieur à 0,001 ; test de normalité des rendements | mots: Jarque-Bera, test de normalité, p-value, khi-deux, loi normale, asymétrie, kurtosis, hypothèse | aller: Analyse du portefeuille/Risque | chiffres: asymetrie, kurtosis -->

### La formule

```
JB = n / 6 × (S² + K² / 4)
p-value = exp(−JB / 2)
```

`n` est le nombre de jours, `S` l'asymétrie, `K` la kurtosis en excès. Sous l'hypothèse de normalité, JB suit une loi du khi-deux à 2 degrés de liberté, dont la probabilité de dépassement vaut exactement `exp(−JB/2)`.

### Exemple

1 000 jours, `S = −0,4`, `K = 2` : `JB = 1 000 / 6 × (0,16 + 1) ≈ 193,3`, p-value ≈ 10⁻⁴², affichée « p = < 0,001 ».

### Interprétation

- p-value inférieure à 5 % : pastille « Normalité rejetée ». Les VaR calculées avec la loi normale sont alors à prendre avec prudence.
- Sinon : « Normalité non rejetée ». Ce n'est pas une preuve de normalité, seulement l'absence de preuve contraire.

Sur plusieurs années de rendements quotidiens d'actions, la normalité est presque toujours rejetée.

### Limites

Le test est asymptotique (fiable pour un grand nombre de jours). Sur un historique très long, le moindre écart suffit à rejeter la normalité, même s'il est sans conséquence pratique.

## La corrélation entre les titres
<!-- fiche: formule-correlation | questions: comment est calculée la corrélation ; corrélation entre deux titres formule ; corrélation moyenne pondérée ; blocs de titres corrélés seuil 0,7 ; pourquoi la corrélation monte en crise ; matrice de corrélation ; corrélation de 0,8 c'est beaucoup | mots: corrélation, coefficient de Pearson, matrice de corrélation, covariance, diversification, blocs, corrélation en crise | aller: Analyse du portefeuille/Expositions -->

### La formule

Coefficient de Pearson des rendements quotidiens `r = cours(t) / cours(t−1) − 1` de deux titres, sur leurs jours communs :

```
ρ(A, B) = covariance(r_A, r_B) / (écart-type(r_A) × écart-type(r_B))
```

### Les mesures dérivées (onglet Expositions)

- **Corrélation moyenne pondérée** : `Σ wᵢwⱼρᵢⱼ / Σ wᵢwⱼ`, sur les paires `i ≠ j`, avec `w` le poids de chaque ligne.
- **Blocs indépendants** : classification hiérarchique (distance `1 − ρ`, lien moyen) ; des titres corrélés à plus de 0,7 forment un même bloc, donc un seul « pari ».
- **Les jours de forte baisse** : corrélation moyenne pondérée calculée sur les 10 % pires jours du portefeuille (au moins 30 jours).
- **Qualificatifs** : très forte à partir de 0,8, forte à partir de 0,6, modérée à partir de 0,3, faible en dessous.

### Exemple

Covariance annuelle 0,018, volatilités 20 % et 30 % : `ρ = 0,018 / (0,20 × 0,30) = 0,30`, corrélation modérée.

### Limites

La corrélation ne mesure qu'un lien linéaire et varie dans le temps : elle monte souvent pendant les crises, quand la diversification serait la plus utile. Les corrélations passées ne sont pas garanties à l'avenir.

## Le ratio de diversification
<!-- fiche: formule-ratio-diversification | questions: c'est quoi le ratio de diversification ; comment est calculé le ratio de diversification ; mon ratio de diversification vaut 1 ; mon portefeuille est-il vraiment diversifié ; nombre effectif de paris ; diversification réelle formule | mots: ratio de diversification, diversification, volatilité pondérée, nombre effectif de paris, corrélation, Choueifaty | aller: Analyse du portefeuille/Expositions -->

### La formule

```
Ratio de diversification = Σ wᵢ × σᵢ / σ_p
σ_p = √(wᵀ Σ w)
```

`wᵢ` est le poids de chaque ligne, `σᵢ` sa volatilité, `Σ` la matrice de covariance des rendements quotidiens, `σ_p` la volatilité du portefeuille.

### Exemple

Deux lignes à 50 %, de volatilités 20 % et 30 %, corrélées à 0,3 : `σ_p ≈ 20,37 %`, d'où un ratio de `(0,5 × 20 % + 0,5 × 30 %) / 20,37 % ≈ 1,23`.

### Interprétation

- 1 : aucune diversification, les lignes évoluent comme un seul actif ;
- plus il est élevé, plus les lignes se compensent.

Le ratio est le même que l'on utilise des covariances quotidiennes ou annualisées.

### Le nombre effectif de paris (Budget de risque)

```
Nombre effectif de paris = 1 / Σ (part du risque de chaque ligne)²
```

Dans l'exemple, les parts du risque sont 34,9 % et 65,1 % : `1 / (0,349² + 0,651²) ≈ 1,83` pari, pour 2 lignes.

### Limites

Il repose sur des volatilités et corrélations passées, qui changent, surtout en crise.

## Le poids d'une ligne et le nombre effectif de lignes
<!-- fiche: formule-poids | questions: comment est calculé le poids d'une ligne ; poids en pourcentage du portefeuille ; nombre effectif de lignes ; indice de herfindahl ; règle 5 10 40 ; concentration du portefeuille formule ; équivalent à combien de lignes de même poids | mots: poids, pondération, allocation, concentration, Herfindahl, nombre effectif, 5/10/40, UCITS | aller: Analyse du portefeuille/Positions | chiffres: nb_titres, valeur_actuelle -->

### Les formules

```
valeur d'une ligne = quantité × dernier cours (en euros)
poids = valeur de la ligne / valeur totale des lignes détenues
nombre effectif de lignes = 1 / Σ poids²
```

Le nombre effectif est l'inverse de l'indice de Herfindahl.

### Exemple

Quatre lignes pesant 40 %, 30 %, 20 % et 10 % : `1 / (0,16 + 0,09 + 0,04 + 0,01) ≈ 3,3`. Le portefeuille équivaut à environ 3 lignes de même poids.

### Autres mesures de concentration (onglet Expositions)

- poids des 5 et des 10 premières lignes ;
- **règle 5/10/40** des fonds UCITS : une ligne au plus 10 %, et les lignes de plus de 5 % au plus 40 % au total. Elle porte sur les actions détenues en direct : un ETF diversifié n'est pas une concentration.

### Interprétation

Les seuils d'alerte sur la plus grosse action dépendent du profil choisi dans [[Seuils adaptés au profil]] : 5 et 10 % pour Prudent, 7 et 10 % pour Équilibré, 10 et 15 % pour Dynamique (premier seuil : attention, second : alerte).

### Limite

Le poids ne dit rien du risque : une ligne de 10 % très volatile peut apporter 30 % du risque (voir les contributions au risque).

## Le PRU (prix de revient unitaire)
<!-- fiche: formule-pru | questions: comment est calculé le pru ; prix de revient unitaire formule ; les frais sont ils inclus dans le pru ; mon pru ne change pas après une vente ; pru moyen pondéré ; pourquoi mon pru est différent de celui de ma banque ; pru après avoir tout vendu | mots: PRU, prix de revient unitaire, prix moyen, coût moyen pondéré, frais d'achat, montant investi | aller: Analyse du portefeuille/Positions | chiffres: montant_investi -->

Le logiciel rejoue toutes les opérations dans l'ordre des dates, selon la méthode du PRU utilisée en France.

### Les règles

```
ACHAT : nouveau PRU = (quantité détenue × PRU + q × prix + frais) / (quantité détenue + q)
VENTE : le PRU ne change pas
Tout vendu : le PRU repart de 0
Montant investi = quantité détenue × PRU
```

Les frais d'achat sont inclus dans le PRU : ils augmentent le coût de revient. Les prix sont convertis en euros au taux du jour de l'opération.

### Exemple

1. Achat de 10 titres à 100 € + 5 € de frais : PRU `(1 000 + 5) / 10 = 100,50 €`.
2. Achat de 10 titres à 120 € + 5 € : PRU `(10 × 100,50 + 1 205) / 20 = 110,50 €`.
3. Vente de 5 titres : le PRU reste 110,50 € ; il reste 15 titres, soit 1 657,50 € investis.

### Pourquoi un écart avec votre banque ?

- certaines banques excluent les frais du PRU ;
- un titre étranger est converti au taux de change de Yahoo Finance, pas à celui de votre banque ;
- une opération manquante (un ancien achat, une division d'actions) change le PRU.

## Plus-values latentes, réalisées et gain total
<!-- fiche: formule-plus-values | questions: comment est calculée la plus-value ; plus value latente formule ; plus-value réalisée avec les frais ; c'est quoi le gain total ; gain sur capital investi en pourcentage ; les dividendes sont ils dans le gain ; différence latente et réalisée | mots: plus-value latente, plus-value réalisée, moins-value, gain total, dividendes, frais, performance en euros | aller: Analyse du portefeuille/Vue d'ensemble | chiffres: gain_total, dividendes, frais_totaux, montant_investi -->

### Les formules

```
Plus-value latente = quantité × (cours − PRU) = valeur − montant investi
Plus-value latente en % = plus-value latente / montant investi
Plus-value réalisée (à chaque vente) = q × (prix de vente − PRU) − frais de vente
Dividendes = Σ (montant reçu − frais)
Gain total = plus-values latentes + plus-values réalisées + dividendes
```

Les frais sont déjà déduits : dans le PRU pour les achats, dans la plus-value réalisée pour les ventes. « Latente » veut dire non encaissée : ce que rapporterait une vente totale aujourd'hui, hors frais de vente et hors impôts.

### Exemple (suite de la fiche sur le PRU)

- vente de 5 titres à 130 € avec 4 € de frais : `5 × (130 − 110,50) − 4 = 93,50 €` réalisés ;
- 15 titres restants, cours 125 € : `15 × (125 − 110,50) = 217,50 €` latents ;
- un dividende de 30 € net de frais ;
- gain total : `217,50 + 93,50 + 30 = 341 €`.

### Le pourcentage « sur le capital investi »

La carte « Gain total » affiche `gain total / montant investi`, où le montant investi est le coût des **seules lignes encore détenues** (ici 341 / 1 657,50 ≈ 20,6 %). Ce n'est ni un TWR ni un TRI.

### Contrôle croisé

L'historique jour par jour calcule aussi `gain = valeur − apports nets` ; le dernier jour, il doit retomber exactement sur le gain total, ce que vérifient les tests du projet.

## La frontière efficiente de Markowitz
<!-- fiche: formule-frontiere-efficiente | questions: comment est calculée la frontière efficiente ; portefeuille de variance minimale ; portefeuille de sharpe maximal formule ; optimisation de markowitz comment ça marche ; rendement espéré et matrice de covariance ; poids maximal par titre 30 % pourquoi ; pourquoi la frontière est approchée | mots: Markowitz, frontière efficiente, variance minimale, Sharpe maximal, portefeuille tangent, matrice de covariance, SLSQP, optimisation | aller: Analyse du portefeuille/Optimisation | chiffres: sharpe, volatilite -->

### Les paramètres

```
μ = moyenne des rendements quotidiens × 252        (rendement espéré de chaque titre)
Σ = covariance des rendements quotidiens × 252    (matrice de covariance)
```

calculés sur les jours où **tous** les titres ont un cours.

### Un portefeuille de poids w

```
rendement = wᵀμ    volatilité = √(wᵀΣw)    Sharpe = (rendement − taux sans risque) / volatilité
```

### Les optimisations

Contraintes : chaque poids entre 0 et le [[Poids maximal par titre]] (30 % par défaut), somme des poids = 100 %. Méthode SLSQP (bibliothèque SciPy), en partant de poids égaux.

- **Variance minimale** : minimise `wᵀΣw`.
- **Sharpe maximal** : maximise le Sharpe (portefeuille « tangent »).
- **Frontière** : 40 rendements cibles, du rendement de la variance minimale au rendement maximal atteignable ; pour chacun, la variance minimale. Si moins de deux points aboutissent, la frontière est approchée par l'enveloppe de 4 000 portefeuilles tirés au hasard (loi de Dirichlet).

### Exemple

Titre A (μ 6 %, σ 20 %), titre B (μ 9 %, σ 30 %), corrélation 0,3, sans limite de poids : variance minimale à 76,6 % de A, volatilité 18,67 % ; Sharpe maximal (taux 2,50 %) à environ 50/50, rendement 7,50 %, volatilité 20,36 %, Sharpe 0,25.

### Répartitions comparées

`montant à acheter (+) ou vendre (−) = (poids cible − poids actuel) × valeur totale`. Un écart inférieur à 0,25 point est jugé inchangé.

### Limite

Les rendements espérés sont des moyennes passées : l'optimiseur surexploite les titres qui ont le mieux marché.

## La projection de Monte-Carlo
<!-- fiche: formule-monte-carlo | questions: comment fonctionne la simulation de monte carlo ; formule mouvement brownien géométrique ; pourquoi moins sigma carré sur 2 ; méthode historique bootstrap ; probabilité de perte comment est elle calculée ; pourquoi la moyenne est supérieure à la médiane ; loi log normale valeur finale | mots: Monte-Carlo, simulation, mouvement brownien géométrique, bootstrap, log-normale, percentiles, médiane, probabilité de perte | aller: Analyse du portefeuille/Projection | chiffres: valeur_actuelle, volatilite -->

### Les paramètres

Par défaut, ceux du portefeuille : `μ = moyenne quotidienne × 252`, `σ = écart-type quotidien × √252`. Ils sont modifiables avec les curseurs.

### Méthode « Loi normale » (mouvement brownien géométrique)

Le pas de temps est le mois (`dt = 1/12`) :

```
log-rendement mensuel ~ Normale( (μ − σ²/2) × dt , σ × √dt )
valeur(m + 1) = valeur(m) × exp(log-rendement) + versement mensuel
```

Le terme `− σ²/2` corrige l'écart entre moyenne arithmétique et croissance composée : +50 % puis −50 % donne une moyenne nulle, mais une perte de 25 %.

### Méthode « Historique (bootstrap) »

Chaque mois additionne 21 log-rendements quotidiens tirés au hasard, avec remise, parmi les vrais jours du portefeuille, recentrés pour que leur moyenne corresponde au rendement choisi. Les queues épaisses réelles sont conservées.

### Les résultats

5 000 scénarios (graine fixe, résultats reproductibles) ; percentiles 5, 25, 50, 75 et 95 ; probabilité de perte = part des scénarios qui finissent sous `valeur de départ + versements`.

### Exemple

100 000 €, μ 7 %, σ 15 %, 10 ans, loi normale : médiane ≈ 178 700 € (théorie : `100 000 × exp((0,07 − 0,01125) × 10) ≈ 179 900 €`), scénario défavorable ≈ 81 900 €, favorable ≈ 389 600 €, moyenne ≈ 199 800 €, probabilité de perte ≈ 10,4 %.

### Interprétation

La valeur finale suit une loi log-normale : la moyenne dépasse la médiane, qui est le repère le plus représentatif. Une projection n'est pas une prévision.

## Les contributions au risque (Euler)
<!-- fiche: formule-contributions-risque | questions: comment est calculée la contribution au risque ; contribution marginale au risque formule ; d'où vient le risque de mon portefeuille ; part du risque supérieure à la part de la valeur ; décomposition d'euler ; plus gros contributeur au risque | mots: contribution au risque, contribution marginale, Euler, budget de risque, décomposition du risque, part du risque, volatilité | aller: Gestion d'actifs/Budget de risque | chiffres: volatilite -->

Le poids d'une ligne ne dit pas quelle part du **risque** elle apporte.

### Les formules

```
σ_p = √(wᵀΣw)
contribution marginale    CMᵢ = (Σw)ᵢ / σ_p
contribution au risque    CRᵢ = wᵢ × CMᵢ
part du risque            CRᵢ / σ_p      (la somme fait 100 %)
```

Propriété d'Euler : `Σ CRᵢ = σ_p`, vérifiée par un test automatique. `Σ` est la matrice de covariance annualisée (rendements quotidiens × 252), estimée sur l'historique.

### Exemple

Deux lignes à 50 % (volatilités 20 % et 30 %, corrélation 0,3) : `σ_p ≈ 20,37 %`. Contributions : 7,12 et 13,25 points, soit **34,9 %** et **65,1 %** du risque pour 50 % de la valeur chacune. Le ratio risque / poids de la seconde ligne vaut 1,30.

### Interprétation

Une ligne dont la part du risque dépasse sa part de la valeur est plus volatile ou plus corrélée au reste. L'onglet [[Budget de risque]] montre les 20 plus gros contributeurs ; l'onglet Expositions répartit ces parts par région.

### La parité des risques

L'allocation « Parité des risques » cherche les poids pour lesquels chaque ligne apporte la même part du risque : elle minimise `½ wᵀΣw − (1/n) × Σ ln(wᵢ)`, puis ramène la somme des poids à 100 % (méthode de Spinu). Dans l'exemple, ce sont 60 % et 40 % : chaque ligne apporte alors 50 % du risque. Elle n'utilise pas les rendements espérés.

## L'attribution de performance de Brinson-Fachler
<!-- fiche: formule-brinson-fachler | questions: comment est calculée l'attribution de performance ; effet allocation formule ; effet sélection ; effet interaction ; modèle de brinson fachler ; lissage de cariño ; pourquoi la somme des effets égale l'écart ; quel indice pour l'attribution | mots: attribution de performance, Brinson-Fachler, effet allocation, effet sélection, effet interaction, Cariño, MSCI ACWI IMI, régions | aller: Gestion d'actifs/Attribution de performance -->

Le modèle explique, région par région, l'écart entre la poche actions et un indice actions mondial.

### Les formules (sur une période)

```
Effet allocation  = (wp − wb) × (rb − Rb)
Effet sélection   = wb × (rp − rb)
Effet interaction = (wp − wb) × (rp − rb)
Rb = Σ wb × rb    Rp = Σ wp × rp
```

`wp`, `wb` : poids de la région dans le portefeuille et dans l'indice ; `rp`, `rb` : rendements de la région. La somme des trois effets, toutes régions comprises, vaut `Rp − Rb`.

### Exemple

États-Unis : wp 70 %, wb 60 %, rp 12 %, rb 10 %. Europe : wp 30 %, wb 40 %, rp 3 %, rb 5 %. Rb = 8 %, Rp = 9,3 %.
Allocation : +0,2 + 0,3 = +0,5 point ; sélection : +1,2 − 0,8 = +0,4 ; interaction : +0,2 + 0,2 = +0,4. Total : +1,3 point = 9,3 % − 8 %.

### La mise en œuvre

- Calcul mois par mois, avec les poids de fin du mois précédent.
- Mois reliés par le lissage de Cariño : chaque mois est pondéré par `kₜ / K`, avec `k = [ln(1 + Rp) − ln(1 + Rb)] / (Rp − Rb)`, pour que la somme tombe exactement sur l'écart composé.
- Indice : poids régionaux du MSCI ACWI IMI au 30/06/2026 (États-Unis 62,7 %, émergents 12,3 %, Europe 8,7 %…, ramenés à 100 %), et un indice boursier par région, converti en euros, hors dividendes.
- Obligations et or exclus ; une région absente de l'indice prend `rb = Rb`.

## La conversion des devises en euros
<!-- fiche: formule-devises | questions: formule de conversion en euros ; comment sont convertis les cours en dollars ; taux eurusd nombre de dollars pour un euro ; pence facteur 0,01 ; taux du jour de l'achat ou du jour ; les frais sont ils convertis ; effet de change dans la performance | mots: conversion, devises, taux de change, EURUSD, pence, GBp, risque de change, euro | aller: Analyse du portefeuille/Positions -->

### La formule

```
prix en euros = prix en devise × facteur / taux EURdevise
```

- `EURUSD=X` (Yahoo Finance) est le nombre de dollars pour 1 euro ;
- facteur = 0,01 pour les cotations en pence (`GBp`, actions de Londres), 1 sinon.

### Quel taux ?

| Élément | Taux utilisé |
|---|---|
| achat, vente, dividende | taux du jour de l'opération |
| valeur jour par jour | taux de chaque jour |
| valeur actuelle | dernier taux connu |
| frais | aucun : toujours en euros |

Un jour sans taux reprend le dernier taux connu.

### Exemples

- Apple à 200 USD, 1 € = 1,10 USD : `200 / 1,10 = 181,82 €`.
- Action de Londres à 1 250 pence, 1 € = 0,85 GBP : `1 250 × 0,01 / 0,85 = 14,71 €`.

### Ce que cela implique

La performance d'un titre étranger combine son cours et sa devise : une action américaine qui gagne 10 % en dollars ne rapporte presque rien en euros si le dollar perd environ 10 %. Le taux est celui de Yahoo Finance, pas celui de votre banque. Le taux du jour figure en bas de la barre latérale (« 1 € en USD », par exemple).

## Duration et choc de taux
<!-- fiche: formule-duration | questions: comment est calculée la perte si les taux montent ; duration moyenne formule ; sensibilité aux taux des obligations ; choc de taux de 1 point ; pourquoi mes obligations baissent quand les taux montent ; où est la duration de mon fonds obligataire | mots: duration, sensibilité, taux d'intérêt, choc de taux, obligations, hausse des taux, approximation | aller: Analyse du portefeuille/Expositions -->

### Les formules

```
duration moyenne = Σ (duration × valeur) / Σ valeur      (lignes obligataires dont la duration est connue)
perte si les taux montent de 1 point ≈ Σ (duration × valeur) × 1 %
en % du portefeuille = perte / valeur totale
```

Approximation au premier ordre : `variation du prix ≈ − duration × variation des taux`.

### Exemple

20 000 € d'un fonds obligataire de duration 7 ans dans un portefeuille de 100 000 € : hausse des taux de 1 point, perte ≈ `7 × 1 % × 20 000 = 1 400 €`, soit −1,4 % du portefeuille.

### D'où vient la duration ?

Du référentiel du projet (`data/referentiel.csv`), seulement pour les fonds obligataires qui y figurent. Sans duration connue, une ligne n'entre pas dans le calcul.

### Interprétation

Plus la duration est longue, plus le prix baisse quand les taux montent, et monte quand ils baissent. Les seuils du diagnostic dépendent du profil : 5 et 8 ans (Prudent), 7 et 10 ans (Équilibré), 8 et 12 ans (Dynamique).

### Limites

Approximation linéaire, valable pour de petits chocs (la convexité est ignorée). Après la baisse, les obligations retrouvent un rendement plus élevé.

## Les stress tests : formules des scénarios
<!-- fiche: formule-stress-tests | questions: comment sont calculés les stress tests ; formule du choc actions beta fois choc ; scénario baisse du dollar de 10 % ; crise de 2008 rejouée comment ; pourquoi un indice remplace mon titre ; part estimée par un indice ; perte en cas de krach | mots: stress test, scénario, crise, choc, bêta, proxy, duration, dollar, 2008, Covid | aller: Conseil patrimonial/Stress tests -->

### Scénarios historiques

```
variation d'une ligne = cours à la date du plus bas / cours à la date du plus haut − 1
variation du portefeuille = Σ poids actuel × variation de la ligne
```

Cinq crises : 2008-2009, dette européenne (2011), Covid (2020), inflation et hausse des taux (2022), mini-krach d'août 2024. Si un titre n'était pas coté (premier cours plus de 7 jours après le début de la crise), l'indice de sa région, ou un fonds obligataire ou d'or de même catégorie, sert d'approximation. Variations en devise locale, hors dividendes.

### Scénarios hypothétiques

```
Baisse des actions de X %  : variation ≈ bêta × (−X %)       (X = 10, 20, 35)
Baisse du dollar de 10 %   : variation = −10 % × part des lignes cotées en dollars
Hausse des taux de 1 point : variation = −1 % × Σ poids × duration
```

### Exemple

Bêta de 0,90 et baisse des actions de 20 % : `0,90 × (−20 %) = −18 %`, soit −18 000 € sur 100 000 €.

### Limites

Le portefeuille actuel est supposé inchangé pendant toute la crise ; l'effet de change est ignoré dans les scénarios historiques ; le choc « dollar » ne regarde que la devise de cotation, pas le contenu des ETF.

## La fiscalité à la sortie : CTO, PEA, assurance-vie
<!-- fiche: formule-fiscalite | questions: comment est calculé l'impôt si je vends tout ; flat tax 31,4 % ; pfu 2026 ; fiscalité pea après 5 ans ; abattement assurance vie 4600 ; formule impôt plus-value compte titres ; pourquoi mes dividendes sont taxés malgré une moins-value | mots: fiscalité, PFU, flat tax, prélèvements sociaux, PEA, assurance-vie, CTO, abattement, impôt | aller: Conseil patrimonial/Fiscalité | chiffres: gain_total, dividendes -->

Le logiciel calcule l'impôt dû si tout le portefeuille était vendu, selon les règles 2026 (particulier résident en France).

### Les formules

| Enveloppe | Base | Impôt sur le revenu | Prélèvements sociaux |
|---|---|---|---|
| CTO | `max(plus-values, 0) + max(dividendes, 0)` | 12,8 % | 18,6 % |
| PEA, moins de 5 ans | `max(gain, 0)` | 12,8 % | 18,6 % |
| PEA, 5 ans et plus | `max(gain, 0)` | 0 | 18,6 % |
| Assurance-vie, moins de 8 ans | `max(gain, 0)` | 12,8 % | 17,2 % |
| Assurance-vie, 8 ans et plus | `max(gain, 0)` | 7,5 % × `max(gain − 4 600 €, 0)` (9 200 € pour un couple) | 17,2 % |

Au CTO, une moins-value s'impute sur les plus-values, pas sur les dividendes. L'ancienneté est comptée depuis la première opération : `jours / 365,25`.

### Exemple, gain de 10 000 €

- CTO : `31,4 % × 10 000 = 3 140 €` ;
- PEA de 6 ans : `18,6 % × 10 000 = 1 860 €` ;
- assurance-vie de 9 ans, célibataire : `7,5 % × 5 400 + 17,2 % × 10 000 = 405 + 1 720 = 2 125 €`.

### Simplifications

Option pour le barème progressif ignorée, primes d'assurance-vie supposées inférieures à 150 000 €, frais de gestion des contrats ignorés, dividendes supposés conservés dans l'enveloppe. Ce n'est pas un calcul fiscal officiel.
