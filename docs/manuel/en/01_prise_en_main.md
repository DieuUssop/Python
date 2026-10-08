# Getting started
<!-- chapitre: demarrage | ordre: 1 -->

This chapter explains what Portfolio Tracker is, how to install it on Windows or Mac, how to start and close it, what works without Internet, how to update or uninstall it, and how to use it online or from its source code. Start here if you are new to the software.

## What is Portfolio Tracker and who is it for?
<!-- fiche: demarrage-presentation | questions: what is this software ; what is portfolio tracker for ; what can I do with this program ; is it investment advice ; who is this tool made for ; does the software connect to my bank ; what exactly does the app do ; software overview ; who is this software aimed at ; which master's programme is it for ; is it the iae caen project ; what does g2c stand for | mots: overview, purpose, features, Master G2C, asset management, risk control, compliance, IAE Caen, University of Caen Normandy, educational tool, portfolio tracking, dashboard | aller: Analyse du portefeuille -->

Portfolio Tracker is a tool for tracking and analysing a securities portfolio, built by a student of the Master G2C (Asset Management, Risk Control and Compliance) at IAE Caen (University of Caen Normandy), as part of the programme. It reads a portfolio's transaction history (purchases, sales, dividends), values it at market prices and calculates the indicators used by investment professionals.

### What it does

- **Tracking**: cost basis per unit (PRU), unrealised and realised gains, dividends, fees, day-by-day value, foreign-currency holdings converted into euros.
- **Performance and risk**: TWR (time-weighted return), IRR (TRI), comparison with a benchmark index, volatility, drawdown, Sharpe and Sortino ratios, beta, alpha, VaR and CVaR.
- **Advanced analyses**: look-through exposures, Markowitz optimisation, Monte Carlo projection.
- **Wealth advice**: comparative taxation of the CTO (securities account), PEA (French equity savings plan) and assurance-vie (life insurance), stress tests.
- **Asset management**: performance attribution, risk budget, strategy backtesting.
- **Reporting**: interactive dashboard in French or English, and a PDF summary report.

### Who it is for

It was designed first for the students and teachers of the Master G2C at IAE Caen: it applies, on a real portfolio, the three strands of the programme: **asset management** (performance measurement and attribution, allocation, Markowitz optimisation, strategy backtesting), **risk control** (volatility, historical, normal and Cornish-Fisher VaR, CVaR, stress tests, risk budget, exposure diagnosis) and **compliance** (checks on the transactions entered, traceability of sources, encrypted data and personal data protection). It can also be used by any individual who wants to understand the performance and risk of their portfolio.

### What it does not do

- It does not connect to your bank or your broker: you give it your transactions as a file (CSV, Excel or PDF) or by manual entry.
- It does not place any stock market orders.
- Its results do not constitute investment advice: it is an educational tool, as the footer of every screen reminds you.

## What computer do I need to use the software?
<!-- fiche: demarrage-configuration | questions: system requirements ; will it work on my pc ; does it work on an intel mac ; which version of windows do I need ; which macos do I need ; does it work on linux ; do I need to install python ; my computer is too old | mots: minimum requirements, prerequisites, Windows 64-bit, Apple Silicon, M1, macOS 12, operating system, compatibility -->

The software comes in two installable versions and one online version.

| System | Version to use | Conditions |
|---|---|---|
| Windows | `.exe` installer | 64-bit Windows (Windows 10 or 11) |
| Recent Mac | `.dmg` disk image | Mac with an Apple Silicon chip (M1, M2, M3, M4…) and macOS 12 or later |
| Intel Mac (before late 2020) | Online version | The Mac application is not designed for these models |
| Linux or other | Source code | Python installed (see the entry on launching from the source code) |

### What you do not need to install

The Windows and Mac versions contain their own Python and all the necessary libraries: you have nothing else to install. No administrator password is requested on Windows.

### The browser

The dashboard is displayed in a browser window. On Windows, it uses Microsoft Edge (present on Windows 10 and 11) or, failing that, Google Chrome. On Mac, it uses Google Chrome, Microsoft Edge or Brave if installed, otherwise your default browser (usually Safari).

### Internet

A connection is only needed to download the software and to obtain the most recent prices. Everything else works offline (see the entry "Using the software without Internet").

## Where do I download the software?
<!-- fiche: demarrage-telecharger | questions: where do I download the software ; download link ; how do I get the installer ; I can't find the exe file ; where to find the dmg for mac ; what is the latest version ; github releases page ; download portfolio tracker | mots: download, GitHub, Releases, installer, exe, dmg, latest version -->

