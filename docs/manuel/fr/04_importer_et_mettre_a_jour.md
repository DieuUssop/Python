# Importer et mettre à jour son portefeuille
<!-- chapitre: import | ordre: 4 -->

Ce chapitre explique comment donner vos opérations au logiciel : quels fichiers il accepte (CSV, Excel, PDF), le format du projet et son modèle, la lecture automatique des exports de banque ou de courtier, l'assistant d'import, la reconnaissance des titres (ticker, ISIN, nom, codes Bloomberg, Google ou Reuters) et des devises. Il décrit ensuite la mise à jour d'un portefeuille : ajout de nouvelles opérations, doublons, contrôles, correction ou suppression d'une opération, annulation. Il se termine par les erreurs fréquentes et un exemple complet.

## Quels fichiers peut-on importer dans le logiciel ?
<!-- fiche: import-fichiers-acceptes | questions: quels fichiers je peux importer ; quel format de fichier accepte le logiciel ; est-ce que je peux mettre un fichier excel ; ça prend les pdf de ma banque ; on peut importer un csv ; mon fichier xls ne passe pas ; est ce que je peux importer une capture d'écran ou une photo ; import depuis boursorama ou bourse direct ; le logiciel se connecte t il à mon courtier | mots: import, formats acceptés, CSV, Excel, xlsx, PDF, relevé, avis d'opéré, export courtier, fichier -->

Le logiciel lit vos opérations à partir d'un fichier que vous lui envoyez. Il ne se connecte ni à votre banque ni à votre courtier.

### Les trois formats acceptés

