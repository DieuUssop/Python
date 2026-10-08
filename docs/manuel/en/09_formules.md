# All the formulas
<!-- chapitre: formules | ordre: 9 -->

This chapter gives, indicator by indicator, the exact formula used by the software, as written in its code, with a small worked example, its interpretation and its limitations. Each fiche can be read on its own. The common conventions (252 trading days, 365-day basis, amounts in euros) are recalled in the first fiche.

## The calculation conventions common to all indicators
<!-- fiche: formule-conventions | questions: why 252 days ; what is the 365 basis ; are purchases counted at the start or end of the day ; are all calculations in euros ; what conventions does the software use ; why annualise with the square root of 252 ; when is a purchase made on a saturday counted ; calculation assumptions of the software | mots: conventions, 252 days, 365 days, annualisation, end of day, euros, closing price, assumptions -->

All indicators rely on the same conventions, written into the code.

| Convention | Value used |
|---|---|
| Trading days per year (volatility, Sharpe, alpha, tracking error) | 252 |
| Days per year to annualise a return (TWR, IRR) | 365 calendar days |
| Timing of transactions | at the end of the day, at that day's price |
| Price used | closing price, not adjusted for dividends |
| Currency | everything is converted into euros |
| Risk-free rate | constant over the whole period (2.50% by default) |

### Two different annualisations

- An **average** of daily returns is multiplied by 252.
- A daily **standard deviation** is multiplied by √252 ≈ 15.87: if the days are independent, variances add up, so the standard deviation grows as the square root of time.
- A **total return** is compounded over 365 days: `(1 + R) ^ (365 / number of days) − 1`.

### Days without a quote

A transaction entered on a day when the market is closed (a Saturday) is attached to the next trading day. On a holiday that affects only one exchange, the security's last known price is carried forward.

## How is each day's return calculated, without the effect of contributions?
<!-- fiche: formule-rendement-quotidien | questions: how is the daily return calculated ; why does my purchase not count as a gain ; daily return neutral to contributions ; formula for a one-day return ; a contribution raises the value but not the performance ; the first day the return is negative why ; how are flows removed from performance | mots: daily return, daily performance, flows, contributions, withdrawals, neutralisation, first day, purchase fees | aller: Analyse du portefeuille/Performance -->

A purchase of €1,000 raises the portfolio value by €1,000, with no gain at all. The software therefore removes the effect of flows.

### The formula

```
r(t) = (value(t) − flow(t)) / value(t−1) − 1
```

where, for each day, `flow` = money paid in (+) or taken out (−):

- BUY: `+ (quantity × price + fees)`;
- SELL: `− (quantity × price − fees)`;
- DIVIDEND: `− (amount − fees)`.

On the first day (or after everything has been sold), the previous day's value is 0: `r = value(t) / flow(t) − 1`. This return captures the purchase fees and the gap between the price paid and the closing price. Days when nothing is invested are excluded.

### Example

- Previous day: €10,000. Purchase that day: €1,000. Value in the evening: €11,200. `r = (11,200 − 1,000) / 10,000 − 1 = +2.00%`.
- First day: 10 securities bought at €500 with €2.50 of fees (flow €5,002.50), close at €505 (value €5,050): `r = 5,050 / 5,002.50 − 1 = +0.95%`.

### Limitation

The transaction is assumed to be made at the closing price: the return on the purchase day includes the gap between your price and that close.

These returns are used for the TWR, volatility, Sharpe, VaR and the projection.

## The TWR: time-weighted return
<!-- fiche: formule-twr | questions: what is the twr ; how is the total twr calculated ; time weighted return formula ; performance weighted by time ; why is my twr different from my percentage gain ; twr or simple return ; the performance of fund managers | mots: TWR, time-weighted return, performance, GIPS, compounding, base 100 | aller: Analyse du portefeuille/Performance | chiffres: twr_total, twr_annualise -->

The TWR (*time-weighted return*) measures the quality of investment choices, independently of the timing and size of contributions. It is the measure used by fund managers (GIPS standard): a manager does not choose when clients pay in money.

### The formula

```
TWR = (1 + r1) × (1 + r2) × … × (1 + rn) − 1
```

where the `r` are the daily returns neutralised for contributions (see the previous fiche). The "base 100" curve in the Performance tab is the same product, accumulated day after day: `index(t) = 100 × Π (1 + r)`.

### Example

+10% one day, then −5% the next: `1.10 × 0.95 − 1 = +4.5%`, not +5%.

### Interpretation

Two investors who hold the same securities in the same proportions have the same TWR, even if one invested €1,000 and the other €100,000, or on different dates. The TWR can therefore be compared directly with an index.

### Limitation

It ignores the effect of the timing of your contributions: to measure what your money has actually earned, see the IRR. The "by calendar year" TWR applies the same formula to the days of each year.

## The annualised TWR
<!-- fiche: formule-twr-annualise | questions: how is annualised performance calculated ; annualised twr formula ; why a 365-day basis ; return per year ; annualised perf huge over 3 months ; convert a total performance into an annual one ; 21% in two years how much is that per year | mots: annualisation, annualised TWR, annualised performance, annual return, 365 basis, compounding | aller: Analyse du portefeuille/Performance | chiffres: twr_annualise, twr_total -->

This is the "Annualised return" figure in the key figures and the "Annualised TWR" card in the Performance tab.

### The formula

```
Annualised TWR = (1 + total TWR) ^ (365 / number of days) − 1
```

The number of days is the gap, in calendar days, between the first and the last daily return in the history.

### Example

+21% over 730 days: `1.21 ^ (365 / 730) − 1 = +10%` a year, not 10.5%: gains compound from one year to the next.

### Interpretation

It is the constant return that, each year, would have led to the same result. It allows periods of different lengths to be compared.

### Limitations

- Over a short period, it **extrapolates**: +5% over 91 days gives about +21.6% a year, which says nothing about the coming year. Be wary of the annualised TWR over less than a year.
- It is meaningless if the first and last days are the same (the software then displays "n/a").

## The IRR: return on the money invested
<!-- fiche: formule-tri | questions: what is the irr ; internal rate of return formula ; money weighted return ; difference between irr and twr ; why is my irr negative while the twr is positive ; how is the annual irr calculated ; irr n/a why ; return on my money | mots: IRR, internal rate of return, TRI, money-weighted return, discounting, bisection, flows | aller: Analyse du portefeuille/Performance | chiffres: tri_annuel, twr_annualise -->

