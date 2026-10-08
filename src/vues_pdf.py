"""
vues_pdf.py — Formulaire « Compléter l'opération » : le filet de sécurité de l'import PDF.

Quand un PDF n'est pas lu automatiquement (mise en page inconnue, chiffres incohérents,
titre introuvable…), au lieu d'un simple message d'erreur, ce formulaire propose tout ce
qui a été trouvé dans le document (src/lecture_pdf.candidats) :

    - la date d'exécution probable, et les autres dates du document ;
    - le ou les codes ISIN, avec le nom du titre ;
    - le sens (achat, vente, dividende) ;
    - pour la quantité, le cours et les frais : une liste des nombres trouvés, chacun avec
      les mots qui l'entourent (« Quantité : [60] »), la meilleure proposition déjà choisie.

L'utilisateur vérifie, corrige au besoin (on peut aussi taper une autre valeur) et valide.
Rien n'est inventé : chaque valeur proposée figure dans le document.
Utilisé par la page « Ajouter des opérations » (src/vues_mouvements.py) et par l'envoi d'un
fichier depuis la barre latérale (app.py).
"""

import pandas as pd
import streamlit as st

from . import import_fichier, lecture_pdf
from . import interface as ui
from .langues import anglais, t, td

TYPES = ["ACHAT", "VENTE", "DIVIDENDE"]


def html(morceau):
    st.markdown(morceau, unsafe_allow_html=True)


def resoudre_titre(saisie):
    """Ticker Yahoo et nom d'un titre saisi à la main (ticker, ISIN, nom ou code Bloomberg)."""
    saisie = saisie.strip()
    from .analyse import charger_referentiel
    connus = set(charger_referentiel().index)
    nature = import_fichier.nature_identifiant(saisie, connus)
    if nature == "ticker":
        return saisie.upper(), ""
    resolution = import_fichier.resoudre_identifiants([saisie], tickers_connus=connus)
    ligne = resolution.iloc[0]
    if ligne["statut"] == "introuvable":
        raise ValueError(t("Titre introuvable : {titre}. Indiquez son ticker Yahoo Finance (ex. MC.PA).",
                           titre=saisie))
    return ligne["ticker"], ligne.get("nom", "") or ""


@st.cache_data(show_spinner=False, ttl=3600, max_entries=20)
def candidats_pdf(brut):
    """Ce que contient le PDF (texte intégré, ou reconnaissance de caractères pour un scan
    ou un texte « codé »)."""
    textes = []
    try:
        textes = [p["texte"] for p in import_fichier._pages_pdf(brut)]
    except Exception:
        pass
    texte = "".join(textes)
    if len(texte.strip()) < 20 or lecture_pdf.texte_illisible(texte):
        from . import ocr
        textes = ocr.texte_pdf(brut) if ocr.disponible() else []
        if textes and not lecture_pdf.isins("\n".join(textes)):        # 2e essai : image nettoyée et redressée
            textes = ocr.texte_pdf(brut, echelle=4, pretraitement=True)
    return lecture_pdf.candidats(textes)


@st.cache_data(show_spinner=False, ttl=3600, max_entries=50)
def cours_marche(isin, date):
    """(ticker, cours de clôture) du titre le jour de l'opération, ou None (pas d'Internet,
    titre introuvable). Sert à vérifier le prix lu et à classer les propositions."""
    try:
        ticker, _ = resoudre_titre(isin)
        jour = pd.to_datetime(date, dayfirst=True)
        from .market_data import obtenir_historique
        from pathlib import Path
        cache = Path(__file__).resolve().parent.parent / "data" / "cache_import.csv"
        historique, _ = obtenir_historique([ticker], (jour - pd.Timedelta(days=10)).strftime("%Y-%m-%d"),
                                           chemin_cache=cache)
        cours = import_fichier._valeur_au(historique[ticker], jour)
        return (ticker, float(cours)) if cours == cours else None
    except Exception:
        return None


def _empreinte(brut):
    import hashlib
    return hashlib.md5(brut).hexdigest()[:12]


def version_lisible(brut):
    """Le PDF tel qu'il faut le lire : sa copie déchiffrée si l'utilisateur a donné le mot de passe."""
    return st.session_state.get("pdf_dechiffres", {}).get(_empreinte(brut), brut)


