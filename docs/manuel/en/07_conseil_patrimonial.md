# Wealth advisory
<!-- chapitre: conseil | ordre: 7 -->

This chapter describes the "Wealth advisory" workspace and its two tabs. The **Taxation** tab compares what would be left of your gain after tax in a securities account (CTO), a PEA (French equity savings plan) or a life insurance contract (assurance-vie), at 2026 rates, today or at a future horizon, and measures the share of your portfolio that is eligible for a PEA. The **Stress tests** tab replays five past crises and four to five hypothetical shocks on your current portfolio. The tax rules are deliberately simplified: each fiche states what is modelled and what is not.

## What does the Wealth advisory workspace contain?
<!-- fiche: conseil-presentation | questions: what is the wealth advisory section for ; where do I find the taxation tab ; where are the stress tests ; what can I do in wealth advisory ; where did the client profile go ; is wealth advisory real financial advice ; whats the difference between wealth advisory and asset management | mots: wealth advisory, taxation, stress tests, tax wrappers, PEA, life insurance, assurance-vie, securities account, CTO, crises, scenarios | aller: Conseil patrimonial -->

The **Wealth advisory** workspace is selected from the "Workspace" menu in the sidebar. It analyses the same portfolio, with the same settings, as the "Portfolio analysis" workspace. It has two tabs.

| Tab | Question it answers |
|---|---|
| [[Taxation]] | How much is left after tax, depending on the wrapper (securities account, PEA, life insurance) and the exit date? What share of the portfolio can go into a PEA? |
| [[Stress tests]] | What would the current portfolio lose if a past crisis happened again, or if a hypothetical shock occurred? |

### What the workspace does not do

- It contains no client questionnaire, no regulatory risk profile and no suitability test: these functions are not part of the software. The only profile choice (Cautious, Balanced, Dynamic) is found in the Exposures tab of the "Portfolio analysis" workspace.
- It does not replace personalised tax advice: the progressive income tax scale, the contribution ceilings and contract fees are not modelled (see the fiche on simplifications).

The main results of these two tabs also appear in the PDF report; the taxation there is calculated for a single person, the software's default setting.

As the footer reminds you, the tool is educational and does not constitute investment advice.

## Which tax rates does the software use (2026)?
<!-- fiche: conseil-taux-2026 | questions: what is the flat tax rate in 2026 ; why 31.4% and not 30% ; social contributions went up ; what tax rates does the software use ; PFU 2026 ; why is life insurance at 17.2% ; what are the tax rates in the software ; did the CSG go up in 2026 | mots: flat tax, PFU, single flat-rate levy, social contributions, CSG, 2026 rates, CSG increase, income tax, social security financing act 2026 | aller: Conseil patrimonial/Fiscalité -->

The software applies the rules for an **individual who is tax resident in France, in 2026**. The source cited in the code is Law No. 2025-1403 of 30 December 2025 on the financing of social security for 2026, which raised the CSG (a social contribution) on investment income.

| Rate | Value | Used for |
|---|---|---|
| Income tax (PFU) | 12.8% | CTO; PEA before 5 years; life insurance before 8 years |
| Social contributions, investment income | **18.6%** | CTO and PEA |
| Social contributions, life insurance | **17.2%** | life insurance (not affected by the increase) |
| Total flat tax (12.8 + 18.6) | **31.4%** | CTO; PEA before 5 years |
| Income tax, life insurance after 8 years | 7.5% | above the allowance |
| Annual allowance, life insurance after 8 years | €4,600 (single), €9,200 (couple) | on the part of the gain subject to income tax |

### The latest change

Before 2026, the flat tax was 30% (12.8% + 17.2%). The CSG increase takes social contributions to 18.6% and the flat tax to **31.4%**. Life insurance stays at 17.2% social contributions: before 8 years it is therefore taxed at 30% in total, slightly less than the securities account.

The subtitle of the "Assumptions" box on the tab shows "2026 rates", and a note at the bottom of the "PEA eligibility" box summarises these rates.

### What is not modelled

The option for the progressive income tax scale, the 12.8% rate on life insurance above €150,000 of premiums, and the partial deductibility of the CSG are not taken into account.

