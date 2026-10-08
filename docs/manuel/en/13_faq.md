# Frequently asked questions
<!-- chapitre: faq | ordre: 13 -->

This chapter gives short answers to the questions most often asked about Portfolio Tracker, including those from a jury or a teacher during a thesis defence: reliability, sources, confidentiality, methodological choices and limitations. Each answer refers, where needed, to the chapter that covers the subject in detail.

## Is the software reliable?
<!-- fiche: faq-fiabilite | questions: is the software reliable ; can I trust the results ; are the calculations right ; are the numbers accurate ; how much should I trust portfolio tracker ; can the software be wrong ; reliability of the indicators | mots: reliability, trust, accuracy, calculations, checks, tests, limitations, educational tool -->

Yes for its **calculations**, with reservations about its **data**.

### What is solid

- **The formulas** are those of the financial literature (TWR, IRR, Sharpe, VaR, Markowitz, Brinson-Fachler…) and are described exactly in the "All the formulas" chapter.
- **The calculations are tested** automatically on examples whose result is known (see the fiche "How do you know the formulas are right?").
- **The checks** stop the analysis rather than display a wrong figure: sale of securities not held, missing price or exchange rate, unknown transaction type.
- **The source** of prices and the date of the data are always displayed.

### The reservations

- Prices come from **a single source**, Yahoo Finance, with no cross-checking.
- The result depends on **your transactions**: a forgotten dividend or an unentered stock split distorts the analysis.
- Some data are **fixed and dated** (ETF composition, risk-free rate, classification of securities).

### In short

It is a reliable educational tool for analysing and understanding a portfolio. It replaces neither the official statements of your institution nor investment advice.

## How do you check that prices are right?
<!-- fiche: faq-verification-cours | questions: how do you check that prices are right ; are prices checked ; what happens if yahoo gives a wrong price ; do you cross-check prices with another source ; price checks at import ; what should I say to the jury about data quality | mots: verification, price checks, data quality, Yahoo Finance, 25% gap, cross-check, closing price -->

### What the software does

1. It uses the **raw closing price** (not adjusted for dividends): anyone can compare it with that of the exchange or their broker.
2. **At import**, with Internet access, each purchase and sale price in your file is compared with the Yahoo Finance closing price of the same day. A gap of more than 25% is flagged. This cross-check reveals an entry error just as well as a wrong security or an abnormal price.
3. A ticker without a listing venue is only kept if its price matches yours (median gap below 15%).
4. A missing price, history or exchange rate **stops** the analysis, with a message naming the security.

### What it does not do

It does not compare prices with a second source and does not look for outliers in the history. A suspended security keeps its last known price.

### What you can say

"The prices are the daily closing prices from Yahoo Finance, not adjusted for dividends; transaction prices were checked against these prices, with an alert threshold of 25%; prices were not cross-checked with a second source." For an important figure, check it on the exchange's website or your broker's.

## Why Yahoo Finance and not Bloomberg?
<!-- fiche: faq-pourquoi-yahoo | questions: why yahoo finance ; why not bloomberg or refinitiv ; is yahoo finance a serious source ; can I change the data source ; why a free source ; where does the yahoo data come from | mots: Yahoo Finance, Bloomberg, Refinitiv, data source, free, yfinance, subscription, provider -->

### The reasons for the choice

- **Free and no subscription**: the software is an educational tool, usable by any student; a Bloomberg terminal or Refinitiv access is paid and reserved for subscribers.
- **No account or access key**: the software queries Yahoo Finance through the Python `yfinance` library, with no login.
- **Wide coverage**: stocks and ETFs from the world's main exchanges, indices and exchange rates, with a daily history of several years.
- **Security recognition**: its search engine makes it possible to find a ticker from an ISIN or a name.

### The trade-offs

Yahoo Finance does not guarantee the quality of its data and may be temporarily unavailable. That is why the software keeps a cache and a local database, and always displays the source used.

### Changing source

The software offers no setting for this. In the code, all access to prices is isolated in a single file (`src/market_data.py`): changing provider would only require modifying that file.

## Is my data confidential?
<!-- fiche: faq-confidentialite | questions: is my data confidential ; is my portfolio sent over the internet ; who can see my data ; is it secure ; do my amounts go to yahoo ; gdpr and privacy ; is the software safe | mots: confidentiality, privacy, security, encryption, localhost, GDPR, personal data -->

With the installed version, yes.

### Everything stays on your computer

- The dashboard runs at the `localhost` address: it accepts no connection from any other device.
- Your files are read and processed on your computer.
- Portfolios saved in your space are **encrypted** with a key derived from your password (PBKDF2 and Fernet): neither other users nor an administrator can read them.

### What goes out over the Internet

