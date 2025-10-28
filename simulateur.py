import streamlit as st


# --- Configuration générale de la page ---
st.set_page_config(
    page_title="UCAMWAL",
    page_icon="https://businesstodayng.com/wp-content/uploads/2025/06/IMG_0855.jpeg",
    layout="wide"
)

# --- Logo dans la sidebar ---
logo_url = "https://unitedcapitalplcgroup.com/wp-content/uploads/2021/08/United-Capital-logo-websites.png"
st.sidebar.image(logo_url, width=250, caption="Asset Management West Africa Limited")



# --- Titre principal ---
st.title("Simulateur d'Investissement UCAMWAL")

st.write(
        """
        UCAMWAL (United Capital Asset Management West Africa Limited) est une société de gestion d'OPCVM
        qui offre une gamme de produits d'investissement adaptés aux besoins des investisseurs individuels
        et institutionnels. Ce simulateur est conçu pour vous aider à comprendre le potentiel de croissance
        de vos investissements avec UCAMWAL.

        Ce simulateur vous permet d'estimer la valeur future de votre investissement avec UCAMWAL.
        Entrez le montant initial et la durée de l'investissement pour voir comment votre investissement peut croître au fil du temps.
        """
    )

with st.expander("Saisissez vos informations", expanded=False):     

        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Montant initial (en FCFA)", min_value=0, value=1000000)
            Dure = st.number_input("Durée de l'investissement (en années)", min_value=1, value=5)
            st.selectbox("Sélectionné le Fond", options=["DIAMOND", "SAPPHIRE"])
             
        with col2:
            choix = st.checkbox("Investissement périodique", value=False)
            if choix:
                st.number_input("Montant périodique (en FCFA)", min_value=0, value=100000)
                st.selectbox("Fréquence des contributions", options=["Mensuelle", "Annuelle"])
                st.number_input("Nombre d'années de contributions", min_value=0, value=5, max_value=Dure)
                #if Dure < st.session_state.get('nombre_annees_contributions', 5):
                   # st.info("La durée de l'investissement doit être supérieure ou égale à la durée des contributions.")
        
Rendement_dict = {
    "DIAMOND": 0.08,
    "SAPPHIRE": 0.09,
    "DATE": 0.10
}


# --- Calcul et affichage des résultats ---
if st.button("🚀 Exécuter la simulation", use_container_width=True):

    montant_initial = st.session_state.get('montant_initial', 1000000)
    duree_investissement = st.session_state.get('duree_investissement', 5)
    fond_choisi = st.session_state.get('fond_choisi', "DIAMOND")
    taux_rendement = Rendement_dict.get(fond_choisi, 0.08)

    retour = []

    if choix:
        montant_periodique = st.session_state.get('montant_periodique', 100000)
        frequence = st.session_state.get('frequence', "Mensuelle")

        if frequence == "Mensuelle":
            n = 12
            taux_rendement /= n
        else:
            n = 1

        montant_total = montant_initial + montant_periodique * n * duree_investissement

        retour_1 = montant_initial * (1 + taux_rendement)
        retour.append(retour_1)

        montant_2 = montant_periodique +  retour_1

        for i in range(duree_investissement * n):
            montant_retour =  montant_2 * (1 + taux_rendement) ** (i + 1)
            retour.append(montant_retour)
            montant_retour += montant_periodique





# --- Pied de page ---
st.markdown(
    """
    <style>
    footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: #f1f1f1;
        text-align: center;
        padding: 10px;
    }
    </style>
    <footer>
        <p>© 2025 United Capital Asset Management West Africa Limited </p>
    </footer>
    """,
    unsafe_allow_html=True
)