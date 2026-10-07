"""
graphiques_interactifs.py — Les graphiques du tableau de bord (Plotly).

Différence avec graphiques.py (matplotlib) :
    matplotlib produit des IMAGES fixes (pour un rapport PDF) ;
    Plotly produit des graphiques INTERACTIFS : survol à la souris, zoom,
    choix de la période, masquage d'une courbe en cliquant sur la légende.

Chaque fonction reçoit des données et renvoie une "figure" Plotly, que
app.py affiche avec st.plotly_chart().
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from .langues import anglais, eur, espace_pct, t, td
from .simulation import TRANCHES, points_nuage

_t = t      # alias : dans certaines fonctions, "t" désigne un tableau de données

# Mêmes couleurs que les graphiques matplotlib, pour la cohérence visuelle.
BLEU = "#2a78d6"        # le portefeuille
ORANGE = "#eb6834"      # l'argent investi
GRIS_FONCE = "#5f5e5a"  # l'indice de référence
GRIS = "#898781"        # axes, textes secondaires
GRILLE = "#e1e0d9"
ROUGE = "#d03b3b"       # pertes, baisses
VERT = "#0ca30c"        # gains
TEXTE = "#1a1a19"
VIOLET = "#7a4fb5"     # VaR Cornish-Fisher


# ======================================================================
# Réglages communs
# ======================================================================
POLICE = "Inter, 'Segoe UI', Roboto, Arial, sans-serif"

# Options de la barre d'outils Plotly (à passer à st.plotly_chart(config=...)) :
# on retire le logo Plotly et les outils de sélection peu utiles.
# La barre d'outils est masquée : elle recouvrait le haut des graphiques. Le zoom
# reste possible (cliquer-glisser) et un double-clic revient à la vue d'origine.
CONFIG_PLOTLY = {
    "displayModeBar": False,
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
        # virgule décimale et espace pour les milliers (à la française), ou l'inverse en anglais
        separators=".," if anglais() else ", ",
    )
    fig.update_xaxes(showgrid=False, linecolor=GRILLE, tickfont=dict(color=GRIS, size=11))
    fig.update_yaxes(gridcolor="#eef0f3", zeroline=False, tickfont=dict(color=GRIS, size=11))
    return fig


def _axe_dates(fig):
    """Dates au format français (pas de noms de mois en anglais), ou anglais."""
    if anglais():
        fig.update_xaxes(tickformat="%b %Y", hoverformat="%d %b %Y")
    else:
        fig.update_xaxes(tickformat="%m/%Y", hoverformat="%d/%m/%Y")
    return fig


def _lire(objet, cle):
    """Attribut d'un objet Plotly (ou clé d'un dictionnaire), ou None."""
    try:
        return objet[cle]
    except Exception:
        return getattr(objet, cle, None)


def _ecrire(objet, cle, valeur):
    try:
        objet[cle] = valeur
    except Exception:
        setattr(objet, cle, valeur)


def _couleur_nuit(couleur):
    from .theme import REMPLACEMENTS_NUIT
    if isinstance(couleur, str):
        return REMPLACEMENTS_NUIT.get(couleur.lower(), couleur)
    if isinstance(couleur, (list, tuple)):
        return [_couleur_nuit(c) for c in couleur]
    return couleur


def theme_figure(fig):
    """Adapte un graphique au mode nuit (texte, grilles, bulles, couleurs sombres des courbes).
    Sans effet en mode clair. Appelé juste avant l'affichage (st.plotly_chart)."""
    from . import theme
    if not theme.nuit():
        return fig
    c = theme.NUIT
    fig.update_layout(font=dict(color=c["texte_2"]), legend=dict(font=dict(color=c["texte_2"])),
                      hoverlabel=dict(bgcolor=c["carte"], bordercolor=c["bordure"], font=dict(color=c["texte"])),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig.update_xaxes(gridcolor=c["grille"], linecolor=c["bordure"], zerolinecolor=c["bordure"],
                     tickfont=dict(color=c["texte_3"]), title_font=dict(color=c["texte_3"]))
    fig.update_yaxes(gridcolor=c["grille"], linecolor=c["bordure"], zerolinecolor=c["bordure"],
                     tickfont=dict(color=c["texte_3"]), title_font=dict(color=c["texte_3"]))
    for trace in fig.data:
        echelle = _lire(trace, "colorscale")
        if echelle is not None and not isinstance(echelle, str):
            try:
                _ecrire(trace, "colorscale", [[pos, _couleur_nuit(coul)] for pos, coul in echelle])
            except Exception:
                pass
        for partie in ("line", "marker", "textfont", "insidetextfont", "outsidetextfont"):
            element = _lire(trace, partie)
            if element is None:
                continue
            couleur = _lire(element, "color")
            if couleur is not None:
                _ecrire(element, "color", _couleur_nuit(couleur))
            echelle = _lire(element, "colorscale") if partie == "marker" else None
            if echelle is not None and not isinstance(echelle, str):
                try:
                    _ecrire(element, "colorscale", [[pos, _couleur_nuit(coul)] for pos, coul in echelle])
                except Exception:
                    pass
            contour = _lire(element, "line")
            if contour is not None and _lire(contour, "color") is not None:
                _ecrire(contour, "color", _couleur_nuit(_lire(contour, "color")))
    if hasattr(fig, "layout"):
        try:
            for annotation in fig.layout.annotations or ():
                if annotation.font and annotation.font.color:
                    annotation.font.color = _couleur_nuit(annotation.font.color)
                elif annotation.font is not None:
                    annotation.font.color = c["texte_2"]
            for forme in fig.layout.shapes or ():
                if forme.line and forme.line.color:
                    forme.line.color = _couleur_nuit(forme.line.color)
            if any(type(trace).__name__ in ("Choropleth", "Scattergeo") for trace in fig.data):   # carte du monde
                fig.update_geos(bgcolor="rgba(0,0,0,0)", landcolor="#1d2e47", showframe=False)
        except Exception:
            pass
    return fig


def _axe_euros(axe):
    """Montants en euros sur un axe : '1 000 €' ou '€1,000'."""
    return dict(tickprefix="€") if anglais() else dict(ticksuffix=" €")


def _p(valeur, decimales=1, signe=False):
    """Pourcentage (valeur déjà en %) pour un texte de barre : '12,3 %' ou '12.3%'."""
    texte = f"{valeur:+.{decimales}f}" if signe else f"{valeur:.{decimales}f}"
    return texte + "%" if anglais() else texte.replace(".", ",") + " %"


def _selecteur_periode(fig):
    """Ajoute des boutons 1M / 6M / YTD / 1A / Tout au-dessus d'un graphique."""
    fig.update_xaxes(
        rangeselector=dict(
            buttons=[
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label=t("1A"), step="year", stepmode="backward"),
                dict(step="all", label=t("Tout")),
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
        x=histo.index, y=histo["apports_nets"], name=t("Argent investi (apports nets)"),
        mode="lines", line=dict(color=ORANGE, width=2, shape="hv"),
        hovertemplate=eur("%{y:,.0f}") + f"<extra>{t('Investi')}</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=histo.index, y=histo["valeur"], name=t("Valeur du portefeuille"),
        mode="lines", line=dict(color=BLEU, width=2.5),
        fill="tonexty", fillcolor="rgba(42, 120, 214, 0.08)",
        hovertemplate=eur("%{y:,.0f}") + f"<extra>{t('Valeur')}</extra>",
    ))
    _style(fig, hauteur=440)
    fig.update_layout(hovermode="x unified")
    fig.update_yaxes(tickformat=",.0f", **_axe_euros("y"))
    return _selecteur_periode(fig)


def fig_repartition(positions, max_lignes=15):
    """Poids de chaque ligne (barres horizontales). Au-delà de 15 lignes,
    les plus petites sont regroupées dans "Autres" pour rester lisible."""
    tableau = positions.sort_values("poids_pct", ascending=False)[["nom", "poids_pct", "valeur"]]
    if len(tableau) > max_lignes:
        reste = tableau.iloc[max_lignes - 1:]
        tableau = tableau.iloc[:max_lignes - 1].copy()
        tableau.loc["Autres"] = [t("Autres ({n} lignes)", n=len(reste)), reste["poids_pct"].sum(),
                                 reste["valeur"].sum()]
    tableau = tableau.iloc[::-1]                       # la plus grosse en haut
    fig = go.Figure(go.Bar(
        x=tableau["poids_pct"], y=tableau["nom"], orientation="h",
        marker=dict(color=[GRIS if n == tableau["nom"].get("Autres") else BLEU for n in tableau["nom"]],
                    cornerradius=4),
        text=tableau["poids_pct"].map(_p),
        textposition="outside", cliponaxis=False,
        customdata=tableau["valeur"],
        hovertemplate="%{y}<br>" + eur("%{customdata:,.0f}") + f" — %{{x:.1f}}{espace_pct()}%<extra></extra>",
    ))
    _style(fig, hauteur=max(300, 30 * len(tableau) + 60), legende=False)
    fig.update_layout(margin=dict(r=16))
    fig.update_xaxes(visible=False, range=[0, tableau["poids_pct"].max() * 1.35])
    fig.update_yaxes(showgrid=False)
    return fig


# Palette des anneaux : bleus du thème, puis couleurs bien distinctes
PALETTE_ANNEAU = ["#1c5cab", "#6ea3e0", "#0f2a4a", "#e8a33d", "#3aa17e", "#c4543a", "#8e7cc3", "#4fb3bf",
                  "#d4b483", "#b8c4d6", "#9aa5b1"]
GRIS_CLAIR = "#c9cdd3"


def fig_anneau(poids, valeur_totale=None, seuil_autres=0.03, max_parts=8, hauteur=330):
    """Répartition en anneau (camembert évidé).

    poids : Series groupe -> fraction (total ≈ 1). Les parts sous `seuil_autres`
    (ou au-delà de `max_parts`) sont regroupées dans « Autres »."""
    poids = poids[poids > 0].sort_values(ascending=False)
    grandes = poids[poids >= seuil_autres].head(max_parts)
    petites = poids.drop(grandes.index)
    etiquettes = [td(g) for g in grandes.index]
    valeurs = list(grandes.values)
    couleurs = PALETTE_ANNEAU[:len(grandes)]
    if petites.sum() > 0:
        etiquettes.append(t("Autres ({n})", n=len(petites)))
        valeurs.append(float(petites.sum()))
        couleurs.append(GRIS_CLAIR)
    montants = [eur(f"{v * valeur_totale:,.0f}").replace(",", " " if not anglais() else ",")
                if valeur_totale else "" for v in valeurs]
    fig = go.Figure(go.Pie(
        labels=etiquettes, values=valeurs, hole=0.58, sort=False, direction="clockwise", rotation=90,
        marker=dict(colors=couleurs, line=dict(color="white", width=2)),
        textinfo="percent", textposition="inside", insidetextorientation="horizontal",
        texttemplate="%{percent:.0%}", textfont=dict(color="white", size=12),
        customdata=montants,
        hovertemplate="<b>%{label}</b><br>%{percent:.1%}" + (" · %{customdata}" if valeur_totale else "")
                      + "<extra></extra>",
    ))
    _style(fig, hauteur=hauteur)
    fig.update_layout(uniformtext=dict(minsize=10, mode="hide"), margin=dict(l=4, r=4, t=8, b=8),
                      legend=dict(orientation="v", y=0.5, yanchor="middle", x=1.02, xanchor="left",
                                  font=dict(size=12, color="#5f5e5a")))
    return fig


def fig_repartition_groupes(positions, colonne):
    """Poids par groupe (classe d'actifs, région, secteur), en anneau."""
    groupes = positions.groupby(colonne)["valeur"].sum()
    return fig_anneau(groupes / groupes.sum(), positions["valeur"].sum())


# Bleus de la carte : du plus clair (faible poids) au plus foncé (fort poids)
ECHELLE_CARTE = [[0, "#e3edf9"], [0.15, "#a9c8ee"], [0.4, "#5b93d6"], [0.7, "#1c5cab"], [1, "#0f2a4a"]]


def fig_carte_monde(carte, geojson=None, hauteur=430):
    """Carte du monde : chaque pays coloré selon son poids dans la poche actions.

    carte   : tableau de expositions.carte_pays (pays, iso3, poids, valeur, nb_titres, titres)
    geojson : contours des pays (fond_de_carte.py) ; sans eux, Plotly télécharge
              le fond de carte (la carte ne s'affiche alors qu'avec Internet)."""
    fig = go.Figure()
    noms = [td(p) for p in carte["pays"]]
    titres = ["<br>".join(["· " + n for n in liste[:6]] + ([_t("… et {n} autre(s)", n=len(liste) - 6)]
                                                           if len(liste) > 6 else []))
              for liste in carte["titres"]]
    montants = [eur(f"{v:,.0f}").replace(",", " " if not anglais() else ",") for v in carte["valeur"]]
    donnees = [[n, m, k, ti] for n, m, k, ti in zip(noms, montants, carte["nb_titres"], titres)]
    survol = ("<b>%{customdata[0]}</b><br>" + _t("%{z:.1%} de la poche actions") + " · %{customdata[1]}<br>"
              + _t("%{customdata[2]} titre(s)") + "<br>%{customdata[3]}<extra></extra>")
    zmax = float(carte["poids"].max()) if len(carte) else 1.0
    if geojson is not None:
        detenus = set(carte["iso3"])
        autres = [f["id"] for f in geojson["features"] if f["id"] not in detenus]
        fig.add_trace(go.Choropleth(              # pays sans exposition, en gris clair
            geojson=geojson, locations=autres, z=[0] * len(autres), showscale=False,
            colorscale=[[0, "#eceef1"], [1, "#eceef1"]], marker=dict(line=dict(color="white", width=0.5)),
            hoverinfo="skip"))
        fig.add_trace(go.Choropleth(
            geojson=geojson, locations=carte["iso3"], z=carte["poids"], zmin=0, zmax=zmax,
            colorscale=ECHELLE_CARTE, marker=dict(line=dict(color="white", width=0.6)),
            customdata=donnees, hovertemplate=survol,
            colorbar=dict(thickness=10, len=0.6, outlinewidth=0, tickformat=".0%", x=1.0)))
        fig.update_geos(visible=False)
    else:
        fig.add_trace(go.Choropleth(
            locations=carte["iso3"], locationmode="ISO-3", z=carte["poids"], zmin=0, zmax=zmax,
            colorscale=ECHELLE_CARTE, marker=dict(line=dict(color="white", width=0.6)),
            customdata=donnees, hovertemplate=survol,
            colorbar=dict(thickness=10, len=0.6, outlinewidth=0, tickformat=".0%", x=1.0)))
        fig.update_geos(showcountries=True, countrycolor="white", showland=True, landcolor="#eceef1",
                        showcoastlines=False, showocean=False, showlakes=False)
    fig.update_geos(projection_type="natural earth", showframe=False, bgcolor="rgba(0,0,0,0)",
                    lataxis_range=[-57, 84])
    _style(fig, hauteur=hauteur, legende=False)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), dragmode=False)
    return fig


