# Conseil patrimonial
<!-- chapitre: conseil | ordre: 7 -->

Ce chapitre décrit l'espace « Conseil patrimonial » et ses deux onglets. L'onglet **Fiscalité** compare ce qui resterait de votre gain après impôts sur un compte-titres, un PEA ou une assurance-vie, aux taux de 2026, aujourd'hui ou à un horizon futur, et mesure la part de votre portefeuille éligible au PEA. L'onglet **Stress tests** rejoue cinq crises passées et quatre à cinq chocs hypothétiques sur votre portefeuille actuel. Les règles fiscales sont volontairement simplifiées : chaque fiche précise ce qui est modélisé et ce qui ne l'est pas.

## Que contient l'espace Conseil patrimonial ?
<!-- fiche: conseil-presentation | questions: à quoi sert l'espace conseil patrimonial ; ou trouver la fiscalité ; ou sont les stress tests ; que puis je faire dans conseil patrimonial ; ou est passé le profil client ; conseil patrimonial c'est un vrai conseil ; quelle différence entre conseil patrimonial et gestion d'actifs | mots: conseil patrimonial, fiscalité, stress tests, enveloppes, PEA, assurance-vie, compte-titres, crises, scénarios | aller: Conseil patrimonial -->

L'espace **Conseil patrimonial** se choisit dans le menu « Espace de travail » de la barre latérale. Il analyse le même portefeuille, avec les mêmes paramètres, que l'espace « Analyse du portefeuille ». Il comprend deux onglets.

| Onglet | Question à laquelle il répond |
|---|---|
| [[Fiscalité]] | Combien reste-t-il après impôts, selon l'enveloppe (compte-titres, PEA, assurance-vie) et la date de sortie ? Quelle part du portefeuille peut aller dans un PEA ? |
| [[Stress tests]] | Que perdrait le portefeuille actuel si une crise passée se reproduisait, ou si un choc hypothétique survenait ? |

### Ce que l'espace ne fait pas

- Il ne contient ni questionnaire client, ni profil de risque réglementaire, ni test d'adéquation : ces fonctions ne font pas partie du logiciel. Le seul choix de profil (Prudent, Équilibré, Dynamique) se trouve dans l'onglet Expositions de l'espace « Analyse du portefeuille ».
- Il ne remplace pas un conseil fiscal personnalisé : le barème progressif de l'impôt, les plafonds et les frais des contrats ne sont pas modélisés (voir la fiche sur les simplifications).

Les principaux résultats de ces deux onglets figurent aussi dans le rapport PDF ; la fiscalité y est calculée pour un célibataire, réglage par défaut du logiciel.

Comme le rappelle le pied de page, l'outil est pédagogique et ne constitue pas un conseil en investissement.

## Quels taux d'imposition le logiciel utilise-t-il (2026) ?
<!-- fiche: conseil-taux-2026 | questions: quel taux de flat tax en 2026 ; pourquoi 31,4 % et pas 30 % ; les prélèvements sociaux ont augmenté ; taux d'imposition utilisés par le logiciel ; pfu 2026 ; pourquoi l'assurance vie est à 17,2 % ; quels sont les taux de la fiscalité dans le logiciel ; la csg a augmenté en 2026 | mots: flat tax, PFU, prélèvement forfaitaire unique, prélèvements sociaux, CSG, taux 2026, hausse de la CSG, impôt sur le revenu, loi de financement de la sécurité sociale 2026 | aller: Conseil patrimonial/Fiscalité -->

Le logiciel applique les règles d'un **particulier résident fiscal en France, en 2026**. La source citée dans le code est la loi n° 2025-1403 du 30 décembre 2025 de financement de la sécurité sociale pour 2026, qui a relevé la CSG sur les revenus du capital.

| Taux | Valeur | Utilisation |
|---|---|---|
| Impôt sur le revenu (PFU) | 12,8 % | CTO ; PEA avant 5 ans ; assurance-vie avant 8 ans |
| Prélèvements sociaux, revenus du capital | **18,6 %** | CTO et PEA |
| Prélèvements sociaux, assurance-vie | **17,2 %** | assurance-vie (non concernée par la hausse) |
| Flat tax totale (12,8 + 18,6) | **31,4 %** | CTO ; PEA avant 5 ans |
| Impôt sur le revenu, assurance-vie après 8 ans | 7,5 % | au-delà de l'abattement |
| Abattement annuel, assurance-vie après 8 ans | 4 600 € (célibataire), 9 200 € (couple) | sur la part du gain imposable à l'impôt sur le revenu |

### Le point d'actualité

