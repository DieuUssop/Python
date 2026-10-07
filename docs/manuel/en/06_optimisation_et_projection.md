# Optimisation and projection
<!-- chapitre: optim | ordre: 6 -->

This chapter explains the two forward-looking tabs of the "Portfolio analysis" area. The **Optimisation** tab applies Markowitz theory to your holdings: efficient frontier, minimum-variance and maximum-Sharpe portfolios, and a "from → to" table of the changes to make. The **Projection** tab simulates thousands of possible paths for your portfolio using the Monte Carlo method. Each fiche gives the exact formula used by the software, a worked example and the limitations to keep in mind.

## What does the Optimisation tab do? The Markowitz principle
<!-- fiche: optim-principe-markowitz | questions: what is Markowitz optimisation ; what is the optimisation tab for ; how does the software find the best portfolio ; why does diversifying reduce risk ; modern portfolio theory explained simply ; what does optimal portfolio mean ; how does the optimiser work ; what is markowitz exactly | mots: Markowitz, modern portfolio theory, diversification, optimisation, mean-variance, covariance, correlation, optimal allocation, SLSQP | aller: Analyse du portefeuille/Optimisation | chiffres: sharpe, volatilite, nb_titres -->

The **Optimisation** tab looks for other allocations, **among the securities you already hold**, that would offer a better return / risk trade-off. It adds no security: it only changes the weights.

### Markowitz's idea (1952)

An investor looks not only at return but also at risk. Yet the risk of a portfolio is not the average of the risks of its securities: when two securities do not rise and fall exactly together (correlation below 1), their movements partly offset each other. Risk can therefore be reduced without reducing return.

### The two formulas at the heart of the calculation

```
Expected portfolio return = Σ wᵢ × μᵢ            (wᵀ μ)
Portfolio variance        = Σ Σ wᵢ × wⱼ × covᵢⱼ   (wᵀ Σ w)
Volatility                = √variance
```

where `wᵢ` is the weight of security i, `μᵢ` its expected annual return and `covᵢⱼ` the annual covariance between securities i and j.

### Worked example

Two securities: A (return 8%, volatility 20%) and B (return 4%, volatility 10%), correlation 0.2.

- 50 / 50 portfolio: return = 0.5 × 8% + 0.5 × 4% = **6%**. Variance = 0.25 × 0.04 + 0.25 × 0.01 + 2 × 0.25 × 0.2 × 0.20 × 0.10 = 0.0145, i.e. a volatility of **12.04%**, clearly less than the average of the volatilities (15%).
- Minimum-variance portfolio: 14.3% of A and 85.7% of B, volatility **9.56%**, lower than that of B alone (10%) even though it contains a security twice as risky.

That is the whole point of diversification.

### What the software calculates

1. the expected return and the covariance matrix of your securities;
2. the **minimum-variance** portfolio (the least risky possible);
3. the **maximum-Sharpe** portfolio (the best return per unit of risk);
4. the **efficient frontier** (40 points);
5. a cloud of 4,000 randomly drawn portfolios, to visualise the full set of possibilities.

Three cards, below the maximum-weight slider, give for the current portfolio, the minimum variance and the maximum Sharpe, the Sharpe ratio, the return and the volatility.

### The constraints applied

- no short selling: each weight is positive or zero;
- all the capital is invested: the weights add up to 100%;
- a maximum weight per security, adjustable with the [[Maximum weight per security]] slider.

The numerical optimisation uses the SLSQP method from the scipy library (at most 500 iterations), starting from equal weights. The whole exercise remains academic: the software says so under the results, and it is not investment advice.

## How are each security's expected return and risk estimated?
<!-- fiche: optim-estimation-parametres | questions: where do the expected returns in the optimisation come from ; how is the covariance matrix calculated ; why multiply by 252 ; what period is the optimisation calculated over ; are the expected returns forecasts ; what are mu and sigma ; the expected return of my stock is huge is that normal ; does the optimisation include dividends | mots: expected return, mu, covariance, covariance matrix, sigma, 252 days, estimation, historical data, annualisation | aller: Analyse du portefeuille/Optimisation | chiffres: volatilite -->

The optimisation needs two ingredients, estimated from the **history** of your securities.

### The exact formulas

```
μ (expected annual return) = average daily return × 252
Σ (annual covariance)      = covariance of daily returns × 252
Daily return               = today's price / previous day's price − 1
```

252 is the conventional number of trading days in a year. The diagonal of Σ holds the variance of each security; elsewhere it shows how two securities move together. The volatility of a single security is √(annual variance).

### Example

A security gains 0.04% a day on average, with a daily standard deviation of 1.2%:

