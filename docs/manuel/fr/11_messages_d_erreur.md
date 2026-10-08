# Messages d'erreur et problèmes
<!-- chapitre: erreurs | ordre: 11 -->

Ce chapitre recense les messages d'erreur et d'avertissement que le logiciel peut afficher, avec leur texte exact entre guillemets, leur cause et la marche à suivre. Il traite ensuite les problèmes qui surviennent sans message : logiciel qui ne s'ouvre pas, page blanche, port occupé, avertissements à l'installation, cours qui ne bougent pas, graphique vide, titre introuvable ou lenteur. Les points de suspension remplacent la partie variable d'un message (un nom de titre, une date, un nombre).

## « Aucun fichier de transactions : envoyez un fichier CSV depuis la barre latérale. »
<!-- fiche: erreur-aucun-fichier | questions: aucun fichier de transactions ; le tableau de bord est vide au lancement ; il n'y a aucun portefeuille dans la liste ; message envoyez un fichier csv ; je n'ai pas de portefeuille à analyser ; la liste des portefeuilles est vide ; rien ne s'affiche à part un message rouge | mots: aucun fichier, portefeuille absent, liste vide, envoi de fichier, portefeuilles d'exemple, données manquantes -->

### Cause

Aucun portefeuille n'est disponible : pas de fichier envoyé, aucun portefeuille enregistré dans votre espace, et aucun portefeuille d'exemple trouvé dans le dossier `data` du logiciel (fichiers `transactions*.csv`).

### Solution

1. Dans la barre latérale, rubrique « Données », utilisez [[Envoyer un fichier (CSV, Excel ou PDF)]] pour charger vos opérations.
2. Ou connectez-vous avec [[Se connecter]] : vos portefeuilles enregistrés apparaissent alors dans la liste.
3. Si vous n'avez pas encore de fichier, téléchargez le [[Modèle de fichier]], remplissez-le et envoyez-le.

Le logiciel est livré avec des portefeuilles d'exemple. Si la liste est vide, les fichiers `transactions*.csv` du dossier `data` ont peut-être été déplacés ou supprimés : réinstaller le logiciel les remet en place (vos comptes sont conservés).

L'espace « Manuel et aide » reste accessible même sans portefeuille.

## « Impossible d'analyser le portefeuille : … »
<!-- fiche: erreur-impossible-analyser | questions: impossible d'analyser le portefeuille ; message rouge impossible d'analyser ; mon portefeuille ne s'affiche pas ; erreur à l'analyse que faire ; le calcul des indicateurs plante ; analyse impossible après import ; que veut dire le texte après impossible d'analyser | mots: erreur d'analyse, échec, plantage, message rouge, diagnostic, assistant d'import, cours manquant, vente impossible -->

Ce message général précède toujours une explication plus précise : le portefeuille n'a pas pu être lu, valorisé ou calculé. Le logiciel préfère s'arrêter plutôt que d'afficher un résultat faux. Les onglets d'analyse ne s'affichent alors pas.

### Lisez la suite du message

| Suite du message | Fiche à consulter |
|---|---|
| « Vente impossible le … » | Vente impossible |
| « Cours manquant pour : … », « Historique de cours manquant pour : … » | Cours ou historique manquant |
| « Impossible de récupérer les cours : pas de connexion… » | Pas de connexion et aucun cache |
| « Taux de change introuvables : … » | Taux de change introuvables |
| « Impossible de récupérer l'historique de l'indice … » | Indice de référence indisponible |
| « Type(s) de transaction inconnu(s) : … » | Type d'opération inconnu |

### Que faire tout de suite ?

- Pour un fichier envoyé, le bouton [[Ouvrir l'assistant d'import]] apparaît sous le message : il permet de relire le fichier autrement (colonnes, tickers, devises).
- Pour ajouter une opération manquante, le bouton [[Ajouter des opérations]] reste disponible dans la barre latérale.
- Pour corriger une opération existante, l'onglet Transactions n'étant pas affiché, corrigez votre fichier, ou téléchargez le portefeuille depuis [[Mon compte]], corrigez-le dans un tableur et ajoutez-le de nouveau.
- Pour un problème de cours, connectez-vous à Internet et cliquez sur [[Actualiser les cours]].

## « Vente impossible le … : on vend … mais on n'en détient que … »
<!-- fiche: erreur-vente-impossible | questions: vente impossible on n'en détient que ; je vends plus que ce que j'ai ; message vente de mais seulement détenu à cette date ; vente à découvert refusée ; il manque un achat dans mon fichier ; erreur vente quantité ; mon relevé ne commence pas au début | mots: vente impossible, vente à découvert, quantité détenue, achat manquant, historique incomplet, contrôle bloquant | aller: Analyse du portefeuille/Transactions -->

Deux formulations existent :

- à l'analyse : « Vente impossible le … : on vend … mais on n'en détient que … » ;
- à l'ajout ou à la modification d'opérations : « Vente de … le …, mais seulement … détenu(s) à cette date. »

### Cause

Le logiciel rejoue les opérations par ordre de date. À la date indiquée, la vente porte sur plus de titres que vous n'en détenez. Causes fréquentes :

- un achat ancien manque, parce que le relevé ne couvre pas tout l'historique ;
- une quantité est mal saisie ou mal lue ;
- l'achat est daté après la vente (inversion jour et mois) ;
- une division d'actions n'a pas été traduite en quantité (voir le chapitre sur les sources) ;
- le même titre figure sous deux tickers différents.

### Solution

1. Ajoutez l'achat manquant avec [[Ajouter des opérations]] (bouton de la barre latérale, disponible même quand l'analyse échoue).
2. Pour corriger une quantité ou une date existante, corrigez le fichier d'origine (ou le portefeuille téléchargé depuis [[Mon compte]]), puis importez-le de nouveau.
3. Si vous venez de supprimer un achat dans l'onglet Transactions, supprimez aussi les ventes qui en dépendent : le logiciel le rappelle sous le message.
4. Le logiciel n'accepte pas la vente à découvert : il n'existe pas de position négative.

## « Cours manquant pour : … » ou « Historique de cours manquant pour : … »
<!-- fiche: erreur-cours-manquant | questions: cours manquant pour ; historique de cours manquant ; aucun cours disponible après la première transaction ; mon titre n'a pas de cours ; ticker mal écrit ; le logiciel ne trouve pas le prix de mon action ; titre radié pas de cours | mots: cours manquant, historique manquant, ticker inconnu, titre radié, Yahoo Finance, base locale, hors connexion -->