Avant 2026, la flat tax valait 30 % (12,8 % + 17,2 %). La hausse de la CSG porte les prélèvements sociaux à 18,6 % et la flat tax à **31,4 %**. L'assurance-vie reste à 17,2 % de prélèvements sociaux : avant 8 ans, elle est donc taxée à 30 % au total, soit un peu moins que le compte-titres.

Le sous-titre du cadre « Hypothèses » de l'onglet rappelle « taux 2026 », et une note en bas de l'encadré « Éligibilité au PEA » récapitule ces taux.

### Ce qui n'est pas modélisé

L'option pour le barème progressif de l'impôt sur le revenu, le taux de 12,8 % de l'assurance-vie au-delà de 150 000 € de primes, et la déductibilité partielle de la CSG ne sont pas pris en compte.

## Comment est calculé l'impôt sur un compte-titres (CTO) ?
<!-- fiche: conseil-cto | questions: combien d'impôt si je vends tout sur mon compte titres ; fiscalité du cto ; pourquoi je paie de l'impôt alors que je suis en perte ; les moins values effacent elles les dividendes ; flat tax sur les plus values ; impôt sur les dividendes dans le logiciel ; compte titres ordinaire imposition | mots: CTO, compte-titres ordinaire, flat tax, plus-values, moins-values, dividendes, imputation, PFU, impôt sur les plus-values | aller: Conseil patrimonial/Fiscalité | chiffres: gain_total, dividendes -->

Sur un compte-titres ordinaire, le logiciel applique la flat tax de **31,4 %** à la base imposable, sans avantage lié à la durée de détention.

### La formule exacte

```
plus-values      = gain total − dividendes
base imposable   = max(0 ; plus-values) + max(0 ; dividendes)
impôt sur le revenu       = 12,8 % × base
prélèvements sociaux      = 18,6 % × base
```

Le **gain total** est celui de l'onglet Vue d'ensemble : plus-values latentes + plus-values réalisées + dividendes nets.

### L'intuition : une moins-value n'efface pas les dividendes

Les moins-values s'imputent sur les plus-values, **pas sur les dividendes**. Un portefeuille globalement en perte peut donc devoir de l'impôt sur ses dividendes.

### Exemples

**Gain de 20 000 €, dont 2 000 € de dividendes** : base = 18 000 + 2 000 = 20 000 € ; impôt = 2 560 € + 3 720 € = **6 280 €** ; gain net = **13 720 €** (taux effectif 31,4 %).

**Perte de 5 000 €, mais 2 000 € de dividendes** : plus-values = −7 000 € ; base = 0 + 2 000 = 2 000 € ; impôt = 256 € + 372 € = **628 €**, alors que le gain total est négatif.

### Interprétation

Dans la carte « Sortie CTO », la mention « Pas d'avantage lié à la durée » rappelle que le taux ne baisse jamais avec le temps. C'est la référence à laquelle comparer le PEA et l'assurance-vie.

### Limites

Le calcul suppose que tout le gain est imposé en une fois, à la sortie. En réalité, sur un CTO, les dividendes et les plus-values réalisées sont imposés l'année où ils sont perçus. L'option pour le barème progressif, parfois plus avantageuse pour les faibles revenus, n'est pas modélisée.

## Comment est calculé l'impôt sur un PEA ?
<!-- fiche: conseil-pea | questions: fiscalité du pea après 5 ans ; combien d'impôt si je retire de mon pea ; pea avant 5 ans que se passe t il ; pourquoi le pea est taxé à 18,6 % ; quand le pea devient il intéressant ; avantage fiscal du pea ; mon pea a 3 ans combien je paierai | mots: PEA, plan d'épargne en actions, 5 ans, exonération, prélèvements sociaux, clôture, avantage fiscal, plafond PEA | aller: Conseil patrimonial/Fiscalité | chiffres: gain_total -->

Le **plan d'épargne en actions (PEA)** offre une exonération d'impôt sur le revenu après 5 ans. Le logiciel calcule l'impôt comme si votre portefeuille avait été logé dans un PEA depuis votre première opération.

### La formule exacte

```
base = max(0 ; gain total)
avant 5 ans : impôt sur le revenu = 12,8 % × base     (retrait = clôture du plan)
après 5 ans : impôt sur le revenu = 0
prélèvements sociaux = 18,6 % × base                   (dans tous les cas)
```

L'ancienneté est mesurée de la date de votre **première opération** à la dernière date de l'historique, divisée par 365,25 jours.

### Exemple

Gain de 20 000 € :

