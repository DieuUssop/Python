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


def graphique_correlations(matrice, chemin_png, ordre=None, noms=None, titre="Corrélation des rendements quotidiens"):
    """Carte de chaleur des corrélations, lisible même avec beaucoup de titres.

    - ordre : titres regroupés par blocs qui évoluent ensemble (expositions.ordre_regroupement) ;
    - triangle inférieur seulement, sans la diagonale (toujours égale à 1) ;
    - palette divergente : bleu = négative, blanc = nulle, rouge = positive ;
    - valeurs écrites dans les cases jusqu'à 12 lignes.
    """
    palette = LinearSegmentedColormap.from_list(
        "divergente", ["#1c5cab", "#8fb6e6", "#f7f7f5", "#eaa48f", "#a8322a"])
    palette.set_bad("white")
    ordre = [o for o in (ordre or list(matrice.index)) if o in matrice.index]
    m = matrice.loc[ordre, ordre]
    noms = noms or {}
    court = lambda c: (lambda x: x if len(x) <= 18 else x[:17] + "…")(str(noms.get(c, c)))
    lignes, colonnes = ordre[1:], ordre[:-1]
    valeurs = np.array([[m.at[a, b] if j < i else np.nan for j, b in enumerate(colonnes)]
                        for i, a in enumerate(lignes, start=1)], dtype=float)
    n = len(lignes)
    cote = min(max(0.32 * n + 2.5, 4.5), 11)
    fig, ax = plt.subplots(figsize=(cote + 1.2, cote), dpi=120)
    image = ax.imshow(np.ma.masked_invalid(valeurs), cmap=palette, vmin=-1, vmax=1)
    ax.set_xticks(range(n), [court(c) for c in colonnes], rotation=60, ha="right")
    ax.set_yticks(range(n), [court(c) for c in lignes])
    ax.tick_params(colors="#333333", labelsize=9 if n <= 15 else 7 if n <= 30 else 5.5, length=0)
    if n <= 12:
        for i in range(n):
            for j in range(i + 1):
                valeur = valeurs[i, j]
                ax.text(j, i, f"{valeur:.2f}".replace(".", ","), ha="center", va="center",
                        fontsize=8 if n > 8 else 9, color="white" if abs(valeur) > 0.6 else "#1a1a19")
    ax.set_xticks(np.arange(-0.5, n), minor=True)
    ax.set_yticks(np.arange(-0.5, n), minor=True)
    ax.grid(which="minor", color="white", linewidth=1 if n > 20 else 2)
    ax.tick_params(which="minor", length=0)
    for bord in ax.spines.values():
        bord.set_visible(False)
    barre = fig.colorbar(image, ax=ax, fraction=0.035, pad=0.03, ticks=[-1, -0.5, 0, 0.5, 1])
    barre.outline.set_visible(False)
    barre.ax.tick_params(colors=GRIS, labelsize=8)
    ax.set_title(titre, loc="left", fontsize=12, fontweight="bold", color="#1a1a19")
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


def graphique_poids(res, chemin_png, cible="sharpe_max", max_lignes=18):
    """Graphique « de → à » : poids actuel (rond blanc) et poids conseillé (triangle),
    vert si on renforce, rouge si on allège ; plafond par titre en pointillés."""
    from .optimisation import comparer_repartitions
    tableau = comparer_repartitions(res, cible)
    bouge = tableau[tableau["sens"] != "inchange"].head(max_lignes).iloc[::-1]
    n = max(len(bouge), 1)
    fig, ax = plt.subplots(figsize=(10, max(3.2, 0.42 * n + 1.6)), dpi=120)
    couleurs = {"renforcer": "#0b7a33", "alleger": "#c0392b", "sortir": "#c0392b"}
    y = np.arange(len(bouge))
    for i, (_, l) in enumerate(bouge.iterrows()):
        c = couleurs[l["sens"]]
        ax.plot([l["actuel"] * 100, l["cible"] * 100], [i, i], color=c, linewidth=2.6, solid_capstyle="round")
        ax.plot(l["cible"] * 100, i, marker=">" if l["sens"] == "renforcer" else "<", color=c, markersize=10)
        ax.plot(l["actuel"] * 100, i, "o", markerfacecolor="white", markeredgecolor="#5f5e5a", markersize=8,
                markeredgewidth=1.6)
        texte = f"{l['actuel'] * 100:.1f} % → {l['cible'] * 100:.1f} %".replace(".", ",")
        ax.annotate(texte, (max(l["actuel"], l["cible"]) * 100, i), xytext=(8, 0), textcoords="offset points",
                    va="center", fontsize=8.5, color="#5f5e5a")
    if res.get("poids_max", 1) < 1:
        ax.axvline(res["poids_max"] * 100, color=GRIS, linestyle="--", linewidth=1.2)
        ax.annotate(f"Plafond {res['poids_max'] * 100:.0f} %", (res["poids_max"] * 100, len(bouge) - 0.4),
                    xytext=(4, 0), textcoords="offset points", fontsize=8.5, color=GRIS)
    ax.set_yticks(y, bouge["nom"])
    xmax = max(bouge[["actuel", "cible"]].max().max() * 100 if len(bouge) else 10, res.get("poids_max", 0) * 100
               if res.get("poids_max", 1) < 1 else 0)
    ax.set_xlim(0, xmax * 1.3 + 1)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:g} %"))
    ax.set_title("Du portefeuille actuel au portefeuille de Sharpe maximal" if cible == "sharpe_max"
                 else "Du portefeuille actuel au portefeuille de variance minimale",
                 loc="left", fontsize=12, fontweight="bold", color="#1a1a19")
    ax.grid(axis="x", color=GRILLE, linewidth=0.8)
    ax.set_axisbelow(True)
    for cote in ["top", "right", "left"]:
        ax.spines[cote].set_visible(False)
    ax.tick_params(colors="#333333", labelsize=9, length=0)
    from matplotlib.lines import Line2D
    ax.legend(handles=[Line2D([], [], marker="o", color="none", markerfacecolor="white", markeredgecolor="#5f5e5a",
                              label="Poids actuel"),
                       Line2D([], [], marker=">", color="#0b7a33", label="À renforcer"),
                       Line2D([], [], marker="<", color="#c0392b", label="À alléger ou vendre")],
              loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=False, fontsize=8.5)
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


