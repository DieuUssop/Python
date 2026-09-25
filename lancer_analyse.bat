@echo off
REM Double-cliquer pour lancer l analyse complete (graphiques et rapport PDF).
cd /d "%~dp0"
python main.py
echo.
echo Rapport cree : rapport_portefeuille.pdf
pause