- ancienneté de 3 ans : 2 560 € + 3 720 € = 6 280 € d'impôts, gain net **13 720 €** (31,4 %, comme le CTO). La carte indique « Avantage fiscal dans 2,0 an(s) » ;
- ancienneté de 9 ans : 0 € + 3 720 € = 3 720 €, gain net **16 280 €** (18,6 %). La carte indique « Avantage fiscal acquis ».

Différence après 5 ans : **2 560 €** de plus dans la poche, soit les 12,8 % d'impôt sur le revenu.

### Interprétation

Contrairement au CTO, une perte ne crée jamais d'impôt : la base est le gain total, ramené à zéro s'il est négatif, sans distinguer dividendes et plus-values.

### Limites

- Le plafond de versements de 150 000 € n'est pas appliqué au calcul ; une note le signale si votre montant investi le dépasse.
- Seules certaines valeurs sont éligibles : voir la fiche « Quelle part de mon portefeuille peut aller dans un PEA ? ».
- Le calcul applique le PEA à **tout** le portefeuille, même aux lignes non éligibles : c'est une comparaison théorique.

## Comment est calculé l'impôt sur une assurance-vie ?
<!-- fiche: conseil-assurance-vie | questions: fiscalité de l'assurance vie après 8 ans ; abattement de 4600 euros ; assurance vie couple 9200 ; combien d'impôt sur un rachat d'assurance vie ; pourquoi l'assurance vie est taxée à 30 % avant 8 ans ; comment choisir célibataire ou couple ; assurance vie 7,5 % | mots: assurance-vie, unités de compte, 8 ans, abattement, 4 600 €, 9 200 €, rachat, couple, célibataire | aller: Conseil patrimonial/Fiscalité | chiffres: gain_total -->

Le logiciel traite le portefeuille comme s'il était logé en **unités de compte** d'un contrat d'assurance-vie ouvert à la date de votre première opération.

### La formule exacte

```
base = max(0 ; gain total)
prélèvements sociaux = 17,2 % × base
avant 8 ans : impôt sur le revenu = 12,8 % × base
après 8 ans : impôt sur le revenu = 7,5 % × max(0 ; base − abattement)
abattement = 4 600 € (célibataire) ou 9 200 € (couple)
```

La situation familiale se choisit avec le bouton [[Situation familiale (abattement assurance-vie)]], en haut de l'onglet [[Fiscalité]]. Le réglage de départ est « Célibataire ».

### Exemples

Gain de 20 000 € :

| Situation | Impôt sur le revenu | Prélèvements sociaux | Gain net | Taux effectif |
|---|---|---|---|---|
| 3 ans d'ancienneté | 2 560 € | 3 440 € | 14 000 € | 30,0 % |
| 9 ans, célibataire | 7,5 % × 15 400 = 1 155 € | 3 440 € | 15 405 € | 23,0 % |
| 9 ans, couple | 7,5 % × 10 800 = 810 € | 3 440 € | 15 750 € | 21,3 % |

### Interprétation

- Avant 8 ans, l'assurance-vie (30 %) est légèrement plus favorable que le CTO et le PEA de moins de 5 ans (31,4 %), parce que ses prélèvements sociaux restent à 17,2 %.
- Après 8 ans, l'abattement rend l'assurance-vie très intéressante pour des gains modestes : un gain inférieur à 4 600 € (9 200 € pour un couple) ne supporte que les prélèvements sociaux.
- Comparée à un PEA de plus de 5 ans (18,6 %), l'assurance-vie de plus de 8 ans (17,2 % + 7,5 % au-delà de l'abattement) n'est moins taxée que pour les petits gains : jusqu'à environ 5 656 € pour un célibataire (0,172 G + 0,075 (G − 4 600) = 0,186 G) et 11 311 € pour un couple. Au-delà, le PEA l'emporte.

### Limites

- L'abattement est annuel en réalité ; ici, la sortie totale est faite en une seule fois, donc un seul abattement.
- Les primes sont supposées inférieures à 150 000 € (au-delà, le taux est de 12,8 % et non 7,5 %) ; une note le signale si votre montant investi dépasse ce seuil.
- Les frais de gestion du contrat ne sont pas déduits.
- En réalité, l'impôt d'un rachat partiel ne porte que sur la part de gains contenue dans le rachat ; le logiciel simule une sortie totale.

## Lire « Si tout était vendu aujourd'hui » : cartes et tableau des enveloppes
<!-- fiche: conseil-sortie-aujourdhui | questions: combien me resterait il si je vendais tout aujourd'hui ; comparer cto pea assurance vie pour mon portefeuille ; que veut dire taux effectif ; c'est quoi performance nette ; avantage fiscal dans 2 ans ça veut dire quoi ; le tableau de la fiscalité ; gain net après impôts | mots: gain net, gain brut, taux effectif, performance nette, comparaison des enveloppes, sortie, impôts, rachat total | aller: Conseil patrimonial/Fiscalité | chiffres: gain_total, montant_investi, dividendes -->

