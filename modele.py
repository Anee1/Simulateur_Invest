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
