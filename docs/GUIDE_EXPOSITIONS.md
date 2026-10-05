# Guide — Expositions, diversification réelle et indices de référence

## 1. L'analyse « en transparence »

Un ETF MSCI World est un seul titre, coté à Paris en euros… mais il contient ≈ 1 400 actions
de 23 pays, dont ≈ 73 % aux États-Unis. Pour mesurer les vraies expositions, chaque ETF est
**réparti selon la composition de l'indice qu'il suit** (`src/composition_etf.py`) :

- poids par pays et par secteur des grands indices (MSCI World, ACWI, Emerging Markets,
  Europe, S&P 500, Nasdaq-100, Euro Stoxx 50, CAC 40, DAX…) et des grands indices obligataires ;
- sources : fiches MSCI au 30/09/2026 pour les 5 premiers pays et les secteurs, ordres de
  grandeur pour le reste. C'est une **approximation** (quelques points d'écart au plus), indiquée
  sous la carte et dans l'onglet.

La même analyse alimente : la **carte du monde** et les **anneaux** de la vue d'ensemble,
l'onglet **Expositions**, et la page « Expositions et diversification » du rapport PDF.

## 2. L'onglet « Expositions » (Analyse du portefeuille)

| Dimension | Ce qui est mesuré | Pourquoi c'est important |
|---|---|---|
| Géographie | Pays et régions de la poche actions, comparés au marché mondial (MSCI ACWI) | Risque politique / économique concentré, biais domestique, part des émergents |
| Secteurs | Secteurs GICS de la poche actions | Dépendance à un seul cycle ; présence de secteurs défensifs |
| Devises | Exposition **réelle** (un ETF monde coté en € reste exposé au dollar, sauf s'il est couvert) | Risque de change : une baisse de 10 % du dollar fait perdre ≈ 10 % × la part en dollars |
| Concentration | Plus grosses lignes, nombre effectif de lignes (1 / Σ poids²), règle UCITS 5/10/40, titres détenus en direct ET via un ETF | Risque propre à une entreprise |
| Taux | Duration moyenne des obligations, perte si les taux montent de 1 point | Sensibilité aux taux (≈ − duration × variation des taux) |
| Diversification réelle | Corrélations : blocs de titres corrélés, corrélation moyenne, ratio de diversification, corrélation les jours de forte baisse | Dix lignes qui bougent ensemble ne valent qu'un seul pari |

**Diagnostic** : des règles simples aux seuils documentés (`SEUILS` dans `src/expositions.py`)
classent chaque dimension en vert (bon), orange (à surveiller) ou rouge (à corriger). Les seuils
dépendent du **profil** (prudent, équilibré, dynamique), repris du questionnaire de l'espace
« Conseil patrimonial » ou choisi dans l'onglet. Chaque constat donne le chiffre observé, le
risque associé et des pistes. Ce n'est pas un conseil en investissement.

### Les corrélations, lisibles même avec 50 titres

- titres **regroupés par blocs** qui évoluent ensemble (classification hiérarchique, distance
  = 1 − corrélation) : les blocs apparaissent comme des carrés rouges ;
- **moitié du tableau** seulement, sans la diagonale ; cases carrées ;
- au-delà de 20 titres, vue **par classe d'actifs / région / secteur** par défaut (corrélation
  entre les rendements des sous-portefeuilles) ;
- **ratio de diversification** = Σ wᵢσᵢ / σₚ (1 = aucune diversification) ;
- **blocs indépendants** : groupes de titres corrélés à plus de 0,7 ;
- corrélation moyenne les **10 % pires jours** : elle monte souvent en crise.

### Ce qui a été réorganisé (pour éviter les doublons)

- Les corrélations ont quitté l'onglet « Risque » pour « Expositions ».
- « Gestion d'actifs › Budget de risque » se concentre désormais sur la **construction
  d'allocations** (part du risque de chaque ligne, parité des risques, variance minimale) ; le
  diagnostic par région / secteur / devise et le ratio de diversification sont dans « Expositions ».

## 3. Les indices de référence (`src/indices.py`)

| Famille | Indices | Ticker utilisé |
|---|---|---|
| Actions | MSCI World, MSCI ACWI, S&P 500, Nasdaq-100, Stoxx Europe 600, Euro Stoxx 50, CAC 40, MSCI Émergents | ETF capitalisants (dividendes réinvestis) ou indices de prix |
| Obligations | Emprunts d'État zone euro, obligations d'entreprises en euros | DBXN.DE (sinon EUNH.DE), EUN5.DE |
| Monétaire | €STR | XEON.DE |
| Mixtes | Prudent 20/80, Équilibré 60/40, Dynamique 80/20 | **calculés** : MSCI World + emprunts d'État €, rééquilibrés chaque mois |

Chaque indice a plusieurs tickers « candidats » : le premier disponible (Yahoo ou base locale)
est utilisé. Face à un indice obligataire ou monétaire, le bêta et l'alpha ont peu de sens : une
note le rappelle dans l'onglet « Performance ».

## 4. Tests

`tests/test_expositions.py` : compositions complètes (total 100 %), ETF monde éclaté et devise
réelle, obligations / or / duration, règle 5/10/40, regroupement de deux blocs synthétiques,
ratio de diversification (deux actifs identiques → 1), écarts à l'indice, indice composite.
