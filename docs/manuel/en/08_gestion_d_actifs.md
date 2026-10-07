# Asset management
<!-- chapitre: gestion | ordre: 8 -->

This chapter presents the "Asset management" space, which brings together the tools of a portfolio manager. The **Performance attribution** tab explains the gap with a world index using the Brinson-Fachler model. The **Risk budget** tab measures where the risk comes from and compares your allocation with risk parity. The **Strategy backtest** tab tests rebalancing and gradual investing on real historical data. Each entry gives the exact formula, a worked example and the limitations.

## What does the Asset management space contain?
<!-- fiche: gestion-presentation | questions: what is the asset management space for ; where do I find the backtest ; where is the risk budget ; where is the performance attribution ; what can I do in asset management ; difference between asset management and portfolio analysis | mots: asset management, attribution, risk budget, backtest, risk parity, rebalancing, DCA, portfolio manager | aller: Gestion d'actifs -->

The **Asset management** space is chosen in the "Workspace" menu of the sidebar. It analyses the same portfolio, with the same settings, as the "Portfolio analysis" space. It has three tabs.

| Tab | Question it answers |
|---|---|
| Performance attribution | Why did the portfolio do better (or worse) than a world index? Choice of regions or choice of securities? |
| Risk budget | Which holdings bring the most risk? What would an allocation in which every holding brings the same amount of risk look like? |
| Strategy backtest | Would it have been better to rebalance regularly? To invest all at once or gradually? |

### Good to know

- The attribution downloads regional indices: Internet is needed the first time it is displayed, after which a cache takes over.
- The risk budget and the backtest use the prices already loaded for the analysis.
- The diversification diagnosis (regions, sectors, currencies, correlations) is in the Exposures tab of the "Portfolio analysis" space: the Risk budget tab recalls this with a note.
- The main results also appear in the PDF report (backtest with 0.1% fees and comparison on €10,000 over 12 months).

In case of an error, each tab displays a "… unavailable" message followed by the cause, without blocking the others.

## Brinson-Fachler performance attribution
<!-- fiche: gestion-brinson-fachler | questions: why did my portfolio do worse than the index ; what is the allocation effect ; what is the selection effect ; interaction effect explanation ; how do I read the performance attribution ; brinson fachler formula ; did I choose my securities or my regions well ; where does my outperformance come from | mots: performance attribution, Brinson-Fachler, allocation effect, selection effect, interaction effect, outperformance, underperformance, gap to the index, regions | aller: Gestion d'actifs/Attribution de performance | chiffres: twr_total -->

The **Performance attribution** tab breaks down the return gap between your portfolio and a benchmark index, **region by region**, into three effects.

### The exact formulas (for one month)

```
Allocation effect  = (wp − wb) × (rb − Rb)
Selection effect   = wb × (rp − rb)
Interaction effect = (wp − wb) × (rp − rb)
```

- `wp`, `wb`: weight of the region in the portfolio and in the index;
- `rp`, `rb`: return of the region in the portfolio and in the index;
- `Rb`: total return of the index = Σ wb × rb.

The sum of the three effects across all regions equals the gap `Rp − Rb`.

### The intuition

- **Allocation**: did you overweight the regions that did better than the overall index?
- **Selection**: within each region, did your securities do better than that region's index?
- **Interaction**: cross effect, positive if you overweighted a region where you also chose well.

### Verified example

| Region | wp | rp | wb | rb |
|---|---|---|---|---|
| United States | 50% | +10% | 70% | +8% |
| Europe | 50% | +2% | 30% | +4% |

Rb = 0.7 × 8% + 0.3 × 4% = **6.8%**; Rp = 0.5 × 10% + 0.5 × 2% = **6.0%**; gap **−0.8 points**.

| Region | Allocation | Selection | Interaction |
|---|---|---|---|
| United States | (−0.2) × (8 − 6.8) = −0.24 | 0.7 × 2 = +1.40 | (−0.2) × 2 = −0.40 |
| Europe | 0.2 × (4 − 6.8) = −0.56 | 0.3 × (−2) = −0.60 | 0.2 × (−2) = −0.40 |
| **Total** | **−0.80** | **+0.80** | **−0.80** |

Sum: −0.80 + 0.80 − 0.80 = **−0.80 points**, exactly the gap. Reading: the selection of US securities was good, but the overweight in Europe, which did worse than the index, cost performance.

### What is displayed