Only the **security codes** (tickers) to obtain prices and, to recognise an unknown security at import, its ISIN or name. Quantities, amounts and the portfolio composition are never sent.

### The exceptions

- **The online version** runs on a remote server: your files are processed there. Prefer the installed version for real data.
- A few shared local files are not encrypted (price cache, security memory, log of unanswered questions): they contain no quantity or amount, but reveal which securities have been analysed.

The details are in the chapter "Your account and the security of your data".

## Can the software's creator see my portfolio?
<!-- fiche: faq-createur | questions: can the creator see my portfolio ; does the developer have access to my data ; can my teacher see my positions ; is there any telemetry ; does the software send statistics ; can anyone else read my portfolios | mots: creator, developer, teacher, telemetry, usage statistics, data access, encryption -->

**No.** With the installed version, the creator receives nothing:

- there is **no server** for the software: your account exists only on your computer;
- Streamlit's usage statistics collection is **disabled**, in the project configuration and at launch;
- questions put to the assistant stay in a local file;
- the software does not even check whether updates exist.

### Even with your computer in someone's hands

Your saved portfolios are encrypted with your password. Without it, nobody, creator included, can read them or reset that password.

### Your teacher

They only see your portfolios if you yourself send them a file (CSV export, PDF report) or show them your screen.

### On the online version

The software runs there on a server administered by the person who published the site: files you send there are processed on that server.

## Does the software work without Internet?
<!-- fiche: faq-hors-connexion | questions: does the software work without internet ; can I use it offline ; no wifi during the defence ; airplane mode ; what happens without a connection ; how old are the prices without internet | mots: offline, without Internet, local database, cache, defence, airplane mode -->

**Yes, largely.** The software is delivered with a local database of several thousand securities, indices and exchange rates, with their daily prices (since 2015 for securities, 2007 for indices and currencies).

### What works offline

Opening the software, signing in, analysing a portfolio whose securities are in the database or the cache, importing a CSV or Excel file, all the analyses, the PDF report, the assistant and the manual.

### What requires Internet

Today's prices, a security never seen before, recognition of an unknown ISIN, the [[Refresh prices]] button, and the world map if its background has never been saved.

### How to tell

The banner displays "Cached prices (offline)" with an orange dot, and the sidebar shows the date of the latest known prices. The calculations remain correct, but stop at that date.

### Tip for a defence

The day before, analyse your portfolio with Internet: its prices will be added to the database and the cache, and on the day, the software will work even without a network.

## What are the limitations of the normal distribution in the software?
<!-- fiche: faq-loi-normale | questions: limitations of the normal distribution ; why use the normal distribution when returns are not normal ; normal var underestimates risk ; fat tails ; how does the software correct the normal distribution ; criticism of the normality assumption | mots: normal distribution, normality, fat tails, Jarque-Bera, Cornish-Fisher, bootstrap, historical VaR, crash | aller: Analyse du portefeuille/Risque -->

### Where the software uses the normal distribution

- the **normal-distribution VaR** (parametric);
- the Monte Carlo projection, **"Normal distribution"** method (geometric Brownian motion);
- the comparison curve on the returns histogram.

### Its main limitation

Real returns have **fat tails** and often **negative skewness**: crashes are more frequent than the normal distribution predicts. It therefore underestimates extreme losses, especially at 99%.

### What the software offers to go beyond it

1. **It measures the gap**: skewness, excess kurtosis, share of days beyond 3 standard deviations (against 0.27% expected) and the Jarque-Bera test, in the Risk tab.
2. **It compares several VaRs**: historical (no distribution assumption), normal distribution, Cornish-Fisher (corrected for skewness and kurtosis), and the CVaR.
3. **It offers a "Historical (bootstrap)" projection**, which draws real days from the portfolio and keeps its actual crashes.
4. **It complements this with stress tests** that replay real crises.

### Key point

The normal distribution remains a simple, standard benchmark; the software always presents it next to measures that do not assume it.

## TWR or IRR: which one should I look at?
<!-- fiche: faq-twr-tri | questions: difference between twr and irr ; which to look at twr or irr ; why is my irr different from my twr ; what performance should I give my client ; twr or mwr ; which one is my real performance | mots: TWR, IRR, TRI, performance, time-weighted return, money-weighted return, contributions, timing, comparison | aller: Analyse du portefeuille/Performance | chiffres: twr_annualise, tri_annuel -->

Both are correct: they answer two different questions.

| | TWR | IRR |
|---|---|---|
| Question | Were the security choices good? | How much has my money earned? |
| Effect of contributions | neutralised | taken into account |
| Comparable to an index | yes | no |
| Used by | fund managers (GIPS standard) | the investor, for their own money |

### Example

