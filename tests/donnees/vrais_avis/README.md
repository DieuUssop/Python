# Vrais avis d'opéré (anonymisés)

Ce dossier accueille de VRAIS documents de courtiers et de banques, pour vérifier la lecture
des PDF sur autre chose que les avis fictifs de `tests/avis_fictifs.py`.

Pour ajouter un document :

1. Masquer les données personnelles (nom, adresse, numéro de compte) : dans le logiciel, le
   formulaire « Compléter l'opération » propose « Préparer un rapport anonymisé », et
   `python diagnostic_pdf.py fichier.pdf --anonyme` produit le même rapport. Pour le PDF
   lui-même, le noircir avec un logiciel de PDF (fonction « Biffer / Caviarder »).
2. Copier le PDF dans ce dossier.
3. Ajouter une ligne par opération dans `attendus.csv` (séparateur « ; », nombres avec un
   point décimal) : `fichier;date;sens;isin;quantite;cours;frais`
   (date au format JJ/MM/AAAA, sens ACHAT / VENTE / DIVIDENDE, frais vide si inconnus).
4. Lancer `python -m pytest tests/test_pdf_universel.py` : chaque document doit être lu
   exactement comme indiqué.