def demander_mot_de_passe(brut, nom_fichier, cle):
    """PDF protégé : champ mot de passe. Le PDF déchiffré est gardé en mémoire pour la session
    (le mot de passe, lui, n'est conservé nulle part) ; la page est alors relancée."""
    with st.container(border=True):
        html(ui.titre_section(t("PDF protégé"), nom_fichier))
        st.caption(t(import_fichier.MESSAGE_PROTEGE))
        with st.form(f"pdf_mdp_{cle}", border=False):
            mot_de_passe = st.text_input(t("Mot de passe du PDF"), type="password", key=f"pdf_mdp_champ_{cle}")
            ouvrir = st.form_submit_button(t("Ouvrir le PDF"), type="primary")
        if ouvrir and mot_de_passe:
            try:
                st.session_state.setdefault("pdf_dechiffres", {})[_empreinte(brut)] = \
                    import_fichier.dechiffrer_pdf(brut, mot_de_passe)
                st.rerun()
            except ValueError:
                st.error(t("Mot de passe incorrect."))


def formulaire_utile(brut):
    """Vrai si le PDF n'a donné aucune opération : le formulaire remplace alors l'assistant
    d'import (qui sert aux tableaux)."""
    try:
        import_fichier.grille_pdf(brut)
        return False
    except Exception:
        return True


def _nombre_texte(valeur):
    texte = f"{valeur:.6f}".rstrip("0").rstrip(".")
    return texte if anglais() else texte.replace(".", ",")


def _choix_nombre(colonne, libelle, nombres, propose, cle, aide, proche_de=None):
    """Liste des nombres trouvés (avec leur contexte), la proposition choisie d'avance ;
    on peut aussi taper une autre valeur. proche_de : sans proposition, les nombres les plus
    proches de cette valeur (le cours du marché) passent en tête."""
    options, vus = [], set()
    if proche_de and propose is None:
        nombres = sorted(nombres, key=lambda n: abs(n["valeur"] / proche_de - 1))
    if propose is not None:
        options.append(_nombre_texte(propose))
        vus.add(round(propose, 6))
    contextes = {}
    for n in nombres:
        if round(n["valeur"], 6) in vus:
            contextes.setdefault(_nombre_texte(n["valeur"]), n["contexte"])
            continue
        vus.add(round(n["valeur"], 6))
        options.append(_nombre_texte(n["valeur"]))
        contextes[_nombre_texte(n["valeur"])] = n["contexte"]
    choix = colonne.selectbox(
        libelle, options, index=0 if propose is not None else None, key=cle, accept_new_options=True,
        placeholder=t("Choisir ou saisir"), help=aide,
        format_func=lambda o: f"{o}   ·   {contextes[o]}" if o in contextes else o)
    if choix in (None, ""):
        return None
    valeur = import_fichier.convertir_nombres(pd.Series([str(choix)])).iloc[0]
    return None if valeur != valeur else abs(float(valeur))


