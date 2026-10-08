# Prise en main
<!-- chapitre: demarrage | ordre: 1 -->

Ce chapitre explique ce qu'est Portfolio Tracker, comment l'installer sous Windows ou sur Mac, comment le lancer et le fermer, ce qui fonctionne sans Internet, comment le mettre à jour ou le désinstaller, et comment l'utiliser en ligne ou depuis son code source. Commencez par ici si vous découvrez le logiciel.

## Qu'est-ce que Portfolio Tracker et à qui sert-il ?
<!-- fiche: demarrage-presentation | questions: c'est quoi ce logiciel ; a quoi sert portfolio tracker ; qu'est-ce que je peux faire avec ce programme ; est-ce que c'est un conseil en investissement ; pour qui est fait cet outil ; est-ce que le logiciel se connecte à ma banque ; que fait l'application exactement ; presentation du logiciel ; à qui s'adresse ce logiciel ; c'est fait pour quel master ; c'est le projet de l'iae de caen ; que veut dire g2c | mots: présentation, objectif, fonctionnalités, Master G2C, gestion d'actifs, contrôle des risques, conformité, IAE Caen, Université de Caen Normandie, outil pédagogique, suivi de portefeuille, tableau de bord | aller: Analyse du portefeuille -->

Portfolio Tracker est un outil de suivi et d'analyse de portefeuille boursier, réalisé par un étudiant du Master G2C (Gestion d'actifs, Contrôle des risques et Conformité) de l'IAE Caen (Université de Caen Normandie), dans le cadre de sa formation. Il lit l'historique des opérations d'un portefeuille (achats, ventes, dividendes), le valorise aux cours de marché et calcule les indicateurs utilisés par les professionnels de la gestion.

### Ce qu'il fait

- **Suivi** : prix de revient unitaire (PRU), plus-values latentes et réalisées, dividendes, frais, valeur jour par jour, titres en devises convertis en euros.
- **Performance et risque** : TWR, TRI, comparaison avec un indice de référence, volatilité, drawdown, ratios de Sharpe et de Sortino, bêta, alpha, VaR et CVaR.
- **Analyses avancées** : expositions en transparence, optimisation de Markowitz, projection de Monte-Carlo.
- **Conseil patrimonial** : fiscalité comparée CTO, PEA et assurance-vie, stress tests.
- **Gestion d'actifs** : attribution de performance, budget de risque, backtest de stratégies.
- **Restitution** : tableau de bord interactif en français ou en anglais, et rapport PDF de synthèse.

### À qui il s'adresse

Il a été conçu d'abord pour les étudiants et les enseignants du Master G2C de l'IAE Caen : il met en pratique, sur un vrai portefeuille, les trois volets de la formation : la **gestion d'actifs** (mesure et attribution de la performance, allocation, optimisation de Markowitz, backtest de stratégies), le **contrôle des risques** (volatilité, VaR historique, normale et Cornish-Fisher, CVaR, stress tests, budget de risque, diagnostic des expositions) et la **conformité** (contrôles des opérations saisies, traçabilité des sources, données chiffrées et protection des données personnelles). Il peut aussi servir à tout particulier qui veut comprendre la performance et le risque de son portefeuille.

### Ce qu'il ne fait pas

- Il ne se connecte pas à votre banque ni à votre courtier : vous lui donnez vos opérations sous forme de fichier (CSV, Excel ou PDF) ou par saisie.
- Il ne passe aucun ordre de bourse.
- Ses résultats ne constituent pas un conseil en investissement : c'est un outil pédagogique, comme le rappelle le pied de page de chaque écran.

## Quel ordinateur faut-il pour utiliser le logiciel ?
<!-- fiche: demarrage-configuration | questions: configuration requise ; est-ce que ça marche sur mon pc ; est-ce que ca marche sur un mac intel ; quelle version de windows faut il ; il faut quel macos ; ça marche sur linux ; est-ce qu'il faut installer python ; mon ordinateur est trop vieux | mots: configuration minimale, prérequis, Windows 64 bits, Apple Silicon, M1, macOS 12, système d'exploitation, compatibilité -->

Le logiciel existe en deux versions installables et en une version en ligne.

| Système | Version à utiliser | Conditions |
|---|---|---|
| Windows | Installateur `.exe` | Windows 64 bits (Windows 10 ou 11) |
| Mac récent | Image disque `.dmg` | Mac à puce Apple Silicon (M1, M2, M3, M4…) et macOS 12 ou plus récent |
| Mac Intel (avant fin 2020) | Version en ligne | L'application Mac n'est pas prévue pour ces modèles |
| Linux ou autre | Code source | Python installé (voir la fiche sur le lancement depuis le code source) |

### Ce qu'il n'est pas nécessaire d'installer

