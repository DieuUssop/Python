# Error messages and problems
<!-- chapitre: erreurs | ordre: 11 -->

This chapter lists the error and warning messages the software may display, with their exact text in quotation marks, their cause and what to do. It then covers the problems that occur without a message: software that does not open, blank page, busy port, installation warnings, prices that do not move, empty chart, security not found or slowness. An ellipsis replaces the variable part of a message (a security name, a date, a number). Where a message exists in the English interface, its English text is quoted; a few messages are not yet translated in the program and are still displayed in French: for those, the French text is given first and an English rendering follows.

## "No transactions file: upload a CSV file from the sidebar."
<!-- fiche: erreur-aucun-fichier | questions: no transactions file ; the dashboard is empty at launch ; there is no portfolio in the list ; message upload a csv file ; I have no portfolio to analyse ; the list of portfolios is empty ; nothing shows except a red message | mots: no file, missing portfolio, empty list, file upload, sample portfolios, missing data -->

### Cause

No portfolio is available: no file uploaded, no portfolio saved in your space, and no sample portfolio found in the software's `data` folder (`transactions*.csv` files).

### Solution

1. In the sidebar, under "Data", use [[Upload a file (CSV, Excel or PDF)]] to load your transactions.
2. Or sign in with [[Sign in]]: your saved portfolios then appear in the list.
3. If you do not have a file yet, download the [[File template]], fill it in and upload it.

The software is shipped with sample portfolios. If the list is empty, the `transactions*.csv` files in the `data` folder may have been moved or deleted: reinstalling the software puts them back (your accounts are kept).

The "Manual and help" area remains accessible even without a portfolio.

## "Unable to analyse the portfolio: …"
<!-- fiche: erreur-impossible-analyser | questions: unable to analyse the portfolio ; red message unable to analyse ; my portfolio does not show ; error during analysis what do I do ; the calculation of the indicators crashes ; analysis impossible after import ; what does the text after unable to analyse mean | mots: analysis error, failure, crash, red message, diagnosis, import assistant, missing price, impossible sale -->

This general message always comes before a more precise explanation: the portfolio could not be read, valued or calculated. The software prefers to stop rather than display a wrong result. The analysis tabs are then not displayed.

### Read the rest of the message

| Rest of the message | Entry to consult |
|---|---|
| "Vente impossible le …" (sale not possible on …) | Sale not possible |
| "Cours manquant pour : …", "Historique de cours manquant pour : …" (missing price / price history for: …) | Missing price or history |
| "Impossible de récupérer les cours : pas de connexion…" (unable to retrieve prices: no connection…) | No connection and no cache |
| "Taux de change introuvables : …" (exchange rates not found: …) | Exchange rates not found |
| "Impossible de récupérer l'historique de l'indice …" (unable to retrieve the history of the index …) | Benchmark index unavailable |
| "Type(s) de transaction inconnu(s) : …" (unknown transaction type(s): …) | Unknown transaction type |

### What to do right away

- For an uploaded file, the [[Open the import assistant]] button appears under the message: it lets you read the file again in another way (columns, tickers, currencies).
- To add a missing transaction, the [[Add transactions]] button remains available in the sidebar.
- To correct an existing transaction, since the Transactions tab is not displayed, correct your file, or download the portfolio from [[My account]], correct it in a spreadsheet and add it again.
- For a price problem, connect to the Internet and click [[Refresh prices]].

## "Vente impossible le … : on vend … mais on n'en détient que …" (sale not possible)
<!-- fiche: erreur-vente-impossible | questions: sale not possible only holding ; I am selling more than I have ; message sale of but only held on that date ; short selling refused ; a purchase is missing from my file ; sale quantity error ; my statement does not start at the beginning | mots: sale not possible, short selling, quantity held, missing purchase, incomplete history, blocking check | aller: Analyse du portefeuille/Transactions -->

Two wordings exist:

- during the analysis: "Vente impossible le … : on vend … mais on n'en détient que …" (in English: "Sale not possible on …: selling … but only … held");
- when adding or editing transactions: "Sale of … on …, but only … held on that date."

### Cause

The software replays the transactions in date order. On the date shown, the sale covers more securities than you hold. Frequent causes:

- an older purchase is missing, because the statement does not cover the whole history;
- a quantity is wrongly entered or wrongly read;
- the purchase is dated after the sale (day and month swapped);
- a stock split has not been translated into a quantity (see the chapter on sources);
- the same security appears under two different tickers.

### Solution

1. Add the missing purchase with [[Add transactions]] (sidebar button, available even when the analysis fails).
2. To correct an existing quantity or date, correct the original file (or the portfolio downloaded from [[My account]]), then import it again.
3. If you have just deleted a purchase in the Transactions tab, also delete the sales that depend on it: the software reminds you of this under the message.
4. The software does not accept short selling: there is no such thing as a negative position.

