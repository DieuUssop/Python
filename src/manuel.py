"""
manuel.py — Le manuel du logiciel et l'assistant « Poser une question ».

Le manuel est écrit en Markdown dans docs/manuel/fr (et docs/manuel/en) : un
fichier par chapitre, découpé en « fiches » (une section ## = une fiche).
Chaque fiche peut porter une ligne de métadonnées, en commentaire HTML :

    ## Supprimer ou corriger une opération
    <!-- fiche: supprimer-operation | questions: comment j'enlève un achat mis par erreur ; effacer une ligne ; ... | mots: effacer, retirer | aller: Analyse du portefeuille/Transactions | chiffres: nb_operations -->

    - fiche     : identifiant unique (sert aux liens « Voir aussi ») ;
    - questions : 5 à 10 vraies formulations de la question, séparées par « ; » (le plus fort
                  poids dans la recherche : c'est ce qui fait qu'une question est bien comprise) ;
    - mots      : synonymes et mots-clés, séparés par des virgules ;
    - aller   : espace de travail (et onglet) où se trouve ce qui est décrit ;
    - chiffres: valeurs du portefeuille de l'utilisateur à afficher avec la fiche.

Dans le texte, [[Nom du bouton]] désigne un élément de l'écran (affiché en gras ;
un test vérifie que chacun existe vraiment dans le logiciel).

L'ASSISTANT n'utilise aucune intelligence artificielle générative et fonctionne
hors connexion : il cherche dans le manuel la fiche qui répond le mieux à la
question (mots du titre, des synonymes et du texte ; fautes de frappe tolérées ;
synonymes courants), et l'affiche telle qu'elle est écrite. Il ne peut donc rien
inventer. Quand aucune fiche ne correspond assez, il le dit et propose les plus
proches ; la question est notée dans un journal local pour compléter le manuel.
"""

import difflib
import math
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent.parent / "docs" / "manuel"
JOURNAL = Path(__file__).resolve().parent.parent / "data" / "questions_sans_reponse.csv"

SEUIL_REPONSE = 4.0          # score minimal pour présenter une fiche comme « la réponse »
SEUIL_SUGGESTION = 1.5       # score minimal pour proposer une fiche comme « proche »
PART_CONNUE_MIN = 0.5        # moins de la moitié des mots connus du manuel : question jugée hors sujet

MOTS_VIDES = set("""
a à ai au aux avec ce ces cet cette comment combien d de des du elle en est et eux faire faut il ils je
j l la le les leur lui ma mais me mes moi mon n ne nos notre on ou où par pas peut peux pour pourquoi
puis puisse qu que quel quelle quelles quels qui sa se ses si son sont sur ta te tes toi ton tu un une
vos votre vous y c ça cela ceci est-ce quoi dois doit veux voudrais aimerais svp stp merci bonjour
the of to and in is it how what why can do i my a an for on with does are be this that which where
""".split())