The IRR is the annual return as seen by the investor: it takes into account the amount and date of each contribution.

### The formula

It is the annual rate `i` that makes the discounted value of all flows equal to zero:

```
Σ CF_k / (1 + i) ^ (days_k / 365) = 0
```

- purchase: money leaving your pocket, `CF < 0`;
- sale, dividend: money coming in, `CF > 0`;
- on the last day, everything is treated as sold: `+ final value`;
- `days_k`: number of days since the first flow.

There is no direct formula: the software searches for `i` by bisection (200 iterations) between −99% and +1,000% a year. If there is no solution in this interval, it displays "n/a".

### Example: TWR and IRR point in opposite directions

€10,000 invested, +20% in the first year (€12,000). You then add €50,000, and the portfolio then loses 10% (€55,800).

- TWR: `1.20 × 0.90 − 1 = +8%` over two years, i.e. +3.9% a year.
- IRR: −6.05% a year, because the fall hit a sum five times larger than the rise.

### Interpretation

An IRR above the TWR means your contributions were well timed; below it, that they arrived before a fall.

## Annualised volatility
<!-- fiche: formule-volatilite | questions: how is volatility calculated ; why square root of 252 ; volatility formula standard deviation ; my volatility is 15% what does it mean ; annualised portfolio volatility ; measure of portfolio risk ; what is the standard deviation of returns | mots: volatility, standard deviation, risk, annualisation, square root of 252, dispersion, sigma | aller: Analyse du portefeuille/Risque | chiffres: volatilite -->

### The formula

```
Annual volatility = standard deviation of daily returns × √252
```

The standard deviation is the sample standard deviation (division by n − 1), calculated on daily returns neutralised for contributions.

### Why √252?

If daily returns are independent, their variances add up: annual variance = 252 × daily variance, so annual standard deviation = √252 × daily standard deviation.

### Example

A daily standard deviation of 1% gives `1% × √252 = 15.87%` a year.

### Interpretation

With a volatility of 15%, a year's return "typically" departs by 15 points from its average. The card also shows the volatility of the benchmark index over the same period.

### Limitations

- Volatility counts rises as well as falls: the Sortino ratio corrects this.
- The √252 rule assumes independent days; it underestimates risk when falls come in a row.
- It does not describe extreme losses: see the VaR, the CVaR and the max drawdown.

## The max drawdown (worst fall)
<!-- fiche: formule-max-drawdown | questions: what is the max drawdown ; how is the worst fall calculated ; drawdown formula ; maximum loss from a peak ; why does my drawdown not count my withdrawals ; date of the trough and recovery date ; peak not yet recovered what does it mean | mots: max drawdown, drawdown, maximum loss, peak, trough, recovery, base 100 | aller: Analyse du portefeuille/Performance | chiffres: max_drawdown -->

### The formula

```
drawdown(t) = index(t) / highest index up to t − 1      (always ≤ 0)
Max drawdown = the lowest of these values
```

The calculation is based on the **base-100 index** (the cumulative TWR), not on the portfolio value: otherwise a simple withdrawal of money would look like a loss, and a contribution would mask a real fall.

The software also gives the date of the peak, the date of the trough and the date on which the peak was regained ("peak not yet recovered" if that has not happened yet).

### Example

The index goes from 100 to 120, falls to 90, then rises to 110. Max drawdown: `90 / 120 − 1 = −25%`. The peak of 120 has not been regained.

### Interpretation

It is the worst loss that an investor who got in at the worst moment and out at the worst moment would have suffered. After a 25% fall, a 33% rise is needed to get back to the peak.

### Limitations

It depends on the period observed: a recent portfolio may not yet have been through a crisis. Stress tests complement this measure.

## The Sharpe ratio
<!-- fiche: formule-sharpe | questions: what is the sharpe ratio ; how is the sharpe calculated ; sharpe ratio formula ; my sharpe is negative is that bad ; what is a good sharpe ratio ; the sharpe changes when I change the risk-free rate ; return per unit of risk | mots: Sharpe ratio, Sharpe, excess return, risk-free rate, risk-adjusted return, risk premium | aller: Analyse du portefeuille/Risque | chiffres: sharpe, volatilite -->

The Sharpe ratio answers the question: was the risk taken well paid?

### The formula

```
daily risk-free rate rf_d = (1 + annual rate) ^ (1/252) − 1
excess(t) = r(t) − rf_d
Sharpe = mean(excess) × 252 / (standard deviation(excess) × √252)
```

The annual rate is the one set in [[Settings]] (2.50% by default).

### Example

Average daily return 0.05%, daily standard deviation 1%, risk-free rate 2.50% (i.e. 0.0098% a day):
`(0.05% − 0.0098%) × 252 / (1% × √252) ≈ 10.13% / 15.87% ≈ 0.64`.

### Interpretation

Benchmarks given by the code: negative, poor (worse than a risk-free investment); 0.5, acceptable; above 1, very good. The card also shows the index's Sharpe over the same period.

### Limitations

- Volatility also penalises rises (see the Sortino).
- The risk-free rate is constant over the whole period, whereas it has varied: over several years, the Sharpe is approximate.
- Over a short period, it is very unstable.

## The Sortino ratio
<!-- fiche: formule-sortino | questions: what is the sortino ratio ; difference between sharpe and sortino ; semi deviation formula ; why is sortino higher than sharpe ; ratio that only penalises falls ; how is the sortino calculated ; downside deviation | mots: Sortino ratio, semi-deviation, downside deviation, downside risk, Sharpe, risk-free rate | aller: Analyse du portefeuille/Risque | chiffres: sortino, sharpe -->

A criticism of the Sharpe: volatility counts big rises as risk. The Sortino only penalises the days below the risk-free rate.

### The formula

```
excess(t) = r(t) − rf_d
falls(t) = min(excess(t), 0)
semi-deviation = √( mean of falls² ) × √252
Sortino = mean(excess) × 252 / semi-deviation
```

The mean of squares is taken over **all** days: rising days count as 0. The rate `rf_d` is the same as for the Sharpe.

### Example

