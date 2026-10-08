# Questions fréquentes
<!-- chapitre: faq | ordre: 13 -->

Ce chapitre répond brièvement aux questions les plus souvent posées sur Portfolio Tracker, y compris celles d'un jury ou d'un professeur lors d'une soutenance : fiabilité, sources, confidentialité, choix méthodologiques et limites. Chaque réponse renvoie, si besoin, au chapitre qui détaille le sujet.

## Le logiciel est-il fiable ?
<!-- fiche: faq-fiabilite | questions: le logiciel est il fiable ; peut on faire confiance aux résultats ; les calculs sont ils justes ; est-ce que les chiffres sont exacts ; quelle confiance accorder à portfolio tracker ; le logiciel peut il se tromper ; fiabilité des indicateurs | mots: fiabilité, confiance, exactitude, calculs, contrôles, tests, limites, outil pédagogique -->

Oui pour ses **calculs**, avec des réserves sur ses **données**.

### Ce qui est solide

- **Les formules** sont celles de la littérature financière (TWR, TRI, Sharpe, VaR, Markowitz, Brinson-Fachler…) et sont décrites exactement au chapitre « Toutes les formules ».
- **Les calculs sont testés** automatiquement sur des exemples dont le résultat est connu (voir la fiche « Comment savez-vous que les formules sont justes ? »).
- **Les contrôles** arrêtent l'analyse plutôt que d'afficher un chiffre faux : vente de titres non détenus, cours ou taux de change manquant, type d'opération inconnu.
- **La source** des cours et la date des données sont toujours affichées.

### Les réserves

- Les cours viennent d'**une seule source**, Yahoo Finance, sans recoupement.
- Le résultat dépend de **vos opérations** : un dividende oublié ou une division d'actions non saisie faussent l'analyse.
- Certaines données sont **fixes et datées** (composition des ETF, taux sans risque, classement des titres).

### En résumé

C'est un outil pédagogique fiable pour analyser et comprendre un portefeuille. Il ne remplace ni les relevés officiels de votre établissement ni un conseil en investissement.

## Comment vérifiez-vous que les cours sont justes ?
<!-- fiche: faq-verification-cours | questions: comment vérifiez vous que les cours sont justes ; les cours sont ils contrôlés ; que se passe-t-il si yahoo donne un cours faux ; recoupez vous les cours avec une autre source ; contrôle des prix à l'import ; que répondre au jury sur la qualité des données | mots: vérification, contrôle des cours, qualité des données, Yahoo Finance, écart de 25 %, recoupement, cours de clôture -->

### Ce que fait le logiciel

1. Il utilise le **cours de clôture brut** (non ajusté des dividendes) : chacun peut le comparer à celui de la bourse ou de son courtier.
2. **À l'import**, avec Internet, chaque prix d'achat et de vente de votre fichier est comparé au cours de clôture de Yahoo Finance du même jour. Un écart de plus de 25 % est signalé. Ce contrôle croisé révèle aussi bien une erreur de saisie qu'un mauvais titre ou un cours anormal.
3. Un ticker sans place de cotation n'est retenu que si son cours colle à vos prix (écart médian inférieur à 15 %).
4. Un cours, un historique ou un taux de change manquant **arrête** l'analyse, avec un message qui nomme le titre.

### Ce qu'il ne fait pas

Il ne compare pas les cours à une seconde source et ne cherche pas de valeurs aberrantes dans l'historique. Un titre suspendu garde son dernier cours connu.

### Ce que vous pouvez dire

« Les cours sont les cours de clôture quotidiens de Yahoo Finance, non ajustés des dividendes ; les prix de transaction ont été contrôlés par rapport à ces cours, avec un seuil d'alerte de 25 % ; les cours n'ont pas été recoupés avec une seconde source. » Pour un chiffre important, vérifiez-le sur le site de la bourse ou de votre courtier.

## Pourquoi Yahoo Finance et pas Bloomberg ?
<!-- fiche: faq-pourquoi-yahoo | questions: pourquoi yahoo finance ; pourquoi pas bloomberg ou refinitiv ; yahoo finance est-il une source sérieuse ; peut on changer de source de données ; pourquoi une source gratuite ; d'où viennent les données de yahoo | mots: Yahoo Finance, Bloomberg, Refinitiv, source de données, gratuit, yfinance, abonnement, fournisseur -->

### Les raisons du choix

- **Gratuit et sans abonnement** : le logiciel est un outil pédagogique, utilisable par tout étudiant ; un terminal Bloomberg ou un accès Refinitiv sont payants et réservés à leurs abonnés.
- **Sans compte ni clé d'accès** : le logiciel interroge Yahoo Finance par la bibliothèque Python `yfinance`, sans identifiant.
- **Large couverture** : actions et ETF des grandes places mondiales, indices et taux de change, avec un historique quotidien de plusieurs années.
- **Reconnaissance des titres** : son moteur de recherche permet de retrouver un ticker à partir d'un ISIN ou d'un nom.

### Les contreparties

Yahoo Finance ne garantit pas la qualité de ses données et peut être momentanément indisponible. C'est pourquoi le logiciel garde un cache et une base locale, et affiche toujours la source utilisée.

### Changer de source

Le logiciel ne propose pas de réglage pour cela. Dans le code, tout l'accès aux cours est isolé dans un seul fichier (`src/market_data.py`) : changer de fournisseur ne demanderait de modifier que ce fichier.

## Mes données sont-elles confidentielles ?
<!-- fiche: faq-confidentialite | questions: mes données sont elles confidentielles ; mon portefeuille est il envoyé sur internet ; qui peut voir mes données ; est-ce sécurisé ; mes montants partent-ils chez yahoo ; rgpd et confidentialité ; le logiciel est il sûr | mots: confidentialité, vie privée, sécurité, chiffrement, localhost, RGPD, données personnelles -->

Avec la version installée, oui.

### Tout reste sur votre ordinateur

- Le tableau de bord tourne à l'adresse `localhost` : il n'accepte aucune connexion d'un autre appareil.
- Vos fichiers sont lus et calculés sur votre ordinateur.
- Les portefeuilles enregistrés dans votre espace sont **chiffrés** avec une clé tirée de votre mot de passe (PBKDF2 et Fernet) : ni les autres utilisateurs, ni un administrateur ne peuvent les lire.

