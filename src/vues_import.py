"""
vues_import.py — Assistant d'import : pour analyser un fichier qui n'est pas
au format du projet (export de banque ou de courtier, tableau Excel personnel).

Il s'affiche à la place du tableau de bord quand un fichier envoyé n'est pas
reconnu automatiquement (ou contient des codes ISIN), ou quand l'utilisateur
clique sur « Ouvrir l'assistant d'import ». En 4 étapes :

    1. le fichier : feuille Excel, ligne des titres de colonnes, aperçu ;
    2. la correspondance des colonnes (date, quantité, prix...) ;
    3. l'interprétation des types d'opération et des codes des titres
       (ISIN ou noms -> tickers Yahoo Finance, modifiables à la main) ;
    4. l'aperçu du résultat, puis « Analyser ce portefeuille ».

La logique est dans src/import_fichier.py ; ce fichier ne fait que l'affichage.
"""

import pandas as pd
import streamlit as st

from . import import_fichier as imp
from . import interface as ui
from .analyse import charger_referentiel
from .langues import t, td

AUCUNE = "__aucune__"


def html(morceau):
    st.markdown(morceau, unsafe_allow_html=True)


@st.cache_data(show_spinner=False, ttl=3600)
def _marche(tickers, debut):
    """Devises et cours historiques des titres (pour vérifier les prix du fichier)."""
    repere = pd.DataFrame({"ticker": list(tickers), "date": pd.Timestamp(debut)})
    return imp.donnees_de_marche(repere)


def texte_devises(rapport):
    """Phrases décrivant les conversions de devises et les prix douteux."""
    lectures = {"euros": t("montants en euros convertis"), "devise": t("prix en {devise} convertis dans l'unité de cotation")}
    messages = []
    if not rapport.get("verifie"):
        messages.append(t("Prix non vérifiés avec les cours du marché (pas de connexion)."))
    for c in rapport.get("conversions", []):
        messages.append(f"{c['ticker']} : " + lectures[c["lecture"]].format(devise=c["devise"]))
    for a in rapport.get("alertes", []):
        messages.append(t("{ticker} : {n} prix éloigné(s) du cours du jour (écart médian {ecart}) — ticker, "
                          "devise ou division d'actions à vérifier.", ticker=a["ticker"], n=a["lignes"],
                          ecart=f"{a['ecart']:+.0%}"))
    return messages


def texte_resume(resume):
    """Résumé de l'import automatique, affiché dans la barre latérale."""
    parties = [t("Fichier reconnu automatiquement : {n} opération(s), {titres} titre(s).",
                 n=resume.get("operations", 0), titres=resume.get("titres", 0))]
    if resume.get("sans_entete"):
        parties.append(t("Colonnes identifiées d'après leur contenu (pas de ligne de titres)."))
    if resume.get("titres_convertis"):
        parties.append(t("{n} code(s) ISIN ou nom(s) convertis en tickers.", n=resume["titres_convertis"]))
    if resume.get("dates_ambigues"):
        parties.append(t("Dates lues au format jour/mois (JJ/MM)."))
    elif resume.get("ordre_dates") == "mois":
        parties.append(t("Dates lues au format américain (MM/JJ)."))
    if resume.get("ignorees"):
        parties.append(t("{n} ligne(s) ignorée(s) (frais de garde, virements...).", n=resume["ignorees"]))
    parties += texte_devises(resume.get("devises", {}))
    return " ".join(parties)


@st.cache_data(show_spinner=False, ttl=24 * 3600)
def _resoudre(valeurs, noms, tickers_connus):
    """Recherche des tickers (mise en cache : une seule recherche par fichier)."""
    return imp.resoudre_identifiants(list(valeurs), dict(noms), set(tickers_connus))


def _libelle_type(code):
    return t("Ignorer la ligne") if code == imp.IGNORER else td(code)