- μ = 0.0004 × 252 = **10.08%** a year;
- volatility = 1.2% × √252 = **19.05%** a year.

### Over what period?

- The prices used are those of the portfolio analysis period, which begins at your first transaction.
- Only the days on which **all** your current securities have a return are kept. A recently listed security therefore shortens the period for all the others.
- Prices are converted into euros and are not adjusted for dividends (see the chapter on sources): for a security that pays out a lot, μ is slightly underestimated.

### Interpretation

μ is not a forecast: it is the average observed in the past, extrapolated to one year. Over a short, favourable period, a security can show a μ of 40% or more, which says nothing about the future. This is the first source of fragility in the optimisation (see the fiche on limitations).

## Reading the efficient frontier chart
<!-- fiche: optim-frontiere-efficiente | questions: what is the efficient frontier ; how do I read the optimisation chart ; what do the blue dots represent ; what is the dashed line ; why is no point above the curve ; where is my portfolio on the chart ; what does the green star mean ; the little grey dots with names | mots: efficient frontier, cloud of portfolios, capital market line, tangency portfolio, Dirichlet, risk return chart | aller: Analyse du portefeuille/Optimisation | chiffres: sharpe, volatilite -->

The chart in the "Efficient frontier" section places each portfolio according to its **annual volatility** (horizontal axis) and its **expected annual return** (vertical axis). The best place is at the top left: plenty of return for little risk.

### The elements of the chart

| Element | What it represents |
|---|---|
| Blue dots ("Random portfolios") | 4,000 randomly drawn allocations; the darker the blue, the higher the Sharpe (scale on the right) |
| Thick black curve ("Efficient frontier") | for each level of return, the least risky portfolio |
| Grey dots with a code | each security on its own (100% of the portfolio in that security); codes are only shown up to 20 securities |
| Orange circle ("My portfolio") | your current allocation |
| Diamond ("Minimum variance") | the least risky portfolio |
| Green star ("Maximum Sharpe") | the best return per unit of risk |
| Dashed line ("Capital market line") | combinations of the risk-free investment and the maximum-Sharpe portfolio |

Each notable portfolio shows its Sharpe in the legend. Hover over a point to read its volatility and return.

### How the frontier is built

The software sets 40 target returns, evenly spaced between the return of the minimum-variance portfolio and the maximum achievable return given the per-security cap (securities are filled from the most profitable to the least profitable, each up to the cap). For each target, it looks for the weights that minimise the variance `wᵀ Σ w`. An impossible target is simply ignored.

Below the minimum variance, portfolios are "inefficient": more return can be obtained for the same risk.

### The random portfolios

The weights are drawn from a Dirichlet distribution (all positive, summing to 100%), with a fixed random seed: the cloud is identical from one display to the next. These portfolios do **not** respect the per-security cap. As the frontier is calculated with that cap, a few points may slightly exceed a very constrained frontier; without a cap, none exceeds it, which visually checks the optimisation.

### The capital market line

```
Return = risk-free rate + slope × volatility
slope  = (maximum-Sharpe return − risk-free rate) / maximum-Sharpe volatility
```

It starts from the risk-free rate (set in [[Risk-free rate (% per year)]]) and touches the frontier at the maximum-Sharpe portfolio, hence its other name, the "tangency portfolio".

## The "Maximum weight per security" setting
<!-- fiche: optim-poids-maximal | questions: what is the maximum weight per security for ; why does the optimiser put everything in two stocks ; how do I limit concentration in the optimisation ; why can't I choose 10% ; the slider only offers no limit ; what does no limit mean ; which cap should I choose ; the dashed line cap 30% | mots: maximum weight, cap, constraint, concentration, limit per holding, UCITS, forced diversification, 30% | aller: Analyse du portefeuille/Optimisation | chiffres: nb_titres -->

The [[Maximum weight per security]] slider, at the top of the Optimisation tab, sets the maximum share that a security can take in the optimised portfolios (minimum variance, maximum Sharpe and frontier).

### Why a cap?

Without a limit, the optimiser often concentrates everything in 2 or 3 securities: those that have done best in the past. The cap imposes a minimum level of diversification. The default value is **30%**. For reference, fund regulations (UCITS) limit each holding to 10%, with a tolerance of up to 40% for the total of all holdings above 5%.

### The values offered

10%, 15%, 20%, 25%, 30%, 40%, 50% and "no limit". Only the values that allow 100% of the capital to be invested appear:

```
condition: number of securities × maximum weight ≥ 100%
```

Examples:

- with 3 securities, 30% × 3 = 90%: impossible. The slider only offers 40%, 50% and no limit;
- with 5 securities, all values from 20% upwards are offered;
- with 10 or more securities, all values are offered.

