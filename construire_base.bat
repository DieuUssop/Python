@echo off
REM Double-cliquer pour construire (ou mettre a jour) la base locale de titres.
REM A faire avec Internet. Premiere fois : environ 1 heure. Ensuite : quelques minutes.
REM Si c'est interrompu, relancer : le telechargement reprend ou il s'etait arrete.
cd /d "%~dp0"
if exist data\base\progression.json goto complete
if exist data\base\cours goto miseajour
:complete
python construire_base_titres.py
goto fin
:miseajour
python construire_base_titres.py --mise-a-jour
:fin
pause