Six cards (Portfolio, Benchmark index, Difference, Allocation effect, Selection effect, Interaction effect), the "Effects by region" chart, the "Cumulative effects over time" chart and the "Detail by region" table. In this table, the portfolio weights are **monthly averages** and the regions' returns are **compounded** over the period.

### Special rules

- a region absent from the index takes `rb = Rb`: its allocation and selection effects are zero, everything goes into **interaction**;
- a region absent from the portfolio takes `rp = rb`: only the allocation effect applies.

## Why a "Cariño smoothing"? The month-by-month calculation
<!-- fiche: gestion-carino | questions: what is cariño smoothing ; why don't the monthly effects add up to the gap ; how are the months added together in the attribution ; what does the cumulative effects chart show ; why calculate the attribution every month ; multi-period attribution ; linking of effects | mots: Cariño, smoothing, linking, multi-period, compounding, cumulative effects, month by month, logarithmic coefficient | aller: Gestion d'actifs/Attribution de performance -->

The attribution is calculated **month by month**, with the weights at the start of each month, then the months are linked.

### The problem

Returns compound: +10% then +10% gives +21%, not +20%. Adding up the monthly gaps therefore does not give the total gap back.

### Cariño's method (1999)

Each monthly effect is multiplied by a factor `kₜ / K`:

```
kₜ = [ln(1 + Rpₜ) − ln(1 + Rbₜ)] / (Rpₜ − Rbₜ)     (returns of month t)
K  = [ln(1 + Rp)  − ln(1 + Rb)]  / (Rp − Rb)       (compounded returns of the whole period)
if the two returns are equal: k = 1 / (1 + R)
linked effect of month t = effect of month t × kₜ / K
```

In this way, the sum of the linked effects is **exactly** equal to the compounded gap `Rp − Rb`. An automatic test in the software checks it.

### Verified example

Two months: portfolio +10% then +10% (Rp = 21%), index +5% then +5% (Rb = 10.25%).

- Actual gap: 21% − 10.25% = **10.75 points**; sum of the monthly gaps: 5 + 5 = 10 points.
- kₜ = (ln 1.10 − ln 1.05) / 0.05 = 0.9304; K = (ln 1.21 − ln 1.1025) / 0.1075 = 0.8655.
- Factor = 0.9304 / 0.8655 = **1.075**; each month is worth 5 × 1.075 = 5.375 points; total **10.75 points**. The sum is right.

### Splitting into months

The software takes the last trading day of each month of the history (the latest available date counts as the end of the current month) and calculates each month from one month end to the next. At least two month ends are needed; otherwise the message "History too short: at least two month ends are needed" is displayed.

### The "Cumulative effects over time" chart

It plots the cumulative sum of the linked allocation, selection and interaction effects, month after month. The three curves end on the values of the cards. A curve that rises steadily signals a persistent effect; a jump, an exceptional month.

### Limitation

Weights are frozen at the start of each month: a purchase or sale during the month is only taken into account the following month. The "Portfolio" return is therefore that of the holdings, and may differ slightly from the TWR in the Performance tab.

## Which benchmark index for the attribution? Regions and weights
<!-- fiche: gestion-indice-reference-attribution | questions: which index is my portfolio compared with in the attribution ; why is it not the index chosen in the settings ; weights of the regions of the msci acwi index ; which indices are used for each region ; does the attribution index include dividends ; why does the united states weigh 63% | mots: MSCI ACWI IMI, benchmark index, benchmark, regional weights, S&P 500, Euro Stoxx 50, Nikkei, regional indices, conversion into euros | aller: Gestion d'actifs/Attribution de performance -->

The attribution compares your portfolio with a **reconstituted world equity index**, and **not** with the index chosen with the [[Benchmark index]] menu in Settings. The "Benchmark index" card says so: "MSCI ACWI (regional weights)".

### The index weights

These are the regional weights of the **MSCI ACWI IMI at 30 Jun 2026**, renormalised so that they add up to 100% (the raw sum is 99.6%):

| Region | Raw weight | Weight used | Representative index |
|---|---|---|---|
| United States | 62.7% | 62.95% | S&P 500 (^GSPC) |
| Emerging markets | 12.3% | 12.35% | EEM |
| Europe (excluding the United Kingdom and Switzerland) | 8.7% | 8.73% | Euro Stoxx 50 (^STOXX50E) |
| Japan | 5.6% | 5.62% | Nikkei 225 (^N225) |
| United Kingdom | 3.1% | 3.11% | FTSE 100 (^FTSE) |
| Canada | 3.0% | 3.01% | ^GSPTSE |
| Asia-Pacific | 2.3% | 2.31% | ^AXJO |
| Switzerland | 1.9% | 1.91% | ^SSMI |