If 30% is not possible (fewer than 4 securities), the slider starts on "no limit".

### Effect on the results

The lower the cap, the more the optimised portfolios resemble a balanced portfolio, and the more their Sharpe falls slightly. The cap appears in the compared allocations chart as a dashed vertical line, labelled "Cap 30% per holding" (or the value chosen).

In the two-security example A (8%, 20%) and B (4%, 10%), correlation 0.2, risk-free rate 2.5%: with no limit, the maximum Sharpe puts 56.3% in A (Sharpe 0.292); with a 50% cap, it is held at 50 / 50 (Sharpe 0.291).

## Maximum Sharpe or minimum variance: which one should I look at?
<!-- fiche: optim-sharpe-ou-variance | questions: what is the difference between maximum sharpe and minimum variance ; which optimised portfolio should I choose ; what is the minimum variance portfolio ; tangency portfolio explained ; why is the maximum sharpe riskier ; how is the sharpe calculated in the optimisation ; which of the two is better | mots: maximum Sharpe, minimum variance, tangency portfolio, min variance, Sharpe ratio, return per unit of risk, cautious allocation | aller: Analyse du portefeuille/Optimisation | chiffres: sharpe, volatilite -->

The software calculates two notable portfolios, with the same constraints (positive weights, sum 100%, per-security cap).

### Minimum variance

```
minimise   wᵀ Σ w
```

This is the **least risky portfolio possible** with your securities. It **does not use expected returns**, only volatilities and correlations. That is an advantage: covariances can be estimated much better than returns. It is often more stable over time.

### Maximum Sharpe

```
Sharpe = (expected return − risk-free rate) / volatility
maximise Sharpe   (in practice: minimise −Sharpe)
```

This is the portfolio that offers the **best return per unit of risk**. Combined with the risk-free investment, it gives the best possible line: it is the tangency portfolio. It depends directly on the expected returns, and therefore on the history.

### Example

Securities A (8%, 20%) and B (4%, 10%), correlation 0.2, risk-free rate 2.5%, no cap:

| Portfolio | Weights A / B | Return | Volatility | Sharpe |
|---|---|---|---|---|
| Minimum variance | 14.3% / 85.7% | 4.57% | 9.56% | 0.22 |
| Maximum Sharpe | 56.3% / 43.7% | 6.25% | 12.87% | 0.29 |

The Sharpe is calculated here on the expected annual return (`wᵀ μ`): it may differ from the Sharpe ratio in the Performance tab, which is calculated on the portfolio's actual returns.

### Which one should I look at?

- **Minimum variance**: for a cautious investor, or if you doubt past returns.
- **Maximum Sharpe**: for the best theoretical efficiency, accepting that it exploits the securities that have done best.

The [[Compare my portfolio with]] selector in the "Allocations compared" section lets you display the changes to make towards one or the other. By default, it is the maximum Sharpe.

## Reading the "Allocations compared": what would need to change?
<!-- fiche: optim-repartitions-comparees | questions: how do I read the compared allocations ; what do the green and red arrows mean ; what should I buy or sell according to the optimisation ; why are some securities missing from the chart ; what are the equities bonds gold bars ; what does 35% of the portfolio changes place in total mean ; what does sell entirely mean ; unchanged securities not shown | mots: allocations compared, from to, arrows, rebalancing, increase, reduce, sell entirely, asset classes, turnover, unchanged | aller: Analyse du portefeuille/Optimisation | chiffres: valeur_actuelle, nb_titres -->

The "Allocations compared" section turns the optimisation result into concrete changes, **with the total value unchanged and excluding fees**. First choose the target with [[Compare my portfolio with]]: [[Maximum Sharpe]] or [[Minimum variance]].

### 1. The summary sentence

It cites the three largest increases and the three largest reductions, the number of securities that are sold out, the share of the portfolio that changes place, and the asset class that moves the most (if its weight changes by at least 5 points).

### 2. The bars by asset class

Two stacked bars at 100%: "Current" and the chosen portfolio, split into Equities, Bonds, Gold, Money market. They only appear if the portfolio contains something other than equities. A security missing from the reference database is counted as an equity.

### 3. The "from → to" chart

For each security: a white circle at the current weight and an arrow to the suggested weight, with a label such as "40% → 34.7%".

| Colour | Meaning | Rule in the code |
|---|---|---|
| Green, arrow pointing right | To increase | positive difference |
| Red, arrow pointing left | To reduce | negative difference |
| Red | To sell entirely | suggested weight below 0.25% |
| Not shown | Unchanged | difference below 0.25 points in absolute value |

The biggest change is at the top. At most 20 rows are drawn; a note under the chart gives the number of unchanged securities not shown and the number of small adjustments left to the detailed table.

