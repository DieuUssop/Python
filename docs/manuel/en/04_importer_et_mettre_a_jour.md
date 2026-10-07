# Importing and updating your portfolio
<!-- chapitre: import | ordre: 4 -->

This chapter explains how to give your transactions to the software: which files it accepts (CSV, Excel, PDF), the project format and its template, the automatic reading of bank or broker exports, the import assistant, the recognition of securities (ticker, ISIN, name, Bloomberg, Google or Reuters codes) and of currencies. It then describes how to update a portfolio: adding new transactions, duplicates, checks, correcting or deleting a transaction, and undoing a change. It ends with common errors and a full worked example.

## Which files can be imported into the software?
<!-- fiche: import-fichiers-acceptes | questions: which files can I import ; what file format does the software accept ; can I use an excel file ; does it take the PDFs from my bank ; can I import a csv ; my xls file wont work ; can I import a screenshot or a photo ; import from boursorama or bourse direct ; does the software connect to my broker | mots: import, accepted formats, CSV, Excel, xlsx, PDF, statement, trade confirmation, broker export, file -->

The software reads your transactions from a file that you send to it. It does not connect to your bank or to your broker.

### The three accepted formats

| Format | Extension | Examples |
|---|---|---|
| CSV (text) | `.csv` | File in the project format, broker export, file saved from Excel |
| Excel | `.xlsx` | Personal spreadsheet, bank export |
| PDF | `.pdf` | Transaction statement presented as a table, trade confirmation (a confirmation of an executed order) |

The upload areas accept only these three extensions. The old Excel format `.xls` is not accepted: open the file in Excel and save it as `.xlsx` or as CSV. The software recognises the real nature of a file from its content (a PDF starts with `%PDF-`, an `.xlsx` is a ZIP archive), then reads it accordingly.

### What the file must contain

It must contain a **history of dated transactions**: purchases, sales, and possibly dividends. A simple list of positions (securities and quantities held today, with no purchase dates) does not allow performance to be calculated. Three pieces of information are essential for each row: the **date**, the **security** and the **quantity**, together with the **unit price or the total amount**.

### The format does not need to be perfect

The file may have its own column names, in French or English, header lines above the table, ISIN codes instead of tickers, numbers in the French style or amounts in euros for foreign securities: automatic detection takes care of it (see the following fiches). If it has any doubt, the import assistant opens.

### What is not possible

- a photo or screenshot in image format (`.png`, `.jpg`) is not accepted;
- a scanned PDF is read only if a character recognition (OCR) engine is installed, and only for trade confirmations (see the fiche on image PDFs);
- there is no automatic connection to a bank account.

## What happens when I upload a file?
<!-- fiche: import-envoyer-fichier | questions: how do I import my portfolio ; where is the button to upload my file ; I added my file and nothing happens ; how do I load my transactions ; does the uploaded file replace my portfolio ; why does the assistant open instead of the dashboard ; how do I go back to my saved portfolio after an upload ; file upload | mots: upload a file, upload, sidebar, Data, automatic import, detection, drag and drop, loading -->

### Where to upload the file

In the sidebar, under "Data", use the [[Upload a file (CSV, Excel or PDF)]] area: drag the file onto it or click to choose it. The uploaded file takes **priority** over the portfolio selected in the list just above: as long as it is present in the upload area, it is the one being analysed.

### What the software does

1. The message "Reading the file and checking prices against market data..." is displayed.
2. The software reads the file, recognises the columns, converts the security codes into Yahoo Finance tickers and checks the prices against market data.
3. **If the result is reliable**, the portfolio is analysed immediately. A box in the sidebar summarises what was understood, for example "File recognised automatically: 12 transaction(s), 5 security(ies).".
4. **If any doubt remains** (unrecognised column, security not found, unreadable row), the **import assistant** is displayed in place of the dashboard, already pre-filled: you just need to check and confirm.

You can restart the reading manually at any time with the [[Open the import assistant]] button, visible under the upload area as long as a file is present.

### The file is not kept automatically

An uploaded file is kept only for the session. To find it again next time:

- if you are signed in, the [[Save to my space]] block appears under the upload area once the file has been analysed;
- otherwise, the software reminds you: "To keep this file, sign in ("Sign in", at the top of the sidebar).".

### Going back to another portfolio

Remove the file from the upload area (small cross to the right of its name): the portfolio selected in the "Data" list is analysed again.

## The project format: which columns should my file have?
<!-- fiche: import-format-projet | questions: what is the format of the transactions file ; which columns are needed ; how do I prepare my csv file ; date type ticker nom quantite prix frais ; which currency should I put the price in ; are fees in euros or dollars ; what is the yahoo ticker ; which date format should I use ; can I put decimals in the quantity | mots: project format, columns, header, date, type, ticker, nom, quantite, prix, frais, trading currency, file structure -->

The project format is a CSV file with seven columns, one row per transaction:

```
date,type,ticker,nom,quantite,prix,frais
2024-01-15,ACHAT,CW8.PA,Amundi MSCI World,10,420.00,2.50
2024-02-01,ACHAT,MC.PA,LVMH,3,780.00,2.00
2024-05-22,DIVIDENDE,MC.PA,LVMH,0,39.00,0.00
2024-09-18,VENTE,MC.PA,LVMH,1,700.00,2.00
```

### Meaning of each column

| Column | Content |
|---|---|
| `date` | Transaction date, preferably in YYYY-MM-DD format. A day with no trading is attached to the next trading day. |
| `type` | `ACHAT` (buy), `VENTE` (sell) or `DIVIDENDE` (dividend) (see the fiche on transaction types) |
| `ticker` | The security's code on Yahoo Finance: `MC.PA` (LVMH in Paris), `AAPL` (Apple), `ULVR.L` (Unilever in London). An ISIN code is also accepted on upload: it is converted. |
| `nom` | Name of the security, free text (used for display) |
| `quantite` | Number of securities bought or sold; 0 for a dividend. Fractional units are accepted. |
| `prix` | Unit price, **in the security's trading currency** (dollars for Apple, pence for London); for a dividend, the total amount received |
| `frais` | Brokerage fees for the transaction, **always in euros** |

### The two currency rules to remember

- The **price** is in the currency in which the security is quoted on Yahoo Finance. The software converts it into euros itself, at the exchange rate of the transaction day.
- **Fees** are always in euros, whatever the security.

If your statement gives prices already converted into euros, that is not a problem: on upload, the software compares each price with the actual price of the day and converts back if necessary (see the fiche on currencies).

### Useful details

- The order of the rows is free: the software sorts the transactions by date.
- Quantities and prices must be positive: it is the type that indicates the direction. In a broker export, a negative quantity is accepted and made positive.
- Both the dot and the comma are accepted as the decimal separator, and the semicolon as the column separator (see the fiche on broker exports).
- The [[File template]] button in the sidebar downloads an example ready to be completed.

## Buy, sell, dividend: what goes in the price and the fees?
<!-- fiche: import-types-operations | questions: how do I enter a dividend ; what do I put in price for a dividend ; is zero quantity normal for a dividend ; buy sell dividend which types are accepted ; how do I record a bond coupon ; are fees included in the price ; how is the cost basis calculated with fees ; how do I enter a sale ; dividend in dollars | mots: ACHAT, VENTE, DIVIDENDE, coupon, distribution, cost basis, PRU, brokerage fees, total amount, transaction type -->

The project format knows only three transaction types. Each uses the columns in a specific way.

| Type | `quantite` | `prix` | `frais` |
|---|---|---|---|
| `ACHAT` | Number of securities bought | Unit purchase price (trading currency) | Brokerage fees in euros |
| `VENTE` | Number of securities sold (positive) | Unit selling price (trading currency) | Brokerage fees in euros |
| `DIVIDENDE` | 0 | **Total amount received** for the row (trading currency) | Any fees in euros (often 0) |

### The case of the dividend

For a dividend, the `prix` column does not contain the dividend per share but the **total amount** received. Example: 3 LVMH shares with a dividend of €13 per share give the row `2024-05-22,DIVIDENDE,MC.PA,LVMH,0,39.00,0.00` (3 × 13 = 39). The amount is also expressed in the trading currency: in dollars for a US share, in pence for a London share. The software adds this amount, less the `frais` column, to the security's total dividends. Bond coupons and ETF distributions are entered in the same way.

### How fees are counted

- **Purchase**: fees are included in the unit cost basis (PRU, the average purchase cost per unit). `New PRU = (quantity held × old PRU + quantity bought × price + fees) / new quantity`. Example: 3 LVMH bought at €780 with €2 of fees give a PRU of (3 × 780 + 2) / 3 = €780.67.
- **Sale**: fees reduce the realised gain. `Gain = quantity sold × (selling price − PRU) − fees`.
- The fees of all transactions are added up in the "Brokerage fees" indicator.

### A sale cannot exceed the quantity held

Selling more securities than you own at that date causes an error during analysis ("Sale impossible on …"). Short selling is not supported.

### Other transactions

Custody fees, transfers, taxes or corporate actions that are neither purchases, nor sales, nor dividends have no place in the project format. In a broker export, these rows are recognised and ignored (see the fiche on recognised transaction types).

## Downloading and filling in the file template
<!-- fiche: import-modele | questions: where do I find a file template ; example csv file to fill in ; what is modele_transactions.csv ; how do I create my transactions file in excel ; I dont have a broker export what do I do ; transactions file template ; the template opens in a single column in excel ; download an example file | mots: file template, template, example, modele_transactions.csv, Excel, data entry, CSV -->