Average annual excess return of 8%, volatility of 16% and semi-deviation of 10%: Sharpe `8 / 16 = 0.50`, Sortino `8 / 10 = 0.80`.

### Interpretation

A Sortino clearly above the Sharpe indicates that the volatility comes mainly from rises. If they are close, rises and falls are of comparable size.

### Limitation

Like the Sharpe, it depends on the risk-free rate used and on the period.

## Beta
<!-- fiche: formule-beta | questions: what is beta ; how is the portfolio beta calculated ; beta above 1 what does it mean ; beta formula covariance variance ; is my portfolio riskier than the market ; sensitivity to the index ; beta against a bond index | mots: beta, sensitivity, covariance, variance, CAPM, systematic risk, benchmark index | aller: Analyse du portefeuille/Performance | chiffres: beta -->

### The formula

```
Beta = covariance(r_portfolio, r_index) / variance(r_index)
```

- Daily returns of the portfolio and of the benchmark index, on common days only.
- The index is aligned with the portfolio's calendar (last known price carried forward), then `r = price(t) / price(t−1) − 1`.
- Sample covariance and variance (division by n − 1).

### Example

Daily covariance of 0.00012 and daily index variance of 0.00010: `beta = 1.2`. When the index gains 1%, the portfolio gains 1.2% on average.

### Interpretation

- 1: the portfolio moves like the index;
- above 1: more sensitive, riskier than the market;
- below 1: more defensive.

Beta is also used in the hypothetical stress tests (equities fall by X% ≈ beta × X).

### Limitations

Beta measures sensitivity to an equity market: against a bond or money-market index, it has little meaning, and the Performance tab flags this. It depends on the index chosen in [[Benchmark index]].

## Jensen's alpha
<!-- fiche: formule-alpha | questions: what is alpha ; how is jensen's alpha calculated ; positive alpha what does it mean ; alpha capm formula ; my alpha is negative ; performance not explained by the market ; annual alpha | mots: alpha, Jensen's alpha, CAPM, outperformance, stock picking, abnormal return | aller: Analyse du portefeuille/Performance | chiffres: alpha, beta -->

### The formula

```
daily alpha = mean(r_p − rf_d) − beta × mean(r_i − rf_d)
Annual alpha = daily alpha × 252
```

`r_p` and `r_i` are the daily returns of the portfolio and of the index on common days, `rf_d` the daily risk-free rate `(1 + rate) ^ (1/252) − 1`.

### Example

Daily averages: portfolio 0.06%, index 0.04%, beta 1.2, risk-free rate 2.50%:
`[(0.06% − 0.0098%) − 1.2 × (0.04% − 0.0098%)] × 252 ≈ +3.5%` a year.

### Interpretation

Alpha is the performance that is **not** explained by exposure to the market (market model, CAPM). Positive: security selection, or a bias absent from the index, created value. Negative: the market risk taken was not rewarded.

### Limitations

- It depends on the index chosen: a poorly suited index (for example the CAC 40 excluding dividends) distorts alpha.
- It depends on the risk-free rate, assumed constant.
- Over a short period, it is mostly statistical noise.

## Tracking error
<!-- fiche: formule-tracking-error | questions: what is tracking error ; how is tracking error calculated ; tracking error formula ; high tracking error what does it mean ; does my portfolio stick to the index ; passive or active management ; tracking difference vs error | mots: tracking error, passive management, active management, volatility of the difference | aller: Analyse du portefeuille/Performance | chiffres: tracking_error -->

### The formula

```
gap(t) = r_portfolio(t) − r_index(t)
Tracking error = standard deviation(gap) × √252
```

Calculated on the days common to the portfolio and the index.

### Example

A daily gap with a standard deviation of 0.3% gives `0.3% × √252 ≈ 4.76%` a year.

### Interpretation

It is the volatility of the gap with the index. Benchmarks from the code:

- less than 2%: the portfolio "sticks" to the index (passive management);
- more than 5%: management very different from the index.

A high tracking error is neither good nor bad in itself: it measures how bold the management is. The information ratio says whether that boldness paid off.

### Limitations

It depends on the index chosen. A portfolio of European equities compared with the MSCI World will necessarily have a high tracking error.

## The information ratio
<!-- fiche: formule-ratio-information | questions: what is the information ratio ; information ratio formula ; how is the information ratio calculated ; what is a good information ratio ; negative information ratio ; has the gap with the index been paid for | mots: information ratio, tracking error, outperformance, active management, average gap | aller: Analyse du portefeuille/Performance -->

### The formula

```
Information ratio = mean(r_portfolio − r_index) × 252 / tracking error
```

It is the average annualised return gap, divided by the tracking error (see the previous fiche).

### Example

Average daily gap of 0.02% (i.e. 5.04% a year) and tracking error of 4.76%: `5.04 / 4.76 ≈ 1.06`.

### Interpretation

It is the equivalent of the Sharpe, but relative to the index: has the gap with the index been "paid for"? The code uses as a benchmark that a ratio above 0.5 is considered good. Negative: the portfolio did worse than the index.

### Do not confuse

The "Difference vs" the index card, at the top of the Performance tab, is the gap between the **compounded TWRs** over the same period (`portfolio TWR − index TWR`), whereas the information ratio uses the **arithmetic mean** of the daily gaps. The two may differ slightly.

### Limitation

Like the tracking error, it only makes sense with an index comparable to the portfolio.

## Historical VaR
<!-- fiche: formule-var-historique | questions: how is historical var calculated ; value at risk historical method ; what does var 95% 1 day mean ; what is var in euros ; loss on a bad day ; percentile of returns ; historical var formula | mots: VaR, value at risk, historical VaR, quantile, percentile, maximum loss, confidence level, 1 day | aller: Analyse du portefeuille/Risque | chiffres: var_historique, valeur_actuelle -->

### The formula

```
Historical VaR = − quantile(1 − level) of daily returns
VaR in euros = historical VaR × current portfolio value
```

The level is set at the top of the Risk tab, with [[VaR confidence level]]: 90, 95 (default) or 99%. The quantile is calculated by the pandas library, with linear interpolation between two observations. The result is a positive number: a loss.

### Example

