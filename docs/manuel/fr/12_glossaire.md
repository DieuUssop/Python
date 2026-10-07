# Glossaire
<!-- chapitre: glossaire | ordre: 12 -->

Ce glossaire définit, en une à trois phrases, les termes de finance, de statistique et d'informatique employés par le logiciel et par ce manuel. Les définitions sont celles retenues par Portfolio Tracker ; le chapitre « Toutes les formules » donne le calcul exact de chaque indicateur. Les termes sont regroupés par lettre.

## Glossaire : A
<!-- fiche: glossaire-a | questions: que veut dire alpha ; c'est quoi l'achat-conservation ; apports nets définition ; c'est quoi l'analyse en transparence ; asymétrie définition ; c'est quoi un avis d'opéré ; annualiser ça veut dire quoi ; assurance vie dans le logiciel | mots: achat-conservation, buy and hold, actualiser, alpha, analyse en transparence, annualisation, apports nets, assistant d'import, assurance-vie, asymétrie, avis d'opéré -->

**Achat-conservation** (*buy and hold*) : stratégie du backtest qui achète les titres une fois et n'y touche plus ; les poids dérivent avec les cours, les gagnants grossissent.

**Actualiser les cours** : bouton en bas de la barre latérale qui efface les résultats gardés en mémoire (une heure) et télécharge de nouveau les cours. Internet est nécessaire.

**Alpha de Jensen** : performance annuelle qui ne s'explique pas par l'exposition au marché, selon le MEDAF. Positif, le choix des titres a créé de la valeur par rapport à l'indice.

**Analyse en transparence** : méthode qui répartit chaque ETF selon la composition de l'indice qu'il suit (pays, secteurs, devises). Un ETF MSCI World de 10 000 € compte ainsi pour environ 7 300 € d'actions américaines.

**Annualisation** : conversion d'un chiffre sur une période en chiffre « par an ». Un rendement total se compose sur 365 jours ; une volatilité se multiplie par √252.

**Apports nets** : somme de tout l'argent apporté par les achats, moins l'argent récupéré par les ventes et les dividendes. C'est l'argent « de votre poche » encore investi.

**Assistant d'import** : écran en quatre étapes qui permet d'indiquer comment lire un fichier : feuille et ligne des titres, colonnes, types d'opération et tickers, puis résultat.

**Assurance-vie** : enveloppe fiscale comparée dans l'onglet Fiscalité : prélèvements sociaux de 17,2 %, impôt de 12,8 % avant 8 ans, puis de 7,5 % après un abattement annuel de 4 600 € (9 200 € pour un couple).

**Asymétrie** (*skewness*) : mesure de la dissymétrie des rendements quotidiens. Nulle pour une loi normale ; négative, les fortes baisses sont plus fréquentes ou plus violentes que les fortes hausses.

**Avis d'opéré** : document envoyé par la banque après l'exécution d'un ordre (date, sens, ISIN, quantité, cours, frais). Le logiciel sait le lire en PDF.

## Glossaire : B
<!-- fiche: glossaire-b | questions: que veut dire base 100 ; c'est quoi la base locale de titres ; c'est quoi un backtest ; bêta définition ; c'est quoi un benchmark ; bootstrap définition ; brinson fachler c'est quoi ; blocs corrélés ça veut dire quoi | mots: backtest, base 100, base locale, benchmark, bêta, blocs corrélés, bootstrap, Brinson-Fachler -->

**Backtest** : test d'une stratégie sur l'historique réel. L'onglet [[Backtest de stratégies]] compare, avec les mêmes titres et les mêmes poids de départ, l'achat-conservation et des rééquilibrages réguliers, puis l'investissement en une fois ou progressif.

**Base 100** : série qui part de 100 et suit la performance (100 × produit des 1 + r). Elle permet de comparer le portefeuille et l'indice sur un même graphique.