Dans l'onglet [[Fiscalité]], la section « Si tout était vendu aujourd'hui » suppose que vous vendez **tout le portefeuille** aujourd'hui, et compare le résultat dans les trois enveloppes. Son sous-titre rappelle le **gain brut** (gain total de l'onglet Vue d'ensemble).

### Les trois cartes

Une carte par enveloppe : « Sortie CTO », « Sortie PEA », « Sortie Assurance-vie ». Chacune affiche :

- le **gain net** d'impôts, en euros ;
- une pastille « impôts x % » : le **taux effectif** ;
- l'état de l'avantage fiscal : « Pas d'avantage lié à la durée » (CTO), « Avantage fiscal dans n an(s) » ou « Avantage fiscal acquis ».

### Les formules

```
gain net            = gain brut − impôt sur le revenu − prélèvements sociaux
taux effectif       = impôts totaux / gain brut          (0 si le gain est négatif)
performance brute   = gain brut / montant investi
performance nette   = gain net / montant investi
années avant avantage = max(0 ; durée de l'enveloppe − ancienneté)   (5 ans PEA, 8 ans assurance-vie)
```

### Exemple

Montant investi 100 000 €, gain 20 000 € dont 2 000 € de dividendes, ancienneté 3 ans, célibataire :

| Enveloppe | Impôt sur le revenu | Prélèvements sociaux | Gain net | Performance nette |
|---|---|---|---|---|
| CTO | 2 560 € | 3 720 € | 13 720 € | 13,7 % |
| PEA | 2 560 € | 3 720 € | 13 720 € | 13,7 % |
| Assurance-vie | 2 560 € | 3 440 € | 14 000 € | 14,0 % |

Performance brute : 20 % pour les trois. Le PEA affiche « Avantage fiscal dans 2,0 an(s) », l'assurance-vie « dans 5,0 an(s) ».

### Le tableau

Sous les cartes, un tableau reprend pour chaque enveloppe : Gain brut, Impôt sur le revenu, Prélèvements sociaux, Gain net, Performance brute et Performance nette.

### Interprétation

Ce n'est pas votre impôt réel : c'est ce que **vous auriez payé** si ce même portefeuille avait été logé dans chacune des enveloppes depuis votre première opération. L'outil sert à comparer les enveloppes, pas à préparer une déclaration.

## Le graphique « Gain net selon l'année de sortie »
<!-- fiche: conseil-annee-sortie | questions: quand vaut il mieux sortir de mon pea ; que montrent les sauts dans le graphique de la fiscalité ; à partir de quand le pea est plus intéressant que le cto ; pourquoi ouvrir un pea tôt ; gain net si je vends dans 10 ans ; quel rendement est utilisé pour les sorties futures ; prendre date assurance vie | mots: année de sortie, horizon, prendre date, saut fiscal, 5 ans, 8 ans, gain net futur, rendement supposé, capitalisation | aller: Conseil patrimonial/Fiscalité | chiffres: valeur_actuelle, gain_total -->

À gauche, sous les cartes de l'onglet [[Fiscalité]], le graphique « Gain net selon l'année de sortie » montre, pour chaque enveloppe, le gain net d'impôts si vous vendiez tout dans 0 à 20 ans.

### Le réglage

Le curseur [[Rendement annuel supposé pour les sorties futures (%)]] (0 à 10 %, pas de 0,5, départ 5 %) fixe la croissance supposée du portefeuille.

### La formule

```
gain dans n années = gain actuel + valeur actuelle × ((1 + rendement)ⁿ − 1)
ancienneté dans n années = ancienneté actuelle + n
gain net = gain − impôt de l'enveloppe (calculé avec cette ancienneté)
```

Les dividendes restent fixés à leur montant actuel (ce qui ne compte que pour le CTO).

### Les sauts

Les courbes du PEA et de l'assurance-vie sont **en escalier** : elles sautent vers le haut quand l'ancienneté franchit **5 ans** (PEA) ou **8 ans** (assurance-vie). La courbe du CTO, sans avantage lié à la durée, est continue.

### Exemple

Valeur actuelle 120 000 €, gain actuel 20 000 € (dont 2 000 € de dividendes), ancienneté 3 ans, rendement supposé 5 %, célibataire :

