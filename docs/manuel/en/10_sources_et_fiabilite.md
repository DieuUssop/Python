# Where the data comes from and how far to trust it
<!-- chapitre: sources | ordre: 10 -->

This chapter states where each piece of data used by the software comes from: share prices, the local securities database, currencies, recognition of ISIN codes, ETF composition, security classification, benchmark indices, the risk-free rate and the world map background. It then sets out, honestly, what the software checks, what it does not check, and what to do if a figure looks wrong.

## Where does the software's data come from?
<!-- fiche: sources-vue-ensemble | questions: where does the data come from ; what is the source of the prices ; where do the numbers in the software come from ; which data sources are used ; is the data from bloomberg ; who provides the prices ; where does the ETF information come from ; is the software connected to my bank | mots: sources, origin of the data, provenance, Yahoo Finance, Wikipedia, MSCI, ECB, Natural Earth, reference file -->

The software has no subscription to a professional data provider (Bloomberg, Refinitiv…) and is not linked to any bank. Its data comes from the following sources.

| Data | Source | Updated |
|---|---|---|
| Daily prices of securities, indices and exchange rates | Yahoo Finance, through the Python library `yfinance` | at every analysis with Internet; otherwise local database and cache |
| Quotation currency of each security | Yahoo Finance, otherwise the local database, otherwise a rule based on the security's code | once per security, then kept |
| List of securities in the local database | Wikipedia pages of 32 stock indices, a list of 66 ETFs and the project's reference file | when the database is built |
| Matching an ISIN, name or Bloomberg code to a ticker | built-in table of 31 ETFs, local memory, local database, then the Yahoo Finance search engine | at every import of an unknown security |
| Country, region, sector, asset class, duration | the project's `data/referentiel.csv` file, supplemented by the local database | fixed, shipped with the software |
| ETF composition by country and sector | MSCI factsheets as of 30/09/2026 and 2025-2026 orders of magnitude | fixed, to be reviewed once a year |
| Regional index weights for performance attribution | MSCI ACWI IMI as of 30/06/2026 | fixed |
| Risk-free rate | fixed value of 2.50% (the ECB deposit facility rate), editable | setting |
| Country outlines (world map) | Natural Earth, public domain | downloaded once |

### What comes from you

Transactions (dates, quantities, prices, fees, dividends) come only from your files or your entries. The software checks them, but never corrects them without your knowledge.

### Where to see the source of the prices

- In the banner at the top of the page: "Live prices · Yahoo Finance" (green dot) or "Cached prices (offline)" (orange dot), and the "Data as of" note followed by the date of the last price in the history.
- At the bottom of the sidebar, the "Prices" line: "Yahoo Finance (en direct)", or "cache local du" followed by a date, with the note "Yahoo Finance injoignable". These two strings come from the program as it stands and are shown in French.

## Which prices exactly does the software use?
<!-- fiche: sources-cours-yahoo | questions: does the software use the closing price or the adjusted price ; adj close or close ; what is auto_adjust ; which price is used to value my portfolio ; are the prices real time ; why is the price different from my broker ; closing price adjusted for dividends ; where does the latest price come from | mots: closing price, Close, Adj Close, auto_adjust, adjusted price, Yahoo Finance, yfinance, real time, latest price -->

### The closing price, not adjusted for dividends

The software downloads prices with the `auto_adjust=False` setting of the `yfinance` library and keeps the **`Close`** column (closing price). It **never** uses the `Adj Close` column (price adjusted for dividends). This choice is the same everywhere: analysis history, latest price, building the local database.

Why? To value your portfolio at the **real price shown on the exchange**, the one you see at your broker, and to count dividends only once: through the "DIVIDENDE" lines of your file.

### Two uses

| Use | What is requested from Yahoo Finance |
|---|---|
| History (day-by-day value, performance, risk) | the daily closing prices since the date of your first transaction |
| Current value | the prices of the last 5 days; the software keeps the last known value of each security |

The latest price is therefore the most recent one Yahoo Finance provides: the closing price of the last session, or a value from the current session if the exchange is open. The 5 days are there so that a price can always be found at weekends and on public holidays.

### Days without trading

When a market is closed (local public holiday), the value of the security that day is its last known price. A transaction entered on a day without trading (a Saturday, for example) is attached to the next trading day.

### Why a difference from your broker?

- different moment (closing price versus price at the moment);
- different trading venue (the same security in Paris and in Amsterdam, or an ETF listed in two currencies);
- conversion into euros at the Yahoo Finance exchange rate, not your bank's;
- a possible error in the source (see the entry "A price looks wrong: what should I do?").

## Dividends and stock splits: what an unadjusted price implies
<!-- fiche: sources-dividendes-divisions | questions: are my dividends included in the performance ; the price drops on the dividend day ; stock split my performance is wrong ; my share did a split and I am losing 90% ; how do I enter a stock split ; accumulating or distributing ETF ; reverse split ; does the software handle splits | mots: dividend, ex-dividend date, split, stock split, reverse split, accumulating ETF, distributing ETF, corporate action, adjustment -->

### Dividends

