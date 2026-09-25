"""
graphiques_interactifs.py — Les graphiques du tableau de bord (Plotly).

Différence avec graphiques.py (matplotlib) :
    matplotlib produit des IMAGES fixes (pour un rapport PDF) ;
    Plotly produit des graphiques INTERACTIFS : survol à la souris, zoom,
    choix de la période, masquage d'une courbe en cliquant sur la légende.

Chaque fonction reçoit des données et renvoie une "figure" Plotly, que
app.py affiche avec st.plotly_chart().
"""

import plotly.graph_objects as go

from .simulation import TRANCHES, points_nuage

# Mêmes couleurs que les graphiques matplotlib, pour la cohérence visuelle.
BLEU = "#2a78d6"        # le portefeuille
ORANGE = "#eb6834"      # l'argent investi
GRIS_FONCE = "#5f5e5a"  # l'indice de référence
GRIS = "#898781"        # axes, textes secondaires
GRILLE = "#e1e0d9"
ROUGE = "#d03b3b"       # pertes, baisses
VERT = "#0ca30c"        # gains
TEXTE = "#1a1a19"


# ======================================================================
# Réglages communs
# ======================================================================
POLICE = "Inter, 'Segoe UI', Roboto, Arial, sans-serif"

# Options de la barre d'outils Plotly (à passer à st.plotly_chart(config=...)) :
# on retire le logo Plotly et les outils de sélection peu utiles.
CONFIG_PLOTLY = {
    "displaylogo": False,
    "modeBarButtonsToRemove": ["select2d", "lasso2d", "autoScale2d", "toggleSpikelines"],
    "toImageButtonOptions": {"format": "png", "scale": 2},   # export net pour le rapport
}


def _style(fig, titre=None, hauteur=420, legende=True):
    """Applique le même style sobre à tous les graphiques."""
    fig.update_layout(
        template="plotly_white",
        height=hauteur,
        title=dict(text=titre, x=0, xanchor="left", font=dict(size=15, color=TEXTE)) if titre else None,
        margin=dict(l=4, r=8, t=50 if titre else 12, b=4),
        font=dict(family=POLICE, size=12, color=TEXTE),
        paper_bgcolor="rgba(0,0,0,0)",   # fond transparent : le graphique se fond dans son encadré
        plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white", bordercolor=GRILLE, font=dict(family=POLICE, size=12, color=TEXTE)),
        showlegend=legende,
        legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="left", x=0,
                    font=dict(size=12, color="#5f5e5a")),
        separators=", ",   # virgule décimale et espace pour les milliers (à la française)
    )
    fig.update_xaxes(showgrid=False, linecolor=GRILLE, tickfont=dict(color=GRIS, size=11))
    fig.update_yaxes(gridcolor="#eef0f3", zeroline=False, tickfont=dict(color=GRIS, size=11))
    return fig


def _axe_dates(fig):
    """Dates au format français (pas de noms de mois en anglais)."""
    fig.update_xaxes(tickformat="%m/%Y", hoverformat="%d/%m/%Y")
    return fig


def _selecteur_periode(fig):
    """Ajoute des boutons 1M / 6M / YTD / 1A / Tout au-dessus d'un graphique."""
    fig.update_xaxes(
        rangeselector=dict(
            buttons=[
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1A", step="year", stepmode="backward"),
                dict(step="all", label="Tout"),
            ],
            x=0, y=1.0, xanchor="left", yanchor="bottom",
            bgcolor="#f3f5f8", activecolor="#dbe7f7", bordercolor="#e4e7ec", borderwidth=1,
            font=dict(size=11, color=TEXTE),
        )
    )
    fig.update_layout(margin=dict(t=44))
    return _axe_dates(fig)