| Format | Extension | Exemples |
|---|---|---|
| CSV (texte) | `.csv` | Fichier au format du projet, export de courtier, fichier enregistré depuis Excel |
| Excel | `.xlsx` | Tableau personnel, export de banque |
| PDF | `.pdf` | Relevé d'opérations présenté en tableau, avis d'opéré (confirmation d'un ordre exécuté) |

Les zones d'envoi n'acceptent que ces trois extensions. L'ancien format Excel `.xls` n'est pas accepté : ouvrez le fichier dans Excel et enregistrez-le en `.xlsx` ou en CSV. Le logiciel reconnaît la nature réelle du fichier à son contenu (un PDF commence par `%PDF-`, un `.xlsx` est une archive ZIP), puis le lit en conséquence.

### Ce que le fichier doit contenir

Il faut un **historique d'opérations datées** : achats, ventes, et éventuellement dividendes. Une simple liste de positions (titres et quantités détenues aujourd'hui, sans dates d'achat) ne permet pas de calculer les performances. Trois informations sont indispensables pour chaque ligne : la **date**, le **titre** et la **quantité**, ainsi que le **prix unitaire ou le montant total**.

### Le format n'a pas besoin d'être parfait

Le fichier peut avoir ses propres noms de colonnes, en français ou en anglais, des lignes de titre au-dessus du tableau, des codes ISIN au lieu des tickers, des nombres « à la française » ou des montants en euros pour des titres étrangers : la détection automatique s'en charge (voir les fiches suivantes). Si elle a un doute, l'assistant d'import s'ouvre.

### Ce qui n'est pas possible

- une photo ou une capture d'écran au format image (`.png`, `.jpg`) n'est pas acceptée ;
- un PDF scanné n'est lu que si un moteur de reconnaissance de caractères est installé, et seulement pour des avis d'opéré (voir la fiche sur les PDF image) ;
- il n'existe pas de connexion automatique à un compte bancaire.

## Que se passe-t-il quand j'envoie un fichier ?
<!-- fiche: import-envoyer-fichier | questions: comment importer mon portefeuille ; ou est le bouton pour envoyer mon fichier ; j'ai mis mon fichier et rien ne se passe ; comment charger mes transactions ; le fichier envoyé remplace t il mon portefeuille ; pourquoi l'assistant s'ouvre au lieu du tableau de bord ; comment revenir à mon portefeuille enregistré après un envoi ; upload fichier | mots: envoyer un fichier, upload, barre latérale, Données, import automatique, détection, glisser-déposer, chargement -->

### Où envoyer le fichier

Dans la barre latérale, rubrique « Données », utilisez la zone [[Envoyer un fichier (CSV, Excel ou PDF)]] : glissez-y le fichier ou cliquez pour le choisir. Le fichier envoyé est **prioritaire** sur le portefeuille choisi dans la liste juste au-dessus : tant qu'il est présent dans la zone d'envoi, c'est lui qui est analysé.

### Ce que fait le logiciel

1. Le message « Lecture du fichier et vérification des prix avec les cours du marché... » s'affiche.
2. Le logiciel lit le fichier, reconnaît les colonnes, convertit les codes des titres en tickers Yahoo Finance et vérifie les prix avec les cours du marché.
3. **Si le résultat est sûr**, le portefeuille est analysé immédiatement. Un encadré dans la barre latérale résume ce qui a été compris, par exemple « Fichier reconnu automatiquement : 12 opération(s), 5 titre(s). ».
4. **S'il reste un doute** (colonne non reconnue, titre introuvable, ligne illisible), l'**assistant d'import** s'affiche à la place du tableau de bord, déjà pré-rempli : il suffit de vérifier et de valider.

Vous pouvez à tout moment reprendre la lecture à la main avec le bouton [[Ouvrir l'assistant d'import]], visible sous la zone d'envoi tant qu'un fichier y est présent.

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

Le sens est cherché dans le texte (achat, vente, souscription, rachat, buy, sell, dividende, coupon…). Faute de mot reconnu, l'opération est lue comme un achat : vérifiez-la.

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

1. **Hors connexion d'abord** : la table intégrée des ISIN d'ETF courants, puis la mémoire des titres déjà reconnus, puis la base locale de titres (par ticker, par ISIN, ou par nom).
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

## Titres reconnus sans Internet : la table des ETF et la mémoire
<!-- fiche: import-memoire-etf | questions: est-ce que l'import marche sans internet ; isin reconnu hors connexion ; mon etf amundi est il reconnu sans connexion ; c'est quoi la mémoire des titres ; le logiciel se souvient il des isin ; quels etf sont reconnus automatiquement ; la mémoire contient elle mes données ; il a reconnu un mauvais ticker la dernière fois | mots: hors connexion, mémoire des titres, memoire.csv, table des ISIN, ETF, base locale, Amundi, iShares, Vanguard, apprentissage -->

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

### La mémoire des titres reconnus

Chaque fois qu'un ISIN, un nom ou un code est trouvé grâce au moteur de recherche de Yahoo Finance, la correspondance est enregistrée dans un fichier de mémoire (`memoire.csv`, dans le dossier de la base de titres). La fois suivante, elle est retrouvée instantanément, même hors connexion.

- La mémoire est commune à tous les utilisateurs du logiciel sur cet ordinateur.
- Elle ne contient **aucune donnée de portefeuille** : seulement des correspondances entre codes (par exemple FR0000121014 → MC.PA), avec un nom et une date.

### La base locale de titres

Après la table et la mémoire, le logiciel cherche dans la base locale de titres livrée avec le logiciel : par ticker, par code ISIN, puis par nom (« LVMH » retrouve « LVMH Moët Hennessy Louis Vuitton »).

### Sans Internet, concrètement

Un ISIN d'ETF de la table, un titre déjà rencontré ou un titre de la base locale sont reconnus. Un titre totalement nouveau ne peut pas l'être : l'assistant s'ouvre et vous pouvez saisir son ticker à la main.

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

- **Pas de connexion** : la recherche en ligne est impossible ; seuls les titres de la table des ETF, de la mémoire et de la base locale sont reconnus.
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
<!-- fiche: import-pdf-releve | questions: comment importer un pdf de ma banque ; mon relevé pdf est il lu ; le logiciel lit il les tableaux des pdf ; relevé de compte titres pdf ; pdf de plusieurs pages ; aucune opération trouvée dans ce pdf ; pdf avec tableau d'opérations | mots: PDF, relevé d'opérations, tableau, pdfplumber, extraction, plusieurs pages, relevé de compte titres -->

### Comment le PDF est lu

Le logiciel lit le texte et les tableaux du PDF (bibliothèque pdfplumber), page par page.

- Un tableau est retenu s'il a au moins deux lignes, trois colonnes, et des dates sur au moins deux lignes : c'est la marque d'un vrai tableau d'opérations.
- Les tableaux de même largeur sont mis bout à bout (relevé sur plusieurs pages) ; l'en-tête répété en haut de chaque page n'est gardé qu'une fois.
- Le tableau obtenu suit ensuite exactement le même chemin qu'un fichier Excel : ligne des titres, reconnaissance des colonnes, ISIN, dates, nombres, devises.

### Quand le PDF est plutôt un avis d'opéré

Si le texte contient « avis d'opéré », « avis d'exécution », « confirmation d'exécution », « confirmation d'ordre » ou « trade confirmation », le logiciel lit d'abord le document comme un avis d'opéré (une opération par page). S'il n'y a pas de tableau d'opérations exploitable, il essaie aussi cette lecture.

### Si rien n'est trouvé

Le message « Aucune opération trouvée dans ce PDF (ni tableau d'opérations, ni avis d'opéré lisible). » s'affiche. Dans ce cas :

- téléchargez plutôt l'export Excel ou CSV des opérations depuis votre espace bancaire ;
- ou utilisez l'outil de diagnostic pour voir ce que le logiciel lit (voir la fiche sur `diagnostic_pdf.py`).

### Conseil

Sur le site de votre banque, préférez le bouton de téléchargement du document (« Format PDF », « Télécharger ») à la fonction « Imprimer » du navigateur : un PDF téléchargé contient le vrai texte, lu instantanément et exactement ; une page « imprimée en PDF » n'est parfois qu'une image.

## Importer un avis d'opéré PDF (exemple Bourse Direct)
<!-- fiche: import-avis-opere | questions: comment importer un avis d'opéré ; c'est quoi un avis d'opéré ; mon avis d'opéré bourse direct est il reconnu ; le logiciel a pris la date d'édition au lieu de la date d'exécution ; avis d'opéré en pdf vente comptant ; plusieurs avis dans un pdf ; confirmation d'ordre pdf ; quantité négative dans l'avis | mots: avis d'opéré, confirmation d'exécution, Bourse Direct, Format PDF, date d'exécution, courtage, ISIN, ordre exécuté -->

Un **avis d'opéré** est la confirmation que votre courtier envoie après chaque ordre exécuté. Le logiciel en extrait une opération par page.

### Ce qui est lu

| Information | Où le logiciel la cherche |
|---|---|
| Code ISIN | Premier code de 12 caractères dont la clé de contrôle est juste et qui compte au moins 6 chiffres |
| Date | Date d'exécution, d'opération ou de négociation, « exécuté le », « trade date » ; à défaut une date proche du mot exécution ou suivie de « achat »/« vente » ; les dates d'édition, d'émission, de règlement, de valeur ou de livraison sont écartées |
| Sens | Achat, vente, souscription, rachat, buy, sell, dividende, coupon… (achat par défaut) |
| Quantité | « Quantité », « Qté », « Nombre de titres », « Quantity », « Nominal » |
| Cours et devise | « Cours », « Prix unitaire », « Price », avec EUR, USD, GBP, €, $, £… |
| Frais | Somme de toutes les lignes « Courtage », « Commission », « Frais », « TTF » (taxe sur les transactions financières), « Fees » |
| Montant | « Montant net », « Net à débiter/créditer », sinon « Montant » ou « Brut » |
| Libellé | Après « Libellé : » ou « Valeur : », sinon le nom écrit juste après l'ISIN |

Les intitulés et valeurs peuvent être présentés en texte (« Quantité : 15 ») ou rangés dans un tableau. Une opération n'est retenue que si l'ISIN, la quantité et la date sont trouvés.

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

Un PDF de plusieurs pages contenant un avis par page donne une opération par page. Pour ajouter plusieurs avis séparés à un portefeuille existant, la page [[Ajouter des opérations]] accepte plusieurs fichiers à la fois.

### Après la lecture

Le résumé de la barre latérale indique « Avis d'opéré PDF lu. ». Vérifiez toujours l'opération : un avis inhabituel peut être mal interprété.

## Un PDF scanné ou « imprimé » : la reconnaissance de caractères
<!-- fiche: import-pdf-image | questions: mon pdf est une image ; pdf scanné est il lu ; c'est quoi l'ocr ; j'ai imprimé la page en pdf avec microsoft print to pdf ; reconnaissance de caractères comment ça marche ; mon pdf est tourné en paysage ; l'isin est mal lu ; rapidocr ou tesseract ; ça prend du temps à lire le pdf | mots: OCR, reconnaissance de caractères, PDF image, scan, RapidOCR, Tesseract, rotation, ISIN mal lu, Microsoft Print to PDF -->

### PDF texte et PDF image

Un PDF peut contenir du **vrai texte** (chaque caractère est enregistré, comme dans un PDF téléchargé depuis la banque) ou seulement une **image** de la page (scan, photo, ou page web imprimée avec « Microsoft Print to PDF »). Le logiciel considère qu'un PDF est une image quand il contient moins de 20 caractères de texte.

### La reconnaissance de caractères

Pour un PDF image, le logiciel « regarde » chaque page et y reconnaît les lettres et les chiffres, si un moteur est installé :

1. **RapidOCR**, bibliothèque qui fonctionne hors connexion, installée avec le fichier `requirements-ocr.txt` et intégrée aux installateurs lorsque leur fabrication a réussi à l'installer ;
2. à défaut, **Tesseract**, s'il est installé sur l'ordinateur (en français et en anglais si la langue française est disponible).

### Les précautions prises

- **Rotation** : chaque page est essayée dans les quatre sens (0°, 90°, 270°, 180°). Le sens retenu est celui qui fait apparaître le plus de codes ISIN valides et de mots utiles (quantité, cours, courtage, achat, vente, date, montant…). Dès qu'un sens est manifestement bon, les autres ne sont pas essayés.
- **Réparation des ISIN mal lus** : la lettre O lue à la place du chiffre 0 (`FRO013380607`), un I ou un l à la place de 1, S pour 5, B pour 8, Z pour 2, ou un caractère lu en double (`FRO0013380607`). Une correction n'est retenue que si l'ISIN corrigé a une clé de contrôle juste et au moins 6 chiffres : le logiciel n'invente jamais un code. Un mot comme « EURONEXTPARIS » n'est jamais pris pour un ISIN.
- **Mots collés** : la lecture tolère les mots accolés (« VENTECOMPTANT »).

Le texte reconnu est ensuite lu comme un avis d'opéré. La reconnaissance ne lit que des avis d'opéré : un relevé en tableau scanné n'est en général pas exploitable.

### À vérifier systématiquement

La lecture d'une image prend plusieurs secondes et reste moins sûre qu'un PDF texte. Le résumé l'indique : « PDF image lu par reconnaissance de caractères : vérifiez les opérations (onglet « Transactions »). ». Contrôlez la date, la quantité et le cours.

## Pourquoi mon PDF scanné est-il refusé ?
<!-- fiche: import-pdf-scan-refuse | questions: pdf scanné refusé ; message impossible à lire automatiquement ; aucune opération n'a été reconnue dans mon pdf image ; pourquoi mon scan ne passe pas ; le logiciel refuse ma photo d'avis d'opéré ; que faire si mon pdf est une image ; installer la reconnaissance de caractères | mots: PDF scanné, refus, PDF image, OCR non installé, message d'erreur, Format PDF, saisie manuelle, requirements-ocr -->

Deux messages peuvent apparaître pour un PDF image.

### « PDF scanné (image) : impossible à lire automatiquement… »

Aucun moteur de reconnaissance de caractères n'est installé : le PDF ne contient aucun texte à lire. Le message propose trois solutions : exporter le relevé en PDF depuis votre espace bancaire, ou en Excel / CSV, ou saisir l'opération à la main.

Si vous lancez le logiciel depuis le code source, vous pouvez installer le moteur avec la commande `python -m pip install -r requirements-ocr.txt`.

### « PDF image (scan, photo ou page imprimée avec « Imprimer en PDF ») : le texte a été lu par reconnaissance de caractères, mais aucune opération n'a été reconnue… »

Le moteur a bien lu la page, mais n'y a pas trouvé à la fois un code ISIN valide, une quantité et une date. Causes possibles : image floue ou de faible résolution, ISIN illisible, document qui n'est pas un avis d'opéré (relevé en tableau, synthèse de portefeuille).

### Pourquoi le logiciel refuse plutôt que deviner

Une opération mal lue (une quantité de 60 lue 80, un cours décalé d'une virgule) fausserait tous les calculs sans que vous le remarquiez. Le logiciel préfère donc refuser clairement un document qu'il ne comprend pas.

### Les solutions, de la plus sûre à la moins sûre

1. **Télécharger le vrai PDF** depuis votre espace bancaire, avec le bouton « Format PDF » ou « Télécharger » plutôt que « Imprimer » : le texte est alors lu exactement.
2. **Exporter les opérations en Excel ou CSV**, si votre banque le propose.
3. **Saisir l'opération à la main** : page [[Ajouter des opérations]], onglet [[Saisie manuelle]].
4. Lancer le diagnostic du PDF pour comprendre ce qui a été lu (voir la fiche suivante).

## Diagnostiquer un PDF mal lu avec diagnostic_pdf.py
<!-- fiche: import-diagnostic-pdf | questions: comment savoir ce que le logiciel lit dans mon pdf ; diagnostic_pdf.py à quoi ça sert ; mon avis d'opéré est mal lu comment le signaler ; voir le texte extrait du pdf ; envoyer un rapport de lecture pdf ; diagnostic_pdf.txt ; debug pdf | mots: diagnostic, diagnostic_pdf.py, diagnostic_pdf.txt, débogage, texte extrait, PDF mal lu, signalement, terminal -->

Le script `diagnostic_pdf.py`, à la racine du projet, montre exactement ce que le logiciel lit dans un PDF. Il s'adresse surtout à ceux qui disposent du code source (étudiants, développeurs) et sert à comprendre ou à faire corriger une mauvaise lecture.

### Le lancer

Dans un terminal ouvert dans le dossier du projet (par exemple le terminal de VS Code) :

```
python diagnostic_pdf.py "C:\chemin\vers\avis.pdf"
```

### Ce qu'il affiche

- le nom et la taille du fichier, le nombre de pages et le nombre de caractères de texte intégré ;
- **PDF texte** (au moins 20 caractères) : la mention « PDF TEXTE (lecture exacte) », puis le texte de chaque page et chaque tableau détecté, cellules séparées par `|` ;
- **PDF image** : le moteur de reconnaissance utilisé (RapidOCR, Tesseract ou AUCUN), puis, pour la première page, le texte lu dans chacun des quatre sens avec son score, et le texte finalement retenu après correction des ISIN ;
- enfin le **résultat** : le tableau d'opérations obtenu et sa nature (`pdf_tableau` pour un relevé, `pdf_avis` pour un avis d'opéré, `pdf_ocr` pour une lecture par reconnaissance de caractères), ou le message d'erreur.

### Le rapport

Le résultat est aussi enregistré dans le fichier `diagnostic_pdf.txt`, à côté du script. C'est ce fichier qu'il faut transmettre pour faire corriger une mauvaise lecture.

Attention : il contient le texte de votre document. Masquez votre nom et votre numéro de compte avant de l'envoyer.

## Comment vérifier ce que le logiciel a lu ?
<!-- fiche: import-verifier | questions: comment vérifier mon import ; est-ce que toutes mes opérations ont été importées ; où voir les transactions importées ; prix éloigné du cours du jour c'est grave ; le résumé dans la barre latérale ; combien d'opérations ont été lues ; contrôle qualité de l'import ; division d'actions détectée | mots: vérification, résumé de l'import, onglet Transactions, alerte de prix, écart, contrôle qualité, nombre d'opérations, split, division d'actions | aller: Analyse du portefeuille/Transactions | chiffres: nb_operations -->

Après un import, prenez une minute pour contrôler le résultat. Le logiciel vous y aide de trois façons.

### 1. Le résumé de la barre latérale

Après un import automatique, un encadré résume ce qui a été compris : nombre d'opérations et de titres, PDF lu, colonnes identifiées sans ligne de titres, tickers et ISIN convertis, ordre des dates, lignes ignorées, conversions de devise. En bas de la barre latérale, la ligne « Opérations » rappelle le nombre d'opérations analysées. Comparez-le au nombre de lignes de votre relevé.

### 2. Les alertes sur les prix

Chaque prix d'achat et de vente est comparé au cours de clôture du jour. Si des prix s'en écartent de plus de 25 %, une note le signale, par exemple : « AAPL : 2 prix éloigné(s) du cours du jour (écart médian +38 %) — ticker, devise ou division d'actions à vérifier. ».

Causes possibles :
- **mauvais ticker** (homonyme sur une autre place) ;
- **mauvaise devise** (euros lus comme des dollars, livres au lieu de pence) ;
- **division d'actions** : après une division, l'historique de cours peut ne plus correspondre au prix payé à l'époque ;
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

- **Onglet [[Depuis un fichier]]** : zone [[Fichiers (CSV, Excel ou PDF)]], qui accepte plusieurs fichiers à la fois (plusieurs avis d'opéré, un export des dernières opérations…). Chaque fichier passe par la même lecture automatique qu'à l'envoi principal ; le message indique le nombre d'opérations lues, par exemple « avis.pdf : 1 opération(s) lue(s). ». Un fichier déjà lu sur la page n'est pas relu.
- **Onglet [[Saisie manuelle]]** : un ordre saisi au clavier (voir la fiche dédiée).
- Les deux peuvent se combiner : toutes les opérations s'accumulent dans la même liste.

Si un fichier n'est pas compris automatiquement, la raison s'affiche. Cette page n'a pas d'assistant d'import : pour un format inhabituel, envoyez d'abord le fichier depuis la barre latérale, téléchargez le fichier converti, puis ajoutez-le ici.

### La vérification avant enregistrement

Le cadre [[Vérification avant enregistrement]] liste les opérations à ajouter. Les cellules sont modifiables. La colonne [[Ajouter]] permet de décocher une ligne ; la colonne [[Statut]] indique « nouvelle » ou « déjà dans le portefeuille » (les doublons sont décochés d'office). Une ligne de synthèse indique le nombre d'opérations ajoutées et le total après ajout. Les contrôles bloquants s'affichent en rouge (voir la fiche dédiée).

### L'enregistrement

Cliquez sur [[Enregistrer les opérations]]. Les opérations retenues sont fusionnées avec l'existant et triées par date.
- Portefeuille de votre espace : il est réenregistré, chiffré, et la version précédente est conservée ([[Annuler la dernière modification]] dans [[Mon compte]]).
- Fichier envoyé ou portefeuille d'exemple : l'ajout vaut pour la session ; téléchargez le fichier mis à jour pour le garder.

[[Tout effacer]] vide la liste en cours sans rien enregistrer.

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

Cette détection ne s'applique qu'à la page [[Ajouter des opérations]]. Un fichier complet envoyé depuis la barre latérale est lu tel quel : s'il contient deux fois la même ligne, elle sera comptée deux fois. Supprimez alors la ligne en trop dans l'onglet Transactions.

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
| Messages sur les PDF scannés | PDF image | Voir les fiches sur les PDF image et les scans refusés |
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
