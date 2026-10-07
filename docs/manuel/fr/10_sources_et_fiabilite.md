# D'où viennent les données et quelle confiance leur accorder
<!-- chapitre: sources | ordre: 10 -->

Ce chapitre indique l'origine de chaque donnée utilisée par le logiciel : cours de bourse, base locale de titres, devises, reconnaissance des codes ISIN, composition des ETF, classement des titres, indices de référence, taux sans risque et fond de carte. Il détaille ensuite, honnêtement, ce que le logiciel vérifie, ce qu'il ne vérifie pas, et que faire si un chiffre vous paraît faux.

## D'où viennent les données du logiciel ?
<!-- fiche: sources-vue-ensemble | questions: d'où viennent les données ; quelle est la source des cours ; d'ou viennent les chiffres du logiciel ; quelles sources de données sont utilisées ; les données viennent de bloomberg ; qui fournit les prix ; source des informations sur les etf ; le logiciel est-il connecté à ma banque | mots: sources, provenance, origine des données, Yahoo Finance, Wikipédia, MSCI, BCE, Natural Earth, référentiel -->

Le logiciel n'a pas d'abonnement à un fournisseur professionnel (Bloomberg, Refinitiv…) et n'est relié à aucune banque. Ses données viennent des sources suivantes.

| Donnée | Source | Mise à jour |
|---|---|---|
| Cours quotidiens des titres, des indices et des taux de change | Yahoo Finance, par la bibliothèque Python `yfinance` | à chaque analyse avec Internet ; sinon base locale et cache |
| Devise de cotation de chaque titre | Yahoo Finance, sinon base locale, sinon règle d'après le code du titre | une fois par titre, puis gardée |
| Liste des titres de la base locale | pages Wikipédia de 32 indices boursiers, une liste de 66 ETF et le référentiel du projet | à la construction de la base |
| Correspondance ISIN, nom ou code Bloomberg vers le ticker | table intégrée de 31 ETF, mémoire locale, base locale, puis moteur de recherche de Yahoo Finance | à chaque import d'un titre inconnu |
| Pays, région, secteur, classe d'actifs, duration | fichier `data/referentiel.csv` du projet, complété par la base locale | fixe, livré avec le logiciel |
| Composition des ETF par pays et secteur | fiches MSCI au 30/09/2026 et ordres de grandeur 2025-2026 | fixe, à revoir une fois par an |
| Poids régionaux de l'indice pour l'attribution de performance | MSCI ACWI IMI au 30/06/2026 | fixe |
| Taux sans risque | valeur fixe de 2,50 % (taux de la facilité de dépôt de la BCE), modifiable | réglage |
| Contours des pays (carte du monde) | Natural Earth, domaine public | téléchargés une fois |

### Ce qui vient de vous

Les opérations (dates, quantités, prix, frais, dividendes) viennent uniquement de vos fichiers ou de vos saisies. Le logiciel les contrôle, mais ne les corrige jamais à votre insu.

### Où voir la source des cours

- Dans le bandeau en haut de page : « Cours en direct · Yahoo Finance » (point vert) ou « Cours en cache (hors ligne) » (point orange), et la mention « Données au » suivie de la date du dernier cours de l'historique.
- En bas de la barre latérale, la ligne « Cours » : « Yahoo Finance (en direct) », ou « cache local du » suivi d'une date, avec la mention « Yahoo Finance injoignable ».

## Quels cours exactement le logiciel utilise-t-il ?
<!-- fiche: sources-cours-yahoo | questions: le logiciel prend le cours de clôture ou le cours ajusté ; adj close ou close ; auto_adjust c'est quoi ; quel prix est utilisé pour valoriser mon portefeuille ; les cours sont ils en temps réel ; pourquoi le cours n'est pas celui de mon courtier ; cours de clôture ajusté des dividendes ; d'où vient le dernier cours | mots: cours de clôture, Close, Adj Close, auto_adjust, cours ajusté, Yahoo Finance, yfinance, temps réel, dernier cours -->

### Le cours de clôture non ajusté des dividendes

Le logiciel télécharge les cours avec le réglage `auto_adjust=False` de la bibliothèque `yfinance` et retient la colonne **`Close`** (cours de clôture). Il n'utilise **jamais** la colonne `Adj Close` (cours ajusté des dividendes). Ce choix est le même partout : historique des analyses, dernier cours, construction de la base locale.

Pourquoi ? Pour valoriser votre portefeuille au **vrai cours affiché en bourse**, celui que vous voyez chez votre courtier, et pour compter les dividendes une seule fois : par les lignes « DIVIDENDE » de votre fichier.

### Deux usages

| Usage | Ce qui est demandé à Yahoo Finance |
|---|---|
| Historique (valeur jour par jour, performance, risque) | les cours de clôture quotidiens depuis la date de votre première opération |
| Valeur actuelle | les cours des 5 derniers jours ; le logiciel garde la dernière valeur connue de chaque titre |

Le dernier cours est donc le plus récent que Yahoo Finance fournit : le cours de clôture de la dernière séance, ou une valeur de la séance en cours si la bourse est ouverte. Les 5 jours servent à toujours trouver un cours le week-end et les jours fériés.

### Jours sans cotation

Quand une place est fermée (jour férié local), la valeur du titre ce jour-là est le dernier cours connu. Une opération saisie un jour sans cotation (un samedi, par exemple) est rattachée au jour de bourse suivant.

### Pourquoi un écart avec votre courtier ?

- moment différent (cours de clôture contre cours du moment) ;
- autre place de cotation (le même titre à Paris et à Amsterdam, ou un ETF coté dans deux devises) ;
- conversion en euros au taux de change de Yahoo Finance, et non à celui de votre banque ;
- éventuelle erreur de la source (voir la fiche « Un cours me semble faux »).

## Dividendes et divisions d'actions : ce qu'implique le cours non ajusté
<!-- fiche: sources-dividendes-divisions | questions: mes dividendes sont-ils pris en compte dans la performance ; le cours baisse le jour du dividende ; division d'actions split ma performance est fausse ; mon titre a fait un split et je perds 90 % ; comment saisir une division d'actions ; etf capitalisant ou distribuant ; regroupement d'actions ; le logiciel gère t il les splits | mots: dividende, détachement, split, division d'actions, regroupement, ETF capitalisant, ETF distribuant, opération sur titres, ajustement -->

### Les dividendes

