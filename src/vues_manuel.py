"""
vues_manuel.py — Espace « Manuel et aide » : l'assistant « Poser une question »,
le sommaire du manuel, et le téléchargement du manuel complet.

L'assistant cherche dans le manuel (src/manuel.py) : il fonctionne hors
connexion, n'envoie rien, et n'affiche que des fiches écrites à l'avance.
Les « chiffres » d'une fiche (Sharpe, volatilité…) sont ceux du dernier
portefeuille analysé, gardés en mémoire pour la session.
"""

from pathlib import Path

import streamlit as st

from . import interface as ui
from . import langues, manuel
from .interface import euros, nombre, pct
from .langues import t

DOSSIER_EXPORTS = Path(__file__).resolve().parent.parent / "docs" / "manuel"

# Valeurs du portefeuille qu'une fiche peut afficher (métadonnée « chiffres ») :
# clé -> (intitulé, où la lire dans les résultats, mise en forme)
CHIFFRES = {
    "valeur_actuelle": ("Valeur actuelle", ("resume", "valeur_actuelle"), "euros"),
    "montant_investi": ("Montant investi", ("resume", "montant_investi"), "euros"),
    "gain_total": ("Gain total", ("resume", "gain_total"), "euros_signe"),
    "dividendes": ("Dividendes et coupons", ("resume", "dividendes"), "euros"),
    "frais_totaux": ("Frais de courtage", ("resume", "frais_totaux"), "euros"),
    "twr_total": ("TWR total", ("indicateurs", "twr_total"), "pct"),
    "twr_annualise": ("TWR annualisé", ("indicateurs", "twr_annualise"), "pct"),
    "tri_annuel": ("TRI annuel", ("indicateurs", "tri_annuel"), "pct"),
    "volatilite": ("Volatilité", ("indicateurs", "volatilite"), "pct_brut"),
    "max_drawdown": ("Max drawdown", ("indicateurs", "max_drawdown"), "pct"),
    "sharpe": ("Ratio de Sharpe", ("avances", "sharpe"), "nombre"),
    "sortino": ("Ratio de Sortino", ("avances", "sortino"), "nombre"),
    "beta": ("Bêta", ("avances", "beta"), "nombre"),
    "alpha": ("Alpha de Jensen", ("avances", "alpha"), "pct"),
    "tracking_error": ("Tracking error", ("avances", "tracking_error"), "pct_brut"),
    "var_historique": ("VaR historique", ("avances", "var_historique"), "pct_brut"),
    "var_parametrique": ("VaR loi normale", ("avances", "var_parametrique"), "pct_brut"),
    "var_cornish_fisher": ("VaR Cornish-Fisher", ("avances", "var_cornish_fisher"), "pct_brut"),
    "cvar": ("CVaR (Expected Shortfall)", ("avances", "cvar"), "pct_brut"),
    "asymetrie": ("Asymétrie", ("avances", "asymetrie"), "nombre"),
    "kurtosis": ("Kurtosis en excès", ("avances", "kurtosis"), "nombre"),
    "nb_titres": ("Titres en portefeuille", ("resume", "nb_lignes"), "entier"),
    "nb_operations": ("Opérations", ("transactions", None), "entier"),
}


def memoriser_chiffres(res):
    """Garde les valeurs brutes du portefeuille analysé (appelé par app.py après l'analyse)."""
    valeurs = {}
    for cle, (_, (bloc, champ), _) in CHIFFRES.items():
        try:
            valeurs[cle] = len(res[bloc]) if champ is None else float(res[bloc][champ])
        except Exception:
            continue
    st.session_state["chiffres_manuel"] = valeurs


def _formater(valeur, format_):
    if valeur != valeur:                              # NaN
        return t("n.d.")
    return {"euros": lambda v: euros(v), "euros_signe": lambda v: euros(v, signe=True),
            "pct": lambda v: pct(v), "pct_brut": lambda v: pct(v, signe=False),
            "nombre": lambda v: nombre(v), "entier": lambda v: f"{v:.0f}"}[format_](valeur)


ESPACES_ONGLETS = {"Analyse du portefeuille", "Conseil patrimonial", "Gestion d'actifs", "Manuel et aide"}