# Synonymes : chaque groupe est ramené à un même mot (forme normalisée, sans accent)
SYNONYMES = [
    ("supprimer", "effacer", "retirer", "enlever", "delete", "remove", "erase"),
    ("ajouter", "inserer", "importer", "rajouter", "add", "import", "charger", "envoyer", "upload"),
    ("modifier", "corriger", "editer", "rectifier", "edit", "correct", "update", "maj"),
    ("obligatoire", "oblige", "obliger", "indispensable", "necessaire", "requis", "mandatory"),
    ("doublon", "double", "duplique", "duplicate"),
    ("telecharger", "recuperer", "obtenir"),
    ("operation", "transaction", "mouvement", "ordre", "ligne", "achat", "vente", "trade"),
    ("portefeuille", "portfolio", "pea", "compte-titres", "cto"),
    ("compte", "account", "identifiant", "login", "connexion", "connecter", "inscription", "inscrire"),
    ("motdepasse", "password", "mdp"),
    ("volatilite", "volatility", "ecart-type", "ecarttype"),
    ("rendement", "performance", "return", "gain", "rentabilite"),
    ("cours", "prix", "price", "cotation", "quote"),
    ("pdf", "avis", "releve", "statement"),
    ("nuit", "sombre", "dark", "noir"),
    ("langue", "anglais", "english", "francais", "language"),
    ("erreur", "bug", "plante", "probleme", "marche", "fonctionne", "error", "crash"),
    ("installer", "installation", "install", "exe", "dmg"),
    ("indice", "benchmark", "reference"),
    ("fiable", "fiabilite", "verifier", "exact", "juste", "bon", "source", "provenance", "viennent"),
]
# Expressions de plusieurs mots ramenées à un seul mot (avant découpage)
EXPRESSIONS = [("mot de passe", "motdepasse"), ("deux fois", "doublon"), ("en double", "doublon"),
               ("value at risk", "var"), ("expected shortfall", "cvar"), ("perte maximale", "drawdown"),
               ("pire baisse", "drawdown"), ("ratio de sharpe", "sharpe"), ("monte carlo", "montecarlo"),
               ("monte-carlo", "montecarlo"), ("hors connexion", "horsconnexion"), ("sans internet", "horsconnexion"),
               ("hors ligne", "horsconnexion"), ("offline", "horsconnexion"), ("n.d.", " nd "),
               ("n/a", " nd ")]

MOTIF_META = re.compile(r"<!--\s*(.*?)\s*-->", re.S)
MOTIF_LIEN_ECRAN = re.compile(r"\[\[(.+?)\]\]")


# ----------------------------------------------------------------------
# Texte normalisé et racines de mots (français et anglais, très simples)
# ----------------------------------------------------------------------
def normaliser(texte):
    texte = unicodedata.normalize("NFKD", str(texte).lower())
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    return texte.replace("œ", "oe").replace("’", "'")


SUFFIXES = ("issements", "issement", "ations", "ation", "ements", "ement", "ments", "ment", "euses", "euse",
            "eurs", "eur", "ees", "ee", "es", "er", "ez", "ing", "ed", "s", "x", "e")


def _tronquer(mot):
    """Retire une terminaison courante : 'operations' -> 'operation', 'supprimee' -> 'supprim'."""
    for suffixe in SUFFIXES:
        if len(mot) > len(suffixe) + 3 and mot.endswith(suffixe):
            return mot[: -len(suffixe)]
    return mot


# Synonymes : chaque mot d'un groupe (et sa forme tronquée) est ramené à la forme tronquée du premier
_SYNONYME = {}
for _groupe in SYNONYMES:
    for _mot in _groupe:
        _SYNONYME[_mot] = _SYNONYME[_tronquer(_mot)] = _tronquer(_groupe[0])


def racine(mot):
    """Racine approximative d'un mot, synonymes ramenés à un même mot."""
    if mot in _SYNONYME:
        return _SYNONYME[mot]
    court = _tronquer(mot)
    return _SYNONYME.get(court, court)


def jetons(texte):
    """Mots utiles d'un texte, normalisés (sans accents, expressions regroupées), avant racinisation."""
    texte = normaliser(texte)
    for expression, remplacement in EXPRESSIONS:
        texte = texte.replace(expression, remplacement)
    brut = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", texte)
    return [m for m in brut if m not in MOTS_VIDES and len(m) > 1]


def mots(texte):
    """Liste des racines des mots utiles d'un texte."""
    return [racine(m) for m in jetons(texte)]


# ----------------------------------------------------------------------
# Lecture du manuel
# ----------------------------------------------------------------------
@dataclass
class Fiche:
    ident: str
    titre: str
    chapitre: str
    texte: str                       # Markdown, sans la ligne de métadonnées
    mots_cles: list = field(default_factory=list)
    questions: list = field(default_factory=list)
    aller: str = ""                  # « Espace » ou « Espace/Onglet »
    chiffres: list = field(default_factory=list)
    ordre: int = 0