## "Cours manquant pour : …" or "Historique de cours manquant pour : …" (missing price or price history)
<!-- fiche: erreur-cours-manquant | questions: missing price for ; missing price history ; no price available after the first transaction ; my security has no price ; ticker spelt wrong ; the software cannot find the price of my share ; delisted security no price | mots: missing price, missing history, unknown ticker, delisted security, Yahoo Finance, local database, offline -->

### The messages

- "Cours manquant pour : …" (missing price for: …): no latest price for a security that is still held.
- "Historique de cours manquant pour : …" (missing price history for: …): no history for a security held at some point, even if sold since.
- "Aucun cours disponible après la première transaction." (no price available after the first transaction): there is no day of prices after your first transaction.

### Causes

- ticker misspelt or unknown to Yahoo Finance (`MC` instead of `MC.PA`, typing mistake);
- security removed from the market, or unlisted fund;
- no Internet, and the security is absent from the local database and the cache;
- for the last message: transactions dated in the future, or offline prices that stop before your first purchase.

### Solution

1. Check the ticker on the Yahoo Finance website, then correct it: import the file again with [[Open the import assistant]] and the [[Yahoo Finance ticker]] column, or correct your file.
2. Connect to the Internet and click [[Refresh prices]]: the security will then be kept in the local database.
3. A security with no prices at all on Yahoo Finance cannot be tracked by the software.

## "Impossible de récupérer les cours : pas de connexion à Yahoo Finance et aucun cache disponible." (unable to retrieve prices)
<!-- fiche: erreur-pas-de-connexion | questions: unable to retrieve prices ; no connection to yahoo finance and no cache ; unable to retrieve the history ; yahoo finance unreachable ; the software does not work without internet ; connection error on prices ; securities missing from the cache and the local database | mots: connection, Internet, Yahoo Finance unreachable, cache, local database, offline, proxy, firewall -->

In English: "Unable to retrieve prices: no connection to Yahoo Finance and no cache available."

Variant for the history: "Impossible de récupérer l'historique : pas de connexion à Yahoo Finance et titres absents du cache et de la base locale." (in English: "Unable to retrieve the history: no connection to Yahoo Finance and securities absent from the cache and the local database.") The message ends with "Détail :" (Detail:) followed by the technical error.

### Cause

Yahoo Finance did not respond (no Internet, filtered network, service outage), and the software found these securities neither in its cache nor in its local database. With the local database shipped, this case mostly concerns securities that it does not contain.

### Solution

1. Check your connection. On a school or company network, a firewall may block Yahoo Finance: try another network (phone tethering, for example).
2. Click [[Refresh prices]].
3. If Yahoo Finance is down, try again later.

Once analysed with Internet, securities remain available offline.

### Not to be confused with

When Yahoo Finance does not respond but the cache is sufficient, there is **no** error: the banner simply displays "Cached prices (offline)".

## "Taux de change introuvables : …" (exchange rates not found)
<!-- fiche: erreur-taux-de-change | questions: exchange rates not found ; current exchange rates not found ; no exchange rate available for ; my us share blocks the analysis ; eurusd error ; currency not converted ; foreign security offline | mots: exchange rate, currency, EURUSD, conversion, foreign security, offline, cache, local database -->

In English: "Exchange rates not found: …". Variants: "Taux de change actuels introuvables." (current exchange rates not found) and "Aucun taux de change disponible pour …" (no exchange rate available for …).

### Cause

The portfolio contains a security quoted in a currency other than the euro, and the corresponding exchange rate (for example `EURUSD=X`) could be obtained neither from Yahoo Finance nor from the local database. The local database contains 12 currencies; a rarer currency is available only with Internet.

### Solution

1. Connect to the Internet, then click [[Refresh prices]].
2. Check the security's currency: offline, it is read from the local database or, failing that, deduced from the code (no suffix = US dollar). A misspelt ticker can lead to an unexpected currency.
3. If a currency was recorded wrongly, deleting the file `data/cache_devises.csv` forces the software to ask Yahoo Finance for it again (Internet required).

## "Impossible de récupérer l'historique de l'indice …" (unable to retrieve the index history)
<!-- fiche: erreur-indice | questions: unable to retrieve the history of the index ; history not found for the sleeve ; no common prices for the composite index ; my benchmark index does not work ; error with the 60 40 index ; change benchmark to unblock | mots: benchmark index, benchmark, composite, sleeve, history, blended index, offline -->

In English: "Unable to retrieve the history of the index …". Variants: "historique introuvable pour la poche … de …" (history not found for the sleeve … of …) and "pas de cours communs pour l'indice composite" (no common prices for the composite index).

### Cause

None of the ETFs that represent the chosen index has a history available (no Internet and absent from the database), or, for a blended index, one of its sleeves (equities or bonds) cannot be found.