### Ce qui part sur Internet

Seulement les **codes des titres** (tickers) pour obtenir les cours, et, pour reconnaître un titre inconnu à l'import, son ISIN ou son nom. Les quantités, les montants et la composition du portefeuille ne sont jamais envoyés.

### Les exceptions

- **La version en ligne** tourne sur un serveur distant : vos fichiers y sont traités. Préférez la version installée pour des données réelles.
- Quelques fichiers locaux communs ne sont pas chiffrés (cache des cours, mémoire des titres, journal des questions sans réponse) : ils ne contiennent ni quantité ni montant, mais révèlent quels titres ont été analysés.

Le détail figure au chapitre « Votre compte et la sécurité de vos données ».

## Le créateur du logiciel peut-il voir mon portefeuille ?
<!-- fiche: faq-createur | questions: le créateur peut il voir mon portefeuille ; le développeur a-t-il accès à mes données ; mon professeur peut il voir mes positions ; y a-t-il une télémétrie ; le logiciel envoie-t-il des statistiques ; quelqu'un d'autre peut il lire mes portefeuilles | mots: créateur, développeur, professeur, télémétrie, statistiques d'utilisation, accès aux données, chiffrement -->

**Non.** Avec la version installée, le créateur ne reçoit rien :

- il n'existe **aucun serveur** du logiciel : votre compte n'existe que sur votre ordinateur ;
- la collecte de statistiques d'utilisation de Streamlit est **désactivée**, dans la configuration du projet et au lancement ;
- les questions posées à l'assistant restent dans un fichier local ;
- le logiciel ne vérifie même pas l'existence de mises à jour.

### Même avec votre ordinateur entre les mains

Vos portefeuilles enregistrés sont chiffrés avec votre mot de passe. Sans lui, personne, créateur compris, ne peut les lire ni réinitialiser ce mot de passe.

### Votre professeur

Il ne voit vos portefeuilles que si vous lui transmettez vous-même un fichier (export CSV, rapport PDF) ou si vous lui montrez votre écran.

### Sur la version en ligne

Le logiciel y tourne sur un serveur administré par la personne qui a publié le site : les fichiers que vous y envoyez sont traités sur ce serveur.

## Le logiciel fonctionne-t-il sans Internet ?
<!-- fiche: faq-hors-connexion | questions: le logiciel marche-t-il sans internet ; puis je l'utiliser hors connexion ; pas de wifi pendant la soutenance ; mode avion ; que se passe-t-il sans connexion ; les cours sans internet datent de quand | mots: hors connexion, offline, sans Internet, base locale, cache, soutenance, mode avion -->

**Oui, en grande partie.** Le logiciel est livré avec une base locale de plusieurs milliers de titres, d'indices et de taux de change, avec leurs cours quotidiens (depuis 2015 pour les titres, 2007 pour les indices et les devises).

### Ce qui marche hors connexion

Ouvrir le logiciel, se connecter, analyser un portefeuille dont les titres sont dans la base ou le cache, importer un fichier CSV ou Excel, toutes les analyses, le rapport PDF, l'assistant et le manuel.

### Ce qui demande Internet

Les cours du jour, un titre jamais rencontré, la reconnaissance d'un ISIN inconnu, le bouton [[Actualiser les cours]], et la carte du monde si son fond n'a jamais été enregistré.

### Comment le savoir

Le bandeau affiche « Cours en cache (hors ligne) » avec un point orange, et la barre latérale la date des derniers cours connus. Les calculs restent justes, mais arrêtés à cette date.

### Conseil pour une soutenance

La veille, analysez votre portefeuille avec Internet : ses cours seront ajoutés à la base et au cache, et le jour J, le logiciel fonctionnera même sans réseau.

## Quelles sont les limites de la loi normale dans le logiciel ?
<!-- fiche: faq-loi-normale | questions: limites de la loi normale ; pourquoi utiliser la loi normale alors que les rendements ne sont pas normaux ; la var normale sous-estime le risque ; queues épaisses ; comment le logiciel corrige la loi normale ; hypothèse de normalité critique | mots: loi normale, normalité, queues épaisses, Jarque-Bera, Cornish-Fisher, bootstrap, VaR historique, krach | aller: Analyse du portefeuille/Risque -->

### Où le logiciel utilise la loi normale

- la **VaR loi normale** (paramétrique) ;
- la projection Monte-Carlo, méthode **« Loi normale »** (mouvement brownien géométrique) ;
- la courbe de comparaison de l'histogramme des rendements.

### Sa limite principale

Les rendements réels ont des **queues épaisses** et souvent une **asymétrie négative** : les krachs sont plus fréquents que ne le prévoit la loi normale. Elle sous-estime donc les pertes extrêmes, surtout à 99 %.

### Ce que le logiciel propose pour la dépasser

