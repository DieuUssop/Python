# Guide — L'installateur Windows (un seul fichier à partager)

Objectif : que chacun puisse installer Portfolio Tracker **comme n'importe quel logiciel**
(« Suivant, Suivant, Terminer »), sans installer Python, sans copier de dossier, et l'utiliser
**hors connexion**, avec ses portefeuilles chiffrés dans son espace personnel.

---

## Partie 1 — Fabriquer l'installateur (toi, une fois par version)

### Avant de commencer

- Un PC Windows 10 ou 11 (64 bits) avec Internet.
- La base de titres construite : `construire_base.bat` (≈ 1 h la première fois). Sinon,
  l'application installée aura besoin d'Internet pour les cours (le script te prévient).
- Environ 2 Go d'espace libre pendant la fabrication.

### Fabrication

1. Double-cliquer sur **`fabriquer_installateur.bat`** (à la racine du projet).
2. Attendre 10 à 20 minutes. Le script affiche ses 7 étapes :

| Étape | Ce qui se passe |
|---|---|
| 1. Base de titres | Vérifie que `data\base` est construite |
| 2. Inno Setup | Installe (une seule fois, gratuit) le logiciel qui fabrique les installateurs |
| 3. Python embarqué | Télécharge une version de Python qui tient dans un dossier |
| 4. Copie du projet | Copie le projet **sans** les comptes (`data\comptes`), les tests ni les fichiers de travail |
| 5. Bibliothèques | Installe Streamlit, pandas, etc. dans ce Python embarqué |
| 6. Vérification | Vérifie que tout s'importe |
| 7. Installateur | Fabrique `installateur_windows\Installer_Portfolio_Tracker.exe` |

3. À la fin, l'explorateur s'ouvre sur le dossier `installateur_windows` : le fichier
   **`Installer_Portfolio_Tracker.exe`** (≈ 200 Mo) est le seul fichier à partager.

### Partager le fichier

Il est trop lourd pour un mail. Au choix :

- **OneDrive / Google Drive / WeTransfer** : envoyer le lien ;
- **GitHub, « Release »** (limite 2 Go par fichier) : sur la page du dépôt → *Releases* →
  *Draft a new release* → glisser le `.exe` → *Publish*. Le lien de téléchargement est
  permanent, et chaque nouvelle version y est rangée.

Le `.exe` n'est **pas** envoyé dans le dépôt lui-même (il dépasse la limite de 100 Mo par
fichier) : le `.gitignore` exclut `installateur_windows/` et `build_installateur/`.

### Nouvelle version

Après une modification du projet : relancer `fabriquer_installateur.bat` (plus rapide la
deuxième fois, les téléchargements sont gardés) et repartager le nouveau fichier. Chacun
l'installe par-dessus l'ancienne version : **ses comptes et portefeuilles sont conservés**.

---

## Partie 1 bis — Faire fabriquer Windows ET Mac par GitHub (recommandé)

Un Mac est nécessaire pour fabriquer une application Mac : GitHub en prête un
gratuitement. Le fichier `.github/workflows/installateurs.yml` (déjà dans le projet)
fabrique **les deux installateurs** sur les machines de GitHub — ton PC n'est pas utilisé.

1. Envoie le projet sur GitHub (Commit + Push dans GitHub Desktop), base de titres comprise.
2. Sur la page du dépôt : onglet **Actions** → **Fabriquer les installateurs** →
   bouton **Run workflow** → **Run workflow**.
   (La première fois, GitHub peut demander d'activer les Actions : bouton vert « I understand… ».)
3. Attendre 20 à 40 minutes (pastille jaune → verte).
4. Onglet **Releases** : une nouvelle version contient
   - `Installer_Portfolio_Tracker.exe` (Windows),
   - `Portfolio_Tracker_Mac.dmg` (Mac Apple Silicon).
   C'est le lien de cette Release qu'il suffit de partager.

En cas d'échec (pastille rouge) : cliquer sur l'étape en rouge et m'envoyer une capture du message.
Dépôt public : gratuit et illimité. Dépôt privé : quota gratuit de GitHub (suffisant pour
quelques fabrications par mois ; une fabrication Mac compte pour 10 fois sa durée).

### Installation sur Mac (les utilisateurs)

1. Ouvrir `Portfolio_Tracker_Mac.dmg` et glisser **Portfolio Tracker** sur **Applications**.
2. Première ouverture (application hors App Store, non signée par Apple) :
   - macOS 15 et plus : Réglages Système → Confidentialité et sécurité → **Ouvrir quand même** ;
   - macOS 12 à 14 : clic droit sur l'application → **Ouvrir** → **Ouvrir**.
3. Une fenêtre **Terminal** s'ouvre (l'équivalent de la fenêtre noire de Windows) puis le tableau
   de bord. Fermer le Terminal pour quitter.