# ======================================================================
# Onglet "Vue d'ensemble"
# ======================================================================
def fig_valeur_et_apports(histo):
    """Valeur du portefeuille et argent investi au fil du temps."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=histo.index, y=histo["apports_nets"], name="Argent investi (apports nets)",
        mode="lines", line=dict(color=ORANGE, width=2, shape="hv"),
        hovertemplate="%{y:,.0f} €<extra>Investi</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=histo.index, y=histo["valeur"], name="Valeur du portefeuille",
        mode="lines", line=dict(color=BLEU, width=2.5),
        fill="tonexty", fillcolor="rgba(42, 120, 214, 0.08)",
        hovertemplate="%{y:,.0f} €<extra>Valeur</extra>",
    ))
    _style(fig, hauteur=440)
    fig.update_layout(hovermode="x unified")
    fig.update_yaxes(ticksuffix=" €", tickformat=",.0f")
    return _selecteur_periode(fig)


def fig_repartition(positions, max_lignes=15):
    """Poids de chaque ligne (barres horizontales). Au-delà de 15 lignes,
    les plus petites sont regroupées dans "Autres" pour rester lisible."""
    tableau = positions.sort_values("poids_pct", ascending=False)[["nom", "poids_pct", "valeur"]]
    if len(tableau) > max_lignes:
        reste = tableau.iloc[max_lignes - 1:]
        tableau = tableau.iloc[:max_lignes - 1].copy()
        tableau.loc["Autres"] = [f"Autres ({len(reste)} lignes)", reste["poids_pct"].sum(), reste["valeur"].sum()]
    tableau = tableau.iloc[::-1]                       # la plus grosse en haut
    fig = go.Figure(go.Bar(
        x=tableau["poids_pct"], y=tableau["nom"], orientation="h",
        marker=dict(color=[GRIS if str(n).startswith("Autres") else BLEU for n in tableau["nom"]],
                    cornerradius=4),
        text=tableau["poids_pct"].map(lambda v: f"{v:.1f} %".replace(".", ",")),
        textposition="outside", cliponaxis=False,
        customdata=tableau["valeur"],
        hovertemplate="%{y}<br>%{customdata:,.0f} € — %{x:.1f} %<extra></extra>",
    ))
    _style(fig, hauteur=max(300, 30 * len(tableau) + 60), legende=False)
    fig.update_xaxes(visible=False, range=[0, tableau["poids_pct"].max() * 1.2])
    fig.update_yaxes(showgrid=False)
    return fig


def fig_repartition_groupes(positions, colonne):
    """Poids par groupe (région ou secteur), en barres horizontales."""
    groupes = positions.groupby(colonne)["poids_pct"].sum().sort_values()
    fig = go.Figure(go.Bar(
        x=groupes.values, y=groupes.index, orientation="h",
        marker=dict(color=BLEU, cornerradius=4),
        text=[f"{v:.1f} %".replace(".", ",") for v in groupes.values],
        textposition="outside", cliponaxis=False,
        hovertemplate="%{y} : %{x:.1f} %<extra></extra>",
    ))
    _style(fig, hauteur=max(260, 30 * len(groupes) + 50), legende=False)
    fig.update_xaxes(visible=False, range=[0, groupes.max() * 1.2])
    fig.update_yaxes(showgrid=False)
    return fig


# ======================================================================
# Onglet "Positions"
# ======================================================================
def fig_plus_values(positions):
    """Plus-value latente de chaque ligne, en euros (vert = gain, rouge = perte)."""
    tableau = positions.sort_values("pv_latente")
    couleurs = [VERT if v >= 0 else ROUGE for v in tableau["pv_latente"]]
    fig = go.Figure(go.Bar(
        x=tableau["pv_latente"], y=tableau["nom"], orientation="h",
        marker=dict(color=couleurs, cornerradius=4),
        customdata=tableau["pv_latente_pct"],
        hovertemplate="%{y}<br>%{x:+,.0f} € (%{customdata:+.1f} %)<extra></extra>",
    ))
    _style(fig, hauteur=max(300, (32 if len(tableau) <= 20 else 20) * len(tableau) + 60), legende=False)
    fig.update_xaxes(ticksuffix=" €", tickformat=",.0f", showgrid=True, gridcolor=GRILLE,
                     zeroline=True, zerolinecolor=GRIS)
    return fig


# ======================================================================
# Onglet "Performance"
# ======================================================================
def fig_comparaison_indice(avances, nom_indice):
    """Portefeuille et indice de référence, en base 100."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=avances["indice_reference"].index, y=avances["indice_reference"],
        name=nom_indice, mode="lines", line=dict(color=GRIS_FONCE, width=1.8),
        hovertemplate="%{y:.1f}<extra>Indice</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=avances["indice_portefeuille"].index, y=avances["indice_portefeuille"],
        name="Mon portefeuille", mode="lines", line=dict(color=BLEU, width=2.5),
        hovertemplate="%{y:.1f}<extra>Portefeuille</extra>",
    ))
    fig.add_hline(y=100, line=dict(color=GRIS, width=1, dash="dash"))
    _style(fig, hauteur=440)
    fig.update_layout(hovermode="x unified")
    return _selecteur_periode(fig)


