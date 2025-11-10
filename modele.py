import numpy as np 

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet

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



def montant_epargne_cible(capital_necessaire, duree_mois, taux_rendement_annuel, type_contribution):
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
    duree_periodes = duree_mois / (12 / periodes_par_an)

    # Calcul
    if type_contribution == 'Unique':
        montant = capital_necessaire / ((1 + taux_par_periode) ** duree_periodes)
    else:
        montant = capital_necessaire * taux_par_periode / ((1 + taux_par_periode) ** duree_periodes - 1)

    return round(montant, 3), round(capital_necessaire, 2)



from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generate_pdf(logo_url, fond_choisi, taux_rendement, montant_initial, choix, horizon, frequence, annees_contributions, df_resultats, montant_periodique):
    """
    Génère un rapport PDF stylisé de simulation d’investissement.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=30, leftMargin=30,
                            topMargin=30, bottomMargin=30)
    
    # Styles personnalisés
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TitleCenter', parent=styles['Title'], alignment=TA_CENTER, textColor=colors.red))
    styles.add(ParagraphStyle(name='HeadingRed', parent=styles['Heading2'], textColor=colors.red))
    styles.add(ParagraphStyle(name='BodyJustify', parent=styles['BodyText'], alignment=TA_LEFT, leading=14))
    styles.add(ParagraphStyle(name='SubLogo', alignment=TA_CENTER, textColor=colors.grey, fontSize=9, leading=10))
    
    elements = []

    # Logo + nom de l'entreprise
    elements.append(Image(logo_url, width=120, height=50))
    elements.append(Paragraph("Asset Management West Africa Limited", styles['SubLogo']))
    elements.append(Spacer(1, 15))

    # Titre
    title = Paragraph("Rapport de Simulation d'Investissement", styles["TitleCenter"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Introduction
    intro_text = (
        "Ce rapport présente les résultats d’une simulation réalisée afin d’évaluer "
        "l’évolution potentielle d’un investissement en fonction des paramètres sélectionnés."
    )
    elements.append(Paragraph(intro_text, styles['BodyJustify']))
    elements.append(Spacer(1, 15))

    # Paramètres de simulation
    if choix:
        param_text = f"""
        <b>Paramètres de simulation :</b><br/>
        - Fonds : {fond_choisi}<br/>
        - Montant initial : {montant_initial:,.0f} FCFA<br/>
        - Horizon d’investissement : {horizon} ans<br/>
        - Rendement annuel attendu : {taux_rendement}%<br/>
        - Montant périodique : {montant_periodique:,.0f} FCFA<br/>
        - Périodicité des versements : {frequence}<br/>
        - Durée des contributions (années) : {annees_contributions}<br/>
        """
    else:
        param_text = f"""
        <b>Paramètres de simulation :</b><br/>
        - Fonds : {fond_choisi}<br/>
        - Montant initial : {montant_initial:,.0f} FCFA<br/>
        - Horizon d’investissement : {horizon} ans<br/>
        - Rendement annuel attendu : {taux_rendement}%<br/>
        """
    elements.append(Paragraph(param_text, styles['BodyJustify']))
    elements.append(Spacer(1, 15))

    # Résultats de simulation
    elements.append(Paragraph("Résultats de la simulation :", styles['HeadingRed']))
    
    df_display = df_resultats.copy()
    df_display.reset_index(inplace=True)
    df_display.rename(columns={'index': 'Index'}, inplace=True)

    table_data = [df_display.columns.tolist()] + df_display.values.tolist()
    
    table = Table(table_data, hAlign='CENTER')
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.red),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.Color(1, 0.9, 0.9)),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ])
    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 20))

    # Interprétation
    interpretation = (
        "Ces résultats reflètent une estimation basée sur les hypothèses définies. "
        "Ils ne constituent pas une garantie de performance future."
    )
    elements.append(Paragraph(interpretation, styles['BodyJustify']))
    elements.append(Spacer(1, 20))

    # Pied de page
    footer = Paragraph(
        "<font size=8>Document généré automatiquement par l’outil de simulation UCAMWAL.</font>",
        styles["Normal"]
    )
    elements.append(footer)

    doc.build(elements)
    buffer.seek(0)
    return buffer