@dataclass
class Chapitre:
    ident: str
    titre: str
    introduction: str
    fiches: list
    ordre: int = 0


def _meta(texte):
    """'fiche: x | mots: a, b | aller: y' -> {'fiche': 'x', 'mots': 'a, b', 'aller': 'y'}"""
    infos = {}
    for morceau in texte.split("|"):
        if ":" in morceau:
            cle, valeur = morceau.split(":", 1)
            infos[cle.strip().lower()] = valeur.strip()
    return infos


def lire_chapitre(chemin):
    contenu = Path(chemin).read_text(encoding="utf-8")
    titre_chap = re.search(r"^# (.+)$", contenu, re.M)
    titre_chap = titre_chap.group(1).strip() if titre_chap else Path(chemin).stem
    meta_chap = {}
    entete = contenu.split("\n## ", 1)[0]
    m = MOTIF_META.search(entete)
    if m:
        meta_chap = _meta(m.group(1))
    introduction = MOTIF_META.sub("", re.sub(r"^# .+$", "", entete, count=1, flags=re.M)).strip()
    ident_chap = meta_chap.get("chapitre", Path(chemin).stem)
    fiches = []
    for i, bloc in enumerate(re.split(r"\n(?=## )", contenu)[1:]):
        lignes = bloc.split("\n", 1)
        titre = lignes[0][3:].strip()
        corps = lignes[1] if len(lignes) > 1 else ""
        meta = {}
        m = MOTIF_META.search(corps)
        if m and corps[:m.start()].strip() == "":
            meta = _meta(m.group(1))
            corps = corps[m.end():]
        fiches.append(Fiche(
            ident=meta.get("fiche") or f"{ident_chap}-{i + 1}",
            titre=titre, chapitre=titre_chap, texte=corps.strip(),
            mots_cles=[x.strip() for x in meta.get("mots", "").split(",") if x.strip()],
            questions=[x.strip() for x in meta.get("questions", "").split(";") if x.strip()],
            aller=meta.get("aller", ""),
            chiffres=[x.strip() for x in meta.get("chiffres", "").split(",") if x.strip()],
            ordre=i,
        ))
    ordre = int(meta_chap.get("ordre", "0") or 0)
    return Chapitre(ident_chap, titre_chap, introduction, fiches, ordre)


_CACHE = {}


def charger(langue="fr"):
    """Chapitres du manuel dans la langue demandée (le français si la traduction manque)."""
    dossier = DOSSIER / langue
    if not dossier.exists() or not any(dossier.glob("*.md")):
        dossier = DOSSIER / "fr"
    fichiers = sorted(dossier.glob("*.md"))
    cle = (str(dossier), tuple((f.name, f.stat().st_mtime) for f in fichiers))
    if _CACHE.get("cle") != cle:
        chapitres = sorted((lire_chapitre(f) for f in fichiers), key=lambda c: (c.ordre, c.ident))
        _CACHE.update(cle=cle, chapitres=chapitres, index=Index(chapitres))
    return _CACHE["chapitres"]


def index(langue="fr"):
    charger(langue)
    return _CACHE["index"]


def toutes_les_fiches(chapitres):
    return [f for c in chapitres for f in c.fiches]