def fig_comparaison(tableau, col_a, col_b, nom_a, nom_b, max_lignes=12, format_x=".0%", hauteur=None):
    """Deux barres par ligne (ex. portefeuille / indice, part de la valeur / part du risque)."""
    t = tableau.head(max_lignes).iloc[::-1]
    etiquettes = [td(x) for x in t.index]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=t[col_b], y=etiquettes, orientation="h", name=nom_b,
                         marker=dict(color="#b8c4d6", cornerradius=3),
                         hovertemplate="%{y} : %{x:" + format_x.replace("0", "1") + "}<extra>" + nom_b + "</extra>"))
    fig.add_trace(go.Bar(x=t[col_a], y=etiquettes, orientation="h", name=nom_a,
                         marker=dict(color="#1c5cab", cornerradius=3),
                         hovertemplate="%{y} : %{x:" + format_x.replace("0", "1") + "}<extra>" + nom_a + "</extra>"))
    _style(fig, hauteur=hauteur or max(300, 34 * len(t) + 90))
    fig.update_layout(barmode="group", bargap=0.28, bargroupgap=0.06,
                      legend=dict(traceorder="reversed", y=-0.08))
    fig.update_xaxes(tickformat=format_x, showgrid=True, gridcolor="#eef0f3")
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
        hovertemplate="%{y}<br>" + eur("%{x:+,.0f}") + f" (%{{customdata:+.1f}}{espace_pct()}%)<extra></extra>",
    ))
    _style(fig, hauteur=max(300, (32 if len(tableau) <= 20 else 20) * len(tableau) + 60), legende=False)
    fig.update_xaxes(tickformat=",.0f", showgrid=True, gridcolor=GRILLE,
                     zeroline=True, zerolinecolor=GRIS, **_axe_euros("x"))
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
        hovertemplate=f"%{{y:.1f}}<extra>{t('Indice')}</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=avances["indice_portefeuille"].index, y=avances["indice_portefeuille"],
        name=t("Mon portefeuille"), mode="lines", line=dict(color=BLEU, width=2.5),
        hovertemplate=f"%{{y:.1f}}<extra>{t('Portefeuille')}</extra>",
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
        text=[t("Max drawdown : {valeur}", valeur=_p(indicateurs["max_drawdown"] * 100))],
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
    for serie, nom, couleur in [(annees_p, t("Mon portefeuille"), BLEU),
                                (annees_i, nom_indice, GRIS_FONCE)]:
        fig.add_trace(go.Bar(
            x=[str(a) for a in serie.index], y=serie, name=nom,
            marker=dict(color=couleur, cornerradius=4),
            text=[_p(v * 100, signe=True) for v in serie],
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
    """Histogramme des rendements quotidiens comparé à la loi normale de même moyenne et
    même écart-type, avec les trois VaR (historique, normale, Cornish-Fisher) et la CVaR.
    Toutes les lignes ont leur entrée de légende (plus d'étiquettes posées sur les barres)."""
    from statistics import NormalDist
    r = indicateurs["rendements"].dropna()
    n = len(r)
    moyenne, ecart = float(r.mean()), float(r.std())
    # Classes de largeur fixe : nécessaire pour mettre la courbe normale à la même échelle
    bas, haut = float(r.min()), float(r.max())
    nb_classes = int(min(80, max(20, np.sqrt(n) * 1.2)))
    largeur = (haut - bas) / nb_classes if haut > bas else 0.001
    fig = go.Figure(go.Histogram(
        x=r, xbins=dict(start=bas, end=haut + largeur, size=largeur), name=_t("Jours observés"),
        marker=dict(color=BLEU, opacity=0.75, line=dict(color="white", width=0.6)),
        hovertemplate=_t("Rendement %{x:.2%}<br>%{y} jours") + "<extra></extra>",
    ))
    # Loi normale : densité × nombre de jours × largeur de classe = nombre de jours attendu par classe
    if ecart > 0:
        loi = NormalDist(moyenne, ecart)
        xs = np.linspace(bas - largeur, haut + largeur, 300)
        fig.add_trace(go.Scatter(
            x=xs, y=[loi.pdf(x) * n * largeur for x in xs], mode="lines", name=_t("Loi normale (même moyenne et volatilité)"),
            line=dict(color=TEXTE, width=2), hovertemplate=_t("Loi normale : %{y:.0f} jours attendus") + "<extra></extra>",
        ))
    # Lignes verticales (tracées comme des courbes pour figurer dans la légende)
    comptes, _ = np.histogram(r, bins=np.arange(bas, haut + 2 * largeur, largeur))
    sommet = max(comptes.max() if len(comptes) else 1, (NormalDist(moyenne, ecart).pdf(moyenne) * n * largeur) if ecart else 1)
    niveau = f"{niveau_var * 100:.0f}{espace_pct()}%"
    lignes = [("var_historique", _t("VaR historique {niveau}", niveau=niveau), ORANGE, "dash"),
              ("var_parametrique", _t("VaR loi normale {niveau}", niveau=niveau), GRIS_FONCE, "dot"),
              ("var_cornish_fisher", _t("VaR Cornish-Fisher {niveau}", niveau=niveau), VIOLET, "dashdot"),
              ("cvar", "CVaR (Expected Shortfall)", ROUGE, "solid")]
    for cle, nom, couleur, trait in lignes:
        valeur = avances.get(cle)
        if valeur is None or valeur != valeur:
            continue
        fig.add_trace(go.Scatter(
            x=[-valeur, -valeur], y=[0, sommet * 1.08], mode="lines", name=nom,
            line=dict(color=couleur, width=2, dash=trait),
            hovertemplate=f"{nom} : %{{x:.2%}}<extra></extra>",
        ))
    _style(fig, hauteur=420)
    fig.update_layout(bargap=0.04, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    marge = (haut - bas) * 0.04
    gauche = min(bas, *[-avances[c] for c, *_ in lignes if avances.get(c) == avances.get(c) and avances.get(c) is not None])
    fig.update_xaxes(tickformat=".1%", title_text=_t("Rendement quotidien"), range=[gauche - marge, haut + marge],
                     showgrid=True, gridcolor=GRILLE)
    fig.update_yaxes(title_text=_t("Nombre de jours"), rangemode="tozero")
    return fig


# Corrélations : bleu (négative) -> blanc (nulle) -> rouge brique (positive)
ECHELLE_CORRELATION = [[0, "#1c5cab"], [0.25, "#8fb6e6"], [0.5, "#f7f7f5"], [0.72, "#eaa48f"], [1, "#a8322a"]]


def _qualificatif(rho):
    a = abs(rho)
    return _t("très forte") if a >= 0.8 else _t("forte") if a >= 0.6 else _t("modérée") if a >= 0.3 else _t("faible")


def fig_correlations(matrice, ordre=None, noms=None, max_nom=16):
    """Carte des corrélations, lisible même avec 50 titres.

    - ordre : titres regroupés par blocs de titres corrélés (expositions.ordre_regroupement) ;
    - triangle inférieur seulement (l'autre moitié répète la même information), sans la
      diagonale (toujours 1) ;
    - cases carrées, valeurs écrites dans les cases jusqu'à 12 lignes ;
    - noms : dictionnaire code -> nom affiché (sinon le code)."""
    ordre = [o for o in (ordre or list(matrice.index)) if o in matrice.index]
    m = matrice.loc[ordre, ordre]
    n = len(ordre)
    noms = noms or {}
    court = lambda c: (lambda x: x if len(x) <= max_nom else x[:max_nom - 1] + "…")(str(noms.get(c, c)))
    lignes, colonnes = ordre[1:], ordre[:-1]
    d = lambda x: f"{x:.2f}" if anglais() else f"{x:.2f}".replace(".", ",")
    z, texte, survol = [], [], []
    for i, a in enumerate(lignes, start=1):
        z.append([float(m.at[a, b]) if j < i else None for j, b in enumerate(colonnes)])
        texte.append([d(m.at[a, b]) if j < i else "" for j, b in enumerate(colonnes)])
        survol.append([f"{noms.get(a, a)} / {noms.get(b, b)} : {d(m.at[a, b])} ({_qualificatif(m.at[a, b])})"
                       if j < i else "" for j, b in enumerate(colonnes)])
    fig = go.Figure(go.Heatmap(
        z=z, x=[court(c) for c in colonnes], y=[court(c) for c in lignes], zmin=-1, zmax=1,
        colorscale=ECHELLE_CORRELATION, hoverongaps=False, xgap=1, ygap=1,
        text=texte if n <= 13 else None, texttemplate="%{text}" if n <= 13 else None,
        textfont=dict(size=11 if n <= 8 else 9), customdata=survol,
        hovertemplate="%{customdata}<extra></extra>",
        colorbar=dict(thickness=10, len=0.5, outlinewidth=0, tickvals=[-1, -0.5, 0, 0.5, 1],
                      y=0.98, yanchor="top"),
    ))
    taille = 10 if n > 30 else 11
    _style(fig, hauteur=int(min(max(320, (20 if n > 25 else 30) * n + 120), 980)), legende=False)
    fig.update_xaxes(showgrid=False, tickangle=-60, tickfont=dict(size=taille), constrain="domain",
                     showline=False)
    fig.update_yaxes(autorange="reversed", showgrid=False, tickfont=dict(size=taille), scaleanchor="x",
                     scaleratio=1, constrain="domain", showline=False)
    fig.update_layout(margin=dict(l=4, r=4, t=8, b=4))
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
        x=alea["volatilite"], y=alea["rendement"], mode="markers", name=t("Portefeuilles aléatoires"),
        marker=dict(size=4, color=alea["sharpe"], opacity=0.55,
                    colorscale=[[0, "#cde2fb"], [1, "#0d366b"]],
                    colorbar=dict(title=dict(text="Sharpe"), thickness=12, outlinewidth=0)),
        hovertemplate=t("Volatilité %{x:.1%}<br>Rendement %{y:.1%}") + "<extra></extra>",
    ))
    # Droite de marché des capitaux
    rf, tangent = opti["taux_sans_risque"], opti["sharpe_max"]
    volatilites = [v for v in (front.get("volatilite", pd.Series(dtype=float)).max(),
                                alea["volatilite"].max() if len(alea) else None, tangent["volatilite"])
                   if v is not None and v == v]
    vmax = max(volatilites) * 1.05
    pente = (tangent["rendement"] - rf) / tangent["volatilite"]
    fig.add_trace(go.Scatter(
        x=[0, vmax], y=[rf, rf + pente * vmax], mode="lines", name=t("Droite de marché des capitaux"),
        line=dict(color=GRIS, width=1.5, dash="dash"), hoverinfo="skip",
    ))
    # Frontière efficiente (approchée par le nuage si l'optimiseur n'a trouvé aucun point exact)
    nom_frontiere = t("Frontière efficiente (approchée)") if opti.get("frontiere_approchee") \
        else t("Frontière efficiente")
    fig.add_trace(go.Scatter(
        x=front.get("volatilite", []), y=front.get("rendement", []), mode="lines", name=nom_frontiere,
        line=dict(color=TEXTE, width=3),
        hovertemplate=t("Volatilité %{x:.1%}<br>Rendement %{y:.1%}") + f"<extra>{t('Frontière')}</extra>",
    ))
    # Titres seuls
    fig.add_trace(go.Scatter(
        x=seuls["volatilite"], y=seuls["rendement"],
        mode="markers+text" if len(seuls) <= 20 else "markers", name=t("Titres seuls"),
        marker=dict(color=GRIS, size=7), text=list(seuls.index), textposition="top right",
        textfont=dict(size=9, color=GRIS), customdata=seuls["nom"],
        hovertemplate="%{customdata}<br>" + t("Volatilité %{x:.1%}<br>Rendement %{y:.1%}") + "<extra></extra>",
    ))
    # Les trois portefeuilles comparés
    for cle, nom, couleur, symbole, taille in [("actuel", t("Mon portefeuille"), ORANGE, "circle", 15),
                                               ("variance_min", t("Variance minimale"), AQUA, "diamond", 15),
                                               ("sharpe_max", t("Sharpe maximal"), VERT_FONCE, "star", 20)]:
        p = opti[cle]
        sharpe = f"{p['sharpe']:.2f}" if anglais() else f"{p['sharpe']:.2f}".replace(".", ",")
        fig.add_trace(go.Scatter(
            x=[p["volatilite"]], y=[p["rendement"]], mode="markers",
            name=f"{nom} (Sharpe {sharpe})",
            marker=dict(color=couleur, size=taille, symbol=symbole, line=dict(color="white", width=2)),
            hovertemplate=f"<b>{nom}</b><br>" + t("Volatilité %{x:.1%}<br>Rendement %{y:.1%}") + "<extra></extra>",
        ))
    _style(fig, hauteur=560)
    fig.update_xaxes(tickformat=".0%", title_text=t("Volatilité annuelle"), rangemode="tozero",
                     showgrid=True, gridcolor=GRILLE)
    fig.update_yaxes(tickformat=".0%", title_text=t("Rendement annuel espéré"))
    return fig


COULEURS_SENS = {"renforcer": "#0b7a33", "alleger": "#c0392b", "sortir": "#c0392b", "inchange": "#a3a39e"}
COULEURS_CLASSES = {"Actions": "#2a78d6", "Obligations": "#1baf7a", "Or": "#d4a017", "Monétaire": "#8fb6e6"}


def _poids_txt(x):
    """Poids en % sans décimale inutile : 0.3 -> '30 %', 0.025 -> '2,5 %'."""
    v = x * 100
    texte = f"{v:.0f}" if abs(v - round(v)) < 0.05 or v >= 10 else f"{v:.1f}"
    return (texte if anglais() else texte.replace(".", ",")) + espace_pct() + "%"


def fig_poids(tableau, poids_max=1.0, max_lignes=20):
    """Graphique « de → à » : pour chaque titre, un point au poids actuel et une flèche
    jusqu'au poids conseillé (vert : renforcer, rouge : alléger ou sortir).
    tableau : optimisation.comparer_repartitions(...) (déjà trié par ampleur du changement).
    Les lignes inchangées sont regroupées ; au-delà de max_lignes, seules les plus grosses
    variations sont montrées."""
    bouge = tableau[tableau["sens"] != "inchange"]
    bouge = bouge.head(max_lignes).iloc[::-1]          # le plus gros changement en haut
    noms = [n if len(n) <= 34 else n[:33] + "…" for n in bouge["nom"]]
    fig = go.Figure()
    # Segments (une seule courbe, séparée par des None) colorés par sens
    for sens in ["renforcer", "alleger", "sortir"]:
        partie = [(nom, l) for nom, (_, l) in zip(noms, bouge.iterrows()) if l["sens"] == sens]
        if not partie:
            continue
        xs, ys = [], []
        for nom, l in partie:
            xs += [l["actuel"], l["cible"], None]
            ys += [nom, nom, None]
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=COULEURS_SENS[sens], width=3),
                                 hoverinfo="skip", showlegend=False))
    # Point de départ (poids actuel)
    fig.add_trace(go.Scatter(
        x=bouge["actuel"], y=noms, mode="markers", name=_t("Poids actuel"),
        marker=dict(color="white", size=11, line=dict(color=GRIS_FONCE, width=2)),
        customdata=list(zip(bouge["cible"], bouge["euros"])),
        hovertemplate="%{y}<br>" + _t("Actuel %{x:.1%} → conseillé %{customdata[0]:.1%}") + "<br>"
                      + _t("À acheter / vendre : {montant}", montant=eur("%{customdata[1]:+,.0f}")) + "<extra></extra>",
    ))
    # Pointe de flèche au poids conseillé
    for sens, nom_legende in [("renforcer", _t("À renforcer")), ("alleger", _t("À alléger")),
                              ("sortir", _t("À vendre entièrement"))]:
        partie = bouge[bouge["sens"] == sens]
        if partie.empty:
            continue
        ys = [n for n, s_ in zip(noms, bouge["sens"]) if s_ == sens]
        fig.add_trace(go.Scatter(
            x=partie["cible"], y=ys, mode="markers", name=nom_legende,
            marker=dict(color=COULEURS_SENS[sens], size=13,
                        symbol="triangle-right" if sens == "renforcer" else "triangle-left"),
            customdata=list(zip(partie["actuel"], partie["euros"])),
            hovertemplate="%{y}<br>" + _t("Conseillé %{x:.1%} (actuel %{customdata[0]:.1%})") + "<br>"
                          + _t("À acheter / vendre : {montant}", montant=eur("%{customdata[1]:+,.0f}")) + "<extra></extra>",
        ))
    # Étiquettes « 5 % → 30 % » au bout de chaque ligne
    xmax = float(max(bouge[["actuel", "cible"]].max().max() if len(bouge) else 0.1, poids_max if poids_max < 1 else 0))
    fig.add_trace(go.Scatter(
        x=[max(a, c) for a, c in zip(bouge["actuel"], bouge["cible"])], y=noms, mode="text",
        text=[f"   {_poids_txt(a)} → {_poids_txt(c)}" for a, c in zip(bouge["actuel"], bouge["cible"])],
        textposition="middle right", textfont=dict(size=11, color=GRIS_FONCE), hoverinfo="skip", showlegend=False,
    ))
    if poids_max < 1:
        fig.add_vline(x=poids_max, line=dict(color=GRIS, width=1.5, dash="dash"),
                      annotation_text=_t("Plafond {p} par titre", p=_poids_txt(poids_max)), annotation_position="top",
                      annotation_font=dict(size=11, color=GRIS))
    hauteur = max(260, 38 * len(bouge) + 110)
    _style(fig, hauteur=hauteur)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
                      margin=dict(l=4, r=8, t=60, b=4))
    fig.update_xaxes(tickformat=".0%", range=[0, xmax * 1.28 + 0.01], showgrid=True, gridcolor=GRILLE,
                     title_text=_t("Poids dans le portefeuille"))
    fig.update_yaxes(showgrid=False, categoryorder="array", categoryarray=noms)
    return fig