def fig_drawdown(indicateurs):
    """Baisse par rapport au dernier plus haut."""
    dd = indicateurs["drawdown"]
    fig = go.Figure(go.Scatter(
        x=dd.index, y=dd, mode="lines", name="Drawdown",
        line=dict(color=ROUGE, width=1.5), fill="tozeroy", fillcolor="rgba(208, 59, 59, 0.2)",
        hovertemplate="%{y:.1%}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=[indicateurs["date_creux"]], y=[indicateurs["max_drawdown"]], mode="markers+text",
        marker=dict(color=ROUGE, size=10, line=dict(color="white", width=2)),
        text=[f"Max drawdown : {indicateurs['max_drawdown']:.1%}".replace(".", ",")],
        textposition="bottom center", hoverinfo="skip",
    ))
    _style(fig, hauteur=300, legende=False)
    fig.update_yaxes(tickformat=".0%")
    return _axe_dates(fig)


def fig_rendements_annuels(indicateurs, avances, nom_indice):
    """Rendement de chaque année civile : portefeuille et indice côte à côte."""
    annees_p = indicateurs["rendements_annuels"]
    annees_i = avances["rendements_annuels_indice"]
    fig = go.Figure()
    for serie, nom, couleur in [(annees_p, "Mon portefeuille", BLEU),
                                (annees_i, nom_indice, GRIS_FONCE)]:
        fig.add_trace(go.Bar(
            x=[str(a) for a in serie.index], y=serie, name=nom,
            marker=dict(color=couleur, cornerradius=4),
            text=[f"{v:+.1%}".replace(".", ",") for v in serie],
            textposition="outside", cliponaxis=False,
            hovertemplate="%{x} : %{y:+.2%}<extra>" + nom + "</extra>",
        ))
    _style(fig, hauteur=360)
    fig.update_layout(barmode="group", bargap=0.3, bargroupgap=0.08)
    fig.update_yaxes(tickformat=".0%", zeroline=True, zerolinecolor=GRIS)
    return fig


# ======================================================================
# Onglet "Risque"
# ======================================================================
def fig_distribution_rendements(indicateurs, avances, niveau_var):
    """Histogramme des rendements quotidiens, avec la VaR et la CVaR."""
    r = indicateurs["rendements"]
    fig = go.Figure(go.Histogram(
        x=r, nbinsx=70, marker=dict(color=BLEU, line=dict(color="white", width=1)),
        hovertemplate="Rendement %{x:.2%}<br>%{y} jours<extra></extra>",
        name="Jours",
    ))
    niveau = f"{niveau_var:.0%}"
    fig.add_vline(x=-avances["var_historique"], line=dict(color=ORANGE, width=2, dash="dash"),
                  annotation_text=f"VaR {niveau}", annotation_position="top left",
                  annotation_font_color=ORANGE)
    fig.add_vline(x=-avances["cvar"], line=dict(color=ROUGE, width=2, dash="dot"),
                  annotation_text="CVaR", annotation_position="bottom left",
                  annotation_font_color=ROUGE)
    _style(fig, hauteur=380, legende=False)
    fig.update_xaxes(tickformat=".1%", title_text="Rendement quotidien")
    fig.update_yaxes(title_text="Nombre de jours")
    return fig