€10,000 gains 20% in the first year; you then add €50,000, and the portfolio then loses 10%. The TWR is +8% over two years (+3.9% a year): the security choices were good on average. The IRR is −6.05% a year: the fall hit a much larger sum than the rise, and you lost money.

### Which one to look at

- To **judge the management** or compare it with an index: the TWR.
- To know **what your money has really earned**: the IRR.
- An IRR above the TWR means your contributions were well timed.

The exact formulas are in the "All the formulas" chapter.

## How good is Markowitz optimisation really?
<!-- fiche: faq-markowitz | questions: how good is markowitz optimisation ; should I follow the optimal portfolio ; limitations of markowitz ; why does the optimiser concentrate on a few securities ; is the maximum sharpe portfolio reliable ; markowitz criticism from a jury ; why a 30% maximum weight | mots: Markowitz, optimisation, efficient frontier, estimation error, expected returns, maximum weight, concentration, risk parity | aller: Analyse du portefeuille/Optimisation -->

It is an **excellent teaching tool** and a poor autopilot.

### What it shows well

- the value of diversification: combining weakly correlated securities reduces risk;
- the efficient frontier: no randomly drawn portfolio does better, for equal risk;
- the gap between your allocation and a more efficient allocation, with the amounts to buy or sell.

### Its limitations, known and acknowledged

- **Expected returns are past averages**: the optimiser over-exploits the securities that have done best, with no guarantee for the future. A small error on these returns changes the weights considerably.
- **Concentration**: with no limit, it often puts almost everything in 2 or 3 securities. Hence the [[Maximum weight per security]], 30% by default.
- **No fees, no taxation**: adjustments are calculated excluding fees and without the tax on a sale.
- **A single period**: volatilities and correlations are assumed to be stable.

### What the software offers alongside

**Risk parity** and **minimum variance**, in the [[Risk budget]] tab, do not use expected returns, the main source of error.

The screen reminds you: "Academic exercise, not investment advice."

## Is this investment advice?
<!-- fiche: faq-conseil | questions: is this investment advice ; can I follow the software's recommendations ; is the software telling me to buy ; are the diagnostic suggestions advice ; liability in case of loss ; regulated tool ; does the software replace an adviser | mots: investment advice, recommendation, liability, educational tool, diagnostic, suggestions, warning, regulation -->

**No.** The footer of every screen says so: "Educational tool developed as part of the Master G2C — not investment advice."

### Why

- The software knows neither your situation, nor your objectives, nor your horizon, nor your risk tolerance.
- Its calculations rely on the past, which is no guide to the future.
- The diagnostic **suggestions** (Exposures tab) derive from simple rules with documented thresholds; the screen states: "Educational analysis based on simple rules and past data: it is not investment advice."
- Optimisation is presented as an "academic exercise".
- Taxation is simplified.

### Proper use

Understanding, measuring and discussing a portfolio: it is a support for learning and dialogue. An investment decision is up to you, or to an authorised professional who knows your situation.

## Can I manage several accounts and several portfolios?
<!-- fiche: faq-plusieurs-portefeuilles | questions: can I have several portfolios ; several accounts on the same computer ; my pea and cto separate ; combine two portfolios into one ; consolidated view of all my accounts ; how many portfolios per account ; one portfolio per client | mots: several portfolios, several accounts, consolidation, combine, PEA, CTO, multi-user, personal space -->

### Several accounts

Yes: each person using the computer creates their own account, with their own password. Everyone sees only their own portfolios.

### Several portfolios per account

Yes: save as many portfolios as you like (for example a PEA (French equity savings plan) and a securities account). They appear in the list in the "Data" section, preceded by "My space". The [[My account]] page lets you rename, download or delete them.

### A consolidated view?

The software analyses **one portfolio at a time**: there is no view that automatically adds several portfolios together. For a global analysis:

1. download one of the portfolios from [[My account]] (CSV file);
2. open the other one, click [[Add transactions]] and upload that file;
3. check the table, then [[Save transactions]].

Identical transactions are recognised as duplicates. To keep the two portfolios separate as well, work on a copy: first add the downloaded file as a new portfolio in [[My account]], then add the other one's transactions to it.

### For an adviser

One portfolio per client works the same way, but the software has no client record and no regulatory profile.

## Can the software connect to my bank?
<!-- fiche: faq-connexion-bancaire | questions: automatic bank connection ; synchronise with my broker ; import automatically from boursorama ; does the software connect to my bank ; account aggregation ; bank api ; automatic update of my transactions | mots: bank connection, synchronisation, aggregator, API, broker, automatic import, PSD2 -->

**No.** The software connects to no bank and no broker, and places no orders. This is also a confidentiality guarantee: it never asks for your banking credentials.

### How to get your transactions into it