### The formulas

```
difference = suggested weight − current weight
amount     = difference × total portfolio value
turnover   = Σ |difference| / 2
```

Turnover is the share of the portfolio to be moved: every euro sold is reinvested elsewhere, hence the division by 2.

### Verified example

Portfolio of €50,000, maximum Sharpe target:

| Security | Class | Current | Suggested | Amount | Action |
|---|---|---|---|---|---|
| Stock X | Equities | 30% | 0.1% | −€14,950 | Sell entirely |
| Bond fund | Bonds | 10% | 30% | +€10,000 | Increase |
| Gold | Gold | 5% | 20% | +€7,500 | Increase |
| World ETF | Equities | 40% | 34.7% | −€2,650 | Reduce |
| Stock Y | Equities | 15% | 15.2% | +€100 | Unchanged |

Turnover = (29.9 + 20 + 15 + 5.3 + 0.2) / 2 = **35.2%**. The summary says: increase Bond fund and Gold; reduce Stock X and World ETF; 1 security is sold out entirely; 35% of the portfolio changes place; the equity share goes from 85% to 50%.

Note that "Sell entirely" is displayed as soon as the suggested weight falls below 0.25%, even if the calculated amount is not quite equal to the value of the holding.

## The "Adjustment details" table: how much should I buy or sell?
<!-- fiche: optim-detail-ajustements | questions: how much of each security should I buy ; where can I see the amounts to buy and sell ; the adjustments table ; what is the suggested column ; are fees included in the amounts ; I can't find a security in the arrows chart ; export the orders to place | mots: adjustment details, amounts, buy, sell, orders, arbitrage, suggested, reallocation | aller: Analyse du portefeuille/Optimisation | chiffres: valeur_actuelle -->

Under the "from → to" chart, the collapsed panel [[Adjustment details (amounts to buy / sell)]] lists **all** the securities, including the unchanged ones and those that do not fit in the chart.

### The columns

| Column | Content |
|---|---|
| Security | name of the security |
| Class | asset class (Equities, Bonds, Gold, etc.) |
| Current | current weight, in % |
| Suggested | weight in the chosen target portfolio, in % |
| Buy / sell | `(suggested weight − current weight) × total value`, in euros, signed |
| Action | Increase, Reduce, Sell entirely or Unchanged |

The rows are sorted from the biggest change to the smallest. The sum of the amounts is zero: sales fund purchases.

### Example

Portfolio of €50,000, one holding weighs 10% and the target portfolio gives it 30%: amount = (0.30 − 0.10) × 50,000 = **+€10,000** to buy.

### What the amounts do not include

- brokerage **fees**;
- **taxes** on capital gains realised by selling (see the Wealth advisory area, Taxation tab);
- rounding to a whole number of units.

There is no export of stock market orders: the software is not connected to any broker. You have to place the orders yourself with your institution.

## The limitations of Markowitz optimisation
<!-- fiche: optim-limites | questions: can I trust the optimisation ; why does the optimiser recommend absurd things ; limitations of markowitz ; what is estimation error ; should I follow the recommendations of the optimisation tab ; the results change a lot when I change the cap ; why does the maximum sharpe bet on the stocks that rose the most | mots: limitations, estimation error, error maximiser, instability, overfitting, past returns, bias, robustness | aller: Analyse du portefeuille/Optimisation -->

Markowitz optimisation is a powerful teaching tool, but its results must be read with caution. The software itself displays this under the results.

### 1. Estimation error

The expected returns μ are the average of past returns. But an average estimated over a few years is very imprecise. Order of magnitude: for a security with a volatility of 20% observed over 3 years, the standard error on the average annual return is 20% / √3 ≈ **11.5 points**. A μ estimated at 10% is therefore compatible with a true return of between roughly −13% and +33%.

The optimiser takes these figures at face value: it **over-exploits the securities that have done best** and neglects those that have fallen. It is sometimes nicknamed an "error maximiser".

### 2. Instability

A small change in the data (one more month, a different cap) can strongly change the maximum-Sharpe weights. The minimum-variance portfolio, which does not use μ, is more stable.

### 3. The model's assumptions

- risk boils down to volatility (crashes, which are more frequent than the normal distribution predicts, are not better accounted for);
- correlations are assumed to be stable, whereas they often rise in times of crisis;
- a single horizon, with no transaction costs or taxes.

### 4. Limitations specific to the software

- only your current securities are considered;
- the estimation period begins at your first transaction and is limited to the days on which all securities have a price;
- prices exclude dividends.

### How to use it intelligently

