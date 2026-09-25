# Étape 6 — Le tableau de bord web interactif

## Objectif

Tout ce qu'on a calculé aux étapes 1 à 5 s'affichait dans le terminal. On le transforme maintenant en une **vraie application web**, qui s'ouvre dans ton navigateur :

- **5 chiffres clés** en haut de la page ;
- **5 onglets** : Vue d'ensemble, Positions, Performance, Risque, Transactions ;
- des **graphiques interactifs** : survol à la souris, zoom, boutons 1M / 6M / 1A / Tout ;
- des **réglages** modifiables sans toucher au code : indice de référence, taux sans risque, niveau de la VaR ;
- la possibilité d'**envoyer un autre fichier de transactions** ;
- le **téléchargement** d'une sélection de transactions.

C'est ce qui fera le plus d'effet lors de ta démonstration.

## A. Installer la mise à jour

1. Dézippe `mise_a_jour_etape6.zip` et copie son contenu dans `portfolio_tracker` (**Remplacer**).
2. Installe Streamlit et Plotly (une seule fois, ça prend 1 ou 2 minutes) :

```
python -m pip install streamlit plotly
```

Des avertissements jaunes « not on PATH » peuvent apparaître, comme pour matplotlib : ils sont sans importance.

Nouveaux fichiers : `app.py`, `src/analyse.py`, `src/graphiques_interactifs.py`, `GUIDE_ETAPE_6.md`.
Fichiers modifiés : `src/metrics.py`, `requirements.txt`, `README.md`.

## B. Lancer le tableau de bord

```
python -m streamlit run app.py
```

- **Au tout premier lancement**, Streamlit peut te demander une adresse e-mail dans le terminal : appuie simplement sur **Entrée** pour passer.
- Ton navigateur s'ouvre tout seul sur **http://localhost:8501**. Sinon, copie cette adresse dans ton navigateur.
- Le premier chargement prend quelques secondes (téléchargement des cours). Ensuite, tout est gardé en mémoire et la navigation est instantanée.

**Pour arrêter** : clique dans le terminal de VS Code et appuie sur **Ctrl + C**.

> Ce qui s'affiche sur `localhost` est visible uniquement sur ton ordinateur. Pour la soutenance, tu le lances sur ton PC et tu projettes l'écran.

## C. Visite guidée

### En haut : les 5 chiffres clés

Valeur actuelle · Gain total · Performance annualisée (TWR) · Volatilité · Max drawdown.
Survole le petit **?** à côté de chaque chiffre : une explication s'affiche.

### Barre latérale (à gauche)

| Réglage | Effet |
|---|---|
| Fichier de transactions | Envoie un autre CSV (par exemple celui d'un camarade) sans toucher au tien |
| Indice de référence | MSCI World, S&P 500, CAC 40 ou Euro Stoxx 50 : tous les indicateurs se recalculent |
| Taux sans risque | Change le Sharpe, le Sortino et l'alpha |
| Niveau de la VaR | 90 %, 95 % ou 99 % |
| 🔄 Actualiser les cours | Retélécharge les cours du jour |

### Les onglets

1. **Vue d'ensemble** : évolution de la valeur et de l'argent investi, répartition du portefeuille.
2. **Positions** : le tableau détaillé (clique sur un titre de colonne pour trier) et les plus-values ligne par ligne.
3. **Performance** : comparaison avec l'indice en base 100, rendements année par année, drawdown, bêta et alpha.
4. **Risque** : Sharpe, Sortino, VaR, CVaR, distribution des rendements et carte des corrélations.
5. **Transactions** : l'historique complet, avec des filtres et un bouton de téléchargement.

### Astuces sur les graphiques

- **Survole** une courbe pour lire la valeur exacte.
- **Clique-glisse** pour zoomer, puis **double-clique** pour revenir à la vue d'ensemble.
- **Clique sur un nom de la légende** pour masquer ou afficher une courbe.
- Les boutons **1M / 6M / YTD / 1A / Tout** changent la période affichée.

## D. Comprendre le code

### Comment marche Streamlit ?

Le fichier `app.py` est **exécuté de haut en bas à chaque interaction** (un clic, un changement de réglage…). Chaque commande `st.…` ajoute un élément à la page :

```python
st.title("📈 Suivi de portefeuille")        # un titre
c1.metric("Valeur actuelle", "45 113 €")     # un chiffre clé
st.plotly_chart(figure)                      # un graphique
```

### Le cache : `@st.cache_data`

Comme la page est relancée à chaque clic, il faudrait retélécharger les cours à chaque fois, ce qui serait très lent. Le décorateur `@st.cache_data` garde le résultat en mémoire : tant que les réglages ne changent pas, le calcul n'est pas refait.

### L'architecture du projet

```
app.py (affichage web)          main.py (affichage texte)
          \                        /
           src/analyse.py  ← enchaîne tout le calcul
                |
   portfolio.py · market_data.py · metrics.py
```

`app.py` ne contient **aucun calcul financier** : il affiche seulement les résultats. Les calculs restent dans `src/`, là où ils sont testés. C'est le principe de **séparation entre la logique et la présentation**, un vrai argument de qualité logicielle pour ton oral.

## E. Préparer la démo (conseils)

1. **La veille**, lance l'application une fois avec internet : le cache sera rempli. Si le Wi-Fi de la salle ne marche pas, l'application utilisera ces cours enregistrés (c'est indiqué dans la barre latérale).
2. Prépare un **scénario** de 3 minutes. Par exemple :
   - la Vue d'ensemble, pour dire ce que vaut le portefeuille et ce qu'il a rapporté ;
   - l'onglet Performance, pour montrer si on bat le marché ;
   - changer l'indice pour le CAC 40 en direct, et expliquer pourquoi l'alpha change (les dividendes) ;
   - l'onglet Risque, pour montrer ce qu'on risque de perdre un mauvais jour.
3. Mets le navigateur en **plein écran** (touche F11).

## F. Exercices

1. Dans la barre latérale, passe le taux sans risque de 2,5 % à 4 %. Comment évolue le Sharpe ? Pourquoi ?
2. Passe la VaR de 95 % à 99 %. La perte augmente-t-elle beaucoup ? Relie ta réponse aux « queues épaisses ».
3. **Personnalisation** : dans `app.py`, change le titre de la page (`st.title(...)`) pour y mettre le nom de votre groupe. Sauvegarde : la page se met à jour (clique sur « Rerun » en haut à droite si besoin).

## G. Si ça ne marche pas

| Problème | Solution |
|---|---|
| `No module named streamlit` | `python -m pip install streamlit plotly` |
| `streamlit` n'est pas reconnu | Utilise bien `python -m streamlit run app.py` (et pas `streamlit run app.py`) |
| Le navigateur ne s'ouvre pas | Ouvre toi-même http://localhost:8501 |
| `TypeError: ... unexpected keyword argument 'width'` | Streamlit est trop ancien : `python -m pip install --upgrade streamlit` |
| Message rouge « Impossible d'analyser le portefeuille » | Lis le message : c'est la même erreur qu'afficherait `python main.py` |
| Rien ne change après une modification du CSV | Clique sur 🔄 **Actualiser les cours** |

Quand ça tourne, **envoie-moi des captures d'écran de chaque onglet**. Je n'ai pas pu voir le rendu visuel de mon côté : on ajustera ensemble ce qui ne te plaît pas (couleurs, tailles, ordre).

Prochaine étape, la **7** : l'optimisation de Markowitz, avec la frontière efficiente et le portefeuille optimal. C'est le sommet théorique du projet.