### Where to find it

In the sidebar, under "Data", click [[File template]]. The file `modele_transactions.csv` is downloaded. It contains the header of the project format and four example rows:

| date | type | ticker | nom | quantite | prix | frais |
|---|---|---|---|---|---|---|
| 2024-01-15 | ACHAT | CW8.PA | Amundi MSCI World | 10 | 420.00 | 2.50 |
| 2024-02-01 | ACHAT | MC.PA | LVMH | 3 | 780.00 | 2.00 |
| 2024-05-22 | DIVIDENDE | MC.PA | LVMH | 0 | 39.00 | 0.00 |
| 2024-09-18 | VENTE | MC.PA | LVMH | 1 | 700.00 | 2.00 |

### How to use it

1. Open the file in Excel, LibreOffice or a text editor.
2. Replace the example rows with your own transactions, keeping the first row (the column names).
3. Save, as you prefer, as CSV (comma or semicolon separator) or as an Excel `.xlsx` workbook.
4. Upload the file with the [[Upload a file (CSV, Excel or PDF)]] area.

### Data entry tips

- Find the ticker of each security on Yahoo Finance (for example `MC.PA` for LVMH in Paris). If you do not know it, you can write the ISIN code in the `ticker` column: it will be converted on upload.
- Write dates in YYYY-MM-DD or DD/MM/YYYY format; both are recognised.
- Excel often re-saves numbers with a decimal comma and a semicolon between columns: the software accepts both variants.
- If, when opened in Excel, everything appears in the first column, this is not a problem for the software: an entire row placed between quotation marks in column A is also recognised.

### No file at all?

You can also start from an example portfolio and enter your orders by hand with [[Add transactions]], then download the resulting file (see the fiches on manual entry and on using the software without an account).

## Importing my bank or broker export
<!-- fiche: import-export-courtier | questions: how do I import my broker export ; my file has column names in English ; the columns arent named like in the template ; does an export from degiro boursorama or trade republic work ; my csv has semicolons ; there are header lines before the table ; which column names are recognised ; excel file with several sheets ; weird accents in my file | mots: broker export, statement, columns, synonyms, separator, semicolon, tab, encoding, Excel sheet, header, column names -->

A broker export does not need to be transformed before uploading. The software reads it as it is, in four stages: reading the table, recognising the columns, converting the securities, checking the currencies.

### Reading the table

- **Separator**: for a CSV, the software counts, over the first 40 non-empty lines, the semicolons, commas, tabs and vertical bars `|`, and keeps the most frequent.
- **Encoding**: the text is read as UTF-8; failing that, as Windows-1252 (the encoding of older versions of Excel), which preserves accents.
- **Excel sheet**: if the workbook has several sheets, the one with the most filled cells is chosen (the transaction table rather than a notes sheet). The assistant lets you choose another one.
- **Column header row**: among the first 30 rows, the software keeps the fullest one that contains at least 60% text. The rows above it ("Statement of transactions", account number, date of issue) are ignored. If this row contains a date or an ISIN code, there is no header row: the columns are then named "Column 1", "Column 2"… and recognised by their content.
- **What is discarded**: empty rows, rows with neither a date nor a security ("Total" row, note below the table), and a small table placed beside the main table if it is separated from it by an empty column.

### Recognised column names

Names are compared without accents or capital letters. A name is recognised if it is identical to one of the names below, or if it starts with one of them followed by a space ("Quantité exécutée", "Cours (EUR)").

| Information | Examples of recognised names |
|---|---|
| Date | date, date opération, date d'exécution, date de valeur, trade date, transaction date, execution date, jour |
| Type | type, opération, sens, nature, transaction type, side, action, mouvement |
| Security | ticker, symbole, symbol, code, isin, code isin, bloomberg, bbg, ric, code reuters, valeur, titre, instrument, produit, product, security |
| Name | nom, name, libellé, désignation, nom du titre, security name, description |
| Quantity | quantité, qté, qty, quantity, nombre, nombre de titres, nb titres, parts, shares, units |
| Unit price | prix, prix unitaire, cours, cours d'exécution, price, unit price, execution price |
| Total amount | montant, montant net, montant brut, montant total, total, amount, net amount, montant en eur |
| Fees | frais, frais de courtage, courtage, commission, commissions, fees, fee, frais totaux |
| Currency | devise, currency, monnaie, devise de cotation, ccy, cur |
| Exchange | place, place de cotation, marché, bourse, exchange, market, mic, venue, lieu d'exécution |

Columns named commentaire, remarque, note, observation, memo or info are never interpreted. All other unneeded columns are simply ignored.

### What if the names mean nothing?

Columns are also recognised by their **content** and by the **consistency of the figures** (see the next fiche). A file with no header row, or with columns named "A, B, C", can therefore still be understood.

## How does the software recognise the columns in my file?
<!-- fiche: import-detection-colonnes | questions: how does automatic detection work ; how does the software guess the columns ; my file has no header row ; it mixed up the price and the amount ; why does it say not certain about quantities prices and amounts ; when is an import considered reliable ; recognition by content ; qty x price = amount | mots: automatic detection, column mapping, content, consistency, quantity × price, amount, confidence, no header, algorithm -->

Automatic detection proposes, for each piece of information (date, type, security, name, quantity, unit price, total amount, fees, currency, exchange), the column of the file that corresponds to it. Each column is used only once.

### Step 1: names and content

For the date, type, security, name and currency, the software combines the name of the column and what it contains:

| Information | Clue drawn from the content |
|---|---|
| Date | cells written as dates (15/01/2024, 2024-01-15…) and readable |
| Security | ISIN codes whose check digit is correct, Bloomberg, Google or Reuters codes, short capitalised tickers |
| Type | transaction words ("Achat", "Vente", "Coupon"…), with few distinct values |
| Currency | codes EUR, USD, GBP, GBX, CHF, JPY, CAD, AUD, HKD, DKK, SEK, NOK, CNY, SGD |
| Name | fairly long free text that is neither a code, nor a type, nor a currency |

A column of numbers (quantity, price, amount, fees) is accepted on the basis of its name only if at least 60% of its cells are numbers.

### Step 2: consistency of the figures

Number columns left without a meaningful name are told apart by calculation. The software tries the possible combinations and keeps the one in which, most often:

`quantity × price ± fees = amount` (within 1%)

It also favours a quantity in whole numbers, and fees that are small relative to the amount (less than 5%).

Example: in a file with no column headers containing `3 ; 740.00 ; 2222.00 ; 2.00`, only the reading "3 securities at €740 plus €2 of fees = €2,222" works out: the first column is the quantity, the second the price, the third the amount, the fourth the fees.

### When is the result considered reliable?

The analysis starts directly if all these conditions are met:

- the date, security, quantity, and price or amount each have a column;
- the number columns have a recognised name (quantity, and price or amount), **or** the relationship quantity × price ± fees = amount holds on at least 80% of the rows;
- the date column has a recognised name, or at least 90% of its cells are dates;
- all the securities have been identified;
- no row is unreadable (missing date, price, quantity or security).

Otherwise, the import assistant opens; the "Why is the assistant opening?" panel gives the reason, for example "Columns recognised, but not certain about the quantities, prices and amounts.".

## Which date and number formats are recognised?
<!-- fiche: import-dates-nombres | questions: which date format is accepted ; my dates are in american format ; the software swaps the day and the month ; is 03/04/2024 the 3rd of April or the 4th of March ; numbers with comma or dot ; does 1 234,50 work ; amount in brackets negative ; why is a date unreadable ; euro symbol in the amounts | mots: date format, DD/MM/YYYY, MM/DD, ISO, day/month, decimal separator, comma, thousands, negative numbers, unreadable date -->

### Dates

Recognised formats: `2024-01-15`, `15/01/2024`, `15-01-2024`, `15.01.2024`, as well as dates followed by a time (`2024-01-15 00:00:00`, or `2024-01-15T10:30`). Excel cell dates in date format are read directly.

**Day/month or month/day?** For a date such as 03/04/2024, the software examines the whole column:

- if even one date has a first number above 12 (for example 13/04/2024), the format is day/month (French);
- if a date has a second number above 12 (04/13/2024), the format is month/day (American);
- if nothing allows a decision, the day/month format is kept, and the summary says so: "Dates read as day/month (DD/MM).". A detected American format is flagged with "Dates read in US format (MM/DD).".

Dates written out in words ("15 janv. 2024") are not recognised: the row is then flagged with the reason "an unreadable date". Also prefer four-digit years.

### Numbers

The software removes spaces (including non-breaking ones), apostrophes and the symbols €, $, £, EUR and USD, then interprets the decimal separator:

| Written in the file | Read as |
|---|---|
| `1 234,50 €` | 1,234.5 |
| `1.234,50` | 1,234.5 (the last separator is the decimal one) |
| `1,234.50` | 1,234.5 |
| `1.234.567` or `1,234,567` | 1,234,567 |
| `(12,5)` | −12.5 |
| `12,50-` | −12.5 |

Beware of one ambiguous case: a number containing only one separator is always read as a decimal number. `1,234` and `1.234` are therefore both worth 1.234, not one thousand two hundred and thirty-four. If your export writes thousands this way, check the quantities and amounts that were read.

### The sign

The sign of a quantity is used to spot sales when the file has no type column; it is then removed. Fees are always made positive.

