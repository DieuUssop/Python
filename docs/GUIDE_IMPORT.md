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
- Un **PDF scanné** (photo ou scan papier) ne contient pas de texte : il est refusé avec un message clair (exporter le relevé en PDF depuis l'espace bancaire, en Excel / CSV, ou saisir l'opération à la main).
- Un fichier très inhabituel (deux tableaux d'opérations l'un sous l'autre, cellules fusionnées, tableau collé à un autre sans colonne vide) peut encore demander l'assistant.

## Pour les tests

`tests/test_import_auto.py` vérifie la détection par le contenu (fichier sans titres de colonnes), la clé ISIN, l'ordre jour/mois et les conversions de devises (cours simulés). `tests/test_import_libre.py` vérifie la lecture d'un relevé de courtier fictif : lignes de titre, ISIN, « Achat Comptant », quantité négative, montant net, ligne de frais de garde.
`tests/test_pdf.py` vérifie la lecture d'un relevé PDF (tableau), d'un avis d'opéré (date d'exécution et non d'édition, ISIN, quantité, cours, devise) et le refus d'un PDF scanné.

## Les PDF

- **Relevé avec un tableau** : les tableaux du PDF sont extraits (bibliothèque *pdfplumber*), puis lus comme un fichier Excel, avec la même détection automatique.
- **Avis d'opéré** : le texte est lu ligne à ligne : date d'exécution, sens (achat / vente), code ISIN, quantité, cours et devise, courtage et taxes, montant net. Un PDF de plusieurs pages contenant un avis par page donne une opération par page.
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
