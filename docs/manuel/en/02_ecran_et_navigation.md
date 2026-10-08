# The screen and navigation
<!-- chapitre: ecran | ordre: 2 -->

This chapter describes the software's screen: the sidebar block by block, the choice of language and night mode, the four workspaces, the choice of portfolio and analysis settings (benchmark index, risk-free rate, VaR level), the banner and key figures at the top of the page, the PDF report, refreshing prices, the manual's assistant and chart tips. Read it after the getting-started chapter to find out where each function is.

## How is the screen organised?
<!-- fiche: ecran-organisation | questions: how is the screen laid out ; what is the left bar for ; I'm lost in the software where do I start ; what is the menu on the left ; where are the settings ; the sidebar has disappeared ; description of the interface ; what is in the left column | mots: interface, screen, sidebar, menu, navigation, layout, dashboard -->

The screen is split into two parts: the **sidebar**, on the left, which groups all the settings, and the **main area**, on the right, which displays the results.

### The sidebar, from top to bottom

1. **The header**: the "PT" monogram, the name "Portfolio Tracker" and the label "Master G2C". Just below, on a single line, two small selectors: language (FR · EN) on the left and display (Light · Dark) on the right; the active option is in bold.
2. **The personal space**: the label "Encrypted personal space" and the [[Sign in]] link. Once signed in, your initials, your username and the [[My account]] and [[Sign out]] links.
3. **Workspace**: the menu of the four workspaces (Portfolio analysis, Wealth advisory, Asset management, Manual and help), each with a grey line of description. The workspace on screen is highlighted in light blue, with a blue bar on the left.
4. **Data**: the list of portfolios, the [[Upload a file (CSV, Excel or PDF)]] area ([[Browse]] button, or drag and drop the file), then the [[Add transactions]] and [[File template]] links.
5. **Settings**: a collapsed panel that contains the benchmark index and the risk-free rate. Its title summarises the current settings. (The VaR confidence level is set in the Risk tab, the only place where it is used.)
6. **Information** about the portfolio being analysed: file, period, number of transactions, source of prices, and the exchange rates folded under "Exchange rates".
7. **The buttons** [[PDF report]] and [[Refresh prices]].

Blocks 6 and 7 only appear once a portfolio has been analysed: they are absent in the "Manual and help" space and on the "My account" and "Add transactions" pages.

At the bottom right of the screen, on every page, the [[Help]] button opens a small panel to ask the manual a question (see the article on the help bubble).

### The main area

In the analysis spaces, it begins with a blue banner (title, period, benchmark index, source of prices), followed by a row of six key figures, then the tabs of the chosen space. A footer recalls the sources (Yahoo Finance for prices, ECB for the risk-free rate) and that the tool is educational: it does not constitute investment advice.

### If the sidebar is hidden

On a narrow screen, the sidebar may be collapsed. The small arrow-shaped button at the top left of the window lets you reopen it.

## Switching the software to English (or back to French)
<!-- fiche: ecran-langue | questions: how do I put the software in english ; change the language ; switch to english ; the dashboard is in english how do I put it back in french ; where is the FR EN button ; is there an english version ; can the pdf report be in english ; why do some texts stay in french | mots: language, English, French, translation, FR, EN, bilingual -->

The language selector is at the top of the sidebar, under the software's name, on the left: click **EN** for English, **FR** for French. The change is immediate, without losing the current portfolio or settings. French is the starting language.

### What changes

- all the labels, buttons, tabs, help texts and comments of the dashboard;
- data produced by the calculations (regions, sectors, asset classes, scenario names), translated on display;
- the format of numbers and dates: in English, "€1,235", "+12.34%" and "16 Jan 2017"; in French, "1 235 €", "+12,34 %" and "16/01/2017".

### What stays in French

- **the PDF report**, always written in French, whatever the screen language;
- the names of securities and of your portfolios, which are proper names;
- the manual, as long as its English version is not installed with your version of the software: the assistant and the contents then use the French manual;
- the command-line analysis and the guides in the `docs` folder.

An on-screen text that does not yet have a translation is displayed in French, without an error.

### How long the choice lasts

The language is kept for the whole session. It is not saved in your account: the next time you open the software, it restarts in French. Clicking a second time on the language already chosen changes nothing.

## Turning on night mode (dark background)
<!-- fiche: ecran-mode-nuit | questions: how do I turn on dark mode ; dark mode ; the screen is too white it hurts my eyes ; switch to night mode ; go back to light mode ; night mode is not remembered ; why is the pdf white when I'm in night mode ; make the background black | mots: night mode, dark mode, theme, black background, midnight blue, light, display -->