## Which transaction types are recognised in a statement?
<!-- fiche: import-types-reconnus | questions: is achat comptant recognised ; how does the software know if its a buy or a sell ; my file has no type column ; are custody fees imported ; why are rows ignored on import ; transfer in my statement ; is a negative quantity a sale ; buy sell in english ; redemption of units | mots: transaction type, buy, sell, dividend, coupon, subscription, redemption, achat, vente, ignored rows, custody fees, transfer -->

### The recognised words

Each value in the type column is classified according to the words it contains (ignoring accents and capital letters):

| Classified as | Recognised words |
|---|---|
| Buy | achat, buy, bought, purchase, souscription, acquisition, acheté |
| Sell | vente, sell, sold, sale, cession, vendu, rachat |
| Dividend | dividende, dividend, coupon, distribution, détachement, revenu |
| Ignored | any other value: frais de garde (custody fees), virement (transfer), taxe, impôt (tax)… |

So "Achat Comptant" is a purchase, "Coupons/Dividende" a dividend, and "Rachat" a sale (the redemption of fund units).

### Ignored rows

Rows of another type are not errors: they do not concern a security and are discarded. The summary says so, for example "2 row(s) ignored (custody fees, transfers...).". In the assistant, you can change the interpretation of each value (step 3).

### Without a type column

If the file has no type column, the software decides according to the quantity:

- positive quantity: purchase;
- negative quantity: sale;
- zero or empty quantity with an amount: dividend.

The assistant reminds you: "Without a "Transaction type" column: a negative quantity is read as a sale, a positive quantity as a purchase.".

### In a PDF trade confirmation

The direction is searched for in the text (achat, vente, souscription, rachat, buy, sell, dividende, coupon…). If no word is recognised, the transaction is read as a purchase: check it.

## My statement gives the total amount and not the unit price
<!-- fiche: import-montant-prix | questions: my file has no unit price only the amount ; how is the price calculated from the amount ; net amount or gross amount which to choose ; does the total amount include fees ; the calculated price is wrong ; debit credit instead of price ; the unit price doesnt come out right | mots: total amount, net amount, gross amount, unit price, fees included, price derivation, debit, credit -->

The unit price is not mandatory: a total amount column is enough. The software works out the price from it.

### The calculation

If the amount is **net** (fees included, that is, the sum actually debited or credited), which is the default setting:

- purchase: `price = (amount − fees) / quantity`;
- sale: `price = (amount + fees) / quantity`.

If the amount is **gross** (excluding fees): `price = amount / quantity`.

Example: purchase of 3 LVMH, net amount debited €2,222, fees €2: price = (2,222 − 2) / 3 = €740. For a sale of one LVMH with €698 credited and €2 of fees: price = (698 + 2) / 1 = €700.

### The setting in the assistant

At step 2 of the assistant, as soon as a column is matched to "Total amount", the [[The total amount includes fees (net amount debited or credited)]] box appears, ticked by default. Untick it if your amount column excludes fees. Automatic import, for its part, always treats the amount as net.

### Price and amount both present

The unit price in the file is then used as it is; the amount serves only to check the consistency of the columns and, for a dividend, to know the sum received.

### For a dividend

The quantity is set to 0 and the total amount is placed in the price column, as the project format requires. With no amount column, the software takes price × quantity.

### If the price does not come out right

Check in the assistant that the right column is matched to the amount (net or gross, debit or credit) and that the fees box matches your statement. Once the portfolio has been analysed, a price can also be corrected in the Transactions tab.

## The import assistant step by step
<!-- fiche: import-assistant | questions: how do I use the import assistant ; what is the import assistant for ; the assistant opened what should I do ; how do I change the recognised column ; fix the column header row ; choose the excel sheet ; analyse this portfolio doesnt work ; download the converted file ; open the assistant manually | mots: import assistant, column mapping, steps, Excel sheet, header row, interpretation, Yahoo Finance ticker, converted file, validation -->

The assistant is displayed in place of the dashboard when automatic detection has any doubt, or when you click [[Open the import assistant]]. If it opens automatically, the [[Why is the assistant opening?]] panel gives the reason. It has four steps, all pre-filled.

### 1. The file

- [[Excel sheet]]: only for a workbook with several sheets.
- [[Header row]]: the number of the row in the file that contains the column names, detected automatically. Set 0 if the file has no header row.
- A preview shows the first eight rows and the total number of rows.

### 2. Column mapping

For each piece of information, a menu shows the column of your file that contains it: [[Transaction date]], [[Transaction type]], [[Security (ticker, ISIN or name)]], [[Security name]], [[Quantity]], [[Unit price]], [[Total amount]], [[Fees]], [[Currency]], [[Exchange]]. Fields marked with an asterisk are mandatory; choose "— none —" for a missing piece of information. For the price, a "Unit price" or "Total amount" column is enough. If a mandatory field is missing, the assistant stops and says what remains to be done.

### 3. Transaction types and securities

- On the left (if a type column is matched), each distinct value in the file, its number of rows and its [[Interpretation]]: Buy, Sell, Dividend or [[Ignore the row]]. Change as needed.
- On the right, each security in the file, the proposed [[Yahoo Finance ticker]] (editable, for example `MC.PA` for LVMH in Paris), the [[Name found]] and the [[Status]]: "as is", "converted (Bloomberg, Google, Reuters)", "found" or "not found". For a security that is not found, type in its ticker by hand, otherwise its rows are likely to be ignored.

### 4. Result

- [[Currency of the prices in the file]]: [[Automatic detection (recommended)]], [[Trading currency of each security]] or [[Everything is in euros]] (see the fiche on currencies).
- Notes flag ignored rows, currency conversions and prices far from the price of the day.
- The table shows the transactions in the project format.

Finally click [[Analyse this portfolio]]. The [[Download the converted file (project format)]] button saves the result under the name `transactions_converties.csv`: uploaded again later, this file is read directly.

### Good to know

The converted file is remembered for the session: uploading the same file again does not reopen the assistant. When signed in, save it with [[Save to my space]] so you do not have to redo these steps.

## How does the software find a security's ticker (ISIN, name)?
<!-- fiche: import-identifier-titres | questions: my file has isin codes instead of tickers ; how do I convert an isin into a ticker ; I dont know the yahoo ticker ; what is a yahoo finance ticker ; the software picked the wrong exchange ; why is my security listed in frankfurt and not paris ; search by company name ; isin of an irish etf | mots: ticker, ISIN, Yahoo Finance, security identification, search, exchange, company name, conversion, .PA suffix -->

For each security, the software needs its **Yahoo Finance ticker**, that is, the code that lets it download its prices: `MC.PA` (LVMH, Paris), `AAPL` (Apple, New York), `SAP.DE` (SAP, Xetra), `ULVR.L` (Unilever, London). The suffix indicates the exchange (.PA Paris, .DE Xetra, .AS Amsterdam, .MI Milan, .L London, .SW Switzerland, no suffix for the United States).

### What you can put in the security column

| Form | Example | Handling |
|---|---|---|
| Yahoo ticker | `MC.PA`, `AAPL` | Used as is |
| ISIN code | `FR0000121014` | Looked up (see below) |
| Company name | `Air Liquide` | Looked up |
| Bloomberg, Google, Reuters code | `MC FP`, `EPA:MC`, `AAPL.O` | Translated offline (see the dedicated fiche) |
| Ticker without an exchange | `MC`, `AIR`, `TSLA` | Exchange found thanks to prices (see the dedicated fiche) |

A 12-character code starting with two letters and ending with a digit is treated as an ISIN; its check digit (Luhn algorithm) is verified during column recognition and in PDFs.

### The search order for an ISIN or a name

1. **Offline first**: the built-in table of common ETF ISINs, then the memory of securities already recognised, then the local securities database (by ticker, by ISIN, or by name).
2. **Otherwise, the Yahoo Finance search engine** (Internet required), with the ISIN and then, if the file contains one, the name of the security.

Among the answers, only equities, ETFs, funds and indices are kept, and the preferred listing is that of the **stock exchange of the ISIN's country**: FR → Paris, DE → Xetra then Frankfurt, NL → Amsterdam, IT → Milan, ES → Madrid, GB → London, CH → Switzerland, US → New York, etc. For an Irish (IE) or Luxembourg (LU) ISIN, typical of ETFs, a euro listing is preferred (Paris, Xetra, Amsterdam, Milan), then London and New York.

### The answer is remembered

A security found online is kept in the local memory: next time, it is recognised immediately, even without Internet.

### If the chosen exchange does not suit you

In the assistant (step 3), replace the proposed ticker, for example `SAP.DE`, with another ticker for the same security. The choice of exchange changes the currency and the prices used, not the quantity held.

## Bloomberg, Google Finance, Reuters codes and the "Exchange" column
<!-- fiche: import-codes-bloomberg | questions: my file contains bloomberg tickers ; is MC FP equity recognised ; is a reuters ric code accepted ; google finance EPA:MC format ; I have an exchange column ; mic code xpar ; convert a bloomberg ticker to yahoo ; AAPL US Equity | mots: Bloomberg, Google Finance, Reuters, RIC, MIC code, exchange, XPAR, FP, EPA, yellow key, Equity, ticker conversion -->

The security codes used by professional terminals are translated into Yahoo Finance tickers **offline**, thanks to a table of exchange codes built into the software.

### Translation examples