### Solution

1. Open [[Settings]], then choose another [[Benchmark index]], for example the MSCI World offered by default.
2. Connect to the Internet and click [[Refresh prices]].

The index is used mainly for comparisons (beta, alpha, tracking error, base 100 chart): changing it unblocks the analysis without changing anything in your positions.

## "Type(s) de transaction inconnu(s) : …" (unknown transaction type)
<!-- fiche: erreur-type-inconnu | questions: unknown transaction type ; prices and quantities must be positive ; my type column contains buy ; only achat vente dividende ; negative quantity refused ; my file contains custody fees ; transaction type not recognised | mots: transaction type, ACHAT, VENTE, DIVIDENDE, negative quantity, negative price, project format -->

In English: "Unknown transaction type(s): …". A related message: "Les prix et les quantités doivent être positifs." (prices and quantities must be positive).

### Cause

These messages are rare, because the import converts most labels and turns quantities positive. A portfolio can contain only three types: `ACHAT` (buy), `VENTE` (sell) and `DIVIDENDE` (dividend). Any other value ("Frais", "Virement"… that is, fees, transfer), or a negative price or quantity, stops the analysis.

### Solution

1. Correct the `type` column of the file, or delete the lines that are not transactions in securities.
2. Write quantities and prices as positive numbers: it is the type that indicates the direction.
3. For a bank export, upload the file as it is instead: the automatic import recognises many labels (achat, buy, souscription, vente, sell, coupon…) and ignores custody fees or transfers. If in doubt, [[Open the import assistant]] and check step 3.

## "Colonne(s) manquante(s) ou non reconnue(s) : …" (columns missing or not recognised)
<!-- fiche: erreur-colonnes | questions: column missing or not recognised ; columns not recognised ; columns recognised but not certain ; what to indicate for the price unit price or total amount column ; why does the import assistant open ; the software does not understand my file ; column to indicate | mots: columns, mapping, header, import assistant, required fields, unit price, total amount -->

In English: "Missing or unrecognised column(s): …". Several wordings, depending on where it appears:

- "Colonne(s) manquante(s) ou non reconnue(s) : …", followed by the columns read and a reminder of the expected format;
- "Colonne(s) non reconnue(s) : …" or "Colonnes reconnues, mais sans certitude sur les quantités, prix et montants." (columns recognised, but no certainty about quantities, prices and amounts), under [[Why is the assistant opening?]];
- "Still needed: …", in the import assistant (in the French interface: "À indiquer : …"), as long as a required field is not matched. The full English text is: "Still needed: {fields}. For the price, either a "Unit price" or a "Total amount" column is enough."

### Cause

The required fields are: the date, the security (ticker, ISIN or name), the quantity, and a unit price **or** a total amount. An unusual column name, a header row that was wrongly detected, or columns of numbers without a meaningful name prevent automatic reading.

### Solution

1. In the assistant, check the [[Header row]] (and the [[Excel sheet]] for a workbook).
2. In step 2, match each field with the right column. Fields marked with an asterisk are required.
3. Check the result in step 4, then click [[Analyse this portfolio]].

## "… ligne(s) avec date illisible (lignes …) : ignorée(s)" and "Aucune transaction lue." (rows ignored)
<!-- fiche: erreur-lignes-ignorees | questions: rows ignored unreadable date ; missing price or amount ; zero quantity ; missing security ; no transaction read ; some rows could not be read ; why do rows of my file disappear | mots: ignored rows, unreadable date, missing price, zero quantity, missing security, row numbers, no transaction -->

In English: "… row(s) with an unreadable date (rows …): ignored". The sentence is built from the cause ("an unreadable date", and so on) and the row numbers.

### The four reasons

| Reason | Cause | Solution |
|---|---|---|
| unreadable date | empty date, written out in words or damaged | correct the date (`15/01/2024` or `2024-01-15`) |
| missing price or amount | buy or sell with no price or amount | complete it, or match the amount column |
| zero quantity | buy or sell of 0 securities | check the quantity column |
| missing security | empty cell, or ISIN without ticker | complete it, or enter the ticker in step 3 |

Rows are numbered from the first data row; beyond five, the list ends with "…".

### Related messages

- "Certaines lignes n'ont pas pu être lues : …" (some rows could not be read: …): for a file in the project format, any row in error prevents direct reading; the assistant opens.
- "Aucune transaction lue." (no transaction read): all rows were ignored. Check the transaction types (step 3) and the column matching (step 2).
- "… row(s) ignored: other kinds of operations (custody fees, transfers...)" (French: "… ligne(s) ignorée(s) : opérations d'un autre type (frais de garde, virements...)"): this is not an error, these rows are not transactions in securities.

