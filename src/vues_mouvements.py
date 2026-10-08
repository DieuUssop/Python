"""
vues_mouvements.py — Page « Ajouter des opérations » : mettre à jour un
portefeuille avec seulement les NOUVEAUX mouvements, sans renvoyer tout
l'historique.

Trois façons d'ajouter :
    1. un fichier Excel / CSV des dernières opérations (n'importe quel format) ;
    2. un ou plusieurs PDF (avis d'opéré, relevé, y compris scannés) ; si un PDF n'est pas lu
       automatiquement, un formulaire pré-rempli permet de compléter l'opération (src/vues_pdf.py) ;
    3. une saisie à la main (un ordre d'achat, par exemple).

Avant d'enregistrer : tableau de vérification modifiable, doublons décochés,
contrôles bloquants (vente de titres non détenus, date future).
Les calculs sont dans src/mouvements.py.
"""

import hashlib

import pandas as pd
import streamlit as st

from . import import_fichier, lecture_pdf, mouvements, vues_pdf
from . import interface as ui
from .langues import t, td


def html(morceau):
    st.markdown(morceau, unsafe_allow_html=True)


def ouvrir(cible):
    """Ouvre la page pour un portefeuille. cible : {"type": "perso"|"session", "id", "nom", "contenu"}."""
    st.session_state["ajout_operations"] = cible
    st.session_state.pop("ops_ajoutees", None)
    st.session_state.pop("page_compte", None)


def fermer():
    for cle in ("ajout_operations", "ops_ajoutees", "ops_fichiers"):
        st.session_state.pop(cle, None)


_resoudre_titre = vues_pdf.resoudre_titre       # ticker et nom d'un titre saisi à la main


def _avis_ost(brut):
    """Avis de division / regroupement d'actions (src/lecture_pdf.lire_ost), ou None."""
    if import_fichier.nature_fichier(brut) != "pdf":
        return None
    try:
        texte = "\n".join(p["texte"] for p in import_fichier._pages_pdf(brut))
    except Exception:
        return None
    return lecture_pdf.lire_ost(texte)


def _proposer_ost(ost, nom_fichier, empreinte, cible, session_compte):
    """Avis d'opération sur titres : propose d'ajuster les opérations antérieures du titre."""
    with st.container(border=True):
        html(ui.titre_section(t("Opération sur titres"), nom_fichier))
        try:
            ticker, nom = vues_pdf.resoudre_titre(ost["isin"])
        except Exception:
            st.warning(t("Titre introuvable : {titre}. Indiquez son ticker Yahoo Finance (ex. MC.PA).",
                         titre=ost["isin"]))
            return
        facteur = ost["facteur"]
        parite = (t("1 ancienne → {n} nouvelles", n=f"{facteur:g}") if facteur > 1
                  else t("{n} anciennes → 1 nouvelle", n=f"{1 / facteur:g}"))
        st.write(t("{nature} de {titre} ({ticker}) le {date} : {parite}.",
                   nature=t("Division") if facteur > 1 else t("Regroupement"), titre=nom or ost["libelle"],
                   ticker=ticker, date=ost["date"] or "?", parite=parite))
        ajuste, n = mouvements.appliquer_division(cible["contenu"], ticker, pd.to_datetime(ost["date"], dayfirst=True),
                                                  facteur)
        if not n:
            st.caption(t("Aucune opération de ce titre avant cette date : rien à ajuster."))
            return
        st.caption(t("Les {n} opération(s) antérieures seront converties (quantité × {f}, prix ÷ {f}), comme les "
                     "cours de Yahoo Finance, déjà ajustés.", n=n, f=f"{facteur:g}"))
        if st.button(t("Appliquer aux opérations antérieures"), type="primary", key=f"ost_{empreinte}"):
            contenu = mouvements.en_csv(ajuste)
            if cible["type"] == "perso" and session_compte is not None:
                session_compte.enregistrer(cible["nom"], contenu, identifiant=cible["id"], garder_precedente=True)
            else:
                st.session_state["fusion_session"] = {"origine": cible["origine"], "contenu": contenu,
                                                      "nom": cible["nom"]}
            st.session_state["message_compte"] = t("{n} opération(s) de {ticker} ajustée(s).", n=n, ticker=ticker)
            fermer()
            st.rerun()