With an unadjusted price, a share's price falls by roughly the amount of the dividend on its ex-dividend date. The software compensates for this fall **only if the dividend is in your transactions** (a "DIVIDENDE" line, with the total amount received). It does not download dividends on your behalf.

- **Recorded dividends**: they are added to the total gain and to the performance.
- **Forgotten dividends**: the performance is underestimated by the same amount.
- **Accumulating ETFs**: dividends are reinvested in the fund, so they are already in its price; there is nothing to enter.
- **Distributing ETFs**: they pay out dividends, to be recorded as for a share.

The same principle applies to the benchmark index: an accumulating ETF gives a "dividends reinvested" performance, a price index such as the CAC 40 (`^FCHI`) gives an "excluding dividends" performance. The name of each index says which.

### Stock splits

Yahoo Finance retroactively corrects its closing prices after a stock split. The software, for its part, only knows the transaction types ACHAT (buy), VENTE (sell) and DIVIDENDE (dividend): **it does not handle stock splits or reverse splits**.

Example: you bought 10 shares at €800. The company then splits each share into 10. Yahoo now shows a history of around €80 for the date of your purchase. Your file still says 10 shares: the software would value 10 × €80 = €800 instead of €8,000.

At import, the price check flags it: the price in the file is far from the market price of the day (here, a gap of +900%), with the note "check the ticker, currency or a stock split".

**The fix**: express the transaction in securities as they stand after the split, without changing the amount. Here, 100 shares at €80 (100 × 80 = €8,000). You can do this in the Transactions tab with [[Edit transactions]]. The total cost, fees and cash flows stay the same.

### Other corporate actions

Mergers, spin-offs, ticker changes or free share allotments are not handled automatically. You have to translate them yourself into buys and sells.

## The local securities database: what does it contain?
<!-- fiche: sources-base-locale | questions: what is the local securities database ; how many securities are in the database ; which indices are covered ; from what date are the prices ; my share is not in the database ; what is in data base titres.csv ; does the database contain ETFs ; how far back do the prices go | mots: local database, securities database, titres.csv, npz packs, universe, history, 2015, 2007, offline -->

The local database is the software's "memory": it lets it work without Internet and faster online. It is stored in the `data/base` folder.

### Its contents

| Item | Contents |
|---|---|
| `titres.csv` | the record of each security: Yahoo ticker, name, ISIN (when known), country, region, sector, asset class, currency, indices it belongs to |
| `cours/paquet_00.npz` to `paquet_31.npz` | the daily closing prices, split into 32 compressed files |
| `memoire.csv` | the matches learned during imports (ISIN, name or code to ticker) |
| `pays.geojson` | the country outlines, for the world map |

### The universe covered

- **Equities**: the composition, read from Wikipedia, of 32 indices: S&P 500, Nasdaq-100, Dow Jones, Russell 1000, CAC 40, SBF 120, CAC Mid 60, DAX, MDAX, SDAX, TecDAX, FTSE 100, FTSE 250, Euro Stoxx 50, AEX, AMX, BEL 20, IBEX 35, FTSE MIB, SMI, SMIM, OMX Stockholm 30, OMX Copenhagen 25, OMX Helsinki 25, OBX, ATX, PSI, ISEQ 20, Nikkei 225, S&P/TSX 60, S&P/ASX 200 and Hang Seng. The project estimates this at about 3,500 shares.
- **ETFs**: a list of 66 common ETFs (equities, bonds, gold, money market), European and American.
- **Project reference file**: the securities in `data/referentiel.csv`.
- **Market**: 16 stock indices and 12 euro exchange rates (US dollar, pound, Swiss franc, yen, Canadian, Australian, Hong Kong and Singapore dollars, Danish, Swedish and Norwegian krone, zloty).

### Depth of history

- from **1 January 2015** for shares and ETFs;
- from **1 January 2007** for indices and exchange rates, which makes it possible to replay the 2008 crisis in the stress tests.

### Precision and limits

- Prices are stored with about 7 significant digits, which is more than enough for share prices.
- The list reflects the composition of the indices **at the time of building**: a company that left an index beforehand is not in it. If you hold it, its prices are downloaded at the first online analysis, then added to the database.
- The ISIN is filled in only if the index's Wikipedia page gives it.
- The exact number of securities depends on the version shipped: some Wikipedia pages may be unreadable on the day of building, and codes unknown to Yahoo Finance are discarded.

## How the securities database is built and updated
<!-- fiche: sources-base-construction | questions: how do I update the securities database ; how does construire_base_titres.py work ; does the database update itself ; construire_base.bat ; update prices offline ; how long does it take to build the database ; what does cumulative database mean ; what is echecs.csv | mots: building, update, construire_base_titres.py, construire_base.bat, --mise-a-jour, cumulative database, Wikipedia, batches, resume, echecs.csv -->

### The full build

It is done by the script `construire_base_titres.py` (on Windows, from the source code, by double-clicking `construire_base.bat`), with Internet:

1. reading the composition of the 32 indices on Wikipedia;
2. adding the 66 ETFs and the securities of the reference file;
3. downloading the map background;
4. downloading prices: first the indices and exchange rates from 2007, then the securities from 2015, **in batches of 100 securities**, with a 2-second pause between two batches and up to 3 attempts per batch if Yahoo Finance refuses.