Over 20 days, the five worst returns are −3.1%, −2.4%, −1.8%, −1.5% and −1.2%. The 5% quantile falls between the worst and the second-worst day: `−3.1% + 0.95 × 0.7% ≈ −2.44%`. 95% VaR = 2.44%. On €100,000, about €2,440.

### Interpretation

"On 95% of days, the loss does not exceed this amount." The 95% VaR is therefore exceeded about one trading day in twenty. This is the "VaR · 1 day" card in the Risk tab.

### Limitations

- No distribution assumption, but the past is assumed to repeat itself: a crisis absent from the history is invisible.
- It says nothing about the size of the loss beyond the threshold: that is the role of the CVaR.
- Over a short history, it relies on very few days.

## VaR under the normal distribution
<!-- fiche: formule-var-normale | questions: parametric var formula ; gaussian var ; how is normal distribution var calculated ; why 1.645 ; normal var underestimates crashes ; variance covariance var ; difference between historical var and normal var | mots: parametric VaR, Gaussian VaR, normal distribution, 1.645, quantile, standard deviation, mean, fat tails | aller: Analyse du portefeuille/Risque | chiffres: var_parametrique, var_historique -->

### The formula

```
Normal VaR = − (mean + z × standard deviation)
```

- `mean` and `standard deviation`: those of the daily returns;
- `z`: quantile of the standard normal distribution at the threshold `1 − level`: −1.282 at 90%, −1.645 at 95%, −2.326 at 99%.

### Example

Daily mean 0.05%, standard deviation 1.2%, level 95%: `−(0.05% − 1.645 × 1.2%) ≈ 1.92%`, i.e. about €1,924 on €100,000.

### Interpretation

It is the loss on a bad day if returns followed a normal distribution with the same mean and the same volatility. The table in the Risk tab displays it next to the historical VaR, the Cornish-Fisher VaR and the CVaR, as a percentage and in euros.

### Limitations

Real returns have "fat tails": large falls are more frequent than the normal distribution predicts. It therefore often **underestimates** crashes, especially at 99%. The Jarque-Bera test indicates whether the normal distribution is rejected for your portfolio; in that case, the automatic reading advises taking this VaR with caution.

## Cornish-Fisher VaR and its domain of validity
<!-- fiche: formule-var-cornish-fisher | questions: what is cornish fisher var ; cornish fisher formula ; why does cornish fisher show n/a ; var corrected for skewness and kurtosis ; why is cornish fisher var smaller than normal var ; cornish fisher validity domain ; priips var | mots: Cornish-Fisher, modified VaR, skewness, kurtosis, adjusted quantile, PRIIPs, n/a, validity | aller: Analyse du portefeuille/Risque | chiffres: var_cornish_fisher, asymetrie, kurtosis -->

The normal-distribution formula is kept, but the quantile `z` is corrected using the skewness `S` and the excess kurtosis `K` (Cornish-Fisher expansion).

### The formula

```
z_cf = z + (z² − 1)·S/6 + (z³ − 3z)·K/24 − (2z³ − 5z)·S²/36
Cornish-Fisher VaR = − (mean + z_cf × standard deviation)
```

### Example

Mean 0.05%, standard deviation 1.2%, `S = −0.5`, `K = 3`:

- at 95%: `z_cf ≈ −1.722` instead of −1.645, VaR 2.02% instead of 1.92%;
- at 99%: `z_cf ≈ −3.301` instead of −2.326, VaR 3.91% instead of 2.74%.

### Interpretation

Negative skewness always makes the VaR more cautious. The effect of fat tails depends on the level: at 99%, the VaR increases; at 95%, it can on the contrary fall slightly, because a fat-tailed distribution also has a more "peaked" centre. This is the method used for the regulatory PRIIPs risk indicator.

### Domain of validity

The correction only makes sense if it preserves the order of the quantiles. The software checks that the derivative `1 + z·S/3 + (3z² − 3)·K/24 − (6z² − 5)·S²/36` stays positive for `z` from −4 to +4 (in steps of 0.1). Otherwise, or with fewer than 4 days, the VaR is displayed as "n/a", with the note "Cornish-Fisher n/a: skewness or kurtosis too large, the adjustment is no longer reliable." Example: with no skewness, `K` must stay between about −0.5 and 8.

## The CVaR (Expected Shortfall)
<!-- fiche: formule-cvar | questions: what is cvar ; expected shortfall formula ; difference between var and cvar ; average loss beyond the var ; how is cvar calculated ; why is cvar bigger than var ; basel 3 measure | mots: CVaR, Expected Shortfall, ES, average loss, tail of the distribution, conditional VaR, Basel III | aller: Analyse du portefeuille/Risque | chiffres: cvar, var_historique -->

### The formula

```
CVaR = − mean of the daily returns r such that r ≤ − historical VaR
CVaR in euros = CVaR × current value
```

### Example

With the 20 days from the "Historical VaR" fiche (95% VaR of 2.44%), only one day is worse than −2.44%: −3.1%. CVaR = 3.1%. Over 1,000 days, it would be the average of roughly the 50 worst days.

### Interpretation

The VaR answers "how far does a bad day go?", the CVaR answers "and when things go badly, how badly do they go?". It is always at least equal to the historical VaR. It is the measure preferred by banking regulators (Basel III). "CVaR · Expected Shortfall" card in the Risk tab.

### Limitations

It relies on few days (5% of the history at 95%, 1% at 99%): over a short history, it is unstable. Like the historical VaR, it ignores crises absent from the period observed.

## Skewness
<!-- fiche: formule-asymetrie | questions: what is skewness ; skewness formula ; negative skewness what does it mean ; skewness coefficient of returns ; asymmetric distribution ; how is skewness calculated | mots: skewness, asymmetry, third moment, distribution, left tail, big falls | aller: Analyse du portefeuille/Risque | chiffres: asymetrie -->

### The formula

Skewness is calculated by the pandas library: bias-corrected sample coefficient (adjusted Fisher-Pearson coefficient).

```
d = r − mean(r) ;  m2 = mean(d²) ;  m3 = mean(d³)
S = [m3 / m2^(3/2)] × √(n(n − 1)) / (n − 2)
```

### Interpretation

- 0 for a normal (symmetrical) distribution;
- negative: big falls are more frequent or more violent than big rises (the usual case for equities);
- positive: big rises dominate.

