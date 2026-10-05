@echo off
REM Double-cliquer pour ouvrir le tableau de bord dans le navigateur.
REM Fonctionne aussi SANS Internet (cours lus dans la base locale data\base).
cd /d "%~dp0"
if not exist .installe (
    echo Premiere utilisation : installation des bibliotheques - Internet necessaire...
    python -m pip install -r requirements.txt && echo ok> .installe
)
python lanceur.py
pause
