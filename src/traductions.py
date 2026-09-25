"""
traductions.py — Dictionnaire français -> anglais du tableau de bord.

    TEXTES  : textes de l'interface (titres, cartes, notes, graphiques)
    DONNEES : valeurs issues des calculs (régions, secteurs, profils, scénarios...)
    MOTIFS  : données qui contiennent un nombre variable ("Progressif (12 mois)")

Pour ajouter une traduction : copier le texte français EXACT utilisé dans
le code (dans t("...")) et écrire sa version anglaise. Les {noms} entre
accolades doivent être conservés à l'identique.
"""

TEXTES = {
    # ------------------------------------------------------------------
    # Barre latérale et en-tête
    # ------------------------------------------------------------------
    "Suivi de portefeuille": "Portfolio tracking",
    "Outil de suivi de portefeuille": "Portfolio tracking tool",
    "Gestion de portefeuille": "Portfolio management",
    "Espace de travail": "Workspace",
    "Analyse du portefeuille": "Portfolio analysis",
    "Conseil patrimonial": "Wealth advisory",
    "Gestion d'actifs": "Asset management",
    "Performance, risque, optimisation, projection": "Performance, risk, optimisation, projection",
    "Profil client, fiscalité, stress tests": "Client profile, taxation, stress tests",
    "Attribution, budget de risque, backtest": "Attribution, risk budget, backtest",
    "Données": "Data",
    "Portefeuille": "Portfolio",
    "Mon portefeuille": "My portfolio",
    "Portefeuille actions monde": "Global equity portfolio",
    "Portefeuille diversifié (multi-actifs)": "Diversified portfolio (multi-asset)",
    "Fichiers data/transactions*.csv du projet": "Project files data/transactions*.csv",
    "Ou envoyer un autre fichier (CSV)": "Or upload another file (CSV)",
    "Prioritaire sur le portefeuille choisi ci-dessus": "Takes priority over the portfolio selected above",
    "Paramètres d'analyse": "Analysis settings",
    "Indice de référence": "Benchmark index",
    "MSCI World (ETF CW8, dividendes réinvestis)": "MSCI World (CW8 ETF, dividends reinvested)",
    "S&P 500 (ETF ESE, dividendes réinvestis)": "S&P 500 (ESE ETF, dividends reinvested)",
    "CAC 40 (hors dividendes)": "CAC 40 (price index, excl. dividends)",
    "Euro Stoxx 50 (hors dividendes)": "Euro Stoxx 50 (price index, excl. dividends)",
    "Taux sans risque (% par an)": "Risk-free rate (% per year)",
    "Taux de la facilité de dépôt de la BCE : 2,50 % depuis le 16/09/2026":
        "ECB deposit facility rate: 2.50% since 16 Sep 2026",
    "Niveau de confiance de la VaR": "VaR confidence level",
    "Actualiser les cours": "Refresh prices",
    "Aucun fichier de transactions : envoyez un fichier CSV depuis la barre latérale.":
        "No transactions file: upload a CSV file from the sidebar.",
    "Récupération des cours et calcul des indicateurs...": "Fetching prices and computing indicators...",
    "Impossible d'analyser le portefeuille : {erreur}": "Unable to analyse the portfolio: {erreur}",
    "Informations": "Information",
    "Fichier": "File",
    "Opérations": "Transactions",
    "Période": "Period",
    "Cours": "Prices",
    "1 € en {devise}": "€1 in {devise}",
    "Rapport": "Report",
    "Préparer le rapport PDF": "Prepare the PDF report",
    "Le rapport PDF est rédigé en français.": "The PDF report is written in French.",
    "Génération du rapport...": "Generating the report...",
    "Installer reportlab : python -m pip install reportlab": "Install reportlab: python -m pip install reportlab",
    "Télécharger le rapport": "Download the report",
    "Méthodologie": "Methodology",
    "- **TWR** : rendement pondéré par le temps, neutre vis-à-vis des apports.\n"
    "- **TRI** : taux de rendement interne des flux de l'investisseur.\n"
    "- **Volatilité** : écart-type quotidien × √252.\n"
    "- **VaR / CVaR** : méthode historique, horizon 1 jour.\n"
    "- **Markowitz** : optimisation SLSQP, sans vente à découvert.\n\n"
    "Détails dans le fichier README.md du projet.":
        "- **TWR**: time-weighted return, neutral to cash flows.\n"
        "- **IRR**: internal rate of return of the investor's cash flows.\n"
        "- **Volatility**: daily standard deviation × √252.\n"
        "- **VaR / CVaR**: historical method, 1-day horizon.\n"
        "- **Markowitz**: SLSQP optimisation, no short selling.\n\n"
        "Details in the project's README.md file (in French).",
    "Du {debut} au {fin}  ·  {n} lignes  ·  Référence : {indice}":
        "From {debut} to {fin}  ·  {n} holdings  ·  Benchmark: {indice}",
    "Cours en direct · Yahoo Finance": "Live prices · Yahoo Finance",
    "Cours en cache (hors ligne)": "Cached prices (offline)",
    "Données au {date}": "Data as of {date}",
    "Données de marché : Yahoo Finance · Taux sans risque : BCE · "
    "Outil pédagogique réalisé dans le cadre du Master G2C — ne constitue pas un conseil en investissement.":
        "Market data: Yahoo Finance · Risk-free rate: ECB · "
        "Educational tool developed as part of the Master G2C — not investment advice.",

    # ------------------------------------------------------------------
    # Chiffres clés
    # ------------------------------------------------------------------
    "Valeur actuelle": "Current value",
    "Investi au PRU : {montant}": "Invested at average cost: {montant}",
    "Quantité × dernier cours, pour chaque ligne détenue": "Quantity × last price, for each holding",
    "Gain total": "Total gain",
    " sur le capital investi": " on invested capital",
    "Plus-values latentes + plus-values réalisées + dividendes": "Unrealised gains + realised gains + dividends",
    "Perf. annualisée": "Annualised return",
    "TWR total {valeur}": "Total TWR {valeur}",
    "Rendement pondéré par le temps (TWR) : mesure la qualité des choix, hors effet des apports":
        "Time-weighted return (TWR): measures the quality of decisions, excluding the effect of cash flows",
    "Volatilité": "Volatility",
    "Écart-type des rendements quotidiens × √252": "Standard deviation of daily returns × √252",
    "Ratio de Sharpe : (rendement − taux sans risque) / volatilité":
        "Sharpe ratio: (return − risk-free rate) / volatility",
    "Le {date}": "On {date}",
    "Pire baisse depuis un plus haut": "Worst decline from a peak",

    # ------------------------------------------------------------------
    # Onglets de l'analyse
    # ------------------------------------------------------------------
    "Vue d'ensemble": "Overview",
    "Positions": "Holdings",
    "Performance": "Performance",
    "Risque": "Risk",
    "Optimisation": "Optimisation",
    "Projection": "Projection",
    "Transactions": "Transactions",

    # Vue d'ensemble
    "Évolution du portefeuille": "Portfolio value over time",
    "Valeur de marché et capital investi (apports nets)": "Market value and invested capital (net contributions)",
    "Répartition": "Allocation",
    "Poids de chaque ligne dans la valeur totale": "Weight of each holding in total value",
    "Par classe d'actifs": "By asset class",
    "Par région": "By region",
    "Par secteur": "By sector",
    "{n} groupes · poids en % de la valeur": "{n} groups · weight in % of value",
    "Plus-values latentes": "Unrealised gains",
    "non réalisées": "unrealised",
    "Plus-values réalisées": "Realised gains",
    "encaissées": "realised",
    "Dividendes et coupons": "Dividends and coupons",
    "Montants bruts perçus": "Gross amounts received",
    "Frais de courtage": "Brokerage fees",
    "Depuis l'origine": "Since inception",

    # Positions
    "Positions détenues": "Current holdings",
    "Cliquer sur un titre de colonne pour trier": "Click a column header to sort",
    "Titre": "Security",
    "Classe": "Asset class",
    "Région": "Region",
    "Secteur": "Sector",
    "Devise": "Currency",
    "Devise de cotation (montants convertis en euros)": "Trading currency (amounts converted into euros)",
    "Quantité": "Quantity",
    "PRU": "Avg. cost",
    "Valeur": "Value",
    "+/- value": "Gain / loss",
    "+/- value %": "Gain / loss %",
    "Poids": "Weight",
    "Dividendes": "Dividends",
    "Plus-values latentes par ligne": "Unrealised gains by holding",
    "En euros, au dernier cours connu": "In euros, at the last known price",

    # Performance
    "TWR total": "Total TWR",
    "Depuis le {date}": "Since {date}",
    "TWR annualisé": "Annualised TWR",
    "Base 365 jours": "365-day basis",
    "TRI annuel": "Annual IRR",
    "Rendement de l'argent investi": "Money-weighted return",
    "Taux de rendement interne : dépend du calendrier des apports":
        "Internal rate of return: depends on the timing of contributions",
    "Écart avec {indice}": "Difference vs {indice}",
    "surperformance": "outperformance",
    "sous-performance": "underperformance",
    "TWR du portefeuille − TWR de l'indice, sur la même période":
        "Portfolio TWR − index TWR, over the same period",
    "Portefeuille et {indice}": "Portfolio and {indice}",
    "Base 100 à la première date commune": "Rebased to 100 at the first common date",
    "Rendement par année civile": "Calendar-year returns",
    "TWR du portefeuille et de l'indice": "TWR of the portfolio and the index",
    "Du plus haut du {sommet} au plus bas du {creux} · ": "From the peak on {sommet} to the trough on {creux} · ",
    "plus haut non retrouvé": "peak not yet recovered",
    "retrouvé le {date}": "recovered on {date}",
    "Bêta": "Beta",
    "1 = comme l'indice": "1 = same as the index",
    "Sensibilité du portefeuille aux mouvements de l'indice": "Sensitivity of the portfolio to index movements",
    "Alpha de Jensen": "Jensen's alpha",
    "annuel": "annual",
    "Performance non expliquée par l'exposition au marché (MEDAF)":
        "Performance not explained by market exposure (CAPM)",
    "Corrélation": "Correlation",
    "Avec {indice}": "With {indice}",
    "Annualisée": "Annualised",
    "Volatilité de l'écart de rendement avec l'indice": "Volatility of the return difference with the index",
    "Ratio d'information": "Information ratio",
    "Écart / tracking error": "Excess return / tracking error",

    # Risque
    "Ratio de Sharpe": "Sharpe ratio",
    "(Rendement − taux sans risque) / volatilité": "(Return − risk-free rate) / volatility",
    "Ratio de Sortino": "Sortino ratio",
    "Ne pénalise que les baisses": "Only penalises downside moves",
    "VaR {niveau} · 1 jour": "VaR {niveau} · 1 day",
    " méthode historique": " historical method",
    "Dans {niveau} des jours, la perte ne dépasse pas ce montant":
        "On {niveau} of days, the loss does not exceed this amount",
    " au-delà de la VaR": " beyond the VaR",
    "Perte moyenne les jours où la VaR est dépassée": "Average loss on days when the VaR is exceeded",
    "Distribution des rendements quotidiens": "Distribution of daily returns",
    "VaR paramétrique (loi normale) : {valeur}": "Parametric VaR (normal distribution): {valeur}",
    "Si la VaR historique dépasse la VaR paramétrique, les pertes extrêmes sont plus fréquentes "
    "que ne le prévoit la loi normale (« queues épaisses »).":
        "If the historical VaR exceeds the parametric VaR, extreme losses are more frequent than the "
        "normal distribution predicts (\"fat tails\").",
    "Corrélations": "Correlations",
    "Rendements quotidiens des titres détenus": "Daily returns of the securities held",

    # Optimisation
    "Poids maximal par titre": "Maximum weight per security",
    "sans limite": "no limit",
    "Sans limite, l'optimiseur concentre souvent tout sur 2 ou 3 titres.":
        "Without a limit, the optimiser often concentrates everything on 2 or 3 securities.",
    "Optimisation en cours...": "Optimising...",
    "Optimisation impossible : {erreur}": "Optimisation failed: {erreur}",
    "Variance minimale": "Minimum variance",
    "Sharpe maximal": "Maximum Sharpe",
    "Rendement {r} · Volatilité {v}": "Return {r} · Volatility {v}",
    "Frontière efficiente": "Efficient frontier",
    "Chaque point bleu est un portefeuille tiré au hasard : aucun ne dépasse la frontière":
        "Each blue dot is a randomly drawn portfolio: none lies beyond the frontier",
    "Répartitions comparées": "Allocations compared",
    "Poids actuels et poids optimaux": "Current and optimal weights",
    "Ajustements vers le Sharpe maximal": "Trades towards the maximum Sharpe portfolio",
    "À valeur totale inchangée, hors frais": "Same total value, excluding fees",
    "Actuel": "Current",
    "Optimal": "Optimal",
    "Acheter / vendre": "Buy / sell",
    "Exercice académique, pas un conseil en investissement. Les rendements espérés sont estimés sur "
    "le passé : l'optimiseur surexploite les titres qui ont le mieux marché, sans garantie pour l'avenir.":
        "Academic exercise, not investment advice. Expected returns are estimated from the past: the "
        "optimiser over-weights the best past performers, with no guarantee for the future.",

    # Projection
    "Hypothèses de la simulation": "Simulation assumptions",
    "Valeurs historiques du portefeuille : rendement {r}, volatilité {v}":
        "Historical portfolio values: return {r}, volatility {v}",
    "Horizon (années)": "Horizon (years)",
    "Versement mensuel (€)": "Monthly contribution (€)",
    "Objectif (€, facultatif)": "Target (€, optional)",
    "0 = pas d'objectif": "0 = no target",
    "Méthode": "Method",
    "Loi normale": "Normal distribution",
    "Historique (bootstrap)": "Historical (bootstrap)",
    "Historique : tire au hasard de vrais jours de bourse du portefeuille, ce qui conserve les krachs réels.":
        "Historical: randomly draws actual trading days of the portfolio, which preserves real crashes.",
    "Rendement annuel supposé (%)": "Assumed annual return (%)",
    "Par défaut : rendement historique. Le réduire donne une projection plus prudente.":
        "Default: historical return. Lowering it gives a more conservative projection.",
    "Volatilité annuelle (%)": "Annual volatility (%)",
    "Avec la méthode historique, la volatilité réelle est utilisée.":
        "With the historical method, the actual volatility is used.",
    "Simulation de Monte-Carlo...": "Running the Monte Carlo simulation...",
    "Scénario défavorable": "Adverse scenario",
    "1 chance sur 20 de faire pire": "1 in 20 chance of doing worse",
    "Scénario médian": "Median scenario",
    "1 chance sur 2 de faire mieux": "1 in 2 chance of doing better",
    "Scénario favorable": "Favourable scenario",
    "1 chance sur 20 de faire mieux": "1 in 20 chance of doing better",
    "Probabilité de perte": "Probability of loss",
    "Sous {montant} investis": "Below {montant} invested",
    "Part des scénarios qui finissent sous la valeur de départ + versements":
        "Share of scenarios ending below the starting value + contributions",
    "Objectif atteint": "Target reached",
    "Objectif : {montant}": "Target: {montant}",
    "Affichage": "Display",
    "Éventail": "Fan chart",
    "Nuage de points": "Scatter plot",
    "Les deux": "Both",
    "Nuage de points : chaque point est un scénario, coloré selon sa tranche de probabilité.":
        "Scatter plot: each dot is a scenario, coloured by probability band.",
    "Projection sur {n} ans": "{n}-year projection",
    "{n} scénarios simulés · zones : 50 % et 90 % des scénarios":
        "{n} simulated scenarios · bands: 50% and 90% of scenarios",
    "Scénarios par tranche de probabilité": "Scenarios by probability band",
    "{n} scénarios affichés · rouge = défavorable, gris = central, bleu = favorable · "
    "survoler un point pour le détail":
        "{n} scenarios shown · red = adverse, grey = central, blue = favourable · hover over a dot for details",
    "Distribution de la valeur finale": "Distribution of the final value",
    "Comment lire cette projection ?": "How to read this projection",
    "- Chaque scénario est un **futur possible**, tiré au hasard mais cohérent avec le rendement et "
    "le risque choisis.\n"
    "- La **médiane** n'est pas une prévision : c'est le milieu des possibles.\n"
    "- L'écart entre scénarios défavorable et favorable **grandit avec l'horizon** : c'est "
    "l'incertitude qui s'accumule.\n"
    "- La méthode **historique** conserve les vrais krachs du portefeuille ; la **loi normale** "
    "les sous-estime.":
        "- Each scenario is a **possible future**, drawn at random but consistent with the chosen "
        "return and risk.\n"
        "- The **median** is not a forecast: it is the middle of the possible outcomes.\n"
        "- The gap between adverse and favourable scenarios **widens with the horizon**: "
        "uncertainty accumulates.\n"
        "- The **historical** method preserves the portfolio's real crashes; the **normal "
        "distribution** underestimates them.",
    "Une projection n'est pas une prévision : elle suppose que les hypothèses se vérifient, ce qui "
    "n'est jamais garanti.":
        "A projection is not a forecast: it assumes the assumptions hold, which is never guaranteed.",

    # Transactions
    "Historique des opérations": "Transaction history",
    "Type": "Type",
    "Titres": "Securities",
    "Tous les titres": "All securities",
    "{n} opération(s) affichée(s) sur {total}": "{n} of {total} transaction(s) shown",
    "Prix / montant (€)": "Price / amount (€)",
    "Frais": "Fees",
    "Prix en devise": "Price in currency",
    "Prix saisi, avant conversion en euros": "Price entered, before conversion into euros",
    "Télécharger la sélection (CSV)": "Download the selection (CSV)",

    # ------------------------------------------------------------------
    # Briques visuelles (interface.py)
    # ------------------------------------------------------------------
    "Risque plus faible": "Lower risk",
    "Risque plus élevé": "Higher risk",
    "Critère": "Criterion",
    "Limite du profil": "Profile limit",
    "Statut": "Status",
    "Conforme": "Compliant",
    "Dépassé": "Exceeded",

    # ------------------------------------------------------------------
    # Graphiques (graphiques_interactifs.py)
    # ------------------------------------------------------------------
    "1A": "1Y",
    "Tout": "All",
    "Argent investi (apports nets)": "Money invested (net contributions)",
    "Valeur du portefeuille": "Portfolio value",
    "Investi": "Invested",
    "Autres ({n} lignes)": "Others ({n} holdings)",
    "Indice": "Index",
    "Max drawdown : {valeur}": "Max drawdown: {valeur}",
    "Rendement %{x:.2%}<br>%{y} jours": "Return %{x:.2%}<br>%{y} days",
    "Jours": "Days",
    "Rendement quotidien": "Daily return",
    "Nombre de jours": "Number of days",
    "Portefeuilles aléatoires": "Random portfolios",
    "Volatilité %{x:.1%}<br>Rendement %{y:.1%}": "Volatility %{x:.1%}<br>Return %{y:.1%}",
    "Droite de marché des capitaux": "Capital market line",
    "Frontière": "Frontier",
    "Titres seuls": "Individual securities",
    "Volatilité annuelle": "Annual volatility",
    "Rendement annuel espéré": "Expected annual return",
    "90 % des scénarios": "90% of scenarios",
    "50 % des scénarios": "50% of scenarios",
    "Argent investi": "Money invested",
    "Médiane {v}<br>Fourchette 90 % : {bas} – {haut}": "Median {v}<br>90% range: {bas} – {haut}",
    "Objectif": "Target",
    "%{y} scénarios": "%{y} scenarios",
    "Médiane": "Median",
    "Valeur finale": "Final value",
    "Nombre de scénarios": "Number of scenarios",
    "Scénario n° %{customdata[1]} · %{customdata[0]}": "Scenario no. %{customdata[1]} · %{customdata[0]}",
    "Seuil des 95 %": "95% threshold",
    "95e percentile : {v}": "95th percentile: {v}",
    "Médiane : {v}": "Median: {v}",
    "Seuil des 5 %": "5% threshold",
    "5e percentile : {v}": "5th percentile: {v}",
    "Investi : {v}": "Invested: {v}",
    "Sortie dans %{{x}} an(s) : {v}": "Exit in %{{x}} year(s): {v}",
    "Années avant la sortie": "Years until exit",
    "Gain net d'impôts": "Gain net of tax",
    "Part de la valeur": "Share of value",
    "%{y} : %{x:.1%} de la valeur": "%{y}: %{x:.1%} of value",
    "Part du risque": "Share of risk",
    "%{y} : %{x:.1%} du risque": "%{y}: %{x:.1%} of risk",
    "Allocation": "Allocation",
    "Sélection": "Selection",
    "Interaction": "Interaction",

    # ------------------------------------------------------------------
    # Espace "Conseil patrimonial" (vues_conseil.py)
    # ------------------------------------------------------------------
    "Profil client": "Client profile",
    "Fiscalité": "Taxation",
    "Stress tests": "Stress tests",
    "Questionnaire client": "Client questionnaire",
    "Inspiré du test d'adéquation MiFID II · 7 questions": "Based on the MiFID II suitability test · 7 questions",
    "Profil du client": "Client profile",
    "Risque du portefeuille": "Portfolio risk",
    "Volatilité {valeur}": "Volatility {valeur}",
    "Le score correspond au profil « {profil} », mais la perte maximale acceptée plafonne le profil : "
    "le critère le plus prudent l'emporte.":
        "The score corresponds to the \"{profil}\" profile, but the maximum acceptable loss caps the "
        "profile: the most prudent criterion prevails.",
    "Portefeuille adapté au profil": "Portfolio suitable for this profile",
    "Portefeuille trop risqué pour ce profil": "Portfolio too risky for this profile",
    "Pour respecter le profil, conserver environ {part} du capital sur ce portefeuille et placer "
    "{reste} sur un support sans risque (fonds en euros, monétaire).":
        "To comply with the profile, keep about {part} of the capital in this portfolio and invest "
        "{reste} in a risk-free asset (capital-guaranteed fund, money market).",
    "Indicateur de risque (SRI)": "Summary risk indicator (SRI)",
    "Échelle PRIIPs de 1 à 7, estimée à partir de la volatilité": "PRIIPs scale from 1 to 7, estimated from volatility",
    "Test d'adéquation": "Suitability test",
    " (le reste : obligations, or)": " (the rest: bonds, gold)",
    "Part investie en actions (ETF actions compris) : {part}{reste}. Le SRI réglementaire se calcule "
    "à partir de la VaR (Cornish-Fisher) : la volatilité en donne ici une approximation.":
        "Share invested in equities (including equity ETFs): {part}{reste}. The regulatory SRI is "
        "computed from the VaR (Cornish-Fisher): volatility gives an approximation here.",
    "Hypothèses": "Assumptions",
    "Portefeuille ouvert le {date} (ancienneté : {n} ans) · taux 2026":
        "Portfolio opened on {date} (age: {n} years) · 2026 rates",
    "Situation familiale (abattement assurance-vie)": "Marital status (life insurance allowance)",
    "Rendement annuel supposé pour les sorties futures (%)": "Assumed annual return for future exits (%)",
    "Pas d'avantage lié à la durée": "No holding-period advantage",
    "Avantage fiscal acquis": "Tax advantage reached",
    "Avantage fiscal dans {n} an(s)": "Tax advantage in {n} year(s)",
    "Sortie {enveloppe}": "Exit {enveloppe}",
    "impôts {taux}": "tax {taux}",
    "Si tout était vendu aujourd'hui": "If everything were sold today",
    "Gain brut : {montant}": "Gross gain: {montant}",
    "Enveloppe": "Account type",
    "Gain brut": "Gross gain",
    "Impôt sur le revenu": "Income tax",
    "Prélèvements sociaux": "Social contributions",
    "Gain net": "Net gain",
    "Performance brute": "Gross return",
    "Performance nette": "Net return",
    "Gain net selon l'année de sortie": "Net gain by exit year",
    "Hypothèse : {taux} par an · sauts : 5 ans pour le PEA, 8 ans pour l'assurance-vie":
        "Assumption: {taux} per year · steps: 5 years for the PEA, 8 years for life insurance",
    "Éligibilité au PEA": "PEA eligibility",
    "Actions européennes (UE / EEE) et fonds éligibles": "European equities (EU / EEA) and eligible funds",
    "Part éligible au PEA": "PEA-eligible share",
    "{n} ligne(s) non éligible(s)": "{n} ineligible holding(s)",
    "Seule la part éligible peut être logée dans un PEA ; le reste irait sur un compte-titres ou en "
    "unités de compte d'assurance-vie.":
        "Only the eligible share can be held in a PEA; the rest would go into a securities account or "
        "unit-linked life insurance.",
    "Le montant investi dépasse le plafond de versements du PEA (150 000 €) et le seuil de 150 000 € "
    "de primes au-delà duquel l'assurance-vie est taxée à 12,8 % au lieu de 7,5 % après 8 ans (non modélisé).":
        "The amount invested exceeds the PEA contribution cap (€150,000) and the €150,000 premium "
        "threshold above which life insurance is taxed at 12.8% instead of 7.5% after 8 years (not modelled).",
    "Taux 2026 : flat tax de 31,4 % (12,8 % + 18,6 % de prélèvements sociaux) ; assurance-vie : "
    "prélèvements sociaux maintenus à 17,2 %.":
        "2026 rates: 31.4% flat tax (12.8% income tax + 18.6% social contributions); life insurance: "
        "social contributions kept at 17.2%.",
    "Rejeu des crises passées (historique depuis 2008)...": "Replaying past crises (history since 2008)...",
    "Stress tests indisponibles : {erreur}": "Stress tests unavailable: {erreur}",
    "Pire scénario historique": "Worst historical scenario",
    "Perte correspondante": "Corresponding loss",
    "Sur {montant} aujourd'hui": "On {montant} today",
    "Bêta du portefeuille": "Portfolio beta",
    "Sensibilité aux marchés actions": "Sensitivity to equity markets",
    "Crises passées rejouées sur le portefeuille actuel": "Past crises replayed on the current portfolio",
    "Variation du plus haut au plus bas du marché": "Change from market peak to trough",
    "Chocs hypothétiques": "Hypothetical shocks",
    "Actions : bêta × choc · Dollar : part investie en dollars · Taux : duration":
        "Equities: beta × shock · Dollar: share invested in dollars · Rates: duration",
    "Détail des scénarios historiques": "Historical scenarios in detail",
    "Scénario": "Scenario",
    "Variation": "Change",
    "Gain / perte": "Gain / loss",
    "Part estimée par un indice": "Share estimated with an index",
    "Voir le détail ligne par ligne": "Show the detail by holding",
    "Source": "Source",
    "Quand un titre n'était pas encore coté, l'indice boursier de sa région (ou un fonds obligataire "
    "de même catégorie) sert d'approximation. Variations en devise locale, hors dividendes. "
    "Données : {source}.":
        "When a security was not yet listed, its regional stock index (or a bond fund of the same "
        "category) is used as a proxy. Changes in local currency, excluding dividends. Data: {source}.",

    # ------------------------------------------------------------------
    # Espace "Gestion d'actifs" (vues_gestion.py)
    # ------------------------------------------------------------------
    "Attribution de performance": "Performance attribution",
    "Budget de risque": "Risk budget",
    "Backtest de stratégies": "Strategy backtest",
    "Attribution de performance (téléchargement des indices régionaux)...":
        "Performance attribution (downloading regional indices)...",
    "Attribution indisponible : {erreur}": "Attribution unavailable: {erreur}",
    "Rendement des positions (composé)": "Return of the holdings (compounded)",
    "MSCI ACWI (poids régionaux)": "MSCI ACWI (regional weights)",
    "Écart": "Difference",
    "Effet allocation": "Allocation effect",
    "Choix des régions": "Choice of regions",
    "Effet sélection": "Selection effect",
    "Choix des titres": "Choice of securities",
    "Effet interaction": "Interaction effect",
    "Effet croisé": "Cross effect",
    "Portefeuille diversifié : l'attribution porte sur la poche actions ({part} du portefeuille "
    "aujourd'hui), comparée à un indice actions. Les obligations et l'or sont exclus du calcul.":
        "Diversified portfolio: the attribution covers the equity sleeve ({part} of the portfolio today), "
        "compared with an equity index. Bonds and gold are excluded from the calculation.",
    "{part} du portefeuille n'est pas classé dans une région de l'indice (ETF monde, titres absents du "
    "référentiel) : l'attribution est surtout pertinente pour un portefeuille de lignes directes comme "
    "le fonds actions monde.":
        "{part} of the portfolio is not assigned to an index region (global ETF, securities missing from "
        "the reference file): attribution is mostly relevant for a portfolio of direct holdings such as "
        "the global equity fund.",
    "Effets par région": "Effects by region",
    "La somme de tous les effets est égale à l'écart avec l'indice":
        "The sum of all effects equals the difference with the index",
    "Effets cumulés dans le temps": "Cumulative effects over time",
    "Lissage de Cariño": "Cariño smoothing",
    "Détail par région": "Detail by region",
    "Poids portefeuille": "Portfolio weight",
    "Poids indice": "Index weight",
    "Rendement portefeuille": "Portfolio return",
    "Rendement indice": "Index return",
    "Lecture : un effet d'allocation positif signifie que le portefeuille a surpondéré des régions qui "
    "ont fait mieux que l'indice ; un effet de sélection positif, qu'il a choisi dans une région des "
    "titres qui ont fait mieux que l'indice de cette région. Indices régionaux hors dividendes, "
    "convertis en euros.":
        "How to read: a positive allocation effect means the portfolio overweighted regions that beat the "
        "index; a positive selection effect means it picked securities that beat their regional index. "
        "Regional price indices (excluding dividends), converted into euros.",
    "Calcul du budget de risque...": "Computing the risk budget...",
    "Budget de risque indisponible : {erreur}": "Risk budget unavailable: {erreur}",
    "Estimée sur l'historique": "Estimated from history",
    "Ratio de diversification": "Diversification ratio",
    "1 = aucune diversification": "1 = no diversification",
    "Nombre effectif de paris": "Effective number of bets",
    "pour {n} lignes": "for {n} holdings",
    "Plus gros contributeur": "Largest contributor",
    "{nom} ({part} de la valeur)": "{nom} ({part} of value)",
    "Part de la valeur et part du risque": "Share of value and share of risk",
    "Les 20 plus gros contributeurs au risque": "The 20 largest risk contributors",
    "Une ligne dont la part du risque dépasse sa part de la valeur est plus volatile ou plus corrélée "
    "au reste du portefeuille que la moyenne.":
        "A holding whose share of risk exceeds its share of value is more volatile, or more correlated "
        "with the rest of the portfolio, than average.",
    "Quatre façons de répartir les mêmes titres": "Four ways to allocate the same securities",
    "La parité des risques égalise la contribution de chaque ligne au risque":
        "Risk parity equalises each holding's contribution to risk",
    "Rendement espéré": "Expected return",
    "Contribution maximale": "Largest contribution",
    "Voir les poids de chaque allocation": "Show the weights of each allocation",
    "Paramètres": "Settings",
    "Mêmes titres et mêmes poids de départ que le portefeuille actuel":
        "Same securities and same starting weights as the current portfolio",
    "Frais de transaction (%)": "Transaction costs (%)",
    "Capital pour la comparaison DCA (€)": "Capital for the DCA comparison (€)",
    "Durée de l'investissement progressif (mois)": "Length of the gradual investment (months)",
    "Backtest des stratégies...": "Backtesting strategies...",
    "Backtest indisponible : {erreur}": "Backtest unavailable: {erreur}",
    "Rééquilibrer ou non ?": "Rebalance or not?",
    "Base 100 · frais de {frais} par transaction": "Rebased to 100 · {frais} cost per transaction",
    "Résultats": "Results",
    "Stratégie": "Strategy",
    "Rendement annualisé": "Annualised return",
    "Rotation / an": "Turnover / year",
    "Rééquilibrer revient à vendre ce qui a monté pour acheter ce qui a baissé : cela maintient le "
    "risque voulu, mais coûte des frais et peut freiner la performance quand une tendance dure.":
        "Rebalancing means selling what has risen to buy what has fallen: it keeps the intended risk "
        "level, but costs fees and can hold back performance when a trend persists.",
    "Investir en une fois ou progressivement ?": "Invest all at once or gradually?",
    "{montant} investis dès le premier jour ou en {n} versements mensuels":
        "{montant} invested on day one or in {n} monthly instalments",
    "Comparaison": "Comparison",
    "Gain": "Gain",
    "Valeur la plus basse": "Lowest value",
    "Sur un marché haussier, investir en une fois rapporte en général davantage ; l'investissement "
    "progressif réduit le risque d'investir juste avant une baisse. L'argent en attente est rémunéré "
    "au taux sans risque.":
        "In a rising market, investing all at once usually earns more; investing gradually reduces the "
        "risk of investing just before a fall. Cash waiting to be invested earns the risk-free rate.",
}