The automatic reading in the Risk tab considers the distribution "roughly symmetrical" when `|S|` is below 0.3.

### Example

A series of small regular gains punctuated by a few sharp drops has negative skewness, even if its mean is positive.

### Limitations

A single extreme day can change the skewness considerably: it is unstable over a short history. At least 4 days are needed; otherwise it is 0 by convention.

Skewness is used for the Jarque-Bera test and for the Cornish-Fisher VaR.

## Excess kurtosis (fat tails)
<!-- fiche: formule-kurtosis | questions: what is kurtosis ; excess kurtosis formula ; what do fat tails mean ; positive kurtosis ; flatness ; leptokurtic ; days beyond 3 standard deviations | mots: kurtosis, excess kurtosis, flatness, fat tails, leptokurtic, fourth moment, extreme days | aller: Analyse du portefeuille/Risque | chiffres: kurtosis -->

### The formula

Calculated by pandas, directly as an **excess** (the normal distribution is 0), corrected for sample bias:

```
g2 = mean(d⁴) / mean(d²)² − 3
K = [(n + 1) × g2 + 6] × (n − 1) / [(n − 2)(n − 3)]
```

with `d = r − mean(r)`.

### Interpretation

- 0: as many extreme days as the normal distribution;
- positive: "fat tails", extreme days (in both directions) are more frequent than expected. The automatic reading speaks of clearly fat tails above 1.

### Extreme days

The Risk tab also counts the share of days more than 3 standard deviations from the mean, against 0.27% under the normal distribution (`2 × (1 − Φ(3))`). Example: 1.2% of extreme days observed is about 4.4 times more than the normal distribution.

### Limitations

Like skewness, it is very sensitive to a few days and unstable over a short history (minimum 4 days, otherwise 0). It is used for the Jarque-Bera test and for the Cornish-Fisher VaR.

## The Jarque-Bera test
<!-- fiche: formule-jarque-bera | questions: what is the jarque bera test ; normality rejected what does it mean ; jarque bera p value ; do my returns follow a normal distribution ; jarque bera formula ; why p below 0.001 ; normality test of returns | mots: Jarque-Bera, normality test, p-value, chi-squared, normal distribution, skewness, kurtosis, hypothesis | aller: Analyse du portefeuille/Risque | chiffres: asymetrie, kurtosis -->

### The formula

```
JB = n / 6 × (S² + K² / 4)
p-value = exp(−JB / 2)
```

`n` is the number of days, `S` the skewness, `K` the excess kurtosis. Under the hypothesis of normality, JB follows a chi-squared distribution with 2 degrees of freedom, whose exceedance probability is exactly `exp(−JB/2)`.

### Example

1,000 days, `S = −0.4`, `K = 2`: `JB = 1,000 / 6 × (0.16 + 1) ≈ 193.3`, p-value ≈ 10⁻⁴², displayed as "p = < 0.001".

### Interpretation

- p-value below 5%: "Normality rejected" badge. VaRs calculated with the normal distribution should then be taken with caution.
- Otherwise: "Normality not rejected". This is not proof of normality, only the absence of proof to the contrary.

Over several years of daily equity returns, normality is almost always rejected.

### Limitations

The test is asymptotic (reliable for a large number of days). Over a very long history, the slightest deviation is enough to reject normality, even if it has no practical consequence.

## Correlation between securities
<!-- fiche: formule-correlation | questions: how is correlation calculated ; correlation between two securities formula ; weighted average correlation ; blocks of correlated securities 0.7 threshold ; why does correlation rise in a crisis ; correlation matrix ; is a correlation of 0.8 a lot | mots: correlation, Pearson coefficient, correlation matrix, covariance, diversification, blocks, crisis correlation | aller: Analyse du portefeuille/Expositions -->

### The formula

Pearson coefficient of the daily returns `r = price(t) / price(t−1) − 1` of two securities, on their common days:

```
ρ(A, B) = covariance(r_A, r_B) / (standard deviation(r_A) × standard deviation(r_B))
```

### The derived measures (Exposures tab)

- **Weighted average correlation**: `Σ wᵢwⱼρᵢⱼ / Σ wᵢwⱼ`, over the pairs `i ≠ j`, with `w` the weight of each holding.
- **Independent blocks**: hierarchical clustering (distance `1 − ρ`, average linkage); securities correlated above 0.7 form a single block, and therefore a single "bet".
- **Days of sharp falls**: weighted average correlation calculated over the portfolio's worst 10% of days (at least 30 days).
- **Qualifiers**: very strong from 0.8, strong from 0.6, moderate from 0.3, weak below.

### Example

Annual covariance 0.018, volatilities 20% and 30%: `ρ = 0.018 / (0.20 × 0.30) = 0.30`, moderate correlation.

### Limitations

Correlation only measures a linear link and varies over time: it often rises during crises, when diversification would be most useful. Past correlations are not guaranteed in the future.

## The diversification ratio
<!-- fiche: formule-ratio-diversification | questions: what is the diversification ratio ; how is the diversification ratio calculated ; my diversification ratio is 1 ; is my portfolio really diversified ; effective number of bets ; real diversification formula | mots: diversification ratio, diversification, weighted volatility, effective number of bets, correlation, Choueifaty | aller: Analyse du portefeuille/Expositions -->

### The formula

```
Diversification ratio = Σ wᵢ × σᵢ / σ_p
σ_p = √(wᵀ Σ w)
```

`wᵢ` is the weight of each holding, `σᵢ` its volatility, `Σ` the covariance matrix of daily returns, `σ_p` the portfolio volatility.

### Example

Two holdings at 50%, with volatilities of 20% and 30%, correlated at 0.3: `σ_p ≈ 20.37%`, hence a ratio of `(0.5 × 20% + 0.5 × 30%) / 20.37% ≈ 1.23`.

### Interpretation

- 1: no diversification, the holdings move like a single asset;
- the higher it is, the more the holdings offset each other.

The ratio is the same whether daily or annualised covariances are used.

### The effective number of bets (Risk budget)

```
Effective number of bets = 1 / Σ (risk share of each holding)²
```

In the example, the risk shares are 34.9% and 65.1%: `1 / (0.349² + 0.651²) ≈ 1.83` bets, for 2 holdings.

### Limitations

It relies on past volatilities and correlations, which change, especially in a crisis.

