"""
Tests des comptes utilisateurs et du chiffrement : chacun ne voit que ses
données, rien n'est lisible sur le disque, un fichier modifié est rejeté.
"""

import pytest

from src import coffre, comptes

CSV = b"date,type,ticker,nom,quantite,prix,frais\n2024-01-16,ACHAT,MC.PA,LVMH,3,740,2\n"


def test_creation_et_connexion():
    comptes.creer_compte("kevin", "motdepasse1", "motdepasse1")
    session = comptes.connecter("Kevin ", "motdepasse1")          # majuscules et espaces tolérés
    assert session.identifiant == "kevin"
    with pytest.raises(comptes.ErreurCompte):
        comptes.connecter("kevin", "mauvais-mdp")
    with pytest.raises(comptes.ErreurCompte):
        comptes.connecter("inconnu", "motdepasse1")


def test_regles_de_creation():
    with pytest.raises(comptes.ErreurCompte):
        comptes.creer_compte("ab", "motdepasse1")                 # identifiant trop court
    with pytest.raises(comptes.ErreurCompte):
        comptes.creer_compte("alice", "court")                    # mot de passe trop court
    with pytest.raises(comptes.ErreurCompte):
        comptes.creer_compte("alice", "motdepasse1", "autre")     # confirmation différente
    comptes.creer_compte("alice", "motdepasse1")
    with pytest.raises(comptes.ErreurCompte):
        comptes.creer_compte("alice", "motdepasse2")              # identifiant déjà pris


def test_mot_de_passe_jamais_enregistre_et_donnees_chiffrees():
    session = comptes.creer_compte("kevin", "SecretTresLong!")
    session.enregistrer("Mon PEA", CSV)
    for fichier in comptes._dossier().rglob("*"):
        if fichier.is_file():
            contenu = fichier.read_bytes()
            assert b"SecretTresLong" not in contenu
            assert b"LVMH" not in contenu and b"Mon PEA" not in contenu    # ni données ni noms en clair


def test_chacun_ne_voit_que_ses_portefeuilles():
    a = comptes.creer_compte("alice", "motdepasse-a")
    b = comptes.creer_compte("bob", "motdepasse-b")
    ident = a.enregistrer("PEA d'Alice", CSV)
    assert [p["nom"] for p in a.lister()] == ["PEA d'Alice"]
    assert b.lister() == []
    with pytest.raises(comptes.ErreurCompte):
        b.lire(ident)                                             # Bob ne peut pas l'ouvrir
    # Même en copiant le fichier chiffré d'Alice, la clé de Bob ne le déchiffre pas
    fichier = a.dossier / f"{ident}.enc"
    with pytest.raises(coffre.DonneesIllisibles):
        coffre.dechiffrer(b._cle, fichier.read_bytes())
    assert comptes.connecter("alice", "motdepasse-a").lire(ident) == CSV


def test_fichier_modifie_rejete():
    session = comptes.creer_compte("kevin", "motdepasse1")
    ident = session.enregistrer("PEA", CSV)
    fichier = session.dossier / f"{ident}.enc"
    octets = bytearray(fichier.read_bytes())
    octets[40] ^= 1                                               # un seul bit modifié
    fichier.write_bytes(bytes(octets))
    with pytest.raises(coffre.DonneesIllisibles):
        session.lire(ident)


def test_renommer_remplacer_supprimer():
    session = comptes.creer_compte("kevin", "motdepasse1")
    ident = session.enregistrer("PEA", CSV)
    assert session.enregistrer("pea", CSV + b"2024-02-01,ACHAT,AI.PA,Air Liquide,5,170,2\n") == ident  # même nom : remplacé
    assert session.lister()[0]["operations"] == 2
    session.renommer(ident, "PEA Boursorama")
    assert session.lister()[0]["nom"] == "PEA Boursorama"
    session.supprimer(ident)
    assert session.lister() == [] and not (session.dossier / f"{ident}.enc").exists()


def test_changer_de_mot_de_passe_garde_les_donnees():
    session = comptes.creer_compte("kevin", "ancien-mdp")
    ident = session.enregistrer("PEA", CSV)
    with pytest.raises(comptes.ErreurCompte):
        session.changer_mot_de_passe("faux-mdp", "nouveau-mdp")
    session.changer_mot_de_passe("ancien-mdp", "nouveau-mdp", "nouveau-mdp")
    with pytest.raises(comptes.ErreurCompte):
        comptes.connecter("kevin", "ancien-mdp")
    assert comptes.connecter("kevin", "nouveau-mdp").lire(ident) == CSV


def test_suppression_du_compte():
    session = comptes.creer_compte("kevin", "motdepasse1")
    session.enregistrer("PEA", CSV)
    dossier = session.dossier
    with pytest.raises(comptes.ErreurCompte):
        session.supprimer_compte("faux")
    session.supprimer_compte("motdepasse1")
    assert not dossier.exists() and comptes.nombre_de_comptes() == 0
    with pytest.raises(comptes.ErreurCompte):
        comptes.connecter("kevin", "motdepasse1")


def test_blocage_apres_trop_d_essais():
    comptes.creer_compte("kevin", "motdepasse1")
    for _ in range(comptes.ESSAIS_MAX):
        with pytest.raises(comptes.ErreurCompte):
            comptes.connecter("kevin", "faux")
    with pytest.raises(comptes.ErreurCompte) as erreur:
        comptes.connecter("kevin", "motdepasse1")                 # même le bon mot de passe attend
    assert "réessayez" in str(erreur.value)


def test_preferences_chiffrees_et_conservees():
    """Le mode nuit choisi est gardé dans le compte, chiffré, et survit au changement de mot de passe."""
    s = comptes.creer_compte("prefs", "motdepasse123")
    assert s.preference("theme", "clair") == "clair"
    s.definir_preference("theme", "nuit")
    fichier = s.dossier / "preferences.enc"
    assert fichier.exists() and b"nuit" not in fichier.read_bytes()        # illisible sans la clé
    assert comptes.connecter("prefs", "motdepasse123").preference("theme") == "nuit"
    s.changer_mot_de_passe("motdepasse123", "nouveau-mot-de-passe")
    assert comptes.connecter("prefs", "nouveau-mot-de-passe").preference("theme") == "nuit"


def test_theme_nuit_recolore_les_graphiques():
    """En mode nuit, les couleurs sombres des courbes deviennent claires ; rien ne change en mode clair."""
    import plotly.graph_objects as go
    from src import graphiques_interactifs as gi, theme
    fig = go.Figure(go.Scatter(x=[0, 1], y=[0, 1], line=dict(color="#1a1a19")))
    theme.definir("clair")
    assert gi.theme_figure(fig).data[0]["line"]["color"] == "#1a1a19"
    theme.definir("nuit")
    try:
        assert gi.theme_figure(fig).data[0]["line"]["color"] == "#e6ebf2"
    finally:
        theme.definir("clair")