Les versions Windows et Mac contiennent leur propre Python et toutes les bibliothèques nécessaires : vous n'avez rien d'autre à installer. Aucun mot de passe administrateur n'est demandé sous Windows.

### Le navigateur

Le tableau de bord s'affiche dans une fenêtre de navigateur. Sous Windows, il utilise Microsoft Edge (présent sur Windows 10 et 11) ou, à défaut, Google Chrome. Sur Mac, il utilise Google Chrome, Microsoft Edge ou Brave s'ils sont installés, sinon votre navigateur par défaut (Safari, le plus souvent).

### Internet

Une connexion n'est nécessaire que pour télécharger le logiciel et pour obtenir les cours les plus récents. Le reste fonctionne hors connexion (voir la fiche « Utiliser le logiciel sans Internet »).

## Où télécharger le logiciel ?
<!-- fiche: demarrage-telecharger | questions: ou est ce que je telecharge le logiciel ; lien de téléchargement ; comment récupérer l'installateur ; je trouve pas le fichier exe ; ou trouver le dmg pour mac ; quelle est la derniere version ; page releases github ; télécharger portfolio tracker | mots: téléchargement, download, GitHub, Releases, installateur, exe, dmg, dernière version -->

Les installateurs sont publiés sur la page des versions (« Releases ») du dépôt GitHub du projet :

`https://github.com/DieuUssop/Python/releases/latest`

Cette adresse ouvre toujours la version la plus récente. Dans la partie « Assets » de la page, choisissez le fichier qui correspond à votre ordinateur :

| Fichier | Pour |
|---|---|
| `Installer_Portfolio_Tracker.exe` | Windows |
| `Portfolio_Tracker_Mac.dmg` | Mac Apple Silicon |

Ne téléchargez pas les archives « Source code » proposées par GitHub sur la même page : elles contiennent le code du projet, utile seulement pour le lancer comme développeur (voir la fiche sur le code source).

### Numéro de version

Chaque version porte un numéro formé de sa date de fabrication (par exemple « 2026.10.05 »). Les installateurs sont fabriqués automatiquement par GitHub, sur des machines Windows et Mac, puis déposés ensemble dans la même version.

### Le logiciel ne se met pas à jour tout seul

Le logiciel ne vérifie pas lui-même s'il existe une nouvelle version. Pour en profiter, revenez sur cette page et installez la nouvelle version par-dessus l'ancienne : vos comptes sont conservés (voir la fiche « Mettre à jour le logiciel »).

## Installer le logiciel sous Windows
<!-- fiche: demarrage-installer-windows | questions: comment installer sur windows ; installation pas a pas ; j'ai téléchargé le exe et maintenant ; ou s'installe le programme ; faut il etre administrateur ; comment avoir l'icone sur le bureau ; dans quel dossier est installé portfolio tracker ; installer pour un seul utilisateur | mots: installation, setup, installateur, exe, Windows, AppData, menu Démarrer, raccourci, Bureau -->

### Les étapes

1. Téléchargez `Installer_Portfolio_Tracker.exe` depuis la page des versions du projet.
2. Double-cliquez sur le fichier. Si Windows affiche « Windows a protégé votre ordinateur », suivez la fiche « Windows ou Edge bloque l'installateur ».
3. L'assistant d'installation s'ouvre (en français ou en anglais). Cliquez sur Suivant.
4. Laissez cochée, si vous le souhaitez, la case qui crée une icône sur le Bureau.
5. Cliquez sur Installer, puis sur Terminer. La dernière page propose de lancer Portfolio Tracker immédiatement.

### Une installation pour vous seul

L'installation se fait pour l'utilisateur Windows en cours, sans droits d'administrateur. Le logiciel est placé dans votre dossier personnel :