# ----------------------------------------------------------------------
# Données issues des calculs (traduites à l'affichage avec td())
# ----------------------------------------------------------------------
DONNEES = {
    # Classes d'actifs
    "Actions": "Equities", "Obligations": "Bonds", "Or": "Gold",
    # Régions
    "États-Unis": "United States", "Europe": "Europe", "Royaume-Uni": "United Kingdom",
    "Suisse": "Switzerland", "Japon": "Japan", "Asie-Pacifique": "Asia-Pacific", "Canada": "Canada",
    "Émergents": "Emerging markets", "Monde (ETF)": "World (ETF)", "Monde": "World",
    "Non classé": "Unclassified",
    # Secteurs
    "Technologie": "Technology", "Consommation discrétionnaire": "Consumer discretionary",
    "Communication": "Communication services", "Finance": "Financials", "Santé": "Health care",
    "Consommation de base": "Consumer staples", "Énergie": "Energy", "Industrie": "Industrials",
    "Services publics": "Utilities", "Matériaux": "Materials", "Immobilier": "Real estate",
    "ETF diversifié": "Diversified ETF", "Obligations d'État": "Government bonds",
    "Obligations indexées sur l'inflation": "Inflation-linked bonds",
    "Obligations d'entreprises": "Corporate bonds", "Obligations à haut rendement": "High-yield bonds",
    "Obligations émergentes": "Emerging-market bonds",
    # Types d'opérations
    "ACHAT": "BUY", "VENTE": "SELL", "DIVIDENDE": "DIVIDEND",
    # Profils de risque
    "Sécuritaire": "Conservative", "Prudent": "Cautious", "Équilibré": "Balanced",
    "Dynamique": "Dynamic", "Offensif": "Aggressive",
    "Priorité absolue à la préservation du capital.": "Capital preservation comes first.",
    "Recherche de régularité, faible tolérance aux baisses.": "Seeks steady returns, low tolerance for declines.",
    "Compromis entre rendement et sécurité.": "A balance between return and safety.",
    "Recherche de performance, accepte des baisses marquées.": "Seeks performance, accepts significant declines.",
    "Rendement maximal sur le long terme, forte tolérance au risque.":
        "Maximum long-term return, high risk tolerance.",
    # Critères du test d'adéquation
    "Volatilité annuelle": "Annual volatility", "Pire baisse historique": "Worst historical decline",
    "Part d'actions": "Equity share", "Indicateur de risque (SRI)": "Risk indicator (SRI)",
    # Questionnaire client
    "Horizon de placement": "Investment horizon",
    "Moins de 2 ans": "Less than 2 years", "2 à 5 ans": "2 to 5 years", "5 à 8 ans": "5 to 8 years",
    "8 à 15 ans": "8 to 15 years", "Plus de 15 ans": "More than 15 years",
    "Objectif principal": "Main objective",
    "Préserver le capital": "Preserve capital", "Obtenir des revenus réguliers": "Earn regular income",
    "Croissance modérée": "Moderate growth", "Croissance du capital": "Capital growth",
    "Rendement maximal": "Maximum return",
    "Si vos placements baissaient de 20 % en 3 mois, vous…": "If your investments fell by 20% in 3 months, you would…",
    "Vendez tout": "Sell everything", "Vendez une partie": "Sell part of them",
    "Attendez sans rien faire": "Wait and do nothing", "Conservez sans inquiétude": "Hold without worrying",
    "Rachetez à bon prix": "Buy more at a good price",
    "Perte maximale acceptable sur une année": "Maximum acceptable loss over one year",
    "0 à 5 %": "0 to 5%", "5 à 10 %": "5 to 10%", "10 à 20 %": "10 to 20%", "20 à 30 %": "20 to 30%",
    "Plus de 30 %": "More than 30%",
    "Connaissance et expérience des marchés actions": "Knowledge and experience of equity markets",
    "Aucune": "None", "Notions générales": "General notions",
    "Placements en fonds (OPCVM, ETF)": "Investments in funds (mutual funds, ETFs)",
    "Investissement régulier en actions": "Regular investment in equities",
    "Expérience professionnelle": "Professional experience",
    "Part de votre patrimoine financier placée ici": "Share of your financial wealth invested here",
    "Plus de 75 %": "More than 75%", "50 à 75 %": "50 to 75%", "25 à 50 %": "25 to 50%",
    "10 à 25 %": "10 to 25%", "Moins de 10 %": "Less than 10%",
    "Épargne de précaution (3 à 6 mois de dépenses) disponible par ailleurs":
        "Emergency savings (3 to 6 months of expenses) available elsewhere",
    "Non": "No", "En partie": "Partly", "Oui": "Yes",
    # Fiscalité
    "CTO": "Securities account (CTO)", "PEA": "PEA (equity savings plan)", "Assurance-vie": "Life insurance",
    "célibataire": "single", "couple": "couple",
    # Stress tests
    "Crise financière (2008-2009)": "Financial crisis (2008-2009)",
    "Crise de la dette européenne (2011)": "European debt crisis (2011)",
    "Krach du Covid (2020)": "Covid crash (2020)",
    "Inflation et hausse des taux (2022)": "Inflation and rate hikes (2022)",
    "Mini-krach d'août 2024": "August 2024 mini-crash",
    "titre": "security",
    # Backtest et budget de risque
    "Achat-conservation": "Buy and hold", "Rééquilibrage mensuel": "Monthly rebalancing",
    "Rééquilibrage trimestriel": "Quarterly rebalancing", "Rééquilibrage annuel": "Annual rebalancing",
    "En une fois": "All at once",
    "Portefeuille actuel": "Current portfolio", "Équipondéré": "Equal weight",
    "Parité des risques": "Risk parity", "Variance minimale": "Minimum variance",
    # Tranches de probabilité (Monte-Carlo)
    "5 % les plus défavorables": "Worst 5%", "Défavorable (5 à 25 %)": "Adverse (5 to 25%)",
    "Central (25 à 75 %)": "Central (25 to 75%)", "Favorable (75 à 95 %)": "Favourable (75 to 95%)",
    "5 % les plus favorables": "Best 5%",
}

# Données contenant un nombre variable : (expression régulière, remplacement)
MOTIFS = [
    (r"Progressif \((\d+) mois\)", r"Gradual (\1 months)"),
    (r"Baisse des actions de (\d+) ?%", r"Equities fall by \1%"),
    (r"Baisse du dollar de (\d+) ?%", r"Dollar falls by \1%"),
    (r"Hausse des taux de (\d+) points?", r"Interest rates rise by \1 point"),
    (r"indice (.+)", r"index \1"),
]