1. **An export** from your bank or broker, as CSV or Excel: upload it with [[Upload a file (CSV, Excel or PDF)]]; the automatic import recognises most formats, otherwise the import wizard guides you.
2. **A PDF statement or trade confirmation** (several at once if you wish, even password-protected): it is read automatically, whatever the broker (text PDF, or image if character recognition is installed); if it is not recognised, the [[Complete the transaction]] form suggests the values found in the document.
3. **Manual entry**: [[Add transactions]], [[Manual entry]] tab.

### Updating afterwards

No need to send everything again: with [[Add transactions]], upload only the new movements. Transactions already present are recognised and are not added twice.

## Are bonds, gold and money-market funds supported?
<!-- fiche: faq-classes-actifs | questions: does the software handle bonds ; can I track gold ; money market fund supported ; bond etf ; direct bonds ; life insurance euro funds ; multi-asset portfolio | mots: bonds, gold, money market, asset class, bond ETF, duration, euro funds, multi-asset | aller: Analyse du portefeuille/Expositions -->

**Yes, if they are listed** and have a Yahoo Finance ticker, which is the case for bond, gold or money-market ETFs.

### How they are treated

- **Asset class**: Equities, Bonds, Gold or Money market, from the project's reference database, otherwise the local database. A security of unknown class is counted as an equity.
- **Bonds**: their **duration** (if the reference database gives it) is used for interest-rate sensitivity and the rate shock.
- **Gold**: counted separately, "without country", in the look-through analysis.
- **Suitable benchmark indices**: euro-zone government bonds, corporate bonds, €STR money market, or mixed 20/80, 60/40 and 80/20.
- **Coupons**: to be recorded as dividends (DIVIDENDE type).

The sample portfolio "Diversified portfolio (multi-asset)" illustrates these classes.

### What is not supported

Any product without a daily price on Yahoo Finance: life insurance euro funds, savings accounts, directly held bonds with no quotation, structured products. They cannot be valued.

### Note

Performance attribution covers only the **equity portion**; bonds and gold are excluded from it.

## How are currencies handled?
<!-- fiche: faq-devises | questions: does the software handle dollar stocks ; in which currency should I enter the price ; how are foreign securities converted ; is currency risk taken into account ; london stocks in pence ; exchange rate used ; my fees in dollars | mots: currencies, exchange rate, conversion, dollar, pound, pence, currency risk, euro, hedging -->

Everything is expressed **in euros**.

### On entry

- The **price** is entered in the security's **quote currency** (dollars for Apple, pence for a London stock).
- **Fees** are always in euros.
- At import, the software compares each price with that day's price and recognises a price already converted into euros, in currency or in pence; it brings it back to the quote unit.

### The conversion

`price in euros = price in currency × factor / EURcurrency rate` (factor 0.01 for pence), at the rate of the day of each transaction for purchases, sales and dividends, at each day's rate for the history, at the last known rate for the current value. Rates come from Yahoo Finance and are shown at the bottom of the sidebar.

### Currency risk

The performance of a foreign security includes the change in its currency. The Exposures tab measures the **real exposure** to currencies, ETFs included: a world ETF quoted in euros remains exposed to the dollar, unless it is hedged ("EUR Hedged"). The stress tests include a 10% fall in the dollar.

## How are fees taken into account?
<!-- fiche: faq-frais | questions: are fees taken into account ; brokerage fees in performance ; etf management fees ; custody fees ; are fees in the pru ; fees in the optimisation ; ter of my etf | mots: fees, brokerage fees, PRU, management fees, TER, custody fees, net performance, backtest | chiffres: frais_totaux -->

### Brokerage fees

Entered in euros in the `frais` column of each transaction, they count everywhere:

- **on a purchase**, they increase the PRU (unit cost basis);
- **on a sale**, they reduce the realised gain;
- **on a dividend**, they are deducted from the amount received;
- **in performance**, they are part of the flows: the return on the purchase day includes them.

Their total appears in the "Brokerage fees" card of the Overview.

### ETF management fees

They are taken within the fund and are therefore **already included in its price**: there is nothing to enter.

### Custody fees and other account fees

These are not securities transactions: at import, custody or transfer fee lines are ignored. They are therefore not deducted from performance.

### In the advanced analyses

- **Optimisation**: the amounts to buy or sell are calculated excluding fees.
- **Backtest**: adjustable transaction fees (0.10% by default) apply to each purchase and rebalancing.
- **Taxation**: life insurance contract management fees are ignored.

## How are dividends taken into account?
<!-- fiche: faq-dividendes | questions: are dividends taken into account ; how do I enter a dividend ; does the software download my dividends ; dividends in performance ; accumulating etf and dividends ; why does the price fall on the ex-dividend date ; bond coupons | mots: dividends, coupons, ex-dividend, accumulating ETF, distributing ETF, performance, entry, DIVIDENDE | chiffres: dividendes -->

