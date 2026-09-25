# Liste de contrôle avant le rendu

## 1. Le code

- [ ] `python -m pytest` affiche **74 passed**
- [ ] `python main.py` fonctionne et crée `rapport_portefeuille.pdf`
- [ ] `python main.py data/transactions_mondial.csv` fonctionne
- [ ] Le tableau de bord s'ouvre (`lancer_tableau_de_bord.bat`) et les 3 espaces (analyse, conseil patrimonial, gestion d'actifs) s'affichent
- [ ] Les noms du groupe sont indiqués en haut du `README.md`

## 2. Le rapport écrit (Rapport_projet_portefeuille.docx)

- [ ] Page de garde : université, noms, enseignant
- [ ] Toutes les zones **surlignées en jaune** sont complétées avec vos vrais chiffres
      (astuce Word : Ctrl + F, puis rechercher « à compléter » et « Insérer ici »)
- [ ] Les encadrés « À rédiger par le groupe » sont rédigés, puis l'encadré jaune est supprimé
- [ ] Les graphiques sont insérés (fichiers `graphique_*.png` créés par `python main.py`)
- [ ] Le sommaire est à jour (clic droit sur le sommaire > Mettre à jour les champs > Mettre à jour toute la table)
- [ ] Relecture complète, puis export en PDF (Fichier > Enregistrer sous > PDF)

## 3. L'archive du projet à rendre

1. **Supprimer** les fichiers produits automatiquement (ils seront recréés au lancement) :
   `data/cache_*.csv`, `data/historique.csv`, `data/transactions_sauvegarde.csv`, les dossiers `__pycache__`.
2. **Garder** : tout le reste, y compris `data/transactions.csv`, `data/transactions_mondial.csv`,
   `data/referentiel.csv`, et éventuellement `rapport_portefeuille.pdf` comme exemple de sortie.
3. Clic droit sur le dossier `portfolio_tracker` > **Compresser vers > Fichier ZIP**.
4. Tester l'archive : la décompresser dans un autre dossier et lancer `python -m pytest`.

## 4. La veille de la soutenance

- [ ] Lancer le tableau de bord **avec Internet** pour remplir le cache (au cas où le Wi-Fi ne marcherait pas)
- [ ] Préparer le scénario de démonstration (voir docs/GUIDE_ETAPE_6.md, partie E)
- [ ] Avoir le rapport PDF et quelques captures d'écran en secours sur une clé USB