def fig_correlations(matrice):
    """Carte de chaleur des corrélations (bleu = négative, rouge = positive)."""
    valeurs = matrice.round(2) + 0.0          # + 0.0 évite l'affichage « -0.00 »
    fig = go.Figure(go.Heatmap(
        z=valeurs.values, x=list(valeurs.columns), y=list(valeurs.index),
        zmin=-1, zmax=1,
        colorscale=[[0, "#184f95"], [0.5, "#f0efec"], [1, "#b52f2f"]],
        text=valeurs.values, texttemplate="%{text:.2f}" if len(valeurs) <= 15 else "",
        textfont=dict(size=11 if len(valeurs) <= 8 else 9),
        xgap=2, ygap=2,
        hovertemplate="%{y} / %{x} : %{z:.2f}<extra></extra>",
        colorbar=dict(thickness=12, outlinewidth=0),
    ))
    _style(fig, hauteur=min(max(380, 38 * len(valeurs) + 120), 760), legende=False)
    petite = dict(size=9) if len(valeurs) > 20 else dict(size=11)
    fig.update_yaxes(autorange="reversed", showgrid=False, tickfont=petite)
    fig.update_xaxes(showgrid=False, tickangle=-45, tickfont=petite)
    return fig


# ======================================================================
# Onglet "Optimisation" (étape 7)
# ======================================================================
AQUA = "#1baf7a"            # variance minimale
VERT_FONCE = "#008300"      # Sharpe maximal


def fig_frontiere(opti):
    """Nuage des portefeuilles possibles, frontière efficiente et points clés."""
    alea, front, seuls = opti["aleatoires"], opti["frontiere"], opti["titres_seuls"]
    fig = go.Figure()

    # Nuage de portefeuilles aléatoires, coloré selon le Sharpe
    fig.add_trace(go.Scatter(
        x=alea["volatilite"], y=alea["rendement"], mode="markers", name="Portefeuilles aléatoires",
        marker=dict(size=4, color=alea["sharpe"], opacity=0.55,
                    colorscale=[[0, "#cde2fb"], [1, "#0d366b"]],
                    colorbar=dict(title=dict(text="Sharpe"), thickness=12, outlinewidth=0)),
        hovertemplate="Volatilité %{x:.1%}<br>Rendement %{y:.1%}<extra></extra>",
    ))
    # Droite de marché des capitaux
    rf, tangent = opti["taux_sans_risque"], opti["sharpe_max"]
    vmax = front["volatilite"].max() * 1.05
    pente = (tangent["rendement"] - rf) / tangent["volatilite"]
    fig.add_trace(go.Scatter(
        x=[0, vmax], y=[rf, rf + pente * vmax], mode="lines", name="Droite de marché des capitaux",
        line=dict(color=GRIS, width=1.5, dash="dash"), hoverinfo="skip",
    ))
    # Frontière efficiente
    fig.add_trace(go.Scatter(
        x=front["volatilite"], y=front["rendement"], mode="lines", name="Frontière efficiente",
        line=dict(color=TEXTE, width=3),
        hovertemplate="Volatilité %{x:.1%}<br>Rendement %{y:.1%}<extra>Frontière</extra>",
    ))
    # Titres seuls
    fig.add_trace(go.Scatter(
        x=seuls["volatilite"], y=seuls["rendement"],
        mode="markers+text" if len(seuls) <= 20 else "markers", name="Titres seuls",
        marker=dict(color=GRIS, size=7), text=list(seuls.index), textposition="top right",
        textfont=dict(size=9, color=GRIS), customdata=seuls["nom"],
        hovertemplate="%{customdata}<br>Volatilité %{x:.1%}<br>Rendement %{y:.1%}<extra></extra>",
    ))
    # Les trois portefeuilles comparés
    for cle, nom, couleur, symbole, taille in [("actuel", "Mon portefeuille", ORANGE, "circle", 15),
                                               ("variance_min", "Variance minimale", AQUA, "diamond", 15),
                                               ("sharpe_max", "Sharpe maximal", VERT_FONCE, "star", 20)]:
        p = opti[cle]
        fig.add_trace(go.Scatter(
            x=[p["volatilite"]], y=[p["rendement"]], mode="markers",
            name=f"{nom} (Sharpe {p['sharpe']:.2f})".replace(".", ","),
            marker=dict(color=couleur, size=taille, symbol=symbole, line=dict(color="white", width=2)),
            hovertemplate=f"<b>{nom}</b><br>Volatilité %{{x:.1%}}<br>Rendement %{{y:.1%}}<extra></extra>",
        ))
    _style(fig, hauteur=560)
    fig.update_xaxes(tickformat=".0%", title_text="Volatilité annuelle", rangemode="tozero",
                     showgrid=True, gridcolor=GRILLE)
    fig.update_yaxes(tickformat=".0%", title_text="Rendement annuel espéré")
    return fig