### Les messages

- « Cours manquant pour : … » : pas de dernier cours pour un titre encore détenu.
- « Historique de cours manquant pour : … » : pas d'historique pour un titre détenu à un moment donné, même vendu depuis.
- « Aucun cours disponible après la première transaction. » : aucun jour de cours postérieur à votre première opération.

### Causes

- ticker mal écrit ou inconnu de Yahoo Finance (`MC` au lieu de `MC.PA`, faute de frappe) ;
- titre retiré de la cote, ou fonds non coté ;
- pas d'Internet, et titre absent de la base locale et du cache ;
- pour le dernier message : opérations datées dans le futur, ou cours hors connexion qui s'arrêtent avant votre premier achat.

### Solution

1. Vérifiez le ticker sur le site de Yahoo Finance, puis corrigez-le : réimportez le fichier avec [[Ouvrir l'assistant d'import]] et la colonne [[Ticker Yahoo Finance]], ou corrigez votre fichier.
2. Connectez-vous à Internet et cliquez sur [[Actualiser les cours]] : le titre sera ensuite gardé dans la base locale.
3. Un titre sans aucun cours sur Yahoo Finance ne peut pas être suivi par le logiciel.

## « Impossible de récupérer les cours : pas de connexion à Yahoo Finance et aucun cache disponible. »
<!-- fiche: erreur-pas-de-connexion | questions: impossible de récupérer les cours ; pas de connexion à yahoo finance et aucun cache ; impossible de récupérer l'historique ; yahoo finance injoignable ; le logiciel ne marche pas sans internet ; erreur de connexion aux cours ; titres absents du cache et de la base locale | mots: connexion, Internet, Yahoo Finance injoignable, cache, base locale, hors connexion, proxy, pare-feu -->

Variante pour l'historique : « Impossible de récupérer l'historique : pas de connexion à Yahoo Finance et titres absents du cache et de la base locale. » Le message se termine par « Détail : » suivi de l'erreur technique.

### Cause

Yahoo Finance n'a pas répondu (pas d'Internet, réseau filtré, panne du service), et le logiciel n'a trouvé ces titres ni dans son cache ni dans sa base locale. Avec la base locale livrée, ce cas concerne surtout des titres qu'elle ne contient pas.

### Solution

1. Vérifiez votre connexion. Sur un réseau d'école ou d'entreprise, un pare-feu peut bloquer Yahoo Finance : essayez un autre réseau (partage de connexion du téléphone, par exemple).
2. Cliquez sur [[Actualiser les cours]].
3. Si Yahoo Finance est en panne, réessayez plus tard.

Une fois analysés avec Internet, les titres restent disponibles hors connexion.

### À ne pas confondre

Quand Yahoo Finance ne répond pas mais que le cache suffit, il n'y a **pas** d'erreur : le bandeau affiche simplement « Cours en cache (hors ligne) ».

## « Taux de change introuvables : … »
<!-- fiche: erreur-taux-de-change | questions: taux de change introuvables ; taux de change actuels introuvables ; aucun taux de change disponible pour ; mon action américaine bloque l'analyse ; erreur eurusd ; devise non convertie ; titre étranger hors connexion | mots: taux de change, devise, EURUSD, conversion, titre étranger, hors connexion, cache, base locale -->

Variantes : « Taux de change actuels introuvables. » et « Aucun taux de change disponible pour … ».

### Cause

Le portefeuille contient un titre coté dans une autre devise que l'euro, et le taux de change correspondant (par exemple `EURUSD=X`) n'a pu être obtenu ni de Yahoo Finance ni de la base locale. La base locale contient 12 devises ; une devise plus rare n'est disponible qu'avec Internet.

### Solution

1. Connectez-vous à Internet, puis cliquez sur [[Actualiser les cours]].
2. Vérifiez la devise du titre : hors connexion, elle est lue dans la base locale ou, à défaut, déduite du code (pas de suffixe = dollar américain). Un ticker mal écrit peut conduire à une devise inattendue.
3. Si une devise a été mal enregistrée, supprimer le fichier `data/cache_devises.csv` oblige le logiciel à la redemander à Yahoo Finance (Internet nécessaire).

## « Impossible de récupérer l'historique de l'indice … »
<!-- fiche: erreur-indice | questions: impossible de récupérer l'historique de l'indice ; historique introuvable pour la poche ; pas de cours communs pour l'indice composite ; mon indice de référence ne marche pas ; erreur avec l'indice 60 40 ; changer d'indice de référence pour débloquer | mots: indice de référence, benchmark, composite, poche, historique, indice mixte, hors connexion -->

Variantes : « historique introuvable pour la poche … de … » et « pas de cours communs pour l'indice composite ».

### Cause

Aucun des ETF qui représentent l'indice choisi n'a d'historique disponible (pas d'Internet et absent de la base), ou, pour un indice mixte, l'une de ses poches (actions ou obligations) est introuvable.

### Solution

1. Ouvrez [[Paramètres]], puis choisissez un autre [[Indice de référence]], par exemple le MSCI World proposé par défaut.
2. Connectez-vous à Internet et cliquez sur [[Actualiser les cours]].

L'indice sert surtout aux comparaisons (bêta, alpha, tracking error, graphique base 100) : en changer débloque l'analyse sans rien modifier à vos positions.

## « Type(s) de transaction inconnu(s) : … »
<!-- fiche: erreur-type-inconnu | questions: type de transaction inconnu ; les prix et les quantités doivent être positifs ; ma colonne type contient buy ; achat vente dividende seulement ; quantité négative refusée ; mon fichier contient des frais de garde ; type d'opération non reconnu | mots: type d'opération, ACHAT, VENTE, DIVIDENDE, quantité négative, prix négatif, format du projet -->

Message voisin : « Les prix et les quantités doivent être positifs. »

### Cause

Ces messages sont rares, car l'import convertit la plupart des libellés et ramène les quantités en positif. Un portefeuille ne peut contenir que trois types : `ACHAT`, `VENTE` et `DIVIDENDE`. Une autre valeur (« Frais », « Virement »…), ou un prix ou une quantité négatifs, arrêtent l'analyse.

### Solution

1. Corrigez la colonne `type` du fichier, ou supprimez les lignes qui ne sont pas des opérations sur titres.
2. Écrivez les quantités et les prix en positif : c'est le type qui indique le sens.
3. Pour un export de banque, envoyez plutôt le fichier tel quel : l'import automatique reconnaît de nombreux libellés (achat, buy, souscription, vente, sell, coupon…) et ignore les frais de garde ou les virements. En cas de doute, [[Ouvrir l'assistant d'import]] et vérifiez l'étape 3.

