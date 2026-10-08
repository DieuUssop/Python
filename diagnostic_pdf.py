"""
diagnostic_pdf.py — Montre exactement ce que l'application lit dans un PDF.

Usage (terminal de VS Code, dans le dossier du projet) :
    python diagnostic_pdf.py "C:\\chemin\\vers\\avis.pdf"
    python diagnostic_pdf.py "C:\\chemin\\vers\\avis.pdf" --anonyme   # sans nom, adresse, n° de compte

Le résultat est aussi enregistré dans diagnostic_pdf.txt (à côté de ce script) :
c'est ce fichier qu'il faut envoyer pour corriger une mauvaise lecture.
Il contient le texte lu : masquez votre nom et votre numéro de compte si besoin.
"""

import sys
from pathlib import Path

from src import import_fichier as imp
from src import ocr


def main():
    if len(sys.argv) < 2:
        sys.exit('Usage : python diagnostic_pdf.py "chemin\\vers\\fichier.pdf"')
    chemin = Path(sys.argv[1])
    brut = chemin.read_bytes()
    sortie = [f"Fichier : {chemin.name} ({len(brut) // 1024} Ko)"]

    pages = imp._pages_pdf(brut)
    texte = "".join(p["texte"] for p in pages)
    sortie.append(f"Pages : {len(pages)} · texte intégré : {len(texte.strip())} caractères")
    from src import lecture_pdf
    code = lecture_pdf.texte_illisible(texte)
    if len(texte.strip()) >= 20 and not code:
        sortie.append("=> PDF TEXTE (lecture exacte)")
        for i, p in enumerate(pages):
            sortie += [f"--- page {i + 1} : texte ---", p["texte"]]
            for t in p["tableaux_bruts"]:
                sortie += ["--- tableau ---"] + [" | ".join(str(c) for c in ligne) for ligne in t]
    else:
        moteur = "RapidOCR" if ocr._rapidocr() is not None else ("Tesseract" if ocr._tesseract() else "AUCUN")
        if code:
            sortie += ["=> PDF TEXTE « CODÉ » (illisible une fois extrait) : lu comme une image", texte[:600]]
        sortie.append(f"=> PDF IMAGE : reconnaissance de caractères, moteur = {moteur}")
        if moteur != "AUCUN":
            import io
            import pypdfium2
            image = pypdfium2.PdfDocument(io.BytesIO(brut))[0].render(scale=3).to_pil()
            for angle in (0, 90, 270, 180):
                lu = ocr.texte_image(image.rotate(angle, expand=True) if angle else image)
                sortie += [f"--- rotation {angle}° · score {ocr._score(lu):.1f} ---", lu]
            sortie += ["--- texte retenu (après correction des ISIN) ---", ocr.texte_pdf(brut)[0]]

    # Lecture par le contenu (ISIN, date, quantité × cours = montant) : ce que propose le formulaire
    textes = [p["texte"] for p in pages] if not code and len(texte.strip()) >= 20 else \
        (ocr.texte_pdf(brut) if ocr.disponible() else [])
    trouve = lecture_pdf.candidats(textes)
    sortie += ["=== LECTURE PAR LE CONTENU ===",
               f"ISIN : {trouve['isins']}", f"Dates : {trouve['dates']} · date proposée : {trouve['date_proposee']}",
               f"Proposition : {trouve['proposition']}",
               "Nombres : " + " ; ".join(n["contexte"] for n in trouve["nombres"][:40])]

    try:
        grille, nature = imp.grille_pdf(brut)
        sortie += [f"=== RÉSULTAT ({nature}) ==="] + [" | ".join(map(str, ligne)) for ligne in grille]
    except Exception as erreur:
        sortie += ["=== RÉSULTAT ===", f"Erreur : {erreur}"]

    rapport = "\n".join(sortie)
    if "--anonyme" in sys.argv:
        # seulement ce qu'il faut pour corriger la lecture : ni nom, ni adresse, ni numéro de compte
        debut_resultat = next((i for i, l in enumerate(sortie) if l.startswith("=== RÉSULTAT")), len(sortie))
        rapport = (lecture_pdf.rapport_anonymise(textes, nom_fichier=chemin.name) + "\n\n"
                   + lecture_pdf.anonymiser("\n".join(sortie[debut_resultat:])))
    print(rapport)
    fichier = Path(__file__).with_name("diagnostic_pdf_anonyme.txt" if "--anonyme" in sys.argv
                                       else "diagnostic_pdf.txt")
    fichier.write_text(rapport, encoding="utf-8")
    print(f"\nRapport enregistré dans {fichier}")


if __name__ == "__main__":
    main()