Avec un cours non ajusté, le cours d'une action baisse à peu près du montant du dividende le jour de son détachement. Le logiciel compense cette baisse **seulement si le dividende figure dans vos opérations** (une ligne « DIVIDENDE », avec le montant total reçu). Il ne télécharge pas les dividendes à votre place.

- **Dividendes enregistrés** : ils s'ajoutent au gain total et à la performance.
- **Dividendes oubliés** : la performance est sous-estimée d'autant.
- **ETF capitalisant** : les dividendes sont réinvestis dans le fonds, donc déjà dans son cours ; il n'y a rien à saisir.
- **ETF distribuant** : il verse des dividendes, à enregistrer comme pour une action.

Le même principe vaut pour l'indice de référence : un ETF capitalisant donne une performance « dividendes réinvestis », un indice de prix comme le CAC 40 (`^FCHI`) une performance « hors dividendes ». Le nom de chaque indice le précise.

### Les divisions d'actions

Yahoo Finance corrige rétroactivement ses cours de clôture après une division d'actions (« split »). Le logiciel, lui, ne connaît que les types d'opération ACHAT, VENTE et DIVIDENDE : **il ne gère pas les divisions ni les regroupements d'actions**.

Exemple : vous avez acheté 10 actions à 800 €. La société divise ensuite chaque action en 10. Yahoo affiche désormais un historique d'environ 80 € pour la date de votre achat. Votre fichier, lui, indique toujours 10 actions : le logiciel valoriserait 10 × 80 € = 800 € au lieu de 8 000 €.

À l'import, le contrôle des prix le signale : le prix du fichier est éloigné du cours du jour (ici, écart de +900 %), avec la mention « ticker, devise ou division d'actions à vérifier ».

**La correction** : exprimez l'opération en titres d'après la division, sans changer le montant. Ici, 100 actions à 80 € (100 × 80 = 8 000 €). Vous pouvez le faire dans l'onglet Transactions avec [[Modifier les opérations]]. Le prix de revient total, les frais et les flux restent identiques.

### Autres opérations sur titres

Fusions, scissions, changements de code ou attributions gratuites ne sont pas traités automatiquement. Il faut les traduire vous-même en achats et ventes.

## La base locale de titres : que contient-elle ?
<!-- fiche: sources-base-locale | questions: c'est quoi la base locale de titres ; combien de titres sont dans la base ; quels indices sont couverts ; depuis quelle date sont les cours ; mon action n'est pas dans la base ; data base titres.csv ça contient quoi ; la base contient elle les etf ; les cours remontent à quand | mots: base locale, base de titres, titres.csv, paquets npz, univers, historique, 2015, 2007, hors connexion -->

La base locale est la « mémoire » du logiciel : elle lui permet de fonctionner sans Internet et d'aller plus vite en ligne. Elle est rangée dans le dossier `data/base`.

### Son contenu

| Élément | Contenu |
|---|---|
| `titres.csv` | la fiche de chaque titre : ticker Yahoo, nom, ISIN (quand il est connu), pays, région, secteur, classe d'actifs, devise, indices dont il fait partie |
| `cours/paquet_00.npz` à `paquet_31.npz` | les cours de clôture quotidiens, répartis en 32 fichiers compressés |
| `memoire.csv` | les correspondances apprises lors des imports (ISIN, nom ou code vers ticker) |
| `pays.geojson` | les contours des pays, pour la carte du monde |

### L'univers couvert

- **Actions** : la composition, lue sur Wikipédia, de 32 indices : S&P 500, Nasdaq-100, Dow Jones, Russell 1000, CAC 40, SBF 120, CAC Mid 60, DAX, MDAX, SDAX, TecDAX, FTSE 100, FTSE 250, Euro Stoxx 50, AEX, AMX, BEL 20, IBEX 35, FTSE MIB, SMI, SMIM, OMX Stockholm 30, OMX Copenhague 25, OMX Helsinki 25, OBX, ATX, PSI, ISEQ 20, Nikkei 225, S&P/TSX 60, S&P/ASX 200 et Hang Seng. Le projet l'estime à environ 3 500 actions.
- **ETF** : une liste de 66 ETF courants (actions, obligations, or, monétaire), européens et américains.
- **Référentiel du projet** : les titres de `data/referentiel.csv`.
- **Marché** : 16 indices boursiers et 12 taux de change de l'euro (dollar américain, livre, franc suisse, yen, dollars canadien, australien, de Hong Kong et de Singapour, couronnes danoise, suédoise et norvégienne, zloty).

### La profondeur d'historique

- depuis le **1er janvier 2015** pour les actions et les ETF ;
- depuis le **1er janvier 2007** pour les indices et les taux de change, ce qui permet de rejouer la crise de 2008 dans les stress tests.

### Précision et limites

- Les cours sont stockés avec environ 7 chiffres significatifs, ce qui suffit largement pour des cours de bourse.
- La liste reflète la composition des indices **au moment de la construction** : une société sortie d'un indice auparavant n'y est pas. Si vous la détenez, ses cours sont téléchargés à la première analyse en ligne, puis ajoutés à la base.
- L'ISIN n'est renseigné que si la page Wikipédia de l'indice le donne.
- Le nombre exact de titres dépend de la version livrée : certaines pages Wikipédia peuvent être illisibles le jour de la construction, et les codes inconnus de Yahoo Finance sont écartés.

## Comment la base de titres est construite et mise à jour
<!-- fiche: sources-base-construction | questions: comment mettre à jour la base de titres ; construire_base_titres.py comment ça marche ; la base se met-elle à jour toute seule ; construire_base.bat ; mettre a jour les cours hors connexion ; combien de temps pour construire la base ; base cumulative ça veut dire quoi ; echecs.csv c'est quoi | mots: construction, mise à jour, construire_base_titres.py, construire_base.bat, --mise-a-jour, base cumulative, Wikipédia, lots, reprise, echecs.csv -->

### La construction complète

Elle est faite par le script `construire_base_titres.py` (sous Windows, depuis le code source, par un double-clic sur `construire_base.bat`), avec Internet :

1. lecture de la composition des 32 indices sur Wikipédia ;
2. ajout des 66 ETF et des titres du référentiel ;
3. téléchargement du fond de carte ;
4. téléchargement des cours : d'abord les indices et taux de change depuis 2007, puis les titres depuis 2015, **par lots de 100 titres**, avec une pause de 2 secondes entre deux lots et jusqu'à 3 essais par lot en cas de refus de Yahoo Finance.

Le projet l'estime à environ une heure. En cas d'interruption, relancer la commande reprend là où elle s'était arrêtée. Les codes que Yahoo Finance ne reconnaît pas sont listés dans `data/base/echecs.csv`.

