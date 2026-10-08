"""
Tests de l'affichage : anneaux de répartition (parts, couleurs, légende) et menu de la barre latérale.
"""

import pandas as pd

from src import graphiques_interactifs as gi
from src import interface as ui


def test_autres_seulement_a_partir_de_deux_petites_parts():
    une_petite = pd.Series({"A": 0.6, "B": 0.38, "C": 0.02})
    noms = [p["nom"] for p in gi.parts_anneau(une_petite)]
    assert not any(n.startswith("Autres") for n in noms) and len(noms) == 3
    deux_petites = pd.Series({"A": 0.6, "B": 0.36, "C": 0.02, "D": 0.02})
    parts = gi.parts_anneau(deux_petites)
    assert parts[-1]["nom"] == "Autres (2)" and abs(parts[-1]["poids"] - 0.04) < 1e-9
    assert abs(sum(p["poids"] for p in parts) - 1) < 1e-9


def test_couleurs_des_classes_identiques_partout_et_lisibles_de_nuit():
    parts = gi.parts_anneau(pd.Series({"Actions": 0.63, "Obligations": 0.32, "Or": 0.05}),
                            couleurs=gi.COULEURS_CLASSES)
    assert [p["couleur"] for p in parts] == [gi.COULEURS_CLASSES[c] for c in ("Actions", "Obligations", "Or")]
    # aucune couleur d'anneau trop sombre pour le fond bleu nuit (#0f1b2d)
    for couleur in gi.PALETTE_ANNEAU + list(gi.COULEURS_CLASSES.values()):
        r, g, b = (int(couleur[i:i + 2], 16) for i in (1, 3, 5))
        assert 0.2126 * r + 0.7152 * g + 0.0722 * b > 80, couleur
    couleurs = [p["couleur"] for p in gi.parts_anneau(pd.Series({f"G{i}": 1 / 9 for i in range(9)}), max_parts=8)]
    assert len(set(couleurs[:8])) == 8


def test_anneau_et_legende():
    parts = gi.parts_anneau(pd.Series({"Actions": 0.63, "Obligations": 0.37}), 1000.0)
    fig = gi.fig_anneau(None, 1000.0, parts=parts)
    assert fig is not None
    legende = ui.legende_parts(parts)
    assert legende.count("legende-ligne") == 2 and "63,0 %" in legende


def test_style_du_menu():
    css = ui.style_menu(['Légende "1"', "Deux"], actif=1)
    assert ".st-key-menu_0 button p::after" in css and "”" in css and '\\"' not in css
    assert ".st-key-menu_1 button {" in css and ".st-key-menu_0 button {" not in css
    assert ".st-key-menu_" in ui.style_menu(["a"], actif=None) and "fond-actif" not in ui.style_menu(["a"], None)