The display selector is at the top of the sidebar, under the software's name, on the right (on the same line as the language): click **Dark** for a midnight-blue background, **Light** to return to the white background. Light mode is the starting mode.

### What changes

- the background of the page and the sidebar, the figure cards, the boxes, the fields and the menus;
- the charts: texts, grids, hover bubbles and dark curve colours are replaced by shades that are legible on a dark background;
- the data tables, whose colours are inverted so they stay legible.

### The choice is remembered in your account

If you are signed in to your personal space, the chosen mode is saved in your preferences, encrypted along with the rest of your account. The next time you sign in, the software restores it automatically. Without an account, the choice only applies to the current session.

For the mode to be saved, choose it **after** signing in.

### The PDF report stays light

The PDF report always keeps a white background, whatever mode is chosen on screen: it is designed to be printed.

## The four workspaces and what they contain
<!-- fiche: ecran-espaces | questions: what are the workspaces ; where do I find taxation ; where is the backtest ; how do I change workspace ; I can't find the risk tab ; what is the difference between analysis advisory and management ; how do I get back to the analysis from my account ; I'm stuck on the add transactions page ; nothing is ticked in the workspace menu | mots: workspace, menu, navigation, tabs, Portfolio analysis, Wealth advisory, Asset management, Manual and help, sections -->

The **Workspace** menu, in the sidebar, offers four workspaces. Click one to display it; its tabs appear at the top of the main area.

| Workspace | Description in the menu | Tabs |
|---|---|---|
| Portfolio analysis | Performance, risk, optimisation | Overview, Holdings, Performance, Risk, Exposures, Optimisation, Projection, Transactions |
| Wealth advisory | Taxation, stress tests | Taxation, Stress tests |
| Asset management | Attribution, risk budget, backtest | Performance attribution, Risk budget, Strategy backtest |
| Manual and help | User guide, formulas, questions | "Ask a question" assistant, manual contents |

### What they have in common

The first three workspaces analyse the same portfolio with the same settings. They all display the blue banner and the six key figures at the top of the page. The software opens on "Portfolio analysis".

The "Manual and help" workspace opens even if no portfolio could be loaded: you can always look for help there.

### Returning to a workspace from "My account" or "Add transactions"

When the [[My account]] page or the [[Add transactions]] page is open, no workspace is ticked in the menu. A click on **any workspace**, including the one you were in, closes the page and displays the chosen workspace. You can also:

- click [[My account]] again to close that page;
- use the [[Back to the dashboard]] button on the "Add transactions" page.

## Choosing the portfolio to analyse
<!-- fiche: ecran-choisir-portefeuille | questions: how do I change portfolio ; where do I choose my portfolio ; what are the sample portfolios ; I can't see my portfolio in the list ; what does my space in front of the name mean ; the list doesn't change when I pick another portfolio ; how do I go back to the sample after uploading a file ; default portfolio at startup | mots: portfolio, selection, drop-down list, sample, My space, demo, file, portfolio choice -->

The portfolio to analyse is chosen in the **Data** block of the sidebar, with the drop-down list placed under that title. The software immediately analyses the first portfolio in the list.

### What the list contains

1. **Your personal portfolios**, if you are signed in. They appear first, in alphabetical order, preceded by the label "My space · " (for example "My space · PEA Boursorama"). They are decrypted in memory at the time of analysis.
2. **The sample portfolios** supplied with the software, to discover the functions without your own data: "Diversified portfolio (multi-asset)", offered first, and "Global equity portfolio". The small "Sample portfolio" is only offered if it is the only sample file present.

### An uploaded file takes priority

If a file is present in the [[Upload a file (CSV, Excel or PDF)]] area, **it** is the one analysed, whatever the choice in the list. To return to a portfolio from the list, remove the uploaded file by clicking the cross next to its name.

### My portfolio is not in the list

- Check that you are signed in: without signing in, only the samples are offered.
- A file uploaded without being saved does not appear in the list. To find it next time, save it to your space with the [[Save]] button that appears under the upload area once the file has been read.

### To go further

Uploading a file, the import wizard and adding new transactions are explained in the chapter on importing. Managing your saved portfolios (renaming, downloading, deleting) is done on the [[My account]] page.

## Where do I set the analysis settings?
<!-- fiche: ecran-parametres | questions: where are the settings ; how do I change the benchmark index ; I can't find the risk-free rate ; what does the line settings msci world 2.50% mean ; are the settings saved ; why do all the figures change when I change a setting ; analysis settings | mots: settings, options, benchmark index, risk-free rate, VaR, confidence level -->

