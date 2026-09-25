# Étape 2 — Récupérer les cours de bourse et valoriser le portefeuille

## Objectif

À l'étape 1, le programme savait combien tu avais **investi**. Il va maintenant calculer combien ton portefeuille **vaut aujourd'hui**, grâce aux cours de Yahoo Finance :

- la **valeur** de chaque ligne = quantité × cours actuel ;
- la **plus-value latente** = valeur − montant investi (ce que tu gagnerais si tu vendais tout aujourd'hui) ;
- le **poids** de chaque ligne dans le portefeuille ;
- le **gain total** = plus-values latentes + plus-values réalisées + dividendes.

## A. Installer la mise à jour

Le zip `mise_a_jour_etape2.zip` contient **uniquement les fichiers modifiés ou nouveaux**. Ton fichier `data/transactions.csv` (avec Sanofi) n'est pas touché.

1. Dézippe `mise_a_jour_etape2.zip` (clic droit → **Extraire tout…**).
2. Ouvre le dossier extrait : il contient `main.py`, `README.md`, `GUIDE_ETAPE_2.md`, un dossier `src` et un dossier `tests`.
3. Sélectionne tout (**Ctrl + A**), copie (**Ctrl + C**), va dans ton dossier `portfolio_tracker` et colle (**Ctrl + V**).
4. Windows te demande quoi faire des fichiers qui existent déjà : choisis **Remplacer les fichiers dans la destination**.

Nouveau fichier : `src/market_data.py`.
Fichiers modifiés : `src/portfolio.py`, `main.py`, `tests/test_portfolio.py`, `README.md`.

## B. Vérifier que yfinance est installé

Tu l'as normalement installé à l'étape 1 avec `requirements.txt`. Pour vérifier, tape dans le terminal VS Code :

```
pip install yfinance
```

Si tu vois « Requirement already satisfied », c'est bon.

## C. Lancer le programme

```
python main.py
```

Tu dois voir un tableau comme celui-ci (**tes chiffres seront différents** : ce sont les vrais cours du jour) :

```
Source des cours : Yahoo Finance (en direct)

POSITIONS VALORISÉES
                      nom   qté     pru  cours  valeur  +/- value €  +/- value %  poids %
CW8.PA  Amundi MSCI World  15.0  433.67  560.0  8400.0       1895.0        29.13    57.28
MC.PA                LVMH   5.0  724.80  610.0  3050.0       -574.0       -15.84    20.80
...

RÉSUMÉ
Montant investi (au PRU)  :    13,642.00 €
Valeur actuelle           :    14,664.00 €
Plus-values latentes      :     1,022.00 €
...
GAIN TOTAL                :     1,127.60 €
```

Puis lance les tests : `python -m pytest`. Résultat attendu : **10 passed**.

## D. Comprendre le nouveau code

### `src/market_data.py` : aller chercher les cours

- `yf.download(...)` interroge Yahoo Finance.
- On demande les **5 derniers jours** et pas seulement aujourd'hui : le week-end ou un jour férié, la bourse est fermée. On prend alors le dernier cours connu.
- **Le cache** : à chaque fois que les cours sont récupérés, ils sont enregistrés dans `data/cache_prix.csv`. Si Internet ne marche pas, le programme utilise ces cours enregistrés et l'indique clairement. C'est une sécurité pour la soutenance, si le Wi-Fi de la salle ne fonctionne pas.

### `src/portfolio.py` : la nouvelle méthode `valoriser(prix)`

La classe `Portfolio` ne va **pas** chercher les cours elle-même : elle les **reçoit**. C'est le principe de **séparation des responsabilités** :

- `market_data.py` s'occupe des **données** ;
- `portfolio.py` s'occupe des **calculs**.

Avantage concret : les tests fonctionnent **sans Internet**, avec des cours inventés dont on connaît le résultat. C'est un argument fort à présenter au professeur.

## E. Vérifie un calcul à la main

Avec les chiffres de l'exemple ci-dessus, pour **LVMH** :

- valeur = 5 × 610 = **3 050 €**
- plus-value latente = 3 050 − 3 624 = **−574 €**
- en % : −574 / 3 624 = **−15,84 %**

Refais le même calcul avec **tes** chiffres pour une ligne de ton choix.

## F. Exercices

1. **Test hors ligne** : coupe ton Wi-Fi et relance `python main.py`. Le programme doit afficher « cache local du … (Yahoo Finance injoignable) ». Rallume le Wi-Fi ensuite.
2. **Ticker erroné** : ajoute un achat avec le ticker `XXXX.PA` (qui n'existe pas). Que se passe-t-il ? Supprime ensuite la ligne.
3. **Question de réflexion (pour le rapport)** : la plus-value latente ne tient pas compte des frais de vente ni des impôts (flat tax de 30 % sur un compte-titres, régime spécifique en PEA). Comment pourrait-on afficher une plus-value **nette** ?

## G. Si ça ne marche pas

| Message | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'yfinance'` | `pip install yfinance` |
| `No module named 'src.market_data'` | Le fichier `market_data.py` n'a pas été copié dans le dossier `src` |
| `Impossible de récupérer les cours ... aucun cache` | Pas d'Internet lors du tout premier lancement : vérifie ta connexion |
| `Cours manquant pour : [...]` | Le ticker est mal écrit ou n'existe pas sur Yahoo Finance |

Quand tout fonctionne, envoie-moi une capture du résultat. On passera à l'**étape 3** : reconstruire la valeur du portefeuille **jour par jour** depuis ton premier achat. C'est indispensable pour calculer les rendements et le risque, et pour tracer la courbe d'évolution.
