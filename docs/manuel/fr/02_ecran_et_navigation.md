# L'écran et la navigation
<!-- chapitre: ecran | ordre: 2 -->

Ce chapitre décrit l'écran du logiciel : la barre latérale bloc par bloc, le choix de la langue et du mode nuit, les quatre espaces de travail, le choix du portefeuille et des paramètres d'analyse (indice de référence, taux sans risque, niveau de la VaR), le bandeau et les chiffres clés en haut de page, le rapport PDF, l'actualisation des cours, l'assistant du manuel et les astuces des graphiques. Lisez-le après la prise en main pour savoir où trouver chaque fonction.

## Comment est organisé l'écran ?
<!-- fiche: ecran-organisation | questions: comment est organisé l'écran ; a quoi sert la barre de gauche ; je suis perdu dans le logiciel par où commencer ; c'est quoi le menu à gauche ; ou se trouvent les reglages ; la barre latérale a disparu ; description de l'interface ; qu'est-ce qu'il y a dans la colonne de gauche | mots: interface, écran, barre latérale, sidebar, menu, navigation, disposition, tableau de bord -->

L'écran est divisé en deux parties : la **barre latérale**, à gauche, qui regroupe tous les réglages, et la **zone principale**, à droite, qui affiche les résultats.

### La barre latérale, de haut en bas