### They count, provided they are entered

The software does **not** download dividends: only those in your transactions count. A dividend line is written with the type DIVIDENDE, a quantity of 0 and the **total amount received** in the price column (in the quote currency), with any fees separate.

### Their effect

- they add to the **total gain** (net of fees);
- they count in **performance** (TWR, IRR) as money taken out;
- they are shown per holding in the Holdings tab and in total in the "Dividends and coupons" card.

### Why this is essential

The software uses the **unadjusted** price: on the ex-dividend date, the price falls by roughly the amount of the dividend. If the dividend is not entered, this fall appears as a loss and performance is underestimated.

### ETFs

- **Accumulating**: dividends are reinvested in the price; nothing to enter.
- **Distributing**: to be entered as for a stock.

Coupons from a distributing bond fund are entered in the same way.

## Can I get a report to hand in or print?
<!-- fiche: faq-rapport-pdf | questions: can I get a pdf report ; report to hand in for my dissertation ; print the analysis ; is the report in english ; export the results ; report for my client ; does the report use my settings | mots: PDF report, export, printing, dissertation, summary, document, appendix, reportlab -->

**Yes.** At the bottom of the sidebar, click [[PDF report]], then [[Download the PDF report]].

### Its content

An A4 document that covers the whole analysis: summary and key figures, holdings, exposures and diversification, performance, risk, optimisation, projection, wealth advisory (taxation, stress tests), asset management (attribution, risk budget, backtest) and a **methodology** section that defines each indicator and its limitations.

### Its particulars

- It is always **in French** and on a light background, even if the screen is in English or in night mode.
- It uses the portfolio, benchmark index, risk-free rate and VaR level chosen, but **fixed** settings for the optimisation (maximum weight of 30%) and the projection (10 years, 5,000 scenarios, normal distribution, no contributions).
- Each page reminds you that it is an educational tool, not investment advice.

### Other exports

- the transaction history as CSV, in the Transactions tab;
- each portfolio in your space as CSV, from [[My account]].

## Does the software run on Mac?
<!-- fiche: faq-mac | questions: does the software run on mac ; macos version ; is intel mac compatible ; install on macbook air m1 ; which version of macos is needed ; does it work on linux ; ipad or chromebook | mots: Mac, macOS, Apple Silicon, M1, Intel, dmg, Linux, compatibility, online version -->

**Yes, on recent Macs.**

| Computer | Solution |
|---|---|
| Apple Silicon Mac (M1, M2, M3, M4…), macOS 12 or later | `Portfolio_Tracker_Mac.dmg` application |
| Intel Mac (sold before the end of 2020) | online version of the dashboard |
| Windows 10 or 11, 64-bit | `Installer_Portfolio_Tracker.exe` installer |
| Linux | launch from the source code (Python 3.11 or later) |

### On Mac, good to know

- On first launch, macOS blocks the application, which does not come from the App Store: you have to allow it once (see the "Getting started" chapter).
- A Terminal window opens: leave it open, closing it stops the software.
- The dashboard opens in Chrome, Edge or Brave in "application" mode if they are installed, otherwise in Safari.
- Your accounts are stored in `~/Library/Application Support/Portfolio Tracker` and kept during updates.

The screens, calculations and report are identical on Windows and on Mac.

## How do I know whether an update exists?
<!-- fiche: faq-mises-a-jour | questions: how do I update the software ; does the software update itself ; is there a new version ; do I lose my data when updating ; version number ; does the securities database update itself | mots: update, new version, Releases, GitHub, version, reinstallation, securities database -->

The software **does not itself check** whether a new version exists (that is also why it sends nothing to its creator).

### Where to look

On the project's releases page: `https://github.com/DieuUssop/Python/releases/latest`. Each version carries a number made up of its build date (for example "2026.10.05").

### Installing the new version

Close the software, then install the new version **over** the old one, without uninstalling. Your accounts and saved portfolios are kept. As a precaution, still download a copy of your portfolios from [[My account]].

### Prices, for their part, update themselves

Each analysis with Internet downloads recent prices and adds them to the local database. A new version also brings a more recent securities database and, where relevant, revised reference data (risk-free rate, ETF composition).

## What are the software's known limitations?
<!-- fiche: faq-limites | questions: what are the limitations of the software ; what does the software not do ; weak points of portfolio tracker ; possible improvements ; criticisms from the jury ; what the software does not handle ; methodological limitations | mots: limitations, weak points, improvements, simplifications, assumptions, constraints, outlook -->

### Data