```
weight used = raw weight / 99.6
```

### The calculation

Each month, the index return is `Rb = Σ region weight × return of its index`. Index prices are **converted into euros** with exchange rates, to be comparable with your portfolio.

### How your securities are classified

Each security is placed in a region according to the software's securities reference file. A security absent from the reference file is classified as "Unclassified".

### Limitations

- **Indices excluding dividends**: regional indices ignore dividends. Your prices do not take them into account either, which keeps the comparison consistent, but both returns are underestimated, all the more so as the regions pay out a lot.
- **One index per region**, often large caps (Euro Stoxx 50 for Europe).
- **Attribution by region only**, not by sector.
- The index weights are fixed over the whole period.

## Attribution of a diversified portfolio or a world ETF
<!-- fiche: gestion-attribution-poche-actions | questions: why aren't my bonds in the attribution ; what is the equity sleeve ; my world etf is unclassified in the attribution ; message is not classified in an index region ; attribution unavailable no equities ; does the attribution make sense for a single etf ; why is everything in the interaction effect | mots: equity sleeve, diversified portfolio, bonds excluded, world ETF, unclassified, interaction, attribution unavailable, direct holdings | aller: Gestion d'actifs/Attribution de performance -->

### Only the equity sleeve is analysed

The benchmark index is an **equity** index. For a diversified portfolio (equities, bonds, gold), the software therefore compares only the **equities** with this index, as a manager does for each "sleeve". Bonds and gold are excluded. A security absent from the reference file is considered to be an equity.

If equities represent less than 99.5% of the portfolio, a note says so with their current weight: "the attribution covers the equity sleeve (x% of the portfolio today)". If there are no equities at all, the tab displays "Attribution unavailable" with the note "no equities in the portfolio".

### The case of world ETFs

A world ETF is placed in the "World (ETF)" region, which does not exist in the index. The software applies to it the rule for regions absent from the index (`wb = 0`, `rb = Rb`):

```
allocation  = wp × (Rb − Rb) = 0
selection   = 0 × (rp − Rb)  = 0
interaction = wp × (rp − Rb)
```

The whole gap on this line goes into the **interaction effect**. Example: a world ETF that weighs 50% and returns 9% when the index returns 6.8% gives an interaction of 0.5 × 2.2 = **+1.1 points**. The index regions absent from the portfolio then produce an allocation effect (for example, a Europe at 30% in the index and 0% in your portfolio, returning 4% against 6.8%: (0 − 0.3) × (4 − 6.8) = **+0.84 points**).

### The warning displayed

If more than 20% of the portfolio is not classified in an index region (world ETF, securities absent from the reference file), a note warns that the attribution is mainly relevant for a **portfolio of direct holdings**, such as the "global equity" sample portfolio. For a portfolio made up of one or two ETFs, the Performance tab (comparison with the index, alpha, tracking error) is more telling.

## The risk budget: which holdings bring the most risk?
<!-- fiche: gestion-contributions-risque | questions: which holding brings the most risk to my portfolio ; what is the risk contribution ; why is the share of risk different from the weight ; biggest risk contributor ; marginal contribution explanation ; how do I read the risk budget ; euler property | mots: risk budget, risk contribution, marginal contribution, Euler, share of risk, risk budgeting, volatility, risk decomposition | aller: Gestion d'actifs/Budget de risque | chiffres: volatilite, nb_titres -->

A holding's weight does not tell you what share of the **risk** it brings: a very volatile share that is highly correlated with the rest of the portfolio weighs more in the risk than in the value. The **Risk budget** tab does this decomposition.

### The exact formulas

```
portfolio volatility        σp = √(wᵀ Σ w)
marginal contribution       MCᵢ = (Σ w)ᵢ / σp
risk contribution           RCᵢ = wᵢ × MCᵢ
share of risk                  = RCᵢ / σp          (the sum is 100%)
```

`Σ` is the annual covariance matrix, estimated as in the Optimisation tab (daily returns × 252, over the common period of your current securities).

**Euler's property**: the sum of the contributions is exactly equal to the portfolio's volatility (Σ RCᵢ = σp). An automatic test checks it.

### Verified example

Two securities at 50 / 50: A (volatility 20%), B (volatility 10%), correlation 0.2 (covariance 0.004).