1. **L'en-tête** : le monogramme « PT », le nom « Portfolio Tracker » et la mention « Master G2C ». À droite, deux petits sélecteurs : la langue (FR ou EN) et l'affichage (Clair ou Nuit).
2. **L'espace personnel** : la mention « Espace personnel chiffré » et le lien [[Se connecter]]. Une fois connecté, vos initiales, votre identifiant et les liens [[Mon compte]] et [[Déconnexion]].
3. **Espace de travail** : le menu des quatre espaces (Analyse du portefeuille, Conseil patrimonial, Gestion d'actifs, Manuel et aide), chacun avec une ligne de description.
4. **Données** : la liste des portefeuilles, la zone [[Envoyer un fichier (CSV, Excel ou PDF)]], puis les liens [[Ajouter des opérations]] et [[Modèle de fichier]].
5. **Paramètres** : un panneau replié qui contient l'indice de référence, le taux sans risque et le niveau de confiance de la VaR. Son titre résume les réglages en cours.
6. **Les informations** sur le portefeuille analysé : fichier, période, nombre d'opérations, provenance des cours et taux de change.
7. **Les boutons** [[Rapport PDF]] et [[Actualiser les cours]].

Les blocs 6 et 7 n'apparaissent qu'une fois un portefeuille analysé : ils sont absents dans l'espace « Manuel et aide » et sur les pages « Mon compte » et « Ajouter des opérations ».

### La zone principale

Dans les espaces d'analyse, elle commence par un bandeau bleu (titre, période, indice de référence, provenance des cours), suivi d'une ligne de six chiffres clés, puis des onglets de l'espace choisi. Un pied de page rappelle les sources (Yahoo Finance pour les cours, BCE pour le taux sans risque) et que l'outil est pédagogique : il ne constitue pas un conseil en investissement.

### Si la barre latérale est masquée

Sur un écran étroit, la barre latérale peut être repliée. Le petit bouton en forme de flèche, en haut à gauche de la fenêtre, permet de la rouvrir.

## Passer le logiciel en anglais (ou revenir au français)
<!-- fiche: ecran-langue | questions: comment mettre le logiciel en anglais ; changer la langue ; switch to english ; le tableau de bord est en anglais comment remettre en francais ; ou est le bouton FR EN ; is there an english version ; le rapport pdf peut il etre en anglais ; pourquoi certains textes restent en français | mots: langue, anglais, français, English, traduction, language, FR, EN, bilingue -->

Le sélecteur de langue se trouve en haut de la barre latérale, à droite du nom du logiciel : cliquez sur **EN** pour l'anglais, sur **FR** pour le français. Le changement est immédiat, sans perdre le portefeuille ni les réglages en cours. Le français est la langue de départ.

### Ce qui change

- tous les intitulés, boutons, onglets, aides et commentaires du tableau de bord ;
- les données issues des calculs (régions, secteurs, classes d'actifs, noms de scénarios), traduites à l'affichage ;
- le format des nombres et des dates : en anglais, « €1,235 », « +12.34% » et « 16 Jan 2017 » ; en français, « 1 235 € », « +12,34 % » et « 16/01/2017 ».

### Ce qui reste en français

- **le rapport PDF**, toujours rédigé en français, quelle que soit la langue de l'écran ;
- les noms des titres et de vos portefeuilles, qui sont des noms propres ;
- le manuel, tant que sa version anglaise n'est pas installée avec votre version du logiciel : l'assistant et le sommaire utilisent alors le manuel français ;
- l'analyse en ligne de commande et les guides du dossier `docs`.

Un texte d'écran qui n'aurait pas encore de traduction s'affiche en français, sans erreur.

### Durée du choix

La langue est gardée pendant toute la session. Elle n'est pas enregistrée dans votre compte : à la prochaine ouverture du logiciel, il redémarre en français. Cliquer une seconde fois sur la langue déjà choisie ne change rien.

## Activer le mode nuit (fond sombre)
<!-- fiche: ecran-mode-nuit | questions: comment mettre le mode sombre ; dark mode ; l'écran est trop blanc ça fait mal aux yeux ; passer en mode nuit ; revenir en mode clair ; le mode nuit n'est pas gardé ; pourquoi le pdf est blanc alors que je suis en mode nuit ; mettre le fond en noir | mots: mode nuit, mode sombre, dark mode, thème, fond noir, bleu nuit, clair, affichage -->

Le sélecteur d'affichage se trouve en haut de la barre latérale, sous le sélecteur de langue : cliquez sur **Nuit** pour un fond bleu nuit, sur **Clair** pour revenir au fond blanc. Le mode clair est celui de départ.

### Ce qui change

- le fond de la page et de la barre latérale, les cartes de chiffres, les encadrés, les champs et les menus ;
- les graphiques : textes, grilles, bulles de survol et couleurs sombres des courbes sont remplacés par des teintes lisibles sur fond sombre ;
- les tableaux de données, dont les couleurs sont inversées pour rester lisibles.

### Le choix est mémorisé dans votre compte

Si vous êtes connecté à votre espace personnel, le mode choisi est enregistré dans vos préférences, chiffrées avec le reste de votre compte. À votre prochaine connexion, le logiciel le rétablit automatiquement. Sans compte, le choix ne vaut que pour la session en cours.

Pour que le mode soit enregistré, choisissez-le **après** vous être connecté.

### Le rapport PDF reste en clair

Le rapport PDF garde toujours un fond blanc, quel que soit le mode choisi à l'écran : il est conçu pour être imprimé.

## Les quatre espaces de travail et leur contenu
<!-- fiche: ecran-espaces | questions: c'est quoi les espaces de travail ; ou trouver la fiscalité ; ou est le backtest ; comment changer d'espace ; je ne trouve pas l'onglet risque ; quelle différence entre analyse conseil et gestion ; comment revenir à l'analyse depuis mon compte ; je suis bloqué sur la page ajouter des opérations ; le menu des espaces n'a rien de coché | mots: espace de travail, menu, navigation, onglets, Analyse du portefeuille, Conseil patrimonial, Gestion d'actifs, Manuel et aide, rubriques -->

Le menu **Espace de travail**, dans la barre latérale, propose quatre espaces. Cliquez sur l'un d'eux pour l'afficher ; ses onglets apparaissent en haut de la zone principale.

| Espace | Description dans le menu | Onglets |
|---|---|---|
| Analyse du portefeuille | Performance, risque, optimisation | Vue d'ensemble, Positions, Performance, Risque, Expositions, Optimisation, Projection, Transactions |
| Conseil patrimonial | Fiscalité, stress tests | Fiscalité, Stress tests |
| Gestion d'actifs | Attribution, budget de risque, backtest | Attribution de performance, Budget de risque, Backtest de stratégies |
| Manuel et aide | Mode d'emploi, formules, questions | Assistant « Poser une question », sommaire du manuel |

### Ce qui est commun

Les trois premiers espaces analysent le même portefeuille avec les mêmes paramètres. Ils affichent tous le bandeau bleu et les six chiffres clés en haut de page. Le logiciel s'ouvre sur « Analyse du portefeuille ».

L'espace « Manuel et aide » s'ouvre même si aucun portefeuille n'a pu être chargé : vous pouvez toujours y chercher de l'aide.

### Revenir à un espace depuis « Mon compte » ou « Ajouter des opérations »

Quand la page [[Mon compte]] ou la page [[Ajouter des opérations]] est ouverte, aucun espace n'est coché dans le menu. Un clic sur **n'importe quel espace**, y compris celui où vous étiez, ferme la page et affiche l'espace choisi. Vous pouvez aussi :

- cliquer de nouveau sur [[Mon compte]] pour refermer cette page ;
- utiliser le bouton [[Retour au tableau de bord]] de la page « Ajouter des opérations ».

## Choisir le portefeuille à analyser
<!-- fiche: ecran-choisir-portefeuille | questions: comment changer de portefeuille ; ou choisir mon portefeuille ; c'est quoi les portefeuilles d'exemple ; je ne vois pas mon portefeuille dans la liste ; mon espace devant le nom ça veut dire quoi ; la liste ne change pas quand je choisis un autre portefeuille ; comment revenir à l'exemple après avoir envoyé un fichier ; portefeuille par défaut au démarrage | mots: portefeuille, sélection, liste déroulante, exemple, Mon espace, démonstration, fichier, choix du portefeuille -->

Le portefeuille analysé se choisit dans le bloc **Données** de la barre latérale, avec la liste déroulante placée sous ce titre. Le logiciel analyse d'emblée le premier portefeuille de la liste.

### Ce que contient la liste

1. **Vos portefeuilles personnels**, si vous êtes connecté. Ils apparaissent en premier, classés par ordre alphabétique, et précédés de la mention « Mon espace · » (par exemple « Mon espace · PEA Boursorama »). Ils sont déchiffrés en mémoire au moment de l'analyse.
2. **Les portefeuilles d'exemple** livrés avec le logiciel, pour découvrir les fonctions sans vos propres données : « Portefeuille diversifié (multi-actifs) », proposé en premier, et « Portefeuille actions monde ». Le petit portefeuille « Portefeuille d'exemple » n'est proposé que s'il est le seul fichier d'exemple présent.

### Un fichier envoyé est prioritaire

Si un fichier figure dans la zone [[Envoyer un fichier (CSV, Excel ou PDF)]], c'est **lui** qui est analysé, quel que soit le choix de la liste. Pour revenir à un portefeuille de la liste, retirez le fichier envoyé en cliquant sur la croix à côté de son nom.

### Mon portefeuille n'est pas dans la liste

- Vérifiez que vous êtes connecté : sans connexion, seuls les exemples sont proposés.
- Un fichier envoyé sans être enregistré n'apparaît pas dans la liste. Pour le retrouver la prochaine fois, enregistrez-le dans votre espace avec le bouton [[Enregistrer]] qui apparaît sous la zone d'envoi une fois le fichier lu.

### Pour aller plus loin

L'envoi d'un fichier, l'assistant d'import et l'ajout de nouvelles opérations sont expliqués dans le chapitre consacré à l'import. La gestion de vos portefeuilles enregistrés (renommer, télécharger, supprimer) se fait sur la page [[Mon compte]].

## Où régler les paramètres d'analyse ?
<!-- fiche: ecran-parametres | questions: ou sont les parametres ; comment changer l'indice de référence ; je ne trouve pas le taux sans risque ; régler la var ; que veut dire la ligne parametres msci world 2,50 % var 95 % ; les paramètres sont ils enregistrés ; pourquoi tous les chiffres changent quand je modifie un paramètre ; réglages de l'analyse | mots: paramètres, réglages, settings, options, indice de référence, taux sans risque, VaR, niveau de confiance -->

Les paramètres d'analyse se trouvent dans le panneau **Paramètres** de la barre latérale, sous le bloc Données. Il est replié par défaut : cliquez sur son titre pour l'ouvrir.

### Le résumé dans le titre

Même replié, le titre du panneau rappelle les réglages en cours, par exemple :

`Paramètres · MSCI World · 2,50 % · VaR 95 %`

soit l'indice de référence, le taux sans risque annuel et le niveau de confiance de la VaR.

### Les trois réglages

| Réglage | Valeur de départ | Sert à |
|---|---|---|
| [[Indice de référence]] | MSCI World (ETF CW8, dividendes réinvestis) | Comparer la performance, calculer le bêta, l'alpha, la tracking error |
| [[Taux sans risque (% par an)]] | 2,50 % | Ratios de Sharpe et de Sortino, alpha de Jensen |
| [[Niveau de confiance de la VaR]] | 95 % | VaR et CVaR (perte d'un mauvais jour) |

Chacun fait l'objet d'une fiche détaillée dans ce chapitre.

### Effet d'un changement

Tout changement relance l'analyse : les chiffres clés, les onglets des trois espaces d'analyse et le rapport PDF utilisent les nouveaux réglages. Un rapport PDF déjà préparé avec les anciens réglages n'est plus proposé au téléchargement : il faut le préparer de nouveau.

### Durée des réglages

Les réglages sont gardés pendant la session, même si vous changez de portefeuille ou d'espace. Ils ne sont pas enregistrés dans votre compte : à la prochaine ouverture, les valeurs de départ reviennent.

## Choisir l'indice de référence : les 14 indices proposés
<!-- fiche: ecran-indice-reference | questions: quel indice de référence choisir ; c'est quoi le benchmark ; comparer mon portefeuille au cac 40 ; mettre le s&p 500 comme référence ; pourquoi le msci world par défaut ; liste des indices disponibles ; dividendes réinvestis ou hors dividendes quelle différence ; mon portefeuille est obligataire quel indice prendre ; peut on ajouter un autre indice | mots: indice de référence, benchmark, MSCI World, CAC 40, S&P 500, Euro Stoxx 50, ACWI, Nasdaq, obligations, €STR, comparaison -->

L'indice de référence sert de point de comparaison : courbe « portefeuille contre indice » en base 100, écart de performance, bêta, alpha, corrélation, tracking error, ratio d'information. Il se choisit dans le panneau **Paramètres**, menu [[Indice de référence]]. Chaque entrée du menu indique d'abord sa famille, puis son nom (par exemple « Actions · CAC 40 (hors dividendes) »).

### La liste complète

| Famille | Indice proposé | Ce qu'il représente |
|---|---|---|
| Actions | MSCI World (ETF CW8, dividendes réinvestis) | Grandes et moyennes capitalisations des pays développés. **Choix par défaut** |
| Actions | MSCI ACWI, monde avec émergents | Pays développés et émergents, dividendes réinvestis |
| Actions | S&P 500 (ETF ESE, dividendes réinvestis) | 500 grandes sociétés américaines |
| Actions | Nasdaq-100 | 100 grandes sociétés non financières du Nasdaq, très technologiques, dividendes réinvestis |
| Actions | Stoxx Europe 600 | 600 sociétés européennes, dividendes réinvestis |
| Actions | Euro Stoxx 50 (hors dividendes) | 50 grandes sociétés de la zone euro |
| Actions | CAC 40 (hors dividendes) | 40 grandes sociétés françaises |
| Actions | MSCI Marchés émergents | Actions des pays émergents, dividendes réinvestis |
| Obligations | Emprunts d'État zone euro (coupons réinvestis) | Dettes des États de la zone euro |
| Obligations | Obligations d'entreprises en euros (hors coupons) | Dettes des entreprises émises en euros |
| Monétaire | Monétaire €STR (intérêts réinvestis) | Placement au jour le jour au taux €STR de la BCE |
| Mixtes | Mixte prudent : 20 % actions monde / 80 % obligations € | Indice composite calculé par le logiciel |
| Mixtes | Mixte équilibré : 60 % actions monde / 40 % obligations € | Indice composite calculé par le logiciel |
| Mixtes | Mixte dynamique : 80 % actions monde / 20 % obligations € | Indice composite calculé par le logiciel |

### Comment l'indice est suivi

La plupart des indices sont suivis au moyen d'un ETF coté qui les réplique. Pour chacun, plusieurs codes sont prévus : le premier dont l'historique est disponible est utilisé (par exemple CW8.PA, sinon IWDA.AS pour le MSCI World).

### Dividendes réinvestis ou hors dividendes

Un ETF capitalisant réinvestit les dividendes : sa performance est « dividendes compris ». L'Euro Stoxx 50 et le CAC 40 sont des indices de prix, **hors dividendes** : ils désavantagent l'indice d'environ 3 % par an face à un portefeuille qui, lui, encaisse ses dividendes. Préférez un indice dividendes réinvestis pour une comparaison équitable.

### Quel indice choisir ?

Choisissez l'indice qui ressemble le plus à votre portefeuille : MSCI World pour des actions mondiales, CAC 40 ou Stoxx Europe 600 pour des actions françaises ou européennes, un indice mixte pour un portefeuille qui mêle actions et obligations.

Avec un indice obligataire ou monétaire, l'onglet Performance affiche un avertissement : le bêta, l'alpha et la corrélation mesurent la sensibilité à un marché d'actions et ont alors peu de sens. Comparez surtout les rendements et les volatilités.

### Limite

La liste est fixe : il n'est pas possible d'ajouter un autre indice depuis l'écran.

## Que sont les indices mixtes 20/80, 60/40 et 80/20 ?
<!-- fiche: ecran-indices-mixtes | questions: c'est quoi l'indice mixte 60 40 ; indice composite ça veut dire quoi ; mixte prudent équilibré dynamique ; comment est calculé l'indice mixte ; pourquoi rééquilibré chaque mois ; quel indice pour un portefeuille actions et obligations ; benchmark 60/40 | mots: indice mixte, composite, 60/40, 20/80, 80/20, rééquilibrage mensuel, allocation, prudent, équilibré, dynamique -->

Les trois indices de la famille « Mixtes » n'existent pas en bourse : le logiciel les **calcule** à partir de deux composantes.

| Indice | Actions monde | Obligations d'État € | Libellé court |
|---|---|---|---|
| Mixte prudent | 20 % | 80 % | Mixte 20/80 |
| Mixte équilibré | 60 % | 40 % | Mixte 60/40 |
| Mixte dynamique | 80 % | 20 % | Mixte 80/20 |

### Les composantes

- **Actions monde** : le MSCI World, suivi par le premier ETF disponible parmi CW8.PA, IWDA.AS et EUNL.DE ;
- **Obligations** : les emprunts d'État de la zone euro, suivis par DBXN.DE (coupons réinvestis), sinon EUNH.DE.

### Le calcul

L'indice part de 100. Chaque jour, sa valeur suit celle des deux composantes, chacune en proportion des parts détenues. À la **clôture du dernier jour de chaque mois**, les parts sont recalculées pour revenir exactement aux poids cibles (par exemple 60 % et 40 %) : c'est le rééquilibrage mensuel.

Exemple : un indice 60/40 vaut 100 en début de mois. Si les actions montent de 10 % et les obligations ne bougent pas, il vaut `60 × 1,10 + 40 = 106`. Les actions pèsent alors `66 / 106 ≈ 62,3 %`. En fin de mois, l'indice revient à 60 % d'actions (63,60) et 40 % d'obligations (42,40).

### Pourquoi les utiliser

Un portefeuille qui mêle actions et obligations comparé au seul MSCI World paraît toujours moins performant en hausse et moins risqué en baisse. Un indice mixte de même dosage donne une comparaison plus juste. Les trois dosages correspondent aux profils prudent, équilibré et dynamique.

### Limite

Le rééquilibrage est supposé gratuit et parfait, sans frais ni impôt.

## Quel taux sans risque utiliser ?
<!-- fiche: ecran-taux-sans-risque | questions: c'est quoi le taux sans risque ; pourquoi 2,50 % ; d'ou vient le taux sans risque ; changer le taux sans risque ; le taux sans risque change le sharpe ; faut il mettre le livret A ; taux bce estr ; taux sans risque constant sur toute la période | mots: taux sans risque, risk free rate, BCE, facilité de dépôt, €STR, Sharpe, Sortino, alpha, rendement sans risque -->

Le taux sans risque est le rendement d'un placement en euros considéré comme sans risque. Il se règle dans le panneau **Paramètres**, champ [[Taux sans risque (% par an)]].

### Valeur par défaut et source

La valeur de départ est **2,50 % par an** : le taux de la facilité de dépôt de la Banque centrale européenne (BCE), en vigueur depuis le 16/09/2026, comme le rappelle l'aide du champ. Le €STR, taux interbancaire au jour le jour, en est très proche.

### Ce qu'il modifie

- le **ratio de Sharpe** et le **ratio de Sortino**, qui mesurent le rendement obtenu au-delà de ce taux ;
- l'**alpha de Jensen** ;
- les calculs de l'espace Gestion d'actifs et du rapport PDF qui en dépendent.

Pour les calculs quotidiens, le taux annuel est converti en taux par jour de bourse :

`taux journalier = (1 + taux annuel)^(1/252) − 1`

Avec 2,50 % : `1,025^(1/252) − 1 ≈ 0,0098 %` par jour de bourse.

### Réglage

Le champ accepte de 0 % à 10 %, par pas de 0,25 point (les boutons + et −), ou toute valeur tapée au clavier.

### Limite à connaître

Le même taux est appliqué à **toute la période** analysée, alors qu'il a varié dans la réalité. Sur un historique long, le ratio de Sharpe est donc approximatif. Pour une étude sur une période ancienne, vous pouvez saisir le taux moyen de cette période.

## Régler le niveau de confiance de la VaR (90, 95 ou 99 %)
<!-- fiche: ecran-niveau-var | questions: changer le niveau de la var ; var 95 ou 99 laquelle choisir ; c'est quoi le niveau de confiance ; mettre la var à 99 % ; pourquoi la var augmente quand je passe à 99 ; ou régler la value at risk ; var 90 % | mots: VaR, value at risk, niveau de confiance, 95 %, 99 %, 90 %, CVaR, expected shortfall, perte maximale -->

La VaR (Value at Risk) indique la perte d'un mauvais jour. Son niveau de confiance se règle dans le panneau **Paramètres**, avec le curseur [[Niveau de confiance de la VaR]], qui propose trois valeurs : **90 %**, **95 %** (valeur de départ) et **99 %**.

### Ce que signifie le niveau

Avec une VaR à 95 % sur 1 jour, la perte ne dépasse ce montant que 5 % des jours, soit environ un jour de bourse sur vingt. À 99 %, elle n'est dépassée qu'un jour sur cent.

Pour la méthode historique, le logiciel prend le quantile des rendements quotidiens au seuil `1 − niveau` : le 5e centile à 95 %, le 1er centile à 99 %, le 10e centile à 90 %.

### Effet du réglage

Plus le niveau est élevé, plus on regarde loin dans les mauvais jours : la VaR et la CVaR **augmentent**. Le réglage s'applique à :

- la carte VaR et la carte CVaR de l'onglet Risque ;
- le tableau des VaR historique, loi normale et Cornish-Fisher ;
- le graphique de distribution des rendements ;
- le rapport PDF.

### Lequel choisir ?

95 % est l'usage le plus courant en gestion de portefeuille. 99 % est celui de la réglementation bancaire, plus exigeant. Sur un historique court, la VaR à 99 % repose sur très peu de jours : elle est moins fiable.

Le détail des méthodes de calcul de la VaR est expliqué dans le chapitre consacré au risque.

## Le bandeau en haut de page et la pastille « Cours en direct »
<!-- fiche: ecran-bandeau | questions: que veut dire cours en cache hors ligne ; pastille orange en haut à droite ; point vert cours en direct ; données au quelle date ; le bandeau bleu en haut ça indique quoi ; pourquoi mes cours ne sont pas à jour ; nombre de lignes dans le bandeau ; c'est quoi la date en haut à droite | mots: bandeau, en-tête, header, cours en direct, cours en cache, hors ligne, pastille, point vert, point orange, date des données -->

Dans les espaces d'analyse, la zone principale commence par un bandeau bleu.

### À gauche

- en petit : « Master G2C · Gestion de portefeuille » ;
- le titre « Suivi de portefeuille » ;
- une ligne de résumé : la période analysée (« Du 15/01/2024 au … »), le nombre de lignes détenues aujourd'hui et le nom court de l'indice de référence choisi.

### À droite : la provenance des cours

| Pastille | Signification |
|---|---|
| Point vert, « Cours en direct · Yahoo Finance » | Les derniers cours ont été téléchargés auprès de Yahoo Finance lors de l'analyse |
| Point orange, « Cours en cache (hors ligne) » | Yahoo Finance n'a pas répondu : le logiciel utilise les derniers cours enregistrés sur l'ordinateur |

Sous la pastille, la mention « Données au » donne la date du dernier cours de l'historique : c'est la date à laquelle le portefeuille est valorisé.

### Si la pastille est orange

Les calculs restent justes, mais à la date des derniers cours connus. Vérifiez votre connexion Internet, puis cliquez sur [[Actualiser les cours]] en bas de la barre latérale. La ligne « Cours » des informations de la barre latérale précise la date du cache utilisé.

### Bon à savoir

Les résultats d'une analyse sont gardés en mémoire pendant une heure. La pastille décrit la situation au moment de ce calcul : une pastille verte d'il y a quarante minutes ne garantit pas des cours de la dernière minute. Le bouton [[Actualiser les cours]] force un nouveau téléchargement.

## Les chiffres clés en haut de page
<!-- fiche: ecran-chiffres-cles | questions: que veulent dire les chiffres en haut ; c'est quoi les six cartes ; valeur actuelle comment est elle calculée ; gain total ça comprend les dividendes ; perf annualisée c'est quoi ; à quoi sert le point d'interrogation sur les cartes ; le chiffre sous la volatilité c'est quoi ; max drawdown en haut de page | mots: chiffres clés, KPI, indicateurs, cartes, valeur actuelle, gain total, performance annualisée, volatilité, Sharpe, max drawdown, synthèse | aller: Analyse du portefeuille/Vue d'ensemble | chiffres: valeur_actuelle, montant_investi, gain_total, twr_annualise, volatilite, sharpe, max_drawdown -->

Sous le bandeau, six cartes résument le portefeuille. Elles restent affichées dans les trois espaces d'analyse. Survolez le petit **?** à côté d'un intitulé pour lire sa définition.

| Carte | Grand chiffre | Ligne du dessous |
|---|---|---|
| Valeur actuelle | Quantité × dernier cours, pour chaque ligne détenue, en euros | « Investi au PRU » : le capital encore investi, au prix de revient |
| Gain total | Plus-values latentes + plus-values réalisées + dividendes | Pastille : gain rapporté au capital investi |
| Perf. annualisée | TWR annualisé (rendement pondéré par le temps) | Pastille : TWR total depuis le début |
| Volatilité | Écart-type des rendements quotidiens × √252 | Volatilité de l'indice de référence |
| Sharpe | (Rendement − taux sans risque) / volatilité | Sharpe de l'indice de référence |
| Max drawdown | Pire baisse depuis un plus haut | Date du point le plus bas |

### Lire les couleurs

Les pastilles sont vertes quand le chiffre est positif, rouges quand il est négatif, grises quand il est nul.

### Exemple

Un portefeuille dont le capital investi au PRU est de 10 000 € et dont le gain total est de 1 500 € affiche « +1 500 € » dans la carte Gain total, avec la pastille `1 500 / 10 000 = +15,00 %` sur le capital investi.

### Gain total et performance : pourquoi deux chiffres ?

Le gain total est un montant en euros, qui dépend de la somme investie et du moment des apports. La performance annualisée (TWR) neutralise les apports et retraits : elle mesure la qualité des choix de placement et se compare à l'indice. Les deux sont détaillés dans le chapitre sur la performance.

### Comparer avec l'indice

Pour la volatilité et le Sharpe, la ligne du dessous donne la valeur de l'indice de référence choisi dans les paramètres : vous voyez d'un coup d'œil si votre portefeuille est plus ou moins risqué, et mieux ou moins bien rémunéré pour ce risque.

## Obtenir le rapport PDF
<!-- fiche: ecran-rapport-pdf | questions: comment télécharger le rapport pdf ; generer un pdf de mon portefeuille ; le bouton rapport pdf ne télécharge rien ; ou est le rapport ; exporter l'analyse en pdf ; le bouton télécharger le rapport a disparu ; imprimer le rapport ; rapport pdf en anglais ; installer reportlab | mots: rapport PDF, export, imprimer, télécharger, synthèse, document, reportlab, compte rendu -->

Le rapport PDF rassemble l'analyse complète du portefeuille dans un document prêt à imprimer ou à transmettre.

### En deux temps

1. En bas de la barre latérale, cliquez sur [[Rapport PDF]]. Le message « Génération du rapport... » s'affiche pendant la préparation, qui peut prendre quelques secondes.
2. Le bouton devient [[Télécharger le rapport PDF]]. Cliquez dessus : le fichier est enregistré par votre navigateur, en général dans le dossier Téléchargements.

Le fichier s'appelle `rapport_portefeuille_` suivi de la date des dernières données, par exemple `rapport_portefeuille_20261006.pdf`.

### Le bouton de téléchargement a disparu

Le téléchargement n'est proposé que si le rapport correspond exactement aux réglages actuels. Si vous changez de portefeuille, d'indice de référence, de taux sans risque ou de niveau de VaR, le bouton [[Rapport PDF]] réapparaît : cliquez de nouveau pour préparer un rapport à jour.

### Toujours en français et en clair

Le rapport est rédigé en français même si l'écran est en anglais, et garde un fond blanc même en mode nuit.

### Réglages utilisés

Le rapport reprend le portefeuille, l'indice de référence, le taux sans risque et le niveau de VaR choisis. En revanche, pour l'optimisation et la projection, il utilise des réglages fixes, et non ceux des curseurs de l'écran : poids maximal de 30 % par titre, horizon de 10 ans, 5 000 scénarios, loi normale, sans versement mensuel.

### Où est le bouton ?

Il n'apparaît qu'une fois un portefeuille analysé, dans les espaces Analyse du portefeuille, Conseil patrimonial et Gestion d'actifs. Il est absent de l'espace « Manuel et aide » et des pages « Mon compte » et « Ajouter des opérations ».

### Message « Installer reportlab »

Ce message ne concerne que le lancement depuis le code source : la bibliothèque qui fabrique les PDF manque. Installez-la avec `python -m pip install reportlab`. Les versions Windows et Mac la contiennent déjà.

## Que contient le rapport PDF ?
<!-- fiche: ecran-rapport-contenu | questions: qu'y a-t-il dans le rapport pdf ; combien de pages fait le rapport ; le rapport contient il la fiscalité ; est ce que le rapport montre les positions ; plan du rapport pdf ; le rapport est il complet ; methodologie dans le pdf ; pourquoi l'optimisation n'est pas dans mon rapport | mots: rapport PDF, contenu, sommaire, pages, synthèse, positions, risque, méthodologie, annexe, plan -->

Le rapport est un document A4, découpé en parties qui commencent chacune sur une nouvelle page. Chaque page porte en pied la mention « Rapport de suivi de portefeuille », la date du jour, le rappel « Outil pédagogique, ne constitue pas un conseil en investissement » et le numéro de page.

### Les parties

1. **Synthèse** : bandeau avec la période, le nombre de lignes et l'indice de référence ; neuf chiffres clés (valeur actuelle, gain total, gain sur capital investi, TWR annualisé, TRI annuel, volatilité, Sharpe, max drawdown, VaR à 1 jour) ; graphique d'évolution ; montant investi, plus-values latentes et réalisées, dividendes, frais et source des cours.
2. **Positions détenues** : tableau des lignes (ticker, titre, quantité, PRU, cours, valeur, plus ou moins-value, poids), puis répartitions par classe d'actifs, région et secteur, en transparence.
3. **Expositions et diversification** : diagnostic par dimension (géographie, secteurs, devises, concentration, taux, diversification réelle), points à surveiller ou à corriger, corrélations entre les lignes.
4. **Performance** : comparaison avec l'indice, rendement par année civile, bêta, alpha, corrélation, tracking error et ratio d'information.
5. **Risque** : drawdown, volatilité, Sharpe, Sortino, les trois VaR, CVaR, distribution des rendements, asymétrie, kurtosis et test de Jarque-Bera.
6. **Optimisation de Markowitz** : frontière efficiente, portefeuilles de variance minimale et de Sharpe maximal, répartitions comparées.
7. **Projection** : simulation de Monte-Carlo à 10 ans, scénarios défavorable, médian et favorable, probabilité de perte, distribution de la valeur finale.
8. **Conseil patrimonial** : fiscalité d'une vente totale selon l'enveloppe (CTO, PEA, assurance-vie) et stress tests.
9. **Gestion d'actifs** : attribution de performance, budget de risque, backtest des stratégies de rééquilibrage et comparaison entre investir 10 000 € en une fois ou progressivement.
10. **Méthodologie** : définition de chaque indicateur et limites de l'analyse.

### Parties parfois absentes

Si un calcul est impossible (par exemple l'optimisation, avec trop peu de titres pour le poids maximal de 30 %), la partie correspondante est omise ou réduite. Le nombre de pages dépend donc du portefeuille.

## Actualiser les cours
<!-- fiche: ecran-actualiser-cours | questions: comment mettre à jour les cours ; les prix ne sont pas ceux d'aujourd'hui ; rafraichir les données ; le bouton actualiser les cours ne fait rien ; forcer le téléchargement des cours ; refresh ; les cours datent d'hier ; recharger la page | mots: actualiser, rafraîchir, refresh, mise à jour des cours, cache, recharger, cours du jour, Yahoo Finance -->

Le bouton [[Actualiser les cours]] se trouve tout en bas de la barre latérale, sous le bouton du rapport PDF.

### À quoi il sert

Pour rester rapide, le logiciel garde en mémoire les résultats de chaque analyse pendant **une heure**. Tant que ce délai n'est pas écoulé, il ne retélécharge pas les cours. Le bouton efface tous ces résultats en mémoire et relance la page : les cours sont téléchargés de nouveau auprès de Yahoo Finance et tous les calculs sont refaits.

### Quand l'utiliser

- la pastille du bandeau indique « Cours en cache (hors ligne) » et la connexion Internet est revenue ;
- vous laissez le logiciel ouvert longtemps et voulez les cours les plus récents ;
- un titre récemment ajouté n'avait pas encore de cours.

### Il faut Internet

Sans connexion, l'actualisation ne peut rien télécharger : le logiciel reprend les derniers cours enregistrés et la pastille reste orange.

### À savoir

- L'actualisation prend quelques secondes de plus que d'habitude, puisque tout est recalculé.
- Un rapport PDF déjà préparé n'est pas modifié : préparez-le de nouveau si vous voulez les derniers cours.

## Les informations en bas de la barre latérale
<!-- fiche: ecran-informations | questions: c'est quoi les infos en bas à gauche ; que veut dire 1 € en usd ; quelle période est analysée ; combien d'opérations a mon portefeuille ; d'ou viennent les cours ; ligne cours cache local du ; quel taux de change est utilisé ; fichier mis à jour dans la barre | mots: informations, fichier, période, opérations, source des cours, taux de change, devise, cache local, Yahoo Finance | chiffres: nb_operations -->

Une fois le portefeuille analysé, un petit bloc d'informations apparaît en bas de la barre latérale, au-dessus des boutons du rapport et de l'actualisation.

| Ligne | Contenu |
|---|---|
| Fichier | Le nom du portefeuille ou du fichier analysé. La mention « (mis à jour) » signale que des opérations lui ont été ajoutées pendant la session sans être enregistrées |
| Période | Première et dernière date de l'historique valorisé |
| Opérations | Le nombre d'opérations lues (achats, ventes, dividendes) |
| Cours | La provenance des derniers cours : « Yahoo Finance (en direct) », ou « cache local du » suivi de la date, avec la mention « Yahoo Finance injoignable » |
| 1 € en USD, 1 € en GBP… | Une ligne par devise étrangère du portefeuille : le taux de change du jour utilisé pour convertir les titres en euros, avec quatre décimales |

### Lire un taux de change

« 1 € en USD · 1,0850 » signifie qu'un euro vaut 1,0850 dollar. Une action cotée 200 USD vaut donc `200 / 1,0850 ≈ 184,33 €`. Un portefeuille entièrement en euros n'a aucune ligne de taux.

### Après l'envoi d'un fichier

Quand un fichier envoyé a été reconnu automatiquement, une note supplémentaire indique le nombre d'opérations et de titres reconnus, et signale par exemple qu'un PDF image a été lu par reconnaissance de caractères.

## Poser une question à l'assistant du manuel
<!-- fiche: ecran-assistant | questions: comment utiliser l'aide ; poser une question au logiciel ; l'assistant ne trouve pas ma réponse ; est-ce une intelligence artificielle ; l'aide fonctionne sans internet ; ou est le chatbot ; le bouton aller à ne m'ouvre pas le bon onglet ; pourquoi l'assistant affiche mes chiffres | mots: assistant, aide, question, recherche, FAQ, chatbot, manuel, hors connexion, Manuel et aide | aller: Manuel et aide -->

L'assistant se trouve dans l'espace **Manuel et aide**, tout en haut, dans le champ [[Poser une question]].

### Comment faire

1. Choisissez l'espace « Manuel et aide » dans la barre latérale.
2. Tapez votre question avec vos propres mots, par exemple « comment supprimer une opération ? », puis appuyez sur Entrée.
3. La fiche du manuel qui répond le mieux s'affiche en entier, avec le nom de son chapitre.

Trois exemples cliquables sont proposés sous le champ, comme [[Comment supprimer une opération ?]] ou [[Que veut dire le ratio de Sharpe ?]].

### Ce qui accompagne la réponse

- **Voir aussi** : jusqu'à trois autres fiches proches ; un clic ouvre la fiche.
- **Pour votre portefeuille** : certaines fiches affichent vos propres chiffres (par exemple votre ratio de Sharpe). Ce sont ceux du dernier portefeuille analysé pendant la session : affichez d'abord un espace d'analyse pour qu'ils soient disponibles.
- **Le bouton « Aller à »** : il ouvre l'espace concerné. Si la fiche porte sur un onglet précis, un message dans la barre latérale vous indique l'onglet à ouvrir, sur lequel il reste à cliquer.

### Ce n'est pas une intelligence artificielle

L'assistant ne rédige rien : il cherche dans le manuel la fiche la plus proche de votre question (mots du titre, formulations courantes, synonymes, texte) et l'affiche telle qu'elle est écrite. Il tolère les fautes de frappe et l'absence d'accents. Il fonctionne sans Internet et n'envoie rien.

### S'il ne trouve pas

Il l'indique et propose les fiches les plus proches. Essayez d'autres mots, plus simples ou plus techniques. Votre question est alors notée sur l'ordinateur pour compléter le manuel (voir la fiche sur les questions restées sans réponse).

## Parcourir le sommaire du manuel
<!-- fiche: ecran-sommaire-manuel | questions: ou est le manuel ; lire tout le manuel ; sommaire de l'aide ; telecharger le manuel en pdf ; manuel en word ; comment passer d'un chapitre à l'autre ; mode d'emploi du logiciel ; documentation complète | mots: manuel, sommaire, chapitres, mode d'emploi, documentation, guide utilisateur, fiches, Word, PDF | aller: Manuel et aide -->

Sous l'assistant, l'encadré **Sommaire du manuel** donne accès à tout le manuel. Son sous-titre indique le nombre de chapitres et de fiches.

### Comment le parcourir

1. Choisissez un chapitre dans la liste [[Chapitre]] (les chapitres sont numérotés dans l'ordre de lecture conseillé).
2. L'introduction du chapitre s'affiche, suivie de ses fiches, une par question.
3. Cliquez sur le titre d'une fiche pour la déplier, et de nouveau pour la replier.

Une fiche ouverte depuis « Voir aussi » est déjà dépliée dans le sommaire.

### Les éléments en gras

Dans les fiches, les noms de boutons, d'onglets ou de champs sont écrits en gras, exactement comme ils apparaissent à l'écran : cherchez-les tels quels.

### Télécharger le manuel complet

Quand votre version du logiciel est livrée avec le manuel exporté, des boutons « Manuel complet (Word) » et « Manuel complet (PDF) » apparaissent sous les fiches. Sinon, ces boutons sont absents et le manuel se consulte uniquement à l'écran.

### Langue

Le manuel s'affiche dans la langue de l'écran si sa traduction est installée, sinon en français.

## Les questions restées sans réponse et leur export
<!-- fiche: ecran-questions-sans-reponse | questions: ou sont les questions sans réponse ; exporter les questions non résolues ; ma question est elle envoyée quelque part ; comment aider à améliorer le manuel ; supprimer l'historique de mes questions ; fichier questions_sans_reponse.csv ; envoyer mes questions au professeur | mots: questions sans réponse, journal, export, CSV, amélioration du manuel, retour utilisateur, confidentialité | aller: Manuel et aide -->

Quand l'assistant ne trouve pas de réponse sûre, votre question est notée dans un fichier, **sur cet ordinateur uniquement**. Elle n'est jamais envoyée automatiquement.

### Les consulter

En bas de l'espace « Manuel et aide », un panneau replié intitulé « Questions restées sans réponse », suivi de leur nombre entre parenthèses, apparaît dès qu'au moins une question a été notée. Ouvrez-le pour voir les 30 plus récentes, avec leur date et leur heure.

### Les exporter

Le bouton [[Exporter les questions (CSV)]] télécharge le fichier complet, `questions_sans_reponse.csv`, avec deux colonnes : date et question. Transmettez-le au créateur du logiciel ou à votre enseignant : chaque question ajoutée au manuel améliore l'assistant.

### Détails

- Chaque question est limitée à 300 caractères.
- La même question tapée plusieurs fois de suite n'est notée qu'une fois.
- Le fichier est rangé dans le dossier `data` du logiciel, sous le nom `questions_sans_reponse.csv`. Le supprimer efface l'historique ; le logiciel n'a pas de bouton pour le faire.

## Astuces pour les graphiques : zoom, survol, légende
<!-- fiche: ecran-graphiques | questions: comment zoomer sur un graphique ; revenir au graphique entier après un zoom ; masquer une courbe ; afficher la valeur exacte d'un point ; le graphique est trop petit ; comment voir seulement la dernière année ; enregistrer le graphique en image ; je n'arrive pas à zoomer sur la carte | mots: graphique, zoom, survol, info-bulle, légende, double-clic, Plotly, période, 1M, 6M, YTD, interactif -->

Les graphiques du tableau de bord sont interactifs.

### Survoler pour lire les valeurs

Passez la souris sur une courbe, une barre ou un pays : une bulle affiche la valeur exacte. Sur les graphiques d'évolution, la bulle réunit toutes les courbes à la même date, ce qui permet de comparer d'un coup d'œil le portefeuille et l'indice, ou la valeur et le capital investi.

### Zoomer par cliquer-glisser

Cliquez et faites glisser la souris sur la zone qui vous intéresse : le graphique s'agrandit sur cette zone. Vous pouvez recommencer pour zoomer davantage.

### Revenir à la vue d'origine

**Double-cliquez** sur le graphique.

### Choisir une période

Les graphiques « Évolution du portefeuille » et la comparaison avec l'indice ont des boutons au-dessus de la courbe : **1M** (un mois), **6M** (six mois), **YTD** (depuis le 1er janvier), **1A** (un an) et **Tout**.

### Masquer ou isoler une courbe

Cliquez sur un nom dans la légende, sous le graphique, pour masquer la courbe correspondante ; cliquez de nouveau pour la réafficher. Un double-clic sur un nom de la légende n'affiche plus que cette courbe.

### Limites

- La carte du monde ne se zoome pas : le survol des pays reste possible.
- La barre d'outils des graphiques est masquée ; il n'y a donc pas de bouton pour enregistrer un graphique en image. Pour garder les graphiques, utilisez le rapport PDF ou une capture d'écran.
- Les graphiques s'adaptent à la largeur de la fenêtre : agrandissez-la ou repliez la barre latérale pour les voir plus grands.