`C:\Users\<votre nom>\AppData\Local\Programs\Portfolio Tracker\`

Si plusieurs personnes utilisent le même ordinateur avec des sessions Windows différentes, chacune doit l'installer dans sa propre session. À l'inverse, plusieurs personnes peuvent partager la même session Windows : chacune crée alors son propre compte chiffré dans le logiciel.

### Ce que l'installation crée

- un raccourci « Portfolio Tracker » dans le menu Démarrer (et sur le Bureau si la case était cochée) ;
- un raccourci de désinstallation dans le même groupe du menu Démarrer ;
- le dossier du programme, qui contient son propre Python, le code du logiciel et la base locale de titres (cours utilisables hors connexion).

### Ensuite

Lancez le logiciel avec l'icône « Portfolio Tracker ». Une petite fenêtre noire s'ouvre, puis le tableau de bord dans sa propre fenêtre : voir la fiche « Lancer le logiciel ».

## Windows ou Edge bloque l'installateur : que faire ?
<!-- fiche: demarrage-avertissement-windows | questions: windows a protégé votre ordinateur ; smartscreen bloque l'installation ; edge dit que le fichier est dangereux ; executer quand meme ou est le bouton ; mon antivirus bloque le exe ; est-ce que c'est un virus ; editeur inconnu ; impossible de lancer l'installateur | mots: SmartScreen, avertissement, éditeur inconnu, Informations complémentaires, Exécuter quand même, antivirus, programme non signé, sécurité -->

L'installateur n'est pas signé par un certificat d'éditeur (un tel certificat est payant chaque année). Windows et Microsoft Edge affichent donc des avertissements, qui sont normaux pour ce type de logiciel.

### Au téléchargement dans Microsoft Edge

Edge peut signaler que le fichier n'est pas couramment téléchargé et le bloquer. Ouvrez la liste des téléchargements, cliquez sur le menu « … » à côté du fichier, puis choisissez de le conserver (« Conserver », puis éventuellement « Conserver quand même »). Les intitulés exacts dépendent de la version d'Edge.

### Au lancement : « Windows a protégé votre ordinateur »

Ce message de SmartScreen apparaît au double-clic sur l'installateur.

1. Cliquez sur le lien **Informations complémentaires**.
2. Le nom du programme et la mention « Éditeur : Éditeur inconnu » apparaissent.
3. Cliquez sur le bouton **Exécuter quand même**.

L'installation se poursuit ensuite normalement.

### Si votre antivirus bloque le fichier

La cause est la même : le programme n'est pas signé. Si vous l'avez téléchargé depuis la page officielle des versions du projet, vous pouvez l'autoriser dans votre antivirus. En cas de doute, demandez conseil à votre enseignant ou à votre service informatique.

### Bon réflexe

Téléchargez toujours l'installateur depuis la page des versions du projet (`https://github.com/DieuUssop/Python/releases/latest`) ou depuis le lien transmis par votre enseignant, jamais depuis un site tiers.

## Installer le logiciel sur Mac
<!-- fiche: demarrage-installer-mac | questions: comment installer sur mac ; installation macbook ; que faire du fichier dmg ; glisser dans applications ; ça marche sur mac m1 ; installer portfolio tracker sur macos ; ou est l'application sur mac ; mac intel est ce que ca marche | mots: Mac, macOS, dmg, Applications, Apple Silicon, M1, M2, installation, MacBook -->

### Les étapes

1. Téléchargez `Portfolio_Tracker_Mac.dmg` depuis la page des versions du projet.
2. Double-cliquez sur le fichier `.dmg` : une fenêtre s'ouvre avec l'application « Portfolio Tracker », un raccourci vers le dossier « Applications » et un fichier `LISEZ-MOI.txt`.
3. Glissez « Portfolio Tracker » sur le dossier « Applications ».
4. Ouvrez le dossier Applications et double-cliquez sur « Portfolio Tracker ».

La toute première fois, macOS refuse d'ouvrir l'application, car elle ne vient pas de l'App Store : suivez la fiche « macOS refuse d'ouvrir l'application ». Cette manipulation n'est à faire qu'une fois.

### Conditions

- Mac à puce Apple Silicon (M1, M2, M3, M4…) ;
- macOS 12 ou plus récent.

Les Mac à processeur Intel (vendus avant fin 2020) ne sont pas pris en charge par cette application : utilisez la version en ligne du tableau de bord.

### Ce qui se passe au lancement

Une fenêtre Terminal s'ouvre (c'est l'équivalent de la fenêtre noire de Windows), puis le tableau de bord, dans Chrome ou Edge en mode « application » s'ils sont installés, sinon dans votre navigateur par défaut. Laissez la fenêtre Terminal ouverte pendant l'utilisation.

### Où sont vos données

Vos comptes et portefeuilles chiffrés sont rangés dans :

`~/Library/Application Support/Portfolio Tracker`

Ils sont conservés quand vous installez une nouvelle version.

## macOS refuse d'ouvrir l'application au premier lancement
<!-- fiche: demarrage-mac-bloque | questions: impossible d'ouvrir portfolio tracker car le developpeur ne peut pas etre verifie ; mac bloque l'application ; ouvrir quand meme mac ; application endommagée ou non vérifiée ; gatekeeper bloque ; clic droit ouvrir ne marche pas ; macos sequoia bloque l'appli ; comment autoriser l'app sur mac | mots: Gatekeeper, sécurité macOS, Confidentialité et sécurité, Ouvrir quand même, développeur non identifié, Sequoia, autorisation -->

L'application n'est pas distribuée par l'App Store ni signée par Apple. Au premier lancement, macOS l'empêche donc de s'ouvrir. La façon de l'autoriser dépend de votre version de macOS.

### macOS 15 (Sequoia) et plus récent

