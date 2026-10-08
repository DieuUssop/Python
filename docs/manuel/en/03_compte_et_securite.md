# Your account and the security of your data
<!-- chapitre: compte | ordre: 3 -->

This chapter explains how to create your account, sign in, save and manage your portfolios in your encrypted personal space, and use the "My account" page. It then describes precisely how your data is protected, where it is stored, what leaves your computer and what nobody, not even the software's creator, can see.

## What is an account for, and is it mandatory?
<!-- fiche: compte-pourquoi | questions: do I have to create an account ; what is the account for ; can I use the software without an account ; why sign in ; what is the encrypted personal space ; my file disappeared when I relaunched the software ; how do I keep my portfolio from one use to the next ; difference between uploading a file and saving it | mots: account, personal space, encrypted space, registration, without account, keep, save, session -->

An account is **not mandatory** to analyse a portfolio. Without an account, you can choose a sample portfolio or upload your file in the sidebar: all the analyses work.

### What the account brings

The account gives you an **encrypted personal space**, where your portfolios are kept from one use to the next:

- your saved portfolios appear at the top of the sidebar's portfolio list, in the form "My space · " followed by their name;
- you can add new transactions to them, correct or delete a transaction, then go back;
- the [[My account]] page lets you rename them, download them or delete them;
- the display mode you chose (light or dark) is restored at each sign-in.

### Without an account

A file simply uploaded in the sidebar is **not kept**: when you close the software, you will have to upload it again. Transactions added or corrected without an account only apply to the current session; the software then offers to download the updated file. When a file is uploaded without being signed in, the sidebar in fact reminds you: "To keep this file, sign in".

### Why "encrypted"?

Everything you save in your space is encrypted with a key derived from your password. Other users of the same computer, and even the administrator, cannot read it (see the entry "How is my data protected?").

## Creating an account: username and password rules
<!-- fiche: compte-creer | questions: how do I create an account ; sign up in the software ; why is my username invalid ; which characters are allowed in the username ; how many characters for the password ; the password must contain at least 8 characters ; this username is already taken ; can I use capitals or accents in my username ; the two passwords do not match | mots: account creation, registration, username, login, user name, password, rules, minimum length, allowed characters -->

### The steps

1. At the top of the sidebar, next to the label [[Encrypted personal space]], click [[Sign in]]. A form opens (the button becomes [[Close]]).
2. Choose [[Create an account]].
3. Fill in [[Username]], [[Password]] and [[Confirm password]].
4. Click [[Create my account]].

You are signed in straight away, with an empty space.

### Username rules

- **3 to 30 characters**;
- only **unaccented lowercase letters** (a to z), **digits** and the three signs **full stop**, **underscore** and **hyphen**;
- no spaces, no accents, no other symbols.

Leading and trailing spaces are removed, and capitals are converted to lowercase: "Kevin.Brule" becomes "kevin.brule". You can then sign in by typing either one.

| Example | Accepted? |
|---|---|
| `etudiant.g2c` | Yes |
| `marie_2026` | Yes |
| `ab` | No: fewer than 3 characters |
| `jean dupont` | No: space |
| `kévin` | No: accent |

### Password rule

At least **8 characters**. No maximum, no required type of character: letters, digits, spaces, accents and symbols are accepted. The software does not demand complexity, but your password is the only protection for your data: choose one that is long and impossible to guess (a phrase of several words, for example).

### Possible messages

- "Invalid username": a username rule is not met.
- "The password must be at least 8 characters long."
- "The two passwords do not match."
- "This username is already taken.": an account already has this name on this computer.

### Before confirming

The form reminds you: if it is forgotten, the password cannot be recovered, and your portfolios would become permanently unreadable. Write it down somewhere safe.

## Signing in, signing out and automatic sign-out
<!-- fiche: compte-connexion | questions: how do I sign in ; where is the sign in button ; how do I sign out ; I was signed out by myself ; automatic sign-out after 30 minutes ; why do I have to sign in again every time ; I close the window do I stay signed in ; how long do you stay signed in ; incorrect username or password | mots: sign-in, login, sign-out, logout, inactivity, 30 minutes, session, sign in again -->

### Signing in

1. In the sidebar, click [[Sign in]].
2. Leave the choice on [[Sign in]], then enter your [[Username]] and your [[Password]].
3. Confirm with the form's [[Sign in]] button.