The analysis settings are in the **Settings** panel of the sidebar, under the Data block. It is collapsed by default: click its title to open it.

### The summary in the title

Even when collapsed, the panel's title recalls the current settings, for example:

`Settings · MSCI World · 2.50%`

that is, the benchmark index and the annual risk-free rate.

### The two settings

| Setting | Starting value | Used for |
|---|---|---|
| [[Benchmark index]] | MSCI World (CW8 ETF, dividends reinvested) | Comparing performance, calculating beta, alpha and tracking error |
| [[Risk-free rate (% per year)]] | 2.50% | Sharpe and Sortino ratios, Jensen's alpha |

Each has its own detailed entry in this chapter. The VaR confidence level (95% at the start) is not in this panel: it is set at the top of the Risk tab, where the VaR is shown (see the dedicated entry).

### Effect of a change

Any change reruns the analysis: the key figures, the tabs of the three analysis workspaces and the PDF report use the new settings. A PDF report already prepared with the old settings is no longer offered for download: it has to be prepared again.

### How long the settings last

The settings are kept during the session, even if you change portfolio or workspace. They are not saved in your account: the next time you open the software, the starting values return.

## Choosing the benchmark index: the 14 indices offered
<!-- fiche: ecran-indice-reference | questions: which benchmark index should I choose ; what is the benchmark ; compare my portfolio to the cac 40 ; set the s&p 500 as the reference ; why msci world by default ; list of available indices ; dividends reinvested or excluding dividends what is the difference ; my portfolio is bonds which index should I take ; can another index be added | mots: benchmark index, benchmark, MSCI World, CAC 40, S&P 500, Euro Stoxx 50, ACWI, Nasdaq, bonds, €STR, comparison -->

The benchmark index serves as a point of comparison: "portfolio versus index" curve in base 100, performance gap, beta, alpha, correlation, tracking error, information ratio. It is chosen in the **Settings** panel, in the [[Benchmark index]] menu. Each entry in the menu shows its family first, then its name (for example "Equities · CAC 40 (price index, excl. dividends)").

### The full list

| Family | Index offered | What it represents |
|---|---|---|
| Equities | MSCI World (CW8 ETF, dividends reinvested) | Large and mid caps of developed countries. **Default choice** |
| Equities | MSCI ACWI, world including emerging markets | Developed and emerging countries, dividends reinvested |
| Equities | S&P 500 (ESE ETF, dividends reinvested) | 500 large US companies |
| Equities | Nasdaq-100 | 100 large non-financial Nasdaq companies, very technology-heavy, dividends reinvested |
| Equities | Stoxx Europe 600 | 600 European companies, dividends reinvested |
| Equities | Euro Stoxx 50 (price index, excl. dividends) | 50 large eurozone companies |
| Equities | CAC 40 (price index, excl. dividends) | 40 large French companies |
| Equities | MSCI Emerging Markets | Emerging-country equities, dividends reinvested |
| Bonds | Euro area government bonds (coupons reinvested) | Debt of eurozone governments |
| Bonds | Euro corporate bonds (excluding coupons) | Corporate debt issued in euros |
| Money market | Money market €STR (interest reinvested) | Overnight investment at the ECB's €STR rate |
| Multi-asset | Conservative mix: 20% world equities / 80% € bonds | Composite index calculated by the software |
| Multi-asset | Balanced mix: 60% world equities / 40% € bonds | Composite index calculated by the software |
| Multi-asset | Growth mix: 80% world equities / 20% € bonds | Composite index calculated by the software |

### How the index is tracked

Most indices are tracked by means of a listed ETF that replicates them. For each one, several codes are provided: the first one whose history is available is used (for example CW8.PA, otherwise IWDA.AS for the MSCI World).

### Dividends reinvested or excluding dividends

An accumulating ETF reinvests dividends: its performance is "including dividends". The Euro Stoxx 50 and the CAC 40 are price indices, **excluding dividends**: they put the index at a disadvantage of about 3% a year against a portfolio that does collect its dividends. Prefer a dividends-reinvested index for a fair comparison.

### Which index should you choose?

Choose the index that most resembles your portfolio: MSCI World for world equities, CAC 40 or Stoxx Europe 600 for French or European equities, a multi-asset index for a portfolio that mixes equities and bonds.

With a bond or money-market index, the Performance tab displays a warning: beta, alpha and correlation measure sensitivity to an equity market and then make little sense. Mainly compare returns and volatilities.

### Limitation

The list is fixed: it is not possible to add another index from the screen.

