# Le portefeuille diversifié (actions, obligations, or)

## Ce qu'il apporte

Les deux premiers portefeuilles ne contiennent que des actions. Un conseiller propose pourtant rarement 100 % d'actions à un client. Le troisième portefeuille est **multi-actifs**, comme un mandat de gestion « Équilibré » :

| Classe d'actifs | Poids cible | Contenu |
|---|---|---|
| **Actions** | 60 % | 39 sociétés, 8 régions, les 11 secteurs (équipondérées dans chaque région) |
| **Obligations** | 35 % | 10 fonds indiciels (ETF) : États de la zone euro (1-3 ans et toutes maturités), États-Unis (7-10 ans et 20 ans et plus), obligations indexées sur l'inflation, entreprises bien notées (euro et dollar), haut rendement, pays émergents |
| **Or** | 5 % | Xetra-Gold (or physique) |

Il est géré **depuis le 16 janvier 2017**, soit près de 10 ans. Les étapes de gestion :
- 500 000 € investis au départ ;
- chaque trimestre, un versement de 10 000 € et un rééquilibrage vers l'allocation cible ;
- les vrais dividendes et coupons encaissés.

## A. Installer

1. Dézippe la mise à jour et copie son contenu dans `portfolio_tracker` en choisissant **Remplacer**. Ton `transactions.csv` n'est pas dans le zip.
2. Crée le portefeuille (connexion Internet nécessaire, 1 à 2 minutes) :
   ```
   python generer_portefeuille_diversifie.py
   ```
   Le fichier `data/transactions_diversifie.csv` est créé. Environ 900 opérations sont attendues : achats, ventes de rééquilibrage, dividendes et coupons.
3. Lance les tests avec `python -m pytest`. Résultat attendu : **79 passed**.
4. Choisis **« Portefeuille diversifié (multi-actifs) »** dans la barre latérale du tableau de bord, ou lance :
   ```
   python main.py data/transactions_diversifie.csv
   ```
5. **Pour le site en ligne** : dans GitHub Desktop, fais **Commit to main** puis **Push origin**. Le fichier `transactions_diversifie.csv` doit partir avec les autres fichiers. Sinon, le portefeuille n'apparaîtra pas en ligne.

## B. Pourquoi des obligations ? (à savoir expliquer à l'oral)

1. **Adéquation au client.** Le profil « Équilibré » accepte au plus 60 % d'actions et 12 % de volatilité. Un portefeuille 100 % actions ne convient donc qu'aux profils Dynamique et Offensif. Avec des obligations, l'outil peut enfin montrer un portefeuille **adapté** à un client prudent ou équilibré.
2. **Diversification.** Les emprunts d'État montent souvent quand les actions chutent : en 2008 ou en 2020, ils ont amorti les pertes. Attention : **en 2022, actions et obligations ont baissé ensemble** à cause de la hausse des taux. C'est un exemple parfait pour discuter des limites de la diversification.
3. **Le risque de taux.** Une obligation perd de la valeur quand les taux montent. La **duration** mesure cette sensibilité : un fonds de duration 7 ans perd environ 7 % si les taux montent d'un point. L'outil ajoute ce choc aux stress tests.
4. **L'or** sert de valeur refuge : il est peu corrélé aux actions et aux obligations.

## C. Ce qui change dans l'outil

| Écran | Changement |
|---|---|
| Vue d'ensemble | Nouveau graphique **« Par classe d'actifs »** ; colonne « Classe » dans les positions |
| Profil client | La **part d'actions** est calculée (avant, elle valait 100 % par hypothèse) |
| Fiscalité | Les fonds obligataires et l'or ne sont **pas éligibles au PEA**, réservé aux actions. Les coupons sont traités comme des dividendes. |
| Stress tests | Nouveau choc **« Hausse des taux de 1 point »**. Une obligation sans historique en 2008 est approchée par un **fonds obligataire** de même catégorie, et non par un indice actions. |
| Attribution | Calculée sur la **poche actions** seulement, puisque l'indice de référence est un indice actions |
| Budget de risque, Markowitz | Fonctionnent tels quels : les obligations apportent peu de risque par euro investi |

Tout repose sur deux nouvelles colonnes de `data/referentiel.csv` : `classe` (Actions, Obligations, Or) et `duration` (en années, valeur approximative à vérifier sur la fiche de chaque fonds).

## D. Exercices

1. Dans l'onglet Profil client, avec le profil Équilibré, le portefeuille diversifié est-il adapté ? Et le fonds actions monde ? Quel critère fait la différence ?
2. Compare la volatilité et la pire baisse du portefeuille diversifié avec celles du fonds actions monde.
3. Dans les stress tests, quelle crise pèse le plus sur le portefeuille diversifié ? Pourquoi 2022 est-elle particulière ?
4. Dans le budget de risque, quelle part du **risque** viennent des obligations, comparée à leur part de la **valeur** (35 %) ?
5. Le portefeuille dépasse 8 ans : dans l'onglet Fiscalité, compare le gain net en compte-titres, en PEA et en assurance-vie. Pourquoi le PEA serait-il difficile à utiliser ici ?

## E. Si ça ne marche pas

| Problème | Solution |
|---|---|
| « Titres introuvables, retirés » | Un code n'est plus reconnu par Yahoo Finance : les poids des autres lignes sont ajustés, le portefeuille reste utilisable |
| Le portefeuille n'apparaît pas en ligne | `data/transactions_diversifie.csv` n'a pas été envoyé : Commit puis Push dans GitHub Desktop |
| Le premier chargement est long | 10 ans de cours pour 50 lignes : c'est normal. Ensuite le cache prend le relais |
