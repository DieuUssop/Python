# Importer son propre portefeuille (format libre)

## Ce que ça permet

N'importe qui peut envoyer **son** fichier depuis la barre latérale du tableau de bord (« Envoyer un fichier (CSV, Excel ou PDF) »), sans respecter le format du projet :

- un **export de banque ou de courtier** (relevé d'opérations en CSV, Excel ou **PDF**) ;
- un **avis d'opéré en PDF** (la confirmation envoyée par la banque après chaque ordre) ;
- un **tableau Excel personnel**, avec ses propres noms de colonnes ;
- des titres désignés par leur **code ISIN** (FR0000121014) ou leur **nom**, au lieu du ticker Yahoo Finance.

## La détection automatique

Dans la plupart des cas, il n'y a **rien à faire** : l'outil comprend seul le fichier et l'analyse directement. Un encadré dans la barre latérale résume ce qu'il a compris.

1. **Les colonnes sont reconnues par leur nom** (« Date opération », « Qté », « Cours »…) **et par leur contenu** :

   | Rôle | Comment il est reconnu |
   |---|---|
   | Date | presque toutes les cases sont des dates |
   | ISIN | 12 caractères et une **clé de contrôle** vérifiée par calcul (algorithme de Luhn) |
   | Ticker | codes courts en majuscules (AAPL, MC.PA) |
   | Type d'opération | peu de valeurs différentes : « Achat », « Vente », « Coupon »… |
   | Devise | EUR, USD, GBP… |
   | Nom du titre | texte libre |
   | Quantité, prix, montant, frais | l'outil essaie les combinaisons et garde celle où **quantité × prix ± frais = montant** tombe juste |

   Un fichier **sans ligne de titres**, ou avec des titres sans signification (« A, B, C »), est donc compris quand même.

2. **Les dates ambiguës** (03/04/2024 : 3 avril ou 4 mars ?) : une seule date comme 13/04 ou 04/13 dans la colonne suffit à trancher. Sinon, le format français (jour/mois) est retenu et signalé.

3. **Les codes des titres**, quelle que soit leur forme, sont convertis en tickers Yahoo Finance :

   | Forme | Exemple | Devient |
   |---|---|---|
   | Ticker **Bloomberg** | `MC FP Equity`, `AAPL US Equity`, `NESN SW`, `700 HK` | MC.PA, AAPL, NESN.SW, 0700.HK |
   | Google Finance | `EPA:MC`, `NASDAQ:AAPL` | MC.PA, AAPL |
   | Reuters (RIC) | `AAPL.O`, `NESN.S` | AAPL, NESN.SW |
   | Ticker + colonne « Place » | `MC` + `XPAR` (code MIC), `Euronext Paris`, `FP`… | MC.PA |
   | Ticker **sans place** | `MC`, `AIR`, `TTE`, `TSLA` | l'outil essaie les grandes places (New York, Paris, Francfort, Amsterdam, Milan, Madrid, Londres, Zurich, Toronto) et garde celle dont le **cours correspond aux prix du fichier** : `MC` à 740 € est LVMH (MC.PA), pas Moelis (MC à New York, 50 $) |
   | Code **ISIN** | `FR0000121014` | recherche Yahoo Finance, Bourse du pays privilégiée → MC.PA |
   | Nom de société | `LVMH`, `Microsoft` | recherche Yahoo Finance |

   Les conversions Bloomberg, Google et Reuters se font **sans connexion** (table des codes de place). Pour les tickers Bloomberg, la « yellow key » (`Equity`) est facultative.

4. **Les devises** : l'outil compare chaque prix au **vrai cours de clôture du jour**, selon trois lectures (devise de cotation, devise principale — livres au lieu de pence —, ou euros) et garde la plus proche. Un relevé bancaire en euros pour une action américaine est ainsi **reconverti en dollars** automatiquement, avec le taux de change du jour. Par prudence, la conversion n'est faite que si elle colle nettement mieux au marché (plus de 2 % d'écart).

5. **Les informations en plus sont ignorées** : lignes de titre au-dessus du tableau, colonnes inutiles (commentaires…), lignes vides, lignes « Total » ou notes sous le tableau (ni date ni titre), autres feuilles Excel, petit tableau de résumé placé à côté (séparé par une colonne vide).

6. **Le contrôle qualité** : un prix à plus de 25 % du cours du jour est signalé (mauvais ticker, mauvaise devise, division d'actions…).

Si un point reste incertain (colonnes de nombres impossibles à départager, titre introuvable, lignes illisibles), **l'assistant d'import s'ouvre**, déjà pré-rempli : il suffit de vérifier.

## L'assistant d'import

Quand la détection automatique a un doute, l'assistant s'ouvre, en 4 étapes (il comprend aussi le choix de la devise des prix : détection automatique, devise de cotation, ou « tout est en euros ») :

| Étape | Ce que fait l'outil | Ce que fait l'utilisateur |
|---|---|---|
| 1. Le fichier | Trouve la ligne des titres de colonnes, même après des lignes d'en-tête (« Relevé des opérations », n° de compte…) | Choisit la feuille Excel si besoin, corrige la ligne |
| 2. Correspondance | Devine la colonne de chaque information (date, type, titre, quantité, prix unitaire **ou** montant total, frais) | Vérifie, corrige avec les menus |
| 3. Types et titres | Classe les opérations (« Achat Comptant » → achat, « Coupons » → dividende, « Frais de garde » → ignorée) et cherche le **ticker Yahoo Finance** de chaque ISIN ou nom | Corrige une interprétation ou saisit un ticker introuvable |
| 4. Résultat | Montre les transactions converties et les lignes ignorées | Clique sur **Analyser ce portefeuille** (ou télécharge le fichier converti) |

À tout moment, le bouton **« Ouvrir l'assistant d'import »** (barre latérale) permet de reprendre la lecture du fichier à la main.

## Les règles de conversion (à savoir expliquer)

- **Montant total au lieu du prix unitaire** : prix = montant ÷ quantité. Si le montant est « net » (frais inclus) : achat = quantité × prix + frais, donc prix = (montant − frais) ÷ quantité ; vente = quantité × prix − frais.
- **Quantité négative** : elle est rendue positive ; sans colonne « type », elle signifie une vente.
- **Dividendes** : le montant total reçu est conservé, la quantité est mise à 0 (convention du projet).
- **ISIN → ticker** : recherche sur le moteur de Yahoo Finance, en privilégiant la **Bourse du pays** de l'ISIN (FR → Paris « .PA », DE → Francfort « .DE », US → New York…). Pour un ETF irlandais ou luxembourgeois, une cotation en euros est privilégiée.

## Limites

- Il faut un **historique d'opérations** (avec des dates) : une simple liste de positions ne permet pas de calculer les performances.
- La recherche des tickers a besoin d'Internet ; un titre introuvable doit être saisi à la main.
- Les frais de garde, virements et impôts sont ignorés (ils ne concernent pas un titre).
- La conversion des devises utilise le taux de change du marché ; celui de la banque diffère légèrement (sa marge de change), d'où de petits écarts.
- La vérification des prix et la recherche des tickers ont besoin d'Internet ; sans connexion, les prix sont gardés tels quels et c'est signalé.
- Un **PDF scanné** (photo ou scan papier) ne contient pas de texte : il est lu par reconnaissance de caractères si un moteur est installé (requirements-ocr.txt). Sinon, ou si rien n'est reconnu, le formulaire « Compléter l'opération » s'ouvre (voir plus bas).
- Un fichier très inhabituel (deux tableaux d'opérations l'un sous l'autre, cellules fusionnées, tableau collé à un autre sans colonne vide) peut encore demander l'assistant.

## Pour les tests

`tests/test_import_auto.py` vérifie la détection par le contenu (fichier sans titres de colonnes), la clé ISIN, l'ordre jour/mois et les conversions de devises (cours simulés). `tests/test_import_libre.py` vérifie la lecture d'un relevé de courtier fictif : lignes de titre, ISIN, « Achat Comptant », quantité négative, montant net, ligne de frais de garde.
`tests/test_pdf.py` vérifie la lecture d'un relevé PDF (tableau), d'un avis d'opéré (date d'exécution et non d'édition, ISIN, quantité, cours, devise) et le cas d'un PDF scanné.
`tests/test_pdf_universel.py` est le banc d'essai « tous courtiers » : 20 documents fictifs aux mises en page très différentes (`tests/avis_fictifs.py`, fabriqués à la volée : courtier en ligne 2023 en tableau et 2026, intitulés avec ou sans deux-points, deux colonnes, anglais sans intitulé de quantité, quantité fractionnaire, mois en lettres et dollars, date en toutes lettres, deux opérations sans tableau, dividende, montant net seul, frais multiples et bruit, contre-valeur en euros, quantité 1, texte « codé », deux scans, colonnes sans traits, scan abîmé, relevé de portefeuille), plus les tests du départage par le marché, des modèles appris, des contrôles, du PDF protégé, des divisions et de l'anonymisation. Chacun doit être lu exactement, par la chaîne complète ET par la seule lecture du contenu. `python -m tests.avis_fictifs dossier` écrit ces PDF pour les ouvrir.

## Les PDF

- **Relevé avec un tableau** : les tableaux du PDF sont extraits (bibliothèque *pdfplumber*), puis lus comme un fichier Excel, avec la même détection automatique.
- **Avis d'opéré** : le texte est d'abord lu par ses intitulés (« Quantité : », « Cours : », « Courtage : »…) : date d'exécution, sens (achat / vente), code ISIN, quantité, cours et devise, courtage et taxes, montant net. Un PDF de plusieurs pages contenant un avis par page donne une opération par page.
- **N'importe quel courtier : lecture par le contenu** (`src/lecture_pdf.py`). Si les intitulés ne sont pas reconnus, l'outil ne se fie plus à la mise en page : il repère le code ISIN (clé de contrôle), la date d'exécution (en chiffres ou en lettres, en français ou en anglais ; dates d'édition, de règlement et de valeur écartées), tous les nombres de la page, et cherche les trois qui vérifient **quantité × cours = montant brut** au centime près (ou quantité × cours ± frais = montant net). Les frais sont les nombres qui suivent « courtage, commission, frais, costs, TTF… », le sens vient des mots achat / vente / buy / sell / dividende. Plusieurs opérations sur une page : une par code ISIN. Exemple : « Buy 15 VANGUARD S&P 500 … at 85.12 EUR · Value 1,276.80 » → 15 × 85,12 = 1 276,80.
- **Texte « codé »** : certains PDF s'affichent bien mais leur texte extrait est du charabia (police à encodage maison). C'est détecté, et la page est lue comme une image (reconnaissance de caractères).
- **Formulaire « Compléter l'opération »** (`src/vues_pdf.py`) : si rien n'est sûr, pas de message d'erreur sec. Le formulaire propose ce qui a été trouvé : date probable, code ISIN et nom, sens, et pour la quantité, le prix unitaire et les frais la liste des nombres du document, chacun avec les mots qui l'entourent, la meilleure proposition déjà choisie (on peut taper une autre valeur). Une ligne « Contrôle : q × p = m » aide à vérifier. Rien n'est inventé. Il s'ouvre sur la page « Ajouter des opérations » et lors d'un envoi depuis la barre latérale.
- **Départage par le marché** : si plusieurs lectures sont cohérentes (quantité × cours = montant), celle dont le cours est à moins de 5 % du cours de clôture du jour (Yahoo Finance) remplace une lecture à plus de 15 %. Le formulaire affiche aussi ce cours de clôture.
- **Modèles appris** : quand le formulaire est validé, le logiciel retient l'intitulé qui précède chaque valeur (« Nominal », « Px moyen »…) et le code du sens (« Sens : S » = vente) ; le prochain document du même type est lu tout seul. Fichier local `data/base/modeles_pdf.json`, sans montant ni nom en clair (vocabulaire haché).
- **Intitulés au-dessus des valeurs** (colonnes sans traits de tableau) : la position des mots sur la page relie chaque valeur à son intitulé.
- **Scans difficiles** : seconde lecture sur une image redressée, contrastée, en noir et blanc et en plus haute résolution ; chiffres lus comme des lettres corrigés dans les nombres (« 65O,2O » → « 650,20 »).
- **Contrôles après lecture** (dans le résumé) : montant ≠ quantité × cours ± frais, date un samedi ou un dimanche, frais de plus de 3 %, opération en double.
- **Relevé de portefeuille** (positions et PRU) : chaque position devient un achat au PRU à la date du relevé, pour créer un portefeuille de départ.
- **PDF protégé par mot de passe** : le mot de passe est demandé ; la copie déchiffrée reste en mémoire pour la session, le mot de passe n'est conservé nulle part.
- **Plusieurs fichiers d'un coup** depuis la barre latérale : chacun est lu, leurs opérations sont réunies (doublons comptés une fois).
- **Division / regroupement d'actions** (page « Ajouter des opérations ») : les opérations antérieures du titre sont converties (quantité × facteur, prix ÷ facteur), comme les cours de Yahoo Finance.
- **Rapport anonymisé** : bouton « Préparer un rapport anonymisé » dans le formulaire, ou `python diagnostic_pdf.py fichier.pdf --anonyme` ; nom, adresse, e-mail, IBAN, téléphone et numéros de compte masqués. Les vrais avis anonymisés s'ajoutent au banc d'essai dans `tests/donnees/vrais_avis/`.
- **Sans Internet** : 31 ETF, les actions du CAC 40 et les grandes valeurs américaines sont reconnus par leur ISIN.
- **Limite honnête** : aucun lecteur ne garantit 100 % des documents existants ; le formulaire sert de filet de sécurité. Pour un PDF mal lu, `python diagnostic_pdf.py fichier.pdf` montre ce que l'outil y lit (texte, tableaux, lecture par le contenu, résultat).
- **PDF « image »** (scan, photo, ou page web imprimée avec « Microsoft Print to PDF ») : le fichier ne
  contient aucun caractère, seulement une image de la page. L'outil lit alors le texte par
  **reconnaissance de caractères** (OCR, bibliothèque RapidOCR, hors connexion) : il essaie les 4 sens
  de la page (impression en paysage), corrige les codes ISIN mal lus (lettre O au lieu du chiffre 0)
  en vérifiant leur clé de contrôle, puis lit l'avis comme un PDF texte. C'est plus lent (5 à 15 s)
  et moins sûr : les opérations sont à vérifier. Si rien n'est reconnu, un message l'explique.
- **Conseil** : sur le site de la banque, utiliser le bouton « Format PDF » ou « Télécharger » plutôt
  que « Imprimer » : le PDF contient alors le vrai texte, lu instantanément et sans erreur possible.
- Exemple testé : avis d'opéré Bourse Direct (« VENTE COMPTANT », « QUANTITE : -60 »,
  « COURS : +41,295 », « COURTAGE : +3,80 », ISIN dans la colonne Désignation).

## Mettre à jour son portefeuille (sans tout renvoyer)

Bouton **« Ajouter des opérations »** (barre latérale, ou « Mon compte » pour un portefeuille enregistré) :

1. envoyer seulement les nouveaux mouvements : un ou plusieurs avis d'opéré PDF, un export des dernières opérations (Excel, CSV, PDF), ou **saisir un ordre à la main** (date, type, titre par son ticker, son ISIN, son nom ou son code Bloomberg, quantité, prix, frais) ;
2. **vérifier** : le tableau est modifiable ; les opérations **déjà présentes** (même date, titre, type, quantité, prix à 0,5 % près — cas d'un relevé qui chevauche l'ancien) sont décochées ; une **vente de titres non détenus** ou une **date future** bloque l'enregistrement ;
3. **enregistrer** : les opérations sont fusionnées et triées par date. Dans « Mon espace », le portefeuille est rechiffré et le bouton **« Annuler la dernière modification »** permet de revenir en arrière. Sans compte, le fichier mis à jour est proposé au téléchargement.

Ajouter deux fois le même fichier ne change rien. Tests : `tests/test_mouvements.py`.

## Supprimer ou corriger une opération

Onglet **Transactions** → bouton **« Modifier les opérations »** :

1. le tableau devient modifiable : une case **« Supprimer »** par ligne, et la date, la quantité, le prix (dans la devise de cotation du titre) et les frais se corrigent directement ; les filtres Type et Titres aident à retrouver une ligne ;
2. un **récapitulatif** liste les suppressions et les corrections ;
3. **contrôles** : supprimer un achat dont dépend une vente ultérieure (vente de titres non détenus), une date future ou une quantité nulle bloquent l'enregistrement ; le logiciel prévient si un titre disparaît du portefeuille ;
4. cocher **« Je confirme ces modifications »**, puis **« Enregistrer les modifications »**.

Dans « Mon espace », la version précédente est gardée : **« Annuler la dernière modification »** (onglet Transactions ou « Mon compte ») revient en arrière. Pour un fichier envoyé sans compte ou un portefeuille d'exemple, la modification vaut pour la session et le fichier corrigé est proposé au téléchargement. Tests : `tests/test_mouvements.py`.