## "Unreadable file: …" or "Le fichier est vide." (file is empty)
<!-- fiche: erreur-fichier-illisible | questions: unreadable file ; the file is empty ; my excel file will not open ; file format refused ; old xls file format ; corrupted csv file ; the software does not accept my numbers file | mots: unreadable file, empty file, format, xlsx, csv, pdf, corrupted, Excel sheet -->

### Causes

- empty file, or the chosen Excel sheet contains nothing;
- damaged file, or saved in an unaccepted format: the upload accepts only `.csv`, `.xlsx` and `.pdf` (not the old `.xls`, nor `.ods` or `.numbers`).

### Solution

1. Open the file in your spreadsheet to check that it does contain the transactions.
2. Save it again in `.xlsx` or CSV format.
3. For a workbook with several sheets, choose the right [[Excel sheet]] in the assistant (the software proposes the fullest sheet by default).

## "Titre(s) introuvable(s) : …" (securities not found)
<!-- fiche: erreur-titre-introuvable | questions: security not found ; securities not found at import ; enter its yahoo finance ticker ; the software cannot find my share ; my isin is not recognised ; status not found ; enter the security | mots: security not found, ISIN, ticker, search, Yahoo Finance, manual entry, offline -->

Wordings:

- at import: "Titre(s) introuvable(s) : …" (securities not found: …), followed by the codes concerned; the assistant opens with the status "not found" in step 3;
- in manual entry: "Security not found: …. Enter its Yahoo Finance ticker (e.g. MC.PA).";
- empty field in manual entry: "Enter the security.".

### Solution

1. Look the security up on the Yahoo Finance website and note its ticker (`AI.PA` for Air Liquide).
2. Enter it in the [[Yahoo Finance ticker]] column of the assistant, or directly in the "Security" field of [[Manual entry]].
3. Without a ticker, the rows concerned are ignored.

The possible causes are detailed in the entry "A security is not found: the possible causes".

## PDF messages: scan, image, no transaction found
<!-- fiche: erreur-pdf | questions: scanned pdf impossible to read automatically ; no transaction was recognised in my image pdf ; no transaction found in this pdf ; my trade confirmation is not read ; pdf refused ; print to pdf does not work ; character recognition fails | mots: PDF, scan, image, OCR, trade confirmation, statement, no transaction, PDF format, manual entry -->

### The three messages

| Message (start) | Cause |
|---|---|
| "Scanned PDF (image): it cannot be read automatically…" | PDF with no text and no character recognition engine installed |
| "Image PDF (scan, photo or page printed with "Print to PDF"): the text was read by character recognition, but no transaction was recognised…" | Image read, but without a valid ISIN, quantity and date at the same time |
| "No transaction found in this PDF (no transaction table and no readable trade confirmation)." | Text PDF that is neither a statement in table form nor a recognisable trade confirmation |

A PDF is treated as an image when it contains fewer than 20 characters of text.

### Solution, from the most reliable to the least reliable

1. Download the real PDF from your online banking (the "PDF format" or "Download" button, not "Print").
2. Export the transactions to Excel or CSV.
3. Enter the transaction by hand: [[Add transactions]], [[Manual entry]] tab.
4. From the source code, `python diagnostic_pdf.py` shows what the software has read (see the chapter on import).

## "To read a PDF, install pdfplumber…" and other missing libraries
<!-- fiche: erreur-bibliotheques | questions: install pdfplumber ; install openpyxl ; install reportlab ; no module named ; missing library ; the pdf report is not generated install reportlab ; module not found streamlit | mots: library, module, pip install, pdfplumber, openpyxl, reportlab, source code, requirements -->

### The messages

- "To read a PDF, install pdfplumber: python -m pip install pdfplumber"
- "Pour lire un fichier Excel (.xlsx), installer openpyxl : python -m pip install openpyxl. Ou l'enregistrer au format CSV." (to read an Excel file (.xlsx), install openpyxl: python -m pip install openpyxl; or save it as CSV)
- "Install reportlab: python -m pip install reportlab" (when clicking [[PDF report]])

### Cause

These messages concern only launching **from the source code**: a Python library is missing. The Windows and Mac installers already contain all the libraries.

### Solution

From the project folder, install everything at once:

```
python -m pip install -r requirements.txt
```

Then launch the dashboard again. To read image PDFs, add `python -m pip install -r requirements-ocr.txt` (optional).

## "… price(s) far from that day's market price …" and "Prices not checked…"
<!-- fiche: erreur-prix-eloigne | questions: price far from the market price ; check the ticker currency or a stock split ; prices not checked against market data ; what does median gap mean ; my purchase price does not match ; price alert at import | mots: price check, median gap, 25%, currency, stock split, wrong ticker, no connection -->

### The messages

- "…: … price(s) far from that day's market price (median gap …) — check the ticker, currency or a stock split."
- "Prices not checked against market data (no connection)."

They are displayed in the import summary (sidebar) or in step 4 of the assistant. They are warnings: the import is not blocked.

