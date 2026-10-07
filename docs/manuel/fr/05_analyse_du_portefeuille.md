# Analyse du portefeuille
<!-- chapitre: analyse | ordre: 5 -->

Ce chapitre explique, onglet par onglet, l'espace « Analyse du portefeuille » : la vue d'ensemble et la carte du monde, les positions, la performance, le risque, les expositions et la diversification réelle, puis la consultation des transactions. Chaque indicateur a sa fiche : la formule exacte utilisée par le logiciel, l'intuition, un exemple chiffré, la manière de le lire et ses limites. Les onglets Optimisation et Projection sont traités dans un chapitre à part.

## Les huit onglets de l'analyse : que trouver où ?
<!-- fiche: analyse-onglets | questions: quels sont les onglets de l'analyse du portefeuille ; ou trouver la volatilité ; dans quel onglet est la var ; ou voir mes plus-values ; je cherche les corrélations ; ou est le tableau de mes lignes ; à quoi sert chaque onglet ; ou sont les transactions | mots: onglets, Vue d'ensemble, Positions, Performance, Risque, Expositions, Optimisation, Projection, Transactions, navigation | aller: Analyse du portefeuille -->

L'espace « Analyse du portefeuille » compte huit onglets, affichés en haut de la zone principale sous les six chiffres clés.

| Onglet | Ce que vous y trouvez |
|---|---|
| [[Vue d'ensemble]] | Évolution de la valeur et du capital investi, répartition par ligne, carte du monde, répartitions par classe d'actifs, région et secteur, plus-values, dividendes et frais |
| [[Positions]] | Le tableau des lignes détenues (quantité, PRU, cours, valeur, plus-value, poids) et le graphique des plus-values latentes par ligne |
| [[Performance]] | TWR, TRI, écart avec l'indice, courbe en base 100, rendements par année civile, drawdown, bêta, alpha, corrélation, tracking error, ratio d'information |
| [[Risque]] | Sharpe, Sortino, VaR et CVaR, distribution des rendements quotidiens comparée à la loi normale, asymétrie, kurtosis, test de Jarque-Bera |
| [[Expositions]] | Diagnostic en six dimensions (géographie, secteurs, devises, concentration, taux, diversification réelle), constats et pistes, corrélations entre les lignes |
| [[Optimisation]] | Frontière efficiente de Markowitz et répartitions comparées (chapitre consacré à l'optimisation et à la projection) |
| [[Projection]] | Simulation de Monte-Carlo de la valeur future (même chapitre) |
| [[Transactions]] | L'historique des opérations, filtrable et téléchargeable ; la modification des opérations est décrite dans le chapitre sur l'import |

### Bon à savoir

- Tous les onglets analysent le même portefeuille, avec l'indice de référence, le taux sans risque et le niveau de VaR choisis dans le panneau **Paramètres** de la barre latérale.
- Tous les montants sont exprimés **en euros**, y compris pour les titres cotés dans une autre devise.
- Les corrélations entre les lignes ne sont pas dans l'onglet Risque : elles se trouvent dans l'onglet [[Expositions]], sous-onglet [[Corrélations]].

## Que montre l'onglet Vue d'ensemble ?
<!-- fiche: analyse-vue-ensemble | questions: que montre la vue d'ensemble ; à quoi servent les anneaux de couleur ; répartition par classe d'actifs ou la voir ; pourquoi la répartition par région est en pourcentage de la poche actions ; c'est quoi la part autres dans le camembert ; les quatre cartes en bas de la vue d'ensemble ; je ne vois pas l'anneau par secteur ; graphique répartition par ligne | mots: vue d'ensemble, répartition, anneau, camembert, classe d'actifs, région, secteur, poche actions, synthèse, donut | aller: Analyse du portefeuille/Vue d'ensemble | chiffres: valeur_actuelle, gain_total, dividendes, frais_totaux -->

L'onglet [[Vue d'ensemble]] donne une photographie du portefeuille en quatre blocs, de haut en bas.

### 1. Évolution et répartition

- À gauche, **Évolution du portefeuille** : la valeur de marché et le capital investi au fil du temps (voir la fiche dédiée).
- À droite, **Répartition** : une barre par ligne, de la plus grosse à la plus petite, avec son poids dans la valeur totale. Au-delà de 15 lignes, les plus petites sont regroupées dans une barre grise « Autres ». Le survol affiche la valeur en euros.

### 2. Présence dans le monde

La carte colore chaque pays selon son poids dans la **poche actions** (fiche dédiée). Elle n'apparaît que si le portefeuille contient des actions dont le pays est connu.

### 3. Trois anneaux

| Anneau | Base de calcul |
|---|---|
| Par classe d'actifs | En % de la **valeur totale** (actions, obligations, or…) |
| Par région | En % de la **poche actions** seulement |
| Par secteur | En % de la **poche actions** seulement |

Les trois anneaux sont calculés **en transparence** : un ETF est réparti entre les pays et les secteurs de l'indice qu'il suit. Les parts inférieures à 3 % sont regroupées dans « Autres », et chaque anneau montre au plus huit parts nommées. Le survol donne le pourcentage et le montant en euros. Un anneau qui ne compterait qu'un seul groupe (par exemple un portefeuille 100 % actions pour les classes d'actifs) n'est pas affiché.

### 4. Quatre cartes

| Carte | Contenu |
|---|---|
| Plus-values latentes | Gain ou perte non encaissé sur les lignes détenues (« non réalisées ») |
| Plus-values réalisées | Gain ou perte encaissé lors des ventes (« encaissées ») |
| Dividendes et coupons | Total des dividendes et coupons saisis, depuis l'origine |
| Frais de courtage | Total des frais saisis, depuis l'origine |

La somme des trois premières cartes donne le **gain total** affiché en haut de page.

## Lire le graphique « Évolution du portefeuille »
<!-- fiche: analyse-evolution-valeur | questions: que veut dire la courbe orange ; c'est quoi les apports nets ; pourquoi la courbe orange descend ; différence entre valeur et argent investi ; la zone bleue entre les deux courbes ; ma valeur est sous l'argent investi est ce que je perds ; pourquoi la courbe fait des marches ; argent investi négatif | mots: évolution, valeur de marché, apports nets, capital investi, argent investi, courbe, historique, gain latent, graphique | aller: Analyse du portefeuille/Vue d'ensemble | chiffres: valeur_actuelle, gain_total -->

Ce graphique, en haut de l'onglet [[Vue d'ensemble]], superpose deux courbes jour de bourse par jour de bourse.

| Courbe | Calcul |
|---|---|
| **Valeur du portefeuille** (bleue) | Σ quantité détenue ce jour-là × cours de clôture du jour, en euros |
| **Argent investi (apports nets)** (orange, en marches d'escalier) | Somme cumulée de l'argent sorti de votre poche |

### Comment sont calculés les apports nets

Chaque opération crée un flux d'argent :

- **achat** : `+ (quantité × prix + frais)` ;
- **vente** : `− (quantité × prix − frais)` ;
- **dividende** : `− (montant − frais)`.

Les apports nets sont la somme de ces flux depuis le début. Une vente ou un dividende fait donc **descendre** la courbe orange : cet argent est revenu chez vous. Si vous avez récupéré plus que vous n'aviez apporté, la courbe peut même passer sous zéro.

### Lire l'écart entre les deux courbes

L'écart vertical, coloré en bleu clair, est le **gain à cette date** : `valeur − apports nets`. Le dernier jour, il correspond au gain total des chiffres clés, à un petit écart près : la carte utilise le dernier cours téléchargé, la courbe le dernier cours de clôture de l'historique. Une courbe bleue sous la courbe orange signifie qu'à cette date le portefeuille valait moins que l'argent net apporté.

### Exemple

Vous achetez pour 1 000 € (frais compris), puis touchez 30 € de dividende. Les apports nets passent à 1 000 €, puis à 970 €. Si le portefeuille vaut 1 100 €, le gain est de `1 100 − 970 = 130 €`.

### Astuces

Les boutons 1M, 6M, YTD, 1A et Tout choisissent la période ; le survol réunit les deux valeurs à la même date. Une opération saisie un jour sans cotation (un samedi, par exemple) est rattachée au jour de bourse suivant.

## La carte « Présence dans le monde »
<!-- fiche: analyse-carte-monde | questions: comment lire la carte du monde ; pourquoi les états-unis sont foncés alors que je n'ai pas d'action américaine ; la carte ne s'affiche pas ; mes obligations ne sont pas sur la carte ; que veut dire hors carte ; comment voir les titres d'un pays ; pourquoi l'or n'apparaît pas sur la carte ; carte géographique de mon portefeuille | mots: carte du monde, géographie, pays, poche actions, choroplèthe, hors carte, exposition géographique, monde | aller: Analyse du portefeuille/Vue d'ensemble -->

La carte de l'onglet [[Vue d'ensemble]] montre **où sont les entreprises** dont vous détenez des actions, directement ou au travers d'ETF.

### Ce qui est représenté

- Chaque pays est coloré selon son poids dans la **poche actions** (et non dans tout le portefeuille) : plus le bleu est foncé, plus le pays pèse. L'échelle va de 0 au poids du premier pays.
- Les pays sans exposition sont en gris clair.
- Au survol : le pourcentage de la poche actions, le montant en euros, le nombre de titres concernés et jusqu'à six de leurs noms.

### Pourquoi les États-Unis sont souvent foncés

Un ETF MSCI World est réparti selon la composition de son indice. Pour 10 000 € investis, le logiciel compte 7 294 € aux États-Unis, 591 € au Japon, 341 € au Royaume-Uni, 329 € au Canada, 224 € en France, etc. Un portefeuille sans aucune action américaine en direct peut donc être très exposé aux États-Unis.

### Ce qui n'est pas sur la carte

Les obligations, l'or et les titres dont le pays est inconnu (« Non classé ») ne sont pas représentés. Quand ils pèsent plus de 0,5 % de la valeur, une note sous la carte indique leur part, par exemple « Hors carte : Obligations 25 %, Or 5 % ».

### Limites

- La carte est une approximation (fiche suivante).
- Elle ne se zoome pas ; le survol reste possible.
- Elle disparaît si aucune action n'a de pays reconnu.

## Pourquoi la carte du monde est-elle une approximation ?
<!-- fiche: analyse-carte-approximation | questions: la carte est elle exacte ; pourquoi la répartition par pays de mon etf est approximative ; d'où viennent les poids par pays ; mon etf n'a pas exactement ces pays ; les chiffres de la carte sont ils à jour ; approximation au 30/09/2026 ça veut dire quoi ; le msci world contient il vraiment 73 % d'états-unis | mots: approximation, composition des ETF, données au 30/09/2026, fiche MSCI, poids par pays, exactitude, transparence, mise à jour | aller: Analyse du portefeuille/Vue d'ensemble -->

La note sous la carte précise : « ETF répartis selon la composition de leur indice (approximation au 30/09/2026) ». Cette approximation a plusieurs causes, toutes visibles dans le code.

### 1. Une composition type par indice, pas celle de votre fonds

Le logiciel ne lit pas l'inventaire réel de votre ETF. Il reconnaît **l'indice suivi** (par le code du titre, sinon par des mots de son nom comme « World », « S&P 500 », « Emerging ») et applique la composition de cet indice.

### 2. Des sources simplifiées

- MSCI World, ACWI, Marchés émergents et Europe : les cinq premiers pays et les secteurs viennent des fiches MSCI au 30/09/2026 ; les pays suivants sont des ordres de grandeur, ramenés au total « autres pays » de la fiche.
- S&P 500, Nasdaq-100, Euro Stoxx 50, CAC 40, DAX et indices obligataires : ordres de grandeur 2025-2026.
- Le MSCI ACWI est reconstruit en combinant 88 % de MSCI World et 12 % de Marchés émergents.

### 3. Une hypothèse sur les secteurs

Pour un ETF actions, chaque pays reçoit le **même mélange sectoriel** que l'indice entier. En réalité, les entreprises japonaises n'ont pas la même répartition sectorielle que les américaines.

### 4. Les ETF non reconnus

Un fonds dont ni le code ni le nom ne permet de retrouver l'indice garde le pays de sa fiche ; si ce pays n'est pas un vrai pays (« Monde », par exemple), il est compté « Non classé » et ne figure pas sur la carte.

### Est-ce gênant ?

Les poids des grands indices bougent peu d'une année sur l'autre : l'écart reste de quelques points au plus, ce qui suffit pour juger d'une exposition. Pour un chiffre exact, consultez la fiche mensuelle de votre ETF chez son émetteur.

## Que veut dire « en transparence » ?
<!-- fiche: analyse-transparence | questions: que veut dire en transparence ; analyse en transparence c'est quoi ; pourquoi mon etf est découpé en plusieurs pays ; look-through ; mon etf monde est compté comme une action française ; pourquoi la répartition par région diffère de celle du tableau des positions ; comment les etf sont-ils éclatés | mots: transparence, look-through, éclatement des ETF, composition, exposition réelle, ETF, indice suivi, répartition | aller: Analyse du portefeuille/Expositions -->

Un ETF est enregistré comme **un seul titre** : par exemple un ETF MSCI World coté à Paris, en euros. Mais il contient des centaines d'actions de nombreux pays. L'analyse « en transparence » regarde **à travers** le fonds pour mesurer les vraies expositions.

### Comment le logiciel procède

Pour chaque ligne du portefeuille :

1. **Action détenue en direct** : elle garde son pays, son secteur et sa devise de cotation.
2. **ETF ou fonds actions** : sa valeur est répartie entre les pays de l'indice suivi, puis, dans chaque pays, entre les secteurs de l'indice. La devise retenue est celle de chaque pays (dollar pour les États-Unis, yen pour le Japon…), sauf si le nom du fonds indique une couverture de change (« Hedged », « couvert »), auquel cas tout est compté en euros.
3. **Fonds obligataire** : réparti entre les pays de l'indice obligataire ; devise euro pour un indice de la zone euro, dollar sinon.
4. **Or** : compté à part, sans pays ni secteur, avec la « devise » Or.

### Exemple

Un ETF MSCI World de 10 000 € devient environ 7 294 € d'actions américaines (en dollars), 591 € d'actions japonaises (en yens), 341 € d'actions britanniques (en livres), 224 € d'actions françaises (en euros), etc.

### Où la transparence est utilisée

- la carte du monde et les anneaux par région et par secteur de la vue d'ensemble ;
- tout l'onglet [[Expositions]] : géographie, secteurs, devises, doublons probables ;
- la partie « Expositions et diversification » du rapport PDF.