## Holding weight and effective number of holdings
<!-- fiche: formule-poids | questions: how is the weight of a holding calculated ; weight as a percentage of the portfolio ; effective number of holdings ; herfindahl index ; 5 10 40 rule ; portfolio concentration formula ; equivalent to how many holdings of equal weight | mots: weight, weighting, allocation, concentration, Herfindahl, effective number, 5/10/40, UCITS | aller: Analyse du portefeuille/Positions | chiffres: nb_titres, valeur_actuelle -->

### The formulas

```
value of a holding = quantity × last price (in euros)
weight = value of the holding / total value of the holdings
effective number of holdings = 1 / Σ weight²
```

The effective number is the inverse of the Herfindahl index.

### Example

Four holdings weighing 40%, 30%, 20% and 10%: `1 / (0.16 + 0.09 + 0.04 + 0.01) ≈ 3.3`. The portfolio is equivalent to about 3 holdings of equal weight.

### Other concentration measures (Exposures tab)

- weight of the top 5 and top 10 holdings;
- the **5/10/40 rule** for UCITS funds: a holding at most 10%, and holdings above 5% at most 40% in total. It applies to directly held stocks: a diversified ETF is not a concentration.

### Interpretation

The alert thresholds on the largest stock depend on the profile chosen in [[Thresholds for profile]]: 5 and 10% for Cautious, 7 and 10% for Balanced, 10 and 15% for Dynamic (first threshold: caution, second: alert).

### Limitation

Weight says nothing about risk: a very volatile 10% holding can contribute 30% of the risk (see risk contributions).

## The PRU (unit cost basis)
<!-- fiche: formule-pru | questions: how is the pru calculated ; unit cost basis formula ; are fees included in the pru ; my pru does not change after a sale ; weighted average pru ; why is my pru different from my bank's ; pru after selling everything | mots: PRU, unit cost basis, average price, weighted average cost, purchase fees, amount invested | aller: Analyse du portefeuille/Positions | chiffres: montant_investi -->

The software replays all the transactions in date order, using the PRU method (weighted average cost basis) used in France.

### The rules

```
BUY: new PRU = (quantity held × PRU + q × price + fees) / (quantity held + q)
SELL: the PRU does not change
Everything sold: the PRU restarts from 0
Amount invested = quantity held × PRU
```

Purchase fees are included in the PRU: they increase the cost basis. Prices are converted into euros at the rate on the day of the transaction.

### Example

1. Purchase of 10 securities at €100 + €5 of fees: PRU `(1,000 + 5) / 10 = €100.50`.
2. Purchase of 10 securities at €120 + €5: PRU `(10 × 100.50 + 1,205) / 20 = €110.50`.
3. Sale of 5 securities: the PRU stays at €110.50; 15 securities remain, i.e. €1,657.50 invested.

### Why a difference with your bank?

- some banks exclude fees from the PRU;
- a foreign security is converted at the Yahoo Finance exchange rate, not at your bank's;
- a missing transaction (an old purchase, a stock split) changes the PRU.

## Unrealised gains, realised gains and total gain
<!-- fiche: formule-plus-values | questions: how is the capital gain calculated ; unrealised gain formula ; realised gain with fees ; what is the total gain ; gain on invested capital as a percentage ; are dividends in the gain ; difference between unrealised and realised | mots: unrealised gain, realised gain, loss, total gain, dividends, fees, performance in euros | aller: Analyse du portefeuille/Vue d'ensemble | chiffres: gain_total, dividendes, frais_totaux, montant_investi -->

### The formulas

```
Unrealised gain = quantity × (price − PRU) = value − amount invested
Unrealised gain in % = unrealised gain / amount invested
Realised gain (on each sale) = q × (selling price − PRU) − selling fees
Dividends = Σ (amount received − fees)
Total gain = unrealised gains + realised gains + dividends
```

Fees are already deducted: in the PRU for purchases, in the realised gain for sales. "Unrealised" means not cashed in: what a full sale would earn today, before selling fees and taxes.

### Example (continuing from the PRU fiche)

- sale of 5 securities at €130 with €4 of fees: `5 × (130 − 110.50) − 4 = €93.50` realised;
- 15 securities remaining, price €125: `15 × (125 − 110.50) = €217.50` unrealised;
- a dividend of €30 net of fees;
- total gain: `217.50 + 93.50 + 30 = €341`.

### The percentage "on invested capital"

The "Total gain" card displays `total gain / amount invested`, where the amount invested is the cost of **only the holdings still held** (here 341 / 1,657.50 ≈ 20.6%). It is neither a TWR nor an IRR.

### Cross-check

The day-by-day history also calculates `gain = value − net contributions`; on the last day, it must land exactly on the total gain, which the project's tests verify.

## The Markowitz efficient frontier
<!-- fiche: formule-frontiere-efficiente | questions: how is the efficient frontier calculated ; minimum variance portfolio ; maximum sharpe portfolio formula ; markowitz optimisation how does it work ; expected return and covariance matrix ; why a 30% maximum weight per security ; why is the frontier approximate | mots: Markowitz, efficient frontier, minimum variance, maximum Sharpe, tangency portfolio, covariance matrix, SLSQP, optimisation | aller: Analyse du portefeuille/Optimisation | chiffres: sharpe, volatilite -->

### The parameters

```
μ = mean of daily returns × 252        (expected return of each security)
Σ = covariance of daily returns × 252  (covariance matrix)
```

calculated on the days when **all** securities have a price.

### A portfolio with weights w

```
return = wᵀμ    volatility = √(wᵀΣw)    Sharpe = (return − risk-free rate) / volatility
```

### The optimisations

Constraints: each weight between 0 and the [[Maximum weight per security]] (30% by default), sum of weights = 100%. SLSQP method (SciPy library), starting from equal weights.

- **Minimum variance**: minimises `wᵀΣw`.
- **Maximum Sharpe**: maximises the Sharpe (the "tangency" portfolio).
- **Frontier**: 40 target returns, from the return of the minimum variance to the maximum achievable return; for each, the minimum variance. If fewer than two points succeed, the frontier is approximated by the envelope of 4,000 randomly drawn portfolios (Dirichlet distribution).

### Example