1. **Il mesure l'écart** : asymétrie, kurtosis en excès, part des jours à plus de 3 écarts-types (contre 0,27 % attendus) et test de Jarque-Bera, dans l'onglet Risque.
2. **Il compare plusieurs VaR** : historique (sans hypothèse de loi), loi normale, Cornish-Fisher (corrigée de l'asymétrie et de la kurtosis), et la CVaR.
3. **Il propose une projection « Historique (bootstrap) »**, qui tire de vrais jours du portefeuille et conserve ses krachs réels.
4. **Il complète par des stress tests** qui rejouent de vraies crises.

### À retenir

La loi normale reste un repère simple et standard ; le logiciel la présente toujours à côté de mesures qui ne la supposent pas.

## TWR ou TRI : lequel regarder ?
<!-- fiche: faq-twr-tri | questions: différence entre twr et tri ; lequel regarder twr ou tri ; pourquoi mon tri est différent de mon twr ; quelle performance donner à mon client ; twr ou mwr ; ma performance réelle c'est laquelle | mots: TWR, TRI, performance, time-weighted return, money-weighted return, apports, calendrier, comparaison | aller: Analyse du portefeuille/Performance | chiffres: twr_annualise, tri_annuel -->

Les deux sont justes : ils répondent à deux questions différentes.

| | TWR | TRI |
|---|---|---|
| Question | Les choix de titres ont-ils été bons ? | Combien mon argent a-t-il rapporté ? |
| Effet des apports | neutralisé | pris en compte |
| Comparable à un indice | oui | non |
| Utilisé par | les gérants de fonds (norme GIPS) | l'investisseur, pour son propre argent |

### Exemple

10 000 € gagnent 20 % la première année ; vous ajoutez alors 50 000 €, puis le portefeuille perd 10 %. Le TWR est de +8 % sur deux ans (+3,9 % par an) : les choix de titres ont été bons en moyenne. Le TRI est de −6,05 % par an : la baisse a touché une somme bien plus grosse que la hausse, et vous avez perdu de l'argent.

### Lequel regarder

- Pour **juger une gestion** ou la comparer à un indice : le TWR.
- Pour savoir **ce que votre argent a réellement rapporté** : le TRI.
- Un TRI supérieur au TWR signifie que vos apports sont bien tombés.

Les formules exactes sont au chapitre « Toutes les formules ».

## Que vaut vraiment l'optimisation de Markowitz ?
<!-- fiche: faq-markowitz | questions: que vaut l'optimisation de markowitz ; faut il suivre le portefeuille optimal ; limites de markowitz ; pourquoi l'optimiseur concentre sur quelques titres ; le portefeuille de sharpe maximal est il fiable ; critique de markowitz par un jury ; pourquoi un poids maximal de 30 % | mots: Markowitz, optimisation, frontière efficiente, erreur d'estimation, rendements espérés, poids maximal, concentration, parité des risques | aller: Analyse du portefeuille/Optimisation -->

C'est un **excellent outil pédagogique** et un mauvais pilote automatique.

### Ce qu'il montre bien

- l'intérêt de la diversification : combiner des titres peu corrélés réduit le risque ;
- la frontière efficiente : aucun portefeuille tiré au hasard ne fait mieux, à risque égal ;
- l'écart entre votre répartition et une répartition plus efficace, avec les montants à acheter ou vendre.

### Ses limites, connues et assumées

- **Les rendements espérés sont des moyennes passées** : l'optimiseur surexploite les titres qui ont le mieux marché, sans garantie pour l'avenir. Une petite erreur sur ces rendements change fortement les poids.
- **La concentration** : sans limite, il met souvent presque tout sur 2 ou 3 titres. D'où le [[Poids maximal par titre]], 30 % par défaut.
- **Ni frais, ni fiscalité** : les ajustements sont calculés hors frais et sans l'impôt d'une vente.
- **Une seule période** : volatilités et corrélations sont supposées stables.

### Ce que le logiciel propose à côté

La **parité des risques** et la **variance minimale**, dans l'onglet [[Budget de risque]], n'utilisent pas les rendements espérés, la source d'erreur principale.

L'écran le rappelle : « Exercice académique, pas un conseil en investissement. »

## Est-ce un conseil en investissement ?
<!-- fiche: faq-conseil | questions: est-ce un conseil en investissement ; puis je suivre les recommandations du logiciel ; le logiciel me dit d'acheter ; les pistes du diagnostic sont-elles des conseils ; responsabilité en cas de perte ; outil réglementé ; le logiciel remplace-t-il un conseiller | mots: conseil en investissement, recommandation, responsabilité, outil pédagogique, diagnostic, pistes, avertissement, réglementation -->

**Non.** Le pied de page de chaque écran le rappelle : « Outil pédagogique réalisé dans le cadre du Master G2C — ne constitue pas un conseil en investissement. »

### Pourquoi

- Le logiciel ne connaît ni votre situation, ni vos objectifs, ni votre horizon, ni votre tolérance au risque.
- Ses calculs reposent sur le passé, qui ne préjuge pas de l'avenir.
- Les **pistes** du diagnostic (onglet Expositions) découlent de règles simples aux seuils documentés ; l'écran précise : « Analyse pédagogique fondée sur des règles simples et des données passées : elle ne constitue pas un conseil en investissement. »
- L'optimisation est présentée comme un « exercice académique ».
- La fiscalité est simplifiée.

### Le bon usage

Comprendre, mesurer et discuter un portefeuille : c'est un support d'apprentissage et de dialogue. Une décision d'investissement relève de vous, ou d'un professionnel habilité qui connaît votre situation.

## Peut-on gérer plusieurs comptes et plusieurs portefeuilles ?
<!-- fiche: faq-plusieurs-portefeuilles | questions: peut on avoir plusieurs portefeuilles ; plusieurs comptes sur le même ordinateur ; mon pea et mon cto séparés ; regrouper deux portefeuilles en un ; vue consolidée de tous mes comptes ; combien de portefeuilles par compte ; un portefeuille par client | mots: plusieurs portefeuilles, plusieurs comptes, consolidation, regrouper, PEA, CTO, multi-utilisateur, espace personnel -->

### Plusieurs comptes

Oui : chaque personne qui utilise l'ordinateur crée son propre compte, avec son mot de passe. Chacun ne voit que ses portefeuilles.

### Plusieurs portefeuilles par compte

Oui : enregistrez autant de portefeuilles que vous voulez (par exemple un PEA et un compte-titres). Ils apparaissent dans la liste de la rubrique « Données », précédés de « Mon espace ». La page [[Mon compte]] permet de les renommer, télécharger ou supprimer.

### Une vue consolidée ?

Le logiciel analyse **un portefeuille à la fois** : il n'existe pas de vue qui additionne automatiquement plusieurs portefeuilles. Pour une analyse globale :

1. téléchargez l'un des portefeuilles depuis [[Mon compte]] (fichier CSV) ;
2. ouvrez l'autre, cliquez sur [[Ajouter des opérations]] et envoyez ce fichier ;
3. vérifiez le tableau, puis [[Enregistrer les opérations]].

Les opérations identiques sont reconnues comme doublons. Pour garder aussi les deux portefeuilles séparés, travaillez sur une copie : ajoutez d'abord le fichier téléchargé comme nouveau portefeuille dans [[Mon compte]], puis ajoutez-y les opérations de l'autre.

### Pour un conseiller

Un portefeuille par client fonctionne de la même façon, mais le logiciel n'a ni fiche client, ni profil réglementaire.

## Le logiciel peut-il se connecter à ma banque ?
<!-- fiche: faq-connexion-bancaire | questions: connexion bancaire automatique ; synchroniser avec mon courtier ; importer automatiquement depuis boursorama ; le logiciel se connecte-t-il à ma banque ; agrégation de comptes ; api bancaire ; mise à jour automatique de mes opérations | mots: connexion bancaire, synchronisation, agrégateur, API, courtier, import automatique, DSP2 -->

**Non.** Le logiciel ne se connecte à aucune banque ni à aucun courtier, et ne passe aucun ordre. C'est aussi une garantie de confidentialité : il ne vous demande jamais vos identifiants bancaires.

### Comment y faire entrer vos opérations

1. **Un export** de votre banque ou courtier, en CSV ou Excel : envoyez-le avec [[Envoyer un fichier (CSV, Excel ou PDF)]] ; l'import automatique reconnaît la plupart des formats, sinon l'assistant d'import vous guide.
2. **Un relevé ou un avis d'opéré en PDF** (plusieurs à la fois si vous le souhaitez, même protégés par un mot de passe) : il est lu automatiquement, quel que soit le courtier (PDF texte, ou image si la reconnaissance de caractères est installée) ; s'il n'est pas reconnu, le formulaire [[Compléter l'opération]] propose les valeurs trouvées dans le document.
3. **Une saisie à la main** : [[Ajouter des opérations]], onglet [[Saisie manuelle]].

