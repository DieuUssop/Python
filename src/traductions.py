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
    "Ou envoyer un autre fichier (CSV ou Excel)": "Or upload another file (CSV or Excel)",
    "Colonnes : date, type (ACHAT, VENTE, DIVIDENDE), ticker (code Yahoo Finance), nom, quantite, prix, frais. "
    "CSV à virgules ou à points-virgules, ou fichier Excel. Prioritaire sur le portefeuille choisi ci-dessus.":
        "Columns: date, type (ACHAT/BUY, VENTE/SELL, DIVIDENDE/DIVIDEND), ticker (Yahoo Finance code), nom (name), "
        "quantite (quantity), prix (price), frais (fees). Comma- or semicolon-separated CSV, or Excel file. "
        "Takes priority over the portfolio selected above.",
    "Télécharger un modèle de fichier": "Download a template file",
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
    # ------------------------------------------------------------------
    # Assistant d'import (vues_import.py)
    # ------------------------------------------------------------------
    "Ouvrir l'assistant d'import": "Open the import assistant",
    "Pour indiquer vous-même comment lire le fichier envoyé": "To specify yourself how to read the uploaded file",
    "Assistant d'import": "Import assistant",
    "Fichier : {nom}": "File: {nom}",
    "Ce fichier n'est pas au format du projet, ou il contient des codes ISIN. Indiquez ci-dessous comment le "
    "lire : l'outil propose une correspondance, il suffit de la vérifier.":
        "This file is not in the project format, or it contains ISIN codes. Specify below how to read it: "
        "the tool suggests a mapping, you just need to check it.",
    "Pourquoi l'assistant s'ouvre-t-il ?": "Why is the assistant opening?",
    "Fichier illisible : {erreur}": "Unreadable file: {erreur}",
    "1. Le fichier": "1. The file",
    "Choisir la feuille et la ligne qui contient les titres de colonnes":
        "Choose the sheet and the row that contains the column headers",
    "Feuille Excel": "Excel sheet",
    "Ligne des titres de colonnes": "Header row",
    # Détection automatique et devises
    "Lecture du fichier et vérification des prix avec les cours du marché...":
        "Reading the file and checking prices against market data...",
    "Vérification des prix avec les cours du marché...": "Checking prices against market data...",
    "montants en euros convertis": "amounts in euros converted",
    "prix en {devise} convertis dans l'unité de cotation": "prices in {devise} converted to the quotation unit",
    "Fichier reconnu automatiquement : {n} opération(s), {titres} titre(s).":
        "File recognised automatically: {n} transaction(s), {titres} security(ies).",
    "Prix non vérifiés avec les cours du marché (pas de connexion).":
        "Prices not checked against market data (no connection).",
    "{ticker} : {n} prix éloigné(s) du cours du jour (écart médian {ecart}) — ticker, devise ou division "
    "d'actions à vérifier.":
        "{ticker}: {n} price(s) far from that day's market price (median gap {ecart}) — check the ticker, "
        "currency or a stock split.",
    "Colonnes identifiées d'après leur contenu (pas de ligne de titres).":
        "Columns identified from their content (no header row).",
    "{n} code(s) ISIN, Bloomberg ou nom(s) convertis en tickers.":
        "{n} ISIN, Bloomberg code(s) or name(s) converted into tickers.",
    "{n} ticker(s) sans place de cotation identifié(s) grâce aux cours.":
        "{n} ticker(s) without an exchange identified from market prices.",
    "converti (Bloomberg, Google, Reuters)": "converted (Bloomberg, Google, Reuters)",
    "Place de cotation": "Exchange",
    "Dates lues au format jour/mois (JJ/MM).": "Dates read as day/month (DD/MM).",
    "Dates lues au format américain (MM/JJ).": "Dates read in US format (MM/DD).",
    "{n} ligne(s) ignorée(s) (frais de garde, virements...).": "{n} row(s) ignored (custody fees, transfers...).",
    "Devise des prix du fichier": "Currency of the prices in the file",
    "Détection automatique (recommandé)": "Automatic detection (recommended)",
    "Devise de cotation de chaque titre": "Trading currency of each security",
    "Tout est en euros": "Everything is in euros",
    "La détection compare chaque prix au vrai cours de clôture du jour, en dollars, livres, euros... et garde "
    "la lecture la plus proche.":
        "Detection compares each price with that day's actual closing price, in dollars, pounds, euros... and "
        "keeps the closest reading.",
    "Numéro de la ligne du fichier où se trouvent les noms des colonnes (détecté automatiquement). 0 = le "
    "fichier n'a pas de ligne de titres.":
        "Row number in the file where the column names are (detected automatically). 0 = the file has no "
        "header row.",
    "Aperçu des premières lignes ({n} lignes au total)": "Preview of the first rows ({n} rows in total)",
    "2. Correspondance des colonnes": "2. Column mapping",
    "Pour chaque information, la colonne de votre fichier qui la contient (* = obligatoire)":
        "For each item, the column of your file that contains it (* = required)",
    "— aucune —": "— none —",
    "Date de l'opération": "Transaction date",
    "Type d'opération": "Transaction type",
    "Titre (ticker, ISIN ou nom)": "Security (ticker, ISIN or name)",
    "Nom du titre": "Security name",
    "Prix unitaire": "Unit price",
    "Montant total": "Total amount",
    "Le montant total inclut les frais (montant net débité ou crédité)":
        "The total amount includes fees (net amount debited or credited)",
    "Sert à retrouver le prix unitaire quand il n'est pas donné : achat = quantité × prix + frais ; "
    "vente = quantité × prix − frais.":
        "Used to work out the unit price when it is not given: buy = quantity × price + fees; "
        "sell = quantity × price − fees.",
    "À indiquer : {champs}. Pour le prix, une colonne « Prix unitaire » ou « Montant total » suffit.":
        "Still needed: {champs}. For the price, either a \"Unit price\" or a \"Total amount\" column is enough.",
    "Sans colonne « Type d'opération » : une quantité négative est lue comme une vente, une quantité "
    "positive comme un achat.":
        "Without a \"Transaction type\" column: a negative quantity is read as a sale, a positive quantity "
        "as a purchase.",
    "3. Types d'opération et titres": "3. Transaction types and securities",
    "Vérifier l'interprétation proposée ; les cellules modifiables sont en blanc":
        "Check the suggested interpretation; editable cells are white",
    "Dans le fichier": "In the file",
    "Lignes": "Rows",
    "Interprétation": "Interpretation",
    "Ignorer la ligne": "Ignore the row",
    "Recherche des tickers Yahoo Finance...": "Looking up Yahoo Finance tickers...",
    "Ticker Yahoo Finance": "Yahoo Finance ticker",
    "Modifiable : par exemple MC.PA pour LVMH à Paris": "Editable: for example MC.PA for LVMH in Paris",
    "Nom trouvé": "Name found",
    "tel quel": "as is",
    "trouvé": "found",
    "introuvable": "not found",
    "Titres introuvables : saisir leur ticker à la main (recherche sur finance.yahoo.com), sinon leurs "
    "lignes seront ignorées.":
        "Securities not found: enter their ticker manually (search on finance.yahoo.com), otherwise their "
        "rows will be ignored.",
    "4. Résultat": "4. Result",
    "Transactions au format du projet": "Transactions in the project format",
    "{n} ligne(s) ignorée(s) : opérations d'un autre type (frais de garde, virements...)":
        "{n} row(s) ignored: other kinds of operations (custody fees, transfers...)",
    "{n} ligne(s) avec {motif} (lignes {lignes}) : ignorée(s)": "{n} row(s) with {motif} (rows {lignes}): ignored",
    "date illisible": "an unreadable date",
    "prix ou montant manquant": "a missing price or amount",
    "quantité nulle": "a zero quantity",
    "titre manquant": "a missing security",
    "{n} transaction(s) · {titres} titre(s)": "{n} transaction(s) · {titres} security(ies)",
    "Analyser ce portefeuille": "Analyse this portfolio",
    "Télécharger le fichier converti (format du projet)": "Download the converted file (project format)",

    # ------------------------------------------------------------------
    # Espace personnel et comptes (vues_compte.py, comptes.py)
    # ------------------------------------------------------------------
    "Vos portefeuilles enregistrés, puis les portefeuilles d'exemple du projet":
        "Your saved portfolios, then the project's sample portfolios",
    "Mon espace · {nom}": "My space · {nom}",
    "Déconnexion automatique après 30 minutes d'inactivité.": "Automatically signed out after 30 minutes of inactivity.",
    "Mon espace": "My space",
    "Connecté : {identifiant}": "Signed in: {identifiant}",
    "Mon compte": "My account",
    "Déconnexion": "Sign out",
    "Se connecter ou créer un compte": "Sign in or create an account",
    "Action": "Action",
    "Enregistrer dans mon espace": "Save to my space",
    "Nom du portefeuille": "Portfolio name",
    "Enregistrer": "Save",
    "« {nom} » est enregistré dans votre espace (chiffré).": "\"{nom}\" has been saved to your space (encrypted).",
    "Vos portefeuilles sont chiffrés avec une clé tirée de votre mot de passe : personne d'autre (ni les autres "
    "utilisateurs, ni l'administrateur) ne peut les lire.":
        "Your portfolios are encrypted with a key derived from your password: nobody else (neither other users "
        "nor the administrator) can read them.",
    "Identifiant": "Username",
    "Mot de passe": "Password",
    "Mes portefeuilles": "My portfolios",
    "Aucun portefeuille enregistré pour l'instant : ajoutez-en un ci-dessus.":
        "No saved portfolio yet: add one above.",
    "Pour garder ce fichier, connectez-vous ou créez un compte (« Mon espace », en haut de la barre latérale).":
        "To keep this file, log in or create an account (\"My space\", at the top of the sidebar).",
    "Ajouter un portefeuille": "Add a portfolio",
    "Fichier CSV ou Excel, de n'importe quel format": "CSV or Excel file, in any layout",
    "Fichier à enregistrer": "File to save",
    "{n} opération(s) reconnue(s).": "{n} transaction(s) recognised.",
    "Ce fichier n'a pas pu être lu automatiquement. Envoyez-le depuis la barre latérale (« Ou envoyer un autre fichier ») : l'assistant d'import vous guidera, puis le bouton « Enregistrer dans mon espace » apparaîtra sous l'envoi.":
        "This file could not be read automatically. Upload it from the sidebar (\"Or upload another file\"): the "
        "import assistant will guide you, then the \"Save to my space\" button will appear below the upload.",
    "Nom": "Name",
    "{n} opération(s) · modifié le {date}": "{n} transaction(s) · updated on {date}",
    "Télécharger": "Download",
    "Confirmer": "Confirm",
    "Supprimer": "Delete",
    "Changer de mot de passe": "Change password",
    "Vos portefeuilles sont rechiffrés avec le nouveau": "Your portfolios are re-encrypted with the new one",
    "Mot de passe actuel": "Current password",
    "Nouveau mot de passe": "New password",
    "Confirmer le mot de passe": "Confirm password",
    "Supprimer mon compte": "Delete my account",
    "Efface définitivement le compte et tous ses portefeuilles (droit à l'effacement, RGPD)":
        "Permanently erases the account and all its portfolios (right to erasure, GDPR)",
    "Supprimer définitivement mon compte": "Permanently delete my account",
    "Version en ligne de démonstration : les comptes et portefeuilles enregistrés ici peuvent être effacés au "
    "redémarrage du site. Pour les conserver, utilisez l'application sur votre ordinateur.":
        "Online demo version: accounts and portfolios saved here may be erased when the site restarts. To keep "
        "them, use the application on your computer.",
    "Vos portefeuilles seront chiffrés avec votre mot de passe. S'il est oublié, ils seront définitivement "
    "illisibles, y compris pour l'administrateur.":
        "Your portfolios will be encrypted with your password. If you forget it, they will be permanently "
        "unreadable, including for the administrator.",
    "Se connecter": "Sign in",
    "Créer mon compte": "Create my account",
    "Créer un compte": "Create an account",
    "Vérification...": "Checking...",
    "Mot de passe modifié.": "Password changed.",
    "Compte et données supprimés.": "Account and data deleted.",
    "Identifiant invalide : 3 à 30 caractères parmi lettres minuscules, chiffres, « . », « _ » et « - ».":
        "Invalid username: 3 to 30 characters among lowercase letters, digits, \".\", \"_\" and \"-\".",
    "Le mot de passe doit contenir au moins {n} caractères.": "The password must be at least {n} characters long.",
    "Les deux mots de passe ne sont pas identiques.": "The two passwords do not match.",
    "Cet identifiant est déjà utilisé.": "This username is already taken.",
    "Identifiant ou mot de passe incorrect.": "Incorrect username or password.",
    "Trop d'essais ratés : réessayez dans {n} secondes.": "Too many failed attempts: try again in {n} seconds.",
    "Portefeuille introuvable.": "Portfolio not found.",
    "Mot de passe actuel incorrect.": "Current password is incorrect.",
    "Mot de passe incorrect.": "Incorrect password.",
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