## What are the 20/80, 60/40 and 80/20 multi-asset indices?
<!-- fiche: ecran-indices-mixtes | questions: what is the 60 40 mixed index ; what does composite index mean ; conservative balanced growth mix ; how is the mixed index calculated ; why rebalanced every month ; which index for an equity and bond portfolio ; 60/40 benchmark | mots: multi-asset index, composite, 60/40, 20/80, 80/20, monthly rebalancing, allocation, conservative, balanced, growth -->

The three indices of the "Multi-asset" family do not exist on the stock market: the software **calculates** them from two components.

| Index | World equities | € government bonds | Short label |
|---|---|---|---|
| Conservative mix | 20% | 80% | Mix 20/80 |
| Balanced mix | 60% | 40% | Mix 60/40 |
| Growth mix | 80% | 20% | Mix 80/20 |

### The components

- **World equities**: the MSCI World, tracked by the first available ETF among CW8.PA, IWDA.AS and EUNL.DE;
- **Bonds**: eurozone government bonds, tracked by DBXN.DE (coupons reinvested), otherwise EUNH.DE.

### The calculation

The index starts at 100. Each day, its value follows that of the two components, each in proportion to the units held. At the **close of the last day of each month**, the units are recalculated to return exactly to the target weights (for example 60% and 40%): this is the monthly rebalancing.

Example: a 60/40 index is worth 100 at the start of a month. If equities rise by 10% and bonds do not move, it is worth `60 × 1.10 + 40 = 106`. Equities then weigh `66 / 106 ≈ 62.3%`. At month end, the index returns to 60% equities (63.60) and 40% bonds (42.40).

### Why use them

A portfolio that mixes equities and bonds, compared with the MSCI World alone, always looks less profitable in rising markets and less risky in falling ones. A multi-asset index with the same mix gives a fairer comparison. The three mixes correspond to the conservative, balanced and growth profiles.

### Limitation

The rebalancing is assumed to be free and perfect, with no fees or tax.

## Which risk-free rate should I use?
<!-- fiche: ecran-taux-sans-risque | questions: what is the risk-free rate ; why 2.50% ; where does the risk-free rate come from ; change the risk-free rate ; does the risk-free rate change the sharpe ; should I put the livret A ; ecb rate estr ; is the risk-free rate constant over the whole period | mots: risk-free rate, risk free rate, ECB, deposit facility, €STR, Sharpe, Sortino, alpha, risk-free return -->

The risk-free rate is the return on a euro investment regarded as risk-free. It is set in the **Settings** panel, in the [[Risk-free rate (% per year)]] field.

### Default value and source

The starting value is **2.50% per year**: the European Central Bank (ECB) deposit facility rate, in force since 16 Sep 2026, as the field's help text recalls. The €STR, the overnight interbank rate, is very close to it.

### What it affects

- the **Sharpe ratio** and the **Sortino ratio**, which measure the return obtained above this rate;
- **Jensen's alpha**;
- the calculations in the Asset management workspace and the PDF report that depend on it.

For daily calculations, the annual rate is converted into a rate per trading day:

`daily rate = (1 + annual rate)^(1/252) − 1`

With 2.50%: `1.025^(1/252) − 1 ≈ 0.0098%` per trading day.

### Setting

The field accepts from 0% to 10%, in steps of 0.25 points (the + and − buttons), or any value typed on the keyboard.

### A limitation to know about

The same rate is applied to the **whole period** analysed, whereas in reality it has varied. Over a long history, the Sharpe ratio is therefore approximate. For a study of an earlier period, you can enter the average rate for that period.

## Setting the VaR confidence level (90, 95 or 99%)
<!-- fiche: ecran-niveau-var | questions: change the var level ; var 95 or 99 which one to choose ; what is the confidence level ; set the var to 99% ; why does the var go up when I switch to 99 ; where do I set the value at risk ; var 90% | mots: VaR, value at risk, confidence level, 95%, 99%, 90%, CVaR, expected shortfall, maximum loss -->

The VaR (Value at Risk) indicates the loss on a bad day. Its confidence level is set **at the top right of the Risk tab** ("Portfolio analysis" workspace), with the [[VaR confidence level]] selector, which offers three values: **90%**, **95%** (starting value) and **99%**. It is no longer in the sidebar: this is the only screen where the VaR is shown. The chosen level is kept for the whole session, even if you change tab or workspace.

### What the level means

With a 1-day VaR at 95%, the loss exceeds this amount only 5% of days, or about one trading day in twenty. At 99%, it is exceeded only one day in a hundred.

For the historical method, the software takes the quantile of daily returns at the threshold `1 − level`: the 5th percentile at 95%, the 1st percentile at 99%, the 10th percentile at 90%.

### Effect of the setting

