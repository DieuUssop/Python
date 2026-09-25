"""
graphiques.py — Les graphiques du projet.

Pour l'instant : un graphique de l'évolution du portefeuille, enregistré en
image PNG. À l'étape 6, on passera à des graphiques interactifs (Plotly).
"""

import matplotlib
import numpy as np

# "Agg" = on dessine directement dans un fichier, sans ouvrir de fenêtre.
matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as mticker  # noqa: E402

# Couleurs du projet (réutilisées dans tous les graphiques pour la cohérence).
BLEU = "#2a78d6"     # la valeur du portefeuille
ORANGE = "#eb6834"   # l'argent investi
GRIS = "#898781"     # axes, textes secondaires
GRILLE = "#e1e0d9"


def graphique_historique(histo, chemin_png):
    """Trace la valeur du portefeuille et l'argent investi au fil du temps.

    L'écart entre les deux courbes = le gain (ou la perte) à chaque date.
    """
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=120)

    ax.plot(histo.index, histo["valeur"], color=BLEU, linewidth=2,
            label="Valeur du portefeuille")
    # drawstyle="steps-post" : l'argent investi change "par marches",
    # uniquement les jours où il y a une transaction.
    ax.plot(histo.index, histo["apports_nets"], color=ORANGE, linewidth=2,
            drawstyle="steps-post", label="Argent investi (apports nets)")

    # On colorie légèrement l'écart entre les deux courbes.
    ax.fill_between(histo.index, histo["apports_nets"], histo["valeur"],
                    color=BLEU, alpha=0.08, linewidth=0)

    # Étiquettes directes au bout de chaque courbe (valeur du dernier jour).
    dernier = histo.iloc[-1]
    for colonne, couleur in [("valeur", BLEU), ("apports_nets", ORANGE)]:
        ax.annotate(f"{dernier[colonne]:,.0f} €".replace(",", " "),
                    xy=(histo.index[-1], dernier[colonne]),
                    xytext=(6, 0), textcoords="offset points",
                    va="center", fontsize=9, color="#333333")
        ax.plot(histo.index[-1], dernier[colonne], "o", color=couleur,
                markersize=6, markeredgecolor="white", markeredgewidth=1.5)

    # Mise en forme sobre : grille légère, pas de cadre inutile.
    ax.set_title("Évolution du portefeuille", loc="left", fontsize=14,
                 fontweight="bold", color="#1a1a19")
    ax.set_ylabel("Euros", color=GRIS)
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", " ")))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))
    ax.grid(axis="y", color=GRILLE, linewidth=0.8)
    ax.set_axisbelow(True)
    for cote in ["top", "right", "left"]:
        ax.spines[cote].set_visible(False)
    ax.spines["bottom"].set_color(GRIS)
    ax.tick_params(colors=GRIS, labelsize=9)
    ax.legend(loc="upper left", frameon=False, fontsize=10)
    ax.margins(x=0.01)

    fig.tight_layout()
    fig.savefig(chemin_png)
    plt.close(fig)


ROUGE = "#d03b3b"    # les baisses (drawdown)


def _mise_en_forme(ax, titre):
    """Style commun à tous les graphiques (pour ne pas le répéter)."""
    ax.set_title(titre, loc="left", fontsize=12, fontweight="bold", color="#1a1a19")
    ax.grid(axis="y", color=GRILLE, linewidth=0.8)
    ax.set_axisbelow(True)
    for cote in ["top", "right", "left"]:
        ax.spines[cote].set_visible(False)
    ax.spines["bottom"].set_color(GRIS)
    ax.tick_params(colors=GRIS, labelsize=9)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))
    ax.margins(x=0.01)