- above all, compare your portfolio with the **minimum variance**;
- lower the [[Maximum weight per security]] to obtain more reasonable allocations;
- see the differences as food for thought, not as orders;
- complement it with the "Risk budget" tab in the Asset management area, whose risk parity does not use expected returns either.

## Why does the Optimisation tab require at least 2 securities?
<!-- fiche: optim-deux-titres | questions: the optimisation tab is empty ; message at least 2 securities needed ; I only have one etf why no optimisation ; optimisation impossible why ; error the optimisation did not converge ; how to optimise a portfolio with a single fund | mots: two securities, single security, single ETF, optimisation impossible, error, convergence, message | aller: Analyse du portefeuille/Optimisation | chiffres: nb_titres -->

Optimising means choosing an **allocation between several securities**. With a single security, there is only one possible allocation: 100% in that security. The tab then displays the message: "The optimisation compares several allocations between securities: at least 2 securities are needed in the portfolio."

The number of securities taken into account is that of the portfolio's **current positions**.

### If you hold a single ETF

A world ETF contains hundreds of stocks, but the software treats it as **a single security** in the optimisation: it cannot change the fund's internal composition. To use the tab, you need at least two lines (for example an equity ETF and a bond ETF).

### The "Optimisation failed" message

This message, followed by an explanation, appears when the calculation fails. Possible causes:

- the numerical optimiser did not converge (message "The optimisation did not converge");
- a security does not have enough common history with the others to estimate the covariances.

Try another [[Maximum weight per security]] or [[Refresh prices]]. If only the frontier fails while the two notable portfolios are calculated, the software draws an approximate frontier (see the corresponding fiche).

With 2 or 3 securities, the maximum-weight slider only offers caps compatible with 100% investment and starts on "no limit".

## Why is the efficient frontier "approximate"?
<!-- fiche: optim-frontiere-approchee | questions: why does it say efficient frontier approximate ; the frontier curve looks like a staircase ; the frontier does not display correctly ; what does approximate mean in the legend ; the optimiser found no point on the frontier ; weird frontier with a recent stock | mots: approximate frontier, envelope, fallback solution, cloud, approximation, convergence, short history | aller: Analyse du portefeuille/Optimisation -->

When the chart legend says "Efficient frontier (approximate)", it means the optimiser could not calculate at least two points of the exact frontier. The software then uses a **fallback solution** drawn from the cloud of 4,000 random portfolios.

### How the approximate frontier is built

1. the random portfolios are sorted by increasing volatility;
2. only those whose return reaches the best return already seen at a lower volatility (the "running maximum") are kept.

```
keep a portfolio if: return ≥ best return of the less risky portfolios
```

This gives the **upper envelope** of the cloud: for each level of risk, the best return already reached by a randomly drawn portfolio.

### Example

Portfolios sorted by volatility: (8%; 4%), (9%; 5%), (10%; 4.5%), (11%; 6%). The third is discarded (4.5% < 5%); the envelope passes through the other three.

### Frequent causes

- a security with too short a history;
- very tight constraints (low cap with few securities);
- a numerical failure of the optimiser on certain target returns.

### What this changes

The approximate frontier is **slightly below** the true frontier (a random draw never reaches the optimum exactly) and may look like a staircase. It remains useful for placing your portfolio. It ignores the per-security cap, since the random portfolios do not respect it. The "Minimum variance" and "Maximum Sharpe" cards remain calculated exactly.

## What is a Monte Carlo projection?
<!-- fiche: optim-monte-carlo-principe | questions: what is monte carlo ; how does the projection tab work ; how much will my portfolio be worth in 10 years ; how does the software simulate the future ; why 5000 scenarios ; do the results change every time ; simulation of the future value of the portfolio ; what is the projection for | mots: Monte Carlo, simulation, projection, scenarios, geometric Brownian motion, future, horizon, 5000 simulations | aller: Analyse du portefeuille/Projection | chiffres: valeur_actuelle, twr_annualise, volatilite -->

We cannot predict **the** future, but we can simulate **thousands of possible futures**, all consistent with the portfolio's return and risk, and then study the distribution of the results. This is the Monte Carlo method, used in the **Projection** tab.

### What the software does

1. It starts from the **current value** of your portfolio.
2. It simulates **5,000 scenarios**, **month by month**, up to the chosen horizon.
3. Each month, the value is multiplied by a randomly drawn growth, then the monthly contribution is added:

```
Value(month + 1) = Value(month) × exp(log-return of the month) + monthly contribution
```

4. At each date, it calculates the 5th, 25th, 50th, 75th and 95th percentiles of the 5,000 values.

The time step is the **month** (not the day): this is sufficient for a projection over several years and about 20 times faster.

### What is displayed