The higher the level, the further into the bad days you look: VaR and CVaR **increase**. The setting applies to:

- the VaR card and the CVaR card of the Risk tab;
- the table of historical, normal-distribution and Cornish-Fisher VaR;
- the return distribution chart;
- the PDF report.

### Which one to choose?

95% is the most common practice in portfolio management. 99% is that of banking regulation, and is more demanding. Over a short history, the 99% VaR rests on very few days: it is less reliable.

The details of the VaR calculation methods are explained in the chapter on risk.

## The banner at the top of the page and the "Live prices" badge
<!-- fiche: ecran-bandeau | questions: what does cached prices offline mean ; orange badge at the top right ; green dot live prices ; data as of which date ; what does the blue banner at the top show ; why are my prices not up to date ; number of lines in the banner ; what is the date at the top right | mots: banner, header, live prices, cached prices, offline, badge, green dot, orange dot, data date -->

In the analysis spaces, the main area begins with a blue banner.

### On the left

- in small type: "Master G2C · Portfolio management";
- the title "Portfolio tracking";
- a summary line: the period analysed ("From 15/01/2024 to …"), the number of lines held today and the short name of the chosen benchmark index.

### On the right: the source of prices

| Badge | Meaning |
|---|---|
| Green dot, "Live prices · Yahoo Finance" | The latest prices were downloaded from Yahoo Finance during the analysis |
| Orange dot, "Cached prices (offline)" | Yahoo Finance did not respond: the software is using the latest prices saved on the computer |

Under the badge, the "Data as of" line gives the date of the last price in the history: this is the date at which the portfolio is valued.

### If the badge is orange

The calculations remain correct, but as of the date of the latest known prices. Check your Internet connection, then click [[Refresh prices]] at the bottom of the sidebar. The "Prices" line in the sidebar information specifies the date of the cache used.

### Good to know

The results of an analysis are kept in memory for one hour. The badge describes the situation at the time of that calculation: a green badge from forty minutes ago does not guarantee up-to-the-minute prices. The [[Refresh prices]] button forces a new download.

## The key figures at the top of the page
<!-- fiche: ecran-chiffres-cles | questions: what do the figures at the top mean ; what are the six cards ; how is the current value calculated ; does total gain include dividends ; what is annualised performance ; what is the question mark on the cards for ; what is the figure under volatility ; max drawdown at the top of the page | mots: key figures, KPI, indicators, cards, current value, total gain, annualised performance, volatility, Sharpe, max drawdown, summary | aller: Analyse du portefeuille/Vue d'ensemble | chiffres: valeur_actuelle, montant_investi, gain_total, twr_annualise, volatilite, sharpe, max_drawdown -->

Under the banner, six cards summarise the portfolio. They stay displayed in the three analysis workspaces. Hover over the small **?** next to a label to read its definition.

| Card | Big figure | Line below |
|---|---|---|
| Current value | Quantity × latest price, for each line held, in euros | "Invested at average cost": the capital still invested, at cost basis |
| Total gain | Unrealised gains + realised gains + dividends | Badge: gain relative to the capital invested |
| Annualised return | Annualised TWR (time-weighted return) | Badge: total TWR since the start |
| Volatility | Standard deviation of daily returns × √252 | Volatility of the benchmark index |
| Sharpe | (Return − risk-free rate) / volatility | Sharpe of the benchmark index |
| Max drawdown | Worst fall from a peak | Date of the lowest point |

### Reading the colours

The badges are green when the figure is positive, red when it is negative, grey when it is zero.

### Example

A portfolio whose capital invested at cost basis is €10,000 and whose total gain is €1,500 shows "+€1,500" in the Total gain card, with the badge `1,500 / 10,000 = +15.00%` on the capital invested.

### Total gain and performance: why two figures?

The total gain is an amount in euros, which depends on the sum invested and the timing of contributions. The annualised performance (TWR) neutralises contributions and withdrawals: it measures the quality of the investment choices and can be compared with the index. Both are detailed in the chapter on performance.

### Comparing with the index

For volatility and Sharpe, the line below gives the value of the benchmark index chosen in the settings: you see at a glance whether your portfolio is more or less risky, and better or worse rewarded for that risk.

## Getting the PDF report
<!-- fiche: ecran-rapport-pdf | questions: how do I download the pdf report ; generate a pdf of my portfolio ; the pdf report button downloads nothing ; where is the report ; export the analysis to pdf ; the download report button has disappeared ; print the report ; pdf report in english ; install reportlab | mots: PDF report, export, print, download, summary, document, reportlab, write-up -->

The PDF report gathers the complete portfolio analysis in a document ready to print or pass on.