### Cause of the first

With Internet, each buy and sell price is compared with the closing price of the same day. A price more than 25% above (or 20% below) is flagged. Causes: wrong ticker (another company, another venue), currency or pence wrongly interpreted, stock split, typing mistake.

### Solution

1. Check the ticker used; correct it in [[Yahoo Finance ticker]].
2. In step 4, try another choice of [[Currency of the prices in the file]].
3. For a stock split, express the transaction in securities as they stand after the split.

The second message only means that the check could not take place: check foreign securities yourself.

## "Transaction dated in the future" and other blocking checks
<!-- fiche: erreur-controles-bloquants | questions: transaction dated in the future ; zero quantity or price for ; the portfolio cannot be empty ; these holdings are no longer held ; the save button is greyed out ; I cannot save my changes ; blocking check | mots: check, blocking, future date, zero quantity, zero price, empty portfolio, cannot save | aller: Analyse du portefeuille/Transactions -->

These messages appear on the [[Add transactions]] page or in the Transactions tab, during an edit.

| Message | Cause | Solution |
|---|---|---|
| "Transaction dated in the future: …, on …" | date later than today | correct the date (often day and month swapped) |
| "Zero quantity or price for …, on …" | buy or sell of 0 securities or at €0 | correct the quantity or the price |
| "Sale of … on …, but only … held on that date." | sale greater than the quantity held | see the entry "Sale not possible" |
| "The portfolio cannot be empty: keep at least one transaction." | all transactions are ticked "Delete" | untick at least one row |

As long as one of these messages is displayed, the [[Save transactions]] button (add page) or [[Save changes]] (Transactions tab) remains greyed out; in the Transactions tab, the [[I confirm these changes]] box is also inactive.

### A simple warning

"After this change, these holdings are no longer held: …" does not prevent saving: it tells you that a line is disappearing from the portfolio. Check that this is intended.

## A file refused when adding transactions or in "My account"
<!-- fiche: erreur-ajout-fichier | questions: this file could not be read automatically ; my file is refused in add transactions ; cannot add a portfolio in my account ; red message with my file name ; for an unusual format upload the file from the sidebar ; unusual format | mots: adding transactions, My account, refused file, automatic reading, import assistant, unusual format -->

### The messages

- On the [[Add transactions]] page: the file name followed by the reason (for example "statement.pdf: No transaction found in this PDF…").
- In [[My account]], under "Add a portfolio": "This file could not be read automatically. Upload it from the sidebar…".

### Cause

These two pages use only **automatic** reading. They do not open the import assistant: a file in an unusual format, with ambiguous columns or securities that cannot be found, is refused there.

### Solution

1. Upload the file from the sidebar, with [[Upload a file (CSV, Excel or PDF)]]: the import assistant will guide you.
2. Once the file has been read, save it with the "Save to my space" button that appears under the upload.
3. For just a few transactions, use [[Manual entry]].

## "Incorrect username or password." and "Too many failed attempts…"
<!-- fiche: erreur-connexion | questions: incorrect username or password ; too many failed attempts try again in ; I cannot sign in ; account locked for a minute ; my username is not recognised ; password refused although it is right ; sign-in impossible | mots: sign-in, username, password, lockout, failed attempts, account, security -->

### "Incorrect username or password."

The same message is displayed for an unknown username and for a wrong password: the software does not reveal which accounts exist. Check:

- the username (capitals are converted to lowercase, spaces around it are removed);
- the password, which is case-sensitive (Caps Lock key);
- that you are on the right computer and the right session: accounts are specific to each installation.

### "Too many failed attempts: try again in … seconds."

After 5 failed attempts, the account is locked for one minute. Wait for the delay shown.

### Forgotten password

There is no way to recover it: portfolios are encrypted with it. Create a new account and import your files again (see the chapter on the account).

## Messages when creating the account or changing the password
<!-- fiche: erreur-creation-compte | questions: invalid username ; the password must be at least 8 characters long ; the two passwords do not match ; this username is already taken ; current password is incorrect ; I cannot create my account ; which characters for the username | mots: account creation, invalid username, password too short, confirmation, username already taken, change password -->

| Message | Cause | Solution |
|---|---|---|
| "Invalid username: 3 to 30 characters among lowercase letters, digits, ".", "_" and "-"." | space, accent or special character, or length outside the limits | choose, for example, `marie.dupont` |
| "The password must be at least 8 characters long." | password too short | make the password longer |
| "The two passwords do not match." | typing mistake in the confirmation | enter both fields again |
| "This username is already taken." | account already exists on this computer | choose another username, or sign in |
| "Current password is incorrect." | error in the old password, in [[My account]] | enter the old password again |
| "Incorrect password." | error when deleting the account | enter the password again |

### Other account messages