The installers are published on the releases page ("Releases") of the project's GitHub repository:

`https://github.com/DieuUssop/Python/releases/latest`

This address always opens the most recent version. In the "Assets" section of the page, choose the file that matches your computer:

| File | For |
|---|---|
| `Installer_Portfolio_Tracker.exe` | Windows |
| `Portfolio_Tracker_Mac.dmg` | Mac with Apple Silicon |

Do not download the "Source code" archives offered by GitHub on the same page: they contain the project's code, which is only useful for launching it as a developer (see the entry on the source code).

### Version number

Each version carries a number made up of its build date (for example "2026.10.05"). The installers are built automatically by GitHub, on Windows and Mac machines, and then published together in the same release.

### The software does not update itself

The software does not check by itself whether a new version exists. To get one, come back to this page and install the new version over the old one: your accounts are kept (see the entry "Updating the software").

## Installing the software on Windows
<!-- fiche: demarrage-installer-windows | questions: how do I install on windows ; step by step installation ; I downloaded the exe so now what ; where does the program install ; do I need to be an administrator ; how do I get the desktop icon ; which folder is portfolio tracker installed in ; install for a single user | mots: installation, setup, installer, exe, Windows, AppData, Start menu, shortcut, Desktop -->

### The steps

1. Download `Installer_Portfolio_Tracker.exe` from the project's releases page.
2. Double-click the file. If Windows displays "Windows protected your PC", follow the entry "Windows or Edge blocks the installer".
3. The installation wizard opens (in French or English). Click Next.
4. If you wish, leave ticked the box that creates a Desktop icon.
5. Click Install, then Finish. The last page offers to launch Portfolio Tracker straight away.

### An installation for you alone

The installation is done for the current Windows user, without administrator rights. The software is placed in your personal folder:

`C:\Users\<your name>\AppData\Local\Programs\Portfolio Tracker\`

If several people use the same computer with different Windows sessions, each must install it in their own session. Conversely, several people can share the same Windows session: each then creates their own encrypted account in the software.

### What the installation creates

- a "Portfolio Tracker" shortcut in the Start menu (and on the Desktop if the box was ticked);
- an uninstall shortcut in the same Start menu group;
- the program folder, which contains its own Python, the software's code and the local securities database (prices usable offline).

### Next

Launch the software with the "Portfolio Tracker" icon. A small black window opens, then the dashboard in its own window: see the entry "Launching the software".

## Windows or Edge blocks the installer: what should I do?
<!-- fiche: demarrage-avertissement-windows | questions: windows protected your pc ; smartscreen blocks the installation ; edge says the file is dangerous ; run anyway where is the button ; my antivirus blocks the exe ; is it a virus ; unknown publisher ; cannot launch the installer | mots: SmartScreen, warning, unknown publisher, More info, Run anyway, antivirus, unsigned program, security -->

The installer is not signed with a publisher certificate (such a certificate costs money every year). Windows and Microsoft Edge therefore display warnings, which are normal for this type of software.

### When downloading in Microsoft Edge

Edge may report that the file is not commonly downloaded and block it. Open the downloads list, click the "…" menu next to the file, then choose to keep it ("Keep", then possibly "Keep anyway"). The exact wording depends on the version of Edge.

### On launch: "Windows protected your PC"

This SmartScreen message appears when you double-click the installer.

1. Click the **More info** link.
2. The program name and the line "Publisher: Unknown publisher" appear.
3. Click the **Run anyway** button.

The installation then continues normally.

### If your antivirus blocks the file

The cause is the same: the program is not signed. If you downloaded it from the project's official releases page, you can allow it in your antivirus. If in doubt, ask your teacher or your IT department for advice.

### Good habit

Always download the installer from the project's releases page (`https://github.com/DieuUssop/Python/releases/latest`) or from the link provided by your teacher, never from a third-party site.

## Installing the software on Mac
<!-- fiche: demarrage-installer-mac | questions: how do I install on mac ; macbook installation ; what do I do with the dmg file ; drag to applications ; does it work on mac m1 ; install portfolio tracker on macos ; where is the app on mac ; does it work on an intel mac | mots: Mac, macOS, dmg, Applications, Apple Silicon, M1, M2, installation, MacBook -->

### The steps