The check takes a short moment (the message "Checking..." is displayed): this delay is deliberate, it makes hacking attempts very slow. Once signed in, the sidebar shows a badge with your initials, your username, and two links: [[My account]] and [[Sign out]]. The light or dark mode you had chosen is restored.

If the username or the password is wrong, the message is always the same: "Incorrect username or password." The software deliberately does not say which of the two is wrong, so as not to reveal which accounts exist.

### Signing out

Click [[Sign out]]. The encryption key is erased from the session's memory and your portfolios disappear from the list.

### Automatic sign-out

After **30 minutes without any action** in the dashboard, you are signed out. The check takes place at your next action: the sidebar then displays "Automatically signed out after 30 minutes of inactivity." and you simply need to sign in again. Each click or change of setting resets the counter to zero.

### Closing the window or the software

The sign-in is only kept for the open page: it ends if you close the dashboard window, if you reload the page or if you stop the software. Nothing is lost: your saved portfolios are already written to disk, encrypted.

## Account locked after several failed attempts
<!-- fiche: compte-blocage | questions: too many failed attempts try again in ; my account is locked ; how many attempts before lockout ; how long is the account locked ; I got the password wrong several times ; even with the right password it refuses ; why do I have to wait a minute ; protection against password hacking | mots: lockout, locking, failed attempts, tries, brute force, wait, 60 seconds, security -->

### The rule

After **5 wrong passwords** for the same account, that account is **locked for 60 seconds**. During this time, every attempt is refused, even with the right password, with the message "Too many failed attempts: try again in" followed by the number of seconds remaining.

### The details

- The failure counter is specific to each account and saved on disk: closing and relaunching the software does not reset it.
- At the moment of lockout, the counter restarts from zero: after the minute's wait, you have 5 attempts again.
- A successful sign-in also resets the counter to zero.
- A username that does not exist is not locked, but it receives the same message and takes the same calculation time as a real account: it is impossible to guess which accounts exist this way.

### Why this lockout?

It prevents someone from very quickly trying a long list of passwords from the sign-in screen. Combined with the calculation time of each attempt, it makes this type of attack very slow.

### What should you do?

Wait for the indicated time to end, then check:

- the Caps Lock key (the password is case-sensitive, unlike the username);
- the keyboard layout (AZERTY or QWERTY);
- the exact username of the account.

If the password is truly lost, no unlocking is possible: see the entry "I have forgotten my password".

## Saving a portfolio to my space
<!-- fiche: compte-enregistrer | questions: how do I save my portfolio ; back up my file in my account ; where is the save to my space button ; my portfolio doesn't appear in the list ; add a portfolio to my account ; keep my file for next time ; I saved two portfolios with the same name ; the save button doesn't appear | mots: save, back up, add a portfolio, My space, encrypted, import, CSV file, Excel, PDF -->

You need to be signed in. Two routes are possible.

### From the sidebar

1. Upload your file (CSV, Excel or PDF) in the sidebar's upload area.
2. The software reads it and analyses the portfolio. If the file is not recognised on its own, the import wizard guides you first.
3. Once the analysis is displayed, a [[Save to my space]] box appears just under the upload area.
4. Check or edit the [[Portfolio name]] (the file name is suggested), then click [[Save]].

The box then confirms that the portfolio is saved in your space, encrypted.

### From the "My account" page

1. Click [[My account]], then, in the [[Add a portfolio]] section, choose your file.
2. The software reads it automatically and indicates the number of transactions recognised.
3. Check the name, then click [[Save]].

If the file cannot be read automatically, a message invites you to upload it from the sidebar, where the import wizard will help you.

### What is saved

The portfolio is saved **after reading and conversion**, in the project's format (date, type, ticker, name, quantity, price, fees), and not in the form of the original file. It is encrypted before being written to disk. It then appears in the portfolio list, in the form "My space · " followed by its name.

### Beware of identical names

Saving a portfolio under a name **already used** in your space (ignoring capitals) **replaces** the old portfolio of that name; the old version can be recovered with [[Undo last change]] in "My account". To keep both, give a different name.

