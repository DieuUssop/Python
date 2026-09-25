# Étape 10 — Conseil patrimonial et gestion d'actifs

## Ce que contient cette étape

Six outils d'aide à la décision, répartis dans deux nouveaux **espaces** du tableau de bord. On passe de l'un à l'autre avec le sélecteur « Espace de travail », en haut de la barre latérale.

| Espace | Onglet | Question à laquelle il répond |
|---|---|---|
| **Conseil patrimonial** | Profil client | Ce portefeuille convient-il à mon client ? |
| | Fiscalité | Combien reste-t-il après impôts, selon l'enveloppe ? |
| | Stress tests | Que perdrait-on si une crise passée se reproduisait ? |
| **Gestion d'actifs** | Attribution de performance | Pourquoi a-t-on battu (ou non) l'indice ? |
| | Budget de risque | D'où vient le risque du portefeuille ? |
| | Backtest de stratégies | Quelle stratégie de gestion aurait le mieux marché ? |

Les résultats apparaissent aussi dans `python main.py` et sur deux nouvelles pages du rapport PDF.

## A. Installer

1. Dézippe `mise_a_jour_etape10.zip` et copie son contenu dans `portfolio_tracker` (**Remplacer**).
2. Aucune bibliothèque nouvelle à installer.
3. Lance les tests : `python -m pytest`. Résultat attendu : **79 passed**.
4. Relance le tableau de bord : `python -m streamlit run app.py`.

Au premier affichage des stress tests, l'outil télécharge l'historique depuis 2008 (30 secondes à 1 minute pour le portefeuille mondial). Ensuite, le cache prend le relais.

---

## B. Conseil patrimonial

### 1. Le profil de risque client

**Contexte réglementaire.** Depuis la directive européenne **MiFID II** (2018), un conseiller doit évaluer son client *avant* de lui recommander un placement : connaissances, situation financière, objectifs, tolérance aux pertes. C'est le **test d'adéquation**.

**Le questionnaire** comporte 7 questions notées de 0 à 4 (horizon, objectif, réaction à une baisse, perte acceptable, expérience, part du patrimoine, épargne de précaution). Le score, sur 28, donne le profil :

| Score | Profil | Volatilité max | Perte max | Part d'actions max | SRI max |
|---|---|---|---|---|---|
| 0 – 6 | Sécuritaire | 3 % | 5 % | 10 % | 2 |
| 7 – 12 | Prudent | 7 % | 12 % | 30 % | 3 |
| 13 – 18 | Équilibré | 12 % | 20 % | 60 % | 4 |
| 19 – 23 | Dynamique | 18 % | 30 % | 85 % | 5 |
| 24 – 28 | Offensif | 30 % | 45 % | 100 % | 6 |

**Règle de prudence** : la réponse sur la perte acceptable **plafonne** le profil. Un client qui n'accepte pas plus de 5 % de perte ne peut pas être classé « Dynamique », même avec un score élevé. Le critère le plus prudent l'emporte, comme dans les questionnaires réels.

**L'indicateur SRI** (Summary Risk Indicator) est l'échelle de 1 à 7 imprimée sur les documents d'information des produits financiers (règlement européen **PRIIPs**). Il est estimé ici à partir de la volatilité. Le calcul réglementaire utilise une VaR ajustée (Cornish-Fisher) : c'est une approximation, à signaler.

**Si le portefeuille est trop risqué**, l'outil propose une solution simple : mélanger le portefeuille avec un placement sans risque. Si la volatilité du portefeuille est σ et que le profil accepte au plus σ_max, on garde **σ_max / σ** du capital sur le portefeuille. Par exemple, avec 16 % de volatilité pour un maximum de 12 %, on garde 75 % du capital sur le portefeuille et on place 25 % en fonds euros.

### 2. La fiscalité des enveloppes (taux 2026)