### In two steps

1. At the bottom of the sidebar, click [[PDF report]]. The message "Generating the report..." is displayed during preparation, which may take a few seconds.
2. The button becomes [[Download the PDF report]]. Click it: the file is saved by your browser, usually in the Downloads folder.

The file is called `rapport_portefeuille_` followed by the date of the latest data, for example `rapport_portefeuille_20261006.pdf`.

### The download button has disappeared

Download is only offered if the report matches the current settings exactly. If you change portfolio, benchmark index, risk-free rate or VaR level, the [[PDF report]] button reappears: click again to prepare an up-to-date report.

### Always in French and light

The report is written in French even if the screen is in English, and keeps a white background even in night mode.

### Settings used

The report uses the chosen portfolio, benchmark index, risk-free rate and VaR level. By contrast, for optimisation and projection, it uses fixed settings, not those of the on-screen sliders: maximum weight of 30% per security, 10-year horizon, 5,000 scenarios, normal distribution, no monthly contribution.

### Where is the button?

It only appears once a portfolio has been analysed, in the Portfolio analysis, Wealth advisory and Asset management workspaces. It is absent from the "Manual and help" workspace and from the "My account" and "Add transactions" pages.

### "Install reportlab" message

This message only concerns launching from the source code: the library that produces PDFs is missing. Install it with `python -m pip install reportlab`. The Windows and Mac versions already contain it.

## What does the PDF report contain?
<!-- fiche: ecran-rapport-contenu | questions: what is in the pdf report ; how many pages is the report ; does the report include taxation ; does the report show the holdings ; outline of the pdf report ; is the report complete ; methodology in the pdf ; why is the optimisation not in my report | mots: PDF report, contents, table of contents, pages, summary, holdings, risk, methodology, appendix, outline -->

The report is an A4 document, divided into parts that each start on a new page. Each page carries in its footer the line "Rapport de suivi de portefeuille" (Portfolio tracking report), the date of the day, the reminder "Outil pédagogique, ne constitue pas un conseil en investissement" (Educational tool, not investment advice) and the page number.

### The parts

1. **Summary**: banner with the period, the number of lines and the benchmark index; nine key figures (current value, total gain, gain on capital invested, annualised TWR, annual IRR, volatility, Sharpe, max drawdown, 1-day VaR); evolution chart; amount invested, unrealised and realised gains, dividends, fees and source of prices.
2. **Holdings**: table of lines (ticker, security, quantity, cost basis, price, value, gain or loss, weight), then breakdowns by asset class, region and sector, on a look-through basis.
3. **Exposures and diversification**: diagnosis by dimension (geography, sectors, currencies, concentration, interest rates, real diversification), points to monitor or fix, correlations between lines.
4. **Performance**: comparison with the index, return by calendar year, beta, alpha, correlation, tracking error and information ratio.
5. **Risk**: drawdown, volatility, Sharpe, Sortino, the three VaRs, CVaR, return distribution, skewness, kurtosis and Jarque-Bera test.
6. **Markowitz optimisation**: efficient frontier, minimum-variance and maximum-Sharpe portfolios, allocations compared.
7. **Projection**: 10-year Monte Carlo simulation, unfavourable, median and favourable scenarios, probability of loss, distribution of the final value.
8. **Wealth advisory**: taxation of a full sale depending on the wrapper (CTO, PEA, assurance-vie) and stress tests.
9. **Asset management**: performance attribution, risk budget, backtest of rebalancing strategies and comparison between investing €10,000 all at once or gradually.
10. **Methodology**: definition of each indicator and limitations of the analysis.

### Parts sometimes missing

If a calculation is impossible (for example optimisation, with too few securities for the 30% maximum weight), the corresponding part is omitted or shortened. The number of pages therefore depends on the portfolio.

## Refreshing prices
<!-- fiche: ecran-actualiser-cours | questions: how do I update the prices ; the prices are not today's ; refresh the data ; the refresh prices button does nothing ; force the download of prices ; refresh ; the prices are from yesterday ; reload the page | mots: refresh, update, price update, cache, reload, today's prices, Yahoo Finance -->

The [[Refresh prices]] button is at the very bottom of the sidebar, under the PDF report button.

### What it is for

To stay fast, the software keeps the results of each analysis in memory for **one hour**. As long as that time has not elapsed, it does not download the prices again. The button clears all these results from memory and reloads the page: prices are downloaded again from Yahoo Finance and all the calculations are redone.

### When to use it

- the banner badge shows "Cached prices (offline)" and the Internet connection has come back;
- you leave the software open for a long time and want the most recent prices;
- a recently added security did not yet have a price.