- four cards: [[Adverse scenario]] (5th percentile), [[Median scenario]], [[Favourable scenario]] (95th percentile) and [[Probability of loss]], plus [[Target reached]] if a target is entered;
- the fan chart or scatter plot of the paths;
- the distribution of the final value and its reading sentences.

### Reproducible results

The randomness is fixed by a "seed": with the same assumptions, you get exactly the same figures each time it is displayed. Changing a setting launches a new simulation.

### Example

€100,000, return 7%, volatility 15%, 10 years, no contributions, normal distribution: median **€178,727**, adverse scenario **€81,876**, favourable scenario **€389,613**, probability of loss **10.4%**. Theory gives a median of €179,948: the difference comes from the finite number of scenarios.

## The adjustable assumptions of the projection
<!-- fiche: optim-hypotheses-projection | questions: how do I change the projection horizon ; add a monthly contribution to the simulation ; how do I set a target ; what return should I put in the projection ; why is the volatility slider greyed out ; where does the default suggested return come from ; the historical return shown is 35% but the slider stops at 20 ; simulate a monthly savings plan | mots: assumptions, horizon, monthly contribution, target, assumed return, assumed volatility, regular savings, simulation parameters | aller: Analyse du portefeuille/Projection | chiffres: valeur_actuelle, volatilite -->

The "Simulation assumptions" box, at the top of the Projection tab, gives in its subtitle the portfolio's **historical return and volatility**, then offers six settings.

| Setting | Range | Starting value |
|---|---|---|
| [[Horizon (years)]] | 1 to 30 years | 10 years |
| [[Monthly contribution (€)]] | €0 to €1,000,000, steps of €100 | €0 |
| [[Target (€, optional)]] | €0 to €100,000,000, steps of €5,000 | 0 (no target) |
| [[Method]] | [[Normal distribution]] or [[Historical (bootstrap)]] | Normal distribution |
| [[Assumed annual return (%)]] | −5% to 20%, steps of 0.5 | historical return |
| [[Annual volatility (%)]] | 1% to 50%, steps of 0.5 | historical volatility |

### Where the historical values come from

They are calculated from the portfolio's daily returns (those of the TWR performance):

```
historical return     = average daily return × 252
historical volatility = standard deviation of daily returns × √252
```

The sliders start on these values, **rounded to the nearest 0.5 point** and **brought back within the range** of the slider. Example: a historical return of 12.3% gives a slider at 12.5%; a historical return of 35% is brought back to 20%.

### Tips

- A historical return obtained over a short, favourable period is too optimistic: **reduce it** for a cautious projection.
- The **monthly contribution** is added at the end of each month. The total amount invested is `current value + contribution × number of months`.
- The **target** adds a probability card and a dotted horizontal line on the fan chart.

### Why the volatility is greyed out

With the historical method, the volatility slider is disabled: the dispersion comes from the portfolio's actual trading days, drawn at random. The return slider remains active (see the fiche on the two methods).

The amounts are **nominal**: neither inflation, nor taxes, nor fees are deducted.

## Normal method or historical method (bootstrap)?
<!-- fiche: optim-methode-normale-historique | questions: what is the difference between normal distribution and historical in the projection ; what is bootstrap ; which method should I choose for the simulation ; why does the historical method give a lower adverse scenario ; geometric brownian motion explained ; why minus sigma squared over 2 ; the normal distribution underestimates crashes ; fat tails in the simulation | mots: normal distribution, bootstrap, historical, geometric Brownian motion, Black-Scholes, Itô's lemma, fat tails, resampling, crash | aller: Analyse du portefeuille/Projection | chiffres: volatilite, asymetrie, kurtosis -->

The [[Method]] button offers two ways of randomly drawing each month's return.

### 1. Normal distribution (geometric Brownian motion)

This is the Black-Scholes model. Over one month (dt = 1/12 year), the log-return follows:

```
monthly log-return ~ Normal( mean = (μ − σ²/2) × 1/12 , standard deviation = σ × √(1/12) )
```

With μ = 7% and σ = 15%: monthly mean = (0.07 − 0.01125) / 12 = **0.490%**, monthly standard deviation = 0.15 × 0.2887 = **4.33%**.