## The "My account" page: renaming, downloading, deleting a portfolio
<!-- fiche: compte-page-mon-compte | questions: where is the my account page ; how do I rename a portfolio ; download my portfolio as csv ; delete a saved portfolio ; the delete button is greyed out ; get my file back from the software ; manage my portfolios ; I want to export my portfolio | mots: My account, management, rename, download, export, CSV, delete a portfolio, My portfolios -->

Once signed in, click [[My account]] in the sidebar. To return to the analyses, click any workspace in the menu (or [[My account]] again).

The page recalls that your portfolios are encrypted with a key derived from your password. It has four sections: [[Add a portfolio]], [[My portfolios]], [[Change password]] and [[Delete my account]].

### The "My portfolios" section

Each portfolio occupies one row, with its number of transactions and its date of last modification.

| Action | How to do it |
|---|---|
| Rename | Edit the name in the row's field, then confirm (Enter key). An empty name is ignored. |
| Download | [[Download]] button: you get a CSV file bearing the portfolio's name. |
| Delete | Tick [[Confirm]]: the [[Delete]] button, greyed out until then, becomes active. Click it. |
| Add transactions | [[Add transactions]] button (see the next entry). |
| Go back | [[Undo last change]] button, present only after an addition or a correction. |

### Good to know

- **The downloaded file is not encrypted**: it is a CSV readable by Excel, in the project's format. Store it somewhere safe.
- **Deletion is permanent**: the portfolio and its possible previous version are erased. No undo is possible. Download it first if you have any doubt.
- Renaming a portfolio does not change its content and does not create a previous version.

## Adding transactions and undoing the last change
<!-- fiche: compte-ajouter-annuler | questions: how do I add my new purchases to a saved portfolio ; what does undo last change do ; I made a mistake when adding transactions ; go back to the previous version ; the undo button doesn't appear ; can you undo several times ; update my portfolio with a contract note ; undo a correction | mots: add transactions, update, undo, previous version, rollback, restore, contract note -->

### Adding transactions

For a portfolio in your space, two entry points lead to the same page:

- on the [[My account]] page, the [[Add transactions]] button on the portfolio's row;
- in the sidebar, the [[Add transactions]] link, when that portfolio is selected.

Upload only the **new** movements (PDF contract note, CSV or Excel export) or enter them by hand. The software discards transactions that are already present, flags inconsistencies, then has you check them. Finally click [[Save transactions]]. The details of this page are explained in the chapter on importing.

### What happens when you save

The portfolio is saved again, encrypted, with the new transactions. **The previous version is kept**, also encrypted. The same applies when you correct or delete transactions with [[Edit transactions]] in the Transactions tab, then [[Save changes]].

### Undoing the last change

The [[Undo last change]] button then appears on the portfolio's row, in [[My account]], and in the Transactions tab. Its tooltip gives the date of the version you are about to return to. One click puts the portfolio back in exactly that state.

### The limits

- **Only one level of undo.** Only the very latest version is kept. After an undo, the button disappears; and each new addition or correction replaces the version previously kept.
- The button does not exist as long as no addition or correction has been saved.
- Saving a file under the same name from the sidebar or the [[Add a portfolio]] section replaces the portfolio, but keeps the previous version (recoverable with [[Undo last change]]).

## Changing your password
<!-- fiche: compte-changer-mot-de-passe | questions: how do I change my password ; edit my account password ; current password incorrect ; do I lose my portfolios if I change my password ; my password is too simple I want to change it ; someone knows my password what do I do ; password change and re-encryption | mots: password, change, edit, re-encryption, new password, security -->

### The steps

1. Sign in, then open [[My account]].
2. In the [[Change password]] section, enter the [[Current password]], the [[New password]] (at least 8 characters) and [[Confirm password]].
3. Click the [[Change password]] button.

The message "Password changed." confirms the operation. You stay signed in.

### What the software does

Since the encryption key is derived from the password, changing the password also changes the key. The software:

1. checks the old password;
2. decrypts in memory all your portfolios, their previous versions and your preferences;
3. draws two new random "salts" (see the technical entry on encryption);
4. calculates the new fingerprint and the new key;
5. **re-encrypts everything** with the new key.

The old password therefore no longer opens anything. Your portfolios, their names and the ability to undo the last change are kept.

### Possible messages

- "Current password is incorrect."
- "The password must be at least 8 characters long."
- "The two passwords do not match."