- a single price source (Yahoo Finance), with no cross-checking or outlier detection;
- dividends not downloaded: only those entered count;
- stock splits and reverse splits adjusted only from the broker's notice; mergers and other corporate actions not handled;
- ETF composition, classification of securities and risk-free rate fixed and dated;
- country of a stock in the local database deduced from its listing venue.

### Method

- risk-free rate constant over the whole period;
- normal distribution for the parametric VaR and one of the projection methods;
- Markowitz based on past returns;
- stress tests without currency effect and on prices excluding dividends;
- simplified taxation (no progressive scale, no contract fees);
- attribution limited to the equity portion, by major regions.

### Operation

- only three transaction types: buy, sell, dividend; no short selling;
- no bank connection;
- one portfolio analysed at a time;
- forgotten password = lost portfolios;
- no Intel Mac; temporary accounts on the online version;
- no automatic update.

The project itself cites, as a possible improvement, the use of the historical €STR series for the risk-free rate.

## What should I do if the assistant cannot find my answer?
<!-- fiche: faq-assistant | questions: the assistant cannot find my answer ; I did not find a reliable answer ; the help does not understand my question ; how do I ask a good question ; is the assistant an ai ; send my question to the creator | mots: assistant, help, search, question, unanswered, rephrase, contents, export | aller: Manuel et aide -->

The assistant searches this manual for the entry closest to your question and displays it as written. It is not an artificial intelligence writing text: it cannot invent anything, but it may fail to find an answer.

### Try in this order

1. **Rephrase** with other words, simpler ("remove a purchase") or more technical ("delete a transaction").
2. **One question at a time**, short.
3. **The exact name** of an indicator or a button: "VaR", "PRU", "Refresh prices".
4. **The related entries** suggested under the answer.
5. **The contents**: choose a chapter and open its entries.
6. **This chapter**, the "Error messages and problems" chapter and the **glossary**.

### Getting the manual completed

Your unanswered question is recorded on this computer. In the "Manual and help" area, the section for unanswered questions lets you export them with [[Export the questions (CSV)]] and send them to the software's creator. Do not type any personal information there: these questions are visible to all users of the computer.

## Why do my figures differ from my bank's?
<!-- fiche: faq-ecart-banque | questions: why do my figures differ from my bank ; my pru is not the same as at my broker ; the value of my portfolio is different ; my performance does not match my bank's ; gain gap with my statement ; why is the gain different | mots: gap, bank, broker, PRU, valuation, performance, exchange rate, price, difference -->

Several causes, often combined.

| Difference | Explanation |
|---|---|
| Value | Yahoo Finance closing price, not real-time price; another listing venue is possible |
| Foreign securities | Yahoo Finance exchange rate, not your bank's |
| PRU | the software includes purchase fees; some banks do not |
| Capital gains | depend on the PRU, and therefore on fees and exchange rates |
| Total gain | includes the dividends entered; without them, it is lower |
| Performance | the software calculates TWR and IRR; your bank may show another measure (gain in %, performance since 1 January…) |
| History | a missing transaction or an unentered stock split changes everything |

### How to check

1. First compare the **quantities** held (Holdings tab).
2. Then the **prices** and the "Data as of" date in the banner.
3. Then the **transactions** (Transactions tab), in particular dividends and old purchases.

For official amounts, especially tax ones, your institution's documents are what count.

## Can I use the software for my tax return?
<!-- fiche: faq-declaration-impots | questions: can I use the software for my tax return ; are the calculated gains taxable ones ; exact tax calculation ; does the software replace the ifu ; is the software's taxation reliable ; 2026 rates used | mots: tax return, taxation, taxable gains, PFU, tax documents, simplifications, IFU | aller: Conseil patrimonial/Fiscalité -->

**No.** The figures are reliable for analysis and comparison, not for a tax return.

### Why

- The software calculates the tax on a **hypothetical full sale**, to compare CTO (securities account), PEA (equity savings plan) and assurance-vie (life insurance), with 2026 rates (flat tax or PFU of 31.4%, PEA after 5 years, life insurance after 8 years).
- It **simplifies**: option for the progressive scale ignored, life insurance premiums assumed below €150,000, contract fees ignored, dividends assumed to be kept within the wrapper.
- Its prices and exchange rates come from Yahoo Finance, not from your institution.
- It only knows the transactions you give it.

### What counts

The tax documents and statements sent by your bank or broker.

### What the Taxation tab is for

Understanding the effect of the wrapper and the holding period: it shows the net gain according to the year of exit, with the 5-year (PEA) and 8-year (life insurance) thresholds, and the share of the portfolio eligible for a PEA.

## How do you know the formulas are right?
<!-- fiche: faq-calculs-testes | questions: how do you know the formulas are right ; are the calculations tested ; automatic tests of the software ; pytest ; how to prove the twr is correctly calculated ; validation of the calculations ; cross-check | mots: tests, pytest, validation, verification, formulas, cross-check, accuracy, code quality -->

