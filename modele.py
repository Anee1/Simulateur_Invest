import numpy as np 

def simulation(montant_initial, 
               duree_investissement, 
               taux_rendement, 
               montant_periodique=0, 
               frequence='Mensuelle', 
               annees_contributions=3):
    """
    Évalue la valeur finale d’un investissement avec capitalisation.

    Paramètres :
        montant_initial (float) : Capital de départ.
        duree_investissement (int) : Durée totale en années.
        taux_rendement (float) : Rendement annuel (ex : 0.05 pour 5%).
        montant_periodique (float) : Versement périodique (par défaut 0).
        frequence (str) : 'Mensuelle' ou 'Annuelle'.
        annees_contributions (int) : Durée des versements périodiques (en années).
    
    Retourne :
        list : Valeur du portefeuille à la fin de chaque année.
        float : Valeur finale estimée.
    """

    if frequence.lower() == 'mensuelle':
        periodes_par_an = 12
    elif frequence.lower() == 'trimestrielle':
        periodes_par_an = 4
    else:
        periodes_par_an = 1  # annuelle

    rendement_par_periode = taux_rendement / periodes_par_an
    total_periodes = duree_investissement * periodes_par_an
    periodes_contributions = annees_contributions * periodes_par_an

    valeur = montant_initial
    valeurs_annuelles = []

    for periode in range(1, int(total_periodes) + 1):
        # D'abord, appliquer le rendement sur le capital existant
        valeur *= (1 + rendement_par_periode)

        # Ensuite, verser la contribution (à partir de la 2e période)
        if periode <= periodes_contributions and periode > 1:
            valeur += montant_periodique

        # Stocker la valeur à la fin de chaque année
        if periode % periodes_par_an == 0:
            valeurs_annuelles.append(round(valeur, 2))

    #valeur_finale = round(valeur, 2)
    return valeurs_annuelles



def montant_epargne_cible(capital_necessaire, duree_mois, taux_rendement_annuel, type_contribution='mensuelle'):
    """
    Calcule le montant à épargner périodiquement pour constituer un capital 
    dont les rendements couvrent une dépense annuelle donnée.

    Paramètres :
        depense_annuelle (float) : Montant annuel à financer uniquement via les rendements.
        duree_mois (int) : Durée pour constituer le capital (en mois).
        taux_rendement_annuel (float) : Rendement annuel attendu (ex: 0.06 pour 6%).
        type_contribution (str) : 'mensuelle', 'annuelle' ou 'unique'.

    Retourne :
        float : Montant à épargner périodiquement.
        float : Capital cible à atteindre pour couvrir la dépense.
    """
    # Capital nécessaire pour générer la dépense uniquement via les rendements
    #capital_cible  = depense_annuelle / taux_rendement_annuel

    # Conversion du taux annuel en taux mensuel
    taux_mensuel = (1 + taux_rendement_annuel) ** (1 / 12) - 1

    # Contribution unique
    if type_contribution.lower() == 'unique':
        montant = capital_necessaire / ((1 + taux_mensuel) ** duree_mois)

    # Contributions mensuelles
    elif type_contribution.lower() == 'mensuelle':
        
        montant = capital_necessaire * taux_mensuel / ((1 + taux_mensuel) ** duree_mois - 1)

    # Contributions annuelles
    elif type_contribution.lower() == 'annuelle':
        duree_annees = duree_mois / 12
        taux_annuel = taux_rendement_annuel
        montant = capital_necessaire * taux_annuel / ((1 + taux_annuel) ** duree_annees - 1)

    else:
        raise ValueError("type_contribution doit être 'mensuelle', 'annuelle' ou 'unique'.")

    return round(montant, 2), round(capital_necessaire, 2)