Les versions installées sont livrées avec la base présente dans le projet au moment de leur fabrication.

### La mise à jour

```
python construire_base_titres.py --mise-a-jour
```

Le script reprend tous les titres qui ont des cours dans la base, et télécharge leurs cours depuis la dernière date connue moins 7 jours. Il ne dure que quelques minutes. L'option `--liste` reconstruit seulement la liste des titres, sans les cours.

### Une base cumulative

La base se complète aussi **toute seule** :

- chaque historique téléchargé pour une analyse en ligne y est ajouté ;
- les nouvelles valeurs remplacent les anciennes pour les mêmes dates ;
- seuls les fichiers modifiés sont réécrits, par un fichier temporaire renommé ensuite : une coupure ne laisse jamais de fichier abîmé.

Ainsi, un titre analysé une fois avec Internet reste disponible hors connexion.

### Lors d'une nouvelle version

L'installation d'une nouvelle version remplace la base par celle qui est livrée avec cette version. Sur Mac, la mémoire des titres reconnus est conservée. Les cours que votre propre utilisation avait ajoutés seront de nouveau téléchargés à la prochaine analyse en ligne.

## Le cache des cours et le bouton « Actualiser les cours »
<!-- fiche: sources-cache | questions: c'est quoi le cache ; actualiser les cours ça sert à quoi ; les cours ne se mettent pas à jour ; pourquoi les cours sont les mêmes qu'il y a une heure ; cache_prix.csv ; cours en cache hors ligne ; vider le cache ; forcer le téléchargement des cours | mots: cache, mémoire, actualiser, rafraîchir, refresh, une heure, cache_prix.csv, cache_historique.csv, hors ligne -->

Le logiciel garde les cours à deux endroits pour éviter de les retélécharger sans cesse.

### 1. En mémoire, pendant une heure

Les résultats d'une analyse sont gardés en mémoire **une heure** tant que le portefeuille et les paramètres ne changent pas : la page reste rapide. Pendant ce temps, les cours ne sont pas redemandés à Yahoo Finance. Le résultat de la lecture automatique d'un fichier importé est gardé de la même façon.

Le bouton [[Actualiser les cours]], en bas de la barre latérale, efface toute cette mémoire et relance la page : les cours sont téléchargés de nouveau (Internet nécessaire).

### 2. Dans des fichiers, pour le hors connexion

| Fichier (dossier `data`) | Contenu |
|---|---|
| `cache_prix.csv` | les derniers cours de la dernière analyse, avec la date et l'heure du téléchargement |
| `cache_historique.csv` | l'historique de la dernière analyse |
| `cache_devises.csv` | la devise de cotation de chaque titre déjà rencontré |
| `cache_import.csv`, `cache_candidats.csv` | les cours utilisés pour vérifier les fichiers importés |
| `cache_stress.csv`, `cache_attribution.csv` | les historiques longs des stress tests et de l'attribution de performance |

Ces fichiers sont réécrits à chaque téléchargement réussi. Si Yahoo Finance ne répond pas, le logiciel relit le cache, le complète par la base locale de titres, et l'indique : « Cours en cache (hors ligne) » dans le bandeau, « cache local du » suivi d'une date dans la barre latérale. Cette date est la plus ancienne des sources utilisées.

### Une particularité : la devise

La devise de chaque titre, une fois connue, est gardée **sans limite de durée** dans `cache_devises.csv`. Si elle a été déduite hors connexion d'après le code du titre, et qu'elle est fausse, elle le reste. Supprimer ce fichier oblige le logiciel à la redemander à Yahoo Finance.

### Vider les caches

[[Actualiser les cours]] vide la mémoire d'une heure. Les fichiers `cache_*.csv` peuvent être supprimés sans risque : ils sont recréés à la prochaine analyse en ligne. Hors connexion, en revanche, ils ne seront plus disponibles.

## La mémoire des titres reconnus
<!-- fiche: sources-memoire-titres | questions: le logiciel se souvient-il des titres que j'ai importés ; c'est quoi memoire.csv ; un isin mal reconnu revient à chaque import ; corriger une mauvaise correspondance isin ticker ; pourquoi le titre est reconnu sans internet ; effacer la mémoire des titres ; le mauvais ticker est proposé à chaque fois | mots: mémoire, memoire.csv, correspondances, ISIN, ticker, apprentissage, reconnaissance, hors connexion -->

### Le principe

Quand un import demande au moteur de recherche de Yahoo Finance de reconnaître un code ISIN, un nom de société ou un ticker, la réponse est **retenue** dans le fichier `data/base/memoire.csv`. À l'import suivant, le même identifiant est reconnu instantanément, même sans Internet.

Chaque ligne contient : l'identifiant (en majuscules), le ticker Yahoo Finance trouvé, le nom du titre, l'origine de la correspondance et la date. Aucune quantité, aucun montant, aucune donnée de portefeuille.

### L'ordre de consultation

Pour un identifiant à reconnaître, le logiciel consulte dans cet ordre :

1. la table intégrée des ISIN d'ETF (elle prime sur la mémoire, pour réparer une mauvaise correspondance apprise auparavant) ;
2. la mémoire ;
3. la base locale de titres ;
4. le moteur de recherche de Yahoo Finance, en dernier recours.

Seules les réponses obtenues par la recherche en ligne sont ajoutées à la mémoire.

### Une mauvaise correspondance

Si un identifiant a été associé au mauvais titre, la mémoire le reproposera à chaque import. Deux remèdes :

- pour un fichier, dans l'assistant d'import ([[Ouvrir l'assistant d'import]]), corrigez la colonne [[Ticker Yahoo Finance]] de l'étape des titres ; cette correction vaut pour le fichier, mais ne modifie pas la mémoire ;
- pour corriger durablement, supprimez la ligne concernée de `data/base/memoire.csv` (ou le fichier entier). Le logiciel ne propose pas d'écran pour cela.

### Partagée entre utilisateurs

La mémoire est commune à tous les utilisateurs du logiciel sur l'ordinateur : un titre reconnu par l'un est reconnu pour tous.

## La table intégrée des ISIN d'ETF
<!-- fiche: sources-isin-etf | questions: quels etf sont reconnus sans internet ; mon etf n'est pas reconnu à l'import ; liste des isin d'etf intégrés ; cw8 isin reconnu hors ligne ; avis d'opéré etf libellé abrégé ; pourquoi mon etf est reconnu avec le mauvais ticker ; table des 31 etf | mots: ETF, ISIN, table intégrée, hors connexion, avis d'opéré, CW8, Amundi, iShares, Vanguard, reconnaissance -->