Security A (μ 6%, σ 20%), security B (μ 9%, σ 30%), correlation 0.3, no weight limit: minimum variance at 76.6% of A, volatility 18.67%; maximum Sharpe (rate 2.50%) at about 50/50, return 7.50%, volatility 20.36%, Sharpe 0.25.

### Allocations compared

`amount to buy (+) or sell (−) = (target weight − current weight) × total value`. A gap below 0.25 point is considered unchanged.

### Limitation

Expected returns are past averages: the optimiser over-exploits the securities that have done best.

## The Monte Carlo projection
<!-- fiche: formule-monte-carlo | questions: how does the monte carlo simulation work ; geometric brownian motion formula ; why minus sigma squared over 2 ; historical bootstrap method ; how is the probability of loss calculated ; why is the mean higher than the median ; log normal final value | mots: Monte Carlo, simulation, geometric Brownian motion, bootstrap, log-normal, percentiles, median, probability of loss | aller: Analyse du portefeuille/Projection | chiffres: valeur_actuelle, volatilite -->

### The parameters

By default, those of the portfolio: `μ = daily mean × 252`, `σ = daily standard deviation × √252`. They can be changed with the sliders.

### "Normal distribution" method (geometric Brownian motion)

The time step is the month (`dt = 1/12`):

```
monthly log-return ~ Normal( (μ − σ²/2) × dt , σ × √dt )
value(m + 1) = value(m) × exp(log-return) + monthly contribution
```

The `− σ²/2` term corrects the gap between arithmetic mean and compound growth: +50% then −50% gives a zero average, but a loss of 25%.

### "Historical (bootstrap)" method

Each month adds up 21 daily log-returns drawn at random, with replacement, from the portfolio's actual days, re-centred so that their mean matches the chosen return. The real fat tails are preserved.

### The results

5,000 scenarios (fixed seed, reproducible results); 5th, 25th, 50th, 75th and 95th percentiles; probability of loss = share of scenarios that end below `starting value + contributions`.

### Example

€100,000, μ 7%, σ 15%, 10 years, normal distribution: median ≈ €178,700 (theory: `100,000 × exp((0.07 − 0.01125) × 10) ≈ €179,900`), adverse scenario ≈ €81,900, favourable ≈ €389,600, mean ≈ €199,800, probability of loss ≈ 10.4%.

### Interpretation

The final value follows a log-normal distribution: the mean exceeds the median, which is the most representative marker. A projection is not a forecast.

## Risk contributions (Euler)
<!-- fiche: formule-contributions-risque | questions: how is the risk contribution calculated ; marginal risk contribution formula ; where does my portfolio's risk come from ; risk share higher than value share ; euler decomposition ; biggest risk contributor | mots: risk contribution, marginal contribution, Euler, risk budget, risk decomposition, risk share, volatility | aller: Gestion d'actifs/Budget de risque | chiffres: volatilite -->

A holding's weight does not say how much of the **risk** it contributes.

### The formulas

```
σ_p = √(wᵀΣw)
marginal contribution    MCᵢ = (Σw)ᵢ / σ_p
risk contribution        RCᵢ = wᵢ × MCᵢ
risk share               RCᵢ / σ_p      (the total is 100%)
```

Euler property: `Σ RCᵢ = σ_p`, verified by an automatic test. `Σ` is the annualised covariance matrix (daily returns × 252), estimated on the history.

### Example

Two holdings at 50% (volatilities 20% and 30%, correlation 0.3): `σ_p ≈ 20.37%`. Contributions: 7.12 and 13.25 points, i.e. **34.9%** and **65.1%** of the risk for 50% of the value each. The risk / weight ratio of the second holding is 1.30.

### Interpretation

A holding whose risk share exceeds its value share is more volatile or more correlated with the rest. The [[Risk budget]] tab shows the 20 largest contributors; the Exposures tab breaks these shares down by region.

### Risk parity

The "Risk parity" allocation looks for the weights for which each holding contributes the same share of the risk: it minimises `½ wᵀΣw − (1/n) × Σ ln(wᵢ)`, then scales the sum of weights to 100% (Spinu method). In the example, these are 60% and 40%: each holding then contributes 50% of the risk. It does not use expected returns.

## Brinson-Fachler performance attribution
<!-- fiche: formule-brinson-fachler | questions: how is performance attribution calculated ; allocation effect formula ; selection effect ; interaction effect ; brinson fachler model ; carino smoothing ; why does the sum of effects equal the gap ; which index for attribution | mots: performance attribution, Brinson-Fachler, allocation effect, selection effect, interaction effect, Cariño, MSCI ACWI IMI, regions | aller: Gestion d'actifs/Attribution de performance -->

The model explains, region by region, the gap between the equity portion and a global equity index.

### The formulas (over one period)

```
Allocation effect  = (wp − wb) × (rb − Rb)
Selection effect   = wb × (rp − rb)
Interaction effect = (wp − wb) × (rp − rb)
Rb = Σ wb × rb    Rp = Σ wp × rp
```

`wp`, `wb`: weight of the region in the portfolio and in the index; `rp`, `rb`: returns of the region. The sum of the three effects, all regions included, equals `Rp − Rb`.

### Example

United States: wp 70%, wb 60%, rp 12%, rb 10%. Europe: wp 30%, wb 40%, rp 3%, rb 5%. Rb = 8%, Rp = 9.3%.
Allocation: +0.2 + 0.3 = +0.5 point; selection: +1.2 − 0.8 = +0.4; interaction: +0.2 + 0.2 = +0.4. Total: +1.3 points = 9.3% − 8%.

### The implementation

- Calculated month by month, with the weights at the end of the previous month.
- Months linked by Cariño smoothing: each month is weighted by `kₜ / K`, with `k = [ln(1 + Rp) − ln(1 + Rb)] / (Rp − Rb)`, so that the sum lands exactly on the compounded gap.
- Index: regional weights of the MSCI ACWI IMI as at 30/06/2026 (United States 62.7%, emerging markets 12.3%, Europe 8.7%…, scaled back to 100%), and one equity index per region, converted into euros, excluding dividends.
- Bonds and gold excluded; a region absent from the index takes `rb = Rb`.

