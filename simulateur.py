import streamlit as st
import pandas as pd
import numpy as np
from modele import simulation , montant_epargne_cible


# --- Configuration générale ---
st.set_page_config(
    page_title="UCAMWAL - Simulateur d'Investissement",
    page_icon="https://businesstodayng.com/wp-content/uploads/2025/06/IMG_0855.jpeg",
    layout="wide"
)

# --- Personnalisation CSS ---
st.markdown("""
    <style>
    /* Couleur principale : rouge UCAMWAL */
    :root {
        --ucamwal-red: #C8102E;
    }

    /* Titres */
    h1, h2, h3 {
        color: var(--ucamwal-red);
    }

    /* Boutons */
    div.stButton > button:first-child {
        background-color: var(--ucamwal-red);
        color: white;
        border: none;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #a00c25;
        color: #fff;
    }

    /* Tableau : entête rouge */
    .stDataFrame table thead th {
        background-color: var(--ucamwal-red) !important;
        color: white !important;
        font-weight: bold !important;
        text-align: center !important;
    }

    /* Corps du tableau */
    .stDataFrame table tbody td {
        text-align: center !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #fff5f5;
    }

    /* Pied de page */
    footer {
        background-color: #f5f5f5;
        color: #666;
        padding: 10px;
        text-align: center;
        border-top: 2px solid var(--ucamwal-red);
    }
    </style>
""", unsafe_allow_html=True)


# --- Logo dans la sidebar ---
logo_url = "https://unitedcapitalplcgroup.com/wp-content/uploads/2021/08/United-Capital-logo-websites.png"
st.sidebar.image(logo_url, width=250)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("**Asset Management West Africa Limited**")

# --- Titre principal ---
st.title("💼 Simulateur d'Investissement UCAMWAL")

st.write("""
**UCAMWAL (United Capital Asset Management West Africa Limited)** est une société de gestion d’OPCVM qui propose des fonds adaptés aux besoins des investisseurs particuliers et institutionnels.

Ce simulateur vous permet d’estimer :

- 💰 le montant à épargner pour que les rendements couvrent une dépense annuelle,

- 📈 la valeur future de votre capital selon vos contributions et le fonds choisi.

Fonds disponibles et rendements annuels attendus :

- **💎 United Capital Diamond Fund**  rendement annuel attendu : 8 %

- **🔹 United Capital Sapphire Fund**  rendement annuel attendu : 9 %
""")

# --- Saisie des informations ---
with st.expander("🧮 Paramètres de simulation", expanded=False):     
    col1, col2 = st.columns(2)
    with col1:
        montant_initial = st.number_input("Montant initial (FCFA)", min_value=0, value=1_000_000)
        duree_investissement = st.number_input("Durée de l'investissement (années)", min_value=1, value=5)
        fond_choisi = st.selectbox("Fonds sélectionné", ["Unitid Capital Dimond", "United Capital Sapphire"])
    with col2:
        choix = st.checkbox("Activer les versements périodiques", value=False)
        if choix:
            montant_periodique = st.number_input("Montant périodique (FCFA)", min_value=0, value=100_000)
            frequence = st.selectbox("Fréquence des contributions", ["Mensuelle", "Annuelle"])
            annees_contributions = st.number_input("Durée des contributions (années)", min_value=0, value=3, max_value=duree_investissement)
        else:
            montant_periodique = 0
            frequence = "Annuelle"
            annees_contributions = 0

# --- Données de rendement ---
Rendement_dict = {
    "Unitid Capital Dimond": 0.08,
    "United Capital Sapphire": 0.09
}

# --- Calcul ---
if st.button("🚀 Lancer la simulation", use_container_width=True):
    taux_rendement = Rendement_dict[fond_choisi]
    
    valeurs= simulation(montant_initial, duree_investissement, taux_rendement, montant_periodique, frequence, annees_contributions)
    valeurs_dat= simulation(montant_initial, duree_investissement, 0.06, montant_periodique, frequence, annees_contributions)
    
    ecart = list(np.array(valeurs) - np.array(valeurs_dat))
    colonnes = [f"Année {i+1}" for i in range(duree_investissement)]
    
    resultats = pd.DataFrame(
        [valeurs, valeurs_dat, ecart],
        index=[f"{fond_choisi}", "DAT 6%", f"Écart ({fond_choisi} - DAT)"],
        columns=colonnes
    )

    st.subheader("📊 Résultats de la simulation")
    st.dataframe(resultats, use_container_width=True)



# Dictionnaire des fonds et leurs rendements annuels
taux_fonds = {
    "United Capital Diamond": 0.08,
    "United Capital Sapphire": 0.09
}



with st.expander("🧮 Paramètres de l’épargne pour couvrir une dépense", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        choix = st.checkbox("Cocher pour estimer combien épargner pour que le rendement couvre votre charge")

        depense_annuelle = st.number_input(
            "Dépense annuelle à couvrir ou capital cible (FCFA)",
            min_value=0,
            value=1000
        )

        duree_mois = st.number_input(
            "Durée pour constituer le capital (en mois)",
            min_value=1,
            value=60
        )

    with col2:
        fond_choisi = st.selectbox(
            "Fonds sélectionné",
            list(taux_fonds.keys())
        )
        taux_rendement_annuel = taux_fonds[fond_choisi]

        # Options dynamiques selon la durée
        options_type = ["unique"]
        if duree_mois > 1:
            options_type.append("mensuelle")
        if duree_mois > 12:
            options_type.append("annuelle")

        type_contribution = st.selectbox(
            "Type de contribution",
            options_type
        )

# Calcul du capital cible
if st.button("🚀 Calculer l’épargne nécessaire", use_container_width=True):
    if choix:
        capital_cible = depense_annuelle / taux_rendement_annuel
    else:
        capital_cible = depense_annuelle

    montant, capital = montant_epargne_cible(
        capital_cible, duree_mois, taux_rendement_annuel, type_contribution
    )


    Resultat_list = [type_contribution, duree_mois, fond_choisi, taux_rendement_annuel,capital_cible, montant]

    # transformer en liste de lignes
    Resultat_data = pd.DataFrame([Resultat_list], columns=['Periodicité', 'Horizon de placement', 'Fonds', 'Rendement', 'Capital cible','Épargne'])

    st.dataframe(Resultat_data, use_container_width=True)

    
    st.success(f"Montant à épargner ({type_contribution}) : {montant:,.0f} FCFA")
    #st.info(f"Capital cible à atteindre : {capital:,.0f} FCFA")
    st.write(f"Fonds sélectionné : {fond_choisi} — rendement annuel de {taux_rendement_annuel*100:.2f}%")

    
# --- Pied de page ---
st.markdown("""
<footer>
    © 2025 United Capital Asset Management West Africa Limited | Tous droits réservés
</footer>
""", unsafe_allow_html=True)
