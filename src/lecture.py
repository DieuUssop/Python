"""
lecture.py — Phrases de lecture automatique des graphiques.

Chaque fonction transforme des chiffres déjà calculés (src/metrics.py,
src/simulation.py, src/optimisation.py) en quelques phrases simples, dans la
langue choisie (les textes passent par t()). Rien n'est calculé ici : on
interprète seulement, avec des seuils documentés.
"""

from .interface import euros, nombre, pct
from .langues import t


# ----------------------------------------------------------------------
# Distribution des rendements quotidiens (onglet Risque)
# ----------------------------------------------------------------------
SEUIL_ASYMETRIE = 0.3      # |skewness| en dessous : distribution à peu près symétrique
SEUIL_KURTOSIS = 1.0       # kurtosis en excès au-delà : queues nettement épaisses
SEUIL_P_VALUE = 0.05       # test de Jarque-Bera : on rejette la normalité en dessous


def lecture_distribution(av):
    """Liste de phrases expliquant la forme de la distribution et l'écart à la loi normale."""
    phrases = []
    s, k = av["asymetrie"], av["kurtosis"]
    if s < -SEUIL_ASYMETRIE:
        phrases.append(t("Asymétrie de {s} : les fortes baisses sont plus fréquentes ou plus violentes que les "
                         "fortes hausses.", s=nombre(s)))
    elif s > SEUIL_ASYMETRIE:
        phrases.append(t("Asymétrie de {s} : les fortes hausses l'emportent sur les fortes baisses.", s=nombre(s)))
    else:
        phrases.append(t("Asymétrie de {s} : la distribution est à peu près symétrique.", s=nombre(s)))

    ratio = av["jours_extremes"] / av["jours_extremes_normale"] if av["jours_extremes_normale"] else 0
    if k > SEUIL_KURTOSIS:
        phrases.append(t("Kurtosis en excès de {k} : « queues épaisses ». Les journées à plus de 3 écarts-types "
                         "représentent {obs} des jours, contre {theo} selon la loi normale (×{ratio}).",
                         k=nombre(k), obs=pct(av["jours_extremes"], signe=False),
                         theo=pct(av["jours_extremes_normale"], signe=False), ratio=nombre(ratio, 1)))
    elif k > 0:
        phrases.append(t("Kurtosis en excès de {k} : queues légèrement plus épaisses que la loi normale.",
                         k=nombre(k)))
    else:
        phrases.append(t("Kurtosis en excès de {k} : pas plus de journées extrêmes que ne le prévoit la loi "
                         "normale.", k=nombre(k)))

    p = av["p_jarque_bera"]
    if p < SEUIL_P_VALUE:
        phrases.append(t("Le test de Jarque-Bera rejette la loi normale (p-value {p}) : les VaR calculées avec la "
                         "loi normale sont à prendre avec prudence.", p=_p_value(p)))
    else:
        phrases.append(t("Le test de Jarque-Bera ne rejette pas la loi normale (p-value {p}).", p=_p_value(p)))

    hist, norm = av["var_historique"], av["var_parametrique"]
    if norm > 0 and hist > norm * 1.05:
        phrases.append(t("La VaR historique ({h}) dépasse la VaR de la loi normale ({n}) : la loi normale "
                         "sous-estime ici la perte d'un mauvais jour.", h=pct(hist, signe=False),
                         n=pct(norm, signe=False)))
    elif norm > 0 and hist < norm * 0.95:
        phrases.append(t("La VaR historique ({h}) est inférieure à la VaR de la loi normale ({n}) à ce niveau de "
                         "confiance : les pertes extrêmes se concentrent sur quelques jours, que la CVaR mesure "
                         "mieux.", h=pct(hist, signe=False), n=pct(norm, signe=False)))
    else:
        phrases.append(t("VaR historique et VaR de la loi normale sont proches ({h} et {n}).",
                         h=pct(hist, signe=False), n=pct(norm, signe=False)))
    return phrases