- σp = √(0.25 × 0.04 + 0.25 × 0.01 + 2 × 0.25 × 0.004) = **12.04%**;
- MC_A = (0.04 × 0.5 + 0.004 × 0.5) / 0.1204 = 0.1827; RC_A = 0.5 × 0.1827 = 0.0914;
- MC_B = (0.004 × 0.5 + 0.01 × 0.5) / 0.1204 = 0.0581; RC_B = 0.0291;
- shares of risk: A **75.9%**, B **24.1%**, for weights of 50 / 50.

### What is displayed

- three cards: "Current volatility", "Largest contributor" (its share of risk, its name and its share of value) and "Risk-parity volatility";
- the "Share of value and share of risk" chart: for the 20 largest contributors, a light grey-blue bar (share of value) and a blue bar (share of risk).

### Interpretation

A holding whose **share of risk exceeds its share of value** is more volatile, or more correlated with the rest, than average. A negative share of risk is possible for a holding that falls when the others rise (hedge).

### Limitations

Risk is measured by volatility alone, over the observed period. Correlations can change, especially in a crisis.

## Risk parity
<!-- fiche: gestion-parite-risques | questions: what is risk parity ; risk parity explanation ; why does risk parity not use returns ; how is risk parity calculated ; all weather bridgewater ; risk-parity volatility ; should I move to risk parity ; spinu method | mots: risk parity, equal risk contribution, ERC, Spinu, All Weather, allocation without expected return, equal contributions | aller: Gestion d'actifs/Budget de risque | chiffres: volatilite -->

**Risk parity** is an allocation in which **each holding contributes equally** to the portfolio's risk. It was popularised by Bridgewater's "All Weather" fund.

### Why it is interesting

It does **not use expected returns**, which are very poorly estimated, but only volatilities and correlations. It is a direct answer to the main limitation of Markowitz (see the chapter on optimisation).

### The calculation (Spinu's method, 2013)

The software minimises the function:

```
½ wᵀ Σ w − (1/n) × Σ ln(wᵢ)
```