The project estimates this at about an hour. If it is interrupted, running the command again resumes where it stopped. Codes that Yahoo Finance does not recognise are listed in `data/base/echecs.csv`.

Installed versions are shipped with the database that was in the project when they were built.

### The update

```
python construire_base_titres.py --mise-a-jour
```

The script takes all the securities that have prices in the database, and downloads their prices from the last known date minus 7 days. It takes only a few minutes. The `--liste` option rebuilds only the list of securities, without the prices.

### A cumulative database

The database also fills itself in **on its own**:

- each history downloaded for an online analysis is added to it;
- the new values replace the old ones for the same dates;
- only modified files are rewritten, through a temporary file that is then renamed: an interruption never leaves a damaged file.

So a security analysed once with Internet remains available offline.

### With a new version

Installing a new version replaces the database with the one shipped with that version. On Mac, the memory of recognised securities is kept. The prices that your own use had added will be downloaded again at the next online analysis.

## The price cache and the "Refresh prices" button
<!-- fiche: sources-cache | questions: what is the cache ; what is refresh prices for ; the prices are not updating ; why are the prices the same as an hour ago ; cache_prix.csv ; cached prices offline ; how do I clear the cache ; force the download of prices | mots: cache, memory, refresh, reload, an hour, cache_prix.csv, cache_historique.csv, offline -->

The software keeps prices in two places to avoid downloading them again and again.

### 1. In memory, for one hour

The results of an analysis are kept in memory for **one hour** as long as the portfolio and the settings do not change: the page stays fast. During this time, prices are not requested again from Yahoo Finance. The result of the automatic reading of an imported file is kept in the same way.

The [[Refresh prices]] button, at the bottom of the sidebar, clears all this memory and reloads the page: prices are downloaded again (Internet required).

### 2. In files, for offline use

| File (`data` folder) | Contents |
|---|---|
| `cache_prix.csv` | the latest prices from the last analysis, with the date and time of the download |
| `cache_historique.csv` | the history from the last analysis |
| `cache_devises.csv` | the quotation currency of each security already encountered |
| `cache_import.csv`, `cache_candidats.csv` | the prices used to check imported files |
| `cache_stress.csv`, `cache_attribution.csv` | the long histories for the stress tests and performance attribution |

These files are rewritten at every successful download. If Yahoo Finance does not respond, the software reads the cache again, completes it with the local securities database, and says so: "Cached prices (offline)" in the banner, "cache local du" followed by a date in the sidebar (this sidebar text is shown in French). That date is the oldest of the sources used.

### A particularity: the currency

The currency of each security, once known, is kept **with no time limit** in `cache_devises.csv`. If it was deduced offline from the security's code and is wrong, it stays wrong. Deleting this file forces the software to ask Yahoo Finance for it again.

### Clearing the caches

[[Refresh prices]] clears the one-hour memory. The `cache_*.csv` files can be deleted without risk: they are recreated at the next online analysis. Offline, however, they will no longer be available.

## The memory of recognised securities
<!-- fiche: sources-memoire-titres | questions: does the software remember the securities I imported ; what is memoire.csv ; a wrongly recognised isin comes back at every import ; how do I correct a wrong isin ticker match ; why is the security recognised without internet ; erase the securities memory ; the wrong ticker is suggested every time | mots: memory, memoire.csv, matches, ISIN, ticker, learning, recognition, offline -->

### The principle

When an import asks the Yahoo Finance search engine to recognise an ISIN code, a company name or a ticker, the answer is **kept** in the file `data/base/memoire.csv`. At the next import, the same identifier is recognised instantly, even without Internet.

Each line contains: the identifier (in capitals), the Yahoo Finance ticker found, the name of the security, the origin of the match and the date. No quantity, no amount, no portfolio data.

### The order of lookup

For an identifier to be recognised, the software looks in this order:

1. the built-in table of ETF ISINs (it takes priority over the memory, to repair a wrong match learned earlier);
2. the memory;
3. the local securities database;
4. the Yahoo Finance search engine, as a last resort.

Only answers obtained through the online search are added to the memory.

### A wrong match

If an identifier has been matched to the wrong security, the memory will propose it again at every import. Two remedies:

- for one file, in the import assistant ([[Open the import assistant]]), correct the [[Yahoo Finance ticker]] column of the securities step; this correction applies to the file but does not change the memory;
- to correct it permanently, delete the relevant line from `data/base/memoire.csv` (or the whole file). The software does not provide a screen for this.

### Shared between users

The memory is common to all users of the software on the computer: a security recognised by one is recognised for everyone.

## The built-in table of ETF ISINs
<!-- fiche: sources-isin-etf | questions: which ETFs are recognised without internet ; my ETF is not recognised at import ; list of built-in ETF ISINs ; is the cw8 isin recognised offline ; trade confirmation ETF abbreviated name ; why is my ETF recognised with the wrong ticker ; table of the 31 ETFs | mots: ETF, ISIN, built-in table, offline, trade confirmation, CW8, Amundi, iShares, Vanguard, recognition -->