# ----------------------------------------------------------------------
# Optimisation : que faudrait-il changer ? (onglet Optimisation)
# ----------------------------------------------------------------------
def _liste(noms):
    """['A', 'B', 'C'] -> 'A, B et C' (ou 'A, B and C')."""
    noms = list(noms)
    if len(noms) <= 1:
        return "".join(noms)
    return ", ".join(noms[:-1]) + t(" et ") + noms[-1]


def synthese_optimisation(resume, par_classe, nom_cible):
    """Phrase de synthèse : titres à renforcer / alléger, titres qui sortent, part du
    portefeuille à déplacer, et évolution de la classe d'actifs qui bouge le plus."""
    morceaux = []
    if resume["renforcer"]:
        morceaux.append(t("renforcer {noms}", noms=_liste(resume["renforcer"])))
    if resume["alleger"]:
        morceaux.append(t("alléger {noms}", noms=_liste(resume["alleger"])))
    if not morceaux:
        return t("Le portefeuille actuel est déjà très proche du portefeuille « {cible} ».", cible=nom_cible)
    phrase = t("Pour atteindre le portefeuille « {cible} » : {actions}", cible=nom_cible,
               actions=t(" ; ").join(morceaux)) + "."
    if resume["nb_sortent"]:
        phrase += " " + t("{n} titre(s) sortent entièrement du portefeuille.", n=resume["nb_sortent"])
    phrase += " " + t("Au total, {part} du portefeuille change de place.", part=pct(resume["rotation"], signe=False,
                                                                                     decimales=0))
    if len(par_classe):
        ecarts = (par_classe["cible"] - par_classe["actuel"])
        classe = ecarts.abs().idxmax()
        if abs(ecarts[classe]) >= 0.05:
            from .langues import td
            phrase += " " + t("La part en {classe} passe de {avant} à {apres}.", classe=td(classe).lower(),
                              avant=pct(par_classe.at[classe, "actuel"], signe=False, decimales=0),
                              apres=pct(par_classe.at[classe, "cible"], signe=False, decimales=0))
    return phrase


# ----------------------------------------------------------------------
# Projection Monte-Carlo : distribution de la valeur finale (onglet Projection)
# ----------------------------------------------------------------------
def lecture_valeur_finale(sim):
    """Phrases de lecture de la distribution de la valeur finale."""
    annees = sim["parametres"]["annees"]
    phrases = [
        t("Dans 90 % des scénarios, la valeur dans {n} ans se situe entre {bas} et {haut}.", n=annees,
          bas=euros(sim["p5"]), haut=euros(sim["p95"])),
        t("Probabilité de finir sous le montant investi ({investi}) : {p}.", investi=euros(sim["total_apporte"]),
          p=pct(sim["proba_perte"], signe=False, decimales=1)),
        t("Probabilité de doubler le montant investi : {p}.", p=pct(sim["proba_doubler"], signe=False, decimales=1)),
    ]
    if sim["moyenne"] > sim["mediane"] * 1.02:
        phrases.append(t("La moyenne ({moyenne}) dépasse la médiane ({mediane}) : quelques scénarios très favorables "
                         "tirent la moyenne vers le haut (distribution asymétrique, dite log-normale). La médiane est "
                         "le repère le plus représentatif.", moyenne=euros(sim["moyenne"]), mediane=euros(sim["mediane"])))
    return phrases


def _p_value(p):
    """p-value lisible : '< 0,001' quand elle est minuscule."""
    if p < 0.001:
        return "< " + nombre(0.001, 3)
    return nombre(p, 3)


def tableau_html(entetes, lignes, classe="tableau-simple", droite_a_partir_de=1):
    """Petit tableau HTML sobre (les cellules sont déjà mises en forme et échappées)."""
    from html import escape
    tete = "".join(f'<th class="{"num" if i >= droite_a_partir_de else ""}">{escape(h)}</th>'
                   for i, h in enumerate(entetes))
    corps = "".join("<tr>" + "".join(f'<td class="{"num" if i >= droite_a_partir_de else ""}">{c}</td>'
                                     for i, c in enumerate(ligne)) + "</tr>" for ligne in lignes)
    return f'<table class="{classe}"><thead><tr>{tete}</tr></thead><tbody>{corps}</tbody></table>'