**Base locale de titres** : fichiers livrés avec le logiciel (dossier `data/base`) qui contiennent la fiche et les cours quotidiens de plusieurs milliers de titres, d'indices et de taux de change. Elle permet de travailler hors connexion.

**Benchmark** : voir « Indice de référence ».

**Bêta** : sensibilité du portefeuille aux mouvements de l'indice : covariance des rendements divisée par la variance de l'indice. Un bêta de 1,2 signifie qu'un mouvement de 1 % de l'indice s'accompagne en moyenne de 1,2 % pour le portefeuille.

**Blocs corrélés** : groupes de titres dont la corrélation moyenne dépasse 0,7. Chaque bloc ne compte que pour un seul « pari », quel que soit le nombre de lignes.

**Bootstrap** : méthode de simulation qui tire au hasard, avec remise, de vrais rendements passés. La projection « Historique (bootstrap) » construit chaque mois avec 21 vrais jours du portefeuille.

**Brinson-Fachler** : modèle d'attribution de performance (1985) qui découpe l'écart avec l'indice en effets d'allocation, de sélection et d'interaction, région par région.

## Glossaire : C
<!-- fiche: glossaire-c | questions: que veut dire cache ; c'est quoi la classe d'actifs ; clé de contrôle isin ; contribution au risque définition ; c'est quoi la corrélation ; cours de clôture définition ; c'est quoi un cto ; cvar ça veut dire quoi ; couverture de change eur hedged | mots: cache, Cariño, classe d'actifs, clé de contrôle, contribution au risque, corrélation, Cornish-Fisher, cours de clôture, covariance, CTO, CVaR, couverture de change -->

**Cache** : copie locale des derniers cours téléchargés (fichiers `cache_*.csv` du dossier `data`). Si Yahoo Finance ne répond pas, le logiciel la relit et affiche « Cours en cache (hors ligne) ».

**Cariño (lissage de)** : méthode qui relie des effets d'attribution mensuels pour que leur somme tombe exactement sur l'écart de performance composé de toute la période.

**Classe d'actifs** : grande famille d'un placement : Actions, Obligations, Or ou Monétaire. Un titre de classe inconnue est traité comme une action, par prudence.

**Clé de contrôle** : dernier chiffre d'un code ISIN, calculé à partir des autres. Le logiciel n'accepte un ISIN que si sa clé est juste.

**Compte-titres ordinaire (CTO)** : enveloppe sans avantage fiscal : dividendes et plus-values sont imposés au prélèvement forfaitaire unique de 31,4 % (règles 2026).