def fig_classes_comparees(par_classe, nom_cible):
    """Deux barres empilées à 100 % : répartition par classe d'actifs, actuelle et conseillée."""
    fig = go.Figure()
    lignes = [_t("Actuel"), nom_cible]
    for classe, ligne in par_classe.iterrows():
        valeurs = [ligne["actuel"], ligne["cible"]]
        fig.add_trace(go.Bar(
            y=lignes, x=valeurs, orientation="h", name=td(classe),
            marker=dict(color=COULEURS_CLASSES.get(classe, GRIS), line=dict(color="white", width=1.5)),
            text=[_poids_txt(v) if v >= 0.06 else "" for v in valeurs], textposition="inside", insidetextanchor="middle",
            textfont=dict(color="white", size=12),
            hovertemplate="%{y} · " + td(classe) + " : %{x:.1%}<extra></extra>",
        ))
    _style(fig, hauteur=170)
    fig.update_layout(barmode="stack", bargap=0.35, legend=dict(orientation="h", yanchor="bottom", y=1.04,
                                                                    xanchor="left", x=0),
                      margin=dict(l=4, r=8, t=36, b=4))
    fig.update_xaxes(tickformat=".0%", range=[0, 1], showgrid=False, showticklabels=False)
    fig.update_yaxes(autorange="reversed", showgrid=False)
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
                             name=_t("90 % des scénarios"), hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=t.index, y=t["p25"], mode="lines", line=dict(width=0),
                             showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=t.index, y=t["p75"], mode="lines", line=dict(width=0),
                             fill="tonexty", fillcolor="rgba(42, 120, 214, 0.28)",
                             name=_t("50 % des scénarios"), hoverinfo="skip"))
    fig.add_trace(go.Scatter(
        x=t.index, y=t["apports"], mode="lines", name=_t("Argent investi"),
        line=dict(color=ORANGE, width=2, dash="dash"),
        hovertemplate=eur("%{y:,.0f}") + f"<extra>{_t('Investi')}</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=t.index, y=t["p50"], mode="lines", name=_t("Scénario médian"),
        line=dict(color=BLEU, width=3),
        customdata=t[["p5", "p95"]].to_numpy(),
        hovertemplate=_t("Médiane {v}<br>Fourchette 90 % : {bas} – {haut}", v=eur("%{y:,.0f}"),
                         bas="%{customdata[0]:,.0f}", haut=eur("%{customdata[1]:,.0f}")) + "<extra></extra>",
    ))
    if sim.get("objectif"):
        fig.add_hline(y=sim["objectif"], line=dict(color=GRIS_FONCE, width=1, dash="dot"),
                      annotation_text=_t("Objectif"), annotation_position="top left",
                      annotation_font_color=GRIS_FONCE)
    _style(fig, hauteur=460)
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(tickformat="%Y", hoverformat="%b %Y" if anglais() else "%m/%Y")
    fig.update_yaxes(tickformat=",.0f", **_axe_euros("y"))
    return fig