## « Colonne(s) manquante(s) ou non reconnue(s) : … »
<!-- fiche: erreur-colonnes | questions: colonne manquante ou non reconnue ; colonnes non reconnues ; colonnes reconnues mais sans certitude ; à indiquer pour le prix une colonne prix unitaire ou montant total ; pourquoi l'assistant d'import s'ouvre ; le logiciel ne comprend pas mon fichier ; colonne à indiquer | mots: colonnes, correspondance, en-tête, assistant d'import, champs obligatoires, prix unitaire, montant total -->

Plusieurs formulations, selon l'endroit :

- « Colonne(s) manquante(s) ou non reconnue(s) : … », suivi des colonnes lues et d'un rappel du format attendu ;
- « Colonne(s) non reconnue(s) : … » ou « Colonnes reconnues, mais sans certitude sur les quantités, prix et montants. », dans la rubrique [[Pourquoi l'assistant s'ouvre-t-il ?]] ;
- « À indiquer : … », dans l'assistant d'import, tant qu'un champ obligatoire n'est pas associé.

### Cause

Les champs obligatoires sont : la date, le titre (ticker, ISIN ou nom), la quantité, et un prix unitaire **ou** un montant total. Un nom de colonne inhabituel, une ligne de titres mal détectée ou des colonnes de nombres sans nom parlant empêchent la lecture automatique.

### Solution

1. Dans l'assistant, vérifiez la [[Ligne des titres de colonnes]] (et la [[Feuille Excel]] pour un classeur).
2. À l'étape 2, associez chaque champ à la bonne colonne. Les champs marqués d'un astérisque sont obligatoires.
3. Vérifiez le résultat à l'étape 4, puis cliquez sur [[Analyser ce portefeuille]].

## « … ligne(s) avec date illisible (lignes …) : ignorée(s) » et « Aucune transaction lue. »
<!-- fiche: erreur-lignes-ignorees | questions: lignes ignorées date illisible ; prix ou montant manquant ; quantité nulle ; titre manquant ; aucune transaction lue ; certaines lignes n'ont pas pu être lues ; pourquoi des lignes de mon fichier disparaissent | mots: lignes ignorées, date illisible, prix manquant, quantité nulle, titre manquant, numéros de lignes, aucune transaction -->

### Les quatre motifs

| Motif | Cause | Solution |
|---|---|---|
| date illisible | date vide, en toutes lettres ou abîmée | corriger la date (`15/01/2024` ou `2024-01-15`) |
| prix ou montant manquant | achat ou vente sans prix ni montant | compléter, ou associer la colonne du montant |
| quantité nulle | achat ou vente à 0 titre | vérifier la colonne de quantité |
| titre manquant | cellule vide, ou ISIN sans ticker | compléter, ou saisir le ticker à l'étape 3 |

Les lignes sont numérotées à partir de la première ligne de données ; au-delà de cinq, la liste se termine par « … ».

### Les messages associés

- « Certaines lignes n'ont pas pu être lues : … » : pour un fichier au format du projet, toute ligne en erreur empêche la lecture directe ; l'assistant s'ouvre.
- « Aucune transaction lue. » : toutes les lignes ont été ignorées. Vérifiez les types d'opération (étape 3) et la correspondance des colonnes (étape 2).
- « … ligne(s) ignorée(s) : opérations d'un autre type (frais de garde, virements...) » : ce n'est pas une erreur, ces lignes ne sont pas des opérations sur titres.

## « Fichier illisible : … » ou « Le fichier est vide. »
<!-- fiche: erreur-fichier-illisible | questions: fichier illisible ; le fichier est vide ; mon fichier excel ne s'ouvre pas ; format de fichier refusé ; fichier xls ancien format ; fichier csv corrompu ; le logiciel n'accepte pas mon fichier numbers | mots: fichier illisible, fichier vide, format, xlsx, csv, pdf, corrompu, feuille Excel -->

### Causes

- fichier vide, ou feuille Excel choisie qui ne contient rien ;
- fichier abîmé, ou enregistré dans un format non accepté : l'envoi accepte seulement `.csv`, `.xlsx` et `.pdf` (pas l'ancien `.xls`, ni `.ods` ou `.numbers`).

### Solution

1. Ouvrez le fichier dans votre tableur pour vérifier qu'il contient bien les opérations.
2. Réenregistrez-le au format `.xlsx` ou CSV.
3. Pour un classeur à plusieurs feuilles, choisissez la bonne [[Feuille Excel]] dans l'assistant (le logiciel propose d'office la feuille la plus remplie).

## « Titre(s) introuvable(s) : … »
<!-- fiche: erreur-titre-introuvable | questions: titre introuvable ; titres introuvables à l'import ; indiquez son ticker yahoo finance ; le logiciel ne trouve pas mon action ; mon isin n'est pas reconnu ; statut introuvable ; indiquez le titre | mots: titre introuvable, ISIN, ticker, recherche, Yahoo Finance, saisie manuelle, hors connexion -->

Formulations :

- à l'import : « Titre(s) introuvable(s) : … », suivi des codes concernés ; l'assistant s'ouvre avec le statut « introuvable » à l'étape 3 ;
- à la saisie manuelle : « Titre introuvable : … Indiquez son ticker Yahoo Finance (ex. MC.PA). » ;
- champ vide à la saisie : « Indiquez le titre. ».

### Solution

1. Cherchez le titre sur le site de Yahoo Finance et notez son ticker (`AI.PA` pour Air Liquide).
2. Saisissez-le dans la colonne [[Ticker Yahoo Finance]] de l'assistant, ou directement dans le champ « Titre » de la [[Saisie manuelle]].
3. Sans ticker, les lignes concernées sont ignorées.

Les causes possibles sont détaillées dans la fiche « Un titre est introuvable : les causes possibles ».

## Messages sur les PDF : scan, texte codé, mot de passe, opération non reconnue
<!-- fiche: erreur-pdf | questions: pdf scanné impossible à lire automatiquement ; aucune opération n'a été reconnue dans mon pdf image ; opération non reconnue automatiquement dans ce pdf ; le texte de ce pdf est codé ; mon avis d'opéré n'est pas lu ; pdf refusé ; pdf imprimé en pdf ne marche pas ; reconnaissance de caractères échoue ; pdf protégé par un mot de passe saisissez-le ; mot de passe incorrect pour ouvrir le pdf | mots: PDF, scan, image, OCR, texte codé, avis d'opéré, relevé, opération non reconnue, Format PDF, formulaire, saisie manuelle, PDF protégé, mot de passe du PDF -->

