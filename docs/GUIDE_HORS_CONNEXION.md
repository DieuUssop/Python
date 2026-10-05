# Guide — Mode hors connexion et espace personnel chiffré

Ce guide explique les deux nouveautés demandées :

1. **l'application fonctionne sans Internet**, grâce à une base locale de titres ;
2. **chaque utilisateur a son espace personnel**, chiffré : il est le seul à pouvoir lire
   les portefeuilles qu'il y enregistre.

---

## 1. La base locale de titres

### Ce qu'elle contient

Le dossier `data/base/` contient :

| Fichier | Contenu |
|---|---|
| `titres.csv` | La fiche de chaque titre : ticker Yahoo, nom, ISIN (quand il est connu), pays, région, secteur, classe d'actifs, devise, indices dont il fait partie |
| `cours/paquet_00.npz` … `paquet_31.npz` | Les cours de clôture quotidiens, rangés en 32 paquets compressés |
| `memoire.csv` | La mémoire des titres reconnus : chaque ISIN, nom ou code Bloomberg déjà converti en ticker Yahoo |
| `pays.geojson` | Les contours des pays, pour que la carte du monde s'affiche sans Internet (téléchargés une fois) |

L'univers couvert (≈ 3 500 actions) : S&P 500, Russell 1000, Nasdaq-100, CAC 40, SBF 120,
DAX, MDAX, SDAX, FTSE 100, FTSE 250, Euro Stoxx 50, AEX, BEL 20, IBEX 35, FTSE MIB, SMI,
indices nordiques, ATX, PSI, ISEQ, Nikkei 225, S&P/TSX 60, S&P/ASX 200, Hang Seng ; une
soixantaine d'ETF courants (actions, obligations, or) ; les grands indices et les taux de
change.

Historique : depuis 2015 pour les titres, depuis 2007 pour les indices et les taux de change
(utile aux stress tests 2008).

### La construire (une seule fois, avec Internet)

**Windows** : double-cliquer sur `construire_base.bat`.
**Ou dans le terminal VS Code** :

```bash
python -m pip install -r requirements.txt     # si ce n'est pas déjà fait (lxml, cryptography)
python construire_base_titres.py
```

- Durée : **environ 1 heure** (les cours sont téléchargés par lots de 100 titres, avec des
  pauses pour ne pas être bloqué par Yahoo Finance).
- Si c'est interrompu (fenêtre fermée, coupure Internet) : relancer la même commande, le
  téléchargement **reprend là où il s'était arrêté**.
- Taille finale : 40 à 60 Mo, en fichiers d'1 à 2 Mo (GitHub accepte, la limite est de
  100 Mo par fichier).
