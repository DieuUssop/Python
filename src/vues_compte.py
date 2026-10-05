"""
vues_compte.py — L'espace personnel dans le tableau de bord : connexion,
création de compte, « Mes portefeuilles » et page « Mon compte ».

La session ouverte (et donc la clé de chiffrement) est gardée dans
st.session_state : elle n'existe qu'en mémoire, pour ce visiteur, et
disparaît à la déconnexion, à la fermeture de la page ou après 30 minutes
sans activité.
"""

import hashlib
import time
from pathlib import Path

import streamlit as st

from . import comptes, import_fichier
from . import interface as ui
from .langues import t

INACTIVITE_MAX = 30 * 60          # secondes avant déconnexion automatique


def html(morceau):
    st.markdown(morceau, unsafe_allow_html=True)


def en_ligne():
    """Vrai sur Streamlit Community Cloud (le code y est installé dans /mount/src)."""
    return str(Path.cwd()).startswith("/mount/src")


def message(erreur):
    """Message d'une ErreurCompte, traduit."""
    if isinstance(erreur, comptes.ErreurCompte):
        return t(erreur.message, **erreur.valeurs)
    return str(erreur)


def session():
    """La session ouverte (ou None)."""
    return st.session_state.get("session_compte")


def deconnecter(raison=None):
    st.session_state.pop("session_compte", None)
    st.session_state.pop("page_compte", None)
    if raison:
        st.session_state["message_compte"] = raison


# ----------------------------------------------------------------------
# Barre latérale
# ----------------------------------------------------------------------
def barre_laterale():
    """Bloc « Mon espace » de la barre latérale. Renvoie la session ouverte (ou None)."""
    s = session()
    if s is not None and time.time() - s.derniere_activite > INACTIVITE_MAX:
        deconnecter(t("Déconnexion automatique après 30 minutes d'inactivité."))
        s = None
    if s is not None:
        s.derniere_activite = time.time()

    html(ui.bloc_titre(t("Mon espace")))
    if st.session_state.get("message_compte"):
        st.info(st.session_state.pop("message_compte"))
    if s is not None:
        st.caption(t("Connecté : {identifiant}", identifiant=s.identifiant))
        a, b = st.columns(2)
        if a.button(t("Mon compte"), icon=":material/person:", width="stretch", key="bouton_compte"):
            st.session_state["page_compte"] = not st.session_state.get("page_compte", False)
            st.rerun()
        if b.button(t("Déconnexion"), icon=":material/logout:", width="stretch", key="bouton_deconnexion"):
            deconnecter()
            st.rerun()
        return s

    with st.expander(t("Se connecter ou créer un compte")):
        if en_ligne():
            html(ui.note(t("Version en ligne de démonstration : les comptes et portefeuilles enregistrés ici "
                           "peuvent être effacés au redémarrage du site. Pour les conserver, utilisez "
                           "l'application sur votre ordinateur."), attention=True))
        action = st.radio(t("Action"), ["connexion", "creation"], horizontal=True, label_visibility="collapsed",
                          format_func=lambda a: t("Se connecter") if a == "connexion" else t("Créer un compte"),
                          key="action_compte")
        with st.form("formulaire_compte", border=False):
            identifiant = st.text_input(t("Identifiant"), key="champ_identifiant")
            mot_de_passe = st.text_input(t("Mot de passe"), type="password", key="champ_mdp")
            confirmation = st.text_input(t("Confirmer le mot de passe"), type="password", key="champ_mdp2") \
                if action == "creation" else None
            if action == "creation":
                st.caption(t("Vos portefeuilles seront chiffrés avec votre mot de passe. S'il est oublié, ils "
                             "seront définitivement illisibles, y compris pour l'administrateur."))
            valider = st.form_submit_button(t("Se connecter") if action == "connexion" else t("Créer mon compte"),
                                            type="primary", width="stretch")
        if valider:
            try:
                with st.spinner(t("Vérification...")):
                    if action == "connexion":
                        st.session_state["session_compte"] = comptes.connecter(identifiant, mot_de_passe)
                    else:
                        st.session_state["session_compte"] = comptes.creer_compte(identifiant, mot_de_passe,
                                                                                  confirmation)
                st.rerun()
            except comptes.ErreurCompte as erreur:
                st.error(message(erreur))
    return None


def bouton_enregistrer(s, contenu, nom_propose):
    """Juste sous l'envoi de fichier : enregistrer le portefeuille lu dans l'espace personnel
    (le fichier est enregistré au format du projet, après lecture et conversion)."""
    if s is None:
        return
    empreinte = hashlib.md5(contenu).hexdigest()
    deja = st.session_state.setdefault("deja_enregistres", {})
    with st.container(border=True):
        if empreinte in deja:
            st.success(t("« {nom} » est enregistré dans votre espace (chiffré).", nom=deja[empreinte]),
                       icon=":material/lock:")
            return
        st.markdown(f"**{t('Enregistrer dans mon espace')}**")
        nom = st.text_input(t("Nom du portefeuille"), value=nom_propose, key="nom_a_enregistrer")
        if st.button(t("Enregistrer"), type="primary", icon=":material/lock:", width="stretch",
                     key="bouton_enregistrer"):
            s.enregistrer(nom, contenu)
            deja[empreinte] = nom.strip() or nom_propose
            st.rerun()