def fig_poids(opti):
    """Poids actuels, de variance minimale et de Sharpe maximal, titre par titre."""
    poids = opti["poids"]
    if len(poids) > 25:   # beaucoup de titres : on garde les 25 lignes les plus importantes
        importance = poids[["actuel", "variance_min", "sharpe_max"]].max(axis=1)
        poids = poids.loc[importance.sort_values(ascending=False).index[:25]]
    poids = poids.sort_values("actuel")
    fig = go.Figure()
    for colonne, nom, couleur in [("actuel", "Mon portefeuille", ORANGE),
                                  ("variance_min", "Variance minimale", AQUA),
                                  ("sharpe_max", "Sharpe maximal", VERT_FONCE)]:
        fig.add_trace(go.Bar(
            x=poids[colonne], y=poids["nom"], orientation="h", name=nom,
            marker=dict(color=couleur, cornerradius=3),
            hovertemplate="%{y} : %{x:.1%}<extra>" + nom + "</extra>",
        ))
    _style(fig, hauteur=max(360, 48 * len(poids) + 80))
    fig.update_layout(barmode="group", bargap=0.25, bargroupgap=0.05)
    fig.update_xaxes(tickformat=".0%", showgrid=True, gridcolor=GRILLE)
    fig.update_yaxes(showgrid=False)
    return fig


# ======================================================================
# Onglet "Projection" (étape 8)
# ======================================================================
def fig_projection(sim):
    """Éventail des trajectoires simulées (Monte-Carlo)."""
    t = sim["trajectoires"]
    fig = go.Figure()
    # Zone des 90 % : on trace le bas (invisible) puis le haut rempli jusqu'au bas.
    fig.add_trace(go.Scatter(x=t.index, y=t["p5"], mode="lines", line=dict(width=0),
                             showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=t.index, y=t["p95"], mode="lines", line=dict(width=0),
                             fill="tonexty", fillcolor="rgba(42, 120, 214, 0.12)",
                             name="90 % des scénarios", hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=t.index, y=t["p25"], mode="lines", line=dict(width=0),
                             showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=t.index, y=t["p75"], mode="lines", line=dict(width=0),
                             fill="tonexty", fillcolor="rgba(42, 120, 214, 0.28)",
                             name="50 % des scénarios", hoverinfo="skip"))
    fig.add_trace(go.Scatter(
        x=t.index, y=t["apports"], mode="lines", name="Argent investi",
        line=dict(color=ORANGE, width=2, dash="dash"),
        hovertemplate="%{y:,.0f} €<extra>Investi</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=t.index, y=t["p50"], mode="lines", name="Scénario médian",
        line=dict(color=BLEU, width=3),
        customdata=t[["p5", "p95"]].to_numpy(),
        hovertemplate="Médiane %{y:,.0f} €<br>Fourchette 90 % : %{customdata[0]:,.0f} – "
                      "%{customdata[1]:,.0f} €<extra></extra>",
    ))
    if sim.get("objectif"):
        fig.add_hline(y=sim["objectif"], line=dict(color=GRIS_FONCE, width=1, dash="dot"),
                      annotation_text="Objectif", annotation_position="top left",
                      annotation_font_color=GRIS_FONCE)
    _style(fig, hauteur=460)
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(tickformat="%Y", hoverformat="%m/%Y")
    fig.update_yaxes(ticksuffix=" €", tickformat=",.0f")
    return fig