def fig_distribution_finale(sim, echelle_log=False):
    """Histogramme de la valeur finale des scénarios : zone « 90 % des scénarios » (P5 à P95),
    médiane, moyenne et montant investi, tous dans la légende.
    echelle_log : histogramme du logarithme de la valeur. La valeur finale suit (à peu près) une
    loi log-normale : en échelle logarithmique, elle redevient une cloche symétrique."""
    finales = np.asarray(sim["valeurs_finales"], dtype=float)
    finales = finales[np.isfinite(finales) & (finales > 0)]
    bas, haut = np.percentile(finales, [0.5, 99.5])
    reperes = [("total_apporte", _t("Montant investi"), ORANGE, "dash"),
               ("mediane", _t("Médiane"), TEXTE, "solid"),
               ("moyenne", _t("Moyenne"), GRIS_FONCE, "dot")]
    bas = min(bas, sim["total_apporte"] * 0.97)
    haut = max(haut, sim["total_apporte"] * 1.03)
    if echelle_log:
        f = np.log10
        x = f(finales[(finales >= bas) & (finales <= haut)])
    else:
        f = (lambda v: v)
        x = finales[(finales >= bas) & (finales <= haut)]
    debut, fin = float(f(bas)), float(f(haut))
    largeur = (fin - debut) / 60 if fin > debut else 1.0
    fig = go.Figure(go.Histogram(
        x=x, xbins=dict(start=debut, end=fin + largeur, size=largeur), name=_t("Scénarios"), marker=dict(color=BLEU, opacity=0.8, line=dict(color="white", width=0.6)),
        customdata=None,
        hovertemplate=(_t("%{y} scénarios") + "<extra></extra>") if echelle_log
        else (eur("%{x:,.0f}") + "<br>" + _t("%{y} scénarios") + "<extra></extra>"),
        showlegend=False,
    ))
    # Zone des 90 % de scénarios (entrée de légende factice : un carré de la même couleur)
    fig.add_vrect(x0=f(sim["p5"]), x1=f(sim["p95"]), fillcolor="rgba(42, 120, 214, 0.10)", line_width=0, layer="below")
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", name=_t("90 % des scénarios (P5 à P95)"),
                             marker=dict(symbol="square", size=12, color="rgba(42, 120, 214, 0.25)")))
    comptes, _ = np.histogram(x, bins=np.arange(debut, fin + 2 * largeur, largeur))
    sommet = float(comptes.max()) * 1.08 if len(comptes) else 1
    for cle, nom, couleur, trait in reperes:
        v = sim[cle]
        fig.add_trace(go.Scatter(x=[f(v), f(v)], y=[0, sommet], mode="lines", name=nom,
                                 line=dict(color=couleur, width=2, dash=trait),
                                 hovertemplate=f"{nom} : " + eur(f"{v:,.0f}".replace(",", " " if not anglais() else ","))
                                 + "<extra></extra>"))
    _style(fig, hauteur=380)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
                      margin=dict(l=4, r=8, t=56, b=4), bargap=0.04)
    if echelle_log:
        graduations = _graduations_log(bas, haut)
        fig.update_xaxes(range=[f(bas), f(haut)], tickvals=[f(v) for v in graduations],
                         ticktext=[_euros_court(v) for v in graduations],
                         title_text=_t("Valeur finale (échelle logarithmique)"))
    else:
        fig.update_xaxes(range=[bas, haut], tickformat=",.0f", title_text=_t("Valeur finale"), **_axe_euros("x"))
    fig.update_yaxes(title_text=_t("Nombre de scénarios"), rangemode="tozero")
    return fig


