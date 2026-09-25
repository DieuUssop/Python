# Étape 1 — Installer et faire tourner le projet

## A. Installer les outils (une seule fois)

1. **Python** : télécharge-le sur https://www.python.org/downloads/ (version 3.11 ou plus récente).
   ⚠️ Sur Windows, **coche la case « Add Python to PATH »** sur le premier écran de l'installateur.
2. **VS Code** (l'éditeur de code) : https://code.visualstudio.com/
   Une fois ouvert, va dans l'onglet Extensions (icône des 4 carrés) et installe l'extension **Python** de Microsoft.

## B. Ouvrir le projet

1. Dézippe le dossier `portfolio_tracker` où tu veux (par exemple dans `Documents`).
2. Dans VS Code : **Fichier → Ouvrir le dossier…** et choisis `portfolio_tracker`.
3. Ouvre un terminal : **Terminal → Nouveau terminal**. Il s'ouvre en bas de l'écran,
   directement dans le bon dossier.

## C. Installer les bibliothèques

Dans le terminal, tape :

```bash
pip install -r requirements.txt
```

(Si `pip` n'est pas reconnu, essaie `py -m pip install -r requirements.txt`.)

## D. Lancer le programme

```bash
python main.py
```

Tu dois obtenir :

```
POSITIONS OUVERTES
                      nom  quantite     pru  montant_investi
CW8.PA  Amundi MSCI World      15.0  433.67           6505.0
MC.PA                LVMH       5.0  724.80           3624.0
AI.PA         Air Liquide       8.0  175.25           1402.0
TTE.PA      TotalEnergies      10.0   64.10            641.0

RÉSUMÉ
Plus-values réalisées     :     -43.00 €
Dividendes perçus         :      42.20 €
...
```

Puis lance les tests :

```bash
python -m pytest
```

Résultat attendu : `6 passed`.

## E. Comprendre ce qui se passe

Lis `src/portfolio.py` : chaque ligne est commentée. Vérifie ensuite un calcul à la main :

> **TotalEnergies** : achat de 20 titres à 64 € + 2 € de frais
> → PRU = (20 × 64 + 2) / 20 = **64,10 €**
> Vente de 10 titres à 60 € avec 2 € de frais
> → plus-value = 10 × (60 − 64,10) − 2 = **−43 €** (une moins-value)

C'est exactement ce que le programme affiche.

## F. Petits exercices pour prendre la main

1. Ouvre `data/transactions.csv` et ajoute un achat de ton choix (par exemple `SAN.PA`, Sanofi). Relance `python main.py`.
2. Ajoute une vente de 20 LVMH, plus que ce que tu possèdes. Que se passe-t-il ? Pourquoi est-ce une bonne chose ?
3. Remplace le portefeuille d'exemple par un portefeuille qui vous ressemble, pour la démo finale.

Quand tout fonctionne, dis-le-moi : on passera à l'**étape 2**, la récupération des cours
en temps réel et le calcul des plus-values latentes.