### Mettre à jour ensuite

Inutile de tout renvoyer : avec [[Ajouter des opérations]], envoyez seulement les nouveaux mouvements. Les opérations déjà présentes sont reconnues et ne sont pas ajoutées deux fois.

## Obligations, or, monétaire : sont-ils pris en charge ?
<!-- fiche: faq-classes-actifs | questions: le logiciel gère-t-il les obligations ; puis je suivre de l'or ; fonds monétaire pris en charge ; etf obligataire ; obligation en direct ; fonds en euros d'assurance vie ; portefeuille multi actifs | mots: obligations, or, monétaire, classe d'actifs, ETF obligataire, duration, fonds en euros, multi-actifs | aller: Analyse du portefeuille/Expositions -->

**Oui, s'ils sont cotés** et ont un ticker Yahoo Finance, ce qui est le cas des ETF obligataires, d'or ou monétaires.

### Comment ils sont traités

- **Classe d'actifs** : Actions, Obligations, Or ou Monétaire, d'après le référentiel du projet, sinon la base locale. Un titre de classe inconnue est compté comme une action.
- **Obligations** : leur **duration** (si le référentiel la donne) sert à la sensibilité aux taux et au choc de taux.
- **Or** : compté à part, « sans pays », dans l'analyse en transparence.
- **Indices de référence** adaptés : emprunts d'État zone euro, obligations d'entreprises, monétaire €STR, ou mixtes 20/80, 60/40 et 80/20.
- **Coupons** : à enregistrer comme des dividendes (type DIVIDENDE).

Le portefeuille d'exemple « Portefeuille diversifié (multi-actifs) » illustre ces classes.

### Ce qui n'est pas pris en charge

Tout produit sans cours quotidien sur Yahoo Finance : fonds en euros d'assurance-vie, livrets, obligations détenues en direct sans cotation, produits structurés. Ils ne peuvent pas être valorisés.

### À noter

L'attribution de performance ne porte que sur la **poche actions** ; obligations et or en sont exclus.

## Comment sont gérées les devises ?
<!-- fiche: faq-devises | questions: le logiciel gère-t-il les actions en dollars ; dans quelle devise saisir le prix ; comment sont convertis les titres étrangers ; risque de change pris en compte ; actions de londres en pence ; taux de change utilisé ; mes frais en dollars | mots: devises, taux de change, conversion, dollar, livre, pence, risque de change, euro, couverture -->

Tout est exprimé **en euros**.

### À la saisie

- Le **prix** se saisit dans la **devise de cotation** du titre (dollars pour Apple, pence pour une action de Londres).
- Les **frais** sont toujours en euros.
- À l'import, le logiciel compare chaque prix au cours du jour et reconnaît un prix déjà converti en euros, en devise ou en pence ; il le ramène à l'unité de cotation.

### La conversion

`prix en euros = prix en devise × facteur / taux EURdevise` (facteur 0,01 pour les pence), au taux du jour de chaque opération pour les achats, ventes et dividendes, au taux de chaque jour pour l'historique, au dernier taux connu pour la valeur actuelle. Les taux viennent de Yahoo Finance et s'affichent en bas de la barre latérale.

### Le risque de change

La performance d'un titre étranger inclut la variation de sa devise. L'onglet Expositions mesure l'**exposition réelle** aux devises, ETF compris : un ETF monde coté en euros reste exposé au dollar, sauf s'il est couvert (« EUR Hedged »). Les stress tests incluent une baisse du dollar de 10 %.

## Comment les frais sont-ils pris en compte ?
<!-- fiche: faq-frais | questions: les frais sont ils pris en compte ; frais de courtage dans la performance ; frais de gestion des etf ; droits de garde ; les frais sont ils dans le pru ; frais dans l'optimisation ; ter de mon etf | mots: frais, frais de courtage, PRU, frais de gestion, TER, droits de garde, performance nette, backtest | chiffres: frais_totaux -->

### Les frais de courtage

Saisis en euros dans la colonne `frais` de chaque opération, ils comptent partout :

- **à l'achat**, ils augmentent le PRU ;
- **à la vente**, ils réduisent la plus-value réalisée ;
- **sur un dividende**, ils sont déduits du montant reçu ;
- **dans la performance**, ils font partie des flux : le rendement du jour d'achat les intègre.

Leur total figure dans la carte « Frais de courtage » de la Vue d'ensemble.

### Les frais de gestion des ETF

Ils sont prélevés dans le fonds et donc **déjà intégrés à son cours** : il n'y a rien à saisir.

### Les droits de garde et autres frais du compte

Ce ne sont pas des opérations sur titres : à l'import, les lignes de frais de garde ou de virement sont ignorées. Ils ne sont donc pas déduits de la performance.

### Dans les analyses avancées

- **Optimisation** : les montants à acheter ou vendre sont calculés hors frais.
- **Backtest** : des frais de transaction réglables (0,10 % par défaut) s'appliquent à chaque achat et rééquilibrage.
- **Fiscalité** : les frais de gestion des contrats d'assurance-vie sont ignorés.