**Why "− σ²/2"?** The return μ is an arithmetic average, but compound growth is lower: +50% then −50% gives an average of 0%, but you end up at 0.75, i.e. −25%. The −σ²/2 term corrects this effect (Itô's lemma).

### 2. Historical (bootstrap)

Each month is built by randomly drawing, **with replacement**, **21 actual daily returns** of the portfolio, and adding their logarithms. This preserves the real shape of the returns: **fat tails** (crashes more frequent than in the normal distribution) and skewness.

The return is then **re-centred** on the [[Assumed annual return (%)]] slider:

```
σ        = standard deviation of daily returns × √252
target   = (μ − σ²/2) / 252                 (targeted average daily log-return)
re-centred log-returns = log-returns − their mean + target
```

Example: μ = 7%, σ = 15%: target = 0.05875 / 252 = 0.0233% per day, i.e. 0.490% over 21 days, as with the normal distribution. Only the shape of the distribution changes.

This method requires at least 20 daily returns in the history.

### Which one should I choose?

- **Normal distribution**: simple, standard, adjustable (you choose the volatility). It underestimates crashes.
- **Historical**: more realistic on extremes, but limited to the events of your analysis period. If your history contains no crash, it will not invent one.

Compare the two: an adverse scenario clearly lower with the historical method signals fat tails in your portfolio (see also the Risk tab).

## Reading the fan chart and the scatter plot of the projection
<!-- fiche: optim-eventail-nuage | questions: how do I read the projection chart ; what do the blue areas represent ; what is the scatter plot of the simulation ; why are the dots different colours ; what is the orange dotted line ; is the median curve a scenario ; display both charts ; why does the fan widen over time | mots: fan chart, scatter plot, percentiles, probability bands, median, money invested, paths | aller: Analyse du portefeuille/Projection | chiffres: valeur_actuelle -->

The [[Display]] selector offers three views: [[Fan chart]] (default), [[Scatter plot]] or [[Both]].

### The fan chart

| Element | Meaning |
|---|---|
| Light blue area | 90% of scenarios (between the 5th and 95th percentiles) |
| Darker blue area | 50% of scenarios (between the 25th and 75th percentiles) |
| Blue curve | median scenario (50th percentile) |
| Orange dashes | money invested (starting value + cumulative contributions) |
| Dotted line "Target" | your target, if entered |

Hover over the curve to read, at each date, the median and the 90% range.

**Warning**: the percentiles are calculated **date by date**. The median curve is not a real scenario: no scenario stays in the middle all the time.

The fan **widens with the horizon**: this is uncertainty accumulating. With the normal distribution, the standard deviation of cumulative log-returns grows as σ × √years.

### The scatter plot

Each point is **one scenario at a given date**. The software displays the **first 400 scenarios**, every 6 months (every year if the horizon exceeds 15 years), plus the final date. Points on the same date are slightly offset horizontally to stay legible.

Each point is coloured according to its band **at that date**:

| Colour | Band |
|---|---|
| Dark red | Worst 5% (below the 5th percentile) |
| Light red | Adverse (5 to 25%) |
| Grey | Central (25 to 75%) |
| Light blue | Favourable (75 to 95%) |
| Dark blue | Best 5% (above the 95th percentile) |

Reference marks complete the cloud: median, 5% and 95% thresholds (dotted) and money invested. Hover over a point to see its scenario number and its date: the same scenario can change band over time.

The scatter plot shows the **real dispersion** of the results, which the fan chart summarises.

## The final-value distribution: why is it not symmetrical?
<!-- fiche: optim-distribution-finale | questions: why is the mean higher than the median ; how do I read the final value histogram ; what is a log normal distribution ; what is the log scale for ; why is the curve leaning left with a long right tail ; which figure should I keep mean or median ; what do P5 and P95 mean ; the extreme scenarios do not appear | mots: final distribution, log-normal, histogram, mean, median, logarithmic scale, skewness, P5, P95, percentile | aller: Analyse du portefeuille/Projection | chiffres: valeur_actuelle, volatilite -->

The "Distribution of the final value" chart is a histogram: the portfolio value at the horizon, for each of the 5,000 scenarios. It carries three vertical markers: **Amount invested** (orange dashes), **Median** (solid line) and **Mean** (dotted), as well as a bluish zone "90% of scenarios (P5 to P95)".

### Why the distribution is log-normal

Returns **compound**: the final value is a **product** of monthly growths. It is therefore its **logarithm** (a sum) that follows a roughly normal distribution. The value itself follows a **log-normal** distribution: bounded on the left (you cannot lose more than 100%), with a long right tail (compounded gains have no ceiling).

With no contributions and the normal distribution:

```
median = initial value × exp((μ − σ²/2) × T)
mean   = initial value × exp(μ × T)
mean / median = exp(σ² × T / 2)
```

### Example

€100,000, μ = 7%, σ = 15%, T = 10 years:

- theoretical median = 100,000 × exp(0.5875) ≈ **€179,948** (simulated: €178,727);
- theoretical mean = 100,000 × exp(0.70) ≈ **€201,375** (simulated: €199,757);
- ratio = exp(0.1125) ≈ 1.12: the mean exceeds the median by about 12%.

### Mean or median?

A few very favourable scenarios pull the **mean** upwards. The **median** (a one-in-two chance of doing better) is the most representative marker. The software says so in the reading sentences as soon as the mean exceeds the median by more than 2%.

### P5 and P95

- **P5**: 5% of scenarios end below it ("1 chance in 20 of doing worse"). In the example: €81,876.
- **P95**: 5% of scenarios end above it. In the example: €389,613.

The first reading sentence summarises: "In 90% of scenarios, the value in 10 years lies between … and …".

### The logarithmic scale

The [[Log scale]] switch plots the histogram of the logarithm of the value. The bell shape becomes roughly **symmetrical** again, centred on the median. The tick labels remain in euros (for example €50k, €100k, €200k, €500k).

### What is not displayed

For legibility, the axis stops at the 0.5th and 99.5th percentiles (widened if needed to show the amount invested): the most extreme 1% of scenarios are not drawn, but they count in all the figures. With monthly contributions, the distribution is no longer exactly log-normal, but the shape remains the same.

## Probability of loss, of doubling or of reaching a target
<!-- fiche: optim-probabilites | questions: how is the probability of loss calculated ; what chance do I have of reaching my target ; probability of doubling my capital ; does the probability of loss take inflation into account ; what does adverse scenario mean ; 1 chance in 20 of doing worse ; why does the probability of loss increase with contributions | mots: probability of loss, target, doubling, adverse scenario, favourable scenario, chance of success, risk of loss, percentile | aller: Analyse du portefeuille/Projection | chiffres: valeur_actuelle, montant_investi -->

The cards and sentences of the Projection tab simply count the **share of the 5,000 scenarios** that meet a condition, at the chosen horizon.

### The formulas

```
total invested         = current value + monthly contribution × number of months
probability of loss    = share of scenarios whose final value < total invested
probability of doubling = share of scenarios whose final value ≥ 2 × total invested
probability of target  = share of scenarios whose final value ≥ target
adverse scenario       = 5th percentile of the final values
median scenario        = 50th percentile
favourable scenario    = 95th percentile
```

### Verified example

€100,000, contribution of €200 a month, 10 years, μ = 7%, σ = 15%, normal distribution, target €250,000:

- total invested = 100,000 + 200 × 120 = **€124,000**;
- probability of loss = **10.6%**;
- probability of doubling (finishing above €248,000) = **35.9%**;
- probability of reaching €250,000 = **35.2%**;
- adverse scenario €104,075, median €211,406, favourable €439,552.

### Interpretation

- "Adverse scenario" does not mean "worst case": 1 scenario in 20 does even worse.
- The probability of loss compares the final value with the **sum paid in**, without remunerating it: finishing at €124,500 for €124,000 paid in is not a loss in the software's sense, but it is a poor investment.
- It generally decreases with the horizon, because the average rise accumulates faster than the dispersion.

### Limitations

All the amounts are **nominal**: neither inflation, nor taxes, nor fees are deducted. A loss of purchasing power is therefore not counted as a loss. These probabilities depend entirely on the return and volatility chosen.

## A projection is not a forecast
<!-- fiche: optim-pas-une-prevision | questions: is the projection reliable ; will my portfolio really be worth that in 10 years ; can I rely on the median scenario ; why is the projection too optimistic ; guarantee of result of the simulation ; limitations of monte carlo ; does the projection take inflation and taxes into account | mots: forecast, reliability, limitations, assumptions, uncertainty, guarantee, inflation, warning | aller: Analyse du portefeuille/Projection | chiffres: twr_annualise, volatilite -->

A Monte Carlo projection answers the question: **"if the assumptions hold, what is the range of possible outcomes?"**. It does not say what will happen. The software reminds you of this in the "How to read this projection" box: the median is not a forecast, it is the middle of the possibilities.

### What the projection assumes

- a **constant** return and volatility over the whole horizon;
- months that are **independent** of one another (no cycles, no trend);
- for the normal distribution, returns without fat tails;
- for the historical method, a future that resembles the days of your analysis period;
- a portfolio composition that does not change.

### What it ignores

- inflation, taxes and fees: the amounts are nominal and gross;
- changes of strategy, withdrawals or switches;
- events absent from the history or from the model.

### Why it can be too optimistic

The default return is the portfolio's **historical** return. Over a short, favourable period, it can be very high. Example: over 10 years with €100,000, going from 7% to 4% assumed return (volatility 15%) brings the theoretical median down from €179,948 to 100,000 × exp((0.04 − 0.01125) × 10) ≈ **€133,309**.

### How to use it

- test several returns, including a cautious one;
- compare the normal distribution and the historical method;
- look above all at the P5 – P95 **range** rather than a single figure;
- re-run the analysis regularly, as the history lengthens.