def formulaire(brut, nom_fichier, cle, raison=None):
    """Affiche le formulaire. Renvoie l'opération validée (dict : date, type, ticker, nom,
    quantite, prix, frais) au moment de la validation, sinon None."""
    with st.container(border=True):
        html(ui.titre_section(t("Compléter l'opération"),
                              t("{nom} : valeurs trouvées dans le document, à vérifier", nom=nom_fichier)))
        if raison:
            st.caption(t(raison))
        with st.spinner(t("Lecture du document...")):
            c = candidats_pdf(brut)
        proposition = c["proposition"] or {}
        if not (c["isins"] or c["nombres"] or c["dates"]):
            st.info(t("Aucun texte lisible dans ce document : saisissez l'opération à la main."))

        # Cours de clôture du jour (si Internet) : pour vérifier le prix lu
        isin_propose = proposition.get("isin") or (c["isins"][0][0] if c["isins"] else None)
        date_lue = proposition.get("date") or c["date_proposee"]
        marche = cours_marche(isin_propose, date_lue) if isin_propose and date_lue else None
        if marche:
            st.caption(t("Cours de clôture de {ticker} le {date} : {cours} (Yahoo Finance) — le prix unitaire doit en "
                         "être proche.", ticker=marche[0], date=date_lue, cours=_nombre_texte(round(marche[1], 4))))

        # Le type est choisi hors du formulaire : un dividende n'a pas les mêmes champs
        sens_propose = import_fichier.classer_type(proposition.get("sens") or "") if proposition.get("sens") else \
            c["sens"]
        sens_propose = sens_propose if sens_propose in TYPES else "ACHAT"
        type_operation = st.segmented_control(t("Type"), TYPES, default=sens_propose, format_func=td,
                                              key=f"pdf_type_{cle}") or sens_propose
        dividende = type_operation == "DIVIDENDE"

        with st.form(f"pdf_formulaire_{cle}", border=False):
            a, b = st.columns([1, 2])
            date_proposee = proposition.get("date") or c["date_proposee"]
            try:
                defaut = pd.to_datetime(date_proposee, dayfirst=True) if date_proposee else pd.Timestamp.today()
            except Exception:
                defaut = pd.Timestamp.today()
            date = a.date_input(t("Date d'exécution"), value=defaut, format="DD/MM/YYYY",
                                help=(t("Dates trouvées dans le document : {dates}", dates=", ".join(c["dates"][:6]))
                                      if c["dates"] else None))
            titres = [f"{isin} · {nom}" if nom else isin for isin, nom in c["isins"]]
            titre = b.selectbox(t("Titre"), titres, index=0 if titres else None, accept_new_options=True,
                                placeholder=t("Ticker, ISIN, nom ou code Bloomberg"), key=f"pdf_titre_{cle}",
                                help=t("Code ISIN trouvé dans le document, ou tapez un ticker (ex. MC.PA), un ISIN "
                                       "ou un nom"))
            a, b, d = st.columns(3)
            if dividende:
                quantite = None
                prix = _choix_nombre(a, t("Montant total reçu"), c["nombres"], proposition.get("montant"),
                                     f"pdf_montant_{cle}", t("Montant brut du dividende ou du coupon"))
            else:
                quantite = _choix_nombre(a, t("Quantité"), c["nombres"], proposition.get("quantite"),
                                         f"pdf_quantite_{cle}", t("Nombre de titres achetés ou vendus"))
                prix = _choix_nombre(b, t("Prix unitaire"), c["nombres"], proposition.get("cours"), f"pdf_cours_{cle}",
                                     t("Prix d'un titre, dans sa devise de cotation (trouvée : {devise})",
                                       devise=proposition.get("devise") or c["devise"]),
                                     proche_de=marche[1] if marche else None)
            frais = _choix_nombre(d, t("Frais (€)"), c["nombres"], proposition.get("frais"), f"pdf_frais_{cle}",
                                  t("Courtage et taxes ; laissez vide s'il n'y en a pas"))
            if quantite and prix and not dividende:
                st.caption(t("Contrôle : {q} × {p} = {m}", q=_nombre_texte(quantite), p=_nombre_texte(prix),
                             m=_nombre_texte(round(quantite * prix, 2))))
            valider = st.form_submit_button(t("Ajouter cette opération"), type="primary", icon=":material/add:")
        if c["texte"].strip():
            with st.expander(t("Texte lu dans le document")):
                st.code(c["texte"][:4000], language=None)
                st.download_button(
                    t("Préparer un rapport anonymisé"), key=f"pdf_rapport_{cle}",
                    data=lecture_pdf.rapport_anonymise([c["texte"]], nom_fichier=nom_fichier).encode("utf-8"),
                    file_name="rapport_lecture_pdf_anonymise.txt", mime="text/plain", type="tertiary",
                    help=t("Texte lu, sans nom, adresse, e-mail, téléphone ni numéro de compte : à envoyer au "
                           "créateur du logiciel pour qu'il améliore la lecture de ce type de document"))
        if not valider:
            return None
        try:
            if not titre:
                raise ValueError(t("Indiquez le titre."))
            if not prix or (not dividende and not quantite):
                raise ValueError(t("Indiquez la quantité et le cours.") if not dividende
                                 else t("Indiquez le montant reçu."))
            if pd.Timestamp(date) > pd.Timestamp.today():
                raise ValueError(t("La date est dans le futur."))
            code = str(titre).split(" · ")[0].strip()
            nom_lu = str(titre).split(" · ", 1)[1].strip() if " · " in str(titre) else ""
            with st.spinner(t("Recherche du titre...")):
                ticker, nom = resoudre_titre(code)
        except Exception as erreur:
            st.error(str(erreur))
            return None
        if not dividende and c["texte"].strip():
            # retenir le modèle de ce document : le prochain avis du même type sera lu tout seul
            lecture_pdf.apprendre(c["texte"], {"date": pd.Timestamp(date).strftime("%d/%m/%Y"), "type": type_operation,
                                               "quantite": quantite, "cours": prix, "frais": frais,
                                               "montant": round(quantite * prix, 2)})
            import_fichier._GRILLES_PDF.clear()          # relire les PDF avec ce nouveau modèle
        return {"date": pd.Timestamp(date), "type": type_operation, "ticker": ticker, "nom": nom or nom_lu or code,
                "quantite": 0.0 if dividende else float(quantite), "prix": float(prix), "frais": float(frais or 0)}