En revanche, le tableau de l'onglet [[Positions]] affiche le classement **de la ligne elle-même** (par exemple région « Monde » pour un ETF monde), sans éclatement. C'est pourquoi ses régions diffèrent de celles des anneaux.

## Valeur actuelle, capital investi et PRU
<!-- fiche: analyse-valeur-pru | questions: comment est calculé le pru ; c'est quoi le prix de revient unitaire ; les frais sont ils dans le pru ; pourquoi mon pru est différent de celui de mon courtier ; le pru change t il après une vente ; investi au pru ça veut dire quoi ; comment est calculée la valeur actuelle ; pourquoi le montant investi a baissé après une vente | mots: PRU, prix de revient unitaire, prix moyen, coût de revient, montant investi, valeur actuelle, frais d'achat, moyenne pondérée | aller: Analyse du portefeuille/Positions | chiffres: valeur_actuelle, montant_investi -->

### La valeur actuelle

`Valeur d'une ligne = quantité détenue × dernier cours (converti en euros)`

La valeur actuelle est la somme des valeurs des lignes encore détenues. Le dernier cours est celui téléchargé auprès de Yahoo Finance lors de l'analyse, ou le dernier cours enregistré si Internet n'est pas disponible.

### Le PRU (prix de revient unitaire)

Le logiciel rejoue toutes vos opérations dans l'ordre des dates, selon la méthode du prix moyen pondéré utilisée en France.

- **Achat** : `nouveau PRU = (quantité détenue × ancien PRU + quantité achetée × prix + frais) / (quantité détenue + quantité achetée)`. Les frais d'achat sont **inclus** dans le PRU.
- **Vente** : le PRU **ne change pas**. Si vous vendez tout, il repart de zéro.
- **Dividende** : aucun effet sur le PRU.

### Le capital investi au PRU

`Montant investi = Σ quantité détenue × PRU`

C'est le coût de revient des titres encore en portefeuille. Il apparaît sous la carte Valeur actuelle (« Investi au PRU »). Il baisse après une vente, puisque les titres vendus sortent du calcul.

### Exemple

| Opération | Calcul | PRU |
|---|---|---|
| Achat de 10 titres à 100 €, 5 € de frais | `(10 × 100 + 5) / 10` | 100,50 € |
| Achat de 10 titres à 120 €, 5 € de frais | `(1 005 + 1 205) / 20` | 110,50 € |
| Vente de 5 titres à 130 € | PRU inchangé | 110,50 € |

Il reste 15 titres : montant investi `15 × 110,50 = 1 657,50 €`. Au cours de 125 €, la valeur est de `15 × 125 = 1 875 €`.

### Limites

- Si votre courtier calcule un PRU hors frais, le sien sera plus bas.
- Pour un titre en devise, le PRU est en euros, chaque achat étant converti au taux de change de son jour (voir la fiche sur les titres en devises).

## Les plus-values latentes
<!-- fiche: analyse-plus-values-latentes | questions: c'est quoi une plus-value latente ; comment est calculée la plus-value en pourcentage ; pourquoi ma plus-value latente est négative ; plus-value non réalisée ; la colonne +/- value ; le graphique vert et rouge des plus-values ; est ce que la plus-value tient compte des frais de vente ; moins-value latente | mots: plus-value latente, moins-value latente, non réalisée, +/- value, gain latent, PRU, potentiel, graphique des plus-values | aller: Analyse du portefeuille/Positions | chiffres: gain_total, montant_investi -->

Une plus-value **latente** est un gain qui n'est pas encore encaissé : c'est ce que vous gagneriez (ou perdriez) en vendant aujourd'hui.

### Formules

```
Plus-value latente   = valeur − montant investi = quantité × (cours − PRU)
Plus-value latente % = plus-value latente / montant investi × 100
```

### Exemple

15 titres au PRU de 110,50 €, cours actuel 125 € : plus-value latente `15 × (125 − 110,50) = 217,50 €`, soit `217,50 / 1 657,50 = +13,12 %`.

### Où la voir

- Carte **Plus-values latentes** de l'onglet [[Vue d'ensemble]] : le total, toutes lignes confondues.
- Colonnes « +/- value » et « +/- value % » du tableau de l'onglet [[Positions]].
- Graphique **Plus-values latentes par ligne** de l'onglet [[Positions]] : une barre par ligne, verte pour un gain, rouge pour une perte, triées de la plus forte perte au plus fort gain. Le survol donne le montant et le pourcentage.

### Ce qu'elle comprend et ne comprend pas

- Les **frais d'achat** sont déjà dedans, puisqu'ils sont inclus dans le PRU.
- Les **frais de la vente future** ne sont pas déduits.
- Les **impôts** ne sont pas déduits (la fiscalité d'une vente est simulée dans l'espace Conseil patrimonial).
- Pour un titre en devise, elle inclut l'effet du taux de change.
- Les dividendes déjà perçus ne sont pas dans la plus-value latente : ils sont comptés à part.

## Les plus-values réalisées (et les lignes vendues)
<!-- fiche: analyse-plus-values-realisees | questions: c'est quoi une plus-value réalisée ; comment est calculée la plus-value d'une vente ; j'ai vendu une ligne elle a disparu du tableau ; ou voir le gain d'une ligne vendue ; mes ventes sont elles prises en compte ; plus-value encaissée ; une vente partielle change t elle le pru ; moins-value réalisée | mots: plus-value réalisée, moins-value réalisée, vente, encaissée, ligne soldée, ligne vendue, PRU, cession | aller: Analyse du portefeuille/Vue d'ensemble | chiffres: gain_total -->

Une plus-value **réalisée** est le gain (ou la perte) encaissé lors d'une vente.

### Formule

`Plus-value réalisée = quantité vendue × (prix de vente − PRU) − frais de vente`

Le PRU utilisé est celui du moment de la vente ; il reste inchangé après une vente partielle.

### Exemple

Vous détenez 20 titres au PRU de 110,50 € et en vendez 5 à 130 €, avec 4 € de frais : `5 × (130 − 110,50) − 4 = 93,50 €`. Il vous reste 15 titres, toujours au PRU de 110,50 €.

### Où la voir

La carte **Plus-values réalisées** (« encaissées ») de l'onglet [[Vue d'ensemble]] additionne les plus et moins-values de toutes les ventes, depuis l'origine.

### Une ligne entièrement vendue

Une ligne vendue en totalité disparaît du tableau de l'onglet [[Positions]], qui ne montre que les titres encore détenus. Elle n'est pas oubliée pour autant :

- sa plus-value réalisée et ses dividendes restent comptés dans le gain total ;
- son historique reste utilisé pour la courbe d'évolution et les indicateurs de performance ;
- ses opérations restent visibles dans l'onglet [[Transactions]].

En revanche, elle n'entre plus dans les répartitions, les expositions ni les corrélations, qui portent sur les lignes détenues aujourd'hui.

### Limite

Le calcul suit la méthode du PRU moyen pondéré. Il ne déduit aucun impôt.

## Gain total : pourquoi ne correspond-il pas aux seules plus-values latentes ?
<!-- fiche: analyse-gain-total | questions: comment est calculé le gain total ; pourquoi le gain total est différent de ma plus-value ; le gain total inclut il les dividendes ; gain total supérieur à la somme des plus-values du tableau ; pourquoi le pourcentage du gain total est bizarre après une vente ; gain sur capital investi c'est quoi ; mon gain total est positif mais mes lignes sont en perte | mots: gain total, performance globale, plus-values latentes, plus-values réalisées, dividendes, rendement sur capital investi, bénéfice | aller: Analyse du portefeuille/Vue d'ensemble | chiffres: gain_total, montant_investi, dividendes -->

### La formule

`Gain total = plus-values latentes + plus-values réalisées + dividendes`

Le gain total mesure tout ce que le portefeuille a rapporté depuis le début. Les plus-values latentes n'en sont qu'une partie : elles ignorent les ventes passées et les dividendes encaissés. Les frais n'apparaissent pas comme un terme séparé : ils sont déjà déduits, dans le PRU (frais d'achat), dans les plus-values réalisées (frais de vente) et dans les dividendes (frais saisis sur la ligne de dividende).

### Exemple complet

| Élément | Montant |
|---|---|
| Plus-values latentes (15 titres, PRU 110,50 €, cours 125 €) | +217,50 € |
| Plus-value réalisée (vente de 5 titres à 130 €) | +93,50 € |
| Dividendes | +30,00 € |
| **Gain total** | **+341,00 €** |

Vérification par les flux d'argent : achats `1 005 + 1 205 = 2 210 €`, vente nette `650 − 4 = 646 €`, dividende 30 €. Apports nets : `2 210 − 646 − 30 = 1 534 €`. Valeur 1 875 €. Gain : `1 875 − 1 534 = 341 €`. Les deux méthodes donnent le même résultat.

### Le pourcentage « sur le capital investi »

`Gain sur capital investi = gain total / montant investi au PRU`

Dans l'exemple : `341 / 1 657,50 = +20,57 %`. Attention : le dénominateur est le coût des titres **encore détenus**. Après de grosses ventes, il devient petit et le pourcentage peut paraître très élevé. Pour mesurer la qualité de vos placements, préférez le TWR de l'onglet [[Performance]].

### Mes lignes sont en perte, mais le gain total est positif

C'est possible : des ventes passées gagnantes ou des dividendes peuvent compenser des moins-values latentes.

## Dividendes, coupons et frais : comment sont-ils comptés ?
<!-- fiche: analyse-dividendes-frais | questions: les dividendes sont ils comptés dans la performance ; montants bruts perçus ça veut dire quoi ; les dividendes sont ils nets d'impôt ; ou voir mes frais de courtage ; les frais sont ils déduits de la performance ; dividende d'une ligne vendue ; coupons d'obligation pris en compte ; pourquoi mes frais totaux semblent élevés | mots: dividendes, coupons, distributions, frais de courtage, frais totaux, brut, net, prélèvements, performance, coût | aller: Analyse du portefeuille/Vue d'ensemble | chiffres: dividendes, frais_totaux, gain_total -->

### Les dividendes et coupons

- Ils sont saisis comme des opérations DIVIDENDE, avec le **montant total reçu** dans le prix.
- La carte **Dividendes et coupons** de l'onglet [[Vue d'ensemble]] additionne ces montants, diminués des frais éventuellement saisis sur la même ligne. Son sous-titre « Montants bruts perçus » signifie que le logiciel ne déduit **aucun impôt** : le chiffre est celui que vous avez saisi.
- La colonne « Dividendes » du tableau des positions donne le total par ligne détenue.
- Les dividendes d'une ligne vendue depuis restent comptés dans le total.

Ils entrent dans la performance de deux façons : dans le gain total, et dans le TWR et le TRI, où un dividende est un flux d'argent qui revient vers vous. Un portefeuille qui distribue n'est donc pas désavantagé face à un ETF capitalisant.

### Les frais de courtage