| Sortie dans | Gain brut | CTO | PEA | Assurance-vie |
|---|---|---|---|---|
| 0 an | 20 000 € | 13 720 € | 13 720 € | 14 000 € |
| 1 an | 26 000 € | 17 836 € | 17 836 € | 18 200 € |
| 2 ans (PEA à 5 ans) | 32 300 € | 22 158 € | **26 292 €** | 22 610 € |
| 5 ans (assurance-vie à 8 ans) | 53 154 € | 36 464 € | 43 267 € | **40 370 €** |

### Interprétation

Le graphique montre pourquoi un conseiller recommande d'ouvrir ces enveloppes **tôt**, pour « prendre date » : c'est la date d'ouverture qui fait courir les délais, pas la date des versements. Survolez une courbe pour lire le gain net de chaque enveloppe pour une année de sortie.

### Limites

Croissance régulière et certaine, sans frais de contrat ; mêmes simplifications que pour la sortie immédiate.

## Quelle part de mon portefeuille peut aller dans un PEA ?
<!-- fiche: conseil-eligibilite-pea | questions: mes titres sont ils éligibles au pea ; pourquoi apple n'est pas éligible au pea ; part éligible au pea ; un etf monde peut il aller dans un pea ; pourquoi mon etf obligataire n'est pas éligible ; les actions anglaises sont elles éligibles au pea ; lignes non éligibles au pea | mots: éligibilité PEA, éligible, UE, EEE, actions européennes, ETF éligibles, CW8, ESE, réplication synthétique, non éligible | aller: Conseil patrimonial/Fiscalité | chiffres: valeur_actuelle, montant_investi -->

L'encadré « Éligibilité au PEA », à droite du graphique de l'onglet [[Fiscalité]], affiche la carte « Part éligible au PEA » et le nombre de lignes non éligibles.

### La règle du logiciel

Une ligne est jugée éligible si :

- c'est une **action** (classe d'actifs « Actions ») d'une société dont le pays est dans l'**Union européenne ou l'EEE** (Norvège, Islande et Liechtenstein compris) ; ou
- c'est l'un des **fonds indiciels reconnus comme éligibles** : CW8.PA (Amundi MSCI World) et ESE.PA (BNP Paribas Easy S&P 500), éligibles grâce à leur réplication synthétique.

```
part éligible = valeur des lignes éligibles / valeur totale du portefeuille
```

### Ce qui n'est pas éligible

- les actions américaines, britanniques (depuis le Brexit), suisses ou japonaises ;
- les fonds obligataires et l'or (le PEA est réservé aux actions) ;
- les ETF non répertoriés dans la liste ci-dessus, même s'ils le sont en réalité ;
- les titres dont le pays n'est pas renseigné dans le référentiel.

### Exemple

Portefeuille de 100 000 € : 40 000 € d'actions françaises et allemandes, 30 000 € de CW8.PA, 20 000 € d'actions américaines, 10 000 € d'ETF obligataire. Part éligible = (40 000 + 30 000) / 100 000 = **70 %** ; 2 lignes non éligibles.

### Les remarques affichées

- si la part est inférieure à 100 % : seule la part éligible peut aller dans un PEA ; le reste irait sur un compte-titres ou en unités de compte d'assurance-vie ;
- si le montant investi dépasse 150 000 € : rappel du plafond de versements du PEA et du seuil de l'assurance-vie ;
- dans tous les cas, le rappel des taux 2026.

### Limites

La liste des fonds éligibles est courte : vérifiez l'éligibilité réelle de vos ETF dans leur documentation. La fiche de comparaison des enveloppes applique le PEA à tout le portefeuille, même aux lignes non éligibles.

## Les simplifications du calcul fiscal
<!-- fiche: conseil-simplifications-fiscales | questions: le calcul fiscal est il exact ; puis je utiliser l'onglet fiscalité pour ma déclaration ; le barème progressif est il pris en compte ; les frais de l'assurance vie sont ils déduits ; plafond 150000 pea pris en compte ; pourquoi mon impôt réel est différent ; limites de la fiscalité | mots: simplifications, limites, barème progressif, plafond, frais de gestion, déclaration fiscale, approximation, hypothèses | aller: Conseil patrimonial/Fiscalité -->

L'onglet [[Fiscalité]] est un outil de **comparaison pédagogique**. Il n'est pas conçu pour calculer votre impôt réel ni pour remplir une déclaration.

### Ce qui est simplifié