Les avis d'opéré et relevés ne donnent souvent qu'un code ISIN et un libellé abrégé (« AM.C.C.40 UC.ETF C », par exemple). Pour reconnaître les ETF les plus courants **sans Internet**, le logiciel contient une table de **31 ISIN d'ETF**, chacun associé à un ticker Yahoo Finance.

### Les ETF de la table

| Famille | ETF (ticker) |
|---|---|
| Actions France et zone euro | Amundi CAC 40 Acc (CACC.PA) et Dist (CAC.PA), Amundi Euro Stoxx 50 (MSE.PA), iShares Core DAX (EXS1.DE) |
| Actions monde | Amundi MSCI World (CW8.PA), Amundi PEA MSCI World (EWLD.PA), iShares MSCI World Swap PEA (WPEA.PA), iShares Core MSCI World (IWDA.AS), Vanguard FTSE All-World Acc (VWCE.DE) et Dist (VWRL.AS), iShares MSCI ACWI (IUSQ.DE), SPDR MSCI ACWI IMI (SPYI.DE) |
| Actions États-Unis | BNP Paribas Easy S&P 500 (ESE.PA), Amundi PEA S&P 500 (PE500.PA), Amundi PEA Nasdaq-100 (PUST.PA), Vanguard S&P 500 (VUSA.AS), iShares Core S&P 500 (SXR8.DE), Invesco Nasdaq-100 (EQQQ.DE) |
| Actions Europe et émergents | Amundi Stoxx Europe 600 (MEUD.PA), iShares Core MSCI Europe (EUNK.DE), Amundi PEA MSCI Emerging Markets (PAEEM.PA), Amundi MSCI Emerging Markets (AEEM.PA), iShares Core MSCI EM IMI (IS3N.DE) |
| Obligations | iShares Core Euro Govt Bond (EUNH.DE), iShares Euro Inflation Linked Govt Bond (IBCI.DE), iShares Core Euro Corporate Bond (EUN5.DE), iShares Euro High Yield Corp Bond (EUNW.DE), Xtrackers II Eurozone Government Bond 1C (DBXN.DE) |
| Monétaire et or | Amundi Smart Overnight Return (CSH2.PA), Xtrackers II EUR Overnight Rate Swap (XEON.DE), Xetra-Gold (4GLD.DE) |

### Priorité

Cette table est consultée **en premier**, avant la mémoire des titres et avant toute recherche en ligne. Elle répare ainsi une éventuelle mauvaise correspondance apprise auparavant.

### Un ETF absent de la table

Il est cherché dans la mémoire, la base locale, puis, avec Internet, par le moteur de recherche de Yahoo Finance (par son ISIN, puis par son libellé). La réponse est ensuite mémorisée. Hors connexion et inconnu de la mémoire, il ne peut pas être reconnu : l'import le signale comme introuvable.

### La place de cotation choisie

Un même ETF est souvent coté sur plusieurs places et dans plusieurs devises. La table fixe une cotation précise pour chaque ISIN : si vous avez acheté sur une autre place, le cours retenu peut légèrement différer du vôtre.

## Comment un ISIN, un nom ou un code Bloomberg devient un ticker
<!-- fiche: sources-identifiant-ticker | questions: comment le logiciel trouve le ticker à partir de l'isin ; mon fichier contient des codes bloomberg ; MC FP Equity est-il reconnu ; le logiciel a choisi la mauvaise place de cotation ; ticker sans suffixe MC ou AIR ; reconnaissance du nom de la société ; titre introuvable à l'import ; EPA:MC format google finance | mots: ISIN, ticker, Bloomberg, Google Finance, Reuters, RIC, code MIC, place de cotation, suffixe, recherche Yahoo -->

Le logiciel travaille avec les **tickers de Yahoo Finance** (`MC.PA` pour LVMH à Paris, `AAPL` pour Apple). À l'import, chaque identifiant est d'abord classé, puis traduit.

### 1. Déjà un ticker Yahoo

Un code avec un suffixe de place connu de Yahoo (`.PA`, `.DE`, `.L`, `.AS`…), ou un titre du référentiel, est gardé tel quel.

### 2. Codes Bloomberg, Google Finance, Reuters

Ils sont convertis **par des règles, sans Internet** :

| Écrit dans le fichier | Devient |
|---|---|
| `MC FP` ou `MC FP Equity` (Bloomberg) | `MC.PA` |
| `AAPL US Equity` | `AAPL` |
| `EPA:MC` (Google Finance) | `MC.PA` |
| `NESN.S` (Reuters) | `NESN.SW` |
| `700 HK` | `0700.HK` |

Les codes de place MIC (`XPAR`, `XETR`…) et les noms usuels (« Euronext Paris ») sont aussi reconnus dans une colonne de place.

### 3. Code ISIN ou nom de société

Le logiciel cherche dans la table des ISIN d'ETF, la mémoire, puis la base locale (par ticker, par ISIN, puis par nom). À défaut, il interroge le moteur de recherche de Yahoo Finance avec l'ISIN, puis avec le libellé du fichier. Parmi les réponses (actions, ETF, fonds, indices), il préfère la place du pays de l'ISIN (Paris pour un ISIN `FR`, Francfort pour `DE`…), puis une cotation en euros (Paris, Francfort, Amsterdam, Milan), puis les États-Unis.

### 4. Ticker sans place (`MC`, `AIR`, `TSLA`)

Le code peut désigner plusieurs titres. Le logiciel essaie les cotations possibles (base locale, résultats de recherche et 9 places : États-Unis, Paris, Francfort, Amsterdam, Milan, Madrid, Londres, Zurich, Toronto). Il garde celle dont le cours, à la date de chaque achat ou vente, colle le mieux à vos prix, à condition que l'écart médian reste inférieur à 15 %. Exemple tiré du code : « MC » acheté à 740 € en janvier 2024 correspond à `MC.PA` (LVMH), pas à `MC` (Moelis, une cinquantaine de dollars).

### Si rien ne correspond

Le titre est déclaré introuvable et l'assistant d'import s'ouvre : saisissez vous-même son ticker dans la colonne [[Ticker Yahoo Finance]].