- "Automatically signed out after 30 minutes of inactivity.": sign in again; your saved portfolios are not lost.
- "Portfolio not found." or "Nothing to undo.": the portfolio has been deleted, or there is no previous version. Reload the page.

## "Optimisation compares allocations across holdings…" and "Optimisation failed: …"
<!-- fiche: erreur-optimisation | questions: optimisation failed ; the optimisation did not converge ; at least 2 holdings are needed in the portfolio ; why is the optimisation tab empty ; efficient frontier missing ; maximum weight impossible ; the optimisation does not work with my portfolio | mots: optimisation, Markowitz, convergence, efficient frontier, maximum weight, number of holdings | aller: Analyse du portefeuille/Optimisation -->

### "Optimisation compares allocations across holdings: the portfolio needs at least 2 holdings."

With a single line, there is nothing to allocate. Add securities to use the tab.

### "Optimisation failed: …"

The message is followed by the cause, most often "L'optimisation n'a pas convergé : …" (the optimisation did not converge: …): the optimiser did not find a solution that respects the constraints. Frequent causes: a security with a very short history (the calculations use only the days on which all securities have a price), almost identical securities, or very tight constraints.

### Solution

1. Change the [[Maximum weight per security]] (only the values that allow 100% to be invested are offered).
2. Wait until recent securities have more history, or analyse the portfolio without them.

### "Approximate" frontier

If the optimiser finds no exact point on the frontier, the software replaces it with the envelope of 4,000 randomly drawn portfolios: this is not an error.

## "Stress tests unavailable: …", "Attribution unavailable: …"
<!-- fiche: erreur-espaces-indisponibles | questions: stress tests unavailable ; attribution unavailable ; risk budget unavailable ; backtest unavailable ; history too short at least two month ends are needed ; no equities in the portfolio ; the wealth advisory tab shows an error | mots: stress tests, attribution, risk budget, backtest, unavailable, history too short, Internet, regional indices -->

These yellow warnings concern the "Wealth advisory" and "Asset management" areas. The rest of the software works normally.

| Message | Frequent causes | Solution |
|---|---|---|
| "Stress tests unavailable: …" | history since 2008 cannot be obtained (no Internet, no cache) | connect, then [[Refresh prices]] |
| "Attribution unavailable: …" | "Historique trop court : il faut au moins deux fins de mois." (history too short: at least two month ends are needed); "aucune action dans le portefeuille…" (no equities in the portfolio…); regional indices not downloaded | wait for a full month of history; attribution covers only the equity sleeve |
| "Risk budget unavailable: …" | calculation impossible; the rest of the message gives the reason | check the history of recent securities |
| "Backtest unavailable: …" | not enough days on which all securities have a price | same |

The PDF report calculates these analyses separately: if one fails, the others still appear in it.

## "n.d." in place of a figure
<!-- fiche: erreur-nd | questions: why n.d. ; cornish fisher n.d. ; irr n.d. ; an indicator shows n.d. ; figure not available ; missing value in the table ; nan in the indicators | mots: n.d., not available, n/a, NaN, Cornish-Fisher, IRR, missing indicator | aller: Analyse du portefeuille/Risque -->

"n.d." (French for "non disponible") means "not available": the calculation makes no sense or did not succeed. It is not a crash. In the English interface, the same condition is written "n/a".

### Common cases

- **Cornish-Fisher VaR**: the note "Cornish-Fisher n/a: skewness or kurtosis too large, the adjustment is no longer reliable." appears under the table. The formula no longer preserves the ordering of losses: use the historical VaR and the CVaR.
- **IRR (TRI)**: no rate between −99% and +1,000% per year cancels out the cash flows (extreme cases, or a very short history).
- **Annualised TWR**: first and last day identical.
- **Shape indicators** (skewness, kurtosis): fewer than 4 days of history; they are then 0 by convention.

Most often, these indicators become available with a longer history (see the chapter "All the formulas").

## The assistant answers "I could not find a reliable answer in the manual."
<!-- fiche: erreur-assistant | questions: I could not find a reliable answer in the manual ; the assistant cannot find anything ; the help does not answer my question ; the manual cannot be found ; the assistant does not understand ; no answer in the manual | mots: assistant, help, search, no answer, manual, questions, log | aller: Manuel et aide -->

### Cause

The assistant does not write anything itself: it looks for the manual entry closest to your question. If none matches well enough, it says so rather than answering off the point, and offers the "Closest entries".

### Solution

1. Rephrase with other words: simpler ("remove a purchase") or more technical ("delete a transaction").
2. Use the exact name of an indicator or a button ("VaR", "PRU", "Refresh prices").
3. Browse the [[Manual contents]], chapter by chapter.
4. Your question is recorded on this computer; you can send it to the creator with [[Export the questions (CSV)]] to complete the manual.

### "The manual cannot be found (docs/manuel folder)."

The manual files are missing from the software's folder: reinstall it.

