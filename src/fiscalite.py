"""
fiscalite.py — Performance nette d'impôts selon l'enveloppe fiscale.

Un même portefeuille ne rapporte pas la même somme "dans la poche" de
l'investisseur selon qu'il est détenu sur un compte-titres, un PEA ou un
contrat d'assurance-vie. Ce module compare les trois, pour une sortie
(vente de tout le portefeuille) aujourd'hui ou à un horizon futur.

Règles retenues (France, particulier résident, 2026) :

  Compte-titres ordinaire (CTO)
    - prélèvement forfaitaire unique (PFU, "flat tax") de 31,4 % :
      12,8 % d'impôt sur le revenu + 18,6 % de prélèvements sociaux
      (hausse de la CSG au 1er janvier 2026, auparavant 30 %) ;
    - les dividendes et les plus-values sont imposés ; les moins-values
      s'imputent sur les plus-values (pas sur les dividendes).

  Plan d'épargne en actions (PEA)
    - avant 5 ans : retrait = clôture, gain imposé à 31,4 % ;
    - après 5 ans : gain exonéré d'impôt sur le revenu, seuls les
      prélèvements sociaux de 18,6 % s'appliquent ;
    - réservé aux actions de sociétés européennes (UE / EEE) et aux fonds
      éligibles, plafond de versements de 150 000 €.

  Assurance-vie (unités de compte)
    - prélèvements sociaux de 17,2 % (non concernés par la hausse de 2026) ;
    - avant 8 ans : 12,8 % d'impôt sur le revenu (total 30 %) ;
    - après 8 ans : abattement annuel de 4 600 € sur les gains (9 200 € pour
      un couple), puis 7,5 % d'impôt (primes jusqu'à 150 000 €).

Simplifications (à citer dans le rapport) : option pour le barème progressif
ignorée, primes d'assurance-vie supposées inférieures à 150 000 €, frais de
gestion des contrats ignorés, dividendes supposés conservés dans l'enveloppe.
"""

# Taux en vigueur en 2026 (source : loi n° 2025-1403 du 30 décembre 2025 de financement de
# la sécurité sociale pour 2026, hausse de la CSG sur les revenus du capital)
IR_PFU = 0.128
PS_CAPITAL = 0.186            # dividendes, plus-values mobilières, PEA
PS_ASSURANCE_VIE = 0.172      # l'assurance-vie reste à 17,2 %
PFU_TOTAL = IR_PFU + PS_CAPITAL          # 31,4 %
IR_AV_APRES_8_ANS = 0.075
ABATTEMENT_AV = {"célibataire": 4600, "couple": 9200}
DUREE_PEA = 5
DUREE_AV = 8

# Pays de l'Union européenne et de l'EEE (éligibilité PEA)
PAYS_EEE = {
    "France", "Allemagne", "Pays-Bas", "Belgique", "Luxembourg", "Italie", "Espagne", "Portugal",
    "Irlande", "Autriche", "Finlande", "Danemark", "Suède", "Grèce", "Pologne", "Tchéquie",
    "Hongrie", "Roumanie", "Bulgarie", "Croatie", "Slovénie", "Slovaquie", "Estonie", "Lettonie",
    "Lituanie", "Chypre", "Malte", "Norvège", "Islande", "Liechtenstein",
}
# Fonds indiciels connus pour être éligibles au PEA (réplication synthétique)
ETF_ELIGIBLES_PEA = {"CW8.PA", "ESE.PA"}


def impot_sortie(gain_total, duree_annees, enveloppe, dividendes=0.0, situation="célibataire"):
    """Impôt dû si l'on vend tout le portefeuille.

    gain_total   : gain total (plus-values + dividendes), en euros
    duree_annees : ancienneté de l'enveloppe (en années)
    enveloppe    : "CTO", "PEA" ou "Assurance-vie"
    dividendes   : part du gain venant des dividendes (utile pour le CTO :
                   une moins-value ne peut pas effacer des dividendes)

    Renvoie un dictionnaire : impôt sur le revenu, prélèvements sociaux, total.
    """
    if enveloppe == "CTO":
        plus_values = gain_total - dividendes
        base = max(0.0, plus_values) + max(0.0, dividendes)
        ir, ps = IR_PFU * base, PS_CAPITAL * base
    elif enveloppe == "PEA":
        base = max(0.0, gain_total)
        ir = 0.0 if duree_annees >= DUREE_PEA else IR_PFU * base
        ps = PS_CAPITAL * base
    elif enveloppe == "Assurance-vie":
        base = max(0.0, gain_total)
        ps = PS_ASSURANCE_VIE * base
        if duree_annees >= DUREE_AV:
            ir = IR_AV_APRES_8_ANS * max(0.0, base - ABATTEMENT_AV[situation])
        else:
            ir = IR_PFU * base
    else:
        raise ValueError(f"Enveloppe inconnue : {enveloppe}")
    return {"impot_revenu": ir, "prelevements_sociaux": ps, "total": ir + ps}


def comparer_enveloppes(gain_total, capital_investi, duree_annees, dividendes=0.0,
                        situation="célibataire"):
    """Tableau comparatif des trois enveloppes pour un même gain brut.

    Renvoie une liste de dictionnaires (une ligne par enveloppe) :
    impôts, gain net, performance nette, taux d'imposition effectif, et
    nombre d'années restant avant l'avantage fiscal.
    """
    lignes = []
    for enveloppe, duree_avantage in [("CTO", None), ("PEA", DUREE_PEA), ("Assurance-vie", DUREE_AV)]:
        imp = impot_sortie(gain_total, duree_annees, enveloppe, dividendes, situation)
        net = gain_total - imp["total"]
        lignes.append({
            "enveloppe": enveloppe,
            "gain_brut": gain_total,
            "impot_revenu": imp["impot_revenu"],
            "prelevements_sociaux": imp["prelevements_sociaux"],
            "impots": imp["total"],
            "gain_net": net,
            "performance_brute": gain_total / capital_investi if capital_investi else 0.0,
            "performance_nette": net / capital_investi if capital_investi else 0.0,
            "taux_effectif": imp["total"] / gain_total if gain_total > 0 else 0.0,
            "annees_avant_avantage": None if duree_avantage is None else max(0.0, duree_avantage - duree_annees),
        })
    return lignes


def eligibilite_pea(positions):
    """Part de la valeur du portefeuille éligible au PEA.

    Éligibles : actions de sociétés dont le siège est dans l'UE / l'EEE, et
    fonds éligibles connus. Les actions américaines, britanniques (depuis le
    Brexit), suisses ou japonaises ne le sont pas.
    Renvoie (part éligible, liste des titres non éligibles).
    """
    eligible = [
        (t in ETF_ELIGIBLES_PEA) or (str(p.get("pays", "")) in PAYS_EEE)
        for t, p in positions.iterrows()
    ]
    valeurs = positions["valeur"]
    part = float(valeurs[eligible].sum() / valeurs.sum()) if valeurs.sum() else 0.0
    non_eligibles = [t for t, e in zip(positions.index, eligible) if not e]
    return part, non_eligibles
