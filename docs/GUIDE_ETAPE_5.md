# Étape 5 — Les indicateurs avancés

## Objectif

À l'étape 4, on a mesuré la performance et le risque **séparément**. On va maintenant répondre à trois questions plus fines :

1. **Le risque pris a-t-il été bien payé ?** → ratios de Sharpe et de Sortino
2. **Ai-je fait mieux que le marché, et pourquoi ?** → bêta, alpha, tracking error, ratio d'information
3. **Combien puis-je perdre un mauvais jour ?** → VaR et CVaR

On regarde aussi les **corrélations** entre tes titres, pour juger de la diversification.

## A. Installer la mise à jour

1. Dézippe `mise_a_jour_etape5.zip`.
2. Copie son contenu dans ton dossier `portfolio_tracker` et choisis **Remplacer**.
3. Aucune nouvelle bibliothèque à installer.

Nouveaux fichiers : `src/config.py`, `GUIDE_ETAPE_5.md`.
Fichiers modifiés : `src/metrics.py`, `src/graphiques.py`, `main.py`, `tests/test_metrics.py`, `README.md`.

## B. Le fichier de réglages `src/config.py`

Ouvre-le. Il contient les choix méthodologiques qu'un professeur peut discuter :

| Réglage | Valeur | Pourquoi |
|---|---|---|
| `INDICE_REFERENCE` | `CW8.PA` (ETF MSCI World) | ETF **capitalisant** : dividendes réinvestis, comme dans notre calcul. Le CAC 40 (`^FCHI`) est calculé **hors dividendes** : le comparer à notre portefeuille désavantagerait l'indice d'environ 3 % par an. |
| `TAUX_SANS_RISQUE` | 2,50 % | Taux de dépôt de la BCE depuis le 16/09/2026 |
| `NIVEAU_CONFIANCE_VAR` | 95 % | Standard du marché |

Tu peux essayer de changer l'indice pour `"^FCHI"` et observer ce qui change.

## C. Lancer le programme

```
python main.py
```

Nouvelle partie à la fin (exemple, **tes chiffres seront différents**) :

```
INDICATEURS AVANCÉS
Taux sans risque retenu   : 2.50% par an

Rendement ajusté du risque          Portefeuille      Indice
  Ratio de Sharpe                         0.42       -0.46
  Ratio de Sortino                        0.66
  Volatilité annualisée                 12.39%      19.42%
  TWR sur la période                   +21.56%     -20.58%

Comparaison avec : MSCI World (ETF Amundi CW8, dividendes réinvestis)
  Bêta                    : 0.46
  Alpha de Jensen (annuel): +9.32 %
  Corrélation             : 0.71
  Tracking error          : 13.70%
  Ratio d'information     : 1.03

Risque de perte sur 1 jour (niveau de confiance 95%)
  VaR historique          : 1.10%  soit 168 €
  VaR paramétrique        : 1.25%
  CVaR (Expected Shortfall): 1.44%  soit 220 €
```

Puis la matrice de corrélation. Deux nouveaux graphiques apparaissent :

- `graphique_comparaison.png` : ton portefeuille et l'indice, tous deux en base 100 ;
- `graphique_correlations.png` : la carte des corrélations entre tes titres.

Tests : `python -m pytest`. Résultat attendu : **31 passed**.

## D. Comprendre les indicateurs

### 1. Ratio de Sharpe : le risque a-t-il été bien payé ?

```
          rendement moyen − taux sans risque
Sharpe = ------------------------------------
                    volatilité
```

On retire le taux sans risque car on pouvait l'obtenir sans prendre aucun risque. Seul le surplus rémunère le risque pris.

| Sharpe | Lecture |
|---|---|
| < 0 | on aurait mieux fait de rester sur un livret |
| 0 à 0,5 | médiocre |
| 0,5 à 1 | correct |
| > 1 | très bon |

### 2. Ratio de Sortino : ne pénaliser que les baisses

Critique du Sharpe : la volatilité compte **aussi les fortes hausses** comme du risque. Sortino ne garde que les jours de baisse (la « semi-déviation »). Si ton Sortino est nettement plus grand que ton Sharpe, ta volatilité vient surtout de hausses : c'est une bonne nouvelle.

### 3. Bêta : la sensibilité au marché

```
bêta = covariance(portefeuille, indice) / variance(indice)
```

- **β = 1** : le portefeuille suit le marché ;
- **β > 1** (ex. 1,3) : quand le marché fait +1 %, le portefeuille fait en moyenne +1,3 %. Il est **offensif** ;
- **β < 1** (ex. 0,7) : il est **défensif**.