### Automatic tests

The project contains a `tests` folder with about 150 automatic tests, run by the developer with the command `python -m pytest`. They check the calculations on examples whose result is known: PRU, capital gains, TWR, IRR, volatility, VaR, currencies, optimisation, simulation, file import, encrypted accounts…

### Cross-checks

Some mathematical properties must always be true; the tests check them:

- the gain calculated day by day (`value − net contributions`) lands exactly, on the last day, on the total gain calculated line by line;
- the sum of the risk contributions equals the portfolio volatility (Euler property);
- the sum of the attribution effects equals the performance gap with the index (Cariño smoothing).

### Transparent formulas

Each formula is written and commented in the code (`src` folder) and reproduced in the "All the formulas" chapter, with a worked example that anyone can redo with a calculator or in a spreadsheet.

### What the tests do not cover

They do not check Yahoo Finance's data themselves, nor your transactions.

## What is the software programmed with?
<!-- fiche: faq-technologies | questions: what is the software programmed with ; which language ; is it made in python ; which libraries are used ; what is streamlit ; how are the installers built ; architecture of the software | mots: Python, Streamlit, pandas, NumPy, SciPy, Plotly, Matplotlib, ReportLab, yfinance, cryptography, GitHub Actions, architecture -->

The software is written in **Python** (version 3.11 or later from the source code).

### The libraries

| Role | Library |
|---|---|
| Dashboard | Streamlit |
| Calculations | pandas, NumPy, SciPy (optimisation) |
| Interactive charts | Plotly |
| Report charts, PDF report | Matplotlib, ReportLab |
| Stock prices | yfinance (Yahoo Finance) |
| Account encryption | cryptography (PBKDF2, Fernet) |
| File reading | openpyxl (Excel), pdfplumber (PDF), RapidOCR (image PDF, optional) |
| Tests | pytest |

### The organisation

The **calculations** are in the `src` folder (one file per subject: `metrics.py`, `portfolio.py`, `optimisation.py`…), separate from the **display** (`app.py` and the `vues_*.py` files). They can thus be tested without launching the interface.

### Distribution

The Windows (`.exe`) and Mac (`.dmg`) installers are built automatically by GitHub Actions. They embed their own Python and all the libraries: nothing else to install.

## Does the software use artificial intelligence?
<!-- fiche: faq-intelligence-artificielle | questions: does the software use artificial intelligence ; is the assistant chatgpt ; is there an ai in the software ; are the answers generated ; machine learning ; does the software make up answers | mots: artificial intelligence, AI, ChatGPT, assistant, search, OCR, generative, machine learning -->

**No, no generative artificial intelligence.**

### The manual assistant

It writes nothing. It compares the words of your question with those of the manual entries (title, common phrasings, synonyms, text), tolerating typos and missing accents, then displays the closest entry **as it was written**. It therefore cannot invent anything. If it finds nothing, it says so. It works offline and sends nothing.

### The other automatic features

- **Column recognition** in an imported file relies on rules: known column names, cell contents, consistency of the figures.
- **Character recognition** for image PDFs uses a specialised engine (RapidOCR or Tesseract), which reads letters from an image.
- **The diagnostic** in the Exposures tab applies simple rules with documented thresholds.

All figures come from explicit formulas, described in the "All the formulas" chapter.

## Is the software available in English?
<!-- fiche: faq-anglais | questions: is the software available in english ; switch to english ; english version ; the pdf report in english ; the manual in english ; change language | mots: English, language, translation, FR, EN, report in French -->

**Yes for the screen.** At the top of the sidebar, the **FR | EN** selector switches the dashboard to English: menus, buttons, indicators, charts and most messages.

### What stays in French

- **The PDF report**, written in French whatever the screen language.
- **The manual**, as long as its English translation is not provided: the software then displays the French version.
- The names of your securities and the content of your files, as they are.

### The preference

The language is kept during the session. The "The screen and navigation" chapter details this setting.

## Are stock splits and corporate actions handled?
<!-- fiche: faq-divisions | questions: are stock splits handled ; stock split ; my stock did a split ; reverse split ; company merger ; bonus share allocation ; 90% loss after a split | mots: stock split, split, reverse split, merger, spin-off, corporate action, bonus shares -->

**Partly.** The software only knows three transaction types: buy, sell and dividend, and it does not detect a split by itself. But it can adjust your transactions from the split or reverse split notice sent by your broker.

### The problem

After a stock split, Yahoo Finance retroactively corrects its prices. Your file, however, still shows the old number of securities: the calculated value becomes wrong. Example: 10 shares bought at €800, then a 10-for-1 split; Yahoo shows about €80 for the purchase date, and the software would value 10 × €80 instead of 100 × €80.

