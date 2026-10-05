@echo off
REM Double-cliquer pour fabriquer l'installateur Windows (Installer_Portfolio_Tracker.exe).
REM Internet necessaire. Duree : 10 a 20 minutes. Resultat dans le dossier installateur_windows.
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0fabriquer_installateur.ps1"
pause
