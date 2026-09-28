# Importer son propre portefeuille (format libre)

## Ce que ça permet

N'importe qui peut envoyer **son** fichier depuis la barre latérale du tableau de bord (« Ou envoyer un autre fichier »), sans respecter le format du projet :

- un **export de banque ou de courtier** (relevé d'opérations en CSV ou Excel) ;
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
- Un fichier très inhabituel (deux tableaux d'opérations l'un sous l'autre, cellules fusionnées, tableau collé à un autre sans colonne vide) peut encore demander l'assistant.

## Pour les tests

`tests/test_import_auto.py` vérifie la détection par le contenu (fichier sans titres de colonnes), la clé ISIN, l'ordre jour/mois et les conversions de devises (cours simulés). `tests/test_import_libre.py` vérifie la lecture d'un relevé de courtier fictif : lignes de titre, ISIN, « Achat Comptant », quantité négative, montant net, ligne de frais de garde.
