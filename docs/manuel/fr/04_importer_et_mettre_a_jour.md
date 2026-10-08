# Importer et mettre à jour son portefeuille
<!-- chapitre: import | ordre: 4 -->

Ce chapitre explique comment donner vos opérations au logiciel : quels fichiers il accepte (CSV, Excel, PDF), le format du projet et son modèle, la lecture automatique des exports de banque ou de courtier et des PDF (avis d'opéré, relevés, documents scannés ou protégés par un mot de passe, plusieurs fichiers à la fois), l'assistant d'import, la reconnaissance des titres (ticker, ISIN, nom, codes Bloomberg, Google ou Reuters) et des devises. Il décrit ensuite la mise à jour d'un portefeuille : ajout de nouvelles opérations, divisions d'actions, doublons, contrôles, correction ou suppression d'une opération, annulation. Il se termine par les erreurs fréquentes et un exemple complet.

## Quels fichiers peut-on importer dans le logiciel ?
<!-- fiche: import-fichiers-acceptes | questions: quels fichiers je peux importer ; quel format de fichier accepte le logiciel ; est-ce que je peux mettre un fichier excel ; ça prend les pdf de ma banque ; on peut importer un csv ; mon fichier xls ne passe pas ; est ce que je peux importer une capture d'écran ou une photo ; import depuis boursorama ou bourse direct ; le logiciel se connecte t il à mon courtier | mots: import, formats acceptés, CSV, Excel, xlsx, PDF, relevé, avis d'opéré, export courtier, fichier -->

Le logiciel lit vos opérations à partir d'un fichier que vous lui envoyez. Il ne se connecte ni à votre banque ni à votre courtier.

### Les trois formats acceptés

| Format | Extension | Exemples |
|---|---|---|
| CSV (texte) | `.csv` | Fichier au format du projet, export de courtier, fichier enregistré depuis Excel |
| Excel | `.xlsx` | Tableau personnel, export de banque |
| PDF | `.pdf` | Relevé d'opérations présenté en tableau, avis d'opéré (confirmation d'un ordre exécuté), relevé de portefeuille (positions et prix de revient), PDF protégé par un mot de passe |

Les zones d'envoi n'acceptent que ces trois extensions. Elles acceptent plusieurs fichiers à la fois (voir la fiche « Envoyer plusieurs fichiers d'un coup »). L'ancien format Excel `.xls` n'est pas accepté : ouvrez le fichier dans Excel et enregistrez-le en `.xlsx` ou en CSV. Le logiciel reconnaît la nature réelle du fichier à son contenu (un PDF commence par `%PDF-`, un `.xlsx` est une archive ZIP), puis le lit en conséquence.

### Ce que le fichier doit contenir

Il faut un **historique d'opérations datées** : achats, ventes, et éventuellement dividendes. Une simple liste de positions (titres et quantités détenues aujourd'hui, sans dates d'achat) ne permet pas de calculer les performances sur tout l'historique ; seule exception, un relevé de portefeuille PDF peut servir de portefeuille de départ, chaque position devenant un achat à la date du relevé (voir la fiche « Importer un relevé de portefeuille PDF »). Trois informations sont indispensables pour chaque ligne : la **date**, le **titre** et la **quantité**, ainsi que le **prix unitaire ou le montant total**.

### Le format n'a pas besoin d'être parfait

Le fichier peut avoir ses propres noms de colonnes, en français ou en anglais, des lignes de titre au-dessus du tableau, des codes ISIN au lieu des tickers, des nombres « à la française » ou des montants en euros pour des titres étrangers : la détection automatique s'en charge (voir les fiches suivantes). Si elle a un doute, l'assistant d'import s'ouvre.

### Ce qui n'est pas possible

- une photo ou une capture d'écran au format image (`.png`, `.jpg`) n'est pas acceptée ;
- un PDF scanné (ou dont le texte est « codé ») n'est lu automatiquement que si un moteur de reconnaissance de caractères est installé, et seulement pour des avis d'opéré (voir la fiche sur les PDF image) ; à défaut, un formulaire permet de compléter l'opération à la main (voir la fiche « Compléter une opération quand le PDF n'est pas reconnu ») ;
- il n'existe pas de connexion automatique à un compte bancaire.

## Que se passe-t-il quand j'envoie un fichier ?
<!-- fiche: import-envoyer-fichier | questions: comment importer mon portefeuille ; ou est le bouton pour envoyer mon fichier ; j'ai mis mon fichier et rien ne se passe ; comment charger mes transactions ; le fichier envoyé remplace t il mon portefeuille ; pourquoi l'assistant s'ouvre au lieu du tableau de bord ; comment revenir à mon portefeuille enregistré après un envoi ; upload fichier | mots: envoyer un fichier, upload, barre latérale, Données, import automatique, détection, glisser-déposer, chargement -->

### Où envoyer le fichier

Dans la barre latérale, rubrique « Données », utilisez la zone [[Envoyer un fichier (CSV, Excel ou PDF)]] : glissez-y le fichier ou cliquez pour le choisir. Vous pouvez y déposer plusieurs fichiers à la fois : leurs opérations sont réunies (voir la fiche « Envoyer plusieurs fichiers d'un coup »). Le fichier envoyé est **prioritaire** sur le portefeuille choisi dans la liste juste au-dessus : tant qu'il est présent dans la zone d'envoi, c'est lui qui est analysé.

### Ce que fait le logiciel

1. Le message « Lecture du fichier et vérification des prix avec les cours du marché... » s'affiche.
2. Le logiciel lit le fichier, reconnaît les colonnes, convertit les codes des titres en tickers Yahoo Finance et vérifie les prix avec les cours du marché.
3. **Si le résultat est sûr**, le portefeuille est analysé immédiatement. Un encadré dans la barre latérale résume ce qui a été compris, par exemple « Fichier reconnu automatiquement : 12 opération(s), 5 titre(s). ».
4. **S'il reste un doute** (colonne non reconnue, titre introuvable, ligne illisible), l'**assistant d'import** s'affiche à la place du tableau de bord, déjà pré-rempli : il suffit de vérifier et de valider.

Vous pouvez à tout moment reprendre la lecture à la main avec le bouton [[Ouvrir l'assistant d'import]], visible sous la zone d'envoi tant qu'un seul fichier y est présent. Un PDF protégé par un mot de passe affiche d'abord l'encadré [[PDF protégé]] (voir la fiche dédiée).

### Le fichier n'est pas conservé automatiquement

Un fichier envoyé n'est gardé que pendant la session. Pour le retrouver la prochaine fois :

- si vous êtes connecté, le bloc [[Enregistrer dans mon espace]] apparaît sous la zone d'envoi une fois le fichier analysé ;
- sinon, le logiciel rappelle : « Pour garder ce fichier, connectez-vous (« Se connecter », en haut de la barre latérale). ».

### Revenir à un autre portefeuille

Retirez le fichier de la zone d'envoi (petite croix à droite de son nom) : le portefeuille choisi dans la liste de la rubrique « Données » est de nouveau analysé.

## Le format du projet : quelles colonnes mettre dans mon fichier ?
<!-- fiche: import-format-projet | questions: quel est le format du fichier de transactions ; quelles colonnes faut il ; comment préparer mon fichier csv ; date type ticker nom quantite prix frais ; dans quelle devise mettre le prix ; les frais sont en euros ou en dollars ; c'est quoi le ticker yahoo ; format de date à utiliser ; je peux mettre des décimales dans la quantité | mots: format du projet, colonnes, en-tête, date, type, ticker, nom, quantite, prix, frais, devise de cotation, structure du fichier -->

Le format du projet est un fichier CSV à sept colonnes, une ligne par opération :

```
date,type,ticker,nom,quantite,prix,frais
2024-01-15,ACHAT,CW8.PA,Amundi MSCI World,10,420.00,2.50
2024-02-01,ACHAT,MC.PA,LVMH,3,780.00,2.00
2024-05-22,DIVIDENDE,MC.PA,LVMH,0,39.00,0.00
2024-09-18,VENTE,MC.PA,LVMH,1,700.00,2.00
```

### Signification de chaque colonne

| Colonne | Contenu |
|---|---|
| `date` | Date de l'opération, de préférence au format AAAA-MM-JJ. Un jour sans cotation est rattaché au jour de bourse suivant. |
| `type` | `ACHAT`, `VENTE` ou `DIVIDENDE` (voir la fiche sur les types d'opération) |
| `ticker` | Code du titre sur Yahoo Finance : `MC.PA` (LVMH à Paris), `AAPL` (Apple), `ULVR.L` (Unilever à Londres). Un code ISIN est aussi accepté à l'envoi : il est converti. |
| `nom` | Nom du titre, en texte libre (sert à l'affichage) |
| `quantite` | Nombre de titres achetés ou vendus ; 0 pour un dividende. Les fractions de parts sont acceptées. |
| `prix` | Prix unitaire, **dans la devise de cotation du titre** (dollars pour Apple, pence pour Londres) ; pour un dividende, montant total reçu |
| `frais` | Frais de courtage de l'opération, **toujours en euros** |

### Les deux règles de devise à retenir

- Le **prix** est dans la devise où le titre est coté sur Yahoo Finance. Le logiciel le convertit lui-même en euros au taux de change du jour de l'opération.
- Les **frais** sont toujours en euros, quel que soit le titre.

Si votre relevé donne des prix déjà convertis en euros, ce n'est pas grave : à l'envoi, le logiciel compare chaque prix au vrai cours du jour et reconvertit si nécessaire (voir la fiche sur les devises).

### Précisions utiles

- L'ordre des lignes est libre : le logiciel trie les opérations par date.
- Les quantités et les prix doivent être positifs : c'est le type qui indique le sens. Dans un export de courtier, une quantité négative est acceptée et rendue positive.
- Le point et la virgule sont acceptés comme séparateur décimal, et le point-virgule comme séparateur de colonnes (voir la fiche sur les exports de courtier).
- Le bouton [[Modèle de fichier]] de la barre latérale télécharge un exemple prêt à compléter.

## Achat, vente, dividende : que mettre dans le prix et les frais ?
<!-- fiche: import-types-operations | questions: comment saisir un dividende ; que mettre dans prix pour un dividende ; quantité zéro pour un dividende c'est normal ; achat vente dividende quels types sont acceptés ; comment noter un coupon d'obligation ; les frais sont ils inclus dans le prix ; comment le pru est calculé avec les frais ; comment saisir une vente ; dividende en dollars | mots: ACHAT, VENTE, DIVIDENDE, coupon, distribution, PRU, frais de courtage, montant total, type d'opération -->

Le format du projet ne connaît que trois types d'opération. Chacun utilise les colonnes de façon précise.

| Type | `quantite` | `prix` | `frais` |
|---|---|---|---|
| `ACHAT` | Nombre de titres achetés | Prix unitaire d'achat (devise de cotation) | Frais de courtage en euros |
| `VENTE` | Nombre de titres vendus (positif) | Prix unitaire de vente (devise de cotation) | Frais de courtage en euros |
| `DIVIDENDE` | 0 | **Montant total reçu** pour la ligne (devise de cotation) | Frais éventuels en euros (souvent 0) |

### Le cas du dividende

Pour un dividende, la colonne `prix` ne contient pas le dividende par action mais le **montant total** encaissé. Exemple : 3 actions LVMH avec un dividende de 13 € par action donnent la ligne `2024-05-22,DIVIDENDE,MC.PA,LVMH,0,39.00,0.00` (3 × 13 = 39). Le montant est lui aussi exprimé dans la devise de cotation : en dollars pour une action américaine, en pence pour une action de Londres. Le logiciel ajoute ce montant, diminué de la colonne `frais`, au total des dividendes du titre. Les coupons d'obligations et les distributions d'ETF se saisissent de la même façon.

### Comment les frais sont comptés

- **Achat** : les frais entrent dans le prix de revient unitaire. `Nouveau PRU = (quantité détenue × ancien PRU + quantité achetée × prix + frais) / nouvelle quantité`. Exemple : 3 LVMH achetées à 780 € avec 2 € de frais donnent un PRU de (3 × 780 + 2) / 3 = 780,67 €.
- **Vente** : les frais diminuent la plus-value réalisée. `Plus-value = quantité vendue × (prix de vente − PRU) − frais`.
- Les frais de toutes les opérations sont additionnés dans l'indicateur « Frais de courtage ».

### Une vente ne peut pas dépasser la quantité détenue

Vendre plus de titres que vous n'en possédez à cette date provoque une erreur à l'analyse (« Vente impossible le … »). Les ventes à découvert ne sont pas gérées.

### Les autres opérations

Frais de garde, virements, impôts ou opérations sur titres qui ne sont ni des achats, ni des ventes, ni des dividendes n'ont pas leur place dans le format du projet. Dans un export de courtier, ces lignes sont reconnues et ignorées (voir la fiche sur les types d'opération reconnus).

## Télécharger et remplir le modèle de fichier
<!-- fiche: import-modele | questions: ou trouver un modèle de fichier ; exemple de fichier csv à remplir ; modele_transactions.csv c'est quoi ; comment créer mon fichier de transactions dans excel ; je n'ai pas d'export de mon courtier comment faire ; template fichier transactions ; le modèle s'ouvre en une seule colonne dans excel ; télécharger un fichier exemple | mots: modèle de fichier, template, gabarit, exemple, modele_transactions.csv, Excel, saisie, CSV -->

### Où le trouver

Dans la barre latérale, rubrique « Données », cliquez sur [[Modèle de fichier]]. Le fichier `modele_transactions.csv` est téléchargé. Il contient l'en-tête du format du projet et quatre lignes d'exemple :

| date | type | ticker | nom | quantite | prix | frais |
|---|---|---|---|---|---|---|
| 2024-01-15 | ACHAT | CW8.PA | Amundi MSCI World | 10 | 420.00 | 2.50 |
| 2024-02-01 | ACHAT | MC.PA | LVMH | 3 | 780.00 | 2.00 |
| 2024-05-22 | DIVIDENDE | MC.PA | LVMH | 0 | 39.00 | 0.00 |
| 2024-09-18 | VENTE | MC.PA | LVMH | 1 | 700.00 | 2.00 |

### Comment l'utiliser

1. Ouvrez le fichier dans Excel, LibreOffice ou un éditeur de texte.
2. Remplacez les lignes d'exemple par vos propres opérations, en gardant la première ligne (les noms de colonnes).
3. Enregistrez, au choix, en CSV (séparateur virgule ou point-virgule) ou en classeur Excel `.xlsx`.
4. Envoyez le fichier avec la zone [[Envoyer un fichier (CSV, Excel ou PDF)]].

### Conseils de saisie

- Trouvez le ticker de chaque titre sur Yahoo Finance (par exemple `MC.PA` pour LVMH à Paris). Si vous ne le connaissez pas, vous pouvez écrire le code ISIN dans la colonne `ticker` : il sera converti à l'envoi.
- Écrivez les dates au format AAAA-MM-JJ ou JJ/MM/AAAA ; les deux sont reconnus.
- Excel réenregistre souvent les nombres avec une virgule décimale et un point-virgule entre les colonnes : le logiciel accepte ces deux variantes.
- Si, à l'ouverture dans Excel, tout apparaît dans la première colonne, ce n'est pas un problème pour le logiciel : une ligne entière placée entre guillemets dans la colonne A est également reconnue.

### Pas de fichier du tout ?

Vous pouvez aussi partir d'un portefeuille d'exemple et y saisir vos ordres à la main avec [[Ajouter des opérations]], puis télécharger le fichier obtenu (voir les fiches sur la saisie manuelle et sur l'utilisation sans compte).

## Importer l'export de ma banque ou de mon courtier
<!-- fiche: import-export-courtier | questions: comment importer l'export de mon courtier ; mon fichier a des noms de colonnes en anglais ; les colonnes ne s'appellent pas comme dans le modèle ; export degiro boursorama trade republic ça marche ; mon csv a des points virgules ; il y a des lignes de titre avant le tableau ; quels noms de colonnes sont reconnus ; fichier excel avec plusieurs feuilles ; accents bizarres dans mon fichier | mots: export courtier, relevé, colonnes, synonymes, séparateur, point-virgule, tabulation, encodage, feuille Excel, en-tête, noms de colonnes -->

Un export de courtier n'a pas besoin d'être transformé avant l'envoi. Le logiciel le lit tel quel, en quatre temps : lecture du tableau, reconnaissance des colonnes, conversion des titres, vérification des devises.

### Lecture du tableau

- **Séparateur** : pour un CSV, le logiciel compte, sur les 40 premières lignes non vides, les points-virgules, virgules, tabulations et barres verticales `|`, et retient le plus fréquent.
- **Encodage** : le texte est lu en UTF-8 ; à défaut, en Windows-1252 (l'encodage des anciennes versions d'Excel), ce qui préserve les accents.
- **Feuille Excel** : si le classeur a plusieurs feuilles, celle qui contient le plus de cellules remplies est choisie (le tableau des opérations plutôt qu'une feuille de notes). L'assistant permet d'en choisir une autre.
- **Ligne des titres de colonnes** : parmi les 30 premières lignes, le logiciel retient la plus remplie qui contient au moins 60 % de texte. Les lignes au-dessus (« Relevé des opérations », numéro de compte, date d'édition) sont ignorées. Si cette ligne contient une date ou un code ISIN, c'est qu'il n'y a pas de ligne de titres : les colonnes sont alors nommées « Colonne 1 », « Colonne 2 »… et reconnues par leur contenu.
- **Ce qui est écarté** : les lignes vides, les lignes sans date ni titre (ligne « Total », note sous le tableau), et un petit tableau placé à côté du tableau principal s'il en est séparé par une colonne vide.

### Noms de colonnes reconnus

Les noms sont comparés sans accents ni majuscules. Un nom est reconnu s'il est identique à l'un des noms ci-dessous, ou s'il commence par l'un d'eux suivi d'un espace (« Quantité exécutée », « Cours (EUR) »).

| Information | Exemples de noms reconnus |
|---|---|
| Date | date, date opération, date d'exécution, date de valeur, trade date, transaction date, execution date, jour |
| Type | type, opération, sens, nature, transaction type, side, action, mouvement |
| Titre | ticker, symbole, symbol, code, isin, code isin, bloomberg, bbg, ric, code reuters, valeur, titre, instrument, produit, product, security |
| Nom | nom, name, libellé, désignation, nom du titre, security name, description |
| Quantité | quantité, qté, qty, quantity, nombre, nombre de titres, nb titres, parts, shares, units |
| Prix unitaire | prix, prix unitaire, cours, cours d'exécution, price, unit price, execution price |
| Montant total | montant, montant net, montant brut, montant total, total, amount, net amount, montant en eur |
| Frais | frais, frais de courtage, courtage, commission, commissions, fees, fee, frais totaux |
| Devise | devise, currency, monnaie, devise de cotation, ccy, cur |
| Place | place, place de cotation, marché, bourse, exchange, market, mic, venue, lieu d'exécution |

Les colonnes nommées commentaire, remarque, note, observation, memo ou info ne sont jamais interprétées. Toutes les autres colonnes inutiles sont simplement ignorées.

### Et si les noms ne disent rien ?

Les colonnes sont aussi reconnues par leur **contenu** et par la **cohérence des chiffres** (voir la fiche suivante). Un fichier sans ligne de titres, ou aux colonnes nommées « A, B, C », peut donc être compris quand même.

## Comment le logiciel reconnaît-il les colonnes de mon fichier ?
<!-- fiche: import-detection-colonnes | questions: comment marche la détection automatique ; comment le logiciel devine les colonnes ; mon fichier n'a pas de ligne de titres ; il a confondu le prix et le montant ; pourquoi il dit sans certitude sur les quantités prix et montants ; quand est-ce que l'import est considéré comme sûr ; reconnaissance par le contenu ; qté x prix = montant | mots: détection automatique, correspondance des colonnes, contenu, cohérence, quantité × prix, montant, confiance, sans en-tête, algorithme -->

La détection automatique propose, pour chaque information (date, type, titre, nom, quantité, prix unitaire, montant total, frais, devise, place), la colonne du fichier qui lui correspond. Chaque colonne n'est utilisée qu'une fois.

### Étape 1 : les noms et le contenu

Pour la date, le type, le titre, le nom et la devise, le logiciel combine le nom de la colonne et ce qu'elle contient :

| Information | Indice tiré du contenu |
|---|---|
| Date | cases écrites comme des dates (15/01/2024, 2024-01-15…) et lisibles |
| Titre | codes ISIN dont la clé de contrôle est juste, codes Bloomberg, Google ou Reuters, tickers courts en majuscules |
| Type | mots d'opération (« Achat », « Vente », « Coupon »…), avec peu de valeurs différentes |
| Devise | codes EUR, USD, GBP, GBX, CHF, JPY, CAD, AUD, HKD, DKK, SEK, NOK, CNY, SGD |
| Nom | texte libre assez long, qui n'est ni un code, ni un type, ni une devise |

Une colonne de nombres (quantité, prix, montant, frais) n'est retenue sur son nom que si au moins 60 % de ses cases sont des nombres.

### Étape 2 : la cohérence des chiffres

Les colonnes de nombres restées sans nom parlant sont départagées par le calcul. Le logiciel essaie les combinaisons possibles et garde celle où, le plus souvent :

`quantité × prix ± frais = montant` (à 1 % près)

Il favorise aussi une quantité en nombres entiers, et des frais petits par rapport au montant (moins de 5 %).

Exemple : dans un fichier sans titres de colonnes contenant `3 ; 740.00 ; 2222.00 ; 2.00`, seule la lecture « 3 titres à 740 € plus 2 € de frais = 2 222 € » tombe juste : la première colonne est la quantité, la deuxième le prix, la troisième le montant, la quatrième les frais.

### Quand le résultat est-il jugé sûr ?

L'analyse démarre directement si toutes ces conditions sont réunies :

- la date, le titre, la quantité, et le prix ou le montant ont une colonne ;
- les colonnes de nombres ont un nom reconnu (quantité, et prix ou montant), **ou** la relation quantité × prix ± frais = montant est vérifiée sur au moins 80 % des lignes ;
- la colonne de date a un nom reconnu, ou au moins 90 % de ses cases sont des dates ;
- tous les titres ont été identifiés ;
- aucune ligne n'est illisible (date, prix, quantité ou titre manquant).

Sinon, l'assistant d'import s'ouvre ; le volet « Pourquoi l'assistant s'ouvre-t-il ? » donne la raison, par exemple « Colonnes reconnues, mais sans certitude sur les quantités, prix et montants. ».

## Quels formats de dates et de nombres sont reconnus ?
<!-- fiche: import-dates-nombres | questions: format de date accepté ; mes dates sont au format americain ; le logiciel inverse le jour et le mois ; 03/04/2024 c'est le 3 avril ou le 4 mars ; nombres avec virgule ou point ; 1 234,50 est ce que ça passe ; montant entre parenthèses négatif ; date illisible pourquoi ; symbole euro dans les montants | mots: format de date, JJ/MM/AAAA, MM/JJ, ISO, jour/mois, séparateur décimal, virgule, milliers, nombres négatifs, date illisible -->

### Les dates

Formats reconnus : `2024-01-15`, `15/01/2024`, `15-01-2024`, `15.01.2024`, ainsi que les dates suivies d'une heure (`2024-01-15 00:00:00`, ou `2024-01-15T10:30`). Les dates de cellules Excel au format date sont lues directement.

**Jour/mois ou mois/jour ?** Pour une date comme 03/04/2024, le logiciel examine toute la colonne :

- si une seule date a un premier nombre supérieur à 12 (par exemple 13/04/2024), le format est jour/mois (français) ;
- si une date a un deuxième nombre supérieur à 12 (04/13/2024), le format est mois/jour (américain) ;
- si rien ne permet de trancher, le format jour/mois est retenu, et le résumé l'indique : « Dates lues au format jour/mois (JJ/MM). ». Un format américain détecté est signalé par « Dates lues au format américain (MM/JJ). ».

Les dates écrites en toutes lettres (« 15 janv. 2024 ») ne sont pas reconnues : la ligne est alors signalée avec le motif « date illisible ». Préférez aussi les années à quatre chiffres.

### Les nombres

Le logiciel retire les espaces (y compris insécables), les apostrophes et les symboles €, $, £, EUR et USD, puis interprète le séparateur décimal :

| Écrit dans le fichier | Lu comme |
|---|---|
| `1 234,50 €` | 1234,5 |
| `1.234,50` | 1234,5 (le dernier séparateur est le décimal) |
| `1,234.50` | 1234,5 |
| `1.234.567` ou `1,234,567` | 1234567 |
| `(12,5)` | −12,5 |
| `12,50-` | −12,5 |

Attention à un cas ambigu : un nombre ne contenant qu'un seul séparateur est toujours lu comme un nombre décimal. `1,234` et `1.234` valent donc 1,234, et non mille deux cent trente-quatre. Si votre export écrit les milliers ainsi, vérifiez les quantités et les montants lus.

### Le signe

Le signe d'une quantité sert à repérer les ventes quand le fichier n'a pas de colonne de type ; il est ensuite retiré. Les frais sont toujours rendus positifs.

## Quels types d'opération sont reconnus dans un relevé ?
<!-- fiche: import-types-reconnus | questions: achat comptant est il reconnu ; comment le logiciel sait si c'est un achat ou une vente ; mon fichier n'a pas de colonne type ; les frais de garde sont ils importés ; lignes ignorées à l'import pourquoi ; virement dans mon relevé ; quantité négative c'est une vente ; buy sell en anglais ; rachat de parts | mots: type d'opération, achat, vente, dividende, coupon, souscription, rachat, buy, sell, lignes ignorées, frais de garde, virement -->

### Les mots reconnus

Chaque valeur de la colonne de type est classée d'après les mots qu'elle contient (sans tenir compte des accents ni des majuscules) :

| Classé comme | Mots reconnus |
|---|---|
| Achat | achat, buy, bought, purchase, souscription, acquisition, acheté |
| Vente | vente, sell, sold, sale, cession, vendu, rachat |
| Dividende | dividende, dividend, coupon, distribution, détachement, revenu |
| Ignoré | toute autre valeur : frais de garde, virement, taxe, impôt… |

Ainsi « Achat Comptant » est un achat, « Coupons/Dividende » un dividende, et « Rachat » une vente (le rachat de parts d'un fonds).

### Les lignes ignorées

Les lignes d'un autre type ne sont pas des erreurs : elles ne concernent pas un titre et sont écartées. Le résumé l'indique, par exemple « 2 ligne(s) ignorée(s) (frais de garde, virements...). ». Dans l'assistant, vous pouvez changer l'interprétation de chaque valeur (étape 3).

### Sans colonne de type

Si le fichier n'a pas de colonne de type, le logiciel décide d'après la quantité :

- quantité positive : achat ;
- quantité négative : vente ;
- quantité nulle ou vide avec un montant : dividende.

L'assistant le rappelle : « Sans colonne « Type d'opération » : une quantité négative est lue comme une vente, une quantité positive comme un achat. ».

### Dans un avis d'opéré PDF

Le sens est cherché dans le texte (achat, vente, souscription, rachat, buy, sell, dividende, coupon…). Une lecture par les intitulés n'est acceptée que si l'un de ces mots est écrit dans le document. Pour un avis lu par son contenu, le sens doit aussi être trouvé (un mot, ou une quantité précédée de + ou −). Un avis dont le sens n'est écrit qu'en code (« Sens : S ») peut être lu grâce à un modèle appris. Sinon, le formulaire [[Compléter l'opération]] vous fait choisir le sens.

## Mon relevé donne le montant total et pas le prix unitaire
<!-- fiche: import-montant-prix | questions: mon fichier n'a pas de prix unitaire seulement le montant ; comment le prix est calculé à partir du montant ; montant net ou montant brut lequel choisir ; le montant total inclut les frais ; le prix calculé est faux ; débit crédit au lieu du prix ; le prix unitaire ne tombe pas juste | mots: montant total, montant net, montant brut, prix unitaire, frais inclus, déduction du prix, débit, crédit -->

Le prix unitaire n'est pas obligatoire : une colonne de montant total suffit. Le logiciel en déduit le prix.

### Le calcul

Si le montant est **net** (frais compris, c'est-à-dire la somme réellement débitée ou créditée), ce qui est le réglage par défaut :

- achat : `prix = (montant − frais) / quantité` ;
- vente : `prix = (montant + frais) / quantité`.

Si le montant est **brut** (hors frais) : `prix = montant / quantité`.

Exemple : achat de 3 LVMH, montant net débité 2 222 €, frais 2 € : prix = (2 222 − 2) / 3 = 740 €. Pour une vente d'une LVMH avec 698 € crédités et 2 € de frais : prix = (698 + 2) / 1 = 700 €.

### Le réglage dans l'assistant

À l'étape 2 de l'assistant, dès qu'une colonne est associée au « Montant total », la case [[Le montant total inclut les frais (montant net débité ou crédité)]] apparaît, cochée par défaut. Décochez-la si votre colonne de montant est hors frais. L'import automatique, lui, considère toujours le montant comme net.

### Prix et montant tous les deux présents

Le prix unitaire du fichier est alors utilisé tel quel ; le montant sert seulement à vérifier la cohérence des colonnes et, pour un dividende, à connaître la somme reçue.

### Pour un dividende

La quantité est mise à 0 et le montant total est placé dans la colonne prix, comme le veut le format du projet. Sans colonne de montant, le logiciel prend prix × quantité.

### Si le prix ne tombe pas juste

Vérifiez dans l'assistant que la bonne colonne est associée au montant (net ou brut, débit ou crédit) et que la case des frais correspond à votre relevé. Une fois le portefeuille analysé, un prix peut aussi être corrigé dans l'onglet Transactions.

## L'assistant d'import étape par étape
<!-- fiche: import-assistant | questions: comment utiliser l'assistant d'import ; à quoi sert l'assistant d'import ; l'assistant s'est ouvert que dois je faire ; comment changer la colonne reconnue ; corriger la ligne des titres de colonnes ; choisir la feuille excel ; analyser ce portefeuille ne marche pas ; télécharger le fichier converti ; ouvrir l'assistant manuellement | mots: assistant d'import, correspondance des colonnes, étapes, feuille Excel, ligne des titres, interprétation, ticker Yahoo Finance, fichier converti, validation -->

L'assistant s'affiche à la place du tableau de bord quand la détection automatique a un doute, ou quand vous cliquez sur [[Ouvrir l'assistant d'import]]. Si l'ouverture est automatique, le volet [[Pourquoi l'assistant s'ouvre-t-il ?]] en donne la raison. Il comporte quatre étapes, toutes pré-remplies.

### 1. Le fichier

- [[Feuille Excel]] : uniquement pour un classeur à plusieurs feuilles.
- [[Ligne des titres de colonnes]] : numéro de la ligne du fichier qui contient les noms des colonnes, détecté automatiquement. Mettez 0 si le fichier n'a pas de ligne de titres.
- Un aperçu montre les huit premières lignes et le nombre total de lignes.

### 2. Correspondance des colonnes

Pour chaque information, un menu indique la colonne de votre fichier qui la contient : [[Date de l'opération]], [[Type d'opération]], [[Titre (ticker, ISIN ou nom)]], [[Nom du titre]], [[Quantité]], [[Prix unitaire]], [[Montant total]], [[Frais]], [[Devise]], [[Place de cotation]]. Les champs marqués d'un astérisque sont obligatoires ; choisissez « — aucune — » pour une information absente. Pour le prix, une colonne « Prix unitaire » ou « Montant total » suffit. Si un champ obligatoire manque, l'assistant s'arrête et indique ce qui reste à faire.

### 3. Types d'opération et titres

- À gauche (si une colonne de type est associée), chaque valeur distincte du fichier, son nombre de lignes et son [[Interprétation]] : Achat, Vente, Dividende ou [[Ignorer la ligne]]. Modifiez au besoin.
- À droite, chaque titre du fichier, le [[Ticker Yahoo Finance]] proposé (modifiable, par exemple `MC.PA` pour LVMH à Paris), le [[Nom trouvé]] et le [[Statut]] : « tel quel », « converti (Bloomberg, Google, Reuters) », « trouvé » ou « introuvable ». Pour un titre introuvable, saisissez son ticker à la main, sinon ses lignes risquent d'être ignorées.

### 4. Résultat

- [[Devise des prix du fichier]] : [[Détection automatique (recommandé)]], [[Devise de cotation de chaque titre]] ou [[Tout est en euros]] (voir la fiche sur les devises).
- Des notes signalent les lignes ignorées, les conversions de devise et les prix éloignés du cours du jour.
- Le tableau montre les transactions au format du projet.

Cliquez enfin sur [[Analyser ce portefeuille]]. Le bouton [[Télécharger le fichier converti (format du projet)]] enregistre le résultat sous le nom `transactions_converties.csv` : renvoyé plus tard, ce fichier est lu directement.

### Bon à savoir

Le fichier converti est mémorisé pour la session : renvoyer le même fichier ne rouvre pas l'assistant. Connecté, enregistrez-le avec [[Enregistrer dans mon espace]] pour ne pas refaire ces étapes.

## Comment le logiciel trouve-t-il le ticker d'un titre (ISIN, nom) ?
<!-- fiche: import-identifier-titres | questions: mon fichier a des codes isin au lieu des tickers ; comment convertir un isin en ticker ; je ne connais pas le ticker yahoo ; c'est quoi un ticker yahoo finance ; le logiciel a choisi la mauvaise bourse ; pourquoi mon titre est coté à francfort et pas à paris ; recherche par nom de société ; isin d'un etf irlandais | mots: ticker, ISIN, Yahoo Finance, identification des titres, recherche, place de cotation, nom de société, conversion, suffixe .PA -->

Le logiciel a besoin, pour chaque titre, de son **ticker Yahoo Finance**, c'est-à-dire le code qui permet de télécharger ses cours : `MC.PA` (LVMH, Paris), `AAPL` (Apple, New York), `SAP.DE` (SAP, Xetra), `ULVR.L` (Unilever, Londres). Le suffixe indique la place de cotation (.PA Paris, .DE Xetra, .AS Amsterdam, .MI Milan, .L Londres, .SW Suisse, aucun suffixe pour les États-Unis).

### Ce que vous pouvez mettre dans la colonne du titre

| Forme | Exemple | Traitement |
|---|---|---|
| Ticker Yahoo | `MC.PA`, `AAPL` | Utilisé tel quel |
| Code ISIN | `FR0000121014` | Recherché (voir ci-dessous) |
| Nom de société | `Air Liquide` | Recherché |
| Code Bloomberg, Google, Reuters | `MC FP`, `EPA:MC`, `AAPL.O` | Traduit sans connexion (voir la fiche dédiée) |
| Ticker sans place | `MC`, `AIR`, `TSLA` | Place retrouvée grâce aux cours (voir la fiche dédiée) |

Un code de 12 caractères commençant par deux lettres et finissant par un chiffre est traité comme un ISIN ; sa clé de contrôle (algorithme de Luhn) est vérifiée lors de la reconnaissance des colonnes et dans les PDF.

### L'ordre de recherche d'un ISIN ou d'un nom

1. **Hors connexion d'abord** : la table intégrée des ISIN d'ETF courants, puis celle des actions du CAC 40 et des grandes valeurs américaines, puis la mémoire des titres déjà reconnus, puis la base locale de titres (par ticker, par ISIN, ou par nom).
2. **Sinon, le moteur de recherche de Yahoo Finance** (Internet nécessaire), avec l'ISIN puis, si le fichier en contient un, le nom du titre.

Parmi les réponses, seuls les actions, ETF, fonds et indices sont retenus, et la cotation préférée est celle de la **Bourse du pays de l'ISIN** : FR → Paris, DE → Xetra puis Francfort, NL → Amsterdam, IT → Milan, ES → Madrid, GB → Londres, CH → Suisse, US → New York, etc. Pour un ISIN irlandais (IE) ou luxembourgeois (LU), typique des ETF, une cotation en euros est privilégiée (Paris, Xetra, Amsterdam, Milan), puis Londres et New York.

### La réponse est mémorisée

Un titre trouvé en ligne est retenu dans la mémoire locale : la fois suivante, il est reconnu immédiatement, même sans Internet.

### Si la place choisie ne vous convient pas

Dans l'assistant (étape 3), remplacez le ticker proposé, par exemple `SAP.DE` par un autre ticker du même titre. Le choix de la place change la devise et les cours utilisés, pas la quantité détenue.

## Codes Bloomberg, Google Finance, Reuters et colonne « Place »
<!-- fiche: import-codes-bloomberg | questions: mon fichier contient des tickers bloomberg ; MC FP equity c'est reconnu ; code reuters ric accepté ; format EPA:MC de google finance ; j'ai une colonne place de cotation ; code mic xpar ; convertir un ticker bloomberg en yahoo ; AAPL US Equity | mots: Bloomberg, Google Finance, Reuters, RIC, code MIC, place de cotation, XPAR, FP, EPA, yellow key, Equity, conversion de ticker -->

Les codes de titres utilisés par les terminaux professionnels sont traduits en tickers Yahoo Finance **sans connexion**, grâce à une table des codes de place intégrée au logiciel.

### Exemples de traduction

| Source | Écrit dans le fichier | Devient |
|---|---|---|
| Bloomberg | `MC FP`, `MC FP Equity` | MC.PA |
| Bloomberg | `AAPL US Equity` | AAPL |
| Bloomberg | `SAP GY` | SAP.DE |
| Bloomberg | `700 HK` | 0700.HK (complété à 4 chiffres) |
| Bloomberg | `BRK/B US` | BRK-B |
| Google Finance | `EPA:MC`, `NASDAQ:AAPL` | MC.PA, AAPL |
| Forme inversée | `MC:EPA`, `MC:FP` | MC.PA |
| Reuters (RIC) | `AAPL.O` | AAPL |
| Reuters (RIC) | `NESN.S` | NESN.SW |

Pour Bloomberg, le mot `Equity` (la « yellow key ») est facultatif. Les codes de place Bloomberg reconnus incluent notamment FP (Paris), GY et GR (Xetra), NA (Amsterdam), IM (Milan), SM (Madrid), LN (Londres), SW (Suisse), US, UN, UW et UQ (États-Unis), JP (Tokyo), CN (Toronto), HK (Hong Kong). Côté Reuters, les suffixes .O, .N, .OQ, .A, .P et .K renvoient aux États-Unis, .S et .VX à la Suisse, .MA à Madrid et .I à Dublin.

Limite : un code Reuters dont le suffixe est identique à celui de Yahoo (par exemple `LVMH.PA`) est pris tel quel, alors que le ticker Yahoo de LVMH est `MC.PA`. Corrigez-le dans l'assistant si le titre n'a pas de cours.

### Une colonne « Place » séparée

Si le fichier donne le ticker sans place dans une colonne et la place dans une autre (colonne nommée place, marché, bourse, exchange, MIC…), les deux sont assemblés : `MC` + `XPAR` donne `MC.PA`. La place peut être écrite :

- en code MIC : XPAR, XETR, XAMS, XMIL, XLON, XSWX, XNAS, XNYS… ;
- en code Bloomberg ou Google : FP, GY, EPA, ETR, LON… ;
- en toutes lettres : Euronext Paris, Paris, Xetra, Francfort, Amsterdam, Milan, Londres, London, Zurich, New York, Tokyo, Toronto…

Le résumé de l'import indique combien de codes ont été convertis : « … code(s) ISIN, Bloomberg ou nom(s) convertis en tickers. ».

## Mon fichier donne un ticker sans place de cotation (MC, AIR, TSLA)
<!-- fiche: import-ticker-sans-place | questions: mon fichier contient MC au lieu de MC.PA ; ticker sans suffixe ; le logiciel a pris moelis au lieu de lvmh ; comment il devine la bourse d'un ticker court ; AIR c'est airbus ou autre chose ; tickers courts sans .PA ; mauvais titre reconnu à l'import | mots: ticker court, ticker nu, sans suffixe, place de cotation, reconnaissance par les prix, homonyme, MC, Moelis, LVMH -->

Beaucoup de fichiers écrivent `MC` pour LVMH ou `AIR` pour Airbus, sans indiquer la Bourse. Or `MC` seul désigne, sur Yahoo Finance, une société américaine (Moelis) ; LVMH est `MC.PA`. Le logiciel lève l'ambiguïté **grâce aux prix de votre fichier**.

### La méthode

Pour chaque ticker court (1 à 6 caractères, sans suffixe) qui n'est pas déjà un ticker connu :

1. il rassemble des candidats : les titres de la base locale qui ont cette racine, les premières réponses du moteur de recherche de Yahoo Finance, et le code suivi des suffixes des grandes places (New York, Paris, Xetra, Amsterdam, Milan, Madrid, Londres, Suisse, Toronto) ;
2. il récupère les cours de ces candidats ;
3. pour chacun, il compare les prix d'achat et de vente de votre fichier au cours du jour de chaque opération, en lisant le prix dans la devise de cotation, dans la devise principale ou en euros ;
4. il retient le candidat dont l'**écart médian** est le plus faible, à condition qu'il soit **inférieur à 15 %**. À écart presque égal (même titre coté à Paris et à Francfort, par exemple), l'ordre de préférence est conservé.

Exemple : `MC` acheté à 740 € en janvier 2024 correspond au cours de LVMH à Paris, pas à celui de Moelis (autour de 50 $) : le logiciel retient `MC.PA`.

### Ce qu'il faut savoir

- La méthode n'utilise que les achats et les ventes (pas les dividendes).
- Elle a besoin des cours des candidats : sans Internet, seuls les titres déjà présents dans la base locale peuvent être comparés.
- Si aucun candidat ne colle à moins de 15 %, le code passe par le moteur de recherche ; s'il reste introuvable, l'assistant s'ouvre pour que vous saisissiez le ticker.
- Le résumé indique « … ticker(s) sans place de cotation identifié(s) grâce aux cours. ».
- Si votre fichier contient aussi une colonne de place (XPAR, Euronext Paris…), elle est utilisée en priorité.

## Titres reconnus sans Internet : les tables d'ISIN et la mémoire
<!-- fiche: import-memoire-etf | questions: est-ce que l'import marche sans internet ; isin reconnu hors connexion ; mon etf amundi est il reconnu sans connexion ; c'est quoi la mémoire des titres ; le logiciel se souvient il des isin ; quels etf sont reconnus automatiquement ; la mémoire contient elle mes données ; il a reconnu un mauvais ticker la dernière fois ; les actions du cac 40 sont elles reconnues hors ligne | mots: hors connexion, mémoire des titres, memoire.csv, table des ISIN, ETF, base locale, Amundi, iShares, Vanguard, CAC 40, actions américaines, apprentissage -->

### La table des ISIN d'ETF

Les avis d'opéré et les relevés ne donnent souvent qu'un code ISIN et un libellé abrégé (« AM.C.C.40 UC.ETF C »). Pour reconnaître les ETF les plus courants **sans Internet**, le logiciel contient une table de 31 ISIN, parmi lesquels :

| ISIN | Ticker | ETF |
|---|---|---|
| FR0013380607 | CACC.PA | Amundi CAC 40 UCITS ETF Acc |
| LU1681043599 | CW8.PA | Amundi MSCI World UCITS ETF Acc |
| FR0011869353 | EWLD.PA | Amundi PEA MSCI World UCITS ETF |
| IE0002XZSHO1 | WPEA.PA | iShares MSCI World Swap PEA UCITS ETF |
| FR0011871128 | PE500.PA | Amundi PEA S&P 500 UCITS ETF |
| IE00B4L5Y983 | IWDA.AS | iShares Core MSCI World UCITS ETF |
| IE00BK5BQT80 | VWCE.DE | Vanguard FTSE All-World UCITS ETF Acc |
| IE00B5BMR087 | SXR8.DE | iShares Core S&P 500 UCITS ETF |
| DE000A0S9GB0 | 4GLD.DE | Xetra-Gold |

La table couvre aussi des ETF Amundi (Euro Stoxx 50, Nasdaq-100, marchés émergents, Stoxx Europe 600, monétaire), iShares, Vanguard, SPDR, Invesco et Xtrackers, actions comme obligations. Elle est consultée **en premier**, avant la mémoire : elle corrige ainsi une mauvaise correspondance qui aurait été apprise auparavant.

### La table des ISIN d'actions

Une seconde table, consultée juste après celle des ETF, reconnaît sans Internet les actions du **CAC 40** (avec quelques anciens membres) et sept grandes valeurs américaines : Apple (AAPL), Microsoft (MSFT), Amazon (AMZN), Alphabet (GOOGL), Meta (META), NVIDIA (NVDA) et Tesla (TSLA). Exemples : FR0000121014 devient `MC.PA` (LVMH), FR0000120578 `SAN.PA` (Sanofi), US0378331005 `AAPL`. Un avis d'opéré sur l'une de ces actions est donc lu entièrement hors connexion.

### La mémoire des titres reconnus

Chaque fois qu'un ISIN, un nom ou un code est trouvé grâce au moteur de recherche de Yahoo Finance, la correspondance est enregistrée dans un fichier de mémoire (`memoire.csv`, dans le dossier de la base de titres). La fois suivante, elle est retrouvée instantanément, même hors connexion.

- La mémoire est commune à tous les utilisateurs du logiciel sur cet ordinateur.
- Elle ne contient **aucune donnée de portefeuille** : seulement des correspondances entre codes (par exemple FR0000121014 → MC.PA), avec un nom et une date.

### La base locale de titres

Après la table et la mémoire, le logiciel cherche dans la base locale de titres livrée avec le logiciel : par ticker, par code ISIN, puis par nom (« LVMH » retrouve « LVMH Moët Hennessy Louis Vuitton »).

### Sans Internet, concrètement

Un ISIN d'ETF ou d'action des deux tables, un titre déjà rencontré ou un titre de la base locale sont reconnus. Un titre totalement nouveau ne peut pas l'être : l'assistant s'ouvre et vous pouvez saisir son ticker à la main.

## Un titre est introuvable : que faire ?
<!-- fiche: import-titre-introuvable | questions: titre introuvable à l'import ; le logiciel ne trouve pas mon isin ; comment saisir le ticker à la main ; statut introuvable dans l'assistant ; mon fonds n'existe pas sur yahoo ; pas de cours pour mon titre ; sicav ou fonds non coté ; le ticker proposé est faux | mots: introuvable, ticker manuel, ISIN inconnu, fonds non coté, OPCVM, Yahoo Finance, correction du ticker, recherche -->

### Le message

Lors d'un import automatique, un titre non identifié empêche l'analyse directe : l'assistant s'ouvre et indique « Titre(s) introuvable(s) : … » suivi des codes concernés. À l'étape 3, ces titres ont le statut « introuvable ».

### La solution

1. Cherchez le titre sur le site de Yahoo Finance (par son nom ou son ISIN) et notez son ticker, par exemple `AI.PA` pour Air Liquide.
2. Dans l'assistant, étape 3, saisissez ce ticker dans la colonne [[Ticker Yahoo Finance]] de la ligne concernée.
3. Vérifiez le résultat à l'étape 4, puis cliquez sur [[Analyser ce portefeuille]].

Sans ticker, les lignes d'un ISIN introuvable sont ignorées (motif « titre manquant »). Pour un nom introuvable, le nom lui-même est gardé comme code, ce qui ne permettra pas de trouver de cours : corrigez-le.

### Causes fréquentes

- **Pas de connexion** : la recherche en ligne est impossible ; seuls les titres des tables d'ISIN (ETF, CAC 40, grandes valeurs américaines), de la mémoire et de la base locale sont reconnus.
- **Fonds non coté** (certains OPCVM, fonds en euros, produits structurés) : sans cours sur Yahoo Finance, il ne peut pas être suivi par le logiciel.
- **Nom trop vague ou abrégé** : un libellé comme « AM.C.C.40 UC.ETF C » ne donne rien ; c'est l'ISIN qui permet la reconnaissance.

### Si le ticker proposé est faux

Remplacez-le de la même façon à l'étape 3. Le contrôle des prix vous aide à repérer une erreur : un titre dont les prix s'écartent de plus de 25 % du cours du jour est signalé (voir la fiche sur la vérification de l'import).

## Titres étrangers : dans quelle devise mettre le prix ?
<!-- fiche: import-devises | questions: mon relevé donne des prix en euros pour des actions américaines ; dans quelle devise saisir le prix d'apple ; le logiciel convertit il les dollars ; montants en euros convertis ça veut dire quoi ; conversion de devise à l'import ; taux de change utilisé ; détection automatique devise ; tout est en euros option ; frais en dollars | mots: devise, devise de cotation, conversion, taux de change, dollar, USD, EUR, EURUSD, détection automatique, prix en euros -->

### La règle du projet

Le prix d'un achat, d'une vente ou d'un dividende est exprimé dans la **devise de cotation** du titre sur Yahoo Finance : dollars pour Apple, francs suisses pour Nestlé, pence pour Londres. Les **frais restent en euros**. Le logiciel convertit ensuite en euros au taux de change du jour de chaque opération.

### Mais beaucoup de relevés donnent des euros

Un relevé bancaire français affiche souvent un prix déjà converti en euros. À l'envoi, le logiciel le détecte : pour chaque titre, il compare les prix d'achat et de vente du fichier au **vrai cours de clôture du jour**, selon trois lectures possibles :

| Lecture | Le prix du fichier est… |
|---|---|
| Cotation | dans la devise de cotation (ex. 185 $) |
| Devise principale | en livres au lieu de pence (titres de Londres uniquement) |
| Euros | converti en euros (ex. 169,72 €) |

Il calcule l'écart médian de chaque lecture avec le marché et garde la plus proche. Si c'est la lecture en euros, les prix du titre (dividendes compris) sont reconvertis dans la devise de cotation : `prix en devise = prix en euros × taux EUR/devise du jour`.

Exemple : un achat d'Apple noté 169,72 € un jour où 1 € vaut 1,09 $ et où l'action cote 185 $. Lu en euros, 169,72 × 1,09 = 184,99 $ : la lecture colle au marché, le prix est reconverti en 184,99 $, soit environ 185 $.

### Les garde-fous

- La conversion n'est faite que si elle améliore nettement l'accord avec le marché (écart réduit de plus de 2 points, en écart logarithmique) ; sinon le prix est gardé tel quel. Utile pour le franc suisse, qui vaut presque un euro.
- Si même la meilleure lecture s'écarte de plus de 25 % du cours, rien n'est converti (sauf si la colonne Devise du fichier impose la lecture en euros).
- Si le fichier a une colonne **Devise**, elle restreint les lectures : « EUR » sur toutes les lignes d'un titre étranger impose la lecture en euros ; la devise du titre exclut la lecture en euros.
- Sans connexion, les prix sont gardés tels quels et le message « Prix non vérifiés avec les cours du marché (pas de connexion). » s'affiche.

### Choisir soi-même dans l'assistant

À l'étape 4, [[Devise des prix du fichier]] propose [[Détection automatique (recommandé)]], [[Devise de cotation de chaque titre]] (aucune conversion) ou [[Tout est en euros]] (conversion de tous les titres étrangers).

### Limite

Le taux utilisé est le taux de marché du jour ; celui de votre banque inclut sa marge de change. De petits écarts sont donc normaux.

## Actions de Londres : pourquoi des pence (GBp) ?
<!-- fiche: import-pence | questions: c'est quoi GBp ; pourquoi le prix d'unilever est en pence ; mes actions londoniennes ont un prix 100 fois trop grand ; prix en livres ou en pence ; GBX dans mon fichier ; action anglaise mal valorisée ; ULVR.L prix | mots: pence, GBp, GBX, livre sterling, GBP, Londres, LSE, facteur 0,01, .L -->

### Le principe

Sur Yahoo Finance, les actions de la Bourse de Londres (tickers en `.L`) sont cotées en **pence** (GBp ou GBX), pas en livres : 1 livre = 100 pence. Une action affichée à 4 000 GBp vaut donc 40,00 £. Le logiciel le sait : pour ces titres, la devise est la livre (GBP) avec un facteur de 0,01.

### Dans le format du projet

Le prix d'une action de Londres s'écrit **en pence**, comme sur Yahoo Finance : `2024-01-15,ACHAT,ULVR.L,Unilever,20,4000,1.00` pour 20 actions à 40 £. Un dividende s'écrit aussi en pence. Les frais restent en euros.

### Si votre fichier donne des livres ou des euros

À l'envoi, la détection des devises compare le prix au cours en pence selon trois lectures :

- en pence : 4 000 → 4 000 GBp ;
- en livres : 40,00 → 40,00 / 0,01 = 4 000 GBp ;
- en euros : 46,50 € avec 1 € = 0,86 £ → 46,50 × 0,86 / 0,01 = 3 999 GBp.

La lecture la plus proche du cours est retenue et le prix est ramené en pence. Le résumé affiche par exemple « ULVR.L : prix en GBP convertis dans l'unité de cotation ».

### Dans une colonne Devise

La valeur `GBX` est lue comme `GBP`. Elle exclut la lecture en euros, mais laisse le choix entre pence et livres.

### Symptôme d'une erreur

Une ligne de Londres valorisée 100 fois trop haut ou trop bas trahit une confusion entre livres et pence. Corrigez le prix dans l'onglet Transactions (colonne [[Prix (devise de cotation)]], en pence), ou réimportez avec la détection automatique.

## Importer un relevé d'opérations en PDF
<!-- fiche: import-pdf-releve | questions: comment importer un pdf de ma banque ; mon relevé pdf est il lu ; le logiciel lit il les tableaux des pdf ; relevé de compte titres pdf ; pdf de plusieurs pages ; aucune opération trouvée dans ce pdf ; pdf avec tableau d'opérations ; dans quel ordre le logiciel essaie de lire un pdf | mots: PDF, relevé d'opérations, tableau, pdfplumber, extraction, plusieurs pages, relevé de compte titres, ordre des lectures -->

### Comment le PDF est lu

Le logiciel lit le texte et les tableaux du PDF (bibliothèque pdfplumber), page par page.

- Un tableau est retenu s'il a au moins deux lignes, trois colonnes, et des dates sur au moins deux lignes : c'est la marque d'un vrai tableau d'opérations. Si la page n'a pas de traits de tableau, le logiciel essaie aussi de reconstituer les colonnes d'après l'alignement du texte.
- Les tableaux de même largeur sont mis bout à bout (relevé sur plusieurs pages) ; l'en-tête répété en haut de chaque page n'est gardé qu'une fois.
- Le tableau obtenu suit ensuite exactement le même chemin qu'un fichier Excel : ligne des titres, reconnaissance des colonnes, ISIN, dates, nombres, devises.

### Quand le PDF est plutôt un avis d'opéré

Si le texte contient « avis d'opéré », « avis d'exécution », « confirmation d'exécution », « confirmation d'ordre » ou « trade confirmation », le logiciel lit d'abord le document comme un avis d'opéré (une opération par page). S'il n'y a pas de tableau d'opérations exploitable, il essaie aussi cette lecture.

### L'ordre des lectures

1. Texte absent, ou texte « codé » (il s'affiche bien mais s'extrait en caractères incompréhensibles) : le PDF est traité comme un scan (voir la fiche sur les PDF image).
2. Relevé de portefeuille (positions et prix de revient) : chaque position devient un achat à la date du relevé (voir la fiche « Importer un relevé de portefeuille PDF »).
3. Lecture par les intitulés de l'avis d'opéré, et lecture des tableaux du relevé. Une opération lue par ses intitulés n'est acceptée que si un mot de sens (achat, vente, dividende…) est écrit dans le document et si un cours (ou, pour un dividende, un montant) a été trouvé ; sinon, le logiciel passe à la lecture suivante.
4. Lecture **par le contenu**, quel que soit le courtier : code ISIN, date d'exécution et relation `quantité × cours = montant` (voir la fiche « Un avis d'opéré d'une autre banque ou d'un autre courtier »).
5. Lecture avec un **modèle appris** : ce type de document a déjà été complété une fois dans le formulaire (voir la fiche « Le logiciel apprend vos avis d'opéré »).
6. Si rien n'est sûr : « Opération non reconnue automatiquement dans ce PDF : complétez-la dans le formulaire « Compléter l'opération » (les valeurs trouvées sont proposées). ».

Un PDF protégé par un mot de passe demande d'abord ce mot de passe (voir la fiche « Mon PDF est protégé par un mot de passe »).

### Si rien n'est reconnu

Au lieu d'un simple refus, le formulaire [[Compléter l'opération]] s'ouvre avec les dates, codes et nombres trouvés dans le document (voir la fiche « Compléter une opération quand le PDF n'est pas reconnu »). Pour un long relevé en tableau, il est souvent plus rapide de :

- télécharger plutôt l'export Excel ou CSV des opérations depuis votre espace bancaire ;
- ou utiliser l'outil de diagnostic pour voir ce que le logiciel lit (voir la fiche sur `diagnostic_pdf.py`).

### Conseil

Sur le site de votre banque, préférez le bouton de téléchargement du document (« Format PDF », « Télécharger ») à la fonction « Imprimer » du navigateur : un PDF téléchargé contient le vrai texte, lu instantanément et exactement ; une page « imprimée en PDF » n'est parfois qu'une image.

## Importer un avis d'opéré PDF (exemple Bourse Direct)
<!-- fiche: import-avis-opere | questions: comment importer un avis d'opéré ; c'est quoi un avis d'opéré ; mon avis d'opéré bourse direct est il reconnu ; le logiciel a pris la date d'édition au lieu de la date d'exécution ; avis d'opéré en pdf vente comptant ; plusieurs avis dans un pdf ; confirmation d'ordre pdf ; quantité négative dans l'avis | mots: avis d'opéré, confirmation d'exécution, Bourse Direct, Format PDF, date d'exécution, courtage, ISIN, ordre exécuté -->

Un **avis d'opéré** est la confirmation que votre courtier envoie après chaque ordre exécuté. Le logiciel en extrait une opération par page.

L'avis peut venir de **n'importe quelle banque ou courtier** : Bourse Direct n'est qu'un exemple. Le logiciel lit d'abord les intitulés habituels (tableau ci-dessous) ; s'il n'y parvient pas, il lit l'avis par son contenu (voir la fiche « Un avis d'opéré d'une autre banque ou d'un autre courtier »).

### Ce qui est lu

| Information | Où le logiciel la cherche |
|---|---|
| Code ISIN | Premier code de 12 caractères dont la clé de contrôle est juste, qui commence par un code pays existant et compte au moins 4 chiffres |
| Date | Date d'exécution, d'opération ou de négociation, « exécuté le », « trade date » ; à défaut une date proche du mot exécution ou suivie de « achat »/« vente » ; les dates d'édition, d'émission, de règlement, de valeur ou de livraison sont écartées |
| Sens | Achat, vente, souscription, rachat, buy, sell, dividende, coupon… : un de ces mots doit être écrit dans le document |
| Quantité | « Quantité », « Qté », « Nombre de titres », « Quantity », « Nominal » |
| Cours et devise | « Cours », « Prix unitaire », « Price », avec EUR, USD, GBP, €, $, £… |
| Frais | Somme de toutes les lignes « Courtage », « Commission », « Frais », « TTF » (taxe sur les transactions financières), « Fees » |
| Montant | « Montant net », « Net à débiter/créditer », sinon « Montant » ou « Brut » |
| Libellé | Après « Libellé : » ou « Valeur : », sinon le nom écrit juste après l'ISIN |

Les intitulés et valeurs peuvent être présentés en texte (« Quantité : 15 »), rangés dans un tableau, ou placés en colonnes sans traits, l'intitulé au-dessus de la valeur : le logiciel associe alors chaque valeur à l'intitulé placé au-dessus d'elle, d'après la position des mots sur la page (« Quantité » au-dessus de « 12 » donne « Quantité : 12 »).

Une opération n'est retenue par cette lecture que si l'ISIN, la quantité et la date sont trouvés, si un mot de sens est écrit dans le document, et si le cours (ou, pour un dividende, le montant) est trouvé. Sinon, le logiciel passe à la lecture par le contenu.

### Exemple : avis Bourse Direct téléchargé avec « Format PDF »

L'avis contient notamment :

```
28/09/2026 VENTE COMPTANT FR0013380607 AM.C.C.40 UC.ETF C 2 473,90
QUANTITE : -60
COURS : +41,295 BRUT : +2 477,70
COURTAGE : +3,80 TVA : +0,00
```

Le logiciel lit : date 28/09/2026, sens VENTE, ISIN FR0013380607, libellé « AM.C.C.40 UC.ETF C », quantité −60 (rendue positive : 60), cours 41,295, frais 3,80 €. L'ISIN figure dans la table des ETF : il devient `CACC.PA` sans Internet, et le libellé abrégé est remplacé par le nom officiel « Amundi CAC 40 UCITS ETF Acc ». L'opération obtenue est : `2026-09-28, VENTE, CACC.PA, 60 titres à 41,295 €, frais 3,80 €`. Contrôle : 60 × 41,295 = 2 477,70 € brut, moins 3,80 € de courtage = 2 473,90 € crédités.

### Plusieurs avis

Un PDF de plusieurs pages contenant un avis par page donne une opération par page. Plusieurs avis en fichiers séparés peuvent être déposés ensemble, dans la zone d'envoi de la barre latérale comme sur la page [[Ajouter des opérations]] (voir la fiche « Envoyer plusieurs fichiers d'un coup »).

### Après la lecture

Le résumé de la barre latérale indique « Avis d'opéré PDF lu. » (ou, pour une lecture par le contenu, « Avis d'opéré PDF lu d'après son contenu (quantité × cours = montant) : vérifiez l'opération (onglet « Transactions »). »). Il signale aussi un cours remplacé grâce au cours du marché (voir la fiche « Vérification du cours lu avec le cours du marché ») et les points à vérifier repérés après la lecture (voir la fiche « Les contrôles après la lecture d'un PDF »). Vérifiez toujours l'opération : un avis inhabituel peut être mal interprété.

## Un avis d'opéré d'une autre banque ou d'un autre courtier
<!-- fiche: import-pdf-tout-courtier | questions: mon avis d'opéré n'est pas de bourse direct est ce qu'il marche ; le logiciel lit il les avis de boursorama fortuneo degiro trade republic ; avis d'opéré d'une autre banque ; mon courtier n'est pas reconnu ; trade confirmation en anglais est elle lue ; avis d'opere de ma banque avec une autre mise en page ; comment le logiciel lit un pdf sans intitulés ; lecture d'après son contenu c'est quoi ; est ce que ça marche avec tous les courtiers | mots: avis d'opéré, tout courtier, autre banque, lecture par le contenu, quantité × cours, ISIN, trade confirmation, mise en page, pdf_contenu | aller: Analyse du portefeuille/Transactions -->

Chaque courtier présente ses avis d'opéré à sa façon (« Quantité : », « Nombre de titres », « Qté », « Buy 15 … at 85.12 »…). Quand les intitulés habituels ne suffisent pas, le logiciel lit l'avis **par son contenu**, sans se fier à la mise en page.

### Ce que le logiciel cherche

Tout avis d'opéré contient les mêmes éléments :

- un **code ISIN**, reconnu grâce à sa clé de contrôle, avec un code pays existant et au moins 4 chiffres ;
- une **date d'exécution**, écrite en chiffres ou avec le mois en lettres, en français ou en anglais ; les dates d'édition, de règlement ou de valeur sont écartées, et quand deux mots se disputent une date, le plus proche l'emporte ;
- **trois nombres liés** : `quantité × cours = montant brut`, au centime près, ou à défaut `quantité × cours ± frais = montant net` ;
- les **frais** : les nombres qui suivent « courtage », « commission », « frais », « costs », « TTF »… ;
- le **sens** : achat, vente, buy, sell, bought, sold, dividende… ;
- la **devise** écrite à côté du cours.

Plusieurs opérations sur une même page sont lues séparément : une par code ISIN.

### Exemple

Un avis en anglais contient :

```
Date 07-05-2024 14:32
Buy 15 VANGUARD S&P 500 UCITS ETF IE00B3XXRP09 at 85.12 EUR
Value EUR 1,276.80
Transaction costs EUR 2.00
Total EUR 1,278.80
```

Aucun intitulé « Quantité » ni « Cours ». Le logiciel essaie les nombres deux à deux et trouve `15 × 85,12 = 1 276,80`, qui figure dans le texte. Il retient : date 07/05/2024, achat (« Buy »), ISIN IE00B3XXRP09, 15 titres à 85,12 EUR, frais 2,00 (nombre après « costs »), et vérifie que `1 276,80 + 2,00 = 1 278,80`, le total écrit.

### Quand plusieurs lectures tombent juste

Il arrive que deux couples de nombres donnent le même montant. Le logiciel garde la lecture la plus probable (quantité entière, nombres placés près de leurs intitulés), mais retient aussi les autres : avec Internet, le cours de clôture du jour permet ensuite de les départager (voir la fiche « Vérification du cours lu avec le cours du marché »).

### Après la lecture

Le résumé indique « Avis d'opéré PDF lu d'après son contenu (quantité × cours = montant) : vérifiez l'opération (onglet « Transactions »). ». Contrôlez la date, la quantité et le cours dans l'onglet [[Transactions]].

### Les limites

L'opération n'est retenue automatiquement que si l'ISIN, la date, un trio de nombres cohérent et le sens sont tous trouvés (le sens peut aussi venir d'une quantité précédée de + ou −). Aucune lecture ne peut garantir de comprendre 100 % des documents existants : si l'un de ces éléments manque, le logiciel essaie encore un modèle appris (voir la fiche « Le logiciel apprend vos avis d'opéré »), puis le formulaire [[Compléter l'opération]] prend le relais avec les valeurs trouvées (voir la fiche suivante).

## Un relevé d'opérations « une ligne par opération » (ex. Interactive Brokers)
<!-- fiche: import-releve-une-ligne-par-operation | questions: mon relevé interactive brokers est il lu ; trade confirmation report avec plusieurs opérations ; mon relevé n'a pas de code isin seulement des symboles ; le pdf contient toutes mes opérations de l'année ; ibkr pdf import ; relevé imprimé en mode sombre ; mon pdf a un fond noir ; plusieurs achats et ventes dans un seul pdf | mots: relevé d'opérations, Interactive Brokers, IBKR, Trade Confirmation Report, symbole, une ligne par opération, mode sombre, fond noir, pdf_lignes -->

Certains courtiers produisent un relevé où **chaque ligne porte une opération complète** : un code (ISIN ou simple symbole boursier comme « ESE », « PAEJ », « RMS »), la date, le sens (achat, vente, BUY, SELL), puis la quantité, le cours, le montant et la commission. C'est le cas du « Trade Confirmation Report » d'Interactive Brokers.

### Comment le logiciel le lit

- Il retient chaque ligne qui contient une date, un mot de sens et un code ; les lignes « Total » sont ignorées.
- Sur chaque ligne, il cherche les trois nombres qui vérifient **quantité × cours = montant** au centime près. Exemple : `7 × 33,4540 = 234,18`.
- La commission est le petit nombre décimal qui suit le montant (moins de 5 % du montant).
- Une vente est reconnue au mot SELL / vente, ou au signe « − » de la quantité.
- Un symbole suivi d'une minuscule ajoutée par le courtier (« LYSXd ») est ramené au symbole (« LYSX »). Le titre est ensuite identifié par ses cours (la place de cotation dont les prix collent aux prix du relevé), ou par le moteur de recherche.
- Le relevé n'est retenu que si **toutes** ses lignes d'opération sont cohérentes ; sinon le formulaire « Compléter l'opération » prend le relais.

### Relevé imprimé en « mode sombre »

Une page imprimée depuis un navigateur en mode sombre (texte clair sur fond noir, lignes de tableau foncées) est remise en « noir sur blanc » zone par zone, et les bordures du tableau sont effacées avant la reconnaissance de caractères. Les virgules perdues par la lecture (« -23418 » pour -234,18) sont retrouvées grâce à la cohérence quantité × cours = montant.

### Limites

- Une commission mal lue sur une ligne peut rester fausse : vérifiez la colonne Frais dans l'onglet [[Transactions]].
- Le plus sûr reste de télécharger le relevé au format CSV ou PDF « texte » depuis l'espace client du courtier plutôt que de l'imprimer.

## Vérification du cours lu avec le cours du marché
<!-- fiche: import-pdf-verification-marche | questions: le logiciel vérifie t il le cours lu dans mon avis ; cours lu remplacé par pourquoi ; le logiciel a changé ma quantité et mon prix ; comment il choisit entre deux lectures du pdf ; cours de clôture affiché dans le formulaire ; le prix unitaire doit en être proche ça veut dire quoi ; vérification avec yahoo finance du prix de mon avis ; pourquoi les nombres de la liste sont dans cet ordre | mots: vérification par le marché, cours de clôture, Yahoo Finance, départage, arbitrage, lecture alternative, 15 %, 5 %, cours lu remplacé | aller: Analyse du portefeuille/Transactions -->

Dans un avis d'opéré, plusieurs couples de nombres peuvent vérifier `quantité × cours = montant`. Pour choisir la bonne lecture, le logiciel compare le cours lu au **cours de clôture du titre le jour de l'opération**, téléchargé sur Yahoo Finance.

### La règle

Pour un achat ou une vente lu dans un avis d'opéré :

- si le cours retenu s'écarte de **plus de 15 %** du cours de clôture du jour,
- et si une autre lecture cohérente du même document donne un cours à **moins de 5 %** de ce cours de clôture,

alors cette autre lecture remplace la première : la quantité, le cours et, s'ils sont connus, les frais de cette lecture sont repris. Sinon, rien ne change.

### Exemple

Deux lectures tombent juste : `10 × 65,02 = 650,20` et `5 × 130,04 = 650,20`. Le cours de clôture du jour est de 130,50 €. La première lecture s'en écarte de 50 % (plus de 15 %), la seconde de 0,4 % (moins de 5 %) : le logiciel retient 5 titres à 130,04 €.

Le résumé de la barre latérale l'indique, sous la forme : « [ticker] ([date]) : cours lu [ancien] remplacé par [nouveau], la lecture qui correspond au cours de clôture du jour ([cours]). ».

### Dans le formulaire « Compléter l'opération »

Quand le formulaire [[Compléter l'opération]] s'ouvre et que le titre et la date sont connus, une ligne indique le cours de clôture de ce jour, par exemple « Cours de clôture de MC.PA le 04/03/2024 : … (Yahoo Finance) — le prix unitaire doit en être proche. ». Si aucune proposition de cours n'a été trouvée, la liste [[Prix unitaire]] est classée en mettant en tête les nombres les plus proches de ce cours de clôture.

### Les limites

- Il faut disposer du cours du jour, donc en général d'une connexion Internet : sans lui, la lecture n'est ni vérifiée ni modifiée.
- Seuls les achats et les ventes sont concernés, pas les dividendes.
- Le départage ne choisit qu'entre des lectures qui figurent déjà dans le document : il n'invente jamais un cours.
- Le cours de clôture n'est pas votre cours d'exécution : un écart de quelques pour cent est normal.

## Compléter une opération quand le PDF n'est pas reconnu
<!-- fiche: import-pdf-formulaire | questions: mon avis d'opéré n'est pas reconnu ; aucune opération trouvée dans ce pdf ; mon prof a un pdf qui ne passe pas ; le pdf de ma banque ne marche pas que faire ; opération non reconnue automatiquement dans ce pdf ; c'est quoi le formulaire compléter l'opération ; comment choisir la quantité et le cours dans la liste ; le logiciel me propose des nombres je prends lequel ; saisir mon avis d'opéré à la main à partir du pdf | mots: formulaire, compléter l'opération, PDF non reconnu, saisie assistée, valeurs proposées, quantité, cours, frais, filet de sécurité -->

Quand un PDF ne donne aucune opération sûre, le logiciel ne se contente pas d'un message d'erreur : il ouvre le formulaire [[Compléter l'opération]], pré-rempli avec ce qu'il a trouvé dans le document.

### Quand le formulaire apparaît

- Sur la page [[Ajouter des opérations]], onglet [[Depuis un fichier]] : pour tout PDF dont l'import automatique n'est pas sûr (aucune opération lue, titre introuvable…).
- Après un envoi avec [[Envoyer un fichier (CSV, Excel ou PDF)]] dans la barre latérale : quand le PDF ne donne aucune opération, que le fichier soit envoyé seul ou avec d'autres.

La raison s'affiche sous le titre du formulaire, par exemple « Opération non reconnue automatiquement dans ce PDF… ».

### Remplir le formulaire, étape par étape

1. **[[Type]]** (au-dessus du formulaire) : ACHAT, VENTE ou DIVIDENDE, le sens trouvé dans le document étant choisi d'avance. Pour un dividende, la quantité et le cours sont remplacés par le champ [[Montant total reçu]].
2. **[[Date d'exécution]]** : pré-remplie avec la date d'exécution probable ; l'aide du champ liste les dates trouvées dans le document.
3. **[[Titre]]** : le code ISIN trouvé, suivi du nom ; vous pouvez aussi taper un ticker (ex. MC.PA), un ISIN ou un nom.
4. **[[Quantité]]**, **[[Prix unitaire]]** et **[[Frais (€)]]** : chaque liste contient les nombres du document, chacun suivi des mots qui l'entourent (par exemple « Quantité : [60] »). La meilleure proposition est déjà choisie ; vous pouvez en choisir une autre ou taper une valeur.
5. Avec Internet, une ligne rappelle le cours de clôture du titre ce jour-là : le prix unitaire doit en être proche (voir la fiche « Vérification du cours lu avec le cours du marché »).
6. Vérifiez la ligne de contrôle, par exemple « Contrôle : 60 × 41,295 = 2477,7 » : elle doit retomber sur le montant brut de votre avis.
7. Cliquez sur [[Ajouter cette opération]].

L'encadré [[Texte lu dans le document]] montre le texte extrait, pour vérifier une valeur. Il contient aussi le bouton [[Préparer un rapport anonymisé]] (voir la fiche « Envoyer un PDF mal lu sans données personnelles »).

### Le logiciel retient la leçon

En validant un achat ou une vente, vous apprenez au logiciel à lire ce type de document : il retient, sur l'ordinateur, l'intitulé placé devant chaque valeur que vous avez choisie. Le prochain avis de même présentation sera lu automatiquement (voir la fiche « Le logiciel apprend vos avis d'opéré »).

### Ensuite

- Page [[Ajouter des opérations]] : l'opération rejoint le tableau [[Vérification avant enregistrement]]. Le formulaire y ajoute une opération par fichier ; pour une seconde opération du même PDF, utilisez l'onglet [[Saisie manuelle]].
- Barre latérale, fichier envoyé seul : le nombre d'opérations prêtes s'affiche ; ajoutez-en d'autres si le PDF en contient plusieurs, puis cliquez sur [[Analyser ces opérations]].

### Rien n'est inventé

Chaque valeur proposée figure dans le document. Si le PDF ne contient aucun texte lisible (scan sans moteur de reconnaissance de caractères), le formulaire l'indique : « Aucun texte lisible dans ce document : saisissez l'opération à la main. ».

## Le logiciel apprend vos avis d'opéré : les modèles appris
<!-- fiche: import-pdf-modeles-appris | questions: le logiciel apprend il mes avis d'opéré ; je dois remplir le formulaire à chaque fois pour le même courtier ; c'est quoi un modèle appris ; avis lu avec le modèle appris lors d'une saisie précédente ; où est stocké modeles_pdf.json ; le modèle garde t il mes montants ; sens S ou A sur mon avis d'opéré ; pourquoi le formulaire revient alors que j'ai déjà rempli ce type d'avis ; oublier un modèle appris | mots: modèle appris, apprentissage, modeles_pdf.json, intitulés, empreinte, hachage, code de sens, pdf_modele, mise en page -->

Certains avis d'opéré utilisent des intitulés que le logiciel ne connaît pas (« Nominal exécuté », « Px moyen », « Sens : S »…). La première fois, le formulaire [[Compléter l'opération]] vous fait compléter l'opération. Le logiciel en profite pour **apprendre la présentation** du document.

### Ce qui est retenu

Quand vous cliquez sur [[Ajouter cette opération]] pour un achat ou une vente, le logiciel enregistre un « modèle » de ce type de document :

- pour la quantité, le cours, les frais et le montant (quantité × cours, s'il est écrit) : l'**intitulé** écrit juste avant la valeur que vous avez choisie (au plus trois mots) et sa place sur la ligne ;
- l'intitulé écrit juste avant la date retenue ;
- si le sens n'est écrit qu'en code (« Sens : S », « Op. : A ») et qu'aucun mot comme achat ou vente ne figure dans le document : la correspondance entre ce code et le type choisi (par exemple « s » pour VENTE) ;
- le **vocabulaire** du document, mais seulement sous forme d'empreintes (hachage) : les mots eux-mêmes ne sont pas lisibles dans le fichier.

Aucun montant, aucune quantité, aucun nom n'est enregistré en clair. Le modèle n'est retenu que si les intitulés de la quantité et du cours ont été trouvés. Les dividendes ne sont pas appris.

### La fois suivante

Si aucune autre lecture n'aboutit, le logiciel compare le vocabulaire du nouveau document à celui des modèles. Si la ressemblance atteint **0,6** (60 % de mots en commun, mesurés sur l'ensemble des mots des deux documents), il lit les valeurs placées après les intitulés appris. L'opération n'est acceptée que si un ISIN, une quantité, un cours et une date sont trouvés ; si le modèle connaît l'intitulé du montant, quantité × cours doit en plus retomber sur ce montant (à 1 % près, ou à quelques centimes près une fois les frais ajoutés ou retirés). Le résumé indique alors : « Avis d'opéré PDF lu avec le modèle appris lors d'une saisie précédente : vérifiez l'opération (onglet « Transactions »). ».

Le sens est lu dans le document (achat, vente…) ; à défaut, dans le code de sens appris ; si le document n'a ni mot de sens ni code, le type choisi lors de l'apprentissage est repris. Si le document porte un code de sens jamais vu (par exemple « Sens : R » alors que seuls « A » et « S » ont été appris), le formulaire réapparaît : vous choisissez le type, et le nouveau code est appris à son tour.

### Où sont les modèles

Dans le fichier `modeles_pdf.json` du dossier de la base de titres (`data/base`). Les 50 derniers modèles sont gardés ; un document très ressemblant à un modèle existant le remplace, en conservant les codes de sens déjà appris. Le fichier est commun à tous les utilisateurs de l'ordinateur. Le logiciel ne propose pas d'écran pour l'effacer : pour oublier tous les modèles, supprimez ce fichier.

## Un PDF scanné ou « imprimé » : la reconnaissance de caractères
<!-- fiche: import-pdf-image | questions: mon pdf est une image ; pdf scanné est il lu ; c'est quoi l'ocr ; j'ai imprimé la page en pdf avec microsoft print to pdf ; reconnaissance de caractères comment ça marche ; mon pdf est tourné en paysage ; l'isin est mal lu ; rapidocr ou tesseract ; ça prend du temps à lire le pdf ; le chargement est très long avec mon pdf ; mon pdf est en mode sombre ; mon scan est pâle et de travers | mots: OCR, reconnaissance de caractères, PDF image, scan, RapidOCR, Tesseract, rotation, redressement, contraste, ISIN mal lu, chiffres mal lus, Microsoft Print to PDF -->

### PDF texte et PDF image

Un PDF peut contenir du **vrai texte** (chaque caractère est enregistré, comme dans un PDF téléchargé depuis la banque) ou seulement une **image** de la page (scan, photo, ou page web imprimée avec « Microsoft Print to PDF »). Le logiciel considère qu'un PDF est une image quand il contient moins de 20 caractères de texte.

Il existe aussi des PDF au texte **« codé »** : la page s'affiche correctement à l'écran, mais le texte extrait n'est qu'une suite de signes incompréhensibles (par exemple `(cid:12)`). Le logiciel les reconnaît (caractères étranges, très peu de lettres ou aucun mot courant) et les traite exactement comme un scan.

### La reconnaissance de caractères

Pour un PDF image, le logiciel « regarde » chaque page et y reconnaît les lettres et les chiffres, si un moteur est installé :

1. **RapidOCR**, bibliothèque qui fonctionne hors connexion, installée avec le fichier `requirements-ocr.txt` et intégrée aux installateurs lorsque leur fabrication a réussi à l'installer ;
2. à défaut, **Tesseract**, s'il est installé sur l'ordinateur (en français et en anglais si la langue française est disponible).

### Deux tentatives

1. Une **première lecture**, rapide, de l'image de chaque page.
2. Si elle ne donne aucune opération sûre, une **seconde lecture**, plus lente, sur une image nettoyée et en plus haute résolution (échelle 4 au lieu de 3) : passage en niveaux de gris, contraste étiré, page redressée (l'inclinaison est cherchée entre −3° et +3°, par pas d'un demi-degré), puis passage en noir et blanc pur (seuil d'Otsu, qui sépare automatiquement l'encre du fond). Un scan pâle, granuleux ou légèrement de travers devient ainsi lisible.

### Les précautions prises

- **Page à fond sombre** (impression en « mode sombre », lignes de tableau foncées) : la page est remise en noir sur blanc zone par zone, en plus haute résolution, et les bordures de tableau sont effacées avant la lecture.
- **Rotation** : la page est d'abord lue droite ; les trois autres sens (90°, 270°, 180°) ne sont essayés que si elle ne donne presque rien d'utile (ni code ISIN, ni long texte avec des mots attendus : quantité, cours, achat, vente, price, quantity, buy, sell…).
- **Plusieurs pages** : elles sont lues en même temps, ce qui divise le temps d'attente.
- **Réparation des ISIN mal lus** : la lettre O lue à la place du chiffre 0 (`FRO013380607`), un I ou un l à la place de 1, S pour 5, B pour 8, Z pour 2, ou un caractère lu en double (`FRO0013380607`). Une correction n'est retenue que si l'ISIN corrigé a une clé de contrôle juste, un code pays existant et au moins 4 chiffres : le logiciel n'invente jamais un code. Un mot comme « EURONEXTPARIS » n'est jamais pris pour un ISIN.
- **Réparation des nombres** : dans un nombre, une lettre lue à la place d'un chiffre est corrigée (O ou o en 0, I, l ou | en 1, S en 5, B en 8) : « 65O,2O » devient « 650,20 ». La correction n'a lieu que dans un groupe qui contient déjà au moins deux vrais chiffres et une virgule ou un point décimal, sans autre lettre : les mots ne sont jamais modifiés.
- **Mots collés** : la lecture tolère les mots accolés (« VENTECOMPTANT »).

Le texte reconnu est ensuite lu comme un relevé « une ligne par opération » (voir la fiche dédiée), puis comme un avis d'opéré : par ses intitulés, par son contenu (ISIN, date, `quantité × cours = montant`), puis avec un modèle appris. Un relevé de portefeuille scanné n'est en général pas exploitable. Si aucune opération n'est reconnue, le formulaire [[Compléter l'opération]] propose les valeurs lues.

### À vérifier systématiquement

La lecture d'une image prend du temps : environ 10 à 30 secondes par page selon l'ordinateur (davantage si la seconde tentative est nécessaire) ; le message d'attente l'indique avec le nombre de pages. Pendant ce temps, l'ancien tableau de bord reste affiché en grisé : c'est normal. Elle reste moins sûre qu'un PDF texte. Le résumé l'indique : « PDF image lu par reconnaissance de caractères : vérifiez les opérations (onglet « Transactions »). ». Contrôlez la date, la quantité et le cours.

## Pourquoi mon PDF scanné est-il refusé ?
<!-- fiche: import-pdf-scan-refuse | questions: pdf scanné refusé ; message impossible à lire automatiquement ; aucune opération n'a été reconnue dans mon pdf image ; pourquoi mon scan ne passe pas ; le logiciel refuse ma photo d'avis d'opéré ; que faire si mon pdf est une image ; installer la reconnaissance de caractères | mots: PDF scanné, refus, PDF image, OCR non installé, message d'erreur, Format PDF, saisie manuelle, requirements-ocr -->

Un PDF image n'est plus simplement refusé : quand il n'est pas lu automatiquement, l'un des messages ci-dessous s'affiche en tête du formulaire [[Compléter l'opération]] (voir la fiche « Compléter une opération quand le PDF n'est pas reconnu »).

### « PDF scanné (image) : impossible à lire automatiquement… »

Aucun moteur de reconnaissance de caractères n'est installé : le PDF ne contient aucun texte à lire. Le formulaire indique alors « Aucun texte lisible dans ce document : saisissez l'opération à la main. » : il faut taper les valeurs vous-même.

Si vous lancez le logiciel depuis le code source, vous pouvez installer le moteur avec la commande `python -m pip install -r requirements-ocr.txt`.

### « Le texte de ce PDF est « codé »… »

Le PDF contient du texte, mais il s'extrait en signes incompréhensibles, et aucun moteur de reconnaissance de caractères n'est installé. Même solution : installer le moteur, ou compléter l'opération à la main dans le formulaire.

### « PDF image (scan, photo ou page imprimée avec « Imprimer en PDF ») : le texte a été lu par reconnaissance de caractères, mais aucune opération n'a été reconnue… »

Le moteur a bien lu la page, deux fois (la seconde sur une image nettoyée et redressée), mais aucune lecture n'a trouvé une opération sûre. Causes possibles : image floue ou de très faible résolution, ISIN illisible, document qui n'est pas un avis d'opéré (relevé en tableau, synthèse de portefeuille). Le formulaire propose alors les dates, codes et nombres lus sur l'image.

### Pourquoi le logiciel ne devine pas

Une opération mal lue (une quantité de 60 lue 80, un cours décalé d'une virgule) fausserait tous les calculs sans que vous le remarquiez. Le logiciel n'ajoute donc automatiquement que ce dont il est sûr ; pour le reste, c'est vous qui validez les valeurs dans le formulaire.

### Les solutions, de la plus sûre à la moins sûre

1. **Télécharger le vrai PDF** depuis votre espace bancaire, avec le bouton « Format PDF » ou « Télécharger » plutôt que « Imprimer » : le texte est alors lu exactement.
2. **Exporter les opérations en Excel ou CSV**, si votre banque le propose.
3. **Compléter l'opération** dans le formulaire proposé, ou la saisir à la main : page [[Ajouter des opérations]], onglet [[Saisie manuelle]].
4. Lancer le diagnostic du PDF pour comprendre ce qui a été lu, ou préparer un rapport anonymisé à transmettre (voir les fiches suivantes).

## Les contrôles après la lecture d'un PDF
<!-- fiche: import-pdf-controles | questions: le montant écrit ne correspond pas à quantité × cours ; opération datée d'un samedi jour sans bourse ; frais de plus de 3 % vérifiez les frais ; la même opération apparaît deux fois avis envoyé en double ; quels contrôles après la lecture d'un pdf ; messages dans le résumé de la barre latérale après un pdf ; le logiciel vérifie t il mon avis d'opéré ; date d'exécution un dimanche | mots: contrôles, vérification, montant écrit, quantité × cours, week-end, jour sans bourse, frais élevés, 3 %, doublon, avis en double, résumé -->

Après la lecture d'un PDF envoyé depuis la barre latérale, le logiciel passe chaque opération au crible de quatre contrôles. Ils ne bloquent rien : chaque point repéré est ajouté au résumé de la barre latérale, pour que vous le vérifiiez dans l'onglet [[Transactions]].

### Les quatre contrôles

| Contrôle | Message affiché dans le résumé |
|---|---|
| Le montant écrit dans l'avis ne retombe pas sur `quantité × cours`, frais ajoutés ou retirés, à 1 % près | « [ISIN] : le montant écrit ([montant]) ne correspond pas à quantité × cours ± frais ([calcul]) : vérifiez la quantité et le cours. » |
| Achat ou vente daté d'un samedi ou d'un dimanche | « [ticker] : opération datée d'un samedi ([date]), jour sans bourse : vérifiez la date d'exécution. » |
| Frais supérieurs à 3 % du montant `quantité × cours` | « [ticker] : frais de [frais] pour un montant de [montant] (plus de 3 %) : vérifiez les frais. » |
| Même opération deux fois (même date, type, titre, quantité et prix) | « [ticker] : la même opération apparaît deux fois ([date]) : avis envoyé en double ? » |

### Ce que chaque message signale le plus souvent

- **Montant incohérent** : une quantité ou un cours mal lu (une virgule déplacée, un chiffre mal reconnu sur un scan). Ce contrôle porte sur les avis d'opéré, pas sur les relevés en tableau, et ignore les dividendes.
- **Jour sans bourse** : la date d'édition ou de règlement a été prise pour la date d'exécution.
- **Frais élevés** : un montant pris pour des frais, ou de vrais frais élevés sur un petit ordre. Exemple : 2 titres à 50 € (100 €) avec 4,90 € de courtage : 4,9 % du montant, le message apparaît. Pour 30 titres à 172,46 € (5 173,80 €) avec 20,69 € de frais, soit 0,4 %, rien n'est signalé.
- **Doublon** : le même avis présent deux fois dans le PDF.

### Le cas de plusieurs fichiers

Quand plusieurs fichiers sont envoyés ensemble, les contrôles de chaque fichier sont réunis, et une opération présente dans deux fichiers n'est comptée qu'une fois ; le résumé le précise : « … opération(s) présente(s) dans deux fichiers comptée(s) une seule fois. ».

### Que faire

Ouvrez l'onglet [[Transactions]] et comparez l'opération à votre avis. Une erreur se corrige avec [[Modifier les opérations]].

Ces contrôles ne sont pas affichés sur la page [[Ajouter des opérations]], qui a ses propres contrôles avant enregistrement (voir la fiche « Quels contrôles bloquent l'enregistrement ? »).

## Importer un relevé de portefeuille PDF (positions et PRU)
<!-- fiche: import-releve-portefeuille-pdf | questions: importer mon relevé de portefeuille pdf ; je n'ai que la liste de mes positions avec le pru ; relevé de compte titres avec valorisation et prix de revient ; état du portefeuille pdf est il accepté ; portfolio statement pdf ; pourquoi ma performance commence à la date du relevé ; mes positions sont devenues des achats ; comment partir de mon portefeuille actuel sans l'historique | mots: relevé de portefeuille, positions, PRU, prix de revient, valorisation, portefeuille de départ, pdf_positions, état du portefeuille, statement of holdings | aller: Analyse du portefeuille/Positions -->

Un **relevé de portefeuille** (ou « état du portefeuille », « valorisation du portefeuille ») liste les titres détenus à une date, avec leur quantité, leur cours, leur valorisation et souvent le prix de revient unitaire (PRU). Le logiciel peut s'en servir comme **portefeuille de départ**.

### Comment il est reconnu

Le PDF doit contenir un titre comme « Relevé de portefeuille », « Relevé de compte-titres », « Portefeuille titres », « État du portefeuille », « Valorisation du portefeuille », « Inventaire du portefeuille », « Estimation du portefeuille », « Positions au », « Portfolio statement » ou « Statement of holdings », et au moins un code ISIN.

Pour chaque ligne de titre, le logiciel cherche :

- `quantité × cours = valorisation`, au centime près ;
- le **PRU** : le nombre précédé de « PRU », « prix de revient », « prix moyen », « PAM » ou « cost price » ; sinon, un nombre de la ligne compris entre le tiers et le triple du cours, confirmé si `quantité × (cours − PRU)` est égal à la plus-value écrite ;
- la **date du relevé** : une date précédée de « au », « arrêté au », « en date du », « situation », « as of »…, sinon la première date du document.

Si une seule ligne n'est pas sûre, ou s'il manque la date, le document n'est pas lu comme un relevé de portefeuille : le logiciel passe aux autres lectures.

### Ce que devient chaque position

Chaque position devient un **achat** de la quantité détenue, au PRU (ou, sans PRU, au cours du relevé), daté du jour du relevé, sans frais.

Exemple : la ligne `LVMH FR0000121014 10 650,20 731,00 7 310,00 808,00` d'un relevé « Positions au 31/12/2023 » se lit : 10 × 731,00 = 7 310,00 (valorisation) ; PRU 650,20, confirmé car 10 × (731,00 − 650,20) = 808,00, la plus-value écrite. Elle devient : `2023-12-31, ACHAT, MC.PA, 10 titres à 650,20 €`.

### Ce qu'il faut savoir

Le résumé de la barre latérale le rappelle : « Relevé de portefeuille PDF : chaque position est reprise comme un achat au prix de revient (PRU), à la date du relevé ; la performance est donc mesurée à partir de cette date. ».

- L'historique antérieur (dates d'achat réelles, ventes, dividendes passés) n'est pas connu.
- Le PRU pouvant être éloigné du cours de ce jour-là, une note « prix éloigné(s) du cours du jour » peut apparaître : c'est normal ici.
- La lecture ne vaut que pour un PDF texte, pas pour un relevé scanné.
- Ajoutez ensuite vos nouvelles opérations avec [[Ajouter des opérations]].

## Mon PDF est protégé par un mot de passe
<!-- fiche: import-pdf-protege | questions: mon pdf est protégé par un mot de passe ; la banque m'envoie des pdf avec mot de passe ; quel mot de passe pour ouvrir mon relevé ; mot de passe du pdf où le saisir ; mot de passe incorrect pour mon pdf ; le mot de passe du pdf est il enregistré ; pdf chiffré ; ouvrir un pdf verrouillé | mots: PDF protégé, mot de passe, PDF chiffré, verrouillé, déchiffrement, date de naissance, identifiant client, pypdfium2 -->

Certaines banques envoient leurs relevés et avis d'opéré dans des PDF protégés par un mot de passe. Le logiciel sait les ouvrir, à condition que vous lui donniez ce mot de passe.

### Ce qui s'affiche

À l'envoi d'un tel PDF (zone [[Envoyer un fichier (CSV, Excel ou PDF)]] de la barre latérale, ou page [[Ajouter des opérations]]), un encadré [[PDF protégé]] apparaît avec le nom du fichier et le message :

« PDF protégé par un mot de passe : saisissez-le pour l'ouvrir (souvent indiqué dans le courriel de la banque : date de naissance, identifiant client…). Il n'est pas enregistré. »

1. Tapez le mot de passe dans le champ [[Mot de passe du PDF]].
2. Cliquez sur [[Ouvrir le PDF]].
3. Le document est déchiffré, puis lu normalement (lecture automatique, sinon formulaire [[Compléter l'opération]]).

Si le mot de passe est faux, le message « Mot de passe incorrect. » s'affiche : réessayez.

### Que devient le mot de passe ?

- Le **mot de passe** n'est conservé nulle part : il sert une seule fois, à produire une copie sans protection du document.
- Cette **copie déchiffrée** est gardée en mémoire pendant la session, pour ne pas vous redemander le mot de passe à chaque action. Elle n'est pas écrite sur le disque et disparaît à la fermeture du logiciel.
- Si vous enregistrez ensuite le portefeuille dans votre espace, ce sont les opérations lues qui sont enregistrées, chiffrées, pas le PDF.

### Dans « Mon compte »

La rubrique [[Ajouter un portefeuille]] de [[Mon compte]] ne demande pas de mot de passe : envoyez un PDF protégé depuis la barre latérale.

## Envoyer plusieurs fichiers d'un coup
<!-- fiche: import-plusieurs-fichiers | questions: envoyer plusieurs fichiers en même temps ; importer tous mes avis d'opéré d'un coup ; j'ai 10 pdf comment les mettre ensemble ; plusieurs fichiers dans la barre latérale ; analyser les opérations déjà lues ; fichiers envoyés en attente ; un avis est dans deux fichiers est il compté deux fois ; réunir plusieurs relevés dans un portefeuille ; déposer tous mes pdf en une seule fois | mots: plusieurs fichiers, lot, envoi multiple, en une fois, d'un coup, Fichiers envoyés, avis d'opéré, fusion, en attente, doublons, barre latérale -->

La zone [[Envoyer un fichier (CSV, Excel ou PDF)]] de la barre latérale accepte plusieurs fichiers à la fois : par exemple tous les avis d'opéré d'une année, ou un export CSV et quelques avis PDF. Leurs opérations sont réunies dans un même portefeuille.

### Ce qui se passe

Un encadré [[Fichiers envoyés]] s'affiche à la place du tableau de bord et traite chaque fichier :

- un fichier lu automatiquement affiche « [nom] : [n] opération(s) lue(s). » ;
- un PDF protégé affiche l'encadré [[PDF protégé]] pour saisir son mot de passe (voir la fiche dédiée) ;
- un PDF non reconnu ouvre le formulaire [[Compléter l'opération]] ; une fois validé, son opération rejoint les autres ;
- un CSV ou un Excel non reconnu affiche sa raison et le conseil « Envoyez ce fichier seul pour ouvrir l'assistant d'import. » : l'assistant d'import ne s'ouvre pas pour un lot.

Quand tous les fichiers sont lus, l'analyse démarre. Tant que certains attendent, la liste « En attente : … » les nomme, et le bouton « Analyser les [n] opération(s) déjà lues » permet d'analyser sans eux.

### Les doublons entre fichiers

Une opération présente dans plusieurs fichiers (même date, même type, même titre, même quantité, même prix) n'est comptée qu'**une fois**. Le résumé de la barre latérale l'indique : « … opération(s) présente(s) dans deux fichiers comptée(s) une seule fois. ». Il reprend aussi les contrôles de chaque fichier (voir la fiche « Les contrôles après la lecture d'un PDF »).

### Garder le résultat

Comme pour un fichier seul, connecté, le bloc [[Enregistrer dans mon espace]] apparaît sous la zone d'envoi ; le nom proposé est du type « 3 fichiers ». Sans compte, le résultat ne vaut que pour la session.

### Pour compléter un portefeuille existant

Pour ajouter des avis à un portefeuille déjà enregistré, utilisez plutôt la page [[Ajouter des opérations]], dont la zone [[Fichiers (CSV, Excel ou PDF)]] accepte aussi plusieurs fichiers et repère les opérations déjà présentes dans le portefeuille.

## Diagnostiquer un PDF mal lu avec diagnostic_pdf.py
<!-- fiche: import-diagnostic-pdf | questions: comment savoir ce que le logiciel lit dans mon pdf ; diagnostic_pdf.py à quoi ça sert ; mon avis d'opéré est mal lu comment le signaler ; voir le texte extrait du pdf ; envoyer un rapport de lecture pdf ; diagnostic_pdf.txt ; debug pdf | mots: diagnostic, diagnostic_pdf.py, diagnostic_pdf.txt, diagnostic_pdf_anonyme.txt, débogage, texte extrait, PDF mal lu, signalement, terminal, anonyme -->

Le script `diagnostic_pdf.py`, à la racine du projet, montre exactement ce que le logiciel lit dans un PDF. Il s'adresse surtout à ceux qui disposent du code source (étudiants, développeurs) et sert à comprendre ou à faire corriger une mauvaise lecture.

### Le lancer

Dans un terminal ouvert dans le dossier du projet (par exemple le terminal de VS Code) :

```
python diagnostic_pdf.py "C:\chemin\vers\avis.pdf"
python diagnostic_pdf.py "C:\chemin\vers\avis.pdf" --anonyme
```

La seconde forme produit un rapport sans données personnelles (voir plus bas).

### Ce qu'il affiche

- le nom et la taille du fichier, le nombre de pages et le nombre de caractères de texte intégré ;
- **PDF texte** (au moins 20 caractères) : la mention « PDF TEXTE (lecture exacte) », puis le texte de chaque page et chaque tableau détecté, cellules séparées par `|` ;
- **PDF image** ou texte « codé » : le moteur de reconnaissance utilisé (RapidOCR, Tesseract ou AUCUN), puis, pour la première page, le texte lu dans chacun des quatre sens avec son score, et le texte finalement retenu après correction des ISIN et des nombres ;
- la **lecture par le contenu** : codes ISIN, dates, date proposée, proposition d'opération et nombres trouvés avec leur contexte (ce que proposerait le formulaire) ;
- enfin le **résultat** : le tableau d'opérations obtenu et sa nature, ou le message d'erreur.

| Nature | Lecture |
|---|---|
| `pdf_tableau` | relevé d'opérations en tableau |
| `pdf_avis` | avis d'opéré lu par ses intitulés |
| `pdf_contenu` | avis d'opéré lu par son contenu |
| `pdf_modele` | avis d'opéré lu avec un modèle appris |
| `pdf_positions` | relevé de portefeuille (positions et PRU) |
| `pdf_ocr` | lecture par reconnaissance de caractères |

Un PDF protégé par un mot de passe ne peut pas être diagnostiqué ainsi : le script s'arrête sur le message de PDF protégé.

### Le rapport

Le résultat est aussi enregistré dans le fichier `diagnostic_pdf.txt`, à côté du script. Attention : ce fichier contient tout le texte de votre document.

Avec `--anonyme`, le rapport est enregistré dans `diagnostic_pdf_anonyme.txt` : noms, lignes d'adresse, adresses électroniques, IBAN, téléphones et numéros de compte ou de référence y sont masqués ; les codes ISIN, les dates et les montants sont gardés. C'est ce fichier qu'il faut transmettre pour faire corriger une mauvaise lecture (voir la fiche « Envoyer un PDF mal lu sans données personnelles »).

## Envoyer un PDF mal lu sans données personnelles : le rapport anonymisé
<!-- fiche: import-rapport-anonymise | questions: comment signaler un pdf mal lu sans donner mes infos perso ; préparer un rapport anonymisé ça fait quoi ; rapport_lecture_pdf_anonymise.txt ; est ce que mon nom et mon iban sont enlevés ; envoyer mon avis d'opéré au créateur du logiciel ; diagnostic anonyme ; ajouter un vrai avis au banc d'essai ; dossier vrais_avis et attendus.csv | mots: rapport anonymisé, anonymisation, données personnelles, masquage, IBAN, numéro de compte, vrais_avis, attendus.csv, banc d'essai, signalement, diagnostic -->

Pour qu'un type d'avis mal lu soit mieux reconnu dans une prochaine version, le créateur du logiciel a besoin de son texte, pas de vos données personnelles. Le logiciel prépare donc un **rapport anonymisé**.

### Depuis le logiciel

Dans le formulaire [[Compléter l'opération]], ouvrez l'encadré [[Texte lu dans le document]] et cliquez sur [[Préparer un rapport anonymisé]]. Le fichier `rapport_lecture_pdf_anonymise.txt` est téléchargé. Il contient : le nom du fichier, l'indication d'un texte « codé », les codes ISIN et les dates trouvés, la date et l'opération proposées, puis le texte lu, anonymisé.

Rien n'est envoyé automatiquement : c'est vous qui transmettez ce fichier, si vous le souhaitez.

### Depuis le code source

`python diagnostic_pdf.py fichier.pdf --anonyme` produit le même rapport, suivi du résultat de la lecture, dans `diagnostic_pdf_anonyme.txt`.

### Ce qui est masqué, ce qui est gardé

| Masqué | Gardé |
|---|---|
| lignes contenant un nom ou une adresse (Monsieur, Madame, titulaire, client, adresse, numéro et nom de rue, code postal suivi d'une ville) | codes ISIN |
| adresses électroniques, remplacées par « [e-mail] » | dates |
| IBAN, remplacés par « [IBAN] » | montants, cours, quantités |
| numéros de téléphone, remplacés par « [téléphone] » | intitulés (« Quantité », « Cours », « Courtage »…) |
| numéros de compte, de référence, d'ordre, SIREN…, et longues suites de chiffres, remplacés par « [numéro] » | |

Le masquage est automatique : relisez le fichier avant de l'envoyer, une donnée écrite de façon inhabituelle pouvant lui échapper.

### Le banc d'essai des vrais avis

Le projet vérifie sa lecture des PDF sur 20 avis fictifs aux présentations très différentes (intitulés variés, anglais, colonnes sans traits, scans pâles, granuleux et de travers, texte « codé », relevé de portefeuille…), dans `tests/avis_fictifs.py` et `tests/test_pdf_universel.py`. Le dossier `tests/donnees/vrais_avis/` accueille en plus de **vrais** avis anonymisés. Son fichier `README.md` explique la marche à suivre :

1. masquer les données personnelles (rapport anonymisé ci-dessus ; pour le PDF lui-même, le noircir avec un logiciel de PDF) ;
2. copier le PDF dans ce dossier ;
3. ajouter une ligne par opération dans `attendus.csv`, au format `fichier;date;sens;isin;quantite;cours;frais` (date JJ/MM/AAAA, nombres avec un point décimal, frais vide si inconnus) ;
4. lancer `python -m pytest tests/test_pdf_universel.py` : chaque document doit être lu exactement comme indiqué.

## Comment vérifier ce que le logiciel a lu ?
<!-- fiche: import-verifier | questions: comment vérifier mon import ; est-ce que toutes mes opérations ont été importées ; où voir les transactions importées ; prix éloigné du cours du jour c'est grave ; le résumé dans la barre latérale ; combien d'opérations ont été lues ; contrôle qualité de l'import ; division d'actions détectée | mots: vérification, résumé de l'import, onglet Transactions, alerte de prix, écart, contrôle qualité, nombre d'opérations, split, division d'actions | aller: Analyse du portefeuille/Transactions | chiffres: nb_operations -->

Après un import, prenez une minute pour contrôler le résultat. Le logiciel vous y aide de trois façons.

### 1. Le résumé de la barre latérale

Après un import automatique, un encadré résume ce qui a été compris : nombre d'opérations et de titres, PDF lu (et de quelle façon), cours remplacés grâce au cours du marché, points à vérifier après la lecture d'un PDF, colonnes identifiées sans ligne de titres, tickers et ISIN convertis, ordre des dates, lignes ignorées, conversions de devise. En bas de la barre latérale, la ligne « Opérations » rappelle le nombre d'opérations analysées. Comparez-le au nombre de lignes de votre relevé.

### 2. Les alertes sur les prix

Chaque prix d'achat et de vente est comparé au cours de clôture du jour. Si des prix s'en écartent de plus de 25 %, une note le signale, par exemple : « AAPL : 2 prix éloigné(s) du cours du jour (écart médian +38 %) — ticker, devise ou division d'actions à vérifier. ».

Causes possibles :
- **mauvais ticker** (homonyme sur une autre place) ;
- **mauvaise devise** (euros lus comme des dollars, livres au lieu de pence) ;
- **division d'actions** : après une division, l'historique de cours peut ne plus correspondre au prix payé à l'époque (voir la fiche « Division ou regroupement d'actions ») ;
- simple erreur de saisie dans le fichier.

Une alerte n'empêche pas l'analyse : c'est à vous de juger.

### 3. L'onglet Transactions

Dans [[Historique des opérations]], toutes les opérations sont listées, des plus récentes aux plus anciennes, avec le type, le ticker, le titre, la quantité, le prix converti en euros, les frais, la devise et le [[Prix en devise]] tel que lu. Les filtres [[Type]] et [[Titres]] aident à retrouver une ligne. Une erreur se corrige directement avec [[Modifier les opérations]] (voir la fiche dédiée).

### Points de contrôle conseillés

- les quantités détenues (onglet Positions) correspondent à votre relevé de portefeuille ;
- les dates sont dans le bon ordre jour/mois ;
- les dividendes sont des montants totaux, avec une quantité de 0 ;
- les titres étrangers ont un prix cohérent dans leur devise.

## Enregistrer un portefeuille importé dans mon espace
<!-- fiche: import-enregistrer-espace | questions: comment garder mon portefeuille importé ; enregistrer dans mon espace où est le bouton ; je dois renvoyer mon fichier à chaque fois ; sauvegarder le portefeuille chiffré ; ajouter un portefeuille depuis mon compte ; le bouton enregistrer n'apparaît pas ; même nom de portefeuille il est remplacé | mots: enregistrer, sauvegarder, Mon espace, espace personnel, chiffré, Mon compte, Ajouter un portefeuille, persistance -->

Un fichier envoyé n'est conservé que pendant la session. Pour le retrouver plus tard, enregistrez-le dans votre espace personnel chiffré. Il faut être connecté (bouton [[Se connecter]] en haut de la barre latérale).

### Depuis la barre latérale

1. Envoyez le fichier avec [[Envoyer un fichier (CSV, Excel ou PDF)]] et laissez le logiciel l'analyser (assistant compris, si besoin).
2. Sous la zone d'envoi apparaît le bloc [[Enregistrer dans mon espace]], avec un champ [[Nom du portefeuille]] pré-rempli avec le nom du fichier.
3. Modifiez le nom si vous le souhaitez, puis cliquez sur [[Enregistrer]].
4. Le message « « … » est enregistré dans votre espace (chiffré). » confirme l'opération.

Ce qui est enregistré, c'est le portefeuille **après lecture et conversion**, au format du projet (tickers Yahoo, prix dans la devise de cotation) : il sera rouvert sans repasser par la détection.

Le bloc n'apparaît qu'une fois le portefeuille analysé avec succès. Pour ensuite travailler sur la version enregistrée, retirez le fichier de la zone d'envoi et choisissez « Mon espace · nom du portefeuille » dans la liste de la rubrique « Données ».

### Depuis la page « Mon compte »

Cliquez sur [[Mon compte]], puis utilisez la rubrique [[Ajouter un portefeuille]] : choisissez un fichier CSV, Excel ou PDF. S'il est reconnu automatiquement, le nombre d'opérations s'affiche ; saisissez le nom et cliquez sur [[Enregistrer]]. Sinon, un message vous invite à passer par la barre latérale, où l'assistant d'import vous guidera.

### Attention aux noms identiques

Enregistrer sous le nom d'un portefeuille déjà présent dans votre espace (sans tenir compte des majuscules) **remplace** ce portefeuille ; l'ancienne version reste récupérable avec [[Annuler la dernière modification]] dans « Mon compte ». Choisissez un nom différent si vous voulez garder les deux.

## Ajouter de nouvelles opérations à un portefeuille existant
<!-- fiche: import-ajouter-operations | questions: comment ajouter un nouvel achat ; mettre à jour mon portefeuille sans tout renvoyer ; ajouter un avis d'opéré à mon portefeuille ; où est le bouton ajouter des opérations ; ajouter les opérations du mois ; importer seulement les nouvelles transactions ; ajouter plusieurs pdf d'un coup ; mon fichier n'est pas lu dans ajouter des opérations | mots: ajouter des opérations, mise à jour, nouveaux mouvements, avis d'opéré, export, fusion, actualiser le portefeuille, nouvelles transactions -->

Inutile de renvoyer tout l'historique à chaque nouvel ordre : envoyez seulement les nouveaux mouvements, le logiciel les fusionne avec l'existant.

### Où se trouve la page

- dans la barre latérale, rubrique « Données », lien [[Ajouter des opérations]] sous la zone d'envoi : il s'applique au portefeuille affiché ;
- dans [[Mon compte]], sous chaque portefeuille de [[Mes portefeuilles]], bouton [[Ajouter des opérations]].

La page indique le portefeuille concerné. [[Retour au tableau de bord]] la referme sans rien changer.

### Trois façons d'ajouter

- **Onglet [[Depuis un fichier]]** : zone [[Fichiers (CSV, Excel ou PDF)]], qui accepte plusieurs fichiers à la fois (plusieurs avis d'opéré, un export des dernières opérations…). Chaque fichier passe par la même lecture automatique qu'à l'envoi principal ; le message indique le nombre d'opérations lues, par exemple « avis.pdf : 1 opération(s) lue(s). ». Un fichier déjà lu sur la page n'est pas relu. Un PDF protégé demande d'abord son mot de passe (encadré [[PDF protégé]]). Un avis de division ou de regroupement d'actions ouvre l'encadré [[Opération sur titres]] (voir la fiche « Division ou regroupement d'actions »).
- **Onglet [[Saisie manuelle]]** : un ordre saisi au clavier (voir la fiche dédiée).
- Les deux peuvent se combiner : toutes les opérations s'accumulent dans la même liste.

Si un fichier n'est pas compris automatiquement, la raison s'affiche ; pour un PDF, le formulaire [[Compléter l'opération]] s'ouvre avec les valeurs trouvées (voir la fiche dédiée). Cette page n'a pas d'assistant d'import : pour un format inhabituel, envoyez d'abord le fichier depuis la barre latérale, téléchargez le fichier converti, puis ajoutez-le ici.

### La vérification avant enregistrement

Le cadre [[Vérification avant enregistrement]] liste les opérations à ajouter. Les cellules sont modifiables. La colonne [[Ajouter]] permet de décocher une ligne ; la colonne [[Statut]] indique « nouvelle » ou « déjà dans le portefeuille » (les doublons sont décochés d'office). Une ligne de synthèse indique le nombre d'opérations ajoutées et le total après ajout. Les contrôles bloquants s'affichent en rouge (voir la fiche dédiée).

### L'enregistrement

Cliquez sur [[Enregistrer les opérations]]. Les opérations retenues sont fusionnées avec l'existant et triées par date.
- Portefeuille de votre espace : il est réenregistré, chiffré, et la version précédente est conservée ([[Annuler la dernière modification]] dans [[Mon compte]]).
- Fichier envoyé ou portefeuille d'exemple : l'ajout vaut pour la session ; téléchargez le fichier mis à jour pour le garder.

[[Tout effacer]] vide la liste en cours sans rien enregistrer.

## Division ou regroupement d'actions : ajuster les opérations antérieures
<!-- fiche: import-division-actions | questions: mon action a fait un split comment le saisir ; division d'actions par 4 que faire ; regroupement d'actions 10 pour 1 ; avis d'opération sur titres pdf ; appliquer aux opérations antérieures ça fait quoi ; après une division ma valeur est fausse ; reverse split ; parité 1 ancienne pour 4 nouvelles ; comment corriger mes quantités après un split | mots: division d'actions, split, regroupement, reverse split, opération sur titres, OST, parité, nominal, ajustement, Appliquer aux opérations antérieures -->

Après une **division** (« split ») ou un **regroupement** d'actions, Yahoo Finance corrige rétroactivement ses cours. Vos anciennes opérations, elles, sont toujours exprimées dans les anciennes unités : il faut les ajuster. Le logiciel le fait à partir de l'avis d'opération sur titres envoyé par votre courtier.

### Comment faire

1. Ouvrez la page [[Ajouter des opérations]] du portefeuille, onglet [[Depuis un fichier]].
2. Déposez l'avis de division ou de regroupement (PDF texte) dans la zone [[Fichiers (CSV, Excel ou PDF)]].
3. L'encadré [[Opération sur titres]] résume ce qui a été lu, par exemple « Division de Michelin (ML.PA) le 16/06/2023 : 1 ancienne → 4 nouvelles. », puis le nombre d'opérations qui seront converties.
4. Cliquez sur [[Appliquer aux opérations antérieures]].

### Ce que le logiciel reconnaît

- les mots « division » (du nominal, d'actions), « split », « fractionnement », « regroupement », « reverse split » ;
- un code ISIN ;
- la parité : « divisé par 4 », « 1 action ancienne pour 4 actions nouvelles », « 10 actions anciennes pour 1 action nouvelle », « parité : 1 pour 4 » ;
- la date d'effet : « date d'effet », « ex-date », « détachement », « à compter du »…, sinon la date d'exécution.

### Le calcul

Le facteur est le nombre de titres nouveaux pour un ancien : 4 pour une division par 4, 0,1 pour un regroupement de 10 en 1. Pour chaque **achat ou vente de ce titre daté d'avant la date d'effet** :

```
nouvelle quantité = quantité × facteur
nouveau prix      = prix ÷ facteur
```

Le montant (quantité × prix) ne change pas, et les cours de Yahoo Finance, déjà ajustés, correspondent de nouveau à vos prix. Les **dividendes** (montants totaux) ne changent pas, ni les opérations postérieures à la date d'effet.

Exemple : 10 Michelin achetées 120 € le 01/03/2022, division par 4 le 16/06/2023. L'achat devient 40 titres à 30 € (10 × 120 = 40 × 30 = 1 200 €). Un dividende de 45 € reçu en 2023 et un achat du 01/09/2023 restent tels quels.

### L'enregistrement

L'ajustement est enregistré comme les autres modifications : le message « … opération(s) de … ajustée(s). » le confirme.

- Portefeuille de votre espace : réenregistré chiffré, la version précédente reste récupérable avec [[Annuler la dernière modification]].
- Fichier envoyé ou portefeuille d'exemple : l'ajustement vaut pour la session ; téléchargez le fichier mis à jour.

### Si l'avis n'est pas reconnu

Sans opération du titre avant la date d'effet, l'encadré indique qu'il n'y a rien à ajuster. Si l'avis n'est pas lu (scan, parité absente), corrigez vous-même dans l'onglet Transactions avec [[Modifier les opérations]] : quantité multipliée et prix divisé par le même facteur. Les autres opérations sur titres (fusions, scissions, attributions gratuites) ne sont pas traitées automatiquement.

## Saisir un ordre à la main
<!-- fiche: import-saisie-manuelle | questions: comment saisir un achat à la main ; ajouter une opération manuellement ; saisie manuelle d'un dividende ; je n'ai pas de fichier je veux taper mon ordre ; quel prix mettre dans la saisie manuelle ; titre introuvable en saisie manuelle ; saisir un ordre avec l'isin ; le prix est en euros ou en dollars dans la saisie | mots: saisie manuelle, formulaire, ordre, ajout manuel, ticker, ISIN, code Bloomberg, Ajouter à la liste -->

La saisie manuelle se trouve dans la page [[Ajouter des opérations]], onglet [[Saisie manuelle]].

### Les champs

| Champ | Contenu |
|---|---|
| [[Date]] | Date de l'opération (aujourd'hui par défaut), au format JJ/MM/AAAA |
| [[Type]] | Achat, Vente ou Dividende |
| [[Titre]] | Ticker Yahoo, code ISIN, nom de société ou code Bloomberg |
| [[Quantité]] | Nombre de titres (1 par défaut) ; 0 pour un dividende |
| [[Prix unitaire (devise du titre) ou montant du dividende]] | Prix d'un titre dans sa devise de cotation (dollars pour Apple, pence pour Londres) ; pour un dividende, le montant total reçu |
| [[Frais (€)]] | Frais de courtage, en euros |

Cliquez sur [[Ajouter à la liste]] : l'opération rejoint le tableau de vérification. Le formulaire se vide pour une saisie suivante.

### La reconnaissance du titre

- Un ticker connu ou avec un suffixe de place Yahoo (`MC.PA`, `SAP.DE`) est pris tel quel.
- Un ISIN, un nom, un code Bloomberg ou un ticker court sont recherchés comme lors d'un import : table des ETF, mémoire, base locale, puis Yahoo Finance.
- En cas d'échec : « Titre introuvable : … Indiquez son ticker Yahoo Finance (ex. MC.PA). ».

Quand le titre est trouvé par une recherche, son nom officiel est repris dans la liste ; sinon, votre saisie sert de nom.

### Attention à la devise et au prix

Contrairement à un fichier importé, le prix saisi à la main **n'est pas vérifié** avec les cours : il doit être dans la devise de cotation du titre. Pour 10 actions Apple achetées à 185 $, saisissez 185, même si votre banque vous a débité des euros.

Un prix laissé à 0 pour un achat ou une vente bloque l'enregistrement (« Quantité ou prix nul pour … »). De même, une date future est refusée.

### Exemple

Achat de 5 Air Liquide à 172,10 € le 12/09/2024, 1,99 € de frais : Date 12/09/2024, Type Achat, Titre `AI.PA` (ou `Air Liquide`, ou `FR0000120073`), Quantité 5, Prix 172,10, Frais 1,99. Puis [[Ajouter à la liste]] et [[Enregistrer les opérations]].

## Comment les doublons sont-ils repérés ?
<!-- fiche: import-doublons | questions: j'ai importé deux fois le même avis ; le logiciel ajoute t il les opérations en double ; déjà dans le portefeuille ça veut dire quoi ; mon relevé chevauche l'ancien ; pourquoi ma ligne est décochée ; deux achats identiques le même jour ; règle des doublons ; tolérance de prix doublon | mots: doublons, déjà dans le portefeuille, chevauchement, détection des doublons, tolérance 0,5 %, idempotent, opération en double -->

Lors d'un ajout d'opérations, chaque nouvelle opération est comparée à celles du portefeuille et aux autres nouvelles opérations de la liste.

### La règle exacte

Deux opérations sont considérées comme identiques si elles ont :

- la **même date** ;
- le **même ticker** ;
- le **même type** (achat, vente, dividende) ;
- la **même quantité** (à un millionième près) ;
- un **prix égal à 0,5 % près** : `|prix 1 − prix 2| / max(prix 1, prix 2) ≤ 0,5 %`.

Les frais et le nom du titre ne sont pas comparés.

Exemple : un achat de 5 Air Liquide le 01/03/2024 à 170,00 € est déjà dans le portefeuille ; un relevé redonne la même opération à 170,40 €. Écart : 0,40 / 170,40 = 0,23 %, inférieur à 0,5 % : c'est un doublon. À 171,00 €, l'écart serait de 0,58 % et l'opération serait considérée comme nouvelle.

### Ce que fait le logiciel

Un doublon apparaît dans le tableau de vérification avec le statut « déjà dans le portefeuille » et sa case [[Ajouter]] décochée. Il n'est donc pas ajouté, sauf si vous recochez la case.

Conséquence pratique : ajouter deux fois le même fichier ne change rien. Vous pouvez donc envoyer un export qui chevauche le précédent sans craindre les doubles comptes.

### Deux ordres réellement identiques

Si vous avez vraiment passé deux ordres identiques le même jour au même prix, le second est pris pour un doublon : recochez sa case [[Ajouter]] avant d'enregistrer.

### Hors de la page d'ajout

Cette détection ne s'applique qu'à la page [[Ajouter des opérations]]. Un fichier complet envoyé seul depuis la barre latérale est lu tel quel : s'il contient deux fois la même ligne, elle sera comptée deux fois (pour un PDF, le résumé le signale : « … la même opération apparaît deux fois … »). Supprimez alors la ligne en trop dans l'onglet Transactions. Quand plusieurs fichiers sont envoyés ensemble, une opération identique (même date, type, titre, quantité et prix) n'est comptée qu'une fois.

## Quels contrôles bloquent l'enregistrement ?
<!-- fiche: import-controles | questions: pourquoi je ne peux pas enregistrer ; le bouton enregistrer est grisé ; vente de titres mais seulement 0 détenus ; opération datée dans le futur ; quantité ou prix nul message ; vente à découvert refusée ; message rouge dans la vérification ; le portefeuille ne peut pas être vide | mots: contrôles, blocage, vente à découvert, date future, quantité nulle, prix nul, cohérence, validation, erreur bloquante -->

Avant d'enregistrer un ajout ou une modification, le logiciel contrôle la cohérence de **tout le portefeuille** obtenu (anciennes et nouvelles opérations). Tant qu'un contrôle bloquant échoue, le message est affiché en rouge et le bouton d'enregistrement reste inactif.

### Les trois contrôles bloquants

| Contrôle | Message |
|---|---|
| Date future | « Opération datée dans le futur : [titre], le [date]. » |
| Quantité ou prix nul (achat ou vente) | « Quantité ou prix nul pour [titre], le [date]. » |
| Vente supérieure aux titres détenus | « Vente de [quantité] [titre] le [date], mais seulement [n] détenu(s) à cette date. » |

Une opération datée d'aujourd'hui est acceptée. Un dividende peut avoir une quantité nulle (c'est la règle du format).

### Comment la vente est vérifiée

Les opérations sont rejouées dans l'ordre des dates ; le même jour, un achat passe avant un dividende, lui-même avant une vente. Le logiciel suit la quantité détenue de chaque titre ; si une vente la rend négative, le contrôle échoue. Exemple : 3 LVMH achetées le 16/01/2024 ; une vente de 10 LVMH le 02/05/2024 donne « Vente de 10 LVMH le 02/05/2024, mais seulement 3 détenu(s) à cette date. ».

### Les autres alertes de l'onglet Transactions

- Supprimer un achat dont dépend une vente plus tardive déclenche le contrôle de vente ; le logiciel conseille alors : supprimez aussi la ou les ventes qui en dépendent (même titre, date postérieure).
- « Le portefeuille ne peut pas être vide : gardez au moins une opération. » bloque aussi.
- Si un titre n'est plus détenu après la modification, un avertissement le signale (« Après cette modification, ces titres ne sont plus détenus : … »), sans bloquer.

### Que faire

Corrigez la ligne en cause directement dans le tableau (date, quantité, prix) ou décochez-la. Si l'erreur vient d'une opération ancienne du portefeuille, corrigez-la dans l'onglet Transactions.

## Supprimer ou corriger une opération (onglet Transactions)
<!-- fiche: import-modifier-supprimer | questions: comment supprimer une opération ; j'ai mis un achat par erreur ; corriger la quantité d'un achat ; modifier le prix d'une transaction ; effacer une ligne de mon portefeuille ; je me suis trompé de date ; comment changer le ticker d'une opération ; retirer une vente fausse ; modifier les opérations ne s'enregistre pas | mots: modifier, supprimer, corriger, transaction, opération, édition, erreur de saisie, Modifier les opérations, Je confirme ces modifications | aller: Analyse du portefeuille/Transactions | chiffres: nb_operations -->

Toute opération du portefeuille peut être supprimée ou corrigée, dans l'espace « Analyse du portefeuille », onglet Transactions.

### Les étapes

1. Cliquez sur [[Modifier les opérations]] (à droite de [[Historique des opérations]]). Le tableau devient modifiable ; le bouton devient [[Terminer]].
2. Retrouvez la ligne grâce aux filtres [[Type]] et [[Titres]] ; les lignes masquées par les filtres ne sont pas modifiées.
3. Pour **supprimer**, cochez la case [[Supprimer]] de la ligne.
4. Pour **corriger**, modifiez directement la date, la quantité, le [[Prix (devise de cotation)]] ou les frais.
5. Un [[Récapitulatif]] liste les opérations « Supprimée » et « Corrigée », avec l'ancienne et la nouvelle valeur (par exemple « quantité : 10 → 1 »).
6. Les contrôles s'affichent (voir la fiche sur les contrôles bloquants).
7. Cochez [[Je confirme ces modifications]], puis cliquez sur [[Enregistrer les modifications]].

[[Tout annuler]] abandonne les changements en cours et quitte le mode modification.

### Ce qui est modifié

C'est le fichier du portefeuille lui-même qui est modifié, au format du projet : le prix est celui de la **devise de cotation** du titre (dollars, pence…), pas le prix converti en euros affiché en consultation. La colonne « Devise » le rappelle.

### Ce qui n'est pas modifiable ici

Le type, le ticker et le nom d'une opération ne se modifient pas, et l'on ne peut pas ajouter de ligne dans ce tableau. Pour changer le titre ou le type d'une opération : supprimez-la ici, puis ajoutez l'opération correcte avec [[Ajouter des opérations]].

### Où va la modification

- **Portefeuille de votre espace** : il est réenregistré chiffré ; la version précédente est conservée et [[Annuler la dernière modification]] permet d'y revenir.
- **Fichier envoyé ou portefeuille d'exemple** : la modification vaut pour la session ; le message invite à télécharger le fichier mis à jour.

## Annuler la dernière modification
<!-- fiche: import-annuler | questions: comment annuler ma dernière modification ; revenir en arrière après une suppression ; j'ai supprimé une opération par erreur ; annuler un ajout d'opérations ; restaurer la version précédente de mon portefeuille ; le bouton annuler a disparu ; on peut annuler plusieurs fois ; ctrl z | mots: annuler, undo, retour arrière, version précédente, restauration, Annuler la dernière modification, Mon compte | aller: Analyse du portefeuille/Transactions -->

### Pour un portefeuille de votre espace

À chaque ajout d'opérations ou modification enregistrée, le logiciel garde la version précédente du portefeuille (chiffrée elle aussi). Le bouton [[Annuler la dernière modification]] la restaure. Il se trouve :

- dans l'onglet Transactions, sous le tableau, hors du mode modification (ou en mode modification tant qu'aucun changement n'est saisi) ;
- dans [[Mon compte]], sous le portefeuille concerné.

Une bulle d'aide rappelle la date de la version restaurée (« Revenir à la version du … »).

### Un seul niveau d'annulation

Seule la **dernière** version précédente est gardée. Après une annulation, le bouton disparaît : on ne peut pas remonter plus loin. De même, une nouvelle modification remplace la version gardée. Enregistrer un fichier sous un nom déjà utilisé avec [[Enregistrer dans mon espace]] remplace le portefeuille de ce nom, et la version remplacée devient la version récupérable.

### Pour un fichier envoyé ou un portefeuille d'exemple

Après une modification faite dans l'onglet Transactions, le bouton [[Annuler la dernière modification]] apparaît aussi dans cet onglet et revient à l'état précédent pour la session. En revanche, un ajout fait avec [[Ajouter des opérations]] sans compte ne propose pas de bouton d'annulation : supprimez les lignes ajoutées dans l'onglet Transactions. Les changements de session disparaissent de toute façon à la fermeture du logiciel.

### Conseil

Avant une série de corrections importantes, téléchargez une copie du portefeuille : bouton [[Télécharger]] de [[Mon compte]], ou [[Télécharger le fichier mis à jour]] sans compte.

## Sans compte : récupérer le fichier mis à jour
<!-- fiche: import-sans-compte | questions: je n'ai pas de compte comment garder mes modifications ; télécharger le fichier mis à jour ; mes ajouts ont disparu à la fermeture ; où est le fichier corrigé ; utiliser le logiciel sans se connecter ; fichier mis à jour csv ; comment reprendre mon portefeuille la prochaine fois | mots: sans compte, session, téléchargement, fichier mis à jour, mis_a_jour.csv, sauvegarde, export CSV -->

Sans être connecté, vous pouvez tout faire : envoyer un fichier, ajouter des opérations, corriger ou supprimer des lignes. Mais **rien n'est enregistré sur l'ordinateur** : les changements ne valent que pour la session et disparaissent à la fermeture du logiciel.

### Le fichier mis à jour

Après un ajout ou une modification, un message le rappelle : « Téléchargez le fichier mis à jour pour le garder. ». Dans la barre latérale, à côté du lien [[Ajouter des opérations]], le bouton [[Télécharger le fichier mis à jour]] enregistre le portefeuille complet, au format du projet, sous le nom `<nom d'origine>_mis_a_jour.csv`. La ligne « Fichier » des informations de la barre latérale affiche alors « … (mis à jour) ».

La prochaine fois, envoyez simplement ce fichier : il est lu directement.

### Les autres téléchargements

- [[Télécharger le fichier converti (format du projet)]] dans l'assistant d'import : le fichier tel que lu, avant tout ajout.
- [[Télécharger la sélection (CSV)]] dans l'onglet Transactions : les opérations affichées, avec les **prix convertis en euros** et des colonnes supplémentaires (devise, prix en devise). Ce fichier sert à consulter ou à analyser dans un tableur ; pour reprendre le portefeuille plus tard, préférez le fichier mis à jour.

### Une seule mise à jour à la fois

Les changements de session s'appliquent à un seul portefeuille à la fois : enregistrer des ajouts ou des corrections sur un autre portefeuille remplace les changements en cours. Téléchargez le fichier mis à jour avant de passer à un autre portefeuille.

### Le plus simple

Créez un compte : vos portefeuilles sont enregistrés chiffrés, les ajouts et corrections sont conservés, et l'annulation est possible.

## Les portefeuilles d'exemple : à quoi servent-ils ?
<!-- fiche: import-exemples | questions: c'est quoi les portefeuilles d'exemple ; portefeuille diversifié multi-actifs d'où vient il ; je peux modifier un portefeuille d'exemple ; comment tester le logiciel sans mes données ; portefeuille actions monde ; mes modifications sur l'exemple sont-elles gardées ; supprimer les portefeuilles d'exemple de la liste | mots: portefeuilles d'exemple, démonstration, diversifié, actions monde, données de test, transactions_diversifie.csv, essai -->

### Ce qu'ils sont

Le logiciel est livré avec des portefeuilles d'exemple, proposés dans la liste de la rubrique « Données », après vos portefeuilles personnels. Selon les fichiers présents dans le dossier `data` :

| Nom affiché | Fichier |
|---|---|
| Portefeuille diversifié (multi-actifs) | `transactions_diversifie.csv` |
| Portefeuille actions monde | `transactions_mondial.csv` |
| Portefeuille d'exemple | `transactions.csv` (proposé seulement s'il est le seul fichier d'exemple) |

Le portefeuille diversifié est proposé en premier quand il existe. Les deux premiers sont fabriqués par les scripts `generer_portefeuille_diversifie.py` et `generer_portefeuille_mondial.py` du projet.

### À quoi ils servent

- découvrir le logiciel sans préparer de fichier ;
- s'entraîner à lire les indicateurs sur un portefeuille réaliste ;
- tester l'ajout, la correction et la suppression d'opérations sans risque ;
- voir à quoi ressemble un fichier au format du projet.

### Les modifier

Vous pouvez y ajouter des opérations ou en corriger : comme pour un fichier envoyé sans compte, les changements ne valent que pour la session. Le fichier d'origine n'est jamais modifié. Téléchargez le fichier mis à jour si vous voulez garder le résultat, ou enregistrez-le dans votre espace en l'envoyant ensuite depuis la zone d'envoi.

### Les retirer de la liste

La liste ne propose pas de les masquer ; ils restent disponibles, après vos portefeuilles personnels.

## Erreurs fréquentes à l'import et solutions
<!-- fiche: import-erreurs | questions: mon fichier ne s'importe pas ; message impossible d'analyser le portefeuille ; colonne manquante ou non reconnue ; le fichier est vide ; lignes ignorées date illisible ; aucune transaction lue ; vente impossible on n'en détient que ; erreur à l'import que faire ; prix non vérifiés pas de connexion | mots: erreur, dépannage, message d'erreur, problème d'import, colonne non reconnue, date illisible, titre introuvable, vente impossible, fichier vide, solutions -->

| Message ou symptôme | Cause probable | Solution |
|---|---|---|
| « Le fichier est vide. » | Fichier sans contenu, ou mauvaise feuille Excel | Vérifiez le fichier ; dans l'assistant, choisissez la bonne [[Feuille Excel]] |
| « Colonne(s) non reconnue(s) : … » | Nom de colonne inconnu, ou ligne des titres mal détectée | Dans l'assistant, associez la colonne à la main et vérifiez la [[Ligne des titres de colonnes]] |
| « Colonnes reconnues, mais sans certitude sur les quantités, prix et montants. » | Colonnes de nombres sans nom parlant | Vérifiez l'étape 2 de l'assistant, puis validez |
| « Titre(s) introuvable(s) : … » | ISIN ou nom inconnu, ou pas d'Internet | Saisissez le ticker à l'étape 3 de l'assistant |
| « … ligne(s) avec date illisible (lignes …) : ignorée(s) » | Date en toutes lettres, cellule vide ou abîmée | Corrigez la date dans le fichier |
| « … avec prix ou montant manquant » | Achat ou vente sans prix ni montant | Complétez le fichier, ou associez la colonne de montant |
| « … avec quantité nulle » | Achat ou vente à 0 titre | Vérifiez la colonne de quantité |
| « … avec titre manquant » | Cellule de titre vide, ou ISIN sans ticker | Complétez le fichier ou saisissez le ticker |
| « Aucune transaction lue. » | Toutes les lignes ignorées ou en erreur | Vérifiez les types (étape 3) et la correspondance (étape 2) |
| « Impossible d'analyser le portefeuille : Vente impossible le … » | Vente de plus de titres que détenus (achat manquant dans l'historique) | Ajoutez l'achat manquant ou corrigez la quantité |
| « Prix non vérifiés avec les cours du marché (pas de connexion). » | Pas d'Internet pendant l'import | Normal hors connexion ; vérifiez les titres étrangers |
| « … prix éloigné(s) du cours du jour … » | Mauvais ticker, devise ou division d'actions | Voir la fiche sur la vérification de l'import |
| Messages sur les PDF scannés ou au texte « codé » | PDF image, ou texte inextractible | Voir les fiches sur les PDF image et les scans refusés |
| « Opération non reconnue automatiquement dans ce PDF : complétez-la… » | PDF lisible, mais aucune opération sûre | Complétez l'opération dans le formulaire [[Compléter l'opération]] |
| « PDF protégé par un mot de passe : saisissez-le pour l'ouvrir… » | PDF chiffré par la banque | Saisissez le mot de passe dans [[Mot de passe du PDF]], puis [[Ouvrir le PDF]] |
| « Mot de passe incorrect. » | Mot de passe du PDF erroné | Vérifiez-le dans le courriel de la banque (date de naissance, identifiant client…) |
| « … le montant écrit (…) ne correspond pas à quantité × cours ± frais … », « … jour sans bourse … », « … (plus de 3 %) … », « … apparaît deux fois … » | Points repérés après la lecture d'un PDF | Voir la fiche « Les contrôles après la lecture d'un PDF » |
| Valeurs 1 000 fois trop petites | Séparateur de milliers lu comme décimal (`1.234`) | Retirez le séparateur de milliers dans le fichier |
| Actions de Londres 100 fois trop chères | Confusion livres et pence | Voir la fiche sur les pence |

### Les numéros de lignes

Dans les messages « ligne(s) avec … (lignes 3, 7) », les lignes sont numérotées à partir de la première ligne de données sous les titres de colonnes, sans compter les lignes vides. Au-delà de cinq lignes, la liste se termine par « … ».

### Quand l'analyse échoue après l'import

Le message « Impossible d'analyser le portefeuille : … » est suivi, pour un fichier envoyé, du bouton [[Ouvrir l'assistant d'import]] : il permet de relire le fichier autrement. Pour un portefeuille de votre espace, corrigez l'opération en cause.

### Bibliothèques manquantes (code source)

Si vous lancez le logiciel depuis le code source sans toutes les bibliothèques, les messages « Pour lire un PDF, installer pdfplumber… » ou « Pour lire un fichier Excel (.xlsx), installer openpyxl… » indiquent la commande à lancer. Les installateurs Windows et Mac les contiennent déjà.

## Exemple complet : de l'export du courtier au portefeuille à jour
<!-- fiche: import-exemple-complet | questions: exemple d'import pas à pas ; tutoriel import de portefeuille ; je débute par où commencer pour importer ; démonstration complète d'import ; comment faire de a à z ; exemple de relevé de courtier importé ; cas pratique import et mise à jour | mots: tutoriel, pas à pas, exemple, cas pratique, démonstration, import, mise à jour, relevé de courtier -->

Voici un cas complet : un relevé exporté en CSV, son import, son enregistrement, puis l'ajout d'un avis d'opéré et une correction.

### 1. Le fichier du courtier

```
Relevé des opérations - Compte titres n° 12345678
Édité le 05/10/2026

Date opération;Opération;Code ISIN;Libellé;Qté;Cours;Frais;Montant net
15/01/2024;Achat Comptant;FR0000121014;LVMH;3;740,00;2,00;2 222,00
12/03/2024;Achat Comptant;US0378331005;APPLE INC;10;157,50;5,00;1 580,00
22/05/2024;Coupon;FR0000121014;LVMH;0;;;39,00
28/06/2024;Frais de garde;;;;;;-12,00
18/09/2024;Vente Comptant;FR0000121014;LVMH;-1;700,00;2,00;698,00
```

### 2. L'envoi et la lecture automatique

Envoyez le fichier avec [[Envoyer un fichier (CSV, Excel ou PDF)]]. Le logiciel :

- détecte le point-virgule comme séparateur et ignore les trois premières lignes : la ligne des titres est la quatrième ;
- reconnaît les colonnes par leur nom : « Date opération » (date), « Opération » (type), « Code ISIN » (titre), « Libellé » (nom), « Qté » (quantité), « Cours » (prix), « Frais », « Montant net » (montant) ;
- lit les dates au format jour/mois (15/01 ne peut pas être un mois) ;
- classe « Achat Comptant » en achat, « Coupon » en dividende, « Vente Comptant » en vente, et ignore « Frais de garde » ;
- rend positive la quantité −1 de la vente ;
- convertit les ISIN en tickers (FR0000121014 en MC.PA, US0378331005 en AAPL) ;
- vérifie les devises : LVMH est en euros ; pour Apple, si 157,50 € multipliés par le taux EUR/USD du 12/03/2024 donnent un prix proche du cours d'Apple ce jour-là, le prix est reconverti en dollars.

Contrôle de cohérence : 3 × 740 + 2 = 2 222 ; 10 × 157,50 + 5 = 1 580 ; 1 × 700 − 2 = 698. Les colonnes sont cohérentes.

Résultat, au format du projet (avant la vérification des devises) :

```
date,type,ticker,nom,quantite,prix,frais
2024-01-15,ACHAT,MC.PA,LVMH,3,740,2
2024-03-12,ACHAT,AAPL,APPLE INC,10,157.5,5
2024-05-22,DIVIDENDE,MC.PA,LVMH,0,39,0
2024-09-18,VENTE,MC.PA,LVMH,1,700,2
```

Le résumé de la barre latérale indique notamment le nombre d'opérations et « 1 ligne(s) ignorée(s) (frais de garde, virements...). ». Si un titre n'avait pas été trouvé, l'assistant se serait ouvert à l'étape 3.

### 3. La vérification

Ouvrez l'onglet Transactions : quatre opérations. Dans l'onglet Positions : 2 LVMH et 10 Apple.

### 4. L'enregistrement

Connecté, saisissez « Compte titres » dans [[Nom du portefeuille]] sous [[Enregistrer dans mon espace]], puis cliquez sur [[Enregistrer]]. Retirez le fichier de la zone d'envoi et choisissez « Mon espace · Compte titres » dans la liste.

### 5. L'ajout d'un avis d'opéré

En octobre, vous achetez 4 LVMH. Cliquez sur [[Ajouter des opérations]], onglet [[Depuis un fichier]], et déposez l'avis d'opéré PDF. Le tableau [[Vérification avant enregistrement]] affiche l'achat avec le statut « nouvelle ». Vous déposez par erreur un second exemplaire du même avis : sa ligne est marquée « déjà dans le portefeuille » et décochée. Cliquez sur [[Enregistrer les opérations]].

### 6. Une correction

Vous constatez que l'achat d'octobre portait sur 3 titres, pas 4. Onglet Transactions, [[Modifier les opérations]], quantité 4 remplacée par 3. Le récapitulatif affiche « quantité : 4 → 3 ». Cochez [[Je confirme ces modifications]], puis [[Enregistrer les modifications]]. En cas d'erreur, [[Annuler la dernière modification]] restaure la version précédente.