Trade confirmations and statements often give only an ISIN code and an abbreviated name (for example "AM.C.C.40 UC.ETF C"). To recognise the most common ETFs **without Internet**, the software contains a table of **31 ETF ISINs**, each matched to a Yahoo Finance ticker.

### The ETFs in the table

| Family | ETFs (ticker) |
|---|---|
| France and eurozone equities | Amundi CAC 40 Acc (CACC.PA) and Dist (CAC.PA), Amundi Euro Stoxx 50 (MSE.PA), iShares Core DAX (EXS1.DE) |
| World equities | Amundi MSCI World (CW8.PA), Amundi PEA MSCI World (EWLD.PA), iShares MSCI World Swap PEA (WPEA.PA), iShares Core MSCI World (IWDA.AS), Vanguard FTSE All-World Acc (VWCE.DE) and Dist (VWRL.AS), iShares MSCI ACWI (IUSQ.DE), SPDR MSCI ACWI IMI (SPYI.DE) |
| US equities | BNP Paribas Easy S&P 500 (ESE.PA), Amundi PEA S&P 500 (PE500.PA), Amundi PEA Nasdaq-100 (PUST.PA), Vanguard S&P 500 (VUSA.AS), iShares Core S&P 500 (SXR8.DE), Invesco Nasdaq-100 (EQQQ.DE) |
| European and emerging equities | Amundi Stoxx Europe 600 (MEUD.PA), iShares Core MSCI Europe (EUNK.DE), Amundi PEA MSCI Emerging Markets (PAEEM.PA), Amundi MSCI Emerging Markets (AEEM.PA), iShares Core MSCI EM IMI (IS3N.DE) |
| Bonds | iShares Core Euro Govt Bond (EUNH.DE), iShares Euro Inflation Linked Govt Bond (IBCI.DE), iShares Core Euro Corporate Bond (EUN5.DE), iShares Euro High Yield Corp Bond (EUNW.DE), Xtrackers II Eurozone Government Bond 1C (DBXN.DE) |
| Money market and gold | Amundi Smart Overnight Return (CSH2.PA), Xtrackers II EUR Overnight Rate Swap (XEON.DE), Xetra-Gold (4GLD.DE) |

