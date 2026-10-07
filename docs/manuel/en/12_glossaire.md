# Glossary
<!-- chapitre: glossaire | ordre: 12 -->

This glossary defines, in one to three sentences, the finance, statistics and computing terms used by the software and by this manual. The definitions are those adopted by Portfolio Tracker; the chapter "All the formulas" gives the exact calculation of each indicator. Terms are grouped by letter of their French name (shown in italics where it differs from the English), and within each group they are listed in alphabetical order of the English name.

## Glossary: A
<!-- fiche: glossaire-a | questions: what does alpha mean ; what is buy and hold ; net contributions definition ; what is look-through analysis ; skewness definition ; what is a trade confirmation ; what does annualise mean ; life insurance in the software ; what is the import wizard | mots: annualisation, buy and hold, refresh prices, alpha, Jensen's alpha, look-through analysis, net contributions, import assistant, import wizard, life insurance, assurance-vie, skewness, trade confirmation, avis d'opéré -->

**Annualisation** (*annualisation*): conversion of a figure over a period into a "per year" figure. A total return is compounded over 365 days; a volatility is multiplied by √252.

**Buy and hold** (*achat-conservation*): backtest strategy that buys the securities once and never touches them again; weights drift with prices, and the winners grow.

**Import assistant** (*assistant d'import*): four-step screen used to tell the software how to read a file: sheet and header row, columns, transaction types and tickers, then result.

**Jensen's alpha** (*alpha de Jensen*): annual performance that is not explained by exposure to the market, according to the CAPM. When positive, stock selection created value relative to the index.

**Life insurance** (*assurance-vie*): tax wrapper compared in the Taxation tab: social contributions of 17.2%, tax of 12.8% before 8 years, then 7.5% after an annual allowance of €4,600 (€9,200 for a couple).

**Look-through analysis** (*analyse en transparence*): method that splits each ETF according to the composition of the index it tracks (countries, sectors, currencies). A €10,000 MSCI World ETF thus counts for about €7,300 of American shares.

**Net contributions** (*apports nets*): the sum of all the money put in through purchases, minus the money taken back through sales and dividends. It is the money "from your own pocket" that is still invested.

**Refresh prices** (*actualiser les cours*): button at the bottom of the sidebar that clears the results kept in memory (for one hour) and downloads the prices again. An Internet connection is required.

**Skewness** (*asymétrie*): measure of the asymmetry of daily returns. Zero for a normal distribution; when negative, large falls are more frequent or more violent than large rises.

**Trade confirmation** (*avis d'opéré*): document sent by the bank after an order is executed (date, direction, ISIN, quantity, price, fees). The software can read it in PDF format.

## Glossary: B
<!-- fiche: glossaire-b | questions: what does base 100 mean ; what is the local securities database ; what is a backtest ; beta definition ; what is a benchmark ; bootstrap definition ; what is brinson fachler ; correlated blocks what does it mean | mots: backtest, base 100, local database, securities database, benchmark, beta, correlated blocks, bootstrap, Brinson-Fachler -->

**Backtest**: test of a strategy on real history. The [[Strategy backtest]] tab compares, with the same securities and the same starting weights, buy and hold against regular rebalancing, then investing all at once against investing gradually.

**Base 100**: series that starts at 100 and tracks performance (100 × product of 1 + r). It makes it possible to compare the portfolio and the index on one chart.

**Benchmark**: see "Benchmark index".

**Beta** (*bêta*): sensitivity of the portfolio to movements in the index: covariance of returns divided by the variance of the index. A beta of 1.2 means that a 1% move in the index is accompanied on average by a 1.2% move in the portfolio.

**Bootstrap**: simulation method that draws at random, with replacement, from real past returns. The "Historical (bootstrap)" projection builds each month from 21 real days of the portfolio.

**Brinson-Fachler**: performance attribution model (1985) that breaks the gap with the index down into allocation, selection and interaction effects, region by region.

**Correlated blocks** (*blocs corrélés*): groups of securities whose average correlation exceeds 0.7. Each block counts as a single "bet", whatever the number of holdings.

**Local securities database** (*base locale de titres*): files delivered with the software (`data/base` folder) that contain the record and daily prices of several thousand securities, indices and exchange rates. It allows you to work offline.

## Glossary: C
<!-- fiche: glossaire-c | questions: what does cache mean ; what is an asset class ; isin check digit ; risk contribution definition ; what is correlation ; closing price definition ; what is a cto ; what does cvar mean ; currency hedging eur hedged | mots: cache, Cariño, asset class, check digit, risk contribution, correlation, Cornish-Fisher, closing price, covariance, securities account, CTO, CVaR, currency hedging -->

**Asset class** (*classe d'actifs*): broad family of an investment: Equities, Bonds, Gold or Money market. A security of unknown class is treated as an equity, as a precaution.

**Cache**: local copy of the latest downloaded prices (`cache_*.csv` files in the `data` folder). If Yahoo Finance does not respond, the software reads it again and displays "Cached prices (offline)".

**Cariño (smoothing)** (*Cariño, lissage de*): method that links monthly attribution effects so that their sum lands exactly on the compounded performance gap over the whole period.

**Check digit** (*clé de contrôle*): last digit of an ISIN code, calculated from the others. The software only accepts an ISIN if its check digit is correct.

**Closing price** (*cours de clôture*): last price of a trading session. The software uses the closing price not adjusted for dividends.

**Cornish-Fisher**: correction of the normal distribution quantile for skewness and kurtosis, used for a more realistic VaR. It is not calculated ("n/a") when these moments are too extreme.

**Correlation** (*corrélation*): measure, between −1 and +1, of the link between the daily returns of two securities. +1: they always move together; 0: no linear link; −1: in opposite directions.

**Covariance**: measure of how two securities vary together; it combines their correlation and their volatilities. The covariance matrix is the basis of Markowitz and of the risk budget.

**Currency hedging** (*couverture de change*, *EUR Hedged*): technique used by an ETF to neutralise the effect of currencies. An ETF whose name contains "Hedged" or "couvert" is counted in euros in the currency exposure.

**CVaR** (*Expected Shortfall*): average loss on the days when the historical VaR is exceeded. It answers "when things go badly, how badly?".

**Risk contribution** (*contribution au risque*): share of the portfolio's volatility contributed by a holding (Euler decomposition). The sum of the contributions equals the total volatility.

**Securities account (CTO)** (*compte-titres ordinaire*): a tax wrapper with no tax advantage: dividends and capital gains are taxed at the single flat-rate levy (PFU) of 31.4% (2026 rules).

## Glossary: D to E
<!-- fiche: glossaire-d-e | questions: what does dca mean ; what is the trading currency ; dividend definition ; what does drawdown mean ; what is duration ; etf definition ; accumulating or distributing etf ; standard deviation definition ; allocation effect and selection effect | mots: allocation effect, selection effect, interaction effect, DCA, gradual investing, trading currency, diversification, dividend, drawdown, duration, standard deviation, ETF, accumulating, distributing, exposures -->

**Allocation effect, selection effect, interaction effect** (*effet allocation, effet sélection, effet interaction*): the three parts of the gap with the index according to Brinson-Fachler: choice of regions, choice of securities within each region, and the cross effect of the two.

**DCA** (*Dollar Cost Averaging*), or gradual investing (*investissement progressif*): placing a sum of capital in several equal monthly instalments rather than all at once. The backtest compares the two, with money waiting to be invested earning the risk-free rate.

**Diversification**: spreading across investments that do not all move together, to reduce risk without reducing return as much. The software measures it through correlations and the diversification ratio.

**Dividend** (*dividende*): sum paid by a company (or a distributing ETF) to its shareholders. It is recorded with the type DIVIDENDE, a quantity of 0 and the total amount received in the price.

**Drawdown**: fall from the highest level reached so far. The **max drawdown** is the worst of these falls over the period.

**Duration**: sensitivity of a bond to interest rates, in years. A duration of 7 years means a fall of about 7% in the price if rates rise by 1 point.

**ETF** (*Exchange Traded Fund*), or listed index fund: fund that replicates an index and is bought on the stock market like a share. **Accumulating** (*capitalisant*): it reinvests dividends in its price; **distributing** (*distribuant*): it pays them out.

**Exposures** (*expositions*): what the portfolio is really exposed to (countries, sectors, currencies, rates), ETFs included on a look-through basis. It is also the name of the tab that presents them with a diagnosis.

**Standard deviation** (*écart-type*): measure of the dispersion of returns around their mean. Annualised, it gives the volatility.

**Trading currency** (*devise de cotation*): currency in which a security is quoted (dollar for Apple, pence for a London share). The price of a purchase is entered in this currency; the software converts it into euros.

## Glossary: F to I
<!-- fiche: glossaire-f-i | questions: what does flat tax mean ; what is a cash flow ; efficient frontier definition ; what is fernet ; total gain definition ; what does gbp pence mean ; herfindahl definition ; what is an isin ; benchmark index definition ; composite index | mots: flat tax, PFU, cash flows, fees, Fernet, efficient frontier, total gain, GBp, pence, Herfindahl, ISIN, benchmark index, composite index, blended index -->

**Benchmark index** (*indice de référence*): index to which the portfolio is compared (beta, alpha, tracking error, base-100 chart). It is chosen in [[Settings]]; by default, the MSCI World represented by the CW8 ETF.

**Cash flows** (*flux*): money put in (purchase, counted positively) or taken back (sale, dividend, counted negatively) on a given day. Cash flows are removed from the calculation of daily performance.

**Composite index** (*indice composite*, or blended index): index calculated by the software, a mix of an equity portion and a bond portion (20/80, 60/40 or 80/20), reset to its target weights at the end of each month.

**Efficient frontier** (*frontière efficiente*): set of portfolios that offer, for each level of expected return, the lowest possible volatility (Markowitz). No randomly drawn portfolio goes beyond it.

**Fees** (*frais*): brokerage fees on a transaction, always in euros. They are included in the cost basis (PRU) on a purchase and deducted from the capital gain on a sale.

**Fernet**: encryption method (Python `cryptography` library) that protects saved portfolios, with a key derived from your password.

**Flat tax**: see "Single flat-rate levy (PFU)".

**GBp** (pence): quotation unit for London shares. 1,250 GBp is worth £12.50; the software applies a factor of 0.01.

**Herfindahl index** (*indice de Herfindahl*): sum of the squares of the weights. Its inverse gives the **effective number of holdings**: 1 / Σ weight².

**ISIN**: 12-character international code that identifies a security (for example FR0013380607). Two country letters, nine characters and a check digit.

**Total gain** (*gain total*): what the portfolio has earned in euros since the start: unrealised gains + realised gains + dividends, net of fees.

## Glossary: J to M
<!-- fiche: glossaire-j-m | questions: what does jarque bera mean ; kurtosis definition ; what is localhost ; normal distribution definition ; what does log normal mean ; who is markowitz ; capm definition ; monte carlo definition ; securities memory ; what is money market | mots: Jarque-Bera, kurtosis, fat tails, localhost, normal distribution, log-normal, Markowitz, max drawdown, CAPM, MEDAF, securities memory, capital loss, money market, Monte Carlo -->

**Capital loss** (*moins-value*): loss that is realised (sale below the cost basis) or unrealised (price below the cost basis).

**CAPM** (*MEDAF*, capital asset pricing model): model that links a portfolio's return to its beta. It is used to calculate Jensen's alpha.

**Excess kurtosis** (*kurtosis en excès*): measure of the "tails" of the distribution. Zero for a normal distribution; when positive, extreme days, in both directions, are more frequent than expected ("fat tails").

**Jarque-Bera test**: statistical test that checks whether returns follow a normal distribution, based on skewness and kurtosis. A p-value below 5% leads to normality being rejected.

**Localhost**: address that refers to your own computer. The dashboard runs at the address `http://localhost:8501` (or a following port); nobody else on the network can connect to it.

**Log-normal distribution** (*loi log-normale*): distribution of a quantity whose logarithm follows a normal distribution. The final value of a projection follows one: its mean exceeds its median.

**Markowitz optimisation** (*optimisation de Markowitz*): method (1952) that looks for the allocations offering the best return-risk pairing, using the correlations between securities. Optimisation tab.

**Max drawdown**: worst fall suffered, from the peak to the following trough, measured on the base-100 performance curve.

**Money market** (*monétaire*): asset class of overnight investments, close to the risk-free rate (€STR ETFs, for example).

**Monte Carlo method** (*méthode de Monte-Carlo*): simulation of thousands of randomly drawn possible futures (5,000 in the software), to study the distribution of outcomes rather than a single forecast.

**Normal distribution** (*loi normale*): Gauss's "bell-shaped" distribution, symmetric, described by its mean and standard deviation. It is used for the parametric VaR and for the projection, but underestimates crashes.

**Securities memory** (*mémoire des titres*): file `data/base/memoire.csv` that retains the matches found online between an ISIN or a name and a ticker, so they can be recognised afterwards without the Internet.

## Glossary: N to O
<!-- fiche: glossaire-n-o | questions: what does n/a mean ; effective number of bets ; what is the var confidence level ; effective number of holdings ; what is ocr ; bond definition ; gold in the portfolio ; optimisation definition | mots: n/a, n.d., not available, confidence level, effective number of holdings, effective number of bets, OCR, character recognition, bond, gold, optimisation -->

**Bond** (*obligation*): debt security that pays interest (coupons). In the software, bonds are tracked through listed funds, with their duration when the reference file gives it.

**Confidence level** (*niveau de confiance*): probability used for the VaR: 90, 95 (default) or 99%. A 95% VaR is exceeded only about one day in twenty.

**Effective number of bets** (*nombre effectif de paris*): same idea applied to shares of risk: 1 / Σ (share of risk)². It says how many independent holdings the portfolio really represents.

**Effective number of holdings** (*nombre effectif de lignes*): number of equal-weight holdings that would give the same concentration: 1 / Σ weight². Four holdings of 40, 30, 20 and 10% are worth about 3.3.

**Gold** (*or*): a separate asset class, tracked through a listed fund. In look-through analysis, it is counted as "no country" and separately from currencies.

**n/a** (*n.d.*): "not available". The calculation makes no sense or did not succeed (for example the Cornish-Fisher VaR with too high a kurtosis, or an IRR with no solution).

**OCR** (optical character recognition, *reconnaissance de caractères*): reading text from an image. The software uses it for scanned PDFs, if an engine (RapidOCR or Tesseract) is installed.

**Optimisation**: searching, by calculation, for the weights that minimise volatility or maximise the Sharpe ratio, under constraints (positive weights, sum of 100%, maximum weight per security).

## Glossary: P
<!-- fiche: glossaire-p | questions: what does pru mean ; what is the pea ; risk parity definition ; what is pbkdf2 ; percentile definition ; trading venue ; unrealised gain definition ; realised gain ; social contributions rate ; p-value definition | mots: risk parity, PBKDF2, PEA, percentile, trading venue, exchange suffix, unrealised gain, realised gain, weight, maximum weight, tangency portfolio, single flat-rate levy, PFU, social contributions, PRU, cost basis, proxy, p-value -->

**Cost basis (PRU)** (*prix de revient unitaire*): average cost of a security held, purchase fees included. It changes with each purchase and stays fixed on a sale.

**PBKDF2**: method that turns the password into a fingerprint and an encryption key, recomputing it 600,000 times to slow down hacking attempts.

**PEA** (*plan d'épargne en actions*, French equity savings plan): wrapper reserved for European equities and eligible funds. After 5 years, gains bear only social contributions (18.6% in 2026).

**Percentile**: value below which a given percentage of the observations lies. The 5th percentile of the scenarios is the unfavourable scenario of the projection.

**Proxy**: index or fund used in place of a security with no history, for example the index of its region in a stress test.

**p-value**: probability of observing a result at least as extreme if the hypothesis tested (here, normality) were true. Below 5%, the hypothesis is rejected.

**Realised gain** (*plus-value réalisée*): gain cashed in on a sale: quantity × (sale price − PRU) − fees.

**Risk parity** (*parité des risques*): allocation in which each holding contributes the same share of risk. It uses only volatilities and correlations, not expected returns.

**Single flat-rate levy (PFU, flat tax)** (*prélèvement forfaitaire unique*): taxation of investment income: 12.8% income tax and 18.6% social contributions, i.e. 31.4% in 2026.

**Social contributions** (*prélèvements sociaux*): the social part of taxation on investment income: 18.6% in 2026 (CTO, PEA), 17.2% for life insurance.

**Tangency portfolio** (*portefeuille tangent*): maximum-Sharpe portfolio; combined with the risk-free investment, it offers the best return-risk line.

**Trading venue** (*place de cotation*): stock exchange where a security is listed, shown in the Yahoo ticker by a suffix: `.PA` for Paris, `.DE` for Frankfurt, `.L` for London, none for the United States.

**Unrealised gain** (*plus-value latente*): gain not yet cashed in on a holding: quantity × (price − PRU).

**Weight** (*poids*): share of a holding in the portfolio's total value. The **maximum weight per security** limits this share in the optimisation (30% by default).

## Glossary: Q to R
<!-- fiche: glossaire-q-r | questions: what does quantile mean ; information ratio definition ; diversification ratio definition ; what is rebalancing ; daily return ; portfolio turnover ; currency risk definition ; what does reference file mean | mots: quantile, information ratio, diversification ratio, rebalancing, reference file, daily return, currency risk, turnover -->

**Currency risk** (*risque de change*): effect of currency movements on the euro value of a foreign security. An American share can rise in dollars and fall in euros.

**Daily return** (*rendement quotidien*): one day's change, after removing contributions and withdrawals: (value of the day − flow of the day) / value of the previous day − 1.

**Diversification ratio** (*ratio de diversification*): sum of the holdings' volatilities, weighted by their weight, divided by the portfolio's volatility. It equals 1 with no diversification at all and increases as holdings offset each other.

**Information ratio** (*ratio d'information*): annualised average return gap with the index, divided by the tracking error. It says whether the gap with the index has been paid for; above 0.5, it is considered good.

**Quantile**: synonym of percentile, expressed as a fraction. The 5% quantile of daily returns gives the 95% historical VaR.

**Rebalancing** (*rééquilibrage*): periodic return to target weights, by selling what has risen and buying what has fallen. The backtest tests it each month, quarter or year.

**Reference file** (*référentiel*): the project's `data/referentiel.csv` file that describes securities by hand (country, region, sector, asset class, duration). It takes precedence over the local database.

**Turnover** (*rotation*): share of the portfolio to be moved to go from one allocation to another (sum of weight gaps divided by 2), or, in the backtest, amounts traded per year.

## Glossary: S
<!-- fiche: glossaire-s | questions: what does sharpe mean ; sortino definition ; semi deviation ; what is a stress test ; what is streamlit ; gics sector ; overweight definition ; unfavourable median favourable scenario | mots: Sharpe ratio, Sortino ratio, scenario, sector, semi-deviation, underweight, stress test, Streamlit, overweight -->

**Overweight, underweight** (*surpondération, sous-pondération*): weight of a country, sector or region that is higher (or lower) in the portfolio than in the benchmark index.

**Scenarios: unfavourable, median and favourable** (*scénarios défavorable, médian et favorable*): 5th, 50th and 95th percentiles of the value simulated by the projection. There is a one-in-twenty chance of doing worse than the unfavourable scenario.

**Sector** (*secteur*): a company's field of activity (technology, healthcare, finance, etc.), according to the translated GICS classification.

**Semi-deviation** (*semi-déviation*): measure of dispersion that keeps only the days when the return is below the risk-free rate, annualised by √252.

**Sharpe ratio** (*ratio de Sharpe*): annual excess return (above the risk-free rate) divided by the volatility. It measures whether the risk taken was well rewarded: above 1, very good.

**Sortino ratio** (*ratio de Sortino*): variant of the Sharpe that replaces volatility with the semi-deviation, so as to penalise only falls.

**Streamlit**: Python library that displays the dashboard in a browser window.

**Stress test**: estimate of what the current portfolio would lose if a past crisis happened again (2008, Covid, etc.) or if a hypothetical shock occurred (fall in equities, in the dollar, rise in rates).

## Glossary: T to U
<!-- fiche: glossaire-t-u | questions: what does twr mean ; what is the irr ; risk-free rate definition ; ticker definition ; tracking error definition ; transaction ; ucits 5 10 40 rule ; what is the eurusd exchange rate | mots: exchange rate, risk-free rate, ticker, IRR, TRI, TWR, time-weighted return, tracking error, transaction, UCITS, 5/10/40 -->

**Exchange rate** (*taux de change*): price of a currency in euros. The software uses Yahoo Finance rates, expressed as the number of currency units per 1 euro (`EURUSD=X` = dollars per €1).

**IRR** (*TRI*, internal rate of return): annual return on the money actually invested, which takes into account the amount and date of each contribution. It depends on the timing of your payments.

**Risk-free rate** (*taux sans risque*): return on a risk-free investment in euros, used for the Sharpe, the Sortino and alpha. 2.50% by default (ECB deposit facility rate), constant over the period, editable in [[Settings]].

**Ticker**: short code for a security at Yahoo Finance, with its trading venue: `MC.PA` for LVMH in Paris, `AAPL` for Apple.

**Tracking error**: annualised volatility of the daily return gap between the portfolio and the index. Low: the portfolio sticks closely to the index.

**Transaction** (*opération*): purchase, sale or dividend recorded in the portfolio, with its date, security, quantity, price and fees.

**TWR** (*time-weighted return*): product of daily returns neutralised for contributions. It measures the quality of choices, independently of contributions; it is the fund managers' measure.

**UCITS (5/10/40 rule)**: European fund rule: a holding at most 10% of the fund, and holdings above 5% at most 40% in total. The software uses it as a concentration benchmark.

## Glossary: V to Y
<!-- fiche: glossaire-v-y | questions: what does var mean ; value at risk definition ; historical var ; parametric var ; minimum variance ; volatility definition ; what is yahoo finance ; yfinance | mots: VaR, value at risk, historical VaR, normal VaR, variance, minimum variance, volatility, Yahoo Finance, yfinance -->

**Historical VaR** (*VaR historique*): VaR read directly from past returns (quantile), with no assumption about the distribution.

**Minimum-variance portfolio** (*portefeuille de variance minimale*): the least volatile possible allocation of the current securities, under the optimisation constraints.

**Normal VaR** (parametric) (*VaR loi normale*): VaR calculated by assuming that returns follow a normal distribution with the same mean and the same volatility. It often underestimates crashes.

**VaR** (*Value at Risk*): loss on a bad day at a given confidence level. A 95% VaR of €2,000 means the loss exceeds this amount only about 5% of days.

**Variance**: square of the standard deviation; measure of dispersion used in Markowitz calculations.

**Volatility** (*volatilité*): annualised standard deviation of daily returns (× √252). It is the most common measure of risk: 15% means a year's return typically deviates by 15 points from its mean.

**Yahoo Finance**: free stock market information service from which prices, exchange rates and the recognition of unknown securities come.

**yfinance**: Python library used by the software to query Yahoo Finance.