### The signal

At import, the price check flags the gap ("check the ticker, currency or stock split"). A sudden loss of about 50, 67 or 90% should also raise an alert.

### The fix

Express the transaction in securities as they are after the split, **without changing the amount**: here, 100 shares at €80. The simplest way: drop the split notice (PDF) on the [[Add transactions]] page, then click [[Apply to earlier transactions]] (see the chapter on import, fiche "Stock split or reverse split"). Otherwise, do it by hand in the Transactions tab with [[Edit transactions]].

### Other corporate actions

Mergers, spin-offs, ticker changes or bonus share allocations: to be translated by yourself into purchases and sales.

## Why is the MSCI World the default benchmark index?
<!-- fiche: faq-indice-defaut | questions: why msci world by default ; why compare with an etf ; which index should I choose for my portfolio ; why not the cac 40 ; suitable benchmark index ; change index | mots: benchmark index, MSCI World, CW8, benchmark, CAC 40, reinvested dividends, choice of index | aller: Analyse du portefeuille/Performance -->

### The reasons

- **A global market**: most diversified equity portfolios are compared with global equities.
- **Reinvested dividends**: it is represented by the Amundi MSCI World ETF (CW8), which is **accumulating**. As your performance includes your dividends, the comparison is fair.

### Why not the CAC 40?

The CAC 40 offered is the price index, **excluding dividends**: it puts the index at a disadvantage, by about 3% a year according to the project. It is only relevant for a portfolio of French equities, keeping this bias in mind.

### Choosing the right index

In [[Settings]], [[Benchmark index]] offers equity, bond, money-market and mixed indices (20/80, 60/40, 80/20). Choose the one that resembles your allocation: a balanced portfolio compares better with a 60/40 index than with the MSCI World. An unsuitable index distorts beta, alpha and tracking error; against a bond or money-market index, the Performance tab warns that beta and alpha have little meaning.

## Is the Monte Carlo projection a forecast?
<!-- fiche: faq-projection | questions: is the projection a forecast ; how much will my portfolio be worth in 10 years ; will the median scenario happen ; reliability of the monte carlo simulation ; is the probability of loss reliable ; why does the fan widen | mots: projection, Monte Carlo, forecast, median scenario, probability, uncertainty, assumptions, horizon | aller: Analyse du portefeuille/Projection -->

**No.** The screen reminds you: "A projection is not a forecast: it assumes the assumptions hold, which is never guaranteed."

### What it does

It simulates 5,000 possible futures, all consistent with a chosen return and volatility (by default, those of the portfolio's past), and shows their distribution: adverse, median and favourable scenarios, probability of loss, probability of reaching a target.

### How to read it

- The **median** is not a forecast: it is the middle of the possibilities.
- The gap between scenarios **grows with the horizon**: uncertainty accumulates.
- The mean exceeds the median (log-normal distribution): the median is the most representative marker.

### Its assumptions

- **constant** return and volatility over the whole horizon;
- "Normal distribution" method: crashes underestimated; the "Historical (bootstrap)" method keeps the portfolio's real crashes;
- historical return often flattering: reducing the [[Assumed annual return (%)]] gives a more cautious projection.

## Why several VaRs, and which one should I use?
<!-- fiche: faq-plusieurs-var | questions: why several vars ; which var should I use ; historical var or normal var ; difference between var and cvar ; which risk measure to present ; is var enough ; why a one-day var | mots: VaR, CVaR, historical VaR, normal distribution VaR, Cornish-Fisher, risk measure, Expected Shortfall | aller: Analyse du portefeuille/Risque | chiffres: var_historique, var_parametrique, var_cornish_fisher, cvar -->

Each method relies on a different assumption; comparing them is part of the analysis.

| Measure | Assumption | Strength | Limitation |
|---|---|---|---|
| Historical VaR | the past repeats itself | no distribution assumed | blind to crises absent from the history |
| Normal-distribution VaR | normal returns | simple, standard | underestimates crashes |
| Cornish-Fisher VaR | corrected normal distribution | takes skewness and kurtosis into account | "n/a" if they are too large |
| CVaR | the past repeats itself | measures the severity beyond the threshold | relies on few days |

### Which one to use

- **The historical VaR** is the software's main measure: it is the one on the euro card of the Risk tab and in the report.
- **The CVaR** complements it: it says what a day beyond the threshold costs.
- **The gap between historical VaR and normal VaR** is information in itself: the automatic reading comments on it.

### Why over one day?

The software's VaRs cover the loss over **one trading day**, calculated on daily returns. For longer horizons, see the max drawdown, the stress tests and the projection.
