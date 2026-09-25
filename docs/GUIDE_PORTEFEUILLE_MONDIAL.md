# Portefeuille actions monde et nuage de points Monte-Carlo

## Ce que contient cette mise à jour

1. **Un portefeuille d'actions mondiales géré comme par un asset manager** : 69 actions, 8 devises, environ 550 opérations.
2. **Un référentiel des titres** (`data/referentiel.csv`) : la région, le secteur et le pays de chaque titre. Le tableau de bord et le rapport PDF affichent désormais la répartition par région et par secteur.
3. **Un nouvel affichage de la projection Monte-Carlo** : un nuage de points coloré par tranche de probabilité, en plus de l'éventail.

## A. Installer

1. Dézippe `mise_a_jour_portefeuille_mondial.zip` et copie son contenu dans `portfolio_tracker` (**Remplacer**).
   Ton fichier `data/transactions.csv` n'est pas touché. Seul `data/referentiel.csv` est ajouté.
2. Crée le portefeuille mondial (il faut Internet, compter 1 à 2 minutes) :

```
python generer_portefeuille_mondial.py
```

Résultat attendu :

```
⏳ Univers : 69 actions dans 8 régions
⏳ Téléchargement des cours et de 8 taux de change (AUD, CAD, CHF, DKK, GBP, HKD, JPY, USD)...
✅ 11 dates de gestion : investissement initial + 10 rééquilibrages
⏳ Récupération des dividendes (une requête par titre, patience)...
✅ data/transactions_mondial.csv créé : ... opérations
```

3. Analyse-le :
   - **en texte** : `python main.py data/transactions_mondial.csv` ;
   - **dans le tableau de bord** : `python -m streamlit run app.py`, puis choisis **« Portefeuille actions monde »** dans la liste « Portefeuille » de la barre latérale.

4. Tests : `python -m pytest`. Résultat attendu : **55 passed**.

## B. La politique de gestion simulée

Le script reproduit la gestion d'un **fonds actions monde** :

| Élément | Choix | Pourquoi |
|---|---|---|
| Allocation par région | États-Unis 55 %, Europe 18 %, Japon 6 %, Royaume-Uni 5 %, Émergents 5 %, Suisse 4 %, Asie-Pacifique 4 %, Canada 3 % | Proche du poids des pays dans le MSCI World, avec une poche d'émergents |
| Dans chaque région | Titres équipondérés | Règle simple, qui évite de concentrer le fonds sur les plus grosses capitalisations |
| Capital initial | 2 000 000 € le 15/01/2024 | Taille d'un petit mandat de gestion |
| Souscriptions | 100 000 € par trimestre | Arrivée de nouveaux clients |
| Rééquilibrage | Chaque trimestre, si une ligne s'écarte de plus de 10 % de sa cible | La bande de tolérance évite des transactions inutiles (et leurs frais) |
| Frais | 0,05 % du montant, minimum 5 € | Barème institutionnel |
| Émergents | Via des ADR (actions cotées à New York, en dollars) | Pratique courante, qui évite de gérer 4 devises de plus |

**À dire à l'oral** : le rééquilibrage revient à vendre ce qui a monté et à acheter ce qui a baissé. C'est une discipline **contrariante**, qui maintient le profil de risque voulu.

## C. Le nuage de points Monte-Carlo

Dans l'onglet **Projection**, le sélecteur **Affichage** propose : *Éventail*, *Nuage de points*, *Les deux*.

Dans le nuage, **chaque point est un scénario simulé** à une date donnée (tous les 6 mois). On en affiche 400, tirés parmi les 5 000. Sa couleur indique sa **tranche de probabilité** à cette date, par rapport à l'ensemble des 5 000 scénarios :

| Couleur | Tranche | Lecture |
|---|---|---|
| Rouge foncé | 5 % les plus défavorables | 1 scénario sur 20 fait pire que ce seuil |
| Rouge clair | 5 à 25 % | Défavorable |
| Gris | 25 à 75 % | La moitié centrale des scénarios |
| Bleu clair | 75 à 95 % | Favorable |
| Bleu foncé | 5 % les plus favorables | 1 scénario sur 20 fait mieux |

Survole un point pour voir son numéro de scénario, sa date et sa valeur.

**Ce que le nuage montre mieux que l'éventail :**

- la **dispersion réelle** des scénarios, qui s'étale de plus en plus avec le temps ;
- l'**asymétrie** : les points bleus montent beaucoup plus haut que les rouges ne descendent. Avec des rendements composés, les gains ne sont pas plafonnés alors que les pertes le sont (on ne peut pas perdre plus de 100 %) : c'est la **loi log-normale** ;
- les **scénarios extrêmes**, un par un.

Le rapport PDF contient les deux graphiques sur la page de projection.

## D. Adaptations pour un grand portefeuille

Avec 69 lignes, certains affichages devenaient illisibles. Ils s'adaptent donc automatiquement :

- **Répartition** : les 14 plus grosses lignes, les autres sont regroupées dans « Autres ».
- **Nouveaux graphiques** : répartition par région et par secteur.
- **Corrélations** : au-delà de 15 titres, la carte n'affiche plus les chiffres (le survol les donne). Dans le PDF, elle est remplacée par la corrélation moyenne et les tableaux de répartition.
- **Markowitz** : les noms des titres ne s'affichent plus sur la frontière et le graphique des poids se limite aux 25 lignes principales.

## E. Exercices

1. Compare **« Mon portefeuille »** et **« Portefeuille actions monde »** dans le tableau de bord : lequel a la meilleure volatilité ? le meilleur Sharpe ? Relie ta réponse à la diversification (corrélation moyenne).
2. Dans l'onglet **Risque**, quelle est la VaR du portefeuille mondial ? Pourquoi est-elle plus faible en pourcentage que celle d'une action seule ?
3. Dans l'onglet **Optimisation**, choisis un poids maximal de **10 %** (la règle des fonds OPCVM). Combien de titres garde l'optimiseur ?
4. Dans **Projection**, affiche le nuage de points sur 20 ans. Les points rouges passent-ils sous la ligne orange (argent investi) ? À partir de quel horizon n'y en a-t-il presque plus ?
5. Modifie `POIDS_REGIONS` en haut de `generer_portefeuille_mondial.py` (par exemple 40 % États-Unis et 33 % Europe), relance-le et compare les résultats.

## F. Si ça ne marche pas

| Problème | Solution |
|---|---|
| « Titres introuvables, retirés de l'univers » | Normal si Yahoo ne connaît plus un ticker : le script continue sans lui et répartit son poids sur les autres |
| Le script est long | Il fait une requête de dividendes par titre (69) : 1 à 2 minutes, c'est normal |
| Le tableau de bord est lent au premier chargement | Normal avec 69 titres (téléchargement + optimisation). Ensuite, le cache le rend instantané |
| « Portefeuille actions monde » n'apparaît pas dans la liste | Lance d'abord `python generer_portefeuille_mondial.py` |