(PEA = Plan d'Épargne en Actions, the French equity savings plan.)

### Priority

This table is consulted **first**, before the securities memory and before any online search. It thus repairs any wrong match learned earlier.

### An ETF missing from the table

It is looked up in the memory, the local database, then, with Internet, through the Yahoo Finance search engine (by its ISIN, then by its name). The answer is then memorised. Offline and unknown to the memory, it cannot be recognised: the import reports it as not found.

### The trading venue chosen

The same ETF is often listed on several venues and in several currencies. The table fixes one specific listing for each ISIN: if you bought on another venue, the price used may differ slightly from yours.

## How an ISIN, a name or a Bloomberg code becomes a ticker
<!-- fiche: sources-identifiant-ticker | questions: how does the software find the ticker from the isin ; my file contains bloomberg codes ; is MC FP Equity recognised ; the software chose the wrong trading venue ; ticker without suffix MC or AIR ; recognition of the company name ; security not found at import ; EPA:MC google finance format | mots: ISIN, ticker, Bloomberg, Google Finance, Reuters, RIC, MIC code, trading venue, suffix, Yahoo search -->

The software works with **Yahoo Finance tickers** (`MC.PA` for LVMH in Paris, `AAPL` for Apple). At import, each identifier is first classified, then translated.

### 1. Already a Yahoo ticker

A code with an exchange suffix known to Yahoo (`.PA`, `.DE`, `.L`, `.AS`…), or a security from the reference file, is kept as it is.

### 2. Bloomberg, Google Finance and Reuters codes

They are converted **by rules, without Internet**:

| Written in the file | Becomes |
|---|---|
| `MC FP` or `MC FP Equity` (Bloomberg) | `MC.PA` |
| `AAPL US Equity` | `AAPL` |
| `EPA:MC` (Google Finance) | `MC.PA` |
| `NESN.S` (Reuters) | `NESN.SW` |
| `700 HK` | `0700.HK` |

MIC venue codes (`XPAR`, `XETR`…) and usual names ("Euronext Paris") are also recognised in a venue column.

### 3. ISIN code or company name

The software searches the table of ETF ISINs, the memory, then the local database (by ticker, by ISIN, then by name). Failing that, it queries the Yahoo Finance search engine with the ISIN, then with the label from the file. Among the answers (shares, ETFs, funds, indices), it prefers the venue of the ISIN's country (Paris for an `FR` ISIN, Frankfurt for `DE`…), then a listing in euros (Paris, Frankfurt, Amsterdam, Milan), then the United States.

### 4. Ticker without a venue (`MC`, `AIR`, `TSLA`)

The code may designate several securities. The software tries the possible listings (local database, search results and 9 venues: United States, Paris, Frankfurt, Amsterdam, Milan, Madrid, London, Zurich, Toronto). It keeps the one whose price, on the date of each buy or sell, best matches your prices, provided the median gap stays below 15%. Example taken from the code: "MC" bought at €740 in January 2024 corresponds to `MC.PA` (LVMH), not to `MC` (Moelis, around fifty dollars).

### If nothing matches

The security is declared not found and the import assistant opens: enter its ticker yourself in the [[Yahoo Finance ticker]] column.

## Converting currencies into euros
<!-- fiche: sources-devises | questions: how are securities in dollars converted ; which exchange rate is used ; London shares are in pence ; exchange rate on the day of purchase ; where do the exchange rates come from ; are my fees in euros ; currency risk in the performance ; exchange rates not found | mots: currencies, exchange rates, EURUSD, conversion, pence, GBp, currency risk, euro, USD, Yahoo Finance -->

Everything is expressed in euros. A security quoted in another currency is converted using the Yahoo Finance exchange rates.

### The currency of each security

The software asks Yahoo Finance for it. Offline, it takes the one in the local database, then, failing that, deduces it from the code: no suffix = US dollar, `.L` = pence, `.SW` = Swiss franc, `.T` = yen, and so on. The answer is kept in `cache_devises.csv`.

### The formula

```
price in euros = price in currency × factor / EURcurrency rate
```

- The `EURUSD=X` rate is the number of dollars for 1 euro.
- The factor is 1, except for London shares, quoted in **pence**: factor 0.01.

Examples:

- Apple at 200 USD, with €1 = 1.10 USD: 200 / 1.10 = **€181.82**.
- A London share at 1,250 pence, with €1 = 0.85 GBP: 1,250 × 0.01 / 0.85 = **€14.71**.

### Which rate, which day?

- a **buy, sell or dividend** is converted at the rate **of the day of the transaction**;
- the **day-by-day value** uses each day's rate;
- the **current value** uses the last known rate.

A day with no rate takes the last known rate. **Fees** are always considered to be in euros and are not converted.

### What this implies

The performance of a foreign security combines the change in its price and that of the currency: this is currency risk. A US share that gains 10% in dollars earns nothing in euros if the dollar loses about 10% against the euro over the same period.

### The limits

- The rate is the Yahoo Finance one, not the one applied by your bank.
- Offline, only currencies whose rate is in the local database (12 currencies) or in the cache can be converted.
- If a rate is missing, the analysis stops with the message "Taux de change introuvables" (exchange rates not found).
- Offline, for an uncommon venue, the currency deduced from the code may be wrong (the euro is used by default).

## ETF composition: where does the look-through analysis come from?
<!-- fiche: sources-composition-etf | questions: how does the software know the composition of my ETF ; is the country breakdown of my ETF accurate ; where do the msci world percentages come from ; is the look-through analysis reliable ; date of the ETF composition data ; my ETF is classed as unclassified ; why 73% united states in my world ETF | mots: look-through, transparency, composition, ETF, MSCI World, country breakdown, sectors, approximation, MSCI factsheets -->

The Exposures tab "breaks down" each ETF according to the composition of the index it tracks. These compositions **are not downloaded**: they are written into the software.

### The sources and their dates

- **MSCI World, MSCI ACWI, MSCI Emerging Markets, MSCI Europe**: the top 5 countries and the sectors come from the MSCI factsheets as of **30/09/2026**. The following countries are usual orders of magnitude, scaled to the factsheet's "other countries" total.
- **S&P 500, Nasdaq-100, Euro Stoxx 50, CAC 40, DAX, Russell 2000**, government and corporate bonds: 2025-2026 orders of magnitude, based on ETF issuers' factsheets.

The MSCI World thus has 72.94% in the United States: a €10,000 MSCI World ETF is counted as about €7,300 of US equities. The screen reminds you: "approximation as of 30/09/2026".

### How an ETF is linked to an index

1. through a table of 58 ETF tickers (CW8.PA and IWDA.AS for the MSCI World, ESE.PA for the S&P 500…);
2. otherwise, through words in the name: "All-World" or "ACWI", "Emerging", "World", "S&P 500", "Stoxx Europe 600"…;
3. a name containing "Hedged" or "couvert" is considered hedged against currency risk.

A fund that matches nothing stays "Unclassified".

### Approximations to be aware of

- Actual weights change every day; the project estimates the gap at a few points at most, as the weights of the major indices move little from one year to the next.
- The same sector mix is applied to every country of an index: this is a calculation assumption.
- An ETF is assumed to track its index exactly.
- Dated data must be reviewed once a year in the project's code.

### Other fixed reference data

Performance attribution uses the regional weights of the MSCI ACWI IMI as of 30/06/2026, also written into the software.

## How each security is classified (country, sector, asset class)
<!-- fiche: sources-classification | questions: where do the country and sector of my securities come from ; my share is unclassified ; what is referentiel.csv ; my security is classed in the wrong country ; why is my bond counted as an equity ; where is the duration of bond funds ; add a security to the reference file ; default asset class | mots: classification, reference file, referentiel.csv, country, region, sector, asset class, duration, Unclassified, GICS -->

### Two sources, in this order

1. **The project's reference file**, `data/referentiel.csv`: 86 securities described by hand, with the columns ticker, name, country, region, sector, class (Equities, Bonds, Gold, Money market) and duration for bond funds. It **always prevails**.
2. **The local securities database** (`data/base/titres.csv`), for all other securities.

### How the local database classifies a security

- **Country and region**: according to the **trading venue** of the ticker (`.PA` = France, `.DE` = Germany, no suffix = United States…), not according to the company's head office. A foreign company listed in Paris is therefore classed as "France".
- **Sector**: the sector given by the index's Wikipedia page (GICS sectors, translated), when there is one.
- **Asset class**: "Equities" for shares; for the ETFs on the list, "Bonds" or "Gold" depending on their name.

### Default values

- A security with no known country, region or sector is classed as **"Unclassified"**.
- A security with no known asset class is considered to be an **equity**: this is the cautious assumption for measuring risk.
- **Duration** is known only for the bond funds in the reference file; elsewhere, it is absent.

### Correcting a classification

The software does not provide a screen for changing the classification of a security. From the source code, you can add or correct a line of `data/referentiel.csv`, respecting its columns: it will take priority over the local database. In the installed version, this file is in the program's `data` folder and would be replaced by a new installation.

## Benchmark indices and composite indices
<!-- fiche: sources-indices | questions: which benchmark indices are offered ; how is the 60 40 blended index calculated ; does the benchmark include dividends ; why compare with an ETF rather than the index ; composite index rebalanced every month ; how do I change the benchmark ; the cac 40 excludes dividends ; where does the index history come from | mots: benchmark, benchmark index, composite, blended, 60/40, monthly rebalancing, MSCI World, CAC 40, €STR, dividends reinvested -->

The benchmark index is chosen in [[Settings]], at the bottom of the sidebar, under [[Benchmark index]]. By default: the MSCI World, represented by the CW8 ETF.

### The four families

| Family | Indices | Represented by |
|---|---|---|
| Equities | MSCI World, MSCI ACWI, S&P 500, Nasdaq-100, Stoxx Europe 600, MSCI Emerging Markets | accumulating ETFs: dividends reinvested |
| Equities | Euro Stoxx 50, CAC 40 | the price index: **excluding dividends** |
| Bonds | Eurozone government bonds; euro corporate bonds | an accumulating ETF (coupons reinvested); an "excluding coupons" ETF |
| Money market | €STR | an accumulating ETF (interest reinvested) |
| Blended | conservative 20/80, balanced 60/40, dynamic 80/20 | calculated by the software |

The label of each index says whether it includes dividends. Comparing with an index that excludes dividends flatters the portfolio: the project estimates this at about 3% a year for the CAC 40.

### Why an ETF?

An accumulating ETF includes dividends in its price, just as your performance includes your dividends: the comparison is fair. Each index has several "candidate" ETFs; the first one whose history is available is used (for example CW8.PA, otherwise IWDA.AS).

### The blended indices

```
Composite = X% equity sleeve + Y% bond sleeve, rebalanced at every month end
```

- Equity sleeve: MSCI World (CW8.PA, otherwise IWDA.AS, otherwise EUNL.DE).
- Bond sleeve: eurozone government bonds (DBXN.DE, otherwise EUNH.DE).
- Prices converted into euros, series in base 100.
- On the last trading day of each month, the weights are reset to their target.

Example for the 60/40: over a month in which equities gain 10% and bonds lose 2%, the index gains 0.60 × 10% + 0.40 × (−2%) = **5.2%**. The weights then start again from 60/40.

### The limits

An ETF tracks its index with a small gap (fees, replication). The composite includes neither fees nor rebalancing costs.

## The risk-free rate
<!-- fiche: sources-taux-sans-risque | questions: which risk-free rate is used ; where does the 2.5% rate come from ; how do I change the risk-free rate ; ecb rate for the sharpe ratio ; is the risk-free rate historical ; why does the sharpe change when I change the rate ; €str or deposit rate | mots: risk-free rate, ECB, deposit facility, €STR, Sharpe ratio, Sortino, alpha, settings, 2.50% -->

### The default value

**2.50% per year**, which is the deposit facility rate of the European Central Bank. The project's code gives it as in force since 16/09/2026 (source cited: ECB, "Key ECB interest rates"). The €STR, the overnight interbank rate, is very close to it.

This rate is used for the **Sharpe ratio**, the **Sortino ratio** and **alpha**.

### It is not downloaded

The software does not fetch this rate from the Internet: it is a **fixed value**, written into the code. When the ECB changes its rates, it is updated only with a new version of the software, or by yourself.

### Changing it

In the sidebar, open [[Settings]] and change [[Risk-free rate (% per year)]]: from 0 to 10%, in steps of 0.25 points. The tooltip recalls the ECB value. All the indicators concerned are recalculated.

### The simplification to be aware of

The rate is **constant over the whole period analysed**, whereas it has varied in the past (the code cites 4% in early 2024 and 2% in mid-2025). Over a long period, the Sharpe ratio and alpha are therefore approximate. The project notes, as a possible improvement, using the historical €STR series.

### For comparison

Choosing the benchmark index "Money market €STR (ETF, interest reinvested)" shows what a money-market investment would have earned over the same period, based on the price of a money-market ETF.

## The world map background
<!-- fiche: sources-fond-de-carte | questions: the world map is not displaying ; where do the country outlines come from ; empty map without internet ; what is pays.geojson ; natural earth ; french guiana shows in colour on the map ; why is antarctica not on the map | mots: world map, map background, Natural Earth, GeoJSON, pays.geojson, country outlines, offline, Plotly -->

The world map in the Exposures tab colours each country according to its weight in the equity sleeve.

### The source

The country outlines come from **Natural Earth**, a public-domain mapping database, at a scale of 1:110,000,000. The file is downloaded from GitHub, or failing that from the jsDelivr service, then simplified:

- coordinates rounded to about 1 km, for a file of about 400 KB;
- Antarctica removed (no stock exchange);
- for France, only the mainland is kept: otherwise, French Guiana, drawn together with France, would be coloured by a French share.

It is saved in `data/base/pays.geojson`.

### When it is downloaded

Only once: when the database is built, when the installer is made, or, failing that, by the dashboard the first time it needs it (a single attempt each time the software is launched). After that, the map is displayed without Internet.

### If the file is missing

The map is then drawn with the map background that the charting library downloads itself: without Internet, it stays empty. The rest of the tab is not affected.

### What the map does not show

A note under the map gives the share of the portfolio that is "not on the map", by asset class: bonds, gold, money market, or equities with no known country. ETFs are allocated there according to the approximate composition of their index.

## What the software checks
<!-- fiche: sources-controles | questions: what checks does the software carry out ; does the software check my purchase prices ; how are duplicates detected ; price far from the market price what does it mean ; sale impossible only holding ; checking imported data ; does the software detect input errors ; data quality control | mots: checks, verifications, quality control, duplicates, price far from market, 25%, consistency, ISIN, check digit, validation -->

Here, one by one, are the checks that are actually in place.

### When reading the file

- Only the types ACHAT, VENTE and DIVIDENDE (buy, sell, dividend) are accepted; negative prices and quantities are refused.
- **Sale not possible**: selling more securities than are held on that date stops the analysis, with a message giving the date and the quantities.
- The columns of an unknown file are accepted automatically only if their names are meaningful, or if the numbers are consistent (quantity × price, plus or minus fees, equals the amount to within 1% on at least 80% of the rows). Otherwise, the import assistant opens.
- An **ISIN code** is recognised only if its check digit is correct; in a PDF, it must in addition contain at least 6 digits.
- Ambiguous dates (day/month or month/day) are detected and the choice made is reported.

### Prices compared with the market

At import, with Internet, each buy or sell price is compared with the security's closing price that day:

- the software recognises a price entered in euros, in currency or in pence, and brings it back to the quotation unit;
- a price more than 25% above (or 20% below) the day's price is flagged: "price(s) far from that day's market price", with the median gap, "check the ticker, currency or a stock split".

Without Internet, the summary says "Prices not checked against market data (no connection)."

### When adding transactions

- **Duplicates**: a transaction with the same date, same security, same type, same quantity and the same price to within 0.5% is unticked automatically.
- Transaction dated in the future, zero quantity or price, sale greater than the quantity held: blocking alerts.

### During the analysis

- A missing price, a missing history or an exchange rate that cannot be found stops the analysis with a message naming the securities concerned, rather than giving a wrong result.
- The source of the prices (live or cache) and the date of the data are always displayed.

### In the project's tests

The automatic tests check, among other things, that the gain calculated day by day falls back exactly on the total gain. These tests are run by the developer, not while you are using the software.

## What the software does not check
<!-- fiche: sources-limites | questions: what are the limits of the data ; does the software compare several price sources ; is a wrong yahoo price detected ; does the software detect a delisted security ; is the data guaranteed ; can I rely on the figures for my tax return ; limits of the software on data | mots: limits, reliability, single source, data errors, outlier price, delisted security, corporate actions, guarantee, disclaimer -->

To be honest about reliability, here is what is **not** checked.

### Prices

- **A single source**: all prices come from Yahoo Finance. The software does not compare them with any other source (Euronext, Bloomberg, your broker).
- **No detection of outlier prices** in the history: an abnormal one-day jump, a missing value or a frozen price are not spotted. A day with no price simply takes the last known price.
- **No freshness check per security**: a suspended or delisted security keeps its last known price, with no alert.
- **No adjustment for corporate actions**: splits, reverse splits, spin-offs, mergers and ticker changes are not handled.
- **No download of dividends**: only those in your file count.
- The 25% price check takes place only **at import**, with Internet, and only on buys and sells.

### Other data

- The quotation currency, once known, is not checked again.
- Recognition of an ISIN by the search engine may choose a different trading venue from yours.
- ETF composition, security classification and the risk-free rate are fixed, dated values, not continuously updated.
- The country of a share in the local database is that of its trading venue.

### Your own data

The software cannot know whether you have forgotten a transaction, a dividend or fees. It calculates correctly from what you give it.

### As a result

The results are reliable for analysis and learning, but do not replace the official statements of your financial institution, in particular for a tax return. They do not constitute investment advice.

## A price looks wrong: what should I do?
<!-- fiche: sources-cours-faux | questions: the price shown is wrong ; my current value looks odd ; huge loss on a security although the price went up ; the price of my share is not right ; the price is in pence instead of pounds ; how do I correct a price ; my ETF has a different price from my broker ; my portfolio value is inconsistent | mots: wrong price, price error, incorrect price, troubleshooting, ticker, trading venue, currency, pence, split, correction -->

The software does not let you enter a price by hand: you have to find the cause. Proceed in this order.

### 1. Check the source and the date

Does the banner say "Cached prices (offline)"? If so, the prices date from the day shown in the sidebar. Reconnect to the Internet and click [[Refresh prices]].

### 2. Check the ticker and the venue

In the Holdings or Transactions tab, look at the ticker used. `MC` (Moelis, in New York) is not `MC.PA` (LVMH, in Paris); an ETF listed in London in dollars does not have the same price as its equivalent listed in Paris in euros. If the ticker is wrong, correct your file, or import it again with [[Open the import assistant]] and correct the [[Yahoo Finance ticker]] column.

### 3. Check the currency

London shares are quoted in pence (1,250 pence = 12.50 pounds). The price in your file must be in the security's quotation currency, and the fees in euros. The import summary shows the conversions made.

### 4. Think of a stock split

A loss of about 50%, 67% or 90% that appeared suddenly suggests a stock split. Correct the transaction as explained in the entry "Dividends and stock splits: what an unadjusted price implies".

### 5. Compare with another source

Compare the price with your broker's site, with that of the exchange concerned, or with the security's page on Yahoo Finance. If Yahoo Finance itself shows a wrong value, the software picks it up: wait for it to be corrected, then click [[Refresh prices]]. The new values then replace the old ones in the local database.

### 6. Check your transactions

A wrongly entered quantity or price distorts the value as much as a wrong price. Use [[Edit transactions]] in the Transactions tab to correct it.

## How do you make sure the prices are right?
<!-- fiche: sources-fiabilite | questions: how do you make sure the prices are right ; is the data reliable ; can I trust yahoo finance prices ; is the source safe ; are the figures correct ; how much credit should I give the results ; is yahoo finance reliable for a thesis ; what do I tell the jury about data reliability | mots: reliability, trust, data quality, Yahoo Finance, verification, accuracy, free source, thesis defence -->

### The honest answer

The software **does not guarantee** the accuracy of the prices: it takes them from Yahoo Finance, a free and widely used source, but with no quality commitment, and **without comparing them with a second source**. Nor does it look for outliers in the history.

### What it does to limit errors

1. **A raw, traceable price**: the closing price not adjusted for dividends, which anyone can compare with the one shown by the exchange or by a broker.
2. **A source always displayed**: live or cache, with the date of the data.
3. **A check of your prices at import**: each buy and sell price is compared with the Yahoo Finance closing price of the same day. A gap of more than 25% is flagged. This cross-check reveals an error in your file just as well as a wrong security or an abnormal price.
4. **Recognition of securities through prices**: a ticker without a venue is accepted only if its price matches your prices (median gap below 15%).
5. **Stops rather than approximations**: a missing price, history or exchange rate stops the analysis with a clear message.
6. **A database that corrects itself**: each download replaces the old values with those from Yahoo Finance.
7. **Tested calculations**: the formulas are verified by automatic tests, on examples whose result is known.

### What you can say

For academic work, a fair wording is: "Prices are the daily closing prices from Yahoo Finance, not adjusted for dividends; transaction prices were checked against these prices, with an alert threshold of 25%; the prices were not cross-checked against a second source."

### To go further

For an important figure, check it yourself against a second source: the exchange's site, your broker or your institution's statement.

## Offline: up to what date do the prices go?
<!-- fiche: sources-hors-connexion-date | questions: up to what date are prices available without internet ; the prices stop at an old date ; data as of which date ; what does cache local du mean ; how do I get more recent prices offline ; when is the shipped database from ; my prices do not go up to today | mots: offline, date of the prices, local cache, local database, update, data as of, last date -->

### There is no fixed date

Offline, prices stop at the **last date known** on your computer. It depends on:

- the database shipped with your version, updated by the creator at the time of building it;
- your own online analyses: each history downloaded is added to the database;
- the cache of the last analysis.

### Where to read this date

- **"Data as of"**, in the banner at the top of the page: the date of the last price in the history used;
- the **"Prices"** line at the bottom of the sidebar: "cache local du" followed by a date, the oldest of the sources used for current prices (this text is shown in French);
- the **"Cached prices (offline)"** badge, with an orange dot.

The calculations remain correct, but are stopped at this date: the current value is the value at the date of the last known price.

### Getting more recent prices

- Reconnect to the Internet, then click [[Refresh prices]]: the missing prices are downloaded and added to the database.
- From the source code, `python construire_base_titres.py --mise-a-jour` updates the whole database in a few minutes.
- Installing the latest version of the software brings a more recent database.

### A security with no prices at all

A security that is absent from the database, the cache and the memory has no prices offline: the analysis stops with a message that names it. It will be available from the first analysis with Internet.

### Not all securities stop on the same day

The prices of all the securities in a portfolio do not necessarily stop on the same day. For each security, the software takes its last known price.