## La conversion des devises en euros
<!-- fiche: sources-devises | questions: comment sont convertis les titres en dollars ; quel taux de change est utilisé ; les actions de londres sont en pence ; taux de change du jour de l'achat ; d'où viennent les taux de change ; mes frais sont ils en euros ; risque de change dans la performance ; taux de change introuvables | mots: devises, taux de change, EURUSD, conversion, pence, GBp, risque de change, euro, USD, Yahoo Finance -->

Tout est exprimé en euros. Un titre coté dans une autre devise est converti avec les taux de change de Yahoo Finance.

### La devise de chaque titre

Le logiciel la demande à Yahoo Finance. Hors connexion, il prend celle de la base locale, puis, à défaut, la déduit du code : pas de suffixe = dollar américain, `.L` = pence, `.SW` = franc suisse, `.T` = yen, et ainsi de suite. La réponse est gardée dans `cache_devises.csv`.

### La formule

```
prix en euros = prix en devise × facteur / taux EURdevise
```

- Le taux `EURUSD=X` est le nombre de dollars pour 1 euro.
- Le facteur vaut 1, sauf pour les actions de Londres, cotées en **pence** : facteur 0,01.

Exemples :

- Apple à 200 USD, avec 1 € = 1,10 USD : 200 / 1,10 = **181,82 €**.
- Une action de Londres à 1 250 pence, avec 1 € = 0,85 GBP : 1 250 × 0,01 / 0,85 = **14,71 €**.

### Quel taux, quel jour ?

- un **achat, une vente ou un dividende** est converti au taux **du jour de l'opération** ;
- la **valeur jour par jour** utilise le taux de chaque jour ;
- la **valeur actuelle** utilise le dernier taux connu.

Un jour sans taux reprend le dernier taux connu. Les **frais** sont toujours considérés en euros et ne sont pas convertis.

### Ce que cela implique

La performance d'un titre étranger combine la variation de son cours et celle de la devise : c'est le risque de change. Une action américaine qui gagne 10 % en dollars ne rapporte rien en euros si le dollar perd environ 10 % face à l'euro sur la même période.

### Les limites