### Internet is needed

Without a connection, refreshing cannot download anything: the software takes the latest saved prices and the badge stays orange.

### Good to know

- Refreshing takes a few seconds longer than usual, since everything is recalculated.
- A PDF report that has already been prepared is not changed: prepare it again if you want the latest prices.

## The information at the bottom of the sidebar
<!-- fiche: ecran-informations | questions: what is the info at the bottom left ; what does 1 € in usd mean ; which period is analysed ; how many transactions does my portfolio have ; where do the prices come from ; the prices line local cache of ; which exchange rate is used ; file updated in the sidebar | mots: information, file, period, transactions, price source, exchange rate, currency, local cache, Yahoo Finance | chiffres: nb_operations -->

Once the portfolio has been analysed, a small block of information appears at the bottom of the sidebar, above the report and refresh buttons.

| Line | Content |
|---|---|
| File | The name of the portfolio or file analysed. The label "(updated)" indicates that transactions have been added to it during the session without being saved |
| Period | First and last date of the valued history |
| Transactions | The number of transactions read (purchases, sales, dividends) |
| Prices | The source of the latest prices: "Yahoo Finance (live)", or "local cache of" followed by the date, with the note "Yahoo Finance unreachable" |
| Exchange rates (n) | Folded by default: click it to show one line per foreign currency in the portfolio ("€1 in USD", "€1 in GBP"…), the day's exchange rate used to convert securities into euros, to four decimal places. The number in brackets is the number of currencies |

### Reading an exchange rate

"€1 in USD · 1.0850" means that one euro is worth 1.0850 dollars. A share quoted at 200 USD is therefore worth `200 / 1.0850 ≈ €184.33`. A portfolio entirely in euros has no rate line, and "Exchange rates" does not appear.

### After uploading a file

When an uploaded file has been recognised automatically, an additional note indicates the number of transactions and securities recognised, and flags, for example, that an image PDF was read by character recognition.

## Asking the manual's assistant a question
<!-- fiche: ecran-assistant | questions: how do I use the help ; ask the software a question ; the assistant can't find my answer ; is it artificial intelligence ; does the help work without internet ; where is the chatbot ; the go to button doesn't open the right tab ; why does the assistant show my figures | mots: assistant, help, question, search, FAQ, chatbot, manual, offline, Manual and help | aller: Manuel et aide -->

The assistant is in the **Manual and help** workspace, right at the top, in the [[Ask a question]] field.

### How to do it

1. Choose the "Manual and help" workspace in the sidebar.
2. Type your question in your own words, for example "how do I delete a transaction?", then press Enter.
3. The manual entry that best answers is displayed in full, with the name of its chapter.

Three clickable examples are offered under the field, such as [[How do I delete a transaction?]] or [[What does the Sharpe ratio mean?]].

### What accompanies the answer

- **See also**: up to three other related entries; a click opens the entry.
- **For your portfolio**: some entries display your own figures (for example your Sharpe ratio). These are those of the last portfolio analysed during the session: display an analysis workspace first so that they are available.
- **The "Go to" button**: it opens the relevant workspace. If the entry concerns a specific tab, a message in the sidebar tells you which tab to open, which you still have to click.

### It is not artificial intelligence

The assistant writes nothing: it searches the manual for the entry closest to your question (title words, common phrasings, synonyms, text) and displays it as written. It tolerates typing mistakes and missing accents. It works without Internet and sends nothing.

### If it does not find anything

It says so and offers the closest entries. Try other words, simpler or more technical. Your question is then recorded on the computer to complete the manual (see the entry on unanswered questions).

## The help bubble at the bottom right of the screen
<!-- fiche: ecran-bulle-aide | questions: what is the help button at the bottom right ; ask a question without leaving my tab ; where is the help bubble ; how do i close the small help window ; the bubble does not find my answer ; see my previous questions again ; the help button hides part of the screen ; quick help while looking at my charts | mots: bubble, help, chat, help window, floating button, quick question, assistant, popup, panel | aller: Manuel et aide -->

The [[Help]] button, fixed at the bottom right of the screen, is visible on every page: the three analysis workspaces, "Manual and help", "My account" and "Add transactions". It lets you ask the manual a question without leaving the current tab.

### How to do it

1. Click [[Help]]: a small panel opens above the button.
2. Type your question in your own words, then press Enter or click [[Send]].
3. The panel shows the title of the article that answers, its beginning (with the formula if there is a short one) and, where the article allows, your own figures.
4. Click outside the panel, or on [[Help]] again, to close it.

### The links under the answer

