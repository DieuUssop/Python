# Portfolio analysis
<!-- chapitre: analyse | ordre: 5 -->

This chapter explains, tab by tab, the "Portfolio analysis" workspace: the overview and the world map, holdings, performance, risk, exposures and real diversification, and then the viewing of transactions. Each indicator has its own entry: the exact formula used by the software, the intuition, a worked example, how to read it and its limits. The Optimisation and Projection tabs are covered in a separate chapter.

## The eight analysis tabs: what is where?
<!-- fiche: analyse-onglets | questions: what are the tabs in the portfolio analysis ; where do I find volatility ; which tab has the VaR ; where can I see my capital gains ; i am looking for the correlations ; where is the table of my holdings ; what is each tab for ; where are the transactions | mots: tabs, Overview, Holdings, Performance, Risk, Exposures, Optimisation, Projection, Transactions, navigation | aller: Analyse du portefeuille -->

The "Portfolio analysis" workspace has eight tabs, displayed at the top of the main area below the six key figures.

| Tab | What you find there |
|---|---|
| [[Overview]] | Change in value and invested capital over time, allocation by holding, world map, breakdowns by asset class, region and sector, gains, dividends and fees |
| [[Holdings]] | The table of positions held (quantity, cost basis (PRU), price, value, gain, weight) and the chart of unrealised gains by holding |
| [[Performance]] | TWR, IRR (TRI), gap versus the benchmark, base-100 curve, returns by calendar year, drawdown, beta, alpha, correlation, tracking error, information ratio |
| [[Risk]] | Sharpe, Sortino, VaR and CVaR, distribution of daily returns compared with the normal distribution, skewness, kurtosis, Jarque-Bera test |
| [[Exposures]] | Diagnosis across six dimensions (geography, sectors, currencies, concentration, interest rates, real diversification), findings and suggestions, correlations between holdings |
| [[Optimisation]] | Markowitz efficient frontier and compared allocations (chapter devoted to optimisation and projection) |
| [[Projection]] | Monte Carlo simulation of future value (same chapter) |
| [[Transactions]] | The transaction history, filterable and downloadable; editing transactions is described in the chapter on importing |

### Good to know

- All tabs analyse the same portfolio, with the benchmark index and the risk-free rate chosen in the **Settings** panel of the sidebar; the VaR level is set in the Risk tab.
- All amounts are expressed **in euros**, including for securities quoted in another currency.
- Correlations between holdings are not in the Risk tab: they are in the [[Exposures]] tab, [[Correlations]] sub-tab.

## What does the Overview tab show?
<!-- fiche: analyse-vue-ensemble | questions: what does the overview show ; what are the coloured rings for ; where do i see the breakdown by asset class ; why is the region breakdown a percentage of the equity portion ; what is the others slice in the pie chart ; where do i see the percentages of the rings ; the four cards at the bottom of the overview ; i dont see the sector ring ; allocation by holding chart | mots: overview, allocation, ring, pie chart, asset class, region, sector, equity portion, summary, donut | aller: Analyse du portefeuille/Vue d'ensemble | chiffres: valeur_actuelle, gain_total, dividendes, frais_totaux -->

The [[Overview]] tab gives a snapshot of the portfolio in four blocks, from top to bottom.

### 1. Change in value and allocation

- On the left, **Portfolio value over time**: market value and invested capital over time (see the dedicated entry).
- On the right, **Allocation**: one bar per holding, from largest to smallest, with its weight in the total value. Beyond 15 holdings, the smallest are grouped into a grey "Others" bar. Hovering shows the value in euros.

### 2. Presence around the world

The map colours each country according to its weight in the **equity portion** (dedicated entry). It only appears if the portfolio contains equities whose country is known.

### 3. Three rings

| Ring | Basis of calculation |
|---|---|
| By asset class | As a % of the **total value** (equities, bonds, gold, etc.) |
| By region | As a % of the **equity portion** only |
| By sector | As a % of the **equity portion** only |

The three rings are calculated **on a look-through basis**: an ETF is split between the countries and sectors of the index it tracks. They are all the same size; under each one, a legend gives every share with its percentage (one decimal place), from largest to smallest, and the centre of the ring shows the largest share. Hovering also gives the amount in euros.

Shares below 3% are grouped into "Other (n)", n being the number of groups combined; a single small share keeps its own name (there is never "Other (1)"). Each ring shows at most eight named shares. Asset classes always have the same colours throughout the software: equities in blue, bonds in green, gold in golden yellow, money market in light blue, as in the "Allocations compared" chart of the [[Optimisation]] tab. A ring that would contain only one group (for example a 100% equity portfolio for asset classes) is not displayed.

### 4. Four cards

| Card | Content |
|---|---|
| Unrealised gains | Gain or loss not yet cashed in on the holdings still held ("unrealised") |
| Realised gains | Gain or loss cashed in on sales ("realised") |
| Dividends and coupons | Total dividends and coupons entered, since inception |
| Brokerage fees | Total fees entered, since inception |

The sum of the first three cards gives the **total gain** shown at the top of the page.

## Reading the "Portfolio value over time" chart
<!-- fiche: analyse-evolution-valeur | questions: what does the orange line mean ; what are net contributions ; why is the orange line going down ; difference between value and money invested ; the blue area between the two lines ; my value is below the money invested am i losing ; why does the line move in steps ; negative money invested | mots: change in value, market value, net contributions, invested capital, money invested, curve, history, unrealised gain, chart | aller: Analyse du portefeuille/Vue d'ensemble | chiffres: valeur_actuelle, gain_total -->

This chart, at the top of the [[Overview]] tab, superimposes two curves, trading day by trading day.

| Curve | Calculation |
|---|---|
| **Portfolio value** (blue) | Σ quantity held that day × the day's closing price, in euros |
| **Money invested (net contributions)** (orange, stepped) | Cumulative sum of the money that came out of your pocket |

### How net contributions are calculated

Each transaction creates a cash flow:

- **purchase**: `+ (quantity × price + fees)`;
- **sale**: `− (quantity × price − fees)`;
- **dividend**: `− (amount − fees)`.

Net contributions are the sum of these flows since the start. A sale or a dividend therefore makes the orange line **go down**: that money has come back to you. If you have taken out more than you put in, the line can even fall below zero.

### Reading the gap between the two curves

The vertical gap, shaded light blue, is the **gain at that date**: `value − net contributions`. On the last day it matches the total gain in the key figures, give or take a small difference: the card uses the latest downloaded price, the curve uses the last closing price in the history. A blue curve below the orange curve means that at that date the portfolio was worth less than the net money contributed.

### Example

You buy €1,000 of securities (fees included), then receive €30 in dividends. Net contributions go to €1,000, then to €970. If the portfolio is worth €1,100, the gain is `1,100 − 970 = €130`.

### Tips

The 1M, 6M, YTD, 1Y and All buttons choose the period; hovering shows both values at the same date. A transaction entered on a day without trading (a Saturday, for example) is attached to the next trading day.

## The "Worldwide presence" map
<!-- fiche: analyse-carte-monde | questions: how do i read the world map ; why is the us dark when i have no american stocks ; the map doesnt show up ; my bonds are not on the map ; what does not on the map mean ; how do i see the securities of a country ; why isnt gold on the map ; geographic map of my portfolio | mots: world map, geography, country, equity portion, choropleth, not on the map, geographic exposure, world | aller: Analyse du portefeuille/Vue d'ensemble -->

The map in the [[Overview]] tab shows **where the companies are** whose shares you hold, directly or through ETFs.

### What is shown

- Each country is coloured according to its weight in the **equity portion** (not in the whole portfolio): the darker the blue, the heavier the country. The scale runs from 0 to the weight of the top country.
- Countries with no exposure are light grey.
- On hover: the percentage of the equity portion, the amount in euros, the number of securities involved and up to six of their names.

### Why the United States is often dark

An MSCI World ETF is split according to the composition of its index. For €10,000 invested, the software counts €7,294 in the United States, €591 in Japan, €341 in the United Kingdom, €329 in Canada, €224 in France, and so on. A portfolio with no directly held American shares can therefore be heavily exposed to the United States.

### What is not on the map

Bonds, gold and securities whose country is unknown ("Unclassified") are not shown. When they weigh more than 0.5% of the value, a note under the map gives their share, for example "Not on the map: Bonds 25%, Gold 5%".

### Limits

- The map is an approximation (next entry).
- It cannot be zoomed; hovering still works.
- It disappears if no equity has a recognised country.

## Why is the world map an approximation?
<!-- fiche: analyse-carte-approximation | questions: is the map accurate ; why is the country breakdown of my etf approximate ; where do the country weights come from ; my etf doesnt have exactly these countries ; are the map figures up to date ; what does approximation at 30/09/2026 mean ; does msci world really contain 73% us | mots: approximation, ETF composition, data as of 30/09/2026, MSCI factsheet, country weights, accuracy, look-through, update | aller: Analyse du portefeuille/Vue d'ensemble -->

The note under the map states: "ETFs split according to the composition of their index (approximation as of 30/09/2026)". This approximation has several causes, all visible in the code.

### 1. A typical composition per index, not that of your fund