# ======================================================================
# Ajouts : expositions, carte du monde, indices, PDF, nouvelles opérations
# ======================================================================
TEXTES.update({
    # --- Diagnostic d'exposition (src/expositions.py) ---
    "{poids} du portefeuille est exposé à des devises étrangères, dont {devise} pour {poids_devise}.":
        "{poids} of the portfolio is exposed to foreign currencies, including {devise} for {poids_devise}.",
    "Une baisse de ces devises face à l'euro réduit la performance, même si les titres montent : une baisse de 10 % du dollar coûterait environ {perte} au portefeuille.":
        "A fall of these currencies against the euro reduces performance even if the securities rise: a 10% "
        "drop in the dollar would cost the portfolio about {perte}.",
    "Pour une partie de la poche, choisir des ETF couverts en euros (« EUR Hedged »).":
        "For part of the allocation, choose euro-hedged ETFs (\"EUR Hedged\").",
    "Le risque de change diversifie aussi : le dollar monte souvent en période de crise. Couvrir partiellement est un compromis courant.":
        "Currency risk also diversifies: the dollar often rises in a crisis. Partial hedging is a common compromise.",
    "Risque de change limité : {poids} hors euro.": "Limited currency risk: {poids} outside the euro.",
    "Une seule action, {nom}, représente {poids} du portefeuille.": "A single stock, {nom}, makes up {poids} of the portfolio.",
    "Le risque propre à une entreprise (résultats, procès, scandale) n'est pas diversifié : une chute de 30 % de ce titre coûterait {perte} au portefeuille.":
        "Company-specific risk (earnings, lawsuits, scandals) is not diversified: a 30% fall in this stock would "
        "cost the portfolio {perte}.",
    "Réduire la ligne progressivement ou la compléter par des titres du même secteur.":
        "Reduce the position gradually or complement it with other stocks from the same sector.",
    "Repère réglementaire : un fonds UCITS ne peut pas dépasser 10 % sur un émetteur.":
        "Regulatory benchmark: a UCITS fund may not exceed 10% in a single issuer.",
    "Les {n} actions de plus de 5 % totalisent {poids} (règle 5/10/40 dépassée).":
        "The {n} stocks above 5% add up to {poids} (5/10/40 rule exceeded).",
    "Règle des fonds UCITS : les lignes de plus de 5 % ne doivent pas dépasser 40 % au total. Au-delà, le portefeuille dépend de quelques entreprises.":
        "UCITS rule: positions above 5% must not exceed 40% in total. Beyond that, the portfolio depends on a "
        "few companies.",
    "Ramener certaines lignes sous 5 % ou ajouter des ETF diversifiés.":
        "Bring some positions below 5% or add diversified ETFs.",
    "{noms} : détenu(s) en direct ET probablement aussi via votre ETF {indice}.":
        "{noms}: held directly AND probably also through your {indice} ETF.",
    "L'exposition réelle à ces entreprises est plus forte que leur seule ligne ne le laisse penser.":
        "Your real exposure to these companies is higher than their own position suggests.",
    "En tenir compte avant de renforcer ces lignes.": "Take this into account before adding to these positions.",
    "Aucune ligne trop concentrée ({n} lignes, équivalent à {eff} lignes de même poids).":
        "No overly concentrated position ({n} positions, equivalent to {eff} equal-weight positions).",
    "Duration moyenne des obligations : {duration} ans. Une hausse des taux de 1 point coûterait environ {perte} au portefeuille.":
        "Average bond duration: {duration} years. A 1-point rise in interest rates would cost the portfolio "
        "about {perte}.",
    "Plus la duration est longue, plus le prix des obligations baisse quand les taux montent (et monte quand ils baissent).":
        "The longer the duration, the more bond prices fall when rates rise (and rise when they fall).",
    "Raccourcir la duration (obligations 1-3 ans) pour réduire la sensibilité aux taux.":
        "Shorten duration (1-3 year bonds) to reduce interest-rate sensitivity.",
    "Biais domestique : la France représente {poids} de la poche actions.":
        "Home bias: France makes up {poids} of the equity allocation.",
    "Les investisseurs surpondèrent souvent leur propre pays : le patrimoine (emploi, immobilier) est alors déjà exposé à la même économie.":
        "Investors often overweight their own country, while their wealth (job, real estate) is already exposed "
        "to the same economy.",
    "Un ETF monde éligible au PEA permet de garder l'enveloppe tout en diversifiant.":
        "A PEA-eligible world ETF keeps the tax wrapper while diversifying.",
    "Les pays émergents représentent {poids} de la poche actions.": "Emerging markets make up {poids} of the equity allocation.",
    "Marchés plus volatils, avec des risques politiques, de gouvernance et de change plus élevés.":
        "More volatile markets, with higher political, governance and currency risks.",
    "Limiter cette poche selon le profil, ou la faire porter par un ETF large plutôt que par quelques titres.":
        "Limit this allocation according to the profile, or hold it through a broad ETF rather than a few stocks.",
    "Répartition géographique proche du marché mondial (premier pays : {pays}, {poids}).":
        "Geographic allocation close to the world market (largest country: {pays}, {poids}).",
    "Le secteur {secteur} pèse {poids} de la poche actions ({monde} dans le marché mondial).":
        "The {secteur} sector makes up {poids} of the equity allocation ({monde} in the world market).",
    "Le portefeuille dépend d'un seul cycle économique : un retournement du secteur (valorisations, taux, réglementation) pèserait lourd sur la performance.":
        "The portfolio depends on a single economic cycle: a sector downturn (valuations, rates, regulation) "
        "would weigh heavily on performance.",
    "Équilibrer avec des secteurs peu représentés, notamment défensifs (santé, consommation de base, services publics).":
        "Balance with under-represented sectors, especially defensive ones (health care, consumer staples, utilities).",
    "Un ETF monde équipondéré ou sectoriel peut corriger le biais.": "An equal-weight world ETF or a sector ETF can correct the bias.",
    "Peu de secteurs défensifs : {poids} (santé, consommation de base, services publics).":
        "Few defensive sectors: {poids} (health care, consumer staples, utilities).",
    "Ces secteurs amortissent généralement les baisses de marché : sans eux, le portefeuille souffre davantage en récession.":
        "These sectors usually cushion market falls: without them, the portfolio suffers more in a recession.",
    "Ajouter une poche défensive pour lisser les baisses.": "Add a defensive allocation to smooth out declines.",
    "Répartition sectorielle équilibrée (premier secteur : {secteur}, {poids}).":
        "Balanced sector allocation (largest sector: {secteur}, {poids}).",
    "{n} lignes très corrélées entre elles ({rho} en moyenne) pèsent {poids} : {noms}. {n} lignes, mais en pratique un seul pari.":
        "{n} highly correlated positions ({rho} on average) weigh {poids}: {noms}. {n} positions, but in "
        "practice a single bet.",
    "La diversification n'est qu'apparente : ces titres baissent ensemble.":
        "The diversification is only apparent: these securities fall together.",
    "Remplacer une partie de ce bloc par des actifs peu corrélés (autres secteurs, obligations, or).":
        "Replace part of this block with weakly correlated assets (other sectors, bonds, gold).",
    "Ou regrouper ces lignes dans un seul ETF du même thème, moins risqué.":
        "Or combine these positions into a single, less risky ETF on the same theme.",
    "Corrélation moyenne élevée entre les lignes : {rho}.": "High average correlation between positions: {rho}.",
    "Les lignes évoluent dans le même sens : le portefeuille se comporte presque comme un seul actif.":
        "The positions move together: the portfolio behaves almost like a single asset.",
    "Ajouter des classes d'actifs différentes (obligations, or) ou d'autres zones.":
        "Add different asset classes (bonds, gold) or other regions.",
    "Les jours de forte baisse, la corrélation moyenne monte à {crise} (contre {rho} en temps normal).":
        "On days of sharp declines, the average correlation rises to {crise} (versus {rho} normally).",
    "La diversification protège moins quand on en a le plus besoin : c'est typique des crises.":
        "Diversification protects less when it is needed most: this is typical of crises.",
    "Voir les stress tests (espace « Conseil patrimonial ») pour mesurer l'impact d'une crise.":
        "See the stress tests (\"Wealth advisory\" workspace) to measure the impact of a crisis.",
    "Amortisseurs présents : {noms} ({poids}) évoluent peu avec le reste du portefeuille.":
        "Shock absorbers present: {noms} ({poids}) move little with the rest of the portfolio.",
    "Diversification réelle satisfaisante : {blocs} blocs indépendants pour {n} lignes, ratio de diversification {ratio}.":
        "Satisfactory real diversification: {blocs} independent blocks for {n} positions, diversification "
        "ratio {ratio}.",
    "{pays} pèse {poids} de la poche actions ({monde} dans le marché mondial).":
        "{pays} makes up {poids} of the equity allocation ({monde} in the world market).",
    "Votre performance dépend fortement de l'économie, de la politique et de la monnaie d'un seul pays. Un choc local (récession, élection, réglementation) toucherait une grande partie du portefeuille.":
        "Your performance depends heavily on the economy, politics and currency of a single country. A local "
        "shock (recession, election, regulation) would hit a large part of the portfolio.",
    "Diversifier une partie de cette poche avec un ETF monde (MSCI World ou ACWI).":
        "Diversify part of this allocation with a world ETF (MSCI World or ACWI).",
    "Renforcer les zones sous-représentées plutôt que de vendre, si la fiscalité l'impose.":
        "Add to under-represented regions rather than selling, if taxes make selling costly.",
    "Surpondération marquée d'un pays par rapport au marché mondial.": "Marked overweight of one country versus the world market.",
    "Vérifier que ce choix est volontaire (conviction, biais domestique).": "Check that this choice is deliberate (conviction, home bias).",
    "très forte": "very strong", "forte": "strong", "modérée": "moderate", "faible": "weak",
    "Bon": "Good", "À surveiller": "To monitor", "À corriger": "To fix", "Non concerné": "Not applicable",
    "Géographie": "Geography", "Secteurs": "Sectors", "Devises": "Currencies", "Concentration": "Concentration",
    "Taux": "Interest rates", "Diversification réelle": "Real diversification",
    # --- Graphiques ---
    "Autres ({n})": "Other ({n})",
    "%{customdata[2]} titre(s)": "%{customdata[2]} security(ies)",
    "%{z:.1%} de la poche actions": "%{z:.1%} of the equity allocation",
    "… et {n} autre(s)": "… and {n} more",
    # --- Indices de référence (src/indices.py) ---
    "Actions": "Equities", "Obligations": "Bonds", "Monétaire": "Money market", "Mixtes": "Multi-asset",
    "MSCI World": "MSCI World", "MSCI ACWI": "MSCI ACWI", "S&P 500": "S&P 500", "Nasdaq-100": "Nasdaq-100",
    "Stoxx Europe 600": "Stoxx Europe 600", "Euro Stoxx 50": "Euro Stoxx 50", "CAC 40": "CAC 40",
    "MSCI ACWI, monde avec émergents (ETF, dividendes réinvestis)":
        "MSCI ACWI, world including emerging markets (ETF, dividends reinvested)",
    "Nasdaq-100 (ETF, dividendes réinvestis)": "Nasdaq-100 (ETF, dividends reinvested)",
    "Stoxx Europe 600 (ETF, dividendes réinvestis)": "Stoxx Europe 600 (ETF, dividends reinvested)",
    "MSCI Marchés émergents (ETF, dividendes réinvestis)": "MSCI Emerging Markets (ETF, dividends reinvested)",
    "MSCI Émergents": "MSCI Emerging",
    "Emprunts d'État zone euro (ETF, coupons réinvestis)": "Euro area government bonds (ETF, coupons reinvested)",
    "Emprunts d'État €": "€ government bonds",
    "Obligations d'entreprises en euros (ETF, hors coupons)": "Euro corporate bonds (ETF, excluding coupons)",
    "Oblig. entreprises €": "€ corporate bonds",
    "Monétaire €STR (ETF, intérêts réinvestis)": "Money market €STR (ETF, interest reinvested)",
    "€STR": "€STR",
    "Mixte prudent : 20 % actions monde / 80 % obligations €": "Conservative mix: 20% world equities / 80% € bonds",
    "Mixte équilibré : 60 % actions monde / 40 % obligations €": "Balanced mix: 60% world equities / 40% € bonds",
    "Mixte dynamique : 80 % actions monde / 20 % obligations €": "Growth mix: 80% world equities / 20% € bonds",
    "Mixte 20/80": "Mix 20/80", "Mixte 60/40": "Mix 60/40", "Mixte 80/20": "Mix 80/20",
    "Actions, obligations, monétaire, ou indice mixte actions / obligations recalculé chaque mois":
        "Equities, bonds, money market, or a multi-asset equity / bond index rebalanced monthly",
    "Indice {famille} : le bêta, l'alpha et la corrélation mesurent la sensibilité à un marché d'actions ; face à cet indice, ils ont peu de sens. Comparez surtout les rendements et les volatilités.":
        "{famille} index: beta, alpha and correlation measure sensitivity to an equity market; against this "
        "index they make little sense. Compare returns and volatilities instead.",
    # --- Tableau de bord ---
    "Portefeuille d'exemple": "Sample portfolio",
    "Portefeuille actuel": "Current portfolio",
    "Régions (poche actions)": "Regions (equity allocation)",
    "Secteurs (poche actions)": "Sectors (equity allocation)",
    "Ou envoyer un autre fichier (CSV, Excel ou PDF)": "Or upload another file (CSV, Excel or PDF)",
    "Colonnes : date, type (ACHAT, VENTE, DIVIDENDE), ticker (code Yahoo Finance), nom, quantite, prix, frais. CSV à virgules ou à points-virgules, fichier Excel, ou PDF (relevé d'opérations, avis d'opéré). Prioritaire sur le portefeuille choisi ci-dessus.":
        "Columns: date, type (ACHAT = buy, VENTE = sell, DIVIDENDE = dividend), ticker (Yahoo Finance code), "
        "name, quantity, price, fees. Comma or semicolon CSV, Excel file, or PDF (transaction statement, trade "
        "confirmation). Takes priority over the portfolio selected above.",
    "Expositions": "Exposures",
    "Si la VaR historique dépasse la VaR paramétrique, les pertes extrêmes sont plus fréquentes que ne le prévoit la loi normale (« queues épaisses »). Corrélations et diversification : onglet « Expositions ».":
        "If historical VaR exceeds parametric VaR, extreme losses are more frequent than the normal distribution "
        "predicts (\"fat tails\"). Correlations and diversification: \"Exposures\" tab.",
    "Présence dans le monde": "Worldwide presence",
    "Poids de chaque pays dans la poche actions · plus la couleur est foncée, plus le pays pèse · survoler un pays pour le détail":
        "Weight of each country in the equity allocation · the darker the colour, the larger the weight · hover "
        "over a country for details",
    "ETF répartis selon la composition de leur indice (approximation au {date}).":
        "ETFs allocated according to the composition of their index (approximation as of {date}).",
    "Hors carte : {detail}.": "Not on the map: {detail}.",
    "{n} groupes · en % de la valeur": "{n} groups · as % of value",
    "{n} groupes · en % de la poche actions": "{n} groups · as % of the equity allocation",
    "Mettre à jour ce portefeuille avec de nouveaux mouvements : avis d'opéré PDF, export Excel / CSV ou saisie manuelle":
        "Update this portfolio with new transactions: PDF trade confirmation, Excel / CSV export or manual entry",
    "Télécharger le fichier mis à jour": "Download the updated file",
    "{nom} (mis à jour)": "{nom} (updated)",
    # --- Onglet Expositions (src/vues_expositions.py) ---
    "Seuils adaptés au profil": "Thresholds for profile",
    "Hors euro : {poids}": "Outside the euro: {poids}",
    "Plus grosse ligne : {poids}": "Largest position: {poids}",
    "Corrélation moyenne : {rho}": "Average correlation: {rho}",
    "Par titre": "By security",
    "Analyse des expositions...": "Analysing exposures...",
    "Profil défini dans l'espace « Conseil patrimonial » (questionnaire), ou choisi ici.":
        "Profile set in the \"Wealth advisory\" workspace (questionnaire), or chosen here.",
    "1er pays : {pays} {poids}": "Top country: {pays} {poids}",
    "1er secteur : {secteur} {poids}": "Top sector: {secteur} {poids}",
    "Duration : {d} ans": "Duration: {d} years",
    "Pas d'obligations": "No bonds",
    "Géographie et secteurs": "Geography and sectors",
    "Devises et taux": "Currencies and rates",
    "Au moins deux lignes sont nécessaires.": "At least two positions are needed.",
    "Expositions et diversification": "Exposures and diversification",
    "Analyse en transparence : chaque ETF est réparti selon la composition de son indice (approximation au {date})":
        "Look-through analysis: each ETF is allocated according to the composition of its index (approximation "
        "as of {date})",
    "Constats et pistes": "Findings and suggestions",
    "Analyse pédagogique fondée sur des règles simples et des données passées : elle ne constitue pas un conseil en investissement.":
        "Educational analysis based on simple rules and past data: it is not investment advice.",
    "Afficher": "Show",
    "Corrélations historiques des rendements quotidiens ({n} jours) : elles ne sont pas garanties à l'avenir.":
        "Historical correlations of daily returns ({n} days): they are not guaranteed in the future.",
    "{n} point(s) à surveiller ou à corriger": "{n} point(s) to monitor or fix",
    "Aucun point d'attention": "Nothing to flag",
    "Points positifs ({n})": "Strengths ({n})",
    "Exposition réelle aux devises": "Real currency exposure",
    "Tout le portefeuille, ETF répartis selon les pays de leur indice":
        "Whole portfolio, ETFs allocated according to the countries in their index",
    "Un ETF coté en euros reste exposé aux devises des actions qu'il contient, sauf s'il est couvert (« EUR Hedged »). L'or, coté en dollars, est compté à part.":
        "A euro-listed ETF remains exposed to the currencies of the stocks it holds, unless it is hedged "
        "(\"EUR Hedged\"). Gold, priced in dollars, is shown separately.",
    "Sensibilité aux taux": "Interest-rate sensitivity",
    "Poche obligataire": "Bond allocation",
    "Le portefeuille ne contient pas d'obligations.": "The portfolio holds no bonds.",
    "Les plus grosses lignes": "Largest positions",
    "Poids et poids cumulé": "Weight and cumulative weight",
    "Corrélation moyenne": "Average correlation",
    "Blocs indépendants": "Independent blocks",
    "Les jours de forte baisse": "On sharp-decline days",
    "Corrélations entre les titres": "Correlations between securities",
    "Titres regroupés par blocs qui évoluent ensemble · rouge = évoluent ensemble, bleu = en sens inverse":
        "Securities grouped into blocks that move together · red = move together, blue = move in opposite directions",
    "Corrélations entre groupes": "Correlations between groups",
    "Rendement de chaque groupe (lignes pondérées par leur poids)": "Return of each group (positions weighted by size)",
    "Paires les plus corrélées": "Most correlated pairs",
    "Lignes qui diversifient le mieux": "Best diversifiers",
    "Corrélation avec le reste du portefeuille": "Correlation with the rest of the portfolio",
    "Pas de poche actions à analyser.": "No equity allocation to analyse.",
    "Principaux écarts par pays": "Main differences by country",
    "Sur- et sous-pondérations de la poche actions face à {indice}":
        "Over- and underweights of the equity allocation versus {indice}",
    "Part de la valeur et part du risque par région": "Share of value and share of risk by region",
    "Une région qui apporte plus de risque que de valeur est plus volatile ou plus corrélée au reste":
        "A region that brings more risk than value is more volatile or more correlated with the rest",
    "Approximation : variation du prix ≈ − duration × variation des taux. Les obligations retrouvent ensuite un rendement plus élevé.":
        "Approximation: price change ≈ − duration × change in rates. Bonds then earn a higher yield.",
    "5 premières lignes": "Top 5 positions", "10 premières lignes": "Top 10 positions",
    "Actions de plus de 5 %": "Stocks above 5%", "Cumul": "Cumulative",
    "pondérée par les poids": "weighted by position size",
    "Corrélation typique entre deux euros investis dans deux lignes différentes":
        "Typical correlation between two euros invested in two different positions",
    "Somme des volatilités pondérées / volatilité du portefeuille": "Sum of weighted volatilities / portfolio volatility",
    "Groupes de titres corrélés à plus de 0,7 : chacun ne compte que pour un pari":
        "Groups of securities correlated above 0.7: each counts as a single bet",
    "corrélation moyenne (10 % pires jours)": "average correlation (worst 10% of days)",
    "Les corrélations montent pendant les crises : la diversification protège alors moins":
        "Correlations rise during crises: diversification then protects less",
    "Lien": "Strength", "Blocs de titres corrélés": "Blocks of correlated securities",
    "Corrélation moyenne supérieure à 0,7": "Average correlation above 0.7",
    "**{poids}** · {noms} (corrélation {rho})": "**{poids}** · {noms} (correlation {rho})",
    "Pays": "Country",
    "équivalent à {n} lignes de même poids": "equivalent to {n} equal-weight positions",
    "Nombre effectif = 1 / Σ poids² (inverse de l'indice de Herfindahl)":
        "Effective number = 1 / Σ weight² (inverse of the Herfindahl index)",
    "Limite UCITS : 40 %": "UCITS limit: 40%",
    "Règle 5/10/40 des fonds : une ligne ≤ 10 %, et les lignes > 5 % ≤ 40 % au total":
        "Fund 5/10/40 rule: one position ≤ 10%, and positions > 5% ≤ 40% in total",
    "Duration moyenne": "Average duration", "{d} ans": "{d} years",
    "Si les taux montent de 1 point": "If rates rise by 1 point",
    "Durée de vie moyenne pondérée des flux : mesure la sensibilité aux taux":
        "Weighted average life of cash flows: measures interest-rate sensitivity",
    "≈ {montant}": "≈ {montant}",
    # --- Gestion d'actifs ---
    "Le diagnostic de diversification (régions, secteurs, devises, corrélations, ratio de diversification) se trouve dans « Analyse du portefeuille » › onglet « Expositions ».":
        "The diversification diagnosis (regions, sectors, currencies, correlations, diversification ratio) is in "
        "\"Portfolio analysis\" › \"Exposures\" tab.",
    "Les 20 plus gros contributeurs au risque · une ligne dont la part du risque dépasse sa part de la valeur est plus volatile ou plus corrélée au reste":
        "The 20 largest risk contributors · a position whose share of risk exceeds its share of value is more "
        "volatile or more correlated with the rest",
    "Volatilité actuelle": "Current volatility",
    "Volatilité en parité des risques": "Risk-parity volatility",
    "Mêmes titres, risque réparti également": "Same securities, risk spread equally",
    # --- Mon compte et nouvelles opérations ---
    "Fichier CSV, Excel ou PDF, de n'importe quel format": "CSV, Excel or PDF file, in any layout",
    "Ajouter des opérations": "Add transactions",
    "Annuler le dernier ajout": "Undo last addition",
    "Revenir à la version du {date}": "Go back to the version of {date}",
    "Aucun ajout à annuler.": "Nothing to undo.",
    "Retour au tableau de bord": "Back to the dashboard",
    "Titre introuvable : {titre}. Indiquez son ticker Yahoo Finance (ex. MC.PA).":
        "Security not found: {titre}. Enter its Yahoo Finance ticker (e.g. MC.PA).",
    "Portefeuille : {nom}": "Portfolio: {nom}",
    "Envoyez seulement les nouveaux mouvements : un avis d'opéré (PDF), un export des dernières opérations (Excel, CSV ou PDF), ou saisissez un ordre à la main. Les opérations déjà présentes sont reconnues et ne sont pas ajoutées deux fois.":
        "Upload only the new transactions: a trade confirmation (PDF), an export of recent transactions (Excel, "
        "CSV or PDF), or enter an order manually. Transactions already present are recognised and not added twice.",
    "Depuis un fichier": "From a file", "Saisie manuelle": "Manual entry",
    "Fichiers (CSV, Excel ou PDF)": "Files (CSV, Excel or PDF)",
    "{n} opération(s) ajoutée(s) · {total} au total ({avant} avant)":
        "{n} transaction(s) added · {total} in total ({avant} before)",
    "Enregistrer les opérations": "Save transactions", "Tout effacer": "Clear all",
    "Date": "Date",
    "Prix unitaire (devise du titre) ou montant du dividende": "Unit price (security currency) or dividend amount",
    "Frais (€)": "Fees (€)", "Ajouter à la liste": "Add to the list",
    "Vérification avant enregistrement": "Check before saving",
    "Décochez une ligne pour ne pas l'ajouter. Les cellules sont modifiables.":
        "Untick a row to leave it out. Cells can be edited.",
    "{n} opération(s) ajoutée(s) à « {nom} ». Vous pouvez annuler cet ajout depuis « Mon compte ».":
        "{n} transaction(s) added to \"{nom}\". You can undo this from \"My account\".",
    "{n} opération(s) ajoutée(s) pour cette session. Téléchargez le fichier mis à jour pour le garder.":
        "{n} transaction(s) added for this session. Download the updated file to keep it.",
    "Lecture de {nom}...": "Reading {nom}...",
    "{nom} : {n} opération(s) lue(s).": "{nom}: {n} transaction(s) read.",
    "{nom} : {raison}": "{nom}: {raison}",
    "Ticker, ISIN, nom ou code Bloomberg": "Ticker, ISIN, name or Bloomberg code",
    "Pour un format inhabituel, envoyez le fichier depuis la barre latérale : l'assistant d'import vous guidera.":
        "For an unusual layout, upload the file from the sidebar: the import assistant will guide you.",
    "Ajouter": "Add", "Prix": "Price", "Indiquez le titre.": "Enter the security.",
    "Recherche du titre...": "Looking up the security...",
    "déjà dans le portefeuille": "already in the portfolio", "nouvelle": "new",
    "Opération datée dans le futur : {titre}, le {date}.": "Transaction dated in the future: {titre}, on {date}.",
    "Quantité ou prix nul pour {titre}, le {date}.": "Zero quantity or price for {titre}, on {date}.",
    "Vente de {quantite} {titre} le {date}, mais seulement {detenu} détenu(s) à cette date.":
        "Sale of {quantite} {titre} on {date}, but only {detenu} held on that date.",
    "PDF scanné (image) : impossible à lire automatiquement. Exportez le relevé en PDF depuis votre espace bancaire, ou en Excel / CSV, ou saisissez l'opération à la main.":
        "Scanned PDF (image): it cannot be read automatically. Export the statement as a PDF from your online "
        "banking, or as Excel / CSV, or enter the transaction manually.",
    "Aucune opération trouvée dans ce PDF (ni tableau d'opérations, ni avis d'opéré lisible).":
        "No transaction found in this PDF (no transaction table and no readable trade confirmation).",
    "PDF image (scan, photo ou page imprimée avec « Imprimer en PDF ») : le texte a été lu par reconnaissance de caractères, mais aucune opération n'a été reconnue. Utilisez le bouton « Format PDF » de votre banque, un export Excel / CSV, ou la saisie manuelle.":
        "Image PDF (scan, photo or page printed with \"Print to PDF\"): the text was read by character "
        "recognition, but no transaction was recognised. Use your bank's \"PDF format\" button, an Excel / CSV "
        "export, or manual entry.",
    "PDF image lu par reconnaissance de caractères : vérifiez les opérations (onglet « Transactions »).":
        "Image PDF read by character recognition: please check the transactions (\"Transactions\" tab).",
    "Avis d'opéré PDF lu.": "PDF trade confirmation read.",
    "Pour lire un PDF, installer pdfplumber : python -m pip install pdfplumber":
        "To read a PDF, install pdfplumber: python -m pip install pdfplumber",
})