def graphique_performance(ind, chemin_png):
    """Deux graphiques superposés, avec le même axe des dates :
      - en haut : la performance pure (indice base 100, TWR) ;
      - en bas  : le drawdown (baisse depuis le dernier plus haut).
    """
    fig, (haut, bas) = plt.subplots(
        2, 1, figsize=(11, 7), dpi=120, sharex=True,
        gridspec_kw={"height_ratios": [2, 1]},
    )

    # --- En haut : indice base 100 ---
    indice = ind["indice"]
    haut.plot(indice.index, indice, color=BLEU, linewidth=2)
    haut.axhline(100, color=GRIS, linewidth=0.8, linestyle="--")
    haut.annotate(f"{indice.iloc[-1]:.1f}", xy=(indice.index[-1], indice.iloc[-1]),
                  xytext=(6, 0), textcoords="offset points", va="center",
                  fontsize=9, color="#333333")
    _mise_en_forme(haut, "Performance du portefeuille (base 100, hors effet des apports)")

    # --- En bas : drawdown en % ---
    dd = ind["drawdown"] * 100
    bas.fill_between(dd.index, dd, 0, color=ROUGE, alpha=0.25, linewidth=0)
    bas.plot(dd.index, dd, color=ROUGE, linewidth=1.2)
    # On marque le pire moment.
    bas.plot(ind["date_creux"], ind["max_drawdown"] * 100, "o", color=ROUGE,
             markersize=7, markeredgecolor="white", markeredgewidth=1.5)
    # Si le creux est dans la partie droite du graphique, on écrit à gauche du point.
    a_droite = ind["date_creux"] > dd.index[0] + (dd.index[-1] - dd.index[0]) * 0.6
    bas.annotate(f"Max drawdown : {ind['max_drawdown'] * 100:.1f} %",
                 xy=(ind["date_creux"], ind["max_drawdown"] * 100),
                 xytext=(-10 if a_droite else 10, 0), textcoords="offset points",
                 ha="right" if a_droite else "left", va="center",
                 fontsize=9, color="#333333")
    bas.set_ylim(top=0.5)
    bas.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:g} %"))
    _mise_en_forme(bas, "Drawdown (baisse depuis le dernier plus haut)")

    fig.tight_layout()
    fig.savefig(chemin_png)
    plt.close(fig)


# ======================================================================
# Étape 5
# ======================================================================
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

GRIS_FONCE = "#5f5e5a"   # l'indice de référence (neutre, en retrait)


def graphique_comparaison(avance, nom_indice, chemin_png):
    """Portefeuille et indice de référence, tous deux en base 100."""
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=120)
    series = [
        (avance["indice_portefeuille"], BLEU, "Mon portefeuille", 2.2),
        (avance["indice_reference"], GRIS_FONCE, nom_indice, 1.6),
    ]
    for serie, couleur, nom, epaisseur in series:
        ax.plot(serie.index, serie, color=couleur, linewidth=epaisseur, label=nom)
        ax.plot(serie.index[-1], serie.iloc[-1], "o", color=couleur, markersize=6,
                markeredgecolor="white", markeredgewidth=1.5)
        ax.annotate(f"{serie.iloc[-1]:.1f}", xy=(serie.index[-1], serie.iloc[-1]),
                    xytext=(6, 0), textcoords="offset points", va="center",
                    fontsize=9, color="#333333")
    ax.axhline(100, color=GRIS, linewidth=0.8, linestyle="--")
    _mise_en_forme(ax, "Mon portefeuille face à l'indice de référence (base 100)")
    ax.legend(loc="upper left", frameon=False, fontsize=10)
    fig.tight_layout()
    fig.savefig(chemin_png)
    plt.close(fig)


