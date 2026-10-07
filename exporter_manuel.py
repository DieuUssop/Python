"""
exporter_manuel.py — Fabrique les versions Word et PDF du manuel (docs/manuel/<langue>/*.md).

Usage (dans le dossier du projet) :
    python exporter_manuel.py            # français
    python exporter_manuel.py en         # anglais (si le manuel anglais existe)

Nécessite pandoc (https://pandoc.org) pour le Word, et LibreOffice pour le PDF
(facultatif). Les fichiers produits sont rangés dans docs/manuel/ :
    Manuel_Portfolio_Tracker_fr.docx et Manuel_Portfolio_Tracker_fr.pdf
Le logiciel propose ensuite de les télécharger depuis l'espace « Manuel et aide ».

Les métadonnées des fiches (questions, mots-clés, liens vers l'écran) servent à
l'assistant et sont retirées de la version imprimable ; [[Bouton]] devient **Bouton**.
"""

import datetime
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent
DOSSIER = RACINE / "docs" / "manuel"

TITRES = {
    "fr": ("Portfolio Tracker", "Manuel de l'utilisateur", "Master G2C · Outil de suivi et d'analyse de portefeuille",
           "Sommaire"),
    "en": ("Portfolio Tracker", "User manual", "Master G2C · Portfolio tracking and analysis tool", "Contents"),
}


def markdown_imprimable(langue, titre_sommaire="Sommaire"):
    """Assemble les chapitres en un seul Markdown, sans métadonnées, précédé d'un sommaire
    (chapitres et fiches, sans numéros de page : il s'affiche pareil dans Word et en PDF)."""
    sys.path.insert(0, str(RACINE))
    from src import manuel
    chapitres = manuel.charger(langue)
    morceaux = [f"# {titre_sommaire}\n"]
    for i, chapitre in enumerate(chapitres, 1):
        morceaux.append(f"**{i}. {chapitre.titre}**\n")
        morceaux.append("\n".join(f"- {fiche.titre}" for fiche in chapitre.fiches) + "\n")
    for i, chapitre in enumerate(chapitres, 1):
        morceaux.append(f"# {i}. {chapitre.titre}\n")
        if chapitre.introduction:
            morceaux.append(chapitre.introduction + "\n")
        for fiche in chapitre.fiches:
            texte = manuel.texte_affiche(fiche)
            texte = re.sub(r"^### ", "#### ", texte, flags=re.M)        # sous-titres d'une fiche
            morceaux.append(f"## {fiche.titre}\n\n{texte}\n")
    return "\n".join(morceaux)


def modele_word(chemin):
    """Modèle Word de pandoc, retouché : police, couleurs des titres, marges."""
    source = Path(chemin).with_suffix(".source.docx")
    subprocess.run(["pandoc", "-o", str(source), "--print-default-data-file", "reference.docx"], check=True)
    with zipfile.ZipFile(source) as entree, zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED) as sortie:
        for element in entree.infolist():
            contenu = entree.read(element.filename)
            if element.filename == "word/styles.xml":
                xml = contenu.decode("utf-8")
                polices = '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/>'
                xml = re.sub(r"<w:rFonts [^>]*/>", polices, xml)
                if "<w:rPrDefault><w:rPr>" in xml and polices not in xml.split("</w:rPrDefault>")[0]:
                    xml = xml.replace("<w:rPrDefault><w:rPr>", "<w:rPrDefault><w:rPr>" + polices, 1)
                xml = re.sub(r'<w:color w:val="[0-9A-Fa-f]{6}"( w:themeColor="[^"]*")?( w:themeShade="[^"]*")?/>',
                             '<w:color w:val="0F2A4A"/>', xml)
                # chaque chapitre (Titre 1) commence sur une nouvelle page
                xml = re.sub(r'(<w:style [^>]*w:styleId="Heading1"[^>]*>.*?<w:pPr>)', r"\1<w:pageBreakBefore/>", xml,
                             count=1, flags=re.S)
                contenu = xml.encode("utf-8")
            sortie.writestr(element, contenu)
    source.unlink()


def exporter(langue="fr"):
    if not shutil.which("pandoc"):
        sys.exit("pandoc est introuvable : installez-le depuis https://pandoc.org")
    titre, sous_titre, ligne, sommaire = TITRES.get(langue, TITRES["fr"])
    date = datetime.date.today().strftime("%d/%m/%Y")
    with tempfile.TemporaryDirectory() as dossier:
        dossier = Path(dossier)
        md = dossier / "manuel.md"
        md.write_text(f"---\ntitle: \"{titre}\"\nsubtitle: \"{sous_titre}\"\nauthor: \"{ligne}\"\ndate: \"{date}\"\n"
                      f"lang: {langue}\n---\n\n" + markdown_imprimable(langue, sommaire),
                      encoding="utf-8")
        modele = dossier / "modele.docx"
        modele_word(modele)
        docx = DOSSIER / f"Manuel_Portfolio_Tracker_{langue}.docx"
        subprocess.run(["pandoc", str(md), "-o", str(docx), f"--reference-doc={modele}"],
                       check=True)
        print(f"Word : {docx}")
        bureautique = shutil.which("soffice") or shutil.which("libreoffice")
        if bureautique:
            subprocess.run([bureautique, "--headless", "--convert-to", "pdf", "--outdir", str(DOSSIER), str(docx)],
                           check=True, capture_output=True)
            print(f"PDF : {docx.with_suffix('.pdf')}")
        else:
            print("LibreOffice introuvable : pas de PDF (ouvrez le Word et enregistrez-le en PDF).")


if __name__ == "__main__":
    exporter(sys.argv[1] if len(sys.argv) > 1 else "fr")