starting from weights inversely proportional to the volatilities (scipy's L-BFGS-B method, strictly positive weights). The weights obtained are then renormalised so that they add up to 100%. At the optimum, all the risk contributions are equal.

### Verified example

Securities A (volatility 20%) and B (volatility 10%), correlation 0.2, expected returns 8% and 4%, risk-free rate 2.5%:

| Allocation | Weights A / B | Volatility | Shares of risk | Sharpe |
|---|---|---|---|---|
| 50 / 50 portfolio | 50% / 50% | 12.04% | 75.9% / 24.1% | 0.29 |
| Risk parity | 33.3% / 66.7% | 10.33% | 50% / 50% | 0.27 |

The more volatile security receives less weight. With two securities, risk parity amounts to weighting by the inverse of the volatilities (1/0.20 and 1/0.10, that is 1/3 and 2/3).

### Interpretation

Risk parity generally reduces volatility and increases risk diversification. It does not maximise return: its Sharpe can be lower, as in the example. With equities and bonds, it gives a lot of weight to bonds, which are less volatile.

### Limitations

- risk-parity funds often use leverage to raise returns: that is not the case here;
- the weights depend on past volatilities and correlations;
- no cap per security is applied.

## Comparing four allocations: diversification ratio and effective number of bets
<!-- fiche: gestion-quatre-allocations | questions: what is the effective number of bets ; diversification ratio formula ; how do I read the four ways to allocate the same securities table ; what is equal weight ; what does largest contribution mean ; my portfolio has 30 holdings but only 5 bets ; see the risk parity weights | mots: effective number of bets, diversification ratio, equal weight, minimum variance, largest contribution, risk concentration, allocation comparison | aller: Gestion d'actifs/Budget de risque | chiffres: nb_titres, sharpe -->

The "Four ways to allocate the same securities" table compares, using **your current securities**:

| Allocation | Principle |
|---|---|
| Current portfolio | your weights today |
| Equal weight | the same weight for each holding (1/n) |
| Risk parity | each holding brings the same share of the risk |
| Minimum variance | the lowest possible volatility, **with no cap per security** |

Note: this minimum variance applies no cap, unlike the one in the Optimisation tab (adjustable cap). It can therefore be more concentrated.

### The columns and their formulas

```
Expected return          = Σ wᵢ × μᵢ                     (μ = daily average × 252)
Volatility               = √(wᵀ Σ w)
Sharpe                   = (expected return − risk-free rate) / volatility
Diversification ratio    = Σ wᵢ × σᵢ / σp
Effective number of bets = 1 / Σ (share of riskᵢ)²
Largest contribution     = largest share of risk of a single holding
```

### Verified example

Two securities A (20%) and B (10%), correlation 0.2, at 50 / 50:

- diversification ratio = (0.5 × 0.20 + 0.5 × 0.10) / 0.1204 = **1.25**;
- effective number of bets = 1 / (0.759² + 0.241²) = **1.58**;
- largest contribution = 75.9%.

In risk parity: ratio 1.29, effective number of bets **2.0**, largest contribution 50%.

### Interpretation

- **Diversification ratio**: 1 means no diversification (all securities perfectly correlated); the higher it is, the more the securities offset one another.
- **Effective number of bets**: how many "independent" holdings the portfolio really represents from a risk point of view. It equals n if all holdings contribute equally, 1 if a single holding carries all the risk. A portfolio of 69 holdings may be worth only about thirty bets.
- **Largest contribution**: dependence on a single holding.

The [[Show the weights of each allocation]] panel displays the weights (in %) of each security in the four allocations.

### Limitations

The expected returns are historical (the same fragility as in the Optimisation tab); the other columns depend only on past volatilities and correlations.

## The backtest: should you rebalance your portfolio?
<!-- fiche: gestion-backtest-reequilibrage | questions: should I rebalance my portfolio ; monthly quarterly or annual rebalancing which is best ; what is buy and hold ; how do I read the backtest ; buy and hold or rebalancing ; does the backtest use my real transactions ; when does the rebalancing take place | mots: backtest, rebalancing, buy and hold, monthly, quarterly, annual, target weights, strategy, historical simulation | aller: Gestion d'actifs/Backtest de stratégies | chiffres: volatilite, max_drawdown -->

The **Strategy backtest** tab replays the real history with **the same securities and the same starting weights** as your current portfolio, according to four strategies.

| Strategy | Rule |
|---|---|
| Buy and hold | you buy once and touch nothing more: weights drift with prices |
| Monthly rebalancing | back to the starting weights on the first trading day of each month |
| Quarterly rebalancing | on the first trading day of each quarter |
| Annual rebalancing | on the first trading day of each year |

The first day of the period is not a rebalancing day. All strategies pay the fees on the initial purchase.

### This is not your real history

The backtest assumes you had bought the current weights **right from the start**. It ignores your real transactions. The period starts on the first day on which **all** your current securities have a price, within the portfolio's analysis period.

### How rebalancing works

```
amount traded = Σ |target value of the holding − current value of the holding|
fees          = fee rate × amount traded
new value     = value − fees, split according to the target weights
```

### What is displayed

- the "Rebalance or not?" chart, rebased to 100;
- the "Results" table: Annualised return, Volatility, Max drawdown, Sharpe, Turnover / year.

```
Annualised return = (final value / initial value)^(365 / number of days) − 1
Volatility        = standard deviation of daily returns × √252
Max drawdown      = largest fall from a peak
Sharpe            = (annualised return − risk-free rate) / volatility
```

Sharpe example: annualised return 8%, volatility 14%, risk-free rate 2.5%: (8 − 2.5) / 14 = **0.39**.

### Interpretation

Rebalancing means **selling what has risen to buy what has fallen**. It maintains the intended risk, but costs fees and holds back performance when a trend persists (winners are trimmed too early). In a trendless market, with ups and downs, rebalancing can on the contrary pay off. Buy and hold lets winners grow: its risk drifts over time.

## Backtest fees and turnover
<!-- fiche: gestion-backtest-frais-rotation | questions: what is turnover per year ; how much do rebalancings cost ; how do I set the transaction costs of the backtest ; what does turnover 40% mean ; brokerage fees in the backtest ; why does monthly rebalancing earn less | mots: transaction costs, turnover, costs, brokerage, rebalancing fees, cost of rebalancing | aller: Gestion d'actifs/Backtest de stratégies | chiffres: frais_totaux -->

### The setting

The [[Transaction costs (%)]] slider goes from 0 to 0.5%, in steps of 0.05, with **0.10%** to start. Fees apply to the amounts bought or sold, including the initial purchase. The chart's subtitle recalls the chosen rate.

### Turnover

```
turnover of one rebalancing = amount traded / portfolio value
Turnover / year = sum of the turnovers / number of years in the period (days / 365)
```

The amount traded counts sales **and** purchases: a turnover of 10% corresponds to 5% of the portfolio sold and 5% bought back.

### Verified example

Two securities at 50 / 50 on €100. After one month, A has gained 10% and B has lost 10%: the holdings are worth €55 and €45. The rebalancing brings each holding back to €50:

- amount traded = |50 − 55| + |50 − 45| = **€10**;
- fees at 0.1% = **€0.01**;
- turnover = 10 / 100 = **10%**.

With the fees on the initial purchase (0.1%), the portfolio is worth €99.90 before this rebalancing and €99.89 after.

### Interpretation

The higher the frequency, the higher the turnover and fees. The "Turnover / year" column lets you estimate the annual cost: turnover × fee rate. For example, 40% turnover per year at 0.1% costs 0.04% per year. The performance gaps between strategies often come more from the trend effect than from fees.

### Limitations

Fees are proportional: no fixed fee per order, no bid-ask spread, no tax on gains realised on sales (which weighs on a securities account).

## Investing all at once or gradually (DCA)?
<!-- fiche: gestion-dca | questions: is it better to invest all at once or little by little ; what is dca ; dollar cost averaging explanation ; gradual investing over 12 months ; what happens to the money waiting ; what is the lowest value ; why does investing all at once earn more ; smoothing your stock market purchases | mots: DCA, dollar cost averaging, gradual investing, regular contributions, lump sum, all at once, market timing, cash | aller: Gestion d'actifs/Backtest de stratégies -->

The second part of the **Strategy backtest** tab compares two ways of investing the same capital in the same basket of securities (current weights, no rebalancing afterwards).

### The settings

- [[Capital for the DCA comparison (€)]]: from €1,000 to €10,000,000, in steps of 1,000, **€10,000** to start;
- [[Length of the gradual investment (months)]]: from 3 to 24 months, **12** to start;
- the fees from the [[Transaction costs (%)]] slider apply to each purchase.

### The two strategies

- **All at once**: all the capital is invested on the first day of the period.
- **Gradual**: the capital is divided into equal parts, invested on the first trading day of each of the first months. Money waiting is remunerated at the **risk-free rate** from Settings:

```
monthly instalment = capital / number of months
daily rate on cash = (1 + risk-free rate)^(1/252) − 1
value = basket units held × basket value + cash
```

### Example

€10,000 over 12 months: €833.33 per month. With 0.1% fees, each instalment buys 833.33 × 0.999 = **€832.50** of securities. With a risk-free rate of 2.5%, cash earns (1.025)^(1/252) − 1 ≈ **0.0098%** per trading day.

### What is displayed

The chart of the two value curves, in euros, and the "Comparison" table: Final value, Gain (final value − capital) and Lowest value reached during the period.

### Interpretation

In a rising market, investing **all at once** generally earns more: the money works sooner. **Gradual** investing reduces the risk of investing just before a fall: its lowest value is often higher, especially since part of it stays in cash at the start. It is a trade-off between expected return and regret.

### Limitations

- a single history: the result depends entirely on the period observed;
- if the period has fewer months than the chosen length, the capital is spread over the months available;
- prices excluding dividends.

## The limits of the backtest
<!-- fiche: gestion-backtest-limites | questions: can I rely on the backtest ; does the backtest guarantee future results ; why is the backtest short ; backtest unavailable what do I do ; are dividends included in the backtest ; backtest bias | mots: limitations, backtest, bias, overfitting, short period, excluding dividends, past performance, robustness | aller: Gestion d'actifs/Backtest de stratégies -->

A backtest tells you what **would have** worked over a past period. It guarantees nothing for the future.

### The software's own limitations

- **A single period**: that of your portfolio, starting from the day on which all your current securities have a price. If one of your securities is recent, the period is short, and conclusions are fragile.
- **Prices excluding dividends**: returns are slightly underestimated, in the same way for all strategies.
- **Securities chosen today**: the backtest tests securities that you hold **now**, often because they have done well. This is a selection bias.
- **Simplified fees**: proportional, with no tax on sales.
- **Not your real transactions**: the starting weights are your current weights.

### Good practice

Compare strategies with one another rather than retaining an absolute figure, and look at return, volatility, max drawdown and turnover together.

### In case of the "Backtest unavailable" message

The message is followed by the cause. It appears, for example, if the common history of your securities is empty or too short. Check your prices with [[Refresh prices]].