def graphique_correlations(matrice, chemin_png):
    """Carte de chaleur de la matrice de corrélation.

    Palette "divergente" : bleu = corrélation négative, gris = nulle,
    rouge = positive. Les valeurs sont écrites dans chaque case.
    """
    palette = LinearSegmentedColormap.from_list(
        "divergente", ["#184f95", "#f0efec", "#b52f2f"])
    n = len(matrice)
    # Taille adaptée au nombre de titres, plafonnée pour rester raisonnable.
    fig, ax = plt.subplots(figsize=(min(1.3 * n + 2.5, 12), min(1.1 * n + 1.5, 10)), dpi=120)
    taille_texte = 9 if n <= 8 else 7
    image = ax.imshow(matrice.values, cmap=palette, vmin=-1, vmax=1)

    ax.set_xticks(range(n), matrice.columns, rotation=45, ha="right")
    ax.set_yticks(range(n), matrice.index)
    ax.tick_params(colors="#333333", labelsize=9 if n <= 20 else 6, length=0)
    for i in range(n if n <= 15 else 0):          # au-delà de 15 titres : pas de chiffres (illisibles)
        for j in range(n):
            valeur = matrice.values[i, j]
            couleur_texte = "white" if abs(valeur) > 0.6 else "#1a1a19"
            ax.text(j, i, f"{round(valeur, 2) + 0.0:.2f}", ha="center", va="center",
                    fontsize=taille_texte, color=couleur_texte)
    # Fines lignes blanches entre les cases
    ax.set_xticks(np.arange(-0.5, n), minor=True)
    ax.set_yticks(np.arange(-0.5, n), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", length=0)
    for cote in ax.spines.values():
        cote.set_visible(False)

    barre = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    barre.outline.set_visible(False)
    barre.ax.tick_params(colors=GRIS, labelsize=8)
    ax.set_title("Corrélation des rendements quotidiens", loc="left",
                 fontsize=12, fontweight="bold", color="#1a1a19")
    fig.tight_layout()
    fig.savefig(chemin_png)
    plt.close(fig)


# ======================================================================
# Étape 7 : Markowitz
# ======================================================================
AQUA = "#1baf7a"     # portefeuille de variance minimale
VERT = "#008300"     # portefeuille de Sharpe maximal


def graphique_frontiere(res, chemin_png):
    """Nuage des portefeuilles possibles, frontière efficiente et points clés."""
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=120)
    alea, front = res["aleatoires"], res["frontiere"]

    # Nuage de portefeuilles aléatoires, coloré selon le Sharpe (bleu clair -> foncé)
    nuage = ax.scatter(alea["volatilite"] * 100, alea["rendement"] * 100, c=alea["sharpe"],
                       cmap=LinearSegmentedColormap.from_list("bleus", ["#cde2fb", "#0d366b"]),
                       s=6, alpha=0.6, linewidths=0)
    barre = fig.colorbar(nuage, ax=ax, fraction=0.035, pad=0.02)
    barre.set_label("Ratio de Sharpe", color=GRIS, fontsize=9)
    barre.outline.set_visible(False)
    barre.ax.tick_params(colors=GRIS, labelsize=8)

    # Frontière efficiente
    ax.plot(front["volatilite"] * 100, front["rendement"] * 100, color="#1a1a19",
            linewidth=2.2, label="Frontière efficiente")

    # Droite de marché des capitaux (CML) : du taux sans risque au portefeuille tangent
    rf, tangent = res["taux_sans_risque"], res["sharpe_max"]
    vmax = front["volatilite"].max() * 100 * 1.05
    pente = (tangent["rendement"] - rf) / tangent["volatilite"]
    ax.plot([0, vmax], [rf * 100, (rf + pente * vmax / 100) * 100], color=GRIS,
            linewidth=1.2, linestyle="--", label="Droite de marché des capitaux")

    # Titres seuls (petits points gris + nom)
    seuls = res["titres_seuls"]
    ax.scatter(seuls["volatilite"] * 100, seuls["rendement"] * 100, color=GRIS, s=18, zorder=3)
    for ticker, ligne in (seuls.iterrows() if len(seuls) <= 20 else []):
        ax.annotate(ticker, (ligne["volatilite"] * 100, ligne["rendement"] * 100),
                    xytext=(4, 3), textcoords="offset points", fontsize=7, color=GRIS)

    # Les trois portefeuilles à comparer
    for cle, nom, couleur, marqueur in [("actuel", "Mon portefeuille", ORANGE, "o"),
                                        ("variance_min", "Variance minimale", AQUA, "D"),
                                        ("sharpe_max", "Sharpe maximal", VERT, "*")]:
        p = res[cle]
        ax.scatter(p["volatilite"] * 100, p["rendement"] * 100, color=couleur, marker=marqueur,
                   s=220 if marqueur == "*" else 110, edgecolors="white", linewidths=1.5,
                   zorder=5, label=f"{nom} (Sharpe {p['sharpe']:.2f})")

    ax.set_xlabel("Volatilité annuelle (%)", color=GRIS)
    ax.set_ylabel("Rendement annuel espéré (%)", color=GRIS)
    ax.set_xlim(left=0)
    ax.set_title(f"Frontière efficiente de Markowitz (poids max {res['poids_max']:.0%} par titre)",
                 loc="left", fontsize=12, fontweight="bold", color="#1a1a19")
    ax.grid(color=GRILLE, linewidth=0.8)
    ax.set_axisbelow(True)
    for cote in ["top", "right"]:
        ax.spines[cote].set_visible(False)
    for cote in ["left", "bottom"]:
        ax.spines[cote].set_color(GRIS)
    ax.tick_params(colors=GRIS, labelsize=9)
    ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor=GRILLE, fontsize=9)
    fig.tight_layout()
    fig.savefig(chemin_png)
    plt.close(fig)