- Le taux est celui de Yahoo Finance, pas celui appliqué par votre banque.
- Hors connexion, seules les devises dont le taux est dans la base locale (12 devises) ou dans le cache peuvent être converties.
- Si un taux manque, l'analyse s'arrête avec le message « Taux de change introuvables ».
- Hors connexion, pour une place peu courante, la devise déduite du code peut être fausse (l'euro est retenu par défaut).

## La composition des ETF : d'où vient l'analyse en transparence ?
<!-- fiche: sources-composition-etf | questions: comment le logiciel connait la composition de mon etf ; la répartition par pays de mon etf est-elle exacte ; d'où viennent les pourcentages du msci world ; analyse en transparence c'est fiable ; date des données de composition des etf ; mon etf est classé non classé ; pourquoi 73 % états-unis dans mon etf monde | mots: transparence, composition, ETF, MSCI World, répartition par pays, secteurs, look-through, approximation, fiches MSCI -->

L'onglet Expositions « éclate » chaque ETF selon la composition de l'indice qu'il suit. Ces compositions **ne sont pas téléchargées** : elles sont inscrites dans le logiciel.

### Les sources et leur date

- **MSCI World, MSCI ACWI, MSCI Emerging Markets, MSCI Europe** : les 5 premiers pays et les secteurs viennent des fiches MSCI au **30/09/2026**. Les pays suivants sont des ordres de grandeur habituels, ramenés au total « autres pays » de la fiche.
- **S&P 500, Nasdaq-100, Euro Stoxx 50, CAC 40, DAX, Russell 2000**, emprunts d'État et obligations d'entreprises : ordres de grandeur 2025-2026, d'après les fiches des émetteurs d'ETF.

Le MSCI World compte ainsi 72,94 % d'États-Unis : un ETF MSCI World de 10 000 € est compté pour environ 7 300 € d'actions américaines. L'écran le rappelle : « approximation au 30/09/2026 ».

### Comment l'ETF est rattaché à un indice

1. par une table de 58 tickers d'ETF (CW8.PA et IWDA.AS pour le MSCI World, ESE.PA pour le S&P 500…) ;
2. sinon, par des mots du nom : « All-World » ou « ACWI », « Emerging », « World », « S&P 500 », « Stoxx Europe 600 »… ;
3. un nom contenant « Hedged » ou « couvert » est considéré comme couvert contre le risque de change.

Un fonds qui ne correspond à rien reste « Non classé ».

### Les approximations à connaître

- Les poids réels changent chaque jour ; le projet estime l'écart à quelques points au plus, les poids des grands indices bougeant peu d'une année à l'autre.
- Le même mélange de secteurs est appliqué à chaque pays d'un indice : c'est une hypothèse de calcul.
- Un ETF est supposé suivre exactement son indice.
- Les données datées doivent être revues une fois par an dans le code du projet.

### Autres données de référence fixes

L'attribution de performance utilise les poids régionaux du MSCI ACWI IMI au 30/06/2026, également inscrits dans le logiciel.

## Comment chaque titre est classé (pays, secteur, classe d'actifs)
<!-- fiche: sources-classification | questions: d'où viennent le pays et le secteur de mes titres ; mon action est non classé ; c'est quoi referentiel.csv ; mon titre est classé dans le mauvais pays ; pourquoi mon obligation est comptée comme action ; où est la duration des fonds obligataires ; ajouter un titre au référentiel ; classe d'actifs par défaut | mots: classification, référentiel, referentiel.csv, pays, région, secteur, classe d'actifs, duration, Non classé, GICS -->

### Deux sources, dans cet ordre

1. **Le référentiel du projet**, `data/referentiel.csv` : 86 titres décrits à la main, avec les colonnes ticker, nom, pays, région, secteur, classe (Actions, Obligations, Or, Monétaire) et duration pour les fonds obligataires. Il **l'emporte toujours**.
2. **La base locale de titres** (`data/base/titres.csv`), pour tous les autres titres.

### Comment la base locale classe un titre

- **Pays et région** : d'après la **place de cotation** du ticker (`.PA` = France, `.DE` = Allemagne, pas de suffixe = États-Unis…), et non d'après le siège de la société. Une société étrangère cotée à Paris est donc classée « France ».
- **Secteur** : le secteur indiqué par la page Wikipédia de l'indice (secteurs GICS traduits), quand il existe.
- **Classe d'actifs** : « Actions » pour les actions ; pour les ETF de la liste, « Obligations » ou « Or » selon leur nom.

### Les valeurs par défaut

- Un titre sans pays, région ou secteur connu est classé **« Non classé »**.
- Un titre sans classe d'actifs connue est considéré comme une **action** : c'est l'hypothèse prudente pour mesurer le risque.
- La **duration** n'est connue que pour les fonds obligataires du référentiel ; ailleurs, elle est absente.

### Corriger un classement

Le logiciel ne propose pas d'écran pour modifier le classement d'un titre. Depuis le code source, vous pouvez ajouter ou corriger une ligne de `data/referentiel.csv`, en respectant ses colonnes : elle primera sur la base locale. Dans la version installée, ce fichier se trouve dans le dossier `data` du programme et serait remplacé par une nouvelle installation.

## Les indices de référence et les indices composites
<!-- fiche: sources-indices | questions: quels indices de référence sont proposés ; comment est calculé l'indice mixte 60 40 ; l'indice de référence inclut il les dividendes ; pourquoi comparer à un etf plutôt qu'à l'indice ; indice composite rééquilibré chaque mois ; changer d'indice de référence ; le cac 40 est hors dividendes ; d'où vient l'historique de l'indice | mots: benchmark, indice de référence, composite, mixte, 60/40, rééquilibrage mensuel, MSCI World, CAC 40, €STR, dividendes réinvestis -->

L'indice de référence se choisit dans [[Paramètres]], en bas de la barre latérale, rubrique [[Indice de référence]]. Par défaut : le MSCI World, représenté par l'ETF CW8.

### Les quatre familles

| Famille | Indices | Représentés par |
|---|---|---|
| Actions | MSCI World, MSCI ACWI, S&P 500, Nasdaq-100, Stoxx Europe 600, MSCI Marchés émergents | des ETF capitalisants : dividendes réinvestis |
| Actions | Euro Stoxx 50, CAC 40 | l'indice de prix : **hors dividendes** |
| Obligations | Emprunts d'État zone euro ; obligations d'entreprises en euros | un ETF capitalisant (coupons réinvestis) ; un ETF « hors coupons » |
| Monétaire | €STR | un ETF capitalisant (intérêts réinvestis) |
| Mixtes | prudent 20/80, équilibré 60/40, dynamique 80/20 | calculés par le logiciel |

Le libellé de chaque indice précise s'il inclut les dividendes. Comparer à un indice hors dividendes avantage le portefeuille : le projet l'estime à environ 3 % par an pour le CAC 40.

### Pourquoi un ETF ?

Un ETF capitalisant intègre les dividendes dans son cours, comme votre performance intègre vos dividendes : la comparaison est équitable. Chaque indice a plusieurs ETF « candidats » ; le premier dont l'historique est disponible est utilisé (par exemple CW8.PA, sinon IWDA.AS).

### Les indices mixtes

```
Composite = X % poche actions + Y % poche obligations, rééquilibré à chaque fin de mois
```

- Poche actions : MSCI World (CW8.PA, sinon IWDA.AS, sinon EUNL.DE).
- Poche obligations : emprunts d'État zone euro (DBXN.DE, sinon EUNH.DE).
- Cours convertis en euros, série en base 100.
- Au dernier jour de bourse de chaque mois, les poids sont remis à leur cible.

Exemple pour le 60/40 : sur un mois où les actions gagnent 10 % et les obligations perdent 2 %, l'indice gagne 0,60 × 10 % + 0,40 × (−2 %) = **5,2 %**. Les poids repartent ensuite de 60/40.

### Les limites

Un ETF suit son indice avec un petit écart (frais, réplication). Le composite ne compte ni frais ni coût de rééquilibrage.

## Le taux sans risque
<!-- fiche: sources-taux-sans-risque | questions: quel taux sans risque est utilisé ; d'où vient le taux de 2,5 % ; comment changer le taux sans risque ; taux de la bce pour le ratio de sharpe ; le taux sans risque est-il historique ; pourquoi le sharpe change quand je modifie le taux ; €str ou taux de dépôt | mots: taux sans risque, BCE, facilité de dépôt, €STR, ratio de Sharpe, Sortino, alpha, paramètres, 2,50 % -->

### La valeur par défaut

**2,50 % par an**, soit le taux de la facilité de dépôt de la Banque centrale européenne. Le code du projet le donne en vigueur depuis le 16/09/2026 (source indiquée : BCE, « Key ECB interest rates »). Le €STR, taux interbancaire au jour le jour, en est très proche.

Ce taux sert au **ratio de Sharpe**, au **ratio de Sortino** et à l'**alpha**.

### Il n'est pas téléchargé

Le logiciel ne va pas chercher ce taux sur Internet : c'est une **valeur fixe**, inscrite dans le code. Quand la BCE change ses taux, elle n'est mise à jour qu'avec une nouvelle version du logiciel, ou par vous-même.

### Le modifier

Dans la barre latérale, ouvrez [[Paramètres]] et changez [[Taux sans risque (% par an)]] : de 0 à 10 %, par pas de 0,25 point. L'info-bulle rappelle la valeur de la BCE. Tous les indicateurs concernés sont recalculés.

### La simplification à connaître

Le taux est **constant sur toute la période analysée**, alors qu'il a varié dans le passé (le code cite 4 % début 2024 et 2 % mi-2025). Sur une longue période, le Sharpe et l'alpha sont donc approximatifs. Le projet signale, comme amélioration possible, l'utilisation de la série historique du €STR.

### Pour comparer

Choisir l'indice de référence « Monétaire €STR » montre ce qu'aurait rapporté un placement monétaire sur la même période, d'après le cours d'un ETF monétaire.

## Le fond de carte du monde
<!-- fiche: sources-fond-de-carte | questions: la carte du monde ne s'affiche pas ; d'où viennent les contours des pays ; carte vide sans internet ; pays.geojson c'est quoi ; natural earth ; la guyane apparait en couleur sur la carte ; pourquoi l'antarctique n'est pas sur la carte | mots: carte du monde, fond de carte, Natural Earth, GeoJSON, pays.geojson, contours des pays, hors connexion, Plotly -->

La carte du monde de l'onglet Expositions colore chaque pays selon son poids dans la poche actions.

### La source

Les contours des pays viennent de **Natural Earth**, une base cartographique du domaine public, à l'échelle 1:110 000 000. Le fichier est téléchargé depuis GitHub, ou à défaut depuis le service jsDelivr, puis simplifié :

- coordonnées arrondies à environ 1 km, pour un fichier d'environ 400 Ko ;
- Antarctique retiré (aucune bourse) ;
- pour la France, seule la métropole est gardée : sinon, la Guyane, dessinée avec la France, se colorerait avec une action française.

Il est enregistré dans `data/base/pays.geojson`.

### Quand il est téléchargé

Une seule fois : à la construction de la base, à la fabrication de l'installateur, ou, à défaut, par le tableau de bord la première fois qu'il en a besoin (un seul essai à chaque lancement du logiciel). Ensuite, la carte s'affiche sans Internet.

### Si le fichier manque

La carte est alors dessinée avec le fond de carte que la bibliothèque de graphiques télécharge elle-même : sans Internet, elle reste vide. Le reste de l'onglet n'est pas concerné.

### Ce que la carte ne montre pas

Une note sous la carte indique la part du portefeuille « hors carte », par classe d'actifs : obligations, or, monétaire, ou actions sans pays connu. Les ETF y sont répartis selon la composition approximative de leur indice.

## Ce que le logiciel vérifie
<!-- fiche: sources-controles | questions: quels contrôles fait le logiciel ; le logiciel vérifie-t-il mes prix d'achat ; comment sont détectés les doublons ; prix éloigné du cours du jour ça veut dire quoi ; vente impossible on n'en détient que ; vérification des données importées ; le logiciel détecte-t-il les erreurs de saisie ; contrôle qualité des données | mots: contrôles, vérifications, contrôle qualité, doublons, prix éloigné, 25 %, cohérence, ISIN, clé de contrôle, validation -->

Voici, un par un, les contrôles réellement présents.

### À la lecture du fichier

- Seuls les types ACHAT, VENTE et DIVIDENDE sont acceptés ; les prix et quantités négatifs sont refusés.
- **Vente impossible** : vendre plus de titres que ceux détenus à cette date arrête l'analyse, avec un message qui donne la date et les quantités.
- Les colonnes d'un fichier inconnu ne sont acceptées automatiquement que si leurs noms sont parlants, ou si les chiffres sont cohérents (quantité × prix, plus ou moins les frais, égale le montant à 1 % près sur au moins 80 % des lignes). Sinon, l'assistant d'import s'ouvre.
- Un **code ISIN** n'est reconnu que si sa clé de contrôle est juste ; dans un PDF, il doit en plus compter au moins 6 chiffres.
- Les dates ambiguës (jour/mois ou mois/jour) sont détectées et le choix retenu est signalé.

### Les prix comparés au marché

À l'import, avec Internet, chaque prix d'achat ou de vente est comparé au cours de clôture du titre ce jour-là :

- le logiciel reconnaît un prix saisi en euros, en devise ou en pence, et le ramène à l'unité de cotation ;
- un prix plus de 25 % au-dessus (ou 20 % en dessous) du cours du jour est signalé : « prix éloigné(s) du cours du jour », avec l'écart médian, « ticker, devise ou division d'actions à vérifier ».

Sans Internet, le résumé indique « Prix non vérifiés avec les cours du marché (pas de connexion). ».

### À l'ajout d'opérations

- **Doublons** : une opération de même date, même titre, même type, même quantité et même prix à 0,5 % près est décochée d'office.
- Opération datée dans le futur, quantité ou prix nul, vente supérieure à la quantité détenue : alertes bloquantes.

### Pendant l'analyse

- Un cours manquant, un historique manquant ou un taux de change introuvable arrêtent l'analyse avec un message qui nomme les titres concernés, plutôt qu'un résultat faux.
- La source des cours (direct ou cache) et la date des données sont toujours affichées.

### Dans les tests du projet

Les tests automatiques vérifient notamment que le gain calculé jour par jour retombe exactement sur le gain total. Ces tests sont lancés par le développeur, pas pendant votre utilisation.

## Ce que le logiciel ne vérifie pas
<!-- fiche: sources-limites | questions: quelles sont les limites des données ; le logiciel compare-t-il plusieurs sources de cours ; un cours faux de yahoo est-il détecté ; le logiciel détecte-t-il un titre radié ; les données sont-elles garanties ; peut-on se fier aux chiffres pour déclarer ses impôts ; limites du logiciel sur les données | mots: limites, fiabilité, une seule source, erreurs de données, cours aberrant, titre radié, opérations sur titres, garantie, avertissement -->

Pour être honnête sur la fiabilité, voici ce qui **n'est pas** contrôlé.

### Les cours

- **Une seule source** : tous les cours viennent de Yahoo Finance. Le logiciel ne les compare à aucune autre source (Euronext, Bloomberg, votre courtier).
- **Pas de détection des cours aberrants** dans l'historique : un saut anormal d'un jour, une valeur manquante ou un cours figé ne sont pas repérés. Un jour sans cours reprend simplement le dernier cours connu.
- **Pas de contrôle de fraîcheur par titre** : un titre suspendu ou radié garde son dernier cours connu, sans alerte.
- **Pas d'ajustement des opérations sur titres** : divisions, regroupements, scissions, fusions et changements de code ne sont pas traités.
- **Pas de téléchargement des dividendes** : seuls ceux de votre fichier comptent.
- Le contrôle des prix à 25 % n'a lieu qu'**à l'import**, avec Internet, et seulement sur les achats et ventes.

### Les autres données

- La devise de cotation, une fois connue, n'est plus revérifiée.
- La reconnaissance d'un ISIN par le moteur de recherche peut choisir une autre place de cotation que la vôtre.
- La composition des ETF, le classement des titres et le taux sans risque sont des valeurs fixes, datées, et non mises à jour en continu.
- Le pays d'une action de la base locale est celui de sa place de cotation.

### Vos propres données

Le logiciel ne peut pas savoir si vous avez oublié une opération, un dividende ou des frais. Il calcule juste à partir de ce que vous lui donnez.

### En conséquence

Les résultats sont fiables pour l'analyse et l'apprentissage, mais ne remplacent pas les relevés officiels de votre établissement financier, notamment pour une déclaration fiscale. Ils ne constituent pas un conseil en investissement.

## Un cours me semble faux : que faire ?
<!-- fiche: sources-cours-faux | questions: le cours affiché est faux ; ma valeur actuelle est bizarre ; perte énorme sur un titre alors que le cours a monté ; le prix de mon action n'est pas le bon ; le cours est en pence au lieu de livres ; comment corriger un cours ; mon etf a un prix différent de mon courtier ; valeur de mon portefeuille incohérente | mots: cours faux, erreur de cours, prix incorrect, dépannage, ticker, place de cotation, devise, pence, split, correction -->

Le logiciel ne permet pas de saisir un cours à la main : il faut trouver la cause. Procédez dans cet ordre.

### 1. Vérifiez la source et la date

Le bandeau indique-t-il « Cours en cache (hors ligne) » ? Si oui, les cours datent du jour indiqué dans la barre latérale. Reconnectez-vous à Internet et cliquez sur [[Actualiser les cours]].

### 2. Vérifiez le ticker et la place

Dans l'onglet Positions ou Transactions, regardez le ticker retenu. `MC` (Moelis, à New York) n'est pas `MC.PA` (LVMH, à Paris) ; un ETF coté à Londres en dollars n'a pas le même cours que son équivalent coté à Paris en euros. Si le ticker est faux, corrigez votre fichier, ou réimportez-le avec [[Ouvrir l'assistant d'import]] et corrigez la colonne [[Ticker Yahoo Finance]].

### 3. Vérifiez la devise

Les actions de Londres sont cotées en pence (1 250 pence = 12,50 livres). Le prix de votre fichier doit être dans la devise de cotation du titre, les frais en euros. Le résumé de l'import indique les conversions faites.

### 4. Pensez à une division d'actions

Une perte d'environ 50 %, 67 % ou 90 % apparue d'un coup évoque une division d'actions. Corrigez l'opération comme expliqué dans la fiche « Dividendes et divisions d'actions ».

### 5. Comparez avec une autre source

Comparez le cours au site de votre courtier, à celui de la bourse concernée, ou à la page du titre sur Yahoo Finance. Si Yahoo Finance lui-même affiche une valeur fausse, le logiciel la reprend : attendez sa correction, puis cliquez sur [[Actualiser les cours]]. Les nouvelles valeurs remplacent alors les anciennes dans la base locale.

### 6. Vérifiez vos opérations

Une quantité ou un prix mal saisis faussent la valeur autant qu'un mauvais cours. Utilisez [[Modifier les opérations]] dans l'onglet Transactions pour corriger.

## Comment vous assurez-vous que les cours sont bons ?
<!-- fiche: sources-fiabilite | questions: comment vous assurez vous que les cours sont bons ; les données sont-elles fiables ; peut on faire confiance aux cours de yahoo finance ; la source est elle sûre ; est-ce que les chiffres sont justes ; quel crédit accorder aux résultats ; yahoo finance est-il fiable pour un mémoire ; que répondre au jury sur la fiabilité des données | mots: fiabilité, confiance, qualité des données, Yahoo Finance, vérification, exactitude, source gratuite, soutenance -->

### La réponse honnête

Le logiciel **ne garantit pas** l'exactitude des cours : il les reprend de Yahoo Finance, une source gratuite et largement utilisée, mais sans engagement de qualité, et **sans les comparer à une seconde source**. Il ne cherche pas non plus de valeurs aberrantes dans l'historique.

### Ce qu'il fait pour limiter les erreurs

1. **Un cours brut et traçable** : le cours de clôture non ajusté des dividendes, que chacun peut comparer à celui affiché par la bourse ou par un courtier.
2. **Une source toujours affichée** : direct ou cache, avec la date des données.
3. **Le contrôle de vos prix à l'import** : chaque prix d'achat et de vente est comparé au cours de clôture de Yahoo Finance du même jour. Un écart de plus de 25 % est signalé. Ce contrôle croisé révèle aussi bien une erreur de votre fichier qu'un mauvais titre ou un cours anormal.
4. **La reconnaissance des titres par les prix** : un ticker sans place n'est retenu que si son cours colle à vos prix (écart médian inférieur à 15 %).
5. **Des arrêts plutôt que des approximations** : cours, historique ou taux de change manquant arrêtent l'analyse avec un message clair.
6. **Une base qui se corrige** : chaque téléchargement remplace les anciennes valeurs par celles de Yahoo Finance.
7. **Des calculs testés** : les formules sont vérifiées par des tests automatiques, sur des exemples dont le résultat est connu.

### Ce que vous pouvez dire

Pour un travail universitaire, une formulation juste est : « Les cours sont les cours de clôture quotidiens de Yahoo Finance, non ajustés des dividendes ; les prix de transaction ont été contrôlés par rapport à ces cours, avec un seuil d'alerte de 25 % ; les cours n'ont pas été recoupés avec une seconde source. »

### Pour aller plus loin

Pour un chiffre important, vérifiez-le vous-même sur une seconde source : site de la bourse, courtier ou relevé de votre établissement.

## Hors connexion : jusqu'à quelle date vont les cours ?
<!-- fiche: sources-hors-connexion-date | questions: jusqu'à quelle date les cours sont disponibles sans internet ; les cours s'arrêtent à une date ancienne ; données au quelle date ; cache local du ça veut dire quoi ; comment avoir des cours plus récents hors ligne ; la base livrée date de quand ; mes cours ne vont pas jusqu'à aujourd'hui | mots: hors connexion, offline, date des cours, cache local, base locale, mise à jour, données au, dernière date -->

### Il n'y a pas de date fixe

Hors connexion, les cours s'arrêtent à la **dernière date connue** sur votre ordinateur. Elle dépend :

- de la base livrée avec votre version, mise à jour par le créateur au moment de la fabriquer ;
- de vos propres analyses en ligne : chaque historique téléchargé est ajouté à la base ;
- du cache de la dernière analyse.

### Où lire cette date

- **« Données au »**, dans le bandeau en haut de page : la date du dernier cours de l'historique utilisé ;
- la ligne **« Cours »** en bas de la barre latérale : « cache local du » suivi d'une date, la plus ancienne des sources utilisées pour les cours actuels ;
- la pastille **« Cours en cache (hors ligne) »**, avec un point orange.

Les calculs restent justes, mais arrêtés à cette date : la valeur actuelle est la valeur à la date du dernier cours connu.

### Obtenir des cours plus récents

- Reconnectez-vous à Internet, puis cliquez sur [[Actualiser les cours]] : les cours manquants sont téléchargés et ajoutés à la base.
- Depuis le code source, `python construire_base_titres.py --mise-a-jour` met à jour toute la base en quelques minutes.
- Installer la dernière version du logiciel apporte une base plus récente.

### Un titre sans aucun cours

Un titre absent de la base, du cache et de la mémoire n'a pas de cours hors connexion : l'analyse s'arrête avec un message qui le nomme. Il sera disponible dès la première analyse avec Internet.

### Tous les titres ne s'arrêtent pas au même jour

Les cours de tous les titres d'un portefeuille ne s'arrêtent pas forcément au même jour. Le logiciel prend, pour chaque titre, son dernier cours connu.