def page(session_compte, importer):
    cible = st.session_state["ajout_operations"]
    ajoutees = st.session_state.setdefault("ops_ajoutees", [])
    html(ui.titre_section(t("Ajouter des opérations"), t("Portefeuille : {nom}", nom=cible["nom"])))
    if st.button(t("Retour au tableau de bord"), icon=":material/arrow_back:", key="retour_ajout"):
        fermer()
        st.rerun()
    html(ui.note(t("Envoyez seulement les nouveaux mouvements : un avis d'opéré (PDF), un export des dernières "
                   "opérations (Excel, CSV ou PDF), ou saisissez un ordre à la main. Les opérations déjà présentes "
                   "sont reconnues et ne sont pas ajoutées deux fois.")))

    fichier_tab, saisie_tab = st.tabs([t("Depuis un fichier"), t("Saisie manuelle")])
    with fichier_tab:
        fichiers = st.file_uploader(t("Fichiers (CSV, Excel ou PDF)"), type=["csv", "xlsx", "pdf"],
                                    accept_multiple_files=True, key="ops_fichiers")
        for f in fichiers or []:
            brut = vues_pdf.version_lisible(f.getvalue())          # PDF déchiffré si mot de passe donné
            empreinte = hashlib.md5(brut).hexdigest()[:12]
            if any(a.get("source") == empreinte for a in ajoutees):
                continue
            if import_fichier.est_protege(brut):
                vues_pdf.demander_mot_de_passe(brut, f.name, empreinte)
                continue
            ost = _avis_ost(brut)
            if ost is not None:                                     # division ou regroupement d'actions
                _proposer_ost(ost, f.name, empreinte, cible, session_compte)
                continue
            with st.spinner(t("Lecture de {nom}...", nom=f.name)):
                resultat = importer(brut)
            if resultat["sur"]:
                tableau = resultat["transactions"][mouvements.COLONNES].copy()
                tableau["source"] = empreinte
                ajoutees.extend(tableau.to_dict("records"))
                st.success(t("{nom} : {n} opération(s) lue(s).", nom=f.name, n=len(tableau)))
            elif import_fichier.nature_fichier(brut) == "pdf":
                # PDF non lu automatiquement : formulaire pré-rempli avec ce qui a été trouvé
                operation = vues_pdf.formulaire(brut, f.name, empreinte, raison=resultat["raison"])
                if operation is not None:
                    ajoutees.append({**operation, "source": empreinte})
                    st.rerun()
            else:
                st.error(t("{nom} : {raison}", nom=f.name, raison=t(resultat["raison"])))
                st.caption(t("Pour un format inhabituel, envoyez le fichier depuis la barre latérale : "
                             "l'assistant d'import vous guidera."))
    with saisie_tab:
        with st.form("saisie_operation", clear_on_submit=True, border=False):
            a, b, c = st.columns(3)
            date = a.date_input(t("Date"), value=pd.Timestamp.today(), format="DD/MM/YYYY")
            sens = b.selectbox(t("Type"), ["ACHAT", "VENTE", "DIVIDENDE"], format_func=td)
            titre = c.text_input(t("Titre"), placeholder=t("Ticker, ISIN, nom ou code Bloomberg"))
            a, b, c = st.columns(3)
            quantite = a.number_input(t("Quantité"), min_value=0.0, value=1.0, step=1.0)
            prix = b.number_input(t("Prix unitaire (devise du titre) ou montant du dividende"), min_value=0.0,
                                  value=0.0, step=1.0)
            frais = c.number_input(t("Frais (€)"), min_value=0.0, value=0.0, step=0.5)
            if st.form_submit_button(t("Ajouter à la liste"), icon=":material/add:"):
                try:
                    if not titre.strip():
                        raise ValueError(t("Indiquez le titre."))
                    with st.spinner(t("Recherche du titre...")):
                        ticker, nom = _resoudre_titre(titre)
                    ajoutees.append({"date": pd.Timestamp(date), "type": sens, "ticker": ticker,
                                     "nom": nom or titre.strip(), "quantite": quantite, "prix": prix,
                                     "frais": frais, "source": "saisie"})
                except Exception as erreur:
                    st.error(str(erreur))

    if not ajoutees:
        return
    # ------------------------------------------------------------------ vérification
    nouvelles = pd.DataFrame(ajoutees)[mouvements.COLONNES]
    preparees, _ = mouvements.preparer(cible["contenu"], nouvelles)
    with st.container(border=True):
        html(ui.titre_section(t("Vérification avant enregistrement"),
                              t("Décochez une ligne pour ne pas l'ajouter. Les cellules sont modifiables.")))
        affichage = preparees.assign(statut=preparees["statut"].map(t))
        modifiees = st.data_editor(
            affichage[["inclure", "statut"] + mouvements.COLONNES], hide_index=True, width="stretch",
            key="verification_ops", disabled=["statut"],
            column_config={
                "inclure": st.column_config.CheckboxColumn(t("Ajouter")),
                "statut": st.column_config.TextColumn(t("Statut")),
                "date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                "type": st.column_config.SelectboxColumn(t("Type"), options=["ACHAT", "VENTE", "DIVIDENDE"]),
                "ticker": st.column_config.TextColumn("Ticker"),
                "nom": st.column_config.TextColumn(t("Titre")),
                "quantite": st.column_config.NumberColumn(t("Quantité")),
                "prix": st.column_config.NumberColumn(t("Prix")),
                "frais": st.column_config.NumberColumn(t("Frais")),
            })
        retenues = modifiees[modifiees["inclure"].astype(bool)]
        fusion = mouvements.fusionner(cible["contenu"], modifiees)
        alertes = mouvements.controler(fusion)
        bloquantes = [a for a in alertes if a["bloquant"]]
        for a in bloquantes:
            st.error(t(a["message"], **a["valeurs"]))
        avant = mouvements.lire(cible["contenu"])
        st.caption(t("{n} opération(s) ajoutée(s) · {total} au total ({avant} avant)", n=len(retenues),
                     total=len(fusion), avant=len(avant)))
        a, b, _ = st.columns([2, 1, 2])
        if a.button(t("Enregistrer les opérations"), type="primary", icon=":material/save:",
                    disabled=bool(bloquantes) or retenues.empty, key="enregistrer_ops", width="stretch"):
            contenu = mouvements.en_csv(fusion)
            if cible["type"] == "perso" and session_compte is not None:
                session_compte.enregistrer(cible["nom"], contenu, identifiant=cible["id"], garder_precedente=True)
                st.session_state["message_compte"] = t("{n} opération(s) ajoutée(s) à « {nom} ». Vous pouvez "
                                                       "annuler cet ajout depuis « Mon compte ».",
                                                       n=len(retenues), nom=cible["nom"])
            else:
                st.session_state["fusion_session"] = {"origine": cible["origine"], "contenu": contenu,
                                                      "nom": cible["nom"]}
                st.session_state["message_compte"] = t("{n} opération(s) ajoutée(s) pour cette session. "
                                                       "Téléchargez le fichier mis à jour pour le garder.",
                                                       n=len(retenues))
            fermer()
            st.rerun()
        if b.button(t("Tout effacer"), key="effacer_ops", width="stretch"):
            st.session_state["ops_ajoutees"] = []
            st.rerun()