def afficher(brut, nom_fichier, cle, erreur_directe=None):
    """Affiche l'assistant. Quand l'utilisateur valide, le fichier converti est
    rangé dans st.session_state["imports"][cle] et la page est relancée."""
    html(ui.titre_section(t("Assistant d'import"), t("Fichier : {nom}", nom=nom_fichier)))
    html(ui.note(t("Ce fichier n'est pas au format du projet, ou il contient des codes ISIN. Indiquez ci-dessous "
                   "comment le lire : l'outil propose une correspondance, il suffit de la vérifier.")))
    if erreur_directe:
        with st.expander(t("Pourquoi l'assistant s'ouvre-t-il ?")):
            st.write(erreur_directe)

    # ------------------------------------------------------------------
    # 1. Le fichier
    # ------------------------------------------------------------------
    with st.container(border=True):
        html(ui.titre_section(t("1. Le fichier"), t("Choisir la feuille et la ligne qui contient les titres de colonnes")))
        a, b = st.columns(2)
        try:
            feuilles = imp.feuilles_excel(brut)
        except Exception as erreur:
            st.error(t("Fichier illisible : {erreur}", erreur=erreur))
            return
        feuille = a.selectbox(t("Feuille Excel"), feuilles, index=feuilles.index(imp.meilleure_feuille(brut)),
                              key=f"imp_feuille_{cle}") if len(feuilles) > 1 \
            else (feuilles[0] if feuilles else None)
        try:
            _, ligne_auto = imp.lire_tableau_brut(brut, feuille)
            ligne = b.number_input(t("Ligne des titres de colonnes"), min_value=0, max_value=500,
                                   value=ligne_auto + 1, step=1, key=f"imp_ligne_{cle}_{feuille}",
                                   help=t("Numéro de la ligne du fichier où se trouvent les noms des colonnes "
                                          "(détecté automatiquement). 0 = le fichier n'a pas de ligne de titres.")) - 1
            tableau, _ = imp.lire_tableau_brut(brut, feuille, ligne)
        except ValueError as erreur:
            st.error(str(erreur))
            return
        st.caption(t("Aperçu des premières lignes ({n} lignes au total)", n=len(tableau)))
        st.dataframe(tableau.head(8), hide_index=True, width="stretch")

    # ------------------------------------------------------------------
    # 2. Correspondance des colonnes
    # ------------------------------------------------------------------
    with st.container(border=True):
        html(ui.titre_section(t("2. Correspondance des colonnes"),
                              t("Pour chaque information, la colonne de votre fichier qui la contient (* = obligatoire)")))
        proposition = imp.proposer_correspondance(tableau)          # d'après les noms ET le contenu
        options = [AUCUNE] + list(tableau.columns)
        correspondance = {}
        colonnes = st.columns(4)
        for i, (champ, libelle) in enumerate(imp.CHAMPS.items()):
            obligatoire = champ in imp.OBLIGATOIRES
            defaut = proposition.get(champ)
            choix = colonnes[i % 4].selectbox(
                t(libelle) + (" *" if obligatoire else ""), options,
                index=options.index(defaut) if defaut in options else 0,
                format_func=lambda o: t("— aucune —") if o == AUCUNE else str(o),
                key=f"imp_col_{champ}_{cle}_{feuille}_{ligne}",
            )
            correspondance[champ] = None if choix == AUCUNE else choix
        montant_inclut_frais = True
        if correspondance.get("montant"):
            montant_inclut_frais = st.checkbox(
                t("Le montant total inclut les frais (montant net débité ou crédité)"), value=True,
                key=f"imp_net_{cle}",
                help=t("Sert à retrouver le prix unitaire quand il n'est pas donné : "
                       "achat = quantité × prix + frais ; vente = quantité × prix − frais."))
        manquants = imp.correspondance_complete(correspondance)
        if manquants:
            st.warning(t("À indiquer : {champs}. Pour le prix, une colonne « Prix unitaire » ou « Montant total » suffit.",
                         champs=", ".join(t(imp.CHAMPS[m]) for m in manquants)))
            return
        if not correspondance.get("type"):
            html(ui.note(t("Sans colonne « Type d'opération » : une quantité négative est lue comme une vente, "
                           "une quantité positive comme un achat.")))

    # ------------------------------------------------------------------
    # 3. Types d'opération et titres
    # ------------------------------------------------------------------
    types = None
    with st.container(border=True):
        html(ui.titre_section(t("3. Types d'opération et titres"),
                              t("Vérifier l'interprétation proposée ; les cellules modifiables sont en blanc")))
        gauche, droite = st.columns([2, 3], gap="medium")
        if correspondance.get("type"):
            with gauche:
                valeurs = tableau[correspondance["type"]].astype(str).str.strip()
                comptes = valeurs.value_counts()
                libelles = {code: _libelle_type(code) for code in imp.TYPES_POSSIBLES}
                edition = st.data_editor(
                    pd.DataFrame({"valeur": comptes.index, "lignes": comptes.values,
                                  "type": [libelles[imp.classer_type(v)] for v in comptes.index]}),
                    hide_index=True, width="stretch", disabled=["valeur", "lignes"],
                    key=f"imp_types_{cle}_{correspondance['type']}",
                    column_config={
                        "valeur": st.column_config.TextColumn(t("Dans le fichier")),
                        "lignes": st.column_config.NumberColumn(t("Lignes")),
                        "type": st.column_config.SelectboxColumn(t("Interprétation"), options=list(libelles.values()),
                                                                 required=True),
                    },
                )
                inverse = {v: k for k, v in libelles.items()}
                types = {str(v): inverse.get(l, imp.IGNORER) for v, l in zip(edition["valeur"], edition["type"])}

        with droite:
            colonne_id = correspondance["identifiant"]
            identifiants = [v for v in tableau[colonne_id].astype(str).str.strip().unique() if v and v != "nan"]
            noms = {}
            if correspondance.get("nom"):
                for v, n in zip(tableau[colonne_id].astype(str).str.strip(), tableau[correspondance["nom"]].astype(str)):
                    if v and n.strip() and n != "nan":
                        noms.setdefault(v, n.strip())
            tickers_connus = tuple(charger_referentiel().index)
            with st.spinner(t("Recherche des tickers Yahoo Finance...")):
                resolution = _resoudre(tuple(identifiants), tuple(sorted(noms.items())), tickers_connus)
            statuts = {"tel quel": t("tel quel"), "trouvé": t("trouvé"), "introuvable": t("introuvable")}
            edition = st.data_editor(
                resolution.assign(statut=resolution["statut"].map(statuts))[["identifiant", "ticker", "nom", "statut"]],
                hide_index=True, width="stretch", disabled=["identifiant", "nom", "statut"],
                key=f"imp_tickers_{cle}_{colonne_id}",
                column_config={
                    "identifiant": st.column_config.TextColumn(t("Dans le fichier")),
                    "ticker": st.column_config.TextColumn(t("Ticker Yahoo Finance"),
                                                          help=t("Modifiable : par exemple MC.PA pour LVMH à Paris")),
                    "nom": st.column_config.TextColumn(t("Nom trouvé")),
                    "statut": st.column_config.TextColumn(t("Statut")),
                },
            )
            correspondances_titres = {str(i): str(tk).strip().upper() if pd.notna(tk) else ""
                                      for i, tk in zip(edition["identifiant"], edition["ticker"])}
            if (resolution["statut"] == "introuvable").any():
                st.caption(t("Titres introuvables : saisir leur ticker à la main (recherche sur finance.yahoo.com), "
                             "sinon leurs lignes seront ignorées."))

    # ------------------------------------------------------------------
    # 4. Résultat
    # ------------------------------------------------------------------
    with st.container(border=True):
        html(ui.titre_section(t("4. Résultat"), t("Transactions au format du projet")))
        try:
            transactions, rapport = imp.appliquer_correspondance(tableau, correspondance, types,
                                                                 correspondances_titres, montant_inclut_frais)
        except ValueError as erreur:
            st.error(str(erreur))
            return
        # Les noms trouvés par la recherche remplacent les codes quand le fichier n'a pas de colonne de nom
        if not correspondance.get("nom"):
            noms_trouves = {str(tk).strip().upper(): n for tk, n in zip(edition["ticker"], edition["nom"])
                            if pd.notna(tk) and isinstance(n, str) and n}
            transactions["nom"] = [noms_trouves.get(tk, nom) for tk, nom in zip(transactions["ticker"],
                                                                                  transactions["nom"])]
        # Devises : prix vérifiés avec les vrais cours, reconvertis si le fichier donne des euros
        mode = st.radio(t("Devise des prix du fichier"), ["auto", "cotation", "euros"], horizontal=True,
                        format_func=lambda m: {"auto": t("Détection automatique (recommandé)"),
                                               "cotation": t("Devise de cotation de chaque titre"),
                                               "euros": t("Tout est en euros")}[m],
                        key=f"imp_devise_{cle}",
                        help=t("La détection compare chaque prix au vrai cours de clôture du jour, en dollars, "
                               "livres, euros... et garde la lecture la plus proche."))
        try:
            with st.spinner(t("Vérification des prix avec les cours du marché...")):
                info, historique = _marche(tuple(sorted(transactions["ticker"].unique())),
                                           str(transactions["date"].min().date()))
        except Exception:
            info, historique = {}, None
        transactions, rapport_devises = imp.harmoniser_devises(transactions, info, historique, mode)
        messages = texte_devises(rapport_devises)
        messages += [t("{n} ligne(s) avec {motif} (lignes {lignes}) : ignorée(s)", n=e["n"], motif=t(e["motif"]),
                      lignes=e["lignes"]) for e in rapport["erreurs"]]
        if rapport["ignorees"]:
            messages.insert(0, t("{n} ligne(s) ignorée(s) : opérations d'un autre type (frais de garde, virements...)",
                                 n=rapport["ignorees"]))
        for message in messages:
            html(ui.note(message))
        st.caption(t("{n} transaction(s) · {titres} titre(s)", n=len(transactions),
                     titres=transactions["ticker"].nunique()))
        st.dataframe(transactions.assign(type=transactions["type"].map(td)), hide_index=True, width="stretch",
                     height=260)

        a, b = st.columns(2)
        if a.button(t("Analyser ce portefeuille"), type="primary", icon=":material/check:", width="stretch",
                    disabled=transactions.empty, key=f"imp_ok_{cle}"):
            st.session_state.setdefault("imports", {})[cle] = imp.en_csv(transactions)
            st.session_state.pop("assistant_force", None)
            st.rerun()
        b.download_button(t("Télécharger le fichier converti (format du projet)"), data=imp.en_csv(transactions),
                          file_name="transactions_converties.csv", mime="text/csv", icon=":material/download:",
                          width="stretch", disabled=transactions.empty, key=f"imp_dl_{cle}")
