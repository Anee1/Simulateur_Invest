import numpy as np 

def simulation(montant_initial, 
               duree_investissement, 
               taux_rendement, 
               montant_periodique=0, 
               frequence='Mensuelle', 
               annees_contributions=3):
    """
    Évalue la valeur finale d’un investissement avec capitalisation composée.

    Paramètres :
        montant_initial (float) : Capital de départ.
        duree_investissement (int) : Durée totale en années.
        taux_rendement (float) : Rendement annuel composé (ex : 0.05 pour 5%).
        montant_periodique (float) : Versement périodique (par défaut 0).
        frequence (str) : 'Mensuelle', 'Trimestrielle', 'Semestrielle' ou 'Annuelle'.
        annees_contributions (int) : Durée des versements périodiques (en années).
    
    Retourne :
        list : Valeur du portefeuille à la fin de chaque année.
    """

    frequence = frequence.lower()

    if frequence == 'mensuelle':
        periodes_par_an = 12
    elif frequence == 'trimestrielle':
        periodes_par_an = 4
    elif frequence == 'semestrielle':
        periodes_par_an = 2
    else:
        periodes_par_an = 1  # annuelle

    # Conversion du taux annuel en taux équivalent par période
    rendement_par_periode = (1 + taux_rendement)**(1 / periodes_par_an) - 1

    total_periodes = duree_investissement * periodes_par_an
    periodes_contributions = annees_contributions * periodes_par_an

    valeur = montant_initial
    valeurs_annuelles = []

    for periode in range(1, int(total_periodes)+1):
        # Capitalisation
        valeur *= (1 + rendement_par_periode)

        # Versement périodique
        if periode <= periodes_contributions :
            valeur += montant_periodique

        # Enregistrer la valeur à la fin de chaque année

        if periode % periodes_par_an == 0 :
            valeurs_annuelles.append(round(valeur, 2))

    return valeurs_annuelles



def montant_epargne_cible(capital_necessaire, duree_mois, taux_rendement_annuel, type_contribution='Mensuelle'):
    """
    Calcule le montant à épargner périodiquement pour constituer un capital cible.
    """
    type_contribution = type_contribution.capitalize()  # Sensible à la casse

    if type_contribution == "Mensuelle":
        periodes_par_an = 12
    elif type_contribution == "Trimestrielle":
        periodes_par_an = 4
    elif type_contribution == "Semestrielle":
        periodes_par_an = 2
    elif type_contribution == "Annuelle":
        periodes_par_an = 1
    elif type_contribution == "Unique":
        periodes_par_an = 1
    else:
        raise ValueError("type_contribution doit être 'Unique', 'Mensuelle', 'Trimestrielle', 'Semestrielle' ou 'Annuelle'.")

    # Conversion du taux annuel en taux équivalent par période
    taux_par_periode = (1 + taux_rendement_annuel) ** (1 / periodes_par_an) - 1

    # Nombre total de périodes
    duree_periodes = duree_mois / 12 * periodes_par_an

    # Calcul
    if type_contribution == 'Unique':
        montant = capital_necessaire / ((1 + taux_par_periode) ** duree_periodes)
    else:
        montant = capital_necessaire * taux_par_periode / ((1 + taux_par_periode) ** duree_periodes - 1)

    return round(montant, 3), round(capital_necessaire, 2)