# ----------------------------------------------------------------------
# Plusieurs fichiers envoyés d'un coup depuis la barre latérale
# ----------------------------------------------------------------------
def lot_de_fichiers(fichiers, importer):
    """Lit chaque fichier (lecture automatique, sinon mot de passe ou formulaire pour un PDF) et
    réunit toutes les opérations. Renvoie (contenu CSV, nom, résumé) quand tout est prêt — ou
    quand l'utilisateur choisit d'analyser les fichiers déjà lus —, sinon None (la page attend)."""
    import hashlib
    bruts = [(f.name, version_lisible(f.getvalue())) for f in fichiers]
    cle_lot = hashlib.md5("".join(_empreinte(b) for _, b in bruts).encode()).hexdigest()[:12]
    etat = st.session_state.setdefault("lots", {}).setdefault(cle_lot, {"operations": {}, "resumes": {}})
    en_attente = []
    with st.container(border=True):
        html(ui.titre_section(t("Fichiers envoyés"), t("{n} fichiers : chacun est lu, puis toutes les opérations "
                                                       "sont réunies dans un même portefeuille", n=len(bruts))))
        for nom, brut in bruts:
            empreinte = _empreinte(brut)
            if empreinte in etat["operations"]:
                st.caption(t("{nom} : {n} opération(s) lue(s).", nom=nom, n=len(etat["operations"][empreinte])))
                continue
            if import_fichier.est_protege(brut):
                demander_mot_de_passe(brut, nom, empreinte)
                en_attente.append(nom)
                continue
            attente, valeurs = import_fichier.message_attente(brut)
            with st.spinner(nom + " · " + t(attente, **valeurs)):
                resultat = importer(brut)
            if resultat["sur"]:
                etat["operations"][empreinte] = resultat["transactions"][["date", "type", "ticker", "nom", "quantite",
                                                                          "prix", "frais"]].to_dict("records")
                etat["resumes"][empreinte] = resultat["resume"]
                st.caption(t("{nom} : {n} opération(s) lue(s).", nom=nom, n=len(etat["operations"][empreinte])))
            elif import_fichier.nature_fichier(brut) == "pdf":
                operation = formulaire(brut, nom, empreinte, raison=resultat["raison"])
                if operation is not None:
                    etat["operations"][empreinte] = [operation]
                    st.rerun()
                en_attente.append(nom)
            else:
                st.error(t("{nom} : {raison}", nom=nom, raison=t(resultat["raison"])))
                st.caption(t("Envoyez ce fichier seul pour ouvrir l'assistant d'import."))
                en_attente.append(nom)
        lus = [o for ops in etat["operations"].values() for o in ops]
        if en_attente:
            st.caption(t("En attente : {noms}.", noms=", ".join(en_attente)))
            if not lus or not st.button(t("Analyser les {n} opération(s) déjà lues", n=len(lus)), key=f"lot_{cle_lot}"):
                return None
    tableau = pd.DataFrame(lus)
    tableau["date"] = pd.to_datetime(tableau["date"])
    avant = len(tableau)
    tableau = tableau.drop_duplicates(subset=["date", "type", "ticker", "quantite", "prix"])
    resume = {"operations": len(tableau), "titres": int(tableau["ticker"].nunique()), "controles_pdf": []}
    for r in etat["resumes"].values():
        resume["controles_pdf"] += r.get("controles_pdf", [])
    if len(tableau) < avant:
        resume["controles_pdf"].append({"texte": "{n} opération(s) présente(s) dans deux fichiers comptée(s) une "
                                                 "seule fois.", "valeurs": {"n": avant - len(tableau)}})
    return import_fichier.en_csv(tableau.sort_values("date")), t("{n} fichiers", n=len(bruts)), resume