**Contribution au risque** : part de la volatilité du portefeuille apportée par une ligne (décomposition d'Euler). La somme des contributions est égale à la volatilité totale.

**Cornish-Fisher** : correction du quantile de la loi normale par l'asymétrie et la kurtosis, utilisée pour une VaR plus réaliste. Elle n'est pas calculée (« n.d. ») quand ces moments sont trop extrêmes.

**Corrélation** : mesure, entre −1 et +1, du lien entre les rendements quotidiens de deux titres. +1 : ils évoluent toujours ensemble ; 0 : aucun lien linéaire ; −1 : en sens inverse.

**Couverture de change** (*EUR Hedged*) : technique d'un ETF qui neutralise l'effet des devises. Un ETF dont le nom contient « Hedged » ou « couvert » est compté en euros dans l'exposition aux devises.

**Cours de clôture** : dernier cours d'une séance de bourse. Le logiciel utilise le cours de clôture non ajusté des dividendes.

**Covariance** : mesure de la façon dont deux titres varient ensemble ; elle combine leur corrélation et leurs volatilités. La matrice de covariance est la base de Markowitz et du budget de risque.

**CVaR** (*Expected Shortfall*) : perte moyenne des jours où la VaR historique est dépassée. Elle répond à « quand ça va mal, ça va mal comment ? ».

## Glossaire : D à E
<!-- fiche: glossaire-d-e | questions: que veut dire dca ; c'est quoi la devise de cotation ; dividende définition ; drawdown ça veut dire quoi ; c'est quoi la duration ; etf définition ; etf capitalisant ou distribuant ; écart-type définition ; effet allocation et effet sélection | mots: DCA, investissement progressif, devise de cotation, diversification, dividende, drawdown, duration, écart-type, effet allocation, effet sélection, effet interaction, ETF, capitalisant, distribuant, expositions -->

**DCA** (*Dollar Cost Averaging*), ou investissement progressif : placer un capital en plusieurs versements mensuels égaux plutôt qu'en une fois. Le backtest compare les deux, l'argent en attente étant rémunéré au taux sans risque.

**Devise de cotation** : monnaie dans laquelle un titre est coté (dollar pour Apple, pence pour une action de Londres). Le prix d'un achat se saisit dans cette devise ; le logiciel convertit en euros.

**Diversification** : répartition sur des placements qui n'évoluent pas tous ensemble, pour réduire le risque sans réduire autant le rendement. Le logiciel la mesure par les corrélations et le ratio de diversification.

**Dividende** : somme versée par une société (ou un ETF distribuant) à ses actionnaires. Il s'enregistre avec le type DIVIDENDE, une quantité de 0 et le montant total reçu dans le prix.

**Drawdown** : baisse par rapport au plus haut atteint jusque-là. Le **max drawdown** est la pire de ces baisses sur la période.

**Duration** : sensibilité d'une obligation aux taux d'intérêt, en années. Une duration de 7 ans signifie une baisse d'environ 7 % du prix si les taux montent de 1 point.

**Écart-type** : mesure de la dispersion des rendements autour de leur moyenne. Annualisé, il donne la volatilité.

**Effet allocation, effet sélection, effet interaction** : les trois parties de l'écart avec l'indice selon Brinson-Fachler : choix des régions, choix des titres dans chaque région, et effet croisé des deux.

**ETF** (*Exchange Traded Fund*), ou fonds indiciel coté : fonds qui reproduit un indice et s'achète en bourse comme une action. **Capitalisant** : il réinvestit les dividendes dans son cours ; **distribuant** : il les verse.

**Expositions** : ce à quoi le portefeuille est réellement exposé (pays, secteurs, devises, taux), ETF compris en transparence. C'est aussi le nom de l'onglet qui les présente avec un diagnostic.

## Glossaire : F à I
<!-- fiche: glossaire-f-i | questions: que veut dire flat tax ; c'est quoi un flux ; frontière efficiente définition ; fernet c'est quoi ; gain total définition ; gbp pence ça veut dire quoi ; herfindahl définition ; c'est quoi un isin ; indice de référence définition ; indice composite | mots: flat tax, PFU, flux, frais, Fernet, frontière efficiente, gain total, GBp, pence, Herfindahl, ISIN, indice de référence, indice composite, indice mixte -->

**Fernet** : méthode de chiffrement (bibliothèque Python `cryptography`) qui protège les portefeuilles enregistrés, avec une clé tirée de votre mot de passe.

**Flat tax** : voir « Prélèvement forfaitaire unique ».

**Flux** : argent apporté (achat, compté positivement) ou récupéré (vente, dividende, compté négativement) un jour donné. Les flux sont retirés du calcul de la performance quotidienne.

**Frais** : frais de courtage d'une opération, toujours en euros. Ils sont inclus dans le PRU à l'achat et déduits de la plus-value à la vente.

**Frontière efficiente** : ensemble des portefeuilles qui offrent, pour chaque niveau de rendement espéré, la volatilité la plus faible possible (Markowitz). Aucun portefeuille tiré au hasard ne la dépasse.

**Gain total** : ce que le portefeuille a rapporté en euros depuis le début : plus-values latentes + plus-values réalisées + dividendes, frais déduits.

**GBp** (pence) : unité de cotation des actions de Londres. 1 250 GBp valent 12,50 livres ; le logiciel applique un facteur de 0,01.

**Herfindahl (indice de)** : somme des carrés des poids. Son inverse donne le **nombre effectif de lignes** : 1 / Σ poids².

**Indice composite** (ou mixte) : indice calculé par le logiciel, mélange d'une poche actions et d'une poche obligations (20/80, 60/40 ou 80/20), remis à ses poids cibles à chaque fin de mois.

**Indice de référence** (*benchmark*) : indice auquel le portefeuille est comparé (bêta, alpha, tracking error, graphique base 100). Il se choisit dans [[Paramètres]] ; par défaut, le MSCI World représenté par l'ETF CW8.

**ISIN** : code international à 12 caractères qui identifie un titre (par exemple FR0013380607). Deux lettres de pays, neuf caractères et une clé de contrôle.

## Glossaire : J à M
<!-- fiche: glossaire-j-m | questions: que veut dire jarque bera ; kurtosis définition ; c'est quoi localhost ; loi normale définition ; log normale ça veut dire quoi ; markowitz c'est qui ; medaf définition ; monte carlo définition ; mémoire des titres ; c'est quoi le monétaire | mots: Jarque-Bera, kurtosis, queues épaisses, localhost, loi normale, log-normale, Markowitz, max drawdown, MEDAF, CAPM, mémoire des titres, moins-value, monétaire, Monte-Carlo -->

**Jarque-Bera (test de)** : test statistique qui vérifie si les rendements suivent une loi normale, à partir de l'asymétrie et de la kurtosis. Une p-value inférieure à 5 % fait rejeter la normalité.

**Kurtosis en excès** : mesure des « queues » de la distribution. Nulle pour une loi normale ; positive, les journées extrêmes, dans les deux sens, sont plus fréquentes que prévu (« queues épaisses »).

**Localhost** : adresse qui désigne votre propre ordinateur. Le tableau de bord tourne à l'adresse `http://localhost:8501` (ou un port suivant) ; personne d'autre sur le réseau ne peut s'y connecter.

**Loi log-normale** : loi d'une grandeur dont le logarithme suit une loi normale. La valeur finale d'une projection en suit une : sa moyenne dépasse sa médiane.

**Loi normale** : loi « en cloche » de Gauss, symétrique, décrite par sa moyenne et son écart-type. Elle sert à la VaR paramétrique et à la projection, mais sous-estime les krachs.

**Markowitz (optimisation de)** : méthode (1952) qui cherche les répartitions offrant le meilleur couple rendement-risque, grâce aux corrélations entre titres. Onglet Optimisation.

**Max drawdown** : pire baisse subie, du plus haut au plus bas suivant, mesurée sur la courbe base 100 de la performance.

**MEDAF** (modèle d'évaluation des actifs financiers, *CAPM*) : modèle qui relie le rendement d'un portefeuille à son bêta. Il sert à calculer l'alpha de Jensen.

**Mémoire des titres** : fichier `data/base/memoire.csv` qui retient les correspondances trouvées en ligne entre un ISIN ou un nom et un ticker, pour les reconnaître ensuite sans Internet.

**Moins-value** : perte réalisée (vente sous le PRU) ou latente (cours sous le PRU).

**Monétaire** : classe d'actifs des placements au jour le jour, proches du taux sans risque (ETF €STR, par exemple).

**Monte-Carlo (méthode de)** : simulation de milliers de futurs possibles tirés au hasard (5 000 dans le logiciel), pour étudier la distribution des résultats plutôt qu'une seule prévision.

## Glossaire : N à O
<!-- fiche: glossaire-n-o | questions: que veut dire n.d. ; nombre effectif de paris ; niveau de confiance de la var ; nombre effectif de lignes ; c'est quoi l'ocr ; obligation définition ; or dans le portefeuille ; optimisation définition | mots: n.d., niveau de confiance, nombre effectif de lignes, nombre effectif de paris, OCR, reconnaissance de caractères, obligation, or, optimisation -->

**n.d.** : « non disponible ». Le calcul n'a pas de sens ou n'a pas abouti (par exemple la VaR Cornish-Fisher avec une kurtosis trop forte, ou un TRI sans solution).

**Niveau de confiance** : probabilité retenue pour la VaR : 90, 95 (par défaut) ou 99 %. Une VaR à 95 % n'est dépassée qu'un jour sur vingt environ.

**Nombre effectif de lignes** : nombre de lignes de même poids qui donnerait la même concentration : 1 / Σ poids². Quatre lignes de 40, 30, 20 et 10 % en valent environ 3,3.

**Nombre effectif de paris** : même idée appliquée aux parts du risque : 1 / Σ (part du risque)². Il dit combien de lignes indépendantes le portefeuille représente vraiment.

**Obligation** : titre de dette qui verse des intérêts (coupons). Dans le logiciel, les obligations sont suivies au travers de fonds cotés, avec leur duration quand le référentiel la donne.

**OCR** (reconnaissance de caractères) : lecture du texte d'une image. Le logiciel l'utilise pour les PDF scannés, si un moteur (RapidOCR ou Tesseract) est installé.

**Optimisation** : recherche, par le calcul, des poids qui minimisent la volatilité ou maximisent le ratio de Sharpe, sous contraintes (poids positifs, somme de 100 %, poids maximal par titre).

**Or** : classe d'actifs à part, suivie au travers d'un fonds coté. Dans l'analyse en transparence, il est compté « sans pays » et à part des devises.

## Glossaire : P
<!-- fiche: glossaire-p | questions: que veut dire pru ; c'est quoi le pea ; parité des risques définition ; pbkdf2 c'est quoi ; percentile définition ; place de cotation ; plus-value latente définition ; plus value réalisée ; prélèvements sociaux taux ; p-value définition | mots: parité des risques, PBKDF2, PEA, percentile, place de cotation, plus-value latente, plus-value réalisée, poids, poids maximal, portefeuille tangent, prélèvement forfaitaire unique, PFU, prélèvements sociaux, PRU, proxy, p-value -->

**Parité des risques** (*risk parity*) : allocation dans laquelle chaque ligne apporte la même part du risque. Elle n'utilise que les volatilités et les corrélations, pas les rendements espérés.

**PBKDF2** : méthode qui transforme le mot de passe en empreinte et en clé de chiffrement, en la recalculant 600 000 fois pour ralentir les tentatives de piratage.

**PEA** (plan d'épargne en actions) : enveloppe réservée aux actions européennes et aux fonds éligibles. Après 5 ans, les gains ne supportent plus que les prélèvements sociaux (18,6 % en 2026).

**Percentile** : valeur sous laquelle se trouve un pourcentage donné des observations. Le 5ᵉ percentile des scénarios est le scénario défavorable de la projection.

**Place de cotation** : bourse où un titre est coté, indiquée dans le ticker Yahoo par un suffixe : `.PA` pour Paris, `.DE` pour Francfort, `.L` pour Londres, aucun pour les États-Unis.

**Plus-value latente** : gain non encaissé sur une ligne détenue : quantité × (cours − PRU).

**Plus-value réalisée** : gain encaissé lors d'une vente : quantité × (prix de vente − PRU) − frais.

**Poids** : part d'une ligne dans la valeur totale du portefeuille. Le **poids maximal par titre** limite cette part dans l'optimisation (30 % par défaut).

**Portefeuille tangent** : portefeuille de Sharpe maximal ; combiné au placement sans risque, il offre la meilleure droite rendement-risque.

**Prélèvement forfaitaire unique** (PFU, *flat tax*) : imposition des revenus du capital : 12,8 % d'impôt sur le revenu et 18,6 % de prélèvements sociaux, soit 31,4 % en 2026.

**Prélèvements sociaux** : part sociale de l'imposition des revenus du capital : 18,6 % en 2026 (CTO, PEA), 17,2 % pour l'assurance-vie.

**Proxy** : indice ou fonds utilisé à la place d'un titre sans historique, par exemple l'indice de sa région dans un stress test.

**PRU** (prix de revient unitaire) : coût moyen d'un titre détenu, frais d'achat compris. Il change à chaque achat et reste fixe lors d'une vente.

**p-value** : probabilité d'observer un résultat au moins aussi extrême si l'hypothèse testée (ici, la normalité) était vraie. Sous 5 %, l'hypothèse est rejetée.

## Glossaire : Q à R
<!-- fiche: glossaire-q-r | questions: que veut dire quantile ; ratio d'information définition ; ratio de diversification définition ; rééquilibrage c'est quoi ; rendement quotidien ; rotation du portefeuille ; risque de change définition ; référentiel ça veut dire quoi | mots: quantile, ratio d'information, ratio de diversification, rééquilibrage, référentiel, rendement quotidien, risque de change, rotation -->

**Quantile** : synonyme de percentile, exprimé en fraction. Le quantile 5 % des rendements quotidiens donne la VaR historique à 95 %.

**Ratio de diversification** : somme des volatilités des lignes, pondérées par leur poids, divisée par la volatilité du portefeuille. Il vaut 1 sans aucune diversification et augmente quand les lignes se compensent.

**Ratio d'information** : écart de rendement moyen annualisé avec l'indice, divisé par la tracking error. Il dit si l'écart avec l'indice a été payé ; au-delà de 0,5, il est considéré comme bon.

**Rééquilibrage** : retour périodique aux poids cibles, en vendant ce qui a monté et en achetant ce qui a baissé. Le backtest le teste chaque mois, trimestre ou année.

**Référentiel** : fichier `data/referentiel.csv` du projet qui décrit à la main des titres (pays, région, secteur, classe d'actifs, duration). Il l'emporte sur la base locale.

**Rendement quotidien** : variation d'un jour, après retrait des apports et des retraits : (valeur du jour − flux du jour) / valeur de la veille − 1.

**Risque de change** : effet des variations des devises sur la valeur en euros d'un titre étranger. Une action américaine peut monter en dollars et baisser en euros.

**Rotation** : part du portefeuille à déplacer pour passer d'une répartition à une autre (somme des écarts de poids divisée par 2), ou, dans le backtest, montants échangés par an.

## Glossaire : S
<!-- fiche: glossaire-s | questions: que veut dire sharpe ; sortino définition ; semi-déviation ; c'est quoi un stress test ; streamlit c'est quoi ; secteur gics ; surpondération définition ; scénario défavorable médian favorable | mots: ratio de Sharpe, ratio de Sortino, scénario, secteur, semi-déviation, sous-pondération, stress test, Streamlit, surpondération -->

**Ratio de Sharpe** : rendement excédentaire annuel (au-delà du taux sans risque) divisé par la volatilité. Il mesure si le risque pris a été bien payé : au-delà de 1, très bon.

**Ratio de Sortino** : variante du Sharpe qui remplace la volatilité par la semi-déviation, pour ne pénaliser que les baisses.

**Scénarios défavorable, médian et favorable** : 5ᵉ, 50ᵉ et 95ᵉ percentiles de la valeur simulée par la projection. Il y a une chance sur vingt de faire pire que le défavorable.

**Secteur** : domaine d'activité d'une société (technologie, santé, finance…), selon la classification GICS traduite.

**Semi-déviation** : mesure de dispersion qui ne retient que les jours où le rendement est sous le taux sans risque, annualisée par √252.

**Stress test** : estimation de ce que perdrait le portefeuille actuel si une crise passée se reproduisait (2008, Covid…) ou si un choc hypothétique survenait (baisse des actions, du dollar, hausse des taux).

**Streamlit** : bibliothèque Python qui affiche le tableau de bord dans une fenêtre de navigateur.

**Surpondération, sous-pondération** : poids d'un pays, d'un secteur ou d'une région plus élevé (ou plus faible) dans le portefeuille que dans l'indice de référence.

## Glossaire : T à U
<!-- fiche: glossaire-t-u | questions: que veut dire twr ; c'est quoi le tri ; taux sans risque définition ; ticker définition ; tracking error définition ; transaction ; ucits règle 5 10 40 ; c'est quoi le taux de change eurusd | mots: taux de change, taux sans risque, ticker, TRI, IRR, TWR, time-weighted return, tracking error, transaction, UCITS, 5/10/40 -->

**Taux de change** : prix d'une devise en euros. Le logiciel utilise les taux de Yahoo Finance, exprimés en nombre d'unités de devise pour 1 euro (`EURUSD=X` = dollars pour 1 €).

**Taux sans risque** : rendement d'un placement sans risque en euros, servant au Sharpe, au Sortino et à l'alpha. 2,50 % par défaut (taux de la facilité de dépôt de la BCE), constant sur la période, modifiable dans [[Paramètres]].

**Ticker** : code court d'un titre chez Yahoo Finance, avec sa place de cotation : `MC.PA` pour LVMH à Paris, `AAPL` pour Apple.

**Tracking error** : volatilité annualisée de l'écart de rendement quotidien entre le portefeuille et l'indice. Faible : le portefeuille colle à l'indice.

**Transaction** (ou opération) : achat, vente ou dividende enregistré dans le portefeuille, avec sa date, son titre, sa quantité, son prix et ses frais.

**TRI** (taux de rendement interne) : rendement annuel de l'argent effectivement investi, qui tient compte du montant et de la date de chaque apport. Il dépend du calendrier de vos versements.

**TWR** (*time-weighted return*) : rendement pondéré par le temps, produit des rendements quotidiens neutralisés des apports. Il mesure la qualité des choix, indépendamment des apports ; c'est la mesure des gérants de fonds.

**UCITS (règle 5/10/40)** : règle européenne des fonds : une ligne au plus 10 % du fonds, et les lignes de plus de 5 % au plus 40 % au total. Le logiciel s'en sert comme repère de concentration.

## Glossaire : V à Y
<!-- fiche: glossaire-v-y | questions: que veut dire var ; value at risk définition ; var historique ; var paramétrique ; variance minimale ; volatilité définition ; yahoo finance c'est quoi ; yfinance | mots: VaR, value at risk, VaR historique, VaR loi normale, variance, variance minimale, volatilité, Yahoo Finance, yfinance -->

**VaR** (*Value at Risk*) : perte d'un mauvais jour à un niveau de confiance donné. Une VaR à 95 % de 2 000 € signifie que la perte ne dépasse ce montant que 5 % des jours environ.

**VaR historique** : VaR lue directement dans les rendements passés (quantile), sans hypothèse de loi.

**VaR loi normale** (paramétrique) : VaR calculée en supposant que les rendements suivent une loi normale de même moyenne et de même volatilité. Elle sous-estime souvent les krachs.

**Variance** : carré de l'écart-type ; mesure de dispersion utilisée dans les calculs de Markowitz.

**Variance minimale (portefeuille de)** : répartition des titres actuels la moins volatile possible, sous les contraintes de l'optimisation.

**Volatilité** : écart-type annualisé des rendements quotidiens (× √252). C'est la mesure de risque la plus courante : 15 % signifie que le rendement d'une année s'écarte typiquement de 15 points de sa moyenne.

**Yahoo Finance** : service gratuit d'informations boursières d'où viennent les cours, les taux de change et la reconnaissance des titres inconnus.

**yfinance** : bibliothèque Python utilisée par le logiciel pour interroger Yahoo Finance.