### When should you do it?

If you think someone knows your password, or if you chose one that is too short. Changing the password is only possible by knowing the old one: it is not a way of recovering a forgotten password.

## Deleting my account and all my data
<!-- fiche: compte-supprimer-compte | questions: how do I delete my account ; erase all my data ; right to erasure gdpr ; close my account permanently ; is deletion really permanent ; delete my account without uninstalling ; I want my data to be erased ; recover a deleted account | mots: account deletion, erasure, right to be forgotten, GDPR, article 17, permanent, unsubscribe -->

### The steps

1. Sign in and open [[My account]].
2. In the [[Delete my account]] section, enter your [[Password]].
3. Click [[Permanently delete my account]].

You are signed out and the message "Account and data deleted." is displayed.

### What is erased

- your account's folder: all your portfolios, their previous versions, the encrypted list of their names and your preferences;
- your row in the accounts register (username, salts, fingerprint).

The computer's other accounts are not touched. The username becomes free again.

### It is permanent

There is no bin and no grace period: a deleted account cannot be restored. Download your portfolios as CSV first if you might need them. Since the files were encrypted, any remnants on the disk would in any case be unreadable without your password.

### What is not erased

A few files shared by all users, which contain no portfolio data, stay in place: the memory of recognised securities, the price cache files and the log of questions put to the assistant (see the entry "Several users on the same computer").

### Deleting the whole software

To erase all accounts at once, see the entry on uninstalling in the "Getting started" chapter.

## How is my data protected?
<!-- fiche: compte-protection-simple | questions: is my data protected ; are my portfolios safe ; can someone read my files ; is the password stored ; what is encryption ; who can see my portfolios ; is my data encrypted ; can another pc user see my portfolio | mots: security, protection, encryption, confidentiality, password, fingerprint, key -->

Here is the principle, explained simply. The next entry gives the technical detail.

### 1. Your password is never saved

The software only saves a **fingerprint** (hash) of the password: the result of a one-way calculation. When you sign in, it redoes the calculation with what you type and compares the two results. Reading the fingerprint does not allow the password to be found.

### 2. Your portfolios are encrypted

When you sign in, the software makes an **encryption key** from your password. Everything you save is encrypted with this key before being written to disk: a file opened without it is only a string of incomprehensible characters.

### 3. The key is never written

The key exists only in the computer's memory, during your sign-in. It disappears when you sign out, when the page is closed and after 30 minutes of inactivity.

### 4. Even the names are hidden

The list of your portfolios (their names, their dates) and your display preferences are encrypted too. Account folders have randomly drawn names, unrelated to your username.

### 5. Modified files are detected

Each encrypted file carries a check code. If someone modifies it, even by a single character, it is rejected instead of being read wrongly.

### 6. Attempts are slowed down

Each password attempt requires a deliberately long calculation, and the account is locked for a minute after 5 failures.

### The consequence

Without your password, **nobody** can read your portfolios: neither the other users of the computer, nor the administrator, nor the software's creator. The trade-off is that a forgotten password makes the data permanently unreadable.

## Encryption in detail: PBKDF2, salt and Fernet
<!-- fiche: compte-protection-technique | questions: which encryption algorithm is used ; what is pbkdf2 ; how many iterations for the hash ; what is a salt in cryptography ; is fernet aes 128 safe ; where is the encryption key stored ; how is the password fingerprint calculated ; can a hacker crack my password | mots: PBKDF2, HMAC, SHA-256, salt, 600,000 iterations, Fernet, AES-128, HMAC-SHA256, hashing, key derivation, OWASP -->

### The password fingerprint

```
fingerprint = PBKDF2-HMAC-SHA256(password, fingerprint salt, 600,000 iterations)
```

- **PBKDF2-HMAC-SHA256**: a standard, one-way derivation function.
- **Salt**: 16 bytes drawn at random by the system's cryptographic generator, different for each account. Two people who choose the same password have different fingerprints, and precomputed fingerprint tables are unusable.
- **600,000 iterations**: the calculation is repeated 600,000 times (the value recommended by OWASP in 2023), which makes it slow: of the order of a few tenths of a second per attempt, depending on the computer.
- The comparison with the saved fingerprint is made in **constant time**, so as to reveal nothing through the duration of the calculation.

### The encryption key