# ----------------------------------------------------------------------
# Recherche (BM25 simplifié + tolérance aux fautes de frappe)
# ----------------------------------------------------------------------
class Index:
    POIDS = {"questions": 3.5, "titre": 3.0, "mots": 2.5, "texte": 1.0}

    def __init__(self, chapitres):
        self.fiches = toutes_les_fiches(chapitres)
        self.champs = []
        documents = []
        for f in self.fiches:
            champs = {"questions": mots(" ".join(f.questions)), "titre": mots(f.titre),
                      "mots": mots(" ".join(f.mots_cles)), "texte": mots(f.texte)}
            self.champs.append(champs)
            documents.append(set().union(*champs.values()))
        n = max(len(documents), 1)
        frequence = {}
        for doc in documents:
            for m in doc:
                frequence[m] = frequence.get(m, 0) + 1
        self.idf = {m: math.log(1 + (n - d + 0.5) / (d + 0.5)) for m, d in frequence.items()}
        self.vocabulaire = sorted(self.idf)
        # Mots entiers du manuel -> leur racine : une faute de frappe se corrige mieux sur le mot entier
        # (« operaton » -> « operation ») que sur sa racine (« oper »).
        self.mots_entiers = {}
        for f in self.fiches:
            for j in jetons(" ".join([f.titre, f.texte, " ".join(f.questions), " ".join(f.mots_cles)])):
                self.mots_entiers.setdefault(j, racine(j))
        self.liste_mots_entiers = sorted(self.mots_entiers)
        self.longueur_moyenne = sum(len(c["texte"]) for c in self.champs) / n if self.champs else 1

    def _corriger(self, jeton):
        """Mot de la question -> racine connue du manuel ; une faute de frappe est corrigée vers le mot
        entier du manuel le plus proche, s'il ressemble assez."""
        r = racine(jeton)
        if r in self.idf or len(jeton) < 4:
            return r
        proches = difflib.get_close_matches(jeton, self.liste_mots_entiers, n=1,
                                            cutoff=0.8 if len(jeton) >= 7 else 0.85)
        return self.mots_entiers[proches[0]] if proches else r

    def part_connue(self, question):
        """Part des mots de la question connus du manuel (après correction des fautes de frappe).
        Une question dont la plupart des mots sont inconnus est sans doute hors sujet."""
        liste = jetons(question)
        if not liste:
            return 0.0
        return sum(1 for j in liste if self._corriger(j) in self.idf) / len(liste)

    def chercher(self, question, nombre=5):
        """Liste de (score, fiche), du plus pertinent au moins pertinent."""
        termes = [self._corriger(j) for j in jetons(question)]
        termes = list(dict.fromkeys(t for t in termes if t in self.idf))
        if not termes:
            return []
        resultats = []
        for fiche, champs in zip(self.fiches, self.champs):
            score = 0.0
            for terme in termes:
                for nom, poids in self.POIDS.items():
                    tf = champs[nom].count(terme)
                    if not tf:
                        continue
                    longueur = len(champs[nom]) or 1
                    if nom == "texte":
                        norme = 0.25 + 0.75 * longueur / self.longueur_moyenne
                    elif nom == "questions":                    # beaucoup de formulations : pas de pénalité
                        norme = 1.0 + 0.02 * longueur
                    else:
                        norme = 1.0
                    score += poids * self.idf[terme] * (tf * 2.2) / (tf + 1.2 * norme)
            # bonus : tous les termes de la question sont présents dans la fiche
            couverture = sum(1 for terme in termes if any(terme in champs[n] for n in champs)) / len(termes)
            score *= 0.6 + 0.4 * couverture
            # Une question qui reprend les mots du titre vise sans doute cette fiche
            if champs["titre"]:
                score *= 1 + 0.25 * sum(1 for terme in termes if terme in champs["titre"]) / len(termes)
            # Le glossaire (une fiche par lettre, beaucoup de termes) ne doit pas l'emporter sur
            # la fiche qui traite vraiment du sujet : il reste trouvé quand rien d'autre ne répond.
            if fiche.ident.startswith("glossaire-"):
                score *= 0.75
            if score > 0:
                resultats.append((score, fiche))
        resultats.sort(key=lambda r: -r[0])
        return resultats[:nombre]


def repondre(question, langue="fr", nombre=4):
    """{'reponse': Fiche ou None, 'proches': [Fiche...], 'scores': [...]} pour une question."""
    idx = index(langue)
    resultats = idx.chercher(question, nombre=nombre + 1)
    if resultats and resultats[0][0] >= SEUIL_REPONSE and idx.part_connue(question) >= PART_CONNUE_MIN:
        return {"reponse": resultats[0][1], "proches": [f for s, f in resultats[1:] if s >= SEUIL_SUGGESTION][:3],
                "score": resultats[0][0]}
    return {"reponse": None, "proches": [f for s, f in resultats if s >= SEUIL_SUGGESTION][:3],
            "score": resultats[0][0] if resultats else 0.0}