| Source | Written in the file | Becomes |
|---|---|---|
| Bloomberg | `MC FP`, `MC FP Equity` | MC.PA |
| Bloomberg | `AAPL US Equity` | AAPL |
| Bloomberg | `SAP GY` | SAP.DE |
| Bloomberg | `700 HK` | 0700.HK (padded to 4 digits) |
| Bloomberg | `BRK/B US` | BRK-B |
| Google Finance | `EPA:MC`, `NASDAQ:AAPL` | MC.PA, AAPL |
| Reversed form | `MC:EPA`, `MC:FP` | MC.PA |
| Reuters (RIC) | `AAPL.O` | AAPL |
| Reuters (RIC) | `NESN.S` | NESN.SW |

For Bloomberg, the word `Equity` (the "yellow key") is optional. The recognised Bloomberg exchange codes include in particular FP (Paris), GY and GR (Xetra), NA (Amsterdam), IM (Milan), SM (Madrid), LN (London), SW (Switzerland), US, UN, UW and UQ (United States), JP (Tokyo), CN (Toronto), HK (Hong Kong). On the Reuters side, the suffixes .O, .N, .OQ, .A, .P and .K point to the United States, .S and .VX to Switzerland, .MA to Madrid and .I to Dublin.

Limitation: a Reuters code whose suffix is identical to Yahoo's (for example `LVMH.PA`) is taken as it is, whereas LVMH's Yahoo ticker is `MC.PA`. Correct it in the assistant if the security has no prices.

### A separate "Exchange" column

If the file gives the ticker without an exchange in one column and the exchange in another (a column named place, marché, bourse, exchange, MIC…), the two are combined: `MC` + `XPAR` gives `MC.PA`. The exchange can be written:

- as a MIC code: XPAR, XETR, XAMS, XMIL, XLON, XSWX, XNAS, XNYS…;
- as a Bloomberg or Google code: FP, GY, EPA, ETR, LON…;
- in full words: Euronext Paris, Paris, Xetra, Frankfurt, Amsterdam, Milan, London, Zurich, New York, Tokyo, Toronto…

The import summary says how many codes were converted: "… ISIN, Bloomberg code(s) or name(s) converted into tickers.".

## My file gives a ticker without an exchange (MC, AIR, TSLA)
<!-- fiche: import-ticker-sans-place | questions: my file has MC instead of MC.PA ; ticker without suffix ; the software picked moelis instead of lvmh ; how does it guess the exchange of a short ticker ; is AIR airbus or something else ; short tickers without .PA ; wrong security recognised on import | mots: short ticker, bare ticker, no suffix, exchange, recognition by prices, namesake, MC, Moelis, LVMH -->

Many files write `MC` for LVMH or `AIR` for Airbus, without indicating the exchange. But `MC` alone designates, on Yahoo Finance, a US company (Moelis); LVMH is `MC.PA`. The software resolves the ambiguity **using the prices in your file**.

### The method

For each short ticker (1 to 6 characters, with no suffix) that is not already a known ticker:

1. it gathers candidates: the securities in the local database that have this root, the first answers from the Yahoo Finance search engine, and the code followed by the suffixes of the main exchanges (New York, Paris, Xetra, Amsterdam, Milan, Madrid, London, Switzerland, Toronto);
2. it retrieves the prices of these candidates;
3. for each one, it compares the purchase and sale prices in your file with the price of the day of each transaction, reading the price in the trading currency, in the main currency or in euros;
4. it keeps the candidate whose **median gap** is the smallest, provided it is **below 15%**. If the gaps are almost equal (the same security listed in Paris and Frankfurt, for example), the order of preference is kept.

Example: `MC` bought at €740 in January 2024 matches the LVMH price in Paris, not that of Moelis (around $50): the software keeps `MC.PA`.

### What you need to know

- The method uses only purchases and sales (not dividends).
- It needs the candidates' prices: without Internet, only securities already in the local database can be compared.
- If no candidate fits within 15%, the code goes through the search engine; if it is still not found, the assistant opens so that you can enter the ticker.
- The summary says "… ticker(s) without an exchange identified from market prices.".
- If your file also contains an exchange column (XPAR, Euronext Paris…), it is used first.

## Securities recognised without Internet: the ETF table and the memory
<!-- fiche: import-memoire-etf | questions: does the import work without internet ; is an isin recognised offline ; is my amundi etf recognised without a connection ; what is the securities memory ; does the software remember isins ; which etfs are recognised automatically ; does the memory contain my data ; it recognised a wrong ticker last time | mots: offline, securities memory, memoire.csv, ISIN table, ETF, local database, Amundi, iShares, Vanguard, learning -->

### The ETF ISIN table

Trade confirmations and statements often give only an ISIN code and an abbreviated label ("AM.C.C.40 UC.ETF C"). To recognise the most common ETFs **without Internet**, the software contains a table of 31 ISINs, including:

| ISIN | Ticker | ETF |
|---|---|---|
| FR0013380607 | CACC.PA | Amundi CAC 40 UCITS ETF Acc |
| LU1681043599 | CW8.PA | Amundi MSCI World UCITS ETF Acc |
| FR0011869353 | EWLD.PA | Amundi PEA MSCI World UCITS ETF |
| IE0002XZSHO1 | WPEA.PA | iShares MSCI World Swap PEA UCITS ETF |
| FR0011871128 | PE500.PA | Amundi PEA S&P 500 UCITS ETF |
| IE00B4L5Y983 | IWDA.AS | iShares Core MSCI World UCITS ETF |
| IE00BK5BQT80 | VWCE.DE | Vanguard FTSE All-World UCITS ETF Acc |
| IE00B5BMR087 | SXR8.DE | iShares Core S&P 500 UCITS ETF |
| DE000A0S9GB0 | 4GLD.DE | Xetra-Gold |

The table also covers Amundi ETFs (Euro Stoxx 50, Nasdaq-100, emerging markets, Stoxx Europe 600, money market), iShares, Vanguard, SPDR, Invesco and Xtrackers, equity as well as bond funds. It is consulted **first**, before the memory: it thus corrects a wrong match that might have been learned earlier.

### The memory of recognised securities

Whenever an ISIN, a name or a code is found through the Yahoo Finance search engine, the match is recorded in a memory file (`memoire.csv`, in the securities database folder). Next time, it is found instantly, even offline.

- The memory is shared by all users of the software on this computer.
- It contains **no portfolio data**: only matches between codes (for example FR0000121014 → MC.PA), with a name and a date.

### The local securities database

After the table and the memory, the software searches the local securities database supplied with the software: by ticker, by ISIN code, then by name ("LVMH" finds "LVMH Moët Hennessy Louis Vuitton").

### Without Internet, in practice

An ETF ISIN from the table, a security already encountered or a security in the local database are recognised. A completely new security cannot be: the assistant opens and you can enter its ticker by hand.

## A security is not found: what should I do?
<!-- fiche: import-titre-introuvable | questions: security not found on import ; the software doesnt find my isin ; how do I enter the ticker by hand ; not found status in the assistant ; my fund doesnt exist on yahoo ; no prices for my security ; sicav or unlisted fund ; the proposed ticker is wrong | mots: not found, manual ticker, unknown ISIN, unlisted fund, UCITS, Yahoo Finance, ticker correction, search -->

### The message

During an automatic import, an unidentified security prevents direct analysis: the assistant opens and displays "Security(ies) not found: …" followed by the codes concerned. At step 3, these securities have the status "not found".

### The solution

1. Look the security up on the Yahoo Finance website (by name or ISIN) and note its ticker, for example `AI.PA` for Air Liquide.
2. In the assistant, step 3, type this ticker in the [[Yahoo Finance ticker]] column of the row concerned.
3. Check the result at step 4, then click [[Analyse this portfolio]].

Without a ticker, the rows of an ISIN that is not found are ignored (reason "a missing security"). For a name that is not found, the name itself is kept as the code, which will make it impossible to find prices: correct it.

### Frequent causes

- **No connection**: online search is impossible; only securities from the ETF table, the memory and the local database are recognised.
- **Unlisted fund** (some UCITS funds, euro funds, structured products): with no price on Yahoo Finance, it cannot be tracked by the software.
- **Name too vague or abbreviated**: a label such as "AM.C.C.40 UC.ETF C" yields nothing; it is the ISIN that allows recognition.

### If the proposed ticker is wrong

Replace it in the same way at step 3. The price check helps you spot an error: a security whose prices differ by more than 25% from the price of the day is flagged (see the fiche on checking the import).

## Foreign securities: in which currency should I put the price?
<!-- fiche: import-devises | questions: my statement gives prices in euros for american shares ; which currency should I enter the apple price in ; does the software convert dollars ; amounts in euros converted what does that mean ; currency conversion on import ; exchange rate used ; automatic currency detection ; everything is in euros option ; fees in dollars | mots: currency, trading currency, conversion, exchange rate, dollar, USD, EUR, EURUSD, automatic detection, price in euros -->

### The project rule

The price of a purchase, sale or dividend is expressed in the security's **trading currency** on Yahoo Finance: dollars for Apple, Swiss francs for Nestlé, pence for London. **Fees stay in euros**. The software then converts into euros at the exchange rate of the day of each transaction.

### But many statements give euros

A French bank statement often shows a price already converted into euros. On upload, the software detects this: for each security, it compares the purchase and sale prices in the file with the **actual closing price of the day**, using three possible readings:

| Reading | The price in the file is… |
|---|---|
| Trading currency | in the trading currency (e.g. $185) |
| Main currency | in pounds instead of pence (London securities only) |
| Euros | converted into euros (e.g. €169.72) |