def fig_distribution_finale(sim):
    """Histogramme de la valeur finale des scénarios."""
    finales = sim["valeurs_finales"]
    fig = go.Figure(go.Histogram(
        x=finales, nbinsx=60, marker=dict(color=BLEU, line=dict(color="white", width=1)),
        hovertemplate="%{x:,.0f} €<br>%{y} scénarios<extra></extra>",
    ))
    fig.add_vline(x=sim["total_apporte"], line=dict(color=ORANGE, width=2, dash="dash"),
                  annotation_text="Investi", annotation_position="top right",
                  annotation_font_color=ORANGE)
    fig.add_vline(x=sim["mediane"], line=dict(color=TEXTE, width=2),
                  annotation_text="Médiane", annotation_position="top left",
                  annotation_font_color=TEXTE)
    _style(fig, hauteur=320, legende=False)
    fig.update_xaxes(ticksuffix=" €", tickformat=",.0f", title_text="Valeur finale")
    fig.update_yaxes(title_text="Nombre de scénarios")
    return fig


# Couleurs des tranches de probabilité : rouge (défavorable) -> gris -> bleu (favorable)
COULEURS_TRANCHES = ["#a32020", "#e0797b", "#a3a39e", "#5598e7", "#184f95"]


def fig_projection_nuage(sim):
    """Nuage de points : chaque point est UN scénario à une date donnée,
    coloré selon sa tranche de probabilité à cette date."""
    t = sim["trajectoires"]
    points = points_nuage(sim)
    fig = go.Figure()
    for numero, (nom, couleur) in enumerate(zip(TRANCHES, COULEURS_TRANCHES)):
        tranche = points[points["tranche"] == numero]
        fig.add_trace(go.Scatter(
            x=tranche["date"], y=tranche["valeur"], mode="markers", name=nom,
            marker=dict(color=couleur, size=6, opacity=0.75, line=dict(color="white", width=0.5)),
            customdata=list(zip(tranche["date_reelle"].dt.strftime("%m/%Y"), tranche["scenario"])),
            hovertemplate="Scénario n° %{customdata[1]} · %{customdata[0]}<br>%{y:,.0f} €"
                          f"<extra>{nom}</extra>",
        ))
    # Repères : médiane, bornes à 5 % et 95 %, argent investi
    fig.add_trace(go.Scatter(x=t.index, y=t["p95"], mode="lines", name="Seuil des 95 %",
                             line=dict(color=COULEURS_TRANCHES[4], width=1.2, dash="dot"),
                             hovertemplate="95e percentile : %{y:,.0f} €<extra></extra>"))
    fig.add_trace(go.Scatter(x=t.index, y=t["p50"], mode="lines", name="Médiane",
                             line=dict(color=TEXTE, width=2.2),
                             hovertemplate="Médiane : %{y:,.0f} €<extra></extra>"))
    fig.add_trace(go.Scatter(x=t.index, y=t["p5"], mode="lines", name="Seuil des 5 %",
                             line=dict(color=COULEURS_TRANCHES[0], width=1.2, dash="dot"),
                             hovertemplate="5e percentile : %{y:,.0f} €<extra></extra>"))
    fig.add_trace(go.Scatter(x=t.index, y=t["apports"], mode="lines", name="Argent investi",
                             line=dict(color=ORANGE, width=2, dash="dash"),
                             hovertemplate="Investi : %{y:,.0f} €<extra></extra>"))
    _style(fig, hauteur=520)
    fig.update_layout(hovermode="closest")
    fig.update_xaxes(tickformat="%Y")
    fig.update_yaxes(ticksuffix=" €", tickformat=",.0f")
    return fig


# ======================================================================
# Étape 10 : conseil patrimonial et gestion d'actifs
# ======================================================================
# Couleurs catégorielles, toujours dans le même ordre
SERIES = [BLEU, ORANGE, "#1baf7a", "#eda100", "#e87ba4"]


def fig_barres_signees(valeurs, etiquettes, format_texte, hauteur=None, suffixe=""):
    """Barres horizontales : vert si positif, rouge si négatif (pertes, effets...)."""
    couleurs = [VERT if v >= 0 else ROUGE for v in valeurs]
    fig = go.Figure(go.Bar(
        x=list(valeurs), y=list(etiquettes), orientation="h",
        marker=dict(color=couleurs, cornerradius=4),
        text=[format_texte(v) for v in valeurs], textposition="outside", cliponaxis=False,
        hovertemplate="%{y} : %{text}<extra></extra>",
    ))
    _style(fig, hauteur=hauteur or max(260, 46 * len(valeurs) + 60), legende=False)
    ecart = max(abs(min(valeurs)), abs(max(valeurs))) * 1.35 or 1
    fig.update_xaxes(range=[-ecart if min(valeurs) < 0 else 0, ecart if max(valeurs) > 0 else 0],
                     zeroline=True, zerolinecolor=GRIS, showgrid=True, gridcolor=GRILLE, ticksuffix=suffixe)
    fig.update_yaxes(autorange="reversed", showgrid=False)
    return fig