def questions_sans_reponse():
    """Questions restées sans réponse (journal local) : liste de (date, question), les plus récentes d'abord."""
    import csv
    if not JOURNAL.exists():
        return []
    try:
        with JOURNAL.open(encoding="utf-8") as f:
            lignes = [(l["date"], l["question"]) for l in csv.DictReader(f) if l.get("question")]
    except (OSError, KeyError, csv.Error):
        return []
    return lignes[::-1]


def noter_sans_reponse(question):
    """Garde la question dans un fichier local (jamais envoyé), pour compléter le manuel."""
    import csv
    import datetime
    try:
        JOURNAL.parent.mkdir(parents=True, exist_ok=True)
        nouveau = not JOURNAL.exists()
        with JOURNAL.open("a", newline="", encoding="utf-8") as f:
            ecrivain = csv.writer(f)
            if nouveau:
                ecrivain.writerow(["date", "question"])
            ecrivain.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), question.strip()[:300]])
    except OSError:
        pass                                    # dossier en lecture seule : tant pis


# ----------------------------------------------------------------------
# Mise en forme d'une fiche
# ----------------------------------------------------------------------
def texte_affiche(fiche):
    """Markdown affiché : [[Bouton]] -> **Bouton**."""
    return MOTIF_LIEN_ECRAN.sub(lambda m: f"**{m.group(1)}**", fiche.texte)


def resume_fiche(fiche, mots=80):
    """Début d'une fiche pour la bulle d'aide : les premiers paragraphes de texte (sans sous-titres,
    tableaux ni blocs de code), coupés à la fin d'un paragraphe ou d'une liste dès ~`mots` mots.
    Renvoie (markdown, tronque)."""
    morceaux, total, dans_code = [], 0, False
    paragraphes = [p.strip() for p in re.split(r"\n\s*\n", texte_affiche(fiche)) if p.strip()]
    for i, paragraphe in enumerate(paragraphes):
        if (paragraphe.startswith("```") and paragraphe.rstrip().endswith("```") and paragraphe.count("```") == 2
                and paragraphe.count("\n") <= 6 and not dans_code):     # formule courte : gardée
            morceaux.append(paragraphe)
            continue
        if paragraphe.startswith("```") or dans_code:
            if paragraphe.count("```") % 2:
                dans_code = not dans_code
            if total >= mots // 2:
                break
            continue
        if dans_code or paragraphe.startswith("|"):
            if total >= mots // 2:
                break
            continue
        if paragraphe.startswith("#"):                     # sous-titre : gardé en gras si on continue
            if total >= mots // 2:
                break
            titre, _, reste = paragraphe.partition("\n")
            paragraphe = "**" + titre.lstrip("# ").strip() + "**" + ("\n\n" + reste if reste.strip() else "")
            if not reste.strip():
                morceaux.append(paragraphe)
                continue
        morceaux.append(paragraphe)
        total += len(paragraphe.split())
        if total >= mots:
            return "\n\n".join(morceaux), i < len(paragraphes) - 1
    return "\n\n".join(morceaux), len(morceaux) < len(paragraphes)


def elements_ecran(chapitres):
    """Tous les [[éléments d'écran]] cités dans le manuel : {libellé: [identifiants de fiches]}."""
    trouves = {}
    for f in toutes_les_fiches(chapitres):
        for libelle in MOTIF_LIEN_ECRAN.findall(f.texte):
            trouves.setdefault(libelle, []).append(f.ident)
    return trouves


def destination(fiche):
    """('Espace de travail', 'Onglet' ou '') d'après la métadonnée « aller »."""
    if not fiche.aller:
        return None
    morceaux = [m.strip() for m in fiche.aller.split("/")]
    return morceaux[0], (morceaux[1] if len(morceaux) > 1 else "")