It calculates the median gap of each reading against the market and keeps the closest one. If it is the euro reading, the security's prices (dividends included) are converted back into the trading currency: `price in currency = price in euros × EUR/currency rate of the day`.

Example: a purchase of Apple recorded at €169.72 on a day when €1 is worth $1.09 and the share is quoted at $185. Read in euros, 169.72 × 1.09 = $184.99: the reading matches the market, and the price is converted back to $184.99, or about $185.

### The safeguards

- The conversion is made only if it clearly improves the agreement with the market (gap reduced by more than 2 points, measured as a logarithmic gap); otherwise the price is kept as it is. This is useful for the Swiss franc, which is worth almost one euro.
- If even the best reading differs by more than 25% from the price, nothing is converted (unless the file's Currency column imposes the euro reading).
- If the file has a **Currency** column, it restricts the readings: "EUR" on all the rows of a foreign security imposes the euro reading; the security's own currency rules out the euro reading.
- Without a connection, prices are kept as they are and the message "Prices not checked against market data (no connection)." is displayed.

### Choosing yourself in the assistant

At step 4, [[Currency of the prices in the file]] offers [[Automatic detection (recommended)]], [[Trading currency of each security]] (no conversion) or [[Everything is in euros]] (conversion of all foreign securities).

### Limitation

The rate used is the market rate of the day; your bank's rate includes its foreign-exchange margin. Small gaps are therefore normal.

## London shares: why pence (GBp)?
<!-- fiche: import-pence | questions: what is GBp ; why is the unilever price in pence ; my london shares have a price 100 times too big ; price in pounds or pence ; GBX in my file ; british share wrongly valued ; ULVR.L price | mots: pence, GBp, GBX, pound sterling, GBP, London, LSE, factor 0.01, .L -->

### The principle

On Yahoo Finance, shares on the London Stock Exchange (tickers ending in `.L`) are quoted in **pence** (GBp or GBX), not pounds: 1 pound = 100 pence. A share shown at 4,000 GBp is therefore worth £40.00. The software knows this: for these securities, the currency is the pound (GBP) with a factor of 0.01.

### In the project format

The price of a London share is written **in pence**, as on Yahoo Finance: `2024-01-15,ACHAT,ULVR.L,Unilever,20,4000,1.00` for 20 shares at £40. A dividend is also written in pence. Fees stay in euros.

### If your file gives pounds or euros

On upload, currency detection compares the price with the price in pence using three readings:

- in pence: 4,000 → 4,000 GBp;
- in pounds: 40.00 → 40.00 / 0.01 = 4,000 GBp;
- in euros: €46.50 with €1 = £0.86 → 46.50 × 0.86 / 0.01 = 3,999 GBp.

The reading closest to the price is kept and the price is brought back to pence. The summary shows for example "ULVR.L: prices in GBP converted into the quotation unit".

### In a Currency column

The value `GBX` is read as `GBP`. It rules out the euro reading, but leaves the choice between pence and pounds.

### Symptom of an error

A London row valued 100 times too high or too low betrays a confusion between pounds and pence. Correct the price in the Transactions tab ([[Price (trading currency)]] column, in pence), or re-import with automatic detection.

## Importing a PDF statement of transactions
<!-- fiche: import-pdf-releve | questions: how do I import a pdf from my bank ; is my pdf statement read ; does the software read tables in pdfs ; securities account statement pdf ; multi-page pdf ; no transaction found in this pdf ; pdf with a table of transactions | mots: PDF, transaction statement, table, pdfplumber, extraction, multiple pages, securities account statement -->

### How the PDF is read

The software reads the text and tables of the PDF (pdfplumber library), page by page.

- A table is kept if it has at least two rows, three columns, and dates on at least two rows: that is the mark of a genuine transaction table.
- Tables of the same width are joined end to end (statement over several pages); the header repeated at the top of each page is kept only once.
- The resulting table then follows exactly the same path as an Excel file: header row, column recognition, ISIN, dates, numbers, currencies.

### When the PDF is rather a trade confirmation

If the text contains "avis d'opéré", "avis d'exécution", "confirmation d'exécution", "confirmation d'ordre" or "trade confirmation", the software first reads the document as a trade confirmation (one transaction per page). If there is no usable transaction table, it also tries this reading.

### If nothing is found

The message "No transaction found in this PDF (no transaction table and no readable trade confirmation)." is displayed. In that case:

- download the Excel or CSV export of the transactions from your online banking instead;
- or use the diagnostic tool to see what the software reads (see the fiche on `diagnostic_pdf.py`).

### Tip

On your bank's website, prefer the document's download button ("PDF format", "Download") to the browser's "Print" function: a downloaded PDF contains the real text, read instantly and exactly; a page "printed to PDF" is sometimes only an image.

## Importing a PDF trade confirmation (Bourse Direct example)
<!-- fiche: import-avis-opere | questions: how do I import a trade confirmation ; what is an avis d'opere ; is my bourse direct trade confirmation recognised ; the software took the issue date instead of the execution date ; trade confirmation pdf cash sale ; several confirmations in one pdf ; order confirmation pdf ; negative quantity in the confirmation | mots: trade confirmation, avis d'opéré, execution confirmation, Bourse Direct, PDF format, execution date, brokerage, ISIN, executed order -->

A **trade confirmation** (avis d'opéré) is the confirmation your broker sends after each executed order. The software extracts one transaction per page from it.

### What is read

| Information | Where the software looks for it |
|---|---|
| ISIN code | First 12-character code whose check digit is correct and which contains at least 6 digits |
| Date | Execution, transaction or trade date, "exécuté le", "trade date"; failing that a date close to the word exécution or followed by "achat"/"vente"; issue, settlement, value or delivery dates are discarded |
| Direction | Achat, vente, souscription, rachat, buy, sell, dividende, coupon… (purchase by default) |
| Quantity | "Quantité", "Qté", "Nombre de titres", "Quantity", "Nominal" |
| Price and currency | "Cours", "Prix unitaire", "Price", with EUR, USD, GBP, €, $, £… |
| Fees | Sum of all the "Courtage", "Commission", "Frais", "TTF" (financial transaction tax), "Fees" lines |
| Amount | "Montant net", "Net à débiter/créditer", otherwise "Montant" or "Brut" |
| Label | After "Libellé :" or "Valeur :", otherwise the name written just after the ISIN |

Headings and values may be presented as text ("Quantité : 15") or arranged in a table. A transaction is kept only if the ISIN, quantity and date are found.

### Example: a Bourse Direct confirmation downloaded with "PDF format"

The confirmation contains in particular:

```
28/09/2026 VENTE COMPTANT FR0013380607 AM.C.C.40 UC.ETF C 2 473,90
QUANTITE : -60
COURS : +41,295 BRUT : +2 477,70
COURTAGE : +3,80 TVA : +0,00
```

The software reads: date 28/09/2026, direction VENTE (sale), ISIN FR0013380607, label "AM.C.C.40 UC.ETF C", quantity −60 (made positive: 60), price 41.295, fees €3.80. The ISIN is in the ETF table: it becomes `CACC.PA` without Internet, and the abbreviated label is replaced by the official name "Amundi CAC 40 UCITS ETF Acc". The resulting transaction is: `2026-09-28, VENTE, CACC.PA, 60 securities at €41.295, fees €3.80`. Check: 60 × 41.295 = €2,477.70 gross, minus €3.80 of brokerage = €2,473.90 credited.

### Several confirmations

A multi-page PDF containing one confirmation per page gives one transaction per page. To add several separate confirmations to an existing portfolio, the [[Add transactions]] page accepts several files at once.

### After reading

The sidebar summary says "PDF trade confirmation read.". Always check the transaction: an unusual confirmation can be misinterpreted.

## A scanned or "printed" PDF: character recognition
<!-- fiche: import-pdf-image | questions: my pdf is an image ; is a scanned pdf read ; what is ocr ; I printed the page to pdf with microsoft print to pdf ; how does character recognition work ; my pdf is rotated to landscape ; the isin is misread ; rapidocr or tesseract ; reading the pdf takes a long time | mots: OCR, character recognition, image PDF, scan, RapidOCR, Tesseract, rotation, misread ISIN, Microsoft Print to PDF -->

### Text PDFs and image PDFs

A PDF may contain **real text** (each character is stored, as in a PDF downloaded from the bank) or only an **image** of the page (scan, photo, or web page printed with "Microsoft Print to PDF"). The software considers a PDF to be an image when it contains fewer than 20 characters of text.

### Character recognition

For an image PDF, the software "looks at" each page and recognises the letters and digits in it, if an engine is installed:

1. **RapidOCR**, a library that works offline, installed with the `requirements-ocr.txt` file and built into the installers when their build succeeded in installing it;
2. failing that, **Tesseract**, if it is installed on the computer (in French and English if the French language is available).

### The precautions taken

- **Rotation**: each page is tried in all four orientations (0°, 90°, 270°, 180°). The orientation kept is the one that brings out the most valid ISIN codes and useful words (quantité, cours, courtage, achat, vente, date, montant…). As soon as an orientation is clearly right, the others are not tried.
- **Repair of misread ISINs**: the letter O read in place of the digit 0 (`FRO013380607`), an I or an l in place of 1, S for 5, B for 8, Z for 2, or a character read twice (`FRO0013380607`). A correction is kept only if the corrected ISIN has a correct check digit and at least 6 digits: the software never invents a code. A word like "EURONEXTPARIS" is never mistaken for an ISIN.
- **Run-together words**: reading tolerates words stuck together ("VENTECOMPTANT").

The recognised text is then read as a trade confirmation. Recognition reads only trade confirmations: a scanned statement in table form is generally unusable.

### Always check

Reading an image takes several seconds and remains less reliable than a text PDF. The summary says so: "Image PDF read by character recognition: please check the transactions ("Transactions" tab).". Check the date, quantity and price.

## Why is my scanned PDF rejected?
<!-- fiche: import-pdf-scan-refuse | questions: scanned pdf rejected ; message cannot be read automatically ; no transaction was recognised in my image pdf ; why wont my scan work ; the software rejects my photo of a trade confirmation ; what should I do if my pdf is an image ; install character recognition | mots: scanned PDF, rejection, image PDF, OCR not installed, error message, PDF format, manual entry, requirements-ocr -->

Two messages may appear for an image PDF.

### "Scanned PDF (image): it cannot be read automatically…"

No character recognition engine is installed: the PDF contains no text to read. The message offers three solutions: export the statement as a PDF from your online banking, or as Excel / CSV, or enter the transaction by hand.

If you launch the software from the source code, you can install the engine with the command `python -m pip install -r requirements-ocr.txt`.

### "Image PDF (scan, photo or page printed with "Print to PDF"): the text was read by character recognition, but no transaction was recognised…"

The engine did read the page, but did not find a valid ISIN code, a quantity and a date all together. Possible causes: blurred or low-resolution image, unreadable ISIN, a document that is not a trade confirmation (statement in table form, portfolio summary).

### Why the software refuses rather than guesses

A misread transaction (a quantity of 60 read as 80, a price shifted by one decimal place) would distort all the calculations without you noticing. The software therefore prefers to clearly refuse a document it does not understand.

### The solutions, from the most reliable to the least

1. **Download the real PDF** from your online banking, with the "PDF format" or "Download" button rather than "Print": the text is then read exactly.
2. **Export the transactions as Excel or CSV**, if your bank offers it.
3. **Enter the transaction by hand**: [[Add transactions]] page, [[Manual entry]] tab.
4. Run the PDF diagnostic to understand what was read (see the next fiche).

## Diagnosing a misread PDF with diagnostic_pdf.py
<!-- fiche: import-diagnostic-pdf | questions: how can I see what the software reads in my pdf ; what is diagnostic_pdf.py for ; my trade confirmation is misread how do I report it ; see the text extracted from the pdf ; send a pdf reading report ; diagnostic_pdf.txt ; debug pdf | mots: diagnostic, diagnostic_pdf.py, diagnostic_pdf.txt, debugging, extracted text, misread PDF, report, terminal -->

The `diagnostic_pdf.py` script, at the root of the project, shows exactly what the software reads in a PDF. It is mainly aimed at those who have the source code (students, developers) and is used to understand, or to get corrected, a faulty reading.

### Running it

In a terminal opened in the project folder (for example the VS Code terminal):

```
python diagnostic_pdf.py "C:\path\to\confirmation.pdf"
```

### What it displays

- the file name and size, the number of pages and the number of characters of embedded text;
- **text PDF** (at least 20 characters): the mention "PDF TEXTE (lecture exacte)", then the text of each page and each detected table, with cells separated by `|`;
- **image PDF**: the recognition engine used (RapidOCR, Tesseract or AUCUN, meaning none), then, for the first page, the text read in each of the four orientations with its score, and the text finally kept after ISIN correction;
- finally the **result**: the table of transactions obtained and its nature (`pdf_tableau` for a statement, `pdf_avis` for a trade confirmation, `pdf_ocr` for a reading by character recognition), or the error message.

### The report

The result is also saved in the `diagnostic_pdf.txt` file, next to the script. This is the file to send in order to get a faulty reading corrected.

Note: it contains the text of your document. Hide your name and account number before sending it.

## How do I check what the software has read?
<!-- fiche: import-verifier | questions: how do I check my import ; were all my transactions imported ; where do I see the imported transactions ; price far from the day's price is that serious ; the summary in the sidebar ; how many transactions were read ; import quality check ; stock split detected | mots: verification, import summary, Transactions tab, price alert, gap, quality check, number of transactions, split, stock split | aller: Analyse du portefeuille/Transactions | chiffres: nb_operations -->

After an import, take a minute to check the result. The software helps you in three ways.

### 1. The sidebar summary

After an automatic import, a box summarises what was understood: number of transactions and securities, PDF read, columns identified without a header row, tickers and ISINs converted, order of the dates, ignored rows, currency conversions. At the bottom of the sidebar, the "Transactions" line reminds you of the number of transactions analysed. Compare it with the number of rows in your statement.

### 2. The price alerts

Each purchase and sale price is compared with the closing price of the day. If prices differ from it by more than 25%, a note flags it, for example: "AAPL: 2 price(s) far from that day's market price (median gap +38%) — check the ticker, currency or a stock split.".

Possible causes:
- **wrong ticker** (namesake on another exchange);
- **wrong currency** (euros read as dollars, pounds instead of pence);
- **stock split**: after a split, the price history may no longer match the price paid at the time;
- a simple data entry error in the file.

An alert does not stop the analysis: it is up to you to judge.

### 3. The Transactions tab

In [[Transaction history]], all transactions are listed, from most recent to oldest, with the type, ticker, security, quantity, price converted into euros, fees, currency and the [[Price in currency]] as read. The [[Type]] and [[Securities]] filters help you find a row. An error is corrected directly with [[Edit transactions]] (see the dedicated fiche).

### Recommended checkpoints

- the quantities held (Holdings tab) match your portfolio statement;
- the dates are in the right day/month order;
- dividends are total amounts, with a quantity of 0;
- foreign securities have a consistent price in their currency.

## Saving an imported portfolio to my space
<!-- fiche: import-enregistrer-espace | questions: how do I keep my imported portfolio ; save to my space where is the button ; do I have to upload my file every time ; save the encrypted portfolio ; add a portfolio from my account ; the save button doesnt appear ; same portfolio name is it replaced | mots: save, back up, My space, personal space, encrypted, My account, Add a portfolio, persistence -->

An uploaded file is kept only for the session. To find it again later, save it to your encrypted personal space. You must be signed in (the [[Sign in]] button at the top of the sidebar).

### From the sidebar

1. Upload the file with [[Upload a file (CSV, Excel or PDF)]] and let the software analyse it (assistant included, if needed).
2. Under the upload area the [[Save to my space]] block appears, with a [[Portfolio name]] field pre-filled with the file name.
3. Change the name if you wish, then click [[Save]].
4. The message ""…" has been saved to your space (encrypted)." confirms the operation.

What is saved is the portfolio **after reading and conversion**, in the project format (Yahoo tickers, prices in the trading currency): it will be reopened without going through detection again.

The block appears only once the portfolio has been analysed successfully. To then work on the saved version, remove the file from the upload area and choose "My space · portfolio name" in the "Data" list.

### From the "My account" page

Click [[My account]], then use the [[Add a portfolio]] section: choose a CSV, Excel or PDF file. If it is recognised automatically, the number of transactions is displayed; enter the name and click [[Save]]. Otherwise, a message invites you to go through the sidebar, where the import assistant will guide you.

### Beware of identical names

Saving under the name of a portfolio already in your space (ignoring capital letters) **replaces** that portfolio; the old version can still be recovered with [[Undo last change]] in "My account". Choose a different name if you want to keep both.

## Adding new transactions to an existing portfolio
<!-- fiche: import-ajouter-operations | questions: how do I add a new purchase ; update my portfolio without resending everything ; add a trade confirmation to my portfolio ; where is the add transactions button ; add this months transactions ; import only the new transactions ; add several pdfs at once ; my file isnt read in add transactions | mots: add transactions, update, new movements, trade confirmation, export, merge, refresh the portfolio, new transactions -->

There is no need to resend the whole history with every new order: send only the new movements, and the software merges them with the existing ones.

### Where the page is

- in the sidebar, under "Data", the [[Add transactions]] link below the upload area: it applies to the portfolio displayed;
- in [[My account]], under each portfolio in [[My portfolios]], the [[Add transactions]] button.

The page shows which portfolio it concerns. [[Back to the dashboard]] closes it without changing anything.

### Three ways to add

- **[[From a file]] tab**: the [[Files (CSV, Excel or PDF)]] area, which accepts several files at once (several trade confirmations, an export of the latest transactions…). Each file goes through the same automatic reading as the main upload; the message gives the number of transactions read, for example "avis.pdf: 1 transaction(s) read.". A file already read on the page is not read again.
- **[[Manual entry]] tab**: an order typed in by hand (see the dedicated fiche).
- The two can be combined: all the transactions accumulate in the same list.

If a file is not understood automatically, the reason is displayed. This page has no import assistant: for an unusual format, first upload the file from the sidebar, download the converted file, then add it here.

### The check before saving

The [[Check before saving]] box lists the transactions to be added. The cells are editable. The [[Add]] column lets you untick a row; the [[Status]] column shows "new" or "already in the portfolio" (duplicates are unticked by default). A summary line gives the number of transactions added and the total after adding. Blocking checks are displayed in red (see the dedicated fiche).

### Saving

Click [[Save transactions]]. The selected transactions are merged with the existing ones and sorted by date.
- Portfolio in your space: it is saved again, encrypted, and the previous version is kept ([[Undo last change]] in [[My account]]).
- Uploaded file or example portfolio: the addition holds for the session; download the updated file to keep it.

[[Clear all]] empties the current list without saving anything.

## Entering an order by hand
<!-- fiche: import-saisie-manuelle | questions: how do I enter a purchase by hand ; add a transaction manually ; manual entry of a dividend ; I have no file I want to type my order ; which price do I put in manual entry ; security not found in manual entry ; enter an order with the isin ; is the price in euros or dollars in the entry form | mots: manual entry, form, order, manual addition, ticker, ISIN, Bloomberg code, Add to the list -->

Manual entry is found on the [[Add transactions]] page, [[Manual entry]] tab.

### The fields

| Field | Content |
|---|---|
| [[Date]] | Transaction date (today by default), in DD/MM/YYYY format |
| [[Type]] | Buy, Sell or Dividend |
| [[Security]] | Yahoo ticker, ISIN code, company name or Bloomberg code |
| [[Quantity]] | Number of securities (1 by default); 0 for a dividend |
| [[Unit price (security currency) or dividend amount]] | Price of one security in its trading currency (dollars for Apple, pence for London); for a dividend, the total amount received |
| [[Fees (€)]] | Brokerage fees, in euros |

Click [[Add to the list]]: the transaction joins the check table. The form is emptied for the next entry.

### Security recognition

- A known ticker or one with a Yahoo exchange suffix (`MC.PA`, `SAP.DE`) is taken as it is.
- An ISIN, a name, a Bloomberg code or a short ticker are looked up as during an import: ETF table, memory, local database, then Yahoo Finance.
- In case of failure: "Security not found: …. Enter its Yahoo Finance ticker (e.g. MC.PA).".

When the security is found through a search, its official name is used in the list; otherwise, what you typed serves as the name.

### Mind the currency and the price

Unlike an imported file, a price typed by hand **is not checked** against market prices: it must be in the security's trading currency. For 10 Apple shares bought at $185, enter 185, even if your bank debited you in euros.

A price left at 0 for a purchase or a sale blocks saving ("Zero quantity or price for …"). Likewise, a future date is refused.

### Example

Purchase of 5 Air Liquide at €172.10 on 12/09/2024, €1.99 of fees: Date 12/09/2024, Type Buy, Security `AI.PA` (or `Air Liquide`, or `FR0000120073`), Quantity 5, Price 172.10, Fees 1.99. Then [[Add to the list]] and [[Save transactions]].

## How are duplicates detected?
<!-- fiche: import-doublons | questions: I imported the same confirmation twice ; does the software add duplicate transactions ; what does already in the portfolio mean ; my statement overlaps the old one ; why is my row unticked ; two identical purchases on the same day ; duplicate rule ; price tolerance for duplicates | mots: duplicates, already in the portfolio, overlap, duplicate detection, 0.5% tolerance, idempotent, duplicate transaction -->

When transactions are added, each new transaction is compared with those in the portfolio and with the other new transactions in the list.

### The exact rule

Two transactions are considered identical if they have:

- the **same date**;
- the **same ticker**;
- the **same type** (buy, sell, dividend);
- the **same quantity** (to within one millionth);
- a **price equal to within 0.5%**: `|price 1 − price 2| / max(price 1, price 2) ≤ 0.5%`.

Fees and the name of the security are not compared.

Example: a purchase of 5 Air Liquide on 01/03/2024 at €170.00 is already in the portfolio; a statement gives the same transaction again at €170.40. Gap: 0.40 / 170.40 = 0.23%, below 0.5%: it is a duplicate. At €171.00, the gap would be 0.58% and the transaction would be considered new.

### What the software does

A duplicate appears in the check table with the status "already in the portfolio" and its [[Add]] box unticked. It is therefore not added, unless you tick the box again.

Practical consequence: adding the same file twice changes nothing. You can therefore upload an export that overlaps the previous one without fear of double counting.

### Two genuinely identical orders

If you really placed two identical orders on the same day at the same price, the second is taken for a duplicate: tick its [[Add]] box again before saving.

### Outside the add page

This detection applies only to the [[Add transactions]] page. A complete file uploaded from the sidebar is read as it is: if it contains the same row twice, it will be counted twice. Then delete the extra row in the Transactions tab.

## Which checks block saving?
<!-- fiche: import-controles | questions: why cant I save ; the save button is greyed out ; sale of securities but only 0 held ; transaction dated in the future ; zero quantity or price message ; short sale refused ; red message in the check ; the portfolio cannot be empty | mots: checks, blocking, short sale, future date, zero quantity, zero price, consistency, validation, blocking error -->

Before saving an addition or a modification, the software checks the consistency of the **whole resulting portfolio** (old and new transactions). As long as a blocking check fails, the message is displayed in red and the save button stays inactive.

### The three blocking checks

| Check | Message |
|---|---|
| Future date | "Transaction dated in the future: [security], on [date]." |
| Zero quantity or price (purchase or sale) | "Zero quantity or price for [security], on [date]." |
| Sale greater than securities held | "Sale of [quantity] [security] on [date], but only [n] held on that date." |

A transaction dated today is accepted. A dividend may have a zero quantity (that is the rule of the format).

### How the sale is checked

The transactions are replayed in date order; on the same day, a purchase comes before a dividend, which comes before a sale. The software tracks the quantity held of each security; if a sale makes it negative, the check fails. Example: 3 LVMH bought on 16/01/2024; a sale of 10 LVMH on 02/05/2024 gives "Sale of 10 LVMH on 02/05/2024, but only 3 held on that date.".

### The other alerts in the Transactions tab

- Deleting a purchase on which a later sale depends triggers the sale check; the software then advises: also delete the sale(s) that depend on it (same security, later date).
- "The portfolio cannot be empty: keep at least one transaction." also blocks.
- If a security is no longer held after the modification, a warning flags it ("After this change, these holdings are no longer held: …"), without blocking.

### What to do

Correct the row concerned directly in the table (date, quantity, price) or untick it. If the error comes from an older transaction in the portfolio, correct it in the Transactions tab.

## Deleting or correcting a transaction (Transactions tab)
<!-- fiche: import-modifier-supprimer | questions: how do I delete a transaction ; I entered a purchase by mistake ; correct the quantity of a purchase ; change the price of a transaction ; erase a row from my portfolio ; I got the date wrong ; how do I change the ticker of a transaction ; remove a wrong sale ; edit transactions doesnt save | mots: edit, delete, correct, transaction, editing, data entry error, Edit transactions, I confirm these changes | aller: Analyse du portefeuille/Transactions | chiffres: nb_operations -->

Any transaction in the portfolio can be deleted or corrected, in the "Portfolio analysis" workspace, Transactions tab.

### The steps

1. Click [[Edit transactions]] (to the right of [[Transaction history]]). The table becomes editable; the button becomes [[Done]].
2. Find the row using the [[Type]] and [[Securities]] filters; rows hidden by the filters are not modified.
3. To **delete**, tick the [[Delete]] box on the row.
4. To **correct**, edit the date, the quantity, the [[Price (trading currency)]] or the fees directly.
5. A [[Summary]] lists the "Deleted" and "Corrected" transactions, with the old and the new value (for example "quantity: 10 → 1").
6. The checks are displayed (see the fiche on blocking checks).
7. Tick [[I confirm these changes]], then click [[Save changes]].

[[Cancel all]] abandons the changes in progress and leaves edit mode.

### What is modified

It is the portfolio file itself that is modified, in the project format: the price is that of the security's **trading currency** (dollars, pence…), not the price converted into euros shown when viewing. The "Currency" column reminds you of this.

### What cannot be edited here

The type, ticker and name of a transaction cannot be edited, and no row can be added in this table. To change the security or the type of a transaction: delete it here, then add the correct transaction with [[Add transactions]].

### Where the modification goes

- **Portfolio in your space**: it is saved again, encrypted; the previous version is kept and [[Undo last change]] lets you go back to it.
- **Uploaded file or example portfolio**: the modification holds for the session; the message invites you to download the updated file.

## Undoing the last change
<!-- fiche: import-annuler | questions: how do I undo my last change ; go back after a deletion ; I deleted a transaction by mistake ; undo an addition of transactions ; restore the previous version of my portfolio ; the undo button has disappeared ; can I undo several times ; ctrl z | mots: undo, rollback, previous version, restore, Undo last change, My account | aller: Analyse du portefeuille/Transactions -->

### For a portfolio in your space

With each addition of transactions or saved modification, the software keeps the previous version of the portfolio (also encrypted). The [[Undo last change]] button restores it. It is found:

- in the Transactions tab, below the table, outside edit mode (or in edit mode as long as no change has been entered);
- in [[My account]], under the portfolio concerned.

A tooltip reminds you of the date of the version that will be restored ("Go back to the version of …").

### A single level of undo

Only the **last** previous version is kept. After an undo, the button disappears: you cannot go back further. Likewise, a new modification replaces the version kept. Saving a file under a name already used with [[Save to my space]] replaces the portfolio of that name, and the replaced version becomes the recoverable version.

### For an uploaded file or an example portfolio

After a modification made in the Transactions tab, the [[Undo last change]] button also appears in that tab and returns to the previous state for the session. On the other hand, an addition made with [[Add transactions]] without an account does not offer an undo button: delete the added rows in the Transactions tab. Session changes disappear anyway when the software is closed.

### Tip

Before a series of important corrections, download a copy of the portfolio: the [[Download]] button in [[My account]], or [[Download the updated file]] without an account.

## Without an account: retrieving the updated file
<!-- fiche: import-sans-compte | questions: I dont have an account how do I keep my changes ; download the updated file ; my additions disappeared when I closed it ; where is the corrected file ; use the software without signing in ; updated csv file ; how do I resume my portfolio next time | mots: without an account, session, download, updated file, mis_a_jour.csv, backup, CSV export -->

Without being signed in, you can do everything: upload a file, add transactions, correct or delete rows. But **nothing is saved on the computer**: changes hold only for the session and disappear when the software is closed.

### The updated file

After an addition or a modification, a message reminds you: "Download the updated file to keep it.". In the sidebar, next to the [[Add transactions]] link, the [[Download the updated file]] button saves the complete portfolio, in the project format, under the name `<original name>_mis_a_jour.csv`. The "File" line of the sidebar information then shows "… (updated)".

Next time, simply upload this file: it is read directly.

### The other downloads

- [[Download the converted file (project format)]] in the import assistant: the file as read, before any addition.
- [[Download the selection (CSV)]] in the Transactions tab: the transactions displayed, with **prices converted into euros** and extra columns (currency, price in currency). This file is for viewing or analysing in a spreadsheet; to resume the portfolio later, prefer the updated file.

### One update at a time

Session changes apply to one portfolio at a time: saving additions or corrections on another portfolio replaces the changes in progress. Download the updated file before moving on to another portfolio.

### The simplest way

Create an account: your portfolios are saved encrypted, additions and corrections are kept, and undoing is possible.

## The example portfolios: what are they for?
<!-- fiche: import-exemples | questions: what are the example portfolios ; where does the diversified multi-asset portfolio come from ; can I modify an example portfolio ; how do I test the software without my data ; global equity portfolio ; are my changes to the example kept ; remove the example portfolios from the list | mots: example portfolios, demonstration, diversified, global equities, test data, transactions_diversifie.csv, trial -->

### What they are

The software comes with example portfolios, offered in the "Data" list, after your personal portfolios. Depending on the files present in the `data` folder:

| Displayed name | File |
|---|---|
| Diversified portfolio (multi-asset) | `transactions_diversifie.csv` |
| Global equity portfolio | `transactions_mondial.csv` |
| Example portfolio | `transactions.csv` (offered only if it is the only example file) |

The diversified portfolio is offered first when it exists. The first two are produced by the project's scripts `generer_portefeuille_diversifie.py` and `generer_portefeuille_mondial.py`.

### What they are for

- discovering the software without preparing a file;
- practising reading the indicators on a realistic portfolio;
- testing the addition, correction and deletion of transactions without risk;
- seeing what a file in the project format looks like.

### Modifying them

You can add transactions to them or correct them: as for a file uploaded without an account, the changes hold only for the session. The original file is never modified. Download the updated file if you want to keep the result, or save it to your space by uploading it afterwards from the upload area.

### Removing them from the list

The list does not offer a way to hide them; they remain available, after your personal portfolios.

## Common import errors and solutions
<!-- fiche: import-erreurs | questions: my file wont import ; message unable to analyse the portfolio ; missing or unrecognised column ; the file is empty ; rows ignored unreadable date ; no transaction read ; sale impossible we only hold ; import error what do I do ; prices not checked no connection | mots: error, troubleshooting, error message, import problem, unrecognised column, unreadable date, security not found, sale impossible, empty file, solutions -->

| Message or symptom | Probable cause | Solution |
|---|---|---|
| "The file is empty." | File with no content, or wrong Excel sheet | Check the file; in the assistant, choose the right [[Excel sheet]] |
| "Unrecognised column(s): …" | Unknown column name, or header row wrongly detected | In the assistant, match the column by hand and check the [[Header row]] |
| "Columns recognised, but not certain about the quantities, prices and amounts." | Number columns without a meaningful name | Check step 2 of the assistant, then confirm |
| "Security(ies) not found: …" | Unknown ISIN or name, or no Internet | Enter the ticker at step 3 of the assistant |
| "… row(s) with an unreadable date (rows …): ignored" | Date written in words, empty or damaged cell | Correct the date in the file |
| "… with a missing price or amount" | Purchase or sale with neither price nor amount | Complete the file, or match the amount column |
| "… with a zero quantity" | Purchase or sale of 0 securities | Check the quantity column |
| "… with a missing security" | Empty security cell, or ISIN without a ticker | Complete the file or enter the ticker |
| "No transaction read." | All rows ignored or in error | Check the types (step 3) and the mapping (step 2) |
| "Unable to analyse the portfolio: Sale impossible on …" | Sale of more securities than held (missing purchase in the history) | Add the missing purchase or correct the quantity |
| "Prices not checked against market data (no connection)." | No Internet during the import | Normal when offline; check the foreign securities |
| "… price(s) far from that day's market price …" | Wrong ticker, currency or stock split | See the fiche on checking the import |
| Messages about scanned PDFs | Image PDF | See the fiches on image PDFs and rejected scans |
| Values 1,000 times too small | Thousands separator read as a decimal (`1.234`) | Remove the thousands separator in the file |
| London shares 100 times too expensive | Confusion between pounds and pence | See the fiche on pence |

### Row numbers

In the messages "row(s) with … (rows 3, 7)", rows are numbered from the first data row below the column headers, not counting empty rows. Beyond five rows, the list ends with "…".

### When the analysis fails after the import

The message "Unable to analyse the portfolio: …" is followed, for an uploaded file, by the [[Open the import assistant]] button: it lets you re-read the file differently. For a portfolio in your space, correct the transaction concerned.

### Missing libraries (source code)

If you launch the software from the source code without all the libraries, the messages "To read a PDF, install pdfplumber…" or "To read an Excel file (.xlsx), install openpyxl…" give the command to run. The Windows and Mac installers already contain them.

## Full example: from the broker export to an up-to-date portfolio
<!-- fiche: import-exemple-complet | questions: step by step import example ; portfolio import tutorial ; I am a beginner where do I start to import ; complete import demonstration ; how to do it from a to z ; example of an imported broker statement ; practical case import and update | mots: tutorial, step by step, example, practical case, demonstration, import, update, broker statement -->

Here is a complete case: a statement exported as CSV, its import, its saving, then the addition of a trade confirmation and a correction.

### 1. The broker's file

```
Relevé des opérations - Compte titres n° 12345678
Édité le 05/10/2026

Date opération;Opération;Code ISIN;Libellé;Qté;Cours;Frais;Montant net
15/01/2024;Achat Comptant;FR0000121014;LVMH;3;740,00;2,00;2 222,00
12/03/2024;Achat Comptant;US0378331005;APPLE INC;10;157,50;5,00;1 580,00
22/05/2024;Coupon;FR0000121014;LVMH;0;;;39,00
28/06/2024;Frais de garde;;;;;;-12,00
18/09/2024;Vente Comptant;FR0000121014;LVMH;-1;700,00;2,00;698,00
```

### 2. Upload and automatic reading

Upload the file with [[Upload a file (CSV, Excel or PDF)]]. The software:

- detects the semicolon as the separator and ignores the first three lines: the header row is the fourth;
- recognises the columns by their name: "Date opération" (date), "Opération" (type), "Code ISIN" (security), "Libellé" (name), "Qté" (quantity), "Cours" (price), "Frais" (fees), "Montant net" (amount);
- reads the dates as day/month (15/01 cannot be a month);
- classifies "Achat Comptant" as a purchase, "Coupon" as a dividend, "Vente Comptant" as a sale, and ignores "Frais de garde";
- makes the quantity −1 of the sale positive;
- converts the ISINs into tickers (FR0000121014 into MC.PA, US0378331005 into AAPL);
- checks the currencies: LVMH is in euros; for Apple, if €157.50 multiplied by the EUR/USD rate of 12/03/2024 gives a price close to Apple's price that day, the price is converted back into dollars.

Consistency check: 3 × 740 + 2 = 2,222; 10 × 157.50 + 5 = 1,580; 1 × 700 − 2 = 698. The columns are consistent.

Result, in the project format (before the currency check):

```
date,type,ticker,nom,quantite,prix,frais
2024-01-15,ACHAT,MC.PA,LVMH,3,740,2
2024-03-12,ACHAT,AAPL,APPLE INC,10,157.5,5
2024-05-22,DIVIDENDE,MC.PA,LVMH,0,39,0
2024-09-18,VENTE,MC.PA,LVMH,1,700,2
```

The sidebar summary states in particular the number of transactions and "1 row(s) ignored (custody fees, transfers...).". If a security had not been found, the assistant would have opened at step 3.

### 3. The check

Open the Transactions tab: four transactions. In the Holdings tab: 2 LVMH and 10 Apple.

### 4. Saving

When signed in, enter "Compte titres" in [[Portfolio name]] under [[Save to my space]], then click [[Save]]. Remove the file from the upload area and choose "My space · Compte titres" in the list.

### 5. Adding a trade confirmation

In October, you buy 4 LVMH. Click [[Add transactions]], [[From a file]] tab, and drop in the PDF trade confirmation. The [[Check before saving]] table shows the purchase with the status "new". You mistakenly drop in a second copy of the same confirmation: its row is marked "already in the portfolio" and unticked. Click [[Save transactions]].

### 6. A correction

You realise that the October purchase was for 3 securities, not 4. Transactions tab, [[Edit transactions]], quantity 4 replaced by 3. The summary shows "quantity: 4 → 3". Tick [[I confirm these changes]], then [[Save changes]]. In case of error, [[Undo last change]] restores the previous version.