Le bêta mesure le **risque systématique**, celui qu'on ne peut pas éliminer en diversifiant.

### 4. Alpha de Jensen : la valeur ajoutée du gérant

C'est la part du rendement qui ne s'explique **pas** par l'exposition au marché (modèle du MEDAF) :

```
alpha = (rendement portefeuille − rf) − β × (rendement indice − rf)
```

**Alpha > 0** : le choix des titres a créé de la valeur au-delà du simple risque de marché.

### 5. Tracking error et ratio d'information

- **Tracking error** : la volatilité de l'**écart** avec l'indice. Faible (< 2 %) pour un fonds indiciel, élevée (> 5 %) pour une gestion très active.
- **Ratio d'information** = écart de rendement annuel / tracking error. S'écarter de l'indice a-t-il été payant ? Au-delà de 0,5, c'est bon.

### 6. VaR et CVaR : combien puis-je perdre un mauvais jour ?

**VaR 95 % à 1 jour = 168 €** veut dire : *« dans 95 % des jours, je ne perdrai pas plus de 168 €. »* Autrement dit, environ 1 jour sur 20, la perte dépasse ce montant.

Deux méthodes de calcul :

- **Historique** : on prend le 5e pire pourcentage des rendements passés. On ne fait aucune hypothèse, mais on suppose que le passé se répète.
- **Paramétrique** : on suppose une **loi normale**, VaR = −(μ − 1,645 σ). C'est simple, mais la loi normale **sous-estime les krachs** : dans la réalité, les très fortes baisses sont bien plus fréquentes qu'elle ne le prévoit (« queues épaisses »).

La **CVaR** (Expected Shortfall) répond à la question suivante : *« et les jours où ça dépasse, je perds combien en moyenne ? »* Les régulateurs bancaires (Bâle III) l'ont préférée à la VaR, car la VaR ne dit rien de la gravité des pires jours.

> Point de rapport : si ta VaR paramétrique est **plus faible** que ta VaR historique, c'est la preuve des queues épaisses dans tes données. C'est un excellent argument critique.

### 7. Corrélations : la diversification

- **+1** : deux titres bougent toujours ensemble, donc aucune diversification ;
- **0** : aucun lien ;
- **−1** : ils se compensent parfaitement.

Plus tes titres sont **faiblement corrélés**, plus le risque global baisse. C'est le principe de Markowitz, qu'on exploitera à l'étape 7.

À noter : ton portefeuille contient un ETF MSCI World **et** des actions françaises. Or le MSCI World contient déjà… un peu de LVMH, de TotalEnergies, etc.

## E. Exercices

1. Ton **bêta** est-il supérieur ou inférieur à 1 ? Regarde la composition de ton portefeuille : cela te paraît-il logique ?
2. Compare la **VaR historique** et la **VaR paramétrique**. Laquelle est la plus élevée ? Qu'est-ce que ça dit de la distribution de tes rendements ?
3. Dans `src/config.py`, remplace l'indice par `"^FCHI"` (CAC 40), relance, puis compare l'alpha. Pourquoi est-il plus élevé ? (Indice : les dividendes.) Remets ensuite `"CW8.PA"`.
4. Sur la carte des corrélations, quelle paire de titres est la plus corrélée ? Est-ce logique (secteur, taille, zone géographique) ?

## F. Limites à mentionner dans le rapport

Un regard critique sur ses propres outils fait toujours bonne impression :

- **Taux sans risque constant**, alors qu'il a varié entre 2 % et 4 % sur la période.
- **Petit échantillon** : sur moins de 3 ans, un bêta ou un alpha reste statistiquement fragile.
- **VaR à 1 jour** : pour 10 jours, on multiplie souvent par √10, ce qui suppose des jours indépendants.
- **Rendements passés** : ils ne préjugent pas des rendements futurs.

## G. Si ça ne marche pas

| Message | Solution |
|---|---|
| `No module named 'src.config'` | `config.py` n'a pas été copié dans le dossier `src` |
| `KeyError: 'CW8.PA'` (ou autre indice) | L'indice n'a pas été téléchargé : vérifie le code dans `config.py`, supprime `data/cache_historique.csv` et relance |
| `cannot import name 'graphique_comparaison'` | `src/graphiques.py` n'a pas été remplacé |

L'**étape 6** est la plus visible : un **tableau de bord web interactif** avec Streamlit et Plotly. Tout ce qu'on a calculé s'affichera dans une vraie application ouverte dans ton navigateur. C'est ce qui fera le plus d'effet lors de la démo.
