"""
vues_transactions.py — Onglet « Transactions » : historique des opérations, et
modification (suppression ou correction) de n'importe quelle opération.

Ce qui est modifié, c'est le FICHIER du portefeuille lui-même (format du projet :
date, type, ticker, nom, quantité, prix dans la devise de cotation, frais),
pas le tableau converti en euros affiché par ailleurs.

Selon l'origine du portefeuille :
    - espace personnel : réenregistré chiffré ; la version précédente est gardée
      (bouton « Annuler la dernière modification ») ;
    - fichier envoyé sans compte ou portefeuille d'exemple : modification valable
      pour la session, fichier corrigé proposé au téléchargement.

Appelé par app.py : vues_transactions.afficher(res, contenu, cible, session_compte).
"""

import pandas as pd
import streamlit as st

from . import langues, mouvements
from . import interface as ui
from .devises import devise_par_suffixe
from .langues import t, td


def html(morceau):
    st.markdown(morceau, unsafe_allow_html=True)


def afficher(res, contenu, cible, session_compte):
    """cible : {"type": "perso", "id", "nom"} ou {"type": "session", "origine", "nom"}."""
    transactions = res["transactions"]
    if st.session_state.get("message_transactions"):
        st.success(st.session_state.pop("message_transactions"))
    with st.container(border=True):
        tete, bouton = st.columns([4, 1], vertical_alignment="bottom")
        with tete:
            html(ui.titre_section(t("Historique des opérations")))
        edition = st.session_state.get("edition_operations", False)
        if bouton.button(t("Terminer") if edition else t("Modifier les opérations"),
                         type="secondary", width="stretch", key="bouton_edition_operations",
                         help=t("Supprimer ou corriger n'importe quelle opération du portefeuille")):
            st.session_state["edition_operations"] = not edition
            st.rerun()

        gauche, droite = st.columns(2)
        choix_types = gauche.multiselect(t("Type"), ["ACHAT", "VENTE", "DIVIDENDE"],
                                         default=["ACHAT", "VENTE", "DIVIDENDE"], format_func=td)
        choix_titres = droite.multiselect(t("Titres"), sorted(transactions["nom"].unique()),
                                          placeholder=t("Tous les titres"))
        if edition:
            _edition(contenu, cible, session_compte, transactions, choix_types, choix_titres)
        else:
            _consultation(transactions, choix_types, choix_titres)
            _bouton_annuler(cible, session_compte)


# ----------------------------------------------------------------------
# Consultation (tableau converti en euros)
# ----------------------------------------------------------------------
def _consultation(transactions, choix_types, choix_titres):
    filtre = transactions["type"].isin(choix_types)
    if choix_titres:
        filtre &= transactions["nom"].isin(choix_titres)
    selection = transactions[filtre].sort_values("date", ascending=False)
    st.caption(t("{n} opération(s) affichée(s) sur {total}", n=len(selection), total=len(transactions)))
    st.dataframe(
        selection.assign(type=selection["type"].map(td)), hide_index=True, width="stretch",
        column_config={
            "date": st.column_config.DateColumn("Date", format="DD MMM YYYY" if langues.anglais() else "DD/MM/YYYY"),
            "type": st.column_config.TextColumn(t("Type")),
            "ticker": st.column_config.TextColumn("Ticker"),
            "nom": st.column_config.TextColumn(t("Titre")),
            "quantite": st.column_config.NumberColumn(t("Quantité"), format="%d"),
            "prix": st.column_config.NumberColumn(t("Prix / montant (€)"), format=langues.eur_colonne("%.2f")),
            "frais": st.column_config.NumberColumn(t("Frais"), format=langues.eur_colonne("%.2f")),
            "devise": st.column_config.TextColumn(t("Devise")),
            "prix_devise": st.column_config.NumberColumn(t("Prix en devise"), format="%.2f",
                                                         help=t("Prix saisi, avant conversion en euros")),
        },
    )
    # Le fichier téléchargé garde le format d'origine (types ACHAT / VENTE / DIVIDENDE)
    st.download_button(
        t("Télécharger la sélection (CSV)"), data=selection.to_csv(index=False).encode("utf-8"),
        file_name="transactions_selection.csv", mime="text/csv",
    )