# ======================================================================
# Distribution des rendements quotidiens (rapport PDF, onglet Risque)
# ======================================================================
def graphique_distribution(ind, av, niveau_var, chemin_png):
    """Histogramme des rendements quotidiens, loi normale de même moyenne et même
    écart-type, VaR historique / normale / Cornish-Fisher et CVaR (légende en haut)."""
    from statistics import NormalDist
    r = ind["rendements"].dropna() * 100
    n = len(r)
    bas, haut = float(r.min()), float(r.max())
    nb_classes = int(min(80, max(20, np.sqrt(n) * 1.2)))
    largeur = (haut - bas) / nb_classes if haut > bas else 0.1
    fig, ax = plt.subplots(figsize=(11, 5), dpi=120)
    ax.hist(r, bins=np.arange(bas, haut + 2 * largeur, largeur), color=BLEU, alpha=0.7,
            edgecolor="white", linewidth=0.5, label="Jours observés")
    if r.std() > 0:
        loi = NormalDist(float(r.mean()), float(r.std()))
        xs = np.linspace(bas - largeur, haut + largeur, 300)
        ax.plot(xs, [loi.pdf(x) * n * largeur for x in xs], color="#1a1a19", linewidth=1.8,
                label="Loi normale (même moyenne et volatilité)")
    niveau = f"{niveau_var * 100:.0f} %"
    for cle, nom, couleur, trait in [("var_historique", f"VaR historique {niveau}", ORANGE, "--"),
                                     ("var_parametrique", f"VaR loi normale {niveau}", "#5f5e5a", ":"),
                                     ("var_cornish_fisher", f"VaR Cornish-Fisher {niveau}", "#7a4fb5", "-."),
                                     ("cvar", "CVaR (Expected Shortfall)", ROUGE, "-")]:
        v = av.get(cle)
        if v is not None and v == v:
            ax.axvline(-v * 100, color=couleur, linestyle=trait, linewidth=1.8, label=nom)
    ax.set_title("Distribution des rendements quotidiens", loc="left", fontsize=12, fontweight="bold",
                 color="#1a1a19")
    ax.grid(axis="y", color=GRILLE, linewidth=0.8)
    ax.set_axisbelow(True)
    for cote in ["top", "right", "left"]:
        ax.spines[cote].set_visible(False)
    ax.spines["bottom"].set_color(GRIS)
    ax.tick_params(colors=GRIS, labelsize=9)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.1f} %".replace(".", ",")))
    ax.set_xlabel("Rendement quotidien", color=GRIS, fontsize=9)
    ax.set_ylabel("Nombre de jours", color=GRIS, fontsize=9)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3, fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(chemin_png)
    plt.close(fig)


def graphique_distribution_finale(sim, chemin_png):
    """Distribution de la valeur finale (Monte-Carlo) : zone des 90 % de scénarios,
    médiane, moyenne et montant investi."""
    finales = np.asarray(sim["valeurs_finales"], dtype=float)
    finales = finales[np.isfinite(finales) & (finales > 0)]
    bas, haut = np.percentile(finales, [0.5, 99.5])
    bas, haut = min(bas, sim["total_apporte"] * 0.97), max(haut, sim["total_apporte"] * 1.03)
    x = finales[(finales >= bas) & (finales <= haut)]
    fig, ax = plt.subplots(figsize=(11, 4.2), dpi=120)
    ax.axvspan(sim["p5"], sim["p95"], color=BLEU, alpha=0.10, label="90 % des scénarios (P5 à P95)")
    ax.hist(x, bins=60, color=BLEU, alpha=0.8, edgecolor="white", linewidth=0.5)
    for cle, nom, couleur, trait in [("total_apporte", "Montant investi", ORANGE, "--"),
                                     ("mediane", "Médiane", "#1a1a19", "-"), ("moyenne", "Moyenne", "#5f5e5a", ":")]:
        ax.axvline(sim[cle], color=couleur, linestyle=trait, linewidth=1.8, label=nom)
    ax.set_xlim(bas, haut)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f} €".replace(",", " ")))
    ax.set_title("Distribution de la valeur finale", loc="left", fontsize=12, fontweight="bold", color="#1a1a19")
    ax.grid(axis="y", color=GRILLE, linewidth=0.8)
    ax.set_axisbelow(True)
    for cote in ["top", "right", "left"]:
        ax.spines[cote].set_visible(False)
    ax.tick_params(colors=GRIS, labelsize=9)
    ax.set_ylabel("Nombre de scénarios", color=GRIS, fontsize=9)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=4, frameon=False, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(chemin_png)
    plt.close(fig)