## Comment les dividendes sont-ils pris en compte ?
<!-- fiche: faq-dividendes | questions: les dividendes sont ils pris en compte ; comment saisir un dividende ; le logiciel télécharge-t-il mes dividendes ; dividendes dans la performance ; etf capitalisant et dividendes ; pourquoi le cours baisse au détachement ; coupons des obligations | mots: dividendes, coupons, détachement, ETF capitalisant, ETF distribuant, performance, saisie, DIVIDENDE | chiffres: dividendes -->

### Ils comptent, à condition d'être saisis

Le logiciel ne télécharge **pas** les dividendes : seuls ceux de vos opérations comptent. Une ligne de dividende s'écrit avec le type DIVIDENDE, une quantité de 0 et le **montant total reçu** dans la colonne prix (dans la devise de cotation), les frais éventuels à part.

### Leur effet

- ils s'ajoutent au **gain total** (nets de frais) ;
- ils comptent dans la **performance** (TWR, TRI) comme de l'argent récupéré ;
- ils sont affichés par ligne dans l'onglet Positions et au total dans la carte « Dividendes et coupons ».

### Pourquoi c'est indispensable

Le logiciel utilise le cours **non ajusté** : le jour du détachement, le cours baisse à peu près du montant du dividende. Si le dividende n'est pas saisi, cette baisse apparaît comme une perte et la performance est sous-estimée.

### Les ETF

- **Capitalisant** : les dividendes sont réinvestis dans le cours ; rien à saisir.
- **Distribuant** : à saisir comme pour une action.

Les coupons d'un fonds obligataire distribuant se saisissent de la même façon.

## Puis-je obtenir un rapport à rendre ou à imprimer ?
<!-- fiche: faq-rapport-pdf | questions: puis je obtenir un rapport pdf ; rapport à rendre pour mon mémoire ; imprimer l'analyse ; le rapport est il en anglais ; exporter les résultats ; rapport pour mon client ; le rapport reprend-il mes réglages | mots: rapport PDF, export, impression, mémoire, synthèse, document, annexe, reportlab -->

**Oui.** En bas de la barre latérale, cliquez sur [[Rapport PDF]], puis sur [[Télécharger le rapport PDF]].

### Son contenu

Un document A4 qui reprend toute l'analyse : synthèse et chiffres clés, positions, expositions et diversification, performance, risque, optimisation, projection, conseil patrimonial (fiscalité, stress tests), gestion d'actifs (attribution, budget de risque, backtest) et une partie **méthodologie** qui définit chaque indicateur et ses limites.

### Ses particularités

- Il est toujours **en français** et sur fond clair, même si l'écran est en anglais ou en mode nuit.
- Il reprend le portefeuille, l'indice de référence, le taux sans risque et le niveau de VaR choisis, mais des réglages **fixes** pour l'optimisation (poids maximal de 30 %) et la projection (10 ans, 5 000 scénarios, loi normale, sans versement).
- Chaque page rappelle qu'il s'agit d'un outil pédagogique, pas d'un conseil en investissement.

### Autres exports

- l'historique des opérations en CSV, dans l'onglet Transactions ;
- chaque portefeuille de votre espace en CSV, depuis [[Mon compte]].

## Le logiciel fonctionne-t-il sur Mac ?
<!-- fiche: faq-mac | questions: le logiciel fonctionne-t-il sur mac ; version macos ; mac intel compatible ; installer sur macbook air m1 ; quelle version de macos faut il ; ça marche sur linux ; ipad ou chromebook | mots: Mac, macOS, Apple Silicon, M1, Intel, dmg, Linux, compatibilité, version en ligne -->

**Oui, sur les Mac récents.**

| Ordinateur | Solution |
|---|---|
| Mac Apple Silicon (M1, M2, M3, M4…), macOS 12 ou plus récent | application `Portfolio_Tracker_Mac.dmg` |
| Mac Intel (vendu avant fin 2020) | version en ligne du tableau de bord |
| Windows 10 ou 11, 64 bits | installateur `Installer_Portfolio_Tracker.exe` |
| Linux | lancement depuis le code source (Python 3.11 ou plus récent) |

### Sur Mac, à savoir

- Au premier lancement, macOS bloque l'application, qui ne vient pas de l'App Store : il faut l'autoriser une fois (voir le chapitre « Prise en main »).
- Une fenêtre Terminal s'ouvre : laissez-la ouverte, la fermer arrête le logiciel.
- Le tableau de bord s'ouvre dans Chrome, Edge ou Brave en mode « application » s'ils sont installés, sinon dans Safari.
- Vos comptes sont rangés dans `~/Library/Application Support/Portfolio Tracker` et conservés lors des mises à jour.

Les écrans, les calculs et le rapport sont identiques sur Windows et sur Mac.

## Comment savoir s'il existe une mise à jour ?
<!-- fiche: faq-mises-a-jour | questions: comment mettre à jour le logiciel ; le logiciel se met il à jour tout seul ; y a-t-il une nouvelle version ; je perds mes données en mettant à jour ; numéro de version ; la base de titres se met elle à jour | mots: mise à jour, nouvelle version, update, Releases, GitHub, version, réinstallation, base de titres -->

Le logiciel **ne vérifie pas** lui-même l'existence d'une nouvelle version (c'est aussi pourquoi il n'envoie rien à son créateur).

### Où regarder

Sur la page des versions du projet : `https://github.com/DieuUssop/Python/releases/latest`. Chaque version porte un numéro formé de sa date de fabrication (par exemple « 2026.10.05 »).

### Installer la nouvelle version

Fermez le logiciel, puis installez la nouvelle version **par-dessus** l'ancienne, sans désinstaller. Vos comptes et vos portefeuilles enregistrés sont conservés. Par précaution, téléchargez quand même une copie de vos portefeuilles depuis [[Mon compte]].

### Les cours, eux, se mettent à jour seuls

Chaque analyse avec Internet télécharge les cours récents et les ajoute à la base locale. Une nouvelle version apporte en plus une base de titres plus récente et, le cas échéant, des données de référence révisées (taux sans risque, composition des ETF).

## Quelles sont les limites connues du logiciel ?
<!-- fiche: faq-limites | questions: quelles sont les limites du logiciel ; que ne fait pas le logiciel ; points faibles de portfolio tracker ; améliorations possibles ; critiques du jury ; ce que le logiciel ne gère pas ; limites méthodologiques | mots: limites, points faibles, améliorations, simplifications, hypothèses, contraintes, perspectives -->