```
key = PBKDF2-HMAC-SHA256(password, key salt, 600,000 iterations)
```

This is the same calculation, but with a **second, distinct salt**. The fingerprint saved on disk therefore cannot be used as a key. This 32-byte key is **never written**: it exists only in memory, during the sign-in.

### File encryption

Data is encrypted with **Fernet** (the Python `cryptography` library): **128-bit AES** encryption combined with an **HMAC-SHA256** authentication code. The authentication code detects any modification: a file that has been altered, or opened with the wrong key, is rejected.

### What is encrypted

| File | Content |
|---|---|
| `index.enc` | the list of your portfolios (internal identifier, name, dates, number of transactions) |
| one `.enc` file per portfolio | the portfolio's transactions |
| an optional `.prec.enc` file | the previous version, for the undo |
| `preferences.enc` | your display preferences (light or dark mode) |

Account folders and portfolio files have random 32-character names. Each write goes through a temporary file that is then renamed: a power cut never leaves a half-written file.

### Resistance to an attack

The 60-second lockout after 5 failures protects the sign-in screen. But someone who copied the files could test passwords without going through that screen: only the cost of the calculation slows them down. At half a second per attempt on one processor, a million attempts take about 6 days (1,000,000 × 0.5 s = 500,000 s); an attacker equipped with many processors goes faster. **The real protection is therefore a long, unpredictable password**: a phrase of several words resists far better than a dictionary word followed by a digit.

## I have forgotten my password
<!-- fiche: compte-mot-de-passe-oublie | questions: I forgot my password ; lost password how do I recover my portfolios ; reset the password ; can the administrator unlock my account ; there is no forgotten password link ; recover my account ; I can't remember my password what do I do ; can the creator find my data | mots: forgotten password, loss, recovery, reset, lost data, unrecoverable -->

### The frank answer

**There is no way to recover a forgotten password, nor the portfolios it protects.** There is no "forgotten password" link, no secret question, no backup email address. Neither the computer's administrator nor the software's creator can help you.

### Why?

- The password is not saved anywhere: only its fingerprint is, and it does not allow the password to be found.
- The key that decrypts your portfolios is calculated from the password and is never saved.
- Without the password, there is therefore no key, and without a key the files remain unreadable.

This is a deliberate choice: if there were a way to open the data without the password, anyone (another user, a hacker, the administrator) could use it too.

### What to do now

1. Try the likely variants (capitals, AZERTY or QWERTY keyboard, old password), keeping in mind the one-minute lockout after 5 failures.
2. If you downloaded your portfolios as CSV, or if you kept your original files (statements, contract notes), create a new account with a different username and save them again.
3. The old account remains unusable. To make it disappear, you have to be able to sign in to it; failing that, only uninstalling with deletion of accounts erases it, but that also erases the accounts of the other users of this computer.

### For the future

Write your password down in a password manager or somewhere safe, and regularly download a copy of your portfolios from [[My account]].

## Where is my account data stored?
<!-- fiche: compte-emplacement | questions: where are my accounts stored ; which folder are my encrypted portfolios in ; what is the comptes.json file ; where is data comptes on windows ; where is my data on mac ; I see unreadable enc files ; is my data in the cloud ; the folders have strange names | mots: location, folder, storage, data/comptes, comptes.json, AppData, Application Support, enc files -->

Your data stays on the computer where the software is installed. It is not sent to any server.

### Location by version

| Version | Accounts folder |
|---|---|
| Windows (installer) | `C:\Users\<your name>\AppData\Local\Programs\Portfolio Tracker\data\comptes` |
| Mac (application) | `~/Library/Application Support/Portfolio Tracker/app/data/comptes` |
| Source code | `data/comptes` in the project folder |

On Windows, the `AppData` folder is hidden: type the path into File Explorer's address bar. On Mac, in the Finder, use the Go menu, then "Go to Folder…".

### What this folder contains

- `comptes.json`: the accounts register. For each one: the username, in clear; the two salts; the password fingerprint; the number of iterations; the creation date; the failed-attempt counter and the end of any lockout; the name of the account's folder. **No password and no portfolio data.**
- one folder per account, with a random name, which contains the encrypted files `index.enc`, `preferences.enc` and one `.enc` file per portfolio (plus a `.prec.enc` for a previous version).