## The software does not open
<!-- fiche: erreur-ne-souvre-pas | questions: the software does not open ; nothing happens when I click the icon ; the dashboard could not start ; the black window closes immediately ; the application does not launch ; double click has no effect ; portfolio tracker no longer starts | mots: startup, launch, black window, Terminal, launcher, will not start, startup error -->

### Nothing happens

1. Wait a few seconds: the first start is longer (see the entry on slowness).
2. Look at the taskbar (Windows) or the Dock (Mac): the black window or the Terminal may be hidden behind another window.
3. On Mac, at first launch, macOS blocks the application: see the entry "Windows or macOS warnings at installation".

### The black window shows "Le tableau de bord n'a pas pu démarrer (voir le message ci-dessus)."

(In English: "The dashboard could not start (see the message above).") The server has stopped. The technical message above gives the reason. Press Enter to close, launch again, and if the error persists, take a photo of the message and pass it on to your teacher or to the software's creator. You can also reinstall the latest version: your accounts are kept.

### The black window is open, but not the dashboard

The launcher waits up to three minutes for the dashboard to be ready. After that, open your browser yourself at the address shown in the black window, for example `http://localhost:8501`.

### The software was already open

Clicking the icon again does not launch it a second time: it reopens the dashboard window ("Portfolio Tracker est déjà ouvert : ouverture de la fenêtre...", that is, "Portfolio Tracker is already open: opening the window...").

## The page stays blank or shows a connection error
<!-- fiche: erreur-page-blanche | questions: blank page ; the window stays blank ; unable to connect to localhost ; this site cannot be reached localhost ; the dashboard does not load ; grey screen ; connection refused | mots: blank page, localhost, connection refused, reload, black window, server stopped, browser -->

### Causes and solutions

1. **The black window (or the Terminal) was closed**: the software is stopped, the page can no longer load. Launch it again with the "Portfolio Tracker" icon.
2. **The dashboard is still starting**: be patient, then reload the page (F5 or Ctrl + R; Cmd + R on Mac).
3. **Wrong port number**: the address must be the one displayed in the black window (8501, or a following number up to 8510).
4. **A long calculation is under way**: a waiting message is then displayed at the top of the page ("Fetching prices and computing indicators...", for example). Let it finish.

### If nothing works

Close the black window, then launch the software again, after restarting the computer if necessary. The dashboard needs no Internet connection to be displayed: `localhost` means your own computer.

## "Aucun port libre entre 8501 et 8510": the port is busy
<!-- fiche: erreur-port-occupe | questions: no free port between 8501 and 8510 ; port busy ; port 8501 already in use ; close another application then try again ; address already in use ; streamlit port conflict ; two streamlit applications | mots: port, 8501, 8510, localhost, busy port, Streamlit, conflict, launcher -->

### How the software chooses its port

At launch, it goes through ports 8501 to 8510:

- if the dashboard is already running on one of them, it simply reopens its window;
- otherwise, it starts on the first free port.

### The message

"Aucun port libre entre 8501 et 8510 : fermez une autre application puis réessayez." (in English: "No free port between 8501 and 8510: close another application then try again."), followed by "Appuyez sur Entrée pour fermer." ("Press Enter to close."). All ten ports are occupied by other programs, often other Streamlit applications, or old windows of the software left open.

### Solution

1. Close the other black windows or Terminals (old launches, other Streamlit projects).
2. Launch Portfolio Tracker again.
3. If the problem persists, restart the computer.

## Windows or macOS warnings at installation
<!-- fiche: erreur-avertissement-installation | questions: windows protected your pc ; unknown publisher ; the developer cannot be verified ; antivirus blocks portfolio tracker ; edge blocks the download ; macos refuses to open the application ; is it a virus | mots: SmartScreen, Gatekeeper, unknown publisher, warning, antivirus, signature, installation, security -->

The Windows installer and the Mac application are not signed with a paid publisher certificate nor distributed through the App Store. The warnings are therefore normal.

### Windows

- **Edge** may block the download: in the downloads list, "…" menu, choose to keep the file.
- **"Windows protected your PC"** (SmartScreen): click "More info", then "Run anyway".
- **Antivirus**: if the file comes from the official releases page, you can allow it.

### Mac

- **macOS 15 and later**: at the blocking message, click "Done", open System Settings, Privacy & Security, then "Open Anyway".
- **macOS 12 to 14**: right-click the application, "Open", then "Open".
- The application requires an Apple Silicon Mac (M1 and later): on an Intel Mac, use the online version.

Download only from `https://github.com/DieuUssop/Python/releases/latest` or the link from your teacher. The details are in the chapter "Getting started".

## The prices are not updating
<!-- fiche: erreur-cours-pas-a-jour | questions: the prices are not updating ; the prices are the same as an hour ago ; why are the prices from yesterday ; cached prices offline ; refresh prices changes nothing ; the price is not the current one ; the prices are frozen | mots: price update, cache, refresh, an hour, offline, data as of, latest price, weekend -->

