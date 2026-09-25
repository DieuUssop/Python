@echo off
REM Double-cliquer pour ouvrir le tableau de bord dans le navigateur.
cd /d "%~dp0"
python -m streamlit run app.py
pause