### What can be guessed without the password

Someone who opens this folder sees the list of usernames and the accounts' creation date, and can count the encrypted files in a folder. They see neither the name nor the content of the portfolios.

### Updates and uninstalling

Accounts are kept when a new version is installed, on Windows as on Mac. When uninstalling on Windows, a question asks whether to delete them too ("No" by default). On Mac, they stay as long as you do not delete the folder `~/Library/Application Support/Portfolio Tracker`.

### The folder is never published

In the source code, the `data/comptes/` folder is excluded from the GitHub repository and from the installers: your accounts are never published, even encrypted.

## What the software's creator can and cannot see
<!-- fiche: compte-createur | questions: does the software's creator see my data ; does the developer have access to my portfolio ; are there usage statistics ; does the software send data to the creator ; can my teacher see my portfolio ; is there a tracker ; telemetry ; who has access to my data | mots: creator, developer, administrator, telemetry, statistics, tracking, data access, privacy -->

### With the installed version: nothing

The software runs entirely on your computer, at the address `localhost`. It has **no server** to send your data to, and the software's creator receives nothing:

- no online account: your account exists only on your computer;
- no usage statistics: the collection of statistics by Streamlit (the library that displays the dashboard) is disabled, both in the project's configuration and at launch;
- the questions put to the assistant are not sent: they stay in a local file;
- no check for updates.

The only outgoing connections are used to obtain market data (see the entry "What leaves my computer").

### Even with access to your computer

Your saved portfolios are encrypted with a key derived from your password. The creator, like any administrator, could not read them without this password, and cannot reset it either.

### What is readable without a password

A few local files, shared by all the computer's users, are not encrypted: the list of account usernames, the price cache (codes of recently analysed securities and their prices), the memory of recognised securities, the learned trade confirmation models (`modeles_pdf.json`) and the log of unanswered questions. They contain no quantity or amount, but they reveal which securities have been analysed. The learned models only keep the headings of the values ("Quantité", "Cours"…) and the document's vocabulary as fingerprints (hashing): no amount, no name in clear.

### The case of a teacher

Your teacher only sees your portfolios if you pass them a file yourself (CSV export, PDF report) or if you show them your screen.

### Reporting a misread PDF

To help the creator improve the reading of a type of trade confirmation, you can send them yourself the report produced by [[Prepare an anonymised report]] ("Complete the transaction" form): names, address lines, e-mail addresses, IBANs, phone numbers and account numbers are masked in it. Nothing is sent without your action.

### The online version is different

On the online version, the software runs on a hosted server: the files you upload there are processed on that server, which is administered by the person who published the site. For real data, prefer the installed version.

## Several users on the same computer
<!-- fiche: compte-plusieurs-utilisateurs | questions: several of us use the same pc ; can my flatmate see my portfolios ; does each user have to create an account ; share the computer with my family ; shared school computer ; two different windows sessions ; can others see my questions to the assistant ; can another user delete my account | mots: multi-user, shared computer, several accounts, Windows session, flatshare, computer lab, isolation -->

### In the same Windows or Mac session

Each person creates **their own account** in the software. Then:

- each person sees, in the list, only **their** saved portfolios (plus the project's sample portfolios, shared by everyone);
- other people's portfolios are encrypted with their own password: they cannot be read;
- deleting an account, or changing its password, requires that account's password: nobody can do it in your place from the software;
- remember to click [[Sign out]] before giving up your seat, without waiting for the 30-minute automatic sign-out.

### What is shared by everyone

Some files serve everyone and are not encrypted. They contain no quantity or amount:

- the local securities database and the memory of recognised securities (matches between ISIN codes, names and tickers, with their date);
- the price cache files (codes and prices of the latest securities analysed);
- the learned trade confirmation models (`modeles_pdf.json`): headings of the values and fingerprints of the vocabulary, with no amount or name in clear;
- the assistant's log of unanswered questions: **all unanswered questions are visible to all users**, in the Manual and help workspace. Do not type any personal information there.

A user who opens the accounts folder also sees the list of existing usernames.

### With different Windows sessions

On Windows, installation is done for the current user, in their personal folder. If each person has their own Windows session, each installs the software in their session: accounts, database and caches are then completely separate.

### A computer administrator

They can copy or erase the files, like any file on the computer, but they cannot read your encrypted portfolios without your password. Keep a copy of your important portfolios.

## What leaves my computer when I use the software
<!-- fiche: compte-internet | questions: what is sent over the internet ; does yahoo see my portfolio ; are my quantities sent ; what data goes out on the network ; does the software send my isin codes ; is my file sent to a server ; privacy of requests ; does the software work without sending my data | mots: Internet, network, Yahoo Finance, requests, data sent, confidentiality, tickers, ISIN, GitHub, base map -->

The dashboard runs on your computer (`localhost`) and accepts no connection from another device. It contacts the Internet only for **market data**, and only when it needs to.

### What is sent, and to whom

| Recipient | What is sent | When |
|---|---|---|
| Yahoo Finance | the **codes** of the securities (tickers), of the benchmark index and of the exchange rates, with the **start date** of the history requested (the date of your first transaction) | at each analysis, when prices are not already in memory, and with [[Refresh prices]] |
| Yahoo Finance | a security's code, to find out its trading currency | the first time that security is encountered (the answer is then kept) |
| Yahoo Finance search engine | an **ISIN code**, a **company name** or a label read from your file, or a ticker without a trading venue | at import, for a security the software does not yet know |
| GitHub (or, failing that, the jsDelivr service) | a simple request to download the country outlines (Natural Earth) | only once, if the base map is not already on the computer |

If the base map could never be saved, it is the charting library, in the dashboard window, that downloads its own base map to draw the world map.

Like any connection to a site, these requests reveal the IP address of your connection to the service contacted.

### What is never sent

- your quantities, your purchase and sale prices, your amounts, your fees, your dividends;
- your files, in any form whatsoever;
- the names of your portfolios, your username, your password;
- your PDF reports;
- the questions put to the manual's assistant;
- no usage statistics.

The check of the prices in your file is done on your computer: the software downloads market prices, then compares locally.

### What Yahoo Finance can deduce from this

Yahoo sees which security codes are requested, and from what date. It sees neither how many you hold, nor at what price you bought them.

### To limit exchanges even further

Offline, the software uses its local database, its securities memory and its cache: it then sends nothing. Securities that are already known are recognised without any online search.

## GDPR and data protection
<!-- fiche: compte-rgpd | questions: does the software comply with gdpr ; data protection by design ; gdpr article 25 ; article 32 security of processing ; right to erasure article 17 ; does the software comply with the european regulation ; personal data and wealth management ; how do I exercise my right to be forgotten | mots: GDPR, general data protection regulation, article 25, article 32, article 17, privacy by design, right to erasure, CNIL -->

The software was designed taking into account three articles of the General Data Protection Regulation (GDPR). This entry describes the measures taken; it does not constitute legal advice.

### Article 25: data protection by design and by default

- Encryption is applied **by default** to everything saved in a personal space: no setting to turn on.
- No password is stored, only a fingerprint.
- No portfolio data is saved in clear in the personal space; even portfolio names are encrypted.
- Minimisation: only security codes are sent to Yahoo Finance, never quantities or amounts.
- The password of a protected PDF is stored nowhere: the decrypted copy of the document stays in memory for the session.
- The trade confirmation models learned on the computer contain no amount or name in clear (headings and fingerprints only).
- To report a misread PDF, an anonymised report masks names, addresses, IBANs, phone numbers and account numbers before you decide to send it.
- Data stays on the user's computer; it is not passed to any third party.

### Article 32: security of processing

- authenticated encryption (Fernet: 128-bit AES and HMAC-SHA256);
- salted and deliberately slowed fingerprints (PBKDF2-HMAC-SHA256, 600,000 iterations);
- limiting of attempts: 60-second lockout after 5 failures;
- same error message for an unknown username and a wrong password;
- key never written to disk, automatic sign-out after 30 minutes of inactivity;
- detection of any modification of an encrypted file.

### Article 17: right to erasure

The [[Delete my account]] section of the [[My account]] page permanently erases the account and all its portfolios, without anyone's intervention. A single portfolio can also be deleted.

### Note

With the installed version, you are alone in processing your own data, on your computer. On a shared server (online version, school server), the same protections apply to personal spaces, but the files uploaded are processed on that server.

## Accounts on the online version
<!-- fiche: compte-version-en-ligne | questions: my accounts disappeared on the online version ; online demo version ; why was my account erased on the site ; can you keep an account on streamlit cloud ; my portfolio saved online disappeared ; is it safe to put my data on the site ; the site restarted and I lost everything ; temporary accounts | mots: online version, Streamlit Community Cloud, temporary accounts, demo, restart, erasure, server -->

### Temporary accounts

On the online version (Streamlit Community Cloud), the server's disk is wiped each time the site restarts. Saved accounts and portfolios **can therefore disappear at any time**, without prior warning.

The sign-in form reminds you of this with a box that begins "Online demo version". This message only appears on the online version.

### What works

Account creation, sign-in, encryption and the [[My account]] page work exactly as in the installed version, as long as the site has not restarted.

### Precautions

- Always download your portfolios ([[Download]] button in [[My account]]) before leaving the site.
- Keep your original files.
- For lasting use, or for real personal data, use the application installed on your computer.

### The server processes your files

Online, the files you upload are read and analysed on the server. Portfolios saved in a space are encrypted there as elsewhere, but the caches and the assistant's log of unanswered questions are shared there by all the site's visitors.

## Backing up my portfolios or changing computer
<!-- fiche: compte-sauvegarde | questions: how do I back up my portfolios ; changing computer keeping my data ; export my portfolios ; copy my account to another pc ; backup of my data ; I'm going to reinstall windows how do I lose nothing ; transfer my account to mac ; where to keep a copy of my portfolios | mots: backup, export, CSV, transfer, new computer, migration, safety copy -->

### The recommended method: one CSV per portfolio

1. Sign in and open [[My account]].
2. For each portfolio, click [[Download]]: you get a CSV file in the project's format.
3. Store these files somewhere safe (USB stick, backed-up folder, external drive).

This file contains all the transactions. It is read back directly by the software, on any computer, on Windows as on Mac.

### Warning: the CSV is not encrypted

The downloaded file is readable by anyone. If your data is sensitive, store it in a protected location.

### On a new computer

1. Install Portfolio Tracker.
2. Create an account (the same username if you wish).
3. Save each of the CSV files in your space, through the [[Add a portfolio]] section of [[My account]] or through the sidebar's file upload.

### And what about copying the accounts folder?

Copying the `data/comptes` folder directly from one installation to another is not an operation the software supports. The CSV export is simpler and safer.

### What the backup does not contain

- the previous version kept for [[Undo last change]];
- your display preferences, to be chosen again;
- your password, which you must remember yourself.

### How often?

After each important update of a portfolio, and always before uninstalling the software, reinstalling the system or using the online version.

## The log of unanswered questions
<!-- fiche: compte-journal-questions | questions: are my questions to the assistant sent anywhere ; what are unanswered questions ; where are the questions I ask recorded ; delete the history of my questions ; does the assistant keep my questions ; export unanswered questions ; the questions_sans_reponse.csv file ; can others see my questions | mots: log, assistant, unanswered questions, history, questions_sans_reponse.csv, export, manual, confidentiality -->

### What is recorded

When the assistant in the Manual and help workspace does not find a reliable answer to a question typed in [[Ask a question]], it says so and records the question in a local file, with the date and time. Questions that found an answer are not recorded. Each question is truncated to 300 characters.

### Where is this file?

In the software's `data` folder, under the name `questions_sans_reponse.csv` (on Windows, `C:\Users\<your name>\AppData\Local\Programs\Portfolio Tracker\data\`; on Mac, `~/Library/Application Support/Portfolio Tracker/app/data/`). It is in clear, not encrypted, and shared by all the computer's accounts.

### It is never sent

The software passes this file to nobody. At the bottom of the Manual and help workspace, the "Unanswered questions" section shows the 30 most recent and offers the [[Export the questions (CSV)]] button. If you wish, send this file to the software's creator yourself: each question added to the manual improves the assistant.

### Visible to all users

This list is not tied to an account: anyone who uses the software on this computer sees it, even without being signed in. On the online version, it is shared by all the site's visitors. **Never type personal information** (amount, password, name) in a question.

### Erasing it

The software does not offer a button to empty this log. You can delete the `questions_sans_reponse.csv` file yourself: it will be recreated at the next unanswered question. It is kept when the software is updated, on Windows as on Mac.
