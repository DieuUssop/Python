"""
lanceur.py — Ouvre le tableau de bord dans le navigateur.

Utilisé par :
    - le raccourci « Portfolio Tracker » du programme installé (installateur Windows) ;
    - lancer_tableau_de_bord.bat.

Ce qu'il fait :
    1. si le tableau de bord est déjà ouvert, il rouvre simplement le navigateur ;
    2. sinon, il démarre le serveur Streamlit sur CET ordinateur uniquement
       (adresse « localhost » : personne d'autre sur le réseau ne peut s'y connecter,
       et le pare-feu Windows ne pose pas de question) ;
    3. il ouvre le tableau de bord dès qu'il est prêt, dans SA PROPRE FENÊTRE
       (mode « application » de Microsoft Edge, ou de Chrome : sans barre
       d'adresse ni onglets, comme un logiciel), sinon dans le navigateur.

Fermer la fenêtre noire arrête l'application.
"""

import os
import signal
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

RACINE = Path(__file__).resolve().parent
PORTS = range(8501, 8511)
INSTALLE = (RACINE / "python" / "python.exe").exists() or bool(os.environ.get("PORTFOLIO_INSTALLE"))
# (version installée : Python embarqué sous Windows, application Mac)

# Pas de proxy pour parler à son propre ordinateur
_OUVREUR = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def est_le_tableau_de_bord(port):
    """Vrai si un serveur Streamlit répond sur ce port."""
    try:
        with _OUVREUR.open(f"http://localhost:{port}/_stcore/health", timeout=1) as reponse:
            return reponse.read().strip() == b"ok"
    except Exception:
        return False


NAVIGATEURS_MAC = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                   "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
                   "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"]


def navigateur_application():
    """Navigateur capable d'ouvrir une « fenêtre d'application » : Microsoft Edge (installé sur
    Windows 10 et 11) ou Google Chrome ; sur Mac, Chrome, Edge ou Brave s'ils sont installés
    (sinon le tableau de bord s'ouvre dans Safari). Renvoie None si aucun."""
    if os.environ.get("PORTFOLIO_NAVIGATEUR") == "classique":
        return None
    if sys.platform == "darwin":
        return next((n for n in NAVIGATEURS_MAC if Path(n).exists()), None)
    if os.name != "nt":
        return None
    dossiers = [os.environ.get(v) for v in ("ProgramFiles(x86)", "ProgramFiles", "LOCALAPPDATA")]
    for dossier in [d for d in dossiers if d]:
        for relatif in (r"Microsoft\Edge\Application\msedge.exe", r"Google\Chrome\Application\chrome.exe"):
            chemin = Path(dossier) / relatif
            if chemin.exists():
                return str(chemin)
    return None


def ouvrir(adresse):
    """Ouvre le tableau de bord dans une fenêtre d'application, sinon dans le navigateur."""
    navigateur = navigateur_application()
    if navigateur:
        try:
            subprocess.Popen([navigateur, f"--app={adresse}", "--window-size=1440,900"])
            return
        except OSError:
            pass
    webbrowser.open(adresse)


def port_libre(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def main():
    for port in PORTS:
        if est_le_tableau_de_bord(port):
            print("Portfolio Tracker est déjà ouvert : ouverture de la fenêtre...")
            ouvrir(f"http://localhost:{port}")
            time.sleep(3)
            return
        if port_libre(port):
            break
    else:
        print("Aucun port libre entre 8501 et 8510 : fermez une autre application puis réessayez.")
        input("Appuyez sur Entrée pour fermer.")
        return

    adresse = f"http://localhost:{port}"
    print("=" * 66)
    print("  Portfolio Tracker")
    print(f"  Le tableau de bord s'ouvre dans sa fenêtre ({adresse}).")
    print("  Il fonctionne sur cet ordinateur uniquement, même sans Internet.")
    print()
    print("  Laissez cette fenêtre ouverte pendant l'utilisation.")
    print("  Fermez-la pour quitter l'application.")
    print("=" * 66)

    commande = [sys.executable, "-m", "streamlit", "run", str(RACINE / "app.py"),
                "--server.port", str(port),
                "--server.address", "localhost",          # accessible depuis cet ordinateur seulement
                "--server.headless", "true",              # pas de question au premier lancement
                "--browser.gatherUsageStats", "false"]
    if INSTALLE:
        commande += ["--server.fileWatcherType", "none"]  # le code ne change pas : inutile de le surveiller
    serveur = subprocess.Popen(commande, cwd=RACINE, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    # Fenêtre fermée (Mac : Terminal) : on arrête aussi le serveur
    for nom in ("SIGTERM", "SIGHUP"):
        if hasattr(signal, nom):
            signal.signal(getattr(signal, nom), lambda *_: (serveur.terminate(), sys.exit(0)))

    debut = time.time()
    while time.time() - debut < 180:
        if serveur.poll() is not None:
            print()
            print("Le tableau de bord n'a pas pu démarrer (voir le message ci-dessus).")
            input("Appuyez sur Entrée pour fermer.")
            return
        if est_le_tableau_de_bord(port):
            ouvrir(adresse)
            break
        time.sleep(0.5)

    try:
        serveur.wait()
    except KeyboardInterrupt:
        serveur.terminate()


if __name__ == "__main__":
    main()