1. Au message de blocage, cliquez sur « Terminé ».
2. Ouvrez Réglages Système, puis Confidentialité et sécurité.
3. Descendez jusqu'au message qui concerne « Portfolio Tracker ».
4. Cliquez sur « Ouvrir quand même », puis confirmez (macOS peut demander votre mot de passe de session).

### macOS 12 à 14

1. Dans le dossier Applications, faites un clic droit (ou Ctrl + clic) sur « Portfolio Tracker ».
2. Choisissez « Ouvrir ».
3. Dans la fenêtre qui apparaît, cliquez à nouveau sur « Ouvrir ».

### Une seule fois

Une fois l'application autorisée, elle s'ouvre ensuite par un simple double-clic. Il peut être nécessaire de recommencer après l'installation d'une nouvelle version.

### Le Terminal s'ouvre : c'est normal

Le lancement ouvre une fenêtre Terminal qui fait tourner le tableau de bord. Ne la fermez pas pendant l'utilisation : la fermer arrête le logiciel.

## Lancer le logiciel : la fenêtre noire et la fenêtre du tableau de bord
<!-- fiche: demarrage-premier-lancement | questions: comment ouvrir le logiciel ; pourquoi une fenetre noire s'ouvre ; c'est quoi la console noire au lancement ; le logiciel s'ouvre dans edge c'est normal ; pourquoi ça s'ouvre dans le navigateur ; premier lancement ; c'est quoi localhost 8501 ; je peux fermer la fenetre noire | mots: lancement, démarrage, fenêtre noire, console, Terminal, Edge, Chrome, mode application, localhost, 8501 -->

### Ce qui se passe quand vous cliquez sur l'icône

1. **Une fenêtre noire s'ouvre** (le Terminal sur Mac). Elle affiche le nom du logiciel, l'adresse du tableau de bord et ce message : laissez cette fenêtre ouverte pendant l'utilisation, fermez-la pour quitter l'application. C'est le « moteur » du logiciel.
2. **Le tableau de bord s'ouvre dans sa propre fenêtre**, dès qu'il est prêt (comptez quelques secondes). Il s'agit d'une fenêtre de Microsoft Edge ou de Google Chrome en mode « application » : sans barre d'adresse ni onglets, elle ressemble à un logiciel classique. Si aucun de ces navigateurs n'est trouvé, le tableau de bord s'ouvre dans votre navigateur habituel.

### Pourquoi un navigateur ?

Le logiciel est une application web qui tourne sur votre propre ordinateur. Son adresse commence par `http://localhost:` suivi d'un numéro (8501 en général, ou le suivant libre jusqu'à 8510). « localhost » désigne votre ordinateur lui-même : rien ne passe par Internet pour afficher le tableau de bord, et personne d'autre sur le réseau (Wi-Fi de l'école, par exemple) ne peut s'y connecter.

### Ce que vous voyez en premier