def _graduations_log(bas, haut):
    """Graduations « rondes » (1, 2, 5 × 10^k) entre bas et haut, pour un axe logarithmique."""
    valeurs = []
    k = int(np.floor(np.log10(bas)))
    while 10 ** k <= haut * 10:
        for m in (1, 2, 5):
            v = m * 10 ** k
            if bas <= v <= haut:
                valeurs.append(v)
        k += 1
    return valeurs or [bas, haut]


def _euros_court(v):
    """1 500 000 -> '1,5 M€' ; 250 000 -> '250 k€' (ou '€1.5M', '€250k' en anglais)."""
    if v >= 1e6:
        texte, unite = f"{v / 1e6:g}", "M"
    elif v >= 1e3:
        texte, unite = f"{v / 1e3:g}", "k"
    else:
        texte, unite = f"{v:g}", ""
    return f"€{texte}{unite}" if anglais() else f"{texte.replace('.', ',')} {unite}€"


# Couleurs des tranches de probabilité : rouge (défavorable) -> gris -> bleu (favorable)
COULEURS_TRANCHES = ["#a32020", "#e0797b", "#a3a39e", "#5598e7", "#184f95"]


def fig_projection_nuage(sim):
    """Nuage de points : chaque point est UN scénario à une date donnée,
    coloré selon sa tranche de probabilité à cette date."""
    t = sim["trajectoires"]
    points = points_nuage(sim)
    fig = go.Figure()
    for numero, (nom, couleur) in enumerate(zip(TRANCHES, COULEURS_TRANCHES)):
        nom = td(nom)
        tranche = points[points["tranche"] == numero]
        fig.add_trace(go.Scatter(
            x=tranche["date"], y=tranche["valeur"], mode="markers", name=nom,
            marker=dict(color=couleur, size=6, opacity=0.75, line=dict(color="white", width=0.5)),
            customdata=list(zip(tranche["date_reelle"].dt.strftime("%b %Y" if anglais() else "%m/%Y"),
                                tranche["scenario"])),
            hovertemplate=_t("Scénario n° %{customdata[1]} · %{customdata[0]}") + "<br>" + eur("%{y:,.0f}")
                          + f"<extra>{nom}</extra>",
        ))
    # Repères : médiane, bornes à 5 % et 95 %, argent investi
    fig.add_trace(go.Scatter(x=t.index, y=t["p95"], mode="lines", name=_t("Seuil des 95 %"),
                             line=dict(color=COULEURS_TRANCHES[4], width=1.2, dash="dot"),
                             hovertemplate=_t("95e percentile : {v}", v=eur("%{y:,.0f}")) + "<extra></extra>"))
    fig.add_trace(go.Scatter(x=t.index, y=t["p50"], mode="lines", name=_t("Médiane"),
                             line=dict(color=TEXTE, width=2.2),
                             hovertemplate=_t("Médiane : {v}", v=eur("%{y:,.0f}")) + "<extra></extra>"))
    fig.add_trace(go.Scatter(x=t.index, y=t["p5"], mode="lines", name=_t("Seuil des 5 %"),
                             line=dict(color=COULEURS_TRANCHES[0], width=1.2, dash="dot"),
                             hovertemplate=_t("5e percentile : {v}", v=eur("%{y:,.0f}")) + "<extra></extra>"))
    fig.add_trace(go.Scatter(x=t.index, y=t["apports"], mode="lines", name=_t("Argent investi"),
                             line=dict(color=ORANGE, width=2, dash="dash"),
                             hovertemplate=_t("Investi : {v}", v=eur("%{y:,.0f}")) + "<extra></extra>"))
    _style(fig, hauteur=520)
    fig.update_layout(hovermode="closest")
    fig.update_xaxes(tickformat="%Y")
    fig.update_yaxes(tickformat=",.0f", **_axe_euros("y"))
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


