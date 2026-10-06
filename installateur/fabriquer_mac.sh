#!/bin/bash
# fabriquer_mac.sh — Fabrique l'application Mac « Portfolio Tracker.app » et son
# image disque « Portfolio_Tracker_Mac.dmg ».
#
# Lancé AUTOMATIQUEMENT par GitHub (fichier .github/workflows/installateurs.yml),
# sur un Mac prêté par GitHub : il n'y a rien à faire sur ton PC.
#
# Même principe que l'installateur Windows :
#   - Python « autonome » (python-build-standalone) rangé DANS l'application,
#     avec toutes les bibliothèques : rien à installer sur le Mac de l'utilisateur ;
#   - au lancement, une fenêtre Terminal s'ouvre (l'équivalent de la fenêtre noire
#     de Windows) et le tableau de bord s'ouvre dans sa fenêtre ; fermer le
#     Terminal arrête l'application ;
#   - les données (comptes chiffrés, base de titres, mémoire) sont rangées dans
#     ~/Library/Application Support/Portfolio Tracker et CONSERVÉES lors des mises à jour ;
#   - tout fonctionne hors connexion.
#
# Usage (sur un Mac) : bash installateur/fabriquer_mac.sh 2026.10.05
set -euo pipefail

VERSION="${1:-$(date +%Y.%m.%d)}"
RACINE="$(cd "$(dirname "$0")/.." && pwd)"
TRAVAIL="$RACINE/build_mac"
APP="$TRAVAIL/dmg/Portfolio Tracker.app"
RES="$APP/Contents/Resources"
SORTIE="$RACINE/installateur_mac"

echo "==> 1/6 Préparation (version $VERSION)"
rm -rf "$TRAVAIL" "$SORTIE"
mkdir -p "$APP/Contents/MacOS" "$RES" "$SORTIE"

echo "==> 2/6 Python autonome (python-build-standalone, Apple Silicon)"
cd "$TRAVAIL"
gh release download --repo astral-sh/python-build-standalone \
   --pattern "cpython-3.12.*-aarch64-apple-darwin-install_only.tar.gz" --dir "$TRAVAIL" --clobber
ARCHIVE="$(ls "$TRAVAIL"/cpython-3.12.*-aarch64-apple-darwin-install_only.tar.gz | head -1)"
tar -xzf "$ARCHIVE" -C "$RES"                     # crée $RES/python
PY="$RES/python/bin/python3"
"$PY" --version

echo "==> 3/6 Bibliothèques"
"$PY" -m pip install --upgrade pip --quiet
"$PY" -m pip install --no-warn-script-location -r "$RACINE/requirements.txt"
"$PY" -m pip install --no-warn-script-location -r "$RACINE/requirements-ocr.txt" \
  || echo "    Reconnaissance de caractères non installée : les PDF image seront refusés."
"$PY" -c "import streamlit, pandas, scipy, plotly, matplotlib, reportlab, openpyxl, cryptography, yfinance, pdfplumber; print('    bibliothèques OK')"

echo "==> 4/6 Copie du projet"
rsync -a "$RACINE/" "$RES/app/" \
  --exclude ".git/" --exclude ".github/" --exclude "build_mac/" --exclude "build_installateur/" \
  --exclude "installateur/" --exclude "installateur_windows/" --exclude "installateur_mac/" \
  --exclude "tests/" --exclude "data/comptes/" --exclude "__pycache__/" --exclude ".pytest_cache/" \
  --exclude "*.bat" --exclude "*.ps1" --exclude ".installe" --exclude "data/cache_*.csv" \
  --exclude "data/historique.csv" --exclude "data/transactions_sauvegarde.csv" --exclude "graphique_*.png" \
  --exclude "rapport_portefeuille*.pdf" --exclude "*.zip" --exclude ".gitignore" --exclude "pytest.ini" \
  --exclude "data/base/progression.json" --exclude "data/base/*.tmp"
( cd "$RES/app" && "$PY" -c "import src.analyse, src.comptes, src.expositions; print('    modules du projet OK')" )
# Fond de carte du monde (carte hors connexion)
( cd "$RES/app" && "$PY" -c "from src import fond_de_carte as f; print('    fond de carte :', f.chemin().exists() or f.telecharger())" ) || true
# Fichiers .pyc précompilés : démarrage plus rapide, sans rien écrire dans l'application
"$PY" -m compileall -q "$RES/python/lib" "$RES/app" > /dev/null || true
echo "$VERSION" > "$RES/version.txt"