def afficher():
    langue = langues.langue()
    chapitres = manuel.charger(langue)
    fiches = {f.ident: f for f in manuel.toutes_les_fiches(chapitres)}

    html(ui.titre_section(t("Manuel et aide"),
                          t("Posez une question ou parcourez le manuel. Tout fonctionne hors connexion : "
                            "les réponses viennent du manuel, rien n'est envoyé sur Internet.")))

    # ------------------------------------------------------------------ assistant
    if "question_a_appliquer" in st.session_state:          # exemple cliqué / « Voir aussi » (tour précédent)
        st.session_state["question_aide"] = st.session_state.pop("question_a_appliquer")
    with st.container(border=True):
        question = st.text_input(t("Poser une question"), key="question_aide",
                                 placeholder=t("Par exemple : comment supprimer une opération ?"))
        exemples = [t("Comment supprimer une opération ?"), t("Que veut dire le ratio de Sharpe ?"),
                    t("D'où viennent les cours ?")]
        colonnes = st.columns(len(exemples))
        for colonne, exemple in zip(colonnes, exemples):
            if colonne.button(exemple, type="tertiary", key=f"exemple_{exemple}"):
                st.session_state["question_a_appliquer"] = exemple
                st.session_state.pop("fiche_ouverte", None)
                st.rerun()
        if question and question.strip():
            resultat = manuel.repondre(question, langue)
            if resultat["reponse"] is not None:
                _fiche(resultat["reponse"], principale=True)
                if resultat["proches"]:
                    _voir_aussi(resultat["proches"])
                if st.button(t("Ce n'est pas la réponse que je cherchais"), type="tertiary", key="pas_la_reponse",
                             help=t("Note la question (sur cet ordinateur) pour améliorer le manuel")):
                    manuel.noter_sans_reponse(question)
                    st.session_state["derniere_question_notee"] = question
                    st.toast(t("Merci : la question est notée pour compléter le manuel."))
            else:
                st.info(t("Je n'ai pas trouvé de réponse sûre dans le manuel. Essayez d'autres mots, ou consultez "
                          "les fiches les plus proches ci-dessous. Votre question est notée (sur cet ordinateur "
                          "uniquement) pour compléter le manuel."))
                if st.session_state.get("derniere_question_notee") != question:
                    manuel.noter_sans_reponse(question)
                    st.session_state["derniere_question_notee"] = question
                if resultat["proches"]:
                    _voir_aussi(resultat["proches"], titre=t("Fiches les plus proches"))

    # ------------------------------------------------------------------ fiche ouverte depuis « Voir aussi »
    ouverte = st.session_state.get("fiche_ouverte")
    if ouverte in fiches and not (question and question.strip()):
        with st.container(border=True):
            _fiche(fiches[ouverte], principale=True)

    # ------------------------------------------------------------------ sommaire
    with st.container(border=True):
        html(ui.titre_section(t("Sommaire du manuel"),
                              t("{c} chapitres · {f} fiches", c=len(chapitres), f=len(fiches))))
        if not chapitres:
            st.caption(t("Le manuel est introuvable (dossier docs/manuel)."))
            return
        noms = [c.titre for c in chapitres]
        choix = st.selectbox(t("Chapitre"), range(len(chapitres)), format_func=lambda i: f"{i + 1}. {noms[i]}",
                             key="chapitre_manuel")
        chapitre = chapitres[choix]
        if chapitre.introduction:
            st.markdown(chapitre.introduction)
        for fiche in chapitre.fiches:
            with st.expander(fiche.titre, expanded=(fiche.ident == ouverte)):
                _fiche(fiche, principale=False)
        _telechargements(langue)

    # ------------------------------------------------------------------ questions restées sans réponse
    sans_reponse = manuel.questions_sans_reponse()
    if sans_reponse:
        with st.expander(t("Questions restées sans réponse ({n})", n=len(sans_reponse))):
            st.caption(t("Notées sur cet ordinateur uniquement. Envoyez ce fichier au créateur du logiciel pour "
                         "compléter le manuel : chaque question ajoutée améliore l'assistant."))
            for date, texte in sans_reponse[:30]:
                st.markdown(f"- {date} · {texte}")
            st.download_button(t("Exporter les questions (CSV)"), data=manuel.JOURNAL.read_bytes(),
                               file_name="questions_sans_reponse.csv", mime="text/csv", key="export_questions")


def html(morceau):
    st.markdown(morceau, unsafe_allow_html=True)


def _fiche(fiche, principale=True):
    if principale:
        st.caption(fiche.chapitre)
        st.markdown(f"#### {fiche.titre}")
    st.markdown(manuel.texte_affiche(fiche))
    _chiffres(fiche)
    _bouton_aller(fiche)


def _chiffres(fiche):
    valeurs = st.session_state.get("chiffres_manuel") or {}
    lignes = [(CHIFFRES[c][0], _formater(valeurs[c], CHIFFRES[c][2])) for c in fiche.chiffres
              if c in CHIFFRES and c in valeurs]
    if lignes:
        texte = " · ".join(f"{t(nom)} : {valeur}" if not langues.anglais() else f"{t(nom)}: {valeur}"
                           for nom, valeur in lignes)
        html(ui.note(t("Pour votre portefeuille : {valeurs}", valeurs=texte)))


def _bouton_aller(fiche):
    cible = manuel.destination(fiche)
    if not cible or cible[0] not in ESPACES_ONGLETS or cible[0] == "Manuel et aide":
        return
    espace, onglet = cible
    libelle = t("Aller à « {espace} »", espace=t(espace)) + (t(", onglet « {onglet} »", onglet=t(onglet))
                                                             if onglet else "")
    if st.button(libelle, key=f"aller_{fiche.ident}_{id(fiche)}", type="secondary"):
        st.session_state["espace_actif"] = espace
        st.session_state.pop("fiche_ouverte", None)
        if onglet:
            st.session_state["message_compte"] = t("Ouvrez l'onglet « {onglet} ».", onglet=t(onglet))
        st.rerun()


def _voir_aussi(proches, titre=None):
    st.caption(titre or t("Voir aussi"))
    for fiche in proches:
        if st.button(fiche.titre, type="tertiary", key=f"voir_{fiche.ident}"):
            st.session_state["fiche_ouverte"] = fiche.ident
            st.session_state["question_a_appliquer"] = ""
            st.rerun()


def _telechargements(langue):
    fichiers = [(DOSSIER_EXPORTS / f"Manuel_Portfolio_Tracker_{langue}.docx", "Word", "application/vnd."
                 "openxmlformats-officedocument.wordprocessingml.document"),
                (DOSSIER_EXPORTS / f"Manuel_Portfolio_Tracker_{langue}.pdf", "PDF", "application/pdf")]
    disponibles = [(f, nom, mime) for f, nom, mime in fichiers if f.exists()]
    if not disponibles:
        return
    colonnes = st.columns(len(disponibles) + 2)
    for colonne, (f, nom, mime) in zip(colonnes, disponibles):
        colonne.download_button(t("Manuel complet ({format})", format=nom), data=f.read_bytes(), file_name=f.name,
                                mime=mime, key=f"manuel_{nom}")