1. Download `Portfolio_Tracker_Mac.dmg` from the project's releases page.
2. Double-click the `.dmg` file: a window opens with the "Portfolio Tracker" application, a shortcut to the "Applications" folder and a `LISEZ-MOI.txt` file (the French "read me" file).
3. Drag "Portfolio Tracker" onto the "Applications" folder.
4. Open the Applications folder and double-click "Portfolio Tracker".

The very first time, macOS refuses to open the application because it does not come from the App Store: follow the entry "macOS refuses to open the application". This step only has to be done once.

### Conditions

- Mac with an Apple Silicon chip (M1, M2, M3, M4…);
- macOS 12 or later.

Macs with an Intel processor (sold before late 2020) are not supported by this application: use the online version of the dashboard.

### What happens at launch

A Terminal window opens (it is the equivalent of the black window on Windows), then the dashboard, in Chrome or Edge in "application" mode if they are installed, otherwise in your default browser. Leave the Terminal window open while you are using the software.

### Where your data is

Your encrypted accounts and portfolios are stored in:

`~/Library/Application Support/Portfolio Tracker`

They are kept when you install a new version.

## macOS refuses to open the application on first launch
<!-- fiche: demarrage-mac-bloque | questions: cannot open portfolio tracker because the developer cannot be verified ; mac blocks the application ; open anyway mac ; app is damaged or unverified ; gatekeeper blocks it ; right click open doesn't work ; macos sequoia blocks the app ; how do I allow the app on mac | mots: Gatekeeper, macOS security, Privacy and Security, Open Anyway, unidentified developer, Sequoia, permission -->

The application is not distributed through the App Store and is not signed by Apple. At first launch, macOS therefore prevents it from opening. How to allow it depends on your version of macOS.

### macOS 15 (Sequoia) and later

1. At the blocking message, click "Done".
2. Open System Settings, then Privacy & Security.
3. Scroll down to the message about "Portfolio Tracker".
4. Click "Open Anyway", then confirm (macOS may ask for your login password).

### macOS 12 to 14

1. In the Applications folder, right-click (or Ctrl-click) "Portfolio Tracker".
2. Choose "Open".
3. In the window that appears, click "Open" again.

### Only once

Once the application has been allowed, it then opens with a simple double-click. You may need to do this again after installing a new version.

### The Terminal opens: this is normal

Launching opens a Terminal window that runs the dashboard. Do not close it while you are using the software: closing it stops the software.

## Launching the software: the black window and the dashboard window
<!-- fiche: demarrage-premier-lancement | questions: how do I open the software ; why does a black window open ; what is the black console at launch ; the software opens in edge is that normal ; why does it open in the browser ; first launch ; what is localhost 8501 ; can I close the black window | mots: launch, startup, black window, console, Terminal, Edge, Chrome, application mode, localhost, 8501 -->

### What happens when you click the icon

1. **A black window opens** (the Terminal on Mac). It shows the software's name, the dashboard address and this message: leave this window open while you are using the software, close it to quit the application. It is the software's "engine".
2. **The dashboard opens in its own window**, as soon as it is ready (allow a few seconds). It is a Microsoft Edge or Google Chrome window in "application" mode: with no address bar or tabs, it looks like a conventional piece of software. If neither of these browsers is found, the dashboard opens in your usual browser.

### Why a browser?

The software is a web application that runs on your own computer. Its address begins with `http://localhost:` followed by a number (usually 8501, or the next free one up to 8510). "localhost" refers to your computer itself: nothing goes through the Internet to display the dashboard, and nobody else on the network (the school Wi-Fi, for example) can connect to it.

### What you see first

The dashboard opens on the "Portfolio analysis" space, with the first portfolio in the list. You can immediately choose another one, upload your own file or sign in to your personal space (see the chapter "The screen and navigation").

### If you click the icon a second time

If the software is already running, it is not started again: the dashboard window is simply reopened. This is useful if you closed the dashboard window by mistake, as long as the black window is still open.

## The dashboard does not open
<!-- fiche: demarrage-fenetre-ne-souvre-pas | questions: nothing opens when I launch the software ; the dashboard window doesn't show ; blank page at startup ; no free port ; the dashboard could not start ; the black window opens but nothing else ; the software won't launch ; it keeps loading forever | mots: launch problem, troubleshooting, startup error, port, 8501, localhost, blank page, won't start -->

### The black window is open but no window appears

The first start can take a little while. If nothing appears, open your browser yourself and type the address shown in the black window, for example `http://localhost:8501`. The software waits up to three minutes for the dashboard to be ready before opening the window; after that, it keeps running, but it is up to you to open the address.

### Message "No free port between 8501 and 8510"