# ----------------------------------------------------------------------
# Page « Mon compte »
# ----------------------------------------------------------------------
def page_compte(s, importer=None):
    html(ui.titre_section(t("Mon compte"), t("Connecté : {identifiant}", identifiant=s.identifiant)))
    html(ui.note(t("Vos portefeuilles sont chiffrés avec une clé tirée de votre mot de passe : personne d'autre "
                   "(ni les autres utilisateurs, ni l'administrateur) ne peut les lire.")))

    # 0. Ajouter un portefeuille (CSV ou Excel, lu automatiquement)
    with st.container(border=True):
        html(ui.titre_section(t("Ajouter un portefeuille"), t("Fichier CSV, Excel ou PDF, de n'importe quel format")))
        fichier = st.file_uploader(t("Fichier à enregistrer"), type=["csv", "xlsx", "pdf"], key="ajout_compte",
                                   label_visibility="collapsed")
        if fichier is not None and importer is not None:
            brut = fichier.getvalue()
            empreinte = hashlib.md5(brut).hexdigest()
            deja = st.session_state.setdefault("deja_ajoutes", {})
            if empreinte in deja:
                st.success(t("« {nom} » est enregistré dans votre espace (chiffré).", nom=deja[empreinte]),
                           icon=":material/lock:")
            else:
                with st.spinner(t("Lecture du fichier et vérification des prix avec les cours du marché...")):
                    auto = importer(brut)
                if auto["sur"]:
                    nom = st.text_input(t("Nom du portefeuille"), value=Path(fichier.name).stem, key="nom_ajout")
                    st.caption(t("{n} opération(s) reconnue(s).", n=len(auto["transactions"])))
                    if st.button(t("Enregistrer"), type="primary", icon=":material/lock:", key="bouton_ajout"):
                        s.enregistrer(nom, import_fichier.en_csv(auto["transactions"]))
                        deja[empreinte] = nom.strip() or Path(fichier.name).stem
                        st.rerun()
                else:
                    st.warning(t("Ce fichier n'a pas pu être lu automatiquement. Envoyez-le depuis la barre "
                                 "latérale (« Ou envoyer un autre fichier ») : l'assistant d'import vous guidera, "
                                 "puis le bouton « Enregistrer dans mon espace » apparaîtra sous l'envoi."))

    # 1. Mes portefeuilles
    with st.container(border=True):
        html(ui.titre_section(t("Mes portefeuilles")))
        portefeuilles = s.lister()
        if not portefeuilles:
            st.caption(t("Aucun portefeuille enregistré pour l'instant : ajoutez-en un ci-dessus."))
        for p in portefeuilles:
            a, b, c, d = st.columns([4, 2, 2, 2], vertical_alignment="center")
            nouveau_nom = a.text_input(t("Nom"), value=p["nom"], key=f"nom_{p['id']}", label_visibility="collapsed")
            a.caption(t("{n} opération(s) · modifié le {date}", n=p["operations"], date=p["maj"]))
            if nouveau_nom.strip() and nouveau_nom != p["nom"]:
                s.renommer(p["id"], nouveau_nom)
                st.rerun()
            b.download_button(t("Télécharger"), data=s.lire(p["id"]), file_name=f"{p['nom']}.csv",
                              mime="text/csv", icon=":material/download:", key=f"dl_{p['id']}", width="stretch")
            confirmer = c.checkbox(t("Confirmer"), key=f"conf_{p['id']}")
            if d.button(t("Supprimer"), icon=":material/delete:", disabled=not confirmer, key=f"sup_{p['id']}",
                        width="stretch"):
                s.supprimer(p["id"])
                st.rerun()
            e, f, _ = st.columns([3, 3, 4])
            if e.button(t("Ajouter des opérations"), icon=":material/playlist_add:", key=f"ajout_{p['id']}",
                        width="stretch"):
                from . import vues_mouvements
                vues_mouvements.ouvrir({"type": "perso", "id": p["id"], "nom": p["nom"], "contenu": s.lire(p["id"])})
                st.rerun()
            if p.get("precedente") and f.button(t("Annuler le dernier ajout"), icon=":material/undo:",
                                                key=f"annuler_{p['id']}", width="stretch",
                                                help=t("Revenir à la version du {date}",
                                                       date=p["precedente"].get("maj", ""))):
                s.annuler_dernier_ajout(p["id"])
                st.rerun()
            st.divider()

    # 2. Mot de passe
    with st.container(border=True):
        html(ui.titre_section(t("Changer de mot de passe"), t("Vos portefeuilles sont rechiffrés avec le nouveau")))
        with st.form("formulaire_mdp", border=False):
            ancien = st.text_input(t("Mot de passe actuel"), type="password")
            nouveau = st.text_input(t("Nouveau mot de passe"), type="password")
            confirmation = st.text_input(t("Confirmer le mot de passe"), type="password")
            if st.form_submit_button(t("Changer de mot de passe")):
                try:
                    with st.spinner(t("Vérification...")):
                        s.changer_mot_de_passe(ancien, nouveau, confirmation)
                    st.success(t("Mot de passe modifié."))
                except comptes.ErreurCompte as erreur:
                    st.error(message(erreur))

    # 3. Suppression du compte
    with st.container(border=True):
        html(ui.titre_section(t("Supprimer mon compte"),
                              t("Efface définitivement le compte et tous ses portefeuilles (droit à l'effacement, RGPD)")))
        with st.form("formulaire_suppression", border=False):
            mdp = st.text_input(t("Mot de passe"), type="password")
            if st.form_submit_button(t("Supprimer définitivement mon compte"), type="primary"):
                try:
                    s.supprimer_compte(mdp)
                    deconnecter(t("Compte et données supprimés."))
                    st.rerun()
                except comptes.ErreurCompte as erreur:
                    st.error(message(erreur))