def fig_lignes(tableau, format_y=",.0f", suffixe="", hauteur=420, base100=False):
    """Plusieurs courbes (une par colonne), couleurs dans l'ordre fixe."""
    fig = go.Figure()
    for i, colonne in enumerate(tableau.columns):
        serie = tableau[colonne].dropna()
        if base100:
            serie = 100 * serie / serie.iloc[0]
        fig.add_trace(go.Scatter(
            x=serie.index, y=serie, mode="lines", name=str(colonne),
            line=dict(color=SERIES[i % len(SERIES)], width=2.4 if i == 0 else 1.8),
            hovertemplate=f"%{{y:{format_y}}}{suffixe}<extra>{colonne}</extra>",
        ))
    _style(fig, hauteur=hauteur)
    fig.update_layout(hovermode="x unified")
    fig.update_yaxes(tickformat=format_y, ticksuffix=suffixe)
    return _axe_dates(fig)


def fig_fiscalite_horizon(tableau):
    """Gain net selon l'année de sortie, pour chaque enveloppe (une courbe par enveloppe)."""
    fig = go.Figure()
    for i, colonne in enumerate(tableau.columns):
        fig.add_trace(go.Scatter(
            x=tableau.index, y=tableau[colonne], mode="lines+markers", name=colonne,
            line=dict(color=SERIES[i], width=2.2, shape="hv" if colonne != "CTO" else "linear"),
            marker=dict(size=5),
            hovertemplate="Sortie dans %{x} an(s) : %{y:,.0f} €<extra>" + colonne + "</extra>",
        ))
    _style(fig, hauteur=380)
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(title_text="Années avant la sortie", dtick=2)
    fig.update_yaxes(ticksuffix=" €", tickformat=",.0f", title_text="Gain net d'impôts")
    return fig


def fig_poids_et_risque(par_ligne, max_lignes=20):
    """Pour chaque ligne : sa part de la valeur et sa part du risque."""
    t = par_ligne.head(max_lignes).iloc[::-1]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=t["poids"], y=t["nom"], orientation="h", name="Part de la valeur",
                         marker=dict(color="#b8c4d6", cornerradius=3),
                         hovertemplate="%{y} : %{x:.1%} de la valeur<extra></extra>"))
    fig.add_trace(go.Bar(x=t["part_risque"], y=t["nom"], orientation="h", name="Part du risque",
                         marker=dict(color=BLEU, cornerradius=3),
                         hovertemplate="%{y} : %{x:.1%} du risque<extra></extra>"))
    _style(fig, hauteur=max(360, 40 * len(t) + 80))
    fig.update_layout(barmode="group", bargap=0.25, bargroupgap=0.05)
    fig.update_xaxes(tickformat=".0%", showgrid=True, gridcolor=GRILLE)
    fig.update_yaxes(showgrid=False)
    return fig


def fig_effets_attribution(par_region):
    """Effets d'allocation, de sélection et d'interaction par région (barres groupées)."""
    fig = go.Figure()
    for i, (colonne, nom) in enumerate([("allocation", "Allocation"), ("selection", "Sélection"),
                                        ("interaction", "Interaction")]):
        fig.add_trace(go.Bar(
            x=par_region.index, y=par_region[colonne], name=nom,
            marker=dict(color=SERIES[i], cornerradius=3),
            hovertemplate="%{x} : %{y:+.2%}<extra>" + nom + "</extra>",
        ))
    _style(fig, hauteur=400)
    fig.update_layout(barmode="group", bargap=0.25)
    fig.update_yaxes(tickformat=".1%", zeroline=True, zerolinecolor=GRIS)
    return fig