echo "==> 5/6 Application (icône, lanceur, signature)"
# Icône : assets/icone.ico -> icone.icns
"$PY" - <<PYEOF
from PIL import Image
Image.open("$RACINE/assets/icone.ico").convert("RGBA").resize((1024, 1024), Image.LANCZOS).save("$TRAVAIL/icone.png")
PYEOF
mkdir -p "$TRAVAIL/icone.iconset"
for taille in 16 32 128 256 512; do
  sips -z $taille $taille "$TRAVAIL/icone.png" --out "$TRAVAIL/icone.iconset/icon_${taille}x${taille}.png" > /dev/null
  double=$((taille * 2))
  sips -z $double $double "$TRAVAIL/icone.png" --out "$TRAVAIL/icone.iconset/icon_${taille}x${taille}@2x.png" > /dev/null
done
iconutil -c icns "$TRAVAIL/icone.iconset" -o "$RES/icone.icns"

cat > "$APP/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>Portfolio Tracker</string>
  <key>CFBundleDisplayName</key><string>Portfolio Tracker</string>
  <key>CFBundleIdentifier</key><string>fr.masterg2c.portfoliotracker</string>
  <key>CFBundleVersion</key><string>$VERSION</string>
  <key>CFBundleShortVersionString</key><string>$VERSION</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleExecutable</key><string>Portfolio Tracker</string>
  <key>CFBundleIconFile</key><string>icone</string>
  <key>LSMinimumSystemVersion</key><string>12.0</string>
  <key>NSHighResolutionCapable</key><true/>
</dict>
</plist>
PLIST

# Le lanceur : met à jour la copie de travail (sans toucher aux comptes), puis ouvre
# une fenêtre Terminal qui démarre le tableau de bord.
cat > "$APP/Contents/MacOS/Portfolio Tracker" <<'LANCEUR'
#!/bin/bash
RES="$(cd "$(dirname "$0")/../Resources" && pwd)"
SUPPORT="$HOME/Library/Application Support/Portfolio Tracker"
VERSION="$(cat "$RES/version.txt")"
mkdir -p "$SUPPORT"
if [ "$(cat "$SUPPORT/version.txt" 2>/dev/null)" != "$VERSION" ]; then
  # Nouvelle version : le code et la base de titres sont remplacés ;
  # les comptes (data/comptes) et la mémoire des titres sont conservés.
  /usr/bin/rsync -a --delete --exclude "/data/comptes/" --exclude "/data/base/memoire.csv" \
    --exclude "/data/cache_*" "$RES/app/" "$SUPPORT/app/"
  echo "$VERSION" > "$SUPPORT/version.txt"
fi
cat > "$SUPPORT/Portfolio Tracker.command" <<EOF
#!/bin/bash
clear
export PORTFOLIO_INSTALLE=1 PYTHONDONTWRITEBYTECODE=1
cd "$SUPPORT/app"
"$RES/python/bin/python3" lanceur.py
EOF
chmod +x "$SUPPORT/Portfolio Tracker.command"
open -a Terminal "$SUPPORT/Portfolio Tracker.command"
LANCEUR
chmod +x "$APP/Contents/MacOS/Portfolio Tracker"
codesign --force --deep --sign - "$APP" || echo "    (signature ad hoc impossible : sans gravité)"

echo "==> 6/6 Image disque (.dmg)"
ln -s /Applications "$TRAVAIL/dmg/Applications"
cp "$RACINE/installateur/LISEZ-MOI_Mac.txt" "$TRAVAIL/dmg/LISEZ-MOI.txt" 2>/dev/null || true
hdiutil create -volname "Portfolio Tracker" -srcfolder "$TRAVAIL/dmg" -ov -format UDZO \
  "$SORTIE/Portfolio_Tracker_Mac.dmg"
ls -lh "$SORTIE"
echo "✅ Application Mac prête : installateur_mac/Portfolio_Tracker_Mac.dmg"