## How is tax calculated on a securities account (CTO)?
<!-- fiche: conseil-cto | questions: how much tax if I sell everything in my brokerage account ; CTO taxation ; why do I pay tax when Im at a loss ; do losses cancel out dividends ; flat tax on capital gains ; tax on dividends in the software ; how is an ordinary securities account taxed | mots: CTO, ordinary securities account, flat tax, capital gains, capital losses, dividends, offsetting, PFU, capital gains tax | aller: Conseil patrimonial/Fiscalité | chiffres: gain_total, dividendes -->

On an ordinary securities account (CTO), the software applies the **31.4%** flat tax to the taxable base, with no advantage linked to the holding period.

### The exact formula

```
capital gains        = total gain − dividends
taxable base         = max(0 ; capital gains) + max(0 ; dividends)
income tax           = 12.8% × base
social contributions = 18.6% × base
```

The **total gain** is the one shown in the Overview tab: unrealised gains + realised gains + net dividends.

### The idea: a loss does not wipe out dividends

Capital losses are offset against capital gains, **not against dividends**. A portfolio that is down overall may therefore still owe tax on its dividends.

### Examples

**Gain of €20,000, including €2,000 of dividends**: base = 18,000 + 2,000 = €20,000; tax = €2,560 + €3,720 = **€6,280**; net gain = **€13,720** (effective rate 31.4%).

**Loss of €5,000, but €2,000 of dividends**: capital gains = −€7,000; base = 0 + 2,000 = €2,000; tax = €256 + €372 = **€628**, even though the total gain is negative.

### Interpretation

On the "CTO exit" card, the "No holding-period advantage" label is a reminder that the rate never falls over time. This is the benchmark against which to compare the PEA and life insurance.

### Limitations

The calculation assumes the whole gain is taxed at once, on exit. In reality, on a CTO, dividends and realised gains are taxed in the year they are received. The option for the progressive scale, sometimes more favourable for low incomes, is not modelled.

## How is tax calculated on a PEA?
<!-- fiche: conseil-pea | questions: PEA taxation after 5 years ; how much tax if I withdraw from my PEA ; what happens if I withdraw from a PEA before 5 years ; why is the PEA taxed at 18.6% ; when does a PEA become worthwhile ; tax advantage of the PEA ; my PEA is 3 years old how much will I pay ; pea tax calculaton | mots: PEA, equity savings plan, 5 years, exemption, social contributions, closure, tax advantage, PEA ceiling | aller: Conseil patrimonial/Fiscalité | chiffres: gain_total -->