### Données

- une seule source de cours (Yahoo Finance), sans recoupement ni détection des valeurs aberrantes ;
- dividendes non téléchargés : seuls ceux saisis comptent ;
- divisions et regroupements d'actions ajustés seulement à partir de l'avis du courtier ; fusions et autres opérations sur titres non gérées ;
- composition des ETF, classement des titres et taux sans risque fixes et datés ;
- pays d'une action de la base locale déduit de sa place de cotation.

### Méthode

- taux sans risque constant sur toute la période ;
- loi normale pour la VaR paramétrique et une des méthodes de projection ;
- Markowitz fondé sur les rendements passés ;
- stress tests sans effet de change et sur des cours hors dividendes ;
- fiscalité simplifiée (pas de barème progressif, pas de frais de contrat) ;
- attribution limitée à la poche actions, par grandes régions.

### Fonctionnement

- trois types d'opération seulement : achat, vente, dividende ; pas de vente à découvert ;
- pas de connexion bancaire ;
- un portefeuille analysé à la fois ;
- mot de passe oublié = portefeuilles perdus ;
- pas de Mac Intel ; comptes temporaires sur la version en ligne ;
- pas de mise à jour automatique.

Le projet cite lui-même, comme amélioration possible, l'utilisation de la série historique du €STR pour le taux sans risque.

## Que faire si l'assistant ne trouve pas ma réponse ?
<!-- fiche: faq-assistant | questions: l'assistant ne trouve pas ma réponse ; je n'ai pas trouvé de réponse sûre ; l'aide ne comprend pas ma question ; comment poser une bonne question ; l'assistant est il une ia ; envoyer ma question au créateur | mots: assistant, aide, recherche, question, sans réponse, reformuler, sommaire, export | aller: Manuel et aide -->

L'assistant cherche dans ce manuel la fiche la plus proche de votre question et l'affiche telle qu'elle est écrite. Ce n'est pas une intelligence artificielle qui rédige : il ne peut rien inventer, mais il peut ne pas trouver.

### Essayez dans cet ordre

1. **Reformulez** avec d'autres mots, plus simples (« enlever un achat ») ou plus techniques (« supprimer une transaction »).
2. **Une seule question à la fois**, courte.
3. **Le nom exact** d'un indicateur ou d'un bouton : « VaR », « PRU », « Actualiser les cours ».
4. **Les fiches proches** proposées sous la réponse.
5. **Le sommaire** : choisissez un chapitre et ouvrez ses fiches.
6. **Ce chapitre**, le chapitre « Messages d'erreur et problèmes » et le **glossaire**.

### Faire compléter le manuel

Votre question sans réponse est notée sur cet ordinateur. Dans l'espace « Manuel et aide », la rubrique des questions restées sans réponse permet de les exporter avec [[Exporter les questions (CSV)]] et de les envoyer au créateur du logiciel. N'y tapez pas d'information personnelle : ces questions sont visibles par tous les utilisateurs de l'ordinateur.

## Pourquoi mes chiffres diffèrent-ils de ceux de ma banque ?
<!-- fiche: faq-ecart-banque | questions: pourquoi mes chiffres diffèrent de ma banque ; mon pru n'est pas le même que chez mon courtier ; la valeur de mon portefeuille est différente ; ma performance ne correspond pas à celle de ma banque ; écart de plus-value avec mon relevé ; pourquoi le gain est différent | mots: écart, banque, courtier, PRU, valorisation, performance, taux de change, cours, différence -->

Plusieurs causes, souvent cumulées.

| Différence | Explication |
|---|---|
| Valeur | cours de clôture de Yahoo Finance, et non cours en temps réel ; autre place de cotation possible |
| Titres étrangers | taux de change de Yahoo Finance, pas celui de votre banque |
| PRU | le logiciel inclut les frais d'achat ; certaines banques non |
| Plus-values | dépendent du PRU, donc des frais et des taux de change |
| Gain total | inclut les dividendes saisis ; sans eux, il est plus faible |
| Performance | le logiciel calcule TWR et TRI ; votre banque peut afficher une autre mesure (plus-value en %, performance depuis le 1er janvier…) |
| Historique | une opération manquante ou une division d'actions non saisie change tout |

### Comment vérifier

1. Comparez d'abord les **quantités** détenues (onglet Positions).
2. Puis les **cours** et la date « Données au » du bandeau.
3. Puis les **opérations** (onglet Transactions), en particulier les dividendes et les anciens achats.

Pour les montants officiels, notamment fiscaux, ce sont les documents de votre établissement qui font foi.

## Peut-on utiliser le logiciel pour sa déclaration d'impôts ?
<!-- fiche: faq-declaration-impots | questions: puis je utiliser le logiciel pour ma déclaration d'impôts ; les plus-values calculées sont elles fiscales ; calcul de l'impôt exact ; le logiciel remplace-t-il l'ifu ; fiscalité du logiciel fiable ; taux 2026 utilisés | mots: déclaration d'impôts, fiscalité, plus-values imposables, PFU, documents fiscaux, simplifications, IFU | aller: Conseil patrimonial/Fiscalité -->

**Non.** Les chiffres sont fiables pour l'analyse et la comparaison, pas pour une déclaration.

### Pourquoi

- Le logiciel calcule l'impôt d'une **vente totale hypothétique**, pour comparer CTO, PEA et assurance-vie, avec les taux 2026 (prélèvement forfaitaire unique de 31,4 %, PEA après 5 ans, assurance-vie après 8 ans).
- Il **simplifie** : option pour le barème progressif ignorée, primes d'assurance-vie supposées inférieures à 150 000 €, frais de contrat ignorés, dividendes supposés conservés dans l'enveloppe.
- Ses cours et taux de change viennent de Yahoo Finance, pas de votre établissement.
- Il ne connaît que les opérations que vous lui donnez.

### Ce qui fait foi

Les documents fiscaux et relevés transmis par votre banque ou votre courtier.

### À quoi sert l'onglet Fiscalité

À comprendre l'effet de l'enveloppe et de la durée de détention : il montre le gain net selon l'année de sortie, avec les seuils de 5 ans (PEA) et 8 ans (assurance-vie), et la part du portefeuille éligible au PEA.