# ----------------------------------------------------------------------
# Modification : supprimer ou corriger
# ----------------------------------------------------------------------
def _edition(contenu, cible, session_compte, transactions, choix_types, choix_titres):
    source = mouvements.lire(contenu)
    noms = dict(zip(transactions["ticker"], transactions["nom"]))         # noms complets (référentiel)
    source["nom"] = [n if str(n).strip() else noms.get(tk, tk) for n, tk in zip(source["nom"], source["ticker"])]
    filtre = source["type"].isin(choix_types)
    if choix_titres:
        filtre &= source["nom"].isin(choix_titres) | source["ticker"].map(noms).isin(choix_titres)
    vue = source[filtre].sort_values("date", ascending=False)

    if cible["type"] == "perso":
        html(ui.note(t("Les modifications seront enregistrées dans votre espace (chiffré). La version actuelle est "
                       "conservée : vous pourrez revenir en arrière.")))
    else:
        html(ui.note(t("Portefeuille hors de votre espace : les modifications valent pour cette session. Le fichier "
                       "corrigé pourra être téléchargé.")))
    st.caption(t("Cochez « Supprimer » ou modifiez directement la date, la quantité, le prix ou les frais. "
                 "Le prix est celui de la devise de cotation du titre."))

    tableau = vue.assign(supprimer=False, devise=[devise_par_suffixe(tk) for tk in vue["ticker"]],
                         type_affiche=vue["type"].map(td))
    tableau = tableau[["supprimer", "date", "type_affiche", "ticker", "nom", "quantite", "prix", "devise", "frais"]]
    edite = st.data_editor(
        tableau, key=f"editeur_operations_{cible.get('id') or cible.get('origine')}", hide_index=True,
        width="stretch", num_rows="fixed",
        disabled=["type_affiche", "ticker", "nom", "devise"],
        column_config={
            "supprimer": st.column_config.CheckboxColumn(t("Supprimer"), default=False, width="small"),
            "date": st.column_config.DateColumn("Date", format="DD MMM YYYY" if langues.anglais() else "DD/MM/YYYY"),
            "type_affiche": st.column_config.TextColumn(t("Type")),
            "ticker": st.column_config.TextColumn("Ticker"),
            "nom": st.column_config.TextColumn(t("Titre")),
            "quantite": st.column_config.NumberColumn(t("Quantité"), min_value=0.0, format="%g"),
            "prix": st.column_config.NumberColumn(t("Prix (devise de cotation)"), min_value=0.0, format="%.4g"),
            "devise": st.column_config.TextColumn(t("Devise")),
            "frais": st.column_config.NumberColumn(t("Frais"), min_value=0.0, format="%.2f"),
        },
    )
    edite = pd.DataFrame(edite).set_axis(tableau.index)
    nouveau, supprimees, corrections = mouvements.appliquer_modifications(source, edite)
    nb_corrigees = len({c["ligne"] for c in corrections})
    if supprimees.empty and not corrections:
        st.caption(t("Aucune modification pour l'instant."))
        _bouton_annuler(cible, session_compte)
        return

    # Récapitulatif
    html(ui.titre_section(t("Récapitulatif"), t("{s} suppression(s) · {c} correction(s)", s=len(supprimees),
                                                    c=nb_corrigees)))
    lignes = []
    for _, l in supprimees.iterrows():
        lignes.append([t("Supprimée"), _decrire(l)])
    libelles = {"date": t("date"), "quantite": t("quantité"), "prix": t("prix"), "frais": t("frais")}
    for c in corrections:
        l = source.loc[c["ligne"]]
        lignes.append([t("Corrigée"), _decrire(l) + " · " + t("{champ} : {avant} → {apres}", champ=libelles[c["champ"]],
                                                             avant=_valeur(c["avant"]), apres=_valeur(c["apres"]))])
    from html import escape
    from .lecture import tableau_html
    html(tableau_html([t("Action"), t("Opération")], [[escape(a), escape(b)] for a, b in lignes], droite_a_partir_de=9))

    # Contrôles : vente à découvert, date future, quantité ou prix nul
    alertes = mouvements.controler(nouveau)
    bloquantes = [a for a in alertes if a["bloquant"]]
    for a in bloquantes:
        st.error(t(a["message"], **a["valeurs"]))
    if any("Vente de" in a["message"] for a in bloquantes):
        st.caption(t("Si vous supprimez un achat, supprimez aussi la ou les ventes qui en dépendent (même titre, "
                     "date postérieure)."))
    disparus = mouvements.titres_disparus(source, nouveau)
    if disparus and not bloquantes:
        st.warning(t("Après cette modification, ces titres ne sont plus détenus : {titres}.",
                     titres=", ".join(noms.get(tk, tk) for tk in disparus)))
    if nouveau.empty:
        st.error(t("Le portefeuille ne peut pas être vide : gardez au moins une opération."))
        bloquantes = bloquantes + [{"message": "vide"}]

    a, b, _ = st.columns([2, 1, 2])
    confirme = a.checkbox(t("Je confirme ces modifications"), key="confirmer_modifications", disabled=bool(bloquantes))
    if a.button(t("Enregistrer les modifications"), type="primary", disabled=bool(bloquantes) or not confirme,
                key="enregistrer_modifications", width="stretch"):
        _enregistrer(nouveau, contenu, cible, session_compte, len(supprimees), nb_corrigees)
    if b.button(t("Tout annuler"), key="abandonner_modifications", width="stretch"):
        st.session_state.pop(f"editeur_operations_{cible.get('id') or cible.get('origine')}", None)
        st.session_state["edition_operations"] = False
        st.rerun()