| Simplification | Conséquence |
|---|---|
| Option pour le barème progressif ignorée | pour un foyer faiblement imposé, l'impôt réel peut être plus bas |
| Primes d'assurance-vie supposées inférieures à 150 000 € | au-delà, le taux réel après 8 ans est 12,8 % et non 7,5 % (une note le signale) |
| Plafond de versements du PEA (150 000 €) non appliqué | une note le signale si le montant investi le dépasse |
| Frais de gestion des contrats ignorés | le gain net de l'assurance-vie est surestimé |
| Dividendes supposés conservés dans l'enveloppe | le gain total (latent + réalisé + dividendes) est imposé en une seule fois à la sortie |
| Sortie totale en une fois | un seul abattement d'assurance-vie, pas de rachats partiels étalés |
| Même portefeuille dans les trois enveloppes | le PEA est appliqué même aux lignes non éligibles |
| Ancienneté = depuis la première opération | une enveloppe ouverte plus tôt aurait déjà pris date |

### Ce qui n'est pas traité du tout

Les successions, les donations, l'impôt sur la fortune immobilière, les plans d'épargne retraite et les situations de non-résident ne sont pas couverts.

### Pourquoi garder un modèle simple ?

Un modèle simple rend visible l'essentiel : la différence de taux entre enveloppes et l'effet des délais de 5 et 8 ans. Pour une décision réelle, faites valider le calcul par un professionnel.

## Les stress tests historiques : que perdrait mon portefeuille lors d'une crise ?
<!-- fiche: conseil-stress-historiques | questions: que perdrait mon portefeuille en cas de krach ; c'est quoi les stress tests ; combien j'aurais perdu en 2008 ; quelles crises sont rejouées ; dates des crises dans les stress tests ; le pire scénario historique ; rejouer le covid sur mon portefeuille ; pourquoi le stress test prend du temps | mots: stress test, crise, krach, 2008, Covid, dette européenne, 2022, août 2024, scénario historique, perte maximale | aller: Conseil patrimonial/Stress tests | chiffres: valeur_actuelle, max_drawdown -->

L'onglet [[Stress tests]] applique à **chaque ligne de votre portefeuille actuel** la variation qu'elle a réellement subie pendant une crise passée, du plus haut au plus bas du marché.

### Les cinq crises rejouées

| Crise | Du (plus haut) | Au (plus bas) |
|---|---|---|
| Crise financière (2008-2009) | 01/09/2008 | 09/03/2009 |
| Crise de la dette européenne (2011) | 01/07/2011 | 22/09/2011 |
| Krach du Covid (2020) | 19/02/2020 | 23/03/2020 |
| Inflation et hausse des taux (2022) | 03/01/2022 | 12/10/2022 |
| Mini-krach d'août 2024 | 16/07/2024 | 05/08/2024 |

### La formule

```
variation d'une ligne = cours à la date de fin / cours à la date de début − 1
variation du portefeuille = Σ poids actuel de la ligne × variation de la ligne
perte en euros = variation du portefeuille × valeur actuelle
```

Le cours retenu à chaque date est le dernier cours connu à cette date.

### Exemple

50 % d'une ligne qui a perdu 45 %, 30 % d'une ligne qui a perdu 40 % et 20 % d'un fonds obligataire qui a gagné 5 % : variation = −22,5 % − 12 % + 1 % = **−33,5 %**, soit −33 500 € sur 100 000 €.

### Ce qui est affiché

- trois cartes : « Pire scénario historique », « Perte correspondante » (en euros, sur la valeur actuelle) et « Bêta du portefeuille » ;
- un graphique en barres « Crises passées rejouées sur le portefeuille actuel » (vert si gain, rouge si perte) ;
- le tableau « Détail des scénarios historiques » : Scénario, Période, Variation, Gain / perte, Part estimée par un indice ;
- la liste [[Voir le détail ligne par ligne]], qui affiche pour la crise choisie la variation de chaque titre et sa source (le titre lui-même ou un indice).

### Premier affichage

Il faut télécharger les cours depuis 2008 : le message « Rejeu des crises passées (historique depuis 2008)... » s'affiche le temps du calcul. Les cours sont ensuite gardés dans un fichier de cache séparé. Sans Internet au premier affichage, le message « Stress tests indisponibles » peut apparaître.

### Interprétation

« Au pire moment de 2008, ce portefeuille aurait perdu 33,5 %, soit 33 500 € » parle davantage à un client qu'une volatilité. Les poids sont ceux d'**aujourd'hui** : on teste la composition actuelle, pas le portefeuille que vous déteniez à l'époque.

## Titre non coté à l'époque : comment le stress test l'estime-t-il ?
<!-- fiche: conseil-stress-proxy | questions: mon etf n'existait pas en 2008 comment est calculé le stress test ; c'est quoi part estimée par un indice ; pourquoi la source indique indice gspc ; quel indice remplace un titre récent ; comment sont traitées les obligations dans les stress tests ; le stress test est il fiable si mes titres sont récents ; proxy stress test | mots: proxy, approximation, indice régional, S&P 500, Euro Stoxx 50, fonds obligataire, part estimée, titre récent, historique manquant | aller: Conseil patrimonial/Stress tests -->