def fig_lignes(tableau, format_y=",.0f", euros=False, hauteur=420, base100=False):
    """Plusieurs courbes (une par colonne), couleurs dans l'ordre fixe."""
    fig = go.Figure()
    for i, colonne in enumerate(tableau.columns):
        serie = tableau[colonne].dropna()
        if base100:
            serie = 100 * serie / serie.iloc[0]
        fig.add_trace(go.Scatter(
            x=serie.index, y=serie, mode="lines", name=td(str(colonne)),
            line=dict(color=SERIES[i % len(SERIES)], width=2.4 if i == 0 else 1.8),
            hovertemplate=(eur(f"%{{y:{format_y}}}") if euros else f"%{{y:{format_y}}}")
                          + f"<extra>{td(str(colonne))}</extra>",
        ))
    _style(fig, hauteur=hauteur)
    fig.update_layout(hovermode="x unified")
    fig.update_yaxes(tickformat=format_y, **(_axe_euros("y") if euros else {}))
    return _axe_dates(fig)


def fig_fiscalite_horizon(tableau):
    """Gain net selon l'année de sortie, pour chaque enveloppe (une courbe par enveloppe)."""
    fig = go.Figure()
    for i, colonne in enumerate(tableau.columns):
        fig.add_trace(go.Scatter(
            x=tableau.index, y=tableau[colonne], mode="lines+markers", name=td(colonne),
            line=dict(color=SERIES[i], width=2.2, shape="hv" if colonne != "CTO" else "linear"),
            marker=dict(size=5),
            hovertemplate=t("Sortie dans %{{x}} an(s) : {v}", v=eur("%{y:,.0f}")) + f"<extra>{td(colonne)}</extra>",
        ))
    _style(fig, hauteur=380)
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(title_text=t("Années avant la sortie"), dtick=2)
    fig.update_yaxes(tickformat=",.0f", title_text=t("Gain net d'impôts"), **_axe_euros("y"))
    return fig


