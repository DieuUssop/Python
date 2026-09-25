"""
config.py — Les réglages du projet, regroupés au même endroit.

Pour changer d'indice de référence ou de taux sans risque, il suffit de
modifier ce fichier : le reste du code s'adapte automatiquement.
"""

# ----------------------------------------------------------------------
# Indice de référence ("benchmark")
# ----------------------------------------------------------------------
# On compare le portefeuille à cet indice (bêta, alpha, tracking error...).
#
# Choix par défaut : l'ETF Amundi MSCI World (CW8.PA). Il est CAPITALISANT :
# les dividendes sont réinvestis, comme dans notre calcul de performance.
# La comparaison est donc équitable.
#
# Autres choix possibles (codes Yahoo Finance) :
#   "^FCHI"     CAC 40         -> attention : indice HORS dividendes, il
#                                 désavantage l'indice d'environ 3 % par an
#   "^STOXX50E" Euro Stoxx 50  -> hors dividendes également
INDICE_REFERENCE = "CW8.PA"
NOM_INDICE = "MSCI World (ETF Amundi CW8, dividendes réinvestis)"

# ----------------------------------------------------------------------
# Taux sans risque (annuel)
# ----------------------------------------------------------------------
# Rendement d'un placement "sans risque" en euros. Sert au ratio de Sharpe,
# au ratio de Sortino et à l'alpha.
#
# Valeur retenue : 2,50 % = taux de la facilité de dépôt de la BCE, en
# vigueur depuis le 16/09/2026 (source : BCE, "Key ECB interest rates").
# Le €STR (taux interbancaire au jour le jour) est très proche.
#
# Simplification : on utilise un taux CONSTANT sur toute la période, alors
# qu'il a varié (4 % début 2024, 2 % mi-2025...). Amélioration possible :
# télécharger la série historique du €STR.
TAUX_SANS_RISQUE = 0.025

# ----------------------------------------------------------------------
# Value at Risk
# ----------------------------------------------------------------------
# 0.95 = VaR à 95 % : la perte qui n'est dépassée que 5 % des jours.
NIVEAU_CONFIANCE_VAR = 0.95

# ----------------------------------------------------------------------
# Optimisation de Markowitz (étape 7)
# ----------------------------------------------------------------------
# Poids maximal d'un titre dans les portefeuilles optimisés.
# Sans cette limite, l'optimiseur a tendance à tout concentrer sur 2 ou 3
# titres (les meilleurs du passé), ce qui est peu prudent.
# Repère : la réglementation des fonds (OPCVM) limite chaque ligne à 10 %,
# avec une tolérance jusqu'à 40 % pour l'ensemble des lignes de plus de 5 %.
POIDS_MAX = 0.30

# ----------------------------------------------------------------------
# Projection Monte-Carlo (étape 8)
# ----------------------------------------------------------------------
HORIZON_PROJECTION = 10          # années
VERSEMENT_MENSUEL = 0.0          # euros ajoutés chaque mois dans la projection
NB_SIMULATIONS = 5000            # nombre de scénarios simulés
METHODE_SIMULATION = "normale"   # "normale" ou "historique" (bootstrap)

# ----------------------------------------------------------------------
# Conseil patrimonial (étape 10)
# ----------------------------------------------------------------------
# Profil utilisé par main.py et le rapport PDF (dans le tableau de bord,
# le profil est calculé à partir du questionnaire).
# Choix : "Sécuritaire", "Prudent", "Équilibré", "Dynamique", "Offensif"
PROFIL_CLIENT = "Équilibré"
SITUATION_FAMILIALE = "célibataire"      # ou "couple" (abattement de l'assurance-vie)