Beaucoup de titres n'existaient pas lors des crises anciennes. Le logiciel remplace alors la variation du titre par celle d'un **indice ou d'un fonds représentatif** (un « proxy »).

### Quand un titre est-il remplacé ?

Quand il n'a pas de cours, ou quand son premier cours connu est postérieur de plus de 7 jours au début de la crise.

### Quel remplaçant ?

**Pour une obligation ou de l'or** (classe d'actifs autre que « Actions »), un fonds de la même catégorie, coté depuis 2007 au plus tard :

| Catégorie | Fonds utilisé |
|---|---|
| Obligations d'État | IEF |
| Obligations indexées sur l'inflation | TIP |
| Obligations d'entreprises | LQD |
| Obligations à haut rendement | HYG |
| Obligations émergentes | EMB |
| Or | GLD |

Un indice actions serait une mauvaise approximation : en 2008, les emprunts d'État ont monté pendant que les actions chutaient.

**Pour une action** (ou si la catégorie n'est pas reconnue), l'indice de sa région :

| Région | Indice |
|---|---|
| États-Unis, Monde (ETF) | ^GSPC (S&P 500) |
| Europe | ^STOXX50E (Euro Stoxx 50) |
| Royaume-Uni | ^FTSE |
| Suisse | ^SSMI |
| Japon | ^N225 |
| Asie-Pacifique | ^AXJO |
| Canada | ^GSPTSE |
| Émergents | EEM |

Si la région est inconnue, ou si le remplaçant n'a pas non plus de cours, le S&P 500 est utilisé. Si aucun cours n'est disponible du tout, la variation de la ligne est comptée à 0.

### La colonne « Part estimée par un indice »

```
part estimée = Σ poids actuels des lignes remplacées par un indice ou un fonds
```

Exemple : une ligne de 30 % remplacée par ^GSPC et une de 10 % par IEF donnent **40 %**. Plus ce chiffre est élevé, plus le résultat est une approximation. Le détail ligne par ligne indique la source (« titre » ou « indice ^GSPC »).

### Limites

Un ETF « monde » approché par le S&P 500 ignore le reste du monde ; une petite capitalisation approchée par un grand indice sous-estime souvent sa baisse.

## Les chocs hypothétiques : baisse des actions et du dollar
<!-- fiche: conseil-chocs-hypothetiques | questions: que se passe t il si la bourse baisse de 20 % ; comment est calculé le choc sur les actions ; pourquoi utiliser le bêta dans les stress tests ; impact d'une baisse du dollar sur mon portefeuille ; mon etf sp500 en euros n'est pas compté dans la baisse du dollar ; scénarios hypothétiques stress test ; baisse de 35 % des marchés | mots: choc hypothétique, bêta, baisse des actions, dollar, change, USD, sensibilité, scénario, 10 %, 20 %, 35 % | aller: Conseil patrimonial/Stress tests | chiffres: beta, valeur_actuelle -->

À droite des crises passées, le graphique « Chocs hypothétiques » applique des scénarios simples. Son sous-titre résume les règles : « Actions : bêta × choc · Dollar : part investie en dollars · Taux : duration ».

### Baisse des actions de 10 %, 20 % et 35 %

```
variation du portefeuille ≈ bêta × choc
```

Le **bêta** est celui de l'onglet Risque : la sensibilité du portefeuille à l'indice choisi avec le menu [[Indice de référence]] des Paramètres. Un bêta de 0,85 signifie que le portefeuille bouge en moyenne de 0,85 % quand l'indice bouge de 1 %.

Exemple : bêta 0,85, choc −20 % : variation = 0,85 × −20 % = **−17 %**, soit −17 000 € sur 100 000 €.

### Baisse du dollar de 10 %

```
variation = −10 % × part du portefeuille cotée en dollars
```

Exemple : 35 % du portefeuille en titres cotés en USD : variation = −10 % × 35 % = **−3,5 %**.

Attention : le logiciel regarde la **devise de cotation**. Un ETF coté en euros qui investit en actions américaines n'est pas compté, alors qu'il subit en réalité l'effet de change. Pour une vue complète de l'exposition aux devises, consultez l'onglet Expositions.

### Interprétation

Le bêta résume le risque de marché en un seul chiffre. Il est pratique, mais linéaire : en crise, les corrélations montent et la perte réelle peut dépasser bêta × choc. C'est pourquoi les scénarios historiques, qui utilisent les vraies variations, complètent ces chocs.

### Limites

- le bêta est estimé sur votre période d'analyse ;
- le choc dollar ignore l'effet sur les entreprises elles-mêmes (exportateurs, etc.) ;
- un choc sur un indice ne dit rien d'un choc propre à un secteur.

## Le choc de hausse des taux et la duration
<!-- fiche: conseil-hausse-taux | questions: que se passe t il si les taux montent de 1 % ; c'est quoi la duration ; pourquoi mes obligations baissent quand les taux montent ; le scénario hausse des taux n'apparait pas ; comment est calculée la perte de mes fonds obligataires ; sensibilité aux taux de mon portefeuille | mots: hausse des taux, duration, sensibilité, obligations, taux d'intérêt, fonds obligataire, 1 point, risque de taux | aller: Conseil patrimonial/Stress tests | chiffres: valeur_actuelle -->

Le scénario « Hausse des taux de 1 point » estime la perte des **fonds obligataires** de votre portefeuille si les taux d'intérêt montaient de 1 point (par exemple de 3 % à 4 %).

### La duration

La **duration** d'une obligation (en années) mesure sa sensibilité aux taux : une duration de 7 ans signifie qu'une hausse des taux de 1 point fait baisser son prix d'environ 7 %. Quand les taux montent, les obligations anciennes, qui rapportent moins que les nouvelles, perdent de la valeur.

### La formule

```
variation du portefeuille = −1 % × Σ (poids de la ligne × duration de la ligne)
```

Les lignes sans duration (actions, or) comptent pour 0. La duration de chaque fonds vient du référentiel de titres du logiciel.

### Exemple

15 % du portefeuille dans un fonds de duration 7 ans et 5 % dans un fonds de duration 3 ans :

- variation = −1 % × (0,15 × 7 + 0,05 × 3) = −1 % × 1,2 = **−1,2 %**, soit −1 200 € sur 100 000 € ;
- duration moyenne des obligations = 1,2 / 0,20 = 6 ans.

### Quand ce scénario apparaît-il ?

Seulement si au moins une ligne a une duration connue. Un portefeuille 100 % actions, ou des fonds obligataires absents du référentiel, ne l'affichent pas.

### Limites

- la relation est linéaire : pour un gros choc, la convexité rend la perte réelle un peu plus faible ;
- l'effet d'une hausse des taux sur les **actions** n'est pas pris en compte dans ce scénario (voir plutôt la crise « Inflation et hausse des taux (2022) » dans les scénarios historiques) ;
- les durations du référentiel sont des valeurs fixes, qui évoluent en réalité avec le temps.

## Les limites des stress tests
<!-- fiche: conseil-stress-limites | questions: les stress tests sont ils fiables ; pourquoi la perte affichée est différente de ce que j'ai vraiment perdu en 2020 ; les dividendes sont ils pris en compte dans les stress tests ; effet de change dans les crises passées ; stress tests indisponibles que faire ; le pire scénario peut il être pire | mots: limites, fiabilité, devise locale, hors dividendes, change, approximation, cache, indisponible | aller: Conseil patrimonial/Stress tests -->

Les stress tests donnent des ordres de grandeur, pas des chiffres exacts.

### Les simplifications

- **Devise locale** : dans les scénarios historiques, les variations sont calculées dans la devise de cotation de chaque titre. L'effet de change pour un investisseur en euros est ignoré : une hausse ou une baisse du dollar pendant la crise aurait amorti ou aggravé la perte réelle en euros.
- **Hors dividendes** : les cours ne sont pas ajustés des dividendes. Sur une crise de quelques mois, l'écart reste faible.
- **Poids actuels** : on teste la composition d'aujourd'hui, pas celle que vous aviez à l'époque. Ce n'est donc pas ce que vous avez réellement perdu.
- **Du plus haut au plus bas du marché** : les dates sont celles du marché dans son ensemble ; un titre peut avoir touché son plus bas un autre jour.
- **Proxies** : un titre récent est remplacé par un indice ou un fonds (voir la colonne « Part estimée par un indice »).
- **Chocs linéaires** : bêta × choc et duration × hausse des taux sont des approximations au premier ordre.

### Le pire peut être pire

Les cinq crises ne couvrent pas tous les risques : une crise future peut être différente (inflation durable, choc géopolitique, krach sectoriel). Le pire scénario affiché n'est pas une borne.

### En cas de message « Stress tests indisponibles »

La cause la plus fréquente est l'absence d'Internet au premier affichage : l'historique depuis 2008 n'a pas encore été téléchargé. Reconnectez-vous et rouvrez l'onglet. Ensuite, le cache prend le relais.