The software uses the first free number between 8501 and 8510. If all of them are taken by other programs, it cannot start. Close another application (for example another Streamlit application), then relaunch Portfolio Tracker.

### Message "The dashboard could not start"

A technical error message is displayed just above. Press Enter to close the window, then relaunch. If the error persists, note down or photograph this message and pass it on to your teacher or to the software's creator.

### The window opens but stays blank or shows a connection error

Check that the black window is still open: if it has been closed, the software has stopped. Relaunch it with the icon.

### The dashboard shows "Unable to analyse the portfolio"

The software is working, but the chosen portfolio could not be read or valued. Choose another portfolio or see the chapter on importing files.

## Closing the software
<!-- fiche: demarrage-fermer | questions: how do I quit the software ; how do I close portfolio tracker ; I closed the window but it is still running ; do I need to close the black window ; stop the application ; quit on mac ; ctrl c to stop ; is my data saved when I close | mots: quit, close, stop, exit, black window, Terminal, Ctrl+C, end of session -->

### On Windows

Close the **black window**: it is what runs the software. Closing only the dashboard window does not stop it; you can in fact reopen it by clicking the "Portfolio Tracker" icon again.

### On Mac

Close the **Terminal window** opened at launch. macOS asks whether you want to end the running process: click "Close". The dashboard stops with it.

### From the source code

If you launched the software with the command `python -m streamlit run app.py`, press Ctrl + C in the terminal.

### Is your data saved?

- Portfolios saved in your personal space are written to disk, encrypted, when you save or modify them: nothing is lost on closing.
- By contrast, a file simply uploaded in the sidebar, without being saved to your space, is not kept: you will have to upload it again the next time you open the software.
- Your session (signed-in account, language, screen settings) ends when you close it. The light or dark mode chosen while you were signed in is restored the next time you sign in.

Without closing the software, you are in any case signed out of your account automatically after 30 minutes of inactivity.

## Does my data leave my computer?
<!-- fiche: demarrage-confidentialite | questions: is my data sent over the internet ; does my portfolio go to a server ; data privacy ; who can see my positions ; gdpr ; does yahoo see my amounts ; can someone on the wifi see my dashboard ; is it secure | mots: confidentiality, privacy, GDPR, security, personal data, localhost, encryption, Yahoo Finance -->

With the installed version (Windows or Mac), everything stays on your computer.

### The dashboard runs locally

The software runs at the address `localhost`, that is, on your computer itself. It accepts no connection from another device: nobody on the same network can open your dashboard.

### Your portfolios are encrypted

Portfolios saved in your personal space are encrypted with a key derived from your password. Other users of the same computer cannot read them. The trade-off: a forgotten password makes the portfolios permanently unreadable (see the chapter on accounts).

### What is sent over the Internet

To obtain prices, the software queries Yahoo Finance with the **security codes** (tickers) and, to recognise an unknown security during an import, with its ISIN code or its name. Quantities, amounts and the composition of your portfolio are never sent.

### Questions asked to the assistant

The manual's assistant works without Internet. Questions left unanswered are recorded in a file on your computer only; they are passed on to nobody, unless you export that file yourself.

### The online version

On the online version, the software runs on a remote server: the files you upload there are processed on that server. For real personal data, prefer the installed version.

## Using the software without Internet
<!-- fiche: demarrage-hors-connexion | questions: does it work without internet ; use offline ; offline mode ; I'm on the train with no wifi ; why are the prices not up to date ; what does cached prices mean ; the prices are from a long time ago ; no connection does the software still work | mots: offline, without Internet, cache, local database, cached prices, aeroplane -->

The software is designed to work without Internet. It comes with a **local securities database**: the record of several thousand shares, ETFs, indices and exchange rates, with their daily closing prices (since 2015 for securities, since 2007 for indices and exchange rates).

### What works offline

- opening the dashboard, signing in to your account, opening your portfolios;
- analysing a portfolio whose securities are in the database or in the cache;
- importing a CSV or Excel file, recognising ISIN codes or names already known to the database or to the securities memory;
- converting currencies, comparing with a benchmark index, and using the other spaces;
- the world map, if its base map has already been saved;
- the assistant and the manual.

### How to tell that the prices are not from today

- In the banner at the top of the page, the badge reads "Cached prices (offline)" with an orange dot, instead of "Live prices · Yahoo Finance".
- At the bottom of the sidebar, the "Prices" line reads "local cache of" followed by the date of the latest known prices, and the note "Yahoo Finance unreachable".