DONNEES.update({
    "France": "France", "Allemagne": "Germany", "Pays-Bas": "Netherlands", "Espagne": "Spain", "Italie": "Italy",
    "Belgique": "Belgium", "Finlande": "Finland", "Irlande": "Ireland", "Autriche": "Austria",
    "Portugal": "Portugal", "Grèce": "Greece", "Slovaquie": "Slovakia", "Slovénie": "Slovenia",
    "Luxembourg": "Luxembourg", "Suède": "Sweden", "Danemark": "Denmark", "Norvège": "Norway",
    "Pologne": "Poland", "Hongrie": "Hungary", "Tchéquie": "Czech Republic", "Israël": "Israel",
    "Australie": "Australia", "Nouvelle-Zélande": "New Zealand", "Hong Kong": "Hong Kong",
    "Singapour": "Singapore", "Chine": "China", "Taïwan": "Taiwan", "Corée du Sud": "South Korea",
    "Inde": "India", "Brésil": "Brazil", "Mexique": "Mexico", "Afrique du Sud": "South Africa",
    "Arabie saoudite": "Saudi Arabia", "Émirats arabes unis": "United Arab Emirates", "Qatar": "Qatar",
    "Koweït": "Kuwait", "Indonésie": "Indonesia", "Malaisie": "Malaysia", "Thaïlande": "Thailand",
    "Philippines": "Philippines", "Turquie": "Turkey", "Chili": "Chile", "Pérou": "Peru",
    "Colombie": "Colombia", "Égypte": "Egypt", "Zone euro": "Euro area", "Monétaire": "Money market",
    "Sans pays (or)": "No country (gold)", "Autres pays": "Other countries",
})