## Converting currencies into euros
<!-- fiche: formule-devises | questions: formula for converting into euros ; how are dollar prices converted ; eurusd rate number of dollars for one euro ; pence factor 0.01 ; rate on the purchase day or the current day ; are fees converted ; currency effect in performance | mots: conversion, currencies, exchange rate, EURUSD, pence, GBp, currency risk, euro | aller: Analyse du portefeuille/Positions -->

### The formula

```
price in euros = price in currency × factor / EURcurrency rate
```

- `EURUSD=X` (Yahoo Finance) is the number of dollars for 1 euro;
- factor = 0.01 for quotes in pence (`GBp`, London stocks), 1 otherwise.

### Which rate?

| Item | Rate used |
|---|---|
| purchase, sale, dividend | rate on the day of the transaction |
| day-by-day value | rate of each day |
| current value | last known rate |
| fees | none: always in euros |

A day without a rate takes the last known rate.

### Examples

- Apple at 200 USD, €1 = 1.10 USD: `200 / 1.10 = €181.82`.
- London stock at 1,250 pence, €1 = 0.85 GBP: `1,250 × 0.01 / 0.85 = €14.71`.

### What this implies

The performance of a foreign security combines its price and its currency: a US stock that gains 10% in dollars earns almost nothing in euros if the dollar loses about 10%. The rate is Yahoo Finance's, not your bank's. The day's rate appears at the bottom of the sidebar ("€1 in USD", for example).

## Duration and interest-rate shock
<!-- fiche: formule-duration | questions: how is the loss calculated if rates rise ; average duration formula ; interest rate sensitivity of bonds ; rate shock of 1 point ; why do my bonds fall when rates rise ; where is the duration of my bond fund | mots: duration, sensitivity, interest rate, rate shock, bonds, rate rise, approximation | aller: Analyse du portefeuille/Expositions -->

### The formulas

```
average duration = Σ (duration × value) / Σ value      (bond holdings whose duration is known)
loss if rates rise by 1 point ≈ Σ (duration × value) × 1%
as a % of the portfolio = loss / total value
```

First-order approximation: `price change ≈ − duration × change in rates`.

### Example

€20,000 of a bond fund with a duration of 7 years in a portfolio of €100,000: rates rise by 1 point, loss ≈ `7 × 1% × 20,000 = €1,400`, i.e. −1.4% of the portfolio.

### Where does the duration come from?

From the project's reference database (`data/referentiel.csv`), only for the bond funds that appear in it. Without a known duration, a holding is not included in the calculation.

### Interpretation

The longer the duration, the more the price falls when rates rise, and rises when they fall. The diagnostic thresholds depend on the profile: 5 and 8 years (Cautious), 7 and 10 years (Balanced), 8 and 12 years (Dynamic).

### Limitations

Linear approximation, valid for small shocks (convexity is ignored). After the fall, bonds offer a higher yield again.

## Stress tests: scenario formulas
<!-- fiche: formule-stress-tests | questions: how are the stress tests calculated ; equity shock formula beta times shock ; scenario dollar falls 10% ; how is the 2008 crisis replayed ; why does an index replace my security ; share estimated by an index ; loss in a crash | mots: stress test, scenario, crisis, shock, beta, proxy, duration, dollar, 2008, Covid | aller: Conseil patrimonial/Stress tests -->

### Historical scenarios

```
change in a holding = price at the low date / price at the high date − 1
change in the portfolio = Σ current weight × change in the holding
```

Five crises: 2008-2009, European debt (2011), Covid (2020), inflation and rate rises (2022), mini-crash of August 2024. If a security was not listed (first price more than 7 days after the start of the crisis), the index of its region, or a bond or gold fund of the same category, is used as an approximation. Changes in local currency, excluding dividends.

### Hypothetical scenarios

```
Equities fall by X%     : change ≈ beta × (−X%)       (X = 10, 20, 35)
Dollar falls by 10%     : change = −10% × share of holdings quoted in dollars
Rates rise by 1 point   : change = −1% × Σ weight × duration
```

### Example

Beta of 0.90 and equities falling by 20%: `0.90 × (−20%) = −18%`, i.e. −€18,000 on €100,000.

### Limitations

The current portfolio is assumed unchanged throughout the crisis; the currency effect is ignored in the historical scenarios; the "dollar" shock only looks at the quote currency, not the content of ETFs.

## Taxation on exit: CTO, PEA, life insurance
<!-- fiche: formule-fiscalite | questions: how is the tax calculated if I sell everything ; flat tax 31.4% ; pfu 2026 ; pea taxation after 5 years ; life insurance allowance 4600 ; tax formula capital gain securities account ; why are my dividends taxed despite a loss | mots: taxation, PFU, flat tax, social charges, PEA, life insurance, CTO, allowance, tax | aller: Conseil patrimonial/Fiscalité | chiffres: gain_total, dividendes -->

The software calculates the tax due if the whole portfolio were sold, under the 2026 rules (individual resident in France). Terms: CTO = compte-titres ordinaire (ordinary securities account); PEA = plan d'épargne en actions (French equity savings plan); assurance-vie = life insurance wrapper; PFU = prélèvement forfaitaire unique (flat tax).

### The formulas

| Wrapper | Base | Income tax | Social charges |
|---|---|---|---|
| CTO | `max(capital gains, 0) + max(dividends, 0)` | 12.8% | 18.6% |
| PEA, under 5 years | `max(gain, 0)` | 12.8% | 18.6% |
| PEA, 5 years and over | `max(gain, 0)` | 0 | 18.6% |
| Life insurance, under 8 years | `max(gain, 0)` | 12.8% | 17.2% |
| Life insurance, 8 years and over | `max(gain, 0)` | 7.5% × `max(gain − €4,600, 0)` (€9,200 for a couple) | 17.2% |

In a CTO, a loss is set against capital gains, not against dividends. Age is counted from the first transaction: `days / 365.25`.

### Example, gain of €10,000

- CTO: `31.4% × 10,000 = €3,140`;
- 6-year-old PEA: `18.6% × 10,000 = €1,860`;
- 9-year-old life insurance, single person: `7.5% × 5,400 + 17.2% × 10,000 = 405 + 1,720 = €2,125`.

### Simplifications

Option for the progressive income tax scale ignored, life insurance premiums assumed below €150,000, contract management fees ignored, dividends assumed to be kept within the wrapper. This is not an official tax calculation.