Offline, prices therefore stop at the latest date known to the database or the cache. The calculations remain correct, but as of that date.

### When Internet comes back

Prices are completed automatically at the next analysis. Since results are kept in memory for one hour, use the [[Refresh prices]] button to force an immediate download.

### Limitation

A security that is absent from the local database and has never been encountered before has no price offline: the software flags it.

## What requires an Internet connection
<!-- fiche: demarrage-internet-necessaire | questions: when do I need internet ; what doesn't work without a connection ; why does my security have no price ; refresh prices doesn't work ; the world map is empty ; do I need internet to install ; unknown security offline ; what is the connection for | mots: Internet, connection required, online, Yahoo Finance, price download, world map, base map, update -->

Most functions work offline. Internet is still needed in the following cases.

| Situation | Why |
|---|---|
| Downloading the installer or a new version | The files are on the project's releases page |
| Getting today's prices | They come from Yahoo Finance |
| Analysing a security that is absent from the local database | Its history has to be downloaded the first time (it is then added to the database) |
| Recognising, at import, an unknown ISIN code or company name | The search is made with Yahoo Finance (the result is then remembered) |
| [[Refresh prices]] button | It downloads the prices again |
| Displaying the world map if its base map has never been saved | The country outlines are downloaded once, then kept on the computer |
| Launching the software from the source code for the first time | The Python libraries have to be installed |

### The database learns as it goes

Each time the software downloads prices or recognises a security, it adds them to its local database or its memory. The next time, this information is available even without Internet.

### If Yahoo Finance does not respond

The software does not crash: it uses the latest saved prices and says so in the banner ("Cached prices (offline)") and at the bottom of the sidebar. If it has no price at all for a security, a clear message flags it.

### What never needs Internet

Reading your files, the calculations, your encrypted accounts, the PDF report and the manual's assistant all work entirely on your computer.

## Updating the software
<!-- fiche: demarrage-mettre-a-jour | questions: how do I install a new version ; update portfolio tracker ; do I lose my portfolios if I reinstall ; do I have to uninstall first ; update on mac ; does the software update itself ; new version available ; reinstall over the top | mots: update, new version, reinstall, upgrade, keep accounts -->

The software does not update automatically. To move to a new version, download it from the project's releases page and install it over the old one. **Your accounts and saved portfolios are kept.** There is no need to uninstall first.

### On Windows

1. Close the software (close the black window).
2. Download the new `Installer_Portfolio_Tracker.exe`.
3. Launch it and follow the same steps as the first installation.

The installer completely replaces the embedded Python and the software's code. The accounts folder (`data\comptes`) is never touched by an update.

### On Mac

1. Close the software (close the Terminal window).
2. Open the new `Portfolio_Tracker_Mac.dmg`.
3. Drag "Portfolio Tracker" onto "Applications" and agree to replace the old application.

At the next launch, the application detects the new version and replaces its code and its securities database, keeping your accounts and the memory of recognised securities, stored in `~/Library/Application Support/Portfolio Tracker`. You may need to allow the application again (see the entry "macOS refuses to open the application").

### Precaution

Even though updates keep accounts, keep a copy of your important portfolios: the "My account" page lets you download each of them as a CSV file.

## Where is my data saved?
<!-- fiche: demarrage-ou-sont-donnees | questions: where are my portfolios stored ; which folder are my accounts in ; where is the data folder ; back up my data ; changing computer how do I recover my portfolios ; application support folder mac ; appdata portfolio tracker ; where is the securities database | mots: folder, location, storage, backup, AppData, Application Support, data, accounts, securities database -->

### On Windows

In the program folder:

`C:\Users\<your name>\AppData\Local\Programs\Portfolio Tracker\`

- `data\comptes\`: the encrypted accounts and portfolios of each user of this computer;
- `data\base\`: the local securities (prices) database and the memory of recognised securities.

The `AppData` folder is hidden by default in File Explorer: type the path into the address bar to reach it.

### On Mac

`~/Library/Application Support/Portfolio Tracker`

In the Finder, open the Go menu, then "Go to Folder…", and paste this path.

### From the source code

In the project's `data` folder (`data/comptes` and `data/base`).

### The files are encrypted

The portfolios and the list of their names are encrypted, and account folders have random names. The files can only be read through the software, with the right password.

### Changing computer or making a backup

The simplest and safest method: sign in, open the "My account" page and download each of your portfolios as CSV. On the new computer, install the software, create an account and add these files. Copying the accounts folder directly from one computer to another is not an operation the software supports.

## Uninstalling the software
<!-- fiche: demarrage-desinstaller | questions: how do I uninstall portfolio tracker ; remove the software from my pc ; remove the app from the mac ; does uninstalling delete my accounts ; also delete the accounts and portfolios ; keep my data when uninstalling ; uninstall cleanly ; erase all my data | mots: uninstall, remove, delete, erase, bin, accounts, permanent deletion -->

### On Windows

1. Open Windows Settings, then Apps, and choose "Portfolio Tracker", then Uninstall. You can also use the uninstall shortcut in the Start menu.
2. At the end, if accounts exist, a question is asked: "Also delete the saved accounts and portfolios?".
   - **No** (the default choice): the accounts and portfolios stay on the computer and will be found again if you reinstall Portfolio Tracker.
   - **Yes**: the software's folder is erased entirely, accounts included. This deletion is permanent.

### On Mac

1. Move "Portfolio Tracker" (in the Applications folder) to the Bin.
2. To also erase the accounts and portfolios, delete the folder `~/Library/Application Support/Portfolio Tracker` (Finder, Go menu, then "Go to Folder…").

If you delete only the application, your data stays on the Mac and will be found again after a reinstallation.

### Deleting a single account without uninstalling

Sign in, open the "My account" page and use the "Delete my account" section: the account and all its portfolios are erased permanently (right to erasure), without touching other users.

### Before erasing everything

Download a copy of your portfolios from the "My account" page if you think you might need them one day.

## The online version and its limits
<!-- fiche: demarrage-version-en-ligne | questions: is there an online version ; use the software without installing it ; streamlit cloud ; my accounts disappeared on the site ; demo version ; I'm on an intel mac what can I do ; can I use it on a tablet or chromebook ; difference between the site and the app | mots: online version, website, Streamlit Cloud, demo, browser, no installation, temporary accounts -->

The dashboard can also be published on Streamlit Community Cloud, a free hosting service. The address of this version is given to you by the software's creator or by your teacher.

### Who it is for

- users of Intel Macs, for whom the Mac application is not designed;
- those who want to try the software without installing anything;
- users of a computer on which they cannot install programs.

### Its limits

- **Accounts are temporary.** The online service's disk is wiped each time the site restarts: saved accounts and portfolios may disappear. A warning reminds you of this in the sign-in form: "Online demo version". Always keep a copy of your files.
- **Internet is essential**, since the software runs on a remote server.
- **Your files are processed on that server**, not on your computer. For real personal data, prefer the installed application.
- The site may be slower, especially if it was asleep and has to restart.

### What is identical

The screens, the calculations, the PDF report and the manual are the same as in the installed version.

## Launching the software from the source code
<!-- fiche: demarrage-code-source | questions: how do I launch with python ; what is lancer_tableau_de_bord.bat for ; streamlit run app.py ; I'm a student and want to run the project in vs code ; pip install requirements ; module not found streamlit ; install the libraries ; run on linux | mots: source code, Python, Streamlit, VS Code, pip, requirements.txt, terminal, developer, lancer_tableau_de_bord.bat -->

This method is aimed at students and developers who work on the project itself. It requires Python on the computer (the project specifies Python 3.11 or later).

### On Windows: the lancer_tableau_de_bord.bat file

Double-click `lancer_tableau_de_bord.bat`, at the root of the project.

- **The first time**, it installs the necessary libraries (the `requirements.txt` file), then the character recognition for image PDFs (the `requirements-ocr.txt` file). Internet is needed at that point. It then creates a small `.installe` file so as not to repeat this step.
- It then launches the same launcher as the installed version: the dashboard opens in its own window, at the address `http://localhost:8501` (or the next free port).
- To quit, close the black window.

### In a terminal (Windows, Mac, Linux)

From the project folder:

```
python -m pip install -r requirements.txt       (une seule fois)
python -m pip install -r requirements-ocr.txt   (facultatif : PDF image)
python -m streamlit run app.py                  (tableau de bord)
```

The dashboard opens in the browser, at the address `http://localhost:8501`. To stop it: Ctrl + C in the terminal.

### Other useful commands

- `python main.py`: command-line analysis and PDF report;
- `python construire_base_titres.py --mise-a-jour`: adds the latest prices to the local database;
- `python -m pytest`: runs the automated tests.

### In case of the error "No module named streamlit"

The libraries are not installed for the Python being used: run the installation command `python -m pip install -r requirements.txt` again.