Le tableau de bord s'ouvre sur l'espace « Analyse du portefeuille », avec le premier portefeuille de la liste. Vous pouvez immédiatement en choisir un autre, envoyer votre propre fichier ou vous connecter à votre espace personnel (voir le chapitre « L'écran et la navigation »).

### Si vous cliquez une deuxième fois sur l'icône

Si le logiciel est déjà en marche, il n'est pas relancé : la fenêtre du tableau de bord est simplement rouverte. C'est utile si vous avez fermé la fenêtre du tableau de bord par erreur, tant que la fenêtre noire est encore ouverte.

## Le tableau de bord ne s'ouvre pas
<!-- fiche: demarrage-fenetre-ne-souvre-pas | questions: rien ne s'ouvre quand je lance le logiciel ; la fenetre du tableau de bord ne s'affiche pas ; page blanche au demarrage ; aucun port libre ; le tableau de bord n'a pas pu démarrer ; la fenetre noire s'ouvre mais rien d'autre ; le logiciel ne se lance pas ; ça charge à l'infini | mots: problème de lancement, dépannage, erreur au démarrage, port, 8501, localhost, page blanche, ne démarre pas -->

### La fenêtre noire est ouverte mais aucune fenêtre n'apparaît

Le premier démarrage peut prendre un peu de temps. Si rien ne s'affiche, ouvrez vous-même votre navigateur et tapez l'adresse indiquée dans la fenêtre noire, par exemple `http://localhost:8501`. Le logiciel attend jusqu'à trois minutes que le tableau de bord soit prêt avant d'ouvrir la fenêtre ; passé ce délai, il continue de tourner, mais c'est à vous d'ouvrir l'adresse.

### Message « Aucun port libre entre 8501 et 8510 »

Le logiciel utilise le premier numéro libre entre 8501 et 8510. Si tous sont occupés par d'autres programmes, il ne peut pas démarrer. Fermez une autre application (par exemple une autre application Streamlit), puis relancez Portfolio Tracker.

### Message « Le tableau de bord n'a pas pu démarrer »

Un message d'erreur technique est affiché juste au-dessus. Appuyez sur Entrée pour fermer la fenêtre, puis relancez. Si l'erreur persiste, notez ou photographiez ce message et transmettez-le à votre enseignant ou au créateur du logiciel.

### La fenêtre s'ouvre mais reste blanche ou indique une erreur de connexion

Vérifiez que la fenêtre noire est toujours ouverte : si elle a été fermée, le logiciel est arrêté. Relancez-le avec l'icône.

### Le tableau de bord affiche « Impossible d'analyser le portefeuille »

Le logiciel fonctionne, mais le portefeuille choisi n'a pas pu être lu ou valorisé. Choisissez un autre portefeuille ou consultez le chapitre consacré à l'import des fichiers.

## Fermer le logiciel
<!-- fiche: demarrage-fermer | questions: comment quitter le logiciel ; comment fermer portfolio tracker ; j'ai fermé la fenetre mais il tourne encore ; faut il fermer la fenetre noire ; arreter l'application ; quitter sur mac ; ctrl c pour arreter ; est-ce que mes données sont enregistrées quand je ferme | mots: quitter, fermer, arrêter, sortir, fenêtre noire, Terminal, Ctrl+C, fin de session -->

### Sous Windows

Fermez la **fenêtre noire** : c'est elle qui fait tourner le logiciel. Fermer seulement la fenêtre du tableau de bord ne l'arrête pas ; vous pouvez d'ailleurs la rouvrir en cliquant de nouveau sur l'icône « Portfolio Tracker ».

### Sur Mac

Fermez la **fenêtre Terminal** ouverte au lancement. macOS demande si vous voulez mettre fin au processus en cours : cliquez sur « Fermer ». Le tableau de bord s'arrête avec elle.

### Depuis le code source

Si vous avez lancé le logiciel avec la commande `python -m streamlit run app.py`, appuyez sur Ctrl + C dans le terminal.

### Vos données sont-elles enregistrées ?

- Les portefeuilles enregistrés dans votre espace personnel sont écrits sur le disque, chiffrés, au moment où vous les enregistrez ou les modifiez : rien n'est perdu à la fermeture.
- En revanche, un fichier simplement envoyé dans la barre latérale, sans être enregistré dans votre espace, n'est pas conservé : il faudra l'envoyer de nouveau à la prochaine ouverture.
- Votre session (compte connecté, langue, réglages de l'écran) se termine à la fermeture. Le mode clair ou nuit choisi pendant que vous étiez connecté est retrouvé à votre prochaine connexion.

Sans fermer le logiciel, vous êtes de toute façon déconnecté automatiquement de votre compte après 30 minutes d'inactivité.

## Mes données quittent-elles mon ordinateur ?
<!-- fiche: demarrage-confidentialite | questions: mes données sont elles envoyées sur internet ; est-ce que mon portefeuille part sur un serveur ; confidentialité des données ; qui peut voir mes positions ; rgpd ; est-ce que yahoo voit mes montants ; est-ce que quelqu'un sur le wifi peut voir mon tableau de bord ; c'est sécurisé | mots: confidentialité, vie privée, RGPD, sécurité, données personnelles, localhost, chiffrement, Yahoo Finance -->

Avec la version installée (Windows ou Mac), tout reste sur votre ordinateur.

### Le tableau de bord tourne en local

Le logiciel fonctionne à l'adresse `localhost`, c'est-à-dire sur votre ordinateur lui-même. Il n'accepte aucune connexion venant d'un autre appareil : personne sur le même réseau ne peut ouvrir votre tableau de bord.

### Vos portefeuilles sont chiffrés

Les portefeuilles enregistrés dans votre espace personnel sont chiffrés avec une clé tirée de votre mot de passe. Les autres utilisateurs du même ordinateur ne peuvent pas les lire. Contrepartie : un mot de passe oublié rend les portefeuilles définitivement illisibles (voir le chapitre consacré aux comptes).

### Ce qui est envoyé sur Internet

Pour obtenir les cours, le logiciel interroge Yahoo Finance avec les **codes des titres** (tickers) et, pour reconnaître un titre inconnu lors d'un import, avec son code ISIN ou son nom. Les quantités, les montants et la composition de votre portefeuille ne sont jamais envoyés.

### Les questions posées à l'assistant

L'assistant du manuel fonctionne sans Internet. Les questions restées sans réponse sont notées dans un fichier sur votre ordinateur uniquement ; elles ne sont transmises à personne, sauf si vous exportez ce fichier vous-même.

### Cas de la version en ligne

Sur la version en ligne, le logiciel tourne sur un serveur distant : les fichiers que vous y envoyez sont traités sur ce serveur. Pour des données personnelles réelles, préférez la version installée.

## Utiliser le logiciel sans Internet
<!-- fiche: demarrage-hors-connexion | questions: est-ce que ça marche sans internet ; utiliser hors ligne ; mode hors connexion ; je suis dans le train sans wifi ; pourquoi les cours ne sont pas à jour ; cours en cache ça veut dire quoi ; les cours datent d'il y a longtemps ; pas de connexion le logiciel marche quand meme | mots: hors connexion, hors ligne, offline, sans Internet, cache, base locale, cours en cache, avion -->

Le logiciel est conçu pour fonctionner sans Internet. Il est livré avec une **base locale de titres** : la fiche de plusieurs milliers d'actions, d'ETF, d'indices et de taux de change, avec leurs cours de clôture quotidiens (depuis 2015 pour les titres, depuis 2007 pour les indices et les taux de change).

### Ce qui fonctionne hors connexion

- ouvrir le tableau de bord, se connecter à son compte, ouvrir ses portefeuilles ;
- analyser un portefeuille dont les titres sont dans la base ou dans le cache ;
- importer un fichier CSV ou Excel, reconnaître les codes ISIN ou les noms déjà connus de la base ou de la mémoire des titres ;
- convertir les devises, comparer à un indice de référence, et utiliser les autres espaces ;
- la carte du monde, si son fond de carte a déjà été enregistré ;
- l'assistant et le manuel.

### Comment savoir que les cours ne sont pas du jour

- Dans le bandeau en haut de page, la pastille indique « Cours en cache (hors ligne) » avec un point orange, au lieu de « Cours en direct · Yahoo Finance ».
- En bas de la barre latérale, la ligne « Cours » indique « cache local du » suivi de la date des derniers cours connus, et la mention « Yahoo Finance injoignable ».

Hors connexion, les cours s'arrêtent donc à la dernière date connue de la base ou du cache. Les calculs restent justes, mais à cette date.

### Quand Internet revient

Les cours se complètent automatiquement à la prochaine analyse. Les résultats étant gardés en mémoire une heure, utilisez le bouton [[Actualiser les cours]] pour forcer le téléchargement immédiat.

### Limite

Un titre absent de la base locale et jamais rencontré auparavant n'a pas de cours hors connexion : le logiciel le signale.

## Ce qui nécessite une connexion Internet
<!-- fiche: demarrage-internet-necessaire | questions: quand faut il internet ; qu'est-ce qui ne marche pas sans connexion ; pourquoi mon titre n'a pas de cours ; actualiser les cours ne marche pas ; la carte du monde est vide ; il faut internet pour installer ; titre inconnu hors ligne ; à quoi sert la connexion | mots: Internet, connexion requise, en ligne, Yahoo Finance, téléchargement des cours, carte du monde, fond de carte, mise à jour -->

La plupart des fonctions marchent hors connexion. Internet reste nécessaire dans les cas suivants.

| Situation | Pourquoi |
|---|---|
| Télécharger l'installateur ou une nouvelle version | Les fichiers sont sur la page des versions du projet |
| Obtenir les cours du jour | Ils viennent de Yahoo Finance |
| Analyser un titre absent de la base locale | Son historique doit être téléchargé une première fois (il est ensuite ajouté à la base) |
| Reconnaître, à l'import, un code ISIN ou un nom de société inconnus | La recherche se fait auprès de Yahoo Finance (le résultat est ensuite mémorisé) |
| Bouton [[Actualiser les cours]] | Il télécharge à nouveau les cours |
| Afficher la carte du monde si son fond de carte n'a jamais été enregistré | Les contours des pays sont téléchargés une fois, puis gardés sur l'ordinateur |
| Lancer le logiciel depuis le code source pour la première fois | Les bibliothèques Python doivent être installées |

### La base apprend au fil de l'eau

Chaque fois que le logiciel télécharge des cours ou reconnaît un titre, il les ajoute à sa base locale ou à sa mémoire. La fois suivante, ces informations sont disponibles même sans Internet.

### Si Yahoo Finance ne répond pas

Le logiciel ne plante pas : il utilise les derniers cours enregistrés et l'indique dans le bandeau (« Cours en cache (hors ligne) ») et en bas de la barre latérale. S'il n'a aucun cours pour un titre, un message clair le signale.

### Ce qui ne demande jamais Internet

La lecture de vos fichiers, les calculs, vos comptes chiffrés, le rapport PDF et l'assistant du manuel fonctionnent entièrement sur votre ordinateur.

## Mettre à jour le logiciel
<!-- fiche: demarrage-mettre-a-jour | questions: comment installer une nouvelle version ; mettre à jour portfolio tracker ; est-ce que je perds mes portefeuilles si je réinstalle ; faut il désinstaller avant ; mise a jour sur mac ; le logiciel se met il a jour tout seul ; nouvelle version disponible ; réinstaller par dessus | mots: mise à jour, update, nouvelle version, réinstaller, upgrade, conserver les comptes -->

Le logiciel ne se met pas à jour automatiquement. Pour passer à une nouvelle version, téléchargez-la sur la page des versions du projet et installez-la par-dessus l'ancienne. **Vos comptes et vos portefeuilles enregistrés sont conservés.** Inutile de désinstaller d'abord.

### Sous Windows

1. Fermez le logiciel (fermez la fenêtre noire).
2. Téléchargez le nouvel `Installer_Portfolio_Tracker.exe`.
3. Lancez-le et suivez les mêmes étapes que la première installation.

L'installateur remplace entièrement le Python embarqué et le code du logiciel. Le dossier des comptes (`data\comptes`) n'est jamais touché par une mise à jour.

### Sur Mac

1. Fermez le logiciel (fermez la fenêtre Terminal).
2. Ouvrez le nouveau `Portfolio_Tracker_Mac.dmg`.
3. Glissez « Portfolio Tracker » sur « Applications » et acceptez de remplacer l'ancienne application.

Au lancement suivant, l'application détecte la nouvelle version et remplace son code et sa base de titres, en conservant vos comptes et la mémoire des titres reconnus, rangés dans `~/Library/Application Support/Portfolio Tracker`. Il peut être nécessaire d'autoriser à nouveau l'application (voir la fiche « macOS refuse d'ouvrir l'application »).

### Précaution

Même si les mises à jour conservent les comptes, gardez une copie de vos portefeuilles importants : la page « Mon compte » permet de télécharger chacun d'eux en fichier CSV.

## Où sont enregistrées mes données ?
<!-- fiche: demarrage-ou-sont-donnees | questions: ou sont stockés mes portefeuilles ; dans quel dossier sont mes comptes ; ou se trouve le dossier data ; sauvegarder mes données ; changer d'ordinateur comment récupérer mes portefeuilles ; dossier application support mac ; appdata portfolio tracker ; ou est la base de titres | mots: dossier, emplacement, stockage, sauvegarde, AppData, Application Support, data, comptes, base de titres -->

### Sous Windows

Dans le dossier du programme :

`C:\Users\<votre nom>\AppData\Local\Programs\Portfolio Tracker\`

- `data\comptes\` : les comptes et les portefeuilles chiffrés de chaque utilisateur de cet ordinateur ;
- `data\base\` : la base locale de titres (cours) et la mémoire des titres reconnus.

Le dossier `AppData` est masqué par défaut dans l'Explorateur : tapez le chemin dans la barre d'adresse pour y accéder.

### Sur Mac

`~/Library/Application Support/Portfolio Tracker`

Dans le Finder, menu Aller, puis « Aller au dossier… », et collez ce chemin.

### Depuis le code source

Dans le dossier `data` du projet (`data/comptes` et `data/base`).

### Les fichiers sont chiffrés

Les portefeuilles et la liste de leurs noms sont chiffrés, et les dossiers des comptes ont des noms aléatoires. Les fichiers ne sont lisibles qu'à travers le logiciel, avec le bon mot de passe.

### Changer d'ordinateur ou faire une sauvegarde

La méthode la plus simple et la plus sûre : connectez-vous, ouvrez la page « Mon compte » et téléchargez chacun de vos portefeuilles en CSV. Sur le nouvel ordinateur, installez le logiciel, créez un compte et ajoutez ces fichiers. Copier directement le dossier des comptes d'un ordinateur à l'autre n'est pas une manipulation prévue par le logiciel.

## Désinstaller le logiciel
<!-- fiche: demarrage-desinstaller | questions: comment désinstaller portfolio tracker ; supprimer le logiciel de mon pc ; enlever l'application du mac ; est-ce que la désinstallation efface mes comptes ; supprimer aussi les comptes et les portefeuilles ; garder mes données en désinstallant ; desinstaller proprement ; effacer toutes mes données | mots: désinstallation, supprimer, uninstall, effacer, corbeille, comptes, suppression définitive -->

### Sous Windows

1. Ouvrez Paramètres Windows, puis Applications, et choisissez « Portfolio Tracker », puis Désinstaller. Vous pouvez aussi utiliser le raccourci de désinstallation du menu Démarrer.
2. À la fin, si des comptes existent, une question est posée : « Supprimer aussi les comptes et les portefeuilles enregistrés ? ».
   - **Non** (choix proposé par défaut) : les comptes et portefeuilles restent sur l'ordinateur et seront retrouvés si vous réinstallez Portfolio Tracker.
   - **Oui** : le dossier du logiciel est entièrement effacé, comptes compris. Cette suppression est définitive.

### Sur Mac

1. Mettez « Portfolio Tracker » (dans le dossier Applications) à la corbeille.
2. Pour effacer aussi les comptes et portefeuilles, supprimez le dossier `~/Library/Application Support/Portfolio Tracker` (Finder, menu Aller, puis « Aller au dossier… »).

Si vous ne supprimez que l'application, vos données restent sur le Mac et seront retrouvées après une réinstallation.

### Supprimer un seul compte sans désinstaller

Connectez-vous, ouvrez la page « Mon compte » et utilisez la rubrique « Supprimer mon compte » : le compte et tous ses portefeuilles sont effacés définitivement (droit à l'effacement), sans toucher aux autres utilisateurs.

### Avant de tout effacer

Téléchargez une copie de vos portefeuilles depuis la page « Mon compte » si vous pensez en avoir besoin un jour.

## La version en ligne et ses limites
<!-- fiche: demarrage-version-en-ligne | questions: y a t il une version en ligne ; utiliser le logiciel sans l'installer ; streamlit cloud ; mes comptes ont disparu sur le site ; version de démonstration ; je suis sur mac intel que faire ; est-ce que je peux l'utiliser sur tablette ou chromebook ; différence entre le site et l'application | mots: version en ligne, site web, Streamlit Cloud, démonstration, navigateur, sans installation, comptes temporaires -->

Le tableau de bord peut aussi être publié sur Streamlit Community Cloud, un service d'hébergement gratuit. L'adresse de cette version vous est communiquée par le créateur du logiciel ou par votre enseignant.

### Pour qui

- les utilisateurs de Mac Intel, pour qui l'application Mac n'est pas prévue ;
- ceux qui veulent découvrir le logiciel sans rien installer ;
- les utilisateurs d'un ordinateur sur lequel ils ne peuvent pas installer de programme.

### Ses limites

- **Les comptes sont temporaires.** Le disque du service en ligne est effacé à chaque redémarrage du site : les comptes et portefeuilles enregistrés peuvent disparaître. Un avertissement le rappelle dans le formulaire de connexion : « Version en ligne de démonstration ». Gardez toujours une copie de vos fichiers.
- **Internet est indispensable**, puisque le logiciel tourne sur un serveur distant.
- **Vos fichiers sont traités sur ce serveur**, et non sur votre ordinateur. Pour des données personnelles réelles, préférez l'application installée.
- Le site peut être plus lent, notamment s'il était en veille et doit redémarrer.

### Ce qui est identique

Les écrans, les calculs, le rapport PDF et le manuel sont les mêmes que dans la version installée.

## Lancer le logiciel depuis le code source
<!-- fiche: demarrage-code-source | questions: comment lancer avec python ; lancer_tableau_de_bord.bat ça sert à quoi ; streamlit run app.py ; je suis étudiant je veux lancer le projet dans vs code ; pip install requirements ; module not found streamlit ; installer les bibliothèques ; lancer sur linux | mots: code source, Python, Streamlit, VS Code, pip, requirements.txt, terminal, développeur, lancer_tableau_de_bord.bat -->

Cette méthode s'adresse aux étudiants et aux développeurs qui travaillent sur le projet lui-même. Elle demande Python sur l'ordinateur (le projet indique Python 3.11 ou plus récent).

### Sous Windows : le fichier lancer_tableau_de_bord.bat

Double-cliquez sur `lancer_tableau_de_bord.bat`, à la racine du projet.

- **La première fois**, il installe les bibliothèques nécessaires (fichier `requirements.txt`), puis la reconnaissance de caractères des PDF image (fichier `requirements-ocr.txt`). Internet est alors nécessaire. Il crée ensuite un petit fichier `.installe` pour ne plus refaire cette étape.
- Il lance ensuite le même lanceur que la version installée : le tableau de bord s'ouvre dans sa fenêtre, à l'adresse `http://localhost:8501` (ou le port suivant libre).
- Pour quitter, fermez la fenêtre noire.

### Dans un terminal (Windows, Mac, Linux)

Depuis le dossier du projet :

```
python -m pip install -r requirements.txt       (une seule fois)
python -m pip install -r requirements-ocr.txt   (facultatif : PDF image)
python -m streamlit run app.py                  (tableau de bord)
```

Le tableau de bord s'ouvre dans le navigateur, à l'adresse `http://localhost:8501`. Pour l'arrêter : Ctrl + C dans le terminal.

### Autres commandes utiles

- `python main.py` : analyse en ligne de commande et rapport PDF ;
- `python construire_base_titres.py --mise-a-jour` : ajoute les derniers cours à la base locale ;
- `python -m pytest` : lance les tests automatiques.

### En cas d'erreur « No module named streamlit »

Les bibliothèques ne sont pas installées pour le Python utilisé : relancez la commande d'installation `python -m pip install -r requirements.txt`.