def fig_poids_et_risque(par_ligne, max_lignes=20):
    """Pour chaque ligne : sa part de la valeur et sa part du risque."""
    t = par_ligne.head(max_lignes).iloc[::-1]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=t["poids"], y=t["nom"], orientation="h", name=_t("Part de la valeur"),
                         marker=dict(color="#b8c4d6", cornerradius=3),
                         hovertemplate=_t("%{y} : %{x:.1%} de la valeur") + "<extra></extra>"))
    fig.add_trace(go.Bar(x=t["part_risque"], y=t["nom"], orientation="h", name=_t("Part du risque"),
                         marker=dict(color=BLEU, cornerradius=3),
                         hovertemplate=_t("%{y} : %{x:.1%} du risque") + "<extra></extra>"))
    _style(fig, hauteur=max(360, 40 * len(t) + 80))
    fig.update_layout(barmode="group", bargap=0.25, bargroupgap=0.05)
    fig.update_xaxes(tickformat=".0%", showgrid=True, gridcolor=GRILLE)
    fig.update_yaxes(showgrid=False)
    return fig


def fig_effets_attribution(par_region):
    """Effets d'allocation, de sélection et d'interaction par région (barres groupées)."""
    fig = go.Figure()
    for i, (colonne, nom) in enumerate([("allocation", t("Allocation")), ("selection", t("Sélection")),
                                        ("interaction", t("Interaction"))]):
        fig.add_trace(go.Bar(
            x=[td(r) for r in par_region.index], y=par_region[colonne], name=nom,
            marker=dict(color=SERIES[i], cornerradius=3),
            hovertemplate="%{x} : %{y:+.2%}<extra>" + nom + "</extra>",
        ))
    _style(fig, hauteur=400)
    fig.update_layout(barmode="group", bargap=0.25)
    fig.update_yaxes(tickformat=".1%", zeroline=True, zerolinecolor=GRIS)
    return fig