def graphique_poids(res, chemin_png):
    """Poids actuels et poids optimaux (Sharpe maximal), titre par titre."""
    poids = res["poids"]
    if len(poids) > 25:   # beaucoup de titres : on garde les 25 lignes les plus importantes
        importance = poids[["actuel", "variance_min", "sharpe_max"]].max(axis=1)
        poids = poids.loc[importance.sort_values(ascending=False).index[:25]]
    poids = poids.sort_values("actuel")
    n = len(poids)
    fig, ax = plt.subplots(figsize=(10, max(4, 0.45 * n + 1.5)), dpi=120)
    y = np.arange(n)
    hauteur = 0.38
    ax.barh(y + hauteur / 2, poids["actuel"] * 100, height=hauteur, color=ORANGE,
            label="Mon portefeuille")
    ax.barh(y - hauteur / 2, poids["sharpe_max"] * 100, height=hauteur, color=VERT,
            label="Sharpe maximal")
    ax.set_yticks(y, poids["nom"])
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:g} %"))
    ax.set_title("Poids actuels et poids optimaux", loc="left", fontsize=12,
                 fontweight="bold", color="#1a1a19")
    ax.grid(axis="x", color=GRILLE, linewidth=0.8)
    ax.set_axisbelow(True)
    for cote in ["top", "right", "left"]:
        ax.spines[cote].set_visible(False)
    ax.tick_params(colors="#333333", labelsize=9, length=0)
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(chemin_png)
    plt.close(fig)


# ======================================================================
# Étape 8 : projection Monte-Carlo
# ======================================================================
def graphique_projection(sim, chemin_png):
    """Éventail des trajectoires simulées : zones de 90 % et 50 %, médiane,
    et argent investi. chemin_png peut être un nom de fichier ou un fichier
    en mémoire (io.BytesIO) : utile pour le rapport PDF."""
    t = sim["trajectoires"]
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=120)
    ax.fill_between(t.index, t["p5"], t["p95"], color=BLEU, alpha=0.12, linewidth=0,
                    label="90 % des scénarios (5e – 95e percentile)")
    ax.fill_between(t.index, t["p25"], t["p75"], color=BLEU, alpha=0.25, linewidth=0,
                    label="50 % des scénarios (25e – 75e percentile)")
    ax.plot(t.index, t["p50"], color=BLEU, linewidth=2.2, label="Scénario médian")
    ax.plot(t.index, t["apports"], color=ORANGE, linewidth=1.6, linestyle="--",
            label="Argent investi")
    for colonne in ["p5", "p50", "p95"]:
        valeur = t[colonne].iloc[-1]
        ax.annotate(f"{valeur:,.0f} €".replace(",", " "), xy=(t.index[-1], valeur),
                    xytext=(6, 0), textcoords="offset points", va="center",
                    fontsize=9, color="#333333")
    _mise_en_forme(ax, f"Projection Monte-Carlo sur {sim['parametres']['annees']:g} ans "
                       f"({sim['parametres']['nb_simulations']:,} scénarios)".replace(",", " "))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", " ")))
    ax.set_ylabel("Euros", color=GRIS)
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.margins(x=0.01)
    fig.tight_layout()
    fig.savefig(chemin_png)
    plt.close(fig)


COULEURS_TRANCHES = ["#a32020", "#e0797b", "#a3a39e", "#5598e7", "#184f95"]


def graphique_projection_nuage(sim, chemin_png):
    """Nuage de points : chaque point est un scénario à une date, coloré selon
    sa tranche de probabilité (du rouge = défavorable au bleu = favorable)."""
    from .simulation import TRANCHES, points_nuage   # import local : évite une dépendance circulaire
    t = sim["trajectoires"]
    points = points_nuage(sim)
    fig, ax = plt.subplots(figsize=(11, 5), dpi=120)
    for numero, (nom, couleur) in enumerate(zip(TRANCHES, COULEURS_TRANCHES)):
        tranche = points[points["tranche"] == numero]
        ax.scatter(tranche["date"], tranche["valeur"], s=9, color=couleur, alpha=0.75,
                   linewidths=0, label=nom)
    ax.plot(t.index, t["p50"], color="#1a1a19", linewidth=1.8, label="Médiane")
    ax.plot(t.index, t["p5"], color=COULEURS_TRANCHES[0], linewidth=1, linestyle=":")
    ax.plot(t.index, t["p95"], color=COULEURS_TRANCHES[4], linewidth=1, linestyle=":")
    ax.plot(t.index, t["apports"], color=ORANGE, linewidth=1.4, linestyle="--", label="Argent investi")
    _mise_en_forme(ax, f"Scénarios simulés par tranche de probabilité ({len(sim['echantillon'].columns)} "
                       "scénarios affichés)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}".replace(",", " ")))
    ax.set_ylabel("Euros", color=GRIS)
    ax.legend(loc="upper left", frameon=False, fontsize=8, ncol=2, markerscale=2)
    fig.tight_layout()
    fig.savefig(chemin_png)
    plt.close(fig)