The software does not read the actual holdings of your ETF. It recognises the **index tracked** (by the security's code, otherwise by words in its name such as "World", "S&P 500", "Emerging") and applies that index's composition.

### 2. Simplified sources

- MSCI World, ACWI, Emerging Markets and Europe: the top five countries and the sectors come from the MSCI factsheets as of 30/09/2026; the following countries are orders of magnitude, scaled to the "other countries" total in the factsheet.
- S&P 500, Nasdaq-100, Euro Stoxx 50, CAC 40, DAX and bond indices: 2025-2026 orders of magnitude.
- The MSCI ACWI is rebuilt by combining 88% MSCI World and 12% Emerging Markets.

### 3. An assumption about sectors

For an equity ETF, each country receives the **same sector mix** as the whole index. In reality, Japanese companies do not have the same sector breakdown as American ones.

### 4. Unrecognised ETFs

A fund whose index cannot be identified from either its code or its name keeps the country on its record; if that country is not a real country ("World", for example), it is counted as "Unclassified" and does not appear on the map.

### Is this a problem?

The weights of the major indices change little from one year to the next: the gap stays within a few points at most, which is enough to judge an exposure. For an exact figure, consult your ETF's monthly factsheet from its issuer.

## What does "look-through" mean?
<!-- fiche: analyse-transparence | questions: what does look-through mean ; what is look-through analysis ; why is my etf split into several countries ; look through ; my world etf is counted as a french stock ; why does the region breakdown differ from the holdings table ; how are etfs broken down | mots: look-through, transparency, ETF breakdown, composition, real exposure, ETF, tracked index, allocation | aller: Analyse du portefeuille/Expositions -->

An ETF is recorded as **a single security**: for example an MSCI World ETF listed in Paris, in euros. But it contains hundreds of shares from many countries. "Look-through" analysis looks **through** the fund to measure the true exposures.

### How the software proceeds

For each holding in the portfolio:

1. **Directly held share**: it keeps its country, its sector and its trading currency.
2. **ETF or equity fund**: its value is split between the countries of the tracked index, then, within each country, between the sectors of the index. The currency used is that of each country (dollar for the United States, yen for Japan, etc.), unless the fund's name indicates currency hedging ("Hedged", "couvert"), in which case everything is counted in euros.
3. **Bond fund**: split between the countries of the bond index; euro currency for a euro-zone index, dollar otherwise.
4. **Gold**: counted separately, with no country or sector, with "Gold" as its "currency".

### Example

A €10,000 MSCI World ETF becomes about €7,294 of American shares (in dollars), €591 of Japanese shares (in yen), €341 of British shares (in pounds), €224 of French shares (in euros), and so on.

### Where look-through is used

- the world map and the region and sector rings of the overview;
- the whole [[Exposures]] tab: geography, sectors, currencies, likely duplicates;
- the "Exposures and diversification" part of the PDF report.

By contrast, the table in the [[Holdings]] tab shows the classification **of the holding itself** (for example region "World" for a world ETF), without breaking it down. This is why its regions differ from those of the rings.

## Current value, invested capital and cost basis (PRU)
<!-- fiche: analyse-valeur-pru | questions: how is the pru calculated ; what is the average cost per share ; are fees included in the pru ; why is my pru different from my brokers ; does the pru change after a sale ; invested at pru what does it mean ; how is the current value calculated ; why did the amount invested drop after a sale | mots: PRU, cost basis, average cost, average price, cost price, amount invested, current value, purchase fees, weighted average | aller: Analyse du portefeuille/Positions | chiffres: valeur_actuelle, montant_investi -->

### Current value

`Value of a holding = quantity held × latest price (converted into euros)`

The current value is the sum of the values of the holdings still held. The latest price is the one downloaded from Yahoo Finance during the analysis, or the last stored price if the Internet is unavailable.

### The PRU (cost basis, "prix de revient unitaire")

The software replays all your transactions in date order, using the weighted average price method used in France.

- **Purchase**: `new PRU = (quantity held × old PRU + quantity bought × price + fees) / (quantity held + quantity bought)`. Purchase fees are **included** in the PRU.
- **Sale**: the PRU **does not change**. If you sell everything, it starts again from zero.
- **Dividend**: no effect on the PRU.

### Invested capital at cost (PRU)

`Amount invested = Σ quantity held × PRU`

This is the cost basis of the securities still in the portfolio. It appears under the Current value card ("Invested at average cost"). It falls after a sale, because the securities sold drop out of the calculation.

### Example

| Transaction | Calculation | PRU |
|---|---|---|
| Buy 10 shares at €100, €5 fees | `(10 × 100 + 5) / 10` | €100.50 |
| Buy 10 shares at €120, €5 fees | `(1,005 + 1,205) / 20` | €110.50 |
| Sell 5 shares at €130 | PRU unchanged | €110.50 |

15 shares remain: amount invested `15 × 110.50 = €1,657.50`. At a price of €125, the value is `15 × 125 = €1,875`.

### Limits

- If your broker calculates a PRU excluding fees, theirs will be lower.
- For a security in a foreign currency, the PRU is in euros, each purchase being converted at the exchange rate of its day (see the entry on securities in foreign currencies).

## Unrealised gains
<!-- fiche: analyse-plus-values-latentes | questions: what is an unrealised gain ; how is the percentage gain calculated ; why is my unrealised gain negative ; paper gain ; the gain / loss column ; the green and red gains chart ; does the gain take selling fees into account ; unrealised loss | mots: unrealised gain, unrealised loss, paper gain, gain / loss, latent gain, PRU, potential, gains chart | aller: Analyse du portefeuille/Positions | chiffres: gain_total, montant_investi -->

An **unrealised** gain is a gain that has not yet been cashed in: it is what you would gain (or lose) by selling today.

### Formulas

```
Unrealised gain   = value − amount invested = quantity × (price − PRU)
Unrealised gain % = unrealised gain / amount invested × 100
```

### Example

15 shares at a PRU of €110.50, current price €125: unrealised gain `15 × (125 − 110.50) = €217.50`, or `217.50 / 1,657.50 = +13.12%`.

### Where to see it

- **Unrealised gains** card in the [[Overview]] tab: the total, all holdings combined.
- "Gain / loss" and "Gain / loss %" columns of the table in the [[Holdings]] tab.
- **Unrealised gains by holding** chart in the [[Holdings]] tab: one bar per holding, green for a gain, red for a loss, sorted from the largest loss to the largest gain. Hovering gives the amount and the percentage.

### What it includes and does not include

- **Purchase fees** are already in it, since they are included in the PRU.
- **Fees on a future sale** are not deducted.
- **Taxes** are not deducted (the tax on a sale is simulated in the Wealth advisory workspace).
- For a security in a foreign currency, it includes the effect of the exchange rate.
- Dividends already received are not part of the unrealised gain: they are counted separately.

## Realised gains (and sold holdings)
<!-- fiche: analyse-plus-values-realisees | questions: what is a realised gain ; how is the gain on a sale calculated ; i sold a holding and it disappeared from the table ; where can i see the gain on a sold holding ; are my sales taken into account ; cashed in gain ; does a partial sale change the pru ; realised loss | mots: realised gain, realised loss, sale, cashed in, closed position, sold holding, PRU, disposal | aller: Analyse du portefeuille/Vue d'ensemble | chiffres: gain_total -->

A **realised** gain is the gain (or loss) cashed in on a sale.

### Formula

`Realised gain = quantity sold × (sale price − PRU) − selling fees`

The PRU used is the one at the time of the sale; it remains unchanged after a partial sale.

### Example

You hold 20 shares at a PRU of €110.50 and sell 5 at €130, with €4 in fees: `5 × (130 − 110.50) − 4 = €93.50`. You have 15 shares left, still at a PRU of €110.50.

### Where to see it

The **Realised gains** card ("realised") in the [[Overview]] tab adds up the gains and losses from all sales, since inception.

### A holding sold in full

A holding sold in full disappears from the table in the [[Holdings]] tab, which only shows securities still held. It is not forgotten, though:

- its realised gain and its dividends remain counted in the total gain;
- its history remains used for the value curve and the performance indicators;
- its transactions remain visible in the [[Transactions]] tab.

On the other hand, it no longer enters the allocations, exposures or correlations, which cover the holdings held today.

### Limit

The calculation follows the weighted average PRU method. It deducts no tax.

## Total gain: why is it not the same as unrealised gains alone?
<!-- fiche: analyse-gain-total | questions: how is the total gain calculated ; why is the total gain different from my capital gain ; does the total gain include dividends ; total gain higher than the sum of the gains in the table ; why is the total gain percentage odd after a sale ; gain on invested capital what is it ; my total gain is positive but my holdings are at a loss | mots: total gain, overall performance, unrealised gains, realised gains, dividends, return on invested capital, profit | aller: Analyse du portefeuille/Vue d'ensemble | chiffres: gain_total, montant_investi, dividendes -->

### The formula

`Total gain = unrealised gains + realised gains + dividends`

The total gain measures everything the portfolio has earned since the start. Unrealised gains are only a part of it: they ignore past sales and dividends received. Fees do not appear as a separate term: they are already deducted, in the PRU (purchase fees), in realised gains (selling fees) and in dividends (fees entered on the dividend line).

### Full example

| Item | Amount |
|---|---|
| Unrealised gains (15 shares, PRU €110.50, price €125) | +€217.50 |
| Realised gain (sale of 5 shares at €130) | +€93.50 |
| Dividends | +€30.00 |
| **Total gain** | **+€341.00** |

Check using cash flows: purchases `1,005 + 1,205 = €2,210`, net sale `650 − 4 = €646`, dividend €30. Net contributions: `2,210 − 646 − 30 = €1,534`. Value €1,875. Gain: `1,875 − 1,534 = €341`. Both methods give the same result.

### The "on invested capital" percentage

`Gain on invested capital = total gain / amount invested at PRU`

In the example: `341 / 1,657.50 = +20.57%`. Note: the denominator is the cost of the securities **still held**. After large sales it becomes small and the percentage can look very high. To measure the quality of your investments, prefer the TWR from the [[Performance]] tab.

### My holdings are at a loss, but the total gain is positive

This is possible: profitable past sales or dividends can offset unrealised losses.

## Dividends, coupons and fees: how are they counted?
<!-- fiche: analyse-dividendes-frais | questions: are dividends counted in the performance ; gross amounts received what does it mean ; are dividends net of tax ; where can i see my brokerage fees ; are fees deducted from performance ; dividend on a holding that was sold ; are bond coupons included ; why do my total fees look high | mots: dividends, coupons, distributions, brokerage fees, total fees, gross, net, withholding, performance, cost | aller: Analyse du portefeuille/Vue d'ensemble | chiffres: dividendes, frais_totaux, gain_total -->

### Dividends and coupons

- They are entered as DIVIDENDE (dividend) transactions, with the **total amount received** in the price.
- The **Dividends and coupons** card in the [[Overview]] tab adds up these amounts, less any fees entered on the same line. Its subtitle "Gross amounts received" means that the software deducts **no tax**: the figure is the one you entered.
- The "Dividends" column of the holdings table gives the total per holding still held.
- Dividends from a holding sold since then remain counted in the total.

They enter the performance in two ways: in the total gain, and in the TWR and IRR, where a dividend is a cash flow coming back to you. A distributing portfolio is therefore not at a disadvantage against an accumulating ETF.

### Brokerage fees

The **Brokerage fees** card ("Since inception") adds up the fees on all transactions: purchases, sales and dividends. They are always entered **in euros**, even for a security in dollars.

They are not deducted a second time: they are already taken into account in the PRU (purchases), in the realised gain (sales) and in the net amount of dividends. In daily returns, the fees on a purchase appear on the day of the transaction, since the money paid out (fees included) exceeds the value of the securities received.

### What is not counted

The software only knows what is in your transactions: custody fees, account-keeping fees, taxes and social contributions are not taken into account unless they are entered.

## Securities quoted in dollars or another currency: how are they valued?
<!-- fiche: analyse-titres-devises | questions: how are my dollar securities converted ; my performance in euros is different from the one in dollars ; which exchange rate is used ; my american stock went up but im losing money ; currency effect on my portfolio ; the pru of a dollar stock is in euros ; currency column of the holdings table ; currency risk | mots: currency, exchange rate, dollar, USD, conversion into euros, currency effect, currency risk, trading currency, EURUSD | aller: Analyse du portefeuille/Positions -->

All calculations are done **in euros**. A security quoted in another currency is converted as follows:

- each **transaction** is converted at the exchange rate of its day (last known rate at that date);
- each **historical price** is converted at the rate of the same day;
- the **current price** is converted at the day's rate; this rate appears in the information at the bottom of the sidebar (for example "€1 in USD").

`Price in euros = price in currency / rate (number of currency units for €1)`

London shares, quoted in pence, are first divided by 100. Fees remain in euros.

### Two effects in performance

The performance of a foreign security, seen in euros, combines the change in its price **and** that of its currency.

Example: you buy a share at USD 100 when €1 is worth USD 1.00, i.e. €100. A year later, it is quoted at USD 110 (+10%) but €1 is worth USD 1.10: it is worth `110 / 1.10 = €100`. In euros, the gain is nil.

### Where to see it

- "Currency" column of the [[Holdings]] tab: the trading currency. The PRU, price, value and gains are in euros.
- [[Transactions]] tab: the "Currency" and "Price in currency" columns show the price entered before conversion.
- [[Exposures]] tab, [[Currencies and rates]] sub-tab: the real currency exposure, ETFs included.

### Limit

The rate used is a daily market rate, not the one actually applied by your broker, which often adds a margin. The details of the conversion are explained in the chapter on sources and reliability.

## Why do my figures differ from my broker's?
<!-- fiche: analyse-ecart-courtier | questions: why are my figures different from my bank ; my broker doesnt show the same capital gain ; the pru is not the same as on my broker app ; valuation gap with my statement ; my portfolio value doesnt match my account ; my performance is different from my life insurance ; are the figures wrong | mots: gap, broker, bank, statement, difference, reconciliation, valuation, PRU, exchange rate, reliability | aller: Analyse du portefeuille/Positions | chiffres: valeur_actuelle, gain_total -->

A difference from your broker does not necessarily point to an error. Here are the most frequent causes, in the order in which to check them.

1. **A transaction is missing or entered incorrectly.** Compare the [[Transactions]] tab with your statements: quantity, price, fees, date. This is the most common cause.
2. **The PRU includes purchase fees.** If your broker shows a PRU excluding fees, theirs is lower and their gain higher.
3. **The price is not taken at the same moment.** The software uses the latest price downloaded during the analysis, kept in memory for one hour; your broker may show a more recent price or the previous evening's.
4. **The exchange rate differs.** The software converts at the day's market rate; your broker applied its own rate, with its margin.
5. **Dividends.** The software counts the amounts entered, without tax. A broker may show amounts net of withholding, or may not include them in the gain.
6. **The notion of performance.** The TWR neutralises your contributions; the return shown by a broker or an insurer is often a different calculation (gain relative to payments, return for the year, etc.).
7. **Fees not entered** (custody fees, account-keeping fees) are not known to the software.

### What to do

Correct the erroneous transactions in the [[Transactions]] tab (see the chapter on importing), then click [[Refresh prices]] to start again from the most recent prices.

## The holdings table, column by column
<!-- fiche: analyse-positions | questions: what do the columns of the holdings table mean ; how do i sort the holdings table ; what is the weight column ; the blue bar in the weight column ; why is the region of my etf world ; unclassified in the sector column ; is the price in euros or dollars ; table of my holdings | mots: holdings, table, columns, weight, PRU, price, quantity, ticker, class, sector, region, sorting | aller: Analyse du portefeuille/Positions | chiffres: nb_titres, valeur_actuelle -->

The [[Holdings]] tab shows one row per security **still held**, from the largest value to the smallest. Click a column header to sort.

| Column | Content |
|---|---|
| Ticker | The security's Yahoo Finance code |
| Security | The name |
| Asset class | Equities, Bonds, Gold, etc. (a security unknown to the reference file is classed as an equity) |
| Region, Sector | The classification of the holding itself, without ETF look-through; "Unclassified" if the security is not known |
| Currency | The trading currency; the amounts in the other columns are converted into euros |
| Quantity | The number of securities held |
| Avg. cost (PRU) | Cost basis per unit, purchase fees included, in euros |
| Price | The latest price, in euros |
| Value | Quantity × price |
| Gain / loss, Gain / loss % | Unrealised gain in euros and as a percentage of the amount invested |
| Weight | Share of the holding in the total value, with a proportional bar |
| Dividends | Dividends received on this holding since inception |

### The weight

`Weight = value of the holding / total value × 100`

The blue bar is at full length for the largest holding; the others are proportional. Example: a €15,000 holding in a €100,000 portfolio weighs 15.0%.

### The chart under the table

**Unrealised gains by holding**: one horizontal bar per security, green for a gain, red for a loss, in euros, at the last known price.

### Region and sector different from the overview?

The table classes a world ETF under the region "World"; the overview rings and the [[Exposures]] tab split it **on a look-through basis** between the countries of its index. Both are correct: they answer two different questions.

## What does the Performance tab contain?
<!-- fiche: analyse-onglet-performance | questions: what does the performance tab contain ; how do i know if im beating the index ; what is the base 100 chart for ; what does the warning about the bond index mean ; the five cards at the bottom of the performance tab ; how to read the performance tab ; where do i see my performance by year | mots: performance, TWR, IRR, TRI, benchmark index, base 100, annual return, drawdown, beta, alpha, comparison | aller: Analyse du portefeuille/Performance | chiffres: twr_total, twr_annualise, tri_annuel -->

The [[Performance]] tab answers two questions: how much have you earned, and have you done better than the benchmark index?

### From top to bottom

1. **Four cards**: Total TWR ("Since" + start date), Annualised TWR ("365-day basis"), Annual IRR ("Money-weighted return") and Difference vs the index (an "outperformance" or "underperformance" badge).
2. **Portfolio and index**: the two curves rebased to 100 at the first common date.
3. **Calendar-year returns**: the TWR for each year, portfolio and index side by side.
4. **Drawdown**: the fall from the last peak, with, in the subtitle, the dates of the peak, the trough and the return to the peak.
5. **Five cards** comparing with the index: Beta, Jensen's alpha, Correlation, Tracking error and Information ratio.

### The orange warning

If the index chosen in [[Benchmark index]] is a bond or money-market index, a box points out that beta, alpha and correlation measure sensitivity to an equity market: against such an index they have little meaning. In that case, mainly compare returns and volatilities.

### Suggested reading order

Start with the annualised TWR and the difference vs the index, look at the curve to see **when** the gap opened up, then the drawdown to measure the worst ordeal endured. The following entries detail each indicator.

## "Contribution-neutral" daily returns
<!-- fiche: analyse-rendements-quotidiens | questions: how are daily returns calculated ; why does a purchase not count as a gain ; what does neutralising contributions mean ; my deposit makes the line go up but not the performance ; why is the first day return negative ; basis of calculation of the indicators ; daily return | mots: daily return, cash flows, contributions, withdrawals, neutralisation, base 100, end of day | aller: Analyse du portefeuille/Performance -->

Almost all indicators (TWR, volatility, Sharpe, VaR, beta, etc.) rest on one series: the return of each trading day, **without the effect of your contributions and withdrawals**.

### The problem

If you buy €1,000 of securities today, the portfolio's value rises by €1,000, but you have gained nothing. The effect of that money must be removed.

### The software's formula

```
r(t) = (value(t) − flow(t)) / value(t−1) − 1
```

where `flow(t)` = money contributed that day (positive for a purchase, negative for a sale or a dividend). Transactions are assumed to be made **at the end of the day**, at the day's price: money contributed today has not yet "worked".

**First day** (or restart after selling everything): the previous day was worth 0, so the software compares the end-of-day value with the money contributed: `r = value(t) / flow(t) − 1`. This return captures purchase fees and the gap between the price paid and the closing price: it is often slightly negative.

Days when nothing was invested are not counted.

### Example

The portfolio was worth €10,000 last night. You buy €1,000 of securities today, and it is worth €11,150 tonight.
`r = (11,150 − 1,000) / 10,000 − 1 = +1.50%`.
Without neutralisation, you would have read +11.5%.

### The base-100 curve

Chaining these returns gives an index starting at 100: `index(t) = 100 × (1 + r1) × (1 + r2) × … × (1 + rt)`. It is the "pure performance" of your choices, comparable to a stock market index; the drawdown is calculated on it.

### Limit

Transactions are attached to a trading day and assumed to be made at the closing price. A purchase made during the session at a different price creates a small gap on the same day.

## The TWR (time-weighted return) and its annualisation
<!-- fiche: analyse-twr | questions: what is the twr ; how is annualised performance calculated ; time weighted return ; why is my annualised perf huge when i started 3 months ago ; total twr vs annualised twr what is the difference ; why 365 days and not 252 ; performance of my portfolio excluding deposits | mots: TWR, time-weighted return, performance, annualisation, 365 basis, GIPS, compound return | aller: Analyse du portefeuille/Performance | chiffres: twr_total, twr_annualise -->

### The total TWR

`TWR = (1 + r1) × (1 + r2) × … × (1 + rn) − 1`

where the `r` are the contribution-neutral daily returns. The TWR measures the **quality of investment choices**, independently of the timing and amount of your payments. It is the measure used by fund managers (GIPS standard): a manager does not decide when clients deposit money.

Example: +10% then −5% gives `1.10 × 0.95 − 1 = +4.50%`, not +5%.

### The annualised TWR

`Annualised TWR = (1 + total TWR) ^ (365 / number of days) − 1`

The number of days is calendar days, between the first and last day of the return series. Examples:

- +21% over 730 days: `1.21 ^ (1/2) − 1 = +10.00%` per year (not 10.5%: gains compound);
- +4.50% over 200 days: `1.045 ^ (365/200) − 1 = +8.36%` per year.

Why 365 and not 252? Return is annualised in **calendar** days; 252 trading days are used only to annualise volatility.

### Where to see it

"Total TWR" and "Annualised TWR" cards in the [[Performance]] tab; the annualised TWR is also the "Annualised return" card in the key figures.

### Limits

- **Short period**: annualisation amplifies everything. +5% over 91 days gives `1.05 ^ (365/91) − 1 ≈ +21.6%` per year, which does not mean the year will deliver +21.6%. Below one year, look at the total TWR instead.
- The TWR ignores your actual money: an excellent TWR on a small sum can coexist with a loss in euros if you invested heavily just before a fall. That is the role of the IRR.

## The IRR (internal rate of return)
<!-- fiche: analyse-tri | questions: what is the irr ; how is the internal rate of return calculated ; irr money weighted return ; return on the money invested ; why is my irr negative ; irr not available ; does the irr take the dates of my payments into account ; xirr like in excel | mots: IRR, TRI, internal rate of return, XIRR, money-weighted return, return on invested money, discounting, cash flows | aller: Analyse du portefeuille/Performance | chiffres: tri_annuel -->

The IRR (TRI in French) is the annual return **on your money**, as you experienced it, taking into account the dates and amounts of your payments.

### The formula

The IRR is the annual rate `i` that brings the present value of all cash flows to zero:

```
Σ CF_k / (1 + i) ^ (days_k / 365) = 0
```

From the investor's point of view:

- a purchase is money **leaving** your pocket: negative flow (fees included);
- a sale or a dividend is money **coming in**: positive flow;
- on the last day, the software acts as if you sold everything: `+ final value`.

`days_k` is the number of days between the first flow and flow k; flows on the same day are added together.

### The calculation

There is no direct formula. The software searches for `i` by **bisection** between −99% and +1,000% per year, halving the interval 200 times. If there is no solution in this interval, the IRR is not calculated. It is the same principle as the XIRR function of a spreadsheet.

### Example

You invest €1,000 on 02/01/2023; a year later it is worth €1,200 and you add €10,000. The following year, the portfolio falls by 10% and is worth €10,080 on 01/01/2025.
Flows: −€1,000 (day 0), −€10,000 (day 365), +€10,080 (day 730). The IRR is **−7.72% per year**: you lost money, because the largest sum suffered the fall.

### Where to see it

"Annual IRR" card in the [[Performance]] tab.

### Limits

The IRR depends on your payment schedule: it cannot be used to judge a manager or to compare yourself with an index. Over a very short period, it can take extreme values.

## Why are the TWR and the IRR different?
<!-- fiche: analyse-twr-tri | questions: why are the twr and irr different ; positive twr and negative irr is that possible ; which figure should i trust twr or irr ; my performance is good but i lost money ; difference between time-weighted and money-weighted return ; which one to compare with the index ; irr higher than twr why | mots: TWR, IRR, TRI, difference, time-weighted, money-weighted, timing of contributions, comparison, payments | aller: Analyse du portefeuille/Performance | chiffres: twr_annualise, tri_annuel -->

The two indicators answer two different questions.

| | TWR | IRR |
|---|---|---|
| Question | Were my investment choices good? | How much has my money earned? |
| Effect of payments | Neutralised | Taken into account (amounts and dates) |
| Used for | Comparing with an index or a fund | Measuring your personal result |

### Example: positive TWR, negative IRR

- Year 1: €1,000 invested, +20%: it is worth €1,200.
- Start of year 2: you add €10,000. The portfolio is worth €11,200.
- Year 2: −10%: it is worth €10,080.

**TWR**: `1.20 × 0.90 − 1 = +8.00%` over two years. Your investments, on average, worked well.
**IRR**: −7.72% per year. You contributed €11,000 and €10,080 remains: the bad year hit the large payment, the good year benefited only the small one.

### Reading the gap

- **IRR > TWR**: you invested more before the rising periods (good timing, or luck).
- **IRR < TWR**: you invested more before the falls.
- **IRR ≈ TWR**: few payments, or regular payments without a marked timing effect.

Note: the IRR is already annual, whereas the TWR exists in total and annualised versions. Compare the IRR with the **annualised TWR**.

### Which one to believe?

Both are correct. To compare yourself with the index, use the TWR, as the "Difference vs" the index card does. To know what your savings have really earned, look at the IRR and the total gain.

## Comparing your portfolio with the index (base 100 and gap)
<!-- fiche: analyse-comparaison-indice | questions: how do i know if im beating the market ; portfolio vs index chart ; what is base 100 ; how is the gap with msci world calculated ; outperformance or underperformance ; the two curves dont start on the same day ; the gap with the index doesnt match the difference of the annualised twrs | mots: comparison, benchmark index, benchmark, base 100, outperformance, underperformance, gap, MSCI World, curve | aller: Analyse du portefeuille/Performance | chiffres: twr_total -->

### The "Portfolio and index" chart

Two curves start at 100 on the **first common date**: "My portfolio" (blue) and the chosen index (grey). A dotted line marks the level 100. If your curve ends at 130 and the index's at 125, your portfolio made +30% and the index +25% over the period.

The portfolio curve chains the contribution-neutral daily returns: your payments do not make it jump. The 1M, 6M, YTD, 1Y and All buttons choose the period displayed, but both curves stay rebased to 100 at the start of the history.

### The "Difference vs" the index card

`Gap = portfolio TWR − index TWR, over the same period`

Both TWRs are **total** (not annualised) and calculated only on the days when both returns exist. The very first day of investment, which has no corresponding index return, is excluded: the TWR used may therefore differ slightly from the total TWR displayed next to it. The badge shows "outperformance" if the gap is positive or zero, "underperformance" otherwise.

Example: portfolio +30.0%, index +25.0%: gap **+5.00%**.

### A fair comparison

- Choose an index that resembles the portfolio (a blended index for an equity and bond portfolio).
- "Price-only" indices (CAC 40, Euro Stoxx 50) put the index at a disadvantage, since your dividends are counted.
- The index is converted into euros, like the portfolio.

### Limit

A gap over a short period is often due to chance. Also look at calendar-year returns and the information ratio.

## Calendar-year returns
<!-- fiche: analyse-rendements-annuels | questions: performance by year ; return of my portfolio in 2025 ; why is the first year low ; is the current year complete ; compare each year with the index ; bar chart of the years ; annual performance | mots: annual return, calendar year, performance by year, YTD, bars, annual comparison, calendar | aller: Analyse du portefeuille/Performance -->

The **Calendar-year returns** chart in the [[Performance]] tab shows, for each year, the portfolio's TWR (blue bars, "My portfolio") and the index's (grey bars).

### The calculation

Daily returns are grouped by calendar year, then compounded:

`Return for the year = Π (1 + r_day) − 1, over the days of the year`

Example: a year with a first half at +6% and a second half at −2% gives `1.06 × 0.98 − 1 = +3.88%`.

### Good to know

- The **first year** only starts at your first investment: it is partial.
- The **current year** runs from 1 January to the last price date: it is a year-to-date return, not a full year.
- The bars are not annualised.
- Hovering gives the return to two decimal places.

### How to read it

Steady outperformance, year after year, is more convincing than a single excellent year. A year very different from the index in either direction signals a portfolio far from its reference: the tracking error confirms it.

## Max drawdown (worst fall)
<!-- fiche: analyse-drawdown | questions: what is the max drawdown ; worst fall of my portfolio ; peak not yet recovered what does it mean ; how do i read the red drawdown chart ; how long to recover ; maximum loss from a peak ; is drawdown calculated on value or on performance | mots: drawdown, max drawdown, maximum loss, fall from a peak, trough, peak, recovery | aller: Analyse du portefeuille/Performance | chiffres: max_drawdown -->

The drawdown measures, each day, the fall from the highest level reached so far. The max drawdown is the worst of these falls.

### Formulas

```
drawdown(t) = index(t) / peak of the index up to t − 1   (always ≤ 0)
max drawdown = the smallest drawdown over the period
```

The calculation is done on the **base-100 curve** (contribution-neutral performance), not on the value in euros: otherwise a withdrawal would look like a loss, and a contribution would mask a genuine fall.

### Example

The curve goes through 100, 120, 90, 110, then 130. The peak before the fall is 120; the trough is 90. Max drawdown: `90 / 120 − 1 = −25.00%`. The peak is recovered when the curve returns to 120 or more: here, at the 130 point (110 is not enough).

### Reading the chart

In the [[Performance]] tab, the red area shows the drawdown day by day; a dot marks the lowest point, labelled "Max drawdown". The subtitle gives the date of the peak, that of the trough, then "recovered on" and the date of the return to the peak, or "peak not yet recovered". The "Max drawdown" card in the key figures shows the date of the trough.

### Interpretation

It is the most telling risk indicator: "at the worst moment, I would have lost 25% from the peak". A 25% fall needs a rise of `1 / 0.75 − 1 = 33.3%` to be wiped out.

### Limits

It depends on the period observed: a two-year history may not have seen any real crisis. It does not tell you how many times or for how long you were in a decline.

## Beta and correlation with the index
<!-- fiche: analyse-beta | questions: what is beta ; my beta is 1.2 what does that mean ; beta below 1 ; how is beta calculated ; correlation with the index what is it ; is my portfolio defensive ; negative beta possible ; sensitivity to the market | mots: beta, market sensitivity, correlation, CAPM, MEDAF, systematic risk, defensive, aggressive | aller: Analyse du portefeuille/Performance | chiffres: beta -->

### Beta

`Beta = covariance(portfolio returns, index returns) / variance(index returns)`

It is calculated on the daily returns of the days common to the portfolio and the index.

**Intuition**: when the index makes +1%, the portfolio makes on average `beta × 1%`.

| Beta | Reading |
|---|---|
| 1 | The portfolio moves like the index ("1 = same as the index") |
| 1.2 | It amplifies movements: +1.2% when the index makes +1%, and vice versa on the downside |
| 0.8 | More defensive than the index |
| Close to 0 | Little linked to the index |

**Example**: over five days, the index makes +1%, −1%, +2%, −2%, 0% and the portfolio +1.2%, −1.1%, +2.5%, −2.4%, +0.1%. Covariance 0.0003025, index variance 0.00025: beta = `0.0003025 / 0.00025 = 1.21`.

### Correlation

The "Correlation" card ("With" the index) measures, between −1 and +1, how far the two move **in the same direction**, regardless of magnitude. A correlation of 0.95 means the index explains almost all of the portfolio's movements; 0.5, that a large part of its movements is its own.

`Beta = correlation × portfolio volatility / index volatility`

Example: correlation 0.9, volatility 18% against 15% for the index: beta `0.9 × 18 / 15 = 1.08`.

### Limits

- Beta only makes sense against an index that resembles the portfolio; with a bond or money-market index, a warning is displayed.
- With a low correlation, beta explains little.
- It is estimated on the past and changes over time.

## Jensen's alpha
<!-- fiche: analyse-alpha | questions: what is alpha ; jensens alpha how to calculate ; my alpha is negative is that bad ; positive alpha means i beat the market ; difference between alpha and gap with the index ; value created by stock picking ; capm alpha | mots: alpha, Jensen's alpha, CAPM, MEDAF, risk-adjusted outperformance, stock selection, excess return | aller: Analyse du portefeuille/Performance | chiffres: alpha, beta -->

Alpha measures the performance that is **not explained** by exposure to the market (CAPM model).

### The software's formula

```
daily alpha  = mean(r_portfolio − rf) − beta × mean(r_index − rf)
annual alpha = daily alpha × 252
```

`rf` is the daily risk-free rate: `(1 + annual rate) ^ (1/252) − 1`, about 0.0098% per day with 2.50% per year. The means are arithmetic, over the days common to the portfolio and the index.

### Intuition

A portfolio with a beta of 1.1 "should" make 1.1 times the index's excess return. Alpha is what it made on top (or fell short).

### Example

Portfolio's average annualised excess return: 8%; the index's: 6%; beta: 1.1.
`Alpha = 8% − 1.1 × 6% = +1.40%` per year.

### Reading

- **Alpha > 0** (green "annual" badge): your choices created value beyond the market risk taken.
- **Alpha < 0**: for the same market risk, the index did better.

Alpha differs from the gap with the index: a portfolio with a beta of 1.3 that beats the index in a rising market can have a zero alpha, because it only took more risk.

### Limits

- The risk-free rate is assumed constant over the whole period.
- Over less than two or three years, alpha is very unstable.
- It only makes sense against an equity index comparable to the portfolio.

## Tracking error and information ratio
<!-- fiche: analyse-tracking-error | questions: what is tracking error ; does my portfolio stick to the index ; what is the information ratio ; how to calculate tracking error ; passive or active management ; is a tracking error of 5% a lot ; a good information ratio ; tracking difference | mots: tracking error, information ratio, active management, passive management, relative risk, deviation from the index | aller: Analyse du portefeuille/Performance | chiffres: tracking_error -->

### Tracking error

`Tracking error = standard deviation(r_portfolio − r_index) × √252`

It is the volatility of the daily return **gap** with the index, scaled to the year ("Tracking error" card, "Annualised").

| Tracking error | Reading |
|---|---|
| Less than 2% | The portfolio sticks to the index (passive management) |
| More than 5% | Management very different from the index |

### Information ratio

`Information ratio = mean(r_portfolio − r_index) × 252 / tracking error`

It answers the question: has the gap with the index been "paid for"? It is the equivalent of the Sharpe ratio, but relative to the index. A ratio above 0.5 is considered good.

### Example

Average daily gap of 0.004% and standard deviation of the gap of 0.30%:

- tracking error: `0.30% × √252 = 4.76%`;
- information ratio: `0.004% × 252 / 4.76% = 1.008% / 4.76% = 0.21`.

The portfolio departs markedly from the index, but that gap has earned little.

### Good to know

The mean used by the information ratio is **arithmetic** (daily mean × 252). It therefore does not exactly match the "Difference vs" the index card, which compares compounded, non-annualised TWRs.

### Limits

Same reservations as for beta: choose a comparable index, and beware of short periods.

## What does the Risk tab contain?
<!-- fiche: analyse-onglet-risque | questions: what does the risk tab contain ; how do i read the risk tab ; where is the var ; where did the correlations go ; what does n/a mean in the var table ; what is the loss on a bad day table for ; the sentences under the distribution chart | mots: risk, VaR, CVaR, Sharpe, Sortino, distribution, skewness, kurtosis, Jarque-Bera, loss on a bad day | aller: Analyse du portefeuille/Risque | chiffres: sharpe, sortino, var_historique, cvar -->

The [[Risk]] tab measures the risk taken and the shape of bad days.

### At the top: four cards

| Card | Line below |
|---|---|
| Sharpe ratio | Sharpe of the benchmark index |
| Sortino ratio | "Only penalises downside moves" |
| VaR (chosen level) · 1 day, in euros | The same VaR in %, "historical method" |
| CVaR · Expected Shortfall, in euros | The CVaR in %, "beyond the VaR" |

### In the centre: the distribution of daily returns

- On the left, the histogram of daily returns, the normal distribution curve and the VaR lines (dedicated entry). The subtitle gives the number of days used.
- On the right, four cards: Skewness, Excess kurtosis, Days beyond 3 standard deviations and Jarque-Bera test; then the **Loss on a bad day** table, with the historical VaR, the normal VaR, the Cornish-Fisher VaR and the CVaR, in % and in euros.
- "n/a" (not available) means the Cornish-Fisher VaR was not calculated because skewness or kurtosis are too extreme: a note explains this under the table.

### At the bottom: the automatic reading

A few sentences interpret the distribution: skewness, fat tails, the result of the Jarque-Bera test and a comparison of the historical and normal VaRs. A final note reminds you that correlations and diversification are in the [[Exposures]] tab.

### The setting that matters

The level of the VaRs and the CVaR is set at the top right of this tab, with the [[VaR confidence level]] selector (90, 95 or 99%).

## Volatility
<!-- fiche: analyse-volatilite | questions: what is volatility ; how is annualised volatility calculated ; why square root of 252 ; my volatility is 15% is that a lot ; index volatility under the card ; standard deviation of returns ; is my portfolio risky | mots: volatility, standard deviation, risk, √252, annualisation, dispersion, variability | aller: Analyse du portefeuille/Risque | chiffres: volatilite -->

### The formula

`Annual volatility = standard deviation of daily returns × √252`

The standard deviation is the sample one (division by n − 1), calculated on the contribution-neutral daily returns.

### Why √252

There are 252 trading days in a year. If daily returns are independent, their variances add up: `annual variance = 252 × daily variance`, so `annual standard deviation = √252 × daily standard deviation`.

### Example

A daily standard deviation of 1.00% gives `1% × √252 = 1% × 15.87 = 15.87%` per year.

### Interpretation

With a volatility of 15%, a year's return "typically" deviates by ± 15% from its mean. The most useful thing is the comparison with the benchmark index, whose volatility is shown under the Volatility card in the key figures.

### Limits

- Volatility counts rises as risk, just like falls (the Sortino ratio corrects this flaw).
- The √252 rule assumes returns are independent from one day to the next.
- It describes usual deviations, not crashes: for extreme losses, look at the VaR, the CVaR and the max drawdown.

## The Sharpe ratio
<!-- fiche: analyse-sharpe | questions: what is the sharpe ratio ; what does the sharpe ratio mean ; what is a good sharpe ; my sharpe is negative ; how is sharpe calculated ; why does my sharpe change when i change the risk-free rate ; index sharpe under the card ; return per unit of risk | mots: Sharpe, Sharpe ratio, risk-adjusted return, risk-free rate, excess return, volatility, reward to variability | aller: Analyse du portefeuille/Risque | chiffres: sharpe, volatilite -->

The Sharpe ratio answers the question: **was the risk taken well rewarded?**

### The software's formula

```
daily excess = r_day − rf_day,   with rf_day = (1 + risk-free rate) ^ (1/252) − 1
Sharpe = mean(excess) × 252 / (standard deviation(excess) × √252)
```

The return is the **arithmetic** mean of the daily returns, annualised by 252; it is not the annualised TWR. The risk-free rate is the one in the **Settings** panel (2.50% by default).

### Example

Average daily return of 0.040%, daily standard deviation of 1.00%, risk-free rate of 2.50% (i.e. 0.0098% per day):

- annualised excess: `(0.040% − 0.0098%) × 252 = 7.61%`;
- volatility: `1% × √252 = 15.87%`;
- Sharpe: `7.61 / 15.87 = 0.48`.

### Orders of magnitude

| Sharpe | Reading |
|---|---|
| Less than 0 | The portfolio did worse than a risk-free investment |
| Around 0.5 | Decent |
| More than 1 | Very good |

Above all, compare with the index's Sharpe, shown under the card.

### Limits

- It penalises large rises as much as large falls (see the Sortino).
- It assumes a constant risk-free rate over the whole period.
- Over a short period, it varies a lot; a rise in the risk-free rate lowers it.

## The Sortino ratio
<!-- fiche: analyse-sortino | questions: what is the sortino ratio ; difference between sharpe and sortino ; why is my sortino higher than my sharpe ; what is semi deviation ; ratio that only penalises falls ; how is sortino calculated ; downside deviation | mots: Sortino, semi-deviation, downside deviation, downside risk, Sharpe, adjusted return, negative volatility | aller: Analyse du portefeuille/Risque | chiffres: sortino, sharpe -->

The Sortino ratio is a Sharpe that **only penalises falls**: an investor does not complain about large rises.

### The software's formula

```
excess = r_day − rf_day
semi-deviation = √( mean( min(excess, 0)² ) ) × √252
Sortino = mean(excess) × 252 / semi-deviation
```

Days above the risk-free rate are replaced by 0, then the mean of the squares is taken over **all** days.

### Example (risk-free rate at 0% for simplicity)

Six days: +1.2%, −2.0%, +0.6%, −0.8%, +1.5%, +0.3%.

- mean: 0.1333% per day, i.e. `33.60%` annualised;
- volatility: 20.91%, so Sharpe = `33.60 / 20.91 = 1.61`;
- semi-deviation: `√((0.020² + 0.008²) / 6) = 0.879%` per day, i.e. `13.96%` annualised;
- Sortino: `33.60 / 13.96 = 2.41`.

The Sortino is higher than the Sharpe: part of the volatility came from rises.

### Reading

- Sortino clearly above the Sharpe: the portfolio's swings are mostly rises.
- Sortino close to the Sharpe: falls and rises are of comparable size.

### Limits

With few down days, the semi-deviation rests on few observations and the ratio becomes unstable. It also inherits the limits of the Sharpe (constant risk-free rate, period observed).

## Historical VaR (and VaR in euros)
<!-- fiche: analyse-var-historique | questions: what is the var ; how does historical value at risk work ; what does var 95% 1 day mean ; how much can i lose in a day ; how is var in euros calculated ; is the var a maximum loss ; why did my var change ; 99% var | mots: VaR, value at risk, historical VaR, loss on a bad day, quantile, percentile, confidence level, loss risk | aller: Analyse du portefeuille/Risque | chiffres: var_historique, valeur_actuelle -->

The VaR (Value at Risk) answers: **how much can I lose on a bad day?**

### The formula

`Historical VaR = − quantile of daily returns at the threshold (1 − level)`

At 95%, it is the 5th percentile of past returns, with the sign changed so that it reads as a loss. No assumption is made about the shape of the distribution: the software takes the actual days.

`VaR in euros = historical VaR × current portfolio value`

### Example

Over 1,000 days, the 5th percentile lies between the 50th and 51st worst day. If it is −1.60%, the 95% historical VaR is 1.60%. For a €100,000 portfolio, the card shows **€1,600**.

Reading: "on 95% of days, the loss does not exceed €1,600"; in other words, about one trading day in twenty, roughly once a month, the loss is larger.

### Where to see it

- "VaR (level) · 1 day" card in the [[Risk]] tab: the amount in euros, and the badge in % "historical method".
- "Historical VaR" row of the **Loss on a bad day** table.
- Dashed orange line on the distribution chart.

### What the VaR is not

It is **not** a maximum loss: it says where the zone of bad days begins, not how far it extends. For that, look at the CVaR.

### Limits

- It assumes the past repeats itself: a calm history gives a low VaR.
- At 99%, it rests on 1% of days, which is very few observations over a short history.
- It is a **one-day** VaR, calculated on the current value.

## The "normal distribution" (parametric) VaR
<!-- fiche: analyse-var-normale | questions: what is parametric var ; gaussian var ; how is normal distribution var calculated ; why 1.645 ; difference between historical var and normal var ; does the normal distribution underestimate crashes ; variance covariance var | mots: parametric VaR, Gaussian VaR, normal distribution, 1.645, quantile, standard deviation, mean, variance-covariance | aller: Analyse du portefeuille/Risque | chiffres: var_parametrique, var_historique -->

### The formula

`Normal VaR = −(mean of daily returns + z × standard deviation)`

where `z` is the quantile of the normal distribution at the threshold `1 − level`:

| Level | z |
|---|---|
| 90% | −1.2816 |
| 95% | −1.6449 |
| 99% | −2.3263 |

### Intuition

We assume daily returns follow a normal distribution (a "bell curve") with the same mean and standard deviation as yours, and read the loss at the desired threshold.

### Example

Daily mean 0.04%, standard deviation 1.00%:

- at 95%: `−(0.04% − 1.6449 × 1%) = 1.60%`;
- at 99%: `−(0.04% − 2.3263 × 1%) = 2.29%`;
- at 90%: `1.24%`.

### Reading

It is the simplest method, and it can be calculated even with little data. But real returns have **fat tails**: large falls are more frequent than the normal distribution predicts. At 99%, the normal VaR therefore often underestimates the risk.

The software automatically compares the two methods: if the historical VaR exceeds the normal VaR by more than 5%, the reading under the chart says so ("the normal distribution underestimates the loss on a bad day here").

### Limits

- The normality assumption is almost always rejected by the Jarque-Bera test on market data.
- The Cornish-Fisher VaR partly corrects this flaw.

## The Cornish-Fisher VaR and its domain of validity
<!-- fiche: analyse-var-cornish-fisher | questions: what is the cornish fisher var ; why is the cornish fisher var n/a ; var corrected for skewness and kurtosis ; skewness or kurtosis too high the correction is no longer reliable ; cornish fisher lower than normal var why ; modified var ; priips method | mots: Cornish-Fisher, modified VaR, adjusted VaR, skewness, kurtosis, PRIIPs, n/a, domain of validity, adjusted quantile | aller: Analyse du portefeuille/Risque | chiffres: var_cornish_fisher, asymetrie, kurtosis -->

The Cornish-Fisher VaR keeps the normal distribution formula, but **corrects the quantile z** using the skewness S and the excess kurtosis K of the returns.

### The formula

```
z_cf = z + (z² − 1) × S/6 + (z³ − 3z) × K/24 − (2z³ − 5z) × S²/36
Cornish-Fisher VaR = −(mean + z_cf × standard deviation)
```

This is the method used for the regulatory risk indicator of investment products (PRIIPs).

### Examples (mean 0.04%, standard deviation 1%)

| Level | S | K | z_cf | Cornish-Fisher VaR | Normal VaR |
|---|---|---|---|---|---|
| 95% | −0.5 | 3 | −1.7217 | 1.68% | 1.60% |
| 95% | 0 | 3 | −1.5843 | 1.54% | 1.60% |
| 99% | −0.5 | 3 | −3.3013 | 3.26% | 2.29% |
| 99% | 0 | 3 | −3.0277 | 2.99% | 2.29% |

### Reading

- A **negative skewness** always makes the VaR more cautious.
- **Fat tails** (K > 0) increase the 99% VaR, but may lower it slightly at 95%: a fat-tailed distribution also has a more peaked centre, with more calm days.

### The domain of validity: why "n/a"

The correction only makes sense if it respects the order of the quantiles: the smaller z is, the smaller z_cf must be. The software checks that the derivative of z_cf stays strictly positive for z from −4 to +4, in steps of 0.1:

`derivative = 1 + z × S/3 + (3z² − 3) × K/24 − (6z² − 5) × S²/36`

If this is not the case, the VaR is not calculated: the table shows "n/a", the purple line disappears from the chart, and a note states "skewness or kurtosis too high, the correction is no longer reliable". The VaR is also not calculated with fewer than four returns.

Examples of valid pairs (checked on a grid of K in steps of 0.1):

| Skewness S | Valid excess kurtosis K |
|---|---|
| 0 | from 0 to 7.9 |
| −0.5 | from 0.2 to 8.2 |
| −1 | from 1.6 to 8.8 |
| −2 | from 6.6 to 11.2 |

A strong skewness with tails that are too **thin** is therefore also outside the domain.

### Limit

It is an approximation: with a distribution very far from the normal distribution, prefer the historical VaR and the CVaR.

## The CVaR (Expected Shortfall)
<!-- fiche: analyse-cvar | questions: what is the cvar ; expected shortfall ; difference between var and cvar ; average loss beyond the var ; when things go badly how bad is it ; cvar in euros ; why is the cvar bigger than the var ; conditional value at risk | mots: CVaR, Expected Shortfall, ES, average loss, tail of the distribution, beyond the VaR, Basel III, extreme risk | aller: Analyse du portefeuille/Risque | chiffres: cvar, var_historique -->

The CVaR (Conditional Value at Risk), or Expected Shortfall, answers: **and when things go badly, how badly?**

### The formula

`CVaR = − mean of daily returns less than or equal to −historical VaR`

It is the **average** loss on the days when the historical VaR is reached or exceeded.

`CVaR in euros = CVaR × current value`

### Example (twenty days, for illustration)

Ranked returns: −3.1%, −2.2%, −1.5%, −1.2%, … , +2.0%.

- The 95% historical VaR is interpolated between the two worst days: `−(−3.1% + 0.95 × 0.9%) = 2.245%`.
- Only one day is below −2.245%: −3.1%. The CVaR is therefore **3.10%**.

On a real history of 1,000 days, the 95% CVaR is the average of about 50 days.

### Where to see it

- "CVaR · Expected Shortfall" card in the [[Risk]] tab, in euros, with the badge in % "beyond the VaR".
- "CVaR (Expected Shortfall)" row of the table and the solid red line on the chart.

### Reading

The CVaR is always at least equal to the historical VaR. A large gap between the two signals a fat distribution tail: bad days are rare but violent. It is the measure favoured by banking regulators (Basel III), because it looks beyond the threshold.

### Limits

It rests on few days, especially at 99%: over a year of data (about 252 days), the 99% CVaR is the average of two or three days.

## Three different VaRs: which one to believe?
<!-- fiche: analyse-trois-var | questions: why three different vars ; which var should i use ; historical var lower than normal var ; the vars disagree ; which is the right var ; comparison of var methods ; loss on a bad day table | mots: VaR, comparison, historical VaR, normal VaR, Cornish-Fisher, CVaR, methods, choice of method, loss on a bad day | aller: Analyse du portefeuille/Risque | chiffres: var_historique, var_parametrique, var_cornish_fisher, cvar -->

The **Loss on a bad day** table in the [[Risk]] tab shows three VaRs and the CVaR, in % and in euros. They answer the same question under three assumptions.

| Method | Assumption | Strength | Weakness |
|---|---|---|---|
| Historical VaR | The past repeats itself | No assumption about shape | Depends on the period observed |
| Normal VaR | Bell-shaped returns | Simple, stable | Underestimates crashes |
| Cornish-Fisher VaR | Bell curve corrected for skewness and kurtosis | Takes the real shape into account | Approximation, sometimes "n/a" |
| CVaR | The past repeats itself | Measures the severity of bad days | Rests on few days |

### What the automatic reading says

Under the chart, a sentence compares the historical VaR and the normal VaR:

- historical **more than 5% higher**: the normal distribution underestimates the loss on a bad day here;
- historical **more than 5% lower**: extreme losses are concentrated on a few days, which the CVaR measures better;
- otherwise: the two are close.

### How to decide

1. Look at the Jarque-Bera test: if normality is rejected, treat the normal VaR with caution.
2. Take the **higher** of the historical and Cornish-Fisher VaRs as a cautious order of magnitude.
3. Complete with the CVaR to see how far bad days go, and with the max drawdown for a fall over several days.

No VaR is a maximum loss. All are one-day estimates, drawn from the portfolio's history.

## Reading the return distribution chart
<!-- fiche: analyse-distribution | questions: how do i read the distribution chart ; what is the black curve ; what do the vertical lines correspond to ; histogram of daily returns ; var legend orange purple red ; why are there bars far to the left ; compare my returns with the normal distribution ; a var line disappeared from the chart | mots: distribution, histogram, normal distribution, bell curve, fat tails, VaR lines, legend, daily returns, Gaussian | aller: Analyse du portefeuille/Risque | chiffres: asymetrie, kurtosis -->

The **Distribution of daily returns** chart in the [[Risk]] tab compares your actual days with what a normal distribution would predict.

### The blue bars: "Observed days"

Each bar counts the number of days whose return falls in a class. All classes have the same width; their number is `√n × 1.2`, bounded between 20 and 80 (n = number of days). Example: 1,000 days give 37 classes. Hovering shows "Return …" and the number of days.

### The dark curve: "Normal distribution (same mean and volatility)"

It is the bell that would be obtained if your returns followed a normal distribution with the **same mean and standard deviation**. It is scaled to the bars:

`expected days = normal density × number of days × class width`

Hovering gives the number of expected days.

### The vertical lines

Each is placed at `−VaR` (loss side) and appears in the legend above the chart.

| Line | Style |
|---|---|
| Historical VaR (level) | Orange, dashed |
| Normal VaR (level) | Dark grey, dotted |
| Cornish-Fisher VaR (level) | Purple, dash-dot |
| CVaR (Expected Shortfall) | Red, solid line |

A missing line corresponds to a value that was not calculated (Cornish-Fisher VaR "n/a"). Clicking a legend name hides or shows the line.

### What to look at

- **The centre**: bars that exceed the bell around zero indicate more calm days than expected.
- **The extremes**: isolated bars far to the left, where the bell is almost zero, are the crashes the normal distribution does not predict ("fat tails").
- **The gap between the lines**: an orange line to the left of the grey line means the historical VaR exceeds the normal VaR.

The sentences under the chart summarise these observations.

## Skewness
<!-- fiche: analyse-asymetrie | questions: what is skewness ; negative skewness what does it mean ; my skewness is -0.5 is that bad ; asymmetric distribution ; large falls are more frequent than large rises ; skewness 0 for a normal distribution ; skewness coefficient | mots: skewness, asymmetry, skewness coefficient, distribution, left tail, large falls, normal distribution, third moment | aller: Analyse du portefeuille/Risque | chiffres: asymetrie -->

Skewness measures whether the distribution of daily returns leans to one side.

### The calculation

The software uses the sample skewness coefficient, bias-corrected (third moment of the deviations from the mean, divided by the cube of the standard deviation). It is **0 for a normal distribution**.

### Reading (thresholds of the automatic reading)

| Skewness | Sentence displayed |
|---|---|
| Below −0.3 | Large falls are more frequent or more violent than large rises |
| Between −0.3 and +0.3 | The distribution is roughly symmetric |
| Above +0.3 | Large rises outweigh large falls |

### Example

An equity portfolio often shows a negative skewness, for example −0.5: markets rise in small steps and fall in jolts. At 95%, with an excess kurtosis of 3, the Cornish-Fisher VaR then goes from 1.54% (zero skewness) to 1.68% (skewness −0.5), for a mean of 0.04% and a standard deviation of 1%.

### Why it matters

A negative skewness means the risk is concentrated on the bad side: volatility and the normal VaR, which assume a symmetric distribution, then underestimate losses.

### Limits

Skewness is very sensitive to a few extreme days: a single crash in the history can tip it. It needs a long history to be reliable.

## Excess kurtosis and extreme days
<!-- fiche: analyse-kurtosis | questions: what is kurtosis ; what does excess kurtosis mean ; what are fat tails ; days beyond 3 standard deviations ; why 0.27% under the normal distribution ; fat tails ; peakedness ; my kurtosis is 5 | mots: kurtosis, excess kurtosis, peakedness, fat tails, leptokurtic, extreme days, 3 standard deviations, fourth moment | aller: Analyse du portefeuille/Risque | chiffres: kurtosis -->

### Excess kurtosis

It measures the thickness of the distribution's tails: the frequency of extreme days, in both directions. The software calculates the sample **excess** kurtosis, bias-corrected: it is **0 for a normal distribution**.

| Excess kurtosis | Automatic reading sentence |
|---|---|
| Above 1 | "Fat tails", with the number of extreme days observed and expected |
| Between 0 and 1 | Tails slightly fatter than the normal distribution |
| 0 or less | No more extreme days than the normal distribution predicts |

### Days beyond 3 standard deviations

`Share of extreme days = share of days where |return − mean| > 3 × standard deviation`

Under the normal distribution, this share is `2 × (1 − Φ(3)) = 0.27%`, about one day in 370. The "Days beyond 3 standard deviations" card compares the observed share with this theoretical figure.

### Example

Over 1,000 days, the normal distribution predicts 2 to 3 extreme days. If you observe 12 (1.20%), there are about 4.4 times more than predicted: the automatic reading says so ("×4.4").

### Why it matters

Financial markets almost always have a positive kurtosis. Volatility and the normal VaR describe ordinary days well, but underestimate crashes: at 99%, prefer the historical VaR, the Cornish-Fisher VaR and the CVaR.

### Limits

Like skewness, kurtosis is dominated by a few days. A short history without a crisis can show a low kurtosis that guarantees nothing.

## The Jarque-Bera test
<!-- fiche: analyse-jarque-bera | questions: what is the jarque bera test ; normality rejected what does it mean ; jarque bera p-value ; how do i read p < 0.001 ; do my returns follow a normal distribution ; normality test ; why is normality always rejected | mots: Jarque-Bera, normality test, p-value, normal distribution, chi-squared, normality rejected, JB statistic, hypothesis | aller: Analyse du portefeuille/Risque | chiffres: asymetrie, kurtosis -->

The Jarque-Bera test checks whether your daily returns can reasonably follow a normal distribution.

### The formula

```
JB = n / 6 × (S² + K² / 4)
p-value = exp(−JB / 2)
```

with n the number of days, S the skewness and K the excess kurtosis. Under the normality hypothesis, JB follows a chi-squared distribution with 2 degrees of freedom, whose exceedance probability is exactly `exp(−JB/2)`.

### Reading

The "Jarque-Bera test" card shows "p = " followed by the p-value ("< 0.001" when it is tiny), with a badge:

- **p < 0.05**: red "Normality rejected" badge. VaRs based on the normal distribution should be treated with caution.
- **p ≥ 0.05**: green "Normality not rejected" badge. This does not prove the distribution is normal: the data simply do not allow it to be ruled out.

### Examples

- 1,000 days, S = −0.5, K = 3: `JB = 1,000 / 6 × (0.25 + 2.25) = 416.7`; p-value almost zero, displayed "< 0.001": normality rejected.
- 250 days, S = −0.1, K = 0.3: `JB = 250 / 6 × (0.01 + 0.0225) = 1.35`; `p = exp(−0.677) = 0.508`: normality not rejected.

### Why normality is almost always rejected

With many days, the slightest departure in skewness or kurtosis becomes significant. On several years of market data, rejection is the rule: this is precisely why the software offers the historical VaR and the Cornish-Fisher VaR.

### Limit

With fewer than four returns, the test is not calculated (p-value set to 1).

## What does the Exposures tab contain?
<!-- fiche: analyse-onglet-expositions | questions: what does the exposures tab contain ; how do i read the green orange red badges ; what does not applicable mean ; what are the geography currencies concentration correlations sub-tabs for ; where do i see my points of attention ; findings and suggestions what is that ; is my portfolio well diversified | mots: exposures, diversification, summary, findings, suggestions, badges, geography, sectors, currencies, concentration, rates, correlations | aller: Analyse du portefeuille/Expositions -->

The [[Exposures]] tab answers two questions: what is the portfolio **really** exposed to, and is it **truly** diversified? Everything in it is calculated on a look-through basis.

### 1. The header and the profile

The title "Exposures and diversification" is a reminder that ETFs are split according to their index (approximation as of 30/09/2026). On the right, the [[Thresholds for profile]] menu chooses the diagnosis thresholds: Cautious, Balanced (default) or Dynamic.

### 2. The summary: six boxes

| Dimension | Figure shown under the badge |
|---|---|
| Geography | Top country of the equity portion and its weight |
| Sectors | Top sector of the equity portion and its weight |
| Currencies | Share outside the euro |
| Concentration | Weight of the largest holding |
| Interest rates | Average duration, or "No bonds" |
| Real diversification | Average correlation between holdings |

The badge gives the most serious finding for the dimension: green "Good", orange "To monitor", red "To fix", or grey "Not applicable" (for example, the Interest rates dimension with no bonds).

### 3. Findings and suggestions

Orange and red points are listed from most to least serious. Each finding gives the observed figure, the associated risk and suggestions. Green points are placed in a "Strengths" panel, open by default if there is no point of attention.

### 4. Four detail sub-tabs

- [[Geography and sectors]]: regions and sectors compared with the index, main differences by country, share of value and share of risk by region;
- [[Currencies and rates]]: real currency exposure, interest-rate sensitivity;
- [[Concentration]]: number of holdings, weight of the largest ones, 5/10/40 rule;
- [[Correlations]]: matrix, blocks, pairs, holdings that diversify.

## Is the exposures diagnosis advice?
<!-- fiche: analyse-diagnostic | questions: is the diagnosis investment advice ; should i follow the suggestions ; how are the findings produced ; why does the software tell me to diversify ; to fix does that mean i have to sell ; are the suggestions personalised ; what is the diagnosis based on | mots: diagnosis, finding, suggestions, investment advice, rules, thresholds, educational, recommendation, disclaimer | aller: Analyse du portefeuille/Expositions -->

**No.** As the note in the [[Exposures]] tab says, it is an "educational analysis based on simple rules and past data: it does not constitute investment advice".

### How the findings are produced

The software applies fixed rules, written in advance, to the portfolio's figures: weight of a country compared with the world market (MSCI ACWI), weight of a sector, share outside the euro, weight of a share, duration, correlations. Each rule has a threshold; depending on the observed value, it produces a green, orange or red finding, accompanied by a sentence on the risk and general suggestions. The thresholds are detailed in the following entries.

### What the diagnosis does not know

- your personal situation: wealth outside this portfolio, income, horizon, objectives, taxation;
- your reasons: an overweight may be a deliberate choice;
- the future: correlations and compositions are drawn from the past and from index factsheets.

### How to use it

Read each finding as a question to ask yourself: "is this bias intended?". The suggestions illustrate common solutions (world ETF, currency hedging, shorter duration, etc.), without taking your constraints into account. Before any decision, especially a sale that would trigger tax, consult a qualified professional.

### The PDF report

The "Exposures and diversification" part of the report reuses this diagnosis with the **Balanced** profile thresholds, whatever the profile chosen on screen.

## Thresholds by profile: Cautious, Balanced, Dynamic
<!-- fiche: analyse-seuils-profil | questions: what is the profile choice in exposures for ; what are the cautious balanced dynamic thresholds ; why does a finding turn red in cautious profile ; what does changing profile change ; diagnosis alert thresholds ; is my profile saved ; concentration threshold by profile | mots: profile, Cautious, Balanced, Dynamic, thresholds, alert, diagnosis, risk tolerance, settings | aller: Analyse du portefeuille/Expositions -->

The [[Thresholds for profile]] menu, at the top of the [[Exposures]] tab, sets the severity of the diagnosis. It changes no calculation: only the colour of the findings.

### Thresholds that depend on the profile

For each rule, the first value turns it orange ("To monitor"), the second red ("To fix"); you must **exceed** it.

| Rule | Cautious | Balanced | Dynamic |
|---|---|---|---|
| Share of portfolio outside the euro | 30% / 50% | 50% / 70% | 70% / 85% |
| Emerging countries in the equity portion | 10% / 20% | 20% / 30% | 25% / 40% |
| Largest directly held share | 5% / 10% | 7% / 10% | 10% / 15% |
| Average duration of bonds | 5 / 8 years | 7 / 10 years | 8 / 12 years |

### Rules identical for all profiles

Geography (excluding emerging markets), sectors, the 5/10/40 rule, likely duplicates and correlations have the same thresholds whatever the profile (see the corresponding entries).

### Example

A €100,000 portfolio: a €60,000 MSCI World ETF and four French shares (LVMH €15,000, TotalEnergies €10,000, Airbus €8,000, Sanofi €7,000). Share outside the euro: 55% (of which 44% in dollars, via the ETF). Largest share: LVMH, 15%.

| Profile | Currencies (55%) | LVMH (15%) |
|---|---|---|
| Cautious | To fix (> 50%) | To fix (> 10%) |
| Balanced | To monitor (> 50%) | To fix (> 10%) |
| Dynamic | Good (≤ 70%) | To monitor (> 10%) |

### How long the choice lasts

The profile is kept for the session; it is not saved in your account. The PDF report always uses the Balanced profile.

## Geography and sectors: the rules and the gaps to the index
<!-- fiche: analyse-geographie-secteurs | questions: why is france in red ; what is home bias ; how is the gap with the world market calculated ; few defensive sectors what does it mean ; is my portfolio too concentrated in technology ; compare my regions with the index ; share of value and share of risk by region ; main differences by country | mots: geography, country, region, sectors, home bias, emerging, defensive sectors, overweight, underweight, MSCI ACWI, gaps | aller: Analyse du portefeuille/Expositions -->

### The geography rules (equity portion)

They apply if equities weigh more than 5% of the portfolio. The top three countries are compared with their weight in the **MSCI ACWI** (world market):

- **To fix**: a country exceeds its world weight by more than 25 points, or a country other than the United States weighs more than 40%;
- **To monitor**: it exceeds it by more than 15 points;
- **Home bias** (to monitor): France weighs more than 15% **and** more than four times its world weight (about 2%);
- **Emerging countries**: thresholds depend on the profile.

### The sector rules (equity portion)

They apply under the same conditions. For the top three sectors: to fix above 40% or 15 points above the world market; to monitor above 30% or 8 points. A "few defensive sectors" finding appears if healthcare, consumer staples and utilities total less than 10%.

### Example

MSCI World ETF €60,000, LVMH €15,000, TotalEnergies €10,000, Airbus €8,000, Sanofi €7,000. On a look-through basis, France weighs 41% of the equity portion (against 2% in the world market): red finding, because a country other than the United States exceeds 40%, and an orange home-bias finding. Consumer discretionary weighs 20% against 8% worldwide (+12 points): to monitor.

### The [[Geography and sectors]] sub-tab

- **Regions (equity allocation)** and **Sectors (equity allocation)**: two bars per group, "Portfolio" (dark blue) and the index (blue-grey). The index is the one chosen in the settings if it contains equities; otherwise (bond or money-market index), it is the MSCI ACWI.
- **Main differences by country**: the ten largest overweights and underweights, in points.
- **Share of value and share of risk by region**: a region that brings more risk than value is more volatile or more correlated with the rest. The risk share of each holding is explained in the Asset management workspace, Risk budget tab.

### Limit

The weights of countries and sectors in ETFs and in the MSCI ACWI are approximations (see the entry on the world map).

## Real currency exposure
<!-- fiche: analyse-devises-exposition | questions: why am i exposed to the dollar when my etf is in euros ; how is currency exposure calculated ; currency risk of my portfolio ; eur hedged etf ; how much would a fall in the dollar cost me ; is gold in dollars ; share outside the euro | mots: currencies, currency risk, dollar exposure, EUR Hedged, currency hedging, share outside the euro, USD, gold, real currency | aller: Analyse du portefeuille/Expositions -->

An MSCI World ETF quoted in euros remains exposed to the **dollar**, the yen, the pound, etc.: it holds shares whose value is formed in those currencies. The [[Currencies and rates]] sub-tab measures this real exposure.

### The calculation

On a look-through basis, each piece of an equity ETF receives the currency of its country; a directly held share keeps its trading currency; a fund whose name indicates hedging ("Hedged", "couvert") is counted in euros; bonds are in euros for a euro-zone index, in dollars otherwise; gold is counted separately, with "Gold" as its "currency". The **Real currency exposure** ring covers the **whole** portfolio.

`Share outside the euro = sum of the weights of all currencies except the euro and gold`

### Example

MSCI World ETF €60,000 and €40,000 of French shares. Dollar: `60% × 72.94% = 43.8%`; yen 3.5%; pound 2.0%; Canadian dollar 2.0%; Swiss franc 1.4%; etc. Share outside the euro: **55%**. The finding estimates the effect of a 10% fall in the dollar: `43.8% × 10% ≈ 4%` of the portfolio.

### The finding

It depends on the profile: above 30% outside the euro (Cautious), 50% (Balanced) or 70% (Dynamic), it turns orange, then red above 50%, 70% or 85%. Otherwise: "Limited currency risk".

### Reading

Currency risk is not only negative: the dollar often rises in times of crisis, which cushions falls. Hedging part of the portion is a common compromise; that is the suggestion made.

### Limits

A country's currency is an approximation: an American company earns part of its revenue in other currencies. Hedging is only recognised if it appears in the fund's name.

## Duration and interest-rate sensitivity
<!-- fiche: analyse-duration | questions: what is duration ; if rates rise by 1 point how much do i lose ; sensitivity of my bonds to rates ; why no bonds in rates ; average duration of my portfolio ; interest rate risk ; my bonds fell because of rates | mots: duration, sensitivity, interest rates, bonds, rate risk, rate rise, bond portion, estimated loss | aller: Analyse du portefeuille/Expositions -->

### Duration

It is the weighted average life of a bond's cash flows, in years. It measures **sensitivity to rates**: the longer it is, the more the price falls when rates rise (and rises when they fall).

The software reads the duration of each bond fund from its descriptive record, then calculates:

```
Average duration = Σ (duration × value) / Σ value, over the bond holdings whose duration is known
Loss if rates rise by 1 point ≈ Σ (duration × value) × 1%
```

### Example

€100,000 portfolio; bonds A: €30,000, duration 4 years; bonds B: €10,000, duration 8 years.

- average duration: `(4 × 30,000 + 8 × 10,000) / 40,000 = 5.0 years`;
- estimated loss: `(4 × 30,000 + 8 × 10,000) × 1% = €2,000`, i.e. **−2.0%** of the portfolio.

### Where to see it

[[Currencies and rates]] sub-tab, **Interest-rate sensitivity** block: "Average duration" and "If rates rise by 1 point" cards (in % of the portfolio and in euros). With no bonds, the block says the portfolio contains none, and the Interest rates box in the summary shows "Not applicable".

### The finding

The colour depends on the profile: to monitor above 5 years (Cautious), 7 years (Balanced) or 8 years (Dynamic); to fix above 8, 10 or 12 years. In the example (5.0 years), the finding is green for all profiles.

### Limits

- First-order approximation: `price change ≈ − duration × change in rates`, valid for small changes.
- A bond whose duration is not known is excluded from the average and the estimated loss.
- After a rise in rates, bonds then offer a higher yield, which gradually offsets the loss.

## Concentration, effective number of holdings and the 5/10/40 rule
<!-- fiche: analyse-concentration | questions: what is the 5 10 40 rule ; is my portfolio too concentrated ; effective number of holdings ; equivalent to 3 equal-weight holdings what does it mean ; ucits 40% limit ; a single share represents too much ; likely duplicates etf and directly held share ; held directly and via your etf | mots: concentration, 5/10/40 rule, UCITS, effective number, Herfindahl, largest holdings, duplicates, specific risk | aller: Analyse du portefeuille/Expositions -->

### The effective number of holdings

`Effective number = 1 / Σ weight²` (inverse of the Herfindahl index)

It tells you how many **equal-weight** holdings your portfolio is equivalent to. Example: four holdings of 40%, 30%, 20% and 10%: `1 / (0.16 + 0.09 + 0.04 + 0.01) = 3.33`, displayed as "equivalent to 3 equal-weight positions".

### The [[Concentration]] sub-tab

Four cards: "Rows" (with the effective number), "Top 5 positions", "Top 10 positions" and "Stocks above 5%" ("UCITS limit: 40%"); then the **Largest positions** table (15 at most), with weight and cumulative weight.

### The 5/10/40 rule

A UCITS (European mutual fund) rule: no holding exceeds 10%, and holdings above 5% do not total more than 40%. The software applies it only to **directly held shares**: a diversified ETF is not a concentration.

- Shares above 5% total more than 40%: red finding "5/10/40 rule exceeded".
- The largest share exceeds the profile threshold (5, 7 or 10% for orange; 10, 10 or 15% for red): a finding that quantifies the effect of a 30% fall in the stock.

Example: LVMH 15%, TotalEnergies 10%, Airbus 8%, Sanofi 7% total **exactly 40%**: the rule is not exceeded (it must be more than 40%). However, LVMH at 15% is "To fix" under the Balanced profile; a 30% fall in the stock would cost `15% × 30% ≈ 4%` of the portfolio.

### Likely duplicates

A directly held share may also be in an ETF that you hold: your exposure to that company is then greater than its line alone. The software flags it (orange finding "held directly AND probably also via your ETF") when:

- the ETF tracks the MSCI World, the ACWI or the EAFE and the share's country is part of the index, unless the security's record indicates it belongs to no major index;
- the ETF tracks the MSCI Europe and the share is European, British or Swiss, with the same reservation;
- the ETF tracks the S&P 500 or the US market and the share is American, unless the security's record lists indices without mentioning the S&P 500;
- or the security's record explicitly mentions the ETF's index.

This is a **probability**: the software does not read the fund's actual holdings.

## Reading the correlation matrix
<!-- fiche: analyse-matrice-correlation | questions: how do i read the correlation matrix ; what do the red and blue cells mean ; why is half the table empty ; correlation between my securities ; most correlated pairs ; holdings that diversify best ; view by asset class or by security ; why are the securities not in order | mots: correlation, correlation matrix, heatmap, pairs, diversifiers, blocks, hierarchical clustering, co-movement | aller: Analyse du portefeuille/Expositions -->

The matrix is in the [[Correlations]] sub-tab of the [[Exposures]] tab.

### Correlation

It measures, between −1 and +1, how far the daily returns of two securities move together:

| Value | Reading | Qualifier displayed |
|---|---|---|
| 0.8 to 1 | Almost always rise and fall together | very strong |
| 0.6 to 0.8 | Often move together | strong |
| 0.3 to 0.6 | Partial link | moderate |
| Less than 0.3 | Little link | weak |
| Negative | When one rises, the other tends to fall | (same scale, in absolute value) |

It is calculated on the euro prices of the holdings still held, over the days when all have a return. The note under the chart gives this number of days.

### Reading the map

- **Colours**: red = move together; white = no link; blue = opposite directions.
- **Half of the table**: only the lower triangle is displayed, without the diagonal (always 1); the other half would repeat the same information.
- **Order**: securities are arranged in blocks that move together (hierarchical clustering, distance = 1 − correlation). Blocks appear as red squares.
- **Values**: written in the cells up to 13 securities; beyond that, hover over a cell to read the two names, the value and its qualifier.

### Changing view

The [[Show]] selector offers [[By security]], [[By asset class]], [[By region]] and [[By sector]] (group views only appear if the portfolio has several groups). A group view shows the correlation between the returns of the sub-portfolios, each holding weighted by its weight; groups follow the classification of the holdings, without ETF look-through. Beyond 20 securities, a group view opens by default.

### The tables on the right

- **Most correlated pairs**: the five most closely linked pairs of securities.
- **Best diversifiers**: the five holdings least correlated with the **rest** of the portfolio (the portfolio without them).
- **Blocks of correlated securities**: groups with an average correlation above 0.7 (dedicated entry).

### Limit

Correlations are historical: they are not guaranteed in the future and often rise during crises.

## Average correlation, in normal times and on sharp-decline days
<!-- fiche: analyse-correlation-moyenne | questions: what is the weighted average correlation ; is a high average correlation bad ; correlation on sharp-decline days ; why does correlation rise in a crisis ; the card shows a dash for sharp-decline days ; correlation in a crisis ; does my diversification protect me in a crash | mots: average correlation, weighted correlation, crisis, sharp-decline days, worst 10% of days, contagion, diversification, crash | aller: Analyse du portefeuille/Expositions -->

### The weighted average correlation

```
Average correlation = Σ_{i≠j} wᵢ × wⱼ × ρᵢⱼ / Σ_{i≠j} wᵢ × wⱼ
```

where `w` are the holdings' weights and `ρ` their correlations. It is the "typical" correlation between two euros invested in two different holdings: large holdings count for more.

**Example**: three holdings of 50%, 30% and 20%; correlations 0.8 (A-B), 0.2 (A-C), 0.3 (B-C).
`(0.15 × 0.8 + 0.10 × 0.2 + 0.06 × 0.3) / (0.15 + 0.10 + 0.06) = 0.158 / 0.31 = 0.51`.

**Findings**: above 0.45, "To monitor"; above 0.6, "To fix": the portfolio behaves almost like a single asset.

### Sharp-decline days

The software reconstructs the portfolio's daily return **with its current weights**, keeps its worst 10% of days, and recalculates the weighted average correlation on those days alone.

- "On sharp-decline days" card in the [[Correlations]] sub-tab ("average correlation (worst 10% of days)").
- At least 30 sharp-decline days are needed, i.e. about 300 days of common history: otherwise the card shows a dash.
- If it exceeds the average correlation by more than 0.10, an orange finding says so: "diversification protects less when you need it most".

### Why correlation rises in a crisis

In a crash, investors sell a bit of everything at the same time: assets that are usually independent fall together. Diversification that looks good in normal times can then evaporate. The stress tests in the Wealth advisory workspace let you measure the impact of a crisis.

### Limit

Current weights are applied to the whole history: it is the behaviour of **today's** portfolio in past crises, not that of your real portfolio at the time.

## The diversification ratio
<!-- fiche: analyse-ratio-diversification | questions: what is the diversification ratio ; diversification ratio of 1 what does it mean ; how is the diversification ratio calculated ; what is a good diversification ratio ; is my portfolio really diversified ; diversification ratio choueifaty | mots: diversification ratio, weighted volatility, portfolio volatility, risk reduction, correlation | aller: Analyse du portefeuille/Expositions -->

### The formula

`Diversification ratio = Σ wᵢ × σᵢ / σₚ`

- `Σ wᵢ × σᵢ`: the weighted average of the holdings' volatilities, i.e. the volatility the portfolio would have if all holdings moved exactly together;
- `σₚ`: the portfolio's real volatility, which takes correlations into account.

Both are calculated on daily returns in euros, with current weights.

### Intuition

The ratio measures **how far risk offsets itself** between holdings. It equals 1 when there is no diversification (perfectly correlated holdings) and increases as holdings offset each other.

### Example

Two holdings of 50%, each with volatility 20%:

| Correlation | Portfolio volatility | Ratio |
|---|---|---|
| 1 | 20.00% | 1.00 |
| 0.5 | 17.32% | 1.15 |
| 0 | 14.14% | 1.41 |

With a correlation of 0.5: `σₚ = √(0.25 × 0.04 + 0.25 × 0.04 + 2 × 0.25 × 0.5 × 0.04) = √0.03 = 17.32%`, and `20 / 17.32 = 1.15`.

### Where to see it

"Diversification ratio" card in the [[Correlations]] sub-tab ("1 = no diversification"); it is also cited in the green finding "Satisfactory real diversification".

### Limits

- The ratio has no alert threshold in the diagnosis: it is read by comparison, from one version of the portfolio to another.
- It depends on past correlations.
- Adding a very low-risk holding (money market) changes it little: it measures the offsetting between holdings, not the level of risk.

## Blocks of correlated securities (independent blocks)
<!-- fiche: analyse-blocs-correles | questions: what are independent blocks ; a single bet what does it mean ; blocks of securities correlated above 0.7 ; my 10 holdings are only worth one bet ; how are the blocks formed ; why are my tech stocks in the same block ; number of blocks for my holdings | mots: correlated blocks, independent blocks, bets, hierarchical clustering, clustering, grouping, correlation 0.7, apparent diversification | aller: Analyse du portefeuille/Expositions -->

Ten holdings that rise and fall together are worth only **one bet**. Blocks measure this real diversification.

### How blocks are formed

1. Distance between two securities = `1 − correlation`.
2. Hierarchical clustering by average linkage: the closest securities are grouped, then the groups with each other.
3. Grouping stops at a distance of 0.3: a block gathers securities whose average correlation exceeds about **0.7**.

A security that resembles no other forms a block on its own.

### Where to see it

- "Independent blocks" card ("for" n holdings) in the [[Correlations]] sub-tab: the total number of blocks, isolated securities included.
- **Blocks of correlated securities** block: the five largest blocks of at least two securities, with their weight, their names and their average correlation.
- Blocks also appear as red squares in the matrix.

### Example

Suppose an 8-holding portfolio that shows "5 independent blocks". Three semiconductor shares, correlated at 0.78 on average and weighing 28%, form a block: the diagnosis flags "3 holdings highly correlated with each other (0.78 on average) weigh 28% … 3 holdings, but in practice a single bet".

### The findings

The three largest blocks are examined:

- weight below 15%: no finding;
- from 15 to 25%: "To monitor";
- 25% or more: "To fix".

The suggestions made: replace part of the block with weakly correlated assets, or group these holdings into a single ETF on the same theme.

### Limits

The 0.7 threshold is a convention. Blocks rest on past correlations and may change from one period to another.

## Viewing the transaction history (Transactions tab)
<!-- fiche: analyse-transactions | questions: where do i see all my transactions ; filter transactions by security ; show only dividends ; export my transactions to csv ; why is the price in euros in the history ; price in currency column ; how many transactions in my portfolio ; history of purchases and sales | mots: transactions, history, filter, CSV export, purchases, sales, dividends, viewing, price in currency | aller: Analyse du portefeuille/Transactions | chiffres: nb_operations -->

The [[Transactions]] tab shows all the portfolio's transactions, from most recent to oldest.

### Filtering

- [[Type]]: remove or add ACHAT (purchase), VENTE (sale) and DIVIDENDE (dividend) (all are selected at the start).
- [[Securities]]: choose one or more securities; left empty, it shows "All securities".

A line gives the number of transactions displayed out of the total.

### The columns

| Column | Content |
|---|---|
| Date | Transaction date |
| Type | ACHAT, VENTE or DIVIDENDE |
| Ticker, Security | Code and name of the security |
| Quantity | Number of securities (0 for a dividend) |
| Price / amount (€) | Unit price, or total amount for a dividend, **converted into euros** |
| Fees | Fees in euros |
| Currency, Price in currency | Present if the portfolio contains securities in foreign currencies: the trading currency and the price entered before conversion |

### Exporting

The [[Download the selection (CSV)]] button saves the transactions displayed in the file `transactions_selection.csv`. The types remain written ACHAT, VENTE, DIVIDENDE, but the price column is the one **converted into euros**; the currency and price-in-currency columns are added where relevant. To re-import a portfolio, use the original file or the updated file instead.

### Editing a transaction

The [[Edit transactions]] button lets you delete or correct any transaction. This function, its checks and undoing are described in the chapter on importing and updating the portfolio.