### Les messages de lecture

| Message | Cause |
|---|---|
| « Opération non reconnue automatiquement dans ce PDF : complétez-la dans le formulaire « Compléter l'opération » (les valeurs trouvées sont proposées). » | PDF texte lisible, mais ni tableau d'opérations, ni avis d'opéré lu avec certitude (par ses intitulés ou par son contenu) |
| « Le texte de ce PDF est « codé » (il s'affiche correctement mais ne peut pas être extrait) et aucun moteur de reconnaissance de caractères n'est installé. Complétez l'opération dans le formulaire, ou installez la reconnaissance de caractères (requirements-ocr.txt). » | Texte qui s'extrait en signes incompréhensibles, sans moteur de reconnaissance de caractères |
| « PDF scanné (image) : impossible à lire automatiquement… » | PDF sans texte et aucun moteur de reconnaissance de caractères installé |
| « PDF image (scan, photo ou page imprimée avec « Imprimer en PDF ») : le texte a été lu par reconnaissance de caractères, mais aucune opération n'a été reconnue… » | Image (ou texte codé) lue, mais aucune opération sûre trouvée |

Un PDF est traité comme une image quand il contient moins de 20 caractères de texte ; un texte « codé » est traité de la même façon.

### Les messages de mot de passe

| Message | Cause | Solution |
|---|---|---|
| « PDF protégé par un mot de passe : saisissez-le pour l'ouvrir (souvent indiqué dans le courriel de la banque : date de naissance, identifiant client…). Il n'est pas enregistré. » | La banque a chiffré le PDF : il ne s'ouvre pas sans mot de passe | Tapez le mot de passe dans [[Mot de passe du PDF]], puis cliquez sur [[Ouvrir le PDF]] (encadré [[PDF protégé]]) |
| « Mot de passe incorrect. » | Le mot de passe saisi n'ouvre pas le document | Vérifiez-le dans le courriel ou le règlement de votre banque (souvent une date de naissance ou un identifiant client) et réessayez |

Le mot de passe n'est conservé nulle part ; la copie déchiffrée du PDF reste en mémoire le temps de la session. Dans « Mon compte », rubrique « Ajouter un portefeuille », aucun mot de passe n'est demandé : envoyez le PDF depuis la barre latérale (voir le chapitre sur l'import, fiche « Mon PDF est protégé par un mot de passe »).

### Les points à vérifier dans le résumé

Après la lecture d'un PDF, le résumé de la barre latérale peut contenir des messages qui ne bloquent rien mais demandent une vérification : « … le montant écrit (…) ne correspond pas à quantité × cours ± frais (…) : vérifiez la quantité et le cours. », « … opération datée d'un samedi (…), jour sans bourse : vérifiez la date d'exécution. », « … frais de … pour un montant de … (plus de 3 %) : vérifiez les frais. », « … la même opération apparaît deux fois (…) : avis envoyé en double ? ». Il peut aussi indiquer qu'un cours lu a été remplacé par la lecture qui correspond au cours de clôture du jour. Voir le chapitre sur l'import, fiches « Les contrôles après la lecture d'un PDF » et « Vérification du cours lu avec le cours du marché ».

### Ce qui s'affiche

Ces messages ne bloquent plus l'import d'un PDF : ils apparaissent en tête du formulaire [[Compléter l'opération]], qui propose la date, le code ISIN et les nombres trouvés dans le document. Vérifiez-les, corrigez au besoin, puis cliquez sur [[Ajouter cette opération]] (voir le chapitre sur l'import, fiche « Compléter une opération quand le PDF n'est pas reconnu »).

### Solution, de la plus sûre à la moins sûre

1. Téléchargez le vrai PDF depuis votre espace bancaire (bouton « Format PDF » ou « Télécharger », pas « Imprimer »).
2. Exportez les opérations en Excel ou CSV.
3. Complétez l'opération dans le formulaire proposé, ou saisissez-la à la main : [[Ajouter des opérations]], onglet [[Saisie manuelle]].
4. Pour un scan ou un texte codé, installez la reconnaissance de caractères depuis le code source : `python -m pip install -r requirements-ocr.txt`.
5. Depuis le code source, `python diagnostic_pdf.py` montre ce que le logiciel a lu ; avec `--anonyme`, le rapport ne contient ni nom, ni adresse, ni numéro de compte. Dans le formulaire, [[Préparer un rapport anonymisé]] produit le même type de rapport (voir le chapitre sur l'import).

## « Pour lire un PDF, installer pdfplumber… » et autres bibliothèques manquantes
<!-- fiche: erreur-bibliotheques | questions: installer pdfplumber ; installer openpyxl ; installer reportlab ; no module named ; bibliothèque manquante ; le rapport pdf ne se génère pas installer reportlab ; module not found streamlit | mots: bibliothèque, module, pip install, pdfplumber, openpyxl, reportlab, code source, requirements -->

### Les messages

- « Pour lire un PDF, installer pdfplumber : python -m pip install pdfplumber »
- « Pour lire un fichier Excel (.xlsx), installer openpyxl : python -m pip install openpyxl. Ou l'enregistrer au format CSV. »
- « Installer reportlab : python -m pip install reportlab » (au clic sur [[Rapport PDF]])

### Cause

Ces messages ne concernent que le lancement **depuis le code source** : une bibliothèque Python manque. Les installateurs Windows et Mac contiennent déjà toutes les bibliothèques.

### Solution

Depuis le dossier du projet, installez tout d'un coup :

```
python -m pip install -r requirements.txt
```

Puis relancez le tableau de bord. Pour lire les PDF image, ajoutez `python -m pip install -r requirements-ocr.txt` (facultatif).

## « … prix éloigné(s) du cours du jour … » et « Prix non vérifiés… »
<!-- fiche: erreur-prix-eloigne | questions: prix éloigné du cours du jour ; ticker devise ou division d'actions à vérifier ; prix non vérifiés avec les cours du marché ; écart médian ça veut dire quoi ; mon prix d'achat ne correspond pas ; alerte sur le prix à l'import | mots: contrôle des prix, écart médian, 25 %, devise, division d'actions, mauvais ticker, pas de connexion -->

### Les messages

- « … : … prix éloigné(s) du cours du jour (écart médian …) — ticker, devise ou division d'actions à vérifier. »
- « Prix non vérifiés avec les cours du marché (pas de connexion). »

Ils s'affichent dans le résumé de l'import (barre latérale) ou à l'étape 4 de l'assistant. Ce sont des avertissements : l'import n'est pas bloqué.

### Cause du premier

Avec Internet, chaque prix d'achat et de vente est comparé au cours de clôture du même jour. Un prix plus de 25 % au-dessus (ou 20 % en dessous) est signalé. Causes : mauvais ticker (autre société, autre place), devise ou pence mal interprétés, division d'actions, faute de frappe.

### Solution

1. Vérifiez le ticker retenu ; corrigez-le dans [[Ticker Yahoo Finance]].
2. À l'étape 4, essayez un autre choix de [[Devise des prix du fichier]].
3. Pour une division d'actions, exprimez l'opération en titres d'après la division.

Le second message signifie seulement que le contrôle n'a pas pu avoir lieu : vérifiez vous-même les titres étrangers.

## « Opération datée dans le futur » et autres contrôles bloquants
<!-- fiche: erreur-controles-bloquants | questions: opération datée dans le futur ; quantité ou prix nul pour ; le portefeuille ne peut pas être vide ; ces titres ne sont plus détenus ; le bouton enregistrer est grisé ; je ne peux pas enregistrer mes modifications ; contrôle bloquant | mots: contrôle, bloquant, date future, quantité nulle, prix nul, portefeuille vide, enregistrement impossible | aller: Analyse du portefeuille/Transactions -->

Ces messages apparaissent sur la page [[Ajouter des opérations]] ou dans l'onglet Transactions, pendant une modification.

| Message | Cause | Solution |
|---|---|---|
| « Opération datée dans le futur : …, le … » | date postérieure à aujourd'hui | corriger la date (souvent une inversion jour et mois) |
| « Quantité ou prix nul pour …, le … » | achat ou vente à 0 titre ou à 0 € | corriger la quantité ou le prix |
| « Vente de … le …, mais seulement … détenu(s) à cette date. » | vente supérieure à la quantité détenue | voir la fiche « Vente impossible » |
| « Le portefeuille ne peut pas être vide : gardez au moins une opération. » | toutes les opérations sont cochées « Supprimer » | décocher au moins une ligne |

Tant qu'un de ces messages est affiché, le bouton [[Enregistrer les opérations]] (page d'ajout) ou [[Enregistrer les modifications]] (onglet Transactions) reste grisé ; dans l'onglet Transactions, la case [[Je confirme ces modifications]] est aussi inactive.

### Un simple avertissement

« Après cette modification, ces titres ne sont plus détenus : … » n'empêche pas d'enregistrer : il vous signale qu'une ligne disparaît du portefeuille. Vérifiez que c'est voulu.

## Un fichier refusé à l'ajout d'opérations ou dans « Mon compte »
<!-- fiche: erreur-ajout-fichier | questions: ce fichier n'a pas pu être lu automatiquement ; mon fichier est refusé dans ajouter des opérations ; impossible d'ajouter un portefeuille dans mon compte ; message rouge avec le nom de mon fichier ; pour un format inhabituel envoyez le fichier depuis la barre latérale ; format inhabituel | mots: ajout d'opérations, Mon compte, fichier refusé, lecture automatique, assistant d'import, format inhabituel -->

### Les messages

- Sur la page [[Ajouter des opérations]] : le nom du fichier suivi de la raison (par exemple « export.csv : Colonne(s) non reconnue(s) : … »). Un PDF n'est pas refusé de cette façon : le formulaire [[Compléter l'opération]] s'ouvre à la place, avec la raison en tête (par exemple « Opération non reconnue automatiquement dans ce PDF… »).
- Dans [[Mon compte]], rubrique « Ajouter un portefeuille » : « Ce fichier n'a pas pu être lu automatiquement. Envoyez-le depuis la barre latérale… ».

### Cause

Ces deux pages n'utilisent que la lecture **automatique**. Elles n'ouvrent pas l'assistant d'import : un fichier au format inhabituel, avec des colonnes ambiguës ou des titres introuvables, y est refusé.

### Solution

1. Envoyez le fichier depuis la barre latérale, avec [[Envoyer un fichier (CSV, Excel ou PDF)]] : l'assistant d'import vous guidera.
2. Une fois le fichier lu, enregistrez-le avec le bouton « Enregistrer dans mon espace » qui apparaît sous l'envoi.
3. Pour quelques opérations seulement, utilisez la [[Saisie manuelle]].

## « Identifiant ou mot de passe incorrect. » et « Trop d'essais ratés… »
<!-- fiche: erreur-connexion | questions: identifiant ou mot de passe incorrect ; trop d'essais ratés réessayez dans ; je n'arrive pas à me connecter ; compte bloqué une minute ; mon identifiant n'est pas reconnu ; mot de passe refusé alors qu'il est bon ; connexion impossible | mots: connexion, identifiant, mot de passe, blocage, essais ratés, compte, sécurité -->

### « Identifiant ou mot de passe incorrect. »

Le même message s'affiche pour un identifiant inconnu et pour un mauvais mot de passe : le logiciel ne révèle pas quels comptes existent. Vérifiez :

- l'identifiant (les majuscules sont converties en minuscules, les espaces autour sont retirés) ;
- le mot de passe, qui distingue majuscules et minuscules (touche Verr. Maj.) ;
- que vous êtes sur le bon ordinateur et la bonne session : les comptes sont propres à chaque installation.

### « Trop d'essais ratés : réessayez dans … secondes. »

Après 5 essais ratés, le compte est bloqué une minute. Attendez le délai indiqué.

### Mot de passe oublié

Il n'existe aucun moyen de le récupérer : les portefeuilles sont chiffrés avec lui. Créez un nouveau compte et réimportez vos fichiers (voir le chapitre sur le compte).

## Messages à la création du compte ou au changement de mot de passe
<!-- fiche: erreur-creation-compte | questions: identifiant invalide ; le mot de passe doit contenir au moins 8 caractères ; les deux mots de passe ne sont pas identiques ; cet identifiant est déjà utilisé ; mot de passe actuel incorrect ; impossible de créer mon compte ; quels caractères pour l'identifiant | mots: création de compte, identifiant invalide, mot de passe trop court, confirmation, identifiant déjà utilisé, changer de mot de passe -->

| Message | Cause | Solution |
|---|---|---|
| « Identifiant invalide : 3 à 30 caractères parmi lettres minuscules, chiffres, « . », « _ » et « - ». » | espace, accent ou caractère spécial, ou longueur hors limites | choisir par exemple `marie.dupont` |
| « Le mot de passe doit contenir au moins 8 caractères. » | mot de passe trop court | allonger le mot de passe |
| « Les deux mots de passe ne sont pas identiques. » | faute de frappe dans la confirmation | ressaisir les deux champs |
| « Cet identifiant est déjà utilisé. » | compte existant sur cet ordinateur | choisir un autre identifiant, ou se connecter |
| « Mot de passe actuel incorrect. » | erreur sur l'ancien mot de passe, dans [[Mon compte]] | ressaisir l'ancien mot de passe |
| « Mot de passe incorrect. » | erreur lors de la suppression du compte | ressaisir le mot de passe |

### Autres messages du compte

- « Déconnexion automatique après 30 minutes d'inactivité. » : reconnectez-vous ; vos portefeuilles enregistrés ne sont pas perdus.
- « Portefeuille introuvable. » ou « Aucun ajout à annuler. » : le portefeuille a été supprimé, ou il n'y a pas de version précédente. Rechargez la page.

## « L'optimisation compare plusieurs répartitions… » et « Optimisation impossible : … »
<!-- fiche: erreur-optimisation | questions: optimisation impossible ; l'optimisation n'a pas convergé ; il faut au moins 2 titres dans le portefeuille ; pourquoi l'onglet optimisation est vide ; frontière efficiente absente ; poids maximal impossible ; l'optimisation ne marche pas avec mon portefeuille | mots: optimisation, Markowitz, convergence, frontière efficiente, poids maximal, nombre de titres | aller: Analyse du portefeuille/Optimisation -->

### « L'optimisation compare plusieurs répartitions entre titres : il faut au moins 2 titres dans le portefeuille. »

Avec une seule ligne, il n'y a rien à répartir. Ajoutez des titres pour utiliser l'onglet.

### « Optimisation impossible : … »

Le message est suivi de la cause, le plus souvent « L'optimisation n'a pas convergé : … » : l'optimiseur n'a pas trouvé de solution respectant les contraintes. Causes fréquentes : un titre à l'historique très court (les calculs ne portent que sur les jours où tous les titres ont un cours), des titres presque identiques, ou des contraintes très serrées.

### Solution

1. Changez le [[Poids maximal par titre]] (seules les valeurs qui permettent d'investir 100 % sont proposées).
2. Attendez que les titres récents aient plus d'historique, ou analysez le portefeuille sans eux.

### Frontière « approchée »

Si l'optimiseur ne trouve aucun point exact de la frontière, le logiciel la remplace par l'enveloppe de 4 000 portefeuilles tirés au hasard : ce n'est pas une erreur.

## « Stress tests indisponibles : … », « Attribution indisponible : … »
<!-- fiche: erreur-espaces-indisponibles | questions: stress tests indisponibles ; attribution indisponible ; budget de risque indisponible ; backtest indisponible ; historique trop court il faut au moins deux fins de mois ; aucune action dans le portefeuille ; l'onglet conseil patrimonial affiche une erreur | mots: stress tests, attribution, budget de risque, backtest, indisponible, historique trop court, Internet, indices régionaux -->

Ces avertissements jaunes concernent les espaces « Conseil patrimonial » et « Gestion d'actifs ». Le reste du logiciel fonctionne normalement.

| Message | Causes fréquentes | Solution |
|---|---|---|
| « Stress tests indisponibles : … » | historique depuis 2008 impossible à obtenir (pas d'Internet, cache absent) | se connecter, puis [[Actualiser les cours]] |
| « Attribution indisponible : … » | « Historique trop court : il faut au moins deux fins de mois. » ; « aucune action dans le portefeuille… » ; indices régionaux non téléchargés | attendre un mois complet d'historique ; l'attribution ne porte que sur la poche actions |
| « Budget de risque indisponible : … » | calcul impossible ; la suite du message en donne la raison | vérifier l'historique des titres récents |
| « Backtest indisponible : … » | pas assez de jours où tous les titres ont un cours | idem |

Le rapport PDF calcule ces analyses séparément : si l'une échoue, les autres y figurent quand même.

## « n.d. » à la place d'un chiffre
<!-- fiche: erreur-nd | questions: pourquoi n.d. ; cornish fisher n.d. ; tri n.d. ; un indicateur affiche n.d. ; chiffre non disponible ; valeur manquante dans le tableau ; nan dans les indicateurs | mots: n.d., non disponible, NaN, Cornish-Fisher, TRI, indicateur manquant | aller: Analyse du portefeuille/Risque -->

« n.d. » signifie « non disponible » : le calcul n'a pas de sens ou n'a pas abouti. Ce n'est pas un plantage.

### Les cas courants

- **VaR Cornish-Fisher** : la mention « Cornish-Fisher n.d. : asymétrie ou kurtosis trop fortes, la correction n'est plus fiable. » apparaît sous le tableau. La formule ne conserve plus l'ordre des pertes : utilisez la VaR historique et la CVaR.
- **TRI** : aucun taux entre −99 % et +1 000 % par an n'annule les flux (cas extrêmes, ou historique très court).
- **TWR annualisé** : premier et dernier jour confondus.
- **Indicateurs de forme** (asymétrie, kurtosis) : moins de 4 jours d'historique ; ils valent alors 0 par convention.

Le plus souvent, ces indicateurs deviennent disponibles avec un historique plus long (voir le chapitre « Toutes les formules »).

## L'assistant répond « Je n'ai pas trouvé de réponse sûre dans le manuel. »
<!-- fiche: erreur-assistant | questions: je n'ai pas trouvé de réponse sûre dans le manuel ; l'assistant ne trouve pas ; l'aide ne répond pas à ma question ; le manuel est introuvable ; l'assistant ne comprend pas ; aucune réponse dans le manuel | mots: assistant, aide, recherche, sans réponse, manuel, questions, journal | aller: Manuel et aide -->

### Cause

L'assistant ne rédige rien : il cherche la fiche du manuel la plus proche de votre question. Si aucune ne correspond assez, il le dit plutôt que de répondre à côté, et propose les « Fiches les plus proches ».

### Solution

1. Reformulez avec d'autres mots : plus simples (« enlever un achat ») ou plus techniques (« supprimer une transaction »).
2. Utilisez le nom exact d'un indicateur ou d'un bouton (« VaR », « PRU », « Actualiser les cours »).
3. Parcourez le [[Sommaire du manuel]], par chapitre.
4. Votre question est notée sur cet ordinateur ; vous pouvez l'envoyer au créateur avec [[Exporter les questions (CSV)]] pour compléter le manuel.

### « Le manuel est introuvable (dossier docs/manuel). »

Les fichiers du manuel manquent dans le dossier du logiciel : réinstallez-le.

## Le logiciel ne s'ouvre pas
<!-- fiche: erreur-ne-souvre-pas | questions: le logiciel ne s'ouvre pas ; rien ne se passe quand je clique sur l'icône ; le tableau de bord n'a pas pu démarrer ; la fenêtre noire se ferme tout de suite ; l'application ne se lance pas ; double clic sans effet ; portfolio tracker ne démarre plus | mots: démarrage, lancement, fenêtre noire, Terminal, lanceur, ne démarre pas, erreur au démarrage -->

### Rien ne se passe

1. Attendez quelques secondes : le premier démarrage est plus long (voir la fiche sur la lenteur).
2. Regardez la barre des tâches (Windows) ou le Dock (Mac) : la fenêtre noire ou le Terminal est peut-être caché derrière une autre fenêtre.
3. Sur Mac, au premier lancement, macOS bloque l'application : voir la fiche « Avertissements à l'installation ».

### La fenêtre noire affiche « Le tableau de bord n'a pas pu démarrer (voir le message ci-dessus). »

Le serveur s'est arrêté. Le message technique au-dessus en donne la raison. Appuyez sur Entrée pour fermer, relancez, et si l'erreur persiste, photographiez le message et transmettez-le à votre enseignant ou au créateur du logiciel. Vous pouvez aussi réinstaller la dernière version : vos comptes sont conservés.

### La fenêtre noire est ouverte, mais pas le tableau de bord

Le lanceur attend jusqu'à trois minutes que le tableau de bord soit prêt. Passé ce délai, ouvrez vous-même votre navigateur à l'adresse indiquée dans la fenêtre noire, par exemple `http://localhost:8501`.

### Le logiciel était déjà ouvert

Un nouveau clic sur l'icône ne le relance pas : il rouvre la fenêtre du tableau de bord (« Portfolio Tracker est déjà ouvert : ouverture de la fenêtre... »).

## La page reste blanche ou indique une erreur de connexion
<!-- fiche: erreur-page-blanche | questions: page blanche ; la fenêtre reste blanche ; impossible de se connecter à localhost ; ce site est inaccessible localhost ; le tableau de bord ne charge pas ; écran gris ; connection refused | mots: page blanche, localhost, connexion refusée, rechargement, fenêtre noire, serveur arrêté, navigateur -->

### Causes et solutions

1. **La fenêtre noire (ou le Terminal) a été fermée** : le logiciel est arrêté, la page ne peut plus se charger. Relancez-le avec l'icône « Portfolio Tracker ».
2. **Le tableau de bord démarre encore** : patientez, puis rechargez la page (touche F5 ou Ctrl + R ; Cmd + R sur Mac).
3. **Mauvais numéro de port** : l'adresse doit être celle affichée dans la fenêtre noire (8501, ou un numéro suivant jusqu'à 8510).
4. **Un calcul long est en cours** : un message d'attente s'affiche alors en haut de la page (« Récupération des cours et calcul des indicateurs... », par exemple). Laissez-le se terminer.

### Si rien n'y fait

Fermez la fenêtre noire, puis relancez le logiciel, au besoin après avoir redémarré l'ordinateur. Le tableau de bord n'a besoin d'aucune connexion Internet pour s'afficher : `localhost` désigne votre propre ordinateur.

## « Aucun port libre entre 8501 et 8510 » : le port est occupé
<!-- fiche: erreur-port-occupe | questions: aucun port libre entre 8501 et 8510 ; port occupé ; port 8501 déjà utilisé ; fermez une autre application puis réessayez ; address already in use ; conflit de port streamlit ; deux applications streamlit | mots: port, 8501, 8510, localhost, port occupé, Streamlit, conflit, lanceur -->

### Comment le logiciel choisit son port

Au lancement, il passe en revue les ports 8501 à 8510 :

- si le tableau de bord tourne déjà sur l'un d'eux, il rouvre simplement sa fenêtre ;
- sinon, il démarre sur le premier port libre.

### Le message

« Aucun port libre entre 8501 et 8510 : fermez une autre application puis réessayez. », suivi de « Appuyez sur Entrée pour fermer. ». Les dix ports sont occupés par d'autres programmes, souvent d'autres applications Streamlit, ou d'anciennes fenêtres du logiciel restées ouvertes.

### Solution

1. Fermez les autres fenêtres noires ou Terminal (anciens lancements, autres projets Streamlit).
2. Relancez Portfolio Tracker.
3. Si le problème persiste, redémarrez l'ordinateur.

## Avertissements de Windows ou de macOS à l'installation
<!-- fiche: erreur-avertissement-installation | questions: windows a protégé votre ordinateur ; éditeur inconnu ; le développeur ne peut pas être vérifié ; antivirus bloque portfolio tracker ; edge bloque le téléchargement ; macos refuse d'ouvrir l'application ; est-ce un virus | mots: SmartScreen, Gatekeeper, éditeur inconnu, avertissement, antivirus, signature, installation, sécurité -->

L'installateur Windows et l'application Mac ne sont pas signés par un certificat d'éditeur payant ni distribués par l'App Store. Les avertissements sont donc normaux.

### Windows

- **Edge** peut bloquer le téléchargement : dans la liste des téléchargements, menu « … », choisissez de conserver le fichier.
- **« Windows a protégé votre ordinateur »** (SmartScreen) : cliquez sur « Informations complémentaires », puis sur « Exécuter quand même ».
- **Antivirus** : si le fichier vient de la page officielle des versions, vous pouvez l'autoriser.

### Mac

- **macOS 15 et plus récent** : au message de blocage, cliquez sur « Terminé », ouvrez Réglages Système, Confidentialité et sécurité, puis « Ouvrir quand même ».
- **macOS 12 à 14** : clic droit sur l'application, « Ouvrir », puis « Ouvrir ».
- L'application exige un Mac Apple Silicon (M1 et suivants) : sur un Mac Intel, utilisez la version en ligne.

Téléchargez uniquement depuis `https://github.com/DieuUssop/Python/releases/latest` ou le lien de votre enseignant. Le détail figure au chapitre « Prise en main ».

## Les cours ne se mettent pas à jour
<!-- fiche: erreur-cours-pas-a-jour | questions: les cours ne se mettent pas à jour ; les cours sont les mêmes qu'il y a une heure ; pourquoi les cours datent d'hier ; cours en cache hors ligne ; actualiser les cours ne change rien ; le cours n'est pas celui de maintenant ; les prix sont figés | mots: mise à jour des cours, cache, actualiser, une heure, hors ligne, données au, dernier cours, week-end -->

### Vérifiez d'abord la source

- Bandeau : « Cours en direct · Yahoo Finance » (point vert) ou « Cours en cache (hors ligne) » (point orange).
- « Données au » : la date du dernier cours de l'historique.
- Barre latérale, ligne « Cours » : « Yahoo Finance (en direct) », ou « cache local du » suivi d'une date.

### Les causes

1. **La mémoire d'une heure** : tant que le portefeuille et les réglages ne changent pas, les résultats sont gardés une heure et les cours ne sont pas redemandés. Cliquez sur [[Actualiser les cours]].
2. **Pas d'Internet, ou Yahoo Finance injoignable** : le logiciel utilise son cache et sa base locale. Reconnectez-vous, puis actualisez.
3. **Bourse fermée** : le week-end ou un jour férié, le dernier cours est celui de la dernière séance. C'est normal.
4. **Titre suspendu ou radié** : il garde son dernier cours connu, sans alerte.

### Ce que le logiciel utilise

Le cours de clôture (ou une valeur de la séance en cours si la bourse est ouverte), jamais un flux en temps réel.

## Un graphique est vide ou absent
<!-- fiche: erreur-graphique-vide | questions: le graphique est vide ; la carte du monde ne s'affiche pas ; pas de graphique de corrélations ; au moins deux lignes sont nécessaires ; pas de poche actions à analyser ; le graphique des anneaux a disparu ; le graphique ne s'affiche pas | mots: graphique vide, carte du monde, corrélations, anneaux, poche actions, obligations, affichage -->

### Les cas prévus par le logiciel

| Ce que vous voyez | Cause |
|---|---|
| Carte du monde vide | fond de carte jamais enregistré et pas d'Internet |
| Carte du monde absente | aucune action avec un pays connu (portefeuille 100 % obligataire, or ou monétaire) |
| Anneau par région ou par secteur absent | un seul groupe : l'anneau n'est dessiné qu'à partir de deux groupes |
| « Au moins deux lignes sont nécessaires. » | corrélations avec une seule ligne |
| « Pas de poche actions à analyser. » | régions et secteurs sans action |
| « Le portefeuille ne contient pas d'obligations. » | sensibilité aux taux sans obligation |
| Onglet Optimisation sans graphique | moins de 2 titres, ou optimisation impossible |

### Autres causes

- **Un clic dans la légende** masque une courbe : cliquez de nouveau sur son nom pour la réafficher.
- **Un zoom** trop serré : double-cliquez dans le graphique pour revenir à la vue d'ensemble.
- **Historique très court** : avec quelques jours seulement, les courbes et histogrammes sont presque vides.

## Un titre est introuvable : les causes possibles
<!-- fiche: erreur-titre-introuvable-causes | questions: pourquoi mon titre est introuvable ; mon fonds n'existe pas sur yahoo ; mon action n'a pas de ticker ; fonds en euros assurance vie introuvable ; sicav introuvable ; le logiciel ne connaît pas ce titre ; comment trouver le ticker yahoo | mots: titre introuvable, ticker, ISIN, fonds non coté, OPCVM, fonds en euros, Yahoo Finance, place de cotation -->

Le logiciel ne connaît que les titres qui ont un **ticker Yahoo Finance** avec des cours quotidiens.

### Les causes, par ordre de fréquence

1. **Pas d'Internet** : seuls les 31 ETF de la table intégrée, la mémoire des titres reconnus et la base locale sont consultés.
2. **Libellé abrégé** : « AM.C.C.40 UC.ETF C » ne donne rien ; c'est l'ISIN qui permet la reconnaissance.
3. **Ticker sans place** (`MC`, `AIR`) : le logiciel cherche la cotation dont le cours colle à vos prix (écart médian inférieur à 15 %) ; à défaut, il interroge le moteur de recherche, qui peut ne rien trouver.
4. **Produit non coté** : fonds en euros d'assurance-vie, certains OPCVM, produits structurés, obligations sans cotation sur Yahoo Finance. Ils ne peuvent pas être suivis.
5. **Titre radié ou fusionné** : Yahoo Finance n'a parfois plus son historique.

### Trouver le bon ticker

Sur le site de Yahoo Finance, cherchez le nom ou l'ISIN, puis notez le code complet avec sa place : `.PA` (Paris), `.DE` (Francfort), `.AS` (Amsterdam), `.L` (Londres), rien pour les États-Unis. Saisissez-le dans [[Ticker Yahoo Finance]] (assistant d'import) ou dans la [[Saisie manuelle]].

## Le logiciel est lent, surtout au premier lancement
<!-- fiche: erreur-lenteur | questions: le logiciel est lent ; premier lancement très long ; ça charge longtemps ; les stress tests mettent du temps ; pourquoi le calcul est long ; le pdf met longtemps à être lu ; le site en ligne est lent | mots: lenteur, chargement, premier lancement, attente, téléchargement, cache, performances, spinner -->

### Au premier lancement

- **Sur Mac**, au premier lancement d'une nouvelle version, l'application copie son code et sa base de titres dans `~/Library/Application Support/Portfolio Tracker` avant de démarrer.
- **Partout**, le serveur du tableau de bord doit démarrer : comptez quelques secondes.

### Au premier affichage d'un portefeuille

Les cours sont téléchargés depuis Yahoo Finance (« Récupération des cours et calcul des indicateurs... »). Ensuite, les résultats sont gardés une heure : la navigation devient rapide.

### Les calculs les plus longs

- **stress tests** : téléchargement de l'historique depuis 2008, gardé ensuite en cache ;
- **attribution de performance** : téléchargement des indices régionaux ;
- **lecture d'un fichier envoyé** : vérification des prix, recherche des titres inconnus ;
- **PDF image** : reconnaissance de caractères, plusieurs secondes ;
- **rapport PDF** : toutes les analyses recalculées.

### Conseils

- Évitez [[Actualiser les cours]] sans raison : il efface toute la mémoire.
- La version en ligne peut être plus lente, notamment si le site était en veille.