4. Données : `~/Library/Application Support/Portfolio Tracker` (comptes chiffrés, conservés lors
   d'une mise à jour : il suffit de remplacer l'application dans Applications).

Mac Intel (avant fin 2020) : non pris en charge par cette application, utiliser le site en ligne.

## Partie 2 — Installer Portfolio Tracker (les utilisateurs)

1. Double-cliquer sur `Installer_Portfolio_Tracker.exe`.
2. Windows peut afficher **« Windows a protégé votre ordinateur »** (programme non signé,
   éditeur inconnu) : cliquer sur **Informations complémentaires**, puis **Exécuter quand même**.
3. Suivant → (cocher « Créer une icône sur le Bureau ») → Installer → Terminer.
   Aucun mot de passe administrateur n'est demandé.
4. Le tableau de bord s'ouvre dans **sa propre fenêtre**, comme un logiciel (Microsoft Edge en mode
   « application », sans barre d'adresse ni onglets ; à défaut, dans le navigateur habituel).

Ensuite : icône **Portfolio Tracker** sur le Bureau ou dans le menu Démarrer.

- Une petite fenêtre noire s'ouvre avec le tableau de bord : **la laisser ouverte** pendant
  l'utilisation, **la fermer pour quitter**.
- Le tableau de bord fonctionne **sur cet ordinateur uniquement** (adresse `localhost`) :
  personne d'autre sur le réseau (Wi-Fi de l'école…) ne peut s'y connecter.
- Sans Internet, tout fonctionne avec les cours de la base livrée avec l'installateur.

### Où sont les données ?

`C:\Users\<nom>\AppData\Local\Programs\Portfolio Tracker\`

- `data\comptes\` : les comptes et portefeuilles **chiffrés** de chaque utilisateur de cet ordinateur ;
- `data\base\` : la base de titres et sa mémoire.

### Désinstaller

Paramètres Windows → Applications → Portfolio Tracker → Désinstaller. Une question est posée :
supprimer aussi les comptes et portefeuilles (définitif), ou les garder pour une réinstallation.

---

## En cas de problème

| Problème | Solution |
|---|---|
| Le script s'arrête à l'étape 3 ou 5 | Vérifier la connexion Internet, relancer : les téléchargements déjà faits sont gardés |
| Étape 2 : Inno Setup introuvable | L'installer à la main depuis https://jrsoftware.org/isdl.php, puis relancer |
| Étape 6 : un module ne s'importe pas | Lire le message affiché (nom de la bibliothèque) et me l'envoyer |
| La fenêtre du tableau de bord ne s'ouvre pas | Ouvrir à la main l'adresse affichée dans la fenêtre noire (`http://localhost:8501`) |
| L'antivirus bloque l'installateur | Même cause que l'avertissement Windows (programme non signé) : l'autoriser |

## Limites

- Windows 64 bits ; Mac Apple Silicon via la fabrication GitHub (Partie 1 bis).
- Pas de mise à jour automatique : il faut redistribuer le nouveau fichier.
- Programme non signé : l'avertissement Windows est normal (un certificat de signature coûte
  plusieurs centaines d'euros par an).
- Hors connexion, les cours s'arrêtent à la date de fabrication de l'installateur (ils se
  complètent automatiquement dès que l'ordinateur retrouve Internet).