### Check the source first

- Banner: "Live prices · Yahoo Finance" (green dot) or "Cached prices (offline)" (orange dot).
- "Data as of": the date of the last price in the history.
- Sidebar, "Prices" line: "Yahoo Finance (en direct)" (live), or "cache local du" (local cache of) followed by a date. These two sidebar texts are displayed in French.

### The causes

1. **The one-hour memory**: as long as the portfolio and the settings do not change, results are kept for an hour and prices are not requested again. Click [[Refresh prices]].
2. **No Internet, or Yahoo Finance unreachable**: the software uses its cache and its local database. Reconnect, then refresh.
3. **Market closed**: at weekends or on a public holiday, the latest price is that of the last session. This is normal.
4. **Suspended or delisted security**: it keeps its last known price, with no alert.

### What the software uses

The closing price (or a value from the current session if the exchange is open), never a real-time feed.

## A chart is empty or missing
<!-- fiche: erreur-graphique-vide | questions: the chart is empty ; the world map does not show ; no correlation chart ; at least two positions are needed ; no equity allocation to analyse ; the donut chart has disappeared ; the chart does not display | mots: empty chart, world map, correlations, donuts, equity sleeve, bonds, display -->

### The cases the software provides for

| What you see | Cause |
|---|---|
| Empty world map | map background never saved and no Internet |
| World map missing | no share with a known country (100% bond, gold or money-market portfolio) |
| Donut by region or by sector missing | only one group: the donut is drawn only from two groups |
| "At least two positions are needed." | correlations with a single line |
| "No equity allocation to analyse." | regions and sectors with no equities |
| "The portfolio holds no bonds." | rate sensitivity without any bonds |
| Optimisation tab without a chart | fewer than 2 securities, or optimisation impossible |

### Other causes

- **A click in the legend** hides a curve: click its name again to show it again.
- **A zoom** that is too tight: double-click in the chart to return to the overall view.
- **Very short history**: with only a few days, the curves and histograms are almost empty.

## A security is not found: the possible causes
<!-- fiche: erreur-titre-introuvable-causes | questions: why is my security not found ; my fund does not exist on yahoo ; my share has no ticker ; life insurance euro fund not found ; sicav not found ; the software does not know this security ; how do I find the yahoo ticker | mots: security not found, ticker, ISIN, unlisted fund, UCITS, euro fund, Yahoo Finance, trading venue -->

The software knows only the securities that have a **Yahoo Finance ticker** with daily prices.

### The causes, in order of frequency

1. **No Internet**: only the 31 ETFs of the built-in table, the memory of recognised securities and the local database are consulted.
2. **Abbreviated name**: "AM.C.C.40 UC.ETF C" gives nothing; it is the ISIN that allows recognition.
3. **Ticker without a venue** (`MC`, `AIR`): the software looks for the listing whose price matches your prices (median gap below 15%); failing that, it queries the search engine, which may find nothing.
4. **Unlisted product**: euro funds of life insurance (assurance-vie), some UCITS funds (OPCVM), structured products, bonds with no listing on Yahoo Finance. They cannot be tracked.
5. **Delisted or merged security**: Yahoo Finance sometimes no longer has its history.

### Finding the right ticker

On the Yahoo Finance website, search for the name or the ISIN, then note the full code with its venue: `.PA` (Paris), `.DE` (Frankfurt), `.AS` (Amsterdam), `.L` (London), nothing for the United States. Enter it in [[Yahoo Finance ticker]] (import assistant) or in [[Manual entry]].

## The software is slow, especially at first launch
<!-- fiche: erreur-lenteur | questions: the software is slow ; first launch takes very long ; it takes a long time to load ; the stress tests take a while ; why is the calculation slow ; the pdf takes a long time to be read ; the online site is slow | mots: slowness, loading, first launch, waiting, download, cache, performance, spinner -->

### At first launch

- **On Mac**, at the first launch of a new version, the application copies its code and its securities database into `~/Library/Application Support/Portfolio Tracker` before starting.
- **Everywhere**, the dashboard server has to start: allow a few seconds.

### At the first display of a portfolio

Prices are downloaded from Yahoo Finance ("Fetching prices and computing indicators..."). After that, the results are kept for an hour: navigation becomes fast.

### The longest calculations

- **stress tests**: download of the history since 2008, then kept in cache;
- **performance attribution**: download of the regional indices;
- **reading an uploaded file**: checking prices, searching for unknown securities;
- **image PDF**: character recognition, several seconds;
- **PDF report**: all the analyses recalculated.

### Tips

- Avoid [[Refresh prices]] without a reason: it clears all the memory.
- The online version may be slower, especially if the site was asleep.
