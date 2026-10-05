# fabriquer_installateur.ps1 — Fabrique l'installateur Windows de Portfolio Tracker.
# Lancé par fabriquer_installateur.bat (double-clic). Internet nécessaire. Durée : 10 à 20 min.
#
# Étapes :
#   1. vérifie la base de titres (data\base) ;
#   2. installe Inno Setup (le logiciel qui fabrique les installateurs) s'il manque ;
#   3. télécharge Python « embarqué » (une version de Python qui tient dans un dossier) ;
#   4. copie le projet (sans les comptes ni les fichiers de travail) ;
#   5. installe les bibliothèques (requirements.txt) dans ce Python embarqué ;
#   6. vérifie que tout s'importe ;
#   7. compile installateur\portfolio_tracker.iss -> installateur_windows\Installer_Portfolio_Tracker.exe

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"          # téléchargements beaucoup plus rapides
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$Racine          = Split-Path -Parent $MyInvocation.MyCommand.Path
$Travail         = Join-Path $Racine "build_installateur"
$Telechargements = Join-Path $Travail "telechargements"
$Programme       = Join-Path $Travail "programme"
$Sortie          = Join-Path $Racine "installateur_windows"
$VersionsPython  = @("3.12.10", "3.12.9", "3.12.8")

function Etape($texte) { Write-Host ""; Write-Host "==> $texte" -ForegroundColor Cyan }
function Ok($texte)    { Write-Host "    $texte" -ForegroundColor Green }
function Echec($texte) { Write-Host ""; Write-Host "ERREUR : $texte" -ForegroundColor Red; exit 1 }
function Telecharger($url, $fichier) {
    if (-not (Test-Path $fichier)) { Invoke-WebRequest -Uri $url -OutFile $fichier -UseBasicParsing }
}

New-Item -ItemType Directory -Force -Path $Telechargements | Out-Null

# ---------------------------------------------------------------- 1. Base de titres
Etape "1/7 Base de titres"
if (Test-Path (Join-Path $Racine "data\base\cours")) {
    $taille = (Get-ChildItem (Join-Path $Racine "data\base") -Recurse -File | Measure-Object Length -Sum).Sum / 1MB
    Ok ("Base présente ({0:N0} Mo) : l'application installée fonctionnera hors connexion." -f $taille)
} else {
    Write-Host "    La base de titres n'est pas construite (data\base\cours absent)." -ForegroundColor Yellow
    Write-Host "    Sans elle, l'application installée aura besoin d'Internet pour les cours." -ForegroundColor Yellow
    Write-Host "    Pour la construire : double-cliquer sur construire_base.bat (environ 1 h)." -ForegroundColor Yellow
    $reponse = Read-Host "    Continuer quand même ? (O/N)"
    if ($reponse -notmatch '^[oOyY]') { exit 0 }
}

# ---------------------------------------------------------------- 2. Inno Setup
Etape "2/7 Inno Setup"
function Trouver-ISCC {
    $chemins = @(
        (Join-Path ${env:ProgramFiles(x86)} "Inno Setup 6\ISCC.exe"),
        (Join-Path $env:ProgramFiles "Inno Setup 6\ISCC.exe"),
        (Join-Path $env:LOCALAPPDATA "Programs\Inno Setup 6\ISCC.exe")
    )
    foreach ($c in $chemins) { if ($c -and (Test-Path $c)) { return $c } }
    return $null
}
$ISCC = Trouver-ISCC
if (-not $ISCC) {
    Write-Host "    Installation d'Inno Setup (gratuit, une seule fois)..."
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id JRSoftware.InnoSetup -e --silent --accept-package-agreements --accept-source-agreements | Out-Host
        $ISCC = Trouver-ISCC
    }
}
if (-not $ISCC) {
    $installeur = Join-Path $Telechargements "innosetup.exe"
    Telecharger "https://jrsoftware.org/download.php/is.exe" $installeur
    Start-Process -Wait -FilePath $installeur -ArgumentList "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/CURRENTUSER"
    $ISCC = Trouver-ISCC
}
if (-not $ISCC) { Echec "Inno Setup introuvable. L'installer à la main depuis https://jrsoftware.org/isdl.php puis relancer." }
Ok "Inno Setup : $ISCC"

# ---------------------------------------------------------------- 3. Python embarqué
Etape "3/7 Python embarqué"
$ZipPython = $null
foreach ($v in $VersionsPython) {
    $f = Join-Path $Telechargements "python-$v-embed-amd64.zip"
    try {
        Telecharger "https://www.python.org/ftp/python/$v/python-$v-embed-amd64.zip" $f
        $ZipPython = $f; Ok "Python $v"; break
    } catch {
        Remove-Item $f -ErrorAction SilentlyContinue
    }
}
if (-not $ZipPython) { Echec "téléchargement de Python impossible (connexion Internet ?)." }