| Enveloppe | Avant le délai | Après le délai |
|---|---|---|
| **Compte-titres** | Flat tax **31,4 %** (12,8 % d'impôt + 18,6 % de prélèvements sociaux) | — |
| **PEA** (délai : 5 ans) | 31,4 % | **18,6 %** (prélèvements sociaux seulement) |
| **Assurance-vie** (délai : 8 ans) | 30 % (12,8 % + 17,2 %) | **7,5 %** au-delà d'un abattement de 4 600 € (9 200 € pour un couple) + **17,2 %** |

**Nouveauté 2026** : la loi de financement de la Sécurité sociale a porté la CSG sur les revenus du capital à un niveau tel que les prélèvements sociaux passent de 17,2 % à **18,6 %** (flat tax : 30 % → **31,4 %**). L'assurance-vie reste à 17,2 %. C'est un point d'actualité à citer à l'oral.

Le graphique « Gain net selon l'année de sortie » montre les **sauts** à 5 ans (PEA) et à 8 ans (assurance-vie). Il permet de montrer concrètement pourquoi un conseiller recommande d'ouvrir ces enveloppes tôt, pour « prendre date ».

**Éligibilité au PEA** : seules les actions de sociétés européennes (UE/EEE) et certains fonds sont éligibles. Pour le portefeuille mondial, la part éligible est faible, ce qui en fait un bon sujet de discussion.

**Simplifications** : option pour le barème progressif, plafonds de 150 000 € et frais des contrats ne sont pas modélisés.

### 3. Les stress tests

On rejoue **5 crises réelles** sur le portefeuille **actuel**, du plus haut au plus bas du marché :

| Crise | Période |
|---|---|
| Crise financière | 01/09/2008 → 09/03/2009 |
| Dette européenne | 01/07/2011 → 22/09/2011 |
| Covid | 19/02/2020 → 23/03/2020 |
| Inflation et hausse des taux | 03/01/2022 → 12/10/2022 |
| Mini-krach d'août 2024 | 16/07/2024 → 05/08/2024 |

Si un titre n'était pas coté à l'époque, on utilise l'**indice de sa région** (S&P 500, Euro Stoxx 50, FTSE 100, etc.). La colonne « Part estimée par un indice » l'indique.

**Chocs hypothétiques** : baisse des actions de 10, 20 et 35 %, traduite par le **bêta** du portefeuille (perte ≈ β × choc), et baisse du dollar de 10 % sur la part investie en dollars.

**Intérêt pour l'oral** : « au pire moment de 2008, ce portefeuille aurait perdu X % soit Y € » parle bien plus à un client qu'une volatilité.

---

## C. Gestion d'actifs

### 4. L'attribution de performance (Brinson-Fachler, 1985)

Elle explique l'écart de performance avec l'indice de référence, région par région, en trois effets :

- **Allocation** = (wₚ − w_b) × (r_b − R_b) : a-t-on surpondéré les régions qui ont fait mieux que l'indice ?
- **Sélection** = w_b × (rₚ − r_b) : dans chaque région, a-t-on choisi de meilleurs titres que l'indice ?
- **Interaction** = (wₚ − w_b) × (rₚ − r_b) : l'effet croisé des deux.

**Indice de référence** : les poids régionaux du **MSCI ACWI IMI** au 30/06/2026 (États-Unis 62,7 %, Émergents 12,3 %, Europe 8,7 %, Japon 5,6 %…), avec un indice boursier par région, converti en euros.

**Point de rigueur à expliquer** : le calcul est fait mois par mois. Or les rendements se composent : +10 % puis +10 % donnent +21 %, pas +20 %. Additionner simplement les effets mensuels ne redonne donc pas l'écart total. La méthode de **Cariño (1999)** pondère chaque mois pour que la somme des effets soit **exactement** égale à l'écart. Un test automatique le vérifie.

**Limites** : indices régionaux hors dividendes (l'indice est donc désavantagé d'environ 2 % par an), et attribution par région seulement (pas par secteur).

### 5. Le budget de risque et la parité des risques

**Contribution au risque** : le poids d'une ligne ne dit pas quelle part du **risque** elle apporte. Pour chaque ligne :

```
contribution = wᵢ × (Σ w)ᵢ / σₚ        la somme des contributions = σₚ (propriété d'Euler)
```

Une ligne dont la part du risque dépasse sa part de la valeur est plus volatile ou plus corrélée au reste que la moyenne.

**Parité des risques** : chaque ligne contribue **autant** au risque. Cette allocation n'utilise **pas les rendements espérés**, qui sont très mal estimés : c'est la réponse directe à la limite de Markowitz. Elle a été popularisée par le fonds « All Weather » de Bridgewater. Calcul : méthode de Spinu (2013).

**Nombre effectif de paris** = 1 / Σ(part de risqueᵢ)². Il indique combien de lignes « indépendantes » le portefeuille représente vraiment : 69 lignes peuvent ne valoir qu'une trentaine de paris.

### 6. Le backtest de stratégies

Avec les **mêmes titres et les mêmes poids de départ** que le portefeuille actuel :

- **Rééquilibrer ou non ?** Achat-conservation, ou retour aux poids cibles chaque mois, trimestre ou année, avec 0,1 % de frais. Le rééquilibrage maintient le risque voulu, mais coûte des frais (voir la colonne « Rotation / an ») et freine la performance quand une tendance dure.
- **Investir en une fois ou progressivement (DCA) ?** Sur un marché haussier, investir en une fois rapporte en général plus (l'argent travaille plus tôt). L'investissement progressif réduit le risque d'investir juste avant une baisse. C'est une question que posent très souvent les clients.

**Limite** : cours hors dividendes, et un seul historique (depuis 2024). Un résultat de backtest ne garantit rien pour l'avenir.

---

## D. Réglages (src/config.py)

```python
PROFIL_CLIENT = "Équilibré"          # profil utilisé par main.py et le rapport PDF
SITUATION_FAMILIALE = "célibataire"  # ou "couple"
```

Dans le tableau de bord, le profil est calculé à partir du questionnaire.

## E. Exercices

1. Remplis le questionnaire pour un étudiant de 23 ans, puis pour un retraité de 70 ans. Le portefeuille mondial est-il adapté à chacun ? Que proposes-tu au retraité ?
2. Dans l'onglet Fiscalité, à partir de combien d'années le PEA devient-il plus intéressant que le compte-titres ? Et l'assurance-vie ?
3. Quelle crise aurait coûté le plus cher au portefeuille actuel ? Pourquoi (régions, secteurs) ?
4. Dans l'attribution, l'écart avec l'indice vient-il surtout de l'allocation ou de la sélection ? Relie ta réponse à l'équipondération des titres du fonds mondial (les grandes capitalisations, très lourdes dans l'indice, sont sous-pondérées).
5. Compare « Portefeuille actuel » et « Parité des risques » : laquelle des deux allocations a le meilleur Sharpe ? Le plus grand nombre effectif de paris ?
6. Le rééquilibrage a-t-il amélioré la performance sur la période ? Explique pourquoi avec le comportement des marchés depuis 2024.

## F. Si ça ne marche pas

| Problème | Solution |
|---|---|
| « Stress tests indisponibles » | Pas d'Internet au premier chargement : il faut télécharger l'historique depuis 2008 une fois |
| « Attribution indisponible » | Même cause (indices régionaux) ; ou historique de moins de deux fins de mois |
| Note « … n'est pas classé dans une région de l'indice » | Normal pour ton portefeuille personnel (ETF monde) : l'attribution est faite pour le fonds mondial |
| Le premier affichage des stress tests est long | Normal (historique depuis 2008) ; ensuite, c'est instantané grâce au cache |