- [[Read the full article]]: opens the "Manual and help" space on the whole article.
- [[Go to the screen]]: opens the workspace concerned; if the article is about a specific tab, a message in the sidebar tells you which tab to open.
- **See also**: up to three related articles; a click shows their beginning in the panel.
- [[This is not the answer I was looking for]]: records the question on the computer to improve the manual.
- **Your previous questions**: the last five questions of the session; a click shows the answer again. They are forgotten when the software is closed.

### Same engine as the manual's assistant

The bubble uses exactly the same search as the [[Ask a question]] field in the "Manual and help" space: offline, without artificial intelligence, tolerant of typing errors. A question without a reliable answer is recorded in the same way (see the article on unanswered questions). The button does not appear in the PDF report or when printing.

## Browsing the manual's contents
<!-- fiche: ecran-sommaire-manuel | questions: where is the manual ; read the whole manual ; help contents ; download the manual as pdf ; manual in word ; how do I move from one chapter to another ; user guide for the software ; full documentation | mots: manual, contents, chapters, user guide, documentation, entries, Word, PDF | aller: Manuel et aide -->

Under the assistant, the **Manual contents** box gives access to the whole manual. Its subtitle shows the number of chapters and entries.

### How to browse it

1. Choose a chapter in the [[Chapter]] list (chapters are numbered in the recommended reading order).
2. The chapter's introduction is displayed, followed by its entries, one per question.
3. Click an entry's title to expand it, and again to collapse it.

An entry opened from "See also" is already expanded in the contents.

### The bold elements

In the entries, the names of buttons, tabs or fields are written in bold, exactly as they appear on screen: search for them as they are.

### Downloading the full manual

When your version of the software is supplied with the exported manual, "Full manual (Word)" and "Full manual (PDF)" buttons appear under the entries. Otherwise, these buttons are absent and the manual can only be consulted on screen.

### Language

The manual is displayed in the screen language if its translation is installed, otherwise in French.

## Unanswered questions and exporting them
<!-- fiche: ecran-questions-sans-reponse | questions: where are the unanswered questions ; export unresolved questions ; is my question sent anywhere ; how can I help improve the manual ; delete my question history ; questions_sans_reponse.csv file ; send my questions to the teacher | mots: unanswered questions, log, export, CSV, manual improvement, user feedback, privacy | aller: Manuel et aide -->

When the assistant does not find a reliable answer, your question is recorded in a file, **on this computer only**. It is never sent automatically.

### Viewing them

At the bottom of the "Manual and help" workspace, a collapsed panel titled "Unanswered questions", followed by their number in brackets, appears as soon as at least one question has been recorded. Open it to see the 30 most recent, with their date and time.

### Exporting them

The [[Export the questions (CSV)]] button downloads the complete file, `questions_sans_reponse.csv`, with two columns: date and question. Pass it on to the software's creator or to your teacher: each question added to the manual improves the assistant.

### Details

- Each question is limited to 300 characters.
- The same question typed several times in a row is recorded only once.
- The file is stored in the software's `data` folder, under the name `questions_sans_reponse.csv`. Deleting it erases the history; the software has no button to do this.

## Chart tips: zoom, hover, legend
<!-- fiche: ecran-graphiques | questions: how do I zoom in on a chart ; go back to the full chart after zooming ; hide a curve ; show the exact value of a point ; the chart is too small ; how do I see only the last year ; save the chart as an image ; I can't zoom on the map | mots: chart, zoom, hover, tooltip, legend, double-click, Plotly, period, 1M, 6M, YTD, interactive -->

The dashboard's charts are interactive.

### Hover to read values

Move the mouse over a curve, a bar or a country: a bubble shows the exact value. On evolution charts, the bubble gathers all the curves at the same date, which lets you compare the portfolio and the index, or the value and the capital invested, at a glance.

### Zoom by click and drag

Click and drag the mouse over the area that interests you: the chart enlarges on that area. You can repeat the action to zoom in further.

### Returning to the original view

**Double-click** the chart.

### Choosing a period

The "Portfolio value over time" charts and the comparison with the index have buttons above the curve: **1M** (one month), **6M** (six months), **YTD** (since 1 January), **1Y** (one year) and **All**.

### Hiding or isolating a curve

Click a name in the legend, under the chart, to hide the corresponding curve; click again to show it again. A double-click on a name in the legend shows only that curve.

### Limitations

- The world map cannot be zoomed: hovering over countries remains possible.
- The charts' toolbar is hidden; there is therefore no button to save a chart as an image. To keep charts, use the PDF report or a screenshot.
- The charts adapt to the width of the window: enlarge it or collapse the sidebar to see them larger.