# ---------------------------------------------------------------- 4. Copie du projet
Etape "4/7 Copie du projet"
if (Test-Path $Programme) { Remove-Item -Recurse -Force $Programme }
New-Item -ItemType Directory -Force -Path $Programme | Out-Null
$dossiersExclus = @($Travail, $Sortie, (Join-Path $Racine ".git"), (Join-Path $Racine "data\comptes"),
                    (Join-Path $Racine "tests"), (Join-Path $Racine "installateur"),
                    "__pycache__", ".pytest_cache", ".github", ".vscode")
$fichiersExclus = @("*.bat", "*.ps1", ".installe", "cache_*.csv", "progression.json", "echecs.csv", "*.tmp",
                    "historique.csv", "transactions_sauvegarde.csv", "graphique_*.png", "rapport_portefeuille*.pdf",
                    "*.zip", ".gitignore", "pytest.ini")
robocopy $Racine $Programme /E /NFL /NDL /NJH /NJS /NP /XD $dossiersExclus /XF $fichiersExclus | Out-Null
if ($LASTEXITCODE -ge 8) { Echec "copie du projet impossible (code robocopy $LASTEXITCODE)." }
$global:LASTEXITCODE = 0
if (-not (Test-Path (Join-Path $Programme "app.py"))) { Echec "app.py absent de la copie." }
Ok "Projet copié (sans comptes, tests ni fichiers de travail)"

# ---------------------------------------------------------------- 5. Bibliothèques
Etape "5/7 Bibliothèques (5 à 15 min)"
$DossierPython = Join-Path $Programme "python"
Expand-Archive -Path $ZipPython -DestinationPath $DossierPython -Force
$py = Join-Path $DossierPython "python.exe"
# Le fichier ._pth règle les dossiers que ce Python consulte : on active les
# bibliothèques installées (import site) et on ajoute le dossier du projet (..).
$pth = Get-ChildItem (Join-Path $DossierPython "python*._pth") | Select-Object -First 1
$lignes = Get-Content $pth.FullName | ForEach-Object { if ($_ -match '^\s*#\s*import site') { 'import site' } else { $_ } }
$lignes += '..'
Set-Content -Path $pth.FullName -Value $lignes -Encoding ASCII

$getpip = Join-Path $Telechargements "get-pip.py"
Telecharger "https://bootstrap.pypa.io/get-pip.py" $getpip
& $py $getpip --no-warn-script-location
if ($LASTEXITCODE -ne 0) { Echec "installation de pip impossible." }
& $py -m pip install --no-warn-script-location --disable-pip-version-check -r (Join-Path $Racine "requirements.txt")
if ($LASTEXITCODE -ne 0) { Echec "installation des bibliothèques impossible (voir le message ci-dessus)." }
Ok "Bibliothèques installées"

# ---------------------------------------------------------------- 6. Vérification
Etape "6/7 Vérification"
& $py -c "import streamlit, pandas, numpy, scipy, plotly, matplotlib, reportlab, openpyxl, cryptography, yfinance; import src.analyse, src.comptes, src.base_titres, src.vues_compte; print('    Tout s importe correctement')"
if ($LASTEXITCODE -ne 0) { Echec "une bibliothèque ou un module du projet ne s'importe pas (voir ci-dessus)." }
# Fond de carte du monde (pour que la carte s'affiche hors connexion)
& $py -c "from src import fond_de_carte; import sys; sys.exit(0 if fond_de_carte.chemin().exists() or fond_de_carte.telecharger() else 1)"
if ($LASTEXITCODE -ne 0) { Write-Host "    Fond de carte non telecharge : la carte du monde demandera Internet." -ForegroundColor Yellow }
$global:LASTEXITCODE = 0
Get-ChildItem $Programme -Recurse -Directory -Filter "__pycache__" |
    Where-Object { $_.FullName -notlike "*\python\*" } | Remove-Item -Recurse -Force

# ---------------------------------------------------------------- 7. Installateur
Etape "7/7 Fabrication de l'installateur (quelques minutes)"
$Version = Get-Date -Format "yyyy.MM.dd"
& $ISCC "/Qp" "/DVersion=$Version" (Join-Path $Racine "installateur\portfolio_tracker.iss")
if ($LASTEXITCODE -ne 0) { Echec "la compilation Inno Setup a échoué (voir ci-dessus)." }

$exe = Join-Path $Sortie "Installer_Portfolio_Tracker.exe"
$taille = (Get-Item $exe).Length / 1MB
Write-Host ""
Write-Host ("Installateur prêt : {0} ({1:N0} Mo), version {2}" -f $exe, $taille, $Version) -ForegroundColor Green
Write-Host "C'est ce fichier unique qu'il faut partager (OneDrive, Google Drive, WeTransfer, clé USB)."
Start-Process explorer.exe $Sortie
