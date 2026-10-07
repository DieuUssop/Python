"""
Tests de la mise à jour d'un portefeuille par ajout de nouvelles opérations :
doublons reconnus, vente à découvert refusée, tri, ajout idempotent, et
annulation du dernier ajout dans l'espace chiffré.
"""

import pandas as pd
import pytest

from src import comptes, mouvements as mv

EXISTANT = (b"date,type,ticker,nom,quantite,prix,frais\n"
            b"2024-01-16,ACHAT,MC.PA,LVMH,3,740,2\n"
            b"2024-03-01,ACHAT,AI.PA,Air Liquide,5,170,2\n")


def _nouvelles(lignes):
    return pd.DataFrame(lignes, columns=mv.COLONNES)


def test_doublons_et_fusion_triee():
    nouvelles = _nouvelles([["2024-03-01", "ACHAT", "AI.PA", "Air Liquide", 5, 170.4, 2],   # déjà là (0,2 %)
                            ["2024-02-10", "ACHAT", "AAPL", "Apple", 4, 185, 1]])
    fusion, doublons, alertes = mv.fusionner_operations(EXISTANT, nouvelles)
    assert len(doublons) == 1 and doublons.iloc[0]["ticker"] == "AI.PA"
    assert list(fusion["ticker"]) == ["MC.PA", "AAPL", "AI.PA"]                 # trié par date
    assert alertes == []


def test_ajout_idempotent():
    nouvelles = _nouvelles([["2024-05-02", "VENTE", "MC.PA", "LVMH", 1, 800, 2]])
    fusion1, _, _ = mv.fusionner_operations(EXISTANT, nouvelles)
    fusion2, doublons, _ = mv.fusionner_operations(mv.en_csv(fusion1), nouvelles)
    assert len(fusion2) == len(fusion1) == 3 and len(doublons) == 1


def test_vente_a_decouvert_et_date_future_bloquantes():
    nouvelles = _nouvelles([["2024-05-02", "VENTE", "MC.PA", "LVMH", 10, 800, 2],
                            [(pd.Timestamp.today() + pd.Timedelta(days=30)).strftime("%Y-%m-%d"), "ACHAT", "AAPL",
                             "Apple", 1, 190, 1]])
    _, alertes = mv.preparer(EXISTANT, nouvelles)
    messages = " ".join(a["message"] for a in alertes)
    assert all(a["bloquant"] for a in alertes) and len(alertes) == 2
    assert "seulement" in messages and "futur" in messages


def test_annuler_le_dernier_ajout():
    s = comptes.creer_compte("kevin", "motdepasse1")
    pid = s.enregistrer("PEA", EXISTANT)
    fusion, _, _ = mv.fusionner_operations(EXISTANT, _nouvelles([["2024-06-03", "ACHAT", "AAPL", "Apple", 2, 190, 1]]))
    s.enregistrer("PEA", mv.en_csv(fusion), identifiant=pid, garder_precedente=True)
    assert s.lister()[0]["operations"] == 3 and "precedente" in s.lister()[0]
    s.changer_mot_de_passe("motdepasse1", "nouveaumdp2", "nouveaumdp2")        # la version précédente suit
    s.annuler_dernier_ajout(pid)
    assert s.lire(pid) == EXISTANT and "precedente" not in s.lister()[0]
    with pytest.raises(comptes.ErreurCompte):
        s.annuler_dernier_ajout(pid)


# ----------------------------------------------------------------------
# Supprimer ou corriger des opérations existantes (onglet Transactions)
# ----------------------------------------------------------------------
AVEC_VENTE = (b"date,type,ticker,nom,quantite,prix,frais\n"
              b"2024-01-16,ACHAT,MC.PA,LVMH,3,740,2\n"
              b"2024-03-01,ACHAT,AI.PA,Air Liquide,5,170,2\n"
              b"2024-06-03,VENTE,MC.PA,LVMH,2,780,2\n")


def _edition(source, **changements):
    """Tableau édité : toutes les lignes, avec les changements {ligne: {champ: valeur}}."""
    tableau = mv.lire(source).assign(supprimer=False)
    for ligne, valeurs in changements.items():
        for champ, valeur in valeurs.items():
            tableau.at[int(ligne[1:]), champ] = valeur
    return tableau


def test_suppression_et_correction():
    edite = _edition(AVEC_VENTE, l1={"supprimer": True}, l0={"quantite": 4, "prix": 735.5})
    nouveau, supprimees, corrections = mv.appliquer_modifications(AVEC_VENTE, edite)
    assert list(supprimees["ticker"]) == ["AI.PA"] and len(nouveau) == 2
    assert {(c["champ"], c["apres"]) for c in corrections} == {("quantite", 4.0), ("prix", 735.5)}
    assert nouveau.iloc[0]["quantite"] == 4 and mv.controler(nouveau) == []
    assert mv.titres_disparus(AVEC_VENTE, nouveau) == ["AI.PA"]


def test_suppression_d_un_achat_dont_depend_une_vente_est_bloquee():
    edite = _edition(AVEC_VENTE, l0={"supprimer": True})
    nouveau, _, _ = mv.appliquer_modifications(AVEC_VENTE, edite)
    alertes = mv.controler(nouveau)
    assert alertes and alertes[0]["bloquant"] and alertes[0]["ticker"] == "MC.PA"
    # en supprimant aussi la vente, tout redevient cohérent
    nouveau, _, _ = mv.appliquer_modifications(AVEC_VENTE, _edition(AVEC_VENTE, l0={"supprimer": True},
                                                                       l2={"supprimer": True}))
    assert mv.controler(nouveau) == [] and list(nouveau["ticker"]) == ["AI.PA"]


def test_correction_de_date_retrie_et_ignore_les_lignes_filtrees():
    edite = _edition(AVEC_VENTE, l1={"date": pd.Timestamp("2023-12-01")}).loc[[1]]   # une seule ligne affichée
    nouveau, supprimees, corrections = mv.appliquer_modifications(AVEC_VENTE, edite)
    assert supprimees.empty and len(corrections) == 1 and len(nouveau) == 3
    assert list(nouveau["ticker"]) == ["AI.PA", "MC.PA", "MC.PA"]                 # retrié par date


def test_annuler_la_derniere_modification():
    s = comptes.creer_compte("kevin2", "motdepasse123")
    ident = s.enregistrer("PEA", AVEC_VENTE)
    nouveau, _, _ = mv.appliquer_modifications(AVEC_VENTE, _edition(AVEC_VENTE, l1={"supprimer": True}))
    s.enregistrer("PEA", mv.en_csv(nouveau), identifiant=ident, garder_precedente=True)
    assert b"AI.PA" not in s.lire(ident)
    s.annuler_derniere_modification(ident)
    assert s.lire(ident) == AVEC_VENTE
