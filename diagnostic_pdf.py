"""
diagnostic_pdf.py — Montre exactement ce que l'application lit dans un PDF.

Usage (terminal de VS Code, dans le dossier du projet) :
    python diagnostic_pdf.py "C:\\chemin\\vers\\avis.pdf"

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
    if len(texte.strip()) >= 20:
        sortie.append("=> PDF TEXTE (lecture exacte)")
        for i, p in enumerate(pages):
            sortie += [f"--- page {i + 1} : texte ---", p["texte"]]
            for t in p["tableaux_bruts"]:
                sortie += ["--- tableau ---"] + [" | ".join(str(c) for c in ligne) for ligne in t]
    else:
        moteur = "RapidOCR" if ocr._rapidocr() is not None else ("Tesseract" if ocr._tesseract() else "AUCUN")
        sortie.append(f"=> PDF IMAGE : reconnaissance de caractères, moteur = {moteur}")
        if moteur != "AUCUN":
            import io
            import pypdfium2
            image = pypdfium2.PdfDocument(io.BytesIO(brut))[0].render(scale=3).to_pil()
            for angle in (0, 90, 270, 180):
                lu = ocr.texte_image(image.rotate(angle, expand=True) if angle else image)
                sortie += [f"--- rotation {angle}° · score {ocr._score(lu):.1f} ---", lu]
            sortie += ["--- texte retenu (après correction des ISIN) ---", ocr.texte_pdf(brut)[0]]

    try:
        grille, nature = imp.grille_pdf(brut)
        sortie += [f"=== RÉSULTAT ({nature}) ==="] + [" | ".join(map(str, ligne)) for ligne in grille]
    except Exception as erreur:
        sortie += ["=== RÉSULTAT ===", f"Erreur : {erreur}"]

    rapport = "\n".join(sortie)
    print(rapport)
    fichier = Path(__file__).with_name("diagnostic_pdf.txt")
    fichier.write_text(rapport, encoding="utf-8")
    print(f"\nRapport enregistré dans {fichier}")


if __name__ == "__main__":
    main()