## Comment savez-vous que les formules sont justes ?
<!-- fiche: faq-calculs-testes | questions: comment savez vous que les formules sont justes ; les calculs sont ils testés ; tests automatiques du logiciel ; pytest ; comment prouver que le twr est bien calculé ; validation des calculs ; vérification croisée | mots: tests, pytest, validation, vérification, formules, contrôle croisé, exactitude, qualité du code -->

### Des tests automatiques

Le projet contient un dossier `tests` d'environ 150 tests automatiques, lancés par le développeur avec la commande `python -m pytest`. Ils vérifient les calculs sur des exemples dont le résultat est connu : PRU, plus-values, TWR, TRI, volatilité, VaR, devises, optimisation, simulation, import des fichiers, comptes chiffrés…

### Des vérifications croisées

Certaines propriétés mathématiques doivent toujours être vraies ; les tests les contrôlent :

- le gain calculé jour par jour (`valeur − apports nets`) retombe exactement, le dernier jour, sur le gain total calculé ligne par ligne ;
- la somme des contributions au risque est égale à la volatilité du portefeuille (propriété d'Euler) ;
- la somme des effets d'attribution est égale à l'écart de performance avec l'indice (lissage de Cariño).

### Des formules transparentes

Chaque formule est écrite et commentée dans le code (dossier `src`) et reproduite au chapitre « Toutes les formules », avec un exemple chiffré que chacun peut refaire à la calculatrice ou dans un tableur.

### Ce que les tests ne couvrent pas

Ils ne vérifient pas les données de Yahoo Finance elles-mêmes, ni vos opérations.

## Avec quoi le logiciel est-il programmé ?
<!-- fiche: faq-technologies | questions: avec quoi le logiciel est programmé ; quel langage ; c'est fait en python ; quelles bibliothèques sont utilisées ; streamlit c'est quoi ; comment sont fabriqués les installateurs ; architecture du logiciel | mots: Python, Streamlit, pandas, NumPy, SciPy, Plotly, Matplotlib, ReportLab, yfinance, cryptography, GitHub Actions, architecture -->

Le logiciel est écrit en **Python** (version 3.11 ou plus récente depuis le code source).

### Les bibliothèques

| Rôle | Bibliothèque |
|---|---|
| Tableau de bord | Streamlit |
| Calculs | pandas, NumPy, SciPy (optimisation) |
| Graphiques interactifs | Plotly |
| Graphiques du rapport, rapport PDF | Matplotlib, ReportLab |
| Cours de bourse | yfinance (Yahoo Finance) |
| Chiffrement des comptes | cryptography (PBKDF2, Fernet) |
| Lecture des fichiers | openpyxl (Excel), pdfplumber (PDF), RapidOCR (PDF image, facultatif) |
| Tests | pytest |

### L'organisation

Les **calculs** sont dans le dossier `src` (un fichier par sujet : `metrics.py`, `portfolio.py`, `optimisation.py`…), séparés de l'**affichage** (`app.py` et les fichiers `vues_*.py`). Ils peuvent ainsi être testés sans lancer l'interface.

### La distribution

Les installateurs Windows (`.exe`) et Mac (`.dmg`) sont fabriqués automatiquement par GitHub Actions. Ils embarquent leur propre Python et toutes les bibliothèques : rien d'autre à installer.

## Le logiciel utilise-t-il l'intelligence artificielle ?
<!-- fiche: faq-intelligence-artificielle | questions: le logiciel utilise-t-il l'intelligence artificielle ; l'assistant est-il chatgpt ; y a-t-il une ia dans le logiciel ; les réponses sont-elles générées ; machine learning ; le logiciel invente-t-il des réponses | mots: intelligence artificielle, IA, ChatGPT, assistant, recherche, OCR, génératif, machine learning -->

**Non, pas d'intelligence artificielle générative.**

### L'assistant du manuel

Il ne rédige rien. Il compare les mots de votre question à ceux des fiches du manuel (titre, formulations courantes, synonymes, texte), en tolérant les fautes de frappe et l'absence d'accents, puis affiche la fiche la plus proche **telle qu'elle a été écrite**. Il ne peut donc rien inventer. S'il ne trouve pas, il le dit. Il fonctionne hors connexion et n'envoie rien.

### Les autres automatismes

- **La reconnaissance des colonnes** d'un fichier importé repose sur des règles : noms de colonnes connus, contenu des cellules, cohérence des chiffres.
- **La reconnaissance de caractères** des PDF image utilise un moteur spécialisé (RapidOCR ou Tesseract), qui lit des lettres sur une image.
- **Le diagnostic** de l'onglet Expositions applique des règles simples aux seuils documentés.

Tous les résultats chiffrés viennent de formules explicites, décrites au chapitre « Toutes les formules ».

## Le logiciel existe-t-il en anglais ?
<!-- fiche: faq-anglais | questions: le logiciel existe-t-il en anglais ; passer en anglais ; english version ; le rapport pdf en anglais ; le manuel en anglais ; changer de langue | mots: anglais, English, langue, traduction, FR, EN, rapport en français -->

**Oui pour l'écran.** En haut de la barre latérale, le sélecteur **FR | EN** fait passer le tableau de bord en anglais : menus, boutons, indicateurs, graphiques et l'essentiel des messages.

### Ce qui reste en français

- **Le rapport PDF**, rédigé en français quelle que soit la langue de l'écran.
- **Le manuel**, tant que sa traduction anglaise n'est pas fournie : le logiciel affiche alors la version française.
- Les noms de vos titres et le contenu de vos fichiers, tels quels.

### La préférence

La langue est gardée pendant la session. Le chapitre « L'écran et la navigation » détaille ce réglage.

## Les divisions d'actions et opérations sur titres sont-elles gérées ?
<!-- fiche: faq-divisions | questions: les divisions d'actions sont elles gérées ; split d'actions ; mon titre a fait un split ; regroupement d'actions ; fusion de sociétés ; attribution d'actions gratuites ; perte de 90 % après un split | mots: division d'actions, split, regroupement, fusion, scission, opération sur titres, actions gratuites -->

**En partie.** Le logiciel ne connaît que trois types d'opération : achat, vente et dividende, et il ne détecte pas seul une division. Mais il sait ajuster vos opérations à partir de l'avis de division ou de regroupement envoyé par votre courtier.

### Le problème

Après une division d'actions, Yahoo Finance corrige rétroactivement ses cours. Votre fichier, lui, indique toujours l'ancien nombre de titres : la valeur calculée devient fausse. Exemple : 10 actions achetées 800 €, puis division par 10 ; Yahoo affiche environ 80 € pour la date d'achat, et le logiciel valoriserait 10 × 80 € au lieu de 100 × 80 €.

### Le signal

À l'import, le contrôle des prix signale l'écart (« ticker, devise ou division d'actions à vérifier »). Une perte soudaine d'environ 50, 67 ou 90 % doit aussi alerter.

### La correction

Exprimez l'opération en titres d'après la division, **sans changer le montant** : ici, 100 actions à 80 €. Le plus simple : déposez l'avis de division (PDF) sur la page [[Ajouter des opérations]], puis cliquez sur [[Appliquer aux opérations antérieures]] (voir le chapitre sur l'import, fiche « Division ou regroupement d'actions »). Sinon, faites-le à la main dans l'onglet Transactions avec [[Modifier les opérations]].

### Les autres opérations sur titres

Fusions, scissions, changements de code ou attributions gratuites : à traduire vous-même en achats et ventes.

## Pourquoi le MSCI World est-il l'indice de référence par défaut ?
<!-- fiche: faq-indice-defaut | questions: pourquoi le msci world par défaut ; pourquoi comparer à un etf ; quel indice choisir pour mon portefeuille ; pourquoi pas le cac 40 ; indice de référence adapté ; changer d'indice | mots: indice de référence, MSCI World, CW8, benchmark, CAC 40, dividendes réinvestis, choix de l'indice | aller: Analyse du portefeuille/Performance -->

### Les raisons

- **Un marché mondial** : la plupart des portefeuilles d'actions diversifiés sont comparés aux actions mondiales.
- **Dividendes réinvestis** : il est représenté par l'ETF Amundi MSCI World (CW8), **capitalisant**. Comme votre performance inclut vos dividendes, la comparaison est équitable.

### Pourquoi pas le CAC 40 ?

Le CAC 40 proposé est l'indice de prix, **hors dividendes** : il désavantage l'indice, d'environ 3 % par an selon le projet. Il n'est pertinent que pour un portefeuille d'actions françaises, en gardant ce biais en tête.

### Choisir le bon indice

Dans [[Paramètres]], [[Indice de référence]] propose des indices d'actions, obligataires, monétaire et mixtes (20/80, 60/40, 80/20). Choisissez celui qui ressemble à votre allocation : un portefeuille équilibré se compare mieux à un indice 60/40 qu'au MSCI World. Un indice inadapté fausse le bêta, l'alpha et la tracking error ; face à un indice obligataire ou monétaire, l'onglet Performance prévient que le bêta et l'alpha ont peu de sens.

## La projection Monte-Carlo est-elle une prévision ?
<!-- fiche: faq-projection | questions: la projection est elle une prévision ; combien vaudra mon portefeuille dans 10 ans ; le scénario médian va-t-il se réaliser ; fiabilité de la simulation monte carlo ; probabilité de perte fiable ; pourquoi l'éventail s'élargit | mots: projection, Monte-Carlo, prévision, scénario médian, probabilité, incertitude, hypothèses, horizon | aller: Analyse du portefeuille/Projection -->

**Non.** L'écran le rappelle : « Une projection n'est pas une prévision : elle suppose que les hypothèses se vérifient, ce qui n'est jamais garanti. »

### Ce qu'elle fait

Elle simule 5 000 futurs possibles, tous cohérents avec un rendement et une volatilité choisis (par défaut, ceux du passé du portefeuille), et montre leur distribution : scénarios défavorable, médian et favorable, probabilité de perte, probabilité d'atteindre un objectif.

### Comment la lire

- La **médiane** n'est pas une prévision : c'est le milieu des possibles.
- L'écart entre les scénarios **grandit avec l'horizon** : l'incertitude s'accumule.
- La moyenne dépasse la médiane (loi log-normale) : la médiane est le repère le plus représentatif.

### Ses hypothèses

- rendement et volatilité **constants** sur tout l'horizon ;
- méthode « Loi normale » : krachs sous-estimés ; la méthode « Historique (bootstrap) » conserve les vrais krachs du portefeuille ;
- rendement historique souvent flatteur : réduire le [[Rendement annuel supposé (%)]] donne une projection plus prudente.

## Pourquoi plusieurs VaR, et laquelle retenir ?
<!-- fiche: faq-plusieurs-var | questions: pourquoi plusieurs var ; quelle var retenir ; var historique ou var normale ; différence entre var et cvar ; quelle mesure de risque présenter ; la var est-elle suffisante ; pourquoi une var sur un jour | mots: VaR, CVaR, VaR historique, VaR loi normale, Cornish-Fisher, mesure de risque, Expected Shortfall | aller: Analyse du portefeuille/Risque | chiffres: var_historique, var_parametrique, var_cornish_fisher, cvar -->

Chaque méthode repose sur une hypothèse différente ; les comparer fait partie de l'analyse.

| Mesure | Hypothèse | Atout | Limite |
|---|---|---|---|
| VaR historique | le passé se répète | aucune loi supposée | aveugle aux crises absentes de l'historique |
| VaR loi normale | rendements normaux | simple, standard | sous-estime les krachs |
| VaR Cornish-Fisher | loi normale corrigée | tient compte de l'asymétrie et de la kurtosis | « n.d. » si elles sont trop fortes |
| CVaR | le passé se répète | mesure la gravité au-delà du seuil | repose sur peu de jours |

### Laquelle retenir

- **La VaR historique** est la mesure principale du logiciel : c'est elle qui figure sur la carte en euros de l'onglet Risque et dans le rapport.
- **La CVaR** la complète : elle dit ce que coûte un jour au-delà du seuil.
- **L'écart entre VaR historique et VaR normale** est en soi une information : la lecture automatique le commente.

### Pourquoi sur un jour ?

Les VaR du logiciel portent sur la perte d'**un jour de bourse**, calculée sur les rendements quotidiens. Pour des horizons plus longs, voyez le max drawdown, les stress tests et la projection.