- Les tickers que Yahoo ne reconnaît pas sont listés dans `data/base/echecs.csv` (quelques
  dizaines, c'est normal : sociétés rachetées, tickers changés).

### La mettre à jour

```bash
python construire_base_titres.py --mise-a-jour
```

Quelques minutes : seuls les derniers jours sont ajoutés. `construire_base.bat` choisit
automatiquement entre construction et mise à jour.

### La base se remplit aussi toute seule

C'est une base **cumulative** : à chaque utilisation avec Internet, les cours téléchargés pour
analyser un portefeuille y sont ajoutés (l'ancien cache était remplacé à chaque fois). Et chaque
titre reconnu à l'import (ISIN, nom, code Bloomberg) est ajouté à la mémoire : la prochaine fois,
il est reconnu instantanément, même sans Internet.

---

## 2. Ce qui marche hors connexion

| Situation | Avec Internet | Sans Internet |
|---|---|---|
| Ouvrir le tableau de bord | ✅ | ✅ |
| Analyser un portefeuille dont les titres sont dans la base | ✅ cours du jour | ✅ cours jusqu'à la dernière mise à jour de la base |
| Titre absent de la base | ✅ téléchargé, puis ajouté à la base | ❌ message clair : titre sans cours |
| Importer un fichier Excel / CSV | ✅ | ✅ (lecture, détection des colonnes et des dates : tout est local) |
| Ticker Yahoo, Bloomberg (`MC FP Equity`), Google (`EPA:MC`), Reuters (`MC.PA`) | ✅ | ✅ (conversion par règles, sans Internet) |
| Code ISIN | ✅ | ✅ s'il est dans la base ou dans la mémoire |
| Nom de société (« LVMH ») | ✅ | ✅ s'il est dans la base ou dans la mémoire |
| Ticker sans place (`MC`, `ASML`) | ✅ | ✅ si le titre est dans la base (place retrouvée en comparant les prix) |
| Conversion des devises en euros | ✅ | ✅ (taux de change dans la base) |
| Indice de référence, stress tests, attribution | ✅ | ✅ (indices dans la base) |
| Espace personnel (comptes) | ✅ | ✅ |

Le tableau de bord indique la source des cours : « Yahoo Finance » ou « cache local (Yahoo
Finance injoignable) ».

### Lancer l'application sans Internet

Exactement comme d'habitude : double-cliquer sur `lancer_tableau_de_bord.bat` (ou
`python -m streamlit run app.py` dans le terminal VS Code). L'adresse `http://localhost:8501`
est sur l'ordinateur lui-même : aucune connexion n'est nécessaire.

La toute première fois seulement, `lancer_tableau_de_bord.bat` installe les bibliothèques
(il faut alors Internet) ; il crée ensuite un petit fichier `.installe` pour ne plus le refaire.

---

## 3. L'espace personnel chiffré

### Pour l'utilisateur

1. Barre latérale → **Mon espace** → *Se connecter ou créer un compte*.
2. Créer un compte : identifiant (3 à 30 caractères : minuscules, chiffres, `.`, `_`, `-`) et
   mot de passe (8 caractères minimum).
3. Enregistrer un portefeuille, au choix :
   - envoyer le fichier (CSV ou Excel) dans la barre latérale : une fois lu, un encadré
     **Enregistrer dans mon espace** apparaît juste sous l'envoi ;
   - ou **Mon compte** → *Ajouter un portefeuille* → choisir le fichier → *Enregistrer*.

   Le portefeuille est enregistré au format du projet (après conversion), et chiffré.
4. Ses portefeuilles apparaissent ensuite dans la liste des portefeuilles, sous la forme
   « Mon espace · nom ».
5. **Mon compte** : renommer, télécharger, supprimer un portefeuille ; changer de mot de passe ;
   supprimer le compte.

Déconnexion automatique après 30 minutes d'inactivité.

### Comment c'est protégé

| Menace | Protection |
|---|---|
| Quelqu'un lit le fichier des comptes | Il n'y a **aucun mot de passe** dedans : seulement une *empreinte* (PBKDF2-HMAC-SHA256, 600 000 itérations, sel aléatoire par compte). Retrouver le mot de passe à partir de l'empreinte prendrait des années. |
| Quelqu'un ouvre les fichiers d'un autre | Les portefeuilles sont **chiffrés** (Fernet : AES-128 + code d'authentification) avec une clé tirée du mot de passe. Sans le mot de passe, ils sont illisibles — même pour l'administrateur. |
| Un fichier chiffré est modifié | Le code d'authentification le détecte : le fichier est refusé, pas lu de travers. |
| Quelqu'un essaie des mots de passe | Chaque essai prend ≈ 0,5 s, et le compte est bloqué 1 minute après 5 échecs. |
| Quelqu'un cherche quels comptes existent | Même message pour un identifiant inconnu et un mauvais mot de passe, même durée de calcul. |
| Les noms des portefeuilles trahissent quelque chose | La liste des portefeuilles est elle aussi chiffrée ; les dossiers ont des noms aléatoires. |

La clé de chiffrement n'est **jamais écrite sur le disque** : elle n'existe qu'en mémoire,
pendant la session, et disparaît à la déconnexion.

### La contrepartie : mot de passe oublié = données perdues

C'est voulu : s'il existait un moyen de récupérer les données sans le mot de passe,
l'administrateur (ou un pirate) pourrait l'utiliser aussi. Conseil aux utilisateurs : garder
une copie de leurs fichiers (bouton *Télécharger* de la page « Mon compte »).

### Le lien avec le RGPD

- **Article 25 (protection des données dès la conception)** : chiffrement par défaut,
  aucune donnée en clair, aucun mot de passe stocké.
- **Article 32 (sécurité du traitement)** : chiffrement, empreintes salées, limitation des
  essais.
- **Article 17 (droit à l'effacement)** : bouton « Supprimer définitivement mon compte ».
- Les données restent sur l'ordinateur (ou le serveur privé) où l'application est installée :
  aucun envoi à un tiers. Seuls les tickers des titres sont envoyés à Yahoo Finance pour
  obtenir les cours, jamais les quantités ni les montants.

### Où sont les données

```
data/comptes/
├── comptes.json      identifiants, sels, empreintes (aucun mot de passe, aucune donnée)
└── 3f9a2c.../        un dossier par compte, au nom aléatoire
    ├── index.enc     liste chiffrée des portefeuilles
    └── 8b1e....enc   chaque portefeuille, chiffré
```

`data/comptes/` est dans `.gitignore` : **il n'est jamais envoyé sur GitHub**.

### Et sur le site en ligne ?

Sur Streamlit Community Cloud, le disque est effacé à chaque redémarrage du site : les comptes
y sont donc temporaires (un avertissement l'indique). L'espace personnel est fait pour :

- l'application installée sur l'ordinateur de chacun (le plus simple) ;
- ou un serveur privé de l'école (un seul serveur, plusieurs utilisateurs : chacun ne voit que
  ses propres portefeuilles).

---

## 4. Vérifier que tout marche

```bash
python -m pytest
```

Résultat attendu : **135 passed** (dont 9 tests sur les comptes — mauvais mot de passe refusé,
données d'un autre illisibles, fichier modifié détecté, blocage après 5 essais, changement de mot
de passe… — et 5 tests sur la base de titres).

Puis, pour tester le hors connexion : construire la base, couper le Wi-Fi, lancer
`lancer_tableau_de_bord.bat` et analyser un portefeuille.