The **PEA (plan d'épargne en actions, a French equity savings plan)** offers an exemption from income tax after 5 years. The software calculates the tax as if your portfolio had been held in a PEA since your first transaction.

### The exact formula

```
base = max(0 ; total gain)
before 5 years: income tax = 12.8% × base     (a withdrawal closes the plan)
after 5 years:  income tax = 0
social contributions = 18.6% × base            (in all cases)
```

Age is measured from the date of your **first transaction** to the last date in the history, divided by 365.25 days.

### Example

Gain of €20,000:

- age of 3 years: €2,560 + €3,720 = €6,280 of tax, net gain **€13,720** (31.4%, as for the CTO). The card shows "Tax advantage in 2.0 year(s)";
- age of 9 years: €0 + €3,720 = €3,720, net gain **€16,280** (18.6%). The card shows "Tax advantage reached".

Difference after 5 years: **€2,560** more in your pocket, which is the 12.8% income tax.

### Interpretation

Unlike the CTO, a loss never creates tax: the base is the total gain, floored at zero if negative, without distinguishing dividends from capital gains.

### Limitations

- The €150,000 contribution ceiling is not applied in the calculation; a note flags it if your invested amount exceeds it.
- Only certain securities are eligible: see the fiche "What share of my portfolio can go into a PEA?".
- The calculation applies the PEA to the **whole** portfolio, even to ineligible holdings: it is a theoretical comparison.

## How is tax calculated on life insurance (assurance-vie)?
<!-- fiche: conseil-assurance-vie | questions: life insurance taxation after 8 years ; the 4600 euro allowance ; life insurance for a couple 9200 ; how much tax on a life insurance withdrawal ; why is life insurance taxed at 30% before 8 years ; how do I choose single or couple ; life insurance 7.5% | mots: life insurance, assurance-vie, unit-linked, 8 years, allowance, 4600, 9200, withdrawal, couple, single | aller: Conseil patrimonial/Fiscalité | chiffres: gain_total -->

The software treats the portfolio as if it were held in **unit-linked funds** (unités de compte) of a life insurance contract (assurance-vie) opened on the date of your first transaction.

### The exact formula

```
base = max(0 ; total gain)
social contributions = 17.2% × base
before 8 years: income tax = 12.8% × base
after 8 years:  income tax = 7.5% × max(0 ; base − allowance)
allowance = €4,600 (single) or €9,200 (couple)
```

Marital status is chosen with the [[Marital status (life insurance allowance)]] control at the top of the [[Taxation]] tab. The default setting is "Single".

### Examples

Gain of €20,000:

| Situation | Income tax | Social contributions | Net gain | Effective rate |
|---|---|---|---|---|
| 3 years old | €2,560 | €3,440 | €14,000 | 30.0% |
| 9 years, single | 7.5% × 15,400 = €1,155 | €3,440 | €15,405 | 23.0% |
| 9 years, couple | 7.5% × 10,800 = €810 | €3,440 | €15,750 | 21.3% |

### Interpretation

- Before 8 years, life insurance (30%) is slightly more favourable than the CTO and the PEA under 5 years (31.4%), because its social contributions remain at 17.2%.
- After 8 years, the allowance makes life insurance very attractive for modest gains: a gain below €4,600 (€9,200 for a couple) bears only social contributions.
- Compared with a PEA over 5 years old (18.6%), life insurance over 8 years old (17.2% + 7.5% above the allowance) is taxed less only for small gains: up to about €5,656 for a single person (0.172 G + 0.075 (G − 4,600) = 0.186 G) and €11,311 for a couple. Beyond that, the PEA wins.

### Limitations

- The allowance is annual in reality; here, the full exit is made in one go, so only one allowance applies.
- Premiums are assumed to be below €150,000 (above that, the rate is 12.8% rather than 7.5%); a note flags it if your invested amount exceeds that threshold.
- The contract's management fees are not deducted.
- In reality, the tax on a partial withdrawal applies only to the share of gains contained in the withdrawal; the software simulates a full exit.

## Reading "If everything were sold today": cards and wrapper table
<!-- fiche: conseil-sortie-aujourdhui | questions: how much would I have left if I sold everything today ; compare CTO PEA and life insurance for my portfolio ; what does effective rate mean ; what is net return ; what does tax advantage in 2 years mean ; the taxation table explained ; net gain after tax | mots: net gain, gross gain, effective rate, net return, wrapper comparison, exit, tax, full withdrawal | aller: Conseil patrimonial/Fiscalité | chiffres: gain_total, montant_investi, dividendes -->

In the [[Taxation]] tab, the "If everything were sold today" section assumes you sell the **whole portfolio** today, and compares the result in the three wrappers. Its subtitle shows the **gross gain** (the total gain from the Overview tab).

### The three cards

One card per wrapper: "CTO exit", "PEA exit", "Life insurance exit". Each shows:

- the **net gain** after tax, in euros;
- a "tax x%" badge: the **effective rate**;
- the state of the tax advantage: "No holding-period advantage" (CTO), "Tax advantage in n year(s)" or "Tax advantage reached".

### The formulas

```
net gain             = gross gain − income tax − social contributions
effective rate       = total tax / gross gain          (0 if the gain is negative)
gross return         = gross gain / amount invested
net return           = net gain / amount invested
years before advantage = max(0 ; wrapper term − age)   (5 years PEA, 8 years life insurance)
```

### Example

Amount invested €100,000, gain €20,000 including €2,000 of dividends, age 3 years, single:

| Wrapper | Income tax | Social contributions | Net gain | Net return |
|---|---|---|---|---|
| CTO | €2,560 | €3,720 | €13,720 | 13.7% |
| PEA | €2,560 | €3,720 | €13,720 | 13.7% |
| Life insurance | €2,560 | €3,440 | €14,000 | 14.0% |

Gross return: 20% for all three. The PEA shows "Tax advantage in 2.0 year(s)", life insurance "in 5.0 year(s)".

### The table

Below the cards, a table gives for each wrapper: Gross gain, Income tax, Social contributions, Net gain, Gross return and Net return.

### Interpretation

This is not your actual tax: it is what **you would have paid** if this same portfolio had been held in each of the wrappers since your first transaction. The tool is for comparing wrappers, not for preparing a tax return.

## The "Net gain by exit year" chart
<!-- fiche: conseil-annee-sortie | questions: when is it better to leave my PEA ; what do the jumps in the taxation chart mean ; from when is the PEA better than the CTO ; why open a PEA early ; net gain if I sell in 10 years ; what return is used for future exits ; start the life insurance clock early | mots: exit year, horizon, start the clock, tax jump, 5 years, 8 years, future net gain, assumed return, compounding | aller: Conseil patrimonial/Fiscalité | chiffres: valeur_actuelle, gain_total -->

On the left, below the cards in the [[Taxation]] tab, the "Net gain by exit year" chart shows, for each wrapper, the net gain after tax if you sold everything in 0 to 20 years.

### The setting

The [[Assumed annual return for future exits (%)]] slider (0 to 10%, in steps of 0.5, default 5%) sets the assumed growth of the portfolio.

### The formula

```
gain in n years = current gain + current value × ((1 + return)ⁿ − 1)
age in n years  = current age + n
net gain        = gain − wrapper tax (calculated with this age)
```

Dividends stay fixed at their current amount (which matters only for the CTO).

### The jumps

The PEA and life insurance curves are **step-shaped**: they jump upwards when the age passes **5 years** (PEA) or **8 years** (life insurance). The CTO curve, with no holding-period advantage, is continuous.

### Example

Current value €120,000, current gain €20,000 (including €2,000 of dividends), age 3 years, assumed return 5%, single:

| Exit in | Gross gain | CTO | PEA | Life insurance |
|---|---|---|---|---|
| 0 years | €20,000 | €13,720 | €13,720 | €14,000 |
| 1 year | €26,000 | €17,836 | €17,836 | €18,200 |
| 2 years (PEA at 5 years) | €32,300 | €22,158 | **€26,292** | €22,610 |
| 5 years (life insurance at 8 years) | €53,154 | €36,464 | €43,267 | **€40,370** |

### Interpretation

The chart shows why an adviser recommends opening these wrappers **early**, to "start the clock": it is the opening date that starts the waiting periods, not the date of the payments. Hover over a curve to read the net gain of each wrapper for a given exit year.

### Limitations

Steady, certain growth, with no contract fees; same simplifications as for the immediate exit.

## What share of my portfolio can go into a PEA?
<!-- fiche: conseil-eligibilite-pea | questions: are my securities eligible for a PEA ; why isnt Apple eligible for a PEA ; PEA-eligible share ; can a world ETF go into a PEA ; why is my bond ETF not eligible ; are UK shares eligible for a PEA ; ineligible holdings in the PEA box | mots: PEA eligibility, eligible, EU, EEA, European shares, eligible ETFs, CW8, ESE, synthetic replication, ineligible | aller: Conseil patrimonial/Fiscalité | chiffres: valeur_actuelle, montant_investi -->

The "PEA eligibility" box, to the right of the chart in the [[Taxation]] tab, shows the "PEA-eligible share" card and the number of ineligible holdings.

### The software's rule

A holding is considered eligible if:

- it is a **share** (asset class "Equities") of a company whose country is in the **European Union or the EEA** (Norway, Iceland and Liechtenstein included); or
- it is one of the **index funds recognised as eligible**: CW8.PA (Amundi MSCI World) and ESE.PA (BNP Paribas Easy S&P 500), eligible thanks to their synthetic replication.

```
eligible share = value of eligible holdings / total portfolio value
```

### What is not eligible

- US, British (since Brexit), Swiss or Japanese shares;
- bond funds and gold (the PEA is reserved for equities);
- ETFs not listed above, even if they are in fact eligible;
- securities whose country is not recorded in the reference data.

### Example

Portfolio of €100,000: €40,000 of French and German shares, €30,000 of CW8.PA, €20,000 of US shares, €10,000 of bond ETF. Eligible share = (40,000 + 30,000) / 100,000 = **70%**; 2 ineligible holdings.

### The notes displayed

- if the share is below 100%: only the eligible share can go into a PEA; the rest would go into a securities account or into life insurance unit-linked funds;
- if the amount invested exceeds €150,000: a reminder of the PEA contribution ceiling and the life insurance threshold;
- in all cases, a reminder of the 2026 rates.

### Limitations

The list of eligible funds is short: check the actual eligibility of your ETFs in their documentation. The wrapper comparison fiche applies the PEA to the whole portfolio, even to ineligible holdings.

## The simplifications in the tax calculation
<!-- fiche: conseil-simplifications-fiscales | questions: is the tax calculation accurate ; can I use the taxation tab for my tax return ; is the progressive scale taken into account ; are life insurance fees deducted ; is the 150000 PEA ceiling taken into account ; why is my real tax different ; limits of the taxation tab | mots: simplifications, limitations, progressive scale, ceiling, management fees, tax return, approximation, assumptions | aller: Conseil patrimonial/Fiscalité -->

The [[Taxation]] tab is an **educational comparison tool**. It is not designed to calculate your actual tax or to fill in a tax return.

### What is simplified

| Simplification | Consequence |
|---|---|
| Option for the progressive scale ignored | for a lightly taxed household, the actual tax may be lower |
| Life insurance premiums assumed below €150,000 | above that, the actual rate after 8 years is 12.8% rather than 7.5% (a note flags it) |
| PEA contribution ceiling (€150,000) not applied | a note flags it if the amount invested exceeds it |
| Contract management fees ignored | the net gain on life insurance is overstated |
| Dividends assumed to stay in the wrapper | the total gain (unrealised + realised + dividends) is taxed in one go on exit |
| Full exit in one go | a single life insurance allowance, no staggered partial withdrawals |
| Same portfolio in all three wrappers | the PEA is applied even to ineligible holdings |
| Age = since the first transaction | a wrapper opened earlier would already have started its clock |

### What is not covered at all

Inheritance, gifts, the property wealth tax (IFI), retirement savings plans (PER) and non-resident situations are not covered.

### Why keep the model simple?

A simple model makes the essentials visible: the difference in rates between wrappers and the effect of the 5- and 8-year waiting periods. For a real decision, have the calculation validated by a professional.

## Historical stress tests: what would my portfolio lose in a crisis?
<!-- fiche: conseil-stress-historiques | questions: what would my portfolio lose in a crash ; what are stress tests ; how much would I have lost in 2008 ; which crises are replayed ; dates of the crises in the stress tests ; the worst historical scenario ; replay covid on my portfolio ; why does the stress test take a while | mots: stress test, crisis, crash, 2008, Covid, European debt, 2022, August 2024, historical scenario, maximum loss | aller: Conseil patrimonial/Stress tests | chiffres: valeur_actuelle, max_drawdown -->

The [[Stress tests]] tab applies to **each holding in your current portfolio** the change it actually suffered during a past crisis, from the market peak to the market trough.

### The five crises replayed

| Crisis | From (peak) | To (trough) |
|---|---|---|
| Financial crisis (2008-2009) | 01/09/2008 | 09/03/2009 |
| European debt crisis (2011) | 01/07/2011 | 22/09/2011 |
| Covid crash (2020) | 19/02/2020 | 23/03/2020 |
| Inflation and rate hikes (2022) | 03/01/2022 | 12/10/2022 |
| August 2024 mini-crash | 16/07/2024 | 05/08/2024 |

Dates are in DD/MM/YYYY format.

### The formula

```
change of a holding = price at end date / price at start date − 1
portfolio change    = Σ current weight of the holding × change of the holding
loss in euros       = portfolio change × current value
```

The price used at each date is the last known price at that date.

### Example

50% in a holding that lost 45%, 30% in a holding that lost 40% and 20% in a bond fund that gained 5%: change = −22.5% − 12% + 1% = **−33.5%**, i.e. −€33,500 on €100,000.

### What is displayed

- three cards: "Worst historical scenario", "Corresponding loss" (in euros, on the current value) and "Portfolio beta";
- a bar chart "Past crises replayed on the current portfolio" (green for a gain, red for a loss);
- the table "Historical scenarios in detail": Scenario, Period, Change, Gain / loss, Share estimated with an index;
- the [[Show the detail by holding]] list, which shows, for the selected crisis, the change of each security and its source (the security itself or an index).

### First display

Prices since 2008 have to be downloaded: the message "Replaying past crises (history since 2008)..." is shown while the calculation runs. The prices are then kept in a separate cache file. Without Internet on the first display, the message "Stress tests unavailable" may appear.

### Interpretation

"At the worst point of 2008, this portfolio would have lost 33.5%, or €33,500" speaks to a client more than a volatility figure does. The weights are those of **today**: the test applies to the current composition, not to the portfolio you held at the time.

## A security not listed at the time: how does the stress test estimate it?
<!-- fiche: conseil-stress-proxy | questions: my ETF didnt exist in 2008 so how is the stress test calculated ; what does share estimated with an index mean ; why does the source say GSPC index ; which index replaces a recent security ; how are bonds treated in the stress tests ; is the stress test reliable if my securities are recent ; stress test proxy | mots: proxy, approximation, regional index, S&P 500, Euro Stoxx 50, bond fund, estimated share, recent security, missing history | aller: Conseil patrimonial/Stress tests -->

Many securities did not exist during the older crises. The software then replaces the security's change with that of a **representative index or fund** (a "proxy").

### When is a security replaced?

When it has no price history, or when its first known price is more than 7 days after the start of the crisis.

### Which substitute?

**For a bond or gold** (an asset class other than "Equities"), a fund of the same category, listed since 2007 at the latest:

| Category | Fund used |
|---|---|
| Government bonds | IEF |
| Inflation-linked bonds | TIP |
| Corporate bonds | LQD |
| High-yield bonds | HYG |
| Emerging-market bonds | EMB |
| Gold | GLD |

An equity index would be a poor approximation: in 2008, government bonds rose while equities fell.

**For an equity** (or if the category is not recognised), the index of its region:

| Region | Index |
|---|---|
| United States, World (ETF) | ^GSPC (S&P 500) |
| Europe | ^STOXX50E (Euro Stoxx 50) |
| United Kingdom | ^FTSE |
| Switzerland | ^SSMI |
| Japan | ^N225 |
| Asia-Pacific | ^AXJO |
| Canada | ^GSPTSE |
| Emerging markets | EEM |

If the region is unknown, or if the substitute has no price history either, the S&P 500 is used. If no price is available at all, the change of the holding is counted as 0.

### The "Share estimated with an index" column

```
estimated share = Σ current weights of the holdings replaced by an index or a fund
```

Example: a 30% holding replaced by ^GSPC and a 10% holding replaced by IEF give **40%**. The higher this figure, the more the result is an approximation. The detail by holding shows the source ("security" or "index ^GSPC").

### Limitations

A "world" ETF approximated by the S&P 500 ignores the rest of the world; a small-cap approximated by a large index often underestimates its fall.

## Hypothetical shocks: a fall in equities and in the dollar
<!-- fiche: conseil-chocs-hypothetiques | questions: what happens if the stock market falls 20% ; how is the equity shock calculated ; why use beta in the stress tests ; impact of a fall in the dollar on my portfolio ; my S&P 500 ETF in euros isnt counted in the dollar fall ; hypothetical scenarios stress test ; 35% market drop | mots: hypothetical shock, beta, equity fall, dollar, currency, USD, sensitivity, scenario, 10%, 20%, 35% | aller: Conseil patrimonial/Stress tests | chiffres: beta, valeur_actuelle -->

To the right of the past crises, the "Hypothetical shocks" chart applies simple scenarios. Its subtitle summarises the rules: "Equities: beta × shock · Dollar: share invested in dollars · Rates: duration".

### Equities falling by 10%, 20% and 35%

```
portfolio change ≈ beta × shock
```

The **beta** is the one from the Risk tab: the portfolio's sensitivity to the index chosen with the [[Benchmark index]] menu in the Settings. A beta of 0.85 means the portfolio moves on average by 0.85% when the index moves by 1%.

Example: beta 0.85, shock −20%: change = 0.85 × −20% = **−17%**, i.e. −€17,000 on €100,000.

### The dollar falling by 10%

```
change = −10% × share of the portfolio quoted in dollars
```

Example: 35% of the portfolio in USD-quoted securities: change = −10% × 35% = **−3.5%**.

Note: the software looks at the **trading currency**. A euro-quoted ETF that invests in US equities is not counted, even though it does in fact suffer the currency effect. For a full view of currency exposure, see the Exposures tab.

### Interpretation

Beta summarises market risk in a single figure. It is convenient but linear: in a crisis, correlations rise and the actual loss may exceed beta × shock. This is why the historical scenarios, which use real changes, complement these shocks.

### Limitations

- beta is estimated over your analysis period;
- the dollar shock ignores the effect on the companies themselves (exporters, etc.);
- a shock to an index says nothing about a shock specific to one sector.

## The interest-rate rise shock and duration
<!-- fiche: conseil-hausse-taux | questions: what happens if interest rates rise by 1% ; what is duration ; why do my bonds fall when rates rise ; the rate rise scenario doesnt appear ; how is the loss on my bond funds calculated ; interest rate sensitivity of my portfolio | mots: rate rise, duration, sensitivity, bonds, interest rates, bond fund, 1 point, interest rate risk | aller: Conseil patrimonial/Stress tests | chiffres: valeur_actuelle -->

The "Rates up 1 point" scenario estimates the loss on the **bond funds** in your portfolio if interest rates rose by 1 percentage point (for example from 3% to 4%).

### Duration

A bond's **duration** (in years) measures its sensitivity to rates: a duration of 7 years means that a 1-point rise in rates lowers its price by about 7%. When rates rise, older bonds, which pay less than new ones, lose value.

### The formula

```
portfolio change = −1% × Σ (weight of the holding × duration of the holding)
```

Holdings with no duration (equities, gold) count as 0. The duration of each fund comes from the software's securities reference data.

### Example

15% of the portfolio in a fund with a duration of 7 years and 5% in a fund with a duration of 3 years:

- change = −1% × (0.15 × 7 + 0.05 × 3) = −1% × 1.2 = **−1.2%**, i.e. −€1,200 on €100,000;
- average bond duration = 1.2 / 0.20 = 6 years.

### When does this scenario appear?

Only if at least one holding has a known duration. A 100% equity portfolio, or bond funds absent from the reference data, will not show it.

### Limitations

- the relationship is linear: for a large shock, convexity makes the actual loss somewhat smaller;
- the effect of a rate rise on **equities** is not taken into account in this scenario (see instead the "Inflation and rate hikes (2022)" crisis among the historical scenarios);
- the durations in the reference data are fixed values, which in reality change over time.

## The limitations of the stress tests
<!-- fiche: conseil-stress-limites | questions: are the stress tests reliable ; why is the loss shown different from what I really lost in 2020 ; are dividends included in the stress tests ; currency effect in past crises ; stress tests unavailable what do I do ; can the worst scenario be worse | mots: limitations, reliability, local currency, excluding dividends, currency, approximation, cache, unavailable | aller: Conseil patrimonial/Stress tests -->

The stress tests give orders of magnitude, not exact figures.

### The simplifications

- **Local currency**: in the historical scenarios, changes are calculated in each security's trading currency. The currency effect for a euro-based investor is ignored: a rise or fall of the dollar during the crisis would have cushioned or worsened the actual loss in euros.
- **Excluding dividends**: prices are not adjusted for dividends. Over a crisis lasting a few months, the difference is small.
- **Current weights**: the test applies to today's composition, not the one you had at the time. It is therefore not what you actually lost.
- **From market peak to market trough**: the dates are those of the market as a whole; a security may have hit its low on a different day.
- **Proxies**: a recent security is replaced by an index or a fund (see the "Share estimated with an index" column).
- **Linear shocks**: beta × shock and duration × rate rise are first-order approximations.

### The worst can be worse

The five crises do not cover every risk: a future crisis may be different (lasting inflation, geopolitical shock, sector crash). The worst scenario displayed is not a limit.

### If the message "Stress tests unavailable" appears

The most frequent cause is the lack of an Internet connection on the first display: the history since 2008 has not yet been downloaded. Reconnect and reopen the tab. After that, the cache takes over.