def _decrire(ligne):
    date = pd.Timestamp(ligne["date"]).strftime("%d/%m/%Y")
    return f"{date} · {td(ligne['type'])} · {ligne['quantite']:g} {ligne['nom'] or ligne['ticker']}"


def _valeur(v):
    if isinstance(v, pd.Timestamp):
        return v.strftime("%d/%m/%Y")
    texte = f"{float(v):g}"
    return texte if langues.anglais() else texte.replace(".", ",")


def _enregistrer(nouveau, contenu_actuel, cible, session_compte, nb_supprimees, nb_corrigees):
    contenu = mouvements.en_csv(nouveau)
    if cible["type"] == "perso" and session_compte is not None:
        session_compte.enregistrer(cible["nom"], contenu, identifiant=cible["id"], garder_precedente=True)
        message = t("Portefeuille « {nom} » modifié : {s} suppression(s), {c} correction(s). « Annuler la dernière "
                    "modification » permet de revenir en arrière.", nom=cible["nom"], s=nb_supprimees, c=nb_corrigees)
    else:
        st.session_state["fusion_session"] = {"origine": cible["origine"], "contenu": contenu, "nom": cible["nom"],
                                              "precedent": contenu_actuel}
        message = t("Modifications appliquées pour cette session : {s} suppression(s), {c} correction(s). "
                    "Téléchargez le fichier mis à jour pour le garder.", s=nb_supprimees, c=nb_corrigees)
    st.session_state["message_compte"] = message
    st.session_state["message_transactions"] = message
    st.session_state["edition_operations"] = False
    st.rerun()


def _bouton_annuler(cible, session_compte):
    """« Annuler la dernière modification » : version précédente du portefeuille."""
    if cible["type"] == "perso" and session_compte is not None:
        fiche = next((p for p in session_compte.lister() if p["id"] == cible["id"]), None)
        if fiche and fiche.get("precedente"):
            if st.button(t("Annuler la dernière modification"), key="annuler_modif_transactions",
                         help=t("Revenir à la version du {date}", date=fiche["precedente"].get("maj", ""))):
                session_compte.annuler_derniere_modification(cible["id"])
                st.session_state["edition_operations"] = False
                st.rerun()
    else:
        fusion = st.session_state.get("fusion_session")
        if fusion and fusion.get("origine") == cible.get("origine") and fusion.get("precedent") is not None:
            if st.button(t("Annuler la dernière modification"), key="annuler_modif_session"):
                import hashlib
                if hashlib.md5(fusion["precedent"]).hexdigest()[:12] == cible.get("origine"):
                    st.session_state.pop("fusion_session")           # retour au fichier d'origine
                else:
                    fusion["contenu"], fusion["precedent"] = fusion["precedent"], None
                st.session_state["edition_operations"] = False
                st.rerun()
