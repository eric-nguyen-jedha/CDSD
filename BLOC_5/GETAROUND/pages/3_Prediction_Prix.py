import streamlit as st
import requests
import time

# --- Configuration de la Page ---

# --- INJECTION DE CSS POUR PERSONNALISER LE FORMULAIRE ---
st.markdown("""
<style>
    /* ------------------- STYLES GÉNÉRAUX ------------------- */
    
    /* Couleur et graisse des labels au-dessus des widgets */
    label {
        color: #333333 !important;
        font-weight: bold !important;
    }
    
    /* ------------------- STYLES POUR LES CHAMPS DE SAISIE ------------------- */
    
    /* Style commun pour les champs selectbox et number_input */
    .stSelectbox div[data-baseweb="select"] > div,
    .stNumberInput div[data-baseweb="input"] {
        background-color: #4A4A6A;
        border: 2px solid #C576F6;
        border-radius: 10px;
        color: white;
    }
    .stNumberInput input {
        background-color: transparent; /* Fond transparent pour hériter de la couleur parente */
        color: white;
    }
    
    /* Style pour les flèches + et - du number_input */
    .stNumberInput button {
        background-color: #C576F6 !important;
        border-radius: 5px;
    }
    .stNumberInput button svg {
        fill: white;
    }
    /* ------------------- ✨ STYLE CORRIGÉ POUR LA CHECKBOX ✨ ------------------- */
    
    /* Cibler le texte (label) à côté de la checkbox */
    .stCheckbox span {
        color: #333333;
        font-size: 16px;
    }
    
    /* CORRECTION ICI : Changer la couleur de la coche en DORÉ pour correspondre à la maquette */
    .stCheckbox [data-testid="stTickData"] svg {
        fill: #F3C583 !important;  /* Couleur dorée/jaune */
        stroke: #F3C583 !important; /* Couleur dorée/jaune */
    }
    
    /* Changer la couleur de la bordure de la case (pour un look plus doux) */
    .stCheckbox [data-testid="stWidgetLabel"]+div {
        border-color: #BBBBBB !important;
    }
    /* Mettre la bordure en doré quand la case est cochée */
    .stCheckbox [data-testid="stTickData"] ~ div {
        border-color: #F3C583 !important;
    }
    /* ------------------- STYLE POUR LE BOUTON DU FORMULAIRE ------------------- */
    
    .stForm [data-testid="stFormSubmitButton"] button {
        background-color: #C576F6;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
    }
    .stForm [data-testid="stFormSubmitButton"] button:hover {
        background-color: #b725c8;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Prédiction GetAround",
    page_icon="🚗",
    layout="wide" # Utilise toute la largeur de la page
)

with st.sidebar:
    st.title("Dashboard Menu")
    
    st.page_link("app.py", label="Accueil", icon="🏠")
    st.page_link("pages/1_EDA_GetAround.py", label="EDA GetAround", icon="📈")
    st.page_link("pages/2_Simulateur_Seuil.py", label="Simulateur Seuil", icon="⏱️")
    st.page_link("pages/3_Prediction_Prix.py", label="Prediction Prix", icon="💰")

st.html(
    "<h1 style='color: #b725c8cc; font-size: 22px'>🚗 Estimateur de Prix de Location GetAround</span>!</h1>"
)

# --- Variables Globales ---
# URL de l'API que nous avons mis tant de temps à faire fonctionner !
API_URL = "https://ericjedha-getaroundapi.hf.space/predict/"

# --- Titre et Description ---
st.markdown("Estimation du prix de location journalier pour un véhicule")
st.markdown("---") # Ajoute une ligne de séparation

# --- Création des Colonnes ---
col_form, col_result = st.columns([2, 1]) # La colonne du formulaire sera 2x plus large que celle du résultat

# ==============================================================================
# --- COLONNE DE GAUCHE : Le Formulaire de Saisie ---
# ==============================================================================
with col_form:
    st.header("Caractéristiques du véhicule")

    # Utiliser un formulaire pour regrouper les champs et n'envoyer la requête qu'au clic du bouton
    with st.form("prediction_form"):
        
        # Diviser le formulaire en sous-colonnes pour un meilleur agencement
        sub_col1, sub_col2 = st.columns(2)

        with sub_col1:
            # Choix prédéfinis pour éviter les erreurs de saisie
            model_key = st.selectbox("Marque du véhicule", ["Citroën", "Peugeot", "PGO", "Renault", "Audi", "BMW", "Mercedes", "Opel", "Volkswagen", "Ferrari", "Nissan", "SEAT", "Subaru", "Toyota", "Maserati", "Porsche", "Ford", "KIA Motors", "Alfa Romeo", "Fiat", "Lamborghini", "Honda", "Lexus", "Mini", "Mitsubishi", "Smart"])
            paint_color = st.selectbox("Couleur", ["black", "grey", "white", "red", "silver", "blue", "orange", "brown", "green"])
            car_type = st.selectbox("Type de carrosserie", ["estate", "sedan", "suv", "hatchback", "subcompact", "coupe", "convertible", "van"])
            fuel = st.selectbox("Carburant", ["diesel", "petrol", "hybrid_petrol", "electro"])

        with sub_col2:
            mileage = st.number_input("Kilométrage", min_value=0, value=100000, step=1000)
            engine_power = st.number_input("Puissance du moteur (ch)", min_value=0, value=120, step=10)
            
        st.markdown("---")
        st.subheader("Équipements et options")
        
        # Utiliser des checkbox pour les options binaires (Oui/Non)
        # C'est plus intuitif pour l'utilisateur
        opt_col1, opt_col2, opt_col3 = st.columns(3)
        with opt_col1:
            private_parking_available = st.checkbox("Parking privé disponible", value=True)
            has_gps = st.checkbox("GPS intégré", value=True)
            has_air_conditioning = st.checkbox("Climatisation", value=True)

        with opt_col2:
            automatic_car = st.checkbox("Boîte automatique", value=False)
            has_getaround_connect = st.checkbox("GetAround Connect", value=True)
            has_speed_regulator = st.checkbox("Régulateur de vitesse", value=True)

        with opt_col3:
            winter_tires = st.checkbox("Pneus hiver", value=False)


        # Bouton de soumission du formulaire
        submitted = st.form_submit_button("Lancer la Prédiction ✨")

# ==============================================================================
# --- COLONNE DE DROITE : Affichage du Résultat ---
# ==============================================================================
with col_result:
    st.header("Résultat de la prédiction")

    if submitted:
        # Afficher un message d'attente pendant l'appel à l'API
        with st.spinner("Analyse des données et calcul en cours..."):
            
            # Conversion des booléens (True/False) des checkbox en entiers (1/0) pour l'API
            data = {
                "model_key": model_key,
                "mileage": mileage,
                "engine_power": engine_power,
                "fuel": fuel,
                "paint_color": paint_color,
                "car_type": car_type,
                "private_parking_available": 1 if private_parking_available else 0,
                "has_gps": 1 if has_gps else 0,
                "has_air_conditioning": 1 if has_air_conditioning else 0,
                "automatic_car": 1 if automatic_car else 0,
                "has_getaround_connect": 1 if has_getaround_connect else 0,
                "has_speed_regulator": 1 if has_speed_regulator else 0,
                "winter_tires": 1 if winter_tires else 0
            }

            try:
                # Envoyer la requête POST à l'API FastAPI
                response = requests.post(API_URL, json=data, timeout=30)
                response.raise_for_status()  # Lève une exception si le statut est une erreur (4xx ou 5xx)

                # Extraire la prédiction
                prediction_data = response.json()
                price = prediction_data.get("prediction")

                # Afficher le résultat de manière claire et visible
                st.metric(
                    label="Prix journalier recommandé",
                    value=f"{price:.2f} €",
                    delta="Basé sur le modèle XGBoost",
                    delta_color="off"
                )
                
                st.success("Prédiction calculée avec succès !")
                
                # Pour le débogage, on peut aussi afficher la réponse brute
                with st.expander("Voir la réponse brute de l'API"):
                    st.json(prediction_data)

            except requests.exceptions.HTTPError as err:
                st.error(f"Erreur HTTP de l'API : {err.response.status_code}")
                st.warning("Veuillez vérifier les logs de l'API sur Hugging Face pour plus de détails.")
                st.json(err.response.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion à l'API : {e}")
                st.warning("L'API est peut-être en cours de redémarrage. Veuillez réessayer dans un instant.")

    else:
        # Message par défaut quand rien n'a encore été soumis
        st.info("Veuillez remplir le formulaire et cliquer sur 'Lancer la Prédiction' pour voir le résultat.")