La carte **Frais de courtage** (« Depuis l'origine ») additionne les frais de toutes les opérations : achats, ventes et dividendes. Ils sont toujours saisis **en euros**, même pour un titre en dollars.

Ils ne sont pas retirés une seconde fois : ils sont déjà pris en compte dans le PRU (achats), dans la plus-value réalisée (ventes) et dans le montant net des dividendes. Dans les rendements quotidiens, les frais d'un achat apparaissent le jour de l'opération, puisque l'argent sorti (frais compris) dépasse la valeur des titres reçus.

### Ce qui n'est pas compté

Le logiciel ne connaît que ce qui figure dans vos opérations : les droits de garde, les frais de tenue de compte, les impôts et prélèvements sociaux ne sont pas pris en compte s'ils ne sont pas saisis.

## Titres cotés en dollars ou en autre devise : comment sont-ils valorisés ?
<!-- fiche: analyse-titres-devises | questions: comment sont convertis mes titres en dollars ; ma performance en euros est différente de celle en dollars ; quel taux de change est utilisé ; mon action américaine a monté mais je perds de l'argent ; effet de change sur mon portefeuille ; le pru d'une action en dollars est en euros ; colonne devise du tableau des positions ; risque de change | mots: devise, taux de change, dollar, USD, conversion en euros, effet de change, risque de change, devise de cotation, EURUSD | aller: Analyse du portefeuille/Positions -->

Tous les calculs se font **en euros**. Un titre coté dans une autre devise est converti ainsi :

- chaque **opération** est convertie au taux de change de son jour (dernier taux connu à cette date) ;
- chaque **cours historique** est converti au taux du même jour ;
- le **cours actuel** est converti au taux du jour ; ce taux figure dans les informations en bas de la barre latérale (par exemple « 1 € en USD »).

`Prix en euros = prix en devise / taux (nombre d'unités de devise pour 1 €)`

Les actions de Londres, cotées en pence, sont d'abord divisées par 100. Les frais restent en euros.

### Deux effets dans la performance

La performance d'un titre étranger, vue en euros, combine la variation de son cours **et** celle de sa devise.

Exemple : vous achetez une action à 100 USD quand 1 € vaut 1,00 USD, soit 100 €. Un an plus tard, elle cote 110 USD (+10 %) mais 1 € vaut 1,10 USD : elle vaut `110 / 1,10 = 100 €`. En euros, le gain est nul.

### Où le voir

- Colonne « Devise » de l'onglet [[Positions]] : la devise de cotation. Le PRU, le cours, la valeur et les plus-values sont, eux, en euros.
- Onglet [[Transactions]] : les colonnes « Devise » et « Prix en devise » montrent le prix saisi avant conversion.
- Onglet [[Expositions]], sous-onglet [[Devises et taux]] : l'exposition réelle aux devises, ETF compris.

### Limite

Le taux utilisé est un taux de marché quotidien, pas celui réellement appliqué par votre courtier, qui y ajoute souvent une marge. Le détail de la conversion est expliqué dans le chapitre sur les sources et la fiabilité.

## Pourquoi mes chiffres diffèrent-ils de ceux de mon courtier ?
<!-- fiche: analyse-ecart-courtier | questions: pourquoi mes chiffres sont différents de ma banque ; mon courtier n'affiche pas la même plus-value ; le pru n'est pas le même que sur boursorama ; écart de valorisation avec mon relevé ; la valeur de mon portefeuille ne correspond pas à mon compte ; ma performance est différente de celle de mon assurance vie ; les chiffres sont ils faux | mots: écart, courtier, banque, relevé, différence, réconciliation, valorisation, PRU, taux de change, fiabilité | aller: Analyse du portefeuille/Positions | chiffres: valeur_actuelle, gain_total -->

Un écart avec votre courtier ne signale pas forcément une erreur. Voici les causes les plus fréquentes, dans l'ordre où les vérifier.

1. **Une opération manque ou est mal saisie.** Comparez l'onglet [[Transactions]] avec vos relevés : quantité, prix, frais, date. C'est la cause la plus courante.
2. **Le PRU inclut les frais d'achat.** Si votre courtier affiche un PRU hors frais, le sien est plus bas et sa plus-value plus haute.
3. **Le cours n'est pas pris au même moment.** Le logiciel utilise le dernier cours téléchargé lors de l'analyse, gardé en mémoire une heure ; votre courtier peut afficher un cours plus récent ou celui de la veille au soir.
4. **Le taux de change diffère.** Le logiciel convertit au taux de marché du jour ; votre courtier a appliqué son propre taux, avec sa marge.
5. **Les dividendes.** Le logiciel compte les montants saisis, sans impôt. Un courtier peut afficher des montants nets de prélèvements, ou ne pas les inclure dans la plus-value.
6. **La notion de performance.** Le TWR neutralise vos apports ; le rendement affiché par un courtier ou un assureur est souvent un autre calcul (gain rapporté aux versements, rendement de l'année…).
7. **Les frais non saisis** (droits de garde, frais de tenue de compte) ne sont pas connus du logiciel.

### Que faire

Corrigez les opérations erronées dans l'onglet [[Transactions]] (voir le chapitre sur l'import), puis cliquez sur [[Actualiser les cours]] pour repartir des cours les plus récents.

## Le tableau des positions, colonne par colonne
<!-- fiche: analyse-positions | questions: que veulent dire les colonnes du tableau des positions ; comment trier le tableau des positions ; c'est quoi la colonne poids ; la barre bleue dans la colonne poids ; pourquoi la région de mon etf est monde ; non classé dans la colonne secteur ; le cours est en euros ou en dollars ; tableau de mes lignes | mots: positions, tableau, colonnes, poids, PRU, cours, quantité, ticker, classe, secteur, région, tri | aller: Analyse du portefeuille/Positions | chiffres: nb_titres, valeur_actuelle -->

L'onglet [[Positions]] présente une ligne par titre **encore détenu**, de la plus grosse valeur à la plus petite. Cliquez sur un titre de colonne pour trier.

| Colonne | Contenu |
|---|---|
| Ticker | Le code Yahoo Finance du titre |
| Titre | Le nom |
| Classe | Actions, Obligations, Or… (un titre inconnu du référentiel est classé en actions) |
| Région, Secteur | Le classement de la ligne elle-même, sans éclatement des ETF ; « Non classé » si le titre n'est pas connu |
| Devise | La devise de cotation ; les montants des autres colonnes sont convertis en euros |
| Quantité | Le nombre de titres détenus |
| PRU | Prix de revient unitaire, frais d'achat compris, en euros |
| Cours | Le dernier cours, en euros |
| Valeur | Quantité × cours |
| +/- value, +/- value % | Plus-value latente en euros et en pourcentage du montant investi |
| Poids | Part de la ligne dans la valeur totale, avec une barre proportionnelle |
| Dividendes | Dividendes perçus sur cette ligne depuis l'origine |

### Le poids

`Poids = valeur de la ligne / valeur totale × 100`

La barre bleue est à pleine longueur pour la plus grosse ligne ; les autres sont proportionnelles. Exemple : une ligne de 15 000 € dans un portefeuille de 100 000 € pèse 15,0 %.

### Le graphique sous le tableau

**Plus-values latentes par ligne** : une barre horizontale par titre, verte pour un gain, rouge pour une perte, en euros, au dernier cours connu.

### Région et secteur différents de la vue d'ensemble ?

Le tableau classe un ETF monde en région « Monde » ; les anneaux de la vue d'ensemble et l'onglet [[Expositions]] le répartissent **en transparence** entre les pays de son indice. Les deux sont justes : ils répondent à deux questions différentes.

## Que contient l'onglet Performance ?
<!-- fiche: analyse-onglet-performance | questions: que contient l'onglet performance ; comment savoir si je bats l'indice ; à quoi sert le graphique base 100 ; que veut dire l'avertissement sur l'indice obligataire ; les cinq cartes en bas de l'onglet performance ; comment lire l'onglet performance ; ou voir mes performances par année | mots: performance, TWR, TRI, indice de référence, base 100, rendement annuel, drawdown, bêta, alpha, comparaison | aller: Analyse du portefeuille/Performance | chiffres: twr_total, twr_annualise, tri_annuel -->

L'onglet [[Performance]] répond à deux questions : combien avez-vous gagné, et avez-vous fait mieux que l'indice de référence ?

### De haut en bas

1. **Quatre cartes** : TWR total (« Depuis le » + date de début), TWR annualisé (« Base 365 jours »), TRI annuel (« Rendement de l'argent investi ») et Écart avec l'indice (pastille « surperformance » ou « sous-performance »).
2. **Portefeuille et indice** : les deux courbes en base 100 à la première date commune.
3. **Rendement par année civile** : le TWR de chaque année, portefeuille et indice côte à côte.
4. **Drawdown** : la baisse depuis le dernier plus haut, avec, dans le sous-titre, les dates du plus haut, du plus bas et du retour au plus haut.
5. **Cinq cartes** de comparaison avec l'indice : Bêta, Alpha de Jensen, Corrélation, Tracking error et Ratio d'information.

### L'avertissement orange

Si l'indice choisi dans [[Indice de référence]] est obligataire ou monétaire, un encadré rappelle que le bêta, l'alpha et la corrélation mesurent la sensibilité à un marché d'actions : face à un tel indice, ils ont peu de sens. Comparez alors surtout les rendements et les volatilités.

### Ordre de lecture conseillé

Commencez par le TWR annualisé et l'écart avec l'indice, regardez la courbe pour voir **quand** l'écart s'est creusé, puis le drawdown pour mesurer la pire épreuve traversée. Les fiches suivantes détaillent chaque indicateur.

## Les rendements quotidiens « neutres aux apports »
<!-- fiche: analyse-rendements-quotidiens | questions: comment sont calculés les rendements quotidiens ; pourquoi un achat ne compte pas comme un gain ; neutraliser les apports ça veut dire quoi ; mon versement fait monter la courbe mais pas la performance ; rendement du premier jour négatif pourquoi ; base de calcul des indicateurs ; rendement journalier | mots: rendement quotidien, rendement journalier, flux, apports, retraits, neutralisation, base 100, fin de journée | aller: Analyse du portefeuille/Performance -->

Presque tous les indicateurs (TWR, volatilité, Sharpe, VaR, bêta…) reposent sur une série : le rendement de chaque jour de bourse, **sans l'effet de vos apports et retraits**.

### Le problème

Si vous achetez pour 1 000 € aujourd'hui, la valeur du portefeuille monte de 1 000 €, mais vous n'avez rien gagné. Il faut retirer l'effet de cet argent.

### La formule du logiciel

```
r(t) = (valeur(t) − flux(t)) / valeur(t−1) − 1
```

avec `flux(t)` = argent apporté ce jour-là (positif pour un achat, négatif pour une vente ou un dividende). Les opérations sont supposées faites **en fin de journée**, au cours du jour : l'argent apporté aujourd'hui n'a pas encore « travaillé ».

**Premier jour** (ou reprise après avoir tout vendu) : la veille valait 0, le logiciel compare la valeur en fin de journée à l'argent apporté : `r = valeur(t) / flux(t) − 1`. Ce rendement capte les frais d'achat et l'écart entre le prix payé et le cours de clôture : il est souvent légèrement négatif.

Les jours où rien n'était investi ne sont pas comptés.

### Exemple

Le portefeuille valait 10 000 € hier soir. Vous achetez pour 1 000 € aujourd'hui, et il vaut 11 150 € ce soir.
`r = (11 150 − 1 000) / 10 000 − 1 = +1,50 %`.
Sans neutralisation, on aurait lu +11,5 %.

### La courbe base 100

En enchaînant ces rendements, on obtient un indice qui part de 100 : `indice(t) = 100 × (1 + r1) × (1 + r2) × … × (1 + rt)`. C'est la « performance pure » de vos choix, comparable à un indice boursier ; le drawdown est calculé sur elle.

### Limite

Les opérations sont rattachées à un jour de bourse et supposées faites au cours de clôture. Un achat réalisé en séance à un cours différent crée un petit écart le jour même.

## Le TWR (rendement pondéré par le temps) et son annualisation
<!-- fiche: analyse-twr | questions: c'est quoi le twr ; comment est calculée la performance annualisée ; time weighted return ; pourquoi ma perf annualisée est énorme alors que j'ai commencé il y a 3 mois ; twr total et twr annualisé quelle différence ; pourquoi 365 jours et pas 252 ; performance de mon portefeuille hors versements | mots: TWR, time-weighted return, rendement pondéré par le temps, performance, annualisation, base 365, GIPS, rendement composé | aller: Analyse du portefeuille/Performance | chiffres: twr_total, twr_annualise -->

### Le TWR total

`TWR = (1 + r1) × (1 + r2) × … × (1 + rn) − 1`

où les `r` sont les rendements quotidiens neutres aux apports. Le TWR mesure la **qualité des choix d'investissement**, indépendamment du moment et du montant de vos versements. C'est la mesure des gérants de fonds (norme GIPS) : un gérant ne décide pas quand ses clients déposent de l'argent.

Exemple : +10 % puis −5 % donnent `1,10 × 0,95 − 1 = +4,50 %`, et non +5 %.

### Le TWR annualisé

`TWR annualisé = (1 + TWR total) ^ (365 / nombre de jours) − 1`

Le nombre de jours est calendaire, entre le premier et le dernier jour de la série de rendements. Exemples :

- +21 % en 730 jours : `1,21 ^ (1/2) − 1 = +10,00 %` par an (et non 10,5 % : les gains se composent) ;
- +4,50 % en 200 jours : `1,045 ^ (365/200) − 1 = +8,36 %` par an.

Pourquoi 365 et non 252 ? Le rendement s'annualise en jours **calendaires** ; 252 jours de bourse servent seulement à annualiser la volatilité.

### Où le voir

Cartes « TWR total » et « TWR annualisé » de l'onglet [[Performance]] ; le TWR annualisé est aussi la carte « Perf. annualisée » des chiffres clés.

### Limites

- **Période courte** : l'annualisation amplifie tout. +5 % en 91 jours donne `1,05 ^ (365/91) − 1 ≈ +21,6 %` par an, ce qui ne veut pas dire que l'année fera +21,6 %. En dessous d'un an, regardez plutôt le TWR total.
- Le TWR ignore votre argent réel : un excellent TWR sur une petite somme peut coexister avec une perte en euros si vous avez beaucoup investi juste avant une baisse. C'est le rôle du TRI.

## Le TRI (taux de rendement interne)
<!-- fiche: analyse-tri | questions: c'est quoi le tri ; comment est calculé le taux de rendement interne ; irr money weighted return ; rendement de l'argent investi ; pourquoi mon tri est négatif ; tri non disponible ; le tri tient il compte des dates de mes versements ; xirr comme dans excel | mots: TRI, taux de rendement interne, IRR, XIRR, money-weighted return, rendement de l'argent investi, actualisation, flux | aller: Analyse du portefeuille/Performance | chiffres: tri_annuel -->

Le TRI est le rendement annuel **de votre argent**, tel que vous l'avez vécu, en tenant compte des dates et des montants de vos versements.

### La formule

Le TRI est le taux annuel `i` qui annule la valeur actualisée de tous les flux :

```
Σ CF_k / (1 + i) ^ (jours_k / 365) = 0
```

Du point de vue de l'investisseur :

- un achat est de l'argent qui **sort** de votre poche : flux négatif (frais compris) ;
- une vente ou un dividende est de l'argent qui **entre** : flux positif ;
- le dernier jour, le logiciel fait comme si vous vendiez tout : `+ valeur finale`.

`jours_k` est le nombre de jours entre le premier flux et le flux k ; les flux d'un même jour sont additionnés.

### Le calcul

Il n'existe pas de formule directe. Le logiciel cherche `i` par **dichotomie** entre −99 % et +1 000 % par an, en coupant l'intervalle en deux 200 fois. S'il n'existe pas de solution dans cet intervalle, le TRI n'est pas calculé. C'est le même principe que la fonction TRI.PAIEMENTS (XIRR) d'un tableur.

### Exemple

Vous investissez 1 000 € le 02/01/2023 ; un an plus tard, ils valent 1 200 € et vous ajoutez 10 000 €. L'année suivante, le portefeuille baisse de 10 % et vaut 10 080 € le 01/01/2025.
Flux : −1 000 € (jour 0), −10 000 € (jour 365), +10 080 € (jour 730). Le TRI vaut **−7,72 % par an** : vous avez perdu de l'argent, car la plus grosse somme a subi la baisse.

### Où le voir

Carte « TRI annuel » de l'onglet [[Performance]].

### Limites

Le TRI dépend de votre calendrier de versements : il ne permet pas de juger un gérant ni de se comparer à un indice. Sur une période très courte, il peut prendre des valeurs extrêmes.

## Pourquoi le TWR et le TRI sont-ils différents ?
<!-- fiche: analyse-twr-tri | questions: pourquoi le twr et le tri sont différents ; twr positif et tri négatif c'est possible ; quel chiffre croire twr ou tri ; ma performance est bonne mais j'ai perdu de l'argent ; différence entre rendement pondéré par le temps et par l'argent ; lequel comparer à l'indice ; tri plus élevé que le twr pourquoi | mots: TWR, TRI, différence, time-weighted, money-weighted, calendrier des apports, timing, comparaison, versements | aller: Analyse du portefeuille/Performance | chiffres: twr_annualise, tri_annuel -->

Les deux indicateurs répondent à deux questions différentes.

| | TWR | TRI |
|---|---|---|
| Question | Mes choix de placement étaient-ils bons ? | Combien mon argent a-t-il rapporté ? |
| Effet des versements | Neutralisé | Pris en compte (montants et dates) |
| Sert à | Se comparer à un indice ou à un fonds | Mesurer votre résultat personnel |

### Exemple : TWR positif, TRI négatif

- Année 1 : 1 000 € investis, +20 % : ils valent 1 200 €.
- Début de l'année 2 : vous ajoutez 10 000 €. Le portefeuille vaut 11 200 €.
- Année 2 : −10 % : il vaut 10 080 €.

**TWR** : `1,20 × 0,90 − 1 = +8,00 %` sur deux ans. Vos placements ont, en moyenne, bien travaillé.
**TRI** : −7,72 % par an. Vous avez apporté 11 000 € et il en reste 10 080 € : la mauvaise année a frappé le gros versement, la bonne n'a profité qu'au petit.

### Lire l'écart

- **TRI > TWR** : vous avez investi davantage avant les périodes de hausse (bon timing, ou chance).
- **TRI < TWR** : vous avez investi davantage avant les baisses.
- **TRI ≈ TWR** : peu de versements, ou des versements réguliers sans effet de calendrier marqué.

Attention : le TRI est déjà annuel, alors que le TWR existe en version totale et annualisée. Comparez le TRI au **TWR annualisé**.

### Lequel croire ?

Les deux sont justes. Pour vous comparer à l'indice, utilisez le TWR, comme le fait la carte « Écart avec » l'indice. Pour savoir ce que votre épargne a réellement rapporté, regardez le TRI et le gain total.

## Comparer son portefeuille à l'indice (base 100 et écart)
<!-- fiche: analyse-comparaison-indice | questions: comment savoir si je bats le marché ; graphique portefeuille contre indice ; c'est quoi la base 100 ; comment est calculé l'écart avec le msci world ; surperformance ou sous-performance ; les deux courbes ne partent pas du même jour ; l'écart avec l'indice ne correspond pas à la différence des twr annualisés | mots: comparaison, indice de référence, benchmark, base 100, surperformance, sous-performance, écart, MSCI World, courbe | aller: Analyse du portefeuille/Performance | chiffres: twr_total -->

### Le graphique « Portefeuille et indice »

Deux courbes partent de 100 à la **première date commune** : « Mon portefeuille » (bleue) et l'indice choisi (grise). Une ligne pointillée marque le niveau 100. Si votre courbe finit à 130 et celle de l'indice à 125, votre portefeuille a fait +30 % et l'indice +25 % sur la période.

La courbe du portefeuille enchaîne les rendements quotidiens neutres aux apports : vos versements ne la font pas sauter. Les boutons 1M, 6M, YTD, 1A et Tout choisissent la période affichée, mais les deux courbes restent en base 100 au début de l'historique.

### La carte « Écart avec » l'indice

`Écart = TWR du portefeuille − TWR de l'indice, sur la même période`

Les deux TWR sont **totaux** (non annualisés) et calculés sur les seuls jours où les deux rendements existent. Le tout premier jour d'investissement, qui n'a pas de rendement d'indice correspondant, en est exclu : le TWR utilisé peut donc différer légèrement du TWR total affiché à côté. La pastille indique « surperformance » si l'écart est positif ou nul, « sous-performance » sinon.

Exemple : portefeuille +30,0 %, indice +25,0 % : écart **+5,00 %**.

### Une comparaison équitable

- Choisissez un indice qui ressemble au portefeuille (un indice mixte pour un portefeuille actions et obligations).
- Les indices « hors dividendes » (CAC 40, Euro Stoxx 50) désavantagent l'indice, puisque vos dividendes, eux, sont comptés.
- L'indice est converti en euros, comme le portefeuille.

### Limite

Un écart sur une courte période est souvent dû au hasard. Regardez aussi les rendements par année civile et le ratio d'information.

## Le rendement par année civile
<!-- fiche: analyse-rendements-annuels | questions: performance par année ; rendement de mon portefeuille en 2025 ; pourquoi la première année est faible ; l'année en cours est elle complète ; comparer chaque année à l'indice ; graphique en barres des années ; performance annuelle | mots: rendement annuel, année civile, performance par année, YTD, barres, comparaison annuelle, calendrier | aller: Analyse du portefeuille/Performance -->

Le graphique **Rendement par année civile** de l'onglet [[Performance]] montre, pour chaque année, le TWR du portefeuille (barres bleues, « Mon portefeuille ») et celui de l'indice (barres grises).

### Le calcul

Les rendements quotidiens sont regroupés par année civile, puis composés :

`Rendement de l'année = Π (1 + r_jour) − 1, sur les jours de l'année`

Exemple : une année avec un premier semestre à +6 % et un second à −2 % donne `1,06 × 0,98 − 1 = +3,88 %`.

### À savoir

- La **première année** ne commence qu'à votre premier investissement : elle est partielle.
- L'**année en cours** va du 1er janvier à la dernière date de cours : c'est un rendement depuis le début de l'année, pas une année complète.
- Les barres ne sont pas annualisées.
- Le survol donne le rendement avec deux décimales.

### Comment le lire

Une surperformance régulière, année après année, est plus convaincante qu'une seule excellente année. Une année très différente de l'indice dans les deux sens signale un portefeuille éloigné de sa référence : la tracking error le confirme.

## Le max drawdown (pire baisse)
<!-- fiche: analyse-drawdown | questions: c'est quoi le max drawdown ; pire baisse de mon portefeuille ; plus haut non retrouvé ça veut dire quoi ; comment lire le graphique rouge du drawdown ; combien de temps pour récupérer ; perte maximale depuis un sommet ; drawdown calculé sur la valeur ou sur la performance | mots: drawdown, max drawdown, perte maximale, baisse depuis un plus haut, creux, sommet, récupération, recovery | aller: Analyse du portefeuille/Performance | chiffres: max_drawdown -->

Le drawdown mesure, chaque jour, la baisse par rapport au plus haut atteint jusque-là. Le max drawdown est la pire de ces baisses.

### Formules

```
drawdown(t) = indice(t) / plus haut de l'indice jusqu'à t − 1   (toujours ≤ 0)
max drawdown = le plus petit drawdown de la période
```

Le calcul se fait sur la **courbe base 100** (performance neutre aux apports), et non sur la valeur en euros : sinon un retrait ressemblerait à une perte, et un apport masquerait une vraie baisse.

### Exemple

La courbe passe par 100, 120, 90, 110, puis 130. Le plus haut avant la chute est 120 ; le creux est 90. Max drawdown : `90 / 120 − 1 = −25,00 %`. Le plus haut est retrouvé quand la courbe revient à 120 ou plus : ici, au point 130 (110 ne suffit pas).

### Lire le graphique

Dans l'onglet [[Performance]], la zone rouge montre le drawdown jour par jour ; un point marque le plus bas, avec l'étiquette « Max drawdown ». Le sous-titre donne la date du plus haut, celle du plus bas, puis « retrouvé le » et la date du retour au plus haut, ou « plus haut non retrouvé ». La carte « Max drawdown » des chiffres clés affiche la date du creux.

### Interprétation

C'est l'indicateur de risque le plus parlant : « au pire moment, j'aurais perdu 25 % depuis le sommet ». Une baisse de 25 % demande une hausse de `1 / 0,75 − 1 = 33,3 %` pour être effacée.

### Limites

Il dépend de la période observée : un historique de deux ans peut n'avoir connu aucune vraie crise. Il ne dit pas combien de fois ni combien de temps vous avez été en baisse.

## Le bêta et la corrélation avec l'indice
<!-- fiche: analyse-beta | questions: c'est quoi le bêta ; mon bêta est de 1,2 qu'est ce que ça veut dire ; bêta inférieur à 1 ; comment est calculé le bêta ; corrélation avec l'indice c'est quoi ; mon portefeuille est il défensif ; bêta négatif possible ; sensibilité au marché | mots: bêta, beta, sensibilité au marché, corrélation, MEDAF, CAPM, risque systématique, défensif, agressif | aller: Analyse du portefeuille/Performance | chiffres: beta -->

### Le bêta

`Bêta = covariance(rendements du portefeuille, rendements de l'indice) / variance(rendements de l'indice)`

Il est calculé sur les rendements quotidiens des jours communs au portefeuille et à l'indice.

**Intuition** : quand l'indice fait +1 %, le portefeuille fait en moyenne `bêta × 1 %`.

| Bêta | Lecture |
|---|---|
| 1 | Le portefeuille bouge comme l'indice (« 1 = comme l'indice ») |
| 1,2 | Il amplifie les mouvements : +1,2 % quand l'indice fait +1 %, et inversement à la baisse |
| 0,8 | Plus défensif que l'indice |
| Proche de 0 | Peu lié à l'indice |

**Exemple** : sur cinq jours, l'indice fait +1 %, −1 %, +2 %, −2 %, 0 % et le portefeuille +1,2 %, −1,1 %, +2,5 %, −2,4 %, +0,1 %. Covariance 0,0003025, variance de l'indice 0,00025 : bêta = `0,0003025 / 0,00025 = 1,21`.

### La corrélation

La carte « Corrélation » (« Avec » l'indice) mesure, entre −1 et +1, à quel point les deux évoluent **dans le même sens**, sans tenir compte de l'ampleur. Une corrélation de 0,95 signifie que l'indice explique presque tous les mouvements du portefeuille ; 0,5, qu'une grande partie de ses mouvements lui est propre.

`Bêta = corrélation × volatilité du portefeuille / volatilité de l'indice`

Exemple : corrélation 0,9, volatilité 18 % contre 15 % pour l'indice : bêta `0,9 × 18 / 15 = 1,08`.

### Limites

- Le bêta n'a de sens que face à un indice qui ressemble au portefeuille ; avec un indice obligataire ou monétaire, un avertissement s'affiche.
- Avec une corrélation faible, le bêta explique peu de chose.
- Il est estimé sur le passé et change avec le temps.

## L'alpha de Jensen
<!-- fiche: analyse-alpha | questions: c'est quoi l'alpha ; alpha de jensen comment le calculer ; mon alpha est négatif est ce grave ; alpha positif ça veut dire que je bats le marché ; différence entre alpha et écart avec l'indice ; création de valeur par le choix des titres ; medaf alpha | mots: alpha, alpha de Jensen, MEDAF, CAPM, surperformance ajustée du risque, sélection de titres, rendement excédentaire | aller: Analyse du portefeuille/Performance | chiffres: alpha, beta -->

L'alpha mesure la performance qui **ne s'explique pas** par l'exposition au marché (modèle du MEDAF).

### La formule du logiciel

```
alpha quotidien = moyenne(r_portefeuille − rf) − bêta × moyenne(r_indice − rf)
alpha annuel    = alpha quotidien × 252
```

`rf` est le taux sans risque journalier : `(1 + taux annuel) ^ (1/252) − 1`, soit environ 0,0098 % par jour avec 2,50 % par an. Les moyennes sont arithmétiques, sur les jours communs au portefeuille et à l'indice.

### Intuition

Un portefeuille de bêta 1,1 « devrait » faire 1,1 fois le rendement excédentaire de l'indice. L'alpha est ce qu'il a fait en plus (ou en moins).

### Exemple

Rendement excédentaire moyen annualisé du portefeuille : 8 % ; de l'indice : 6 % ; bêta : 1,1.
`Alpha = 8 % − 1,1 × 6 % = +1,40 %` par an.

### Lecture

- **Alpha > 0** (pastille verte « annuel ») : vos choix ont créé de la valeur au-delà du risque de marché pris.
- **Alpha < 0** : à risque de marché égal, l'indice a fait mieux.

L'alpha diffère de l'écart avec l'indice : un portefeuille de bêta 1,3 qui bat l'indice en période de hausse peut avoir un alpha nul, car il n'a fait que prendre plus de risque.

### Limites

- Le taux sans risque est supposé constant sur toute la période.
- Sur moins de deux ou trois ans, l'alpha est très instable.
- Il n'a de sens que face à un indice d'actions comparable au portefeuille.

## La tracking error et le ratio d'information
<!-- fiche: analyse-tracking-error | questions: c'est quoi la tracking error ; mon portefeuille colle t il à l'indice ; ratio d'information c'est quoi ; comment calculer la tracking error ; gestion passive ou active ; tracking error de 5 % c'est beaucoup ; un bon ratio d'information ; écart de suivi | mots: tracking error, écart de suivi, ratio d'information, information ratio, gestion active, gestion passive, risque relatif, écart à l'indice | aller: Analyse du portefeuille/Performance | chiffres: tracking_error -->

### La tracking error

`Tracking error = écart-type(r_portefeuille − r_indice) × √252`

C'est la volatilité de **l'écart** de rendement quotidien avec l'indice, ramenée à l'année (carte « Tracking error », « Annualisée »).

| Tracking error | Lecture |
|---|---|
| Moins de 2 % | Le portefeuille colle à l'indice (gestion passive) |
| Plus de 5 % | Gestion très différente de l'indice |

### Le ratio d'information

`Ratio d'information = moyenne(r_portefeuille − r_indice) × 252 / tracking error`

Il répond à la question : l'écart avec l'indice a-t-il été « payé » ? C'est l'équivalent du ratio de Sharpe, mais par rapport à l'indice. Un ratio supérieur à 0,5 est considéré comme bon.

### Exemple

Écart quotidien moyen de 0,004 % et écart-type de l'écart de 0,30 % :

- tracking error : `0,30 % × √252 = 4,76 %` ;
- ratio d'information : `0,004 % × 252 / 4,76 % = 1,008 % / 4,76 % = 0,21`.

Le portefeuille s'écarte nettement de l'indice, mais cet écart n'a rapporté que peu.

### À savoir

La moyenne utilisée par le ratio d'information est **arithmétique** (moyenne quotidienne × 252). Elle ne coïncide donc pas exactement avec la carte « Écart avec » l'indice, qui compare des TWR composés et non annualisés.

### Limites

Mêmes réserves que pour le bêta : choisissez un indice comparable, et méfiez-vous des périodes courtes.

## Que contient l'onglet Risque ?
<!-- fiche: analyse-onglet-risque | questions: que contient l'onglet risque ; comment lire l'onglet risque ; ou est la var ; ou sont passées les corrélations ; que veut dire n.d. dans le tableau des var ; à quoi sert le tableau perte d'un mauvais jour ; les phrases sous le graphique de distribution | mots: risque, VaR, CVaR, Sharpe, Sortino, distribution, asymétrie, kurtosis, Jarque-Bera, perte d'un mauvais jour | aller: Analyse du portefeuille/Risque | chiffres: sharpe, sortino, var_historique, cvar -->

L'onglet [[Risque]] mesure le risque pris et la forme des mauvaises journées.

### En haut : quatre cartes

| Carte | Ligne du dessous |
|---|---|
| Ratio de Sharpe | Sharpe de l'indice de référence |
| Ratio de Sortino | « Ne pénalise que les baisses » |
| VaR (niveau choisi) · 1 jour, en euros | La même VaR en %, « méthode historique » |
| CVaR · Expected Shortfall, en euros | La CVaR en %, « au-delà de la VaR » |

### Au centre : la distribution des rendements quotidiens

- À gauche, l'histogramme des rendements quotidiens, la courbe de la loi normale et les lignes des VaR (fiche dédiée). Le sous-titre indique le nombre de jours utilisés.
- À droite, quatre cartes : Asymétrie, Kurtosis en excès, Jours à plus de 3 écarts-types et Test de Jarque-Bera ; puis le tableau **Perte d'un mauvais jour**, avec la VaR historique, la VaR loi normale, la VaR Cornish-Fisher et la CVaR, en % et en euros.
- « n.d. » (non disponible) signifie que la VaR Cornish-Fisher n'a pas été calculée, car l'asymétrie ou la kurtosis sont trop fortes : une note l'explique sous le tableau.

### En bas : la lecture automatique

Quelques phrases interprètent la distribution : asymétrie, queues épaisses, résultat du test de Jarque-Bera et comparaison des VaR historique et normale. Une dernière note rappelle que les corrélations et la diversification se trouvent dans l'onglet [[Expositions]].

### Le réglage qui compte

Le niveau des VaR et de la CVaR se règle dans **Paramètres**, avec le curseur [[Niveau de confiance de la VaR]] (90, 95 ou 99 %).

## La volatilité
<!-- fiche: analyse-volatilite | questions: c'est quoi la volatilité ; comment est calculée la volatilité annualisée ; pourquoi racine de 252 ; ma volatilité est de 15 % c'est beaucoup ; volatilité de l'indice sous la carte ; écart type des rendements ; mon portefeuille est il risqué | mots: volatilité, écart-type, risque, √252, annualisation, dispersion, standard deviation, variabilité | aller: Analyse du portefeuille/Risque | chiffres: volatilite -->

### La formule

`Volatilité annuelle = écart-type des rendements quotidiens × √252`

L'écart-type est celui de l'échantillon (division par n − 1), calculé sur les rendements quotidiens neutres aux apports.

### Pourquoi √252

On compte 252 jours de bourse par an. Si les rendements quotidiens sont indépendants, leurs variances s'additionnent : `variance annuelle = 252 × variance quotidienne`, donc `écart-type annuel = √252 × écart-type quotidien`.

### Exemple

Un écart-type quotidien de 1,00 % donne `1 % × √252 = 1 % × 15,87 = 15,87 %` par an.

### Interprétation

Avec une volatilité de 15 %, le rendement d'une année s'écarte « typiquement » de ± 15 % de sa moyenne. Le plus utile est la comparaison avec l'indice de référence, dont la volatilité est affichée sous la carte Volatilité des chiffres clés.

### Limites

- La volatilité compte les hausses comme du risque, au même titre que les baisses (le ratio de Sortino corrige ce défaut).
- La règle √252 suppose des rendements indépendants d'un jour à l'autre.
- Elle décrit les écarts habituels, pas les krachs : pour les pertes extrêmes, voyez la VaR, la CVaR et le max drawdown.

## Le ratio de Sharpe
<!-- fiche: analyse-sharpe | questions: c'est quoi le ratio de sharpe ; que veut dire le ratio de sharpe ; un bon sharpe c'est combien ; mon sharpe est négatif ; comment est calculé le sharpe ; pourquoi mon sharpe change quand je modifie le taux sans risque ; sharpe de l'indice sous la carte ; rendement par unité de risque | mots: Sharpe, ratio de Sharpe, rendement ajusté du risque, taux sans risque, excès de rendement, volatilité, rentabilité du risque | aller: Analyse du portefeuille/Risque | chiffres: sharpe, volatilite -->

Le ratio de Sharpe répond à la question : **le risque pris a-t-il été bien payé ?**

### La formule du logiciel

```
excédent quotidien = r_jour − rf_jour,   avec rf_jour = (1 + taux sans risque) ^ (1/252) − 1
Sharpe = moyenne(excédent) × 252 / (écart-type(excédent) × √252)
```

Le rendement est la moyenne **arithmétique** des rendements quotidiens, annualisée par 252 ; ce n'est pas le TWR annualisé. Le taux sans risque est celui du panneau **Paramètres** (2,50 % par défaut).

### Exemple

Rendement quotidien moyen de 0,040 %, écart-type quotidien de 1,00 %, taux sans risque de 2,50 % (soit 0,0098 % par jour) :

- excédent annualisé : `(0,040 % − 0,0098 %) × 252 = 7,61 %` ;
- volatilité : `1 % × √252 = 15,87 %` ;
- Sharpe : `7,61 / 15,87 = 0,48`.

### Ordres de grandeur

| Sharpe | Lecture |
|---|---|
| Moins de 0 | Le portefeuille a fait moins bien qu'un placement sans risque |
| Autour de 0,5 | Correct |
| Plus de 1 | Très bon |

Comparez surtout au Sharpe de l'indice, affiché sous la carte.

### Limites

- Il pénalise autant les fortes hausses que les fortes baisses (voir le Sortino).
- Il suppose un taux sans risque constant sur toute la période.
- Sur une période courte, il varie beaucoup ; une hausse du taux sans risque le fait baisser.

## Le ratio de Sortino
<!-- fiche: analyse-sortino | questions: c'est quoi le ratio de sortino ; différence entre sharpe et sortino ; pourquoi mon sortino est plus élevé que mon sharpe ; semi déviation c'est quoi ; ratio qui ne pénalise que les baisses ; comment est calculé le sortino ; downside deviation | mots: Sortino, semi-déviation, downside deviation, risque de baisse, Sharpe, rendement ajusté, volatilité négative | aller: Analyse du portefeuille/Risque | chiffres: sortino, sharpe -->

Le ratio de Sortino est un Sharpe qui **ne pénalise que les baisses** : un investisseur ne se plaint pas des fortes hausses.

### La formule du logiciel

```
excédent = r_jour − rf_jour
semi-déviation = √( moyenne( min(excédent, 0)² ) ) × √252
Sortino = moyenne(excédent) × 252 / semi-déviation
```

Les jours au-dessus du taux sans risque sont remplacés par 0, puis la moyenne des carrés est prise sur **tous** les jours.

### Exemple (taux sans risque à 0 % pour simplifier)

Six jours : +1,2 %, −2,0 %, +0,6 %, −0,8 %, +1,5 %, +0,3 %.

- moyenne : 0,1333 % par jour, soit `33,60 %` annualisés ;
- volatilité : 20,91 %, donc Sharpe = `33,60 / 20,91 = 1,61` ;
- semi-déviation : `√((0,020² + 0,008²) / 6) = 0,879 %` par jour, soit `13,96 %` annualisés ;
- Sortino : `33,60 / 13,96 = 2,41`.

Le Sortino est plus élevé que le Sharpe : une partie de la volatilité venait des hausses.

### Lecture

- Sortino nettement supérieur au Sharpe : les écarts du portefeuille sont surtout des hausses.
- Sortino proche du Sharpe : baisses et hausses ont une ampleur comparable.

### Limites

Avec peu de jours de baisse, la semi-déviation repose sur peu d'observations et le ratio devient instable. Il hérite aussi des limites du Sharpe (taux sans risque constant, période observée).

## La VaR historique (et la VaR en euros)
<!-- fiche: analyse-var-historique | questions: c'est quoi la var ; value at risk historique comment ça marche ; que veut dire var 95 % 1 jour ; combien je peux perdre en une journée ; var en euros comment est elle calculée ; la var est elle une perte maximale ; pourquoi ma var a changé ; var à 99 % | mots: VaR, value at risk, VaR historique, perte d'un mauvais jour, quantile, percentile, niveau de confiance, risque de perte | aller: Analyse du portefeuille/Risque | chiffres: var_historique, valeur_actuelle -->

La VaR (Value at Risk) répond à : **combien puis-je perdre lors d'un mauvais jour ?**

### La formule

`VaR historique = − quantile des rendements quotidiens au seuil (1 − niveau)`

À 95 %, c'est le 5e centile des rendements passés, changé de signe pour être lu comme une perte. Aucune hypothèse sur la forme de la distribution : le logiciel prend les jours réels.

`VaR en euros = VaR historique × valeur actuelle du portefeuille`

### Exemple

Sur 1 000 jours, le 5e centile se situe entre la 50e et la 51e plus mauvaise journée. S'il vaut −1,60 %, la VaR historique à 95 % est de 1,60 %. Pour un portefeuille de 100 000 €, la carte affiche **1 600 €**.

Lecture : « dans 95 % des jours, la perte ne dépasse pas 1 600 € » ; autrement dit, environ un jour de bourse sur vingt, soit à peu près une fois par mois, la perte est plus forte.

### Où la voir

- Carte « VaR (niveau) · 1 jour » de l'onglet [[Risque]] : le montant en euros, et la pastille en % « méthode historique ».
- Ligne « VaR historique » du tableau **Perte d'un mauvais jour**.
- Ligne orange en tirets du graphique de distribution.

### Ce que la VaR n'est pas

Ce n'est **pas** une perte maximale : elle dit où commence la zone des mauvais jours, pas jusqu'où elle va. Pour cela, regardez la CVaR.

### Limites

- Elle suppose que le passé se répète : un historique calme donne une VaR faible.
- À 99 %, elle repose sur 1 % des jours, soit très peu d'observations sur un historique court.
- C'est une VaR à **un jour**, calculée sur la valeur actuelle.

## La VaR « loi normale » (paramétrique)
<!-- fiche: analyse-var-normale | questions: c'est quoi la var paramétrique ; var gaussienne ; var loi normale comment est elle calculée ; pourquoi 1,645 ; différence entre var historique et var normale ; la loi normale sous estime t elle les krachs ; var variance covariance | mots: VaR paramétrique, VaR gaussienne, loi normale, 1,645, quantile, écart-type, moyenne, variance-covariance | aller: Analyse du portefeuille/Risque | chiffres: var_parametrique, var_historique -->

### La formule

`VaR loi normale = −(moyenne des rendements quotidiens + z × écart-type)`

où `z` est le quantile de la loi normale au seuil `1 − niveau` :

| Niveau | z |
|---|---|
| 90 % | −1,2816 |
| 95 % | −1,6449 |
| 99 % | −2,3263 |

### Intuition

On suppose que les rendements quotidiens suivent une loi normale (une « courbe en cloche ») de même moyenne et de même écart-type que les vôtres, et on lit la perte au seuil voulu.

### Exemple

Moyenne quotidienne 0,04 %, écart-type 1,00 % :

- à 95 % : `−(0,04 % − 1,6449 × 1 %) = 1,60 %` ;
- à 99 % : `−(0,04 % − 2,3263 × 1 %) = 2,29 %` ;
- à 90 % : `1,24 %`.

### Lecture

C'est la méthode la plus simple, et elle se calcule même avec peu de données. Mais les vrais rendements ont des **queues épaisses** : les fortes baisses sont plus fréquentes que ne le prévoit la loi normale. À 99 %, la VaR normale sous-estime donc souvent le risque.

Le logiciel compare automatiquement les deux méthodes : si la VaR historique dépasse la VaR normale de plus de 5 %, la lecture sous le graphique l'indique (« la loi normale sous-estime ici la perte d'un mauvais jour »).

### Limites

- L'hypothèse de normalité est presque toujours rejetée par le test de Jarque-Bera sur des données de marché.
- La VaR Cornish-Fisher corrige en partie ce défaut.

## La VaR Cornish-Fisher et son domaine de validité
<!-- fiche: analyse-var-cornish-fisher | questions: c'est quoi la var cornish fisher ; pourquoi la var cornish fisher est n.d. ; var corrigée de l'asymétrie et de la kurtosis ; asymétrie ou kurtosis trop fortes la correction n'est plus fiable ; cornish fisher plus faible que la var normale pourquoi ; var modifiée ; méthode priips | mots: Cornish-Fisher, VaR modifiée, VaR corrigée, asymétrie, kurtosis, PRIIPs, n.d., domaine de validité, quantile ajusté | aller: Analyse du portefeuille/Risque | chiffres: var_cornish_fisher, asymetrie, kurtosis -->

La VaR Cornish-Fisher garde la formule de la loi normale, mais **corrige le quantile z** avec l'asymétrie S et la kurtosis en excès K des rendements.

### La formule

```
z_cf = z + (z² − 1) × S/6 + (z³ − 3z) × K/24 − (2z³ − 5z) × S²/36
VaR Cornish-Fisher = −(moyenne + z_cf × écart-type)
```

C'est la méthode retenue pour l'indicateur de risque réglementaire des produits d'investissement (PRIIPs).

### Exemples (moyenne 0,04 %, écart-type 1 %)

| Niveau | S | K | z_cf | VaR Cornish-Fisher | VaR normale |
|---|---|---|---|---|---|
| 95 % | −0,5 | 3 | −1,7217 | 1,68 % | 1,60 % |
| 95 % | 0 | 3 | −1,5843 | 1,54 % | 1,60 % |
| 99 % | −0,5 | 3 | −3,3013 | 3,26 % | 2,29 % |
| 99 % | 0 | 3 | −3,0277 | 2,99 % | 2,29 % |

### Lecture

- Une **asymétrie négative** rend toujours la VaR plus prudente.
- Les **queues épaisses** (K > 0) augmentent la VaR à 99 %, mais peuvent la faire **baisser** légèrement à 95 % : une distribution à queues épaisses a aussi un centre plus pointu, avec davantage de jours calmes.

### Le domaine de validité : pourquoi « n.d. »

La correction n'a de sens que si elle respecte l'ordre des quantiles : plus z est petit, plus z_cf doit l'être. Le logiciel vérifie que la dérivée de z_cf reste strictement positive pour z de −4 à +4, par pas de 0,1 :

`dérivée = 1 + z × S/3 + (3z² − 3) × K/24 − (6z² − 5) × S²/36`

Si ce n'est pas le cas, la VaR n'est pas calculée : le tableau affiche « n.d. », la ligne violette disparaît du graphique, et une note précise « asymétrie ou kurtosis trop fortes, la correction n'est plus fiable ». La VaR n'est pas non plus calculée avec moins de quatre rendements.

Exemples de couples valides (vérifiés sur une grille de K par pas de 0,1) :

| Asymétrie S | Kurtosis en excès K valide |
|---|---|
| 0 | de 0 à 7,9 |
| −0,5 | de 0,2 à 8,2 |
| −1 | de 1,6 à 8,8 |
| −2 | de 6,6 à 11,2 |

Une forte asymétrie avec des queues trop **minces** est donc aussi hors du domaine.

### Limite

C'est une approximation : avec une distribution très éloignée de la loi normale, préférez la VaR historique et la CVaR.

## La CVaR (Expected Shortfall)
<!-- fiche: analyse-cvar | questions: c'est quoi la cvar ; expected shortfall ; différence entre var et cvar ; perte moyenne au-delà de la var ; quand ça va mal ça va mal comment ; cvar en euros ; pourquoi la cvar est plus grande que la var ; conditional value at risk | mots: CVaR, Expected Shortfall, ES, perte moyenne, queue de distribution, au-delà de la VaR, Bâle III, risque extrême | aller: Analyse du portefeuille/Risque | chiffres: cvar, var_historique -->

La CVaR (Conditional Value at Risk), ou Expected Shortfall, répond à : **et quand ça va mal, ça va mal comment ?**

### La formule

`CVaR = − moyenne des rendements quotidiens inférieurs ou égaux à −VaR historique`

C'est la perte **moyenne** des jours où la VaR historique est atteinte ou dépassée.

`CVaR en euros = CVaR × valeur actuelle`

### Exemple (vingt jours, pour l'illustration)

Rendements classés : −3,1 %, −2,2 %, −1,5 %, −1,2 %, … , +2,0 %.

- La VaR historique à 95 % est interpolée entre les deux pires jours : `−(−3,1 % + 0,95 × 0,9 %) = 2,245 %`.
- Un seul jour est inférieur à −2,245 % : −3,1 %. La CVaR vaut donc **3,10 %**.

Sur un vrai historique de 1 000 jours, la CVaR à 95 % est la moyenne d'environ 50 jours.

### Où la voir

- Carte « CVaR · Expected Shortfall » de l'onglet [[Risque]], en euros, avec la pastille en % « au-delà de la VaR ».
- Ligne « CVaR (Expected Shortfall) » du tableau et ligne rouge continue du graphique.

### Lecture

La CVaR est toujours au moins égale à la VaR historique. Un grand écart entre les deux signale une queue de distribution épaisse : les mauvais jours sont rares mais violents. C'est la mesure privilégiée par les régulateurs bancaires (Bâle III), car elle regarde au-delà du seuil.

### Limites

Elle repose sur peu de jours, surtout à 99 % : sur un an de données (environ 252 jours), la CVaR à 99 % est la moyenne de deux ou trois journées.

## Trois VaR différentes : laquelle croire ?
<!-- fiche: analyse-trois-var | questions: pourquoi trois var différentes ; quelle var utiliser ; var historique plus faible que la var normale ; les var ne sont pas d'accord ; laquelle est la bonne var ; comparaison des méthodes de var ; tableau perte d'un mauvais jour | mots: VaR, comparaison, VaR historique, VaR loi normale, Cornish-Fisher, CVaR, méthodes, choix de la méthode, perte d'un mauvais jour | aller: Analyse du portefeuille/Risque | chiffres: var_historique, var_parametrique, var_cornish_fisher, cvar -->

Le tableau **Perte d'un mauvais jour** de l'onglet [[Risque]] affiche trois VaR et la CVaR, en % et en euros. Elles répondent à la même question avec trois hypothèses.

| Méthode | Hypothèse | Point fort | Point faible |
|---|---|---|---|
| VaR historique | Le passé se répète | Aucune hypothèse de forme | Dépend de la période observée |
| VaR loi normale | Rendements en cloche | Simple, stable | Sous-estime les krachs |
| VaR Cornish-Fisher | Cloche corrigée de l'asymétrie et de la kurtosis | Tient compte de la forme réelle | Approximation, parfois « n.d. » |
| CVaR | Le passé se répète | Mesure la gravité des mauvais jours | Repose sur peu de jours |

### Ce que dit la lecture automatique

Sous le graphique, une phrase compare la VaR historique et la VaR loi normale :

- historique **supérieure de plus de 5 %** : la loi normale sous-estime ici la perte d'un mauvais jour ;
- historique **inférieure de plus de 5 %** : les pertes extrêmes se concentrent sur quelques jours, que la CVaR mesure mieux ;
- sinon : les deux sont proches.

### Comment trancher

1. Regardez le test de Jarque-Bera : si la normalité est rejetée, la VaR loi normale est à prendre avec prudence.
2. Retenez la **plus élevée** des VaR historique et Cornish-Fisher comme ordre de grandeur prudent.
3. Complétez par la CVaR pour savoir jusqu'où vont les mauvais jours, et par le max drawdown pour une baisse sur plusieurs jours.

Aucune VaR n'est une perte maximale. Toutes sont des estimations à un jour, tirées de l'historique du portefeuille.

## Lire le graphique de distribution des rendements
<!-- fiche: analyse-distribution | questions: comment lire le graphique de distribution ; que représente la courbe noire ; à quoi correspondent les lignes verticales ; histogramme des rendements quotidiens ; légende var orange violet rouge ; pourquoi des barres très à gauche ; comparer mes rendements à la loi normale ; une ligne de var a disparu du graphique | mots: distribution, histogramme, loi normale, courbe en cloche, queues épaisses, lignes VaR, légende, rendements quotidiens, gaussienne | aller: Analyse du portefeuille/Risque | chiffres: asymetrie, kurtosis -->

Le graphique **Distribution des rendements quotidiens** de l'onglet [[Risque]] compare vos journées réelles à ce que prévoirait une loi normale.

### Les barres bleues : « Jours observés »

Chaque barre compte le nombre de jours dont le rendement tombe dans une classe. Toutes les classes ont la même largeur ; leur nombre vaut `√n × 1,2`, borné entre 20 et 80 (n = nombre de jours). Exemple : 1 000 jours donnent 37 classes. Le survol affiche « Rendement … » et le nombre de jours.

### La courbe sombre : « Loi normale (même moyenne et volatilité) »

C'est la cloche qu'on obtiendrait si vos rendements suivaient une loi normale de **même moyenne et même écart-type**. Elle est mise à l'échelle des barres :

`jours attendus = densité de la loi normale × nombre de jours × largeur de classe`

Le survol donne le nombre de jours attendus.

### Les lignes verticales

Chacune est placée à `−VaR` (côté des pertes) et figure dans la légende au-dessus du graphique.

| Ligne | Style |
|---|---|
| VaR historique (niveau) | Orange, en tirets |
| VaR loi normale (niveau) | Gris foncé, en pointillés |
| VaR Cornish-Fisher (niveau) | Violet, en tirets et points |
| CVaR (Expected Shortfall) | Rouge, trait plein |

Une ligne absente correspond à une valeur non calculée (VaR Cornish-Fisher « n.d. »). Un clic sur un nom de la légende masque ou réaffiche la ligne.

### Ce qu'il faut regarder

- **Le centre** : des barres qui dépassent la cloche autour de zéro indiquent davantage de jours calmes que prévu.
- **Les extrémités** : des barres isolées loin à gauche, là où la cloche est presque nulle, sont les krachs que la loi normale ne prévoit pas (« queues épaisses »).
- **L'écart entre les lignes** : une ligne orange à gauche de la ligne grise signifie que la VaR historique dépasse la VaR normale.

Les phrases sous le graphique résument ces observations.

## L'asymétrie (skewness)
<!-- fiche: analyse-asymetrie | questions: c'est quoi l'asymétrie ; skewness négative ça veut dire quoi ; mon asymétrie est de -0,5 est ce grave ; distribution asymétrique ; les fortes baisses sont plus fréquentes que les fortes hausses ; asymétrie 0 pour une loi normale ; coefficient d'asymétrie | mots: asymétrie, skewness, coefficient d'asymétrie, distribution, queue gauche, fortes baisses, loi normale, moment d'ordre 3 | aller: Analyse du portefeuille/Risque | chiffres: asymetrie -->

L'asymétrie mesure si la distribution des rendements quotidiens penche d'un côté.

### Le calcul

Le logiciel utilise le coefficient d'asymétrie de l'échantillon, corrigé du biais (moment d'ordre 3 des écarts à la moyenne, rapporté au cube de l'écart-type). Il vaut **0 pour une loi normale**.

### Lecture (seuils de la lecture automatique)

| Asymétrie | Phrase affichée |
|---|---|
| Inférieure à −0,3 | Les fortes baisses sont plus fréquentes ou plus violentes que les fortes hausses |
| Entre −0,3 et +0,3 | La distribution est à peu près symétrique |
| Supérieure à +0,3 | Les fortes hausses l'emportent sur les fortes baisses |

### Exemple

Un portefeuille d'actions affiche souvent une asymétrie négative, par exemple −0,5 : les marchés montent par petites étapes et baissent par à-coups. À 95 %, avec une kurtosis en excès de 3, la VaR Cornish-Fisher passe alors de 1,54 % (asymétrie nulle) à 1,68 % (asymétrie −0,5), pour une moyenne de 0,04 % et un écart-type de 1 %.

### Pourquoi c'est important

Une asymétrie négative signifie que le risque est concentré du mauvais côté : la volatilité et la VaR loi normale, qui supposent une distribution symétrique, sous-estiment alors les pertes.

### Limites

L'asymétrie est très sensible à quelques journées extrêmes : un seul krach dans l'historique peut la faire basculer. Elle demande un historique long pour être fiable.

## La kurtosis en excès et les jours extrêmes
<!-- fiche: analyse-kurtosis | questions: c'est quoi la kurtosis ; kurtosis en excès ça veut dire quoi ; queues épaisses c'est quoi ; jours à plus de 3 écarts-types ; pourquoi 0,27 % selon la loi normale ; fat tails ; aplatissement ; ma kurtosis est de 5 | mots: kurtosis, kurtosis en excès, aplatissement, queues épaisses, fat tails, leptokurtique, jours extrêmes, 3 écarts-types, moment d'ordre 4 | aller: Analyse du portefeuille/Risque | chiffres: kurtosis -->

### La kurtosis en excès

Elle mesure l'épaisseur des queues de la distribution : la fréquence des journées extrêmes, dans les deux sens. Le logiciel calcule la kurtosis **en excès** de l'échantillon, corrigée du biais : elle vaut **0 pour une loi normale**.

| Kurtosis en excès | Phrase de la lecture automatique |
|---|---|
| Supérieure à 1 | « Queues épaisses », avec le nombre de journées extrêmes observées et attendues |
| Entre 0 et 1 | Queues légèrement plus épaisses que la loi normale |
| 0 ou moins | Pas plus de journées extrêmes que ne le prévoit la loi normale |

### Les jours à plus de 3 écarts-types

`Part des jours extrêmes = part des jours où |rendement − moyenne| > 3 × écart-type`

Selon la loi normale, cette part vaut `2 × (1 − Φ(3)) = 0,27 %`, soit environ un jour sur 370. La carte « Jours à plus de 3 écarts-types » compare la part observée à ce chiffre théorique.

### Exemple

Sur 1 000 jours, la loi normale prévoit 2 à 3 jours extrêmes. Si vous en observez 12 (1,20 %), il y en a environ 4,4 fois plus que prévu : la lecture automatique l'indique (« ×4,4 »).

### Pourquoi c'est important

Les marchés financiers ont presque toujours une kurtosis positive. La volatilité et la VaR loi normale décrivent bien les jours ordinaires, mais sous-estiment les krachs : à 99 %, préférez la VaR historique, la VaR Cornish-Fisher et la CVaR.

### Limites

Comme l'asymétrie, la kurtosis est dominée par quelques journées. Un historique court sans crise peut afficher une kurtosis faible qui ne garantit rien.

## Le test de Jarque-Bera
<!-- fiche: analyse-jarque-bera | questions: c'est quoi le test de jarque bera ; normalité rejetée ça veut dire quoi ; p-value jarque bera ; comment lire p < 0,001 ; mes rendements suivent ils une loi normale ; test de normalité ; pourquoi la normalité est toujours rejetée | mots: Jarque-Bera, test de normalité, p-value, loi normale, khi-deux, normalité rejetée, statistique JB, hypothèse | aller: Analyse du portefeuille/Risque | chiffres: asymetrie, kurtosis -->

Le test de Jarque-Bera vérifie si vos rendements quotidiens peuvent raisonnablement suivre une loi normale.

### La formule

```
JB = n / 6 × (S² + K² / 4)
p-value = exp(−JB / 2)
```

avec n le nombre de jours, S l'asymétrie et K la kurtosis en excès. Sous l'hypothèse de normalité, JB suit une loi du khi-deux à 2 degrés de liberté, dont la probabilité de dépassement vaut exactement `exp(−JB/2)`.

### Lecture

La carte « Test de Jarque-Bera » affiche « p = » suivi de la p-value (« < 0,001 » quand elle est minuscule), avec une pastille :

- **p < 0,05** : pastille rouge « Normalité rejetée ». Les VaR fondées sur la loi normale sont à prendre avec prudence.
- **p ≥ 0,05** : pastille verte « Normalité non rejetée ». Cela ne prouve pas que la loi est normale : les données ne permettent simplement pas de l'exclure.

### Exemples

- 1 000 jours, S = −0,5, K = 3 : `JB = 1 000 / 6 × (0,25 + 2,25) = 416,7` ; p-value quasi nulle, affichée « < 0,001 » : normalité rejetée.
- 250 jours, S = −0,1, K = 0,3 : `JB = 250 / 6 × (0,01 + 0,0225) = 1,35` ; `p = exp(−0,677) = 0,508` : normalité non rejetée.

### Pourquoi la normalité est presque toujours rejetée

Avec beaucoup de jours, le moindre écart d'asymétrie ou de kurtosis devient significatif. Sur des données de marché de plusieurs années, le rejet est la règle : c'est précisément pour cela que le logiciel propose la VaR historique et la VaR Cornish-Fisher.

### Limite

Avec moins de quatre rendements, le test n'est pas calculé (p-value fixée à 1).

## Que contient l'onglet Expositions ?
<!-- fiche: analyse-onglet-expositions | questions: que contient l'onglet expositions ; comment lire les pastilles vertes orange rouges ; que veut dire non concerné ; à quoi servent les sous-onglets géographie devises concentration corrélations ; ou voir mes points d'attention ; constats et pistes c'est quoi ; mon portefeuille est il bien diversifié | mots: expositions, diversification, synthèse, constats, pistes, pastilles, géographie, secteurs, devises, concentration, taux, corrélations | aller: Analyse du portefeuille/Expositions -->

L'onglet [[Expositions]] répond à deux questions : à quoi le portefeuille est-il **réellement** exposé, et est-il **vraiment** diversifié ? Tout y est calculé en transparence.

### 1. L'en-tête et le profil

Le titre « Expositions et diversification » rappelle que les ETF sont répartis selon leur indice (approximation au 30/09/2026). À droite, le menu [[Seuils adaptés au profil]] choisit les seuils du diagnostic : Prudent, Équilibré (par défaut) ou Dynamique.

### 2. La synthèse : six cases

| Dimension | Chiffre affiché sous la pastille |
|---|---|
| Géographie | 1er pays de la poche actions et son poids |
| Secteurs | 1er secteur de la poche actions et son poids |
| Devises | Part hors euro |
| Concentration | Poids de la plus grosse ligne |
| Taux | Duration moyenne, ou « Pas d'obligations » |
| Diversification réelle | Corrélation moyenne entre les lignes |

La pastille donne le constat le plus grave de la dimension : verte « Bon », orange « À surveiller », rouge « À corriger », ou grise « Non concerné » (par exemple, la dimension Taux sans obligation).

### 3. Constats et pistes

Les points orange et rouges sont listés du plus grave au moins grave. Chaque constat donne le chiffre observé, le risque associé et des pistes. Les points verts sont rangés dans un panneau « Points positifs », ouvert d'emblée s'il n'y a aucun point d'attention.

### 4. Quatre sous-onglets de détail

- [[Géographie et secteurs]] : régions et secteurs comparés à l'indice, principaux écarts par pays, part de la valeur et part du risque par région ;
- [[Devises et taux]] : exposition réelle aux devises, sensibilité aux taux ;
- [[Concentration]] : nombre de lignes, poids des plus grosses, règle 5/10/40 ;
- [[Corrélations]] : matrice, blocs, paires, lignes qui diversifient.

## Le diagnostic des expositions est-il un conseil ?
<!-- fiche: analyse-diagnostic | questions: le diagnostic est il un conseil en investissement ; dois je suivre les pistes proposées ; comment sont établis les constats ; pourquoi le logiciel me dit de diversifier ; à corriger ça veut dire que je dois vendre ; les pistes sont elles personnalisées ; sur quoi se base le diagnostic | mots: diagnostic, constat, pistes, conseil en investissement, règles, seuils, pédagogique, recommandation, avertissement | aller: Analyse du portefeuille/Expositions -->

**Non.** Comme le rappelle la note de l'onglet [[Expositions]], c'est une « analyse pédagogique fondée sur des règles simples et des données passées : elle ne constitue pas un conseil en investissement ».

### Comment les constats sont produits

Le logiciel applique des règles fixes, écrites à l'avance, aux chiffres du portefeuille : poids d'un pays comparé au marché mondial (MSCI ACWI), poids d'un secteur, part hors euro, poids d'une action, duration, corrélations. Chaque règle a un seuil ; selon la valeur observée, elle produit un constat vert, orange ou rouge, accompagné d'une phrase sur le risque et de pistes générales. Le détail des seuils figure dans les fiches suivantes.

### Ce que le diagnostic ne connaît pas

- votre situation personnelle : patrimoine hors de ce portefeuille, revenus, horizon, objectifs, fiscalité ;
- vos raisons : une surpondération peut être un choix délibéré ;
- l'avenir : les corrélations et compositions sont tirées du passé et des fiches d'indices.

### Comment l'utiliser

Lisez chaque constat comme une question à vous poser : « ce biais est-il voulu ? ». Les pistes illustrent des solutions courantes (ETF monde, couverture de change, duration plus courte…), sans tenir compte de vos contraintes. Avant toute décision, notamment une vente qui déclencherait un impôt, consultez un professionnel habilité.

### Le rapport PDF

La partie « Expositions et diversification » du rapport reprend ce diagnostic avec les seuils du profil **Équilibré**, quel que soit le profil choisi à l'écran.

## Les seuils par profil : Prudent, Équilibré, Dynamique
<!-- fiche: analyse-seuils-profil | questions: à quoi sert le choix du profil dans expositions ; quels sont les seuils prudent équilibré dynamique ; pourquoi un constat devient rouge en profil prudent ; changer de profil change quoi ; seuils d'alerte du diagnostic ; mon profil est il enregistré ; seuil de concentration par profil | mots: profil, Prudent, Équilibré, Dynamique, seuils, alerte, diagnostic, tolérance au risque, paramétrage | aller: Analyse du portefeuille/Expositions -->

Le menu [[Seuils adaptés au profil]], en haut de l'onglet [[Expositions]], règle la sévérité du diagnostic. Il ne modifie aucun calcul : seulement la couleur des constats.

### Les seuils qui dépendent du profil

Pour chaque règle, la première valeur fait passer à l'orange (« À surveiller »), la seconde au rouge (« À corriger ») ; il faut la **dépasser**.

| Règle | Prudent | Équilibré | Dynamique |
|---|---|---|---|
| Part du portefeuille hors euro | 30 % / 50 % | 50 % / 70 % | 70 % / 85 % |
| Pays émergents dans la poche actions | 10 % / 20 % | 20 % / 30 % | 25 % / 40 % |
| Plus grosse action détenue en direct | 5 % / 10 % | 7 % / 10 % | 10 % / 15 % |
| Duration moyenne des obligations | 5 / 8 ans | 7 / 10 ans | 8 / 12 ans |

### Les règles identiques pour tous les profils

Géographie (hors émergents), secteurs, règle 5/10/40, doublons probables et corrélations ont les mêmes seuils quel que soit le profil (voir les fiches correspondantes).

### Exemple

Un portefeuille de 100 000 € : un ETF MSCI World de 60 000 € et quatre actions françaises (LVMH 15 000 €, TotalEnergies 10 000 €, Airbus 8 000 €, Sanofi 7 000 €). Part hors euro : 55 % (dont 44 % en dollars, via l'ETF). Plus grosse action : LVMH, 15 %.

| Profil | Devises (55 %) | LVMH (15 %) |
|---|---|---|
| Prudent | À corriger (> 50 %) | À corriger (> 10 %) |
| Équilibré | À surveiller (> 50 %) | À corriger (> 10 %) |
| Dynamique | Bon (≤ 70 %) | À surveiller (> 10 %) |

### Durée du choix

Le profil est gardé pendant la session ; il n'est pas enregistré dans votre compte. Le rapport PDF utilise toujours le profil Équilibré.

## Géographie et secteurs : les règles et les écarts à l'indice
<!-- fiche: analyse-geographie-secteurs | questions: pourquoi la france est en rouge ; biais domestique c'est quoi ; comment est calculé l'écart avec le marché mondial ; peu de secteurs défensifs ça veut dire quoi ; mon portefeuille est trop concentré sur la technologie ; comparer mes régions à l'indice ; part de la valeur et part du risque par région ; principaux écarts par pays | mots: géographie, pays, région, secteurs, biais domestique, émergents, secteurs défensifs, surpondération, sous-pondération, MSCI ACWI, écarts | aller: Analyse du portefeuille/Expositions -->

### Les règles de géographie (poche actions)

Elles s'appliquent si les actions pèsent plus de 5 % du portefeuille. Les trois premiers pays sont comparés à leur poids dans le **MSCI ACWI** (marché mondial) :

- **À corriger** : un pays dépasse son poids mondial de plus de 25 points, ou un pays autre que les États-Unis pèse plus de 40 % ;
- **À surveiller** : il le dépasse de plus de 15 points ;
- **Biais domestique** (à surveiller) : la France pèse plus de 15 % **et** plus de quatre fois son poids mondial (environ 2 %) ;
- **Pays émergents** : seuils selon le profil.

### Les règles de secteurs (poche actions)

Elles s'appliquent dans les mêmes conditions. Pour les trois premiers secteurs : à corriger au-delà de 40 % ou de 15 points au-dessus du marché mondial ; à surveiller au-delà de 30 % ou de 8 points. Un constat « peu de secteurs défensifs » apparaît si santé, consommation de base et services publics totalisent moins de 10 %.

### Exemple

ETF MSCI World 60 000 €, LVMH 15 000 €, TotalEnergies 10 000 €, Airbus 8 000 €, Sanofi 7 000 €. En transparence, la France pèse 41 % de la poche actions (contre 2 % dans le marché mondial) : constat rouge, car un pays autre que les États-Unis dépasse 40 %, et constat orange de biais domestique. La consommation discrétionnaire pèse 20 % contre 8 % dans le monde (+12 points) : à surveiller.

### Le sous-onglet [[Géographie et secteurs]]

- **Régions (poche actions)** et **Secteurs (poche actions)** : deux barres par groupe, « Portefeuille » (bleu foncé) et l'indice (bleu-gris). L'indice est celui choisi dans les paramètres s'il comporte des actions ; sinon (indice obligataire ou monétaire), c'est le MSCI ACWI.
- **Principaux écarts par pays** : les dix plus fortes sur- et sous-pondérations, en points.
- **Part de la valeur et part du risque par région** : une région qui apporte plus de risque que de valeur est plus volatile ou plus corrélée au reste. La part du risque de chaque ligne est expliquée dans l'espace Gestion d'actifs, onglet Budget de risque.

### Limite

Les poids des pays et des secteurs dans les ETF et dans le MSCI ACWI sont des approximations (voir la fiche sur la carte du monde).

## L'exposition réelle aux devises
<!-- fiche: analyse-devises-exposition | questions: pourquoi je suis exposé au dollar alors que mon etf est en euros ; exposition aux devises comment est elle calculée ; risque de change de mon portefeuille ; etf couvert eur hedged ; une baisse du dollar me coûterait combien ; l'or est il en dollars ; part hors euro | mots: devises, risque de change, exposition au dollar, EUR Hedged, couverture de change, part hors euro, USD, or, devise réelle | aller: Analyse du portefeuille/Expositions -->

Un ETF MSCI World coté en euros reste exposé au **dollar**, au yen, à la livre… : il détient des actions dont la valeur se forme dans ces monnaies. Le sous-onglet [[Devises et taux]] mesure cette exposition réelle.

### Le calcul

En transparence, chaque morceau d'ETF actions reçoit la devise de son pays ; une action en direct garde sa devise de cotation ; un fonds dont le nom indique une couverture (« Hedged », « couvert ») est compté en euros ; les obligations sont en euros pour un indice de la zone euro, en dollars sinon ; l'or est compté à part, avec la « devise » Or. L'anneau **Exposition réelle aux devises** porte sur **tout** le portefeuille.

`Part hors euro = somme des poids de toutes les devises sauf l'euro et l'or`

### Exemple

ETF MSCI World 60 000 € et 40 000 € d'actions françaises. Dollar : `60 % × 72,94 % = 43,8 %` ; yen 3,5 % ; livre 2,0 % ; dollar canadien 2,0 % ; franc suisse 1,4 % ; etc. Part hors euro : **55 %**. Le constat estime l'effet d'une baisse de 10 % du dollar : `43,8 % × 10 % ≈ 4 %` du portefeuille.

### Le constat

Il dépend du profil : au-delà de 30 % hors euro (Prudent), 50 % (Équilibré) ou 70 % (Dynamique), il passe à l'orange, puis au rouge au-delà de 50 %, 70 % ou 85 %. Sinon : « Risque de change limité ».

### Lecture

Le risque de change n'est pas que négatif : le dollar monte souvent en période de crise, ce qui amortit les baisses. Couvrir une partie de la poche est un compromis courant ; c'est la piste proposée.

### Limites

La devise d'un pays est une approximation : une entreprise américaine réalise une partie de son chiffre d'affaires dans d'autres monnaies. La couverture n'est reconnue que si elle figure dans le nom du fonds.

## La duration et la sensibilité aux taux
<!-- fiche: analyse-duration | questions: c'est quoi la duration ; si les taux montent de 1 point combien je perds ; sensibilité de mes obligations aux taux ; pourquoi pas d'obligations dans taux ; duration moyenne de mon portefeuille ; risque de taux ; mes obligations ont baissé à cause des taux | mots: duration, sensibilité, taux d'intérêt, obligations, risque de taux, hausse des taux, poche obligataire, perte estimée | aller: Analyse du portefeuille/Expositions -->

### La duration

C'est la durée de vie moyenne pondérée des flux d'une obligation, en années. Elle mesure la **sensibilité aux taux** : plus elle est longue, plus le prix baisse quand les taux montent (et monte quand ils baissent).

Le logiciel lit la duration de chaque fonds obligataire dans sa fiche descriptive, puis calcule :

```
Duration moyenne = Σ (duration × valeur) / Σ valeur, sur les lignes obligataires dont la duration est connue
Perte si les taux montent de 1 point ≈ Σ (duration × valeur) × 1 %
```

### Exemple

Portefeuille de 100 000 € ; obligations A : 30 000 €, duration 4 ans ; obligations B : 10 000 €, duration 8 ans.

- duration moyenne : `(4 × 30 000 + 8 × 10 000) / 40 000 = 5,0 ans` ;
- perte estimée : `(4 × 30 000 + 8 × 10 000) × 1 % = 2 000 €`, soit **−2,0 %** du portefeuille.

### Où le voir

Sous-onglet [[Devises et taux]], bloc **Sensibilité aux taux** : cartes « Duration moyenne » et « Si les taux montent de 1 point » (en % du portefeuille et en euros). Sans obligation, le bloc indique que le portefeuille n'en contient pas, et la case Taux de la synthèse affiche « Non concerné ».

### Le constat

La couleur dépend du profil : à surveiller au-delà de 5 ans (Prudent), 7 ans (Équilibré) ou 8 ans (Dynamique) ; à corriger au-delà de 8, 10 ou 12 ans. Dans l'exemple (5,0 ans), le constat est vert pour tous les profils.

### Limites

- Approximation au premier ordre : `variation du prix ≈ − duration × variation des taux`, valable pour de petites variations.
- Une obligation dont la duration n'est pas connue est exclue de la moyenne et de la perte estimée.
- Après une hausse des taux, les obligations offrent ensuite un rendement plus élevé, qui compense peu à peu la perte.

## Concentration, nombre effectif de lignes et règle 5/10/40
<!-- fiche: analyse-concentration | questions: c'est quoi la règle 5 10 40 ; mon portefeuille est il trop concentré ; nombre effectif de lignes ; équivalent à 3 lignes de même poids ça veut dire quoi ; limite ucits 40 % ; une seule action représente trop ; doublons probables etf et action en direct ; détenu en direct et via votre etf | mots: concentration, règle 5/10/40, UCITS, OPCVM, nombre effectif, Herfindahl, plus grosses lignes, doublons, risque spécifique | aller: Analyse du portefeuille/Expositions -->

### Le nombre effectif de lignes

`Nombre effectif = 1 / Σ poids²` (inverse de l'indice de Herfindahl)

Il dit à combien de lignes **de même poids** votre portefeuille équivaut. Exemple : quatre lignes de 40 %, 30 %, 20 % et 10 % : `1 / (0,16 + 0,09 + 0,04 + 0,01) = 3,33`, affiché « équivalent à 3 lignes de même poids ».

### Le sous-onglet [[Concentration]]

Quatre cartes : « Lignes » (avec le nombre effectif), « 5 premières lignes », « 10 premières lignes » et « Actions de plus de 5 % » (« Limite UCITS : 40 % ») ; puis le tableau **Les plus grosses lignes** (15 au plus), avec poids et poids cumulé.

### La règle 5/10/40

Règle des fonds UCITS (OPCVM européens) : une ligne ne dépasse pas 10 %, et les lignes de plus de 5 % ne totalisent pas plus de 40 %. Le logiciel l'applique aux seules **actions détenues en direct** : un ETF diversifié n'est pas une concentration.

- Les actions de plus de 5 % totalisent plus de 40 % : constat rouge « règle 5/10/40 dépassée ».
- La plus grosse action dépasse le seuil du profil (5, 7 ou 10 % pour l'orange ; 10, 10 ou 15 % pour le rouge) : constat qui chiffre l'effet d'une chute de 30 % du titre.

Exemple : LVMH 15 %, TotalEnergies 10 %, Airbus 8 %, Sanofi 7 % totalisent **exactement 40 %** : la règle n'est pas dépassée (il faut plus de 40 %). En revanche, LVMH à 15 % est « À corriger » en profil Équilibré ; une chute de 30 % du titre coûterait `15 % × 30 % ≈ 4 %` du portefeuille.

### Les doublons probables

Une action détenue en direct peut aussi figurer dans un ETF que vous détenez : votre exposition à cette entreprise est alors plus forte que sa seule ligne. Le logiciel le signale (constat orange « détenu(s) en direct ET probablement aussi via votre ETF ») quand :

- l'ETF suit le MSCI World, l'ACWI ou l'EAFE et le pays de l'action fait partie de l'indice, sauf si la fiche du titre indique qu'il n'appartient à aucun grand indice ;
- l'ETF suit le MSCI Europe et l'action est européenne, britannique ou suisse, avec la même réserve ;
- l'ETF suit le S&P 500 ou le marché américain et l'action est américaine, sauf si la fiche du titre indique des indices sans mentionner le S&P 500 ;
- ou la fiche du titre mentionne explicitement l'indice de l'ETF.

C'est une **probabilité** : le logiciel ne lit pas l'inventaire réel du fonds.

## Lire la matrice de corrélation
<!-- fiche: analyse-matrice-correlation | questions: comment lire la matrice de corrélation ; que veulent dire les cases rouges et bleues ; pourquoi la moitié du tableau est vide ; corrélation entre mes titres ; paires les plus corrélées ; lignes qui diversifient le mieux ; vue par classe d'actifs ou par titre ; pourquoi les titres ne sont pas dans l'ordre | mots: corrélation, matrice de corrélation, heatmap, carte de chaleur, paires, diversifiants, blocs, classification hiérarchique, co-mouvement | aller: Analyse du portefeuille/Expositions -->

La matrice se trouve dans le sous-onglet [[Corrélations]] de l'onglet [[Expositions]].

### La corrélation

Elle mesure, entre −1 et +1, à quel point les rendements quotidiens de deux titres évoluent ensemble :

| Valeur | Lecture | Qualificatif affiché |
|---|---|---|
| 0,8 à 1 | Montent et baissent presque toujours ensemble | très forte |
| 0,6 à 0,8 | Évoluent souvent ensemble | forte |
| 0,3 à 0,6 | Lien partiel | modérée |
| Moins de 0,3 | Peu de lien | faible |
| Négative | Quand l'un monte, l'autre tend à baisser | (même échelle, en valeur absolue) |

Elle est calculée sur les cours en euros des lignes détenues, sur les jours où toutes ont un rendement. La note sous le graphique indique ce nombre de jours.

### Lire la carte

- **Couleurs** : rouge = évoluent ensemble ; blanc = pas de lien ; bleu = en sens inverse.
- **Moitié du tableau** : seul le triangle inférieur est affiché, sans la diagonale (toujours 1) ; l'autre moitié répéterait la même information.
- **Ordre** : les titres sont rangés par blocs qui évoluent ensemble (classification hiérarchique, distance = 1 − corrélation). Les blocs apparaissent comme des carrés rouges.
- **Valeurs** : écrites dans les cases jusqu'à 13 titres ; au-delà, survolez une case pour lire les deux noms, la valeur et son qualificatif.

### Changer de vue

Le sélecteur [[Afficher]] propose [[Par titre]], [[Par classe d'actifs]], [[Par région]] et [[Par secteur]] (les vues de groupe n'apparaissent que si le portefeuille compte plusieurs groupes). Une vue de groupe montre la corrélation entre les rendements des sous-portefeuilles, chaque ligne pondérée par son poids ; les groupes suivent le classement des lignes, sans éclatement des ETF. Au-delà de 20 titres, une vue par groupe s'ouvre d'emblée.

### Les tableaux à droite

- **Paires les plus corrélées** : les cinq paires de titres les plus liées.
- **Lignes qui diversifient le mieux** : les cinq lignes les moins corrélées au **reste** du portefeuille (le portefeuille sans elles).
- **Blocs de titres corrélés** : les groupes de corrélation moyenne supérieure à 0,7 (fiche dédiée).

### Limite

Les corrélations sont historiques : elles ne sont pas garanties à l'avenir et montent souvent pendant les crises.

## La corrélation moyenne, en temps normal et les jours de forte baisse
<!-- fiche: analyse-correlation-moyenne | questions: c'est quoi la corrélation moyenne pondérée ; corrélation moyenne élevée est ce grave ; les jours de forte baisse corrélation ; pourquoi la corrélation monte en crise ; la carte affiche un tiret pour les jours de forte baisse ; corrélation en crise ; ma diversification protège t elle en cas de krach | mots: corrélation moyenne, corrélation pondérée, crise, jours de forte baisse, 10 % pires jours, contagion, diversification, krach | aller: Analyse du portefeuille/Expositions -->

### La corrélation moyenne pondérée

```
Corrélation moyenne = Σ_{i≠j} wᵢ × wⱼ × ρᵢⱼ / Σ_{i≠j} wᵢ × wⱼ
```

où `w` sont les poids des lignes et `ρ` leurs corrélations. C'est la corrélation « typique » entre deux euros investis dans deux lignes différentes : les grosses lignes comptent davantage.

**Exemple** : trois lignes de 50 %, 30 % et 20 % ; corrélations 0,8 (A-B), 0,2 (A-C), 0,3 (B-C).
`(0,15 × 0,8 + 0,10 × 0,2 + 0,06 × 0,3) / (0,15 + 0,10 + 0,06) = 0,158 / 0,31 = 0,51`.

**Constats** : au-delà de 0,45, « À surveiller » ; au-delà de 0,6, « À corriger » : le portefeuille se comporte presque comme un seul actif.

### Les jours de forte baisse

Le logiciel reconstitue le rendement quotidien du portefeuille **avec ses poids actuels**, retient ses 10 % pires journées, et recalcule la corrélation moyenne pondérée sur ces seuls jours.

- Carte « Les jours de forte baisse » du sous-onglet [[Corrélations]] (« corrélation moyenne (10 % pires jours) »).
- Il faut au moins 30 jours de forte baisse, soit environ 300 jours d'historique commun : sinon la carte affiche un tiret.
- Si elle dépasse la corrélation moyenne de plus de 0,10, un constat orange l'indique : « la diversification protège moins quand on en a le plus besoin ».

### Pourquoi la corrélation monte en crise

Lors d'un krach, les investisseurs vendent un peu de tout en même temps : des actifs habituellement indépendants baissent ensemble. Une diversification qui paraît bonne en temps normal peut alors s'évaporer. Les stress tests de l'espace Conseil patrimonial permettent de mesurer l'impact d'une crise.

### Limite

Les poids actuels sont appliqués à tout l'historique : c'est le comportement du portefeuille **d'aujourd'hui** dans les crises passées, pas celui de votre portefeuille réel à l'époque.

## Le ratio de diversification
<!-- fiche: analyse-ratio-diversification | questions: c'est quoi le ratio de diversification ; ratio de diversification de 1 ça veut dire quoi ; comment est calculé le ratio de diversification ; un bon ratio de diversification c'est combien ; mon portefeuille est il vraiment diversifié ; diversification ratio choueifaty | mots: ratio de diversification, diversification ratio, volatilité pondérée, volatilité du portefeuille, réduction du risque, corrélation | aller: Analyse du portefeuille/Expositions -->

### La formule

`Ratio de diversification = Σ wᵢ × σᵢ / σₚ`

- `Σ wᵢ × σᵢ` : la moyenne pondérée des volatilités des lignes, c'est-à-dire la volatilité qu'aurait le portefeuille si toutes les lignes bougeaient exactement ensemble ;
- `σₚ` : la volatilité réelle du portefeuille, qui tient compte des corrélations.

Les deux sont calculées sur les rendements quotidiens en euros, avec les poids actuels.

### Intuition

Le ratio mesure **combien le risque se compense** entre les lignes. Il vaut 1 quand il n'y a aucune diversification (lignes parfaitement corrélées) et augmente quand les lignes se compensent.

### Exemple

Deux lignes de 50 %, chacune de volatilité 20 % :

| Corrélation | Volatilité du portefeuille | Ratio |
|---|---|---|
| 1 | 20,00 % | 1,00 |
| 0,5 | 17,32 % | 1,15 |
| 0 | 14,14 % | 1,41 |

Avec une corrélation de 0,5 : `σₚ = √(0,25 × 0,04 + 0,25 × 0,04 + 2 × 0,25 × 0,5 × 0,04) = √0,03 = 17,32 %`, et `20 / 17,32 = 1,15`.

### Où le voir

Carte « Ratio de diversification » du sous-onglet [[Corrélations]] (« 1 = aucune diversification ») ; il est aussi cité dans le constat vert « Diversification réelle satisfaisante ».

### Limites

- Le ratio n'a pas de seuil d'alerte dans le diagnostic : il se lit par comparaison, d'une version du portefeuille à l'autre.
- Il dépend des corrélations passées.
- Ajouter une ligne très peu risquée (monétaire) le modifie peu : il mesure la compensation entre lignes, pas le niveau de risque.

## Les blocs de titres corrélés (blocs indépendants)
<!-- fiche: analyse-blocs-correles | questions: c'est quoi les blocs indépendants ; un seul pari ça veut dire quoi ; blocs de titres corrélés à plus de 0,7 ; mes 10 lignes ne valent qu'un pari ; comment sont formés les blocs ; pourquoi mes actions technologiques sont dans le même bloc ; nombre de blocs pour mes lignes | mots: blocs corrélés, blocs indépendants, paris, classification hiérarchique, clustering, regroupement, corrélation 0,7, diversification apparente | aller: Analyse du portefeuille/Expositions -->

Dix lignes qui montent et baissent ensemble ne valent qu'**un seul pari**. Les blocs mesurent cette diversification réelle.

### Comment les blocs sont formés

1. Distance entre deux titres = `1 − corrélation`.
2. Classification hiérarchique par lien moyen : les titres les plus proches sont regroupés, puis les groupes entre eux.
3. Le regroupement s'arrête à la distance 0,3 : un bloc réunit des titres dont la corrélation moyenne dépasse environ **0,7**.

Un titre qui ne ressemble à aucun autre forme un bloc à lui seul.

### Où le voir

- Carte « Blocs indépendants » (« pour » n lignes) du sous-onglet [[Corrélations]] : le nombre total de blocs, titres isolés compris.
- Bloc **Blocs de titres corrélés** : les cinq plus gros blocs d'au moins deux titres, avec leur poids, leurs noms et leur corrélation moyenne.
- Les blocs apparaissent aussi comme des carrés rouges dans la matrice.

### Exemple

Supposons un portefeuille de 8 lignes qui affiche « 5 blocs indépendants ». Trois actions de semi-conducteurs, corrélées à 0,78 en moyenne et pesant 28 %, forment un bloc : le diagnostic signale « 3 lignes très corrélées entre elles (0,78 en moyenne) pèsent 28 % … 3 lignes, mais en pratique un seul pari ».

### Les constats

Les trois plus gros blocs sont examinés :

- poids inférieur à 15 % : pas de constat ;
- de 15 à 25 % : « À surveiller » ;
- 25 % ou plus : « À corriger ».

Les pistes proposées : remplacer une partie du bloc par des actifs peu corrélés, ou regrouper ces lignes dans un seul ETF du même thème.

### Limites

Le seuil de 0,7 est une convention. Les blocs reposent sur des corrélations passées et peuvent changer d'une période à l'autre.

## Consulter l'historique des opérations (onglet Transactions)
<!-- fiche: analyse-transactions | questions: ou voir toutes mes transactions ; filtrer les opérations par titre ; afficher seulement les dividendes ; exporter mes transactions en csv ; pourquoi le prix est en euros dans l'historique ; colonne prix en devise ; combien d'opérations dans mon portefeuille ; historique des achats et ventes | mots: transactions, opérations, historique, filtre, export CSV, achats, ventes, dividendes, consultation, prix en devise | aller: Analyse du portefeuille/Transactions | chiffres: nb_operations -->

L'onglet [[Transactions]] affiche toutes les opérations du portefeuille, de la plus récente à la plus ancienne.

### Filtrer

- [[Type]] : retirez ou ajoutez ACHAT, VENTE et DIVIDENDE (tous sont sélectionnés au départ).
- [[Titres]] : choisissez un ou plusieurs titres ; laissé vide, il affiche « Tous les titres ».

Une ligne indique le nombre d'opérations affichées sur le total.

### Les colonnes

| Colonne | Contenu |
|---|---|
| Date | Date de l'opération |
| Type | ACHAT, VENTE ou DIVIDENDE |
| Ticker, Titre | Code et nom du titre |
| Quantité | Nombre de titres (0 pour un dividende) |
| Prix / montant (€) | Prix unitaire, ou montant total pour un dividende, **converti en euros** |
| Frais | Frais en euros |
| Devise, Prix en devise | Présentes si le portefeuille contient des titres en devises : la devise de cotation et le prix saisi avant conversion |

### Exporter

Le bouton [[Télécharger la sélection (CSV)]] enregistre les opérations affichées dans le fichier `transactions_selection.csv`. Les types y restent écrits ACHAT, VENTE, DIVIDENDE, mais la colonne de prix est celle **convertie en euros** ; les colonnes de devise et de prix en devise sont ajoutées le cas échéant. Pour réimporter un portefeuille, utilisez plutôt le fichier d'origine ou le fichier mis à jour.

### Modifier une opération

Le bouton [[Modifier les opérations]] permet de supprimer ou de corriger n'importe quelle opération. Cette fonction, ses contrôles et l'annulation sont décrits dans le chapitre sur l'import et la mise à jour du portefeuille.
